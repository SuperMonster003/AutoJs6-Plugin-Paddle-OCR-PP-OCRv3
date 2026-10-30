<!--suppress HtmlDeprecatedAttribute, HttpUrlsUsage -->

<div align="center">
  <p>
    <picture>
      <img src="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/app/src/main/res/mipmap/ic_launcher.png?raw=true" alt="autojs6-plugin-paddle-ocr-pp-ocrv3-ic-launcher" border="0" width="128" />
    </picture>
  </p>

  <p>用於 AutoJs6 的 Paddle OCR PP-OCRv3 文字辨識外掛</p>

  <p>
    <a href="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/releases"><img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3?label=Release"/></a>
    <a href="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/issues"><img alt="GitHub closed issues" src="https://img.shields.io/github/issues/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3?color=A24232&label=Issues"/></a>
    <a href="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/LICENSE"><img alt="GitHub License" src="https://img.shields.io/github/license/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3?color=534BAE&label=License"/></a>
  </p>
</div>

******

### 語言 (Languages)

******

目前 README.md 支援以下語言:

- [简体中文 [zh-Hans]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-zh-Hans.md)
- [繁體中文 (香港) [zh-Hant-HK]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-zh-Hant-HK.md)
- 繁體中文 (台灣) [zh-Hant-TW] # 目前
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

AutoJs6 Paddle OCR (PP-OCRv3) 外掛為 AutoJs6 提供基於 PaddleOCR PP-OCRv3 與 ONNX Runtime 的光學字元辨識能力, 支援截圖, 本機影像檔案和原始影像輸入. 自 2.0.0 起推論引擎由 Paddle Lite 改為 ONNX Runtime, 支援 4 個 ABI, 並依辨識語種分為 5 個語種包.

> **Paddle Lite 版**: 1.0.x 的 Paddle Lite 實作已改名為 [Paddle OCR (PP-OCRv3 Paddle Lite)](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3-Paddle-Lite) 另行發布 (外掛 ID `paddle-ocr-pp-ocrv3-paddle-lite`, 變體 `v3-paddle-lite`), 只支援 arm64-v8a 與 armeabi-v7a, 可與本外掛同時安裝.

******

### 功能

******

- 提供 5 個語種包: 簡體中文, 英文, 繁體中文, 日文, 韓文; 簡體中文包沿用 1.0.x 的套件名稱與外掛 ID `paddle-ocr-pp-ocrv3`, 各語種包的引擎皆為 `paddle-ocr`, 變體皆為 `v3`.
- 支援 AutoJs6 中的 `ocr.paddle.recognizeText(image)` 和 `ocr.paddle.detect(image)`.
- 支援螢幕截圖, 本機影像檔案和原始 ARGB_8888 影像輸入.
- 外掛資訊, 使用說明, README 與 CHANGELOG 均支援西班牙語/法語/俄語/阿拉伯語/日語/韓語/英語/簡體中文/香港繁體/台灣繁體.
- 基於 PaddleOCR PP-OCRv3, ONNX Runtime 1.21.1 和 OpenCV 4.8.0, 支援 arm64-v8a, armeabi-v7a, x86_64 與 x86 共 4 個 ABI.
- `useSlim: true` 使用以 ONNX Runtime 動態量化 (int8) 產生的偵測與辨識模型.
- `useCls: true` 在辨識前判斷文字方向, 可辨識旋轉 180 度的文字; 預設關閉, 與 1.0.x 一致.
- `useOpenCL` 在 ONNX Runtime 版映射為 NNAPI: Android 8.1 (API 27) 及以上使用 NNAPI 執行提供者, 較低版本或 NNAPI 初始化失敗時退回 CPU; 是否更快因裝置而異.
- 影像最多包含 16777216 個像素, 原始影像緩衝區上限為 64 MiB
- 編碼影像最大為 64 MiB, 支援檔案描述元和管線傳輸

******

### 語種包

******

每個語種包是一個獨立 APK, 可以同時安裝多個:

| 語種 | `profile` | 外掛 ID | 套件名稱 | APK 檔名 |
| --- | --- | --- | --- | --- |
| 簡體中文 | `zh` | `paddle-ocr-pp-ocrv3` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3` | `*-zh-<ABI>-*.apk` |
| 英文 | `en` | `paddle-ocr-pp-ocrv3-en` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.en` | `*-en-<ABI>-*.apk` |
| 繁體中文 | `zh-hant` | `paddle-ocr-pp-ocrv3-zh-hant` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.zhhant` | `*-zhhant-<ABI>-*.apk` |
| 日文 | `ja` | `paddle-ocr-pp-ocrv3-ja` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.ja` | `*-ja-<ABI>-*.apk` |
| 韓文 | `ko` | `paddle-ocr-pp-ocrv3-ko` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.ko` | `*-ko-<ABI>-*.apk` |

依要辨識的文字選擇語種包: 簡體中文包也能辨識英文字母與數字, 是預設推薦; 繁體中文, 日文或韓文請安裝對應的語種包; 只辨識英文時也可以安裝英文包. 每個語種包依 ABI 提供 5 個 APK: `arm64-v8a` (大多數手機), `armeabi-v7a`, `x86_64`, `x86` 和 `universal` (包含全部 4 個 ABI, 檔案最大), 只需安裝與裝置相符的一個.

******

### 使用範例

******

辨識螢幕截圖中的文字內容:

```js
let capt = images.captureScreen();
let texts = ocr.paddle.recognizeText(capt);
console.log(texts.join("\n"));
```

辨識本機影像檔案中的文字內容, 以 `test.png` 為例:

```js
let img = images.read("test.png");
let results = ocr.paddle.detect(img);
console.log(results);
```

也可以使用簡寫形式:

```js
ocr.paddle.recognizeText();
ocr.paddle("test.png");
```

指定語種包與選項:

```js
let img = images.read("test.png");
/* 使用日文語種包. */
ocr.paddle(img, { profile: "ja" });
/* 依外掛 ID 指定韓文語種包. */
ocr.paddle(img, { engineId: "paddle-ocr-pp-ocrv3-ko" });
/* 使用量化模型並開啟文字方向分類. */
ocr.paddle(img, { useSlim: true, useCls: true });
/* useOpenCL 在 ONNX Runtime 版映射為 NNAPI. */
ocr.paddle(img, { useOpenCL: true });
/* 使用 Paddle Lite 版外掛. */
ocr.paddle(img, { variant: "v3-paddle-lite" });
```

依 `profile` 選擇語種包與 `useCls` 選項需要 AutoJs6 6.8.0 或更新版本. 較舊的宿主不會依 `profile` 選擇, 也不會傳遞 `useCls`; 同時安裝多個語種包時可用 `engineId` 指定.

******

### 介面方法

******

常用 OCR 介面包括:

```text
ocr.paddle.recognizeText(image)
ocr.paddle.detect(image)
ocr.paddle(image)
ocr.paddle(image, options)
ocr.paddle.recognizeText()
ocr.paddle()
```

`ocr.paddle()` 預設辨識目前截圖, `ocr.paddle(path)` 可辨識本機影像檔案.

******

### 發行歷史

******

# v2.0.0

###### 2026/10/30

* `提示` 辨識引擎由 Paddle Lite 改為 ONNX Runtime, 開發者改為 SuperMonster003; 原 Paddle Lite 實作改名為 Paddle OCR (PP-OCRv3 Paddle Lite) 另行發布 (外掛 ID `paddle-ocr-pp-ocrv3-paddle-lite`, 變體 `v3-paddle-lite`), 可與本外掛同時安裝
* `提示` 依辨識語種分為簡體中文, 英文, 繁體中文, 日文, 韓文 5 個語種包, 每個語種包是獨立的 APK; 簡體中文包沿用原本的套件名稱與外掛 ID
* `提示` 依 `profile` 選擇語種包與 `useCls` 選項需要 AutoJs6 6.8.0 或更新版本; 較舊的宿主不會依 `profile` 選擇, 也不會傳遞 `useCls`
* `新增` 支援 x86_64 與 x86 裝置 (包括模擬器), 共 4 個 ABI
* `新增` 新增 `useCls` 選項, 辨識前先判斷文字方向, 可辨識旋轉 180 度的文字; 預設關閉
* `新增` `useOpenCL` 在 ONNX Runtime 版映射為 NNAPI: Android 8.1 及以上使用 NNAPI, 較低版本或 NNAPI 無法使用時退回 CPU
* `最佳化` `useSlim` 改用以 ONNX Runtime 動態量化 (int8) 產生的偵測與辨識模型
* `依賴` 新增 ONNX Runtime Android 1.21.1, 移除 Paddle Lite
* `依賴` PaddleOCR PP-OCRv3 模型改為 ONNX 格式 (由官方推論模型轉換), 新增英文, 繁體中文, 日文, 韓文辨識模型與文字方向分類模型
* `依賴` OpenCV 4.8.0 改為以共用程式庫 libopencv_java4.so 提供, 與 PP-OCRv4 外掛相同

# v1.0.6

###### 2026/10/10

* `提示` 打包的應用程式使用本版本時, 宿主需為 AutoJs6 6.8.0 或更高版本; 舊版宿主只有同時勾選 OpenCV 才能打包
* `修復` 模型載入或推論發生原生例外時外掛行程直接當機的問題, 現改為向宿主回傳錯誤
* `最佳化` libNative.so 不再匯出 OpenCV 符號, APK 不再附帶 libopencv_java4.so 且體積更小, 打包的應用程式中可與其他版本的 OpenCV 同時使用
* `依賴` 移除 OpenCV Android AAR 4.8.0, 僅保留靜態連結的 OpenCV Android SDK 4.8.0 (下載時驗證 SHA-256)

# v1.0.5

###### 2026/10/05

* `修復` AGP 9.1 建置時的 SDK XML v4 解析警告及 JVM 單元測試組裝工作誤觸發 APK 原生程式庫對齊檢查的問題 (共用建置外掛 1.8.3)
* `最佳化` 將 compileSdk 與 targetSdk 提升到 37 (Android 17), 外掛程式行為不受新目標版本影響
* `最佳化` Android 系統應用程式資訊圖示與圖示工作台共用圖稿及明暗底色, 保留外掛程式中心透明圖稿與現有啟動器選項

##### 更多發行歷史可參閱

* [CHANGELOG.md](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/app/src/main/assets/doc/CHANGELOG-zh-Hant-TW.md)

******

### 建置

******

```powershell
python -I scripts\prepare_ppocrv3_assets.py --profile all --slim
.\gradlew.bat :app:assembleZhDebug
```

Release 建置:

```powershell
.\gradlew.bat :app:appendDigestToReleasedFiles
```

建置參數來自 `version.properties`, 目前最低 SDK 為 24, 目標 SDK 為 37. ONNX 模型不納入版本庫: 建置前先執行上方的 `prepare_ppocrv3_assets.py`, 它會下載 PaddleOCR 官方模型, 轉換為 ONNX 並依 `libs/ppocr-android-sdk/models.provenance.json` 校驗; `--profile` 可選 `zh`, `en`, `zhHant`, `ja`, `ko` 或 `all`. 第三方元件與授權見 [THIRD_PARTY_NOTICES.md](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/THIRD_PARTY_NOTICES.md).

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

`strings.xml` 提供外掛描述本地化; `plugin_instruction.md` 提供宿主側展示的外掛使用說明. README 與 CHANGELOG 由 `.python/generate_markdown.py` 根據 JSON 原始檔生成.

******

### 相關連結

******

- AutoJs6 OCR 文件: https://docs.autojs6.com/#/ocr
- PaddleOCR 官方專案: https://github.com/PaddlePaddle/PaddleOCR
- ONNX Runtime 官方專案: https://github.com/microsoft/onnxruntime
- OpenCV 官方網站: https://opencv.org/
- Paddle OCR (PP-OCRv3 Paddle Lite) 外掛: https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3-Paddle-Lite


[16 KB page alignment and build verification](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/docs/16kb.md)
