# Paddle OCR (PP-OCRv3) ONNX Runtime Roadmap

更新日期: 2026-10-30

本文是 `AutoJs6-Plugin-Paddle-OCR-PP-OCRv3` (显示名 `Paddle OCR (PP-OCRv3)`) 从 Paddle-Lite 切换到 ONNX Runtime 并补齐 4 ABI 的路线图. 立项来源: 维护者 2026-10-29 提问 "v3 能否像 v4 / v5 / v6 一样支持 4 个 ABI". 诊断结论: 旧 v3 只有 arm64-v8a 与 armeabi-v7a 的根因是 Paddle-Lite 官方只提供 Android armv7 / armv8 预编译库 (无 x86 / x86_64), `.nb` 模型也绑定 Paddle-Lite; 补齐 4 ABI 的唯一可行路线是像 v4 一样改用 ONNX Runtime (4 ABI 官方 AAR) 跑 PP-OCRv3 的 ONNX 模型.

维护者经三轮选择题确定的总方案 (第 1 节): 本仓库 (包名, 仓库名, `plugin_id`, 向导键全部不变) 升级为 ONNX Runtime 版的 `2.0.0`, 开发者改为 SuperMonster003, 按语种拆成 5 个 flavor APK; 旧 Paddle-Lite 实现带完整历史复制到新仓库 `AutoJs6-Plugin-Paddle-OCR-PP-OCRv3-Paddle-Lite`, 改名为 `Paddle OCR (PP-OCRv3 Paddle Lite)` 并以 `1.1.0` 发布, 开发者保持 TonyJiangWJ; 两者都是官方插件, 图标一致; 宿主打包 APK 两套内嵌引擎都支持, 两者都装时优先 ONNX Runtime.

以 2026-10-29 的快照为基线: 本仓库 `master@bc01d0a` (37 提交, `VERSION_NAME=1.0.6`, `VERSION_BUILD=36`, `VERSION_CODE_OFFSET=25`, 已发布最高 versionCode 61, 索引清单只登记到 1.0.5 / 48); 宿主 `AutoJs6 master@3fa1fc8ad` (`VERSION_NAME=6.8.0` 未发布, `VERSION_BUILD=4283` + 1652 = versionCode 5935); v4 仓库 `AutoJs6-Plugin-Paddle-OCR-PP-OCRv4` (`1.0.4`, ONNX Runtime 1.21.1, OpenCV 4.8.0 Java AAR, 3 个 flavor) 为复用来源; Rapid OCR 插件同用 ONNX Runtime 1.21.1.

使用方式:

1. 每次会话开始时, 从 "阶段总览" (第 6 节) 选取一个或多个未完成条目, 优先级按阶段顺序; 单次会话可完成多个小节, 除非单个小节已足够繁杂.
2. 条目完成后勾选 `[x]`, 并在条目后追加证据 (提交 hash / 测试类名 / 设备型号与 API / 度量值), 证据等级见附录 E. 未勾选条目属于规划意向, 不代表当前版本能力.
3. 条目前缀标明主要落点: `(插件)` 本仓库 (ONNX Runtime 版), `(旧插件)` 新仓库 `D:/idea-projects/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3-Paddle-Lite`, `(宿主)` `D:/idea-projects/AutoJs6`, `(索引)` `D:/idea-projects/AutoJs6-Official-Plugins-Index`, `(文档)` AutoJs6-Documentation / AutoJs6-TypeScript-Declarations / AutoJs6-Plugin-Ace-Editor / AutoJs6-Plugin-Offline-Docs, `(测试)` 真机或 AVD 验证, `(发布)` 版本, tag, Release 与索引.
4. 宿主侧提交只落本地, 由维护者合并与推送. 宿主工作区多会话共用: 只提交自己的文件, 不推送, 不切分支, 不碰其他会话在改的文件, 宿主构建与其他会话排队. 宿主 `.changelog` 本轮只写 zh-Hans, 其他语言由维护者同步.
5. 第 1 节 "固定决策" 由维护者 2026-10-29 经三轮选择题确认, 后续阶段不再重新讨论 (非推荐项已标注, 同样不再重问); 第 2 节 "派生技术决策" 可在进入对应阶段前推翻 (推翻点已逐条标注), 之后视同固定; 附录 D "待决事项" 在进入对应阶段前由维护者拍板 (调度会话用选择题提问), 拍板结果回填到附录 D 与对应决策行.
6. 本仓库的构建规则见 `AGENTS.md` (Conventional Commits, 每笔提交前 `VERSION_BUILD` = 当前提交数 + 1, `VERSION_CODE_OFFSET=25` 固定, 10 语言资源与生成器); P1 改写 `AGENTS.md` 时保留这些规则, 只替换 Paddle-Lite 相关段落. 旧插件新仓库沿用同一份规则, 改名字段见附录 C.
7. 2026-10-29 的立项会话只落盘本路线图并做一笔 `docs` 提交 (`VERSION_BUILD` 36 -> 38), 同时建看板 `D:/idea-projects/.claude/boards/paddle-ocr-v3.md`; 调度由维护者在新会话 (从 dispatch 环境启动) 输入 `/dispatch paddle-ocr-v3` 启用, 子会话用 claude-opus-5-5.

---

## 1. 固定决策

以下决策 D1-D13 已由维护者于 2026-10-29 分三轮确认. D5 与 D9 为非推荐项 (维护者主动选定), 其余为推荐项.

| 编号 | 决策 | 含义 |
| --- | --- | --- |
| D1 | 路线: 切换到 ONNX Runtime, 同时保留 Paddle-Lite 旧插件 | 新插件用 ONNX Runtime 官方 Android AAR (4 ABI) 跑 PP-OCRv3 ONNX 模型, 与 v4 / v5 / v6 同构; 旧 Paddle-Lite 实现不删, 改名后继续作为官方插件存在 (D7). 不自编译 Paddle-Lite x86 (附录 G). |
| D2 | 开发者与图标 | 新 ONNX Runtime 插件 `plugin_author` = `SuperMonster003`; 旧 Paddle-Lite 插件保持 `TonyJiangWJ`. 两者都是官方插件 (同一 GitHub 组织, 同一签名, 都登记官方索引), 图标一致 (同一 Icon Studio 配方与源图, 索引 `catalog-icons` 各登记一份). |
| D3 | 宿主打包 APK: 同步内嵌 ONNX Runtime 流水线 | 宿主新增 ONNX Runtime 版的内嵌 Paddle OCR 引擎 (D20), 打包目录增加对应变体 (D21), 打包出的 APK 在 4 ABI 上都能用 `ocr.paddle`. 不是 "只在宿主应用内经 Binder 使用". |
| D4 | 保留文字方向分类 (cls) | 新插件包含 `ch_ppocr_mobile_v2.0_cls` 的 ONNX 模型, 与旧 v3 行为一致 (旧引擎三模型 det / rec / cls 都加载); v4 SDK 没有 cls, 需补 (D16). 开关见附录 D Q1; 旧引擎虽加载 cls 但从未运行, 故缺省关闭 (附录 D Q11 (b)). |
| D5 | slim 档位: 用 ONNX Runtime 动态量化生成 int8 作 `OcrOptions.useSlim` 的 slim 档 (非推荐, 维护者选定) | 旧 v3 的 slim 是 Paddle 官方的 slim `.nb` 模型; 新插件没有官方 slim ONNX, 用 `onnxruntime.quantization.quantize_dynamic` 从 fp32 ONNX 生成 int8 (D19). 维护者已知这是非推荐项: 精度与速度必须真机实测 (P4.3), 不达标时按附录 D Q2 处理. |
| D6 | 新插件接管旧标识 | 包名 `io.github.supermonster003.autojs6.plugin.paddleocr.v3` (中文档), 仓库 `AutoJs6-Plugin-Paddle-OCR-PP-OCRv3`, `plugin_id` `paddle-ocr-pp-ocrv3`, 向导键 `official("paddleocr.v3")`, `plugin_engine` `paddle-ocr`, `plugin_variant` `v3` 全部由新 ONNX Runtime 插件继续使用; 用户升级即从 Paddle-Lite 换到 ONNX Runtime (versionCode 接续, D13). 索引 `retired-packages` 不适用 (旧包名没有退役). |
| D7 | 旧 Paddle-Lite 插件命名: 后缀 "PP-OCRv3 Paddle Lite" | 显示名 `Paddle OCR (PP-OCRv3 Paddle Lite)`, 仓库 `AutoJs6-Plugin-Paddle-OCR-PP-OCRv3-Paddle-Lite`, 包名 `io.github.supermonster003.autojs6.plugin.paddleocr.v3.paddlelite`, `plugin_id` `paddle-ocr-pp-ocrv3-paddle-lite`, `plugin_variant` `v3-paddle-lite`, 向导键 `official("paddleocr.v3.paddlelite")`. 全部改名字段见附录 C. |
| D8 | 宿主打包: 两套引擎都支持, 两者都装时优先 ONNX Runtime | 打包目录 `PADDLE_OCR` 同时保留 Paddle-Lite 变体 (改名 `v3-paddle-lite`) 与新增 ONNX Runtime 变体 (`v3`); 两个插件都安装时打包器选 ONNX Runtime 插件 (D21). 内嵌引擎按打包进来的资产自动识别用哪套 (D20). |
| D9 | 模型档位: mobile + 多语种 flavor (非推荐, 维护者选定) | 不做 server 档; 以 PP-OCRv3 mobile 模型为基础, 按语种拆 flavor (D10, D11). 推荐项 "只做中文 mobile 单档" 已放弃. |
| D10 | 2.0.0 语种范围: 中, 英, 繁中, 日, 韩 | flavor `zh` / `en` / `zhHant` / `ja` / `ko` 五个; 其余 7 种 (拉丁, 阿拉伯, 西里尔, 天城文, 泰卢固, 卡纳达, 泰米尔) 登记为 2.1.0 (P6). |
| D11 | 分包方式: 每语种独立 APK | 同 v4 `mobileEn` 模式: Gradle flavor + `applicationIdSuffix`, 每个 flavor 一个独立包 (可同时安装), `plugin_id` `paddle-ocr-pp-ocrv3-<lang>`, `plugin_variant` 统一 `v3`, capability `modelProfile = <lang>`; 中文档沿用无后缀旧标识 (D6) 并声明 `recommendedForMobileDefault = true`, 其他语种为 `false`. 身份表见 5.4. 2026-10-30 P5.3 修正: `productFlavors` 必须是 `create("<名>")` 字面量声明, 索引生成器从发布 tag 静态读取, 不执行 Gradle. |
| D12 | 最低 SDK 24 | 与旧 v3 和宿主一致 (v4 是 26); ONNX Runtime 1.21.1 Android 最低 API 21, OpenCV 4.8.0 Java AAR 最低 API 21; API 24 用 AVD 验证 (附录 F). |
| D13 | 版本号: 新插件 2.0.0, 旧插件 1.1.0 | 本仓库 `VERSION_NAME=2.0.0`, `VERSION_BUILD` 按提交数接续 (本次提交 38, versionCode 63; 发布时按当时提交数), `VERSION_CODE_OFFSET=25` 不变, 保证从 1.0.6 (61) 升级; 旧插件新仓库 `git clone` 带完整历史, `VERSION_NAME=1.1.0`, versionCode 延续方式见附录 D Q4. |

---

## 2. 派生技术决策

D14-D38 据第 1 节派生, 进入对应阶段前可推翻 (推翻点见各条), 之后视同固定. 实现中如有偏差逐条回填.

| 编号 | 决策 | 含义 | 推翻点 |
| --- | --- | --- | --- |
| D14 | ONNX Runtime `1.21.1` + Java API | `com.microsoft.onnxruntime:onnxruntime-android:1.21.1` (与 v4 及 Rapid OCR 插件一致; 宿主打包时同名 `libonnxruntime.so` 只能有一份, 版本必须与 Rapid 锁定, 升级时三处同步). AAR 原生库: `libonnxruntime.so` (arm64 17.9 / armv7 13.0 / x86 21.2 / x86_64 21.4 MB) 与 `libonnxruntime4j_jni.so` (Java API 必需, 74-101 KB), 4 ABI 齐全 (2026-10-29 在本地 Gradle 缓存核对). | P1.1 |
| D15 | OpenCV: 插件内自带 4.8.0 Java AAR, 宿主侧复用宿主自带 | 插件复制 v4 的 `libs/org-opencv-4_8_0` (含 `libopencv_java4.so` 4 ABI, 20.4 / 14.3 / 39.0 / 53.2 MB), 与 v4 相同; 宿主内嵌引擎用宿主已有的 OpenCV Java API (`libs/org-opencv-java-4_8_0`), 打包时 `libopencv_java4.so` 按 `neededOnlyLibsToInclude` 复制 (与 Rapid 变体一致). 不像旧 v3 那样把 OpenCV 静态链进私有 `.so`. | P1.1 |
| D16 | 推理代码: 复制 v4 `libs/ppocr-android-sdk` 并补 cls 与 slim | 包 `com.paddle.ocr` 改为 `io.github.supermonster003.autojs6.plugin.paddleocr.v3.sdk` (避免与 v4 插件在宿主打包时同名类冲突); 新增 `ClassificationEngine` (cls 输入 3x48x192, 输出 2 类, 角度 180 时旋转; 实现参照 PaddleOCR `ppocr/postprocess/cls_postprocess.py` 与 Rapid OCR C++ `AngleNet`), `OCREngine` 流水线改为 det -> (cls) -> rec; `EngineConfig` 增加 `useSlim` (切换模型目录) 与 `useCls`. v4 的 `ppocrv4-plugin-runtime` (服务, `EngineHolder`, `ImageFdDecoder`, `ImageInputBounds`) 同样复制改包名. | P1.2 |
| D17 | 资产布局: 每个 flavor 固定路径 | `app/src/<flavor>/assets/models/ppocrv3/det/inference.onnx`, `rec/inference.onnx`, `rec/inference.yml` (含 `character_dict`, v4 做法), `cls/inference.onnx`; slim 档位 `assets/models/ppocrv3-slim/{det,rec}/inference.onnx` (cls 不量化, 共用). 路径不带语种, 所以宿主打包目录只需一个 ONNX Runtime 变体清单 (D21), 任一语种插件都能打包. 模型文件不入库 (v4 做法: `.gitignore` 排除 `app/src/*/assets/models/`), 由 P0 脚本生成, 来源记录入库 (D18). | P0.1 |
| D18 | 模型来源与转换 | det: 中文 `PP-OCRv3/chinese/ch_PP-OCRv3_det_infer.tar` (3.8 MB), 英文 `english/en_PP-OCRv3_det_infer.tar` (3.8 MB), 繁中 / 日 / 韩 `multilingual/Multilingual_PP-OCRv3_det_infer.tar` (3.7 MB); rec: `chinese/ch_PP-OCRv3_rec_infer.tar` (11.9), `english/en_PP-OCRv3_rec_infer.tar` (9.5), `multilingual/chinese_cht_PP-OCRv3_rec_infer.tar` (11.8), `japan_PP-OCRv3_rec_infer.tar` (10.8), `korean_PP-OCRv3_rec_infer.tar` (10.4); cls: `dygraph_v2.0/ch/ch_ppocr_mobile_v2.0_cls_infer.tar` (2.2); 字典: PaddleOCR 仓库 `ppocr/utils/ppocr_keys_v1.txt`, `en_dict.txt`, `dict/chinese_cht_dict.txt`, `dict/japan_dict.txt`, `dict/korean_dict.txt` (基址 `https://paddleocr.bj.bcebos.com/`, 2026-10-29 全部 HTTP 200). 转换用 `paddle2onnx==1.3.1` (v4 脚本的 fallback venv, `--opset_version 7`), 脚本 `scripts/prepare_ppocrv3_assets.py --profile <lang>|all` 从 v4 `prepare_ppocrv4_assets.py` 改写; `libs/ppocr-android-sdk/models.provenance.json` 按 Rapid OCR `models.provenance.json` 格式记录每个文件的 URL, SHA-256, 转换命令与 opset. | P0.1 |
| D19 | slim 生成 (D5) | `prepare_ppocrv3_assets.py --slim` 对 det 与 rec 的 fp32 ONNX 先 `quant_pre_process` (`skip_symbolic_shape=True`) 再调 `onnxruntime.quantization.quantize_dynamic` (`weight_type=QUInt8`, 只量化 MatMul 与权重不少于 100000 个元素的 Conv, 小 Conv 保持 fp32, 见附录 D Q10; 2026-10-30 P0.2 实施), 输出到 `ppocrv3-slim/`; 量化参数与 onnxruntime Python 版本写入 provenance. 验收 (P4.3): 同一图集下 slim 与 fp32 的文本一致率不低于 95%, rec 平均耗时下降; 不达标按附录 D Q2. | P0.2 |
| D20 | 宿主内嵌 ONNX Runtime 引擎 | 宿主新增模块 `plugin-api/paddle-ocr-onnx-engine` (源码复制自本仓库 `libs/ppocr-android-sdk`, 包 `org.autojs.plugin.paddle.ocr.onnx`; 不含模型与原生库), 依赖 `onnxruntime-android:1.21.1` 的 Java 类但排除其 `jni/` (Gradle `packaging.jniLibs.excludes` 或按 Rapid 插件的 `@aar` + 解包方式只取 classes), 原生库与模型由打包时从插件复制; OpenCV 走宿主自带 Java API. `PaddleOcrEmbeddedEngine` 增加 ONNX Runtime 候选 (条件: `nativeLibraryDir` 含 `libonnxruntime.so` + `libonnxruntime4j_jni.so`, assets 含 `models/ppocrv3/det/inference.onnx`), 排在 Paddle-Lite 候选之前 (D8); `useSlim` 在 slim 目录存在时生效, 否则回退 fp32. | P3.1 |
| D21 | 宿主打包目录两变体 | `ApkBuildLibraryCatalog.PADDLE_OCR.variants`: 新增 `variant = "v3"` (`assetsToInclude` 必含 `assets/models/ppocrv3/`, 可选 `assets/models/ppocrv3-slim/`; `libsToInclude` `libonnxruntime.so`, `libonnxruntime4j_jni.so`, `libc++_shared.so`; `neededOnlyLibsToInclude` `libopencv_java4.so`), 原 Paddle-Lite 条目改为 `variant = "v3-paddle-lite"` (清单不变: `assets/labels/ppocr_keys_v1.txt`, `assets/models/ocr_v3_for_cpu/`, 可选 slim 目录, `libc++_shared.so`, `libpaddle_light_api_shared.so`, `libNative.so`, neededOnly `libopencv_java4.so`). 变体选择 (`selectBestPluginVariantCandidate`) 在多个候选时按 variants 列表顺序取第一个命中的 (ONNX Runtime 在前), 并把注释 "Packaged applications run the embedded Paddle Lite engine only" 改为两套引擎的说明; `docs/dev/opencv-ocr-runtime-decoupling-roadmap.md` D10 行加注 (v4-v6 仍不打包). | P3.2 |
| D22 | 宿主默认插件选择: 平手时看 `recommendedForMobileDefault` | `OcrPluginHost` 无显式条件且优先级存储为空时, 现为 `maxBy` variant 中的数字 (`v3` 与 `v3-paddle-lite` 同为 3, 五个语种 flavor 同为 `v3`, 顺序不确定). 新规则: 数字平手时优先 capability `recommendedForMobileDefault = true` 的候选 (中文档 ONNX Runtime 插件), 仍平手时按包名排序取稳定结果. 旧 Paddle-Lite 插件不声明该键, 自然落后. | P3.3 |
| D23 | `profile` 选项参与插件匹配 | 脚本 `ocr.paddle(img, { profile: "ja" })` 现只把 `PROFILE` 透传给插件 (`PaddleOcrOptionExtraKeys.PROFILE`), 宿主不按它选插件. 新规则: `matchesSelectionCriteria` 增加 `profile` 条件, 与插件 capability `modelProfile` 比较; 插件未声明 `modelProfile` 时该条件视为不匹配 (有显式 profile 就必须命中); v4 (`mobile` / `server` / `mobile-en`) 与 v5 / v6 的 profile 值同样可用. `hasExplicitSelectionCriteria` 同步. Node / Bun 桥已透传 `profile`, 不需改 (2026-10-30 P5.1 修正: 此说法在宿主 bb7e2fe53 之前不成立. 桥只把 `profile` 透传给插件, 自动模式 `selectForCall` 与 Node 桥选插件时都没传它, 所以 `ocr.detect(img, { engine, profile })` 与 Node / Bun 都不按 `profile` 选插件; bb7e2fe53 补上两处, Rhino 已真机验证, Node 桥只有编译证据). | P3.3 |
| D24 | 插件能力声明 | 新插件 `getInfo`: `id` 按 flavor, `engine = paddle-ocr`, `variant = v3`, `supportedAbis` 4 项, `author = SuperMonster003`; capabilities: `REQUIRES_HOST_VERSION` (P3 落地后回填为支持 D22 / D23 的宿主 versionCode, 之前临时 3835; 2026-10-30 已回填 5935 = 宿主 VERSION_BUILD 4283 + 1652, 即宿主 b2dd1757b 及之后的本地提交, 插件 c9b17bd. 宿主 6.7.0 没有 OCR 插件的宿主版本门槛, 2.0.0 照常可用; 2026-07 起的宿主 (`OcrPluginHost.ensureHostVersionCompatible`) 低于 5935 时拒绝调用并提示宿主版本过低, 之后的设备验证需宿主 >= 5935), `SUPPORTS_RAW_IMAGE = true`, `SUPPORTS_TEXT_DETECTION` / `SUPPORTS_TEXT_RECOGNITION` / `SUPPORTS_TEXTLINE_ORIENTATION_CLASSIFICATION` 全 `true`, `modelProfile = <lang>`, `recommendedForMobileDefault` (zh `true`). 旧插件: 只改 `variant = v3-paddle-lite` 与 `id`, 其余 (`REQUIRES_HOST_VERSION 3835`, `SUPPORTS_RAW_IMAGE`) 不变. | P1.3 |
| D25 | `OcrOptions` 到 ONNX Runtime 的映射 | `cpuThreadNum` -> `SessionOptions.setIntraOpNumThreads` (0 或负数用 4, 旧 v3 引擎默认); `useSlim` -> slim 目录 (D19, cls 共用 fp32); `useOpenCL` -> NNAPI 执行提供器 (附录 D Q6 (b): API < 27 或 NNAPI 建会话失败时回退 CPU 并打一条日志; 结果 extras `executionProvider` 报告实际使用的 `cpu` / `nnapi`); extras `DET_LIMIT_SIDE_LEN` > 0 优先, 否则 `detLongSize` > 0, 否则 960 -> det `limit_side_len` (`limit_type = max`, 与旧 v3 的 `det_long_size` 语义一致); `scoreThreshold` -> rec 分数过滤 (>= 0 用给定值, 宿主未设置时传 -1, 此时用 0.1, 与旧 v3 引擎 `Predictor` 默认一致; 2026-10-30 P1.2 反编译旧引擎核对, 原写 "默认 0" 有误); extras `USE_CLS` -> 方向分类 (附录 D Q1 (c); 缺省 `false`, 与旧 v3 实际行为一致, 附录 D Q11 (b)); extras `RAW_IMAGE` 系列 -> `ImageFdDecoder` (v4 原样); det 阈值 0.3 / box 0.5 / unclip 1.6 沿用 v4 默认, extras `detLimitType` / `detMaxSideLimit` / `detThresh` / `detBoxThresh` / `detUnclipRatio` / `recBatchSize` 与 v4 相同. 映射实现为纯函数 `PpOcrV3EngineSettings.resolve`. | P1.2 |
| D26 | APK 形态: 每 flavor 4 ABI 拆分 + universal | `splits.abi` include 4 ABI, `isUniversalApk = true` (与 v4 一致), 5 个 flavor 每版 25 个 APK; 文件名 `autojs6-plugin-paddle-ocr-pp-ocrv3-v2.0.0-<flavor>-<abi>-<CRC32>.apk` (`release_archive.py` 已支持同版本多 flavor 时加 flavor 后缀; 2026-10-30 P5.3 修正: 文件名里的 flavor 用 kebab-case, 即 `zh-hant`, 索引生成器按这个写法把资源归到分发变体, 此前归档为 `zhhant`, 附录 F 的摘要是当时的文件). 预估单 ABI APK: arm64 约 55 MB (ONNX Runtime 18 + OpenCV 20.4 + 模型 16 + 其他), x86_64 约 90 MB; universal 约 200 MB. 是否保留 universal 见附录 D Q3. 2026-10-30 release 实测 (5 个 flavor 的范围): arm64-v8a 30.5 - 33.0 MB, armeabi-v7a 29.0 - 31.5 MB, x86 39.1 - 41.6 MB, x86_64 44.7 - 47.1 MB, universal 94.7 - 97.2 MB, 均小于上面的预估. | P1.4 |
| D27 | 旧插件迁移方式 | 子会话 `git clone` 本仓库 (迁移前的 `bc01d0a` 或其后只含路线图的提交) 到 `D:/idea-projects/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3-Paddle-Lite`, 删除 `ROADMAP.md` (属于本仓库), 按附录 C 改名 (23 个含标识文件 + `.icons/recipe.json` `packages` + `AGENTS.md` + `.readme` / `.changelog` 内容 + 测试夹具), `VERSION_NAME=1.1.0`, changelog 1.1.0 只写 "改名与新旧关系", 不加功能; remote 由维护者在 GitHub 创建后添加 (维护者待办). 之后只修 bug. | P2.1 |
| D28 | 本仓库历史处理 | 本仓库保留全部旧历史继续提交 (不重建, 不 force push); P1 删除 Paddle-Lite 相关内容 (`libs/paddleocr` 原生模块与 `PaddleLite/`, `tools/jni`, `tools/opencv`, `libs/paddle-ocr-engine.aar`, `app/src/main/java/org` 下的 Paddle-Lite 桥接类), `docs/16kb.md` 改写为 ONNX Runtime 的对齐说明 (v4 `docs/16kb.md` 为模板), `libs/opencv-android-sdk-4.8.0.provenance.json` 由 Java AAR 的来源记录替代. | P1.1 |
| D29 | 索引登记 | 新包 (5 个 flavor 包名) 与旧插件新包名各新增 `release-manifests/<package>/<versionCode>.json`; `catalog-icons.json` 目前没有任何 `paddleocr.*` 条目 (2026-10-29 核对), 两个仓库的图标都要新登记; `official-repositories.json` 加 `AutoJs6-Plugin-Paddle-OCR-PP-OCRv3-Paddle-Lite` (当前 51 条 -> 52); `retired-packages.json` 不改 (D6). 运行 `tools/generate_official_plugin_index.py` 与单元测试. | P5.3 |
| D30 | 安装向导条目 | 宿主 `PluginInstallWizardCatalog`: `official("paddleocr.v3")` 条目保留 (现在指向 ONNX Runtime 中文档), 新增 `entry(official("paddleocr.v3.paddlelite"), "Paddle OCR PP OCRv3 Paddle Lite", IMAGE)`; 其他语种 flavor 不进向导 (与 v4 `mobile.en`, v5 语种包一致; 附录 D Q7). `InstalledPluginRepository` 与 `<queries>` 若按包名枚举则加新包名. | P3.4 |
| D31 | 文档与声明 | Documentation `api/ocr.md` (paddle 引擎段: v3 现为 ONNX Runtime 4 ABI, 五个语种档, Paddle Lite 旧插件与 `variant: "v3-paddle-lite"`), `api/ocrOptionsType.md` (`variant` 补 `v3-paddle-lite`; `profile` 补 "参与插件匹配" 与 v3 档位值 `zh` / `en` / `zh-hant` / `ja` / `ko`), d.ts `DetectOptionsPaddle.profile` 注释 (类型仍为 `string`), Ace Editor 与 Offline Docs 同步; 宿主 `.changelog` zh-Hans; 本仓库 README 10 语言 (生成器) 与 2.0.0 changelog; 旧插件 README 说明新旧关系并互相链接. | P5.1 |
| D32 | CI | `.github/workflows/build.yml` 改为: `prepare_ppocrv3_assets.py --profile zh` (缓存模型), `:app:assembleZhDebug` + 单元测试 + `assembleZhDebugAndroidTest`, 模拟器矩阵 x86_64 (含 16 KB page-size 镜像) 跑 `connectedZhDebugAndroidTest` (v4 `build.yml` 为模板); `icon-studio.yml` 与 `markdown.yml` 不变. 发布前本地跑 `--profile all` + `assembleRelease` 5 个 flavor. | P1.5 |
| D33 | 测试 | 单元测试: 契约字面值与 `PluginInfo` 映射, flavor 资产校验 (Gradle 配置期检查每个 flavor 的 4 个模型文件存在), `OcrOptions` 映射, cls 后处理; instrumentation: `PluginBinderContractTest` (v4 复制改名) + 五语种各一张样图的端到端识别; 真机 / AVD 矩阵见附录 F. 新旧对比: 同一图集在旧 Paddle-Lite 插件 (改名前 APK 1.0.6) 与新插件上的文本一致率与耗时 (P4.2). | P1.5 |
| D34 | 精度与速度基线 | 图集: 宿主 `paddle_ocr_test.png` + 五语种各 2 张截图 (放 `.bak/visual/`, 不入库; 清单与 SHA-256 入 `docs/benchmark.md`); 指标: 文本一致率 (与 fp32 新插件的输出逐行比较), det + rec 平均耗时 (10 次取中位数), 在 XQ-AT72 (arm64) 与 x86_64 AVD 各测 fp32 与 slim; 结果写附录 F 表. | P4.3 |
| D35 | 版本与构建号 | 本次 docs 提交 `VERSION_BUILD=38`; P1 第一笔提交把 `VERSION_NAME` 改为 `2.0.0`; versionCode 对 5 个 flavor 相同 (v4 做法), 索引清单按包名各登记一份同 versionCode. | P1.1 |
| D36 | 16 KB 页对齐 | ONNX Runtime 1.21.1 AAR 的 `.so` 与 OpenCV 4.8.0 Java AAR 的 `.so` 已随 v4 1.0.4 四 ABI 发布且通过 v4 的对齐校验 (本仓库 `tools/16kb` 与 `release_archive.py` 的 ELF / ZIP 对齐检查沿用); P0.3 用 `tools/16kb` 复核 ONNX Runtime 4 ABI 原生库. | P0.3 |
| D37 | Node / Bun 桥与 api-coverage | `ocr` 模块签名不变, `profile` 已经桥透传, 不改桥; api-coverage 门禁只在文档页改动时重跑 (P5.1). 2026-10-30 P5.1 修正: 桥选插件时此前没传 `profile` (同 D23), 宿主 bb7e2fe53 在 `NodeBridgeProtocol` 补上, 这一行只有编译证据; 所以 "不改桥" 不成立. Node / Bun 结果的 extras 由 Q26 (b) 另行处理. | P5.1 |
| D38 | 许可证与第三方记录 | 新插件: ONNX Runtime MIT, OpenCV Apache-2.0, PP-OCRv3 模型 Apache-2.0 (PaddleOCR), `THIRD_PARTY_NOTICES` 段落与 README "第三方来源" 更新 (`AGENTS.md` 要求来源记录同步); 旧插件保持原记录 (Paddle-Lite Apache-2.0). | P1.4 |

---

## 3. 范围与非目标

范围 (本仓库 2.0.0, 旧插件 1.1.0, 宿主 6.8.0):

- 本仓库: ONNX Runtime 1.21.1 + OpenCV 4.8.0 Java AAR, det / cls / rec 三模型, fp32 与 slim (int8 动态量化) 两档, 5 个语种 flavor, 4 ABI + universal, `OcrOptions` 全部字段映射, 原始图 (`RAW_IMAGE`) 路径, `WakeActivity`, 10 语言资源与 README / changelog, Icon Studio 配方 (`packages` 扩到 5 个包名), 单元测试 + instrumentation + CI.
- 旧插件: 带历史复制到新仓库, 改名 (附录 C), 1.1.0 发布, 索引登记; 功能不变.
- 宿主: 内嵌 ONNX Runtime 引擎模块, 打包目录两变体 (优先 ONNX Runtime), 默认选择平手规则 (D22), `profile` 参与匹配 (D23), 向导条目 (D30), 注释与 D10 文档加注, zh-Hans changelog, 单元测试, 打包 APK 真机验证.
- 文档: `ocr.md`, `ocrOptionsType.md`, d.ts, Ace / Offline 同步.
- 索引: 6 个包名的清单与图标, 仓库列表 +1.

非目标 (不做或排到之后, 评估记录见附录 G):

- 其余 7 个语种 (2.1.0, P6); server 档; PP-OCRv4 / v5 / v6 的打包支持 (D10 维持); GPU / NNAPI 执行提供器; Paddle-Lite x86 自编译; 把 Rapid OCR 与本插件合并; 旧 Paddle-Lite 插件的新功能.
- 单 APK 内置多语种 (D11 已选独立 APK); 宿主自带 PP-OCRv3 模型 (打包 APK 仍从插件复制).

---

## 4. 现状诊断

### 4.1 可直接复用

- v4 仓库 `libs/ppocr-android-sdk` (`com.paddle.ocr`: `PaddleOCR`, `EngineConfig`, `engine/{DetectionEngine, RecognitionEngine, OCREngine, ORTSessionManager}`, `postprocess/{DBPostProcessor, PolygonUnclip, CTCDecoder, BoxSorter, QuadTextCrop}`, `preprocess/{DetPreprocessor, RecPreprocessor}`, `util/{OpenCVUtils, YamlUtils, ...}`; 无 cls) 与 `libs/ppocrv4-plugin-runtime` (`PpOcrV4PluginService` 能力声明, `PpOcrV4EngineHolder` extras 解析与 `detMaxSideLimit 4000`, `ImageFdDecoder`, `ImageInputBounds`, `InstalledPackageIdentity`, `jniLibs/libc++_shared.so` 4 ABI + provenance), `libs/org-opencv-4_8_0` (Java AAR), `scripts/prepare_ppocrv4_assets.py` (下载, 解包, paddle2onnx 转换, 字典写入 yml), `app/build.gradle.kts` flavor 模板 (`mobileEn`), `.github/workflows/build.yml` (准备资产 + 模拟器矩阵), `docs/16kb.md`, `app/src/androidTest/.../PluginBinderContractTest.java`.
- 本仓库: `AGENTS.md` 规则, `.python/` 生成器与 `release_archive.py` (多 flavor 文件名已支持), `.icons/recipe.json` (generatorVersion 1.3.0, `profile = catalog`, `systemIcon = true`, 源图 SHA-256 `38064bef...`), `.readme` / `.changelog` 10 语言, `app/src/main/.../OcrService.java` 的能力声明与 `WakeActivity.java`, `tools/16kb`.
- Rapid OCR PP-OCRv3 插件: ONNX Runtime 1.21.1 的 `@aar` 解包用法 (`libs/rapidocr/build.gradle.kts:72-77`), `models.provenance.json` 格式, 预转换的 PP-OCRv3 中文 ONNX (det 2432880 B, rec 10690752 B, cls) 可作转换结果的对照.
- 宿主: `plugin-api/paddle-ocr-api` (AIDL `IOcrPlugin` / `OcrOptions` / `OcrResult`, `PaddleOcrOptionExtraKeys`, `PaddleOcrPluginCapabilityKeys`), `OcrPluginHost` (发现, 匹配, 优先级, `SharedMemory` 传图), `PaddleOcrEmbeddedEngine` 候选机制 (`embeddedVariantCandidates` 按资产存在性选择), `ApkBuildLibraryCatalog` 的 Rapid 变体 (ONNX Runtime 原生库清单与 `neededOnly` OpenCV), `libs/org-opencv-java-4_8_0` 与 `plugin-api/opencv-api` (`NATIVE_LIBRARY_FILE_NAME`), `OcrPaddle.kt` 的 `isInrt` 分支.
- 索引: `tools/generate_official_plugin_index.py` + 测试, v4 三个 flavor 包与 v5 语种包的清单作为多包登记先例.

### 4.2 缺口 (需要新建或修改)

- 本仓库: 全部 Paddle-Lite 代码 (`libs/paddleocr` CMake 原生模块, `PaddleLite/`, `libNative.so` 构建链, `tools/jni`, `tools/opencv`), `abiFilters` / `splits` 只有 2 ABI, 无 flavor, 无 ONNX 资产脚本, 无 cls / slim 的 ONNX 实现, `plugin_author` 为 TonyJiangWJ, `.icons/recipe.json` `packages` 只有 1 个包名.
- 旧插件新仓库: 尚不存在; 改名清单附录 C.
- 宿主: 无 `onnxruntime` 依赖 (只在打包策略测试与目录里出现文件名), 无 ONNX Runtime 版内嵌引擎, 打包目录只有 Paddle-Lite 变体, 默认选择无平手规则, `profile` 不参与匹配, 向导无 Paddle Lite 条目.
- 索引: 无任何 `paddleocr.*` 图标登记, 无新包名清单, 仓库列表无 Paddle-Lite 仓库.
- 文档: `ocr.md` / `ocrOptionsType.md` / d.ts 不知道 `v3-paddle-lite` 与 v3 的 profile 值.

### 4.3 外部事实

- Paddle-Lite 官方 Android 预编译只有 armv7 / armv8, 无 x86 系列; 旧 v3 的 `libNative.so` 静态链接 OpenCV 并依赖 `libpaddle_light_api_shared.so`, `.nb` 模型与 Paddle-Lite 绑定, 所以 x86 / x86_64 不可能在不换运行时的前提下补齐.
- ONNX Runtime 1.21.1 Android AAR 含 4 ABI 的 `libonnxruntime.so` 与 `libonnxruntime4j_jni.so`; Java API 走 `ai.onnxruntime.OrtEnvironment` / `OrtSession`, 必须有 jni 库.
- PP-OCRv3 官方模型与字典全部可下载 (D18 列表, 2026-10-29 HTTP 200); `paddle2onnx 1.3.1` 能转换 PP-OCRv3 det / rec / cls (Rapid OCR 的预转换 ONNX 证明可行).
- 本地 Gradle 缓存已有 `onnxruntime-android:1.21.1` AAR (v4 与 Rapid 构建过), 无需联网即可开始 P1.
- 索引清单 `supportedAbis` 为 4 项时与 v4 / v5 / v6 一致; 旧 v3 1.0.5 清单为 2 项.

---

## 5. 目标架构

### 5.1 数据流 (宿主应用内)

```text
脚本 ocr.paddle(img, { profile: "ja", useSlim: true })
  -> OcrPaddle.detectImpl: OcrPluginHost.selectOrThrow(engine = paddle-ocr, variant?, profile = "ja")   (D23)
     候选: paddleocr.v3 (zh, recommended) / .v3.en / .v3.zhhant / .v3.ja / .v3.ko / .v3.paddlelite (v3-paddle-lite)
     无显式条件时: 优先级存储 -> variant 数字 -> recommendedForMobileDefault -> 包名   (D22)
  -> Binder: IOcrPlugin.detect(bitmap 或 RAW_IMAGE fd, OcrOptions)
插件进程 (flavor ja): PpOcrV3EngineHolder -> OCREngine(det -> cls -> rec) on ONNX Runtime 1.21.1 (CPU EP, intra-op = cpuThreadNum)
     useSlim -> models/ppocrv3-slim/{det,rec}, 否则 models/ppocrv3/{det,rec}; cls 固定 models/ppocrv3/cls
  <- OcrResult[] (text, confidence, bounds)
```

### 5.2 数据流 (打包 APK)

```text
打包器: ApkBuildLibraryCatalog.PADDLE_OCR -> 已安装候选: v3 (ONNX Runtime, 任一语种) 优先于 v3-paddle-lite   (D8, D21)
  复制 assets/models/ppocrv3/ (+ ppocrv3-slim/) 与 libonnxruntime.so, libonnxruntime4j_jni.so, libc++_shared.so, (需要时) libopencv_java4.so
运行时 (isInrt): PaddleOcrEmbeddedEngine.resolve -> ONNX Runtime 候选 (资产 + 原生库齐) > Paddle-Lite v5 > Paddle-Lite v3   (D20)
  -> plugin-api/paddle-ocr-onnx-engine (与插件同一份流水线代码) -> OcrResult[]
```

### 5.3 包结构

本仓库 (ONNX Runtime 版):

```text
app/src/main/java/io/github/supermonster003/autojs6/plugin/paddleocr/v3/
  OcrService.java (或 .kt)        IOcrPlugin.Stub: getInfo (flavor 身份), capabilities (D24), recognizeText / detect -> EngineHolder
  WakeActivity                    与 v4 一致
app/src/{zh,en,zhHant,ja,ko}/assets/models/ppocrv3/{det,rec,cls}/inference.onnx, rec/inference.yml; ppocrv3-slim/{det,rec}/inference.onnx   (不入库)
libs/ppocr-android-sdk/            推理流水线 (D16), models.provenance.json, build.gradle.kts (onnxruntime-android 1.21.1, :libs:org-opencv-4_8_0)
libs/ppocrv3-plugin-runtime/       服务骨架, EngineHolder, ImageFdDecoder, jniLibs/libc++_shared.so (4 ABI)
libs/org-opencv-4_8_0/             OpenCV 4.8.0 Java AAR 模块 (v4 复制)
libs/common-plugin-api.aar, libs/paddle-ocr-api.aar
scripts/prepare_ppocrv3_assets.py  下载 / 转换 / 量化 / 写 yml
.python/, .icons/, .readme/, .changelog/, .github/workflows/, docs/16kb.md, docs/benchmark.md, tools/16kb
```

旧插件新仓库 (`AutoJs6-Plugin-Paddle-OCR-PP-OCRv3-Paddle-Lite`): 本仓库 `bc01d0a` 的完整内容按附录 C 改名, 目录结构不变.

宿主 (`D:/idea-projects/AutoJs6`):

```text
plugin-api/paddle-ocr-onnx-engine/                       D20 (settings.gradle.kts 登记, app/build.gradle.kts 依赖)
app/src/main/java/org/autojs/autojs/runtime/api/modules/ocr/PaddleOcrEmbeddedEngine.kt   ONNX Runtime 候选
app/src/main/java/org/autojs/autojs/apkbuilder/ApkBuildLibraryCatalog.kt                 两变体 (D21)
app/src/main/java/org/autojs/autojs/core/plugin/ocr/OcrPluginHost.kt                     D22 / D23
app/src/main/java/org/autojs/autojs/core/plugin/center/wizard/PluginInstallWizardCatalog.kt  D30
docs/dev/opencv-ocr-runtime-decoupling-roadmap.md (D10 加注), .changelog (zh-Hans), 单元测试 (ApkBuilderLibPolicyTest 等)
```

### 5.4 身份派生表 (本仓库 5 个 flavor)

| flavor | `applicationIdSuffix` | 包名 | `plugin_id` | `app_name` | `modelProfile` | `recommendedForMobileDefault` | det 来源 | rec 来源 | 字典 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `zh` (默认) | 无 | `io.github.supermonster003.autojs6.plugin.paddleocr.v3` | `paddle-ocr-pp-ocrv3` | `Paddle OCR (PP-OCRv3)` | `zh` | `true` | ch_PP-OCRv3_det | ch_PP-OCRv3_rec | ppocr_keys_v1 |
| `en` | `.en` | `...paddleocr.v3.en` | `paddle-ocr-pp-ocrv3-en` | `Paddle OCR (PP-OCRv3 EN)` | `en` | `false` | en_PP-OCRv3_det | en_PP-OCRv3_rec | en_dict |
| `zhHant` | `.zhhant` | `...paddleocr.v3.zhhant` | `paddle-ocr-pp-ocrv3-zh-hant` | `Paddle OCR (PP-OCRv3 ZH-Hant)` | `zh-hant` | `false` | Multilingual_PP-OCRv3_det | chinese_cht_PP-OCRv3_rec | chinese_cht_dict |
| `ja` | `.ja` | `...paddleocr.v3.ja` | `paddle-ocr-pp-ocrv3-ja` | `Paddle OCR (PP-OCRv3 JA)` | `ja` | `false` | Multilingual_PP-OCRv3_det | japan_PP-OCRv3_rec | japan_dict |
| `ko` | `.ko` | `...paddleocr.v3.ko` | `paddle-ocr-pp-ocrv3-ko` | `Paddle OCR (PP-OCRv3 KO)` | `ko` | `false` | Multilingual_PP-OCRv3_det | korean_PP-OCRv3_rec | korean_dict |

共同项: `plugin_engine = paddle-ocr`, `plugin_variant = v3`, `plugin_author = SuperMonster003`, cls 共用 `ch_ppocr_mobile_v2.0_cls`, versionCode 相同 (D35), 向导只登记 `zh` (D30), `.icons/recipe.json` `packages` 列出 5 个包名, 索引清单 5 份.

### 5.5 身份派生表 (旧插件)

| 项 | 值 |
| --- | --- |
| 仓库 | `AutoJs6-Plugin-Paddle-OCR-PP-OCRv3-Paddle-Lite`, 根项目名 `autojs6-plugin-paddle-ocr-pp-ocrv3-paddle-lite` |
| 包名 / namespace / Java 包 | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.paddlelite` |
| `app_name` | `Paddle OCR (PP-OCRv3 Paddle Lite)` |
| `plugin_id` / `plugin_engine` / `plugin_variant` | `paddle-ocr-pp-ocrv3-paddle-lite` / `paddle-ocr` / `v3-paddle-lite` |
| `plugin_author` | `TonyJiangWJ` |
| 向导键 | `official("paddleocr.v3.paddlelite")`, 回退标题 `Paddle OCR PP OCRv3 Paddle Lite`, 分类 `IMAGE` |
| 版本 | `VERSION_NAME=1.1.0`, `VERSION_BUILD` = 新仓库提交数 + 1, `VERSION_CODE_OFFSET` 见附录 D Q4 |
| 发布文件名 | `autojs6-plugin-paddle-ocr-pp-ocrv3-paddle-lite-v1.1.0-<abi>-<CRC32>.apk` (universal, arm64-v8a, armeabi-v7a) |
| 索引清单 | `release-manifests/io.github.supermonster003.autojs6.plugin.paddleocr.v3.paddlelite/<versionCode>.json`, `supportedAbis` 2 项 |
| 图标 | 与本仓库同一配方与源图, `packages` 改为新包名 |

### 5.6 宿主打包变体清单 (D21)

| variant | 必含 assets | 可选 assets | libs | neededOnly |
| --- | --- | --- | --- | --- |
| `v3` (ONNX Runtime, 任一语种 flavor) | `assets/models/ppocrv3/` | `assets/models/ppocrv3-slim/` | `libonnxruntime.so`, `libonnxruntime4j_jni.so`, `libc++_shared.so` | `libopencv_java4.so` |
| `v3-paddle-lite` (旧插件) | `assets/labels/ppocr_keys_v1.txt`, `assets/models/ocr_v3_for_cpu/` | `assets/models/ocr_v3_for_cpu(slim)/` | `libc++_shared.so`, `libpaddle_light_api_shared.so`, `libNative.so` | `libopencv_java4.so` |

---

## 6. 阶段总览

| 阶段 | 落点 | 主题 | 状态 |
| --- | --- | --- | --- |
| P0 | 插件 | 资产流水线: 下载, 转换, 字典, slim 量化, provenance, 16 KB 复核 | 已完成 (67d710d) |
| P1 | 插件 | 本体改造: 删 Paddle-Lite, ONNX Runtime SDK + cls + slim, 5 flavor, 服务与能力, 测试, CI, 图标, 文档资源 | 已完成 (b9fa0cc, c9b17bd) |
| P2 | 旧插件 | 带历史复制到新仓库, 改名, 1.1.0 构建与验证 | 已完成: P2.1 (新仓库 ca42783 / dd8e558 / 688983d, 发布前改邮箱后为 ca76366 / cc2208c / ebf6acb, 见 P5.2), P2.2 (Pad 共存验证) |
| P3 | 宿主 | 内嵌 ONNX Runtime 引擎, 打包两变体, 默认选择与 profile 匹配, 向导, changelog, 单测 | 已完成: P3.1 - P3.4 (宿主本地 9 笔, f38abc036 - bfc871fae), P3.5 (宿主本地 f3aa53bb0 / 5737cbdc1) |
| P4 | 测试 | 设备矩阵, 新旧对比, 精度与速度基线, slim 判定, 打包 APK 两引擎 | 已完成 (`docs/benchmark.md`, 附录 F); slim 达标 (Q2 未提问), 新待决 Q14 (Lite 1.1.0 崩溃); OnePlus 与 Redmi 同日补测, 都是 15 / 15 |
| P5 | 文档 / 发布 / 索引 | 四仓库文档, README / changelog, 2.0.0 与 1.1.0 发布, 索引 6 包登记 | 进行中: P5.1 完成 (四仓库本地提交), P5.2 完成 (Lite 1.1.0 已发布 d5e1e19), P5.3 进行中 |
| P6 | 插件 | 2.1.0 其余 7 语种与其他候选 | 未开始 |

依赖顺序:

```text
P0 (资产脚本与模型)   P2 (旧插件新仓库)   P3.1 - P3.4 (宿主引擎 / 打包目录 / 选择规则 / 向导)
 |                     独立, 可与任何阶段并行    P3.1 的引擎代码复制自 v4 SDK, 可与 P1 并行; 最终以 P1.2 定稿的 SDK 为准同步一次
 -> P1 (插件本体)      依赖 P0 的资产布局 (D17) 与脚本
     -> P4 (验证)      依赖 P1 + P3 的 debug 包; P4.1 旧插件冒烟依赖 P2
         -> P5 (文档, 发布, 索引)   依赖 P4 全部通过; P5.2 旧插件发布只依赖 P2 + P4.1
             -> P6 (2.1.0)
```

首批建议 (看板首轮分配): P0 + P1 (同一子会话, 本仓库独占), P2 (独立子会话, 新仓库独占), P3 (独立子会话, 宿主共用工作区) 三路并行; Q1 / Q3 / Q4 / Q6 / Q7 影响首批, 首轮拍板; Q2 在 P4.3 实测后再问; Q5 在 P5.2 前问.

发布门禁 (每个阶段的 "(发布)" 条目都指向本清单):

- R1 `version.properties` 的 `VERSION_NAME` 更新, `VERSION_BUILD` = 提交数 + 1; 10 种语言 `.changelog/lang_*.json` 补齐该版本的 `hint` / `feature` / `fix` / `improvement` / `dependency`, 日期为发布当日; 本仓库 2.0.0 的 `hint` 必须说明 "从 Paddle-Lite 换到 ONNX Runtime, 新增 x86 / x86_64, 新增语种包, Paddle-Lite 版已迁到 Paddle Lite 插件".
- R2 `.readme/lang_*.json` 与 `generate_markdown.py` 生成的 README 10 语言 (功能, 语种包说明, 安装哪一个, 脚本示例含 `profile`, 兼容性, 第三方来源), `strings.xml` 描述与 README 一致性校验通过; `check_markdown.bat` 通过.
- R3 `py D:/idea-projects/prepush_check.py` 通过 (文档校验, `test_repository_contract.py`, 构建号容差, Gradle 单元测试); 附录 F 设备矩阵中每台在线设备完成冒烟 (安装, 激活, `ocr.paddle` 中文样图, `profile` 指定语种样图, `useSlim`), 记录型号 / API / ABI / APK 摘要 / 耗时.
- R4 release APK 经 `:app:appendDigestToReleasedFiles` 收集 (5 flavor x (4 ABI + universal), 或按 Q3 结果), 16 KB 对齐与 CRC32 校验通过, 生成 `SHA256SUMS`, 创建轻量 tag `vX.Y.Z` 与 GitHub Release, 复核下载产物哈希.
- R5 官方索引: `release-manifests` 按包名各一份 (`supportedAbis` 4 项; 旧插件 2 项), `catalog-icons` 登记, `official-repositories.json` 加旧插件仓库, 运行 `tools/generate_official_plugin_index.py` 与索引单元测试, `generate_markdown.py`.

---

## P0: 资产流水线

目标: 一条命令能为任一 flavor 生成 D17 布局的全部模型文件 (fp32 + slim) 与来源记录, 不依赖本机以外的状态. 设备: 无.

### P0.1 下载, 转换与字典 (D17, D18)

- [x] (插件) `scripts/prepare_ppocrv3_assets.py`: 从 v4 脚本改写, `PROFILES` 为 5 个语种 (det / rec / cls URL, 字典 URL, 输出目录 `app/src/<flavor>/assets/models/ppocrv3/`), 下载到缓存目录 (`E:/.cache/ppocrv3-assets/`, 按 SHA-256 复用), 解包 tar, `paddle2onnx 1.3.1` (venv, `--opset_version 7`) 转换 det / rec / cls, 写 `rec/inference.yml` (`character_dict` 来自字典文件, 其余字段照 v4), `--profile all` 一次生成 5 个; 转换结果与 Rapid OCR 的预转换中文 ONNX 对比输入输出名与形状. 证据: 提交 hash, 脚本输出 (5 个 flavor 的文件数与体积), 对比结果.
  - 2026-10-30 完成 (提交见 P0 汇总行). `py -3.12 -I scripts/prepare_ppocrv3_assets.py --profile all --slim --cache-dir E:/.cache/ppocrv3-assets` 输出每 flavor 6 个文件; fp32 四件 (det / rec / cls / yml) 体积: zh 13724361 B, en 11948447 B, zhHant 14213091 B, ja 13119080 B, ko 12925676 B; 含 slim 的总量: zh 20856368 B, en 18636298 B, zhHant 21467134 B, ja 20099640 B, ko 19857869 B. 不带 `--update-provenance` 重跑一次无任何 SHA 警告 (转换与量化在本机可复现).
  - 与 Rapid OCR `ch_PP-OCRv3_*` 对比: det 输入 `x` [N, 3, H, W], 输出 `sigmoid_0.tmp_0` [N, 1, H, W]; rec 输入 `x`, 输出 `softmax_5.tmp_0` [N, T, 6625], 名称与类别数一致; 差异: 本仓库 opset 14 (paddle2onnx 把 7 升到图所需的最低版本; Rapid 为 12), rec 输入高固定 48 (Rapid 为 `?`), cls 输出名 `softmax_0.tmp_0` (Rapid 为另一导出的 `save_infer_model/scale_0.tmp_1`); SDK 按会话的第一个输入输出取用, 不依赖名称.
  - 实施中发现并已处理: (1) `Multilingual_PP-OCRv3_det` 的推理归档声明固定 960 x 960 输入, ORT 拒绝其他尺寸; `paddle2onnx.optimize --input_shape_dict` 会写入 -1 并推出错误的静态形状 (输出变成 32 x 32), 改用 `ppocrv3_onnx_tools.py dynamic-hw` 把高宽改为符号维并清掉中间形状, 脚本在 det 高宽仍固定时报错. (2) en / chinese_cht / japan / korean 字典末行已是空格, 训练时 `use_space_char` 仍追加一个空格类, 所以 `character_dict` 一律为字典条目 + 1 个空格, rec 类别数 = 条目 + 2 (含 blank), 脚本逐语种核对 (ppocr_keys_v1 6623, en 95, chinese_cht 8421, japan 4399, korean 3688 条). v4 SDK `ModelConfig` 只在末行不是空格时才补空格, v4 mobile-en 因此少一类 (v4 仓库只读, 列为后续).
- [x] (插件) `libs/ppocr-android-sdk/models.provenance.json` (Rapid 格式: 每个文件的 URL, 原始 tar SHA-256, 转换后 ONNX SHA-256, 命令, paddle2onnx / onnxruntime 版本), `.gitignore` 排除模型目录, `AGENTS.md` 写明 "先跑脚本再构建". 证据: 提交 hash.
  - 2026-10-30 完成 (提交见 P0 汇总行). provenance 记录 9 个归档与 5 个字典的 URL / 字节数 / SHA-256 (下载不符即失败), 每个模型 fp32 与 slim 的 SHA-256 / opset / 输入输出形状 (转换产物不符只警告), 每个 flavor 的 6 个资产, 转换命令与 paddlepaddle 3.2.1 / paddle2onnx 1.3.1 / onnxruntime 1.21.1 / onnx 1.23.2 版本; `.gitignore` 排除 `/app/src/*/assets/models/` 与 `/.cache/`; `AGENTS.md` (本地文件, 不入库) 已写明构建前先跑脚本.

### P0.2 slim 量化 (D5, D19)

- [x] (插件) `--slim` 选项: `quantize_dynamic` 生成 `ppocrv3-slim/{det,rec}/inference.onnx`, 记录体积压缩比, 量化参数入 provenance; 用 onnxruntime Python 对 `paddle_ocr_test.png` 跑一次 fp32 与 slim 的 det 输出差异 (box 数量与 IoU) 作为桌面侧预检. 证据: 提交 hash, 体积与预检数字 (真机判定在 P4.3).
  - 2026-10-30 完成 (提交见 P0 汇总行). 量化参数 (provenance `quantization`): 先 `quant_pre_process(skip_symbolic_shape=True)` (paddle2onnx 把权重存为 Constant 节点, `quantize_dynamic` 不接受), `QUInt8`, per_channel / reduce_range 关, 默认算子类型, 但排除权重少于 100000 个元素的 Conv (附录 D Q10, 已按推荐先行).
  - 体积 (slim / fp32): rec zh 4788929 / 10651932 B (45.0%), en 4344773 / 8954302 (48.5%), zhHant 4910953 / 11119073 (44.2%), ja 4637470 / 10073349 (46.0%), ko 4589103 / 9888485 (46.4%); det 的 Conv 都低于阈值, slim det 只折叠了 BatchNormalization, 2343078 / 2421707 B (96.8%), 多语种 det 2343090 / 2421719 B.
  - 桌面预检 (`ppocrv3_onnx_tools.py compare-slim --repeat 10`, CPU 4 线程, slim 与 fp32 的 rec 都读 fp32 det 的框): zh (样图 zh.png + zh-rotated.png + 宿主 `paddle_ocr_test.png`) det 框 5 / 5, IoU 最小 1.0, rec 文本 5 / 5 一致; en 2 / 2; zhHant 2 / 2; ja 2 / 2; ko 5 / 5 (多语种 det 按词切框); rec 合计耗时中位数 (fp32 / slim, ms): zh 66.7 / 63.3, en 56.7 / 25.2, zhHant 21.7 / 20.7, ja 20.8 / 18.7, ko 41.1 / 40.8 (桌面数字波动大, 只作参考). 未采用的配置: 默认量化全部 Conv 时 zh rec 输出全空, zhHant / ko det 丢框; 阈值 50000 时 rec 约 30% 体积, zh 一行不一致 (字符一致率 0.95).
  - 样图由 `scripts/generate_ocr_samples.py` 用 Windows 自带字体渲染 (5 语种各一张 + zh 旋转 180 度一张, `app/src/androidTest/assets/samples/`, 期望文本在 `samples.json`), P1.5 的端到端测试复用.

### P0.3 原生库核验 (D14, D36)

- [x] (插件) 从 Gradle 缓存解包 ONNX Runtime 1.21.1 AAR 与 OpenCV 4.8.0 Java AAR, `tools/16kb` 校验 4 ABI 的 `libonnxruntime.so`, `libonnxruntime4j_jni.so`, `libopencv_java4.so` 对齐, 结果写 `docs/16kb.md` (改写为 ONNX Runtime 版). 证据: 校验输出.
  - 2026-10-30 完成 (提交见 P0 汇总行). 新增 `tools/16kb/check_elf_alignment.py` (读 AAR / APK / 目录里的 `.so`, 64 位低于 16 KB 即失败, 32 位只报告); 对 ORT AAR (SHA-256 30e594a4...1d3f), v4 的 `opencv-4.8.0.aar` (8c4b410a...5c25) 与 v4 运行时模块的 `libc++_shared.so` 共 16 个库: 0 个强制项失败; `libonnxruntime.so` 与 `libopencv_java4.so` 4 ABI 都是 0x4000, `libonnxruntime4j_jni.so` 与 `libc++_shared.so` 的 armeabi-v7a / x86 为 0x1000 (32 位, 只作提示). 表格写入 `docs/16kb.md`.
- P0 汇总: 提交 67d710d.

---

## P1: 插件本体改造

目标: 本仓库构建出 5 个 flavor 的 debug 与 release APK, 4 ABI, 在宿主插件中心可识别并能完成识别. 设备: XQ-AT72 (arm64) + x86_64 AVD.

### P1.1 清理与依赖 (D14, D15, D28, D35)

- [x] (插件) 删除 Paddle-Lite 内容 (D28 清单), 移除 `libs/paddle-ocr-engine.aar` 与 `settings.gradle.kts` 中的 `:libs:paddleocr`; 新增 `libs/org-opencv-4_8_0` (v4 复制) 与 ONNX Runtime 依赖; `version.properties`: `VERSION_NAME=2.0.0`, 删除 `PADDLE_OCR_CMAKE_VERSION` / `PADDLE_OCR_NDK_VERSION`, 保留 `PADDLE_OCR_OPENCV_VERSION=4.8.0`; `app/build.gradle.kts` `abiFilters` 与 `splits` 改 4 ABI; `multidex-keep.pro` / `proguard-rules.pro` 去掉 Paddle-Lite 类, 加 `ai.onnxruntime` keep (v4 规则). 证据: 提交 hash, `gradlew :app:assembleZhDebug` 通过.
  - 2026-10-30 完成 (提交见 P1 汇总行). 删除 65 个 Paddle-Lite 文件 (`libs/paddleocr` 模块, `libs/paddle-ocr-engine.aar`, 旧 Java 服务与 `multidex-keep.pro`); `ImageInputBounds` / `InstalledPackageIdentity` 移入 `libs/ppocrv3-plugin-runtime`; 新增 `libs/org-opencv-4_8_0` 与 `tools/opencv` (v4 原样), ONNX Runtime 1.21.1 由 SDK 模块引入; `libs/paddle-ocr-api.aar` 换成宿主 f38abc036 重建的契约 (含 `USE_CLS`). `gradlew :app:assembleZhDebug` 通过 (82 个任务, `verifyZhDebugNativePageAlignment` 16384 字节通过). 工作区里 `libs/paddleocr/` 的旧构建残留 (约 1.9 GB, 原 `.gitignore` 随模块删除) 未入库, 留给维护者删除.

### P1.2 推理流水线 (D16, D25)

- [x] (插件) `libs/ppocr-android-sdk` (改包名) + `ClassificationEngine` + `OCREngine` 的 det -> cls -> rec 流水线 + `EngineConfig.useSlim` / `useCls` + `OcrOptions` 映射 (D25, Q1 / Q6 结果); 单元测试: cls 后处理 (概率 -> 角度), slim 目录切换, 映射表. 证据: 提交 hash, 测试类名与用例数.
  - 2026-10-30 完成 (提交见 P1 汇总行). SDK 包 `io.github.supermonster003.autojs6.plugin.paddleocr.v3.sdk`: 新增 `ClassificationEngine` / `ClsPostprocessor` (标签 [0, 180], 180 且分数 > 0.9 才旋转) / `RecPreprocessor` / `TextLineResize` (rec 高 48, 最小宽 320; cls 3x48x192) / `ExecutionProviders`; `OCREngine` 改为 det -> cls (可选) -> rec; `ORTSessionManager` 按 `EngineConfig.useNnapi` 请求 NNAPI, API < 27 或建会话失败回退 CPU 并打一条日志, 结果 extras `executionProvider` 与 `classificationTimeMs`. 映射见 D25 (`PpOcrV3EngineSettings.resolve`), useCls 缺省 false (附录 D Q11 (b)). 单元测试 (Java, `app/src/test`, 5 个 flavor 各跑一遍, 每个 36 例全部通过): `PpOcrV3EngineSettingsTest` 11 例 (宿主缺省, 线程, 边长优先级, 显式分数含 0, slim 只换 det / rec, useOpenCL -> NNAPI, useCls, 错误类型的 extras 当作缺省, det extras, 引擎缓存相等性, 契约键名), `TextLinePipelineTest` 6 例 (rec 批宽, 缩放宽度, 空裁剪, cls 解码 4 行, 异常输出形状, NNAPI 的 API 27 门槛).

### P1.3 flavor, 服务与能力 (D11, D24)

- [x] (插件) `productFlavors` 5 个 (5.4 表), 配置期资产校验 (每 flavor 4 个必需文件, 缺失时给出 "先跑 prepare 脚本" 的错误), `buildConfigField MODEL_PROFILE`, `resValue plugin_id / app_name`; `libs/ppocrv3-plugin-runtime` (服务, `EngineHolder`, `ImageFdDecoder`, `jniLibs/libc++_shared.so` 4 ABI + provenance), `OcrService` 能力声明 (D24, `REQUIRES_HOST_VERSION` 临时 3835), `WakeActivity`; `PluginInfo` 映射单元测试 (5 个 flavor 各一组期望值). 证据: 提交 hash; 宿主插件中心列出 5 个插件 (任一设备装任意两个 flavor 验证可共存).
  - 2026-10-30 代码完成 (提交见 P1 汇总行): 5 个 flavor (zh 为缺省) 与资产校验任务 `validate<Variant>PpOcrV3Assets` (每 flavor 校验 6 个文件: fp32 det / rec / rec 配置 / cls 与 slim det / rec, 比原写的 4 个多出 slim 两个; 缺失时提示 `python -I scripts\prepare_ppocrv3_assets.py --profile <flavor> --slim`); `FlavorIdentityTest` 3 例 (5 个 flavor 的包名, plugin_id, app_name, profile, 引擎 / 变体 / 模型族, 只有 zh 为移动端默认推荐). 真机 (`tools/device/check_device.py`, 2026-10-30 XQ-AT72 API 31, 宿主 5835, debug 包 2.0.0 (64)): zh 与 en 同时安装, `PADDLE_OCR` 查询到 2 个服务, 插件中心列出 "Paddle OCR (PP-OCRv3)" 与 "Paddle OCR (PP-OCRv3 EN)" (SuperMonster003), 12 / 12 通过; zh 样图在 useSlim x useOpenCL 四种组合下都读出 2 / 2 行 (最低相似度 0.90), 四种组合文本完全一致, useOpenCL true 时插件日志为 "Sessions ready on nnapi"; en 2 / 2 行. debug 包 (debuggable) 的宿主侧温启动约 1.2 s, 不代表 release 性能, 耗时以 P1.4 之后的 release 包实测为准. 宿主 5835 早于 USE_CLS 契约, 不转发 useCls (日志 cls off), cls 改由 P1.5 instrumentation 直接传 extras 验证.
  - 2026-10-30 release 包复测 (`tools/device/check_device.py`, XQ-AT72 API 31 arm64, 宿主 5835, 2.0.0 (66), 12 / 12 通过; 当时 `REQUIRES_HOST_VERSION` 仍是临时 3835): zh 样图 2 / 2 行 (最低相似度 0.90). fp32/cpu 冷 484 ms, 温中位 157 ms; fp32/nnapi 冷 274 ms, 温中位 158 ms (提供器 nnapi); slim/cpu 冷 269 ms, 温中位 149 ms; slim/nnapi 冷 372 ms, 温中位 232 ms; 后三种组合的文本与 fp32/cpu 完全一致. en fp32/cpu 2 / 2 行 (相似度 1.00), 冷 364 ms, 温中位 187 ms. 插件中心标签 "Paddle OCR (PP-OCRv3)" / "Paddle OCR (PP-OCRv3 EN)" 正确. Q6 (b) 记录: 这台机器上 useOpenCL true (NNAPI) 与 false 结果一致, fp32 温启动持平, slim 走 NNAPI 反而慢约 56%. 宿主 5835 不转发 useCls, 旋转样图 0 / 2 行属预期 (INFO), cls 由 P1.5 instrumentation 直接传 extras 验证.
  - 2026-10-30 D24 回填: `OcrService.REQUIRES_HOST_VERSION` 改为 5935 (c9b17bd).

### P1.4 发布形态, 图标与第三方记录 (D26, D38)

- [x] (插件) `appendDigestToReleasedFiles` 与 `release_archive.py` 按 5 flavor x ABI 矩阵 (Q3 结果) 校验与命名, `test_release_archive.py` 夹具更新; `.icons/recipe.json` `packages` 扩到 5 个包名并重跑 `generate_icon_studio.py --check`; `THIRD_PARTY_NOTICES` / README 第三方来源 (ONNX Runtime, OpenCV, PaddleOCR 模型与字典). 证据: 提交 hash, release 产物文件名列表, `--check` 输出.
  - 2026-10-30 完成 (c9b17bd). `release_archive.py` 与 `test_release_archive.py` 新增 `test_language_flavors_by_abi_matrix` (5 flavor x (4 ABI + universal), Q3 (a)); `.icons/recipe.json` `packages` 为 5 个包名, `generate_icon_studio.py --check` 输出 "Verified 15 Icon Studio resources"; 新增 `THIRD_PARTY_NOTICES.md` (ONNX Runtime 1.21.1 MIT, OpenCV 4.8.0 Apache-2.0, PaddleOCR 模型与字典 Apache-2.0, libc++_shared NDK r28c), README 构建段落链接到它. `:app:appendDigestToReleasedFiles` 收集 25 个 APK 到 `releases/v2.0.0/` (16 KB 对齐与 CRC32 校验通过, 另有 `release-manifest.json`): zh-arm64-v8a-469E9ED8, zh-armeabi-v7a-C2B43975, zh-universal-F4B1880F, zh-x86-A60AAA3F, zh-x86_64-260CB94E, en-arm64-v8a-31C1A4C9, en-armeabi-v7a-E43713B2, en-universal-98CABE9C, en-x86-460C1693, en-x86_64-A605C875, zhhant-arm64-v8a-C90C87E8, zhhant-armeabi-v7a-71E55B39, zhhant-universal-28DA5C11, zhhant-x86-55DB503C, zhhant-x86_64-55ABF698, ja-arm64-v8a-53B2DBFB, ja-armeabi-v7a-44BD073F, ja-universal-6F758FFE, ja-x86-0D8FA707, ja-x86_64-9010D4B9, ko-arm64-v8a-9F38C5FC, ko-armeabi-v7a-EBB77492, ko-universal-5B317DD3, ko-x86-2FEE1B93, ko-x86_64-631566F1 (前缀 `autojs6-plugin-paddle-ocr-pp-ocrv3-v2.0.0-`; 这批是回填 D24 之前构建的, 产物不入库, 发布时按 R4 重建). 体积见 D26. 与 1.0.6 (4efab64 起不再打包 `libopencv_java4.so`) 不同, 2.0.0 按 D15 每个 ABI 带 `libopencv_java4.so` (与 v4 相同), 已写进 2.0.0 changelog 的 dependency; 打包应用不从本插件 APK 复制该库 (Q8 (a)).

### P1.5 测试与 CI (D32, D33)

- [x] (插件) `PluginBinderContractTest` (v4 复制改名) + 五语种端到端识别 instrumentation (样图放 `app/src/androidTest/assets`, 每语种一张, 断言包含目标词); `.github/workflows/build.yml` 改为 D32 形态; `AGENTS.md` 改写 (保留提交与版本规则, 替换构建段落, 加 "资产脚本", "flavor", "ONNX Runtime 版本与 Rapid 锁定"). 证据: 提交 hash, 本地 `gradlew :app:testZhDebugUnitTest :app:connectedZhDebugAndroidTest` 通过 (x86_64 AVD), 远端运行待首次推送.
  - 2026-10-30 完成 (c9b17bd). `PluginBinderContractTest` 按 flavor 断言 (id 以 `paddle-ocr-pp-ocrv3` 开头, engine `paddle-ocr`, variant `v3`, `modelProfile` 非空, `REQUIRES_HOST_VERSION` > 0); 新增 `OcrEndToEndTest`: 按已安装 flavor 的 profile 读 `app/src/androidTest/assets/samples` 的样图 (每语种一张, `scripts/generate_ocr_samples.py` 生成, 逐行最佳匹配相似度 >= 0.8), 依次跑 fp32/cpu, slim/cpu, fp32/nnapi, zh flavor 另跑旋转 180 度样图的 useCls 对照. `.github/workflows/build.yml` 改为 D32 形态 (构建 job + binder-runtime 模拟器矩阵 google_apis / ps16k). `AGENTS.md` 已改写, 但它被 `.gitignore` 忽略, 只在本地. 本地证据: `:app:testZhDebugUnitTest` 36 / 36 通过; `:app:connectedZhDebugAndroidTest` 在 AVD_API_33 (API 33, x86_64, 只读启动) 3 / 3 通过: zh fp32/cpu 2 行 (最低相似度 0.90, 216 ms), slim/cpu 0.90 (175 ms), fp32/nnapi 0.90 (272 ms, 提供器 nnapi); 旋转样图不开 cls 相似度 0.00, 开 cls 1.00 (cls 21 ms). 远端 CI 待首次推送.

### P1.6 资源与文档 (R1, R2)

- [x] (插件) 10 语言 `strings.xml` 描述 (说明 ONNX Runtime 与语种包), `.readme/lang_*.json` 改写 (语种包表, 安装哪一个, `profile` 示例, Paddle Lite 版链接), `.changelog/lang_*.json` 2.0.0 条目 (本轮可先只写 zh-Hans 与 en, 其余语言由维护者同步或 P5.1 补), `generate_markdown.py` 生成. 证据: 提交 hash, `check_markdown.bat` 通过.
  - 2026-10-30 完成 (c9b17bd). 11 个 `values*/strings.xml` 的 `plugin_description` 说明 ONNX Runtime 与 5 个语种包 (values 与 values-en 相同); `.readme/lang_*.json` 10 语言改写: 简介, Paddle Lite 版说明与链接, 功能 (语种包, 4 ABI, useSlim, useCls 缺省关闭, "useOpenCL 在 ONNX Runtime 版映射为 NNAPI"), 新增 "语种包" 一节 (profile / 插件 ID / 包名 / APK 文件名表与 "安装哪一个"), `profile` / `engineId` / `useSlim` + `useCls` / `useOpenCL` / `variant: "v3-paddle-lite"` 示例与 6.8.0 宿主要求, 构建命令改为资产脚本 + `assembleZhDebug`; `common.json` 换 ONNX Runtime 与 Paddle Lite 插件链接. `.changelog/lang_*.json` 10 语言都写了 v2.0.0 (hint / feature / improvement / dependency; `released_date` 暂填 2026/10/30, 发布时按 R1 改为发布日). 11 个 `raw*/plugin_instruction.md` (宿主内显示的使用说明) 加 `profile` / `useCls` / `useOpenCL` 示例, 注明 "useOpenCL 在 ONNX Runtime 版映射为 NNAPI, 不可用时回退 CPU" (`plugin_description` 是一行摘要, Q6 要求的说明放在这里与 README). `generate_markdown.py --check` 与 `check_markdown.bat` 通过, `.python` 单元测试 23 / 23 通过, `prepush_check.py` 6 / 6 通过; 新增文本无全角标点.
- P1 汇总: 提交 b9fa0cc (P1.1 - P1.3), c9b17bd (P1.4 - P1.6, D24 回填).

---

## P2: 旧 Paddle-Lite 插件迁移

目标: 新仓库能构建出改名后的 1.1.0 (2 ABI + universal), 安装后与 ONNX Runtime 版共存, 宿主能按 `variant: "v3-paddle-lite"` 选中它. 设备: 任一 arm64 真机.

### P2.1 复制与改名 (D7, D27, 附录 C)

- [x] (旧插件) `git clone` 本仓库到 `D:/idea-projects/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3-Paddle-Lite` (以 `bc01d0a` 或仅含路线图提交的 HEAD 为起点), 删除 `ROADMAP.md`, 按附录 C 改名全部标识 (Java 包目录移动, `settings.gradle.kts` 根项目名, `app/build.gradle.kts` 的 `app_name` / `plugin_id` / `plugin_variant` / `applicationId`, `multidex-keep.pro` / `proguard-rules.pro`, `.run/app.run.xml`, `.icons/recipe.json` `packages`, `AGENTS.md`, `.readme` / `.changelog` 文本, `assets/doc/CHANGELOG-*.md` 由生成器重生成, 测试夹具), `VERSION_NAME=1.1.0`, `VERSION_BUILD` = 新仓库提交数 + 1, `VERSION_CODE_OFFSET` 按 Q4; changelog 1.1.0 (10 语言) 只写改名与新旧关系. 证据: 提交 hash, `rg` 确认无旧标识残留 (`paddleocr.v3"`, `paddle-ocr-pp-ocrv3"` 等精确串), `gradlew assembleRelease` + `appendDigestToReleasedFiles` 通过.
  - 2026-10-30 由 paddle-ocr-v3-p2-1-lite 完成 (看板子会话结果, 本条由 p0-p1 同步): 新仓库 master 本地提交 ca42783 (标识改名, 附录 C 23 个文件), 40 提交, `VERSION_BUILD` 40, versionCode 65 (Q4 (a)), 无 remote, 未推送. `rg` 精确串 `paddleocr.v3"` / `paddle-ocr-pp-ocrv3"` / `paddleocr/v3/` 均 0 命中; `releases/v1.1.0/` 下 arm64-v8a-AB15CF9B / armeabi-v7a-863EA86E / universal-29982533.
- [x] (旧插件) README 10 语言: 标题与说明改为 Paddle Lite 版, 加 "推荐使用 ONNX Runtime 版 (4 ABI)" 的指引与链接, 保留 TonyJiangWJ 署名; `generate_icon_studio.py --check` 通过 (包名变更后产物路径变化). 证据: 提交 hash.
  - 2026-10-30 由 paddle-ocr-v3-p2-1-lite 完成 (同步自看板): dd8e558 (10 语言 README + changelog 1.1.0), 688983d (`tools/device/check_device.py`); `check_markdown`, `generate_icon_studio --check`, `prepush_check` 6 / 6 通过; XQ-DQ72 (debug 宿主 5935) 5 / 5 PASS, 插件中心显示 "Paddle OCR (PP-OCRv3 Paddle Lite)" 1.1.0 (65) TonyJiangWJ, variant `v3-paddle-lite` 识别 468 ms. 旧标签按 Q9 (c) 在 P5.2 推送前删除.

### P2.2 共存验证

- [x] (测试) 任一 arm64 真机同时安装 Paddle Lite 1.1.0 与 ONNX Runtime 2.0.0 (zh), 插件中心两者都识别; 脚本 `ocr.paddle(img, { variant: "v3-paddle-lite" })` 与 `{ variant: "v3" }` 分别命中对应插件 (日志中的包名), 无显式条件时按 D22 命中 ONNX Runtime 版 (需 P3.3 宿主 debug 包; 之前只验证前两项). 证据: 日志片段与设备型号.
  - 2026-10-30 由 paddle-ocr-v3-p2-2-p3-5 完成 (同步自看板, 本条由 paddle-ocr-v3-p4 同步): Xiaomi Pad 23046RP50C (968e9f18, API 35, 宿主 debug 5935, 含宿主本地提交 f3aa53bb0 的选择日志 "select: <包名> (variant X) for <条件>"), v3 2.0.0 (67) 与 paddlelite 1.1.0 (65) 共存, 插件中心 9 个 Paddle OCR 服务, 两者都在并已启用 (截图在共享笔记目录 p2-2-plugin-center-pad-968e9f18.png); `variant: "v3-paddle-lite"` -> `...v3.paddlelite` (2 / 2 行, 4014 ms), `variant: "v3"` -> `...v3` (724 ms), 无条件且其余 7 个关闭 -> `...v3` (581 ms), 即 D22 选 ONNX Runtime 版. 其余 Paddle OCR 插件开着时无条件调用由它们按 D22 平手规则响应 (P4.1 在 Redmi / Pad 上同样观察到).

---

## P3: 宿主

目标: 宿主能内嵌 ONNX Runtime 版 Paddle OCR 打包 APK, 两个插件都装时打包与默认选择都优先 ONNX Runtime, `profile` 能选语种包. 落点宿主仓库, 只落本地提交. 设备: XQ-AT72 + x86_64 AVD (打包 APK 安装验证).

### P3.1 内嵌引擎模块 (D20)

- [x] (宿主) `plugin-api/paddle-ocr-onnx-engine` (源码来自本仓库 `libs/ppocr-android-sdk`, 包 `org.autojs.plugin.paddle.ocr.onnx`; `onnxruntime-android:1.21.1` 只取 Java 类, 排除 `jni/`; OpenCV 用宿主 Java API), `settings.gradle.kts` 与 `app/build.gradle.kts` 登记; `PaddleOcrEmbeddedEngine` 增加 ONNX Runtime 候选 (资产 + 原生库检查, 排第一), `useSlim` 回退逻辑, 缺库时错误文案 (复用 `error_no_embedded_paddle_ocr_assets_found` 或新增); 宿主 APK 体积不增加原生库 (核对 `unzip -l` 无 `libonnxruntime*`). 证据: 提交 hash, 单元测试 (候选解析), 宿主 debug APK 的 `lib/` 清单.
  - 2026-10-30 由 paddle-ocr-v3-p3-host 完成 (同步自看板, 宿主仅本地): 67f36614e 内嵌 ORT 引擎模块, bfc871fae 与 P1.2 定稿 SDK (b9fa0cc) 同步 (rec 保持 BGR, 批宽最小 320, cls 分批, useOpenCL -> NNAPI 失败回退 CPU, extras `executionProvider`, D25 缺省值). 单测: PaddleOcrEmbeddedEngineTest 8, PaddleOcrOnnxPipelineTest 6, 其他 6, 共 20 / 20; 内嵌引擎目前只有编译与单测证据, 打包实测在 P3.5.

### P3.2 打包目录两变体 (D8, D21)

- [x] (宿主) `ApkBuildLibraryCatalog.PADDLE_OCR` 两变体与注释, 候选选择优先 ONNX Runtime, `ApkBuilderLibPolicyTest` / `PackagedNativeLibraryPolicyTest` 更新 (含 `libonnxruntime4j_jni.so`), `docs/dev/opencv-ocr-runtime-decoupling-roadmap.md` D10 行加注; `RemoteApkBuildRequestPreparer` 的 "只装有 v4-v6" 错误文案不变. 证据: 提交 hash, 单元测试通过.
  - 2026-10-30 由 paddle-ocr-v3-p3-host 完成 (同步自看板): fde89093f 打包两变体 (ORT 优先) + Q8 (a) 选中 ORT 变体时自动带入 OpenCV 插件产物.

### P3.3 默认选择与 profile 匹配 (D22, D23)

- [x] (宿主) `OcrPluginHost`: 平手规则 (`recommendedForMobileDefault` -> 包名), `profile` 参与 `matchesSelectionCriteria` 与 `hasExplicitSelectionCriteria`, `selectOrThrow` 签名增加 `profile` 并由 `OcrPaddle` 传入 `parsed.extras` 的 `PROFILE`; 找不到匹配 profile 时的错误文案 (10 语言, 本轮 zh-Hans + en, 其余由维护者同步) 列出已安装插件的 profile 值; 单元测试 (假 `PluginInfo` 列表的选择结果). 证据: 提交 hash, 测试类名.
  - 2026-10-30 由 paddle-ocr-v3-p3-host 完成 (同步自看板): 2b0ecf969 profile 匹配 + 默认选择平手规则; f38abc036 契约 `USE_CLS`, 894f00492 脚本层, 5c19eeb10 Q11 (b) useCls 缺省 false.

### P3.4 向导, 注册与 changelog (D30)

- [x] (宿主) `PluginInstallWizardCatalog` 新增 Paddle Lite 条目, `InstalledPluginRepository` / `<queries>` 按需加包名 (若按前缀匹配则记录 "无需改"); `.changelog` zh-Hans 条目 (打包支持 ONNX Runtime 版 Paddle OCR, `profile` 选语种包, Paddle Lite 插件); 回填 `REQUIRES_HOST_VERSION` 目标值到本路线图 D24 (该提交的 versionCode). 证据: 提交 hash, 向导截图 (任一设备).
  - 2026-10-30 由 paddle-ocr-v3-p3-host 完成 (同步自看板): b2dd1757b 向导 Paddle Lite 条目 + zh-Hans changelog (Q7 (a)), 62fbdda04 向导顺序单测 (PluginInstallWizardLoaderTest 与 CatalogTest 各 5 / 5); `REQUIRES_HOST_VERSION` 目标值 5935 已回填 D24. 向导截图按附录 D Q12 (a) 移到 P5.3 索引登记后再取 (维护者 2026-10-30 已拍板).

### P3.5 打包 APK 验证

- [x] (测试) 宿主 debug 包 + ONNX Runtime 插件 (zh) 打包一个调用 `ocr.paddle` 的脚本: arm64 真机与 x86_64 AVD 各安装运行, 识别结果与宿主应用内一致, `useSlim` 走 slim 目录 (日志); 只装 Paddle Lite 插件时打包仍走 Paddle-Lite 引擎 (arm64 真机); 两者都装时打包器选中 ONNX Runtime (日志 "Selected plugin ... (v3)"). 证据: 三组结果与 APK 的 `lib/` 清单.
  - 2026-10-30 由 paddle-ocr-v3-p2-2-p3-5 完成 (同步自看板): 宿主本地提交 f3aa53bb0 (选择与内嵌引擎加载日志), 5737cbdc1 (设备测试 `PaddleOcrOnnxPackagingDeviceTest` + `tools/paddle-ocr-v3`), 单测 52 / 52. Pad 七组 + AVD_API_33 (x86_64) 两组, 打包应用与宿主识别文本逐项一致; ort 组 `lib/` 8 项 (ONNX Runtime + OpenCV). Pad fp32 456 ms, slim 185 ms (日志 `models/ppocrv3-slim`), `useOpenCL` 358 ms (provider nnapi), 倒置图 `useCls` 关 0 / 2 行, 开 2 / 2 行; AVD fp32 1063 ms, slim 294 ms, nnapi 321 ms, cls 开 2 / 2 行. Lite + ORT 同装 -> 选 ORT; 加装 Rapid OCR ppocrv3 1.0.6 后 `libonnxruntime.so` 三方字节相同 (17908496 字节, `67465b2bcf0a`), 无冲突; 关闭 OpenCV 插件 -> 构建报 `error_apk_paddle_ocr_onnx_runtime_requires_opencv_plugin`; 只装 Lite -> `v3-paddle-lite` (Paddle-Lite 引擎 603 / 80 ms); 只装旧 1.0.5 -> `v3` 回退 `v3-paddle-lite` (535 / 79 ms). 新待决 Q20 (脚本层看不到 `executionProvider`, 已按推荐先行, 见看板). 明细在共享笔记目录 p2-2-p3-5-notes.md 与 p2-2-p3-5-device.log.

---

## P4: 验证

目标: 设备矩阵证明 2.0.0 在 4 ABI 与 API 24-35 可用, 新旧实现结果一致, slim 档有判定结论. 设备: 附录 F.

### P4.1 冒烟矩阵 (D33)

- [x] (测试) 附录 F 每台设备: 安装 zh + 任一其他语种 flavor, 激活, 中文样图 `ocr.paddle` (无条件), `profile` 指定语种样图, `useSlim: true`, `RAW_IMAGE` 路径 (宿主 `SharedMemory` 传图); x86 / x86_64 在 AVD 上跑 (API 24, 33 / 35 x86_64, 16 KB 镜像); 旧 Paddle Lite 1.1.0 在 arm64 真机冒烟. 记录型号 / API / ABI / 耗时. 证据: 附录 F 表填满, 未在线设备写 "未执行".
  - 2026-10-30 由 paddle-ocr-v3-p4 完成 (附录 F 冒烟结果表): 宿主 debug 5935, 插件 release 2.0.0 (67). 全部通过: XQ-AT72 33 / 33 (5 个 flavor), XQ-DQ72 18 / 18, G8441 arm64 18 / 18 与 armeabi-v7a 包 18 / 18, Xiaomi Pad 18 / 18, AVD_API_24 (x86) 15 / 15, AVD_API_33 (x86_64) 15 / 15, AVD_API_35_16K 15 / 15; Paddle Lite 1.1.0 在 6 台 arm64 设备 (G8441 另测 v7a 包) 上 fp32 / slim 都通过. `useOpenCL`: API 27 及以上都报 nnapi 且文本与 CPU 相同, 耗时与 CPU 相差 -10% 到 +23%; API 24 回退 cpu. `RAW_IMAGE` 路径在 API 27 及以上宿主回退 0 次. OnePlus 63751f63 与 Redmi bek749scrwv4wo8h 同日补测, 都是 15 / 15 (`--no-install`, 用首轮已装并核对过的包): 首轮 Redmi 13 / 19 与 OnePlus 11 / 19 的失败都来自 zh 包在插件中心是关闭状态 (沿用同包名旧版的设置, 由维护者打开); OnePlus 的宿主还是 10-29 的旧构建, 不含 P3.3 的 profile 匹配, `profile: 'ko'` 落到 zh, 换成与 Redmi / XQ-AT72 相同的宿主 (sha256 f74c06cf) 后通过. 脚本改动: `--abi`, `--lite`, `--no-install` (ColorOS 每次 adb 安装都要在机上确认), 无条件路由只把插件中心开启的更高版本算作预期 (debug 宿主用 run-as 读开关), 宿主脚本改为 `-e script` 内联启动 (Android 11+ 的 `-e path` 需要全部文件访问权限), 外部目录由宿主自建, 运行前用 adb 启动宿主的启动器活动 (切到前台).

### P4.2 新旧对比

- [x] (测试) 图集 (D34) 在旧 Paddle-Lite (1.0.6 APK 或 Paddle Lite 1.1.0) 与 ONNX Runtime fp32 上逐行比较文本, 记录一致率与差异样例 (预期 >= 95%; 低于则分析是否转换 / 预处理差异并登记待决); 耗时对比 (XQ-AT72). 证据: 数字与差异清单 (`docs/benchmark.md`).
  - 2026-10-30 由 paddle-ocr-v3-p4 完成: `docs/benchmark.md`, 工具 `tools/device/benchmark.py` (`--lite`, `--image`) 与 `tools/device/make_benchmark_images.py` (11 张图, 哈希在文档里). XQ-AT72 (API 31, 宿主 debug 5935) 4 张 1080 x 1500 大图 (zh / en 的 settings 与 notes): Paddle Lite 1.1.0 fp32 与 ORT fp32 一致 56 / 56 (100%), Lite slim 56 / 56, 加宿主样图 57 / 57, 无差异样例; 两引擎对标注文本的命中相同. 中位 wall 合计 ORT fp32 3468 ms, Lite fp32 3292 ms (ORT 慢 5.1%). XQ-DQ72 (API 33) `zh-settings` 19 / 19, 636 / 624 ms. 发现 Lite 1.1.0 "先小图后大图" 崩溃 (登记 Q14), 对比在新进程里只跑大图.

### P4.3 slim 判定 (D5, D19)

- [x] (测试) slim 与 fp32 的一致率与耗时 (XQ-AT72, x86_64 AVD); 达标 (一致率 >= 95% 且 rec 耗时下降) 则 `useSlim` 文档照写; 不达标按附录 D Q2 拍板后处理. 证据: 数字入 `docs/benchmark.md` 与附录 F.
  - 2026-10-30 由 paddle-ocr-v3-p4 完成, 达标, `useSlim` 文档照写, Q2 未提问: 11 张图各用对应语种 flavor, CPU 4 线程, 1 次预热 + 10 次取中位. XQ-AT72 一致率 246 / 251 (98.0%), rec 合计 8716 -> 8074 ms (-7.4%), wall 合计 11311 -> 10768 ms (-4.8%); AVD_API_33 (x86_64) 246 / 251 (98.0%), rec 合计 6894 -> 6764 ms (-1.9%), wall 合计 9295 -> 9362 ms (+0.7%). 两台的 5 个不同框完全相同 (zhHant-notes 1, ja-settings 1, ja-notes 2, ko-settings 1, 各差一两个字), fp32 与 slim 对标注文本的命中逐图相同. 会话加载 fp32 98-147 ms, slim 75-103 ms. NNAPI (zh fp32) 文本与 CPU 相同 (两台 29 / 29 框).

### P4.4 API 24 与 16 KB

- [x] (测试) API 24 AVD (x86 或 x86_64): 安装, 激活, 识别; 16 KB 页 AVD (API 35 16K): 安装与识别 (记忆: 冷引导后等 1 分钟再测). 证据: 结果与 AVD 名.
  - 2026-10-30 由 paddle-ocr-v3-p4 完成: AVD_API_24 ("Android SDK built for x86", API 24, x86, 宿主 debug 5935 x86): zh (x86-61EB321F) 与 ja (x86-D3DCAAF1) 安装, 插件中心发现与标签, 无条件与 `profile: "ja"` 识别, 15 / 15 PASS, 温中位 265-455 ms; `useOpenCL` 回退 cpu, `RAW_IMAGE` 不适用 (API < 27). AVD_API_35_16K (sdk_gphone16k_x86_64, API 35, `getconf PAGE_SIZE` 16384, 只读启动, 冷引导后等待再测): zh (x86_64-5AD7D7C8) 与 zhHant (x86_64-8423519B) 15 / 15 PASS, 温中位 148-412 ms, NNAPI 可用, raw 回退 0. 16K 镜像上宿主在后台会被缓存应用冻结 (`ActivityManager: freezing`) 卡在识别中途, 在宿主脚本里 `app.launch` 也来不及; 脚本改为先用 adb 启动宿主的启动器活动再发脚本, 复测 15 / 15 通过, 宿主未再被冻结.

---

## P5: 文档, 发布与索引

### P5.1 文档与声明 (D31, D37)

- [x] (文档) `api/ocr.md`, `api/ocrOptionsType.md` (`variant` / `profile` 段), d.ts `DetectOptionsPaddle` 注释, Ace Editor 与 Offline Docs 同步; 改动页若在 api-coverage 门禁范围内则重跑门禁. 证据: 各仓库提交 hash (本地).
  - 2026-10-30 由 paddle-ocr-v3-p5-1 完成 (同步自看板), 含 W2 与 Q20 (c): 宿主 22d06da81 (`OcrResult.extras`), bb7e2fe53 (自动选择传 `profile`), 6006aa802 (api-coverage 矩阵); 文档站 f15d21e, a51245b (生成物); d.ts 87fc1eb; Ace 2136195; Offline Docs 63648eb, 均本地未推送. 单测 `OcrResultExtrasTest` 10 项与 ocr 包其余用例共 30 项通过, 插桩 `OcrResultExtrasBundleTest` 3 / 3 (Pad 968e9f18), 设备 `tools/paddle-ocr-v3/device_check.py extras` 8 / 8. api-coverage `check.py --matrix --docs-support` failures 为空, 文档 auto-generate `--check` 与 normalize 通过; 未跑 `--verify-offline` 的 APK 门禁. 多片段合并只有单测证据, 内嵌引擎路径与 Node 桥的 `profile` 传递只有编译证据. 待维护者: 宿主 `.changelog` zh-Hans 两条 (`OcrResult.extras`, `profile` 修复) 与其他语言同步.

### P5.2 旧插件 1.1.0 发布

- [x] (发布) 维护者创建 GitHub 仓库 `AutoJs6-Plugin-Paddle-OCR-PP-OCRv3-Paddle-Lite` 并添加 remote (维护者待办); R1-R4; 索引登记 (R5 的旧插件部分). 证据: tag, Release 链接, 索引提交 hash.
  - 2026-10-30 由 paddle-ocr-v3-p5-2 完成 (同步自看板): tag `v1.1.0` = master = d5e1e19 (轻量, versionCode 67, build 42), Release https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3-Paddle-Lite/releases/tag/v1.1.0 (3 个 APK + `SHA256SUMS`, 下载复核通过, CI 两个工作流通过). 索引 7c18faa + 1aa94ae 已推送 (`release-manifests/...paddlelite/67.json`; 7c18faa 是旧哈希, 由 1aa94ae 更正), CI 机器人追加 ccfdb83. SHA-256: arm64-v8a `8bf31670...` (23C59EBF), armeabi-v7a `41305fa3...` (DEE59924), universal `ed15e937...` (09E98A28). Q14 (a) 修复 bee0ce1, 回归脚本 `tools/device/check_engine_thread.py` (d5e1e19): 修复前 65 在 XQ-AT72 与 XQ-DQ72 都于 6 次调用后崩溃; 最终包 67 两台各 100 calls 0 failed, 112 框与 65 参考相同; XQ-AT72 上 armeabi-v7a 包 40 calls 与 universal 包 20 calls 通过. GitHub email privacy 拒绝首推后, 只改了 5 笔未发布提交的邮箱, 树不变, 哈希对照 ca42783 -> ca76366, dd8e558 -> cc2208c, 688983d -> ebf6acb, 05b532a -> bee0ce1, af48bef -> d5e1e19 (P2.1 证据里的旧哈希按此对照). 其余 4 台补测见附录 F.

### P5.3 本仓库 2.0.0 发布与索引 (D29)

- [ ] (发布) R1-R5 (5 个 flavor 的清单各一份, `catalog-icons` 登记两个仓库的图标, `official-repositories.json` +1); `REQUIRES_HOST_VERSION` 回填为 P3.4 的值 (是否等宿主公开见附录 D Q5). 证据: tag, Release 链接 (APK 数量), 索引提交 hash, SHA-256.

---

## P6: 2.1.0 候选

### P6.1 其余 7 语种 (D10)

- [ ] (插件) flavor `latin` / `arabic` / `cyrillic` / `devanagari` / `te` / `ka` / `ta` (det 全部 Multilingual, rec `<lang>_PP-OCRv3_rec_infer.tar` 9.5-9.9 MB, 字典 `dict/<lang>_dict.txt`; 阿拉伯语 README 品牌名 FSI / PDI 包裹), 资产脚本 `PROFILES` 扩展, 索引清单 +7; 向导不登记. 证据: 同 P1 / P5.

### P6.2 其他候选

| 候选 | 说明 | 依赖 |
| --- | --- | --- |
| NNAPI / XNNPACK 执行提供器 | ORT Android 支持, 需逐机型实测, `useOpenCL` 可映射到它 | P4 基线, 用户需求 |
| 静态量化 slim | 需校准集, 精度通常高于动态量化 | Q2 结果 |
| 宿主打包 v4-v6 | 推翻 D10, 需 v4-v6 的资产布局统一 | 维护者决定 |
| 旧 Paddle Lite 插件 16 KB 对齐复核 | 旧 `.so` 若不对齐, 1.1.0 只能标注不支持 16 KB | P2.1 |

---

## 附录 A. 脚本选择方式

```javascript
// 默认: 无条件时按 D22 选 ONNX Runtime 中文档 (recommendedForMobileDefault)
ocr.paddle(img);
// 指定语种包 (D23): 需要已安装对应 flavor
ocr.paddle(img, { profile: "ja" });
// 指定旧 Paddle Lite 版 (D7)
ocr.paddle(img, { variant: "v3-paddle-lite" });
// 指定精确插件
ocr.paddle(img, { engineId: "paddle-ocr-pp-ocrv3-ko" });
// slim 档 (D5)
ocr.paddle(img, { useSlim: true });
// 原有字段不变: cpuThreadNum, detLongSize, scoreThreshold, mergeLine
```

`ocr.detect(img, { engine: "paddle", profile: "en" })` 走同一条路径 (宿主 bb7e2fe53 起成立; 之前自动模式 `selectForCall` 没传 `profile`, 只有 `ocr.paddle` 按它选插件). Node / Bun 经桥传同样的 options (`profile` 参与选择同样要 bb7e2fe53, Node 桥这一处只有编译证据).

---

## 附录 B. 资产与打包变体清单

| 文件 (每 flavor) | 来源 (D18) | 体积 (ONNX 预估) | 入库 |
| --- | --- | --- | --- |
| `models/ppocrv3/det/inference.onnx` | 语种对应 det tar | 2.3-2.4 MB | 否 (脚本生成) |
| `models/ppocrv3/rec/inference.onnx` | 语种对应 rec tar | 9-12 MB | 否 |
| `models/ppocrv3/rec/inference.yml` | 字典 + 固定字段 | < 100 KB | 否 (脚本生成) |
| `models/ppocrv3/cls/inference.onnx` | `ch_ppocr_mobile_v2.0_cls_infer.tar` | 约 0.6 MB | 否 |
| `models/ppocrv3-slim/{det,rec}/inference.onnx` | `quantize_dynamic` | 约 1/3 | 否 |
| `libs/ppocr-android-sdk/models.provenance.json` | 脚本写出 | - | 是 |

宿主打包变体见 5.6. 原生库 (每 ABI): `libonnxruntime.so` 13-21.4 MB, `libonnxruntime4j_jni.so` 0.1 MB, `libopencv_java4.so` 14.3-53.2 MB, `libc++_shared.so` 约 1 MB.

---

## 附录 C. 旧插件改名清单 (D7, D27)

2026-10-29 用 `rg -l -i "paddleocr\.v3|paddle-ocr-pp-ocrv3|Paddle-OCR-PP-OCRv3|paddleocr/v3"` 在本仓库命中 23 个文件:

- 构建与配置: `settings.gradle.kts` (根项目名), `app/build.gradle.kts` (`applicationId` 来源, `app_name`, `plugin_id`, `plugin_variant`, `plugin_author` 保持), `app/multidex-keep.pro`, `app/proguard-rules.pro`, `libs/paddleocr/build.gradle.kts`, `.run/app.run.xml`.
- 源码: `app/src/main/java/io/github/supermonster003/autojs6/plugin/paddleocr/v3/OcrService.java` 与 `WakeActivity.java` (包目录移到 `.../paddleocr/v3/paddlelite/`, Manifest 的类名引用同步).
- 生成产物: `README.md`, `app/src/main/assets/doc/CHANGELOG*.md` (14 个, 由 `.readme` / `.changelog` 源改后重生成).
- 另需改 (不含标识串但语义相关): `.icons/recipe.json` `packages`, `AGENTS.md` (标题, 根项目名, 服务名), `.readme/common.json` 与 `lang_*.json` (名称, 说明, 作者段), `.changelog/lang_*.json` (1.1.0 条目), `.python/test_*.py` 夹具 (项目名, 包名), `version.properties` (`VERSION_NAME`, `VERSION_BUILD`), `res/values*/strings.xml` 的描述 (若含 "PP-OCRv3" 字样则加 "Paddle Lite").
- 不改: `plugin_engine = paddle-ocr`, 签名配置, 原生模块与模型路径, 10 语言资源键名.

---

## 附录 D. 待决事项

| 编号 | 事项 | 选项 | 拍板时点 |
| --- | --- | --- | --- |
| Q1 | cls 的开关方式 | (a) 默认开启, 不提供开关 (推荐; 与旧 v3 行为一致, 契约零改动, 耗时增加约 5-10%); (b) 默认开启, extras 私有键 `ppocrv3.useCls` 可关 (文档只在插件 README 写); (c) 契约 `PaddleOcrOptionExtraKeys` 新增 `USE_CLS` 并在宿主 `OcrOptions` 解析 (改宿主契约, 四仓库文档) | P1.2 前; 2026-10-30 已决 (c), 宿主 f38abc036 `USE_CLS = "useCls"`; 缺省值见 Q11 |
| Q2 | slim 实测不达标时 | (a) 保留 fp32 作 slim 档, `useSlim` 实际无差别并在文档标注 (推荐; 零返工); (b) 改静态量化 (需校准集, 约 1 天); (c) 去掉 slim 目录, `useSlim` 忽略 (打包目录可选项删掉) | P4.3 后; 2026-10-30 实测达标, 未提问: XQ-AT72 与 AVD_API_33 一致率均 98.0% (246 / 251), rec 合计 -7.4% / -1.9%, `useSlim` 文档照写 (`docs/benchmark.md`) |
| Q3 | 是否保留 universal APK | (a) 保留 (推荐; 与 v4 / v5 / v6 一致, 每版 25 个 APK, universal 约 200 MB); (b) 只发单 ABI (每版 20 个, 索引 `artifacts` 无 universal, 旧用户手动选 ABI) | P1.4 前; 2026-10-30 已决 (a) |
| Q4 | 旧插件 versionCode 延续 | (a) 保持 `VERSION_CODE_OFFSET=25` 与提交数接续 (推荐; 新包名无升级关系, 但保持公式与历史一致, 1.1.0 约 65); (b) 改 `VERSION_CODE_OFFSET=0` 从提交数重算 (约 40, 需改 `AGENTS.md` 的迁移说明) | P2.1 前; 2026-10-30 已决 (a) |
| Q5 | 2.0.0 是否等宿主 6.8.0 公开 | (a) 不等, `REQUIRES_HOST_VERSION` 指向 P3.4 的本地构建 (推荐; Macaw / Prism 先例; 旧公开宿主 6.7.x 上插件仍可用, 只是 `profile` 不参与选择且默认选择顺序不确定); (b) 等宿主公开后再发 | P5.3 前; 2026-10-30 已决 (a) |
| Q6 | `useOpenCL` 的处理 | (a) 忽略并打一条日志 (推荐; ORT CPU 执行提供器); (b) 映射到 NNAPI 执行提供器 (逐机型差异大, 需矩阵实测) | P1.2 前; 2026-10-30 已决 (b), API < 27 或 NNAPI 失败回退 CPU |
| Q7 | 其他语种 flavor 是否进安装向导 | (a) 不进, 只登记 zh 与 Paddle Lite (推荐; 与 v4 `mobile.en` / v5 语种包一致); (b) 全部登记 (向导多 4 行, 回退标题 10 语言) | P3.4 前; 2026-10-30 已决 (a) |
| Q8 | 打包应用里 ORT 内嵌引擎的 OpenCV 原生库来源 | (a) 打包选中 ORT 变体时自动带入 OpenCV 插件产物, OpenCV 插件不可用时报专用错误 (推荐, 已先行); (b) 未勾 OpenCV 时直接报错; (c) 从 ORT 插件 APK 复制 `libopencv_java4.so`; (d) 重写 SDK 前后处理去掉 OpenCV. 详情见看板 (来源 paddle-ocr-v3-p3-host) | 2026-10-30 已决 (a) |
| Q9 | Paddle Lite 新仓库继承的旧标签 v0.2.3 / v1.0.0 / v1.0.5 | (a) 本地保留, P5.2 只推 master 与 v1.1.0 (推荐, 已先行); (b) 一并推送; (c) 在新仓库删除. 详情见看板 (来源 paddle-ocr-v3-p2-1-lite) | 2026-10-30 已决 (c), P5.2 推送前 `git tag -d v0.2.3 v1.0.0 v1.0.5`, 只推 master 与 v1.1.0 |
| Q10 | slim 量化范围 (D19) | (a) 量化 MatMul 与权重不少于 100000 个元素的 Conv (推荐, 已先行; rec 体积 44-49%, 桌面预检 5 语种框与文本 100% 一致; det 的 Conv 都低于阈值, slim det 约等于 fp32 只折叠 BN, 体积 97%); (b) 阈值 50000 (rec 约 30%, zh 字符一致率 0.95, 一行不一致); (c) `quantize_dynamic` 默认全部 Conv (rec 约 26%, zh rec 输出全空, zhHant / ko det 丢框, 不可用). 影响 P0.2, P4.3, Q2; 改选返工: 改 `CONV_MIN_WEIGHTS` 一个常量并重跑脚本, 约 10 分钟 | 2026-10-30 已决 (a); P4.3 真机实测后可再议 |
| Q11 | `useCls` 缺省值 | Q1 选项 (a) 写的 "与旧 v3 行为一致" 前提不成立: 旧 v3 的 `isClassificationEnabled` 从未置 true, 实际从未跑 cls. (a) 保持缺省 true (推荐, 已先行; 契约 f38abc036 已按 true 定稿, 旋转 180 度的文字也能识别, 每次多一次 cls 推理); (b) 缺省 false 与旧 v3 实际行为一致 (改宿主契约说明与插件缺省, 约 30 分钟). 影响 P1.2, P3, P5.1 文档 | 2026-10-30 已决 (b): 插件 `PpOcrV3EngineSettings.DEFAULT_USE_CLS = false` 与 SDK `PaddleOCRConfig.useCls` 缺省 false, 宿主契约说明由 P3 改 |
| Q12 | P3.4 向导截图怎么取 (向导加载器跳过官方索引中没有的条目, Paddle Lite 包名要到 P5.3 才登记索引) | (a) 截图移到 P5.3 索引登记后再取 (推荐, 已先行; `PluginInstallWizardLoaderTest` 5 / 5 已覆盖顺序, 分类与回退标题); (b) 现在在调试宿主上注入本地索引缓存后截图 (约 30 分钟 + 一台设备). 来源 paddle-ocr-v3-p3-host | 2026-10-30 已决 (a): 截图移交 P5.3 索引登记后再取 |
| Q13 | 2.0.0 重新打包 `libopencv_java4.so` (1.0.6 的 4efab64 已把 OpenCV 静态链接进 `libNative.so` 并只导出 3 个 JNI 方法, 不再带这个库; 2.0.0 按 D15 沿用 v4 的 OpenCV 4.8.0 Java 模块, 每个 ABI 带一份, arm64 约 20.4 MB) | (a) 保持打包, 在 2.0.0 changelog 的 dependency 写明 (推荐, 已先行; 与 v4 相同; Q8 (a) 之后打包应用从 OpenCV 插件带入该库, 不从本插件 APK 复制, 1.0.6 要避免的同名库来源冲突不再出现); (b) 改为 JNI 前后处理并静态链接 OpenCV 核心模块 (约 2 天, 体积收益未实测); (c) Kotlin 重写前后处理, 去掉 OpenCV (约 2 - 3 天, 可与 Q8 (d) 合并). 影响 P1.4, D15, 2.0.0 changelog; 改选返工见各选项. 来源 paddle-ocr-v3-p0-p1 | 2026-10-30 已决 (a): 保持打包, 维护者看过三选项体积对比后选定 |
| Q14 | Paddle Lite 1.1.0 在 "先识别小图再识别大图" 时崩溃 (P4.2 发现: 服务在接收调用的 binder 线程上跑引擎, 原生 det 只在第一个线程用 960 x 960 预热; 只跑过小图的线程再收到大图时 SIGSEGV (SEGV_ACCERR, `memset`, `libpaddle_light_api_shared.so` pc `0xbc800`), 该宿主进程之后的调用都报 `DeadObjectException`; XQ-AT72 与 XQ-DQ72 复现, 新进程只跑大图或一次小图后接大图不崩; `libpaddle_light_api_shared.so` 与 1.0.5 字节相同, 已发布版本可能同样受影响 (未实测); ORT 版不受影响) | (a) Lite 仓库的服务把全部引擎调用放到一个常驻线程, 1.1.0 发布前重建并在两台 arm64 上重跑复现集 (推荐, 未先行: Lite 仓库本批只读; 约 1-2 小时); (b) 照常发布, README / changelog 写已知问题 (零返工); (c) 每个新线程先做一次 960 x 960 预热 (约 1 小时, 根因是推测, 每个新线程多约 150 ms). 影响 P5.2 (1.1.0 发布), `docs/benchmark.md` 的 Lite 测法. 来源 paddle-ocr-v3-p4 | 2026-10-30 已决 (a): Lite bee0ce1 (常驻线程) + d5e1e19 (回归脚本), 复现集两台 100 calls 0 failed |
| Q15 - Q19 | 未使用 | 编号保留 | - |
| Q20 | 脚本层 `OcrResult` 看不到结果 extras (`executionProvider`, `quad`) | (a) 保持现状, 仅日志可见 (推荐, 已先行); (b) `OcrResult` 加只读 `executionProvider` (约 2-3 小时); (c) 整个 extras 以对象暴露 (约半天). 影响 D25 在脚本层的可见性与文档. 来源 paddle-ocr-v3-p2-2-p3-5 | 2026-10-30 已决 (c), 非推荐: 宿主 22d06da81 (P5.1) |
| Q21 - Q25 | 未使用 | 编号保留 | - |
| Q26 | Node / Bun 的 ocr 结果是否也带 extras | (a) 暂不做 (推荐, 已先行; 矩阵 not-portable, 只有 Rhino 能读); (b) 现在做 (宿主 `toOcrResultsJson` 加字段含 `quad` 偏移, Node / Bun 声明, 矩阵与文档同步, 约 1-2 小时). 影响 P5 之后, 不阻塞发布. 来源 paddle-ocr-v3-p5-1 | 2026-10-30 已决 (b), 非推荐: 由 paddle-ocr-v3-q26 落实 |
| Q27 | d.ts 与 Ace 本次加 `OcrResult.extras` 是否升版本号 | (a) 随下次发版一起升 (推荐, 已先行; 沿用 api-coverage "version unchanged" 惯例); (b) 现在升到 4.86.0 / 2.48.0 (约 30 分钟, 含 10 语言 changelog). 影响 d.ts 87fc1eb, Ace 2136195. 来源 paddle-ocr-v3-p5-1 | 2026-10-30 已决 (a), 已实施 |

---

## 附录 E. 证据等级

- E1 代码与配置: 提交 hash 可追溯, 相关文件在仓库中.
- E2 JVM 单元测试: 测试类名, 用例数, 运行命令.
- E3 instrumentation / 真机: 测试类名或脚本 + 设备型号 + API + ABI + 日期 + 耗时.
- E4 人工验收: 设备, 步骤, 结果, 截图路径 (`.bak/visual/<version>/`, 不入库).
- E5 发布产物: APK 文件名, SHA-256, tag, GitHub Release 链接, 索引清单文件名.

勾选 `[x]` 的条目至少满足 E1 + (E2 或 E3); 涉及界面的条目另需 E4; "(发布)" 条目需 E5. 未执行的验证必须如实写 "未执行".

---

## 附录 F. 基线快照与设备矩阵

基线 (2026-10-29):

| 项 | 值 |
| --- | --- |
| 本仓库 | `master@bc01d0a`, 37 提交, `1.0.6`, `VERSION_BUILD=36` (本次 docs 提交改 38), `VERSION_CODE_OFFSET=25`, 已发布最高 versionCode 61 (1.0.6), 索引清单只有 48 (1.0.5), `releases/v1.0.4`, `v1.0.5` 本地产物 (不入库) |
| 宿主 | `master@3fa1fc8ad`, `6.8.0` 未发布, versionCode 5935; 无 `onnxruntime` 依赖; `PaddleOcrEmbeddedEngine` 候选 v5 / v3 (Paddle-Lite); 打包目录 `PADDLE_OCR` 只有 Paddle-Lite `v3` 变体 |
| v4 仓库 | `1.0.4`, `VERSION_BUILD=37`, minSdk 26, ONNX Runtime 1.21.1, OpenCV 4.8.0 Java AAR, flavor mobile / server / mobileEn, 模型不入库 |
| Rapid OCR PP-OCRv3 | ONNX Runtime 1.21.1 (`@aar` 解包取 `libonnxruntime.so`), 预转换 PP-OCRv3 中文 ONNX |
| 索引 | `official-repositories.json` 51 条; `catalog-icons.json` 39 条, 无 `paddleocr.*`; `retired-packages.json` 10 条 |
| 模型下载 | D18 全部 URL 2026-10-29 HTTP 200, 体积已记录 |

设备矩阵 (来自 `COMMON_AGENTS.md`; 2026-10-15 起已连接设备可自由安装 / 卸载官方插件; 手机上的对话框由维护者操作):

| 设备 | API | ABI | 用途 |
| --- | --- | --- | --- |
| AVD_API_24 (`E:/.android/avd`) | 24 | x86 / x86_64 | 最低 API 冒烟 (D12) |
| Sony G8441 (BH900ASK9E) | 28 | arm64 | 低端机耗时基线 |
| Sony XQ-AT72 (QV710AF65F) | 31 | arm64 | 开发主力机, 精度与速度基线 (D34), 新旧对比 |
| Sony XQ-DQ72 (QV770340J7) | 33 | arm64 | 冒烟 (注意记忆中 debug 宿主 ART JIT ANR 问题) |
| Redmi 22120RN86C (bek749scrwv4wo8h) | 33 | arm64 | MIUI 冒烟 |
| Xiaomi Pad 23046RP50C (968e9f18) | 35 | arm64 | 打包 APK 验证 (P3.5), 平板 |
| OnePlus OPD2413 (63751f63) | 35 | arm64 | ColorOS 激活与唤醒 |
| x86_64 AVD (API 33 / 35, 含 AVD_API_35_16K) | 33 / 35 | x86_64 | 4 ABI 的核心验证, 16 KB (记忆: 冷引导后等 1 分钟) |
| armeabi-v7a | - | armv7 | 本地无 32 位真机; 用 arm64 设备安装 armv7 APK (系统允许时) 或标注 "仅构建与对齐校验" |

冒烟结果 (P4.1 / P4.4, 2026-10-30, paddle-ocr-v3-p4): `tools/device/check_device.py`, 宿主 debug 5935 (含 P3 改动), 插件 `releases/v2.0.0/` 的 release 包 (67). 每台装 zh + 另一语种 flavor (XQ-AT72 装全部 5 个), 检查插件中心发现与标签, 无条件 `ocr.paddle` (中文样图), `profile` 指定语种样图, fp32 / slim x CPU / `useOpenCL` (NNAPI), 编码图与 `RAW_IMAGE` (`SharedMemory`) 两条路径, 倒置样图 `useCls: true` (INFO, 不计数), arm64 上另装 Paddle Lite 1.1.0 (fp32 / slim). 温中位是 `ocr.paddle` 每项 4 次调用去掉首次后的中位 wall 时间, 含插件选择, 不是基准数据 (基准见 `docs/benchmark.md`). 宿主不在前台时会被系统限速 (Pad 上各引擎都慢到 2.1-2.4 s) 或被缓存应用冻结卡住 (AVD_API_35_16K), 脚本因此先用 adb 启动宿主的启动器活动再发脚本.

| 设备 | API | ABI | 安装的 APK (文件名摘要) | 结果 | 温中位 (ORT) | `useOpenCL` (zh fp32, vs CPU) | Lite 1.1.0 fp32 / slim | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Sony XQ-AT72 (QV710AF65F) | 31 | arm64-v8a | zh 4F117434, en 4FB80072, zhHant 2ABC9F0D, ja A921353B, ko 451909D6, Lite AB15CF9B | 33 / 33 | 170-260 ms | nnapi, 241 vs 219 ms, 文本相同 | 197 / 187 ms | 5 个 `profile` 都命中对应包; raw 回退 0 |
| Sony XQ-DQ72 (QV770340J7) | 33 | arm64-v8a | zh 4F117434, en 4FB80072, Lite AB15CF9B | 18 / 18 | 105-128 ms | nnapi, 117 vs 117 ms | 125 / 125 ms | |
| Sony G8441 (BH900ASK9E) | 28 | arm64-v8a | zh 4F117434, ja A921353B, Lite AB15CF9B | 18 / 18 | 552-774 ms | nnapi, 637 vs 598 ms | 421 / 441 ms | |
| Sony G8441 (BH900ASK9E), 32 位包 | 28 | armeabi-v7a | zh E28140C9, ja B3A17010, Lite 863EA86E | 18 / 18 | 740-909 ms | nnapi, 847 vs 740 ms | 791 / 805 ms | `--abi armeabi-v7a` 安装, `primaryCpuAbi` 核对为 armeabi-v7a; 测完装回 arm64 包 |
| Redmi 22120RN86C (bek749scrwv4wo8h) | 33 | arm64-v8a | zh 4F117434, zhHant 2ABC9F0D, Lite AB15CF9B | 15 / 15 | 1239-1506 ms | nnapi, 1415 vs 1484 ms, 文本相同 | 1160 / 1103 ms | 首轮 13 / 19: zh 包在插件中心是关闭状态 (沿用同包名旧版的设置), 维护者打开后用 `--no-install` 补测; 无条件调用由已装的 v4 / v5 / v6 响应 (D22); raw 回退 0; SoC 为 MT6769, 宿主在前台, 耗时是机型水平 |
| Xiaomi Pad 23046RP50C (968e9f18) | 35 | arm64-v8a | zh 4F117434, en 4FB80072, Lite AB15CF9B | 18 / 18 | 437-530 ms | nnapi, 440 vs 466 ms | 496 / 502 ms | P3.5 释放后测; 无条件调用由已装的 v4 / v5 / v6 响应 (D22) |
| OnePlus OPD2413 (63751f63) | 35 | arm64-v8a | zh 4F117434, ko 451909D6, Lite AB15CF9B | 15 / 15 | 121-214 ms | nnapi, 169 vs 187 ms, 文本相同 | 177 / 175 ms | ColorOS: 三次安装由维护者在机上确认; 首轮 11 / 19 因 zh 在插件中心关闭; 维护者打开后第二轮 13 / 15: ko 路由因宿主早于 P3.3 (`profile: 'ko'` 落到 zh), zh 路由因脚本把插件中心关闭的 v5 / v6.tiny 也算作预期 (已改); 换成与 Redmi 相同的宿主后通过, 无条件调用由本插件 zh 响应; raw 回退 0 |
| AVD_API_24 | 24 | x86 | zh 61EB321F, ja D3DCAAF1 | 15 / 15 | 265-455 ms | 回退 cpu (API < 27), 333 vs 372 ms | - (Lite 无 x86) | `RAW_IMAGE` 低于 API 27 不适用, 两条路径都走编码图 |
| AVD_API_33 | 33 | x86_64 | zh 5AD7D7C8, ko DB9895EE | 15 / 15 | 308-419 ms | nnapi, 380 vs 308 ms | - | raw 回退 0 |
| AVD_API_35_16K | 35 | x86_64 (16 KB 页) | zh 5AD7D7C8, zhHant 8423519B | 15 / 15 | 148-412 ms | nnapi, 178 vs 175 ms | - | `getconf PAGE_SIZE` 16384; raw 回退 0; 覆盖 API 35 x86_64 |

精度与速度基线 (P4.2 / P4.3, 详见 `docs/benchmark.md`; CPU 4 线程, 1 次预热 + 10 次中位; "合计" 是 11 张图各自中位之和):

| 设备 | 档位 | 一致率 (vs 旧 Paddle-Lite) | 一致率 (vs fp32) | det + rec 中位耗时 | 备注 |
| --- | --- | --- | --- | --- | --- |
| XQ-AT72 (API 31, arm64) | fp32 | 56 / 56 (100%, Lite 1.1.0 fp32, 4 张大图) | - | zh-settings 200 + 633 ms; 合计 2028 + 8716 ms | 4 张大图 wall 合计 3468 ms, Lite fp32 3292 ms |
| XQ-AT72 (API 31, arm64) | slim | 56 / 56 (Lite slim vs ORT fp32) | 246 / 251 (98.0%) | zh-settings 210 + 596 ms; 合计 2118 + 8074 ms | rec -7.4%, 达标 |
| AVD_API_33 (x86_64) | fp32 | - (Lite 无 x86_64) | - | zh-settings 183 + 494 ms; 合计 1940 + 6894 ms | |
| AVD_API_33 (x86_64) | slim | - | 246 / 251 (98.0%) | zh-settings 197 + 585 ms; 合计 2071 + 6764 ms | rec -1.9%, 达标; 单图 rec 在模拟器上有升有降, 只判合计 |
| XQ-DQ72 (API 33, arm64) | fp32 | 19 / 19 (zh-settings) | 19 / 19 (slim, zh-settings) | zh-settings det 约 136-140 + rec 476 ms (slim 429 ms) | wall 636 ms, Lite fp32 624 ms |

---

## 附录 G. 已评估暂缓

| 事项 | 结论 |
| --- | --- |
| 自编译 Paddle-Lite x86 / x86_64 | 官方不提供也不维护 x86 Android 目标, 需自建交叉编译链且 `.nb` 模型要按目标重新优化, 维护成本远高于换运行时 (第一轮已否决, D1) |
| 只在宿主应用内经 Binder 使用, 不打包 | 打包 APK 在 x86 上仍无 Paddle OCR, 与补齐 4 ABI 的目标矛盾 (第一轮已否决, D3) |
| 去掉 cls | 旧 v3 行为含 cls, 旋转文本会退化 (第一轮已否决, D4) |
| slim 用 fp32 占位 / 去掉 slim | 维护者选定动态量化 (D5); 这两项作为 Q2 的回退选项保留 |
| 新插件改用新包名, 旧包名退役 | 用户升级要重装, 索引 `retired-packages` 多一条; 接管旧标识更平滑 (第二轮已否决, D6) |
| 旧插件只保留在仓库历史里不发布 | 维护者要求保留为官方插件 (第一轮, D1 / D2) |
| 只做中文 mobile 单档 | 维护者选定多语种 flavor (第二轮, D9) |
| 单 APK 内置 5 语种 | 单 APK 超过 100 MB, 大部分用户只需一种语言 (第三轮已否决, D11) |
| 12 语种一次做完 | 2.0.0 先做 5 种, 其余 2.1.0 (第三轮, D10) |
| minSdk 26 (与 v4 一致) | 旧 v3 用户在 API 24 / 25 上会失去升级路径 (第三轮已否决, D12) |
| 宿主打包 v4-v6 | D10 维持, 列为 P6.2 候选 |
| 与 Rapid OCR 合并 | 两者契约与模型家族不同, 用户已按名称选择 |
