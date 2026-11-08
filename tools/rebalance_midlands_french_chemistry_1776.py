"""Current-file patch: one British steel level, French chemical PMs, seeded lead trade and farm fertilizer demand."""
import argparse, collections as C, hashlib, json, re, shutil, sys
from pathlib import Path
from datetime import datetime, timezone
import audit_anzin_regional_infrastructure as a
import audit_starting_tech_1776 as tech
import validate_starting_technology_1776 as contract
from validate_diplomacy_ottoman_1776 import parse, walk, normalized, scalar

ROOT=a.ROOT; GAME=a.GAME
OUT=ROOT/'docs/reports/economy/MIDLANDS_FRENCH_CHEMISTRY_FERTILIZER_1776'
WEST='common/history/buildings/00_west_europe.txt'
WORLD='common/history/buildings/98_build_start_1776_world_redistribution.txt'
AGRO='common/production_methods/02_agro.txt'
TRADE='common/history/trade/99_1776_british_lead_french_chemistry.txt'
TIERS={'pm_soil_enriching_farming':(5,10),'pm_fertilization':(10,15),'pm_chemical_fertilizer':(15,20),
 'pm_soil_enriching_farming_building_rice_farm':(10,20),
 'pm_fertilization_building_rice_farm':(20,30),'pm_chemical_fertilizer_building_rice_farm':(30,40)}
TARGETS=[WORLD,WEST,AGRO,TRADE]

def dump(name,obj):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def load(name):return json.loads((OUT/name).read_text(encoding='utf8'))
def rewrite(s,ops):
    for lo,hi,text in sorted(ops,reverse=True):s=s[:lo]+text+s[hi:]
    return s
def part(s,state,tag):
    nodes=[n for n in walk(parse(s)) if n.key=='s:'+state]
    selected=[x for n in nodes for x in n.children('region_state:'+tag)]
    assert len(selected)==1,(state,tag,len(selected))
    return selected[0]
def building(n,key):
    nodes=[x for x in n.children('create_building') if scalar(x.one('building'))==key]
    assert len(nodes)==1,(key,len(nodes))
    return nodes[0]
def levels(n):return sum(int(x.value) for x in walk([n]) if x.key=='levels')
def protected_hashes():
    paths=[p for folder in ['common','events','gui','localization','map_data'] for p in (ROOT/folder).rglob('*.txt')]
    paths += [ROOT/'docs/reports/map/SERG_CLOSURE'/name for name in ['ROADMAP.md','ROADMAP_STATE.json','NEXT_ACTION.md','BLOCKERS.md','PROGRESS_HISTORY.md']]
    return {p.relative_to(ROOT).as_posix():a.sha(p) for p in paths if p.is_file()}
def building_inventory():
    rows=[]
    for p in tech.effective('common/history/buildings'):
        s=a.raw(p)
        for st in walk(parse(s)):
            if not st.key.startswith('s:STATE_'):continue
            for owner in st.children():
                if not owner.key.startswith('region_state:'):continue
                for n in owner.children('create_building'):
                    rows.append(dict(file=tech.ref(p),state=st.key[2:],owner=owner.key.split(':')[1],kind=scalar(n.one('building')),levels=levels(n),pms=[scalar(x) for x in a.ids(n,'activate_production_methods')],signature=normalized([n])))
    return rows
def steel(rows):return {sid:sum(x['levels'] for x in rows if x['owner']=='GBR' and x['kind']=='building_steel_mill' and x['state']==sid) for sid in ['STATE_YORKSHIRE','STATE_MIDLANDS']}

def plan():
    result={};s=a.raw(ROOT/WORLD)
    source=building(part(s,'STATE_YORKSHIRE','GBR'),'building_steel_mill')
    assert levels(source)==2
    level=next(n for n in walk([source]) if n.key=='levels');before=s[source.start:source.end]
    source1=re.sub(r'(levels\s*=\s*)2\b',r'\g<1>1',before,count=1)
    assert source1!=before
    # Physical location changes; the original Yorkshire financial-district owner stays identical.
    destination=part(s,'STATE_MIDLANDS','GBR');assert not any(scalar(n.one('building'))=='building_steel_mill' for n in destination.children('create_building'))
    result[WORLD]=rewrite(s,[(source.start,source.end,source1),(destination.end-1,destination.end-1,'\n'+source1+'\n')])
    s=a.raw(ROOT/WEST);chemical=building(part(s,'STATE_NORMANDY','FRA'),'building_chemical_plant')
    selection=chemical.children('activate_production_methods')[0]
    assert 'pm_no_fertilizer_production' in selection.value[0].value
    fragment=s[selection.start:selection.end];assert '"pm_lead_chamber_process"' in fragment
    result[WEST]=rewrite(s,[(selection.start,selection.end,fragment.replace('"pm_no_fertilizer_production"','"pm_artificial_fertilizers"'))])
    s=a.raw(ROOT/AGRO);ops=[];price=float(a.catalog('common/goods')['fertilizer'][0].one('cost'))
    for key,(old,new) in TIERS.items():
        n=next(n for n in parse(s) if n.key==key);fields=[c for c in walk([n]) if c.key=='goods_input_fertilizer_add']
        assert len(fields)==1 and int(fields[0].value)==old,(key,fields)
        text=s[n.start:n.end]
        def replacement(m):
            tail=re.sub(r'#\s*\d+',lambda c:'# '+str(int(new*price)),m[3])
            return m[1]+str(new)+tail
        changed=re.sub(r'(goods_input_fertilizer_add\s*=\s*)(\d+)([^\r\n]*)',replacement,text,count=1)
        ops.append((n.start,n.end,changed))
    result[AGRO]=rewrite(s,ops)
    result[TRADE]='''TRADE = {
 # Opening commercial orders, using the native world-market initialization.
 s:STATE_WEST_COUNTRY = {
  region_state:GBR = { sg:lead = { add_exports = 5 } }
 }
 s:STATE_NORMANDY = {
  region_state:FRA = { sg:lead = { add_imports = 5 } }
 }
}
'''
    return result

def install():
    assert not (OUT/'BASELINE.json').exists(),'Existing receipt must not be overwritten.'
    hashes=protected_hashes();expected=plan();rows=building_inventory()
    for rel in expected:
        if rel in hashes:assert a.sha(ROOT/rel)==hashes[rel],('Concurrent change',rel)
        else:assert not (ROOT/rel).exists(),('New file collision',rel)
    base=dict(utc=datetime.now(timezone.utc).isoformat(),git=a.git_state(),hashes=hashes,buildings_before=rows,
      planned={r:hashlib.sha256(s.encode('utf8')).hexdigest() for r,s in expected.items()},
      vanilla={p.relative_to(GAME).as_posix():a.sha(p) for p in [GAME/'common/history/trade/00_historical_trade.txt',GAME/'common/production_methods/02_agro.txt']},
      user_rice_choice='Conserver l’écart du riz : 20 / 30 / 40',world_market_note='Initial imports/exports, not a permanent bilateral treaty or a fabricated historical trade agreement.')
    for rel in expected:
        if (ROOT/rel).exists():
            p=OUT/'preimages'/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,p)
    dump('BASELINE.json',base)
    for rel,s in expected.items():
        p=ROOT/rel
        if rel in hashes:assert a.sha(p)==hashes[rel],('Concurrent change before write',rel)
        else:assert not p.exists()
        bom=b'\xef\xbb\xbf' if p.exists() and p.read_bytes().startswith(b'\xef\xbb\xbf') else b''
        p.write_bytes(bom+s.encode('utf8'))
    dump('INSTALLED.json',dict(files={r:a.sha(ROOT/r) for r in expected},status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',runtime='NOT_RUN'))
    print('Installed four bounded runtime files.',flush=True)

def validate():
    base=load('BASELINE.json');installed=load('INSTALLED.json');checks=[]
    def ck(name,ok,detail=None):checks.append(dict(name=name,passed=bool(ok),detail=detail))
    for r,h in installed['files'].items():
        ck('installed_hash.'+r,a.sha(ROOT/r)==h)
        try:parse(a.raw(ROOT/r));ok=True
        except Exception:ok=False
        ck('syntax.'+r,ok)
    current=protected_hashes();allowed=set(installed['files'])
    changed=[r for r,h in base['hashes'].items() if r not in allowed and current.get(r)!=h]
    added=[r for r in current if r not in allowed and r not in base['hashes']]
    ck('all_unrelated_scripts_map_tech_recipes_and_SERG_preserved',not changed and not added,dict(changed=changed,added=added))
    ck('git_unchanged',base['git']==a.git_state())
    for r,h in base['vanilla'].items():ck('vanilla_unchanged.'+r,a.sha(GAME/r)==h)
    before=base['buildings_before'];after=building_inventory();bs=steel(before);now=steel(after)
    ck('Yorkshire_one_level_removed',now['STATE_YORKSHIRE']==bs['STATE_YORKSHIRE']-1)
    ck('Midlands_one_level_added',now['STATE_MIDLANDS']==bs['STATE_MIDLANDS']+1)
    ck('GBR_total_steel_levels_preserved',sum(x['levels'] for x in before if x['kind']=='building_steel_mill' and x['owner']=='GBR')==sum(x['levels'] for x in after if x['kind']=='building_steel_mill' and x['owner']=='GBR'))
    # Comparing the rest of the shared file bytes after undoing only this transfer protects concurrent content.
    old=a.raw(OUT/'preimages'/WORLD);s=a.raw(ROOT/WORLD)
    dst=building(part(s,'STATE_MIDLANDS','GBR'),'building_steel_mill');src=building(part(s,'STATE_YORKSHIRE','GBR'),'building_steel_mill')
    owner_fields=lambda n:normalized(n.children('add_ownership'))
    ck('steel_PM_and_owner_of_moved_level_preserved',normalized([dst])==normalized([src]))
    src2=re.sub(r'(levels\s*=\s*)1\b',r'\g<1>2',s[src.start:src.end],count=1)
    restored=rewrite(s,[(src.start,src.end,src2),(dst.start-1,dst.end+1,'')])
    ck('world_building_file_outside_transfer_byte_identical',restored==old)
    old=a.raw(OUT/'preimages'/WEST);s=a.raw(ROOT/WEST)
    chem_sel=building(part(s,'STATE_NORMANDY','FRA'),'building_chemical_plant').children('activate_production_methods')[0]
    undone=rewrite(s,[(chem_sel.start,chem_sel.end,s[chem_sel.start:chem_sel.end].replace('"pm_artificial_fertilizers"','"pm_no_fertilizer_production"'))])
    ck('France_only_fertilizer_activation_changed',undone==old)
    chemical=building(part(s,'STATE_NORMANDY','FRA'),'building_chemical_plant')
    cpms=[scalar(x) for x in a.ids(chemical,'activate_production_methods')]
    ck('France_chemical_both_productions_active','pm_artificial_fertilizers' in cpms and 'pm_lead_chamber_process' in cpms and levels(chemical)==1)
    oldnodes={n.key:n for n in parse(a.raw(OUT/'preimages'/AGRO))};newnodes={n.key:n for n in parse(a.raw(ROOT/AGRO))}
    ck('agro_catalog_identifiers_unchanged',set(oldnodes)==set(newnodes))
    for key,n in newnodes.items():
        if key in TIERS:
            fields=[c for c in walk([n]) if c.key=='goods_input_fertilizer_add'];ck('fertilizer_tier.'+key,len(fields)==1 and int(fields[0].value)==TIERS[key][1])
            fields[0].value=str(TIERS[key][0])
        ck('other_agricultural_recipe_fields_unchanged.'+key,normalized([n])==normalized([oldnodes[key]]))
    trade=parse(a.raw(ROOT/TRADE))[0];exports=part(a.raw(ROOT/TRADE),'STATE_WEST_COUNTRY','GBR').children('sg:lead')[0]
    imports=part(a.raw(ROOT/TRADE),'STATE_NORMANDY','FRA').children('sg:lead')[0]
    ck('opening_lead_export_5',exports.one('add_exports')=='5')
    ck('opening_lead_import_5',imports.one('add_imports')=='5')
    ck('no_bilateral_treaty_or_treasury_gift',all(n.key not in ['create_treaty','add_treasury'] for n in walk([trade])))
    # Reuse the repository's effective starting-technology collector without granting technologies.
    snap=contract.collect_snapshot();compat=[]
    for tag,state,kind in [('GBR','STATE_MIDLANDS','building_steel_mill'),('FRA','STATE_NORMANDY','building_chemical_plant')]:
        known=set(snap['starts'][tag]['technologies']);bn=snap['buildings'][kind]
        missing_build=set(tech.values(bn,'unlocking_technologies'))-known
        ck('construction_tech.'+tag+'.'+kind,not missing_build,sorted(missing_build))
        selected=snap['selected'][(state,tag,kind)]
        for group,pm in selected.items():
            missing=set(tech.values(snap['pms'][pm],'unlocking_technologies'))-known
            ck('selected_PM_tech.'+tag+'.'+pm,not missing,sorted(missing))
        compat.append(dict(TAG=tag,state=state,building=kind,known=sorted(known),selected=selected,missing_build=sorted(missing_build)))
    dump('TARGET_TECH_COMPATIBILITY.json',compat)
    demand=5.;fert_output=40.;steel_output=40.;lead_mine_level_output=20.
    dump('ECONOMIC_ESTIMATES.json',dict(units='Units of goods per week, one level, full workforce, before throughput/other PM modifiers.',
       moved_steel=dict(input_iron=25,input_coal=25,output_steel=steel_output,tooling_steel_input_per_level=3),
       french_chemical=dict(input_lead=demand,input_sulfur=10,input_coal=10,input_tools=10,input_limestone=20,output_industrial_chemicals=40,output_fertilizer=fert_output,base_price_gross_margin_before_wages=1000),
       British_lead_export_share_of_five_West_Country_mines=demand/(5*lead_mine_level_output),
       extra_fertilizer_input=dict(wheat_rye_maize_millet=5,rice=10),extra_fertilizer_cost_at_base_price=dict(wheat_rye_maize_millet=150,rice=300),
       limits='No guaranteed employment, profit, exact matched seller or long-term fixed trade quantity. Runtime market clearing, MAPI, wages, tariffs, shipping costs and AI rebalancing remain active.'))
    result=dict(status='PASS_STATIC' if all(x['passed'] for x in checks) else 'FAIL_STATIC',passed=sum(x['passed'] for x in checks),total=len(checks),checks=checks,steel_declared_levels_before=bs,steel_declared_levels_after=now,runtime='NOT_RUN')
    dump('STATIC_CHECKS.json',result);print(result['status'],result['passed'],'/',result['total'],[x for x in checks if not x['passed']],flush=True)
    return 0 if result['status']=='PASS_STATIC' else 1

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('mode',choices=['install','validate']);args=ap.parse_args()
    if args.mode=='install':install()
    else:sys.exit(validate())
