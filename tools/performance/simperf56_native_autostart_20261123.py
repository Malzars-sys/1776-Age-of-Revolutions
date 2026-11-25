"""Prepare a lab-only native UI pilot if Windows interaction is unavailable."""
from pathlib import Path
import argparse
import copy
import hashlib
import json
import re
import shutil

from simperf56_native_categories_20261123 import LAB, read, sha, write


def sha_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def overlay(plan, compatibility):
    suffix = '_1_15_2' if compatibility else ''
    target = LAB/('native_ui_autostart'+suffix)
    receipt_path = LAB/('NATIVE_UI_AUTOSTART'+suffix+'.json')
    if target.exists():
        receipt = read(receipt_path)
        assert all(sha(target/path) == digest for path, digest in receipt['overlay_sha256'].items())
        return target
    steam_gui = Path(plan['executable']).parent.parent/'game/gui'
    frozen_gui = Path(plan['main_frozen'])/'gui'
    front = 'gui/frontend/frontend_main.gui'
    time = 'gui/timemanip.gui'
    sources = {front: frozen_gui/'frontend/frontend_main.gui', time: steam_gui/'timemanip.gui'}
    blocks = {
        front: '''state = {
    name = sim56_autocontinue
    trigger_when = "[And(And(FrontEndLoadView.CanDoContinue, SaveGameItem.CanLoad), Not(GetVariableSystem.Exists('sim56_autocontinue_fired')))]"
    on_start = "[GetVariableSystem.Set('sim56_autocontinue_fired', 'true')]"
    duration = 8
    on_finish = "[FrontEndLoadView.OnContinue]"
}''',
        time: '''state = {
    name = sim56_start_timed_run
    trigger_when = "[And(And(IsInGame, TimeKeeper.IsPaused), And(GetPlayer.IsValid, Not(GetVariableSystem.Exists('sim56_timed_run_fired'))))]"
    on_start = "[GetVariableSystem.Set('sim56_timed_run_fired', 'true')]"
    duration = 45
    on_finish = "[TimeKeeper.SetGameSpeed('(int32)4')]"
    on_finish = "[TimeKeeper.TogglePause]"
}''',
    }
    if compatibility:
        blocks[time] += '''
widget = {
    parentanchor = right
    position = { -560 72 }
    size = { 310 76 }
    filter_mouse = none
    visible = "[TimeKeeper.IsPaused]"
    vbox = {
        text_single = { raw_text = "PUBLIC [GetDefine('NAI','PRODUCTION_BUILDING_CONSTRUCTION_ENABLED')]" }
        text_single = { raw_text = "PRIVATE [GetDefine('NAI','AUTONOMOUS_INVESTMENT_CONSTRUCTION_ENABLED')]" }
        text_single = { raw_text = "SPENDING [GetDefine('NAI','GOVERNMENT_MONEY_SPENDING_ENABLED')]" }
    }
}'''
    anchors = {front: 'name = "continue_button"', time: 'name = "timemanip"'}
    digests = {}
    for path, source in sources.items():
        raw = source.read_bytes()
        original = raw.decode('utf-8-sig')
        match, = re.finditer(r'(?m)^([\t ]*)'+re.escape(anchors[path])+r'[ \t]*\r?$', original)
        newline = '\r\n' if '\r\n' in original else '\n'
        insertion = ''.join(newline+match[1]+part for part in blocks[path].splitlines())
        payload = (original[:match.end()].rstrip('\r')+insertion+original[match.end()-(1 if match[0].endswith('\r') else 0):]).encode('utf-8')
        if raw.startswith(b'\xef\xbb\xbf'): payload = b'\xef\xbb\xbf'+payload
        assert (original[:match.end()].rstrip('\r')+original[match.end()-(1 if match[0].endswith('\r') else 0):]) == original
        output = target/path
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open('xb') as f: f.write(payload)
        digests[path] = sha_bytes(payload)
    if compatibility:
        # The 1.15.1 mod copies call naval UI functions absent from 1.15.2.
        # Restore just the matching installed GUI for each isolated test profile.
        for name in ('map_list_panel.gui', 'right_click_menu.gui'):
            path = 'gui/'+name
            source = steam_gui/name
            sources[path] = source
            shutil.copyfile(source, target/path)
            digests[path] = sha(target/path)
    write(receipt_path, dict(overlay_sha256=digests,
          sources={str(p): sha(p) for p in sources.values()},
          scope='Only copies of lab GUI profiles, no OS input. UI uses native continue and speed/pause callbacks. Behavior requires pilot verification.'))
    return target


def prepare(label, parent, compatibility):
    assert re.fullmatch(r'[A-Z0-9_]{2,40}', label)
    plan_path = LAB/'PREPARATION.json'
    before = plan_path.read_bytes()
    plan = json.loads(before)
    assert label not in plan['profiles']
    source = plan['profiles'][parent]
    profile = LAB/'profiles'/label
    assert not profile.exists()
    auto = overlay(plan, compatibility)
    seed = Path(source['seed_path'])
    assert sha(seed) == source['common_save_sha256']
    target = profile/'save games'/seed.name
    target.parent.mkdir(parents=True)
    shutil.copyfile(seed, target)
    settings = next((LAB/'runs').glob('NPC2_*/SETTINGS.json'))
    assert sha(settings) == source['settings_sha256']
    shutil.copyfile(settings, profile/'pdx_settings.json')
    shutil.copytree(Path(source['path'])/'user_bindings', profile/'user_bindings')
    content = read(Path(source['path'])/'content_load.json')
    assert [m['path'] for m in content['enabledMods']] == source['mods']
    content['enabledMods'].append({'path': auto.as_posix()})
    write(profile/'content_load.json', content)
    spec = copy.deepcopy(source)
    spec.update(path=str(profile), seed_path=str(target), mods=[m['path'] for m in content['enabledMods']],
                native_ui_autostart=True, matching_steam_gui=compatibility,
                comparison_group=('native_autostart_compatible' if compatibility else 'native_autostart_pilot')+'_1.15.2_20261123')
    plan['profiles'][label] = spec
    with (LAB/('PLAN_BEFORE_'+label+'.json')).open('xb') as f: f.write(before)
    assert plan_path.read_bytes() == before
    plan_path.write_text(json.dumps(plan, indent=2), encoding='utf-8')
    print(json.dumps(dict(trial=label, source=parent, autostart_runtime_verified=False)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('label')
    parser.add_argument('parent')
    parser.add_argument('--compat', action='store_true')
    args = parser.parse_args()
    prepare(args.label, args.parent, args.compat)
