# v1.0.0

###### 2026/07/03

* `新增` Paddle OCR (PP-OCRv3) 插件服務, 插件 ID 為 `paddle-ocr-pp-ocrv3`, 引擎為 `paddle-ocr`, 變體為 `v3`
* `新增` 支援通過 `org.autojs.plugin.PADDLE_OCR` 發現並調用插件
* `新增` 支援 `ocr.paddle.recognizeText(image)` 文本識別和 `ocr.paddle.detect(image)` 文本檢測, 覆蓋截圖, 本地圖像文件和原始 ARGB_8888 圖像輸入
* `新增` 內置 PaddleOCR PP-OCRv3 CPU 模型, 基於 Paddle Lite 和 OpenCV 4.8.0 運行
* `新增` 插件信息, 使用說明, README 與 CHANGELOG 的多語言資源: 西班牙語/法語/俄語/阿拉伯語/日語/韓語/英語/簡體中文/香港繁體/台灣繁體
* `優化` 支援按 ABI 構建 APK, 包括 `arm64-v8a`/`armeabi-v7a` 以及 `universal` 通用包
* `優化` 發布 APK 文件名包含項目名, 版本號和 ABI 變體
