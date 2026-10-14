"""Explicit MAP2K transformations; emit apply_patch, never write gameplay directly."""
import json,difflib,re,collections as C
from pathlib import Path
import validate_diplomacy_ottoman_1776 as cw
from map_1776_audit import values
from map2a_patch import edits
from map2b_patch import state,region,append,transfer_pops
from map2k_work import ROOT,OUT,BASE,dump
MOVES=[('STATE_RHINELAND','BAV','KPF','x11C021'),('STATE_RHINELAND','BAV','KPF','x707505'),
 ('STATE_RHINELAND','PRU','KTR','xD080A0'),('STATE_HESSE','HES','KMZ','x1141A0'),('STATE_NORTH_RHINE','PRU','KCL','x518021')]
NEW={'KPF':('STATE_RHINELAND','BAV','Electoral Palatinate','Palatinat électoral','Karl_Theodor','von_Wittelsbach_Pfalz','1724.12.10',(215,170,50)),
 'KTR':('STATE_RHINELAND','PRU','Electorate of Trier','Électorat de Trèves','Clemens_Wenceslaus','von_Sachsen','1739.9.28',(160,85,115)),
 'KMZ':('STATE_HESSE','HES','Electorate of Mainz','Électorat de Mayence','Friedrich_Karl_Joseph','von_Erthal','1719.1.3',(190,58,48)),
 'KCL':('STATE_NORTH_RHINE','PRU','Electorate of Cologne','Électorat de Cologne','Maximilian_Friedrich','von_Koenigsegg_Rothenfels','1708.5.13',(115,125,185))}
ELECTORS={'mainz':'KMZ','trier':'KTR','cologne':'KCL','bohemia':'AUS','palatinate':'KPF','saxony':'SAX','brandenburg':'PRU','bavaria':'BAV','hanover':'HAN'}
MEMBERS=['AUS','KPF','KTR','KMZ','KCL','MOD','TUS','PAR','PRU','LUB','HAM','BRE','BRA','SCM','MST','OLD','HES','BAV','WUR','BAD','SAX','HEK','MEC','NAS','WEI','SCW','COB','MEI','ANH','WLD','LIP','FRM','HOL','HOH','BEO']
def transform(base):
 originals=base['originals']; result=dict(originals); manifest={'territorial':[],'population':[],'new_tags':list(NEW),'files':[]}
 geo=json.loads((ROOT/'docs/reports/map/MAP1/MAP1_GEOGRAPHIC_EVIDENCE/geometry_index.json').read_text())
 index={r['Province_ID']:r for r in __import__('map1_prepare').table(ROOT/'docs/reports/map/MAP1/MAP1_BASELINE_PROVINCE_INDEX.csv')}
 ratios={}
 for tag,(sid,old,*_) in NEW.items():
  before=[r['key'][0] for r in base['inventory']['owners'] if r['key'][1:]==[sid,old]]
  transferred=[rgb for s,o,t,rgb in MOVES if t==tag]
  numerator=sum(int(index[r]['Province_Pixels']) for r in transferred); denominator=sum(int(index[r]['Province_Pixels']) for r in before)
  ratios[tag]=(numerator,denominator)
 for sid,old,new,rgb in MOVES:
  path='common/history/states/00_states.txt';raw=result[path];src=next(n for n in state(raw,sid).children('create_state') if n.one('country')=='c:'+old);own=src.children('owned_provinces')[0]
  assert rgb in values(src,'owned_provinces'); frag=raw[own.start:own.end];frag=re.sub(r'\b'+rgb+r'\b','',frag)
  raw=edits(raw,[(own.start,own.end,frag)]);s=state(raw,sid);target=next((n for n in s.children('create_state') if n.one('country')=='c:'+new),None)
  if target:
   o=target.children('owned_provinces')[0];raw=edits(raw,[(o.end-1,o.end-1,' '+rgb+' ')])
  else:raw=edits(raw,[(s.end-1,s.end-1,'\n\t\t# MAP-2K: approved coarse electoral-state representation, no new RGB.\n\t\tcreate_state = { country = c:'+new+' owned_provinces = { '+rgb+' } }\n\t')])
  result[path]=raw;manifest['territorial'].append(dict(rgb=rgb,state=sid,before=old,after=new,classification='DOCUMENTED_GAMEPLAY_APPROXIMATION_USER_APPROVED',geometry=geo['bboxes'][rgb],rationale='Restore principal elector with native province; includes coarse non-electoral fragments. Exact historical boundary NOT claimed.'))
 # Exact profiles retained; partial splits use declared geometric allocation, not a census.
 for tag,(sid,old,*_) in NEW.items():
  for path in list(result):
   if '/pops/' not in path:continue
   raw=result[path]
   try:src=region(raw,sid,old)
   except StopIteration:continue
   num,den=ratios[tag];ops=[];fragments=[]
   for pop in src.children('create_pop'):
    count=int(pop.one('size'));amount=(count*num+den//2)//den
    if not amount:continue
    n=pop.children('size')[0];frag=raw[pop.start:pop.end];fragments.append('\t\t\t'+edits(frag,[(n.start-pop.start,n.end-pop.start,'size = '+str(amount))]))
    ops.append((pop.start,pop.end,'') if amount==count else (n.start,n.end,'size = '+str(count-amount)))
    manifest['population'].append(dict(state=sid,before_owner=old,after_owner=tag,culture=pop.one('culture'),religion=pop.one('religion','NATIVE_CULTURE_DEFAULT'),profile=cw.normalized([pop]),before=count,remaining=count-amount,transferred=amount,delta=0,method='Full existing state-country pool' if num==den else 'Integer native-land-area proportional split; demographic approximation, NOT historical census'))
   raw=edits(raw,ops);raw=append(raw,sid,tag,'\n'.join(fragments))
   if num==den:
    src=region(raw,sid,old);assert not src.children('create_pop');raw=edits(raw,[(src.start,src.end,'')])
   result[path]=raw
 # Split each actual ownership declaration. Preserve PM/reserves/private holders;
 # governmental holdings belonging to the administration of the territory follow it.
 for tag,(sid,old,*_) in NEW.items():
  num,den=ratios[tag]
  for path in list(result):
   if '/buildings/' not in path:continue
   raw=result[path]
   try:src=region(raw,sid,old)
   except StopIteration:continue
   ops=[];moved=[]
   for b in src.children('create_building'):
    lv=[n for n in cw.walk(b.children()) if n.key=='levels' and not isinstance(n.value,list)]
    if not lv:continue
    piece=raw[b.start:b.end];pops=[];remaining=[];total_new=0;total_old=0
    for n in lv:
     count=int(n.value);amount=(count*num+den//2)//den
     if b.one('building')=='building_government_administration' and count>0:amount=max(1,amount)
     amount=min(count,amount);total_new+=amount;total_old+=count-amount
     pops.append((n.start-b.start,n.end-b.start,'levels = '+str(amount)));remaining.append((n.start-b.start,n.end-b.start,'levels = '+str(count-amount)))
    if not total_new:continue
    moved_piece=edits(piece,pops)
    # No duplicated zero-level holders; remove them using parsed positions.
    def zero_holders(frag):
     ns=cw.parse(frag)[0];rm=[]
     for add in ns.children('add_ownership'):
      for h in add.children():
       if h.one('levels')=='0':rm.append((h.start,h.end,''))
     return edits(frag,rm)
    moved_piece=zero_holders(moved_piece)
    moved_piece=moved_piece.replace('country = c:'+old,'country = c:'+tag) if b.one('building') in ['building_government_administration','building_construction_sector'] else moved_piece
    moved.append('\t\t\t'+moved_piece)
    ops.append((b.start,b.end,'') if total_old==0 else (b.start,b.end,zero_holders(edits(piece,remaining))))
   raw=edits(raw,ops);raw=append(raw,sid,tag,'\n'.join(moved))
   if num==den:
    src=region(raw,sid,old);assert not src.children('create_building');raw=edits(raw,[(src.start,src.end,'')])
   # Bavarian investors retain ownership, but their HQ cannot stay in an empty subdivision.
   if tag=='KPF':
    ops=[]
    for n in cw.walk(cw.parse(raw)):
     if n.key=='building' and isinstance(n.value,list) and cw.scalar(n.one('country'))=='c:BAV' and cw.scalar(n.one('region'))=='STATE_RHINELAND':
      q=n.children('region')[0];ops.append((q.start,q.end,'region = "STATE_BAVARIA"'))
    raw=edits(raw,ops)
   result[path]=raw
 # Remove empty original Bavarian state; no other country loses its state pool.
 path='common/history/states/00_states.txt';raw=result[path];src=next(n for n in state(raw,'STATE_RHINELAND').children('create_state') if n.one('country')=='c:BAV');assert not values(src,'owned_provinces');result[path]=edits(raw,[(src.start,src.end,'')])
 for tag,(sid,old,en,fr,first,last,birth,color) in NEW.items():
  assert tag not in base['inventory']['countries']
  result['common/country_definitions/1776_imperial_electoral_states.txt']=result.get('common/country_definitions/1776_imperial_electoral_states.txt','')+f'{tag} = {{\n color = {{ {color[0]} {color[1]} {color[2]} }}\n country_type = recognized\n tier = principality\n cultures = {{ '+('south_german' if tag=='KPF' else 'north_german')+f' }}\n religion = catholic\n capital = {sid}\n}}\n'
  # Preserve functioning initial PM technology; same western starting tier.
  source=next((p for p in originals if p.startswith('common/history/countries/') and p.split('/')[-1].lower().startswith(('bav' if tag=='KPF' else 'hes')+' ')),None)
  ns=next(n for n in cw.walk(cw.parse(originals[source])) if n.key=='c:'+('BAV' if tag=='KPF' else 'HES'))
  techs=[n.value for n in ns.children('add_technology_researched')]
  body='\n'.join('  add_technology_researched = '+str(t) for t in techs)
  body+='\n  effect_starting_politics_reactionary = yes\n  activate_law = law_type:law_monarchy\n' if tag=='KPF' else '\n  effect_starting_politics_reactionary = yes\n  activate_law = law_type:law_theocracy\n  activate_law = law_type:law_state_religion\n'
  result[f'common/history/countries/{tag.lower()} - imperial electorate.txt']='COUNTRIES = {\n c:'+tag+' ?= {\n'+body+' }\n}\n'
  char=f'CHARACTERS = {{\n c:{tag} ?= {{\n  create_character = {{\n   first_name = {first}\n   last_name = {last}\n   historical = yes\n   culture = primary_culture\n   religion = rel:catholic\n   ruler = yes\n   birth_date = {birth}\n   interest_group = '+('ig_landowners' if tag=='KPF' else 'ig_devout')+'\n   ideology = ideology_traditionalist\n  }\n }\n}\n'
  result[f'common/history/characters/1776_elector_{tag.lower()}.txt']=char
 # Existing ruler Joseph remains heir of Austria, emperor of the bloc, NOT replaced by Maria Theresa.
 path='common/history/characters/aus.txt';raw=(ROOT/path).read_text(encoding='utf-8-sig');j=next(n for n in cw.walk(cw.parse(raw)) if n.key=='create_character' and n.one('first_name')=='"Joseph"');raw=edits(raw,[(j.end-1,j.end-1,'\n   on_created = { set_variable = aor1776_hre_emperor_character }\n  ')]);result[path]=raw
 # Restore requested original war goals while preserving tested counteroffensive.
 path='common/history/diplomatic_plays/00_otto_iraqi_persia_war.txt';raw=result[path];play=next(n for n in cw.walk(cw.parse(raw)) if n.key=='create_diplomatic_play')
 raw=edits(raw,[(play.end-1,play.end-1,'\n   # MAP-2K follow-up: original Iraqi and Omani claims restored by user.\n   add_target_backers = { c:ARB }\n   add_war_goal = { holder = c:IR1 type = conquer_state target_state = s:STATE_KHUZESTAN.region_state:ARB }\n   add_war_goal = { holder = c:OMA type = take_treaty_port target_state = s:STATE_FARS.region_state:PER }\n  ')]);result[path]=raw
 manifest['ratios']=ratios
 return result,manifest
def emit(result,manifest):
 patches=['*** Begin Patch']
 for path,new in result.items():
  old=(ROOT/path).read_text(encoding='utf-8-sig') if (ROOT/path).exists() else None
  if old==new:continue
  manifest['files'].append(path)
  if old is None:patches.extend(['*** Add File: '+str(ROOT/path),*['+'+l for l in new.splitlines()]])
  else:
   diff=list(difflib.unified_diff(old.splitlines(),new.splitlines(),n=3));patches.append('*** Update File: '+str(ROOT/path))
   for l in diff[2:]:patches.append('@@' if l.startswith('@@') else l)
 patches.append('*** End Patch');(OUT/'IMPLEMENTATION.patch').write_text('\n'.join(patches)+'\n',encoding='utf-8');dump('PLAN.json',manifest)
if __name__=='__main__':
 result,manifest=transform(json.loads(BASE.read_text()));emit(result,manifest);print('Prepared',len(manifest['files']),'files;',len(manifest['territorial']),'RGB transfers')
