"""Decode reference icons only; never change game artwork or definitions."""
import hashlib
import json
from asset4_style_reference_audit import ROOT, GAME, decode

PACK = ROOT / "docs/reports/assets/asset26_preview_2026-10-05"
REFERENCES = [
    (GAME / "gfx/interface/icons/invention_icons/military_drill.dds", "vanilla_military_drill.png"),
    (GAME / "gfx/interface/icons/invention_icons/napoleonic_warfare.dds", "vanilla_napoleonic_warfare.png"),
    (GAME / "gfx/interface/icons/invention_icons/triage.dds", "vanilla_triage.png"),
    (ROOT / "gfx/interface/icons/invention_icons/1776_veterinary_science.dds", "existing_veterinary_science.png"),
]

def main():
    directory = PACK / "references"
    directory.mkdir(parents=True, exist_ok=True)
    rows = []
    for source, filename in REFERENCES:
        target = directory / filename
        if target.exists():
            raise FileExistsError(target)
        picture = decode(source)
        picture.save(target)
        rows.append({"source": str(source), "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(), "preview": "references/" + filename, "dimensions": list(picture.size), "role": "REFERENCE_ONLY_NOT_SELECTED_FOR_INTEGRATION"})
    (PACK / "native_references.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"decoded_references": len(rows), "game_files_changed": False}))

if __name__ == "__main__":
    main()
