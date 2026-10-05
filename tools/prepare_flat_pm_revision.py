"""Preserve references and snapshot game files; DDS decoding only, no artistic edits."""
from pathlib import Path
import hashlib
import json
import re
import shutil
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'docs/reports/assets/asset8_flat_revision_2026-10-03'
GAME = Path('C:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game')
PREVIOUS = ROOT / 'docs/reports/assets/asset8_preview_2026-10-03'
USER_REFS = [
    'codex-clipboard-ddcd534c-18f8-41e2-9401-c90a965bd4a8.png',
    'codex-clipboard-2f3aa9be-6cb9-440a-be0b-461c1f03ecb3.png',
    'codex-clipboard-11d0a2e8-61ee-460e-913e-392f5b1aa6ba.png',
    'codex-clipboard-552e8ff1-98de-4898-b417-759e04690249.png',
]

def digest(data):
    return hashlib.sha256(data).hexdigest()

def write(name, data):
    (PACK / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def blocks(text):
    for match in re.finditer(r'^([A-Za-z0-9_]+)\s*=\s*\{', text, re.M):
        pos, depth = match.end(), 1
        while depth:
            char = text[pos]
            depth += (char == '{') - (char == '}')
            pos += 1
        yield match.group(1), text[match.start():pos]

def main():
    if (PACK / 'baseline.json').exists():
        raise RuntimeError('Revision baseline already exists; refusing to overwrite')
    for folder in ['references', 'edit_inputs', 'previews', 'target_size_png']:
        (PACK / folder).mkdir(parents=True, exist_ok=True)
    baseline = {p.relative_to(ROOT).as_posix(): digest(p.read_bytes())
                for folder in ['common', 'gfx'] for p in sorted((ROOT / folder).rglob('*')) if p.is_file()}
    write('baseline.json', baseline)
    refs = []
    for i, name in enumerate(USER_REFS, 1):
        src = Path('C:/Users/simeo/AppData/Local/Temp') / name
        dst = PACK / 'references' / ('user_pm_%s.png' % i if i < 4 else 'user_cobblestones.png')
        shutil.copyfile(src, dst)
        refs.append({'role': 'PM style' if i < 4 else 'technology pavement reference',
                     'original': str(src), 'copy': dst.relative_to(PACK).as_posix(),
                     'sha256': digest(src.read_bytes())})
    native = GAME / 'gfx/interface/icons/building_icons/building_railway.dds'
    Image.open(native).convert('RGBA').save(PACK / 'references/vanilla_building_railway.png')
    building = ROOT / 'common/buildings/11_private_infrastructure.txt'
    write('vanilla_building_binding.json', {
        'status': 'PLANNED_AUTHORIZED_NATIVE_REUSE', 'id': 'building_railway',
        'file': building.relative_to(ROOT).as_posix(), 'before_sha256': digest(building.read_bytes()),
        'before_text': building.read_text(encoding='utf-8-sig'),
        'old_icon': 'gfx/error_deer.dds', 'new_icon': 'gfx/interface/icons/building_icons/building_railway.dds',
        'native_source': str(native), 'native_sha256': digest(native.read_bytes()),
        'gameplay_changes_allowed': False, 'custom_building_preview_rejected_preserved': True})
    local = {}
    for p in sorted((ROOT / 'localization/french').rglob('*.yml')):
        for match in re.finditer(r'^\s*([A-Za-z0-9_]+):\d*\s+"([^"\n]*)"', p.read_text(encoding='utf-8-sig'), re.M):
            local[match.group(1)] = match.group(2)
    bindings = {}
    for p in sorted((ROOT / 'common/production_methods').glob('*.txt')):
        for key, block in blocks(p.read_text(encoding='utf-8-sig')):
            match = re.search(r'\btexture\s*=\s*"([^"]+)"', block)
            if match:
                bindings.setdefault(match.group(1), []).append({'id':key, 'file':p.relative_to(ROOT).as_posix()})
    entries = []
    for dds in sorted((ROOT / 'gfx/interface/icons/production_method_icons').glob('1776*.dds')):
        relative = dds.relative_to(ROOT).as_posix()
        hits = bindings.get(relative, [])
        if len(hits) != 1:
            raise RuntimeError('Expected one current PM binding for ' + relative + ': ' + repr(hits))
        key = dds.stem.removeprefix('1776_')
        inp = 'edit_inputs/' + key + '.png'
        Image.open(dds).convert('RGBA').save(PACK / inp)
        entries.append({'key': key, 'family':'PM', 'label_fr':local.get(hits[0]['id'], hits[0]['id']),
                        'bindings':hits, 'current_dds':relative, 'current_dds_sha256':digest(dds.read_bytes()),
                        'edit_input':inp, 'preview':'previews/' + key + '_flat.png', 'target_size':208,
                        'integration':'WAITING_USER_APPROVAL'})
    oldplan = json.loads((PREVIOUS / 'generation_plan.json').read_text(encoding='utf-8'))
    for e in oldplan['entries']:
        if e['family'] == 'BUILDING':
            continue
        inp = 'edit_inputs/' + e['key'] + '.png'
        shutil.copyfile(PREVIOUS / e['preview'], PACK / inp)
        entries.append({'key':e['key'], 'family':e['family'], 'label_fr':e['label_fr'],
                        'bindings':[{'id':e['id'], 'file':e['definition']}],
                        'current_texture':e['current_texture'], 'proposed_dds':e['target_dds'],
                        'edit_input':inp, 'preview':'previews/' + e['key'] + ('_cobblestones.png' if e['family']=='TECH' else '_flat.png'),
                        'target_size':e['target_size'], 'integration':'WAITING_USER_APPROVAL'})
    assert len(entries) == 18 and sum(e['family']=='PM' for e in entries) == 17
    write('revision_plan.json', {'status':'INPUTS_READY', 'date':'2026-10-03',
          'mode':'BUILTIN_IMAGE_GEN', 'intent':'EDIT_STYLE_TRANSFER', 'references':refs,
          'pm_style':'Strictly flat 2D schematic silhouettes; beige/ochre matte flat fills, no shadows, no depth, no perspective, no embossed highlights or dimensional materials.',
          'approval_required_before_generated_integration':True,
          'only_authorized_immediate_game_change':'Native railway building icon binding', 'entries':entries})
    print(json.dumps({'protected_files':len(baseline), 'pm_icons_to_revise':17,
                      'technology_icons_to_revise':1, 'native_building_file_found':True}))

if __name__ == '__main__':
    main()
