"""1776 colonies: British expansion restriction and one Nova Scotia administration.

Bounded current-file staging, hash guarded application; no vanilla or Git writes.
"""
import collections as C
import json,sys
from pathlib import Path
from audit_hbc_1776 import ROOT,GAME,effective,runtime,sha,provs
from hbc06_integrate import text,encoded,edit,state_nodes,ownership,rgb_block
from validate_diplomacy_ottoman_1776 import parse,walk,scalar,normalized
from hbc03_quebec_arc import economic_inventory,conservation
from r8_south_correct import pop_signature

OUT=ROOT/'docs/reports/map/NORTH_AMERICA_1776/COLONIES-01/CORE'
ST='common/history/states/00_states.txt';PP='common/history/pops/05_north_america.txt'
BB='common/history/buildings/05_north_america.txt';MIL='common/history/military_formations/01_military_formations_north_america.txt'
US='common/history/countries/usa - usa.txt';LAW='common/laws/01_colonial_affairs.txt'
TRIGGER='aor1776_usa_british_expansion_locked'


def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def dump(name,value):(OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf8')


def stage(files,extra):
    OUT.mkdir(parents=True,exist_ok=True);base=runtime();assert not (OUT/'APPLIED.json').exists()
    dump('BASELINE_RUNTIME.json',base);dump('BASELINE_OWNERS.json',{r:sorted(v) for r,v in ownership().items()});dump('BASELINE_HBC.json',economic_inventory())
    for rel,data in files.items():
        if rel.endswith('.txt'):parse(data.decode('utf-8-sig'))
        p=OUT/'patch'/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
    dump('PATCH.json',dict(input_sha256={r:base.get(r) for r in files},output_sha256={r:sha(OUT/'patch'/r) for r in files}))
    dump('PLAN.json',extra);assert runtime()==base,'Concurrent runtime change'


def apply():
    p=load(OUT/'PATCH.json');assert not (OUT/'APPLIED.json').exists()
    for r,d in p['input_sha256'].items():assert (sha(ROOT/r) if (ROOT/r).exists() else None)==d,r+' changed'
    for r,d in p['output_sha256'].items():assert sha(OUT/'patch'/r)==d
    for r in p['output_sha256']:
        path=ROOT/r
        if path.exists():
            b=OUT/'before'/r;b.parent.mkdir(parents=True,exist_ok=True);b.write_bytes(path.read_bytes())
        path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes((OUT/'patch'/r).read_bytes())
    dump('APPLIED.json',dict(date='2026-10-26',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',engine_tested=False))
    print('Installed core correction.')


def body(raw,n):return raw[raw.index('{',n.start)+1:n.end-1]
def level(n):return sum(int(v.value) for v in walk(n.children()) if v.key=='levels')
def signature(n):
    def clean(v):
        return [[x.key,x.op,clean(x.value)] for x in v if x.key!='levels'] if isinstance(v,list) else scalar(v).replace('c:NBS','c:NVS')
    return clean(n.children())


def prepare():
    OUT.mkdir(parents=True,exist_ok=True);initial=runtime();files={}
    raw=text(ROOT/US);patch=[]
    for n in walk(parse(raw)):
        if n.key=='activate_law' and scalar(n.value)=='law_type:law_frontier_colonization':patch.append((n.start,n.end,'activate_law = law_type:law_no_colonial_affairs'))
        if n.key=='set_institution_investment_level' and scalar(n.one('institution'))=='institution_colonial_affairs':patch.append((n.start,n.end,''))
    assert len(patch)==2;files[US]=encoded(ROOT/US,edit(raw,patch))
    p=ROOT/LAW if (ROOT/LAW).exists() else GAME/LAW;raw=text(p);patch=[]
    laws=[n for n in parse(raw) if scalar(n.one('group'))=='lawgroup_colonization'];assert len(laws)==4
    guard='\n custom_tooltip = { text = aor1776_proclamation_independence_tt NOT = { '+TRIGGER+' = yes } }\n'
    for n in laws:
        if n.key=='law_no_colonial_affairs':continue
        enact=n.children('can_enact')
        if enact:patch.append((enact[0].end-1,enact[0].end-1,guard))
        else:patch.append((n.end-1,n.end-1,'\n can_enact = {'+guard+'}\n'))
        impose=n.children('can_impose');assert len(impose)==1
        patch.append((impose[0].end-1,impose[0].end-1,'\n scope:target_country = {'+guard+'}\n'))
    files[LAW]=encoded(p,edit(raw,patch))
    files['common/scripted_triggers/1776_usa_colonial_expansion.txt']=(TRIGGER+' = { this = c:USA OR = { is_subject = yes aor1776_usa_independence_war_active = yes } }\n').encode()
    for lang in ['french','english']:
        sentence=('Les restrictions coloniales restent en vigueur tant que nous dépendons d’une autre puissance. L’indépendance nous permettra de choisir notre politique de colonisation.' if lang=='french' else 'Colonial restrictions remain in force while we are subject to another power. Independence will allow us to choose our own colonization policy.')
        state='Nouvelle-Écosse' if lang=='french' else 'Nova Scotia'
        files[f'localization/{lang}/replace/1776_colonies_l_{lang}.yml']=b'\xef\xbb\xbf'+(f'l_{lang}:\n aor1776_proclamation_independence_tt:0 "{sentence}"\n STATE_NEW_BRUNSWICK:0 "{state}"\n').encode('utf8')
    raw=text(ROOT/ST);s=state_nodes(raw)['STATE_NEW_BRUNSWICK'];src=next(n for n in s.children('create_state') if n.one('country')=='c:NBS');dst=next(n for n in s.children('create_state') if n.one('country')=='c:NVS')
    cells=set(provs(src,'owned_provinces'))|set(provs(dst,'owned_provinces'));assert len(cells)==40
    node=dst.children('owned_provinces')[0]
    files[ST]=encoded(ROOT/ST,edit(raw,[(src.start,src.end,''),(node.start,node.end,'owned_provinces = '+rgb_block(cells))]))
    raw=text(ROOT/PP);s=state_nodes(raw)['STATE_NEW_BRUNSWICK'];src=s.children('region_state:NBS')[0];dst=s.children('region_state:NVS')[0]
    files[PP]=encoded(ROOT/PP,edit(raw,[(src.start,src.end,''),(dst.end-1,dst.end-1,'\n'+body(raw,src)+'\n')]))
    raw=text(ROOT/BB);s=state_nodes(raw)['STATE_NEW_BRUNSWICK'];src=s.children('region_state:NBS')[0];dst=s.children('region_state:NVS')[0];patch=[];append=[]
    existing={scalar(n.one('building')):n for n in dst.children('create_building')}
    for n in src.children('create_building'):
        kind=scalar(n.one('building'));new=raw[n.start:n.end].replace('c:NBS','c:NVS')
        if kind not in existing:append.append(new)
        else:
            old=existing[kind];assert signature(old)==signature(n),'Different PM/ownership/reserve needs separate treatment: '+kind
            levels=[v for v in walk(old.children()) if v.key=='levels'];assert len(levels)==1
            patch.append((levels[0].start,levels[0].end,'levels = '+str(level(n)+level(old))))
    patch += [(src.start,src.end,''),(dst.end-1,dst.end-1,'\n'+'\n'.join(append)+'\n')]
    files[BB]=encoded(ROOT/BB,edit(raw,patch))
    raw=text(ROOT/MIL);roots=list(walk(parse(raw)));src=next(n for n in roots if n.key=='c:NBS');dst=next(n for n in roots if n.key=='c:NVS')
    files[MIL]=encoded(ROOT/MIL,edit(raw,[(src.start,src.end,''),(dst.end-1,dst.end-1,'\n'+body(raw,src)+'\n')]))
    rel='common/history/diplomacy/00_subject_relationships.txt';raw=text(ROOT/rel);nodes=[n for n in walk(parse(raw)) if n.key=='create_diplomatic_pact' and n.one('country')=='c:NBS'];assert len(nodes)==1
    files[rel]=encoded(ROOT/rel,edit(raw,[(n.start,n.end,'') for n in nodes]))
    assert runtime()==initial,'Input changed while preparing'
    stage(files,dict(maritimes_provinces=40,law='law_no_colonial_affairs',unlock='Independent, not merely transferred to a different overlord',native_frontiers_complete=False))
    print('Prepared law lock and Nova Scotia merger: '+str(len(files))+' files.')


def validate():
    p=load(OUT/'PATCH.json');checks={};old=load(OUT/'BASELINE_OWNERS.json');own=ownership()
    checks['hashes']=all(sha(ROOT/r)==d for r,d in p['output_sha256'].items())
    checks['only_nbs_to_nvs_territorial_change']=all(own[r]=={(s,'NVS' if t=='NBS' else t) for s,t in v} for r,v in old.items()) and set(own)==set(old)
    checks['nova_scotia_40_provinces']=sum(any(t=='NVS' for s,t in v) for v in own.values())==40 and not any(t=='NBS' for v in own.values() for s,t in v)
    def cohorts(raw):
        out=C.Counter()
        for sid,s in state_nodes(raw).items():
            for rs in s.children():
                if rs.key.startswith('region_state:'):
                    for n in rs.children('create_pop'):out[sid,pop_signature(n)]+=int(n.one('size'))
        return out
    checks['all_populations_cultures_religions_types_preserved']=cohorts(text(ROOT/PP))==cohorts(text(OUT/'before'/PP))
    def assets(raw):
        out=C.Counter()
        for n in walk(parse(raw)):
            if n.key=='create_building':out[json.dumps(signature(n),sort_keys=True)]+=level(n)
        return out
    checks['all_building_levels_owners_pm_reserves_preserved']=assets(text(ROOT/BB))==assets(text(OUT/'before'/BB))
    def units(raw):return C.Counter(json.dumps(normalized([n]),sort_keys=True) for n in walk(parse(raw)) if n.key=='create_military_formation')
    checks['all_unit_formations_preserved']=units(text(ROOT/MIL))==units(text(OUT/'before'/MIL))
    checks['no_nbs_asset_orphans']=all('c:NBS' not in text(ROOT/r) and 'region_state:NBS' not in text(ROOT/r) for r in [BB,PP,MIL])
    raw=text(ROOT/US);checks['no_initial_frontier_colonization']='law_type:law_frontier_colonization' not in raw and 'law_type:law_no_colonial_affairs' in raw and 'institution_colonial_affairs' not in raw
    checks['colonization_knowledge_preserved']='add_technology_researched = colonization' in raw
    for n in parse(text(ROOT/LAW)):
        if n.key=='law_no_colonial_affairs':continue
        checks['enact_and_impose_block.'+n.key]=TRIGGER in text(ROOT/LAW)[n.start:n.end] and n.children('can_enact') and any(v.key==TRIGGER for v in walk(n.children('can_enact'))) and any(v.key==TRIGGER for v in walk(n.children('can_impose')))
    checks={k:bool(v) for k,v in checks.items()}
    checks.update({'hbc_'+k:v for k,v in conservation(load(OUT/'BASELINE_HBC.json'),economic_inventory()).items()})
    base=load(OUT/'BASELINE_RUNTIME.json');now=runtime();unexpected=[r for r in base.keys()|now.keys() if base.get(r)!=now.get(r) and r not in p['output_sha256']]
    checks['no_unlisted_runtime_change']=not unexpected
    dump('VALIDATION.json',dict(checks=checks,all_pass=all(checks.values()),engine_tested=False,unexpected=unexpected));print(json.dumps(checks,indent=2));return all(checks.values())


if __name__=='__main__':
    if '--prepare' in sys.argv:prepare()
    elif '--apply' in sys.argv:apply()
    elif '--validate' in sys.argv:sys.exit(0 if validate() else 1)
