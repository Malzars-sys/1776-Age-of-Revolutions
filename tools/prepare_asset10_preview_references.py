"""Preview-only decode of installed maritime technology style references."""
import hashlib
import json
from asset4_style_reference_audit import ROOT, GAME, decode

PACK = ROOT / 'docs/reports/assets/asset10_preview_2026-10-04'

def main():
    refs = PACK / 'references'
    refs.mkdir(parents=True, exist_ok=True)
    metadata = []
    for key in ['navigation', 'mechanical_tools', 'crystal_glass']:
        relative = f'gfx/interface/icons/invention_icons/{key}.dds'
        source = GAME / relative
        output = refs / f'vanilla_{key}.png'
        if output.exists():
            raise FileExistsError(output)
        image = decode(source)
        image.save(output)
        metadata.append({'id': key, 'role': 'STYLE_REFERENCE_ONLY_NOT_A_NEW_ASSET',
                         'native_texture': relative,
                         'native_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                         'preview': output.relative_to(PACK).as_posix(), 'dimensions': list(image.size)})
    (PACK / 'native_references.json').write_text(json.dumps(metadata, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'native_references': len(metadata), 'game_files_changed': False}))

if __name__ == '__main__':
    main()
