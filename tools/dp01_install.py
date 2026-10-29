"""DP-01 bounded guarded history patch; --prepare/--apply/--audit.

Preserves inherited runtime baselines, other workers, POP cohort stocks and unit totals.
"""
from dp01 import *
from arabia01_install import popstock,buildingstock,counterjson
ST='common/history/states/00_states.txt'
POPS=['common/history/pops/09_central_asia.txt','common/history/pops/10_india.txt']
BUILD=['common/history/buildings/09_central_asia.txt','common/history/buildings/10_india.txt','common/history/buildings/98_build_start_1776_world_redistribution.txt']
MIL=['common/history/military_formations/04_military_formations_middle_east.txt','common/history/military_formations/05_military_formations_india.txt']
SCOPE=['STATE_BALUCHISTAN','STATE_QUETTA','STATE_HILL_PUNJAB','STATE_PUNJAB']
PROFILE=['improved_husbandry','international_relations','organized_textile_production','traditional_food_processing','organized_workshops','organized_military_establishments','regulated_small_arms']
LAWS=['monarchy','autocracy','people_of_the_book','subjecthood','hereditary_bureaucrats','peasant_levies','traditionalism','land_based_taxation','guild_system','serfdom','no_workers_rights','no_police','right_of_assembly','migration_controls','no_schools','no_health_system','no_womens_rights','child_labor_allowed','no_colonial_affairs']
def inside(raw,n):return raw[raw.index('{',n.start)+1:n.end-1]
def renamed(s,old,new):return s.replace('region_state:'+old,'region_state:'+new).replace('c:'+old,'c:'+new)
def put(files,rel,raw):files[rel]=encoded(ROOT/rel,raw) if (ROOT/rel).exists() else raw.encode('utf8')
def normalized_owners():
 d=C.defaultdict(set)
 for r,vs in ownership().items():d['x'+r[1:].upper()]|=vs
 return d
def audit_tech(name):
 from validate_starting_technology_1776 import collect_snapshot,audit_country
 s=collect_snapshot();result=[audit_country(t,s,dict(historical_evidence='DP-01 SOURCES.md and REPORT.md: specific restored profiles; inherited capabilities distinguished from census and sectoral certainty.')) for t in ['DUR','PAN','KAL','PTA']];dump(name,result);return result
def split_pops(raw,sid,moves):
 s=state_nodes(raw)[sid];src=s.children('region_state:DUR')[0];ps=src.children('create_pop');assigned=set();rows={}
 for t,indices in moves.items():
  assert not assigned&set(indices);assigned|=set(indices);rows[t]=[ps[i] for i in indices]
 rows['DUR']=[p for i,p in enumerate(ps) if i not in assigned]
 body='\n'.join('region_state:'+t+' = {\n'+'\n'.join(raw[p.start:p.end] for p in nodes)+'\n\t\t}' for t,nodes in rows.items() if nodes)
 return src,body,[dict(owner=t,total=sum(int(p.one('size')) for p in nodes),cohort_indices=[ps.index(p) for p in nodes]) for t,nodes in rows.items()]
def prepare():
 assert not (OUT/'APPLIED.json').exists()
 plan=load('PLAN.json');ow=normalized_owners();before=runtime();files={};ledger=[]
 for z in plan['transfers']:assert ow[z['rgb']]=={(z['state'],z['before'])}
 raw=text(ROOT/ST);ns=state_nodes(raw);patch=[]
 for sid in {z['state'] for z in plan['transfers']}:
  s=ns[sid];by=C.defaultdict(set);original={}
  for n in s.children('create_state'):
   t=scalar(n.one('country'))[2:];by[t]|=set(provs(n,'owned_provinces'));original[t]=n
  for z in plan['transfers']:
   if z['state']==sid:by[z['before']].remove(z['rgb']);by[z['after']].add(z['rgb'])
  for t,n in original.items():
   if set(provs(n,'owned_provinces'))!=by[t]:
    q=n.children('owned_provinces')[0];patch.append((q.start,q.end,'owned_provinces = '+rgb_block(by[t])))
  new=''.join('\n create_state = { country = c:'+t+' owned_provinces = '+rgb_block(rs)+' }\n' for t,rs in sorted(by.items()) if t not in original)
  patch.append((s.end-1,s.end-1,new))
 put(files,ST,edit(raw,patch))
 # Reuse current scaled cohorts whose source order can be checked against vanilla subdivisions.
 # This restores technical provenance, NOT a 1776 census or 1836 political borders.
 for rel in POPS:
  raw=text(ROOT/rel);patch=[]
  for sid,moves in ([('STATE_BALUCHISTAN',{'KAL':[3,4,5,6]}),('STATE_QUETTA',{'KAL':[8]})] if rel==POPS[0] else [('STATE_HILL_PUNJAB',{'PAN':list(range(7)),'PTA':list(range(12,18))})]):
   src,body,led=split_pops(raw,sid,moves);patch.append((src.start,src.end,body));ledger.append(dict(state=sid,allocations=led,policy='Conserved current cohort blocks; legacy country provenance checked separately. Quetta Brahui-labelled cohort is an explicit provisional local allocation, not an ethnic boundary or a new census.'))
  new=edit(raw,patch);assert popstock(raw)==popstock(new);put(files,rel,new)
 dump('POP_LEDGER.json',ledger)
 # Move Kalat's civil core; divide existing Hill-Punjab administration/roads, never duplicate levels.
 for rel in BUILD:
  raw=text(ROOT/rel);ns=state_nodes(raw);patch=[]
  if 'STATE_BALUCHISTAN' in ns:
   for n in ns['STATE_BALUCHISTAN'].children('region_state:DUR'):patch.append((n.start,n.end,renamed(raw[n.start:n.end],'DUR','KAL')))
  if 'STATE_HILL_PUNJAB' in ns:
   s=ns['STATE_HILL_PUNJAB'];src=s.children('region_state:DUR')
   if src:
    src=src[0];by=C.defaultdict(list)
    for b in src.children('create_building'):
     kind=scalar(b.one('building'));allocation={'DUR':2,'PAN':2,'PTA':1} if kind=='building_government_administration' else {'PAN':1,'PTA':1}
     old_levels=[n for n in walk(b.children()) if n.key=='levels'];assert len(old_levels)==1 and int(old_levels[0].value)==sum(allocation.values())
     for tag,number in allocation.items():
      snippet=raw[b.start:b.end];z=old_levels[0];snippet=snippet[:z.start-b.start]+'levels = '+str(number)+snippet[z.end-b.start:];by[tag].append(renamed(snippet,'DUR',tag))
    body='\n'.join('region_state:'+tag+' = {\n'+'\n'.join(bs)+'\n }' for tag,bs in by.items());patch.append((src.start,src.end,body))
  new=edit(raw,patch);assert buildingstock(raw)==buildingstock(new),rel
  if new!=raw:put(files,rel,new)
 # Existing conscripts follow transferred jurisdictions, not new invented standing armies.
 for rel in MIL:
  raw=text(ROOT/rel);patch=[]
  if rel==MIL[0]:
   dur=next(n for n in walk(parse(raw)) if n.key=='c:DUR')
   for f in dur.children('create_military_formation'):
    for u in f.children('combat_unit'):
     if scalar(u.one('service_type',''))=='conscript' and scalar(u.one('state_region')) in ['s:STATE_BALUCHISTAN','s:STATE_HILL_PUNJAB']:
      z=u.children('count')[0];expected=6 if scalar(u.one('state_region'))=='s:STATE_BALUCHISTAN' else 14;assert int(z.value)==expected;patch.append((z.start,z.end,'count = 2'))
  else:
   pan=next(n for n in walk(parse(raw)) if n.key=='c:PAN');f=pan.children('create_military_formation')[0];patch.append((f.end-1,f.end-1,'\n combat_unit = { type = unit_type:combat_unit_type_irregular_infantry service_type = conscript state_region = s:STATE_HILL_PUNJAB count = 8 }\n'))
  put(files,rel,edit(raw,patch))
 put(files,'common/history/military_formations/1776_dp01.txt','MILITARY_FORMATIONS = {\n'+''.join(' c:'+t+' ?= { create_military_formation = { type = army hq_region = sr:'+hq+' name = aor1776_dp01_'+t.lower()+'_levy combat_unit = { type = unit_type:combat_unit_type_irregular_infantry service_type = conscript state_region = s:'+sid+' count = 4 } save_scope_as = dp01_army_'+t.lower()+' } scope:dp01_ruler_'+t.lower()+' = { transfer_to_formation = scope:dp01_army_'+t.lower()+' } }\n' for t,hq,sid in [('KAL','region_greater_persia','STATE_BALUCHISTAN'),('PTA','region_north_india','STATE_HILL_PUNJAB')])+'}\n')
 # Existing country TAGs, each explicitly initialized. No shared industrial tier.
 for t in ['KAL','PTA']:
  rel='common/history/countries/'+('kal - kalat.txt' if t=='KAL' else 'pta - patiala.txt')
  tech=PROFILE if t=='KAL' else ['improved_husbandry','international_relations','organized_textile_production','traditional_food_processing','organized_military_establishments']
  laws=[x if x!='people_of_the_book' else ('people_of_the_book' if t=='KAL' else 'freedom_of_conscience') for x in LAWS]+['aor1776_dp01_customs','debt_slavery']
  put(files,rel,'COUNTRIES = { c:'+t+' ?= {\n'+''.join(' add_technology_researched = '+v+'\n' for v in tech)+''.join(' activate_law = law_type:law_'+v+'\n' for v in laws)+(' set_state_religion = rel:sikh\n' if t=='PTA' else ' set_state_religion = rel:sunni\n')+'} }\n')
 # Suppress 1836 character templates; the existing cleanup still creates Jassa Singh for PAN.
 put(files,'common/history/characters/pan - punjab.txt','CHARACTERS = { } # No Ranjit Singh or 1836 court in 1776; Jassa Singh is initialized by the existing cleanup.\n')
 for t in ['KAL','PTA']:
  rel='common/history/characters/'+('kal - kalat.txt' if t=='KAL' else 'pta - patiala.txt')
  put(files,rel,'CHARACTERS = { c:'+t+' ?= { create_character = { first_name = aor1776_dp01_'+t.lower()+'_ruler last_name = aor1776_dp01_empty_name historical = yes ruler = yes is_general = yes culture = cu:'+('baluchi' if t=='KAL' else 'panjabi')+' religion = rel:'+('sunni' if t=='KAL' else 'sikh')+(' age = 27 # Birth year 1748, no fabricated birthday\n' if t=='PTA' else '\n')+' interest_group = ig_landowners ideology = ideology_traditionalist save_scope_as = dp01_ruler_'+t.lower()+' } } }\n')
 # Suppress the 1839 succession journal at initialization only, not its future definition.
 rel='common/history/countries/pan - panjab.txt';raw=text(ROOT/rel);n=next(n for n in walk(parse(raw)) if n.key=='c:PAN');patch=[]
 for z in n.children('if'):
  if 'je_sikh_sovereignty' in raw[z.start:z.end]:patch.append((z.start,z.end,'# The 1839 maharaja succession journal is not initialized for the 1776 misl aggregate.'))
 put(files,rel,edit(raw,patch))
 # Same native customs variant structure already used in the repository, bounded to the two reactivated TAGs.
 put(files,'common/laws/1776_dp01.txt','''law_aor1776_dp01_customs = {
 group = lawgroup_trade_policy parent = law_mercantilism icon = "gfx/interface/icons/law_icons/mercantilism.dds" progressiveness = 0
 unlocking_technologies = { international_relations }
 is_visible = { OR = { c:KAL ?= this c:PTA ?= this } }
 can_enact = { OR = { c:KAL ?= this c:PTA ?= this } }
 modifier = { state_tariff_import_add = 0.50 state_tariff_export_add = 0.20 state_subvention_export_add = 0.50 state_subvention_import_add = 0.20 state_import_advantage_mult = -0.25 state_export_advantage_mult = 0.25 }
}
''')
 # Recognized suzerainty without recurring tribute. Offensive expedition aid remains unsimulated.
 subject=text(ROOT/'common/subject_types/1776_world_b02_ragusa.txt').replace('subject_type_aor1776_ragusan_tribute','subject_type_aor1776_kalat_suzerainty').replace('aor1776_ragusan_tribute','aor1776_kalat_suzerainty').replace('valid_overlord_country_types = { recognized colonial company }','valid_overlord_country_types = { unrecognized }')
 put(files,'common/subject_types/1776_dp01.txt',subject)
 put(files,'common/diplomatic_actions/1776_dp01.txt','''aor1776_kalat_suzerainty = {
 groups = { general } texture = "gfx/interface/icons/diplomatic_action_icons/tributary_15.dds"
 show_in_lens = no potential = { always = no }
 pact = { cost = 0 has_junior_participant = yes subject_type = subject_type_aor1776_kalat_suzerainty
 income_transfer = 0 second_country_gets_income_transfer = no income_transfer_based_on_second_country = yes
 actor_can_break = { always = yes } target_can_break = { always = yes } }
 ai = { will_break = { always = no } will_propose = { always = no } }
}
''')
 put(files,'common/history/diplomacy/1776_dp01.txt','DIPLOMACY = { c:DUR ?= { create_diplomatic_pact = { country = c:KAL type = aor1776_kalat_suzerainty } } }\n')
 # State hub references sampled at current effective named locators; no generated mesh moved.
 hub_changes={'STATE_BALUCHISTAN':{'city':'xBAE3D2','wood':'xF78D0D'},'STATE_PUNJAB':{'city':'xA6DAD0','mine':'x918140'},'STATE_HILL_PUNJAB':{'farm':'x280F05','wood':'x394B7F'}}
 for p in effective('map_data/state_regions'):
  raw=text(p);patch=[]
  for n in parse(raw):
   for k,r in hub_changes.get(n.key,{}).items():
    z=n.children(k)[0];patch.append((z.start,z.end,k+' = "'+r+'"'))
  if patch:put(files,p.relative_to(ROOT).as_posix(),edit(raw,patch))
 # Every new user-facing key has FR and EN text; inherited country names/flags reused.
 for lang in ['french','english']:
  fr=lang=='french';names={'aor1776_dp01_kal_ruler':('Mir Nasir Khan Ier','Mir Nasir Khan I'),'aor1776_dp01_pta_ruler':('Amar Singh','Amar Singh'),'aor1776_dp01_empty_name':('',''),'aor1776_dp01_kal_levy':('Levée de Kalat','Kalat levy'),'aor1776_dp01_pta_levy':('Levée de Patiala','Patiala levy'),'aor1776_kalat_suzerainty':('Suzeraineté durranie sur Kalat','Durrani suzerainty over Kalat'),'aor1776_kalat_suzerainty_desc':('Kalat reconnaît la suzeraineté du souverain durrani tout en conservant son gouvernement et son armée. Aucun tribut régulier ne lui est imposé.','Kalat acknowledges Durrani suzerainty while retaining its government and army. No regular tribute is imposed.'),'subject_type_aor1776_kalat_suzerainty':('Khanat autonome','Autonomous khanate'),'subject_type_aor1776_kalat_suzerainty_desc':('Le khanat conserve son gouvernement, ses forces et ses propres initiatives diplomatiques, sous une suzeraineté révocable sans versement régulier.','The khanate retains its government, forces and diplomatic initiatives under revocable suzerainty without regular payments.'),'law_aor1776_dp01_customs':('Droits de marché et de passage','Market and transit duties'),'law_aor1776_dp01_customs_desc':('Les marchands acquittent des droits aux marchés et aux passages contrôlés par les autorités locales.','Merchants pay duties at markets and passages controlled by local authorities.')}
  files['localization/'+lang+'/replace/1776_dp01_l_'+lang+'.yml']=b'\xef\xbb\xbf'+('l_'+lang+':\n'+''.join(' '+k+':0 "'+v[0 if fr else 1]+'"\n' for k,v in names.items())).encode()
 manifest=[]
 for rel,data in files.items():
  p=ROOT/rel;old=p.read_bytes() if p.exists() else None
  if old==data:continue
  if p.suffix=='.txt':parse(data.decode('utf-8-sig'))
  q=OUT/'staged'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(data)
  if old is not None:q=OUT/'preimages'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(old)
  manifest.append(dict(file=rel,before_sha256=sha(p) if p.exists() else None,after_sha256=sha(OUT/'staged'/rel)))
 dump('PREPARED.json',dict(files=manifest,world_before=before,ownership_before={r:sorted(vs) for r,vs in ow.items()},planned_transfers=plan['transfers']))
 print(json.dumps(dict(files=len(manifest),transfers=len(plan['transfers']),no_added_people=True,no_added_units=True)))
def apply():
 assert not (OUT/'APPLIED.json').exists();m=load('PREPARED.json')
 audit_tech('TECH_BEFORE.json')
 for z in m['files']:
  p=ROOT/z['file'];assert (sha(p) if p.exists() else None)==z['before_sha256'],('Concurrent change',z['file']);assert sha(OUT/'staged'/z['file'])==z['after_sha256']
 for z in m['files']:
  p=ROOT/z['file'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((OUT/'staged'/z['file']).read_bytes())
 dump('APPLIED.json',dict(status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',files=m['files'],game_launched=False,human_validated=False))
 print('DP-01 installed, runtime validation pending.')
if __name__=='__main__':
 if '--prepare' in sys.argv:prepare()
 elif '--apply' in sys.argv:apply()
