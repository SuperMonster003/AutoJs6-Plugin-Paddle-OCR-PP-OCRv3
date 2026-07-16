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
    <a href="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/commit/6c83d3092ae569a4e84fad3a5e8cec99b5c65856"><img alt="Created" src="https://img.shields.io/date/1773538952?color=2e7d32&label=Created"/></a>
    <br>
    <a href="https://developer.android.com/studio/archive"><img alt="Android Studio" src="https://img.shields.io/badge/Android%20Studio-2023.3+-B64FC8"/></a>
    <a href="https://www.jetbrains.com/idea/download/other.html"><img alt="IntelliJ IDEA" src="https://img.shields.io/badge/IntelliJ%20IDEA-2023.3+-EE4677"/></a>
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

The AutoJs6 Paddle OCR (PP-OCRv3) plugin adds optical character recognition powered by PaddleOCR PP-OCRv3, with support for screenshots, local image files, and raw image input.

******

### Features

******

- Provides the `paddle-ocr-pp-ocrv3` plugin service, with plugin ID `paddle-ocr-pp-ocrv3`.
- Supports `ocr.paddle.recognizeText(image)` and `ocr.paddle.detect(image)` in AutoJs6.
- Supports screenshots, local image files, and raw ARGB_8888 image input.
- Plugin information, instructions, README, and CHANGELOG support Spanish/French/Russian/Arabic/Japanese/Korean/English/Simplified Chinese/Hong Kong Traditional Chinese/Taiwan Traditional Chinese.
- Based on PaddleOCR PP-OCRv3, Paddle Lite, and OpenCV 4.8.0.

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

******

### API Methods

******

Common OCR APIs include:

```text
ocr.paddle.recognizeText(image)
ocr.paddle.detect(image)
ocr.paddle(image)
ocr.paddle.recognizeText()
ocr.paddle()
```

`ocr.paddle()` recognizes the current screenshot by default, and `ocr.paddle(path)` recognizes a local image file.

******

### Release History

******

# v1.0.0

###### 2026/07/17

* `Feature` Paddle OCR (PP-OCRv3) plugin service, with plugin ID `paddle-ocr-pp-ocrv3`, engine `paddle-ocr`, and variant `v3`
* `Feature` Support discovering and invoking the plugin through `org.autojs.plugin.PADDLE_OCR`
* `Feature` Support `ocr.paddle.recognizeText(image)` text recognition and `ocr.paddle.detect(image)` text detection for screenshots, local image files, and raw ARGB_8888 image input
* `Feature` Bundle PaddleOCR PP-OCRv3 CPU models, running on Paddle Lite and OpenCV 4.8.0
* `Feature` Multilingual resources for plugin information, instructions, README, and CHANGELOG: Spanish/French/Russian/Arabic/Japanese/Korean/English/Simplified Chinese/Hong Kong Traditional Chinese/Taiwan Traditional Chinese
* `Improvement` Support ABI APK builds, including `arm64-v8a`/`armeabi-v7a` and `universal` packages
* `Improvement` Release APK filenames include project name, version number, and ABI variant

##### For more release history, see

* [CHANGELOG.md](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.changelog/CHANGELOG-en.md)

******

### Build

******

```powershell
.\gradlew.bat :app:assembleDebug
```

Release build:

```powershell
.\gradlew.bat :app:assembleRelease
```

Build parameters come from `version.properties`, with current min SDK 24 and target SDK 36.

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
- Paddle Lite official project: https://github.com/PaddlePaddle/Paddle-Lite
- OpenCV official website: https://opencv.org/
