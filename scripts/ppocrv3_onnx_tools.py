#!/usr/bin/env python3
"""ONNX helpers for prepare_ppocrv3_assets.py, run inside its pinned converter environment.

Subcommands print one JSON object on the last line of stdout:

    versions                      package versions and the quantize_dynamic parameters
    inspect MODEL                 opset, input and output names and shapes
    dynamic-hw SOURCE TARGET      make the height and width of every input and output dynamic
    quantize SOURCE TARGET        dynamic int8 quantization of a det / rec model
    compare-slim --assets DIR --image PNG [--image PNG ...]
                                  desktop precheck of the fp32 and slim det / rec outputs

compare-slim is a coarse precheck only. It follows the PaddleOCR PP-OCRv3 pre- and
post-processing closely enough to compare the two model variants with each other; the
accuracy decision is made on devices with the Android pipeline.
"""

import argparse
import json
import math
import statistics
import sys
import time
from pathlib import Path


# Dynamically quantizing every Conv empties the zh rec output and drops multilingual det boxes:
# the small early (mostly depthwise) layers are the sensitive ones and hold few weights anyway.
CONV_MIN_WEIGHTS = 100000

QUANTIZE_PARAMETERS = {
    # paddle2onnx 1.3.1 stores weights as Constant nodes, which quantize_dynamic rejects; the
    # recommended pre-processing folds them into initializers (and fuses BatchNormalization).
    "pre_process": "onnxruntime.quantization.shape_inference.quant_pre_process(skip_symbolic_shape=True)",
    "weight_type": "QUInt8",
    "per_channel": False,
    "reduce_range": False,
    "op_types_to_quantize": "default (every operator type quantize_dynamic supports)",
    "nodes_to_exclude": f"Conv nodes whose weight initializer has fewer than {CONV_MIN_WEIGHTS} elements",
}


def versions() -> dict:
    import numpy
    import onnx
    import onnxruntime
    import paddle2onnx

    result = {
        "python": sys.version.split()[0],
        "paddle2onnx": paddle2onnx.__version__,
        "onnxruntime": onnxruntime.__version__,
        "onnx": onnx.__version__,
        "numpy": numpy.__version__,
        "quantize_parameters": QUANTIZE_PARAMETERS,
    }
    try:
        from importlib.metadata import version

        result["paddle"] = version("paddlepaddle")
    except Exception:
        result["paddle"] = None
    return result


def dims(value_info) -> list:
    shape = []
    for dim in value_info.type.tensor_type.shape.dim:
        if dim.HasField("dim_value"):
            shape.append(dim.dim_value)
        elif dim.HasField("dim_param"):
            shape.append(dim.dim_param)
        else:
            shape.append(None)
    return shape


def inspect(model_path: str) -> dict:
    import onnx

    model = onnx.load(model_path, load_external_data=False)
    initializers = {item.name for item in model.graph.initializer}
    opset = next((item.version for item in model.opset_import if item.domain in ("", "ai.onnx")), None)
    return {
        "opset": opset,
        "inputs": [{"name": item.name, "shape": dims(item)} for item in model.graph.input if item.name not in initializers],
        "outputs": [{"name": item.name, "shape": dims(item)} for item in model.graph.output],
    }


def dynamic_hw(source: str, target: str) -> dict:
    """The Multilingual det archive declares a fixed 960 x 960 input, which ONNX Runtime enforces.

    paddle2onnx.optimize --input_shape_dict writes -1 dim values and re-infers wrong static
    shapes, so the NCHW height and width are renamed to symbolic dims here and the stale
    intermediate shapes are dropped; the graph itself has no shape-dependent constants.
    """
    import onnx

    model = onnx.load(source)
    changed = []
    for kind, values in (("input", model.graph.input), ("output", model.graph.output)):
        for value in values:
            shape = value.type.tensor_type.shape.dim
            if len(shape) != 4:
                continue
            for index, axis in ((2, "height"), (3, "width")):
                if shape[index].HasField("dim_value"):
                    shape[index].ClearField("dim_value")
                    shape[index].dim_param = f"{kind}_{value.name}_{axis}"
                    changed.append(f"{kind}:{value.name}:{index}")
    del model.graph.value_info[:]
    onnx.checker.check_model(model)
    Path(target).parent.mkdir(parents=True, exist_ok=True)
    onnx.save(model, target)
    return {"source": source, "target": target, "changed": changed}


def quantize(source: str, target: str) -> dict:
    import onnx
    from onnxruntime.quantization import QuantType, quantize_dynamic
    from onnxruntime.quantization.shape_inference import quant_pre_process

    target_path = Path(target)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    preprocessed = target_path.with_name("preprocessed.onnx")
    try:
        # Symbolic shape inference cannot resolve the dynamic det / rec input sizes.
        quant_pre_process(source, str(preprocessed), skip_symbolic_shape=True)
        model = onnx.load(str(preprocessed))
        weights = {item.name: math.prod(item.dims) for item in model.graph.initializer}
        convs = [node for node in model.graph.node if node.op_type == "Conv"]
        excluded = [node.name for node in convs if weights.get(node.input[1], 0) < CONV_MIN_WEIGHTS]
        quantize_dynamic(
            model_input=str(preprocessed),
            model_output=target,
            weight_type=QuantType.QUInt8,
            per_channel=QUANTIZE_PARAMETERS["per_channel"],
            reduce_range=QUANTIZE_PARAMETERS["reduce_range"],
            nodes_to_exclude=excluded,
        )
    finally:
        preprocessed.unlink(missing_ok=True)
    return {"source": source, "target": target, "conv": len(convs), "conv_quantized": len(convs) - len(excluded)}


def read_dict(yml: Path) -> list[str]:
    chars = []
    for line in yml.read_text("utf-8").split("\n"):
        if line.startswith("    - '") and line.endswith("'"):
            chars.append(line[len("    - '"):-1].replace("''", "'"))
    return chars


def det_preprocess(image, limit_side_len: int = 960):
    import cv2
    import numpy as np

    height, width = image.shape[:2]
    ratio = 1.0
    if max(height, width) > limit_side_len:
        ratio = limit_side_len / max(height, width)
    resize_h = max(int(round(height * ratio / 32) * 32), 32)
    resize_w = max(int(round(width * ratio / 32) * 32), 32)
    resized = cv2.resize(image, (resize_w, resize_h))
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    data = (resized.astype(np.float32) / 255.0 - mean) / std
    return data.transpose(2, 0, 1)[None].astype(np.float32), resize_h / height, resize_w / width


def db_boxes(pred, scale_h: float, scale_w: float, thresh=0.3, box_thresh=0.5, unclip_ratio=1.6):
    import cv2
    import numpy as np

    prob = pred[0, 0]
    bitmap = (prob > thresh).astype(np.uint8)
    contours, _ = cv2.findContours(bitmap, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    boxes = []
    for contour in contours[:1000]:
        rect = cv2.minAreaRect(contour)
        if min(rect[1]) < 3:
            continue
        points = cv2.boxPoints(rect)
        mask = np.zeros_like(bitmap)
        cv2.fillPoly(mask, [points.astype(np.int32)], 1)
        if mask.sum() == 0 or float(prob[mask.astype(bool)].mean()) < box_thresh:
            continue
        (cx, cy), (w, h), angle = rect
        distance = w * h * unclip_ratio / (2 * (w + h))
        expanded = cv2.boxPoints(((cx, cy), (w + 2 * distance, h + 2 * distance), angle))
        if min(w + 2 * distance, h + 2 * distance) < 5:
            continue
        xs = expanded[:, 0] / scale_w
        ys = expanded[:, 1] / scale_h
        boxes.append((float(xs.min()), float(ys.min()), float(xs.max()), float(ys.max())))
    boxes.sort(key=lambda b: (round(b[1] / 10), b[0]))
    return boxes


def iou(a, b) -> float:
    ix = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = ix * iy
    union = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return inter / union if union > 0 else 0.0


def rec_preprocess(crop):
    import cv2
    import numpy as np

    height, width = crop.shape[:2]
    img_w = int(48 * max(320 / 48, width / height))
    resized_w = min(img_w, int(math.ceil(48 * width / height)))
    resized = cv2.resize(crop, (resized_w, 48)).astype(np.float32)
    resized = (resized / 255.0 - 0.5) / 0.5
    padded = np.zeros((48, img_w, 3), dtype=np.float32)
    padded[:, :resized_w] = resized
    return padded.transpose(2, 0, 1)[None]


def ctc_decode(pred, chars: list[str]) -> str:
    indices = pred[0].argmax(axis=1)
    text = []
    previous = -1
    for index in indices:
        if index != 0 and index != previous and index - 1 < len(chars):
            text.append(chars[index - 1])
        previous = index
    return "".join(text)


def edit_distance(a: str, b: str) -> int:
    previous = list(range(len(b) + 1))
    for i, char_a in enumerate(a, 1):
        current = [i]
        for j, char_b in enumerate(b, 1):
            current.append(min(previous[j] + 1, current[j - 1] + 1, previous[j - 1] + (char_a != char_b)))
        previous = current
    return previous[-1]


def timed_run(session, data, repeat: int):
    name = session.get_inputs()[0].name
    times = []
    output = None
    for _ in range(repeat):
        start = time.perf_counter()
        output = session.run(None, {name: data})[0]
        times.append((time.perf_counter() - start) * 1000)
    return output, statistics.median(times)


def compare_slim(assets: Path, image_paths: list[Path], repeat: int) -> dict:
    import cv2
    import numpy as np
    import onnxruntime as ort

    def session(path: Path):
        options = ort.SessionOptions()
        options.intra_op_num_threads = 4
        return ort.InferenceSession(str(path), options, providers=["CPUExecutionProvider"])

    fp32_root = assets / "models" / "ppocrv3"
    slim_root = assets / "models" / "ppocrv3-slim"
    det_sessions = {"fp32": session(fp32_root / "det" / "inference.onnx"), "slim": session(slim_root / "det" / "inference.onnx")}
    rec_sessions = {"fp32": session(fp32_root / "rec" / "inference.onnx"), "slim": session(slim_root / "rec" / "inference.onnx")}
    chars = read_dict(fp32_root / "rec" / "inference.yml")

    boxes_count = {"fp32": 0, "slim": 0}
    det_ms = {"fp32": 0.0, "slim": 0.0}
    rec_ms = {"fp32": 0.0, "slim": 0.0}
    best = []
    lines = same_text = fp32_chars = char_errors = 0
    for image_path in image_paths:
        image = cv2.imdecode(np.fromfile(str(image_path), dtype=np.uint8), cv2.IMREAD_COLOR)
        if image is None:
            raise RuntimeError(f"cannot decode {image_path}")
        det_input, scale_h, scale_w = det_preprocess(image)
        boxes = {}
        for variant, det_session in det_sessions.items():
            pred, median_ms = timed_run(det_session, det_input, repeat)
            boxes[variant] = db_boxes(pred, scale_h, scale_w)
            boxes_count[variant] += len(boxes[variant])
            det_ms[variant] += median_ms
        best += [max((iou(box, other) for other in boxes["slim"]), default=0.0) for box in boxes["fp32"]]

        # Both rec variants read the fp32 det boxes, so the comparison isolates the rec model.
        for x0, y0, x1, y1 in boxes["fp32"]:
            crop = image[max(0, int(y0)):int(math.ceil(y1)), max(0, int(x0)):int(math.ceil(x1))]
            if crop.size == 0:
                continue
            data = rec_preprocess(crop)
            texts = {}
            for variant, rec_session in rec_sessions.items():
                pred, median_ms = timed_run(rec_session, data, repeat)
                rec_ms[variant] += median_ms
                texts[variant] = ctc_decode(pred, chars)
            lines += 1
            same_text += int(texts["fp32"] == texts["slim"])
            fp32_chars += len(texts["fp32"])
            char_errors += edit_distance(texts["fp32"], texts["slim"])

    matched = [value for value in best if value >= 0.5]
    return {
        "images": len(image_paths),
        "det_boxes": boxes_count,
        "det_matched_iou_0_5": len(matched),
        "det_mean_best_iou": round(sum(best) / len(best), 4) if best else None,
        "det_min_best_iou": round(min(best), 4) if best else None,
        "det_total_median_ms": {variant: round(value, 2) for variant, value in det_ms.items()},
        "rec_lines": lines,
        "rec_same_text": same_text,
        "rec_fp32_chars": fp32_chars,
        "rec_char_agreement": round(1 - char_errors / fp32_chars, 4) if fp32_chars else None,
        "rec_total_median_ms": {variant: round(value, 2) for variant, value in rec_ms.items()},
        "repeat": repeat,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("versions")
    inspect_parser = commands.add_parser("inspect")
    inspect_parser.add_argument("model")
    dynamic_parser = commands.add_parser("dynamic-hw")
    dynamic_parser.add_argument("source")
    dynamic_parser.add_argument("target")
    quantize_parser = commands.add_parser("quantize")
    quantize_parser.add_argument("source")
    quantize_parser.add_argument("target")
    compare_parser = commands.add_parser("compare-slim")
    compare_parser.add_argument("--assets", required=True, help="app/src/<flavor>/assets")
    compare_parser.add_argument("--image", required=True, action="append", type=Path)
    compare_parser.add_argument("--repeat", type=int, default=5)
    args = parser.parse_args()

    if args.command == "versions":
        result = versions()
    elif args.command == "inspect":
        result = inspect(args.model)
    elif args.command == "dynamic-hw":
        result = dynamic_hw(args.source, args.target)
    elif args.command == "quantize":
        result = quantize(args.source, args.target)
    else:
        result = compare_slim(Path(args.assets), args.image, args.repeat)
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
