#!/usr/bin/env python3
"""Render the per-flavor OCR sample images used by the instrumentation tests.

The images are committed, so CI does not need the fonts. Re-run only when the sample
text changes; the fonts below ship with Windows, pass --fonts-dir elsewhere. Pillow only draws
the scripts that need no text shaping, so the others are rendered by headless Microsoft Edge.

Output: app/src/androidTest/assets/samples/<flavor>.png, zh-rotated.png (the zh sample
turned 180 degrees, for the text line orientation classifier) and samples.json, which lists
the expected lines of every image.

Usage:
  python -I scripts/generate_ocr_samples.py [--fonts-dir C:/Windows/Fonts]
"""

import argparse
import html
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from PIL import Image, ImageChops, ImageDraw, ImageFont

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPO_ROOT / "app" / "src" / "androidTest" / "assets" / "samples"
EDGE = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")

SAMPLES = {
    "zh": {"font": "msyh.ttc", "lines": ["欢迎使用文字识别插件", "今天的天气非常好"]},
    "en": {"font": "arial.ttf", "lines": ["Hello AutoJs6 Plugin", "Optical Character Recognition"]},
    "zhHant": {"font": "msjh.ttc", "lines": ["歡迎使用文字識別插件", "繁體中文測試成功"]},
    "ja": {"font": "YuGothM.ttc", "lines": ["日本語の文字認識", "こんにちは世界"]},
    "ko": {"font": "malgun.ttf", "lines": ["한국어 문자 인식", "안녕하세요 세계"]},
}

# flavor -> html lang, text direction, font family, expected lines in logical order. The
# Devanagari, Telugu, Kannada and Tamil lines avoid conjuncts: the models read those poorly, and
# these samples check the pipeline, not accuracy.
SHAPED_SAMPLES = {
    "latin": {"lang": "fr", "dir": "ltr", "font": "Segoe UI", "lines": ["Reconnaissance de caractères", "Schöne Grüße aus München"]},
    "arabic": {"lang": "ar", "dir": "rtl", "font": "Segoe UI", "lines": ["التعرف على النصوص", "مرحبا بالعالم"]},
    "cyrillic": {"lang": "ru", "dir": "ltr", "font": "Segoe UI", "lines": ["Распознавание текста", "Привет мир"]},
    "devanagari": {"lang": "hi", "dir": "ltr", "font": "Nirmala UI", "lines": ["पाठ की पहचान", "भारत देश महान"]},
    "te": {"lang": "te", "dir": "ltr", "font": "Nirmala UI", "lines": ["మన దేశం", "తెలుగు భాష"]},
    "ka": {"lang": "kn", "dir": "ltr", "font": "Nirmala UI", "lines": ["ಬೆಂಗಳೂರು ನಗರ", "ರಾಮನು ಕಾಡಿಗೆ ಹೋದನು"]},
    "ta": {"lang": "ta", "dir": "ltr", "font": "Nirmala UI", "lines": ["வணக்கம் உலகம்", "பள்ளி மாணவர்கள் படிக்கிறார்கள்"]},
}

FONT_SIZE = 40
PADDING = 32
LINE_GAP = 28


def render(lines: list[str], font: ImageFont.FreeTypeFont) -> Image.Image:
    boxes = [font.getbbox(line) for line in lines]
    width = max(box[2] - box[0] for box in boxes) + PADDING * 2
    height = sum(box[3] - box[1] for box in boxes) + LINE_GAP * (len(lines) - 1) + PADDING * 2
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    y = PADDING
    for line, box in zip(lines, boxes):
        draw.text((PADDING - box[0], y - box[1]), line, fill="black", font=font)
        y += box[3] - box[1] + LINE_GAP
    return image


def render_shaped(sample: dict, target: Path) -> None:
    body = "".join(f"<p>{html.escape(line)}</p>" for line in sample["lines"])
    page = (
        f'<!doctype html><html lang="{sample["lang"]}" dir="{sample["dir"]}"><meta charset="utf-8">'
        f"<style>html, body {{ margin: 0; background: white; }} body {{ padding: {PADDING * 2}px; }}"
        f"p {{ margin: 0 0 {LINE_GAP}px; color: black; font: {FONT_SIZE}px '{sample['font']}'; white-space: nowrap; }}</style>"
        f"<body>{body}</body></html>"
    )
    with tempfile.TemporaryDirectory() as directory:
        source = Path(directory) / "sample.html"
        source.write_text(page, "utf-8")
        shot = Path(directory) / "sample.png"
        subprocess.run(
            [str(EDGE), "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
             f"--user-data-dir={Path(directory) / 'profile'}", "--force-device-scale-factor=1",
             "--window-size=1000,400", f"--screenshot={shot}", source.as_uri()],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120,
        )
        image = Image.open(shot).convert("RGB")
        box = ImageChops.difference(image, Image.new("RGB", image.size, "white")).getbbox()
        margin = (box[0] - PADDING, box[1] - PADDING, box[2] + PADDING, box[3] + PADDING)
        image.crop(margin).save(target, optimize=True)
        image.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--fonts-dir", type=Path, default=Path("C:/Windows/Fonts"))
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for flavor, sample in SAMPLES.items():
        font = ImageFont.truetype(str(args.fonts_dir / sample["font"]), FONT_SIZE)
        image = render(sample["lines"], font)
        image.save(OUTPUT_DIR / f"{flavor}.png", optimize=True)
        manifest[flavor] = {"file": f"{flavor}.png", "lines": sample["lines"]}
        if flavor == "zh":
            image.rotate(180).save(OUTPUT_DIR / "zh-rotated.png", optimize=True)
            manifest["zh-rotated"] = {"file": "zh-rotated.png", "lines": sample["lines"], "rotated": True}
    for flavor, sample in SHAPED_SAMPLES.items():
        render_shaped(sample, OUTPUT_DIR / f"{flavor}.png")
        manifest[flavor] = {"file": f"{flavor}.png", "lines": sample["lines"]}
    (OUTPUT_DIR / "samples.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", "utf-8", newline="\n")
    print(f"samples written: {OUTPUT_DIR.relative_to(REPO_ROOT).as_posix()} ({len(manifest)} images)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
