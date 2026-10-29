"""Read-only streaming analysis of the fresh, engine-created R9 test save."""
import re,json,collections as C,sys,difflib
from pathlib import Path
from r9_final_validation import OUT,BASE,PP,BB,load,dump
from audit_hbc_1776 import ROOT
from hbc06_integrate import text,state_nodes
from validate_diplomacy_ottoman_1776 import parse,normalized,walk,scalar

def objects(path):
 section=None;ident=None;lines=[];start=0
 for no,line in enumerate(path.open(encoding='utf8'),1):
  if line and not line[0].isspace():section=line.split('=',1)[0] if line.endswith('={\n') else None
  m=re.fullmatch(r'\t\t(\d+)=\{\n',line)
  if m:ident=int(m[1]);lines=[line];start=no
  elif ident is not None:
   lines.append(line)
   if line=='\t\t}\n':yield section,ident,''.join(lines),start;ident=None
def field(raw,key):
 m=re.search(r'^\t{3}'+re.escape(key)+r'=(.*)$',raw,re.M);return m[1].strip('"') if m else None
def sample():
 found=set()
 for sec,i,r,n in objects(OUT/'FRESH_INITIAL_MELTED.txt'):
  if sec in {'pops','states','provinces'} and sec not in found:
   print(sec,i,n,r[:3800]);found.add(sec)
  if len(found)==3:break
def differences():
 for rel,old in [(BB,BASE/'R9-02/patch'/BB),('common/history/buildings/98_build_start_1776_world_redistribution.txt',BASE/'R9-02/patch/common/history/buildings/98_build_start_1776_world_redistribution.txt'),(PP,BASE/'R9-07/PAMPAS_CUYO/patch'/PP)]:
  d=list(difflib.unified_diff(text(old).splitlines(),text(ROOT/rel).splitlines(),fromfile=str(old),tofile=rel,n=3))
  (OUT/('FOLLOWUP_'+Path(rel).stem+'.diff')).write_text('\n'.join(d)+'\n',encoding='utf8');print('\n'.join(d)[:17000])
def audit():
 path=OUT/'FRESH_INITIAL_MELTED.txt';countries={};states={};buildings=[];sizes=C.Counter();date=None
 scope={r['state'] for r in load(OUT/'R9_SCOPES.json')}
 for sec,i,r,n in objects(path):
  if sec=='country_manager':countries[str(i)]=field(r,'definition')
  elif sec=='states':
   sid=field(r,'region')
   if sid not in scope:continue
   stats={k:int(v) for k,v in re.findall(r'^\t{4}(population_(?:lower|middle|upper)_strata)=(\d+)$',r,re.M)}
   states[str(i)]={'state_id':i,'region':sid,'country_id':field(r,'country'),'line':n,'incorporation':field(r,'incorporation') or '0','strata_population':sum(stats.values()),'strata':stats,'infrastructure':field(r,'infrastructure'),'infrastructure_usage':field(r,'infrastructure_usage'),'capital':field(r,'capital')}
  elif sec=='building_manager':
   b={'id':i,'state_id':field(r,'state'),'building':field(r,'building'),'levels':int(field(r,'levels') or 0),'line':n}
   buildings.append(b)
 # Province engine IDs are never treated as RGBs. Count live province records
 # only, comparing state shares; no unsupported engine-ID-to-RGB mapping.
 section=False;pid=None
 for line in path.open(encoding='utf8'):
  if line=='provinces={\n':section=True;continue
  if section and line=='}\n':break
  if section:
   m=re.match(r'^\t(\d+)=\{',line)
   if m:pid=m[1]
   m=re.match(r'^\t\tstate=(\d+)',line)
   if m:sizes[m[1]]+=1
 for s in states.values():s['owner']=countries.get(s['country_id']);s['province_count']=sizes[str(s['state_id'])]
 observed={};counter=C.Counter()
 for b in buildings:
  if b['state_id'] not in states:continue
  st=states[b['state_id']];b.update(region=st['region'],owner=st['owner']);observed[b['id']]=b;counter[(st['region'],st['owner'],b['building'])]+=b['levels']
 inv=load(OUT/'GLOBAL_CURRENT_INVENTORY.json');expected_count=C.Counter()
 for z in inv['owners']:
  rgb,s,t=z['key']
  if s in scope:expected_count[s,t]+=z['count']
 actual_count=C.Counter({(s['region'],s['owner']):s['province_count'] for s in states.values()})
 owner_delta={'missing':[(k,v) for k,v in (expected_count-actual_count).items()],'unexpected':[(k,v) for k,v in (actual_count-expected_count).items()]}
 expectedpop=C.Counter()
 for z in load(OUT/'R9_POPULATION_COHORTS.json'):expectedpop[z['state'],z['owner']]+=z['size']
 pop_rows=[dict(region=s['region'],owner=s['owner'],expected=expectedpop[s['region'],s['owner']],loaded=s['strata_population'],delta=s['strata_population']-expectedpop[s['region'],s['owner']]) for s in states.values()]
 expectedbuild=C.Counter();declared_max=C.Counter();repeated=C.defaultdict(list)
 for b in load(OUT/'R9_BUILDING_COMMANDS.json'):
  # Explicit history ownership levels create the initial building size.
  k=b['state'],b['owner'],b['building'];v=sum(b['economic_levels']) or int(b['explicit_level'] or 1)
  expectedbuild[k]+=v;declared_max[k]=max(declared_max[k],v);repeated[k].append({'file':b['file'],'line':b['line'],'levels':v})
 bdelta=[dict(region=k[0],owner=k[1],building=k[2],expected=v,loaded=counter[k],delta=counter[k]-v) for k,v in expectedbuild.items() if counter[k]!=v]
 # Read actual port state names from the delivery files to avoid guessed scope.
 ports=[]
 for rel in ['common/history/buildings/1776_sacramento.txt','common/history/buildings/1776_r904_chiloe_port.txt','common/history/buildings/1776_r907_malvinas_port.txt']:
  for s in state_nodes(text(ROOT/rel)).values():
   for rs in s.children():
    if rs.key.startswith('region_state:'):
     sid=s.key.removeprefix('s:');tag=rs.key.split(':')[1];ports.append(dict(file=rel,region=sid,owner=tag,loaded_port_levels=counter[sid,tag,'building_port']))
 dump('FRESH_SAVE_STATES.json',list(states.values()));dump('FRESH_SAVE_BUILDINGS.json',list(observed.values()));dump('FRESH_SAVE_POPULATION_COMPARISON.json',pop_rows);dump('FRESH_SAVE_BUILDING_COMPARISON.json',bdelta)
 maxdelta=[dict(region=k[0],owner=k[1],building=k[2],maximum_declared_level=v,loaded=counter[k],declarations=repeated[k]) for k,v in declared_max.items() if counter[k]!=v]
 dump('FRESH_SAVE_BUILDING_MAX_DIAGNOSTIC.json',maxdelta)
 result={'source':path.name,'date':'1776.1.1','engine':'1.13.11','country':'SPA','state_share_count':len(states),'province_count':sum(s['province_count'] for s in states.values()),'owner_count_comparison':owner_delta,'state_share_owners_and_province_counts_match_input':not owner_delta['missing'] and not owner_delta['unexpected'],'province_RGB_mapping_tested':False,'population_input':sum(expectedpop.values()),'population_saved_strata':sum(s['strata_population'] for s in states.values()),'population_rows_differing':[z for z in pop_rows if z['delta']],'building_level_differences':len(bdelta),'added_ports':ports,'load_and_manual_save_observed':True,'simulation_tested':False,'reload_tested':False,'human_validated':False,'UI_limitation':'FrameArrived timed out twice after world zoom; input stopped as required.'}
 dump('FRESH_SAVE_VALIDATION.json',result);print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':
 if '--sample' in sys.argv:sample()
 elif '--diff' in sys.argv:differences()
 else:audit()
