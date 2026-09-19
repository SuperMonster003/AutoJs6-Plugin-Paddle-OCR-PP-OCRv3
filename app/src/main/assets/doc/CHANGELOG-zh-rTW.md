******

### 發行歷史

******

# v1.0.5

###### 2026/09/19

* `修復` AGP 9.1 建置時的 SDK XML v4 解析警告及 JVM 單元測試組裝工作誤觸發 APK 原生程式庫對齊檢查的問題 (共用建置外掛 1.8.3)
* `最佳化` 將 compileSdk 與 targetSdk 提升到 37 (Android 17), 外掛程式行為不受新目標版本影響

# v1.0.4

###### 2026/09/13

* `修復` 初始化字串轉換的 JNI 暫存參照清理不完整的問題, 並在 JNI 例外時及時終止初始化 _[`issue #575`](http://issues.autojs6.com/575)_
* `修復` 外掛中心顯示的版本與 ABI 資訊符合實際安裝的 APK
* `修復` 編碼影像最大為 64 MiB, 支援檔案描述元和管線傳輸
* `修復` 版本日期保持統一的英文格式
* `最佳化` 發行下載檔案產生前驗證 APK 版本, 簽章與完整變體集合
* `最佳化` 影像最多包含 16777216 個像素, 原始影像緩衝區上限為 64 MiB

# v1.0.3

###### 2026/09/12

* `修復` 進程首次文字檢測使用較矮圖片 (如 1000 x 320) 時 Paddle Lite 崩潰 (SIGSEGV); 現在首次真實檢測前會先用 960 x 960 空白圖預熱檢測器一次

# v1.0.2

###### 2026/09/12

* `修復` Paddle OCR 原生依賴清理開關未初始化時 `clean` 任務執行失敗
* `最佳化` 同步 OpenCV 4.8.0 原生程式庫至 NDK r28c (Clang 19.0.1) 重新建置版本 (donor: AutoJs6-Plugin-OpenCV), 4 個 ABI 的 `libopencv_java4.so` 保持 16 KB `PT_LOAD` 對齊並附帶 provenance 清單

# v1.0.1

###### 2026/09/11

* `最佳化` 建置階段校驗 64 位原生函式庫的 16 KB 頁面大小對齊, 檢查 manifest 契約並輸出 JSON 報告

# v1.0.0

###### 2026/09/01

* `新增` Paddle OCR (PP-OCRv3) 外掛服務, 外掛 ID 為 `paddle-ocr-pp-ocrv3`, 引擎為 `paddle-ocr`, 變體為 `v3`
* `新增` 支援透過 `org.autojs.plugin.PADDLE_OCR` 發現並呼叫外掛
* `新增` 支援 `ocr.paddle.recognizeText(image)` 文字辨識和 `ocr.paddle.detect(image)` 文字偵測, 涵蓋截圖, 本機影像檔案和原始 ARGB_8888 影像輸入
* `新增` 內建 PaddleOCR PP-OCRv3 CPU 模型, 基於 Paddle Lite 和 OpenCV 4.8.0 執行
* `新增` 外掛資訊, 使用說明, README 與 CHANGELOG 的多語言資源: 西班牙語/法語/俄語/阿拉伯語/日語/韓語/英語/簡體中文/香港繁體/台灣繁體
* `最佳化` 支援按 ABI 建置 APK, 包括 `arm64-v8a`/`armeabi-v7a` 以及 `universal` 通用包
* `最佳化` 發行 APK 檔名包含專案名, 版本號和 ABI 變體
* `最佳化` 統一 README 版式與 Gradle 平台版本管理方式
