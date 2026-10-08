"""Decode three same-family native technology references; no game edits."""
import hashlib
import json
from asset4_style_reference_audit import ROOT, GAME, decode

PACK = ROOT / "docs/reports/assets/asset29_preview_2026-10-05"
REFERENCES = [
    ("rationalism", "vanilla_rationalism.png"),
    ("medical_degrees", "vanilla_medical_degrees.png"),
    ("pharmaceuticals", "vanilla_pharmaceuticals.png"),
]

def main():
    directory = PACK / "references"
    directory.mkdir(parents=True, exist_ok=True)
    rows = []
    for key, filename in REFERENCES:
        source = GAME / "gfx/interface/icons/invention_icons" / (key + ".dds")
        target = directory / filename
        if target.exists():
            raise FileExistsError(target)
        picture = decode(source)
        picture.save(target)
        rows.append({"source":str(source),"source_sha256":hashlib.sha256(source.read_bytes()).hexdigest(),"preview":"references/"+filename,"dimensions":list(picture.size),"role":"STYLE_REFERENCE_ONLY"})
    (PACK / "native_references.json").write_text(json.dumps(rows,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"decoded_references":len(rows),"game_files_changed":False}))

if __name__ == "__main__":
    main()

