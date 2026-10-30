<!--suppress HtmlDeprecatedAttribute, HttpUrlsUsage -->

<div align="center">
  <p>
    <picture>
      <img src="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/app/src/main/res/mipmap/ic_launcher.png?raw=true" alt="autojs6-plugin-paddle-ocr-pp-ocrv3-ic-launcher" border="0" width="128" />
    </picture>
  </p>

  <p>Paddle OCR PP-OCRv3 text recognition plugin for AutoJs6</p>

  <p>
    <a href="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/releases"><img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3?label=Release"/></a>
    <a href="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/issues"><img alt="GitHub closed issues" src="https://img.shields.io/github/issues/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3?color=A24232&label=Issues"/></a>
    <a href="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/LICENSE"><img alt="GitHub License" src="https://img.shields.io/github/license/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3?color=534BAE&label=License"/></a>
  </p>
</div>

******

### Languages

******

Current README.md supports the following languages:

- [简体中文 [zh-Hans]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-zh-Hans.md)
- [繁體中文 (香港) [zh-Hant-HK]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-zh-Hant-HK.md)
- [繁體中文 (台灣) [zh-Hant-TW]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-zh-Hant-TW.md)
- English [en] # current
- [Français [fr]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-fr.md)
- [Español [es]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-es.md)
- [日本語 [ja]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-ja.md)
- [한국어 [ko]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-ko.md)
- [Русский [ru]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-ru.md)
- [العربية [ar]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-ar.md)

******

### Introduction

******

The AutoJs6 Paddle OCR (PP-OCRv3) plugin adds optical character recognition powered by PaddleOCR PP-OCRv3 and ONNX Runtime, with support for screenshots, local image files, and raw image input. Since 2.0.0 it runs on ONNX Runtime instead of Paddle Lite, supports four ABIs, and comes as five language packages.

> **Paddle Lite edition**: the Paddle Lite implementation of 1.0.x is now published separately as [Paddle OCR (PP-OCRv3 Paddle Lite)](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3-Paddle-Lite) (plugin ID `paddle-ocr-pp-ocrv3-paddle-lite`, variant `v3-paddle-lite`). It supports only arm64-v8a and armeabi-v7a and can be installed alongside this plugin.

******

### Features

******

- Comes as five language packages: Simplified Chinese, English, Traditional Chinese, Japanese, and Korean. The Simplified Chinese package keeps the 1.0.x package name and plugin ID `paddle-ocr-pp-ocrv3`; every package uses engine `paddle-ocr` and variant `v3`.
- Supports `ocr.paddle.recognizeText(image)` and `ocr.paddle.detect(image)` in AutoJs6.
- Supports screenshots, local image files, and raw ARGB_8888 image input.
- Plugin information, instructions, README, and CHANGELOG support Spanish/French/Russian/Arabic/Japanese/Korean/English/Simplified Chinese/Hong Kong Traditional Chinese/Taiwan Traditional Chinese.
- Based on PaddleOCR PP-OCRv3, ONNX Runtime 1.21.1, and OpenCV 4.8.0, for four ABIs: arm64-v8a, armeabi-v7a, x86_64, and x86.
- `useSlim: true` uses detection and recognition models quantized to int8 with ONNX Runtime dynamic quantization.
- `useCls: true` checks the text direction before recognition so text rotated by 180 degrees can be read; it is off by default, as in 1.0.x.
- `useOpenCL` maps to NNAPI in the ONNX Runtime edition: on Android 8.1 (API 27) and later the NNAPI execution provider is used; on older versions, or when NNAPI fails to start, recognition falls back to the CPU. Whether it is faster depends on the device.
- Images may contain at most 16777216 pixels; raw image buffers are limited to 64 MiB
- Encoded image input is limited to 64 MiB and supports file descriptors and pipes

******

### Language packages

******

Each language package is a separate APK, and several can be installed at the same time:

| Language | `profile` | Plugin ID | Package name | APK file name |
| --- | --- | --- | --- | --- |
| Simplified Chinese | `zh` | `paddle-ocr-pp-ocrv3` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3` | `*-zh-<ABI>-*.apk` |
| English | `en` | `paddle-ocr-pp-ocrv3-en` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.en` | `*-en-<ABI>-*.apk` |
| Traditional Chinese | `zh-hant` | `paddle-ocr-pp-ocrv3-zh-hant` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.zhhant` | `*-zh-hant-<ABI>-*.apk` |
| Japanese | `ja` | `paddle-ocr-pp-ocrv3-ja` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.ja` | `*-ja-<ABI>-*.apk` |
| Korean | `ko` | `paddle-ocr-pp-ocrv3-ko` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.ko` | `*-ko-<ABI>-*.apk` |

Pick the package for the text you want to read: the Simplified Chinese package also reads English letters and digits and is the default recommendation; for Traditional Chinese, Japanese, or Korean text, install the matching package; for English-only text you can also install the English package. Each package comes as five APKs by ABI: `arm64-v8a` (most phones), `armeabi-v7a`, `x86_64`, `x86`, and `universal` (all four ABIs, the largest). Install only the one that matches your device.

******

### Usage

******

Recognize text content in a screenshot:

```js
let capt = images.captureScreen();
let texts = ocr.paddle.recognizeText(capt);
console.log(texts.join("\n"));
```

Recognize text content in a local image file, using `test.png` as an example:

```js
let img = images.read("test.png");
let results = ocr.paddle.detect(img);
console.log(results);
```

Shortcut forms are also available:

```js
ocr.paddle.recognizeText();
ocr.paddle("test.png");
```

Choose a language package and set recognition options:

```js
let img = images.read("test.png");
/* Use the Japanese package. */
ocr.paddle(img, { profile: "ja" });
/* Pick the Korean package by plugin ID. */
ocr.paddle(img, { engineId: "paddle-ocr-pp-ocrv3-ko" });
/* Use the quantized models and turn on text direction classification. */
ocr.paddle(img, { useSlim: true, useCls: true });
/* useOpenCL maps to NNAPI in the ONNX Runtime edition. */
ocr.paddle(img, { useOpenCL: true });
/* Use the Paddle Lite edition. */
ocr.paddle(img, { variant: "v3-paddle-lite" });
```

Choosing a package by `profile` and the `useCls` option need AutoJs6 6.8.0 or later. Older hosts do not choose by `profile` and do not pass `useCls` on; when several language packages are installed, use `engineId` to pick one.

******

### API Methods

******

Common OCR APIs include:

```text
ocr.paddle.recognizeText(image)
ocr.paddle.detect(image)
ocr.paddle(image)
ocr.paddle(image, options)
ocr.paddle.recognizeText()
ocr.paddle()
```

`ocr.paddle()` recognizes the current screenshot by default, and `ocr.paddle(path)` recognizes a local image file.

******

### Release History

******

# v2.0.0

###### 2026/10/30

* `Hint` Recognition now runs on ONNX Runtime instead of Paddle Lite, and the developer is now SuperMonster003. The previous Paddle Lite implementation is published separately as Paddle OCR (PP-OCRv3 Paddle Lite) (plugin ID `paddle-ocr-pp-ocrv3-paddle-lite`, variant `v3-paddle-lite`) and can be installed alongside this plugin. Versions 1.0.6 and earlier belong to that Paddle Lite plugin, which continues in its own repository
* `Hint` The plugin now comes as five language packages (Simplified Chinese, English, Traditional Chinese, Japanese, and Korean), each a separate APK; the Simplified Chinese package keeps the original package name and plugin ID
* `Hint` Choosing a package by `profile` and the `useCls` option need AutoJs6 6.8.0 or later; older hosts do not choose by `profile` and do not pass `useCls` on. This plugin declares host version code 5935 (AutoJs6 6.8.0) as its minimum
* `Feature` Support x86_64 and x86 devices, including emulators, for four ABIs in total
* `Feature` Add the `useCls` option, which checks the text direction before recognition so text rotated by 180 degrees can be read; it is off by default
* `Feature` `useOpenCL` maps to NNAPI in the ONNX Runtime edition: Android 8.1 and later use NNAPI, and older versions or devices where NNAPI is unavailable fall back to the CPU
* `Feature` Choose a language with `profile` (`zh`, `en`, `zh-hant`, `ja`, `ko`) and the Paddle Lite edition with `variant: "v3-paddle-lite"`; without them, the Simplified Chinese package is the default among the PP-OCRv3 plugins
* `Improvement` `useSlim` now uses detection and recognition models quantized to int8 with ONNX Runtime dynamic quantization
* `Dependency` Add ONNX Runtime Android 1.21.1 and remove Paddle Lite
* `Dependency` PaddleOCR PP-OCRv3 models are now in ONNX format, converted from the official inference models, with new English, Traditional Chinese, Japanese, and Korean recognition models and a text direction model
* `Dependency` OpenCV 4.8.0 is shipped again as the shared library libopencv_java4.so, one per ABI, as in the PP-OCRv4 plugin (1.0.6 linked it statically into libNative.so). Packaged applications take this library from the OpenCV plugin, not from this plugin: packaging with this plugin adds the OpenCV plugin automatically and fails if it is not installed

# v1.0.6

###### 2026/10/10

* `Hint` Packaged apps that use this version need AutoJs6 6.8.0 or later as the host; older hosts can package it only together with OpenCV
* `Fix` Native failures during model loading or inference aborted the plugin process; they are now reported to the host as errors
* `Improvement` libNative.so no longer exports OpenCV symbols and the APK no longer ships libopencv_java4.so, so it is smaller and packaged apps can use it alongside another OpenCV version
* `Dependency` Remove the OpenCV Android AAR 4.8.0; only the statically linked OpenCV Android SDK 4.8.0 remains, verified by SHA-256 when downloaded

# v1.0.5

###### 2026/10/05

* `Fix` SDK XML v4 parsing warnings with AGP 9.1 and APK native alignment checks incorrectly triggered by JVM unit-test assembly tasks, using shared build plugins 1.8.3
* `Improvement` Raise compileSdk and targetSdk to 37 (Android 17); the plugin's behavior does not depend on the new target
* `Improvement` Android App info icons share Icon Studio artwork and light/dark backgrounds while preserving transparent Plugin Center artwork and existing launcher choices

##### For more release history, see

* [CHANGELOG.md](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/app/src/main/assets/doc/CHANGELOG-en.md)

******

### Build

******

```powershell
python -I scripts\prepare_ppocrv3_assets.py --profile all --slim
.\gradlew.bat :app:assembleZhDebug
```

Release build:

```powershell
.\gradlew.bat :app:appendDigestToReleasedFiles
```

Build parameters come from `version.properties`, with current min SDK 24 and target SDK 37. ONNX models are not committed: before building, run `prepare_ppocrv3_assets.py` as shown above. It downloads the official PaddleOCR models, converts them to ONNX, and checks them against `libs/ppocr-android-sdk/models.provenance.json`; `--profile` accepts `zh`, `en`, `zhHant`, `ja`, `ko`, or `all`. Third-party components and licenses are listed in [THIRD_PARTY_NOTICES.md](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/THIRD_PARTY_NOTICES.md).

******

### Resource Layout

******

```text
.readme/lang_*.json
.changelog/lang_*.json
.python/generate_markdown.py
app/src/main/assets/doc/CHANGELOG*.md
app/src/main/res/values-*/strings.xml
app/src/main/res/raw-*/plugin_instruction.md
```

`strings.xml` provides localized plugin descriptions; `plugin_instruction.md` provides plugin instructions shown by the host. README and CHANGELOG are generated by `.python/generate_markdown.py` from JSON source files.

******

### Links

******

- AutoJs6 OCR docs: https://docs.autojs6.com/#/ocr
- PaddleOCR official project: https://github.com/PaddlePaddle/PaddleOCR
- ONNX Runtime official project: https://github.com/microsoft/onnxruntime
- OpenCV official website: https://opencv.org/
- Paddle OCR (PP-OCRv3 Paddle Lite) plugin: https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3-Paddle-Lite


[16 KB page alignment and build verification](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/docs/16kb.md)
