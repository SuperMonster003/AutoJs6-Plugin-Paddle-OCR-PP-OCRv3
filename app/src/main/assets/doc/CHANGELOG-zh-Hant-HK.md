******

### 發行歷史

******

# v1.0.3

###### 2026/09/12

* `修復` 進程首次文字檢測使用較矮圖片 (如 1000 x 320) 時 Paddle Lite 崩潰 (SIGSEGV); 現在首次真實檢測前會先用 960 x 960 空白圖預熱檢測器一次

# v1.0.2

###### 2026/09/12

* `修復` Paddle OCR 原生依賴清理開關未初始化時 `clean` 任務執行失敗
* `優化` 同步 OpenCV 4.8.0 原生庫至 NDK r28c (Clang 19.0.1) 重編版本 (donor: AutoJs6-Plugin-OpenCV), 4 個 ABI 的 `libopencv_java4.so` 保持 16 KB `PT_LOAD` 對齊並附帶 provenance 清單

# v1.0.1

###### 2026/09/11

* `優化` 建置階段校驗 64 位原生程式庫的 16 KB 頁面大小對齊, 檢查 manifest 契約並輸出 JSON 報告

# v1.0.0

###### 2026/09/01

* `新增` Paddle OCR (PP-OCRv3) 插件服務, 插件 ID 為 `paddle-ocr-pp-ocrv3`, 引擎為 `paddle-ocr`, 變體為 `v3`
* `新增` 支援通過 `org.autojs.plugin.PADDLE_OCR` 發現並調用插件
* `新增` 支援 `ocr.paddle.recognizeText(image)` 文本識別和 `ocr.paddle.detect(image)` 文本檢測, 覆蓋截圖, 本地圖像文件和原始 ARGB_8888 圖像輸入
* `新增` 內置 PaddleOCR PP-OCRv3 CPU 模型, 基於 Paddle Lite 和 OpenCV 4.8.0 運行
* `新增` 插件信息, 使用說明, README 與 CHANGELOG 的多語言資源: 西班牙語/法語/俄語/阿拉伯語/日語/韓語/英語/簡體中文/香港繁體/台灣繁體
* `優化` 支援按 ABI 構建 APK, 包括 `arm64-v8a`/`armeabi-v7a` 以及 `universal` 通用包
* `優化` 發布 APK 文件名包含項目名, 版本號和 ABI 變體
* `優化` 統一 README 版式與 Gradle 平台版本管理方式
