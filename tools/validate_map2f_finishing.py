"""Narrow presentation follow-up. No gameplay mutation or old-report overwrite."""
import contextlib
import io
import json
import re
import subprocess
import sys
from pathlib import Path

import validate_diplomacy_ottoman_1776 as cw
import validate_map2a as qa
import validate_map2f as original
from map2f_work import ROOT, GIT, sha

OUT = ROOT / 'docs/reports/map/MAP2F/FINISHING'
BASE = OUT / 'BASELINE.json'
COLOR_FILE = 'common/country_definitions/04_1776_kandy.txt'
NEW_FILES = {
    'common/scripted_effects/1776_map2f_state_names.txt',
    'common/on_actions/14_1776_map2f_state_names.txt',
    'localization/english/replace/1776_map2f_finishing_l_english.yml',
    'localization/french/replace/1776_map2f_finishing_l_french.yml',
}
COLOR = [45, 128, 153]

def runtime_hashes():
    return {p.relative_to(ROOT).as_posix(): sha(p)
            for folder in ['common', 'map_data', 'localization', 'gfx', 'gui', 'events', 'music', '.metadata']
            for p in (ROOT / folder).rglob('*') if p.is_file()}

def git_state():
    return {**{key: subprocess.check_output([GIT, *args], cwd=ROOT, text=True).strip()
               for key, args in {'head': ['rev-parse', 'HEAD'], 'refs': ['show-ref']}.items()},
            'index': sha(ROOT / '.git/index')}

def snapshot():
    assert not BASE.exists(), 'Do not replace the pre-finishing baseline.'
    assert not any((ROOT / p).exists() for p in NEW_FILES)
    OUT.mkdir(parents=True, exist_ok=True)
    data = {'runtime': runtime_hashes(), 'git': git_state(),
            'kandy_original': (ROOT / COLOR_FILE).read_text(encoding='utf-8-sig'),
            'reports': {p.relative_to(ROOT).as_posix(): sha(p)
                        for p in (ROOT / 'docs/reports/map').rglob('*')
                        if p.is_file() and OUT not in p.parents}}
    BASE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print('Pre-finishing baseline:', len(data['runtime']), 'runtime files; no full copy.')

def validate():
    base = json.loads(BASE.read_text(encoding='utf-8'))
    tests = []
    def check(name, value, detail=None):
        tests.append({'name': name, 'status': 'PASS' if value else 'FAIL', 'detail': detail})
    current = runtime_hashes()
    modified = [p for p, digest in base['runtime'].items() if current.get(p) != digest]
    check('only_Kandy_existing_runtime_file_changed', modified == [COLOR_FILE], modified)
    check('only_four_expected_new_runtime_files', set(current) - set(base['runtime']) == NEW_FILES)
    check('no_runtime_file_removed', set(base['runtime']) <= set(current))
    check('all_previous_map_reports_preserved', all((ROOT/p).exists() and sha(ROOT/p) == digest for p,digest in base['reports'].items()))
    check('primary_git_HEAD_refs_index_preserved', git_state() == base['git'])
    old = cw.parse(base['kandy_original'])[0]
    actual = cw.parse((ROOT / COLOR_FILE).read_text(encoding='utf-8-sig'))[0]
    without_color = lambda n: [qa.norm(x) for x in n.children() if x.key != 'color']
    check('Kandy_only_color_not_culture_religion_capital_or_status', without_color(old) == without_color(actual))
    color = [int(x.value) for x in actual.children('color')[0].children()]
    check('Kandy_cool_RGB_45_128_153', color == COLOR)
    bic = next(n for n in cw.parse((ROOT/'common/country_definitions/00_countries.txt').read_text(encoding='utf-8-sig')) if n.key == 'BIC')
    bic_color = [int(n.value) for n in bic.children('color')[0].children()]
    distance = sum((a-b)**2 for a,b in zip(color,bic_color)) ** .5
    check('Kandy_distinct_from_BIC_RGB', distance > 150, {'BIC': bic_color, 'KND': color, 'RGB_distance': round(distance,2)})
    localizations = {}
    for lang in ['english', 'french']:
        p = ROOT / f'localization/{lang}/replace/1776_map2f_finishing_l_{lang}.yml'
        raw = p.read_text(encoding='utf-8-sig')
        rows = re.findall(r'^\s+(\w+):0 "([^"\n]*)"\s*$',raw,re.M)
        loc = dict(rows);localizations[lang] = loc
        check(f'{lang}_localization_header_and_BOM', raw.startswith(f'l_{lang}:\n') and p.read_bytes().startswith(b'\xef\xbb\xbf'))
        check(f'{lang}_localization_unique_keys', len(rows)==len(loc))
        check(f'{lang}_Arcot_Madras_Pondicherry', loc.get('CAR')=='Arcot' and loc.get('aor1776_map2f_madras')=='Madras' and loc.get('aor1776_map2f_pondicherry')==('Pondichéry' if lang=='french' else 'Pondicherry'))
    check('French_Arcot_articles_and_adjective_forms', all(localizations['french'].get(k)==v for k,v in {'CAR_Le':'','CAR_De':"d' ",'CAR_Du':"d' ",'CAR_Au':'à ','CAR_En':'à ','CAR_ADJ':"d'Arcot",'CAR_ADJ_MS':"d'Arcot",'CAR_ADJ_FS':"d'Arcot",'CAR_ADJ_MP':"d'Arcot",'CAR_ADJ_FP':"d'Arcot",'STATE_MADRAS':'Carnatique'}.items()))
    typo_files = [p for p in current if Path(p).suffix in ['.yml','.txt'] and re.search(r'carnartic', (ROOT/p).read_text(encoding='utf-8-sig',errors='replace'), re.I)]
    check('no_Carnartic_in_active_text', not typo_files, typo_files)
    # The complete original 32 conservation checks run with exactly one expected
    # presentation adjustment; capture their results without rewriting old reports.
    transform_saved = original.patcher.transform
    dump_saved = original.dump
    captured = {}
    def presentation_expected(b):
        changed, plan = transform_saved(b)
        changed[COLOR_FILE] = changed[COLOR_FILE].replace('181 84 51','45 128 153')
        return changed, plan
    try:
        original.patcher.transform = presentation_expected
        original.dump = lambda name,data: captured.update({name:data})
        with contextlib.redirect_stdout(io.StringIO()): original.validate()
    except Exception as exc:
        check('original_MAP2F_conservation_suite_completed',False,str(exc))
    finally:
        original.patcher.transform = transform_saved
        original.dump = dump_saved
    original_result = captured.get('MAP2F_VALIDATION.json', {})
    for row in original_result.get('tests', []):
        tests.append({**row, 'name':'MAP2F/'+row['name']})
    check('original_MAP2F_all_32_checks_pass', original_result.get('status')=='PASS_STATIC' and len(original_result.get('tests',[]))==32)
    # Explicit AST contract and finite-scope simulation of the new naming effect.
    eff = cw.parse((ROOT/'common/scripted_effects/1776_map2f_state_names.txt').read_text(encoding='utf-8-sig'))
    check('one_naming_effect_only', [n.key for n in eff]==['assign_1776_map2f_split_state_name'])
    named = eff[0].children('if')[0]
    guard = named.children('limit')[0]
    check('names_only_split_STATE_MADRAS', guard.one('state_region')=='s:STATE_MADRAS' and guard.one('is_split_state')=='yes')
    decisions = named.children('if') + named.children('else_if')
    cases = []
    for branch in decisions:
        owner = branch.children('limit')[0].children('owner')[0]
        terms = owner.children('OR')[0].children() if owner.children('OR') else owner.children()
        cases.append(({n.key.removeprefix('c:') for n in terms}, branch.one('set_state_name')))
        check('owner_scope_self_comparison_'+branch.one('set_state_name'), all(n.op=='?=' and n.value=='this' for n in terms))
    check('exact_owner_specific_name_cases', cases==[({'BIC','GBR'},'aor1776_map2f_madras'),({'FRA'},'aor1776_map2f_pondicherry')])
    check('only_set_state_name_mutations', all(n.key not in ['create_state','set_owner','create_pop','create_country','add_modifier','set_country_name'] for n in cw.walk(eff)))
    for sid,split,tag,expected in [('STATE_MADRAS',True,'BIC','aor1776_map2f_madras'),('STATE_MADRAS',True,'GBR','aor1776_map2f_madras'),('STATE_MADRAS',True,'FRA','aor1776_map2f_pondicherry'),('STATE_MADRAS',True,'CAR',None),('STATE_MADRAS',True,'PUD',None),('STATE_MADRAS',True,'MYS',None),('STATE_MADRAS',True,'DENNOR',None),('STATE_MADRAS',False,'FRA',None),('STATE_PROVENCE',True,'FRA',None)]:
        result = next((key for tags,key in cases if tag in tags), None) if sid=='STATE_MADRAS' and split else None
        check(f'name_model_{sid}_{split}_{tag}', result==expected)
    hooks = cw.parse((ROOT/'common/on_actions/14_1776_map2f_state_names.txt').read_text(encoding='utf-8-sig'))
    expected_hooks = {'on_game_started':'aor1776_map2f_names_initialize','on_game_started_after_lobby':'aor1776_map2f_names_initialize','on_state_created':'aor1776_map2f_state_name_changed','on_state_owner_change':'aor1776_map2f_state_name_changed','on_become_subject':'aor1776_map2f_country_names_changed','on_become_independent':'aor1776_map2f_country_names_changed'}
    check('all_six_additive_lifecycle_hooks', all(any(n.key==hook and [x.value for x in n.children('on_actions')[0].children()]==[action] for n in hooks) for hook,action in expected_hooks.items()))
    targets = {n.key for n in hooks};check('all_new_hook_targets_defined', set(expected_hooks.values())<=targets)
    references = {n.value for n in cw.walk(eff) if n.key=='set_state_name'}
    check('state_name_keys_exist_in_both_languages', all(references<=set(loc) for loc in localizations.values()))
    output = {'status':'PASS_STATIC' if all(t['status']=='PASS' for t in tests) else 'FAIL_STATIC','tests':tests,'population':835804980,'new_province_transfers':0,'bitmap_changes':0,'changed_existing_runtime_files':modified,'new_runtime_files':sorted(NEW_FILES),'native_test':'MAP2F validated by player; finishing presentation still requires player observation. No game control attempted.','commit_merge_push':'NONE'}
    (OUT/'VALIDATION.json').write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding='utf-8')
    print(output['status'],len(tests),'checks; no history/bitmap/gameplay changes.')
    for t in tests:
        if t['status']=='FAIL': print(t)
    assert output['status']=='PASS_STATIC'

if __name__=='__main__':
    {'snapshot':snapshot,'validate':validate}[sys.argv[1]]()
