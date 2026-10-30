******

### Release History

******

# v2.0.0

###### 2026/10/30

* `Hint` Recognition now runs on ONNX Runtime instead of Paddle Lite, and the developer is now SuperMonster003. The previous Paddle Lite implementation is published separately as Paddle OCR (PP-OCRv3 Paddle Lite) (plugin ID `paddle-ocr-pp-ocrv3-paddle-lite`, variant `v3-paddle-lite`) and can be installed alongside this plugin. Versions 1.0.6 and earlier belong to that Paddle Lite plugin, which continues in its own repository
* `Hint` The plugin now comes as five language packages (Simplified Chinese, English, Traditional Chinese, Japanese, and Korean), each a separate APK; the Simplified Chinese package keeps the original package name and plugin ID
* `Hint` Choosing a package by `profile` and the `useCls` option need AutoJs6 6.8.0 or later; older hosts do not choose by `profile` and do not pass `useCls` on. This plugin declares host version code 5935 (AutoJs6 6.8.0) as its minimum
* `Feature` Support x86_64 and x86 devices, including emulators, for four ABIs in total
* `Feature` Add the `useCls` option, which checks the text direction before recognition so text rotated by 180 degrees can be read; it is off by default
* `Feature` `useOpenCL` maps to NNAPI in the ONNX Runtime edition: Android 8.1 and later use NNAPI, and older versions or devices where NNAPI is unavailable fall back to the CPU
* `Feature` Choose a language with `profile` (`zh`, `en`, `zh-hant`, `ja`, `ko`) and the Paddle Lite edition with `variant: "v3-paddle-lite"`; without them, the Simplified Chinese package is the default among the PP-OCRv3 plugins
* `Improvement` `useSlim` now uses detection and recognition models quantized to int8 with ONNX Runtime dynamic quantization
* `Dependency` Add ONNX Runtime Android 1.21.1 and remove Paddle Lite
* `Dependency` PaddleOCR PP-OCRv3 models are now in ONNX format, converted from the official inference models, with new English, Traditional Chinese, Japanese, and Korean recognition models and a text direction model
* `Dependency` OpenCV 4.8.0 is shipped again as the shared library libopencv_java4.so, one per ABI, as in the PP-OCRv4 plugin (1.0.6 linked it statically into libNative.so). Packaged applications take this library from the OpenCV plugin, not from this plugin: packaging with this plugin adds the OpenCV plugin automatically and fails if it is not installed

# v1.0.6

###### 2026/10/10

* `Hint` Packaged apps that use this version need AutoJs6 6.8.0 or later as the host; older hosts can package it only together with OpenCV
* `Fix` Native failures during model loading or inference aborted the plugin process; they are now reported to the host as errors
* `Improvement` libNative.so no longer exports OpenCV symbols and the APK no longer ships libopencv_java4.so, so it is smaller and packaged apps can use it alongside another OpenCV version
* `Dependency` Remove the OpenCV Android AAR 4.8.0; only the statically linked OpenCV Android SDK 4.8.0 remains, verified by SHA-256 when downloaded

# v1.0.5

###### 2026/10/05

* `Fix` SDK XML v4 parsing warnings with AGP 9.1 and APK native alignment checks incorrectly triggered by JVM unit-test assembly tasks, using shared build plugins 1.8.3
* `Improvement` Raise compileSdk and targetSdk to 37 (Android 17); the plugin's behavior does not depend on the new target
* `Improvement` Android App info icons share Icon Studio artwork and light/dark backgrounds while preserving transparent Plugin Center artwork and existing launcher choices

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
