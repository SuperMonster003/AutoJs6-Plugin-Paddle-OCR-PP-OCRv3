# v1.0.0

###### 2026/07/03

* `Feature` Paddle OCR (PP-OCRv3) plugin service, with plugin ID `paddle-ocr-pp-ocrv3`, engine `paddle-ocr`, and variant `v3`
* `Feature` Support discovering and invoking the plugin through `org.autojs.plugin.PADDLE_OCR`
* `Feature` Support `ocr.paddle.recognizeText(image)` text recognition and `ocr.paddle.detect(image)` text detection for screenshots, local image files, and raw ARGB_8888 image input
* `Feature` Bundle PaddleOCR PP-OCRv3 CPU models, running on Paddle Lite and OpenCV 4.8.0
* `Feature` Multilingual resources for plugin information, instructions, README, and CHANGELOG: Spanish/French/Russian/Arabic/Japanese/Korean/English/Simplified Chinese/Hong Kong Traditional Chinese/Taiwan Traditional Chinese
* `Improvement` Support ABI APK builds, including `arm64-v8a`/`armeabi-v7a` and `universal` packages
* `Improvement` Release APK filenames include project name, version number, and ABI variant
