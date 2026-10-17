"""Differential checks for the applied source-traced Franconia lot, not engine QA."""
import collections as C
import json
import re
import subprocess
import numpy as np
import validate_map2a as qa
import validate_diplomacy_ottoman_1776 as cw
from map_1776_audit import effective,values
from map2l_franconia import ROOT,OUT,SID,TAGS,baseline,packed,sha,csvout
from map2l_hre_work import GIT
from map2l_registry import active_registry_path,apply_territorial_migrations,approved_lot_dirs,effective_assignments,ancestor_rgb,ownership_rows,migrate_extent,expected_country_definitions
from validate_map2k_imperial import node,textnode,profiles


def validate():
    b=baseline();a=qa.inventory();g=json.loads((OUT/'GEOMETRY.json').read_text());p=json.loads((OUT/'PLAN.json').read_text())
    integrated=json.loads((OUT/'IMPERIAL_FILES.json').read_text());checks=[]
    later_dirs=approved_lot_dirs()[1:]
    later_geos=[json.loads((fp/'GEOMETRY.json').read_text()) for fp in later_dirs]
    rhdir=later_dirs[-1] if later_dirs else OUT
    rh=later_geos[-1] if later_geos else None
    reviewed=effective_assignments([g]+later_geos)
    def check(name,passed,detail=''):
        checks.append(dict(name=name,passed=bool(passed),detail=detail))
    check('World population preserved',sum(r['count'] for r in a['pops'])==sum(r['count'] for r in b['inventory']['pops'])==835804980)
    check('Every culture and religion preserved',a['pops']==b['inventory']['pops'] and a['resolved_demographics']==b['inventory']['resolved_demographics'])
    check('Population profiles by region preserved',profiles(None,'pops')==profiles(b,'pops'))
    check('Building levels by type preserved',a['building_levels_written']==b['inventory']['building_levels_written'])
    check('PMs reserves and all other building attributes weighted by level preserved',profiles(None,'buildings')==profiles(b,'buildings'))
    check('Armies navies formations and recruitment unchanged',a['units']==b['inventory']['units'])
    check('No new reference errors',a['errors']==b['inventory']['errors'],str(a['errors']))
    check('No new duplicate assignments',a['duplicates']==b['inventory']['duplicates'])
    expected=qa.counter(b['inventory']['owners'])
    for r in b['inventory']['owners']:
        if r['key'][1]==SID:expected[tuple(r['key'])]-=r['count']
    for r in g['assignments']:expected[(r['rgb'],SID,r['owner'])]+=1
    for fp in later_dirs:
        m=json.loads((fp/'REGISTRY_MIGRATION.json').read_text())
        for r in ownership_rows(m,'previous'):expected[(r['rgb'],r['state'],r['beneficiary'])]-=1
        for r in ownership_rows(m,'updated'):expected[(r['rgb'],r['state'],r['beneficiary'])]+=1
    check('Exact reviewed owners; all other territories unchanged',+expected==qa.counter(a['owners']))
    subsequent_tags={t for fp in later_dirs for t in json.loads((fp/'REGISTRY_MIGRATION.json').read_text())['new_members']}
    check('Exactly five Franconian estate tags plus explicitly approved subsequent estates',set(a['countries'])-set(b['inventory']['countries'])==set(TAGS)|subsequent_tags)
    expected_definitions=expected_country_definitions(b['inventory']['countries'],[json.loads((fp/'REGISTRY_MIGRATION.json').read_text()) for fp in later_dirs])
    check('Previous country definitions preserved except exact reviewed WUR tier',all(a['countries'][t]==expected_definitions[t] for t in b['inventory']['countries']))
    check('Every new capital state is owned',all([SID,t] in a['states'] for t in TAGS))
    bmp=packed(ROOT/'map_data/provinces.png');oldbmp=packed(ROOT/b['bitmap_backup']);new={int(r['rgb'][1:],16):r for r in g['new_provinces']}
    check('Baseline bitmap still exact',sha(ROOT/b['bitmap_backup'])==b['bitmap_sha256'])
    check('Live bitmap is reviewed candidate',sha(ROOT/'map_data/provinces.png')==(rh or g)['candidate_sha256'])
    all_new=dict(new)
    for geo in later_geos:all_new.update({int(r['rgb'][1:],16):r for r in geo['new_provinces']})
    check('35 Franconian RGBs plus explicit later splits, no original identity removed',set(np.unique(bmp).tolist())-set(np.unique(oldbmp).tolist())==set(all_new) and set(np.unique(oldbmp).tolist())<=set(np.unique(bmp).tolist()) and len(new)==35)
    originals={int(r['key'][0][1:],16) for r in b['inventory']['owners'] if r['key'][1]==SID}
    old_colors=set(np.unique(oldbmp).tolist())
    for geo in later_geos:originals|={ancestor_rgb(r,old_colors) for r in geo['parents']}
    delta=bmp!=oldbmp
    check('No bitmap change outside Franconia and explicitly reviewed later parents',set(np.unique(oldbmp[delta]).tolist())<=originals)
    check('Every new RGB inside its exact parent',all(np.all(oldbmp[bmp==rgb]==int(row['parent_rgb'][1:],16)) for rgb,row in new.items()))
    for r in reviewed:
        rgb=int(r['rgb'][1:],16)
        check('Reviewed cells '+r['rgb'],int((bmp==rgb).sum())==r['pixels'] and all(int(bmp[y,x])==rgb for x,y in r['cells']))
        # Derived adjacency is inspected, not guessed from province names.
        cells={tuple(x) for x in r['cells']};todo=[next(iter(cells))];seen={todo[0]}
        while todo:
            x,y=todo.pop()
            for q in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
                if q in cells and q not in seen:seen.add(q);todo.append(q)
        check('Province is four-connected '+r['rgb'],len(cells)==len(seen))
    oldterrain=(ROOT/'map_data/province_terrains.txt').read_text(encoding='utf-8-sig')
    tmap={k.upper():v for k,v in re.findall(r'(?im)^\s*(x[0-9a-f]{6})\s*=\s*"([^"\n]+)"',oldterrain)}
    check('Every child inherits parent terrain',all(tmap[r['rgb'].upper()]==tmap[r['parent_rgb'].upper()] for r in g['new_provinces']))
    hubs=[('xD0C0A0',4351,877,'NUR'),('xF91154',4362,862,'ANS'),('x51C0A0',4322,861,'WZB'),('x648AD1',4347,862,'FBM')]
    for rgb,x,y,owner in hubs:check('Native hub stays on declared RGB '+rgb,int(bmp[y,x])==int(rgb[1:],16) and next(r for r in g['assignments'] if r['rgb']==rgb)['owner']==owner)
    ledger=json.loads(active_registry_path().read_text());rights={r['rgb']:r for r in ledger}
    later_migrations=[json.loads((fp/'REGISTRY_MIGRATION.json').read_text()) for fp in later_dirs]
    check('Exact approved imperial register, unique RGBs',ledger==apply_territorial_migrations(b['de_jure_registry']) and len(ledger)==len(rights)==359+sum(len(mi['updated'])-len(mi['previous']) for mi in later_migrations))
    migrated={s for fp in later_dirs for s in json.loads((fp/'REGISTRY_MIGRATION.json').read_text())['replaced_regions']}
    check('Every other right including SAR and Belgian estates unchanged',all(rights[r['rgb']]==r for r in b['de_jure_registry'] if r['state'] not in {SID,*migrated}))
    check('Reviewed registered rights match owners',all(rights[r['rgb']]['beneficiary']==r['owner'] and rights[r['rgb']]['state']==r['state'] for r in reviewed if r['rgb'] in rights))
    check('Imperial extent changes only by explicit deltas',np.array_equal(migrate_extent(np.isin(oldbmp,[int(r['rgb'][1:],16) for r in b['de_jure_registry']]),later_migrations),np.isin(bmp,[int(r['rgb'][1:],16) for r in ledger])))
    from map2k_imperial_system import compile_system,MEMBERS
    import map2k_imperial_system as compiler
    compiler.OUT=OUT;compiled=compile_system()
    for rel,raw in compiled.items():
        check('Compiler matches runtime '+rel,(ROOT/rel).read_text(encoding='utf-8-sig')==raw.lstrip('\ufeff'))
        if rel.endswith('.txt'):cw.parse(raw)
    check('Five new countries recognised as members',set(TAGS)<=set(MEMBERS))
    bloc=next(n for n in cw.walk(cw.parse((ROOT/'common/history/power_blocs/00_power_blocs.txt').read_text(encoding='utf-8-sig'))) if n.key=='c:AUS')
    members=[cw.scalar(n.value) for n in cw.walk(bloc.children()) if n.key=='member']
    check('New members and SAR exactly once in starting bloc',all(members.count('c:'+t)==1 for t in TAGS+['SAR']))
    free=node('common/scripted_triggers/1776_imperial_constitution.txt','aor1776_hre_free_city')
    check('Nuremberg recognised as a free city','c:NUR' in textnode(free))
    elect=node('common/scripted_triggers/1776_imperial_constitution.txt','aor1776_hre_elector')
    check('No new electoral titles',not any('c:'+t in textnode(elect) for t in TAGS))
    law_nodes={n.key:n for f in effective(ROOT,qa.GAME,'common/laws') for n in cw.parse(f.read_text(encoding='utf-8-sig'))}
    for tag in TAGS:
        raw=(ROOT/f'common/history/countries/{tag.lower()} - franconian estate.txt').read_text();ns=list(cw.walk(cw.parse(raw)))
        tech={cw.scalar(n.value) for n in ns if n.key=='add_technology_researched'}
        chosen=[cw.scalar(n.value).split(':')[1] for n in ns if n.key=='activate_law']
        for key in chosen:
            check('Starting law techs valid '+tag+' '+key,key in law_nodes and set(values(law_nodes[key],'unlocking_technologies'))<=tech)
        check('No advanced blanket grant '+tag,tech==set(p['technology_initializations']) and 'national_sovereignty' not in tech and 'abolitionist_mobilization' not in tech)
        check('No old incompatible politics preset '+tag,'effect_starting_politics_' not in raw)
    for key in ['law_aor1776_imperial_city_republic','law_aor1776_imperial_customs','law_aor1776_imperial_no_slavery']:
        check('Native variant parent exists '+key,cw.scalar(law_nodes[key].one('parent')) in law_nodes)
    citygov=node('common/government_types/00_1776_map2l_nuremberg.txt','gov_aor1776_nuremberg_council')
    check('Nuremberg council government is country scoped','c:NUR' in textnode(citygov) and 'law_aor1776_imperial_city_republic' in textnode(citygov))
    for lang in ['french','english']:
        file=ROOT/f'localization/{lang}/1776_map2l_franconia_l_{lang}.yml';s=file.read_text(encoding='utf-8-sig')
        check('Localisation BOM and estate names '+lang,file.read_bytes().startswith(b'\xef\xbb\xbf') and all(' '+t+':0 ' in s and ' '+t+'_ADJ:0 ' in s for t in TAGS))
    for rel in p['files']:
        if rel.endswith('.txt'):
            raw=(ROOT/rel).read_text(encoding='utf-8-sig');ns=cw.parse(raw)
            for n in cw.walk(ns):
                if n.key in {'icon','texture','pattern'} and isinstance(n.value,str):
                    value=cw.scalar(n.value)
                    if value.startswith('gfx/'):check('Asset reference '+value,(ROOT/value).exists() or (qa.GAME/value).exists())
    allowed=set(p['files'])|set(integrated['files'])|{'map_data/provinces.png','map_data/province_terrains.txt','gfx/interface/journal_entries/aor1776_hre_registered_map.dds','gfx/map/map_painting/aor1776_hre_mask.dds','gfx/map/map_painting/aor1776_hre_sentinel.dds'}
    for fp in later_dirs:allowed|=set(json.loads((fp/'PLAN.json').read_text())['files'])|set(json.loads((fp/'IMPERIAL_FILES.json').read_text())['files'])
    changed=[rel for rel,h in b['hashes'].items() if sha(ROOT/rel)!=h]
    check('Only scoped runtime changes',set(changed)<=allowed,str(sorted(set(changed)-allowed)))
    check('HEAD and Git index unchanged',subprocess.check_output([GIT,'rev-parse','HEAD'],cwd=ROOT,text=True).strip()==b['git_head'] and sha(ROOT/'.git/index')==b['git_index_sha256'])
    for module,func,args in [('validate_map2k_feedback','validate_feedback',[ledger]),('validate_map2k_reforms','validate_reforms',[]),('validate_map2k_repairs','validate_repairs',[ledger]),('validate_map2k_dashboard','validate_dashboard',[]),('validate_map2k_demand_feedback','validate_demand_feedback',[]),('validate_map2k_atlas_access','validate_atlas_access',[]),('validate_map2k_electoral_choices','validate_electoral_choices',[])]:getattr(__import__(module),func)(check,node,textnode,*args)
    main=json.loads(((rhdir if rh else OUT)/'MAIN_MAP/VALIDATION.json').read_text())
    check('Updated map passes offline checks',main['province_RGBs']==len(ledger) and all(r['passed'] for r in main['checks']))
    population=C.Counter()
    for r in a['regional_pop']:
        if r['key'][0]==SID:population[r['key'][1]]+=r['count']
    report=dict(status='PASS_STATIC_ENGINE_PENDING' if all(r['passed'] for r in checks) else 'FAIL',checks=checks,
        population_by_country=dict(population),world_population=835804980,new_countries=TAGS,new_RGBs=len(new),registered_RGBs=len(ledger),
        changed_pixels=int(delta.sum()),runtime_changed_files=changed,engine_tested=False,limitations=g['limitations'],
        inherited_errors=a['errors'],inherited_duplicate_RGBs=a['duplicates'])
    from map2l_runtime_receipt import annotate
    annotate(report,OUT)
    (OUT/'VALIDATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(report['status'],len(checks),'checks;',dict(population))
    for row in checks:
        if not row['passed']:print('FAIL',row['name'],row['detail'])
    return 0 if report['status'].startswith('PASS') else 1


if __name__=='__main__':raise SystemExit(validate())
