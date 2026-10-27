"""Unify the two anachronistic Canadas in the 1776 Province of Quebec.

Prepare a bounded patch, check current hashes before --apply, then validate.
No restoration of shared files from Git; no vanilla or Git writes.
"""
import collections as C
import csv
import json
from pathlib import Path
import sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from audit_hbc_1776 import ROOT,GAME,effective,provs,runtime,sha
from validate_diplomacy_ottoman_1776 import parse,walk,scalar
from hbc06_integrate import text,encoded,edit,state_nodes,ownership,BASE,GROUPS
from hbc03_quebec_arc import economic_inventory,conservation,canonical
from hbc04_land_links import pair

OUT=BASE/'CANADA-01'
ST='common/history/states/00_states.txt'
POP='common/history/pops/05_north_america.txt'
BUILD='common/history/buildings/05_north_america.txt'
MIL='common/history/military_formations/01_military_formations_north_america.txt'
QUE='common/history/countries/que - quebec.txt'
CLAIMS={'STATE_OHIO','STATE_INDIANA','STATE_ILLINOIS','STATE_MICHIGAN','STATE_WISCONSIN'}
# Calibration, not a census: conventional 1775 total and a small pre-Loyalist minority.
# Existing colonial Indigenous groups are retained exactly, not taken from HBC/natives.
POPS={
 'STATE_ONTARIO':[('franco_canadian','catholic',587),('franco_canadian','protestant',13),('anglo_canadian','protestant',8),('cree','DEFAULT',238),('iroquoian','DEFAULT',77),('algonquian','DEFAULT',77)],
 'STATE_QUEBEC':[('franco_canadian','catholic',87021),('anglo_canadian','protestant',1492),('cree','DEFAULT',487)],
}


def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def dump(n,v):(OUT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def country(raw,tag):return next(n for n in walk(parse(raw)) if n.key=='c:'+tag)
def normalized(n,rename=True):
    key=n.key.replace('region_state:ONT','region_state:QUE') if rename else n.key
    val=[normalized(v,rename) for v in n.children()] if isinstance(n.value,list) else scalar(n.value)
    if rename and val=='c:ONT':val='c:QUE'
    return [key,n.op,val]
def pop_total(raw,tags):
    return sum(int(p.one('size')) for n in walk(parse(raw)) if n.key in {'region_state:'+t for t in tags} for p in n.children('create_pop'))


def prepare():
    OUT.mkdir(parents=True,exist_ok=True);assert not (OUT/'APPLIED.json').exists()
    before=runtime();own=ownership();files={};notes=[]
    assert all(conservation(load(BASE/'HBC-03/CONSERVATION_BASELINE.json'),economic_inventory()).values())
    for rel in [ST,POP,BUILD,MIL,QUE,'common/history/diplomacy/00_subject_relationships.txt','common/history/diplomacy/00_relations.txt','common/history/political_movements/00_movements.txt','common/history/ai/00_secret_goals.txt','common/history/characters/cleanup2c1 - non europe rulers 1776.txt']:
        raw=text(ROOT/rel);patch=[]
        if rel==ST:
            for s in state_nodes(raw).values():
                for n in s.children('create_state'):
                    if scalar(n.one('country',''))=='c:ONT':
                        q=n.children('country')[0];patch.append((q.start,q.end,'country = c:QUE'))
                if s.key[2:] in CLAIMS and not any(scalar(n.value)=='c:QUE' for n in s.children('add_claim')):
                    patch.append((s.end-1,s.end-1,'\n\t\tadd_claim = c:QUE\n\t'))
        elif rel==POP:
            for sid,s in state_nodes(raw).items():
                for n in s.children():
                    if n.key not in {'region_state:ONT','region_state:QUE'}:continue
                    assert sid in POPS
                    body='region_state:QUE = {\n'
                    for cu,religion,size in POPS[sid]:
                        body+=f'\t\t\tcreate_pop = {{ culture = {cu} '+('religion = '+religion+' ' if religion!='DEFAULT' else '')+f'size = {size} }}\n'
                    body+='\t\t}'
                    patch.append((n.start,n.end,body))
        elif rel==BUILD:
            regions=state_nodes(raw);src=regions['STATE_ONTARIO'].children('region_state:ONT')[0]
            srcbuild=src.children('create_building');assert len(srcbuild)==1 and scalar(srcbuild[0].one('building'))=='building_barrack'
            dest=regions['STATE_QUEBEC'].children('region_state:QUE')[0]
            barrack=next(n for n in dest.children('create_building') if scalar(n.one('building'))=='building_barrack')
            assert normalized(srcbuild[0])==normalized(barrack),'Consolidation only allowed for identical building commands except owner.'
            lev=[n for n in walk(barrack.children()) if n.key=='levels'];assert len(lev)==1 and int(lev[0].value)==5
            patch.extend([(src.start,src.end,''),(lev[0].start,lev[0].end,'levels = 10')])
        elif rel==MIL:
            src=country(raw,'ONT');dest=country(raw,'QUE');content=raw[raw.index('{',src.start)+1:src.end-1]
            content=content.replace('state_region = s:STATE_ONTARIO','state_region = s:STATE_QUEBEC').replace('name = aor_ont_garrison','name = aor1776_quebec_west_garrison')
            patch.extend([(src.start,src.end,''),(dest.end-1,dest.end-1,content)])
        elif rel==QUE:
            replacements={'law_wealth_voting':'law_autocracy','law_homesteading':'law_tenant_farmers'}
            for n in walk(parse(raw)):
                if n.key=='activate_law' and scalar(n.value).removeprefix('law_type:') in replacements:
                    patch.append((n.start,n.end,'activate_law = law_type:'+replacements[scalar(n.value).removeprefix('law_type:')]))
        elif rel.endswith('00_subject_relationships.txt'):
            for n in walk(parse(raw)):
                if n.key=='create_diplomatic_pact' and scalar(n.one('country',''))=='c:ONT':patch.append((n.start,n.end,''))
        elif rel.endswith('00_relations.txt'):
            n=country(raw,'ONT');patch.append((n.start,n.end,''))
        elif rel.endswith('00_movements.txt'):
            for t in ['ONT','QUE']:
                n=country(raw,t);patch.append((n.start,n.end,''))
        elif rel.endswith('00_secret_goals.txt'):
            for n in walk(parse(raw)):
                if n.key=='set_mutual_secret_goal' and scalar(n.one('country',''))=='c:ONT':patch.append((n.start,n.end,''))
        elif 'cleanup2c1' in rel:
            n=country(raw,'QUE');cu=next(v for v in walk(n.children()) if v.key=='culture');patch.append((cu.start,cu.end,'culture = british'))
        updated=edit(raw,patch)
        if rel.endswith('00_subject_relationships.txt'):updated=updated.replace('# Province of Upper Canada','# Province of Quebec, unified until 1791').replace('# Province of Lower Canada','# Single Quebec colonial relationship')
        if rel.endswith('00_movements.txt'):updated=updated.replace('# brewing rebellions of 1837','# The 1837 Canadian reform movements are not initialized in 1776.')
        files[rel]=encoded(ROOT/rel,updated)
    # Keep future ONT tag/history, events and formation mechanics available for later play.
    files['common/dynamic_country_names/1776_quebec_province.txt']=b'''QUE = {
 dynamic_country_name = {
  name = aor1776_province_quebec
  adjective = QUE_ADJ
  is_main_tag_only = yes
  priority = 100
  trigger = {
   NOT = { exists = c:ONT }
   exists = c:GBR
   c:GBR ?= { has_diplomatic_pact = { who = c:QUE type = colony is_initiator = yes } }
  }
 }
}
'''
    for lang,name,army,flavor in [
      ('french','Province de Québec','Garnison des Grands Lacs','La province de Québec demeure une colonie britannique, gouvernée sans assemblée élue. Le régime seigneurial et le droit civil français subsistent, tandis que la pratique du catholicisme est protégée. La révolte des Treize Colonies menace la vallée du Saint-Laurent et les postes des Grands Lacs ; habitants et gouverneur doivent décider comment défendre le pays.'),
      ('english','Province of Quebec','Great Lakes Garrison','The Province of Quebec remains a British colony governed without an elected assembly. Seigneurial tenure and French civil law endure, while Catholic worship is protected. The revolt of the Thirteen Colonies threatens the St Lawrence valley and the Great Lakes posts; inhabitants and governor must decide how to defend the province.')]:
        rel=f'localization/{lang}/1776_quebec_province_l_{lang}.yml'
        files[rel]=b'\xef\xbb\xbf'+f'l_{lang}:\n aor1776_province_quebec:0 "{name}"\n aor1776_quebec_west_garrison:0 "{army}"\n'.encode('utf8')
        rel=f'localization/{lang}/country_flavor_text_l_{lang}.yml';raw=text(ROOT/rel);lines=raw.splitlines(keepends=True)
        ids=[i for i,l in enumerate(lines) if l.lstrip().startswith('QUE_FLAVOR_TEXT:')];assert len(ids)==1
        i=ids[0];newline='\r\n' if lines[i].endswith('\r\n') else '\n';lines[i]=' QUE_FLAVOR_TEXT:0 "'+flavor+'"'+newline
        files[rel]=encoded(ROOT/rel,''.join(lines))
    dump('BASELINE_RUNTIME.json',before)
    dump('OWNERSHIP_BEFORE.json',{r:sorted(v) for r,v in own.items()})
    dump('PLAN.json',dict(date='2026-10-26',successor='QUE',inactive_initial_tag='ONT',former_ont_rgb=sorted(r for r,v in own.items() if any(t=='ONT' for s,t in v)),former_que_rgb=sorted(r for r,v in own.items() if any(t=='QUE' for s,t in v)),population_before=pop_total(text(ROOT/POP),{'ONT','QUE'}),population_after=sum(n for rows in POPS.values() for cu,re,n in rows),population_detail=POPS,claims=sorted(CLAIMS),frontier_changes='Internal ONT-QUE political border removed; outer contours retained pending finer historical mapping. Claims are not administration.',military='Two formations and ten existing irregular battalion slots retained; former ONT recruitment and five barrack levels consolidated into Quebec manpower region. Not a claim of historical troop strength.'))
    for rel,data in files.items():
        if rel.endswith('.txt'):parse(data.decode('utf-8-sig'))
        p=OUT/'patch'/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
    dump('PATCH.json',dict(input_sha256={r:before.get(r) for r in files},output_sha256={r:sha(OUT/'patch'/r) for r in files}))
    assert runtime()==before,'Concurrent edits detected during preparation.'
    print('Prepared',len(files),'files; population',98000,'->',90000)


def apply():
    assert not (OUT/'APPLIED.json').exists();p=load(OUT/'PATCH.json')
    for rel,before in p['input_sha256'].items():
        target=ROOT/rel;assert (sha(target) if target.exists() else None)==before,rel+' changed'
        assert sha(OUT/'patch'/rel)==p['output_sha256'][rel]
    for rel in p['input_sha256']:
        target=ROOT/rel
        if target.exists():
            backup=OUT/'before'/rel;backup.parent.mkdir(parents=True,exist_ok=True);backup.write_bytes(target.read_bytes())
        target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((OUT/'patch'/rel).read_bytes())
    dump('APPLIED.json',dict(status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',engine_tested=False,files=p['output_sha256']))
    validate()


def validate():
    p=load(OUT/'PATCH.json');plan=load(OUT/'PLAN.json');before=load(OUT/'BASELINE_RUNTIME.json');after=runtime();own=ownership();old={r:{tuple(v) for v in vs} for r,vs in load(OUT/'OWNERSHIP_BEFORE.json').items()};checks={}
    checks['files_match_reviewed_patch']=all(sha(ROOT/r)==v for r,v in p['output_sha256'].items())
    checks['only_authorized_runtime_files_changed']={r for r in before.keys()|after.keys() if before.get(r)!=after.get(r)}==set(p['output_sha256'])
    expected={r:{(s,'QUE' if t=='ONT' else t) for s,t in vs} for r,vs in old.items()}
    checks['world_ownership_exact_except_ont_successor']=own==expected
    checks['no_ont_initial_territory']=not any(t=='ONT' for vs in own.values() for s,t in vs)
    checks['all_transferred_provinces_single_owner']=all(len(own[r])==1 for r in plan['former_ont_rgb']+plan['former_que_rgb'])
    checks['population_exactly_90000']=pop_total(text(ROOT/POP),{'ONT','QUE'})==90000
    checks['world_population_delta_minus_8000']=pop_total(text(ROOT/POP),{'ONT','QUE'})-plan['population_before']==-8000
    # Every non-colonial block is unchanged, including HBC and the inflated native scenario.
    def other_pops(raw):return [normalized(n,False) for n in walk(parse(raw)) if n.key.startswith('region_state:') and n.key not in {'region_state:ONT','region_state:QUE'}]
    checks['all_other_population_blocks_preserved']=other_pops(text(OUT/'before'/POP))==other_pops(text(ROOT/POP))
    checks.update(conservation(load(BASE/'HBC-03/CONSERVATION_BASELINE.json'),economic_inventory()))
    checks['native_scenario_untouched']=all(after[r]==v for r,v in before.items() if '1776_hbc_indigenous' in r)
    # Material conservation for buildings, with only the two identical barracks consolidated.
    def buildings(raw):
        result=[]
        for s in state_nodes(raw).values():
            for rs in s.children():
                if rs.key in {'region_state:ONT','region_state:QUE'}:
                    for n in rs.children('create_building'):result.append((s.key,scalar(n.one('building')),normalized(n)))
        return result
    oldb=buildings(text(OUT/'before'/BUILD));newb=buildings(text(ROOT/BUILD))
    checks['all_non_barrack_economy_preserved']=[r for r in oldb if r[1]!='building_barrack']==[r for r in newb if r[1]!='building_barrack']
    oldslots=sum(int(n.value) for s in state_nodes(text(OUT/'before'/BUILD)).values() for rs in s.children() if rs.key in {'region_state:ONT','region_state:QUE'} for b in rs.children('create_building') if scalar(b.one('building'))=='building_barrack' for n in walk(b.children()) if n.key=='levels')
    newslots=sum(int(n.value) for s in state_nodes(text(ROOT/BUILD)).values() for rs in s.children() if rs.key=='region_state:QUE' for b in rs.children('create_building') if scalar(b.one('building'))=='building_barrack' for n in walk(b.children()) if n.key=='levels')
    checks['ten_barrack_levels_preserved']=oldslots==newslots==10
    checks['no_orphan_ont_buildings']=not any('region_state:ONT' in text(q) or 'c:ONT' in text(q) for q in effective('common/history/buildings'))
    def troops(raw,tags):return sum(int(n.one('count',0)) for c in walk(parse(raw)) if c.key in {'c:'+t for t in tags} for n in walk(c.children()) if n.key=='combat_unit')
    checks['ten_battalion_slots_preserved']=troops(text(OUT/'before'/MIL),{'ONT','QUE'})==troops(text(ROOT/MIL),{'QUE'})==10
    checks['no_orphan_ont_formations']='c:ONT' not in text(ROOT/MIL)
    subjects=[n for n in walk(parse(text(ROOT/'common/history/diplomacy/00_subject_relationships.txt'))) if n.key=='create_diplomatic_pact' and scalar(n.one('country','')) in {'c:ONT','c:QUE'}]
    checks['single_quebec_colony_pact']=len(subjects)==1 and scalar(subjects[0].one('country'))=='c:QUE' and scalar(subjects[0].one('type'))=='colony'
    checks['no_1837_canadian_movements']=not any(n.key in {'c:ONT','c:QUE'} for n in walk(parse(text(ROOT/'common/history/political_movements/00_movements.txt'))))
    laws={scalar(n.value) for n in walk(parse(text(ROOT/QUE))) if n.key=='activate_law'}
    checks['unelected_government_and_tenure']='law_type:law_autocracy' in laws and 'law_type:law_wealth_voting' not in laws and 'law_type:law_tenant_farmers' in laws
    checks['claims_present_without_annexation']=all(any(scalar(n.value)=='c:QUE' for n in state_nodes(text(ROOT/ST))[s].children('add_claim')) for s in CLAIMS)
    witness=load(BASE/'HBC-04/PIXEL_PATH_WITNESS.json')
    labels=[next(iter(own[r['rgb']]))[1] for r in witness]
    checks['protected_military_country_chain']=list(dict.fromkeys(labels))==['HBC','QUE','USA']
    checks['bitmap_terrains_hubs_unchanged']=all(after[r]==v for r,v in before.items() if r.startswith(('map_data/','gfx/map/')))
    checks['localization_bom']=all((ROOT/r).read_bytes().startswith(b'\xef\xbb\xbf') for r in p['output_sha256'] if r.endswith('.yml'))
    dump('VALIDATION.json',dict(checks=checks,all_pass=all(checks.values()),engine_tested=False,status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION'));print(json.dumps(checks,indent=2));assert all(checks.values()),checks
    render(own)


def render(own):
    b=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32);a=(b[:,:,0]<<16)|(b[:,:,1]<<8)|b[:,:,2]
    canvas=np.full((*a.shape,3),[37,48,58],dtype=np.uint8);canvas[np.isin(a,[int(r[1:],16) for r in own])]=[100,112,109]
    colors={g[0]:g[5] for g in GROUPS}|{'QUE':[98,148,190],'HBC':[235,183,50],'USA':[171,89,89]}
    for tag,color in colors.items():canvas[np.isin(a,[int(r[1:],16) for r,v in own.items() if any(t==tag for s,t in v)])]=color
    edge=np.zeros(a.shape,bool);edge[1:]|=a[1:]!=a[:-1];edge[:,1:]|=a[:,1:]!=a[:,:-1];canvas[edge&np.isin(a,[int(r[1:],16) for r in own])]=[45,49,48]
    crop=Image.fromarray(canvas[725:1130,2020:2800]).resize((1560,810),Image.Resampling.NEAREST);sheet=Image.new('RGB',(1560,950),'#25303a');sheet.paste(crop,(0,90));d=ImageDraw.Draw(sheet);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',25);sm=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',19)
    d.text((15,10),'1776 — une seule province de Québec britannique',font=font,fill='white');d.text((15,49),'Bleu : province réunifiée ; jaune : HBC ; autres couleurs : peuples décentralisés ; rouge : Treize Colonies.',font=sm,fill='white')
    d.text((15,910),'90 000 habitants dans la colonie ; frontières extérieures conservées, limites fines et occupation militaire à reprendre.',font=sm,fill='white');sheet.save(OUT/'QUEBEC_1776.png')


if __name__=='__main__':
    if '--prepare' in sys.argv:prepare()
    elif '--apply' in sys.argv:apply()
    elif '--validate' in sys.argv:validate()
    else:raise SystemExit('Use --prepare, --apply or --validate.')
