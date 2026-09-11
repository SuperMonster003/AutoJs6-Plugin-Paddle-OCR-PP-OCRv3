# Paddle Lite native libraries

The original upstream release, build flags and download URL for the checked-in
`libpaddle_light_api_shared.so` files were not recorded in this repository. This
adaptation does not assign an unverified upstream version to those binaries.
Both files were measured with PT_LOAD alignment `0x10000` on 2026-09-11.

The original arm64 SHA-256 was
`7d83c3ee78648d2bdeb5b354707b3f1389bd644de17dcbd359f1199b1b5e4ba7`.
Use `dynsym-normalization.json` as the authoritative original/current digest
receipt: `tools/16kb/normalize_dynsym.py` corrects the `.dynsym` section header's
first-global-symbol index from 3 to 10, as required by current LLVM LLD. The tool
pins the input SHA-256 and verifies that every byte in every PT_LOAD segment is
unchanged. This repair changes linker metadata only, not executable code or data.

`libc++_shared.so` now comes from Android NDK `28.2.13676358`, under
`toolchains/llvm/prebuilt/windows-x86_64/sysroot/usr/lib/`:

- arm64-v8a: `aarch64-linux-android/libc++_shared.so`, PT_LOAD `0x4000`.
- armeabi-v7a: `arm-linux-androideabi/libc++_shared.so`, PT_LOAD `0x1000` (32-bit advisory).

See `native-libraries.provenance.json` for the current SHA-256 and alignment of
each file. The JNI bridge is rebuilt with the same NDK and explicit 16 KB maximum
and common page sizes. A 16 KB arm64 device OCR smoke remains required; ELF
verification and 4 KB execution do not substitute for that test.

中文: 原 Paddle Lite 预编译库的具体版本和下载来源未记录, 不推测其来源.
arm64 库只修正 `.dynsym` 节头, 全部 PT_LOAD 内容逐字节保持一致.
libc++ 已统一为 NDK r28.2 副本, 具体摘要与对齐见同目录 provenance JSON.
