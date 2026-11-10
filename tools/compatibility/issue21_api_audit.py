"""Read-only checks for mission 21's 1.15 API migration; no engine launch."""
from pathlib import Path
import argparse, collections, hashlib, json, re, sys
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from validate_diplomacy_ottoman_1776 import parse, walk
LOT = ROOT / 'docs/reports/compatibility/V1_15_ISSUE21_REVIEW_2026_11_08'
GAME = Path('C:/Games/Victoria 3/game')
SHA = lambda b: hashlib.sha256(b).hexdigest()


def text(path):
    return path.read_bytes().decode('utf-8-sig').replace('\r\n', '\n')


def shape(nodes):
    return [(n.key, n.op, shape(n.children()) if isinstance(n.value, list) else n.value) for n in nodes]


def audit(candidate=False, replacements=None):
    replacements = replacements or {}
    checks = []
    def check(label, ok):
        checks.append({'check': label, 'passed': bool(ok)})
    migrations = json.loads(text(LOT / 'MIGRATIONS.json'))
    base = json.loads(text(LOT / 'BASELINE.json'))
    changed = collections.defaultdict(list)
    for row in migrations:
        changed[row['file']].append(row)
    supplied = {p.relative_to(LOT/'candidate').as_posix(): p for p in (LOT/'candidate').rglob('*') if p.is_file()}
    def read(rel):
        return replacements.get(rel, text(supplied[rel] if candidate else ROOT/rel))
    for rel, rows in changed.items():
        raw = (LOT/'before'/rel).read_bytes(); before = text(LOT/'before'/rel)
        check(rel+'.entry_snapshot', SHA(raw) == base['runtime_hashes'][rel])
        expected = before
        for row in sorted(rows, key=lambda r: -r['start']):
            check(rel+':'+str(row['line'])+'.exact_old_span', expected[row['start']:row['end']] == row['old'])
            expected = expected[:row['start']]+row['new']+expected[row['end']:]
        check(rel+'.only_authorized_spans', read(rel) == expected)
        current = (supplied[rel] if candidate else ROOT/rel).read_bytes()
        check(rel+'.BOM_preserved', raw.startswith(b'\xef\xbb\xbf') == current.startswith(b'\xef\xbb\xbf'))
        check(rel+'.EOL_preserved', (b'\r\n' in raw) == (b'\r\n' in current))
    parsed = {}
    for rel in supplied:
        if not rel.endswith('.txt'): continue
        try:
            parsed[rel] = parse(read(rel)); check(rel+'.parse', True)
        except ValueError:
            check(rel+'.parse', False)
    # Every copied helper, with full parameters and effects, equals its native provider.
    for row in json.loads(text(LOT/'RESTORED_HELPERS.json')):
        check(row['source']+'.canonical_provider_hash', SHA((GAME/row['source']).read_bytes()) == row['sha256'])
        if row['key'].startswith('on_monthly'): continue
        native = next(n for n in parse(text(GAME/row['source'])) if n.key == row['key'])
        found = [n for n in parsed[row['destination']] if n.key == row['key']]
        check(row['key']+'.native_payload', len(found) == 1 and shape(found) == shape([native]))
    # Ship identities can differ by narrative context even for the same old unit.
    for rel in ['events/tech_events/naval_tech_events.txt','events/dreadnought_hoax.txt','events/agitators_events/revolution_events_02.txt']:
        native_roots={n.key:n for n in parse(text(GAME/rel))}
        def targets(nodes):
            return {n.one('target') for n in walk(nodes) if n.key in ['formation_ship_type_fraction','country_ship_type_fraction']}
        for obj in parsed[rel]:
            local_targets=targets([obj])
            if not local_targets: continue
            ref=native_roots.get(obj.key)
            native_targets=targets([ref]) if ref else set()
            # Some new native tech events use any_scope_ship / is_ship_type instead.
            if ref:
                native_targets.update(n.value for n in walk([ref]) if n.key=='is_ship_type')
            check(obj.key+'.context_specific_native_ship_identity', bool(native_targets) and local_targets <= native_targets)
    expiry = read('common/on_actions/zz_1776_v115_character_expiry.txt')
    native_monthly = next(n for n in parse(text(GAME/'common/on_actions/00_code_on_actions.txt')) if n.key == 'on_monthly_pulse_character')
    native_expiry = [n for n in native_monthly.children('effect')[0].children()
                     if any('temporary_immortality_var' in str(c.value) for c in walk([n]))]
    actual_expiry = next(n for n in parse(expiry) if n.key == 'aor1776_v115_event_immortality_expiry').children('effect')[0].children()
    check('temporary_immortality.native_monthly_expiry', shape(actual_expiry) == shape(native_expiry) and len(native_expiry) == 2)
    # Global exact-key inventory excludes comments, unlike substring-only searches.
    removed = {'can_reach_target_country','can_reach_target_state','ai_desires_target_state',
        'ai_strongly_desires_target_state','country_war_exhaustion_casualties_mult',
        'current_date','is_ruler','is_heir','country_navy_unit_type_fraction','formation_navy_unit_type_fraction',
        'has_port','every_country_in_iberia','handle_ai_great_game_objectives','generate_new_eic_government_leader',
        'upgrade_moderniser_movement_effect','add_war_exhaustion','has_war_exhaustion','additional_war_exhaustion',
        'ship_interest_gain_mult','strait_trade_importance_by'}
    pattern = re.compile(r'\b('+'|'.join(map(re.escape, removed))+r')\b\s*(?:[=<>?]|\()')
    findings = []; ratio_count = 0
    role_types = {'admiral','general','politician','agitator'}
    # Effective native ship identities, accounting for local same-path masks.
    ships = set()
    providers = {p.name:p for p in (GAME/'common/ship_types').glob('*.txt')}
    providers.update({p.name:p for p in (ROOT/'common/ship_types').glob('*.txt')})
    for p in providers.values(): ships.update(n.key.removeprefix('REPLACE_OR_CREATE:') for n in parse(text(p)))
    for area in ['common','events']:
        paths = {p.relative_to(ROOT).as_posix():p for p in (ROOT/area).rglob('*.txt')}
        paths.update({rel:p for rel,p in supplied.items() if rel.startswith(area+'/')})
        for rel,p in paths.items():
            content = read(rel) if rel in supplied else text(p)
            clean = re.sub(r'#[^\n]*', '', content)
            for m in pattern.finditer(clean): findings.append((rel,m[1]))
            interesting = any(k in clean for k in ['primary_cultures_percent','has_role','ship_type_fraction'])
            interesting |= rel.startswith('common/production_methods/') and 'ai_weight' in clean
            if not interesting: continue
            for n in walk(parse(content)):
                if n.key == 'primary_cultures_percent_state':
                    ratio_count += 1
                    check(rel+'.primary_culture_target', n.one('target_country') == 'owner' and len(n.children('value')) == 1)
                if n.key == 'has_role':
                    check(rel+'.role_database_argument', n.value not in role_types)
                if n.key in ['country_ship_type_fraction','formation_ship_type_fraction']:
                    check(rel+'.ship_type_target', isinstance(n.one('target'),str) and n.one('target').startswith('ship_type:') and n.one('target').split(':',1)[1] in ships)
                if rel.startswith('common/production_methods/') and n.key == 'ai_weight':
                    check(rel+'.no_rejected_PM_ai_weight', False)
    check('no_audited_removed_API_remaining', not findings)
    check('primary_culture_inventory_eight', ratio_count == 8)
    # The existing +/- effects and duplicate correction, not a balance rework.
    bloc = parsed['common/power_bloc_principles/1776_imperial_principles.txt']
    cost = 'country_institution_cost_institution_workplace_safety_mult'
    costs = [n.value for n in walk(bloc) if n.key == cost]
    check('imperial.workplace_discount_once_per_tier', costs == ['-0.10','-0.20','-0.30'])
    check('imperial.no_embedded_directive', 'country_institution_cost_REPLACE_OR_CREATE:' not in read('common/power_bloc_principles/1776_imperial_principles.txt'))
    modifiers = parsed['common/modifier_type_definitions/zz_1776_v115_missing_modifier_types.txt']
    check('both_missing_modifiers_registered', {n.key for n in modifiers} == {cost,'building_limestone_quarry_throughput_add'})
    score = parsed['common/script_values/zz_1776_v115_ideology_compatibility.txt'][0]
    groups = json.loads(text(LOT/'SOCIAL_DEMOCRAT_SCORE.json'))
    policy = next(n for n in parse(text(ROOT/'common/ideologies/01_character_ideologies.txt')) if n.key == 'ideology_social_democrat')
    rank = {'strongly_disapprove':-2,'disapprove':-1,'neutral':0,'approve':1,'strongly_approve':2}
    for g, branch in zip(groups, score.children('if')):
        stances = policy.children(g['group'])[0].children()
        least = min(rank[n.value] for n in stances)
        expected_laws = {n.key for n in stances if rank[n.value] == least}
        got = {n.value.removeprefix('law_type:') for n in walk(branch.children('limit')) if n.key == 'has_law_or_variant'}
        check(g['group']+'.score_uses_retained_lowest_stances', got == expected_laws and branch.one('add') == '1')
    check('social_democrat.seven_policy_groups', len(groups) == len(score.children('if')) == 7 and score.one('value') == '0')
    locs=[]
    for lang in ['english','french']:
        rel=f'localization/{lang}/1776_v115_missing_modifiers_l_{lang}.yml'
        data=(supplied[rel] if candidate else ROOT/rel).read_bytes();s=read(rel)
        check(lang+'.localization_BOM', data.startswith(b'\xef\xbb\xbf'))
        check(lang+'.localization_header', s.splitlines()[0]=='l_'+lang+':')
        locs.append(set(re.findall(r'^ ([\w]+):',s,re.M)))
    check('localization.languages_same_four_keys', locs[0]==locs[1] and len(locs[0])==4)
    protected_changes = [rel for rel,h in base['runtime_hashes'].items() if rel not in supplied and (not (ROOT/rel).is_file() or SHA((ROOT/rel).read_bytes()) != h)]
    errors=[c['check'] for c in checks if not c['passed']]
    return {'status':'FAIL_STATIC' if errors else 'PASS_STATIC_ONLY','checks_passed':len(checks)-len(errors),
        'checks_total':len(checks),'errors':errors,'removed_API_findings':findings,
        'bounded_edits':len(migrations),'changed_existing_files':len(changed),'new_files':len(supplied)-len(changed),
        'protected_files_checked':len(base['runtime_hashes'])-len(changed),
        'concurrent_changes':protected_changes,'checks':checks,'engine_tested':False,'human_validated':False}


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--candidate',action='store_true')
    p.add_argument('--output',type=Path)
    a=p.parse_args(); result=audit(a.candidate)
    if a.output: a.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
    sys.exit(bool(result['errors']))
