"""Rebalance cumulative PM employment; exhaustive, read-only audit by default.

--apply first simulates the patch and refuses it unless every selectable PM
combination has nonnegative employment in every profession. Sources and hashes
are frozen before writing. No Git, vanilla, maps or history mutations.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from copy import deepcopy
import csv
from datetime import datetime, timezone
import itertools
import json
from pathlib import Path
import re
import shutil
from decimal import Decimal

import audit_anzin_regional_infrastructure as a
from validate_diplomacy_ottoman_1776 import parse, normalized
from localization_duplicate_audit import entries

ROOT = a.ROOT
REPORT = ROOT / 'docs/reports/economy/AUTOMATION_EMPLOYMENT_R1'
NEW_PM = 'common/production_methods/1776_automation_employment_profiles.txt'
NEW_PMG = 'common/production_method_groups/1776_automation_employment_profiles.txt'
SCI = 'pm_scientific_management'


def jobs(node):
    result = defaultdict(int)
    for block in node.children('building_modifiers'):
        for scale in block.children():
            for stat in scale.children():
                if stat.key.startswith('building_employment_') and stat.key.endswith('_add'):
                    assert scale.key == 'level_scaled', (node.key, scale.key)
                    result[stat.key[20:-4]] += int(stat.value)
    return dict(result)


def valid(combo, methods):
    # Native lists are alternatives: e.g. elastics requires sewing machines OR
    # electric sewing machines, which occupy the very same PM group.
    selected = set(combo)
    return all(not (required := set(a.ids(methods[pm][0], 'unlocking_production_methods')))
               or bool(required & selected) for pm in combo)


def audit(buildings, groups, methods):
    rows = []
    for key, (node, path) in buildings.items():
        group_keys = a.ids(node, 'production_method_groups')
        assert len(group_keys) == len(set(group_keys)), key
        choices = [a.ids(groups[g][0], 'production_methods') for g in group_keys]
        assert all(choices), key
        all_pms = set(itertools.chain.from_iterable(choices))
        profiles = {pm: jobs(methods[pm][0]) for pm in all_pms}
        professions = sorted(set(itertools.chain.from_iterable(profiles.values())))
        minima = {p: None for p in professions}
        examples = {}
        count = 0
        for combo in itertools.product(*choices):
            if not valid(combo, methods):
                continue
            count += 1
            for profession in professions:
                value = sum(profiles[pm].get(profession, 0) for pm in combo)
                if minima[profession] is None or value < minima[profession]:
                    minima[profession] = value
                    examples[profession] = list(combo)
        assert count, key
        negative = {p: {'value': v, 'combination': examples[p]}
                    for p, v in minima.items() if v < 0}
        rows.append(dict(building=key, groups=group_keys, combinations=count,
                         raw_combinations=__import__('math').prod(map(len, choices)),
                         minima=minima, negative=negative))
    return rows


def build_plan():
    buildings = a.catalog('common/buildings')
    groups = a.catalog('common/production_method_groups')
    methods = a.catalog('common/production_methods')
    before = audit(buildings, groups, methods)
    replacements = {}
    clones = {}
    # Each entry is the complete new employment profile, not an extra modifier.
    # Net headcount is invariant for every recipe, including job conversions.
    def change(pm, profile, required=None):
        assert sum(jobs(methods[pm][0]).values()) == sum(profile.values()), pm
        replacements[pm] = (profile, required)

    def clone(new, old, profile, required=None):
        assert new not in methods and new not in clones
        assert sum(jobs(methods[old][0]).values()) == sum(profile.values()), new
        clones[new] = (old, profile, required)

    def cut(pm, laborers=0, machinists=0, engineers=0, shopkeepers=0, farmers=0, required=None):
        change(pm, {k: -v for k, v in dict(laborers=laborers, machinists=machinists,
               engineers=engineers, shopkeepers=shopkeepers, farmers=farmers).items() if v}, required)

    food = ['pm_baking_powder']
    textile = ['pm_chemical_bleaching_textile_mill', 'pm_sewing_machines', 'pm_electric_sewing_machines']
    glass = ['pm_crystal_glass', 'pm_pressed_glass', 'pm_aluminium_housewares', 'pm_houseware_plastics']
    rubber = ['pm_rubber_grips']
    steel = ['pm_blister_steel_process', 'pm_bessemer_process', 'pm_thomas_process',
             'pm_open_hearth_process', 'pm_electric_arc_process']
    chemistry = a.ids(groups['pmg_fertilizer_production'][0], 'production_methods')[1:] + \
                a.ids(groups['pmg_base_building_chemical_works'][0], 'production_methods')[1:]

    cut('pm_automated_bakery', 2000, 750, 250, required=food)
    cut('pm_automatic_power_looms', 1500, 750, 250, required=textile)
    cut('pm_rotary_valve_engine_building_furniture_manufactory', 1500, 500,
        required=['pm_lathe', 'pm_mechanized_workshops'])
    cut('pm_assembly_lines_building_furniture_manufactory', 1500, 1000, 500,
        required=['pm_mechanized_workshops'])
    cut('pm_unit_electric_drive_building_glassworks', 1000, 750, 250, required=glass)
    cut('pm_automatic_bottle_blowers', 1000, 1000, 500, required=glass)
    cut('pm_rotary_valve_engine_building_paper_mill', 1500, 500,
        required=['pm_sulfite_pulping', 'pm_bleached_paper'])
    cut('pm_unit_electric_drive_building_paper_mill', 1500, 750, 250,
        required=['pm_bleached_paper'])
    cut('pm_watertube_boiler_building_tooling_workshop', 1000, 500,
        required=['pm_pig_iron', 'pm_steel', 'pm_rubber_grips'])
    cut('pm_rotary_valve_engine_building_tooling_workshop', 1000, 500, 500,
        required=['pm_steel', 'pm_rubber_grips'])
    cut('pm_unit_electric_drive_building_tooling_workshop', 1000, 1000, 500, required=rubber)
    cut('pm_assembly_lines_building_tooling_workshop', 1000, 1000, 500, 500, required=rubber)
    cut('pm_watertube_boiler_building_steel_mill', 500, 750, 250, required=steel)
    cut('pm_rotary_valve_engine_building_steel_mill', 500, 1000, 500, required=steel[1:])
    cut('pm_unit_electric_drive_building_steel_mill', 500, 1250, 750, required=steel[-2:])
    cut('pm_watertube_boiler_building_motor_industry', machinists=1000)
    cut('pm_rotary_valve_engine_building_motor_industry', machinists=1500)
    cut('pm_unit_electric_drive_building_motor_industry', machinists=1500, engineers=250)
    cut('pm_assembly_lines_building_motor_industry', machinists=1500, engineers=500)
    cut('pm_assembly_lines_building_automotive_industry', machinists=1000, engineers=500)
    cut('pm_rotary_valve_engine_building_arms_industry', 1000, 1000,
        required=['pm_rifles', 'pm_repeaters', 'pm_bolt_action_rifles'])
    cut('pm_assembly_lines_building_arms_industry', 1000, 1000, 500,
        required=['pm_repeaters', 'pm_bolt_action_rifles'])
    cut('pm_rotary_valve_engine_building_munition_plant', 1000, 1000)
    cut('pm_assembly_lines_building_munition_plant', 1000, 1000, 500)
    cut('pm_tractors', 1500, farmers=500)
    cut('pm_compression_ignition_tractors', 1500, farmers=1000)
    # Reallocate zero-net personnel conversions too; merely fixing transport
    # would leave negative employment with precision machinery or ventilation.
    change('pm_electrical_precision_machinery', dict(laborers=-500, machinists=250, engineers=250))
    change('pm_rayon', dict(engineers=-500, machinists=500))
    for pm, value in [('pm_standardized_pharmaceuticals', 250),
                      ('pm_synthetic_pharmaceuticals', 500), ('pm_antibiotic_mass_production', 500)]:
        change(pm, dict(machinists=-value, engineers=value), chemistry)
    for pm in ['pm_electric_mine_ventilation', 'pm_electric_mine_ventilation_building_bauxite_mine']:
        change(pm, dict(laborers=-250, machinists=100, engineers=150))
    for pm in [SCI, SCI+'_automotive_industry', SCI+'_electrics_industry']:
        change(pm, dict(laborers=-500, clerks=250, engineers=250))

    clone('pm_aor1776_scientific_management_process', SCI,
          dict(machinists=-500, clerks=250, engineers=250))
    clone('pm_aor1776_scientific_management_chemical', SCI,
          dict(machinists=-500, clerks=250, engineers=250), chemistry)
    clone('pm_aor1776_scientific_management_power', SCI,
          dict(laborers=-200, machinists=-300, clerks=250, engineers=250))
    clone('pm_aor1776_rail_transport_chemical', 'pm_rail_transport_mine', dict(laborers=-1000), chemistry)
    for stem, profile, required in [
        ('watertube_boiler', dict(laborers=-500, machinists=-750, engineers=-250),
         ['pm_basic_smelting_process', 'pm_electric_arc_process_alloying']),
        ('rotary_valve_engine', dict(laborers=-500, machinists=-1000, engineers=-500),
         ['pm_electric_arc_process_alloying']),
        ('unit_electric_drive', dict(laborers=-500, machinists=-1250, engineers=-750),
         ['pm_electric_arc_process_alloying'])]:
        clone(f'pm_aor1776_{stem}_alloys', f'pm_{stem}_building_steel_mill', profile, required)
    for stem, profile, required in [
        ('rotary_valve_engine', dict(laborers=-1000, machinists=-1000),
         ['pm_cannons', 'pm_smoothbores', 'pm_breech_loaders', 'pm_recoiled_barrels']),
        ('assembly_lines', dict(laborers=-1000, machinists=-1000, engineers=-500),
         ['pm_breech_loaders', 'pm_recoiled_barrels'])]:
        clone(f'pm_aor1776_{stem}_artillery', f'pm_{stem}_building_arms_industry', profile, required)

    group_defs = {
        'pmg_aor1776_scientific_management_process': ('pmg_scientific_management',
            ['pm_no_scientific_management', 'pm_aor1776_scientific_management_process']),
        'pmg_aor1776_scientific_management_chemical': ('pmg_scientific_management',
            ['pm_no_scientific_management', 'pm_aor1776_scientific_management_chemical']),
        'pmg_aor1776_scientific_management_power': ('pmg_scientific_management',
            ['pm_no_scientific_management', 'pm_aor1776_scientific_management_power']),
        'pmg_aor1776_transport_chemical': ('pmg_aor1776_industrial_transport',
            ['pm_road_carts', 'pm_aor1776_rail_transport_chemical']),
        'pmg_aor1776_automation_alloys': ('pmg_automation_building_steel_mill',
            ['pm_automation_disabled'] + [f'pm_aor1776_{s}_alloys' for s in
             ['watertube_boiler', 'rotary_valve_engine', 'unit_electric_drive']]),
        'pmg_aor1776_automation_artillery': ('pmg_automation_building_arms_industry',
            ['pm_automation_disabled', 'pm_aor1776_rotary_valve_engine_artillery',
             'pm_aor1776_assembly_lines_artillery']),
    }
    building_changes = {
        'building_chemical_plant': {'pmg_scientific_management':'pmg_aor1776_scientific_management_chemical',
                                   'pmg_aor1776_industrial_transport':'pmg_aor1776_transport_chemical'},
        'building_explosives_factory': {'pmg_scientific_management':'pmg_aor1776_scientific_management_process'},
        'building_synthetics_plant': {'pmg_scientific_management':'pmg_aor1776_scientific_management_process'},
        'building_shipyard': {'pmg_scientific_management':'pmg_aor1776_scientific_management_process'},
        'building_power_plant': {'pmg_scientific_management':'pmg_aor1776_scientific_management_power'},
        'building_alloys_plant': {'pmg_automation_building_steel_mill':'pmg_aor1776_automation_alloys'},
        'building_artillery_foundry': {'pmg_automation_building_arms_industry':'pmg_aor1776_automation_artillery'},
    }
    file_changes = defaultdict(list)
    def profile_text(node, path, profile, required):
        text = a.raw(path)[node.start:node.end]
        newline = '\r\n' if '\r\n' in text else '\n'
        # All employment stats of the recipe sit in a single level_scaled block.
        block = next(b for parent in node.children('building_modifiers')
                     for b in parent.children('level_scaled')
                     if any(s.key.startswith('building_employment_') for s in b.children()))
        chunk = a.raw(path)[block.start:block.end]
        chunk = re.sub(r'(?m)^[\t ]*building_employment_\w+_add\s*=\s*-?\d+[^\r\n]*\r?\n', '', chunk)
        # Source blocks are multiline, including the two ventilation recipes.
        assert 'building_employment_' not in chunk, node.key
        lines = ''.join(f'\t\t\tbuilding_employment_{k}_add = {v}{newline}' for k,v in profile.items())
        chunk = chunk.replace('level_scaled = {'+newline, 'level_scaled = {'+newline+lines, 1)
        start, end = block.start-node.start, block.end-node.start
        text = text[:start]+chunk+text[end:]
        if required is not None:
            assert not node.children('unlocking_production_methods'), node.key
            dep = newline+'\tunlocking_production_methods = {'+newline + \
                  ''.join(f'\t\t{pm}{newline}' for pm in required)+'\t}'+newline
            opening = text.index('{')+1
            text = text[:opening]+newline+dep+text[opening:]
        return text

    for pm, (profile, required) in replacements.items():
        node, path = methods[pm]
        assert path.is_relative_to(ROOT), (pm, path)
        file_changes[path].append((node.start, node.end, profile_text(node, path, profile, required)))
    for key, changes in building_changes.items():
        node, path = buildings[key]
        text = a.raw(path)[node.start:node.end]
        for old,new in changes.items():
            assert len(re.findall(r'\b'+old+r'\b',text)) == 1
            text = re.sub(r'\b'+old+r'\b', new, text)
        file_changes[path].append((node.start,node.end,text))
    new_content = {}
    for path, changes in file_changes.items():
        content = a.raw(path)
        for start,end,text in sorted(changes,reverse=True):
            content = content[:start]+text+content[end:]
        bom = b'\xef\xbb\xbf' if path.read_bytes().startswith(b'\xef\xbb\xbf') else b''
        new_content[path] = bom + content.encode('utf-8')
    pm_text = '# Cumulative automation: employment profiles retain net headcount.\n\n'
    for new, (old, profile, required) in clones.items():
        node,path = methods[old]
        text = profile_text(node,path,profile,required)
        text = re.sub(r'^'+re.escape(old)+r'\b',new,text, count=1)
        pm_text += text.replace('\r\n','\n')+'\n\n'
    new_content[ROOT/NEW_PM] = pm_text.encode('utf-8')
    pmg_text = '# Sector profiles share icons, costs and technological gates.\n\n'
    for new,(old,choices) in group_defs.items():
        node,path = groups[old]
        text = a.raw(path)[node.start:node.end]
        block = node.children('production_methods')[0]
        text = text[:block.start-node.start] + 'production_methods = {\n'+ \
               ''.join('\t\t'+pm+'\n' for pm in choices)+'\t}' + text[block.end-node.start:]
        text = re.sub(r'^'+re.escape(old)+r'\b',new,text,count=1)
        pmg_text += text.replace('\r\n','\n')+'\n\n'
    new_content[ROOT/NEW_PMG] = pmg_text.encode('utf-8')
    aliases = {new:old for new,(old,*_) in clones.items()}
    aliases.update({new:old for new,(old,_) in group_defs.items()})
    for language in ['french','english']:
        loc = f'l_{language}:\n' + ''.join(f' {new}:0 "${old}$"\n' for new,old in aliases.items())
        new_content[ROOT/f'localization/{language}/1776_automation_employment_l_{language}.yml'] = \
            b'\xef\xbb\xbf'+loc.encode('utf-8')
    for catalog,folder in [(methods,'common/production_methods'),(groups,'common/production_method_groups'),
                           (buildings,'common/buildings')]:
        for path,content in new_content.items():
            if path.parent != ROOT/folder:continue
            for node in parse(content.decode('utf-8-sig')):
                if isinstance(node.value,list):catalog[node.key]=(node,path)
    after = audit(buildings,groups,methods)
    # Dependencies must resolve to alternatives on this same building.
    for key,(node,path) in buildings.items():
        available = {pm for g in a.ids(node,'production_method_groups')
                     for pm in a.ids(groups[g][0],'production_methods')}
        for pm in available:
            assert set(a.ids(methods[pm][0],'unlocking_production_methods')) <= available, (key,pm)
    return dict(content=new_content, replacements=replacements, clones=clones,
                groups=group_defs, building_changes=building_changes,
                before=before,after=after)


def write_json(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def validate_applied():
    baseline=json.loads((REPORT/'BASELINE.json').read_text(encoding='utf-8'))
    policy=json.loads((REPORT/'PLAN.json').read_text(encoding='utf-8'))
    catalogs={folder:a.catalog(folder) for folder in
              ['common/buildings','common/production_methods','common/production_method_groups']}
    old=deepcopy(catalogs)
    for folder,catalog in old.items():
        for key,(node,path) in list(catalog.items()):
            if path.is_relative_to(ROOT) and path.relative_to(ROOT).as_posix() in baseline['new']:
                del catalog[key]
        for rel in baseline['owned']:
            if str(Path(rel).parent).replace('\\','/') != folder:continue
            for node in parse(a.raw(REPORT/'baseline'/rel)):
                if isinstance(node.value,list):catalog[node.key]=(node,ROOT/rel)
    B,P,G=(catalogs[k] for k in ['common/buildings','common/production_methods','common/production_method_groups'])
    OB,OP,OG=(old[k] for k in ['common/buildings','common/production_methods','common/production_method_groups'])
    checks={}
    def check(name,result):checks[name]=bool(result)
    after=audit(B,G,P)
    before=audit(OB,OG,OP)
    check('same_131_buildings',set(B)==set(OB) and len(B)==131)
    check('before_audit_reproduced',before==json.loads((REPORT/'BEFORE.json').read_text(encoding='utf-8')))
    check('after_audit_reproduced',after==json.loads((REPORT/'AFTER.json').read_text(encoding='utf-8')))
    for row in after:
        check('all_professions_nonnegative.'+row['building'],not row['negative'])
        available={pm for g in row['groups'] for pm in a.ids(G[g][0],'production_methods')}
        for pm in available:
            required=set(a.ids(P[pm][0],'unlocking_production_methods'))
            check('dependencies_resolve_on_same_building.'+row['building']+'.'+pm,required<=available)
    def stripped(node):
        node=deepcopy(node)
        def clean(n):
            if not isinstance(n.value,list):return
            n.value[:]=[x for x in n.value if not (x.key.startswith('building_employment_') and x.key.endswith('_add'))
                        and x.key!='unlocking_production_methods']
            for x in n.value:clean(x)
        clean(node)
        node.key='recipe'
        return normalized([node])
    changes=[]
    weights={k:Decimal(n.one('wage_weight','0')) for k,(n,p) in a.catalog('common/pop_types').items()}
    for key,(_,path) in OP.items():
        new=P[key][0];previous=OP[key][0]
        check('existing_recipe_only_authorized_fields.'+key,stripped(new)==stripped(previous))
        check('net_headcount_preserved.'+key,sum(jobs(new).values())==sum(jobs(previous).values()))
        if key not in policy['recipes']:
            check('other_recipe_entirely_unchanged.'+key,normalized([new])==normalized([previous]))
    for new,(old_key,profile,required) in policy['clones'].items():
        check('variant_only_authorized_fields.'+new,stripped(P[new][0])==stripped(OP[old_key][0]))
        check('variant_net_headcount_preserved.'+new,sum(jobs(P[new][0]).values())==sum(jobs(OP[old_key][0]).values()))
    for new in list(policy['recipes'])+list(policy['clones']):
        old_key=policy['clones'][new][0] if new in policy['clones'] else new
        previous=jobs(OP[old_key][0]);current=jobs(P[new][0])
        changes.append(dict(method=new,source_recipe=old_key,before=previous,after=current,
             net_jobs_before=sum(previous.values()),net_jobs_after=sum(current.values()),
             wage_weight_delta=str(sum(Decimal(v)*weights[k] for k,v in current.items())-
                                   sum(Decimal(v)*weights[k] for k,v in previous.items())),
             requires_any_active_pm=a.ids(P[new][0],'unlocking_production_methods')))
    for key,(node,path) in B.items():
        restored=deepcopy(node)
        reverse={v:k for k,v in policy['buildings'].get(key,{}).items()}
        for block in restored.children('production_method_groups'):
            for item in block.children():item.value=reverse.get(item.value,item.value)
        check('building_only_authorized_groups.'+key,normalized([restored])==normalized([OB[key][0]]))
    for key,(node,path) in OG.items():
        check('existing_group_unchanged.'+key,normalized([node])==normalized([G[key][0]]))
    for new,(old_key,choices) in policy['groups'].items():
        node=deepcopy(G[new][0]);node.key=old_key
        node.children('production_methods')[0].value=deepcopy(OG[old_key][0].children('production_methods')[0].value)
        check('variant_group_same_other_fields.'+new,normalized([node])==normalized([OG[old_key][0]]))
        check('variant_group_exact_choices.'+new,a.ids(G[new][0],'production_methods')==choices)
    # Existing combinations still admitted by the new PM dependencies retain
    # exactly the same net total workforce, including every auxiliary PM.
    for row in after:
        for combo in itertools.product(*(a.ids(G[g][0],'production_methods') for g in row['groups'])):
            if not valid(combo,P):continue
            mapped=[policy['clones'].get(pm,[pm])[0] for pm in combo]
            assert sum(sum(jobs(P[pm][0]).values()) for pm in combo)==sum(sum(jobs(OP[pm][0]).values()) for pm in mapped)
    check(f'all_{sum(r["combinations"] for r in after)}_combinations_preserve_net_total_workforce',True)
    for lang in ['french','english']:
        path=ROOT/f'localization/{lang}/1776_automation_employment_l_{lang}.yml'
        content=path.read_bytes()
        check('localization_BOM.'+lang,content.startswith(b'\xef\xbb\xbf'))
        aliases=re.findall(r'^ (\w+):0 "\$(\w+)\$"$',content.decode('utf-8-sig'),re.M)
        local=entries(lang)
        native_local=entries(lang,root=a.GAME/'localization')
        check('localization_all_variants.'+lang,len(aliases)==len(policy['clones'])+len(policy['groups']) and
              len({k for k,v in aliases})==len(aliases))
        for key,source in aliases:
            check('localization_source_exists.'+lang+'.'+key,source in local or source in native_local)
            check('new_localization_key_unique.'+lang+'.'+key,len(local.get(key,[]))==1 and key not in native_local)
    check('all_protected_files_unchanged',all(a.sha(ROOT/r)==h for r,h in baseline['protected'].items()))
    check('canonical_vanilla_unchanged',all(a.sha(a.GAME/r)==h for r,h in baseline['native'].items()))
    check('git_head_branch_index_unchanged',a.git_state()==baseline['git'])
    write_json(REPORT/'EMPLOYMENT_CHANGES.json',changes)
    with (REPORT/'PROFESSION_MINIMA.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['building','profession','minimum_before','minimum_after'])
        writer.writeheader()
        old_rows={r['building']:r for r in before}
        for row in after:
            for profession,value in row['minima'].items():
                writer.writerow(dict(building=row['building'],profession=profession,minimum_after=value,
                         minimum_before=old_rows[row['building']]['minima'].get(profession,0)))
    result=dict(status='PASS_STATIC' if all(checks.values()) else 'FAIL',passed=sum(checks.values()),
                total=len(checks),failed=[k for k,v in checks.items() if not v],checks=checks,
                buildings=len(after),combinations=sum(r['combinations'] for r in after),
                protected_files=len(baseline['protected']),runtime='NOT_RUN')
    write_json(REPORT/'VALIDATION.json',result)
    print(json.dumps({k:v for k,v in result.items() if k!='checks'},ensure_ascii=False,indent=2))
    assert all(checks.values())


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--apply',action='store_true')
    parser.add_argument('--validate',action='store_true')
    args=parser.parse_args()
    if args.validate:
        validate_applied()
        return
    if (REPORT/'BASELINE.json').exists():
        assert not args.apply,'Never reapply this lot against its existing baseline.'
        rows=audit(a.catalog('common/buildings'),a.catalog('common/production_method_groups'),
                   a.catalog('common/production_methods'))
        print(json.dumps(dict(buildings=len(rows),combinations=sum(r['combinations'] for r in rows),
                              negative=[r for r in rows if r['negative']]),ensure_ascii=False,indent=2))
        return
    plan=build_plan()
    summary=dict(buildings=len(plan['after']),
                 combinations_before=sum(r['combinations'] for r in plan['before']),
                 combinations_after=sum(r['combinations'] for r in plan['after']),
                 negative_before=[r['building'] for r in plan['before'] if r['negative']],
                 negative_after=[r for r in plan['after'] if r['negative']],
                 modified_recipes=len(plan['replacements']),new_recipes=len(plan['clones']),
                 files=[p.relative_to(ROOT).as_posix() for p in plan['content']])
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    if not args.apply:return
    assert not summary['negative_after'], 'Refuse to apply an unsafe employment plan.'
    assert not (REPORT/'BASELINE.json').exists(), 'Never overwrite the original baseline.'
    REPORT.mkdir(parents=True,exist_ok=True)
    existing={p.relative_to(ROOT).as_posix():a.sha(p) for folder in
              ['common','events','gui','gfx','localization','map_data','history']
              for p in (ROOT/folder).rglob('*') if p.is_file()}
    native={str(p.relative_to(a.GAME)):a.sha(p) for folder in
            ['common/buildings','common/building_groups','common/production_methods','common/production_method_groups']
            for p in (a.GAME/folder).glob('*') if p.is_file()}
    owned={p.relative_to(ROOT).as_posix():a.sha(p) for p in plan['content'] if p.exists()}
    new=[p.relative_to(ROOT).as_posix() for p in plan['content'] if not p.exists()]
    for rel in owned:
        dest=REPORT/'baseline'/rel
        dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(ROOT/rel,dest)
    baseline=dict(utc=datetime.now(timezone.utc).isoformat(),git=a.git_state(),owned=owned,new=new,
                  protected={r:h for r,h in existing.items() if r not in owned},native=native)
    write_json(REPORT/'BASELINE.json',baseline)
    write_json(REPORT/'BEFORE.json',plan['before'])
    write_json(REPORT/'PLAN.json',dict(recipes=plan['replacements'],clones=plan['clones'],
               groups=plan['groups'],buildings=plan['building_changes']))
    for path,content in plan['content'].items():
        assert not path.exists() or a.sha(path)==owned[path.relative_to(ROOT).as_posix()]
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(content)
    actual=audit(a.catalog('common/buildings'),a.catalog('common/production_method_groups'),
                 a.catalog('common/production_methods'))
    assert actual==plan['after']
    write_json(REPORT/'AFTER.json',actual)
    # An on-disk re-read is deliberately independent of the simulated catalogs.
    assert not any(r['negative'] for r in actual)
    assert all(a.sha(ROOT/r)==h for r,h in baseline['protected'].items())
    assert all(a.sha(a.GAME/r)==h for r,h in native.items())
    assert a.git_state()==baseline['git']
    write_json(REPORT/'SUMMARY.json',summary)
    print('APPLIED; exhaustive on-disk employment audit passed; protected files, vanilla and Git unchanged.')


if __name__=='__main__':main()
