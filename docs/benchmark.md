# Benchmark

Measured on 2026-10-30 (roadmap P4.2 and P4.3) with the 2.0.0 release APKs
(versionCode 67, `releases/v2.0.0/`) and Paddle Lite 1.1.0 from the sibling repository
(`AutoJs6-Plugin-Paddle-OCR-PP-OCRv3-Paddle-Lite/releases/v1.1.0/`, source revision 688983d).

- slim (dynamic int8 rec) agrees with fp32 on 98.0% of the boxes and lowers the total rec time
  on both test devices, so `useSlim` stays.
- ONNX Runtime fp32 and Paddle Lite 1.1.0 read the Chinese and English images identically
  (56 of 56 boxes); wall times differ by about 5%.
- Paddle Lite 1.1.0 crashes when a service thread that has only seen small images gets a large
  one (roadmap appendix D Q14).

中文: slim 与 fp32 的结果一致率 98.0%, rec 总耗时在两台测试设备上都下降, `useSlim` 保留.
ONNX Runtime fp32 与 Paddle Lite 1.1.0 对中英文图片的结果完全一致 (56 / 56 个框), 耗时相差约 5%.
Paddle Lite 1.1.0 在 "先识别小图再识别大图" 时会崩溃, 见路线图附录 D Q14.

## Image set

`tools/device/make_benchmark_images.py` renders two 1080 x 1500 phone screens per language flavor
with headless Microsoft Edge: a light settings list and a dark notes page. Each flavor uses the
Windows font for its script (Microsoft YaHei, Segoe UI, Microsoft JhengHei, Yu Gothic UI, Malgun
Gothic). The host's 84 x 57 `paddle_ocr_test.png` is added as a small zh image. The images are
not committed. They are written to `.bak/visual/benchmark/` with `images.json`, which lists each
file's flavor, ground-truth lines and SHA-256. Other Edge or font versions render different
pixels; the hashes below identify the measured files.

| File | Flavor | Lines | SHA-256 |
|---|---|---|---|
| `host-paddle_ocr_test.png` | zh | - | `7231cde17f611eb83d018bf86c7752244b0bc877f60e7716646fc09423ffcfe0` |
| `zh-settings.png` | zh | 19 | `ea21bfc3533621ee170ed9fc70a0e16aee8220637be91422df7a241214995d84` |
| `zh-notes.png` | zh | 9 | `45c1c88c1bc87367ad6ccf32e6274b63abd1ffaff6ccc9ec4f89434bab0740af` |
| `en-settings.png` | en | 19 | `0b47c34f90f9c46de1331657190b9550aa4ea0982a06ed32623aa341983e7d9d` |
| `en-notes.png` | en | 9 | `9cccb2d0e02e6986e56c8acc6772e8f2fe98ced09a69681d1edfaa6daee41cb3` |
| `zhHant-settings.png` | zhHant | 19 | `04113b5adba2a23a4dd5a46bcfec4d089500435e035ccbd519d31621bb79fa6f` |
| `zhHant-notes.png` | zhHant | 9 | `65c896b760b8d7c9bf1e0ddee662dac70321a0b235daf73210ff2dac4f5e3e08` |
| `ja-settings.png` | ja | 19 | `cb907d3cddd0d28a34affa238edbec6eec12b706a103ce399244d6077980d609` |
| `ja-notes.png` | ja | 9 | `65b39e255404bd6f870ef075b52cb0fbc9b0ea0499a21ae9afe7c3039447f373` |
| `ko-settings.png` | ko | 19 | `b5db760bacf0fc25e5ab09f6345cbdd08491961b0db1efd56c016a67c5312af8` |
| `ko-notes.png` | ko | 9 | `c40b611ec51bbc5e8c60336cbd29d198319738752e7af6aeaf477e901aac7d1b` |

## Method

`tools/device/benchmark.py` pushes the images and a script to the AutoJs6 host. The script binds
each plugin service directly and calls `IOcrPlugin.detect` with the encoded PNG, so the times
exclude the host's plugin selection. Every run uses the CPU execution provider with 4 threads
(unless noted), makes 1 warm-up call (which includes the engine load) and 10 timed calls, and
pauses 2 s before the next run. The tables show medians.

- Wall: the binder call as the host script sees it.
- det / rec / total: the plugin's own times from the result extras. Paddle Lite results carry
  none, so Lite comparisons use wall times only.
- Ground truth: a line matches when some recognized text, or up to 4 consecutive ones, has a
  similarity of at least 0.8 with it, spaces ignored. Shown as matched (exact).
- Consistency: boxes of two runs matched by IoU >= 0.5 whose texts are equal (spaces ignored),
  over the larger box count.

Times printed by `tools/device/check_device.py` are smoke-test numbers, not benchmark data: they
go through `ocr.paddle` with plugin selection, make only a few calls and depend on the device
state. On XQ-AT72 its warm median moved between about 110 ms and 260 ms across sessions. The
smoke results of every device are in roadmap appendix F. ColorOS asks to confirm each
`adb install` on the phone, so a rerun there passes `--no-install`, which tests the installed
packages and still checks their versions and ABI.

```
python -I tools/device/make_benchmark_images.py
python -I tools/device/check_device.py --serial <serial> --flavor zh --flavor en --flavor zhHant --flavor ja --flavor ko --lite 1.1.0
python -I tools/device/benchmark.py --serial <serial> --nnapi --json <slim-vs-fp32.json>
python -I tools/device/benchmark.py --serial <serial> --flavor zh --lite --image zh-settings.png --image zh-notes.png --image en-settings.png --image en-notes.png --json <lite.json>
```

Before the Lite run, force-stop the Lite plugin (`adb shell am force-stop <package>`) so it starts
in a fresh process (see the crash below).

## slim vs fp32 (P4.3)

Pass line: consistency >= 95% and a lower total rec time.

| Device | Consistency | rec sum, fp32 -> slim | Wall sum, fp32 -> slim | Result |
|---|---|---|---|---|
| XQ-AT72 (API 31, arm64-v8a) | 246 / 251 (98.0%) | 8716 -> 8074 ms (-7.4%) | 11311 -> 10768 ms (-4.8%) | pass |
| AVD_API_33 (x86_64 emulator) | 246 / 251 (98.0%) | 6894 -> 6764 ms (-1.9%) | 9295 -> 9362 ms (+0.7%) | pass |

Both devices return the same text for all 25 runs, so the 5 differing boxes are the same too:
one in `zhHant-notes`, one in `ja-settings`, two in `ja-notes` (one or two characters each) and
one in `ko-settings`. The ground-truth accuracy of fp32 and slim is identical on every image.

XQ-AT72 per image (median ms):

| Image | Ground truth | fp32 det / rec / total | slim det / rec / total | Equal boxes |
|---|---|---|---|---|
| `host-paddle_ocr_test` | - | 4 / 32 / 36 | 8 / 35 / 43 | 1 / 1 |
| `zh-settings` | 19 / 19 (17) | 200 / 633 / 838 | 210 / 596 / 800 | 19 / 19 |
| `zh-notes` | 9 / 9 (5) | 202 / 498 / 702 | 201 / 460 / 664 | 9 / 9 |
| `en-settings` | 19 / 19 (19) | 203 / 687 / 893 | 202 / 626 / 832 | 19 / 19 |
| `en-notes` | 9 / 9 (9) | 200 / 564 / 770 | 200 / 529 / 734 | 9 / 9 |
| `zhHant-settings` | 17 / 19 (11) | 202 / 920 / 1122 | 200 / 822 / 1028 | 30 / 30 |
| `zhHant-notes` | 9 / 9 (1) | 202 / 626 / 830 | 200 / 566 / 772 | 15 / 16 |
| `ja-settings` | 15 / 19 (9) | 204 / 1079 / 1288 | 206 / 966 / 1178 | 33 / 34 |
| `ja-notes` | 9 / 9 (0) | 198 / 755 / 962 | 202 / 686 / 892 | 18 / 20 |
| `ko-settings` | 17 / 19 (12) | 204 / 1366 / 1582 | 220 / 1222 / 1442 | 43 / 44 |
| `ko-notes` | 4 / 9 (3) | 209 / 1556 / 1776 | 270 / 1567 / 1847 | 50 / 50 |

Session loading for the warm-up call took 98-147 ms with fp32 and 75-103 ms with slim. On the
emulator, per-image rec times move in both directions (host CPU scheduling); only the sum is
judged. The lower accuracy of zhHant, ja and ko comes from the PP-OCRv3 models themselves (the
ko detector boxes words rather than lines) and is the same for fp32 and slim.

NNAPI (`useOpenCL: true`, zh fp32): the provider reported `nnapi` and the text equals the CPU
run (29 / 29 boxes on both devices). Wall sums: XQ-AT72 1649 -> 1729 ms, AVD_API_33 1534 ->
1196 ms. Below API 27 the plugin falls back to the CPU provider.

## Paddle Lite 1.1.0 vs ONNX Runtime fp32 (P4.2)

XQ-AT72, large images, fresh Lite process (median wall ms):

| Image | ORT fp32 | Lite fp32 | Lite slim | Equal, Lite fp32 | Equal, Lite slim |
|---|---|---|---|---|---|
| `zh-settings` | 874 | 827 | 837 | 19 / 19 | 19 / 19 |
| `zh-notes` | 748 | 692 | 674 | 9 / 9 | 9 / 9 |
| `en-settings` | 999 | 957 | 971 | 19 / 19 | 19 / 19 |
| `en-notes` | 847 | 817 | 774 | 9 / 9 | 9 / 9 |

Consistency is 56 / 56 (100%) for Lite fp32 and for Lite slim, and 57 / 57 with the host image
from an earlier run, against the expected >= 95%. The ground-truth accuracy is the same for both
engines: zh 19 / 19 (17) and 9 / 9 (5), en 19 / 19 (19) and 9 / 9 (9). The wall sum is 3468 ms for
ONNX Runtime and 3292 ms for Lite fp32 (ONNX Runtime 5.1% slower). On XQ-DQ72 (API 33),
`zh-settings` gave 19 / 19 equal boxes and 636 ms (ORT fp32) vs 624 ms (Lite fp32).

### Paddle Lite 1.1.0 crash

Lite 1.1.0 runs its engine on whichever binder thread receives the call (calls are serialized by a
lock). The native detector warms up with one 960 x 960 input on the first thread only. When a
thread that has only run small detector inputs later gets a large one, the process dies with
SIGSEGV (SEGV_ACCERR) in `memset`, frame #01 at pc `0xbc800` of `libpaddle_light_api_shared.so`
(BuildId `46c961e2...`), and the host sees `DeadObjectException` for that call and every later
one. Reproduced on XQ-AT72 and XQ-DQ72: several calls with `paddle_ocr_test.png` (spread over
binder threads), then a 1080 x 1500 screen. A fresh process given only large images, or a single
small call followed by a large one, does not crash. The comparison above therefore uses large
images in a fresh process. ONNX Runtime is not affected. `libpaddle_light_api_shared.so` in
1.1.0 is byte-identical to the one in 1.0.5, so the published versions may crash the same way
(not tested). The fix belongs to the Lite repository before its release (roadmap P5.2,
appendix D Q14).
