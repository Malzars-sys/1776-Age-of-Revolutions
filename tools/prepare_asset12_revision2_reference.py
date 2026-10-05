"""Decode one installed technology icon for preview comparison only."""
import hashlib
import json
from asset4_style_reference_audit import ROOT, GAME, decode

pack = ROOT / 'docs/reports/assets/asset12_preview_2026-10-04/revision_2'
relative = 'gfx/interface/icons/invention_icons/watertube_boiler.dds'
source = GAME / relative
output = pack / 'references/vanilla_watertube_boiler.png'
if output.exists():
    raise FileExistsError(output)
output.parent.mkdir(parents=True, exist_ok=True)
image = decode(source)
image.save(output)
metadata = {'id': 'watertube_boiler', 'role': 'STYLE_AND_DISTINCTION_REFERENCE_ONLY',
            'native_texture': relative,
            'native_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'preview': output.relative_to(pack).as_posix(), 'dimensions': list(image.size)}
(pack / 'native_references.json').write_text(json.dumps(metadata, indent=2)+'\n', encoding='utf-8')
print(json.dumps(metadata, indent=2))
