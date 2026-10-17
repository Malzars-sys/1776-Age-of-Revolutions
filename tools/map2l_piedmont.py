"""Explicit country membership + Piedmont-only de-jure extension; no ownership edits."""
import json
import subprocess
import sys
import numpy as np
from PIL import Image
import validate_map2a as qa
import validate_diplomacy_ottoman_1776 as cw
from map2l_belgium import sha,packed
from map2l_hre_work import GIT
from map2l_registry import active_registry_path,approved_territorial_migrations,apply_territorial_migrations,approved_lot_dirs
ROOT=qa.ROOT
LOT=ROOT/'docs/reports/map/MAP2L/PIEDMONT'
RGBS=['x1140E0','x11C061','x90C060','xA9397D','xAA6958','xACB500','xD080E0','xDA86EA','xF00544']


def dump(name,obj):
    LOT.mkdir(parents=True,exist_ok=True)
    (LOT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')


def emit(files,name):
    import map2l_belgium as emitter
    emitter.LOT=LOT
    return emitter.emit(files,name)


def capture():
    assert not (LOT/'BASELINE.json').exists(),'Never replace a lot baseline'
    import map2k_imperial_system as compiler
    LOT.mkdir(parents=True,exist_ok=True);compiler.OUT=LOT
    files=compiler.compile_system()
    # Refuse to overwrite manual/collaborator changes in generated runtime files.
    assert all((ROOT/rel).read_text(encoding='utf-8-sig')==raw.lstrip('\ufeff') for rel,raw in files.items()),'Compiler drift: review manual edits before integration'
    hashes={p.relative_to(ROOT).as_posix():sha(p)
            for folder in ['common','map_data','gui','gfx/FX','gfx/map','localization','events']
            for p in (ROOT/folder).rglob('*') if p.is_file()}
    dump('BASELINE.json',dict(inventory=qa.inventory(),hashes=hashes,
        registry=json.loads(active_registry_path().read_text(encoding='utf-8')),
        registry_sha256=sha(active_registry_path()),bitmap_sha256=sha(ROOT/'map_data/provinces.png'),
        git_head=subprocess.check_output([GIT,'rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        git_index_sha256=sha(ROOT/'.git/index')))
    print('PIEDMONT baseline captured; runtime compiler matches current files')


def prepare():
    base=json.loads((LOT/'BASELINE.json').read_text(encoding='utf-8'))
    assert sha(active_registry_path())==base['registry_sha256']
    inv=qa.inventory()
    owned=[r['key'][0] for r in inv['owners'] if r['key'][1:]==['STATE_PIEDMONT','SAR'] and r['count']==1]
    assert sorted(owned)==RGBS
    assert all(inv['geometry'][rgb]=='STATE_PIEDMONT' for rgb in RGBS)
    extra=[dict(rgb=rgb,state='STATE_PIEDMONT',beneficiary='SAR',
        basis='Explicit user-approved Piedmont-only de-jure extension, 1776-01-01; no claim on Sardinia, Savoy, Nice or Genoese provinces.') for rgb in RGBS]
    assert not {r['rgb'] for r in base['registry']} & set(RGBS)
    ledger=sorted(base['registry']+extra,key=lambda r:(r['rgb'],r['state'],r['beneficiary']))
    extension=dict(member='SAR',regions=['STATE_PIEDMONT'],provinces=extra,
        excludes=['STATE_SARDINIA','STATE_SAVOY','Genoese-owned parts of STATE_PIEDMONT','all other SAR possessions'],
        authorization='User: add Piedmont-Sardinia to the bloc, register only Piedmont, update map.')
    files={active_registry_path().relative_to(ROOT).as_posix():json.dumps(ledger,ensure_ascii=False,indent=2),
        (LOT/'EXTENSION.json').relative_to(ROOT).as_posix():json.dumps(extension,ensure_ascii=False,indent=2)}
    emit(files,'REGISTRY.patch')
    print('Prepared nine registered Piedmont provinces; previous 315 rows preserved')


def compile_imperial():
    import map2k_imperial_system as compiler
    compiler.OUT=LOT
    files=compiler.compile_system()
    changed=emit(files,'IMPERIAL.patch')
    dump('IMPERIAL_FILES.json',dict(files=changed,all_compiled_files=list(files)))
    print('Compiled integration:',len(changed),'changed runtime files')


def maps():
    import render_map2k_imperial_map as journal
    journal.OUT=LOT;journal.render()
    import prototype_map2k_main_map as main
    main.MOD=ROOT;main.PACKAGE=LOT/'MAIN_MAP'
    main.PACKAGE.mkdir(parents=True,exist_ok=True)
    main.build_and_test()


def validate():
    base=json.loads((LOT/'BASELINE.json').read_text(encoding='utf-8'))
    files=json.loads((LOT/'IMPERIAL_FILES.json').read_text(encoding='utf-8'))
    ledger=json.loads(active_registry_path().read_text(encoding='utf-8'))
    old={r['rgb']:r for r in base['registry']};rights={r['rgb']:r for r in ledger}
    inv=qa.inventory();checks=[]
    def check(name,passed,detail=''):
        checks.append(dict(name=name,passed=bool(passed),detail=detail))
    migrations=approved_territorial_migrations();regions={s for m in migrations for s in m['replaced_regions']}
    from map2l_registry import expected_country_definitions
    expected_definitions=expected_country_definitions(base['inventory']['countries'],migrations)
    def outside_inventory(obj):
        result={k:v for k,v in obj.items() if k not in {'owners','states','state_types','geometry','countries','regional_pop','buildings'}}
        for key,at in [('owners',1),('regional_pop',0),('buildings',0)]:result[key]=[r for r in obj[key] if r['key'][at] not in regions]
        result['states']=[r for r in obj['states'] if r[0] not in regions]
        result['state_types']={k:v for k,v in obj['state_types'].items() if k.split('|')[0] not in regions}
        result['geometry']={k:v for k,v in obj['geometry'].items() if v not in regions}
        result['countries']={k:(expected_definitions[k] if obj is base['inventory'] else v) for k,v in obj['countries'].items() if k in base['inventory']['countries']}
        return result
    check('Gameplay inventory outside explicit Franconia migration unchanged',outside_inventory(inv)==outside_inventory(base['inventory']))
    previous_bmp=packed(ROOT/'docs/reports/map/MAP2L/BELGIUM/provinces_candidate.png')
    current_bmp=packed(ROOT/'map_data/provinces.png')
    from map2l_registry import ownership_rows,migrate_extent
    allowed_pixels=np.isin(previous_bmp,[int(r['rgb'][1:],16) for m in migrations for r in ownership_rows(m,'previous')])
    check('Bitmap unchanged outside explicit Franconia migration',np.array_equal(previous_bmp[~allowed_pixels],current_bmp[~allowed_pixels]))
    expected=apply_territorial_migrations(base['registry'])
    check('All earlier rights preserved except exact approved Franconia migration',all(rights[r['rgb']]==r for r in expected))
    added=[r for r in ledger if r['beneficiary']=='SAR']
    check('Exactly nine SAR Piedmont rights added',len(ledger)==len(rights)==len(expected)+9 and {r['rgb'] for r in added}==set(RGBS)
          and all(r['state']=='STATE_PIEDMONT' and r['beneficiary']=='SAR' for r in added))
    check('No Sardinian, Savoyard, Genoese or other SAR territories registered',
          {r['rgb'] for r in ledger if r['beneficiary']=='SAR'}==set(RGBS))
    from validate_map2k_imperial import node,textnode
    member=textnode(node('common/scripted_triggers/1776_imperial_constitution.txt','aor1776_hre_member'))
    elect=textnode(node('common/scripted_triggers/1776_imperial_constitution.txt','aor1776_hre_elector'))
    check('SAR recognised as an imperial member','c:SAR' in member)
    check('SAR has no added electoral title','c:SAR' not in elect)
    bloc=next(n for n in cw.walk(cw.parse((ROOT/'common/history/power_blocs/00_power_blocs.txt').read_text(encoding='utf-8-sig'))) if n.key=='c:AUS')
    check('SAR joins starting imperial bloc exactly once',sum(n.key=='member' and cw.scalar(n.value)=='c:SAR' for n in cw.walk(bloc.children()))==1)
    refresh=textnode(node('common/scripted_effects/1776_imperial_constitution.txt','aor1776_hre_feedback_refresh'))
    check('Registered marker refresh includes all nine Piedmont RGBs',all('p:'+rgb+'.state' in refresh for rgb in RGBS))
    check('Registered marker refresh has no Sardinian RGB',all('p:'+r['key'][0]+'.state' not in refresh for r in inv['owners'] if r['key'][1:] == ['STATE_SARDINIA','SAR']))
    bmp=packed(ROOT/'map_data/provinces.png');newmask=np.isin(bmp,[int(r['rgb'][1:],16) for r in ledger])
    oldmask=np.isin(previous_bmp,[int(r['rgb'][1:],16) for r in base['registry']])
    piedmont=np.isin(bmp,[int(r[1:],16) for r in RGBS])
    check('Map expands only by Piedmont and explicit later deltas',np.array_equal(newmask,migrate_extent(oldmask|piedmont,migrations)))
    report_path=approved_lot_dirs()[-1]/'MAIN_MAP/VALIDATION.json' if migrations else LOT/'MAIN_MAP/VALIDATION.json'
    main=json.loads(report_path.read_text(encoding='utf-8'))
    check('Main map offline suite passes',main['province_RGBs']==len(ledger) and all(r['passed'] for r in main['checks']))
    allowed=set(files['files'])|{'gfx/interface/journal_entries/aor1776_hre_registered_map.dds','gfx/map/map_painting/aor1776_hre_mask.dds','gfx/map/map_painting/aor1776_hre_sentinel.dds'}
    for fp in approved_lot_dirs():
        allowed|=set(json.loads((fp/'PLAN.json').read_text())['files'])|set(json.loads((fp/'IMPERIAL_FILES.json').read_text())['files'])|{'map_data/provinces.png','map_data/province_terrains.txt'}
    changed=[p for p,h in base['hashes'].items() if sha(ROOT/p)!=h]
    check('No unrelated runtime changes',set(changed)<=allowed,str(sorted(set(changed)-allowed)))
    check('HEAD and Git index unchanged',subprocess.check_output([GIT,'rev-parse','HEAD'],cwd=ROOT,text=True).strip()==base['git_head'] and sha(ROOT/'.git/index')==base['git_index_sha256'])
    for module,func,args in [('validate_map2k_feedback','validate_feedback',[ledger]),('validate_map2k_reforms','validate_reforms',[]),('validate_map2k_repairs','validate_repairs',[ledger]),('validate_map2k_dashboard','validate_dashboard',[]),('validate_map2k_demand_feedback','validate_demand_feedback',[]),('validate_map2k_atlas_access','validate_atlas_access',[]),('validate_map2k_electoral_choices','validate_electoral_choices',[])]:
        getattr(__import__(module),func)(check,node,textnode,*args)
    dump('VALIDATION.json',dict(status='PASS_STATIC_ENGINE_PENDING' if all(r['passed'] for r in checks) else 'FAIL',checks=checks,
        registered_RGBs=len(ledger),added_RGBs=RGBS,added_map_pixels=int(piedmont.sum()),runtime_changed_files=changed,engine_tested=False,
        approved_territorial_migrations=migrations))
    print('Piedmont validation:',sum(r['passed'] for r in checks),'/',len(checks),'checks;',int(piedmont.sum()),'new imperial map pixels')
    for r in checks:
        if not r['passed']:print('FAIL:',r['name'],r['detail'])
    return 0 if all(r['passed'] for r in checks) else 1


if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    result={'capture':capture,'prepare':prepare,'compile-imperial':compile_imperial,'maps':maps,'validate':validate}[sys.argv[1]]()
    raise SystemExit(result or 0)
