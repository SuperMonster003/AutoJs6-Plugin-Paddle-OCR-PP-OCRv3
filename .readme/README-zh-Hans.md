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

AutoJs6 Paddle OCR (PP-OCRv3) 插件为 AutoJs6 提供基于 PaddleOCR PP-OCRv3 与 ONNX Runtime 的光学字符识别能力, 支持截图, 本地图像文件和原始图像输入. 自 2.0.0 起推理引擎由 Paddle Lite 改为 ONNX Runtime, 支持 4 个 ABI, 并按识别语种分为 12 个语种包.

> **Paddle Lite 版**: 1.0.x 的 Paddle Lite 实现已改名为 [Paddle OCR (PP-OCRv3 Paddle Lite)](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3-Paddle-Lite) 单独发布 (插件 ID `paddle-ocr-pp-ocrv3-paddle-lite`, 变体 `v3-paddle-lite`), 只支持 arm64-v8a 与 armeabi-v7a, 可与本插件同时安装.

******

### 功能

******

- 提供 12 个语种包: 简体中文, 英文, 繁体中文, 日文, 韩文, 拉丁字母语言, 阿拉伯文, 西里尔字母语言, 天城文, 泰卢固文, 卡纳达文, 泰米尔文; 简体中文包沿用 1.0.x 的包名与插件 ID `paddle-ocr-pp-ocrv3`, 各语种包的引擎均为 `paddle-ocr`, 变体均为 `v3`.
- 阿拉伯文包按阅读顺序返回文字, 同一行的词语从右到左排列.
- 支持 AutoJs6 中的 `ocr.paddle.recognizeText(image)` 和 `ocr.paddle.detect(image)`.
- 支持屏幕截图, 本地图像文件和原始 ARGB_8888 图像输入.
- 插件信息, 使用说明, README 与 CHANGELOG 均支持西班牙语/法语/俄语/阿拉伯语/日语/韩语/英语/简体中文/香港繁体/台湾繁体.
- 基于 PaddleOCR PP-OCRv3, ONNX Runtime 1.21.1 和 OpenCV 4.8.0, 支持 arm64-v8a, armeabi-v7a, x86_64 与 x86 共 4 个 ABI.
- `useSlim: true` 使用由 ONNX Runtime 动态量化 (int8) 生成的检测与识别模型.
- `useCls: true` 在识别前判断文字方向, 可识别旋转 180 度的文字; 默认关闭, 与 1.0.x 一致.
- `useOpenCL` 在 ONNX Runtime 版映射为 NNAPI: Android 8.1 (API 27) 及以上使用 NNAPI 执行提供器, 更低版本或 NNAPI 初始化失败时回退 CPU; 是否更快因设备而异.
- 图像最多包含 16777216 个像素, 原始图像缓冲区上限为 64 MiB
- 编码图像最大为 64 MiB, 支持文件描述符和管道传输

******

### 语种包

******

每个语种包是一个独立 APK, 可以同时安装多个:

| 语种 | `profile` | 插件 ID | 包名 | APK 文件名 |
| --- | --- | --- | --- | --- |
| 简体中文 | `zh` | `paddle-ocr-pp-ocrv3` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3` | `*-zh-<ABI>-*.apk` |
| 英文 | `en` | `paddle-ocr-pp-ocrv3-en` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.en` | `*-en-<ABI>-*.apk` |
| 繁体中文 | `zh-hant` | `paddle-ocr-pp-ocrv3-zh-hant` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.zhhant` | `*-zh-hant-<ABI>-*.apk` |
| 日文 | `ja` | `paddle-ocr-pp-ocrv3-ja` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.ja` | `*-ja-<ABI>-*.apk` |
| 韩文 | `ko` | `paddle-ocr-pp-ocrv3-ko` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.ko` | `*-ko-<ABI>-*.apk` |
| 拉丁字母语言 | `latin` | `paddle-ocr-pp-ocrv3-latin` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.latin` | `*-latin-<ABI>-*.apk` |
| 阿拉伯文 | `arabic` | `paddle-ocr-pp-ocrv3-arabic` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.arabic` | `*-arabic-<ABI>-*.apk` |
| 西里尔字母语言 | `cyrillic` | `paddle-ocr-pp-ocrv3-cyrillic` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.cyrillic` | `*-cyrillic-<ABI>-*.apk` |
| 天城文 | `devanagari` | `paddle-ocr-pp-ocrv3-devanagari` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.devanagari` | `*-devanagari-<ABI>-*.apk` |
| 泰卢固文 | `te` | `paddle-ocr-pp-ocrv3-te` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.te` | `*-te-<ABI>-*.apk` |
| 卡纳达文 | `ka` | `paddle-ocr-pp-ocrv3-ka` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.ka` | `*-ka-<ABI>-*.apk` |
| 泰米尔文 | `ta` | `paddle-ocr-pp-ocrv3-ta` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.ta` | `*-ta-<ABI>-*.apk` |

按要识别的文字选择语种包: 简体中文包也能识别英文字母与数字, 是默认推荐; 繁体中文, 日文, 韩文, 阿拉伯文, 泰卢固文, 卡纳达文或泰米尔文请安装对应的语种包; 拉丁字母语言包用于法语, 德语, 西班牙语等, 西里尔字母语言包用于俄语, 乌克兰语等, 天城文包用于印地语, 马拉地语等; 只识别英文时也可以安装英文包. 天城文, 泰卢固文, 卡纳达文, 泰米尔文模型读简单词语较准, 但连写字母与写在辅音前面的元音符号可能读错或顺序不对. 每个语种包按 ABI 提供 5 个 APK: `arm64-v8a` (大多数手机), `armeabi-v7a`, `x86_64`, `x86` 和 `universal` (包含全部 4 个 ABI, 体积最大), 只需安装与设备匹配的一个.

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

指定语种包与可选项:

```js
let img = images.read("test.png");
/* 使用日文语种包. */
ocr.paddle(img, { profile: "ja" });
/* 按插件 ID 指定韩文语种包. */
ocr.paddle(img, { engineId: "paddle-ocr-pp-ocrv3-ko" });
/* 使用量化模型并开启文字方向分类. */
ocr.paddle(img, { useSlim: true, useCls: true });
/* useOpenCL 在 ONNX Runtime 版映射为 NNAPI. */
ocr.paddle(img, { useOpenCL: true });
/* 使用 Paddle Lite 版插件. */
ocr.paddle(img, { variant: "v3-paddle-lite" });
```

按 `profile` 选择语种包与 `useCls` 选项需要 AutoJs6 6.8.0 或更高版本. 更早的宿主不按 `profile` 选择, 也不传递 `useCls`; 同时安装多个语种包时可用 `engineId` 指定.

******

### 接口方法

******

常用 OCR 接口包括:

```text
ocr.paddle.recognizeText(image)
ocr.paddle.detect(image)
ocr.paddle(image)
ocr.paddle(image, options)
ocr.paddle.recognizeText()
ocr.paddle()
```

`ocr.paddle()` 默认识别当前截图, `ocr.paddle(path)` 可识别本地图像文件.

******

### 发行历史

******

# v2.1.0

###### 2026/10/31

* `提示` 天城文, 泰卢固文, 卡纳达文, 泰米尔文模型读简单词语较准, 但连写字母与写在辅音前面的元音符号可能读错或顺序不对
* `新增` 新增 7 个语种包: 拉丁字母语言 (`latin`), 阿拉伯文 (`arabic`), 西里尔字母语言 (`cyrillic`), 天城文 (`devanagari`), 泰卢固文 (`te`), 卡纳达文 (`ka`), 泰米尔文 (`ta`); 每个语种包是独立的 APK, 可与其他语种包同时安装, 用括号里的 `profile` 指定
* `新增` 阿拉伯文包按阅读顺序返回文字, 同一行的词语从右到左排列

# v2.0.0

###### 2026/10/30

* `提示` 识别引擎由 Paddle Lite 改为 ONNX Runtime, 开发者改为 SuperMonster003; 原 Paddle Lite 实现改名为 Paddle OCR (PP-OCRv3 Paddle Lite) 单独发布 (插件 ID `paddle-ocr-pp-ocrv3-paddle-lite`, 变体 `v3-paddle-lite`), 可与本插件同时安装; 1.0.6 及更早的版本记录属于这个 Paddle Lite 插件, 它现在在新仓库继续更新
* `提示` 按识别语种分为简体中文, 英文, 繁体中文, 日文, 韩文 5 个语种包, 每个语种包是独立的 APK; 简体中文包沿用原来的包名与插件 ID
* `提示` 按 `profile` 选择语种包与 `useCls` 选项需要 AutoJs6 6.8.0 或更高版本; 更早的宿主不按 `profile` 选择, 也不传递 `useCls`; 本插件声明的最低宿主版本号为 5935 (AutoJs6 6.8.0)
* `新增` 支持 x86_64 与 x86 设备 (包括模拟器), 共 4 个 ABI
* `新增` 新增 `useCls` 选项, 识别前先判断文字方向, 可识别旋转 180 度的文字; 默认关闭
* `新增` `useOpenCL` 在 ONNX Runtime 版映射为 NNAPI: Android 8.1 及以上使用 NNAPI, 更低版本或 NNAPI 不可用时回退 CPU
* `新增` 新增语种包选择: 用 `profile` 指定语种 (`zh`, `en`, `zh-hant`, `ja`, `ko`), 用 `variant: "v3-paddle-lite"` 指定 Paddle Lite 版; 不指定时, 在 PP-OCRv3 插件之间默认使用简体中文包
* `优化` `useSlim` 改用由 ONNX Runtime 动态量化 (int8) 生成的检测与识别模型
* `依赖` 新增 ONNX Runtime Android 1.21.1, 移除 Paddle Lite
* `依赖` PaddleOCR PP-OCRv3 模型改为 ONNX 格式 (由官方推理模型转换), 新增英文, 繁体中文, 日文, 韩文识别模型与文字方向分类模型
* `依赖` OpenCV 4.8.0 改回以共享库 libopencv_java4.so 随 APK 提供, 每个 ABI 一份, 与 PP-OCRv4 插件相同 (1.0.6 曾把它静态链接进 libNative.so); 打包应用时这个库来自 OpenCV 插件, 不从本插件复制: 选用本插件打包会自动带入 OpenCV 插件, 未安装时打包报错

# v1.0.6

###### 2026/10/10

* `提示` 打包应用使用本版本时, 宿主需为 AutoJs6 6.8.0 或更高版本; 旧版宿主只有同时勾选 OpenCV 才能打包
* `修复` 模型加载或推理出现原生异常时插件进程直接崩溃的问题, 现改为向宿主返回错误
* `优化` libNative.so 不再导出 OpenCV 符号, APK 不再携带 libopencv_java4.so 且体积更小, 打包应用中可与其他版本的 OpenCV 同时使用
* `依赖` 移除 OpenCV Android AAR 版本 4.8.0 (仅保留静态链接的 OpenCV Android SDK 4.8.0, 下载时校验 SHA-256)

##### 更多发行历史可参阅

* [CHANGELOG.md](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/app/src/main/assets/doc/CHANGELOG-zh-Hans.md)

******

### 构建

******

```powershell
python -I scripts\prepare_ppocrv3_assets.py --profile all --slim
.\gradlew.bat :app:assembleZhDebug
```

Release 构建:

```powershell
.\gradlew.bat :app:appendDigestToReleasedFiles
```

构建参数来自 `version.properties`, 当前最低 SDK 为 24, 目标 SDK 为 37. ONNX 模型不入库: 构建前先运行上面的 `prepare_ppocrv3_assets.py`, 它会下载 PaddleOCR 官方模型, 转换为 ONNX 并按 `libs/ppocr-android-sdk/models.provenance.json` 校验; `--profile` 可选 `zh`, `en`, `zhHant`, `ja`, `ko`, `latin`, `arabic`, `cyrillic`, `devanagari`, `te`, `ka`, `ta` 或 `all`. 第三方组件与许可证见 [THIRD_PARTY_NOTICES.md](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/THIRD_PARTY_NOTICES.md).

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
- ONNX Runtime 官方项目: https://github.com/microsoft/onnxruntime
- OpenCV 官方网站: https://opencv.org/
- Paddle OCR (PP-OCRv3 Paddle Lite) 插件: https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3-Paddle-Lite


[16 KB page alignment and build verification](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/docs/16kb.md)
