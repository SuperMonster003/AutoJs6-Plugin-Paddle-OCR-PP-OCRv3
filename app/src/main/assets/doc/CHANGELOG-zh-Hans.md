******

### 发行历史

******

# v1.0.4

###### 2026/09/13

* `修复` 初始化字符串转换的 JNI 临时引用清理不完整的问题, 并在 JNI 异常时及时终止初始化 _[`issue #575`](http://issues.autojs6.com/575)_
* `修复` 插件中心显示的版本与 ABI 信息匹配实际安装的 APK
* `修复` 编码图像最大为 64 MiB, 支持文件描述符和管道传输
* `修复` 版本日期保持统一的英文格式
* `优化` 发布下载文件生成前校验 APK 版本, 签名与完整变体集合
* `优化` 图像最多包含 16777216 个像素, 原始图像缓冲区上限为 64 MiB

# v1.0.3

###### 2026/09/12

* `修复` 进程首次文字检测使用较矮图片 (如 1000 x 320) 时 Paddle Lite 崩溃 (SIGSEGV); 现在首次真实检测前会先用 960 x 960 空白图预热检测器一次

# v1.0.2

###### 2026/09/12

* `修复` Paddle OCR 原生依赖清理开关未初始化时 `clean` 任务执行失败
* `优化` 同步 OpenCV 4.8.0 原生库至 NDK r28c (Clang 19.0.1) 重编版本 (donor: AutoJs6-Plugin-OpenCV), 4 个 ABI 的 `libopencv_java4.so` 保持 16 KB `PT_LOAD` 对齐并附带 provenance 清单

# v1.0.1

###### 2026/09/11

* `优化` 构建阶段校验 64 位原生库的 16 KB 页大小对齐, 检查 manifest 契约并输出 JSON 报告

# v1.0.0

###### 2026/09/01

* `新增` Paddle OCR (PP-OCRv3) 插件服务, 插件 ID 为 `paddle-ocr-pp-ocrv3`, 引擎为 `paddle-ocr`, 变体为 `v3`
* `新增` 支持通过 `org.autojs.plugin.PADDLE_OCR` 发现并调用插件
* `新增` 支持 `ocr.paddle.recognizeText(image)` 文本识别和 `ocr.paddle.detect(image)` 文本检测, 覆盖截图, 本地图像文件和原始 ARGB_8888 图像输入
* `新增` 内置 PaddleOCR PP-OCRv3 CPU 模型, 基于 Paddle Lite 和 OpenCV 4.8.0 运行
* `新增` 插件信息, 使用说明, README 与 CHANGELOG 的多语言资源: 西班牙语/法语/俄语/阿拉伯语/日语/韩语/英语/简体中文/香港繁体/台湾繁体
* `优化` 支持按 ABI 构建 APK, 包括 `arm64-v8a`/`armeabi-v7a` 以及 `universal` 通用包
* `优化` 发布 APK 文件名包含项目名, 版本号和 ABI 变体
* `优化` 统一 README 版式与 Gradle 平台版本管理方式
