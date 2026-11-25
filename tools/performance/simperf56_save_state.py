"""Read-only native text-save indicators; no binary melting or save edits."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json,re,sys
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from validate_diplomacy_ottoman_1776 import parse
BRACES=re.compile(r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}]')
def block_end(s,start):
 depth=0
 for m in BRACES.finditer(s,start):
  t=m.group()
  if t=='{':depth+=1
  elif t=='}':
   depth-=1
   if depth==0:return m.end()
 raise ValueError('Unclosed native block')
def sections(s):
 result={};pos=s.index('\n')+1
 header=re.compile(r'([A-Za-z_][\w]*)\s*=\s*(\{|"(?:\\.|[^"\\])*"|[^\s{}]+)')
 while pos<len(s):
  while pos<len(s) and s[pos].isspace():pos+=1
  if pos==len(s):break
  m=header.match(s,pos)
  if not m:raise ValueError('Unknown top-level token at '+str(pos))
  end=block_end(s,m.end()-1) if m[2]=='{' else m.end()
  result[m[1]]=(m.start(),end);pos=end
 return result
def records(s,span):
 a,b=span;m=re.search(r'\bdatabase=\{',s[a:b])
 if not m:return
 start=a+m.end()-1;end=block_end(s,start);pos=start+1
 entry=re.compile(r'(\d+)=\{')
 while True:
  m=entry.search(s,pos,end)
  if not m:break
  stop=block_end(s,m.end()-1)
  assert stop<=end
  yield m[1],parse(s[m.start():stop])[0]
  pos=stop
def num(n,key):
 try:return float(n.one(key,0))
 except (TypeError,ValueError):return 0.0
def child(n,key):
 found=n.children(key);return found[0] if found else None
def inspect(path):
 raw=path.read_bytes();s=raw.decode('utf-8-sig');ss=sections(s)
 out=dict(path=str(path),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),date=re.search(r'\bgame_date=([\d.]+)',s[:4096])[1],section_bytes={k:b-a for k,(a,b) in ss.items()})
 sums=Counter();countries={}
 for ident,n in records(s,ss['country_manager']):
  if n.one('dead')=='yes':continue
  stats=child(n,'pop_statistics');pop=sum(num(stats,k) for k in ('population_lower_strata','population_middle_strata','population_upper_strata')) if stats else 0
  if not pop:continue
  row=dict(tag=str(n.one('definition','')).strip('"'),population=pop,country_type=n.one('country_type'),market=n.one('market'))
  if stats:
   for key in ('population_salaried_workforce','population_subsisting_workforce','population_unemployed_workforce','population_government_workforce','population_military_workforce'):
    row[key]=num(stats,key);sums[key]+=row[key]
  countries[ident]=row;sums['population']+=pop
 out['country']=dict(active_with_population=len(countries),totals=dict(sums),by_id=countries)
 bstats=Counter();pm=Counter();pm_by_id={}
 for ident,n in records(s,ss['building_manager']):
  if n.one('building') is None:continue
  bstats['records']+=1;bstats['levels']+=num(n,'levels');bstats['negative_profit']+=num(n,'profit_after_reserves')<0
  methods=child(n,'production_methods');names=[str(x.value).strip('"') for x in methods.children()] if methods else []
  pm.update(names);pm_by_id[ident]=dict(type=n.one('building'),state=n.one('state'),levels=num(n,'levels'),production_methods=names)
  if n.one('active')=='yes':bstats['active']+=1
 out['buildings']=dict(totals=dict(bstats),pm_record_counts=dict(pm),by_id=pm_by_id)
 state=Counter()
 for ident,n in records(s,ss['states']):
  if n.one('country') is None:continue
  state['records']+=1
  state['infrastructure_deficit']+=num(n,'infrastructure_usage')>num(n,'infrastructure')
  stats=child(n,'pop_statistics')
  if stats:state['population']+=sum(num(stats,k) for k in ('population_lower_strata','population_middle_strata','population_upper_strata'))
 out['states']=dict(state)
 ai=Counter();goals=Counter();strategies=Counter();aicountries={}
 for ident,n in records(s,ss['ai']):
  if n.one('country') is None:continue
  ai['records']+=1;ai['enabled']+=n.one('enabled')=='yes'
  for x in n.children('ai_goal'):goals[str(x.one('type'))]+=1
  for x in n.children('ai_strategy'):strategies[str(x.one('type'))]+=1
  for key in ('num_failed_money_spending_attempts','num_failed_authority_spending_attempts','num_failed_autonomous_investments'):
   ai[key]+=num(n,key)
  for key in ('building_subsidies_changed','strategic_region_stances_dirty','authority_spending_changed'):ai[key]+=n.one(key)=='yes'
  cg=child(n,'country_goal');ai['country_goal_entries']+=len(cg.children()) if cg else 0
  aicountries[str(n.one('country'))]=dict(enabled=n.one('enabled'),strategies=[x.one('type') for x in n.children('ai_strategy')],goal_fields=[x.key for x in n.children('ai_goal')],country_goals=len(cg.children()) if cg else 0)
 out['ai']=dict(totals=dict(ai),goal_types=dict(goals),strategy_types=dict(strategies),by_country=aicountries)
 out['pops']=dict(records=sum(1 for _,n in records(s,ss['pops']) if n.one('type') is not None),note='Records are serialized POP objects, not total persons or historical groups.')
 for key in ('market_manager','diplomatic_plays','war_manager','military_formation_manager','new_combat_unit_manager','ship_manager','treaty_manager','ai_regional_objective_manager'):
  out[key]=dict(records=sum(1 for _,n in records(s,ss[key]))) if key in ss else None
 # Counts of serialized variables/modifiers, not scheduled native execution cost.
 out['dated_data']=dict(expiration_date_fields=len(re.findall(r'\bexpiration_date=',s)),aor_variable_names=dict(Counter(re.findall(r'\bname=(aor1776_[\w]+)',s))))
 return out
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('save',type=Path);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
 assert not a.output.exists();out=inspect(a.save)
 with a.output.open('x',encoding='utf-8') as f:json.dump(out,f,indent=2,ensure_ascii=False)
 print(json.dumps({k:v for k,v in out.items() if k not in ('section_bytes','country','buildings','ai','dated_data')},indent=2))
 print(json.dumps(dict(country=out['country']['totals'],buildings=out['buildings']['totals'],ai=out['ai']['totals']),indent=2))
