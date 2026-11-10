"""Issue26: provenance-based1.15 define migration and read-only contract audit.

Audit loading assumptions statically; never launch Victoria3 or certify engine
acceptance. --prepare/--install are explicit, single-use delivery operations.
"""
import argparse,ast,csv,hashlib,json,re,shutil,subprocess,sys
from collections import Counter
from decimal import Decimal,localcontext
from pathlib import Path
from datetime import datetime,timezone
sys.dont_write_bytecode=True
from issue27_journal_outcomes_audit import fields,one,signature
ROOT=Path(__file__).resolve().parents[2]
GAME=Path('C:/Games/Victoria 3/game')
REL='common/defines/00_defines.txt'
NEW='common/defines/zz_1776_scenario.txt'
LOC_PATHS={f'localization/{language}/replace/1776_france_journal_group_l_{language}.yml' for language in ['french','english']}
LOT=ROOT/'docs/reports/compatibility/V1_15_ISSUE26_WAR_SUPPORT_2026_11_07'
PREVIOUS='e5d97261';TECH_COMMIT='756e6c130ef97c41e03a4959eca67c81b57e1d89'
PROFILE_VARS={'min_birthrate':Decimal('0.00110'),'max_birthrate':Decimal('0.00510'),'min_mortality':Decimal('0.00095'),'max_mortality':Decimal('0.00620'),'max_growth_mortality_mult':Decimal('0.50')}

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def raw(p):return p.read_bytes().decode('utf-8-sig')
def save(p,txt):p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(txt.encode('utf8'))
def dump(name,data):save(LOT/name,json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def load(name):return json.loads(raw(LOT/name))
def git(*args):return subprocess.check_output(['git','--no-optional-locks',*args],cwd=ROOT)

def authored_baseline():
 """Read the compact, published contract captured before this migration.

 This makes read-only audits reproducible without private workspace snapshots
 or a bundled copy of the entire historical vanilla defines file.
 """
 contract=load('AUTHORED_CONTRACT.json');source=contract['original_fragment']
 values,_,duplicates,_=definitions(source)
 assert not duplicates and values==contract['expected_resolved_definitions'],'Authored contract is inconsistent'
 return source

def numeric(expr,variables):
 """Evaluate only the literal arithmetic in Jomini's @[...] preprocessor.

 No eval(), calls or attribute lookup. Decimal comparison retains repeatable
 ratios while runtime float rounding remains an engine observation.
 """
 expr=expr.strip()
 if expr.startswith('@['):expr=expr[2:-1]
 elif expr.startswith('@'):return variables[expr[1:]]
 def run(x):
  if isinstance(x,ast.Constant) and isinstance(x.value,(int,float)):return Decimal(ast.get_source_segment(expr,x))
  if isinstance(x,ast.Name):return variables[x.id]
  if isinstance(x,ast.UnaryOp):
   z=run(x.operand)
   if isinstance(x.op,ast.USub):return -z
   if isinstance(x.op,ast.UAdd):return z
  if isinstance(x,ast.BinOp):
   a,z=run(x.left),run(x.right)
   if isinstance(x.op,ast.Add):return a+z
   if isinstance(x.op,ast.Sub):return a-z
   if isinstance(x.op,ast.Mult):return a*z
   if isinstance(x.op,ast.Div):return a/z
  raise ValueError('Unsupported arithmetic: '+expr)
 with localcontext() as ctx:ctx.prec=40;return run(ast.parse(expr,mode='eval').body)

def definitions(text):
 values={};variables={};dups=[];locations={}
 # Macros are file-local and consumed in declaration order, matching the source
 # formulas. Scalar and array definitions retain their exact token structure.
 for parent in fields(text):
  if parent.key.startswith('@'):
   variables[parent.key[1:]]=numeric(parent.value,variables);continue
  if not parent.block:raise ValueError('Unexpected top-level scalar '+parent.key)
  for field in fields(parent.body):
   if field.key.startswith('@'):
    variables[field.key[1:]]=numeric(field.value,variables);continue
   key=parent.key+'.'+field.key
   if key in values:dups.append(key)
   expression=field.value
   if expression.startswith('@'):value=str(numeric(expression,variables))
   else:
    try:value=str(Decimal(expression))
    except Exception:value=' '.join(signature(expression))
   values[key]=value;locations[key]=dict(expression=expression,line=text[:parent.start].count('\n')+parent.body[:field.start].count('\n')+1)
 return values,variables,dups,locations

def equivalent(a,z):
 try:return abs(Decimal(a)-Decimal(z))<=Decimal('1e-30')
 except Exception:return a==z

def candidate(source):
 """Retain proven1776 deltas and the existing demographic formula verbatim.

 Prefix every macro so its file-local identifiers cannot collide with defaults.
 No war/economy/AI coefficients are guessed or inherited from an old baseline.
 """
 start=source.index('### Pop Growth Constants');end=source.index('### End Pop Growth Constant defines',start)+len('### End Pop Growth Constant defines')
 growth=source[start:end]
 growth=re.sub(r'@([A-Za-z_]\w*)',r'@aor1776_\1',growth)
 # Names in inline calculations are bare identifiers, not @variable references.
 growth=re.sub(r'@\[([^\]]+)\]',lambda m:'@['+re.sub(r'\b([A-Za-z_]\w*)\b',r'aor1776_\1',m[1])+']',growth)
 return '''#1776 scenario deltas only. All other defines inherit canonical1.15.
# Provenance: e5d97261 (1.13.9+1776),756e6c13 (demographic design).
# Keep these formulas together; their macros are local to this file.
NGame = { START_DATE = "1776.1.1" }
NPops = { WORKING_ADULT_RATIO_BASE = 0.30 }

'''+growth+'\n'

def inventory(root):
 folders=['common','events','gui','gfx','localization','map_data','docs/reports/map/SERG_CLOSURE','docs/reports/map/WORLD_1776_CLOSURE']
 return {p.relative_to(root).as_posix():sha(p) for folder in folders for p in (root/folder).rglob('*') if p.is_file()}

def prepare():
 LOT.mkdir(parents=True,exist_ok=True);assert not (LOT/'INSTALLATION.json').exists(),'Already installed'
 old=raw(ROOT/REL);native=raw(GAME/REL);prior=git('show',PREVIOUS+':'+REL).decode('utf-8-sig');head=git('show','HEAD:'+REL).decode('utf-8-sig')
 remote=load('REMOTE_INPUT.json')['content'].lstrip('\ufeff')
 a,av,ad,al=definitions(old);v,vv,vd,vl=definitions(native);p,pv,pd,pl=definitions(prior);h,hv,hd,hl=definitions(head);q,qv,qd,ql=definitions(remote)
 assert not(ad or vd or pd or hd or qd),'Duplicate input keys'
 assert a==h and av==hv,'Local defines changed after committed provenance; review them first'
 assert q==a and qv==av,'Remote defines differ semantically; prepare separate preservation plan'
 # The historical baseline report proves e5d97261 was1.13.9+START_DATE only.
 # Reconstruct the historical native baseline and verify its published digest.
 prior_bytes=git('show',PREVIOUS+':'+REL);reconstructed=prior_bytes.replace(b'START_DATE = "1776.1.1"',b'START_DATE = "1836.1.1"')
 assert hashlib.sha256(reconstructed).hexdigest().lower()=='398c364c108ce3ffa57fb25e000e3b8bce50e1f882e37c36a358eea34e4e1cf0'
 differences={key:(p.get(key),a.get(key)) for key in set(p)|set(a) if not equivalent(p.get(key,''),a.get(key,''))}
 changed_variables={key:(pv.get(key),av.get(key)) for key in set(pv)|set(av) if pv.get(key)!=av.get(key)}
 growth_names=set(re.findall(r'(?m)^@(\w+)\s*=',old[old.index('### Pop Growth Constants'):old.index('### End Pop Growth Constant defines')]))
 assert set(PROFILE_VARS)<=set(changed_variables)<=growth_names and all(av[k]==z for k,z in PROFILE_VARS.items())
 literal=lambda text:{k:str(Decimal(v.strip())) for k,v in re.findall(r'(?m)^@(\w+)\s*=\s*([^#\n]+)',text) if not v.strip().startswith('@')}
 pa,za=literal(prior),literal(old)
 assert {k for k in set(pa)|set(za) if pa.get(k)!=za.get(k)}==set(PROFILE_VARS)
 assert all(key.startswith('NPops.POP_GROWTH_') or key=='NPops.WORKING_ADULT_RATIO_BASE' for key in differences)
 output=candidate(old);retained,rv,rd,rl=definitions(output);assert not rd
 for key,value in retained.items():assert equivalent(value,a[key]),(key,value,a[key])
 expected={**v,**retained};rows=[]
 for key in sorted(set(a)|set(v)):
  if key in retained:action='RETAIN_PROVEN_1776_DELTA' if not equivalent(retained[key],v.get(key,'')) else 'RETAIN_DEMOGRAPHIC_FORMULA_CONTEXT'
  elif key not in v:action='REMOVE_OBSOLETE_1_13_DEFAULT'
  elif key not in a:action='INHERIT_NEW_1_15_DEFAULT'
  elif not equivalent(a[key],v[key]):action='INHERIT_CHANGED_1_15_DEFAULT'
  else:action='INHERIT_UNCHANGED_DEFAULT'
  rows.append(dict(key=key,before=a.get(key),native_1_15=v.get(key),after=expected.get(key),action=action,old_line=al.get(key,{}).get('line'),native_line=vl.get(key,{}).get('line'),provenance=TECH_COMMIT if key.startswith('NPops.') and key in retained else PREVIOUS if key=='NGame.START_DATE' else 'Canonical1.15; old baseline was not authored1776 tuning'))
 dump('DEFINE_MAPPING.json',rows);dump('PROVENANCE.json',dict(previous_commit=PREVIOUS,demographic_commit=TECH_COMMIT,reconstructed_native_1_13_9_sha256=hashlib.sha256(reconstructed).hexdigest(),changed_variables={k:[str(a),str(z)] for k,(a,z) in changed_variables.items()},proven_effective_design_deltas=differences,action_counts=dict(Counter(x['action'] for x in rows)),native_definitions=len(v),before_definitions=len(a),retained_override_definitions=len(retained)))
 for name,data in [('inputs/mod/00_defines.txt',(ROOT/REL).read_bytes()),('inputs/native/00_defines.txt',(GAME/REL).read_bytes()),('inputs/historical/00_defines_e5d97261.txt',prior_bytes)]:
  dest=LOT/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
 save(LOT/'candidate'/NEW,output)
 # Remote candidate is independent of dirty local historical/map files.
 save(LOT/'remote_candidate'/NEW,output)
 dump('BEFORE.json',dict(captured_utc=datetime.now(timezone.utc).isoformat(),mod_root=str(ROOT),native_root=str(GAME),old_file_sha256=sha(ROOT/REL),native_file_sha256=sha(GAME/REL),new_file_exists=(ROOT/NEW).exists(),protected=inventory(ROOT),git_head=git('rev-parse','HEAD').decode().strip(),git_branch=git('branch','--show-current').decode().strip(),git_index_sha256=sha(ROOT/'.git/index') if (ROOT/'.git/index').is_file() else None))
 print('Prepared mapping:',len(rows),'keys;',dict(Counter(x['action'] for x in rows)),';',len(retained),'narrow overrides')

def install():
 before=load('BEFORE.json');assert not (LOT/'INSTALLATION.json').exists(),'Already installed'
 assert sha(ROOT/REL)==before['old_file_sha256'] and sha(GAME/REL)==before['native_file_sha256']
 assert not (ROOT/NEW).exists() and not before['new_file_exists']
 txt=candidate(raw(ROOT/REL));assert txt==raw(LOT/'candidate'/NEW)
 save(ROOT/NEW,txt)
 # A backed-up file in the explicitly named defines directory only. Removing
 # it exposes the current canonical file; do not leave a renamed .txt backup.
 target=(ROOT/REL).resolve();assert target.parent==(ROOT/'common/defines').resolve() and target.name=='00_defines.txt'
 assert sha(target)==before['old_file_sha256'];target.unlink()
 dump('INSTALLATION.json',dict(status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',removed_file=REL,removed_sha256=before['old_file_sha256'],backup='inputs/mod/00_defines.txt',added_file=NEW,added_sha256=sha(ROOT/NEW),new_game_run=False,git_metadata_writes=False,vanilla_writes=False))
 print('Installed narrow scenario overrides; old full-file mask removed.')

def effective(mod,game,replacement=None):
 paths={p.name:p for p in (game/'common/defines').glob('*.txt')};paths.update({p.name:p for p in (mod/'common/defines').glob('*.txt')})
 # Audit00_defines and explicit mod deltas; other inherited native files are
 # byte-identical and often repeat namespaces for unrelated graphics settings.
 result={};overrides=[]
 for name,path in sorted(paths.items()):
  if name!='00_defines.txt' and path.parent!=(mod/'common/defines'):continue
  values,_,dups,_=definitions(replacement[name] if replacement and name in replacement else raw(path))
  if dups:raise ValueError('Duplicate keys in '+name+':'+str(dups))
  for k,v in values.items():
   if k in result:overrides.append(dict(key=k,file=name))
   result[k]=v
 return result,paths,overrides

def audit(mod=ROOT,game=GAME,replacement=None):
 errors=[];checks=[]
 def check(name,ok,detail=None):checks.append(dict(check=name,passed=bool(ok),detail=detail));errors.extend([] if ok else [name])
 current,paths,overrides=effective(mod,game,replacement);baseline=authored_baseline();old,_,_,_=definitions(baseline);native,_,_,_=definitions(raw(game/REL));narrow,_,dups,_=definitions(candidate(baseline));allow=set(narrow)
 check('no_mod_full_file_mask',not (mod/REL).exists());check('native_base_file_resolves',paths['00_defines.txt'].resolve()==(game/REL).resolve())
 check('all_native_keys_available',set(native)<=set(current));check('no_obsolete_definitions',not set(current)-set(native),sorted(set(current)-set(native)))
 for key,value in native.items():check('native.'+key,key in allow or equivalent(current.get(key,''),value))
 for key in allow:check('authored1776.'+key,equivalent(current.get(key,''),old[key]))
 check('exact_scenario_key_allowlist',set(definitions(replacement[Path(NEW).name] if replacement and Path(NEW).name in replacement else raw(mod/NEW))[0])==allow)
 check('range0to100',current.get('NDiplomacy.MIN_WAR_SUPPORT')=='0' and current.get('NDiplomacy.MAX_WAR_SUPPORT')=='100')
 check('native_initial_floor',current.get('NDiplomacy.WAR_SUPPORT_INITIAL_FLOOR')==native['NDiplomacy.WAR_SUPPORT_INITIAL_FLOOR'])
 check('no_old_auto_capitulation',not any('AUTO_CAPITULATE_WAR_SUPPORT' in x for x in current))
 check('no_old_war_exhaustion_defines',not any('WAR_EXHAUSTION' in x for x in current))
 check('native_stalemate',current.get('NWar.WAR_STALEMATE_MONTHS')==native['NWar.WAR_STALEMATE_MONTHS'])
 check('no_native_war_coefficients_overridden',not any(k.startswith(('NWar.','NDiplomacy.')) for k in allow))
 # Compare the complete demographic curves, including unchanged thresholds,
 # across a useful SoL grid rather than merely checking changed literals.
 def growth(values,s):
  get=lambda name:Decimal(values['NPops.POP_GROWTH_'+name]);s=Decimal(s)
  birth=(s*get('BIRTHRATE_PRETRANSITION_SLOPE')+get('MAX_BIRTHRATE') if s<get('TRANSITION_SOL') else s*get('BIRTHRATE_TRANSITION_SLOPE')+get('BIRTHRATE_TRANSITION_INTERCEPT') if s<get('STABLE_SOL') else get('MIN_BIRTHRATE'))
  mortality=(s*get('MORTALITY_STARVING_SLOPE')+get('MAX_MORTALITY') if s<get('EQUILIBRIUM_SOL') else s*get('MORTALITY_EQUILIBRIUM_TO_GROWTH_MAX_SLOPE')+get('MORTALITY_EQUILIBRIUM_TO_GROWTH_MAX_INTERCEPT') if s<get('MAX_SOL') else s*get('MORTALITY_GROWTH_MAX_TO_STABLE_SLOPE')+get('MORTALITY_GROWTH_MAX_TO_STABLE_INTERCEPT') if s<get('STABLE_SOL') else get('MIN_MORTALITY'))
  return birth,mortality
 samples=[]
 for sol in ['0','4.99','5','9.99','10','14.99','15','24.99','25','40']:
  a,z=growth(old,sol),growth(current,sol);check('demographic_curve.SoL'+sol,all(equivalent(str(x),str(y)) for x,y in zip(a,z)));samples.append(dict(SoL=sol,birthrate_monthly=str(z[0]),mortality_monthly=str(z[1])))
 return dict(status='PASS_STATIC_ONLY' if not errors else 'FAIL',passed=sum(x['passed'] for x in checks),total=len(checks),errors=errors,checks=checks,static_file_order_assumption='Canonical00_defines followed by alphabetically later scenario overrides; actual engine loading/date/workforce require user test',demographic_curve_samples=samples,effective_definitions=len(current),overrides=overrides,engine_tested=False,human_validated=False)

def self_test():
 original=raw(ROOT/NEW);mutations={
 'negative_war_support':original+'\nNDiplomacy = { MIN_WAR_SUPPORT = -100 }\n',
 'old_auto_capitulation':original+'\nNWar = { AUTO_CAPITULATE_WAR_SUPPORT = -100 }\n',
 'old_exhaustion':original+'\nNWar = { WAR_EXHAUSTION_BASE = 0.2 }\n',
 'changed_stalemate':original+'\nNWar = { WAR_STALEMATE_MONTHS = 1 }\n',
 'missing_workforce_ratio':original.replace('WORKING_ADULT_RATIO_BASE = 0.30','WORKING_ADULT_RATIO_BASE = 0.25'),
 'reset_birthrate':original.replace('@aor1776_min_birthrate = 0.00110','@aor1776_min_birthrate = 0.00060'),
 'wrong_start_date':original.replace('START_DATE = "1776.1.1"','START_DATE = "1836.1.1"'),
 'changed_turmoil':original+'\nNWar = { WAR_SUPPORT_CHANGE_TURMOIL_FACTOR = 1.0 }\n',
 'obsolete_travel_default':original+'\nNTravelNetwork = { ARMY_CONNECTION_DIRT_ROAD_COST_MULT = 1.5 }\n'}
 result=[]
 for name,source in mutations.items():
  try:r=audit(replacement={Path(NEW).name:source});detected=bool(r['errors']);errors=r['errors']
  except Exception as exc:detected=True;errors=[str(exc)]
  result.append(dict(mutation=name,detected=detected,failures=errors[:7]))
 dump('NEGATIVE_CONTROLS.json',result);assert all(z['detected'] for z in result);print('Negative controls',len(result),'/',len(result),'detected')

def validate():
 local=audit();remote=audit(LOT/'remote_candidate');before=load('BEFORE.json');now=inventory(ROOT);allowed={REL,NEW}|LOC_PATHS;external=[dict(file=p,before=before['protected'].get(p),after=now.get(p)) for p in set(before['protected'])|set(now) if before['protected'].get(p)!=now.get(p) and p not in allowed]
 # Preserve an observed peer edit at its exact current hash, without resetting
 # it to our capture or treating every future change as automatically accepted.
 acknowledged=load('CONCURRENT_PRESERVATION.json') if (LOT/'CONCURRENT_PRESERVATION.json').exists() else []
 unreviewed=[x for x in external if x not in acknowledged]
 dump('CONCURRENT_CHANGES.json',dict(outside_scope=external,unreviewed=unreviewed,scoped_changes=[dict(file=p,before=before['protected'].get(p),after=now.get(p)) for p in allowed],no_unrelated_baseline_restored=True))
 protections=dict(no_outside_scope_changes=not external,outside_scope_changes_accounted_for=not unreviewed,git_head_unchanged=git('rev-parse','HEAD').decode().strip()==before['git_head'],git_branch_unchanged=git('branch','--show-current').decode().strip()==before['git_branch'],git_index_unchanged=sha(ROOT/'.git/index')==before['git_index_sha256'],vanilla_unchanged=sha(GAME/REL)==before['native_file_sha256'],cossack_override_unchanged=sha(ROOT/'common/defines/zz_1776_world_russia01.txt')==before['protected'].get('common/defines/zz_1776_world_russia01.txt'))
 dump('VALIDATION_LOCAL.json',local);dump('VALIDATION_REMOTE.json',remote);dump('PROTECTIONS.json',protections)
 print('Local:',local['status'],local['passed'],'/',local['total'],'Remote:',remote['status'],remote['passed'],'/',remote['total']);print('Protections',protections);print('Errors',local['errors'],remote['errors']);assert local['status']==remote['status']=='PASS_STATIC_ONLY' and all(v for k,v in protections.items() if k!='no_outside_scope_changes')

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__)
 for key in ['prepare','install','validate','self-test']:p.add_argument('--'+key,action='store_true')
 p.add_argument('--mod-root',type=Path);p.add_argument('--vanilla-root',type=Path,default=GAME);p.add_argument('--output',type=Path);args=p.parse_args()
 if args.prepare:prepare()
 if args.install:install()
 if args.validate:validate()
 if args.self_test:self_test()
 if args.mod_root:
  result=audit(args.mod_root,args.vanilla_root);data=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
  if args.output:save(args.output,data)
  else:print(data)
  raise SystemExit(bool(result['errors']))
