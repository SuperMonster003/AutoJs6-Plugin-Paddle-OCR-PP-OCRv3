# v1.0.0

###### 2026/07/17

* `新增` Paddle OCR (PP-OCRv3) 插件服务, 插件 ID 为 `paddle-ocr-pp-ocrv3`, 引擎为 `paddle-ocr`, 变体为 `v3`
* `新增` 支持通过 `org.autojs.plugin.PADDLE_OCR` 发现并调用插件
* `新增` 支持 `ocr.paddle.recognizeText(image)` 文本识别和 `ocr.paddle.detect(image)` 文本检测, 覆盖截图, 本地图像文件和原始 ARGB_8888 图像输入
* `新增` 内置 PaddleOCR PP-OCRv3 CPU 模型, 基于 Paddle Lite 和 OpenCV 4.8.0 运行
* `新增` 插件信息, 使用说明, README 与 CHANGELOG 的多语言资源: 西班牙语/法语/俄语/阿拉伯语/日语/韩语/英语/简体中文/香港繁体/台湾繁体
* `优化` 支持按 ABI 构建 APK, 包括 `arm64-v8a`/`armeabi-v7a` 以及 `universal` 通用包
* `优化` 发布 APK 文件名包含项目名, 版本号和 ABI 变体
