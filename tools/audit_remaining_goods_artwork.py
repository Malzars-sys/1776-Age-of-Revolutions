"""Refresh goods artwork inventory and reference previews without game edits."""
import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from asset4_style_reference_audit import ROOT, GAME, catalog, decode, field, header, locs, resolve, state

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--pack", default=".asset-cache/goods_audit")
PACK = (ROOT / parser.parse_args().pack).resolve()
OUTPUT_ROOTS = ((ROOT / "docs/reports/assets").resolve(), (ROOT / ".asset-cache").resolve())
if not any(base in PACK.parents for base in OUTPUT_ROOTS):
    raise ValueError("Audit pack must be inside the artwork reports or ignored asset cache")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def font(size):
    return ImageFont.truetype("C:/Windows/Fonts/arial.ttf", size)


def sheet(rows, output, columns=7):
    width, height = 160, 158
    result = Image.new("RGB", (columns * width, ((len(rows) + columns - 1) // columns) * height), "#263039")
    pen = ImageDraw.Draw(result)
    for index, row in enumerate(rows):
        x, y = index % columns * width, index // columns * height
        pen.text((x + 8, y + 7), row["label_fr"][:22], fill="white", font=font(12))
        pen.text((x + 8, y + 24), row["id"][:25], fill="#bdc6cb", font=font(10))
        if row.get("decode_ok"):
            picture = decode(resolve(row["texture"]))
            picture.thumbnail((100, 100), Image.Resampling.LANCZOS)
            result.paste(picture, (x + (width - picture.width) // 2, y + 40), picture)
        status = "COPPER EXCLUDED" if row["excluded"] else row["status"]
        pen.text((x + 8, y + 143), status[:24], fill="#ffbd76" if row["needs_icon"] else "#a7c7b1", font=font(10))
    result.save(output)


def main():
    PACK.mkdir(parents=True, exist_ok=True)
    french = locs("french")
    errors = []
    for path in sorted((GAME / "gfx").glob("error_*.dds")):
        picture = decode(path)
        errors.append((str(path), picture.size, hashlib.sha256(picture.tobytes()).hexdigest()))
    rows = []
    for key, (tokens, definition) in sorted(catalog("common/goods").items()):
        texture = field(tokens, "texture")
        target = resolve(texture)
        row = {"id": key, "label_fr": french.get(key, key), "texture": texture,
               "status": state(texture), "excluded": key == "copper", "definition": str(definition),
               "decode_ok": False, "copied_error_image": None}
        if target:
            row["sha256"] = sha(target)
            try:
                picture = decode(target)
                digest = hashlib.sha256(picture.tobytes()).hexdigest()
                row.update(decode_ok=True, header=header(target), alpha_bbox=picture.getchannel("A").getbbox())
                row["copied_error_image"] = next((p for p, size, h in errors if size == picture.size and h == digest), None)
            except Exception as exc:
                row["decode_error"] = str(exc)
        row["needs_icon"] = (not row["excluded"] and
                             (row["status"] in {"PLACEHOLDER", "MISSING_FILE", "NO_EXPLICIT_VISUAL"}
                              or not row["decode_ok"] or not row.get("alpha_bbox") or bool(row["copied_error_image"])))
        rows.append(row)
    summary = {"date": "2026-10-06", "scope": "goods only; copper excluded", "total_goods": len(rows),
               "states": dict(Counter(row["status"] for row in rows)),
               "needs_icons": [row["id"] for row in rows if row["needs_icon"]],
               "missing_or_undecodable": [row["id"] for row in rows if not row["decode_ok"]],
               "notes": ["Native reuse is not a missing image.", "No recipe, statistic or runtime artwork is changed.",
                         "This inventory does not claim game-engine or redistribution-license validation."],
               "goods": rows}
    (PACK / "goods_audit.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (PACK / "goods_inventory.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        keys = ["id", "label_fr", "texture", "status", "excluded", "needs_icon", "decode_ok", "definition"]
        writer = csv.DictWriter(stream, fieldnames=keys, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    sheet(rows, PACK / "ALL_GOODS_CURRENT.png")
    selected = [row for row in rows if resolve(row["texture"]) and resolve(row["texture"]).is_relative_to(ROOT)]
    selected.extend(row for row in rows if row["id"] in {"tools", "engines", "steel"})
    sheet(selected, PACK / "CUSTOM_GOODS_AND_NATIVE_REFERENCES.png", 5)
    refs = PACK / "references"
    refs.mkdir(exist_ok=True)
    for key in ("tools", "engines", "steel"):
        row = next(row for row in rows if row["id"] == key)
        decode(resolve(row["texture"])).save(refs / ("vanilla_" + key + ".png"))
    baseline = PACK / "protected_runtime_baseline.json"
    if not baseline.exists():
        hashes = {str(path.relative_to(ROOT)).replace("\\", "/"): sha(path)
                  for directory in ("common", "gfx", "gui", "localization")
                  for path in sorted((ROOT / directory).rglob("*")) if path.is_file()}
        baseline.write_text(json.dumps(hashes, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "goods"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
