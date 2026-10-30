#!/usr/bin/env python3
"""Render the per-flavor OCR sample images used by the instrumentation tests.

The images are committed, so CI does not need the fonts. Re-run only when the sample
text changes; the fonts below ship with Windows, pass --fonts-dir elsewhere.

Output: app/src/androidTest/assets/samples/<flavor>.png, zh-rotated.png (the zh sample
turned 180 degrees, for the text line orientation classifier) and samples.json, which lists
the expected lines of every image.

Usage:
  python -I scripts/generate_ocr_samples.py [--fonts-dir C:/Windows/Fonts]
"""

import argparse
import json
from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPO_ROOT / "app" / "src" / "androidTest" / "assets" / "samples"

SAMPLES = {
    "zh": {"font": "msyh.ttc", "lines": ["欢迎使用文字识别插件", "今天的天气非常好"]},
    "en": {"font": "arial.ttf", "lines": ["Hello AutoJs6 Plugin", "Optical Character Recognition"]},
    "zhHant": {"font": "msjh.ttc", "lines": ["歡迎使用文字識別插件", "繁體中文測試成功"]},
    "ja": {"font": "YuGothM.ttc", "lines": ["日本語の文字認識", "こんにちは世界"]},
    "ko": {"font": "malgun.ttf", "lines": ["한국어 문자 인식", "안녕하세요 세계"]},
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
    (OUTPUT_DIR / "samples.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", "utf-8", newline="\n")
    print(f"samples written: {OUTPUT_DIR.relative_to(REPO_ROOT).as_posix()} ({len(manifest)} images)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
