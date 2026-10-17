"""Package/verify an opt-in companion. Never edit main runtime, Git or playsets.

--deploy copies reviewed source assets to one NEW sibling mod and descriptor;
an existing destination must already match exactly. No archive or game launch.
"""
from pathlib import Path
import itertools
import json
import shutil
import sys
import validate_diplomacy_ottoman_1776 as cw
import validate_infrastructure_landscape as prior

ROOT = prior.ROOT
PACKAGE = ROOT / 'docs/prototypes/REGIONAL_INFRASTRUCTURE'
SOURCE = PACKAGE / 'mod'
DEST = ROOT.parent / 'aor1776_landscape_prototype'
DESCRIPTOR = 'aor1776_landscape_prototype.mod'
PROBE = 'building_aor1776_visual_rail_probe'
BASE = PACKAGE / 'BASELINE.json'


def dump(name, value):
    (PACKAGE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')


def main_hashes():
    return dict(prior.runtime_hashes(), **{p: prior.sha(ROOT / p) for p in prior.ALLOWED})


def capture():
    assert not BASE.exists(), 'Do not replace an existing baseline'
    dump('BASELINE.json', {'main_runtime': main_hashes(), 'git': prior.git_state()})
    print('Captured main runtime hashes and Git state, without copying runtime assets')


def nodes(folder):
    return [n for p in sorted((SOURCE / folder).glob('*.txt'))
            for n in cw.parse(p.read_text(encoding='utf-8-sig'))]


def fields(node):
    return {n.key: n.value for n in node.children()}


def manual_visual_receipt():
    path = PACKAGE / 'RUNTIME_USER_VISUAL_VALIDATION_2026_10_16.json'
    if not path.exists():
        return None
    receipt = json.loads(path.read_text(encoding='utf-8'))
    assert receipt['status'] == 'PASS_RUNTIME_USER_VALIDATED'
    assert receipt['manual_user_validation'] and not receipt['automated_engine_test']
    assert receipt['ground_rail_toggle_validated']
    assert not receipt['full_prototype_runtime_validated']
    assert not receipt['real_rail_pm_transition_validated']
    for evidence in receipt['evidence']:
        image = (PACKAGE / evidence['path']).resolve()
        assert image.is_relative_to((PACKAGE / 'evidence').resolve())
        assert prior.sha(image) == evidence['sha256'], 'Visual evidence hash mismatch'
    return receipt


def run_tests():
    checks = []
    def check(label, value):
        checks.append({'name': label, 'passed': bool(value)})
    baseline = json.loads(BASE.read_text(encoding='utf-8'))
    check('All main runtime files unchanged', main_hashes() == baseline['main_runtime'])
    check('HEAD and index unchanged', prior.git_state() == baseline['git'])
    for p in SOURCE.rglob('*'):
        if p.is_file() and p.suffix in {'.txt', '.mod'}:
            cw.parse(p.read_text(encoding='utf-8-sig'))
            check('Parse ' + p.relative_to(SOURCE).as_posix(), True)
    check('No companion maps/history/shaders/GUI overrides', all(
        not (SOURCE / p).exists() for p in ['map_data', 'gfx', 'gui', 'common/history']))
    defines = nodes('common/defines')
    check('Only one experimental engine define', len(defines) == 1 and defines[0].key == 'NCountry'
          and fields(defines[0]) == {'RAILWAY_BUILDING': '"' + PROBE + '"'})
    building = nodes('common/buildings')
    check('Only new probe building', len(building) == 1 and building[0].key == PROBE)
    bf = fields(building[0])
    check('Probe cannot be built expanded or downsized', all(bf.get(k) == 'no' for k in ['buildable', 'expandable', 'downsizeable']))
    check('No probe city meshes or terrain alteration', not {'city_type', 'terrain_manipulator', 'aliases'} & bf.keys())
    group = nodes('common/building_groups')[0]
    gf = fields(group)
    check('Independent group, no economic inheritance', 'parent_group' not in gf)
    check('No cash urbanization or infrastructure use', all(gf.get(k) == '0' for k in ['cash_reserves_max', 'urbanization', 'infrastructure_usage_per_level']))
    pm = nodes('common/production_methods')
    check('One empty diagnostic PM', len(pm) == 1 and set(fields(pm[0])) == {'texture', 'is_default'})
    pmg = nodes('common/production_method_groups')[0]
    check('Probe PM group reference', cw.scalar(pmg.children('production_methods')[0].children()[0].value) == pm[0].key)
    rail_pmg = cw.parse((ROOT / 'common/production_method_groups/24_tech7a_wave_c_rail_pmgs.txt').read_text())
    pms = {cw.scalar(n.value) for n in rail_pmg[0].children('production_methods')[0].children()} - {'pm_no_rail_network'}
    triggers = {n.key: n for n in nodes('common/scripted_triggers')}
    real = triggers['aor1776_ilp_has_real_rail_pm']
    check('All seven actual rail PMs', {cw.scalar(n.value) for n in cw.walk(real.children()) if n.key == 'has_active_production_method'} == pms and len(pms) == 7)
    # Interpret the actual AST, including the diagnostic overrides, not a
    # duplicate hand-written implementation of its truth table.
    def condition(items, state, building=None):
        def single(n):
            if n.key == 'OR': return any(single(v) for v in n.children())
            if n.key == 'NOT': return not condition(n.children(), state, building)
            if n.key == 'any_scope_building': return any(condition(n.children(), state, b) for b in state['buildings'])
            if n.key == 'is_building_type': return building['type'] == cw.scalar(n.value)
            if n.key == 'level' and n.op == '>=': return building['level'] >= int(n.value)
            if n.key == 'has_active_production_method': return cw.scalar(n.value) in building['pms']
            if n.key == 'has_variable': return cw.scalar(n.value) in state['vars']
            if n.key == 'has_building': return any(b['type'] == cw.scalar(n.value) for b in state['buildings'])
            if n.key in triggers: return condition(triggers[n.key].children(), state)
            raise AssertionError('Unexpected predicate ' + n.key)
        return all(single(n) for n in items)
    effects = {n.key: n for n in nodes('common/scripted_effects')}
    def apply(items, state):
        i = 0
        while i < len(items):
            n = items[i]
            if n.key == 'if':
                take = condition(n.children('limit')[0].children(), state)
                if take: apply([v for v in n.children() if v.key != 'limit'], state)
                if i + 1 < len(items) and items[i+1].key == 'else':
                    i += 1
                    if not take: apply(items[i].children(), state)
            elif n.key == 'create_building':
                f = fields(n)
                assert f['building'] == PROBE and f['level'] == '1'
                state['buildings'].append({'type': PROBE, 'level': 1, 'pms': {pm[0].key}})
            elif n.key == 'remove_building':
                assert n.value == PROBE
                state['buildings'] = [b for b in state['buildings'] if b['type'] != PROBE]
            elif n.key == 'set_variable': state['vars'].add(n.value)
            elif n.key == 'remove_variable': state['vars'].discard(n.value)
            elif n.key in effects: apply(effects[n.key].children(), state)
            elif n.key == 'capital': apply(n.children(), state)
            else: raise AssertionError('Unexpected effect ' + n.key)
            i += 1
    cases = sorted(pms) + ['pm_no_rail_network', 'pm_turnpike_road_network', 'pm_industrial_canals', None]
    sync = effects['aor1776_ilp_sync_state'].children()
    count = lambda s: sum(b['type'] == PROBE for b in s['buildings'])
    for pm_id, on, off in itertools.product(cases, [False, True], [False, True]):
        buildings = [] if pm_id is None else [{'type': 'building_railway', 'level': 3, 'pms': {pm_id}}]
        state = {'buildings': buildings, 'vars': set()}
        if on: state['vars'].add('aor1776_ilp_force_on')
        if off: state['vars'].add('aor1776_ilp_force_off')
        expected = not off and (on or pm_id in pms)
        saved = json.dumps(buildings, default=sorted, sort_keys=True)
        apply(sync, state); apply(sync, state)
        label = f'{pm_id}:on={on}:off={off}'
        check(label + ' probe and idempotence', count(state) == int(expected))
        economic = [b for b in state['buildings'] if b['type'] != PROBE]
        check(label + ' economic data untouched', json.dumps(economic, default=sorted, sort_keys=True) == saved)
    for level, kind in [(0, 'building_railway'), (1, 'building_port')]:
        state = {'buildings': [{'type': kind, 'level': level, 'pms': {'pm_early_trains'}}], 'vars': set()}
        apply(sync, state)
        check('Reject wrong building/zero level ' + str((level, kind)), count(state) == 0)
    decisions = nodes('common/decisions')
    state = {'buildings': [], 'vars': set()}
    for decision, expected in zip(decisions, [1, 0, 0]):
        f = fields(decision)
        check(decision.key + ' player only, AI zero', fields(decision.children('is_shown')[0]) == {'is_player': 'yes'} and fields(decision.children('ai_chance')[0]) == {'value': '0'})
        apply(decision.children('when_taken')[0].children(), state)
        check(decision.key + ' actual decision effects', count(state) == expected)
    state = {'buildings': [{'type': 'building_railway', 'level': 4, 'pms': {'pm_early_trains'}}], 'vars': set()}
    apply(sync, state); state['buildings'][0]['pms'] = {'pm_no_rail_network'}; apply(sync, state)
    check('PM removal removes proxy', count(state) == 0)
    actions = {n.key: n for n in nodes('common/on_actions')}
    native_actions = {n.key for n in cw.parse((ROOT / 'common/on_actions/00_code_on_actions.txt').read_text(encoding='utf-8-sig'))}
    for key, n in actions.items():
        if key.startswith('on_'):
            check(key + ' existing native hook', key in native_actions)
            check(key + ' additive only', set(fields(n)) == {'on_actions'})
            check(key + ' child exists', all(cw.scalar(c.value) in actions for c in n.children('on_actions')[0].children()))
    hook = actions['aor1776_ilp_building_changed']
    check('Proxy creation cannot recurse into sync', any(n.key == 'is_building_type' and n.value == 'building_railway' for n in cw.walk(hook.children())))
    for language in ['french', 'english']:
        path = SOURCE / f'localization/{language}/aor1776_landscape_prototype_l_{language}.yml'
        text = path.read_text(encoding='utf-8-sig')
        check(language + ' UTF8 BOM', path.read_bytes().startswith(b'\xef\xbb\xbf'))
        check(language + ' all decision keys', all(f' {d.key}:' in text and f' {d.key}_desc:' in text for d in decisions))
    receipt = json.loads((ROOT / 'docs/reports/map/MAP2N/RUNTIME_USER_VALIDATION_2026_10_15.json').read_text())
    check('MAP2N receipt is manual and separate', receipt['status'] == 'PASS_RUNTIME_USER_VALIDATED' and not receipt['automated_engine_test'] and not receipt['prototype_included'])
    for relative in ['VALIDATION.json', 'COMPLETION/VALIDATION.json']:
        r = json.loads((ROOT / 'docs/reports/map/MAP2N' / relative).read_text())
        check(relative + ' manual flag separate from static', r['runtime_user_validated'] and not r['engine_tested'] and r['status'] == 'MAP2N_READY_FOR_RUNTIME_VALIDATION')
    installed = json.loads((ROOT / 'docs/reports/map/MAP2N/COMPLETION/INSTALLED_MANIFEST.json').read_text())
    check('MAP2N functional hashes preserved', all(prior.sha(ROOT / p) == h for p, h in installed['functional_files'].items()))
    visual = manual_visual_receipt()
    result = {'status': 'PROTOTYPE_READY_FOR_RUNTIME_TEST' if all(c['passed'] for c in checks) else 'FAIL',
              'passed': sum(c['passed'] for c in checks), 'total': len(checks),
              'automated_engine_test': False, 'visual_hypothesis_validated': bool(visual),
              'visual_validation_source': 'MANUAL_USER_SCREENSHOTS' if visual else None,
              'visual_validation_scope': visual['scope'] if visual else None,
              'runtime_visual_receipt': 'RUNTIME_USER_VISUAL_VALIDATION_2026_10_16.json' if visual else None,
              'full_prototype_runtime_validated': False,
              'main_runtime_changed': False, 'checks': checks}
    dump('VALIDATION.json', result)
    print(json.dumps({k:v for k,v in result.items() if k != 'checks'}, indent=2))
    for c in checks:
        if not c['passed']: print('FAIL', c['name'])
    assert all(c['passed'] for c in checks)


def payload():
    return {**{p.relative_to(SOURCE).as_posix(): p for p in SOURCE.rglob('*') if p.is_file()}, 'README.md': PACKAGE / 'README.md'}


def verify():
    expected = payload()
    assert DEST.is_dir(), 'Not installed'
    assert {p.relative_to(DEST).as_posix() for p in DEST.rglob('*') if p.is_file()} == set(expected), 'Unexpected destination files; do not overwrite'
    for relative, source in expected.items():
        assert prior.sha(DEST / relative) == prior.sha(source), relative
    assert prior.sha(ROOT.parent / DESCRIPTOR) == prior.sha(PACKAGE / DESCRIPTOR)
    visual = manual_visual_receipt()
    dump('INSTALLED_VALIDATION.json', {'status':'PASS_INSTALLED_FILE_HASHES', 'destination':str(DEST),
        'files':{rel:prior.sha(p) for rel,p in expected.items()}, 'launcher_database_changed':False,
        'playset_changed':False, 'runtime_tested':bool(visual), 'automated_engine_test':False,
        'runtime_visual_user_validated':bool(visual), 'full_prototype_runtime_validated':False,
        'runtime_validation_scope':visual['scope'] if visual else None})
    print('Installed payload and launcher descriptor verified; no launcher/playset changes')


def deploy():
    run_tests()
    assert DEST.resolve().parent == ROOT.parent.resolve() and DEST.name == 'aor1776_landscape_prototype'
    descriptor = ROOT.parent / DESCRIPTOR
    if DEST.exists() or descriptor.exists():
        verify()  # only idempotent repeat; never overwrite a differing folder
        return
    DEST.mkdir()
    for relative, source in payload().items():
        target = DEST / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    shutil.copy2(PACKAGE / DESCRIPTOR, descriptor)
    verify()


if __name__ == '__main__':
    options = {'--capture':capture, '--validate':run_tests, '--deploy':deploy, '--verify-installed':verify}
    assert len(sys.argv) == 2 and sys.argv[1] in options
    options[sys.argv[1]]()
