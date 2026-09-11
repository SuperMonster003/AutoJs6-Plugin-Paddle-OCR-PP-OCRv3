"""Normalize the locked Paddle-Lite DSO's non-allocated .dynsym section-header sh_info.

Only a section-header word is changed. All PT_LOAD bytes, dynamic symbols, hashes and relocations
must stay byte-identical. Newer LLD correctly rejects the old, inconsistent local-symbol count.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct

ORIGINAL_SHA256 = "7d83c3ee78648d2bdeB5b354707b3f1389bd644de17dcbd359f1199b1b5e4ba7".lower()


def normalize(original: bytes):
    if hashlib.sha256(original).hexdigest() != ORIGINAL_SHA256:
        raise ValueError("Input is not the locked original arm64 Paddle-Lite DSO")
    if original[:7] != b"\x7fELF\x02\x01\x01":
        raise ValueError("Expected ELF64 little endian")
    data = bytearray(original)
    shoff = struct.unpack_from("<Q", data, 40)[0]
    shsize, count = struct.unpack_from("<HH", data, 58)
    changes = []
    for index in range(count):
        at = shoff + index * shsize
        if struct.unpack_from("<I", data, at + 4)[0] != 11:
            continue
        offset, size = struct.unpack_from("<QQ", data, at + 24)
        stride = struct.unpack_from("<Q", data, at + 56)[0]
        binding = [data[symbol + 4] >> 4 for symbol in range(offset, offset + size, stride)]
        first_global = next(i for i, value in enumerate(binding) if value != 0)
        if any(value == 0 for value in binding[first_global:]):
            raise ValueError("Local and global dynamic symbols are interleaved")
        old = struct.unpack_from("<I", data, at + 44)[0]
        struct.pack_into("<I", data, at + 44, first_global)
        changes.append(dict(fileOffset=at + 44, before=old, after=first_global))
    if len(changes) != 1 or changes[0]["before"] != 3 or changes[0]["after"] != 10:
        raise ValueError("Unexpected original symbol table")
    phoff = struct.unpack_from("<Q", data, 32)[0]
    phsize, phcount = struct.unpack_from("<HH", data, 54)
    load_hashes = []
    for at in range(phoff, phoff + phsize * phcount, phsize):
        if struct.unpack_from("<I", data, at)[0] != 1:
            continue
        offset = struct.unpack_from("<Q", data, at + 8)[0]
        size = struct.unpack_from("<Q", data, at + 32)[0]
        if data[offset:offset + size] != original[offset:offset + size]:
            raise ValueError("Patch would modify a PT_LOAD segment")
        load_hashes.append(dict(offset=offset, size=size, sha256=hashlib.sha256(data[offset:offset + size]).hexdigest()))
    return bytes(data), dict(beforeSha256=ORIGINAL_SHA256, afterSha256=hashlib.sha256(data).hexdigest(),
                            changes=changes, unchangedLoadSegments=load_hashes)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    corrected, receipt = normalize(args.input.read_bytes())
    args.output.write_bytes(corrected)
    args.receipt.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
