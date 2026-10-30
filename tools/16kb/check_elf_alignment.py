"""Report the ELF PT_LOAD alignment of every native library in AARs, APKs or directories.

64-bit libraries (arm64-v8a, x86_64) must have every PT_LOAD segment aligned to at least
16 KB, with matching file offset and virtual address modulo 16 KB; the exit status is 1
otherwise. 32-bit libraries (armeabi-v7a, x86) are reported only, as in the build gate.

Usage:
  python -I tools/16kb/check_elf_alignment.py ARCHIVE_OR_DIR [...] [--json]
"""
import argparse
import json
from pathlib import Path
import struct
import sys
import zipfile

PAGE = 16384


def load_segments(data):
    if data[:4] != b"\x7fELF":
        raise ValueError("not an ELF file")
    is64 = data[4] == 2
    endian = "<" if data[5] == 1 else ">"
    if is64:
        phoff = struct.unpack_from(endian + "Q", data, 32)[0]
        phsize, phnum = struct.unpack_from(endian + "HH", data, 54)
        layout = endian + "IIQQQQQQ"
    else:
        phoff = struct.unpack_from(endian + "I", data, 28)[0]
        phsize, phnum = struct.unpack_from(endian + "HH", data, 42)
        layout = endian + "IIIIIIII"
    segments = []
    for index in range(phnum):
        fields = struct.unpack_from(layout, data, phoff + index * phsize)
        if is64:
            kind, _, offset, address, _, _, _, alignment = fields
        else:
            kind, offset, address, _, _, _, _, alignment = fields
        if kind == 1:
            segments.append((offset, address, alignment))
    return is64, segments


def libraries(path):
    if path.is_dir():
        for item in sorted(path.rglob("*.so")):
            yield item.relative_to(path).as_posix(), item.read_bytes()
        return
    with zipfile.ZipFile(path) as archive:
        for name in sorted(archive.namelist()):
            if name.endswith(".so"):
                yield name, archive.read(name)


def check(path):
    results = []
    for name, data in libraries(path):
        is64, segments = load_segments(data)
        aligned = all(alignment >= PAGE and (offset - address) % PAGE == 0 for offset, address, alignment in segments)
        results.append({
            "library": name,
            "bits": 64 if is64 else 32,
            "bytes": len(data),
            "loadAlignments": sorted({alignment for _, _, alignment in segments}),
            "aligned16k": aligned,
            "enforced": is64,
        })
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--json", action="store_true", help="Print the full report as JSON.")
    args = parser.parse_args()

    report = {path.name: check(path) for path in args.paths}
    failed = [f"{source}:{item['library']}" for source, items in report.items() for item in items
              if item["enforced"] and not item["aligned16k"]]
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        for source, items in report.items():
            for item in items:
                status = "ok" if item["aligned16k"] else ("FAIL" if item["enforced"] else "advisory")
                alignments = ",".join(hex(value) for value in item["loadAlignments"])
                print(f"{status:8} {source}:{item['library']} ({item['bits']}-bit, align {alignments}, {item['bytes']} bytes)")
    print(f"{sum(len(items) for items in report.values())} libraries, {len(failed)} enforced failures")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
