"""Decode installed native references and snapshot the mod; preview-only."""
import hashlib
import json
from pathlib import Path

from asset4_style_reference_audit import GAME, ROOT, catalog, decode, field

PACK = ROOT / "docs/reports/assets/asset5_preview_2026-10-02"
SUBJECTS = {
    "GOOD": ("common/goods", ["coal", "iron", "sulfur"]),
    "TECH": ("common/technology/technologies", ["mechanical_tools", "academia"]),
    "BUILDING": ("common/buildings", ["building_coal_mine", "building_iron_mine"]),
    "PM": ("common/production_methods", ["pm_picks_and_shovels_building_coal_mine", "pm_atmospheric_engine_pump_building_coal_mine", "pm_open_hearth_process"]),
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    PACK.mkdir(parents=True, exist_ok=True)
    refs = PACK / "references"
    refs.mkdir(exist_ok=True)
    manifest = []
    for family, (folder, ids) in SUBJECTS.items():
        native = catalog(folder, native_only=True)
        for key in ids:
            tokens, _ = native[key]
            relative = field(tokens, "icon" if family == "BUILDING" else "texture")
            source = GAME / relative
            target = refs / f"vanilla_{key}.png"
            if target.exists():
                raise FileExistsError(target)
            rgba = decode(source)
            rgba.save(target)
            manifest.append({"family": family, "id": key, "native_texture": relative,
                             "native_sha256": digest(source), "preview": str(target.relative_to(PACK)),
                             "role": "STYLE_ONLY_NOT_AN_ORIGINAL_ASSET", "size": list(rgba.size)})
    (PACK / "native_references.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    baseline = {str(p.relative_to(ROOT)).replace("\\", "/"): digest(p)
                for folder in ("common", "gfx") for p in (ROOT / folder).rglob("*") if p.is_file()}
    target_manifest = json.loads((ROOT / "docs/reports/assets/ASSET5_LOT_2_PHOSPHATE_MINERAIS_2026-10-02.json").read_text(encoding="utf-8"))
    assert all(not (ROOT / e["target_dds"]).exists() for e in target_manifest["entries"])
    (PACK / "gameplay_and_gfx_baseline.json").write_text(json.dumps(baseline, indent=2), encoding="utf-8")
    print(json.dumps({"native_refs": len(manifest), "protected_files": len(baseline), "pack": str(PACK)}))


if __name__ == "__main__":
    main()
