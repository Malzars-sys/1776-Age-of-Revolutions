"""Validate the staged/installed frontier patch against its captured baseline."""
from northwest01 import *
from louisiana01_verify import region_capacity
from hbc04_land_links import flood,path

def native_owners(raw):
 out=C.defaultdict(set)
 for sid,n in state_nodes(raw).items():
  for z in n.children('create_state'):
   for r in provs(z,'owned_provinces'):out['x'+r[1:].upper()].add((sid,scalar(z.one('country'))[2:]))
 return out

def assets(raw):
 return sorted(json.dumps(normalized([n]),sort_keys=True) for n in walk(parse(raw)) if n.key=='create_building')

def main(staged=False):
 plan=load(OUT/'PLAN.json');p=load(OUT/'PATCH.json');base=load(OUT/'BASELINE_RUNTIME.json');now=runtime();checks={}
 def source(r):return OUT/'patch'/r if staged and r in p['output_sha256'] else ROOT/r
 def get(r):return text(source(r))
 def before(r):return text(ROOT/r) if staged else text(OUT/'before'/r)
 checks['hashes_current']=all(now.get(r)==h for r,h in p['input_sha256' if staged else 'output_sha256'].items())
 checks['patch_hashes_current']=all(sha(OUT/'patch'/r)==h for r,h in p['output_sha256'].items())
 external=load(OUT/'CONCURRENT_FILES.json') if (OUT/'CONCURRENT_FILES.json').exists() else {}
 checks['unlisted_runtime_files_unchanged']=all(now.get(r)==base.get(r) or (r in external and now.get(r)==external[r]['observed_sha256']) for r in base.keys()|now.keys() if r not in p['output_sha256'])
 checks['recorded_external_work_preserved']=all(now.get(r)==v['observed_sha256'] for r,v in external.items())
 checks['all_modified_text_parses']=all(parse(get(r)) is not None for r in p['output_sha256'] if r.endswith('.txt'))
 old={r:set(map(tuple,v)) for r,v in load(OUT/'BASELINE_OWNERS.json').items()};actual=native_owners(get(ST));desired={r['rgb']:(r['state'],r['after']) for r in plan['rows']}
 checks['target_ownership_exact']=all(actual.get(r)=={v} for r,v in desired.items())
 checks['ownership_unchanged_outside_scope']=all(actual[r]==v for r,v in old.items() if r not in desired) and set(actual)-set(old)=={plan['new_province']['rgb']}
 checks['no_new_duplicate_owner']=not ({r for r,v in actual.items() if len(v)>1}-{r for r,v in old.items() if len(v)>1})
 checks['all_target_overlaps_resolved']=all(len(actual[r])==1 for r in desired)
 checks['remaining_alaska_russian_territory_only_post']={r for r,v in actual.items() if any(t=='ALK' for s,t in v)}=={plan['new_province']['rgb']}
 rows={n.key:n for z in effective('map_data/state_regions') for n in parse(get(z.relative_to(ROOT).as_posix()) if z.is_relative_to(ROOT) else text(z))}
 before_regs={n.key:n for n in parse(before(REG))};members=C.defaultdict(set)
 for sid,n in rows.items():
  for r in provs(n,'provinces'):members['x'+r[1:].upper()].add(sid)
 checks['target_rgb_state_membership_exact']=all(members[r]=={s} for r,(s,t) in desired.items())
 checks['all_region_ids_unique']=len({n.one('id') for n in rows.values()})==len(rows)
 checks['old_regional_capacity_conserved']=region_capacity(rows[AK])+region_capacity(rows[POST])==region_capacity(before_regs[AK])
 checks['other_region_capacity_unchanged']=all(region_capacity(n)==region_capacity(before_regs[s]) for s,n in rows.items() if s in before_regs and s!=AK)
 pp=state_nodes(get(PP));oldpp=state_nodes(before(PP))
 def cohorts(sids,ns):
  out=C.Counter()
  for sid in sids:
   if sid not in ns:continue
   for rs in ns[sid].children():
    if not rs.key.startswith('region_state:'):continue
    for n in rs.children('create_pop'):out[pop_signature(n)]+=int(n.one('size'))
  return out
 for sid in plan['scope']:
  checks['population_identity_conserved.'+sid]=cohorts([sid]+([POST] if sid==AK else []),pp)==cohorts([sid],oldpp)
 checks['whole_na_population_and_identities_conserved']=cohorts(list(pp),pp)==cohorts(list(oldpp),oldpp)
 shares={(sid,scalar(z.one('country'))[2:]) for sid,n in state_nodes(get(ST)).items() for z in n.children('create_state')}
 checks['all_pop_scopes_have_land']=all((sid,rs.key.split(':')[1]) in shares for sid,n in pp.items() if sid in TARGET|{POST} for rs in n.children() if rs.key.startswith('region_state:') and rs.children('create_pop'))
 checks['colonial_post_population']=sum(int(z.one('size')) for rs in pp[POST].children() for z in rs.children('create_pop'))==1921
 oldassets=assets(before(BB));newassets=assets(get(BB));left=C.Counter(newassets)-C.Counter(oldassets);removed=C.Counter(oldassets)-C.Counter(newassets)
 checks['all_old_building_commands_preserved']=not removed
 checks['only_one_port_added']=sum(left.values())==1 and any(z.one('building')=='building_port' for n in state_nodes(get(BB))[POST].children() for z in n.children('create_building'))
 checks['all_other_building_and_military_files_preserved']=all(now.get(r)==h for r,h in base.items() if r.startswith(('common/history/buildings/','common/history/military_formations/')) and r!=BB)
 country_defs={n.key:n for q in effective('common/country_definitions') for n in parse(get(q.relative_to(ROOT).as_posix()) if q.is_relative_to(ROOT) else text(q))}
 newdefs=parse(get(f'common/country_definitions/{PREFIX}.txt'))
 country_defs.update({n.key:n for n in newdefs})
 checks['every_new_country_capital_owned']=all((scalar(n.one('capital')),n.key) in shares for n in newdefs)
 checks['russian_post_capital_owned']=country_defs['ALK'].one('capital')==POST and (POST,'ALK') in shares
 rh='common/history/countries/rus - russia.txt';checks['no_1799_company_at_start']='company_type:company_russian_american_company' not in get(rh) and 'company:company_russian_american_company' not in get(rh)
 def rus_without_company(raw):return normalized([n for n in parse(raw)[0].children('c:RUS')[0].children() if not (n.key=='add_company' and scalar(n.value)=='company_type:company_russian_american_company') and n.key!='company:company_russian_american_company'])
 checks['other_russian_start_commands_preserved']=rus_without_company(before(rh))==rus_without_company(get(rh))
 dip=get('common/history/diplomacy/00_subject_relationships.txt');z=[v for v in walk(parse(dip)) if v.key=='create_diplomatic_pact' and v.one('country')=='c:ALK'];checks['ordinary_russian_dependency_not_chartered_company']=len(z)==1 and z[0].one('type')=='colony'
 dyn=next(n for n in parse(get('common/dynamic_country_names/00_dynamic_country_names.txt')) if n.key=='ALK');checks['early_name_and_late_company_guard']=any(n.one('name')=='dyn_c_1776_aleutian_traders' for n in dyn.children()) and any(n.key=='current_date' and n.op=='>=' and n.value=='1799.1.1' for n in walk(dyn.children()))
 hist=state_nodes(get(ST));checks['no_usa_claims_in_western_spanish_regions']=all('c:USA' not in [z.value for z in hist[s].children('add_claim')] for s in CLAIM_SCOPE if s!=AK)
 checks['pacific_claims_spanish_not_ruperts_land']=all([z.value for z in hist[s].children('add_claim')]==['c:SC1'] for s in ['STATE_OREGON','STATE_WASHINGTON','STATE_BRITISH_COLUMBIA'])
 checks['no_blanket_russian_alaska_claim']='c:ALK' not in [v.value for v in hist[AK].children('add_claim')] and 'c:ALK' in [v.value for v in hist[POST].children('add_claim')]
 old_history=state_nodes(before(ST))
 checks['only_claim_regions_authorized_changed']=all(normalized(n.children('add_claim'))==normalized(old_history[s].children('add_claim')) for s,n in hist.items() if s not in CLAIM_SCOPE|{POST})
 # Binary proof: only already-land island pixels change color, every sea and
 # every other continent pixel must remain identical.
 baseline_image=ROOT/'map_data/provinces.png' if staged else OUT/'before/map_data/provinces.png'
 oldimage=np.asarray(Image.open(baseline_image).convert('RGB'));newimage=np.asarray(Image.open(source('map_data/provinces.png')).convert('RGB'))
 aa=(oldimage[:,:,0].astype('uint32')<<16)|(oldimage[:,:,1].astype('uint32')<<8)|oldimage[:,:,2]
 a=(newimage[:,:,0].astype('uint32')<<16)|(newimage[:,:,1].astype('uint32')<<8)|newimage[:,:,2]
 yy,xx=np.where(np.any(oldimage!=newimage,axis=2));changed=set(zip(map(int,xx),map(int,yy)));checks['only_approved_island_pixels_recolored']=changed==set(map(tuple,plan['new_province']['pixels']))
 checks['no_land_or_sea_invented']=all(aa[y,x]==0xC00000 and a[y,x]==0xC00001 for x,y in changed)
 # Effective reference checks include new subsistence building and port PMs.
 bdefs={n.key for q in effective('common/buildings') for n in parse(text(q))};pms={n.key for q in effective('common/production_methods') for n in parse(text(q))}
 checks['post_subsistence_reference_exists']=scalar(rows[POST].one('subsistence_building')) in bdefs
 checks['post_port_pm_references_exist']=all(z.value in pms for rs in state_nodes(get(BB))[POST].children() for b in rs.children('create_building') for z in b.children('activate_production_methods')[0].children())
 px,py=plan['new_province']['port_pixel'];exits={int(n.one('id')):set(int(r[1:],16) for r in provs(n,'provinces')) for q in effective('map_data/state_regions') if 'sea' in q.name for n in parse(text(q))};sea=exits[plan['new_province']['naval_exit']]
 checks['russian_port_pixel_and_sea_exit_valid']=int(a[py,px])==0xC00001 and any(int(a[py+dy,px+dx]) in sea for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)])
 for kind in ['city','port','farm','mine','wood']:
  rel=f'gfx/map/map_object_data/generated_map_object_locators_{kind}.txt';ns=parse(get(rel))[0].children('instances')[0].children();ids=[n.one('id') for n in ns if n.one('id') is not None]
  checks['locator_ids_unique.'+kind]=len(ids)==len(set(ids))
  n=next(n for n in ns if n.one('id')==str(plan['new_province']['id']));p0=[float(z.value) for z in n.children('position')[0].children()];checks['new_post_locator_samples_land.'+kind]=int(a[int(a.shape[0]-p0[2]),int(p0[0])])==0xC00001
  for h in [h for h in plan['hubs'] if h['kind']==kind]:
   n=next(n for n in ns if n.one('id')==str(h['id']));v=[float(z.value) for z in n.children('position')[0].children()];r=f'x{int(a[int(a.shape[0]-v[2]),int(v[0])]):06X}'
   checks['historic_hub.'+h['state']+'.'+kind]=r==h['rgb']==scalar(rows[h['state']].one(kind)) and actual[r]=={(h['state'],'SC1')}
 # Global mainland membership, not a detached northern remnant.
 spanish={int(r[1:],16) for r,v in actual.items() if any(t=='SC1' for s,t in v)};adj=graph(a,sorted(spanish));parts=components(adj,spanish);mainpart=set(parts[0]);checks['every_spanish_post_reaches_main_country']=all(int(s['rgb'][1:],16) in mainpart for s in plan['sites'])
 checks['all_spanish_mainland_provinces_connected']=len(parts)==1
 checks['every_corridor_share_incorporated']=all(z.one('state_type')=='incorporated' for sid,n in hist.items() if sid in TARGET for z in n.children('create_state') if z.one('country')=='c:SC1')
 checks['russian_post_incorporated']=hist[POST].children('create_state')[0].one('state_type')=='incorporated'
 # Earlier approved footprints, claims and populations are not overwritten.
 for tag in ['LOU','HBC','QUE','USA','IRO','CHE','MSC','NVS','GBR','SML']:
  checks['protected_territory.'+tag]={r for r,v in old.items() if any(t==tag for s,t in v)}=={r for r,v in actual.items() if any(t==tag for s,t in v)}
 for lang in ['french','english']:
  rel=f'localization/{lang}/replace/{PREFIX}_l_{lang}.yml';data=source(rel).read_bytes();checks['localization_bom.'+lang]=data.startswith(b'\xef\xbb\xbf') and data.decode('utf-8-sig').startswith('l_'+lang+':')
 result=dict(date='2026-10-27',checks=checks,all_pass=all(checks.values()),status='PREPARED' if staged else 'IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',engine_tested=False,preexisting_double_owners=len([r for r,v in old.items() if len(v)>1]),remaining_double_owners=len([r for r,v in actual.items() if len(v)>1]),new_province_pixels=len(changed),spanish_components=[len(z) for z in parts])
 dump(('STAGED_' if staged else '')+'VALIDATION.json',result);render(a,actual,plan)
 print(json.dumps(dict(passed=sum(checks.values()),total=len(checks),failed=[k for k,v in checks.items() if not v],spanish_components=result['spanish_components'])))
 return all(checks.values())

def render(a,own,plan):
 colors={g[0]:g[5] for g in GROUPS}|{'SC1':[242,198,67],'ALK':[75,134,199],'ATB':[135,145,100],'APC':[167,108,73],'NVJ':[149,119,165],'COM':[167,147,98],'CAD':[74,155,143],'WCH':[113,157,164],'USA':[79,130,169]}
 for name,box,size in [('NEW_SPAIN_1776.png',(1220,980,2040,1770),(1230,1185)),('ALASKA_1776.png',(0,70,1450,930),(1450,860))]:
  x0,y0,x1,y1=box;b=a[y0:y1,x0:x1];out=np.empty((*b.shape,3),dtype='uint8');out[:]=[36,49,58]
  for v in np.unique(b):
   r=f'x{int(v):06X}'
   if r in own:out[b==v]=colors.get(next(iter(own[r]))[1],[104,117,102])
  edge=np.zeros(b.shape,bool);edge[:,1:]|=b[:,1:]!=b[:,:-1];edge[1:]|=b[1:]!=b[:-1];out[edge]=[45,51,45]
  im=Image.fromarray(out).resize(size,Image.Resampling.NEAREST);c=Image.new('RGB',(size[0],size[1]+95),(36,49,58));c.paste(im,(0,70));d=ImageDraw.Draw(c);f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
  title='1776 — Nouvelle-Espagne : noyaux, missions et corridors' if name.startswith('NEW') else '1776 — Alaska : peuples autochtones et comptoir d’Unalaska'
  d.text((12,10),title,fill='white',font=f);d.text((12,38),'Or : Nouvelle-Espagne ; bleu : comptoir russe ; autres couleurs : peuples autochtones.',fill='white',font=f)
  sites=plan['sites'] if name.startswith('NEW') else [dict(name='Unalaska',projected=plan['new_province']['port_pixel'])]
  selected={'Monterey','San Diego','Tubac','Santa Fe','San Antonio','Bucareli','Unalaska'}
  for s in sites:
   if s['name'] not in selected:continue
   x,y=s['projected'];x=(x-x0)*size[0]/(x1-x0);y=(y-y0)*size[1]/(y1-y0)+70
   if 0<x<size[0]-80 and 70<y<size[1]+70:d.ellipse((x-3,y-3,x+3,y+3),fill='white');d.text((x+6,y-8),s['name'],fill='white',font=f,stroke_width=2,stroke_fill='black')
  d.text((12,size[1]+72),'Limites régionales approximatives ; corridors de jouabilité explicités dans le rapport.',fill='white',font=f);c.save(OUT/name)

if __name__=='__main__':sys.exit(0 if main('--staged' in sys.argv) else 1)
