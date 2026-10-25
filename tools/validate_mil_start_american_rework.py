"""Read-only regression checks for MIL-START and the American Revolution lots.

Does not launch Victoria 3, apply patches, write reports, or change Git state.
Run from any directory with the bundled Python. JSON is printed on stdout.
The concurrent MAP-2W work is deliberately outside the compared country scopes.
"""
from pathlib import Path
import collections as C
import hashlib
import json
import re
import subprocess
import sys

from validate_diplomacy_ottoman_1776 import parse, walk, scalar, normalized
from map_1776_audit import effective, values
import start_buildings_2026_10_15 as economy
from localization_duplicate_audit import entries

ROOT = Path(__file__).resolve().parents[1]
GAME = Path('C:/Games/Victoria 3/game')
BASE = 'f97dc56'
FOLDER = 'common/history/military_formations/'
FILES = {
    '00_military_formations_europe.txt': ['POR'],
    '01_military_formations_north_america.txt': ['USA'],
    '02_military_formations_south_america.txt': ['BRZ', 'SC2', 'SC4'],
}
TARGETS = ['USA', 'BRZ', 'SC2', 'SC4', 'POR']


def current(file):
    return (ROOT/file).read_text(encoding='utf-8-sig')


def original(file):
    return subprocess.check_output(['git', 'show', BASE+':'+file], cwd=ROOT).decode('utf-8-sig').replace('\r\n', '\n')


def country(raw, tag):
    return next(n for n in walk(parse(raw)) if n.key == 'c:'+tag)


def outside(raw, tags):
    edits = [n for n in walk(parse(raw)) if n.key in {'c:'+t for t in tags}]
    for n in sorted(edits, key=lambda x:x.start, reverse=True):
        raw = raw[:n.start]+'<COUNTRY:'+n.key+'>'+raw[n.end:]
    return raw


def formations(tag):
    file = next(f for f, tags in FILES.items() if tag in tags)
    return country(current(FOLDER+file), tag).children('create_military_formation')


def population():
    result = C.Counter()
    for path in effective(ROOT, GAME, 'common/history/pops'):
        for state in walk(parse(path.read_text(encoding='utf-8-sig'))):
            if not state.key.startswith('s:STATE_'):
                continue
            for region in state.children():
                if region.key.startswith('region_state:'):
                    tag = region.key.split(':')[1]
                    if tag in TARGETS:
                        result[tag] += sum(int(n.value) for n in walk(region.children()) if n.key == 'size')
    return result


def main():
    # BASE is the historical comparison point, not a prohibition on subsequent
    # user merges. Check that this read-only run itself leaves HEAD unchanged.
    head_start = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    checks = {}
    warnings = ['NAV-USA-TECH: five preserved caravels require absent enclosed_dock_systems; runtime review pending.']
    counts = {}
    for file, tags in FILES.items():
        rel = FOLDER+file
        old, new = original(rel), current(rel)
        parse(new)
        checks[file+'_only_target_countries_changed'] = outside(old, tags) == outside(new, tags)
        for tag in tags:
            counts[tag] = C.Counter()
            gates = []
            for formation in formations(tag):
                for unit in formation.children():
                    if unit.key not in ('ship', 'combat_unit'):
                        continue
                    kind = scalar(unit.one('type')).split(':')[1]
                    service = unit.one('service_type', 'regular')
                    count = int(unit.one('count'))
                    counts[tag][kind+'/'+service] += count
                    catalog = economy.catalog('common/ship_types' if unit.key == 'ship' else 'common/combat_unit_types')
                    assert kind in catalog, kind
                    if tag != 'USA' or unit.key != 'ship':
                        gates += list(set(values(catalog[kind], 'unlocking_technologies'))-economy.starting_tech(tag))
                    checks[tag+'_'+kind+'_positive_count'] = count > 0
            checks[tag+'_unit_tech_gates_except_preserved_USA_fleet'] = not gates

    expected = {
        'USA': {'combat_unit_type_musket_infantry/regular':12,'combat_unit_type_improved_cannon_artillery/regular':1,'combat_unit_type_musket_infantry/conscript':15,'ship_type_caravel/regular':5},
        'BRZ': {'combat_unit_type_irregular_infantry/regular':3,'combat_unit_type_lancers/regular':1,'ship_type_caravel/regular':8,'ship_type_galley/regular':1},
        'SC2': {'combat_unit_type_musket_infantry/regular':23,'combat_unit_type_irregular_infantry/regular':6,'combat_unit_type_lancers/regular':5},
        'SC4': {'combat_unit_type_musket_infantry/regular':6,'combat_unit_type_lancers/regular':1},
        'POR': {'combat_unit_type_musket_infantry/regular':18,'combat_unit_type_dragoons/regular':4,'combat_unit_type_improved_cannon_artillery/regular':2,'combat_unit_type_musket_infantry/conscript':23,'ship_type_caravel/regular':8,'ship_type_galley/regular':3,'ship_type_frigate/regular':1},
    }
    for tag in TARGETS:
        checks[tag+'_exact_units'] = dict(counts[tag]) == expected[tag]

    na = FOLDER+'01_military_formations_north_america.txt'
    usa_old, usa_new = country(original(na),'USA'), country(current(na),'USA')
    checks['MIL_USA_formation_nodes_unchanged'] = normalized(usa_old.children('create_military_formation')) == normalized(usa_new.children('create_military_formation'))
    old_hashes = [hashlib.sha256(original(na)[n.start:n.end].encode()).hexdigest() for n in usa_old.children('create_military_formation')]
    new_hashes = [hashlib.sha256(current(na)[n.start:n.end].encode()).hexdigest() for n in usa_new.children('create_military_formation')]
    checks['MIL_USA_formation_text_hashes_unchanged'] = old_hashes == new_hashes
    for a,b in zip(usa_old.children('create_character'),usa_new.children('create_character')):
        checks['existing_character_'+str(a.one('save_scope_as'))+'_preserved_except_template'] = normalized(a.children()) == normalized([n for n in b.children() if n.key!='template'])

    templates = economy.catalog('common/character_templates')
    traitdefs = economy.catalog('common/character_traits')
    chars = usa_new.children('create_character')
    checks['seven_USA_commanders'] = len(chars) == 7
    checks['seven_distinct_templates'] = len({n.one('template') for n in chars}) == 7
    born = []
    for char in chars:
        key = scalar(char.one('template'))
        model = templates[key]
        checks[key+'_no_random_generation'] = model.one('trait_generation') == []
        ts = values(model,'traits')
        checks[key+'_traits_exist_no_compliant_pillager'] = bool(ts) and all(t in traitdefs and t not in ['compliant','pillager'] for t in ts)
        birth = char.one('birth_date',model.one('birth_date'))
        checks[key+'_born_before_start'] = bool(birth) and tuple(map(int,birth.split('.'))) < (1776,1,1)
        born.append(birth)
    definitions = C.Counter(n.key for p in effective(ROOT,GAME,'common/character_templates') for n in parse(p.read_text(encoding='utf-8-sig')))
    checks['new_template_ids_unique'] = all(definitions[n.one('template')]==1 for n in chars)
    transfers = [n.value for n in walk(usa_new.children()) if n.key=='transfer_to_formation']
    checks['four_generals_army_one_admiral_fleet'] = transfers.count('scope:dannys_army')==4 and transfers.count('scope:cleanup2d6_fleet_030')==1 and len(transfers)==5
    saved = {n.value for n in walk(usa_new.children()) if n.key=='save_scope_as'}
    checks['transfer_scopes_exist'] = all(x.removeprefix('scope:') in saved for x in transfers)

    for language in ['french','english']:
        loc = entries(language)
        keys = []
        for stem in ['1776_military_start','1776_usa_commanders']:
            path = ROOT/f'localization/{language}/{stem}_l_{language}.yml'
            text = path.read_text(encoding='utf-8-sig')
            own = [re.match(r'^ ([\w.]+):0 "[^"\r\n]*"$',line) for line in text.splitlines()[1:]]
            checks[language+'_'+stem+'_BOM_header_syntax'] = path.read_bytes().startswith(b'\xef\xbb\xbf') and text.startswith('l_'+language+':\n') and all(own)
            keys += [m.group(1) for m in own if m]
        checks[language+'_all_16_new_keys_unique'] = len(keys)==16 and all(len(loc[k])==1 for k in keys)
        checks[language+'_new_names_consumed'] = all(k in current('common/character_templates/1776_usa_commanders.txt') or any(k in current(FOLDER+f) for f in FILES) for k in keys)

    before = json.loads(current('docs/reports/military/MIL_START_AUDIT/BEFORE.json'))
    pops = population()
    for tag in TARGETS:
        checks[tag+'_population_unchanged'] = pops[tag] == before[tag]['population']
        checks[tag+'_technologies_unchanged'] = sorted(economy.starting_tech(tag)) == before[tag]['technologies']
        paths = [p for p in (ROOT/'common/history/countries').glob('*.txt') if p.name.lower().startswith(tag.lower()+' -')]
        checks[tag+'_country_history_laws_economy_unchanged'] = all(current(p.relative_to(ROOT))==original(p.relative_to(ROOT).as_posix()) for p in paths)

    unchanged = ['common/journal_entries/06_usa_independence_mod.txt','events/french_revolution_mod_events.txt','common/laws/00_army_model.txt','common/combat_unit_types/00_land_combat_unit_types.txt','common/ship_types/00_ship_types.txt','common/ship_types/10_1776_early_ships.txt','common/history/diplomatic_plays/00_american_revolution.txt','common/history/diplomacy/00_subject_relationships.txt']
    for f in unchanged:
        checks[f+'_unchanged'] = current(f)==original(f)
    modfile = 'common/static_modifiers/76mod_modifiers.txt'
    key = 'modifier_usa_war_of_independence'
    a,b = parse(original(modfile)),parse(current(modfile))
    checks['other_static_modifiers_unchanged'] = normalized([n for n in a if n.key!=key]) == normalized([n for n in b if n.key!=key])
    mod = next(n for n in b if n.key==key)
    checks['exact_BAL_R1'] = {n.key:n.value for n in mod.children()} == {'icon':'gfx/interface/icons/timed_modifier_icons/modifier_rifle_positive.dds','building_training_rate_mult':'0.15','unit_morale_recovery_mult':'0.15','unit_morale_loss_mult':'-0.10','country_liberty_desire_add':'0.35'}
    checks['no_staged_changes'] = subprocess.run(['git','diff','--cached','--quiet'],cwd=ROOT).returncode==0
    checks['HEAD_unchanged'] = subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==head_start
    status = 'READY_FOR_RUNTIME_VALIDATION' if all(checks.values()) else 'STATIC_VALIDATION_FAILED'
    result = dict(status=status,runtime_tested=False,base_commit=BASE,checked_head=head_start,checks=checks,passed=sum(checks.values()),failed=[k for k,v in checks.items() if not v],warnings=warnings,formation_sha256=new_hashes,counts=counts,populations=pops,design_status='DESIGN_ONLY; CAVALRY: AUDIT_AND_PROPOSAL_ONLY')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if all(checks.values()) else 1


if __name__=='__main__':
    sys.exit(main())
