"""Prepare three technology preview packs, native references and definition checks only."""
import hashlib
import json
from asset4_style_reference_audit import ROOT, GAME, decode, field, pairs, parse
PACK_NAMES = ["asset25_preview_2026-10-05"]
for name in PACK_NAMES:
    pack = ROOT / "docs/reports/assets" / name
    plan = json.loads((pack / "generation_plan.json").read_text(encoding="utf-8"))
    refs = pack / "references"
    refs.mkdir(exist_ok=True)
    metadata = []
    for relative in plan["style_references"]:
        output = ROOT / relative
        key = output.stem.removeprefix("vanilla_")
        native = f"gfx/interface/icons/invention_icons/{key}.dds"
        source = GAME / native
        if output.exists():
            raise FileExistsError(output)
        picture = decode(source)
        picture.save(output)
        metadata.append({"id":key, "role":"STYLE_REFERENCE_ONLY", "native_texture":native, "native_sha256":hashlib.sha256(source.read_bytes()).hexdigest(), "preview":output.relative_to(pack).as_posix(), "dimensions":list(picture.size)})
    checks = []
    for entry in plan["entries"]:
        tokens = dict(pairs(parse(ROOT / entry["definition"])))[entry["id"]]
        assert field(tokens,"texture") == entry["current_texture"]
        assert field(tokens,"can_research") != "no"
        assert field(tokens,"era") == entry["era"]
        assert not (ROOT / entry["target_dds"]).exists()
        checks.append({"key":entry["key"],"active_researchable_technology":True,"binding":field(tokens,"texture"),"new_target_available":True})
    (pack / "native_references.json").write_text(json.dumps(metadata,indent=2)+"\n",encoding="utf-8")
    (pack / "selection_validation.json").write_text(json.dumps({"status":"PASS_ACTIVE_PLACEHOLDER_SELECTION", "entries":checks},indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"pack":name,"references":len(metadata),"technology_checks":len(checks),"game_files_changed":False}))
