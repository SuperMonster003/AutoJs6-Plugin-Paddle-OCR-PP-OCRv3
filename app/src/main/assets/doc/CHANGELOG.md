******

### 发行历史

******

# v2.1.0

###### 2026/10/31

* `提示` 天城文, 泰卢固文, 卡纳达文, 泰米尔文模型读简单词语较准, 但连写字母与写在辅音前面的元音符号可能读错或顺序不对
* `新增` 新增 7 个语种包: 拉丁字母语言 (`latin`), 阿拉伯文 (`arabic`), 西里尔字母语言 (`cyrillic`), 天城文 (`devanagari`), 泰卢固文 (`te`), 卡纳达文 (`ka`), 泰米尔文 (`ta`); 每个语种包是独立的 APK, 可与其他语种包同时安装, 用括号里的 `profile` 指定
* `新增` 阿拉伯文包按阅读顺序返回文字, 同一行的词语从右到左排列

# v2.0.0

###### 2026/10/30

* `提示` 识别引擎由 Paddle Lite 改为 ONNX Runtime, 开发者改为 SuperMonster003; 原 Paddle Lite 实现改名为 Paddle OCR (PP-OCRv3 Paddle Lite) 单独发布 (插件 ID `paddle-ocr-pp-ocrv3-paddle-lite`, 变体 `v3-paddle-lite`), 可与本插件同时安装; 1.0.6 及更早的版本记录属于这个 Paddle Lite 插件, 它现在在新仓库继续更新
* `提示` 按识别语种分为简体中文, 英文, 繁体中文, 日文, 韩文 5 个语种包, 每个语种包是独立的 APK; 简体中文包沿用原来的包名与插件 ID
* `提示` 按 `profile` 选择语种包与 `useCls` 选项需要 AutoJs6 6.8.0 或更高版本; 更早的宿主不按 `profile` 选择, 也不传递 `useCls`; 本插件声明的最低宿主版本号为 5935 (AutoJs6 6.8.0)
* `新增` 支持 x86_64 与 x86 设备 (包括模拟器), 共 4 个 ABI
* `新增` 新增 `useCls` 选项, 识别前先判断文字方向, 可识别旋转 180 度的文字; 默认关闭
* `新增` `useOpenCL` 在 ONNX Runtime 版映射为 NNAPI: Android 8.1 及以上使用 NNAPI, 更低版本或 NNAPI 不可用时回退 CPU
* `新增` 新增语种包选择: 用 `profile` 指定语种 (`zh`, `en`, `zh-hant`, `ja`, `ko`), 用 `variant: "v3-paddle-lite"` 指定 Paddle Lite 版; 不指定时, 在 PP-OCRv3 插件之间默认使用简体中文包
* `优化` `useSlim` 改用由 ONNX Runtime 动态量化 (int8) 生成的检测与识别模型
* `依赖` 新增 ONNX Runtime Android 1.21.1, 移除 Paddle Lite
* `依赖` PaddleOCR PP-OCRv3 模型改为 ONNX 格式 (由官方推理模型转换), 新增英文, 繁体中文, 日文, 韩文识别模型与文字方向分类模型
* `依赖` OpenCV 4.8.0 改回以共享库 libopencv_java4.so 随 APK 提供, 每个 ABI 一份, 与 PP-OCRv4 插件相同 (1.0.6 曾把它静态链接进 libNative.so); 打包应用时这个库来自 OpenCV 插件, 不从本插件复制: 选用本插件打包会自动带入 OpenCV 插件, 未安装时打包报错

# v1.0.6

###### 2026/10/10

* `提示` 打包应用使用本版本时, 宿主需为 AutoJs6 6.8.0 或更高版本; 旧版宿主只有同时勾选 OpenCV 才能打包
* `修复` 模型加载或推理出现原生异常时插件进程直接崩溃的问题, 现改为向宿主返回错误
* `优化` libNative.so 不再导出 OpenCV 符号, APK 不再携带 libopencv_java4.so 且体积更小, 打包应用中可与其他版本的 OpenCV 同时使用
* `依赖` 移除 OpenCV Android AAR 版本 4.8.0 (仅保留静态链接的 OpenCV Android SDK 4.8.0, 下载时校验 SHA-256)

# v1.0.5

###### 2026/10/05

* `修复` AGP 9.1 构建时的 SDK XML v4 解析警告, 以及 JVM 单元测试误触发 APK 原生库对齐检查的问题 (共享构建插件 1.8.3)
* `优化` compileSdk/targetSdk 升级至 37 (Android 17)
* `优化` Android 系统应用信息图标与图标工作台共用图稿和亮暗底色, 保留插件中心透明图稿及现有启动器选项

# v1.0.4

###### 2026/09/13

* `修复` 初始化字符串转换的 JNI 临时引用清理不完整的问题, 并在 JNI 异常时及时终止初始化 _[`issue #575`](http://issues.autojs6.com/575)_
* `修复` 插件中心显示的版本及 ABI 信息与实际安装包不一致的问题
* `修复` 编码图像的文件描述符及管道输入兼容性问题 (文件大小上限为 64 MiB)
* `修复` 版本日期受构建环境语言影响, 未统一使用英文格式的问题
* `优化` 发布前校验 APK 版本, 签名及变体完整性
* `优化` 图像最多包含 16777216 个像素, 原始图像缓冲区上限为 64 MiB

# v1.0.3

###### 2026/09/12

* `修复` 进程首次文字检测使用较矮图片 (如 1000 x 320) 时 Paddle Lite 崩溃 (SIGSEGV); 现在首次真实检测前会先用 960 x 960 空白图预热检测器一次

# v1.0.2

###### 2026/09/12

* `修复` Paddle OCR 原生依赖清理开关未初始化时 clean 任务执行失败
* `优化` OpenCV 4.8.0 原生库改用 NDK r28c (Clang 19.0.1) 构建, 4 个 ABI 均支持 16 KB 内存页并附带构建来源清单 (来源: AutoJs6-Plugin-OpenCV)

# v1.0.1

###### 2026/09/11

* `优化` 构建阶段校验 64 位原生库的 16 KB 内存页对齐及 Manifest 配置, 并输出校验报告

# v1.0.0

###### 2026/09/01

* `新增` Paddle OCR (PP-OCRv3) 插件服务, 插件 ID 为 `paddle-ocr-pp-ocrv3`, 引擎为 `paddle-ocr`, 变体为 v3
* `新增` 支持通过 org.autojs.plugin.PADDLE_OCR 发现并调用插件
* `新增` 支持 `ocr.paddle.recognizeText(image)` 文本识别和 `ocr.paddle.detect(image)` 文本检测, 覆盖截图, 本地图像文件和原始 ARGB_8888 图像输入
* `新增` 内置 PaddleOCR PP-OCRv3 CPU 模型, 基于 Paddle Lite 和 OpenCV 4.8.0 运行
* `新增` 插件信息, 使用说明, README 及 CHANGELOG 支持 10 种语言 (西班牙语/法语/俄语/阿拉伯语/日语/韩语/英语/简体中文/香港繁体/台湾繁体)
* `优化` 支持按 ABI 构建 APK, 包括 `arm64-v8a`/`armeabi-v7a` 以及 universal 通用包
* `优化` 发布 APK 文件名包含项目名, 版本号和 ABI 变体
* `优化` 统一 README 版式与 Gradle 平台版本管理方式
