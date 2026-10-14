"""Differential QA for the limited Neckar lot. No engine test is performed."""
import collections as C
import json
import re
import subprocess
import numpy as np
import validate_map2a as qa
import validate_diplomacy_ottoman_1776 as cw
from map2l_rhine import ROOT, OUT
from map2l_belgium import packed, sha, components
from map2l_hre_work import GIT
from map2l_registry import active_registry_path, apply_territorial_migrations, approved_lot_dirs,effective_assignments,ancestor_rgb,ownership_rows,migrate_extent
from validate_map2k_imperial import node, textnode, profiles


def validate():
    b=json.loads((OUT/'BASELINE.json').read_text());g=json.loads((OUT/'GEOMETRY.json').read_text());p=json.loads((OUT/'PLAN.json').read_text());m=json.loads((OUT/'REGISTRY_MIGRATION.json').read_text());a=qa.inventory();checks=[]
    later_dirs=approved_lot_dirs()[2:]
    later_geos=[json.loads((fp/'GEOMETRY.json').read_text()) for fp in later_dirs]
    later_migrations=[json.loads((fp/'REGISTRY_MIGRATION.json').read_text()) for fp in later_dirs]
    latest=later_dirs[-1] if later_dirs else OUT
    def check(name,passed,detail=''):checks.append(dict(name=name,passed=bool(passed),detail=detail))
    check('World population preserved',sum(r['count'] for r in a['pops'])==sum(r['count'] for r in b['inventory']['pops'])==835804980)
    check('All cultures religions and resolved demographics preserved',a['pops']==b['inventory']['pops'] and a['resolved_demographics']==b['inventory']['resolved_demographics'])
    check('Regional demographic profiles preserved',profiles(None,'pops')==profiles(b,'pops'))
    check('Building levels preserved',a['building_levels_written']==b['inventory']['building_levels_written'])
    check('Building PMs and weighted attributes preserved',profiles(None,'buildings')==profiles(b,'buildings'))
    check('Armies navies formations recruitment unchanged',a['units']==b['inventory']['units'])
    check('Every country definition and capital unchanged',a['countries']==b['inventory']['countries'])
    check('No new reference errors',a['errors']==b['inventory']['errors'],str(a['errors']))
    check('No new duplicate ownership',a['duplicates']==b['inventory']['duplicates'])
    expected=qa.counter(b['inventory']['owners'])
    for r in m['previous']:expected[(r['rgb'],r['state'],r['beneficiary'])]-=1
    for r in m['updated']:expected[(r['rgb'],r['state'],r['beneficiary'])]+=1
    for migration in later_migrations:
        for r in ownership_rows(migration,'previous'):expected[(r['rgb'],r['state'],r['beneficiary'])]-=1
        for r in ownership_rows(migration,'updated'):expected[(r['rgb'],r['state'],r['beneficiary'])]+=1
    check('Exact reviewed owners and no other transfer',+expected==qa.counter(a['owners']))
    check('KPF KMZ and BAD each own Baden subdivision',all(['STATE_BADEN',tag] in a['states'] for tag in ['KPF','KMZ','BAD']))
    old=packed(ROOT/b['bitmap_backup']);bmp=packed(ROOT/'map_data/provinces.png');delta=bmp!=old
    check('Pre-Neckar bitmap backup immutable',sha(ROOT/b['bitmap_backup'])==b['bitmap_sha256'])
    check('Applied bitmap equals latest reviewed candidate',sha(ROOT/'map_data/provinces.png')==(later_geos[-1] if later_geos else g)['candidate_sha256'])
    check('Same world dimensions',bmp.shape==old.shape==(3616,8192))
    parents={int(r[1:],16) for r in g['parents']};new={int(r['rgb'][1:],16):r for r in g['new_provinces']}
    all_parents=parents|{ancestor_rgb(r,set(np.unique(old).tolist())) for geo in later_geos for r in geo['parents']}
    all_new=set(new)|{int(r['rgb'][1:],16) for geo in later_geos for r in geo['new_provinces']}
    check('Only Neckar and explicitly reviewed later parents altered',set(np.unique(old[delta]).tolist())<=all_parents)
    check('Four Neckar colors plus explicit later children; no original removed',set(np.unique(bmp).tolist())-set(np.unique(old).tolist())==all_new and len(new)==4 and set(np.unique(old).tolist())<=set(np.unique(bmp).tolist()))
    for rgb,row in new.items():check('Child wholly inside parent '+row['rgb'],np.all(old[bmp==rgb]==int(row['parent_rgb'][1:],16)))
    reviewed=effective_assignments([g]+later_geos)
    for r in reviewed:
        rgb=int(r['rgb'][1:],16);mask=bmp==rgb
        check('Exact reviewed cells '+r['rgb'],int(mask.sum())==r['pixels'] and all(bmp[y,x]==rgb for x,y in r['cells']))
        check('Four-connected province '+r['rgb'],len(components(mask))==1)
        check('Province reference resolves '+r['rgb'],a['geometry'][r['rgb']]==r['state'])
    check('Native Heidelberg hub retained in KPF RGB',int(bmp[887,4290])==int('E0A2B9',16) and next(r for r in g['assignments'] if r['rgb']=='xE0A2B9')['owner']=='KPF')
    terrain=(ROOT/'map_data/province_terrains.txt').read_text(encoding='utf-8-sig');tmap={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',terrain)}
    check('Children inherit parent terrains',all(tmap[r['rgb'].upper()]==tmap[r['parent_rgb'].upper()] for r in g['new_provinces']))
    check('Applied terrain equals latest reviewed candidate',(ROOT/'map_data/province_terrains.txt').read_bytes()==(latest/'province_terrains_candidate.txt').read_bytes())
    ledger=json.loads(active_registry_path().read_text());rights={r['rgb']:r for r in ledger}
    check('363 Neckar rights plus exact later registered deltas',len(ledger)==len(rights)==363+sum(len(mi['updated'])-len(mi['previous']) for mi in later_migrations))
    expected_ledger=sorted([r for r in b['registry'] if r['state']!='STATE_BADEN']+m['updated'],key=lambda r:(r['rgb'],r['state'],r['beneficiary']))
    for migration in later_migrations:
        regions=set(migration['replaced_regions'])
        assert sorted([r for r in expected_ledger if r['state'] in regions],key=lambda r:r['rgb'])==sorted(migration['previous'],key=lambda r:r['rgb'])
        expected_ledger=sorted([r for r in expected_ledger if r['state'] not in regions]+migration['updated'],key=lambda r:(r['rgb'],r['state'],r['beneficiary']))
    check('Exact next register migration',ledger==expected_ledger)
    later_regions={sid for migration in later_migrations for sid in migration['replaced_regions']}
    check('Other rights outside exact later migrations unchanged',all(rights[r['rgb']]==r for r in b['registry'] if r['state'] not in {'STATE_BADEN',*later_regions}))
    check('Yellow extent changes only by declared cells',np.array_equal(migrate_extent(np.isin(old,[int(r['rgb'][1:],16) for r in b['registry']]),later_migrations),np.isin(bmp,[int(r['rgb'][1:],16) for r in ledger])))
    check('Registered province right matches effective controller',all(rights[r['rgb']]['beneficiary']==r['owner'] for r in reviewed if r['rgb'] in rights))
    from map2k_imperial_system import compile_system
    import map2k_imperial_system as compiler
    compiler.OUT=OUT
    for rel,raw in compile_system().items():
        check('Compiler matches '+rel,(ROOT/rel).read_text(encoding='utf-8-sig')==raw.lstrip('\ufeff'))
        if rel.endswith('.txt'):cw.parse(raw)
    for rel in p['files']:
        if rel.endswith('.txt'):cw.parse((ROOT/rel).read_text(encoding='utf-8-sig'))
    allowed=set(p['files'])|set(json.loads((OUT/'IMPERIAL_FILES.json').read_text())['files'])|{'map_data/provinces.png','map_data/province_terrains.txt','gfx/interface/journal_entries/aor1776_hre_registered_map.dds','gfx/map/map_painting/aor1776_hre_mask.dds','gfx/map/map_painting/aor1776_hre_sentinel.dds'}
    for fp in later_dirs:allowed|=set(json.loads((fp/'PLAN.json').read_text())['files'])|set(json.loads((fp/'IMPERIAL_FILES.json').read_text())['files'])
    changed=[rel for rel,h in b['hashes'].items() if sha(ROOT/rel)!=h]
    check('Only scoped runtime files changed',set(changed)<=allowed,str(sorted(set(changed)-allowed)))
    current_files={path.relative_to(ROOT).as_posix() for folder in ['common','map_data','gui','gfx/FX','gfx/map','localization','events'] for path in (ROOT/folder).rglob('*') if path.is_file()}
    check('No unexpected new runtime files',current_files-set(b['hashes'])<=allowed)
    check('HEAD and Git index unchanged',subprocess.check_output([GIT,'rev-parse','HEAD'],cwd=ROOT,text=True).strip()==b['git_head'] and sha(ROOT/'.git/index')==b['git_index_sha256'])
    for module,func,args in [('validate_map2k_feedback','validate_feedback',[ledger]),('validate_map2k_reforms','validate_reforms',[]),('validate_map2k_repairs','validate_repairs',[ledger]),('validate_map2k_dashboard','validate_dashboard',[]),('validate_map2k_demand_feedback','validate_demand_feedback',[]),('validate_map2k_atlas_access','validate_atlas_access',[]),('validate_map2k_electoral_choices','validate_electoral_choices',[])]:getattr(__import__(module),func)(check,node,textnode,*args)
    main=json.loads((latest/'MAIN_MAP/VALIDATION.json').read_text())
    check('Map offline suite passes with current registry',main['province_RGBs']==len(ledger) and main['registry_sha256']==sha(active_registry_path()) and all(r['passed'] for r in main['checks']))
    pop=C.Counter()
    for r in a['regional_pop']:
        if r['key'][0]=='STATE_BADEN':pop[r['key'][1]]+=r['count']
    check('Baden regional population total preserved',sum(pop.values())==1015092)
    alignment=json.loads((OUT/'ALIGNMENT.json').read_text())
    check('Source provenance unchanged',alignment['source_sha256']==sha(OUT/'DE_WIT_MAINZ_3500.jpg'))
    report=dict(status='PASS_STATIC_ENGINE_DEFERRED' if all(r['passed'] for r in checks) else 'FAIL',checks=checks,
                engine_tested=False,engine_test_policy='After all HRE lots, per user',new_RGBs=len(new),registered_RGBs=len(ledger),
                province_pixels_by_controller=g['pixels_by_owner'],population_by_country=dict(pop),world_population=835804980,
                runtime_changed_files=changed,changed_pixels=int(delta.sum()),limitations=g['limitations'],
                inherited_duplicate_RGBs=a['duplicates'],inherited_reference_errors=a['errors'])
    dump=OUT/'VALIDATION.json';dump.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(report['status'],sum(c['passed'] for c in checks),'/',len(checks),'checks;',dict(pop))
    for c in checks:
        if not c['passed']:print('FAIL',c['name'],c['detail'])
    return 0 if all(c['passed'] for c in checks) else 1


if __name__=='__main__':raise SystemExit(validate())
