"""Decode same-family native style references and old provisional art; no game edits."""
import hashlib
import json
from asset4_style_reference_audit import ROOT, GAME, decode

PACK = ROOT / "docs/reports/assets/asset28_preview_2026-10-05"
REFERENCES = [
    (GAME / "gfx/interface/icons/invention_icons/intensive_agriculture.dds", "vanilla_intensive_agriculture.png", "STYLE_REFERENCE_ONLY"),
    (GAME / "gfx/interface/icons/invention_icons/mechanical_tools.dds", "vanilla_mechanical_tools.png", "STYLE_REFERENCE_ONLY"),
    (GAME / "gfx/interface/icons/invention_icons/academia.dds", "vanilla_academia.png", "STYLE_REFERENCE_ONLY"),
    (ROOT / "gfx/interface/icons/invention_icons/preview_basileia_agricultural_implements.dds", "old_agricultural_implements.png", "PREVIOUS_PROVISIONAL_ART_ONLY"),
    (ROOT / "gfx/interface/icons/invention_icons/preview_basileia_traditional_papermaking.dds", "old_traditional_papermaking.png", "PREVIOUS_PROVISIONAL_ART_ONLY"),
    (ROOT / "gfx/interface/icons/invention_icons/preview_basileia_organized_workshops.dds", "old_organized_workshops.png", "PREVIOUS_PROVISIONAL_ART_ONLY"),
]

def main():
    directory = PACK / "references"
    directory.mkdir(parents=True, exist_ok=True)
    rows = []
    for source, filename, role in REFERENCES:
        target = directory / filename
        if target.exists():
            raise FileExistsError(target)
        picture = decode(source)
        picture.save(target)
        rows.append({"source":str(source), "source_sha256":hashlib.sha256(source.read_bytes()).hexdigest(), "preview":"references/"+filename, "dimensions":list(picture.size), "role":role})
    (PACK / "native_references.json").write_text(json.dumps(rows, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"decoded_references":len(rows), "game_files_changed":False}))

if __name__ == "__main__":
    main()

