"""Static references and battle-side projections for land fortifications.

Projects the actual condition AST with supplied battle facts. Does not run
Victoria 3, prove native callbacks or replace a game/save/budget test.
"""
from copy import deepcopy
from decimal import Decimal
from pathlib import Path
import hashlib
import json
import re
import subprocess

from PIL import Image
from validate_diplomacy_ottoman_1776 import parse, walk, normalized
from localization_duplicate_audit import entries
import build_land_fortification_battles as build
from build_land_fortification_icon import expected_dds, ICON

ROOT, GAME, REPORT = build.ROOT, build.GAME, build.REPORT
CHECKS = {}
CASES = []
OWN = ['common/building_groups/1776_land_fortifications.txt',
       'common/buildings/1776_land_fortifications.txt',
       'common/production_methods/1776_land_fortifications.txt',
       'common/production_method_groups/1776_land_fortifications.txt',
       'common/modifier_type_definitions/1776_land_fortifications.txt',
       build.BASEFILE, build.NEWFILE, build.TRIGFILE]


def read(path, game=False):
    return ((GAME if game else ROOT) / path).read_text(encoding='utf-8-sig')


def definition(path, key, game=False):
    return next(n for n in parse(read(path, game)) if n.key == key)


def check(name, value):
    CHECKS[name] = bool(value)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Projection:
    """Restricted evaluator: fails on unsupported expressions, never guesses."""
    def __init__(self, helpers):
        self.helpers = helpers

    def value(self, value, cursor, previous, root):
        if isinstance(value, list): return self.arithmetic(value, cursor, previous, root)
        if value in {'yes', 'no'}: return value == 'yes'
        try: return float(value)
        except ValueError: pass
        if value.startswith('prev.'):
            return self.value(value[5:], previous, None, root)
        if value.startswith('opposite_battle_side.'):
            return self.value(value[21:], cursor['opposite_battle_side'], cursor, root)
        if value == 'scope:character': return root.get('commander')
        if value == 'scope:is_advancing_side': return root['advancing']
        if value.startswith('modifier:'):
            return cursor.get('modifiers', {}).get(value[9:], 0)
        if value in cursor: return cursor[value]
        # Fixed database keys are identifiers, not dynamic getters.
        if value.startswith(('battle_condition_', 'building_', 'general')): return value
        raise ValueError('Unknown projected value: ' + value)

    def arithmetic(self, nodes, cursor, previous, root, initial=0):
        result, chain = initial, False
        for n in nodes:
            if n.key in {'if', 'else_if', 'else'}:
                should = (n.key == 'if' or not chain) and (n.key == 'else' or self.all(n.children('limit')[0].children(), cursor, previous, root))
                if n.key == 'if': chain = False
                if should:
                    result = self.arithmetic([x for x in n.children() if x.key != 'limit'], cursor, previous, root, result)
                    chain = True
                continue
            val = self.value(n.value, cursor, previous, root)
            if n.key == 'value': result = val
            elif n.key == 'add': result += val
            elif n.key == 'multiply': result *= val
            elif n.key == 'divide': result /= val
            elif n.key == 'min': result = max(result, val)
            elif n.key == 'max': result = min(result, val)
            else: raise ValueError('Unsupported arithmetic: ' + n.key)
        return result

    def one(self, n, cursor, previous, root):
        if n.key == 'OR': return any(self.one(x, cursor, previous, root) for x in n.children())
        if n.key in {'NOT', 'NOR'}: return not any(self.one(x, cursor, previous, root) for x in n.children())
        if n.key == 'AND': return self.all(n.children(), cursor, previous, root)
        if n.key in self.helpers:
            return self.all(self.helpers[n.key].children(), cursor, previous, root) == (n.value == 'yes')
        if n.key == 'exists': return self.value(n.value, cursor, previous, root) is not None
        if n.key == 'has_battle_condition': return cursor['condition'] == n.value
        if n.key == 'has_building': return n.value in cursor.get('buildings', set())
        if n.key == 'has_role_of_type': return n.value in cursor.get('roles', set())
        actual = self.value(n.key, cursor, previous, root)
        if isinstance(n.value, list) and n.key in {'province', 'state', 'country', 'owner', 'opposite_battle_side', 'scope:character'}:
            return (n.op == '?=') if actual is None else self.all(n.children(), actual, cursor, root)
        desired = self.value(n.value, cursor, previous, root)
        if n.op in {'=', '?='}: return actual == desired
        if n.op == '>': return actual > desired
        if n.op == '>=': return actual >= desired
        if n.op == '<': return actual < desired
        if n.op == '<=': return actual <= desired
        raise ValueError('Unsupported comparison: ' + n.op)

    def all(self, nodes, cursor, previous=None, root=None):
        return all(self.one(n, cursor, previous, root or cursor) for n in nodes)

    def allowed(self, condition, field, side):
        found = condition.children(field)
        return bool(found) and self.all(found[0].children(), side)


def sides(strength=5, *, advancing=False, owner='D', controller='D', country='D', coast=False,
          fort=True, manpower=100, enemy_manpower=100, experience=0, condition=None, enemy_condition=None,
          guerilla=False, commander=True):
    countries = {tag: dict(tag=tag, is_in_guerilla_war=guerilla if tag == country else False) for tag in ['D','A','F']}
    region = dict(owner=countries[owner], controller=countries[controller], is_coastal=coast,
                  buildings={'building_aor1776_land_fortification'} if fort else set(),
                  modifiers={build.STRENGTH: strength})
    province = dict(owner=countries[owner], controller=countries[controller])
    char = dict(owner=countries[country], experience_level=experience, roles={'general'}) if commander else None
    side = dict(country=countries[country], state=region, province=province, commander=char,
                advancing=advancing, condition=condition, current_manpower=manpower, starting_manpower=100)
    enemy = dict(country=countries['A'], state=region, province=province,
                 commander=dict(owner=countries['A'], experience_level=0, roles={'general'}),
                 advancing=not advancing, condition=enemy_condition, current_manpower=enemy_manpower, starting_manpower=100)
    side['opposite_battle_side'] = enemy
    enemy['opposite_battle_side'] = side
    return side


def main():
    for path in OWN: check('syntax.' + path, bool(parse(read(path))))
    outputs, native, standards, forts = build.build()
    helpers = {n.key: n for n in parse(read(build.TRIGFILE))}
    evaluator = Projection(helpers)
    native_eval = Projection({})
    all_conditions = {n.key: n for n in standards + forts}
    for rel, expected in outputs.items(): check('generation.' + rel, read(rel) == expected)

    building = parse(read(OWN[1]))[0]
    naval_building = definition('common/buildings/05_military.txt', 'building_naval_fortification')
    check('construction.only_inland', normalized(building.children('potential')[0].children()) == [('is_coastal','=','no')])
    check('construction.same_gate_as_naval', normalized(building.children('unlocking_technologies')) == normalized(naval_building.children('unlocking_technologies')))
    check('construction.same_cost', building.one('required_construction') == naval_building.one('required_construction'))
    check('construction.native_hard_max_enabled', building.one('has_max_level') == 'yes')
    check('construction.not_naval_or_a_recruiting_barracks', building.one('naval') == 'no' and building.one('recruits_combat_units') is None)
    group = parse(read(OWN[0]))[0]
    check('group.funded_army_no_economy_of_scale', group.one('parent_group') == 'bg_army' and group.one('economy_of_scale') == 'no' and group.one('infrastructure_usage_per_level') == '0.2')
    pmg = parse(read(OWN[3]))[0]
    check('methods.three_levels_in_native_order', [n.value for n in pmg.children('production_methods')[0].children()] == ['pm_aor1776_land_fortification_' + x for x in ['basic','reinforced','advanced']])
    for quality, kind in enumerate(['basic','reinforced','advanced'], 1):
        land = definition(OWN[2], 'pm_aor1776_land_fortification_' + kind)
        sea = definition('common/production_methods/05_military.txt', 'pm_naval_fortification_' + kind)
        check('methods.same_icon.' + kind, land.one('texture') == sea.one('texture'))
        check('methods.same_technology.' + kind, normalized(land.children('unlocking_technologies')) == normalized(sea.children('unlocking_technologies')))
        check('methods.same_goods_and_staff.' + kind, normalized(land.children('building_modifiers')) == normalized(sea.children('building_modifiers')))
        output = land.children('state_modifiers')[0].children('workforce_scaled')[0]
        check('methods.only_staff_scaled_local_strength.' + kind, normalized(output.children()) == [(build.STRENGTH,'=',str(quality))] and len(land.children('state_modifiers')[0].children()) == 1)
        check('methods.no_country_or_maritime_effect.' + kind, not land.children('country_modifiers') and not any(
            any(w in n.key for w in ['naval','blockade','strait','bombardment']) for n in walk(land.children('state_modifiers'))))

    techfile = 'common/technology/technologies/20_tech3a_military.txt'
    before = parse((REPORT/'baseline'/techfile).read_text(encoding='utf-8-sig'))
    after = parse(read(techfile))
    restored = deepcopy(after)
    tech = next(n for n in restored if n.key == 'scientific_fortification_siegecraft')
    cap = tech.children('modifier')[0]
    check('cap.only_five_levels_unlocked', normalized(cap.children()) == [('state_building_aor1776_land_fortification_max_level_add','=','5')])
    tech.value.remove(cap)
    check('technology.other_effects_tree_and_starting_techs_preserved', normalized(restored) == normalized(before))

    # Native modifiers and weights are preserved exactly. Only eligibility and
    # references to the three emergency classes are adapted for local forts.
    for changed in standards:
        old = native[changed.key]
        check('native.unchanged_modifier.' + changed.key, normalized(changed.children('modifier')) == normalized(old.children('modifier')))
        expected_weight = deepcopy(old.children('weight'))
        build.expand_urgent_references(expected_weight)
        check('native.unchanged_weight.' + changed.key, normalized(changed.children('weight')) == normalized(expected_weight))
    check('native.original_21_conditions_preserved', len(standards) == len(native) == 21)
    check('local.15_bands_with_native_emergencies_and_exit', len(forts) == 61)

    def candidates(side, field, conditions=all_conditions, ev=evaluator):
        return {k for k,n in conditions.items() if k != side['condition'] and ev.allowed(n,field,side)}

    # No-fort projections must match the canonical rules, for both sides and
    # all original current-condition classes, including emergency transitions.
    snapshots = [dict(manpower=100,enemy_manpower=100), dict(manpower=15,enemy_manpower=100,experience=6),
                 dict(manpower=5,enemy_manpower=100,experience=6), dict(manpower=1500,enemy_manpower=100),
                 dict(manpower=5,enemy_manpower=100,experience=0), dict(guerilla=True)]
    for index, facts in enumerate(snapshots):
        for advancing in [False,True]:
            for condition in [None] + list(native):
                side = sides(strength=0,fort=False,advancing=advancing,condition=condition,**facts)
                for field in ['possible','instant_switch']:
                    actual = candidates(side,field)
                    expected = candidates(side,field,native,native_eval)
                    check(f'outside_fort.native_equivalence.{index}.{advancing}.{condition}.{field}', actual == expected)

    # Full and partial garrisons, boundaries and illegal location/ownership.
    for value in [0,.001,.49,.5,.99,1,1.49,1.5,2.49,4.9,5,7.5,9.99,14.49,14.5,15,99]:
        side = sides(strength=value)
        actual = candidates(side,'possible')
        if value < .5:
            expected = candidates(side,'possible',native,native_eval)
        else:
            strength = min(15,int(Decimal(str(value)) + Decimal('.5')))
            expected = {build.fort_key('defense',strength)}
        check('strength.band.' + str(value), actual == expected)
    for name, facts in [('attacking',dict(advancing=True)),('coast',dict(coast=True)),
                        ('enemy_owner',dict(owner='A')),('occupied',dict(controller='A')),
                        ('allied_lead_country',dict(country='F')),('demolished',dict(fort=False)),
                        ('empty_garrison',dict(strength=0))]:
        side = sides(**facts)
        check('scope.no_bonus.' + name, not evaluator.all(helpers[build.ELIGIBLE].children(),side)
              and not any(k.startswith('battle_condition_aor1776_') for k in candidates(side,'possible')))
    check('scope.new_owner_can_defend_its_own_captured_fort', evaluator.all(helpers[build.ELIGIBLE].children(),sides(country='A',owner='A',controller='A')))

    for strength in range(1,16):
        for kind in ['defense'] + build.URGENT:
            condition = all_conditions[build.fort_key(kind,strength)]
            actual = {n.key:Decimal(n.value) for n in condition.children('modifier')[0].children()}
            base_stats = {} if kind == 'defense' else {n.key:Decimal(n.value) for n in native['battle_condition_'+kind].children('modifier')[0].children()}
            for key,value in build.protection(strength).items(): base_stats[key] = base_stats.get(key,Decimal(0)) + value
            check(f'local.native_emergency_stats_plus_protection.{kind}.{strength}', actual == base_stats)
            side = sides(strength=strength,condition=condition.key)
            check(f'local.no_self_switch_loop.{kind}.{strength}', not evaluator.allowed(condition,'instant_switch',side))
        for name,facts,expected_kind in [
            ('panic',dict(manpower=15,enemy_manpower=100,experience=0),'panicked_retreat'),
            ('controlled',dict(manpower=15,enemy_manpower=100,experience=6),'controlled_retreat'),
            ('pursuit',dict(manpower=1500,enemy_manpower=100),'pursuit'),
        ]:
            side = sides(strength=strength,condition=build.fort_key('defense',strength),**facts)
            selected = candidates(side,'instant_switch')
            check(f'transition.native_{name}_retains_protection.{strength}', selected == {build.fort_key(expected_kind,strength)})
            CASES.append(dict(kind=name,strength=strength,eligible_instant_switches=sorted(selected),method='STATIC_AST_PROJECTION'))
        # Losing the fort removes its protection on the next native check.
        for kind in ['defense'] + build.URGENT:
            side = sides(strength=0,fort=False,condition=build.fort_key(kind,strength))
            target = 'battle_condition_aor1776_land_fort_abandoned' if kind == 'defense' else 'battle_condition_'+kind
            check(f'exit.no_stale_bonus.{kind}.{strength}', target in candidates(side,'instant_switch'))
    # Current/enemy emergency identity also survives aliases across strength.
    for kind in build.URGENT:
        side = sides(condition=build.fort_key(kind,5))
        check('references.native_emergency_identity.'+kind, evaluator.all(helpers[build.class_key(kind)].children(),side))
    # Independent user-facing calibration, read from the emitted conditions.
    # Five-level totals are 25/50/75 percent, with only the
    # fortification's territorial protection capped at 75%.
    expected_provinces = {
        1: ['-.05','-.10','-.15','-.20','-.25'],
        2: ['-.10','-.20','-.30','-.40','-.50'],
        3: ['-.15','-.30','-.45','-.60','-.75'],
    }
    rates = {1:Decimal('.05'),2:Decimal('.10'),3:Decimal('.15')}
    for quality, levels in expected_provinces.items():
        for level, province_value in enumerate(levels,1):
            strength = quality*level
            actual = {n.key:Decimal(n.value) for n in all_conditions[build.fort_key('defense',strength)].children('modifier')[0].children()}
            expected = {'unit_provinces_lost_mult':Decimal(province_value),
                        'battle_casualties_mult':-rates[quality]*level,
                        'unit_army_defense_mult':rates[quality]*level}
            check(f'calibration.per_level.{quality}.{level}', actual == expected)
            CASES.append(dict(levels=level,staffing=1,quality=quality,strength=strength,
                              modifiers={k:str(v) for k,v in actual.items()},method='STATIC_EMITTED_CONDITION'))
    province_modifiers = [Decimal(n.value) for condition in forts for n in condition.children('modifier')[0].children()
                          if n.key == 'unit_provinces_lost_mult']
    check('cap.all_fortified_stances_and_retreats_at_most_75_percent',
          len(province_modifiers)==60 and all(Decimal('-.75') <= value <= 0 for value in province_modifiers))
    check('calibration.five_advanced_levels_total_75_percent',min(province_modifiers)==Decimal('-.75'))

    # All new aliases and icons resolve; the original naval definitions remain
    # covered by the broad source baseline, not a selective copied comparison.
    definitions = {n.key for path in OWN for n in parse(read(path))}
    all_battle_keys = {p.key for p in standards+forts}
    check('references.all_condition_keys_exist', all(n.value in all_battle_keys for p in OWN for n in walk(parse(read(p))) if n.key=='has_battle_condition'))
    check('references.helper_keys_exist', all(n.key in helpers for p in OWN for n in walk(parse(read(p))) if n.key.startswith('aor1776_land_')))
    for path in OWN:
        for n in walk(parse(read(path))):
            if n.key in {'texture','icon','background'} and isinstance(n.value,str):
                asset=n.value.strip('"')
                check('references.asset.'+asset,(ROOT/asset).exists() or (GAME/asset).exists())
    keysets=[]
    for lang in ['french','english']:
        path=ROOT/f'localization/{lang}/1776_land_fortifications_l_{lang}.yml'
        lines=path.read_text(encoding='utf-8-sig').splitlines()
        matches=[re.fullmatch(r'\s+([A-Za-z0-9_.-]+):0 "([^"\n]|\\")*"',line) for line in lines[1:] if line.strip()]
        keys={m.group(1) for m in matches if m}
        catalog=entries(lang)
        check('localization.valid_BOM.'+lang,path.read_bytes().startswith(b'\xef\xbb\xbf') and lines[0]=='l_'+lang+':' and all(matches))
        check('localization.unique.'+lang,all(len(catalog[k])==1 for k in keys))
        required={n.key for n in forts}|{n.key+'_desc' for n in forts}
        required|={'building_aor1776_land_fortification','bg_aor1776_land_fortification','pmg_aor1776_land_fortification'}
        required|={n.key for n in parse(read(OWN[2]))}
        # Modifier types localize their exact key, as the native naval entries
        # demonstrate. They do not use the static-modifier naming convention.
        native_catalog=entries(lang,root=GAME/'localization')
        check('localization.native_modifier_type_contract.'+lang,
              'state_fortification_naval_invasion_add' in native_catalog
              and 'state_building_naval_fortification_max_level_add' in native_catalog)
        required|={n.key for n in parse(read(OWN[4]))}
        required|={n.key+'_desc' for n in parse(read(OWN[4]))}
        check('localization.all_UI_keys.'+lang,required<=keys)
        check('localization.aliases_resolve.'+lang,all(x in catalog for x in re.findall(r'\$([A-Za-z0-9_.-]+)\$',path.read_text(encoding='utf-8-sig'))))
        compact=path.read_text(encoding='utf-8-sig').replace('\u00a0','')
        check('localization.rebalanced_values_and_cap.'+lang, all(token in compact for token in ['25%','50%','75%','5%']))
        keysets.append(keys)
    check('localization.same_FR_EN_keys',keysets[0]==keysets[1])
    dds,target=expected_dds()
    check('asset.native_format_and_alpha_preserved',ICON.read_bytes()==dds)
    icon=Image.open(ICON).convert('RGBA')
    check('asset.no_white_background',all(icon.getpixel(p)[3]==0 for p in [(0,0),(255,0),(0,255),(255,255)]))
    icon.save(REPORT/'ICON_PREVIEW.png')

    base=json.loads((REPORT/'BASELINE.json').read_text(encoding='utf-8'))
    changed=[rel for rel,digest in base['protected'].items() if sha(ROOT/rel)!=digest]
    check('preservation.all_existing_gameplay_and_map_files',not changed)
    check('preservation.canonical_vanilla_read_only',all(sha(GAME/rel)==digest for rel,digest in base['canonical_game'].items()))
    check('preservation.HEAD',subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==base['head'])
    check('preservation.index',sha(ROOT/'.git/index')==base['index_sha256'])
    r3=json.loads((REPORT/'R3_BASELINE.json').read_text(encoding='utf-8'))
    old_forts=parse((REPORT/'baseline_r3'/build.NEWFILE).read_text(encoding='utf-8-sig'))
    old_shapes,new_shapes=deepcopy(old_forts),deepcopy(forts)
    fields={'unit_provinces_lost_mult'}
    for shape in old_shapes+new_shapes:
        for block in shape.children('modifier'):
            block.value[:]=[n for n in block.children() if n.key not in fields]
    check('R3.only_provinces_lost_values_changed',normalized(old_shapes)==normalized(new_shapes))
    r3_changed=[p for p,h in r3['protected'].items() if sha(ROOT/p)!=h]
    check('R3.other_sources_methods_gates_cap_and_icon_preserved',not r3_changed)
    check('R3.battle_helpers_unchanged',sha(ROOT/build.TRIGFILE)==r3['owned'][build.TRIGFILE])
    report=dict(status='PASS_STATIC' if all(CHECKS.values()) else 'FAIL_STATIC',passed=sum(CHECKS.values()),
                total=len(CHECKS),failed=[k for k,v in CHECKS.items() if not v],checks=CHECKS,
                scenarios=CASES,protected_file_count=len(base['protected']),changed_protected_files=changed,
                runtime='NOT_RUN',native_save_reload='NOT_RUN',native_building_cap='REQUIRES_RUNTIME_VALIDATION',
                native_battle_selection='REQUIRES_RUNTIME_VALIDATION',files=OWN+[techfile],
                rebalance_revision='R3_FIVE_LEVEL_TOTALS_25_50_75',
                fortification_province_loss_cap='75 percent; other country/unit modifiers remain native',
                r3_protected_file_count=len(r3['protected']),r3_changed_protected_files=r3_changed,
                source_sha256={p:sha(ROOT/p) for p in OWN+[techfile]+[
                    f'localization/{lang}/1776_land_fortifications_l_{lang}.yml' for lang in ['french','english']]},
                icon_sha256=sha(ICON))
    (REPORT/'VALIDATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ['status','passed','total','failed','protected_file_count','changed_protected_files','runtime']},ensure_ascii=False,indent=2))
    return 0 if all(CHECKS.values()) else 1


if __name__=='__main__':
    raise SystemExit(main())
