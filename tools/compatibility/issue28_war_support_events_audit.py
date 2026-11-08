"""Read-only issue 28 event audit. No engine or gameplay file writes.

Compare six bounded sites with a captured/native contract, preserve all other
tokens in both files, and reject deliberate in-memory regressions.
"""
import argparse,hashlib,json,re,sys
from pathlib import Path
from decimal import Decimal
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
from validate_diplomacy_ottoman_1776 import parse,walk
FILES=('events/agitators_events/revolution_events_01.txt','events/election_events/election_contextual_events.txt')
LOT=ROOT/'docs/reports/compatibility/V1_15_ISSUE28_WAR_SUPPORT_EVENTS_2026_11_08'
TOKEN=re.compile(r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}]|[?<>!=]+|[^\s{}?<>!=#]+')
LEGACY={'add_war_exhaustion','has_war_exhaustion'}

def read(path):return path.read_bytes().decode('utf-8-sig')
def tokens(text):return tuple(m.group() for m in TOKEN.finditer(text) if not m.group().startswith('#'))
def signature_hash(text):return hashlib.sha256(json.dumps(tokens(text),ensure_ascii=False).encode()).hexdigest()
def one(items,key):
 values=[x for x in items if x.key==key]
 if len(values)!=1:raise ValueError(f'Expected one {key}, found {len(values)}')
 return values[0]
def subtree(items,*path):
 for key in path:items=one(items,key).children()
 return items
def slots(text,path):
 """Stable semantic roles; no line-number or whole-file replacement guesses."""
 events=parse(text);result={}
 if path==FILES[0]:
  event=one(events,'revolution_pulse1_events.2')
  for suffix,label in [('a','revolution_option_a'),('b','revolution_option_b')]:
   option=next(x for x in event.children('option') if x.one('name')=='revolution_pulse1_events.2.'+suffix)
   result[label]=one([x for x in walk(option.children()) if x.key in ['add_war_exhaustion','add_war_support_change','add_war_war_support']],[x.key for x in walk(option.children()) if x.key in ['add_war_exhaustion','add_war_support_change','add_war_war_support']][0])
  result['revolution_trigger_level']=one(subtree(event.children(),'trigger','any_scope_war'),'has_war_support')
  result['revolution_selector_level']=one(subtree(event.children(),'immediate','random_scope_war','limit'),'has_war_support')
 else:
  event=one(events,'election_contextual_events.3')
  for label,pathkeys in [('election_trigger',('trigger','any_scope_war')),('election_selector',('immediate','random_scope_war','limit'))]:
   options=[x for x in subtree(event.children(),*pathkeys) if x.key in ['has_war_exhaustion','has_war_support_change','has_war_support']]
   if len(options)!=1:raise ValueError(label+' has wrong predicate count')
   result[label]=options[0]
 return result
def masked_hash(text,sites):
 for name,n in sorted(sites.items(),key=lambda item:item[1].start,reverse=True):
  text=text[:n.start]+'issue28_'+name+' = yes'+text[n.end:]
 return signature_hash(text)
def transform(text,path):
 changes=[]
 for name,n in slots(text,path).items():
  child=one(n.children(),'value')
  old=text[n.start:n.end];new=old
  if name.startswith('revolution_option'):
   assert n.key=='add_war_exhaustion' and child.op=='=' and child.value=='10'
   new=new.replace('add_war_exhaustion','add_war_support_change',1)
   new=re.sub(r'\bvalue\s*=\s*10\b',lambda m:m[0][:-2]+'-5',new,count=1)
  elif name.startswith('election_'):
   assert n.key=='has_war_exhaustion' and child.op=='>' and child.value=='10'
   new=new.replace('has_war_exhaustion','has_war_support_change',1)
   new=re.sub(r'\bvalue\s*>\s*10\b',lambda m:m[0].replace('>','<')[:-2]+'-5',new,count=1)
  else:
   assert n.key=='has_war_support' and child.op=='<' and child.value=='10'
   new=re.sub(r'\bvalue\s*<\s*10\b',lambda m:m[0][:-2]+'55',new,count=1)
  assert old!=new
  changes.append((n.start,n.end,new))
 for start,end,new in sorted(changes,reverse=True):text=text[:start]+new+text[end:]
 if path==FILES[0]:
  assert text.count('# Get exhaustion no matter what')==1
  text=text.replace('# Get exhaustion no matter what','# Apply the war support change no matter what',1)
 return text

def audit(mod=ROOT,replacements=None):
 contract=json.loads(read(LOT/'CONTRACT.json'));checks=[]
 def check(name,ok):checks.append(dict(check=name,passed=bool(ok)))
 texts={p:(replacements[p] if replacements and p in replacements else read(mod/p)) for p in FILES}
 for path,text in texts.items():
  sites=slots(text,path);expected=contract['files'][path]
  check(path+'.site_set',set(sites)==set(expected['sites']))
  check(path+'.all_other_tokens_preserved',masked_hash(text,sites)==expected['preserved_token_hash'])
  check(path+'.no_removed_commands',not any(n.key in LEGACY for n in walk(parse(text))))
  for role,n in sites.items():
   check(role+'.native_payload',tokens(text[n.start:n.end])==tuple(expected['sites'][role]['native_tokens']))
   check(role+'.target_ROOT',one(n.children(),'target').value=='ROOT')
 # Boundary tests use the parsed installed operator/threshold at each site.
 for role,n in slots(texts[FILES[1]],FILES[1]).items():
  predicate=one(n.children(),'value');threshold=Decimal(predicate.value)
  for sample,expected in [('-6',True),('-5.001',True),('-5',False),('-4.999',False),('0',False),('6',False)]:
   actual=Decimal(sample)<threshold if predicate.op=='<' else Decimal(sample)>threshold if predicate.op=='>' else Decimal(sample)<=threshold if predicate.op=='<=' else None
   check(role+'.delta_boundary.'+sample,actual==expected)
 for role,n in slots(texts[FILES[0]],FILES[0]).items():
  v=one(n.children(),'value')
  if role.endswith('_level'):
   for sample,expected in [('54.99',True),('55',False),('55.01',False)]:
    check(role+'.level_boundary.'+sample,v.op=='<' and (Decimal(sample)<Decimal(v.value))==expected)
  else:check(role+'.harmful_signed_change',v.op=='=' and Decimal(v.value)==Decimal('-5'))
 errors=[x['check'] for x in checks if not x['passed']]
 return dict(status='FAIL_STATIC' if errors else 'PASS_STATIC_ONLY',passed=len(checks)-len(errors),total=len(checks),errors=errors,checks=checks,runtime_tested=False,human_validated=False)

def self_test(mod=ROOT):
 texts={p:read(mod/p) for p in FILES};a,b=FILES
 def alter(path,role,find,replace):
  text=texts[path];n=slots(text,path)[role];part=text[n.start:n.end];assert find in part
  return {path:text[:n.start]+part.replace(find,replace,1)+text[n.end:]}
 mutations={
  'reversed_effect_sign':alter(a,'revolution_option_a','-5','5'),
  'wrong_effect_target':alter(a,'revolution_option_b','ROOT','PREV'),
  'instant_level_effect':alter(a,'revolution_option_a','add_war_support_change','add_war_war_support'),
  'wrong_election_direction':alter(b,'election_trigger','< -5','> 5'),
  'inclusive_election_boundary':alter(b,'election_trigger','< -5','<= -5'),
  'different_saved_war_threshold':alter(b,'election_selector','-5','-4'),
  'unmigrated_level_gate':alter(a,'revolution_trigger_level','55','10'),
  'wrong_warleader':{b:texts[b].replace('attacker_warleader = ROOT','defender_warleader = ROOT',1)},
  'legacy_reintroduced':alter(a,'revolution_option_a','add_war_support_change','add_war_exhaustion')}
 event=one(parse(texts[a]),'revolution_pulse1_events.2');option=next(x for x in event.children('option') if x.one('name')=='revolution_pulse1_events.2.a');choice=option.children('random_list')[0].children()[0]
 mutations['random_weight_changed']={a:texts[a][:choice.start]+'2'+texts[a][choice.start+1:]}
 results=[]
 for name,replacement in mutations.items():
  try:detected=bool(audit(mod,replacement)['errors'])
  except (ValueError,AssertionError,IndexError,StopIteration):detected=True
  results.append(dict(mutation=name,detected=detected))
 assert all(x['detected'] for x in results)
 return results

if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--mod-root',type=Path,default=ROOT);ap.add_argument('--output',type=Path);ap.add_argument('--self-test',action='store_true');args=ap.parse_args()
 result=audit(args.mod_root)
 if args.self_test:result['negative_controls']=self_test(args.mod_root)
 if args.output:args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 print(json.dumps({k:v for k,v in result.items() if k!='checks'},ensure_ascii=False));raise SystemExit(bool(result['errors']))
