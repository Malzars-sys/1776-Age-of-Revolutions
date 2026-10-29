"""Read-only reconciliation after the strict final R9 delivery audit."""
import sys,json,copy,collections as C
from pathlib import Path
from r9_final_validation import BASE,OUT,PP,BB,load,dump
from hbc06_integrate import text,state_nodes
from validate_diplomacy_ottoman_1776 import normalized,walk

def stripped(n):
 n=copy.deepcopy(n)
 def clean(x):
  if isinstance(x.value,list):
   x.value=[q for q in x.value if q.key!='activate_production_methods']
   for q in x.value:clean(q)
 clean(n);return normalized([n])

def reconcile():
 results={}
 from audit_hbc_1776 import ROOT
 old=state_nodes(text(BASE/'R9-02/patch'/BB));new=state_nodes(text(ROOT/BB))
 changed=[s for s in old.keys()|new.keys() if s not in old or s not in new or normalized([old[s]])!=normalized([new[s]])]
 results['inherited_buildings']={'changed_states':sorted(changed),'all_commands_identical_except_PMs':all(s in old and s in new and stripped(old[s])==stripped(new[s]) for s in changed),'PM_changes':{s:{'before':[[z.value for z in n.children()] for n in walk([old[s]]) if n.key=='activate_production_methods'],'current':[[z.value for z in n.children()] for n in walk([new[s]]) if n.key=='activate_production_methods']} for s in changed if s in old and s in new}}
 def levels(n):
  c=C.Counter()
  for rs in n.children():
   if rs.key.startswith('region_state:'):
    for b in rs.children('create_building'):
     total=sum(int(z.value) for o in b.children('add_ownership') for z in walk(o.children()) if z.key=='levels')
     c[rs.key,str(b.one('building')).strip('"')]+=total or int(b.one('level',1))
  return c
 deltas=[]
 for s in changed:
  a=levels(old[s]) if s in old else C.Counter();b=levels(new[s]) if s in new else C.Counter()
  for k in a.keys()|b.keys():
   if a[k]!=b[k]:deltas.append(dict(state=s,owner=k[0],building=k[1],before=a[k],current=b[k],delta=b[k]-a[k]))
 results['inherited_buildings']['declared_level_deltas']=deltas
 results['inherited_buildings']['no_deleted_command_or_decreased_level']=all(s in new and len(list(walk([new[s]])))>=len(list(walk([old[s]]))) and all(levels(new[s])[k]>=v for k,v in levels(old[s]).items()) for s in old)
 rel='common/history/buildings/98_build_start_1776_world_redistribution.txt'
 candidates=[p for p in BASE.glob('R9-*/**/patch/'+rel) if p.is_file()]
 expected=next((p for p in candidates if __import__('hashlib').sha256(p.read_bytes()).hexdigest()==next(z['delivered'] for z in load(OUT/'DELIVERY_FILE_DRIFT.json') if z['path']==rel)),None)
 if expected:
  old=state_nodes(text(expected));new=state_nodes(text(ROOT/rel));changed=[s for s in old.keys()|new.keys() if s not in old or s not in new or normalized([old[s]])!=normalized([new[s]])]
  results['redistribution_buildings']={'baseline':str(expected.relative_to(ROOT)),'changed_states':sorted(changed),'all_commands_identical_except_PMs':all(s in old and s in new and stripped(old[s])==stripped(new[s]) for s in changed)}
 else:results['redistribution_buildings']={'baseline_found':False}
 from central01 import cohorts
 old=cohorts(text(BASE/'R9-07/PAMPAS_CUYO/patch'/PP));new=cohorts(text(ROOT/PP));states=set(s for s,k in old)|set(s for s,k in new)
 results['population']={s:{'before':sum(v for (sid,k),v in old.items() if sid==s),'current':sum(v for (sid,k),v in new.items() if sid==s),'removed_cohorts':[{'signature':k,'size':v} for (sid,k),v in (old-new).items() if sid==s],'added_cohorts':[{'signature':k,'size':v} for (sid,k),v in (new-old).items() if sid==s]} for s in sorted(states) if any(sid==s for sid,k in (old-new).keys()|(new-old).keys())}
 results['strict_result_retained']='STATIC_VALIDATION.json remains 20/22; this receipt explains subsequent shared-file changes without restoring or certifying their historical/economic intent.'
 dump('FOLLOWUP_RECONCILIATION.json',results)
 print(json.dumps({k:v for k,v in results.items() if k!='population'},ensure_ascii=False))

def sample():
 p=OUT/'FRESH_INITIAL_MELTED.txt';wanted=[(1297879,15),(1413662,50),(1933535,100),(2016740,50),(6701063,70),(8565066,45)]
 with p.open(encoding='utf8') as f:
  for i,line in enumerate(f,1):
   if any(a<=i<a+n for a,n in wanted):print(f'{i}:{line.rstrip()}')
   if i>8565115:break
if __name__=='__main__':
 if '--sample' in sys.argv:sample()
 else:reconcile()
