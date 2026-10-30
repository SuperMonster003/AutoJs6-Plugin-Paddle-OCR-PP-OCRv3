# Third-party notices

Each language package (zh, en, zhHant, ja, ko, latin, arabic, cyrillic,
devanagari, te, ka, ta) bundles the components below.
Version 2.0.0 replaced Paddle Lite with ONNX Runtime; the 1.0.x releases
recorded Paddle Lite (Apache License 2.0) instead.

- Inference SDK (`libs/ppocr-android-sdk`): derived from the PaddleOCR
  pipeline (DB detection post-processing, text line orientation classification
  and CTC decoding) through the PP-OCRv4 plugin SDK, renamed to the package
  `io.github.supermonster003.autojs6.plugin.paddleocr.v3.sdk`. Copyright
  PaddlePaddle Authors, Apache License 2.0
  (https://github.com/PaddlePaddle/PaddleOCR/blob/v2.7.0/LICENSE).
- ONNX Runtime 1.21.1 (`com.microsoft.onnxruntime:onnxruntime-android`,
  `libonnxruntime.so` and `libonnxruntime4j_jni.so`): Copyright Microsoft
  Corporation, MIT License
  (https://github.com/microsoft/onnxruntime/blob/v1.21.1/LICENSE).
- OpenCV 4.8.0 Android Java module (`libs/org-opencv-4_8_0`, native libraries
  rebuilt for 16 KB pages): Apache License 2.0
  (https://github.com/opencv/opencv/blob/4.8.0/LICENSE). Build inputs and
  hashes are in `libs/org-opencv-4_8_0/opencv-4.8.0.provenance.json`.
- PaddleOCR PP-OCRv3 detection and recognition models, the PP-OCR mobile v2.0
  text line orientation classifier and the recognition dictionaries: Copyright
  PaddlePaddle Authors, Apache License 2.0
  (https://github.com/PaddlePaddle/PaddleOCR/blob/v2.7.0/LICENSE). They are
  converted to ONNX by `scripts/prepare_ppocrv3_assets.py`, which also derives
  the dynamically quantized slim det / rec models (`useSlim`); download URLs,
  SHA-256 hashes, conversion and quantization commands are in
  `libs/ppocr-android-sdk/models.provenance.json`. The models are not stored in
  this repository.
- LLVM libc++ (`libc++_shared.so` from Android NDK r28c): Apache License 2.0
  with LLVM Exceptions (https://llvm.org/LICENSE.txt). The copied files and
  hashes are in
  `libs/ppocrv3-plugin-runtime/src/main/jniLibs/libc++_shared.provenance.json`.

Paddle2ONNX 1.3.1, PaddlePaddle and the ONNX Runtime Python quantization tools
are used only on the build machine to prepare the models and are not
distributed with the APK. Android platform
libraries listed in the ELF dynamic dependencies are supplied by Android and
are not redistributed by this plugin.
