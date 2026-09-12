<!--suppress HtmlDeprecatedAttribute, HttpUrlsUsage -->

<div align="center">
  <p>
    <picture>
      <img src="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/app/src/main/res/mipmap/ic_launcher.png?raw=true" alt="autojs6-plugin-paddle-ocr-pp-ocrv3-ic-launcher" border="0" width="128" />
    </picture>
  </p>

  <p>用于 AutoJs6 的 Paddle OCR PP-OCRv3 文本识别插件</p>

  <p>
    <a href="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/releases"><img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3?label=Release"/></a>
    <a href="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/issues"><img alt="GitHub closed issues" src="https://img.shields.io/github/issues/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3?color=A24232&label=Issues"/></a>
    <a href="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/LICENSE"><img alt="GitHub License" src="https://img.shields.io/github/license/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3?color=534BAE&label=License"/></a>
  </p>
</div>

******

### 语言 (Languages)

******

当前 README.md 支持以下语言:

- 简体中文 [zh-Hans] # 当前
- [繁體中文 (香港) [zh-Hant-HK]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-zh-Hant-HK.md)
- [繁體中文 (台灣) [zh-Hant-TW]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-zh-Hant-TW.md)
- [English [en]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-en.md)
- [Français [fr]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-fr.md)
- [Español [es]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-es.md)
- [日本語 [ja]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-ja.md)
- [한국어 [ko]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-ko.md)
- [Русский [ru]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-ru.md)
- [العربية [ar]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-ar.md)

******

### 简介

******

AutoJs6 Paddle OCR (PP-OCRv3) 插件为 AutoJs6 提供基于 PaddleOCR PP-OCRv3 的光学字符识别能力, 支持截图, 本地图像文件和原始图像输入.

******

### 功能

******

- 提供 `paddle-ocr-pp-ocrv3` 插件服务, 插件 ID 为 `paddle-ocr-pp-ocrv3`.
- 支持 AutoJs6 中的 `ocr.paddle.recognizeText(image)` 和 `ocr.paddle.detect(image)`.
- 支持屏幕截图, 本地图像文件和原始 ARGB_8888 图像输入.
- 插件信息, 使用说明, README 与 CHANGELOG 均支持西班牙语/法语/俄语/阿拉伯语/日语/韩语/英语/简体中文/香港繁体/台湾繁体.
- 基于 PaddleOCR PP-OCRv3, Paddle Lite 和 OpenCV 4.8.0.

******

### 使用示例

******

识别屏幕截图中的文本内容:

```js
let capt = images.captureScreen();
let texts = ocr.paddle.recognizeText(capt);
console.log(texts.join("\n"));
```

识别本地图像文件中的文本内容, 以 `test.png` 为例:

```js
let img = images.read("test.png");
let results = ocr.paddle.detect(img);
console.log(results);
```

也可以使用简写形式:

```js
ocr.paddle.recognizeText();
ocr.paddle("test.png");
```

******

### 接口方法

******

常用 OCR 接口包括:

```text
ocr.paddle.recognizeText(image)
ocr.paddle.detect(image)
ocr.paddle(image)
ocr.paddle.recognizeText()
ocr.paddle()
```

`ocr.paddle()` 默认识别当前截图, `ocr.paddle(path)` 可识别本地图像文件.

******

### 发行历史

******

# v1.0.2

###### 2026/09/12

* `修复` Paddle OCR 原生依赖清理开关未初始化时 `clean` 任务执行失败
* `优化` 同步 OpenCV 4.8.0 原生库至 NDK r28c (Clang 19.0.1) 重编版本 (donor: AutoJs6-Plugin-OpenCV), 4 个 ABI 的 `libopencv_java4.so` 保持 16 KB `PT_LOAD` 对齐并附带 provenance 清单

# v1.0.1

###### 2026/09/11

* `优化` 构建阶段校验 64 位原生库的 16 KB 页大小对齐, 检查 manifest 契约并输出 JSON 报告

# v1.0.0

###### 2026/09/01

* `新增` Paddle OCR (PP-OCRv3) 插件服务, 插件 ID 为 `paddle-ocr-pp-ocrv3`, 引擎为 `paddle-ocr`, 变体为 `v3`
* `新增` 支持通过 `org.autojs.plugin.PADDLE_OCR` 发现并调用插件
* `新增` 支持 `ocr.paddle.recognizeText(image)` 文本识别和 `ocr.paddle.detect(image)` 文本检测, 覆盖截图, 本地图像文件和原始 ARGB_8888 图像输入
* `新增` 内置 PaddleOCR PP-OCRv3 CPU 模型, 基于 Paddle Lite 和 OpenCV 4.8.0 运行
* `新增` 插件信息, 使用说明, README 与 CHANGELOG 的多语言资源: 西班牙语/法语/俄语/阿拉伯语/日语/韩语/英语/简体中文/香港繁体/台湾繁体
* `优化` 支持按 ABI 构建 APK, 包括 `arm64-v8a`/`armeabi-v7a` 以及 `universal` 通用包
* `优化` 发布 APK 文件名包含项目名, 版本号和 ABI 变体
* `优化` 统一 README 版式与 Gradle 平台版本管理方式

##### 更多发行历史可参阅

* [CHANGELOG.md](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/app/src/main/assets/doc/CHANGELOG-zh-Hans.md)

******

### 构建

******

```powershell
.\gradlew.bat :app:assembleDebug
```

Release 构建:

```powershell
.\gradlew.bat :app:assembleRelease
```

构建参数来自 `version.properties`, 当前最低 SDK 为 24, 目标 SDK 为 36.

******

### 资源结构

******

```text
.readme/lang_*.json
.changelog/lang_*.json
.python/generate_markdown.py
app/src/main/assets/doc/CHANGELOG*.md
app/src/main/res/values-*/strings.xml
app/src/main/res/raw-*/plugin_instruction.md
```

`strings.xml` 提供插件描述本地化; `plugin_instruction.md` 提供宿主侧展示的插件使用说明. README 与 CHANGELOG 由 `.python/generate_markdown.py` 根据 JSON 源文件生成.

******

### 相关链接

******

- AutoJs6 OCR 文档: https://docs.autojs6.com/#/ocr
- PaddleOCR 官方项目: https://github.com/PaddlePaddle/PaddleOCR
- Paddle Lite 官方项目: https://github.com/PaddlePaddle/Paddle-Lite
- OpenCV 官方网站: https://opencv.org/


[16 KB page alignment and build verification](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/docs/16kb.md)
