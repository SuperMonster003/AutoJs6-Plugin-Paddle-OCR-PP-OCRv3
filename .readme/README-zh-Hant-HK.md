<!--suppress HtmlDeprecatedAttribute, HttpUrlsUsage -->

<div align="center">
  <p>
    <picture>
      <img src="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/app/src/main/res/mipmap/ic_launcher.png?raw=true" alt="autojs6-plugin-paddle-ocr-pp-ocrv3-ic-launcher" border="0" width="128" />
    </picture>
  </p>

  <p>用於 AutoJs6 的 Paddle OCR PP-OCRv3 文本識別插件</p>

  <p>
    <a href="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/releases"><img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3?label=Release"/></a>
    <a href="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/issues"><img alt="GitHub closed issues" src="https://img.shields.io/github/issues/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3?color=A24232&label=Issues"/></a>
    <a href="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/LICENSE"><img alt="GitHub License" src="https://img.shields.io/github/license/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3?color=534BAE&label=License"/></a>
  </p>
</div>

******

### 語言 (Languages)

******

當前 README.md 支援以下語言:

- [简体中文 [zh-Hans]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-zh-Hans.md)
- 繁體中文 (香港) [zh-Hant-HK] # 當前
- [繁體中文 (台灣) [zh-Hant-TW]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-zh-Hant-TW.md)
- [English [en]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-en.md)
- [Français [fr]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-fr.md)
- [Español [es]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-es.md)
- [日本語 [ja]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-ja.md)
- [한국어 [ko]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-ko.md)
- [Русский [ru]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-ru.md)
- [العربية [ar]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-ar.md)

******

### 簡介

******

AutoJs6 Paddle OCR (PP-OCRv3) 插件為 AutoJs6 提供基於 PaddleOCR PP-OCRv3 與 ONNX Runtime 的光學字符識別能力, 支援截圖, 本地圖像文件和原始圖像輸入. 自 2.0.0 起推理引擎由 Paddle Lite 改為 ONNX Runtime, 支援 4 個 ABI, 並按識別語種分為 5 個語種包.

> **Paddle Lite 版**: 1.0.x 的 Paddle Lite 實現已改名為 [Paddle OCR (PP-OCRv3 Paddle Lite)](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3-Paddle-Lite) 單獨發佈 (插件 ID `paddle-ocr-pp-ocrv3-paddle-lite`, 變體 `v3-paddle-lite`), 只支援 arm64-v8a 與 armeabi-v7a, 可與本插件同時安裝.

******

### 功能

******

- 提供 5 個語種包: 簡體中文, 英文, 繁體中文, 日文, 韓文; 簡體中文包沿用 1.0.x 的包名與插件 ID `paddle-ocr-pp-ocrv3`, 各語種包的引擎均為 `paddle-ocr`, 變體均為 `v3`.
- 支援 AutoJs6 中的 `ocr.paddle.recognizeText(image)` 和 `ocr.paddle.detect(image)`.
- 支援屏幕截圖, 本地圖像文件和原始 ARGB_8888 圖像輸入.
- 插件信息, 使用說明, README 與 CHANGELOG 均支援西班牙語/法語/俄語/阿拉伯語/日語/韓語/英語/簡體中文/香港繁體/台灣繁體.
- 基於 PaddleOCR PP-OCRv3, ONNX Runtime 1.21.1 和 OpenCV 4.8.0, 支援 arm64-v8a, armeabi-v7a, x86_64 與 x86 共 4 個 ABI.
- `useSlim: true` 使用由 ONNX Runtime 動態量化 (int8) 生成的檢測與識別模型.
- `useCls: true` 在識別前判斷文字方向, 可識別旋轉 180 度的文字; 默認關閉, 與 1.0.x 一致.
- `useOpenCL` 在 ONNX Runtime 版映射為 NNAPI: Android 8.1 (API 27) 及以上使用 NNAPI 執行提供器, 較低版本或 NNAPI 初始化失敗時回退 CPU; 是否更快因設備而異.
- 影像最多包含 16777216 個像素, 原始影像緩衝區上限為 64 MiB
- 編碼圖像最大為 64 MiB, 支援檔案描述符和管道傳輸

******

### 語種包

******

每個語種包是一個獨立 APK, 可以同時安裝多個:

| 語種 | `profile` | 插件 ID | 包名 | APK 文件名 |
| --- | --- | --- | --- | --- |
| 簡體中文 | `zh` | `paddle-ocr-pp-ocrv3` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3` | `*-zh-<ABI>-*.apk` |
| 英文 | `en` | `paddle-ocr-pp-ocrv3-en` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.en` | `*-en-<ABI>-*.apk` |
| 繁體中文 | `zh-hant` | `paddle-ocr-pp-ocrv3-zh-hant` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.zhhant` | `*-zhhant-<ABI>-*.apk` |
| 日文 | `ja` | `paddle-ocr-pp-ocrv3-ja` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.ja` | `*-ja-<ABI>-*.apk` |
| 韓文 | `ko` | `paddle-ocr-pp-ocrv3-ko` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.ko` | `*-ko-<ABI>-*.apk` |

按要識別的文字選擇語種包: 簡體中文包也能識別英文字母與數字, 是默認推薦; 繁體中文, 日文或韓文請安裝對應的語種包; 只識別英文時也可以安裝英文包. 每個語種包按 ABI 提供 5 個 APK: `arm64-v8a` (大多數手機), `armeabi-v7a`, `x86_64`, `x86` 和 `universal` (包含全部 4 個 ABI, 體積最大), 只需安裝與設備匹配的一個.

******

### 使用示例

******

識別屏幕截圖中的文本內容:

```js
let capt = images.captureScreen();
let texts = ocr.paddle.recognizeText(capt);
console.log(texts.join("\n"));
```

識別本地圖像文件中的文本內容, 以 `test.png` 為例:

```js
let img = images.read("test.png");
let results = ocr.paddle.detect(img);
console.log(results);
```

亦可以使用簡寫形式:

```js
ocr.paddle.recognizeText();
ocr.paddle("test.png");
```

指定語種包與選項:

```js
let img = images.read("test.png");
/* 使用日文語種包. */
ocr.paddle(img, { profile: "ja" });
/* 按插件 ID 指定韓文語種包. */
ocr.paddle(img, { engineId: "paddle-ocr-pp-ocrv3-ko" });
/* 使用量化模型並開啟文字方向分類. */
ocr.paddle(img, { useSlim: true, useCls: true });
/* useOpenCL 在 ONNX Runtime 版映射為 NNAPI. */
ocr.paddle(img, { useOpenCL: true });
/* 使用 Paddle Lite 版插件. */
ocr.paddle(img, { variant: "v3-paddle-lite" });
```

按 `profile` 選擇語種包與 `useCls` 選項需要 AutoJs6 6.8.0 或更高版本. 較舊的宿主不會按 `profile` 選擇, 也不會傳遞 `useCls`; 同時安裝多個語種包時可用 `engineId` 指定.

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

`ocr.paddle()` 默認識別當前截圖, `ocr.paddle(path)` 可識別本地圖像文件.

******

### 發行歷史

******

# v2.0.0

###### 2026/10/30

* `提示` 識別引擎由 Paddle Lite 改為 ONNX Runtime, 開發者改為 SuperMonster003; 原 Paddle Lite 實現改名為 Paddle OCR (PP-OCRv3 Paddle Lite) 單獨發佈 (插件 ID `paddle-ocr-pp-ocrv3-paddle-lite`, 變體 `v3-paddle-lite`), 可與本插件同時安裝
* `提示` 按識別語種分為簡體中文, 英文, 繁體中文, 日文, 韓文 5 個語種包, 每個語種包是獨立的 APK; 簡體中文包沿用原來的包名與插件 ID
* `提示` 按 `profile` 選擇語種包與 `useCls` 選項需要 AutoJs6 6.8.0 或更高版本; 較舊的宿主不會按 `profile` 選擇, 也不會傳遞 `useCls`
* `新增` 支援 x86_64 與 x86 設備 (包括模擬器), 共 4 個 ABI
* `新增` 新增 `useCls` 選項, 識別前先判斷文字方向, 可識別旋轉 180 度的文字; 默認關閉
* `新增` `useOpenCL` 在 ONNX Runtime 版映射為 NNAPI: Android 8.1 及以上使用 NNAPI, 較低版本或 NNAPI 不可用時回退 CPU
* `優化` `useSlim` 改用由 ONNX Runtime 動態量化 (int8) 生成的檢測與識別模型
* `依賴` 新增 ONNX Runtime Android 1.21.1, 移除 Paddle Lite
* `依賴` PaddleOCR PP-OCRv3 模型改為 ONNX 格式 (由官方推理模型轉換), 新增英文, 繁體中文, 日文, 韓文識別模型與文字方向分類模型
* `依賴` OpenCV 4.8.0 改為以共享庫 libopencv_java4.so 提供, 與 PP-OCRv4 插件相同

# v1.0.6

###### 2026/10/10

* `提示` 打包應用使用本版本時, 宿主需為 AutoJs6 6.8.0 或更高版本; 舊版宿主只有同時勾選 OpenCV 才能打包
* `修復` 模型加載或推理出現原生異常時插件進程直接崩潰的問題, 現改為向宿主返回錯誤
* `優化` libNative.so 不再導出 OpenCV 符號, APK 不再攜帶 libopencv_java4.so 且體積更小, 打包應用中可與其他版本的 OpenCV 同時使用
* `依賴` 移除 OpenCV Android AAR 4.8.0, 僅保留靜態鏈接的 OpenCV Android SDK 4.8.0 (下載時校驗 SHA-256)

# v1.0.5

###### 2026/10/05

* `修復` AGP 9.1 構建時的 SDK XML v4 解析警告及 JVM 單元測試組裝任務誤觸發 APK 原生程式庫對齊檢查的問題 (共用構建外掛 1.8.3)
* `優化` 將 compileSdk 與 targetSdk 提升到 37 (Android 17), 插件行為不受新目標版本影響
* `優化` Android 系統應用程式資訊圖示與圖示工作台共用圖稿及明暗底色, 保留外掛程式中心透明圖稿與現有啟動器選項

##### 更多發行歷史可參閱

* [CHANGELOG.md](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/app/src/main/assets/doc/CHANGELOG-zh-Hant-HK.md)

******

### 構建

******

```powershell
python -I scripts\prepare_ppocrv3_assets.py --profile all --slim
.\gradlew.bat :app:assembleZhDebug
```

Release 構建:

```powershell
.\gradlew.bat :app:appendDigestToReleasedFiles
```

構建參數來自 `version.properties`, 當前最低 SDK 為 24, 目標 SDK 為 37. ONNX 模型不入庫: 構建前先運行上面的 `prepare_ppocrv3_assets.py`, 它會下載 PaddleOCR 官方模型, 轉換為 ONNX 並按 `libs/ppocr-android-sdk/models.provenance.json` 校驗; `--profile` 可選 `zh`, `en`, `zhHant`, `ja`, `ko` 或 `all`. 第三方組件與許可證見 [THIRD_PARTY_NOTICES.md](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/THIRD_PARTY_NOTICES.md).

******

### 資源結構

******

```text
.readme/lang_*.json
.changelog/lang_*.json
.python/generate_markdown.py
app/src/main/assets/doc/CHANGELOG*.md
app/src/main/res/values-*/strings.xml
app/src/main/res/raw-*/plugin_instruction.md
```

`strings.xml` 提供插件描述本地化; `plugin_instruction.md` 提供宿主側展示的插件使用說明. README 與 CHANGELOG 由 `.python/generate_markdown.py` 根據 JSON 源文件生成.

******

### 相關鏈接

******

- AutoJs6 OCR 文件: https://docs.autojs6.com/#/ocr
- PaddleOCR 官方項目: https://github.com/PaddlePaddle/PaddleOCR
- ONNX Runtime 官方項目: https://github.com/microsoft/onnxruntime
- OpenCV 官方網站: https://opencv.org/
- Paddle OCR (PP-OCRv3 Paddle Lite) 插件: https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3-Paddle-Lite


[16 KB page alignment and build verification](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/docs/16kb.md)
