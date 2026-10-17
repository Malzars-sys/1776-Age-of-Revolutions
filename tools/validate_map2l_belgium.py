"""Differential Belgian territorial and HRE regression checks, not engine QA."""
import collections as C
import json
import re
import sys
import numpy as np
from PIL import Image
import validate_map2a as qa
import validate_diplomacy_ottoman_1776 as cw
from map_1776_audit import effective,values
from map2l_belgium import ROOT,OUT,LOT,REGIONS,TAGS,packed,sha
from map2l_registry import active_registry_path,approved_territorial_extensions,approved_territorial_migrations,apply_territorial_migrations,approved_lot_dirs,effective_assignments,ancestor_rgb,ownership_rows,migrate_extent,expected_country_definitions
from validate_map2k_imperial import node,textnode,profiles


def validate():
    base=json.loads((OUT/'BASELINE.json').read_text(encoding='utf-8'))
    geo=json.loads((LOT/'GEOMETRY.json').read_text(encoding='utf-8'))
    plan=json.loads((LOT/'PLAN.json').read_text(encoding='utf-8'))
    integration=json.loads((LOT/'IMPERIAL_FILES.json').read_text(encoding='utf-8'))
    migrations=approved_territorial_migrations()
    later_dirs=approved_lot_dirs()
    later_geos=[json.loads((p/'GEOMETRY.json').read_text(encoding='utf-8')) for p in later_dirs]
    later_geo=later_geos[-1] if later_geos else None
    migrated_regions={s for m in migrations for s in m['replaced_regions']}
    inv=qa.inventory();before=base['inventory'];checks=[]
    def check(name,passed,detail=''):
        checks.append(dict(name=name,passed=bool(passed),detail=detail))
    check('Exact world population',sum(r['count'] for r in inv['pops'])==sum(r['count'] for r in before['pops'])==835804980)
    check('Every culture and religion count preserved',inv['pops']==before['pops'] and inv['resolved_demographics']==before['resolved_demographics'])
    check('All population attributes preserved within each economic region',profiles(None,'pops')==profiles(base,'pops'))
    check('Every building level preserved',inv['building_levels_written']==before['building_levels_written'])
    check('Every building PM, reserve and other attribute preserved weighted by levels',profiles(None,'buildings')==profiles(base,'buildings'))
    check('Armies, navies, formations and recruitment unchanged',inv['units']==before['units'])
    check('No new broken state or economic holder references',not [r for r in inv['errors'] if r not in before['errors']],str(inv['errors']))
    check('No new multiply assigned province',inv['duplicates']==before['duplicates'])
    expected=qa.counter(before['owners'])
    for r in before['owners']:
        if r['key'][1] in REGIONS:expected[tuple(r['key'])]-=r['count']
    for r in geo['assignments']:expected[(r['rgb'],r['state'],r['owner'])]+=1
    for m in migrations:
        for r in ownership_rows(m,'previous'):expected[(r['rgb'],r['state'],r['beneficiary'])]-=1
        for r in ownership_rows(m,'updated'):expected[(r['rgb'],r['state'],r['beneficiary'])]+=1
    check('Exact reviewed province owners; all other owners untouched',+expected==qa.counter(inv['owners']))
    approved_tags=set(TAGS)|{t for m in migrations for t in m['new_members']}
    check('Exactly reviewed new countries, including later approved estates',set(inv['countries'])-set(before['countries'])==approved_tags and set(before['countries'])<=set(inv['countries']))
    check('Both capitals lie in an owned state',all(['STATE_WALLONIA',tag] in inv['states'] for tag in TAGS))
    expected_definitions=expected_country_definitions(before['countries'],migrations)
    check('Pre-existing definitions preserved except exact reviewed WUR tier',all(inv['countries'][t]==expected_definitions[t] for t in before['countries']))
    bmp=packed(ROOT/'map_data/provinces.png');oldbmp=packed(OUT/'SOURCE/provinces_before.png')
    check('Original bitmap backup still exact',sha(OUT/'SOURCE/provinces_before.png')==base['bitmap_sha256'])
    check('Live bitmap is the latest reviewed candidate',sha(ROOT/'map_data/provinces.png')==(later_geo or geo)['candidate_sha256'])
    check('World dimensions unchanged',bmp.shape==oldbmp.shape==(3616,8192))
    reviewed_children=geo['new_provinces']+[r for g in later_geos for r in g['new_provinces']]
    new={int(r['rgb'][1:],16):r for r in reviewed_children}
    old_colors=set(np.unique(oldbmp).tolist());current_colors=set(np.unique(bmp).tolist())
    check('37 Belgian new colours plus reviewed later splits; no old colour removed',current_colors-old_colors==set(new) and old_colors<=current_colors and len(geo['new_provinces'])==37)
    allowed_colors={int(r['key'][0][1:],16) for r in before['owners'] if r['key'][1] in set(REGIONS)|migrated_regions}
    delta=oldbmp!=bmp
    check('No changed pixel outside Belgian and explicitly approved later lot',set(np.unique(oldbmp[delta]).tolist())<=allowed_colors)
    check('Every new colour remains inside its declared ancestor province',all(np.all(oldbmp[bmp==rgb]==ancestor_rgb(r['parent_rgb'],old_colors)) for rgb,r in new.items()))
    assignments=effective_assignments([geo]+later_geos)
    check('Province areas and shapes match all reviewed cells',all(int(np.count_nonzero(bmp==int(r['rgb'][1:],16)))==r['pixels'] and all(int(bmp[y,x])==int(r['rgb'][1:],16) for x,y in r['cells']) for r in assignments))
    check('No enclave enlarged for visibility','dilation' not in geo and geo['status']=='GAME_RESOLUTION_APPROXIMATION_NOT_CADASTRAL')
    check('Liège city locator remains in Liège',next(r for r in geo['assignments'] if r['rgb']=='xEF2040')['owner']=='LGE' and bmp[839,4223]==int('EF2040',16))
    check('Stavelot is twenty pixels, not artificially inflated',sum(r['pixels'] for r in geo['assignments'] if r['owner']=='STM')==20)
    oldterrain=(qa.GAME/'map_data/province_terrains.txt').read_text(encoding='utf-8-sig')
    terrain=(ROOT/'map_data/province_terrains.txt').read_text(encoding='utf-8-sig')
    terrain_map=lambda text:{k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',text)}
    ot,nt=terrain_map(oldterrain),terrain_map(terrain)
    check('All original province terrains unchanged',all(nt[k]==v for k,v in ot.items()))
    check('Every child inherits its exact parent terrain',all(nt[r['rgb'].upper()]==ot[r['parent_rgb'].upper()] for r in geo['new_provinces']))
    ledger=json.loads(active_registry_path().read_text(encoding='utf-8'));rights={r['rgb']:r for r in ledger}
    extensions=approved_territorial_extensions()
    initial=[r for r in base['de_jure_registry'] if r['state'] not in REGIONS]+[dict(rgb=r['rgb'],state=r['state'],beneficiary=r['owner'],basis='MAP2L Belgian lot: source-traced game-scale approximation; see BELGIUM/GEOMETRY.json') for r in geo['assignments']]
    expected_rights=apply_territorial_migrations(initial+extensions);expected_count=len(expected_rights)
    check('Old MAP2K register remains immutable',sha(ROOT/'docs/reports/map/MAP2K/IMPERIAL_DE_JURE_REGISTRY.json')==base['registry_sha256'])
    check('Active register matches every reviewed Belgian right, extension and migration',ledger==expected_rights and len(ledger)==len(rights)==expected_count)
    check('Every Belgian right belongs to its reviewed polity',all(rights[r['rgb']]['beneficiary']==r['owner'] and rights[r['rgb']]['state']==r['state'] for r in geo['assignments']))
    outside=[r for r in base['de_jure_registry'] if r['state'] not in REGIONS]
    check('Every imperial right outside approved migrations untouched',all(rights[r['rgb']]==r for r in outside if r['state'] not in migrated_regions))
    oldmask=np.isin(oldbmp,[int(r['rgb'][1:],16) for r in base['de_jure_registry']])
    newmask=np.isin(bmp,[int(r['rgb'][1:],16) for r in ledger])
    extended_mask=oldmask|np.isin(bmp,[int(r['rgb'][1:],16) for r in extensions])
    check('Exact Belgian extent and explicit approved extensions/deltas only',np.array_equal(migrate_extent(extended_mask,migrations),newmask))
    from map2k_imperial_system import compile_system,MEMBERS
    compiled=compile_system()
    for rel,raw in compiled.items():check('Compiler matches runtime: '+rel,(ROOT/rel).read_text(encoding='utf-8-sig')==raw.lstrip('\ufeff'))
    check('Liège and Stavelot are recognised imperial estates',set(TAGS)<=set(MEMBERS) and all('c:'+t in textnode(node('common/scripted_triggers/1776_imperial_constitution.txt','aor1776_hre_member')) for t in TAGS))
    bloc=next(n for n in cw.walk(cw.parse((ROOT/'common/history/power_blocs/00_power_blocs.txt').read_text(encoding='utf-8-sig'))) if n.key=='c:AUS')
    members=[cw.scalar(n.value) for n in cw.walk(bloc.children()) if n.key=='member']
    check('Both estates join the starting bloc exactly once',all(members.count('c:'+t)==1 for t in TAGS))
    dip=[p for p in base['hashes'] if p.startswith('common/history/diplomacy/') or p.startswith('common/history/treaties/')]
    check('Historical dependencies and treaties unchanged',all(sha(ROOT/p)==base['hashes'][p] for p in dip))
    check('No new historical subjection to Austria',all('c:'+t not in (ROOT/p).read_text(encoding='utf-8-sig') for p in dip for t in TAGS))
    returns=node('common/scripted_effects/1776_imperial_constitution.txt','aor1776_hre_return_requested_provinces')
    commands=[n for n in cw.walk(returns.children()) if n.key=='set_owner_of_provinces']
    got={(values(n,'provinces')[0],cw.scalar(n.one('country')).removeprefix('c:')) for n in commands}
    check('Restitution returns every province to its own rightful holder',got=={(r['rgb'],r['beneficiary']) for r in ledger} and len(commands)==expected_count)
    for lang in ['french','english']:
        p=ROOT/f'localization/{lang}/1776_map2l_belgian_estates_l_{lang}.yml';raw=p.read_text(encoding='utf-8-sig')
        check('New country names and rulers localized: '+lang,p.read_bytes().startswith(b'\xef\xbb\xbf') and all(' '+key+':0 ' in raw for key in [*TAGS,*[t+'_ADJ' for t in TAGS],'aor1776_lge_francois_charles','aor1776_lge_velbruck','aor1776_stm_jacques','aor1776_stm_hubin']))
    allowed=set(plan['files'])|set(integration['files'])|{'map_data/provinces.png','gfx/interface/journal_entries/aor1776_hre_registered_map.dds','gfx/map/map_painting/aor1776_hre_mask.dds','gfx/map/map_painting/aor1776_hre_sentinel.dds'}
    for lot in later_dirs:
        allowed|=set(json.loads((lot/'PLAN.json').read_text())['files'])|set(json.loads((lot/'IMPERIAL_FILES.json').read_text())['files'])|{'map_data/province_terrains.txt'}
    changed=[p for p,h in base['hashes'].items() if not (ROOT/p).exists() or sha(ROOT/p)!=h]
    check('No unrelated protected runtime file changed',set(changed)<=allowed,str(sorted(set(changed)-allowed)))
    reviewed_regions=set(REGIONS)|migrated_regions
    check('No unrelated region definitions changed',[qa.norm(n) for n in cw.parse(base['originals']['map_data/state_regions/00_west_europe.txt']) if n.key not in reviewed_regions]==[qa.norm(n) for n in cw.parse((ROOT/'map_data/state_regions/00_west_europe.txt').read_text(encoding='utf-8-sig')) if n.key not in reviewed_regions])
    for module,func,args in [('validate_map2k_feedback','validate_feedback',[ledger]),('validate_map2k_reforms','validate_reforms',[]),('validate_map2k_repairs','validate_repairs',[ledger]),('validate_map2k_dashboard','validate_dashboard',[]),('validate_map2k_demand_feedback','validate_demand_feedback',[]),('validate_map2k_atlas_access','validate_atlas_access',[]),('validate_map2k_electoral_choices','validate_electoral_choices',[])]:
        getattr(__import__(module),func)(check,node,textnode,*args)
    mapreport=later_dirs[-1]/'MAIN_MAP/VALIDATION.json' if migrations else OUT/'PIEDMONT/MAIN_MAP/VALIDATION.json' if extensions else LOT/'MAIN_MAP/VALIDATION.json'
    mapcheck=json.loads(mapreport.read_text(encoding='utf-8'))
    check('Native yellow map has passed all offline checks',all(r['passed'] for r in mapcheck['checks']) and mapcheck['province_RGBs']==expected_count)
    import subprocess
    from map2l_hre_work import GIT
    check('No commit or staging mutation',subprocess.check_output([GIT,'rev-parse','HEAD'],cwd=ROOT,text=True).strip()==base['git_head'] and sha(ROOT/'.git/index')==base['git_index_sha256'])
    report=dict(status='PASS_STATIC_ENGINE_PENDING' if all(r['passed'] for r in checks) else 'FAIL',checks=checks,
        world_population=835804980,new_countries=TAGS,new_RGBs=37,changed_pixels=int(delta.sum()),
        engine_tested=False,geometry_status=geo['status'],limitations=geo['limitations'],
        applied_scope='Belgian territorial lot preserved; explicit Piedmont extension and ordered reviewed Franconia/Neckar migrations allowed. No other regional change allowed.',
        approved_territorial_extensions=extensions,
        approved_territorial_migrations=migrations,
        changed_protected_files=changed)
    from map2l_runtime_receipt import annotate
    annotate(report,LOT)
    (LOT/'VALIDATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(report['status'],len(checks),'checks;',report['changed_pixels'],'changed pixels')
    for row in checks:
        if not row['passed']:print('FAIL',row['name'],row['detail'])
    return 0 if report['status'].startswith('PASS') else 1


if __name__=='__main__':raise SystemExit(validate())
