#!/usr/bin/env python3
"""Download, convert and lay out the PP-OCRv3 ONNX assets of every language flavor.

Run it from any directory before building, for example:

    python -I scripts/prepare_ppocrv3_assets.py --profile all --slim

Downloads, extracted archives and converted models are cached under --cache-dir. A cached
download is reused only when its SHA-256 matches libs/ppocr-android-sdk/models.provenance.json,
and a fresh download that does not match the record fails the run. Pass --update-provenance
after an intentional source or converter change to rewrite the record instead.

paddle2onnx and onnxruntime run from a pinned virtual environment inside the cache directory
(created on first use), so the conversion does not depend on the packages of this interpreter.
"""

import argparse
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
import urllib.request
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
PROVENANCE_PATH = REPO_ROOT / "libs" / "ppocr-android-sdk" / "models.provenance.json"
ONNX_TOOLS = Path(__file__).resolve().parent / "ppocrv3_onnx_tools.py"

PADDLEOCR_BOS_BASE = "https://paddleocr.bj.bcebos.com"
PADDLEOCR_TAG = "v2.7.0"
PADDLEOCR_RAW_BASE = f"https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/{PADDLEOCR_TAG}"

SETUPTOOLS_VERSION = "84.2.1"
PADDLEPADDLE_VERSION = "3.2.1"
PADDLE2ONNX_VERSION = "1.3.1"
ONNXRUNTIME_VERSION = "1.21.1"
ONNX_VERSION = "1.23.2"
OPSET_VERSION = 7

CONVERTER_REQUIREMENTS = (
    # Python 3.12 venvs have no setuptools, and importing paddle needs it.
    f"setuptools=={SETUPTOOLS_VERSION}",
    f"paddlepaddle=={PADDLEPADDLE_VERSION}",
    f"paddle2onnx=={PADDLE2ONNX_VERSION}",
    f"onnxruntime=={ONNXRUNTIME_VERSION}",
    f"onnx=={ONNX_VERSION}",
    # Only the desktop slim precheck (ppocrv3_onnx_tools.py compare-slim) decodes images.
    "opencv-python-headless",
)

MODELS = {
    "ch_PP-OCRv3_det": f"{PADDLEOCR_BOS_BASE}/PP-OCRv3/chinese/ch_PP-OCRv3_det_infer.tar",
    "en_PP-OCRv3_det": f"{PADDLEOCR_BOS_BASE}/PP-OCRv3/english/en_PP-OCRv3_det_infer.tar",
    "Multilingual_PP-OCRv3_det": f"{PADDLEOCR_BOS_BASE}/PP-OCRv3/multilingual/Multilingual_PP-OCRv3_det_infer.tar",
    "ch_PP-OCRv3_rec": f"{PADDLEOCR_BOS_BASE}/PP-OCRv3/chinese/ch_PP-OCRv3_rec_infer.tar",
    "en_PP-OCRv3_rec": f"{PADDLEOCR_BOS_BASE}/PP-OCRv3/english/en_PP-OCRv3_rec_infer.tar",
    "chinese_cht_PP-OCRv3_rec": f"{PADDLEOCR_BOS_BASE}/PP-OCRv3/multilingual/chinese_cht_PP-OCRv3_rec_infer.tar",
    "japan_PP-OCRv3_rec": f"{PADDLEOCR_BOS_BASE}/PP-OCRv3/multilingual/japan_PP-OCRv3_rec_infer.tar",
    "korean_PP-OCRv3_rec": f"{PADDLEOCR_BOS_BASE}/PP-OCRv3/multilingual/korean_PP-OCRv3_rec_infer.tar",
    "ch_ppocr_mobile_v2.0_cls": f"{PADDLEOCR_BOS_BASE}/dygraph_v2.0/ch/ch_ppocr_mobile_v2.0_cls_infer.tar",
}

DICTS = {
    "ppocr_keys_v1": f"{PADDLEOCR_RAW_BASE}/ppocr/utils/ppocr_keys_v1.txt",
    "en_dict": f"{PADDLEOCR_RAW_BASE}/ppocr/utils/en_dict.txt",
    "chinese_cht_dict": f"{PADDLEOCR_RAW_BASE}/ppocr/utils/dict/chinese_cht_dict.txt",
    "japan_dict": f"{PADDLEOCR_RAW_BASE}/ppocr/utils/dict/japan_dict.txt",
    "korean_dict": f"{PADDLEOCR_RAW_BASE}/ppocr/utils/dict/korean_dict.txt",
}

CLS_MODEL = "ch_ppocr_mobile_v2.0_cls"
DET_MODELS = {name for name in MODELS if name.endswith("_det")}

# Keys are the Gradle flavor names; modelProfile is the capability value the plugin declares.
PROFILES = {
    "zh": {"modelProfile": "zh", "det": "ch_PP-OCRv3_det", "rec": "ch_PP-OCRv3_rec", "dict": "ppocr_keys_v1"},
    "en": {"modelProfile": "en", "det": "en_PP-OCRv3_det", "rec": "en_PP-OCRv3_rec", "dict": "en_dict"},
    "zhHant": {"modelProfile": "zh-hant", "det": "Multilingual_PP-OCRv3_det", "rec": "chinese_cht_PP-OCRv3_rec", "dict": "chinese_cht_dict"},
    "ja": {"modelProfile": "ja", "det": "Multilingual_PP-OCRv3_det", "rec": "japan_PP-OCRv3_rec", "dict": "japan_dict"},
    "ko": {"modelProfile": "ko", "det": "Multilingual_PP-OCRv3_det", "rec": "korean_PP-OCRv3_rec", "dict": "korean_dict"},
}

ASSET_DIR = "models/ppocrv3"
SLIM_ASSET_DIR = "models/ppocrv3-slim"
SLIM_KINDS = ("det", "rec")


class ProvenanceMismatch(RuntimeError):
    pass


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_record(path: Path) -> dict:
    return {"bytes": path.stat().st_size, "sha256": sha256_of(path)}


def load_provenance() -> dict:
    if PROVENANCE_PATH.is_file():
        return json.loads(PROVENANCE_PATH.read_text("utf-8"))
    return {}


class Recorder:
    """Compares every produced file with the committed provenance and collects the new record."""

    def __init__(self, previous: dict, update: bool):
        self.previous = previous
        self.update = update
        self.sources: dict[str, dict] = {}
        self.models: dict[str, dict] = {}
        self.dictionaries: dict[str, dict] = {}
        self.profiles: dict[str, dict] = {}
        self.warnings: list[str] = []

    def expected_source(self, name: str) -> dict | None:
        return self.previous.get("sources", {}).get(name)

    def expected_model(self, name: str, variant: str) -> dict | None:
        return self.previous.get("models", {}).get(name, {}).get(variant)

    def check_source(self, name: str, url: str, path: Path) -> None:
        record = file_record(path)
        expected = self.expected_source(name)
        if expected is not None and expected.get("sha256") != record["sha256"] and not self.update:
            raise ProvenanceMismatch(
                f"{name}: downloaded {path.name} has SHA-256 {record['sha256']}, "
                f"provenance records {expected.get('sha256')}"
            )
        self.sources[name] = {"file": path.name, "url": url, **record}

    def check_model(self, name: str, variant: str, path: Path, details: dict) -> None:
        record = file_record(path)
        expected = self.expected_model(name, variant)
        if expected is not None and expected.get("sha256") != record["sha256"]:
            # Converter output is not guaranteed to be byte-identical across platforms, so a
            # different digest is reported but does not fail the run; the source archives are
            # the integrity boundary.
            self.warnings.append(
                f"{name} ({variant}) SHA-256 {record['sha256']} differs from provenance "
                f"{expected.get('sha256')}"
            )
        self.models.setdefault(name, {})[variant] = {**record, **details}


def download(url: str, target: Path, expected: dict | None) -> Path:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.is_file() and target.stat().st_size > 0:
        if expected is None or sha256_of(target) == expected.get("sha256"):
            print(f"reuse: {target}", flush=True)
            return target
        print(f"cached file does not match provenance, download again: {target}", flush=True)

    partial = target.with_name(target.name + ".part")
    print(f"download: {url}", flush=True)
    with urllib.request.urlopen(url, timeout=120) as response, partial.open("wb") as output:
        shutil.copyfileobj(response, output, 1 << 20)
    partial.replace(target)
    return target


def safe_extract_tar(tar_path: Path, out_dir: Path) -> Path:
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)

    out_root = out_dir.resolve()
    with tarfile.open(tar_path) as archive:
        for member in archive.getmembers():
            target = (out_dir / member.name).resolve()
            if target != out_root and out_root not in target.parents:
                raise RuntimeError(f"unsafe tar member: {member.name}")
            if not (member.isfile() or member.isdir()):
                raise RuntimeError(f"unexpected tar member type: {member.name}")
        archive.extractall(out_dir, filter="data")

    model_file = next(out_dir.rglob("inference.pdmodel"), None)
    if model_file is None or not (model_file.parent / "inference.pdiparams").is_file():
        raise FileNotFoundError(f"inference.pdmodel / inference.pdiparams not found in {tar_path}")
    return model_file.parent


def venv_executable(venv_dir: Path, name: str) -> Path:
    if os.name == "nt":
        return venv_dir / "Scripts" / f"{name}.exe"
    return venv_dir / "bin" / name


def run_command(cmd: list, cwd: Path | None = None, capture: bool = False) -> str:
    print("run:", " ".join(str(part) for part in cmd), flush=True)
    completed = subprocess.run(
        [str(part) for part in cmd],
        cwd=cwd,
        check=True,
        stdout=subprocess.PIPE if capture else None,
        text=True,
        encoding="utf-8",
    )
    return completed.stdout or ""


class Converter:
    def __init__(self, cache_dir: Path):
        self.venv_dir = cache_dir / f"paddle2onnx-{PADDLE2ONNX_VERSION}-venv"
        self.python = venv_executable(self.venv_dir, "python")
        self.paddle2onnx = venv_executable(self.venv_dir, "paddle2onnx")
        self._versions: dict | None = None

    def ensure(self) -> None:
        if self.python.is_file() and self.paddle2onnx.is_file():
            versions = self.versions()
            if (
                versions.get("paddle2onnx") == PADDLE2ONNX_VERSION
                and versions.get("onnxruntime") == ONNXRUNTIME_VERSION
                and versions.get("onnx") == ONNX_VERSION
            ):
                return
            self._versions = None
        print(f"prepare converter: {self.venv_dir}", flush=True)
        run_command([sys.executable, "-m", "venv", self.venv_dir])
        run_command([self.python, "-m", "pip", "install", "--upgrade", "pip"])
        run_command([self.python, "-m", "pip", "install", *CONVERTER_REQUIREMENTS])

    def tools(self, *args) -> dict:
        output = run_command([self.python, "-I", ONNX_TOOLS, *args], cwd=self.venv_dir, capture=True)
        return json.loads(output.strip().splitlines()[-1])

    def versions(self) -> dict:
        if self._versions is None:
            self._versions = self.tools("versions")
        return self._versions

    def convert(self, model_dir: Path, target: Path) -> None:
        staging = target.parent / "staging"
        if staging.exists():
            shutil.rmtree(staging)
        staging.mkdir(parents=True)
        run_command(
            [
                self.paddle2onnx,
                "--model_dir", model_dir,
                "--model_filename", "inference.pdmodel",
                "--params_filename", "inference.pdiparams",
                "--save_file", staging / "inference.onnx",
                "--opset_version", str(OPSET_VERSION),
            ],
            cwd=self.venv_dir,
        )
        produced = staging / "inference.onnx"
        if not produced.is_file() or produced.stat().st_size == 0:
            raise RuntimeError(f"paddle2onnx produced no model for {model_dir}")
        produced.replace(target)
        shutil.rmtree(staging)


def prepare_model(name: str, cache_dir: Path, converter: Converter, recorder: Recorder, slim: bool) -> dict[str, Path]:
    url = MODELS[name]
    tar_path = cache_dir / "downloads" / url.rsplit("/", 1)[-1]
    fp32 = cache_dir / "onnx" / name / "inference.onnx"
    fp32.parent.mkdir(parents=True, exist_ok=True)

    expected_fp32 = recorder.expected_model(name, "fp32")
    cached = fp32.is_file() and (expected_fp32 is None or sha256_of(fp32) == expected_fp32.get("sha256"))
    download(url, tar_path, recorder.expected_source(name))
    recorder.check_source(name, url, tar_path)
    if cached:
        print(f"reuse converted: {fp32}", flush=True)
    else:
        model_dir = safe_extract_tar(tar_path, cache_dir / "extracted" / name)
        converter.convert(model_dir, fp32)
    details = converter.tools("inspect", fp32)
    if name in DET_MODELS and not dynamic_hw(details):
        # The Multilingual det archive declares a fixed 960 x 960 input; the plugin feeds any size.
        converter.tools("dynamic-hw", fp32, fp32)
        details = converter.tools("inspect", fp32)
        if not dynamic_hw(details):
            raise RuntimeError(f"{name}: det input height and width are still fixed")
    recorder.check_model(name, "fp32", fp32, details)
    outputs = {"fp32": fp32}

    if slim:
        # Quantizing takes seconds, so the slim model is always rebuilt from the current fp32 one.
        slim_path = cache_dir / "onnx-slim" / name / "inference.onnx"
        slim_path.parent.mkdir(parents=True, exist_ok=True)
        converter.tools("quantize", fp32, slim_path)
        recorder.check_model(name, "slim", slim_path, converter.tools("inspect", slim_path))
        outputs["slim"] = slim_path
    return outputs


def dynamic_hw(details: dict) -> bool:
    return all(not isinstance(item["shape"][dim], int) for item in details["inputs"] for dim in (2, 3))


def prepare_dict(name: str, cache_dir: Path, recorder: Recorder) -> list[str]:
    url = DICTS[name]
    path = download(url, cache_dir / "downloads" / "dict" / f"{name}.txt", recorder.expected_source(name))
    recorder.check_source(name, url, path)
    lines = path.read_text("utf-8").replace("\r\n", "\n").replace("\r", "\n").split("\n")
    entries = [line for line in lines if line != ""]
    if not entries:
        raise RuntimeError(f"empty dictionary: {path}")
    # PP-OCRv3 rec models are trained with use_space_char, which appends a space class even when
    # the dictionary already ends with one (en, chinese_cht, japan and korean do); the duplicate
    # label maps to the appended class. inference.yml lists that exact class order.
    chars = [*entries, " "]
    recorder.dictionaries[name] = {"source": name, "entries": len(entries), "characterDict": len(chars)}
    return chars


def yaml_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def write_inference_yml(chars: list[str], target: Path) -> None:
    lines = [
        "PostProcess:",
        "  name: CTCLabelDecode",
        "  character_dict:",
    ]
    lines.extend(f"    - {yaml_quote(ch)}" for ch in chars)
    target.write_text("\n".join(lines) + "\n", "utf-8", newline="\n")


def check_rec_classes(profile: str, chars: list[str], rec_details: dict) -> None:
    # CTCLabelDecode prepends the blank label to character_dict.
    expected = len(chars) + 1
    classes = rec_details["outputs"][0]["shape"][-1]
    if classes != expected:
        raise RuntimeError(f"{profile}: rec model predicts {classes} classes, dictionary implies {expected}")


def install(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.is_file() and target.stat().st_size == source.stat().st_size and sha256_of(target) == sha256_of(source):
        return
    shutil.copyfile(source, target)


def prepare_profile(
    flavor: str,
    assets_root: Path,
    models: dict[str, dict[str, Path]],
    chars: list[str],
    recorder: Recorder,
    slim: bool,
) -> None:
    spec = PROFILES[flavor]
    flavor_assets = assets_root / flavor / "assets"
    base = flavor_assets / ASSET_DIR

    check_rec_classes(flavor, chars, recorder.models[spec["rec"]]["fp32"])
    install(models[spec["det"]]["fp32"], base / "det" / "inference.onnx")
    install(models[spec["rec"]]["fp32"], base / "rec" / "inference.onnx")
    install(models[CLS_MODEL]["fp32"], base / "cls" / "inference.onnx")
    write_inference_yml(chars, base / "rec" / "inference.yml")

    slim_root = flavor_assets / SLIM_ASSET_DIR
    if slim:
        for kind in SLIM_KINDS:
            install(models[spec[kind]]["slim"], slim_root / kind / "inference.onnx")

    assets = {}
    for path in sorted(p for p in flavor_assets.rglob("*") if p.is_file()):
        relative = path.relative_to(flavor_assets).as_posix()
        if relative.startswith(f"{SLIM_ASSET_DIR}/") and not slim:
            continue
        assets[relative] = file_record(path)
    recorder.profiles[flavor] = {
        "modelProfile": spec["modelProfile"],
        "det": spec["det"],
        "rec": spec["rec"],
        "cls": CLS_MODEL,
        "dict": spec["dict"],
        "assets": assets,
    }
    total = sum(record["bytes"] for record in assets.values())
    print(f"prepared: {flavor} ({len(assets)} files, {total} bytes)", flush=True)


def build_provenance(previous: dict, recorder: Recorder, converter: Converter, slim: bool) -> dict:
    versions = converter.versions()
    merged = {
        "sources": {**previous.get("sources", {}), **recorder.sources},
        "models": {**previous.get("models", {})},
        "dictionaries": {**previous.get("dictionaries", {}), **recorder.dictionaries},
        "profiles": {**previous.get("profiles", {}), **recorder.profiles},
    }
    for name, variants in recorder.models.items():
        merged["models"][name] = {**merged["models"].get(name, {}), **variants}

    return {
        "project": "PaddlePaddle/PaddleOCR",
        "scope": (
            "PP-OCRv3 mobile detection and recognition models of the zh, en, zh-hant, ja and ko "
            "flavors, the PP-OCR mobile v2.0 text line orientation classifier and the recognition "
            "dictionaries, converted from the official Paddle inference archives to ONNX and "
            "bundled as Android assets under app/src/<flavor>/assets/models/."
        ),
        "license": "Apache-2.0",
        "license_url": f"https://github.com/PaddlePaddle/PaddleOCR/blob/{PADDLEOCR_TAG}/LICENSE",
        "dictionary_ref": PADDLEOCR_TAG,
        "verified_date": datetime.date.today().isoformat(),
        "generator": "scripts/prepare_ppocrv3_assets.py",
        "converter": {
            "paddlepaddle": versions.get("paddle"),
            "paddle2onnx": versions.get("paddle2onnx"),
            "command": (
                "paddle2onnx --model_dir <extracted archive> --model_filename inference.pdmodel "
                f"--params_filename inference.pdiparams --save_file inference.onnx --opset_version {OPSET_VERSION}"
            ),
        },
        "quantization": {
            "onnxruntime": versions.get("onnxruntime"),
            "onnx": versions.get("onnx"),
            "numpy": versions.get("numpy"),
            "function": "onnxruntime.quantization.quantize_dynamic",
            "parameters": versions.get("quantize_parameters"),
            "models": list(SLIM_KINDS),
            "output_dir": SLIM_ASSET_DIR,
        },
        "notes": [
            "Archives and dictionaries are the integrity boundary: a download whose SHA-256 differs from this record fails prepare_ppocrv3_assets.py.",
            "Converted and quantized models are recorded for reference; converter output on another platform may differ byte-wise and is reported as a warning.",
            "The classifier is shared by every flavor and is not quantized.",
            "paddle2onnx raises --opset_version 7 to the lowest opset the graph needs; the actual opset of every model is recorded below.",
            "Det inputs with a fixed height and width (Multilingual_PP-OCRv3_det declares 960 x 960) are made dynamic by ppocrv3_onnx_tools.py dynamic-hw.",
            "Every det Conv has fewer weights than the quantization threshold, so the slim det is the fp32 det with BatchNormalization folded.",
        ],
        **merged,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--profile", choices=[*PROFILES.keys(), "all"], default="zh")
    parser.add_argument("--slim", action="store_true", help="Also write the dynamically quantized det / rec models.")
    parser.add_argument(
        "--cache-dir",
        default=os.environ.get("PPOCRV3_ASSETS_CACHE", str(REPO_ROOT / ".cache" / "ppocrv3")),
        help="Download, conversion and converter environment cache (default: $PPOCRV3_ASSETS_CACHE or .cache/ppocrv3).",
    )
    parser.add_argument(
        "--assets-root",
        default=str(REPO_ROOT / "app" / "src"),
        help="Directory that holds the <flavor>/assets source sets (default: app/src).",
    )
    parser.add_argument(
        "--update-provenance",
        action="store_true",
        help="Accept new source digests and rewrite libs/ppocr-android-sdk/models.provenance.json.",
    )
    args = parser.parse_args()

    cache_dir = Path(args.cache_dir).resolve()
    assets_root = Path(args.assets_root).resolve()
    flavors = list(PROFILES.keys()) if args.profile == "all" else [args.profile]

    previous = load_provenance()
    recorder = Recorder(previous, args.update_provenance)
    converter = Converter(cache_dir)
    converter.ensure()

    model_names = sorted({PROFILES[f][kind] for f in flavors for kind in ("det", "rec")} | {CLS_MODEL})
    try:
        models = {
            name: prepare_model(name, cache_dir, converter, recorder, args.slim and name != CLS_MODEL)
            for name in model_names
        }
        dicts = {name: prepare_dict(name, cache_dir, recorder) for name in sorted({PROFILES[f]["dict"] for f in flavors})}
        for flavor in flavors:
            prepare_profile(flavor, assets_root, models, dicts[PROFILES[flavor]["dict"]], recorder, args.slim)
    except ProvenanceMismatch as error:
        print(f"error: {error}", file=sys.stderr)
        print("Rerun with --update-provenance only after confirming the new upstream file.", file=sys.stderr)
        return 1

    for warning in recorder.warnings:
        print(f"warning: {warning}", flush=True)

    if args.update_provenance or not previous:
        provenance = build_provenance(previous, recorder, converter, args.slim)
        PROVENANCE_PATH.parent.mkdir(parents=True, exist_ok=True)
        PROVENANCE_PATH.write_text(json.dumps(provenance, indent=2, ensure_ascii=False) + "\n", "utf-8", newline="\n")
        print(f"provenance written: {PROVENANCE_PATH}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
