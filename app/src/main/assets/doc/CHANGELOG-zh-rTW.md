# v1.0.0

###### 2026/07/17

* `新增` Paddle OCR (PP-OCRv3) 外掛服務, 外掛 ID 為 `paddle-ocr-pp-ocrv3`, 引擎為 `paddle-ocr`, 變體為 `v3`
* `新增` 支援透過 `org.autojs.plugin.PADDLE_OCR` 發現並呼叫外掛
* `新增` 支援 `ocr.paddle.recognizeText(image)` 文字辨識和 `ocr.paddle.detect(image)` 文字偵測, 涵蓋截圖, 本機影像檔案和原始 ARGB_8888 影像輸入
* `新增` 內建 PaddleOCR PP-OCRv3 CPU 模型, 基於 Paddle Lite 和 OpenCV 4.8.0 執行
* `新增` 外掛資訊, 使用說明, README 與 CHANGELOG 的多語言資源: 西班牙語/法語/俄語/阿拉伯語/日語/韓語/英語/簡體中文/香港繁體/台灣繁體
* `最佳化` 支援按 ABI 建置 APK, 包括 `arm64-v8a`/`armeabi-v7a` 以及 `universal` 通用包
* `最佳化` 發行 APK 檔名包含專案名, 版本號和 ABI 變體
