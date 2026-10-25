"""Repair only the pending Berchtesgaden salt establishment; preserve prior proofs."""
import contextlib,copy,io,json,os,shutil,subprocess,sys,unittest
from pathlib import Path
import serg_sc1_berchtesgaden as lot
ROOT=lot.ROOT;rm=lot.rm;core=lot.core;sha=lot.sha;load=lot.load
OUT=lot.OUT/'SALT_FIX_R1';TASK=lot.TASK;PREFIX=OUT.relative_to(ROOT).as_posix()+'/'
BUILD='building_aor1776_berchtesgaden_saline';GROUP='bg_aor1776_berchtesgaden_salt'
USER='Petite précision, la saline n’est pas construite. D’ailleurs, il n’y a pas de saline, mais des mines de sel.'
IMAGE=Path('C:/Users/simeo/AppData/Local/Temp/codex-clipboard-aa8b6093-40fd-48b5-9b0d-7dd9ced5d50c.png')
ATTACHMENT=Path('C:/Users/simeo/.codex/attachments/a468856e-7d1a-44c3-8e2e-a64da987b7b4/Texte collé.txt')
os.environ['GIT_OPTIONAL_LOCKS']='0'
def dump(name,data):rm.write_json(OUT/name,data)

def capture():
    assert not (OUT/'BASELINE.json').exists();OUT.mkdir(exist_ok=True)
    s=load(rm.OUT/'ROADMAP_STATE.json');assert s['events'][-1]['id']=='SERG-RM-0032'
    t=next(t for t in s['tasks'] if t['id']==TASK);assert t['installed_delivery_status']=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION' and t['runtime_validation']['attestation'] is None
    old=load(lot.OUT/'DELIVERY_MANIFEST.json');diff=[p for p,h in old['files'].items() if not (ROOT/p).is_file() or sha(ROOT/p)!=h];assert not diff,diff
    git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
    dump('BASELINE.json',dict(roadmap=s,hashes=lot.italian.runtime_hashes(),inventory=core.qa.inventory(),proofs={p.relative_to(ROOT).as_posix():sha(p) for p in rm.OUT.rglob('*') if p.is_file() and OUT not in p.parents},old_tools={p.relative_to(ROOT).as_posix():sha(p) for p in (ROOT/'tools').glob('*.py') if p.name!=Path(__file__).name},git=dict(head=git('rev-parse','HEAD'),branch=git('branch','--show-current'),index=sha(ROOT/'.git/index')),old_delivery_manifest_matches=True))
    shutil.copyfile(IMAGE,OUT/'USER_SCREENSHOT.png');shutil.copyfile(ATTACHMENT,OUT/'REPEATED_BRIXEN_MISSION.txt');(OUT/'USER_CORRECTION.txt').write_text(USER,encoding='utf8')
    logs=Path('C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/logs');selected=[]
    for p in sorted(logs.glob('*.log')):
        for num,line in enumerate(p.read_text(encoding='utf8',errors='replace').splitlines(),1):
            if any(key in line.lower() for key in ['berchtesgaden','frauenreuth','aor1776_berch']):selected.append(dict(file=p.name,line=num,text=line))
    dump('LOG_REVIEW.json',dict(observed=selected,conclusion='Files loaded according to logs; no explicit deletion/initialization error for this establishment found. Exact engine cause not isolated. Generic 0/2 mine shown by user is a different building type.',engine_reproduced_by_agent=False));print('Current delivery intact; correction baseline captured',flush=True)

def install():
    b=load(OUT/'BASELINE.json');assert load(rm.OUT/'ROADMAP_STATE.json')==b['roadmap'];current=lot.italian.runtime_hashes();assert current==b['hashes'],'Concurrent change: review before applying'
    files={};before={}
    def read(p):
        raw=(ROOT/p).read_bytes().decode('utf8');assert sha(ROOT/p)==b['hashes'][p];before[p]=raw;return raw
    p='common/buildings/1776_sc1_berchtesgaden.txt';raw=read(p);assert raw.count('building_group = bg_light_industry city_type = city')==1
    raw=raw.replace('# Inland wood-fired brine boiling, not a coastal pan or a new mining concession.','# Small princely salt mine and brine processing; historical internal key retained.').replace('building_group = bg_light_industry city_type = city','building_group = '+GROUP+' city_type = mine').replace('expandable = no buildable = no downsizeable = no ownership_type = self','expandable = no buildable = no downsizeable = no\n has_max_level = yes max_level = 1')
    files[p]=raw
    p='common/building_groups/1776_sc1_berchtesgaden_salt.txt';assert not (ROOT/p).exists();files[p]='''# Fixed local establishment, not extra capacity for the generic salt-mine resource.
bg_aor1776_berchtesgaden_salt = {
 parent_group = bg_mining
 always_possible = yes
 capped_by_resources = no
 default_building = building_aor1776_berchtesgaden_saline
 economy_of_scale = no
 urbanization = 0
 infrastructure_usage_per_level = 0.1
 subsidized = yes
}
'''
    p='common/scripted_effects/1776_sc1_berchtesgaden.txt';raw=read(p);files[p]=raw+'''
# New-game repair only. Both start hooks may fire; an existing level is never added again.
initialize_aor1776_berchtesgaden_salt = {
 if = {
  limit = { date < 1776.1.2 }
  every_state = {
   limit = {
    state_region = s:STATE_TYROL
    owner = { c:BGT ?= this }
    NOT = { has_building = building_aor1776_berchtesgaden_saline }
   }
   create_building = {
    building = building_aor1776_berchtesgaden_saline
    level = 1
    reserves = 1
    activate_production_methods = { pm_aor1776_berchtesgaden_saline }
   }
  }
 }
}
'''
    p='common/on_actions/99_1776_sc1_berchtesgaden.txt';raw=read(p)
    for key in ['on_game_started','on_game_started_after_lobby']:
        old=key+' = { on_actions = { aor1776_berchtesgaden_names_initialize } }';assert old in raw;raw=raw.replace(old,key+' = { on_actions = { aor1776_berchtesgaden_names_initialize aor1776_berchtesgaden_salt_initialize } }')
    files[p]=raw+'\naor1776_berchtesgaden_salt_initialize = { effect = { initialize_aor1776_berchtesgaden_salt = yes } }\n'
    for lang,values in [('french',{'building_aor1776_berchtesgaden_saline':'Mine de sel de la prévôté','building_aor1776_berchtesgaden_saline_desc':'Les mineurs ouvrent les galeries et recueillent la saumure, puis les ouvriers la chauffent au bois pour en obtenir le sel.','pmg_aor1776_berchtesgaden_saline':'Exploitation du sel','pm_aor1776_berchtesgaden_saline':'Galeries et poêles à sel'}),('english',{'building_aor1776_berchtesgaden_saline':'Prince-Provost’s Salt Mine','building_aor1776_berchtesgaden_saline_desc':'Miners open galleries and collect brine, which workers then boil over wood fires to obtain salt.','pmg_aor1776_berchtesgaden_saline':'Salt Extraction','pm_aor1776_berchtesgaden_saline':'Galleries and Salt Pans'})]:
        p='localization/'+lang+'/1776_sc1_berchtesgaden_l_'+lang+'.yml';raw=read(p)
        for k,v in values.items():
            import re
            raw,n=re.subn(r'(?m)^( '+re.escape(k)+r':0 )"[^"\n]*"',lambda m:m[1]+'"'+v+'"',raw);assert n==1,(k,n)
        files[p]=raw
    for p,raw in files.items():
        if p.endswith('.txt'):core.cw.parse(raw.lstrip('\ufeff'))
        if p in before:assert (ROOT/p).read_bytes()==before[p].encode('utf8')
        else:assert not (ROOT/p).exists()
    dump('TEXT_BEFORE.json',before);dump('EXPECTED_TEXT.json',files)
    for p,raw in files.items():(ROOT/p).write_bytes(raw.encode('utf8'))
    dump('FILES_MODIFIED.json',dict(runtime_files=sorted(files),sha256={p:sha(ROOT/p) for p in files},old_proofs_preserved=True));print('Six bounded files installed; local mine maximum one level; no generic PM change',flush=True)

def validate():
    b=load(OUT/'BASELINE.json');current=lot.italian.runtime_hashes();inv=core.qa.inventory();files=load(OUT/'EXPECTED_TEXT.json');checks=[]
    def ck(name,ok,detail=None):checks.append(dict(name=name,passed=bool(ok),detail=detail))
    ck('All historical populations owners buildings units and country definitions identical',inv==b['inventory'])
    changed=sorted(p for p in set(current)|set(b['hashes']) if current.get(p)!=b['hashes'].get(p));ck('Exactly six declared runtime files changed',changed==sorted(files),changed)
    for p,raw in files.items():
        ck('Exact installed bytes '+p,(ROOT/p).read_bytes()==raw.encode('utf8'))
        if p.endswith('.txt'):
            try:core.cw.parse(raw.lstrip('\ufeff'));ok=True
            except Exception:ok=False
            ck('Paradox syntax '+p,ok)
    buildings=core.cw.parse(files['common/buildings/1776_sc1_berchtesgaden.txt']);mine=buildings[1]
    ck('Court definition byte-for-byte retained',core.qa.signature(buildings[0])==core.qa.signature(core.cw.parse(load(OUT/'TEXT_BEFORE.json')['common/buildings/1776_sc1_berchtesgaden.txt'])[0]))
    ck('Mine shown under resource mining lens',mine.one('building_group')==GROUP and mine.one('city_type')=='mine')
    ck('One-level fixed nonbuildable local establishment',mine.one('has_max_level')=='yes' and mine.one('max_level')=='1' and mine.one('buildable')==mine.one('expandable')=='no')
    ck('Mine still limited to BGT owned Tyrol portion','potential = { state_region = s:STATE_TYROL owner = { c:BGT ?= this } }' in files['common/buildings/1776_sc1_berchtesgaden.txt'])
    group=core.cw.parse(files['common/building_groups/1776_sc1_berchtesgaden_salt.txt'])[0]
    ck('Local group no extra generic resource capacity',group.one('parent_group')=='bg_mining' and group.one('always_possible')=='yes' and group.one('capped_by_resources')=='no' and group.one('default_building')==BUILD)
    ck('Public default ownership like court, no employee self-ownership',mine.one('ownership_type') is None)
    history=core.region((ROOT/'common/history/buildings/1776_sc1_berchtesgaden.txt').read_text('utf8'),lot.SID,lot.TAG).children('create_building');salt=history[1]
    ck('Exactly one national level declared no duplicate historical mine',len(history)==2 and salt.one('building')=='"'+BUILD+'"' and salt.children('add_ownership')[0].children('country')[0].one('levels')=='1')
    pm=core.cw.parse((ROOT/'common/production_methods/1776_sc1_berchtesgaden.txt').read_text('utf8'))[1];mods=pm.children('building_modifiers')[0]
    jobs=sum(int(n.value) for n in mods.children('level_scaled')[0].children());ck('Unchanged 100-job capacity with 1 salt output',jobs==100 and mods.children('workforce_scaled')[0].one('goods_output_salt_add')=='1')
    effect=files['common/scripted_effects/1776_sc1_berchtesgaden.txt'];ck('New-game repair owner region date and absence guards present',all(x in effect for x in ['date < 1776.1.2','owner = { c:BGT ?= this }','state_region = s:STATE_TYROL','NOT = { has_building = '+BUILD+' }','level = 1']))
    ck('Naming effect retained verbatim',effect.startswith(load(OUT/'TEXT_BEFORE.json')['common/scripted_effects/1776_sc1_berchtesgaden.txt']))
    hooks=files['common/on_actions/99_1776_sc1_berchtesgaden.txt'];ck('Both start hooks call idempotent repair',hooks.count('aor1776_berchtesgaden_names_initialize aor1776_berchtesgaden_salt_initialize')==2)
    ck('No technology treaties armies resource changes',not any(x in ' '.join(changed) for x in ['technolog','treaties/','military_formations/','state_regions/','provinces.png','history/pops/']))
    import localization_duplicate_audit as audit
    keysets=[]
    for lang in ['french','english']:
        p='localization/'+lang+'/1776_sc1_berchtesgaden_l_'+lang+'.yml';matched=[audit.KEY.match(line) for line in files[p].lstrip('\ufeff').splitlines()[1:]];keys={m.group(1) for m in matched if m};keysets.append(keys);allentries=audit.entries(lang)
        ck('BOM syntax and no duplicate '+lang,(ROOT/p).read_bytes().startswith(b'\xef\xbb\xbf') and all(matched) and all(len(allentries[k])==1 for k in keys))
    ck('Same 18 localized keys',keysets[0]==keysets[1] and len(keysets[0])==18)
    oldtools=[p for p,h in b['old_tools'].items() if sha(ROOT/p)!=h];ck('All preexisting tools and tests unchanged',not oldtools,oldtools)
    oldproofs=[p for p,h in b['proofs'].items() if Path(p).parent!=rm.OUT.relative_to(ROOT) and sha(ROOT/p)!=h];ck('All old nested proofs including original Berchtesgaden delivery unchanged',not oldproofs,oldproofs)
    ck('No fabricated BGT human receipt',not list(lot.OUT.glob('RUNTIME_USER_ATTESTATION*')))
    git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip();ck('HEAD branch and index preserved',git('rev-parse','HEAD')==b['git']['head'] and git('branch','--show-current')==b['git']['branch'] and sha(ROOT/'.git/index')==b['git']['index'])
    v=dict(task_ids=[TASK],status='PASS' if all(c['passed'] for c in checks) else 'FAIL',passed=sum(c['passed'] for c in checks),total=len(checks),failed=[c['name'] for c in checks if not c['passed']],checks=checks,automated_engine_test=False,engine_executed=False)
    dump('VALIDATION.json',v);print('Correction static',v['passed'],'/',v['total'],v['failed'],flush=True);assert not v['failed'];dump('SESSION_AFTER_STATIC.json',dict(hashes=current,inventory=inv))

if __name__=='__main__':globals()[sys.argv[1]]()
