"""Current-workspace amendment: Sacramento is the BRZ portion of shared Uruguay.

No bitmap, population, building level, country or political-border changes.
Original R9-03 delivery/snapshots are retained as historical evidence.
"""
import collections as C,json,sys
from audit_hbc_1776 import ROOT,effective,provs,sha,runtime
from hbc06_integrate import text,encoded,edit,state_nodes,ownership
from validate_diplomacy_ottoman_1776 import parse,walk,scalar,normalized

OUT=ROOT/'docs/reports/map/SOUTH_AMERICA_1776/R9-03/SHARED_URUGUAY_FEEDBACK'
OLD='STATE_COLONIA_DO_SACRAMENTO';SID='STATE_URUGUAY';RGB='x4E1443'
ST='common/history/states/00_states.txt';PP='common/history/pops/07_south_america.txt';REG='map_data/state_regions/07_south_america.txt';BB='common/history/buildings/1776_sacramento.txt';SR='common/strategic_regions/south_america_strategic_regions.txt'
def dump(n,v):(OUT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def load(n):return json.loads((OUT/n).read_text(encoding='utf-8-sig'))
def prepare():
 OUT.mkdir(exist_ok=True);assert not (OUT/'APPLIED.json').exists();base=runtime();files={}
 raw=text(ROOT/REG);ns={n.key:n for n in parse(raw)};old=ns[OLD];n=ns[SID];assert old.one('id')=='3161' and provs(old,'provinces')==[RGB] and RGB not in provs(n,'provinces')
 z=n.children('provinces')[0];a=n.children('arable_land')[0];f=n.children('capped_resources')[0].children('building_fishing_wharf')[0]
 raw=edit(raw,[(z.end-1,z.end-1,' "'+RGB+'" '),(a.start,a.end,'arable_land = '+str(int(a.value)+int(old.one('arable_land')))),(f.start,f.end,'building_fishing_wharf = '+str(int(f.value)+int(old.children('capped_resources')[0].one('building_fishing_wharf')))),(old.start,old.end,'')]);files[REG]=encoded(ROOT/REG,raw)
 raw=text(ROOT/ST);ns=state_nodes(raw);old=ns[OLD];n=ns[SID];assert len(old.children('create_state'))==1 and old.children('create_state')[0].one('country')=='c:BRZ' and not any(z.one('country')=='c:BRZ' for z in n.children('create_state'))
 chunk=raw[old.children()[0].start:old.children()[0].end];files[ST]=encoded(ROOT/ST,edit(raw,[(old.start,old.end,''),(n.end-1,n.end-1,'\n\t\t'+chunk+'\n\t')]))
 raw=text(ROOT/PP);ns=state_nodes(raw);old=ns[OLD];n=ns[SID];assert len(old.children())==1 and old.children()[0].key=='region_state:BRZ' and not n.children('region_state:BRZ');chunk=raw[old.children()[0].start:old.children()[0].end]
 files[PP]=encoded(ROOT/PP,edit(raw,[(old.start,old.end,''),(n.end-1,n.end-1,'\n\t\t'+chunk+'\n\t')]))
 raw=text(ROOT/BB);assert raw.count(OLD)==1;files[BB]=encoded(ROOT/BB,raw.replace(OLD,SID))
 raw=text(ROOT/SR);ns=[z for z in walk(parse(raw)) if z.key=='states' and any(scalar(v.value)==OLD for v in z.children())];assert len(ns)==1;z=next(v for v in ns[0].children() if scalar(v.value)==OLD);files[SR]=encoded(ROOT/SR,edit(raw,[(z.start,z.end,'')]))
 for kind in ['city','port','farm','mine','wood']:
  rel=f'gfx/map/map_object_data/generated_map_object_locators_{kind}.txt';raw=text(ROOT/rel);ns=parse(raw)[0].children('instances')[0].children();old=[z for z in ns if z.one('id')=='3161'];assert len(old)==1;files[rel]=encoded(ROOT/rel,edit(raw,[(old[0].start,old[0].end,'')]))
 for lang,names in [('french',{'city':'Colônia do Sacramento','port':'Port de Sacramento','farm':'Campagne de Sacramento','mine':'Environs de Sacramento','wood':'Bois de Sacramento'}),('english',{'city':'Colonia do Sacramento','port':'Port of Sacramento','farm':'Sacramento countryside','mine':'Sacramento surroundings','wood':'Sacramento woodlands'})]:
  rel=f'localization/{lang}/replace/1776_sacramento_l_{lang}.yml';files[rel]=b'\xef\xbb\xbf'+('l_'+lang+':\n'+''.join(f' aor1776_sacramento_{k}:0 "{v}"\n' for k,v in names.items())).encode('utf8')
 effect='''# State scope. Keep the shared region/state named Uruguay.
# Only the Portuguese-owned split portion receives Sacramento hub names.
aor1776_sacramento_hub_names = {
 if = {
  limit = { state_region = s:STATE_URUGUAY is_split_state = yes owner = { OR = { c:BRZ ?= this c:POR ?= this } } }
'''+''.join('  set_hub_name = { type = '+k+' name = aor1776_sacramento_'+k+' }\n' for k in ['city','port','farm','mine','wood'])+''' }
}
'''
 files['common/scripted_effects/1776_sacramento_names.txt']=effect.encode('utf8')
 files['common/on_actions/17_1776_sacramento_names.txt']='''on_game_started = { on_actions = { aor1776_sacramento_names_initialize } }
on_game_started_after_lobby = { on_actions = { aor1776_sacramento_names_initialize } }
on_state_created = { on_actions = { aor1776_sacramento_names_update } }
on_state_owner_change = { on_actions = { aor1776_sacramento_names_update } }
aor1776_sacramento_names_initialize = { effect = { every_state = { aor1776_sacramento_hub_names = yes } } }
aor1776_sacramento_names_update = { effect = { aor1776_sacramento_hub_names = yes } }
'''.encode('utf8')
 m=dict(input_sha256={},output_sha256={})
 for rel,data in files.items():
  if rel.endswith('.txt'):parse(data.decode('utf-8-sig'))
  p=ROOT/rel;b=OUT/'before'/rel;q=OUT/'patch'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(data)
  if p.exists():b.parent.mkdir(parents=True,exist_ok=True);b.write_bytes(p.read_bytes())
  m['input_sha256'][rel]=sha(p) if p.exists() else None;m['output_sha256'][rel]=sha(q)
 dump('PATCH.json',m);dump('BASELINE_RUNTIME.json',base);print(json.dumps(dict(files=len(files),bitmap_changed=False,people_changed=0)))
def apply():
 m=load('PATCH.json');assert not (OUT/'APPLIED.json').exists();assert all((sha(ROOT/r) if (ROOT/r).exists() else None)==h for r,h in m['input_sha256'].items()),'Shared file changed: re-examine current content'
 for r,h in m['output_sha256'].items():assert sha(OUT/'patch'/r)==h
 for r in m['output_sha256']:(ROOT/r).parent.mkdir(parents=True,exist_ok=True);(ROOT/r).write_bytes((OUT/'patch'/r).read_bytes())
 dump('APPLIED.json',dict(date='2026-10-28',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',engine_tested=False))
def verify():
 m=load('PATCH.json');base=load('BASELINE_RUNTIME.json');now=runtime();checks={};oldown=__import__('central01').owned(text(OUT/'before'/ST));own=ownership()
 checks['installed_hashes']=all(now.get(r)==h for r,h in m['output_sha256'].items())
 checks['text_scripts_parse']=all(parse(text(ROOT/r)) is not None for r in m['output_sha256'] if r.endswith('.txt'))
 checks['only_region_assignment_changes']=set(own)==set(oldown) and own[RGB]=={(SID,'BRZ')} and all(own[r]==v for r,v in oldown.items() if r!=RGB)
 regs={n.key:n for p in effective('map_data/state_regions') for n in parse(text(p))};checks['one_shared_uruguay_region']=OLD not in regs and RGB in provs(regs[SID],'provinces') and sum(RGB in provs(n,'provinces') for n in regs.values())==1
 ns=state_nodes(text(ROOT/ST));parts=ns[SID].children('create_state');checks['uruguay_has_brazilian_and_spanish_portions']=len(parts)==2 and {z.one('country') for z in parts}=={'c:BRZ','c:SC4'} and OLD not in ns
 def popcounts(raw):
  c=C.Counter()
  for s,n in state_nodes(raw).items():
   for rs in n.children():
    for z in rs.children('create_pop'):c[(SID if s==OLD else s,rs.key,tuple(sorted((v.key,scalar(v.value)) for v in z.children() if v.key!='size')))]+=int(z.one('size'))
  return c
 checks['population_and_identity_preserved_by_owner']=popcounts(text(OUT/'before'/PP))==popcounts(text(ROOT/PP))
 rs=state_nodes(text(ROOT/PP))[SID].children('region_state:BRZ')[0];checks['enclave_3317_habitants_preserved']=sum(int(z.one('size')) for z in rs.children('create_pop'))==3317
 checks['port_identical_under_shared_region']=normalized(parse(text(OUT/'before'/BB).replace(OLD,SID)))==normalized(parse(text(ROOT/BB)))
 def countries(raw):return normalized([z for z in walk(parse(raw)) if z.key=='create_state'])
 checks['state_owner_commands_preserved']=countries(text(OUT/'before'/ST))==countries(text(ROOT/ST)) or C.Counter(json.dumps(normalized([z]),sort_keys=True) for z in walk(parse(text(OUT/'before'/ST))) if z.key=='create_state')==C.Counter(json.dumps(normalized([z]),sort_keys=True) for z in walk(parse(text(ROOT/ST))) if z.key=='create_state')
 oldregs={n.key:n for n in parse(text(OUT/'before'/REG))};newregs={n.key:n for n in parse(text(ROOT/REG))};o=oldregs[SID];p=oldregs[OLD];n=newregs[SID]
 checks['regional_potential_conserved']=int(n.one('arable_land'))==int(o.one('arable_land'))+int(p.one('arable_land')) and int(n.children('capped_resources')[0].one('building_fishing_wharf'))==int(o.children('capped_resources')[0].one('building_fishing_wharf'))+int(p.children('capped_resources')[0].one('building_fishing_wharf'))
 checks['other_regions_unchanged']=set(newregs)==set(oldregs)-{OLD} and all(normalized([n])==normalized([oldregs[s]]) for s,n in newregs.items() if s!=SID)
 checks['uruguay_hubs_and_naval_exit_retained']=all(n.one(k)==o.one(k) for k in ['city','port','farm','mine','wood','naval_exit_id','id'])
 locs=[]
 for kind in ['city','port','farm','mine','wood']:
  rel=f'gfx/map/map_object_data/generated_map_object_locators_{kind}.txt';old=parse(text(OUT/'before'/rel))[0].children('instances')[0].children();new=parse(text(ROOT/rel))[0].children('instances')[0].children();locs.append(normalized([z for z in old if z.one('id')!='3161'])==normalized(new))
 checks['only_obsolete_region_locators_removed']=all(locs)
 checks['bitmap_and_terrain_unchanged']=all(now.get(r)==base[r] for r in ['map_data/provinces.png','map_data/province_terrains.txt'])
 checks['unaffected_building_files_profiles_pacts_preserved']=all(now.get(r)==h for r,h in base.items() if r!=BB and r.startswith(('common/history/buildings/','common/history/countries/','common/history/diplomacy/','common/history/military_formations/')))
 checks['no_state_rename_only_owner_scoped_hub_names']='set_state_name' not in text(ROOT/'common/scripted_effects/1776_sacramento_names.txt') and 'is_split_state = yes' in text(ROOT/'common/scripted_effects/1776_sacramento_names.txt')
 checks['both_languages_have_five_distinct_hub_names']=all((ROOT/f'localization/{l}/replace/1776_sacramento_l_{l}.yml').read_bytes().startswith(b'\xef\xbb\xbf') and len(set(__import__('re').findall(r'"([^"]+)"',text(ROOT/f'localization/{l}/replace/1776_sacramento_l_{l}.yml'))))==5 for l in ['french','english'])
 checks['obsolete_region_not_in_strategic_membership']=OLD not in text(ROOT/SR) and normalized(parse(text(OUT/'before'/SR).replace(OLD,'')))==normalized(parse(text(ROOT/SR)))
 leftovers=[r for r in now if r.endswith('.txt') and r.startswith(('common/','map_data/')) and OLD in text(ROOT/r)];checks['no_obsolete_runtime_references']=not leftovers
 external={r:dict(before=base.get(r),after=now.get(r)) for r in base.keys()|now.keys() if r not in m['output_sha256'] and base.get(r)!=now.get(r)};dump('CONCURRENT_FILES.json',external);checks['no_unlisted_runtime_change']=not external
 dump('VALIDATION.json',dict(date='2026-10-28',checks=checks,passed=sum(checks.values()),total=len(checks),engine_tested=False));print(json.dumps(dict(passed=sum(checks.values()),total=len(checks),failed=[k for k,v in checks.items() if not v])));assert all(checks.values())
if __name__=='__main__':
 if '--prepare' in sys.argv:prepare()
 elif '--apply' in sys.argv:apply()
 elif '--verify' in sys.argv:verify()
