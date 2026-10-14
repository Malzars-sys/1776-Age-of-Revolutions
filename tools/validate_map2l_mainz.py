"""Exact differential QA for the Mainz/Palatinate core lot, not engine QA."""
import collections as C
import csv
import json
import re
import subprocess
import numpy as np
import validate_map2a as qa
import validate_diplomacy_ottoman_1776 as cw
from map2l_mainz import ROOT,OUT,REGIONS,dump
from map2l_belgium import packed,sha,components
from map2l_hre_work import GIT
from map2l_registry import active_registry_path,approved_lot_dirs,effective_assignments,ancestor_rgb,ownership_rows,migrate_extent
from validate_map2k_imperial import node,textnode,profiles

def validate():
    b=json.loads((OUT/'BASELINE.json').read_text());g=json.loads((OUT/'GEOMETRY.json').read_text());p=json.loads((OUT/'PLAN.json').read_text());m=json.loads((OUT/'REGISTRY_MIGRATION.json').read_text());a=qa.inventory();checks=[]
    lots=approved_lot_dirs();later=lots[lots.index(OUT)+1:]
    geos=[g]+[json.loads((fp/'GEOMETRY.json').read_text()) for fp in later]
    migrations=[m]+[json.loads((fp/'REGISTRY_MIGRATION.json').read_text()) for fp in later]
    plans=[p]+[json.loads((fp/'PLAN.json').read_text()) for fp in later]
    latest=later[-1] if later else OUT
    reviewed=effective_assignments(geos)
    regions=set().union(*(set(mi['replaced_regions']) for mi in migrations))
    def check(name,passed,detail=''):checks.append(dict(name=name,passed=bool(passed),detail=detail))
    check('World population exact',sum(r['count'] for r in a['pops'])==sum(r['count'] for r in b['inventory']['pops'])==835804980)
    check('Written and effective culture religion counts conserved',a['pops']==b['inventory']['pops'] and a['resolved_demographics']==b['inventory']['resolved_demographics'])
    check('All regional population attributes conserved',profiles(None,'pops')==profiles(b,'pops'))
    check('Building levels unchanged',a['building_levels_written']==b['inventory']['building_levels_written'])
    check('Building PMs weighted attributes and holders conserved',profiles(None,'buildings')==profiles(b,'buildings'))
    edited_buildings={rel for plan in plans for rel in plan['files'] if rel.startswith('common/history/buildings/')}
    check('All buildings outside explicit allocation files byte-identical',all(sha(ROOT/rel)==digest for rel,digest in b['hashes'].items() if rel.startswith('common/history/buildings/') and rel not in edited_buildings))
    check('Units formations and recruitment unchanged',a['units']==b['inventory']['units'])
    check('Country definitions capitals governments unchanged',a['countries']==b['inventory']['countries'] and all(sha(ROOT/rel)==digest for rel,digest in b['hashes'].items() if rel.startswith(('common/history/countries/','common/government_types/','common/laws/'))))
    check('No new duplicate owners',a['duplicates']==b['inventory']['duplicates'])
    check('No new state holder or province reference error',a['errors']==b['inventory']['errors'])
    expected=qa.counter(b['inventory']['owners'])
    for mi in migrations:
        for r in ownership_rows(mi,'previous'):expected[(r['rgb'],r['state'],r['beneficiary'])]-=1
        for r in ownership_rows(mi,'updated'):expected[(r['rgb'],r['state'],r['beneficiary'])]+=1
    check('Exact reviewed ownership with no other transfer',+expected==qa.counter(a['owners']))
    for sid in ['STATE_HESSE','STATE_FRANCONIA']:check('KMZ owns valid subdivision '+sid,[sid,'KMZ'] in a['states'])
    expected_pop=qa.counter(b['inventory']['regional_pop']);moved=C.Counter();rows=[]
    for alloc in [r for plan in plans for r in plan['allocations']]:
        check('Integer allocation conserved '+alloc['state']+' '+alloc['profile']+' '+alloc['kind'],sum(alloc['after'].values())==alloc['before'])
        if alloc['kind']!='population':continue
        culture,religion=alloc['profile'].split('/');religion='DEFAULT:'+culture if religion=='DEFAULT' else religion
        expected_pop[(alloc['state'],alloc['source'],culture,religion)]-=alloc['before']
        for tag,count in alloc['after'].items():
            expected_pop[(alloc['state'],tag,culture,religion)]+=count
            if tag!=alloc['source']:moved[alloc['state']+'/'+tag]+=count
        rows.append(dict(State=alloc['state'],Source=alloc['source'],Profile=alloc['profile'],Before=alloc['before'],After_Total=sum(alloc['after'].values()),Transferred=sum(v for t,v in alloc['after'].items() if t!=alloc['source'])))
    check('Population moves match every reviewed allocation exactly',+expected_pop==qa.counter(a['regional_pop']))
    with (OUT/'POPULATION_VALIDATION.csv').open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    old=packed(ROOT/b['bitmap_backup']);bmp=packed(ROOT/'map_data/provinces.png');delta=old!=bmp
    check('Lot baseline backup immutable',sha(ROOT/b['bitmap_backup'])==b['bitmap_sha256'])
    check('Live raster equals latest reviewed candidate',sha(ROOT/'map_data/provinces.png')==geos[-1]['candidate_sha256'])
    check('Dimensions exact',bmp.shape==old.shape==(3616,8192))
    oldcolors=set(np.unique(old).tolist());colors=set(np.unique(bmp).tolist())
    parents={ancestor_rgb(r,oldcolors) for geo in geos for r in geo['parents']}
    check('Only explicitly approved parent masks altered',set(np.unique(old[delta]).tolist())<=parents)
    new={int(r['rgb'][1:],16):r for geo in geos for r in geo['new_provinces']}
    check('Exact new RGB set and no original deleted',colors-oldcolors==set(new) and oldcolors<=colors)
    for color,r in new.items():check('Child remains wholly within declared ancestor '+r['rgb'],np.all(old[bmp==color]==ancestor_rgb(r['parent_rgb'],oldcolors)))
    for r in reviewed:
        color=int(r['rgb'][1:],16);mask=bmp==color
        check('Exact traced cells '+r['rgb'],int(mask.sum())==r['pixels'] and all(bmp[y,x]==color for x,y in r['cells']))
        check('Four-connected RGB '+r['rgb'],len(components(mask))==1)
        check('Unique valid state and controller '+r['rgb'],a['geometry'][r['rgb']]==r['state'] and qa.counter(a['owners'])[(r['rgb'],r['state'],r['owner'])]==1)
    anchors=json.loads((OUT.parent/'RHINE_CENTRAL/NATIVE_ANCHORS.json').read_text())
    for r in anchors:
        x,y=int(float(r['Locator_X'])),int(float(r['Locator_Y']))
        check('Native locator raster unchanged '+r['Hub_Name'],bmp[y,x]==old[y,x])
    # Province lists are the only state-region definition changes permitted.
    region_file=globals().get('REGION_FILE','map_data/state_regions/00_west_europe.txt')
    oldnodes=cw.parse(b['originals'][region_file]);newnodes=cw.parse((ROOT/region_file).read_text(encoding='utf-8-sig'))
    def protected(ns):return {n.key:[qa.norm(v) for v in n.children() if n.key not in regions or v.key!='provinces'] for n in ns}
    check('State IDs hubs resources and all unrelated definitions unchanged',protected(oldnodes)==protected(newnodes))
    terrain=(ROOT/'map_data/province_terrains.txt').read_text(encoding='utf-8-sig');tmap={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',terrain)}
    check('Terrain equals latest reviewed candidate',(ROOT/'map_data/province_terrains.txt').read_bytes()==(latest/'province_terrains_candidate.txt').read_bytes())
    check('Children inherit exact parent terrains',all(tmap[r['rgb'].upper()]==tmap[r['parent_rgb'].upper()] for r in new.values()))
    rights=json.loads(active_registry_path().read_text());lookup={r['rgb']:r for r in rights}
    expected_rights=b['registry']
    for mi in migrations:
        check('Migration input matches prior registry '+mi['geometry'],sorted([r for r in expected_rights if r['state'] in mi['replaced_regions']],key=lambda r:r['rgb'])==sorted(mi['previous'],key=lambda r:r['rgb']))
        expected_rights=[r for r in expected_rights if r['state'] not in mi['replaced_regions']]+mi['updated']
    expected_rights=sorted(expected_rights,key=lambda r:(r['rgb'],r['state'],r['beneficiary']))
    check('Exact ordered migrations and unique registered RGBs',rights==expected_rights and len(rights)==len(lookup)==len(b['registry'])+sum(len(mi['updated'])-len(mi['previous']) for mi in migrations))
    check('All rights outside explicit regions untouched',all(lookup[r['rgb']]==r for r in b['registry'] if r['state'] not in regions))
    check('Reviewed registered rights match controllers',all(lookup[r['rgb']]['beneficiary']==r['owner'] and lookup[r['rgb']]['state']==r['state'] for r in reviewed if r['rgb'] in lookup))
    oldmask=np.isin(old,[int(r['rgb'][1:],16) for r in b['registry']])
    check('Yellow extent changes only by declared exact cells',np.array_equal(migrate_extent(oldmask,migrations),np.isin(bmp,[int(r['rgb'][1:],16) for r in rights])))
    effective=effective_assignments([json.loads((fp/'GEOMETRY.json').read_text()) for fp in approved_lot_dirs()])
    check('All preceding effective geometry exact',all(int((bmp==int(r['rgb'][1:],16)).sum())==r['pixels'] and all(bmp[y,x]==int(r['rgb'][1:],16) for x,y in r['cells']) for r in effective))
    import map2k_imperial_system as compiler
    compiler.OUT=OUT
    for rel,raw in compiler.compile_system().items():
        check('Compiler matches '+rel,(ROOT/rel).read_text(encoding='utf-8-sig')==raw.lstrip('\ufeff'))
        if rel.endswith('.txt'):cw.parse(raw)
    for rel in p['files']:
        if rel.endswith('.txt'):cw.parse((ROOT/rel).read_text(encoding='utf-8-sig'))
    allowed=set(p['files'])|set(json.loads((OUT/'IMPERIAL_FILES.json').read_text())['files'])|{'map_data/provinces.png','map_data/province_terrains.txt','gfx/interface/journal_entries/aor1776_hre_registered_map.dds','gfx/map/map_painting/aor1776_hre_mask.dds','gfx/map/map_painting/aor1776_hre_sentinel.dds'}
    for fp,plan in zip(later,plans[1:]):allowed.update(plan['files']);allowed.update(json.loads((fp/'IMPERIAL_FILES.json').read_text())['files'])
    changed=[rel for rel,digest in b['hashes'].items() if sha(ROOT/rel)!=digest]
    check('Only scoped runtime files altered',set(changed)<=allowed,str(sorted(set(changed)-allowed)))
    current={path.relative_to(ROOT).as_posix() for folder in ['common','map_data','gui','gfx/FX','gfx/map','localization','events'] for path in (ROOT/folder).rglob('*') if path.is_file()}
    check('No unexpected new runtime files',current-set(b['hashes'])<=allowed)
    check('Git HEAD and index unchanged',subprocess.check_output([GIT,'rev-parse','HEAD'],cwd=ROOT,text=True).strip()==b['git_head'] and sha(ROOT/'.git/index')==b['git_index_sha256'])
    for module,func,args in [('validate_map2k_feedback','validate_feedback',[rights]),('validate_map2k_reforms','validate_reforms',[]),('validate_map2k_repairs','validate_repairs',[rights]),('validate_map2k_dashboard','validate_dashboard',[]),('validate_map2k_demand_feedback','validate_demand_feedback',[]),('validate_map2k_atlas_access','validate_atlas_access',[]),('validate_map2k_electoral_choices','validate_electoral_choices',[])]:getattr(__import__(module),func)(check,node,textnode,*args)
    main=json.loads((latest/'MAIN_MAP/VALIDATION.json').read_text())
    check('Main map offline checks pass for current registry',main['registry_sha256']==sha(active_registry_path()) and main['province_RGBs']==len(rights) and all(r['passed'] for r in main['checks']))
    align=json.loads((OUT/'ALIGNMENT.json').read_text());cfg=json.loads((OUT/'TRACING.json').read_text())
    if cfg.get('calibrated_sources'):
        check('Conserved calibrated map sources unchanged',all(sha(OUT/r['path'])==r['sha256'] for r in align['sources']))
        check('Candidate belongs to exact reviewed tracing',g['tracing_sha256']==sha(OUT/'TRACING.json'))
        if 'CALIBRATION_CHECK' in globals():CALIBRATION_CHECK(check,OUT,a,b,align,cfg,p)
        else:
            from validate_map2l_mainz_estates import validate_calibration
            validate_calibration(check,OUT,a,b,align,cfg,p)
        if cfg.get('southern_controls'):
            from validate_map2l_mainz_completion import validate_southern_controls
            validate_southern_controls(check,OUT,a,b,align,cfg)
    else:
        check('Conserved map sources unchanged',sha(OUT/cfg['source'])==align['source_sha256'] and sha(OUT/cfg['cross_source'])==align['cross_source_sha256'])
    report=dict(status='PASS_STATIC_ENGINE_DEFERRED' if all(r['passed'] for r in checks) else 'FAIL',checks=checks,
        engine_tested=False,engine_test_policy='After all HRE lots, per user',new_RGBs=len(g['new_provinces']),cumulative_new_RGBs=len(new),registered_RGBs=len(rights),
        transferred_population=dict(moved),territorial_transfers=g['transfers'],changed_pixels=int(delta.sum()),runtime_changed_files=changed,
        inherited_reference_errors=a['errors'],inherited_duplicate_RGBs=a['duplicates'],limitations=g['limitations'])
    dump('VALIDATION.json',report)
    print(report['status'],sum(r['passed'] for r in checks),'/',len(checks),'checks;',dict(moved))
    for r in checks:
        if not r['passed']:print('FAIL',r['name'],r['detail'])
    return 0 if all(r['passed'] for r in checks) else 1

if __name__=='__main__':raise SystemExit(validate())
