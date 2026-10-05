"""Read-only pre-publication checks for the current asset-only Git changes."""
from collections import Counter
from io import BytesIO
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
import sys

from PIL import Image
from asset4_style_reference_audit import ROOT, GAME, TOKENS, pairs
from building_dds_compat import assert_export_layout, matches_export_hash
from validate_asset_color_layout import mip_images


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def sha(payload):
    return hashlib.sha256(payload).hexdigest()


def objects(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from objects(child)
    elif isinstance(value, list):
        for child in value:
            yield from objects(child)


def tokens(data):
    return [t for t in TOKENS.findall(data.decode("utf-8-sig")) if not t.startswith("#")]


def without_visuals(items):
    return [(key, without_visuals(value) if isinstance(value, list) else value)
            for key, value in pairs(items) if key not in ("texture", "icon")]


def main():
    staged = "--staged" in sys.argv
    args = ["diff", "--cached"] if staged else ["diff"]
    paths = {p for p in git(*args, "--name-only", "--", "gfx").decode().splitlines() if p.endswith(".dds")}
    if not staged:
        paths.update(p for p in git("ls-files", "--others", "--exclude-standard", "--", "gfx").decode().splitlines() if p.endswith(".dds"))
    assert paths, "No graphic assets selected"
    metadata = {}
    for report in (ROOT / "docs/reports/assets").rglob("*.json"):
        value = json.loads(report.read_text(encoding="utf-8-sig"))
        for row in objects(value):
            relative = row.get("dds") or row.get("target_dds")
            if isinstance(relative, str) and relative in paths:
                metadata.setdefault(relative, []).append((report, row))
    results = []
    for relative in sorted(paths):
        assert relative.startswith(("gfx/interface/icons/", "gfx/unit_illustrations/")), relative
        payload = (ROOT / relative).read_bytes()
        if staged:
            assert git("show", ":" + relative) == payload, "Staged DDS differs from verified file"
        assert payload[:4] == b"DDS ", relative
        assert_export_layout(payload, relative)
        height, width = struct.unpack_from("<II", payload, 12)
        count = struct.unpack_from("<I", payload, 28)[0]
        assert width == height and width in (208, 256, 512), relative
        assert count == width.bit_length(), relative
        decoded_levels = list(mip_images(payload))
        assert len(decoded_levels) == count
        offset, size = 128, width
        for image in decoded_levels:
            native = Image.frombytes("RGBA", (size, size), payload[offset:offset + size * size * 4], "raw", "BGRA")
            assert image.tobytes() == native.tobytes(), "Native decoder disagreement: " + relative
            offset += size * size * 4
            size = max(1, size // 2)
        assert offset == len(payload)
        proof = None
        for report, row in metadata.get(relative, []):
            hashes = [row.get(k) for k in ("dds_sha256", "export_sha256", "sha256", "after")]
            if any(isinstance(h, str) and re.fullmatch(r"[0-9a-fA-F]{64}", h)
                   and matches_export_hash(payload, h, relative) for h in hashes):
                proof = report, row
                if row.get("target_png"):
                    break
        assert proof, "No matching export/hash evidence: " + relative
        report, row = proof
        expected_png = report.parent / row["target_png"] if row.get("target_png") else None
        if expected_png:
            expected = Image.open(expected_png).convert("RGBA")
            assert decoded_levels[0].tobytes() == expected.tobytes(), "PNG colour/alpha disagreement: " + relative
        if row.get("mip_hashes"):
            assert len(row["mip_hashes"]) == count
            for image, mip in zip(decoded_levels, row["mip_hashes"], strict=True):
                assert image.size == (mip["size"], mip["size"])
                assert sha(image.tobytes()) == mip["rgba_sha256"], relative
        source = row.get("source")
        source_hash = row.get("source_sha256")
        if isinstance(source, str) and source_hash:
            assert sha((report.parent / source).read_bytes()) == source_hash.lower(), "Pinned source changed"
        alpha = decoded_levels[0].getchannel("A")
        assert alpha.getbbox() is not None
        if relative.startswith("gfx/unit_illustrations/"):
            assert alpha.getextrema() == (255, 255), "Unit illustration must be opaque"
        elif relative.startswith("gfx/interface/icons/building_icons/"):
            # A framed building portrait may be fully opaque (the approved
            # laboratory), unlike the transparent technology/PM cutouts.
            assert alpha.getextrema()[0] in (0, 255) and alpha.getextrema()[1] >= 240, relative
        else:
            assert alpha.getextrema()[0] == 0 and alpha.getextrema()[1] >= 240, relative
        results.append({"dds": relative, "sha256": sha(payload), "size": width, "mips": count,
                        "alpha_range": list(alpha.getextrema()),
                        "native_storage": True, "export_proof": report.relative_to(ROOT).as_posix(),
                        "matches_target_png": bool(expected_png)})
    definitions = git(*args, "--name-only", "--", "common").decode().splitlines()
    for relative in definitions:
        assert relative.startswith(("common/buildings/", "common/production_methods/", "common/technology/technologies/")), "Out-of-scope gameplay file: " + relative
        old = git("show", "HEAD:" + relative)
        new = git("show", ":" + relative) if staged else (ROOT / relative).read_bytes()
        assert without_visuals(tokens(old)) == without_visuals(tokens(new)), "Non-visual gameplay changes: " + relative
        for _, block in pairs(tokens(new)):
            if isinstance(block, list):
                for field, value in pairs(block):
                    if field in ("texture", "icon") and isinstance(value, str):
                        assert (ROOT / value).is_file() or (GAME / value).is_file(), "Missing referenced image: " + value
    print(json.dumps({"status": "PASS_ASSET_ONLY_RELEASE", "mode": "STAGED" if staged else "WORKTREE",
                      "dds_count": len(results), "mips_verified": sum(r["mips"] for r in results),
                      "dimensions": dict(Counter(str(r["size"]) for r in results)),
                      "definition_files": definitions, "game_tested": False, "assets": results}, indent=2))


if __name__ == "__main__":
    main()
