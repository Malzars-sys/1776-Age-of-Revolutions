"""Durrani/Punjab 1776: current-workspace survey; no history mutations in survey."""
import collections as C,csv,json,re,sys
from pathlib import Path
from audit_hbc_1776 import ROOT,GAME,effective,provs,sha,runtime
from hbc06_integrate import text,state_nodes,ownership,encoded,edit,rgb_block
from validate_diplomacy_ottoman_1776 import parse,walk,scalar,normalized
OUT=ROOT/'docs/reports/map/DURRANI_PUNJAB_1776/DP-01'
TAGS=['DUR','PAN','KAS','KAL','MAK','SIN','KZH','OZH','UZH','BUK','KHI','KOK']
def dump(name,v):
 OUT.mkdir(parents=True,exist_ok=True);(OUT/name).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def load(name):return json.loads((OUT/name).read_text(encoding='utf8'))
def survey():
 OUT.mkdir(parents=True,exist_ok=True)
 inv=[];sources=[]
 base=ROOT/'docs/reports/map/MAP1/inputs/regional_originals'
 for name in ['R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA','R4_SOUTH_ASIA']:
  rows=list(csv.DictReader((base/(name+'_RECOMMENDATIONS.csv')).open(encoding='utf-8-sig')))
  selected=[r for r in rows if any(re.search(r'\b'+t+r'\b',str(r)) for t in ['DUR','PAN','KAS','KAL','SIN'])]
  print(name, 'fields:',list(rows[0]))
  for r in selected:
   print(json.dumps({k:v for k,v in r.items() if k in ['Change_ID','State_ID','Owner_TAG','Current_Owner_TAG','Recommended_1776_Owner','Proposed_Owner_TAG','Justification','Recommendation','Notes','Source_IDs','Mapping_Notes','Historical_Polity','Evidence_Summary']},ensure_ascii=False))
  inv+=selected
  sources+=list(csv.DictReader((base/(name+'_SOURCES.csv')).open(encoding='utf-8-sig')))
 dump('PRIOR_RECOMMENDATIONS.json',inv)
 refs=set(re.findall(r'R[34]_[A-Z_]+-S\d+',json.dumps(inv)))
 selected=[r for r in sources if any(v in refs for v in r.values())];dump('PRIOR_SOURCES.json',selected)
 print('SOURCE FIELDS',list(sources[0]));print('SOURCES',json.dumps(selected,ensure_ascii=False))
 own=ownership();states=C.defaultdict(lambda:C.defaultdict(list))
 for r,vs in own.items():
  for sid,t in vs:
   if t in TAGS:states[sid][t].append(r)
 dump('CURRENT_OWNERSHIP.json',states)
 print('CURRENT',json.dumps({s:{t:len(rs) for t,rs in d.items()} for s,d in states.items()}))
 records=[]
 for folder in ['common/country_definitions','common/history/countries','common/history/characters','common/history/diplomacy']:
  for p in effective(folder):
   raw=text(p)
   for n in walk(parse(raw)):
    if n.key in TAGS+[f'c:{t}' for t in TAGS]:
     if folder.endswith('diplomacy') and not any(t in raw[n.start:n.end] for t in TAGS):continue
     records.append(dict(folder=folder,file=str(p),key=n.key,line=raw.count('\n',0,n.start)+1,body=raw[n.start:n.end]))
 dump('DEPENDENCIES.json',records)
 for r in records:
  if r['key'] in ['DUR','PAN','KAS','KAL','SIN','c:DUR','c:PAN','c:KAS','c:KAL','c:SIN']:print('DEPENDENCY',json.dumps(r,ensure_ascii=False))
 if not (OUT/'SURVEY_RUNTIME_MANIFEST.json').exists():dump('SURVEY_RUNTIME_MANIFEST.json',runtime())
if __name__=='__main__':survey()
