"""Prepare a lab-only production-method chance variant and inspect saved choices."""
from collections import Counter
from pathlib import Path
import argparse
import copy
import json
import re
import shutil

from simperf56_global_ai_prepare_20261124 import LAB
from simperf56_native_categories_20261123 import read, sha, write
from simperf56_save_state import child, num, records, sections


DEFINE = 'PRODUCTION_METHOD_CHANCE_TO_CHANGE'


def prepare():
    plan_path = LAB/'PREPARATION.json'
    original = plan_path.read_bytes()
    plan = json.loads(original)
    assert 'GPM1' not in plan['profiles']
    parent = plan['profiles']['GON1']
    (run,) = (LAB/'runs').glob('GON1_*')
    settings = run/'SETTINGS.json'
    assert sha(settings) == parent['settings_sha256']
    assert sha(parent['seed_path']) == parent['common_save_sha256']
    assert sha(parent['native_define_file']) == parent['native_define_sha256']
    stock = Path(plan['executable']).parent.parent/'game/common/defines/00_ai.txt'
    assert len(re.findall(rf'(?m)^\s*{DEFINE}\s*=\s*0\.1\b', stock.read_text(encoding='utf-8-sig'))) == 1
    profile = LAB/'profiles/GPM1'
    seed = profile/'save games'/Path(parent['seed_path']).name
    seed.parent.mkdir(parents=True)
    shutil.copyfile(parent['seed_path'], seed)
    shutil.copyfile(settings, profile/'pdx_settings.json')
    shutil.copytree(Path(parent['path'])/'user_bindings', profile/'user_bindings')

    overlay = LAB/'pm_chance_overlay'
    relative_time = Path('gui/timemanip.gui')
    live_gui = Path(parent['mods'][-1])/relative_time
    gui = live_gui.read_bytes()
    match, = re.findall(rb'(?m)^([\t ]*)(?=text_single = \{ raw_text = "SPENDING )', gui)
    position = rb'(?m)^'+re.escape(match)+rb'text_single = \{ raw_text = "SPENDING [^\r\n]+\r?\n'
    newline = b'\r\n' if b'\r\n' in gui else b'\n'
    probe = match+f'''text_single = {{ raw_text = "PM [GetDefine('NAI','{DEFINE}')]" }}'''.encode()+newline
    new_gui, edits = re.subn(position, lambda hit: hit[0]+probe, gui)
    assert edits == 1 and new_gui.replace(probe, b'', 1) == gui
    (overlay/relative_time).parent.mkdir(parents=True)
    (overlay/relative_time).write_bytes(new_gui)
    define_file = overlay/'common/defines/zzzz_sim56_pm_chance.txt'
    define_file.parent.mkdir(parents=True)
    define_file.write_text(f'NAI = {{\n    {DEFINE} = 0\n}}\n', encoding='utf-8')

    content = read(run/'CONTENT_LOAD.json')
    assert [entry['path'] for entry in content['enabledMods']] == parent['mods']
    content['enabledMods'].append({'path': overlay.as_posix()})
    write(profile/'content_load.json', content)
    spec = copy.deepcopy(parent)
    spec.update(path=str(profile), seed_path=str(seed), mods=[entry['path'] for entry in content['enabledMods']],
                native_define_file=str(define_file), native_define_sha256=sha(define_file),
                native_override={DEFINE: 0}, repetition_of=None, gameplay_preserving=False)
    plan['profiles']['GPM1'] = spec
    write(LAB/'PM_CHANCE_SETUP.json', dict(default=0.1, variant=0, source_stock=str(stock),
          expected_effect='Chance of considering a PM change; order of native profitability calculations unmeasured.',
          common_save_verified=sha(seed) == sha(parent['seed_path']),
          added_override_files={str(relative_time): sha(overlay/relative_time),
                                str(define_file.relative_to(overlay)): sha(define_file)}))
    assert plan_path.read_bytes() == original
    with (LAB/'PLAN_BEFORE_GPM1.json').open('xb') as stream:
        stream.write(original)
    plan_path.write_text(json.dumps(plan, indent=2), encoding='utf-8')
    print('Prepared GPM1; defines and a pause-only verification label are overlaid.')


def buildings(path):
    state = Path(path).read_text(encoding='utf-8-sig')
    out = {}
    for identity, obj in records(state, sections(state)['building_manager']):
        methods = child(obj, 'production_methods')
        if obj.one('building') and methods and num(obj, 'levels') > 0:
            scope = (obj.one('building'), obj.one('state'))
            choices = tuple(sorted(str(item.value) for item in methods.children()))
            out[identity] = (scope, choices)
    return out


def compare():
    plan = read(LAB/'PREPARATION.json')
    labels = ('GON1', 'GOF1', 'GPM1')
    source = buildings(plan['profiles']['GON1']['seed_path'])
    evidence = {}
    for trial in labels:
        result = read(LAB/(trial+'_RESULTS.json'))
        witness = result['post_autosave']
        assert sha(witness['preserved']) == witness['sha256']
        target = buildings(witness['preserved'])
        matched = [i for i in source.keys() & target.keys() if source[i][0] == target[i][0]]
        changed = [i for i in matched if source[i][1] != target[i][1]]
        evidence[trial] = dict(matched=len(matched), changed=len(changed),
                               initial=len(source), post=len(target),
                               changed_by_type=dict(Counter(source[i][0][0] for i in changed)),
                               post_date=witness['game_date'], sha256=witness['sha256'])
    write(LAB/'PM_CHOICES_APRIL.json', evidence)
    print(json.dumps(evidence))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('step', choices=['prepare', 'compare'])
    args = parser.parse_args()
    (prepare if args.step == 'prepare' else compare)()
