******

### Release History

******

# v1.0.5

###### 2026/09/15

* `Improvement` Raise compileSdk and targetSdk to 37 (Android 17); the plugin's behavior does not depend on the new target

# v1.0.4

###### 2026/09/13

* `Fix` Incomplete cleanup of temporary JNI references during initialization string conversion; initialization now stops promptly on JNI exceptions _[`issue #575`](http://issues.autojs6.com/575)_
* `Fix` Plugin center version and ABI information matches the installed plugin APK
* `Fix` Encoded image input is limited to 64 MiB and supports file descriptors and pipes
* `Fix` Version dates use a consistent English format
* `Improvement` Validate release APK versions, signing and the complete variant set before creating download artifacts
* `Improvement` Images may contain at most 16777216 pixels; raw image buffers are limited to 64 MiB

# v1.0.3

###### 2026/09/12

* `Fix` Paddle Lite crashed (SIGSEGV) when the first text detection of a process used a short image such as 1000 x 320; the detector is now warmed up once with a 960 x 960 blank image before the first real detection

# v1.0.2

###### 2026/09/12

* `Fix` The `clean` task failed when the Paddle OCR native dependency cleanup flag was not initialized
* `Improvement` Synced the OpenCV 4.8.0 native library to the NDK r28c (Clang 19.0.1) rebuild (donor: AutoJs6-Plugin-OpenCV); `libopencv_java4.so` for all 4 ABIs keeps 16 KB `PT_LOAD` alignment and ships with a provenance manifest

# v1.0.1

###### 2026/09/11

* `Improvement` Build verification of 16 KB page alignment for 64-bit native libraries, including manifest contract checks and JSON reports

# v1.0.0

###### 2026/09/01

* `Feature` Paddle OCR (PP-OCRv3) plugin service, with plugin ID `paddle-ocr-pp-ocrv3`, engine `paddle-ocr`, and variant `v3`
* `Feature` Support discovering and invoking the plugin through `org.autojs.plugin.PADDLE_OCR`
* `Feature` Support `ocr.paddle.recognizeText(image)` text recognition and `ocr.paddle.detect(image)` text detection for screenshots, local image files, and raw ARGB_8888 image input
* `Feature` Bundle PaddleOCR PP-OCRv3 CPU models, running on Paddle Lite and OpenCV 4.8.0
* `Feature` Multilingual resources for plugin information, instructions, README, and CHANGELOG: Spanish/French/Russian/Arabic/Japanese/Korean/English/Simplified Chinese/Hong Kong Traditional Chinese/Taiwan Traditional Chinese
* `Improvement` Support ABI APK builds, including `arm64-v8a`/`armeabi-v7a` and `universal` packages
* `Improvement` Release APK filenames include project name, version number, and ABI variant
* `Improvement` Standardize the README layout and Gradle platform version management
