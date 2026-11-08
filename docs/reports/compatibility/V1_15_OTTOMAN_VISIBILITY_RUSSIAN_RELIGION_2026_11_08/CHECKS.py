"""Bounded read-only checks; writes only this delivery's validation receipt."""
from pathlib import Path
import hashlib,json,re,subprocess,sys
ROOT=Path(__file__).resolve().parents[4]
LOT=Path(__file__).resolve().parent
GAME=Path('C:/Games/Victoria 3/game')
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT/'tools/compatibility'))
sys.path.insert(0,str(ROOT/'tools'))
from issue27_journal_outcomes_audit import fields,one,signature
from validate_diplomacy_ottoman_1776 import parse,walk
checks=[]
def check(name,result):
 checks.append(dict(check=name,passed=bool(result)))
 assert result,name
def read(base,path):return (base/path).read_bytes().decode('utf-8-sig')
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def selected(text,key):return one(fields(text),key)
def seq(items,omit=()):return [(x.key,signature(x.value)) for x in items if x.key not in omit]
def node(text,key):return next(x for x in parse(text) if x.key==key)

# Evaluate only the predicates used by these gates. Unsupported syntax fails;
# this is a logic model, not a claim about the game's journal scheduler.
def condition(items,ctx):
 def test(n):
  if n.key=='text':return True
  if n.key in ['AND','custom_tooltip']:return condition(n.children(),ctx)
  if n.key=='OR':return any(test(x) for x in n.children())
  if n.key in ['NOT','NOR']:return not any(test(x) for x in n.children())
  if n.key=='NAND':return not condition(n.children(),ctx)
  if n.key.startswith('c:') and not n.children():return ctx['tag']==n.key[2:]
  if n.key=='exists':return n.value=='c:RUS' # RUS exists in all law fixtures.
  if n.key=='has_variable':return n.value in ctx.get('vars',{})
  if n.key=='has_journal_entry':return n.value in ctx.get('active',set())
  if n.key=='has_inactive_journal_entry':return n.value in ctx.get('inactive',set())
  if n.key in ['has_law','has_law_or_variant']:return str(n.value).removeprefix('law_type:') in ctx.get('laws',set())
  if n.key=='is_subject_of':return ctx.get('russian_subject',False)
  if n.key=='country_is_subject_type_valid_for_caesaropapism':return ctx.get('eligible_orthodox_subject',False)
  raise ValueError('Unmodeled predicate: '+n.key)
 return all(test(x) for x in items)

p='common/journal_entries/00_sick_man.txt'
old=read(LOT/'before',p);new=read(ROOT,p)
a,b=fields(old),fields(new)
check('same_eight_journal_identifiers',[x.key for x in a]==[x.key for x in b] and len(a)==8)
for x,y in zip(a,b):
 if x.key!='je_sick_man_main':check('unchanged.'+x.key,signature(x.value)==signature(y.value))
 else:
  check('main_original_fields_and_outcomes_unchanged',seq(fields(x.body),{'current_value'})==seq(fields(y.body),{'current_value','possible','is_shown_when_inactive'}))
  check('main_exact_new_fields',len(fields(y.body))==len(fields(x.body))+2)
main=node(new,'je_sick_man_main');shown=main.children('is_shown_when_inactive')[0];possible=main.children('possible')[0]
fixtures=[('early_TUR',dict(tag='TUR',vars={'ottoman_1776_initialized':1}),True,False),
 ('before_initialization',dict(tag='TUR',vars={}),False,False),
 ('foreign_country',dict(tag='RUS',vars={'ottoman_1776_initialized':1}),False,False),
 ('failure_before_delayed_event',dict(tag='TUR',vars={'ottoman_1776_initialized':1,'ottoman_1776_political_failed':1}),True,False),
 ('delayed_event_initialized',dict(tag='TUR',vars={'ottoman_1776_initialized':1,'ottoman_1776_political_failed':1,'ottoman_1776_sick_man_started':1}),True,True),
 ('political_success',dict(tag='TUR',vars={'ottoman_1776_initialized':1,'ottoman_1776_political_complete':1}),False,False),
 ('sick_man_completed',dict(tag='TUR',vars={'ottoman_1776_initialized':1,'sick_man_complete':1,'ottoman_1776_sick_man_started':1}),False,True)]
for label,ctx,visible,eligible in fixtures:
 check('journal_visibility.'+label,condition(shown.children(),ctx)==visible and condition(possible.children(),ctx)==eligible)

def progress(variables):
 ctx=dict(tag='TUR',vars=variables);value=0
 def run(items):
  nonlocal value
  for n in items:
   if n.key=='if':
    if condition(n.children('limit')[0].children(),ctx):run([x for x in n.children() if x.key!='limit'])
   else:
    z=variables[str(n.value)[4:]] if str(n.value).startswith('var:') else float(n.value)
    if n.key=='value':value=z
    elif n.key=='add':value+=z
    else:raise ValueError(n.key)
 run(main.children('current_value')[0].children());return value
check('inactive_progress_reads_no_missing_variable',progress({})==0)
for value in [0,1,2,3,4]:check('active_reform_progress.'+str(value),progress({'sick_man_var':value})==value)

p='common/scripted_effects/1776_ottoman_reform_effects.txt'
old,new=read(LOT/'before',p),read(ROOT,p)
oldfields,newfields=fields(old),fields(new)
check('same_scripted_effects',[x.key for x in oldfields]==[x.key for x in newfields])
for x,y in zip(oldfields,newfields):
 if x.key!='ottoman_1776_start_sick_man':check('unchanged_effect.'+x.key,signature(x.value)==signature(y.value))
start_before=selected(old,'ottoman_1776_start_sick_man');start_after=selected(new,'ottoman_1776_start_sick_man')
outer_before=one(fields(start_before.body),'if');outer_after=one(fields(start_after.body),'if')
inner=fields(outer_after.body)
guards=[x for x in inner if 'has_inactive_journal_entry' in x.value]
check('one_manual_add_fallback_guard',len(guards)==1)
guard=guards[0];add=one(fields(guard.body),'add_journal_entry')
check('starter_only_changes_main_add_guard',seq(fields(outer_before.body))==[(add.key,signature(add.value)) if x is guard else (x.key,signature(x.value)) for x in inner])
fallback=node(new,'ottoman_1776_start_sick_man').children('if')[0]
fallback=next(x for x in fallback.children('if') if any(n.key=='has_inactive_journal_entry' for n in walk(x.children())))
mainid='je_sick_man_main'
for active,inactive,expected in [(False,False,True),(False,True,False),(True,False,False),(True,True,False)]:
 ctx=dict(tag='TUR',active={mainid} if active else set(),inactive={mainid} if inactive else set())
 check(f'no_duplicate_main_add.active{active}.inactive{inactive}',condition(fallback.children('limit')[0].children(),ctx)==expected)

p='common/laws/00_church_and_state.txt'
before_laws,after_laws=fields(read(LOT/'before',p)),fields(read(ROOT,p));native_laws=fields(read(GAME,p))
check('same_shared_law_identifiers',[x.key for x in before_laws]==[x.key for x in after_laws])
for x,y in zip(before_laws,after_laws):
 if x.key!='law_state_religion':check('unchanged_law.'+x.key,signature(x.value)==signature(y.value))
 else:
  check('state_religion_only_changes_visibility',seq(fields(x.body),{'is_visible'})==seq(fields(y.body),{'is_visible'}))
  oldvis=one(fields(x.body),'is_visible');newvis=one(fields(y.body),'is_visible')
  check('original_muslim_variant_exclusions_retained',signature(one(fields(oldvis.body),'NOR').value)==signature(one(fields(newvis.body),'NOR').value))
nativevis=one(fields(one(native_laws,'law_state_religion').body),'is_visible')
check('native_generic_variant_exclusion',signature(one(fields(newvis.body),'NAND').value)==signature(one(fields(nativevis.body),'NAND').value))
restored=read(ROOT,'common/laws/1776_v115_caesaropapism.txt')
check('native_caesaropapism_token_equivalence',signature(one(fields(restored),'law_caesaropapism').value)==signature(one(native_laws,'law_caesaropapism').value))
parentvis=node(read(ROOT,p),'law_state_religion').children('is_visible')[0]
variantvis=node(restored,'law_caesaropapism').children('is_visible')[0]
for label,ctx,base,variant in [
 ('RUS_monarchy',dict(tag='RUS'),False,True),
 ('foreign_non_subject',dict(tag='FRA'),True,False),
 ('eligible_orthodox_subject',dict(tag='ALK',russian_subject=True,eligible_orthodox_subject=True),False,True),
 ('other_russian_subject',dict(tag='KZH',russian_subject=True),True,False),
 ('RUS_theocracy',dict(tag='RUS',laws={'law_theocracy'}),True,False),
 ('ottoman_millet',dict(tag='TUR',laws={'law_millet_system'}),False,False)]:
 check('law_visibility.'+label,condition(parentvis.children(),ctx)==base and condition(variantvis.children(),ctx)==variant)

p='common/history/countries/rus - russia.txt';before_country=read(LOT/'before',p);after_country=read(ROOT,p)
check('russian_profile_single_requested_law_change',after_country.replace('activate_law = law_type:law_caesaropapism','activate_law = law_type:law_state_religion',1)==before_country and after_country.count('activate_law = law_type:law_caesaropapism')==1)
laws={p.name:p for p in (GAME/'common/laws').glob('*.txt')};laws.update({p.name:p for p in (ROOT/'common/laws').glob('*.txt')})
definitions=[x.key for path in laws.values() for x in fields(path.read_text(encoding='utf-8-sig'))]
check('unique_effective_caesaropapism',definitions.count('law_caesaropapism')==1)
check('parent_definition_resolves',definitions.count('law_state_religion')==1)
helper='common/scripted_triggers/00_ip5_victoria_scripted_triggers.txt'
check('native_subject_helper_inherited',not (ROOT/helper).exists() and 'country_is_subject_type_valid_for_caesaropapism' in [x.key for x in fields(read(GAME,helper))])
check('native_icon_exists',(GAME/'gfx/interface/icons/law_icons/caesaropapism.dds').exists())
for lang in ['french','english']:
 native=read(GAME,f'localization/{lang}/laws_l_{lang}.yml')
 for key in ['law_caesaropapism','law_caesaropapism_desc']:check(f'native_localization.{lang}.{key}',bool(re.search(r'(?m)^\s*'+key+r':',native)))
 p=f'localization/{lang}/1776_ottoman_sick_man_visibility_l_{lang}.yml';data=(ROOT/p).read_bytes()
 check('localization_bom.'+lang,data.startswith(b'\xef\xbb\xbf'))
 check('localization_header.'+lang,data.decode('utf-8-sig').startswith('l_'+lang+':\n'))
 texts=[path.read_text(encoding='utf-8-sig') for path in (ROOT/'localization'/lang).rglob('*.yml')]
 check('single_activation_tooltip_key.'+lang,sum(len(re.findall(r'(?m)^\s*aor1776_sick_man_activation_tt:',x)) for x in texts)==1)
 check('referenced_political_journal_title_resolves.'+lang,any(re.search(r'(?m)^\s*je_1776_many_masters:',x) for x in texts))

before=json.loads((LOT/'BEFORE.json').read_text());scope=set(before['scope']);verified=0;concurrent=[]
for path,oldsha in before['protected'].items():
 if path in scope:continue
 # Functional files plus canonical text tracking; do not rehash archived source
 # imagery, PDFs or old experiment copies for these two bounded script changes.
 if not (path.startswith(('common/','events/','localization/','map_data/')) or Path(path).suffix in ['.md','.json']):continue
 p=ROOT/path;actual=digest(p) if p.exists() else None;verified+=1
 if actual!=oldsha:concurrent.append(dict(path=path,before=oldsha,after=actual))
for path,oldsha in before['native_hashes'].items():check('native_unchanged.'+path,digest(GAME/path)==oldsha)
check('git_head_unchanged',subprocess.check_output(['git','--no-optional-locks','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==before['git_head'])
check('git_index_unchanged',digest(ROOT/'.git/index')==before['git_index_sha256'])
result=dict(status='PASS_STATIC_ONLY',checks_passed=len(checks),checks=checks,protected_files_verified=verified,concurrent_changes=concurrent,runtime_tested=False,human_validated=False,limits=['Predicate and counter evaluation is a bounded Python model, not the Paradox scheduler.','Inactive-to-active refresh, deadline timing and save/reload require engine testing.','Starting law is a script request until a fresh game is observed.'])
(LOT/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},ensure_ascii=False))
