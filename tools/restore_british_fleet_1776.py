"""Restore documented pre-budget fleet counts, then modernize 30% of cheap hulls.

Preserves current commanders, stations, armies and all foreign fleets. Not a rank
or budget simulation; staffing and prestige require a fresh game.
"""
from pathlib import Path
import argparse,collections as C,difflib,json,math
import audit_arable_population_1776 as a
import audit_british_colonial_start as n
from hbc06_integrate import edit,encoded

ROOT=a.ROOT
OUT=ROOT/'docs/reports/navy/GBR_RESTORATION_2026_10_29'
ORIGINAL=ROOT/'.asset-cache/british_colonial_start_2026-10-08/baseline.json'
FLEETS='common/history/military_formations/00_military_formations_europe.txt'
BUILDINGS='common/history/buildings/00_west_europe.txt'
CONVERSIONS={'ship_type_caravel':'ship_type_ship_of_the_line','ship_type_galley':'ship_type_frigate'}

def dump(name,obj):
 OUT.mkdir(parents=True,exist_ok=True);(OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

def allocation(total,weights):
 if total<0 or not weights or sum(weights)<=0:raise ValueError('Invalid allocation')
 denominator=sum(weights);out=[total*w//denominator for w in weights]
 for i in sorted(range(len(weights)),key=lambda i:(-(total*weights[i]%denominator),i))[:total-sum(out)]:out[i]+=1
 assert sum(out)==total
 return out

def restoration(current,original_total):
 result=C.Counter(dict(current));extra=original_total-sum(result.values())
 if extra<0:raise ValueError('Restoration would remove existing ships')
 cheap=list(CONVERSIONS)
 if extra:
  for typ,v in zip(cheap,allocation(extra,[result[k] for k in cheap])):result[typ]+=v
 return result

def modernize(restored):
 result=[c.copy() for c in restored];rates={}
 for cheap,modern in CONVERSIONS.items():
  weights=[c[cheap] for c in restored];count=sum(weights);quota=math.floor(count*.30+.5)
  moved=allocation(quota,weights)
  for target,v in zip(result,moved):target[cheap]-=v;target[modern]+=v
  rates[cheap]={'before_conversion':count,'converted':quota,'percent':100*quota/count if count else 0}
 return result,rates

def objects(folder):
 out={}
 for p in a.core.effective(folder):
  for q in a.parse(p.read_text(encoding='utf-8-sig')):out[q.key.removeprefix('REPLACE_OR_CREATE:').removeprefix('REPLACE:')]=q
 return out

def crew(ships,types,mods):
 total=0
 for kind,count in ships.items():
  q=types[kind];base=sum(a.num(x.one('ship_crew_max_add')) for x in q.children('modifier'));mult=0
  for group in q.children('default_modifications'):
   for slot in group.children():
    mod=mods[a.scalar(slot.value)]
    for block in mod.children('modifier'):
     base+=a.num(block.one('ship_crew_max_add'));mult+=a.num(block.one('ship_crew_max_mult'))
  total+=math.ceil(base*(1+mult)/100)*100*count
 return int(total)

def totals(rows):return sum((C.Counter(dict(r['ships'])) for r in rows),C.Counter())

def runtime():
 return {p.relative_to(ROOT).as_posix():a.digest(p) for folder in ['common','events','gui','gfx','map_data','localization'] for p in (ROOT/folder).rglob('*') if p.is_file()}

def prepare():
 assert not (OUT/'PLAN.json').exists(),'Preserve prior proof'
 prior=json.loads(ORIGINAL.read_text());old={r['name']:r for r in n.fleets(prior['naval_raws']) if r['owner']=='GBR'}
 raw=(ROOT/FLEETS).read_text(encoding='utf-8-sig');allfleets=n.fleets({FLEETS:raw});rows=[r for r in allfleets if r['owner']=='GBR']
 assert len(rows)==len(old)==7 and {r['name'] for r in rows}==set(old)
 original_counts=[sum(v for k,v in old[r['name']]['ships']) for r in rows]
 assert sum(original_counts)==120 and sum(totals(rows).values())==97
 restored=[restoration(r['ships'],count) for r,count in zip(rows,original_counts)]
 targets,rates=modernize(restored);changes=[];table=[]
 for r,count,mid,target in zip(rows,original_counts,restored,targets):
  assert sum(target.values())==count
  sequence=[(t,target[t]) for t in ['ship_type_frigate','ship_type_caravel','ship_type_ship_of_the_line','ship_type_galley'] if target[t]>0]
  changes.append((r['start'],r['end'],n.replace_ships(r['text'],sequence)))
  table.append({'fleet':r['name'],'before':dict(r['ships']),'restored_before_conversion':dict(mid),'after':dict(target),'total_before':sum(v for k,v in r['ships']),'total_after':count})
 after_fleets=encoded(ROOT/FLEETS,edit(raw,changes))
 types=objects('common/ship_types');mods=objects('common/ship_modifications');tech=n.technology_sets()['GBR']
 wanted=sum(targets,C.Counter());before=totals(rows);crew_before=crew(before,types,mods);crew_after=crew(wanted,types,mods)
 requirements={kind:a.vals(types[kind],'unlocking_technologies') for kind in wanted}
 assert all(not req or any(k in tech for k in req) for req in requirements.values())
 # Match the already loaded 28 fully staffed domestic levels. Overseas recruitment
 # at Gibraltar was incomplete; no dependence on it for minimum crew coverage.
 cat=a.Catalog();states=a.startup(cat)
 domestic=[r for r in states if r['owner']=='GBR' and r['state'] in ['STATE_HOME_COUNTIES','STATE_LANCASHIRE','STATE_WEST_COUNTRY']]
 domestic_levels=sum(d['levels'] for r in domestic for b in r['buildings'] if b['building']=='building_naval_administration' for d in b['declarations'])
 assert domestic_levels==28
 define=(ROOT/'common/defines/00_defines.txt').read_text(encoding='utf-8-sig')
 import re
 capacity=int(re.search(r'SAILORS_PER_BUILDING_LEVEL\s*=\s*(\d+)',define)[1]);assert capacity==1000
 add=max(0,math.ceil(crew_after/capacity)-int(domestic_levels))
 path=ROOT/BUILDINGS;building_raw=path.read_text(encoding='utf-8-sig');rs=a.state_nodes(building_raw)['STATE_HOME_COUNTIES'].children('region_state:GBR');assert len(rs)==1
 bs=[q for q in rs[0].children('create_building') if a.scalar(q.one('building'))=='building_naval_administration'];assert len(bs)==1
 b=bs[0];old_level,method=a.declared_levels(b);assert old_level==15
 fields=[q for q in a.walk(b.children()) if q.key=='levels'];assert len(fields)==1
 after_buildings=encoded(path,edit(building_raw,[(fields[0].start,fields[0].end,'levels='+str(int(old_level)+add))]))
 assert 'state_dockyard_systems' in tech
 staged={FLEETS:after_fleets,BUILDINGS:after_buildings};files=[];diff=[]
 for rel,value in staged.items():
  p=ROOT/rel;pre=OUT/'preimages'/rel;st=OUT/'staged'/rel;pre.parent.mkdir(parents=True,exist_ok=True);st.parent.mkdir(parents=True,exist_ok=True);pre.write_bytes(p.read_bytes());st.write_bytes(value)
  files.append({'file':rel,'before_sha256':a.digest(p),'after_sha256':a.digest(st)})
  diff+=list(difflib.unified_diff(p.read_text(encoding='utf-8-sig').splitlines(True),value.decode('utf-8-sig').splitlines(True),fromfile=rel+' BEFORE',tofile=rel+' AFTER'))
 dump('PLAN.json',{'status':'PREPARED_AUTHORIZED','original_reference':str(ORIGINAL.relative_to(ROOT)),'original_reference_sha256':a.digest(ORIGINAL),'original_gbr_total':120,'fleets':table,'conversion_rates':rates,'before_totals':dict(before),'after_totals':dict(wanted),'crew_before':crew_before,'crew_after':crew_after,'domestic_naval_levels_before':domestic_levels,'domestic_naval_levels_added':add,'home_counties_before':old_level,'home_counties_after':old_level+add,'domestic_crew_capacity_after':(domestic_levels+add)*capacity,'total_naval_levels_after':32+add,'technologies_available':True,'type_technology_requirements':requirements,'files':files,'game_rank_guaranteed':False,'budget_balance_after_measured':False})
 dump('RUNTIME_BASELINE.json',runtime());(OUT/'CHANGES.diff').write_text(''.join(diff),encoding='utf8')
 print(json.dumps({'before':dict(before),'after':dict(wanted),'crew_before':crew_before,'crew_after':crew_after,'added_naval_levels':add,'conversion_rates':rates}))

def apply():
 assert not (OUT/'APPLIED.json').exists(),'Already installed'
 d=json.loads((OUT/'PLAN.json').read_text());base=json.loads((OUT/'RUNTIME_BASELINE.json').read_text())
 for p,h in base.items():assert a.digest(ROOT/p)==h,('Concurrent runtime edit; review before installation',p)
 for f in d['files']:
  p=ROOT/f['file'];assert a.digest(p)==f['before_sha256'];assert a.digest(OUT/'staged'/f['file'])==f['after_sha256']
 for f in d['files']:(ROOT/f['file']).write_bytes((OUT/'staged'/f['file']).read_bytes())
 dump('APPLIED.json',{'status':'IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION','files':d['files'],'scope':'GBR fleet counts and domestic crew capacity only','rank_confirmed_in_game':False,'budget_measured_after_change':False})
 validate()

def validate():
 d=json.loads((OUT/'PLAN.json').read_text());base=json.loads((OUT/'RUNTIME_BASELINE.json').read_text());allowed={f['file'] for f in d['files']}
 checks={'exactly_two_runtime_files_changed':{p for p,h in base.items() if a.digest(ROOT/p)!=h}==allowed,'installed_hashes_match':all(a.digest(ROOT/f['file'])==f['after_sha256'] for f in d['files'])}
 before=(OUT/'preimages'/FLEETS).read_text(encoding='utf-8-sig');after=(ROOT/FLEETS).read_text(encoding='utf-8-sig');brows=n.fleets({FLEETS:before});arows=n.fleets({FLEETS:after})
 bf=[r for r in brows if r['owner']=='GBR'];af=[r for r in arows if r['owner']=='GBR']
 checks['restored_120_ships']=sum(totals(af).values())==120
 checks['each_station_restored_original_total']=all(sum(v for k,v in r['ships'])==t['total_after'] for r,t in zip(af,d['fleets']))
 checks['conversion_types_and_counts']=dict(totals(af))==d['after_totals']
 checks['foreign_fleets_unchanged']=[r['text'] for r in brows if r['owner']!='GBR']==[r['text'] for r in arows if r['owner']!='GBR']
 def remove_ships(text):
  return edit(text,[(q.start,q.end,'') for q in a.walk(a.parse(text)) if q.key=='ship'])
 def normalized(text):return ''.join(n.catalog.clean_comments(text).split())
 checks['armies_commanders_hq_supply_hubs_and_scopes_unchanged']=normalized(remove_ships(before))==normalized(remove_ships(after))
 old=(OUT/'preimages'/BUILDINGS).read_text(encoding='utf-8-sig');new=(ROOT/BUILDINGS).read_text(encoding='utf-8-sig')
 rs=a.state_nodes(old)['STATE_HOME_COUNTIES'].children('region_state:GBR')[0];b=next(q for q in rs.children('create_building') if a.scalar(q.one('building'))=='building_naval_administration');field=next(q for q in a.walk(b.children()) if q.key=='levels')
 checks['only_home_naval_level_changed']=edit(old,[(field.start,field.end,'levels='+str(int(d['home_counties_after'])))])==new
 checks['domestic_potential_covers_crews']=d['domestic_crew_capacity_after']>=d['crew_after']
 tech=n.technology_sets()['GBR'];checks['required_ship_technologies_available']=all(not req or any(x in tech for x in req) for req in d['type_technology_requirements'].values())
 dump('VALIDATION.json',{'status':'PASS_STATIC_ONLY' if all(checks.values()) else 'FAIL','checks':checks,'runtime_files_preserved':len(base)-len(allowed),'new_game_validated':False,'budget_and_global_rank_not_measured':True})
 print(json.dumps(checks));assert all(checks.values())

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['prepare','apply','validate']);globals()[p.parse_args().action]()
