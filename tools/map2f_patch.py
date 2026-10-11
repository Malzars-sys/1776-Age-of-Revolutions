"""Build a narrow apply_patch from the immutable MAP-2F dirty-tree baseline.
Native provinces are approximations; allocation is technical, never a census.
"""
import collections as C,difflib,json
import validate_diplomacy_ottoman_1776 as cw
import validate_map2a as qa
from map2a_patch import state,edits,append
from map2e_patch import body_rewrite,apportion
from map2f_work import ROOT,OUT,BASE,TARGETS

# Each key is (native State Region, old territorial owner).
# Existing claims are left separate from effective administration.
GROUPS={
 ('STATE_BOMBAY','MARATH'):{'BIC':['xB0D0E0','xEBE18C']},
 ('STATE_CIRCARS','BIC'):{'HYD':['x11F0A0','x207C4F','x42F4F2'],'CAR':['x0AC82E','x180640','xCFF020','xE9BCE7']},
 ('STATE_MADRAS','PUD'):{
  'BIC':['x07104C'],
  'MYS':['x9E4F00','xB278DD','x2D75FD','x6A381C','x20A050'],
  'CAR':['x0559B3','x0E2990','x1FF7C6','x2EAD15','x486310','x56456B','x5AF5BE','x61FE06','x620762','x7CCE50','x99B424','x9A2EF3','xA021D0','xA3158E','xA63901','xAEAE4C','xEC1945']},
 ('STATE_GUJARAT','BHV'):{'BER':['xF87E91','x9C8D06','xCC1D23','x90B589','xADD2A3','x03C674','xECB4F5','x4EB354','x90052D','x128888','x3151E0','x4133D4']},
 ('STATE_RAJPUTANA','GWA'):{
  'JAS':['x006D72','x77810B','xBD0984','x6E8BCD','x1031A8','x599EC5','x6031A0','x25467F','x4CEAC0','x0C11FE'],
  'BIK':['x3C6F90','xD0F7A0','xA99FB3','x53A30A','x5DACF4','xEB0422','x9601FD','x01F0E0','xEBA05F','xF591B3','xF3C5EA','x84F1F8','x6A103F','x214E7A','xC40894','x0170B1'],
  'JOD':['x3FF532','x7B1C30','xDD12D2','x166BD9','x4922B9','xBD1F80','xC28B1B','xCA50D5','x5C95B5','x22627C','xD76ACC','xD77479','xCBE6C4','x9A6A95','x425430','xA389C9','xE0B020'],
  'MEW':['x40881F','xCC8FF3','xDCFF99','xF671B7','xF051DF','x0A34C2','x6E01FB','xA614CA'],
  'JAI':['x0710F5','x0A43D0','x4EA8C5','x5A410D','x604D2F','x61F021','x67EA54','x82B440','xA2025E','xB9580C','xBAD851','xBA06BC','xC7EF85','xFFFB3C','x2A57A1'],
  'KOT':['x37D8C4','xA9F108','xBC1373','xE27278','xE95A9E']},
 ('STATE_ASSAM','NGA'):{'ASM':['x12647B','x70069E','x4803C7','xA458FC','xFB1561','xDF30DF','x7DC31D','xEE6A3D','x673438']},
 ('STATE_ASSAM','TIP'):{'ASM':['xCC2DA0','x9700B9','x3FD07D','xF71958','x344BF5']},
 ('STATE_CEYLON','DEI'):{'KND':['x967CCE','xDAB923','x47B038','x8A707A']},
 ('STATE_BALUCHISTAN','OMA'):{'MAK':['xB7B2BD']},
}
REUSED=['CAR','BER','JAS','BIK','JOD','MEW','JAI','KOT','ASM','MAK']
NEW=['KND']
RATIONALE={
 'STATE_BOMBAY':('R4_BOMBAY_SALSETTE','Company Bombay since 1668 and occupied Salsette since 1774; no retroactive March 1776 treaty. Existing coastal RGBs exceed islands: minimal two-province proxy.'),
 'STATE_CIRCARS':('R4_GUNTUR_NELLORE','Guntur is excluded from British administration in 1776; Basalat Jang/Nizam authority represented by HYD. Nellore assigned to Carnatic, not a British presidency. Krishna boundary is approximate.'),
 'STATE_MADRAS':('R4_CARNATIC_MYSORE','Arcot rather than Pudukottai controls most Carnatic. Tanjore remains under Arcot until its April 1776 restoration. Salem/Baramahal and Coimbatore corridor assigned to Mysore; Pudukottai retains its interior province.'),
 'STATE_GUJARAT':('R4_GAEKWAD','Gaekwad/Maratha administration around Ahmedabad and Baroda represented by BER, not direct Bhavnagar sovereignty. Joint Peshwa revenue rights remain abstracted.'),
 'STATE_RAJPUTANA':('R4_RAJPUT_STATES','Restore six established Rajput authorities using contiguous broad province clusters. Ajmer remains Scindia/GWA; Kota also abstracts neighbouring Bundi. This is not a cadastral reconstruction.'),
 'STATE_ASSAM':('R4_AHOM','Ahom Brahmaputra valley under Lakshmi Singha restored via existing ASM tag. Southern tribal hills retained; eastern valley fringe and rebellion remain approximations.'),
 'STATE_CEYLON':('R4_KANDY','Independent Kandyan interior restored; Dutch coastal provinces and four named coastal hubs preserved. Cinnamon rights are economic rights, not sovereignty over all interior.'),
 'STATE_BALUCHISTAN':('R4_GWADAR','Omani Gwadar grant belongs to 1784, not 1776. MAK represents local Makran/Gichki authority; later Kalat revenue arrangements are not imposed retroactively.'),
 'STATE_BUNDELKHAND':('R4_BUNDELKHAND','Remove premature direct Company ownership; MARATH is a documented umbrella proxy for Maratha influence and local Bundela authorities, not uniform direct Peshwa administration.'),
}

def transform(base):
 result=dict(base['originals']);inv=base['inventory'];geo=json.loads((OUT/'GEOGRAPHY.json').read_text(encoding='utf-8'))['provinces']
 groups={k:dict(v) for k,v in GROUPS.items()}
 groups[('STATE_BUNDELKHAND','BIC')]={'MARATH':[r['key'][0] for r in inv['owners'] if r['key'][1:]==['STATE_BUNDELKHAND','BIC']]}
 raw=result['common/history/states/00_states.txt'];moves=[];weights={}
 for (sid,old),destinations in groups.items():
  assert sid in TARGETS
  cr=next(n for n in state(raw,sid).children('create_state') if n.one('country')=='c:'+old)
  ps=cr.children('owned_provinces')[0];pool=[cw.scalar(n.value) for n in ps.children()]
  selected=[v for vv in destinations.values() for v in vv];assert len(selected)==len(set(selected)) and set(selected)<=set(pool),(sid,selected)
  kept=[v for v in pool if v not in selected];ww=C.Counter()
  for v in pool:ww[next((t for t,vs in destinations.items() if v in vs),old)]+=geo[v]['pixels']
  weights[sid+'|'+old]=dict(ww)
  new='create_state = { country = c:'+old+' owned_provinces = { '+' '.join(kept)+' }'+(' state_type = '+cr.one('state_type') if cr.children('state_type') else '')+' }' if kept else ''
  # Merge into an existing subdivision when the country already has territory.
  extra=[]
  for tag,vs in destinations.items():
   exists=[n for n in state(raw,sid).children('create_state') if n.one('country')=='c:'+tag]
   if exists:
    at=exists[0].children('owned_provinces')[0].end-1;extra.append((at,at,' '+' '.join(vs)+' '))
   else:new+='\n\t\t# MAP-2F: documented existing-province approximation.\n\t\tcreate_state = { country = c:'+tag+' owned_provinces = { '+' '.join(vs)+' } state_type = '+('unincorporated' if tag=='BIC' else 'incorporated')+' }'
   for v in vs:
    code,note=RATIONALE[sid];moves.append({'rgb':v,'state':sid,'before':old,'after':tag,'decision':'DOCUMENTED_GAMEPLAY_APPROXIMATION','pixels':geo[v]['pixels'],'bbox':geo[v]['bbox'],'source_case':code,'note':note})
  raw=edits(raw,[(cr.start,cr.end,new),*extra])
 # Duplicate tokens repeat the same NAG owner, not competing sovereignties.
 cr=next(n for n in state(raw,'STATE_ORISSA').children('create_state') if n.one('country')=='c:NAG');ps=cr.children('owned_provinces')[0]
 vs=[cw.scalar(n.value) for n in ps.children()];raw=edits(raw,[(ps.start,ps.end,'owned_provinces = { '+' '.join(dict.fromkeys(vs))+' }')])
 result['common/history/states/00_states.txt']=raw
 # Create_pop bodies retain ALL fields other than integer size.
 for path,original in base['originals'].items():
  if not path.startswith(('common/history/pops/','common/history/population/')):continue
  ops=[];pending=[]
  for s in cw.walk(cw.parse(original)):
   sid=s.key.removeprefix('s:')
   for r in s.children():
    old=r.key.removeprefix('region_state:');key=sid+'|'+old
    if key not in weights:continue
    assert all(n.key=='create_pop' for n in r.children())
    popweights=weights[key]
    if key=='STATE_BOMBAY|MARATH':
     total=sum(v['count'] for v in inv['regional_pop'] if v['key'][:2]==['STATE_BOMBAY','MARATH'])
     # Whole coastal RGBs overstate the Company's island footprint. A bounded
     # 200,000-person technical pool avoids importing 1.5m mainland residents.
     # All remaining people stay MARATH, with every attribute conserved.
     popweights={'BIC':200000,'MARATH':total-200000}
    for p in r.children('create_pop'):
     for tag,n in apportion(int(p.one('size')),popweights).items():
      if n:pending.append((sid,tag,body_rewrite(original,p,'size',n)))
    ops.append((r.start,r.end,''))
  raw=edits(original,ops)
  for sid,t,frag in pending:raw=append(raw,sid,t,'\t\t\t'+frag)
  if ops:result[path]=raw
 # Split declared levels of each economic holder independently. Economic
 # countries, companies, methods and reserve FRACTIONS remain unchanged.
 # Operational ports/shipyards remain coastal; inland recruitment stays national.
 bt=[];hq=[];port_moves=[]
 for path,original in base['originals'].items():
  if not path.startswith('common/history/buildings/'):continue
  ops=[];pending=[]
  for s in cw.walk(cw.parse(original)):
   sid=s.key.removeprefix('s:')
   for r in s.children():
    old=r.key.removeprefix('region_state:');key=sid+'|'+old
    if key not in weights:continue
    assert all(n.key=='create_building' for n in r.children())
    for b in r.children('create_building'):
     kind=cw.scalar(b.one('building'));ww=weights[key]
     if kind in ['building_barracks','building_naval_base']:ww={old:1} if old in ww else {max(ww,key=ww.get):1}
     if kind in ['building_port','building_shipyard','building_military_shipyard','building_naval_administration'] and sid in ['STATE_CEYLON','STATE_GUJARAT','STATE_CIRCARS','STATE_MADRAS']:ww={old:1}
     levs=[n for n in cw.walk([b]) if n.key=='levels'];assert levs and all(int(n.value)>0 for n in levs)
     parts=[apportion(int(n.value),ww) for n in levs]
     # Ensure road minima in new populated subdivisions when conserved levels
     # suffice; take them from the largest road recipient, never create levels.
     if kind=='building_railway' and len(levs)==1:
      dd=parts[0]
      for t in sorted(ww):
       if dd[t]==0 and sum(dd.values())>=len(ww):
        donor=max(dd,key=dd.get)
        if dd[donor]>1:dd[donor]-=1;dd[t]+=1
     for t in ww:
      if not any(dd[t] for dd in parts):continue
      frag=original[b.start:b.end];e=[]
      # Zero ownership holders are removed, rather than invalid levels=0.
      for holder in b.children('add_ownership'):
       for h in holder.children():
        ll=h.children('levels');assert len(ll)==1
        i=levs.index(ll[0]);n=parts[i][t]
        e.append((h.start-b.start,h.end-b.start,'')) if not n else e.append((ll[0].start-b.start,ll[0].end-b.start,'levels = '+str(n)))
      frag=edits(frag,e);pending.append((sid,t,frag));bt.append([path,sid,old,t,kind,sum(dd[t] for dd in parts)])
    ops.append((r.start,r.end,''))
  raw=edits(original,ops)
  for sid,t,frag in pending:raw=append(raw,sid,t,'\t\t\t'+frag)
  # Newly restored Company coastal subdivisions need an existing port level.
  # Redistribute two BIC levels within R4: Bengal 3->2 and Circars 2->1.
  # Neither donor loses its port; no buildings/levels/owners/PMs are created.
  for donor,dest,expected in [('STATE_WEST_BENGAL','STATE_BOMBAY',3),('STATE_CIRCARS','STATE_MADRAS',2)]:
   ss=[n for n in cw.walk(cw.parse(raw)) if n.key=='s:'+donor]
   if not ss:continue
   rr=ss[0].children('region_state:BIC')
   if not rr:continue
   bb=[n for n in rr[0].children('create_building') if cw.scalar(n.one('building'))=='building_port']
   if not bb:continue
   assert len(bb)==1
   b=bb[0];ll=[n for n in cw.walk([b]) if n.key=='levels'];assert len(ll)==1 and int(ll[0].value)==expected
   frag=raw[b.start:b.end];split=edits(frag,[(ll[0].start-b.start,ll[0].end-b.start,'levels = 1')])
   raw=edits(raw,[(ll[0].start,ll[0].end,'levels = '+str(expected-1))]);raw=append(raw,dest,'BIC','\t\t\t'+split)
   port_moves.append({'file':path,'owner':'BIC','from':donor,'to':dest,'levels':1,'methods_and_reserve_fraction':'unchanged'})
  # Headquarters must refer to surviving owner subdivisions. No economic owner
  # is changed; only an owner's now-orphaned geographical headquarters moves.
  ops=[]
  for h in cw.walk(cw.parse(raw)):
   if h.key!='building' or not h.children('country') or not h.children('region'):continue
   tag=cw.scalar(h.one('country')).removeprefix('c:');sid=cw.scalar(h.one('region'))
   replacement={('OMA','STATE_BALUCHISTAN'):'STATE_OMAN',('BIC','STATE_BUNDELKHAND'):'STATE_BIHAR'}.get((tag,sid))
   if replacement:
    n=h.children('region')[0];ops.append((n.start,n.end,'region = "'+replacement+'"'));hq.append([path,tag,sid,replacement])
  raw=edits(raw,ops)
  if raw!=original:result[path]=raw
 # Gwadar's ten inherited Omani units cannot recruit in a province Oman no
 # longer owns. Only this necessary out-of-R4 recruitment reference changes.
 military=[]
 for path,original in base['originals'].items():
  if not path.startswith('common/history/military_formations/'):continue
  ops=[]
  for c in cw.walk(cw.parse(original)):
   if c.key!='c:OMA':continue
   for u in cw.walk([c]):
    if u.key=='combat_unit' and u.one('state_region')=='s:STATE_BALUCHISTAN':
     n=u.children('state_region')[0];ops.append((n.start,n.end,'state_region = s:STATE_OMAN'));military.append([path,cw.scalar(u.one('type')),int(u.one('count'))])
  if ops:result[path]=edits(original,ops)
 # Capitals of revived native tags are already defined; correct two inherited
 # mismatches. Culture/recognition/tiers of existing tags remain untouched.
 path='common/country_definitions/00_countries.txt';raw=result[path];ops=[]
 for c in cw.parse(raw):
  if c.key in ['JEY','COO']:
   n=c.children('capital')[0];ops.append((n.start,n.end,'capital = '+{'JEY':'STATE_CIRCARS','COO':'STATE_WEST_BENGAL'}[c.key]))
 result[path]=edits(raw,ops)
 result['common/country_definitions/04_1776_kandy.txt']='''# Kandyan authority, not the Kandahar KAN tag.
KND = { color = { 181 84 51 } country_type = unrecognized tier = kingdom cultures = { sinhala tamil } religion = theravada capital = STATE_CEYLON }
'''
 # Initialisation uses existing scripts, no fabricated British protectorate.
 result['common/history/countries/1776_map2f_carnatic_kandy.txt']='''COUNTRIES = {
 c:CAR ?= {
  add_technology_researched = distillation
  add_technology_researched = improved_husbandry
  add_technology_researched = organized_textile_production
  add_technology_researched = traditional_food_processing
  add_technology_researched = organized_workshops
  add_technology_researched = regulated_small_arms
  effect_starting_politics_princely_state = yes
 }
 c:KND ?= {
  add_technology_researched = distillation
  add_technology_researched = improved_husbandry
  add_technology_researched = traditional_food_processing
  add_technology_researched = organized_textile_production
  effect_starting_politics_princely_state = yes
  activate_law = law_type:law_freedom_of_conscience
  activate_law = law_type:law_debt_slavery
 }
}
'''
 # Replace an implausible Hyderabad/Pudukottai vassal dependency with Arcot's
 # nominal suzerainty: native tributary retains much greater local autonomy.
 path='common/history/diplomacy/00_subject_relationships.txt';raw=result[path]
 hy=next(n for n in cw.walk(cw.parse(raw)) if n.key=='c:HYD');pact=next(n for n in hy.children('create_diplomatic_pact') if n.one('country')=='c:PUD')
 result[path]=edits(raw,[(pact.start,pact.end,'# MAP-2F: Nizam nominal suzerainty over Arcot, not direct administration.\n\t\tcreate_diplomatic_pact = { country = c:CAR type = tributary }')])
 result['common/history/diplomacy/1776_map2f_gaekwad.txt']='''DIPLOMACY = {
 # Gaekwad belongs to the Maratha political/revenue system, with local autonomy.
 c:MARATH ?= { create_diplomatic_pact = { country = c:BER type = tributary } }
}
'''
 # Existing Sikh confederacy ruler (Jassa Singh) and formations are preserved.
 path='common/dynamic_country_names/00_dynamic_country_names.txt';raw=result[path];pan=next(n for n in cw.parse(raw) if n.key=='PAN');raw=edits(raw,[(pan.end-1,pan.end-1,'\n dynamic_country_name = { name = aor1776_sikh_confederacies adjective = PAN_ADJ is_main_tag_only = yes priority = 100 trigger = { exists = scope:actor scope:actor ?= { current_date < 1801.1.1 } } }\n')]);result[path]=raw
 result['common/history/characters/1776_map2f_restored_rulers.txt']='''CHARACTERS = {
 c:ASM ?= { create_character = { first_name = aor1776_lakshmi_singha last_name = aor1776_map2f_empty historical = yes culture = primary_culture ruler = yes age = 63 interest_group = ig_landowners ideology = ideology_traditionalist } }
 c:CAR ?= { create_character = { first_name = aor1776_muhammad_ali_wallajah last_name = aor1776_map2f_empty historical = yes culture = cu:tamil religion = rel:sunni ruler = yes age = 58 interest_group = ig_landowners ideology = ideology_traditionalist } }
 c:KND ?= { create_character = { first_name = aor1776_kirti_sri_rajasinha last_name = aor1776_map2f_empty historical = yes culture = cu:tamil religion = rel:theravada ruler = yes age = 41 interest_group = ig_landowners ideology = ideology_traditionalist } }
}
'''
 # Provisional identification flag composed of native components, not an
 # asserted exact reconstruction of the king's banner.
 result['common/coat_of_arms/coat_of_arms/05_1776_kandy.txt']='KND = { pattern = "pattern_solid.tga" color1 = "red" color2 = "yellow" colored_emblem = { texture = "ce_lion_rampant.dds" color1 = "yellow" instance = { scale = { 0.65 0.65 } position = { 0.5 0.5 } } } }\n'
 for lang in ['english','french']:
  fr=lang=='french';loc='\ufeffl_'+lang+':\n'
  pairs={'KND':('Kingdom of Kandy','Royaume de Kandy'),'KND_ADJ':('Kandyan','kandyen'),'aor1776_sikh_confederacies':('Sikh Confederacies','Confédérations sikhes'),'aor1776_lakshmi_singha':('Lakshmi Singha','Lakshmi Singha'),'aor1776_muhammad_ali_wallajah':('Muhammad Ali Wallajah','Muhammad Ali Wallajah'),'aor1776_kirti_sri_rajasinha':('Kirti Sri Rajasinha','Kirti Sri Rajasinha'),'aor1776_map2f_empty':('','')}
  for k,v in pairs.items():loc+=' '+k+':0 "'+v[int(fr)]+'"\n'
  result[f'localization/{lang}/1776_map2f_l_{lang}.yml']=loc
 changed={p:v for p,v in result.items() if v!=base['originals'].get(p)}
 assert len(port_moves)==2
 return changed,{'files':list(changed),'territorial':moves,'duplicates_removed':['xA0A8E0','xA15F01','x30C2D5'],'weights':weights,'building_transfers':bt,'port_redistributions':port_moves,'headquarters_references':hq,'military_recruitment':military,'reused_tags':REUSED,'new_tags':NEW}

def build(repair=False):
 base=json.loads(BASE.read_text(encoding='utf-8'));changed,plan=transform(base);patch='*** Begin Patch\n'
 for p,new in changed.items():
  if p not in base['originals'] and not repair:
   assert not (ROOT/p).exists(),'New-file collision '+p
   patch+='*** Add File: '+str(ROOT/p).replace('\\','/')+'\n'+''.join('+'+l+'\n' for l in new.splitlines())
  else:
   if not repair:assert (ROOT/p).read_text(encoding='utf-8-sig')==base['originals'][p],'Concurrent edit '+p
   old=(ROOT/p).read_text(encoding='utf-8-sig') if repair else base['originals'][p]
   if (ROOT/p).read_bytes().startswith(b'\xef\xbb\xbf'):old='\ufeff'+old
   if old.startswith('\ufeff') and not new.startswith('\ufeff'):new='\ufeff'+new
   if old==new:continue
   patch+='*** Update File: '+str(ROOT/p).replace('\\','/')+'\n'
   for l in list(difflib.unified_diff(old.splitlines(),new.splitlines(),n=6))[2:]:patch+=('@@' if l.startswith('@@') else l)+'\n'
 (OUT/'INTEGRATION.patch').write_text(patch+'*** End Patch\n',encoding='utf-8')
 (OUT/'PLAN.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
 print('Prepared',len(changed),'files;',len(plan['territorial']),'owner transfers; 3 duplicate tokens removed')
if __name__=='__main__':
 import sys
 build('--repair' in sys.argv)
