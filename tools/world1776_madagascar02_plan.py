"""Reviewed Malagasy political envelopes on native cells, no geometric partition."""
import json
import world1776_madagascar02_inspect as h
ROOT,LOT,ST=h.ROOT,h.LOT,h.ST
PREFIX='1776_world_madagascar02'
BASE=list(h.prior.p.BASE);RURAL=list(h.prior.p.RURAL);MIL=h.prior.p.MIL
COUNTRIES={}
def add(tag,side,kind,tech,fr,en,color,basis):
 COUNTRIES[tag]=dict(capital='STATE_'+side+'_MADAGASCAR',kind=kind,tech=tech,fr=fr,en=en,adj_fr=fr.lower(),adj_en=en,culture=['malagasy'],religion='animist',color=color,basis=basis,new=True)
royal=BASE+[MIL]
add('AVR','NORTH','unrecognized',royal,'Ambohimanga','Ambohimanga',[117,151,129],'Kent28pp949-951; Berg1988 extract: northern Imerina royal court distinct from Antananarivo before consolidation. Two native cells approximate the northern royal sector; court coordinates overlap the scale of neighbouring native cells, no precise cadastral boundary claimed. Irrigated rice, cattle, textile/metal craft, exchanges and royal armed retainers.')
add('AHI','NORTH','unrecognized',royal,'Ambohidratrimo','Ambohidratrimo',[172,137,119],'Kent28p950-951: western Imerina royal power not conquered until later1790s. Native western royal-sector envelope, not a new pixel-level palace boundary. Rice/cattle, weaving/workshops and court/market relations.')
add('BOI','NORTH','unrecognized',royal,'Boina','Boina',[158,124,150],'Kent28pp943-947: northwestern Sakalava court, markets and tribute networks, distinct from Menabe and Merina. Royal nucleus and adjoining directly associated western hinterland; not wholesale annexation of every tributary. Trading and military organisation; no commercial-insurance or gun-manufacturing technology.')
add('MEB','SOUTH','unrecognized',royal,'Menabe','Menabe',[157,119,82],'Kent28pp940-945: separate western Sakalava monarchy, riverine royal framework and stock/market economy; northern Boina distinct. Native coastal/interior envelope between western interfaces, not all ethnic Sakalava treated as direct subjects.')
add('ATK','NORTH','unrecognized',royal,'Antankarana','Antankarana',[151,151,97],'Kent28pp945-947: northern royal line and organisation borrowed from Boina, tribute attested before1776; autonomy preserved with native tributary pact. No claimed accession date installed. Native offshore islands remain with their mainland provinces.')
add('TMH','NORTH','decentralized',RURAL,'Tsimihety','Tsimihety',[140,165,119],'Kent28pp945-946: autonomous upper-Sofia/Mandritsara communities, no central kingdom or regular tribute. Rural farming/cattle/craft capabilities, no fictional monarch.')
add('BSM','NORTH','decentralized',BASE+[MIL],'Chefferies betsimisaraka','Betsimisaraka Chiefdoms',[132,163,157],'Kent28pp955-957,944: local filohany and autonomous clans persist after confederation; coastal armed commerce, royal influence and disputed Boina tribute do not equal uniform administration. Plural engine aggregate, not a single new national monarchy. Benyowsky/French coastal installations remain a documented local limitation.')
add('SNK','NORTH','decentralized',BASE,'Sihanaka','Sihanaka',[155,163,111],'Kent28pp951-952: fortified Alaotra communities, potters, bridge and trade; no central authority. Historical Boina tribute not converted into direct provincial rule or a native centralised-subject pact.')
add('BZN','NORTH','decentralized',BASE,'Bezanozano','Bezanozano',[160,150,115],'Kent28pp951-952: Ankay forest-route communities and fortified villages under local mpifehy; later short-lived kingship not projected automatically into1776. Indigenous markets/textile/metal craft and regional exchange.')
add('ANR','NORTH','decentralized',BASE,'Imamo et Andratsay','Imamo and Andratsay',[155,143,153],'Kent28p951: western Imamo and Betafo/Andratsay powers submitted only during later Merina consolidation. Explicit plural aggregate of distinct local authorities, potentially separated by royal cores; no unified ethnic monarchy claimed.')
add('ISD','SOUTH','unrecognized',royal,'Isandra','Isandra',[138,125,168],'Kent28pp947-949: eighteenth-century Andriamanalina court, royal rice/cattle reforms and diplomacy/armed retainers. Extent of hegemony and its chronology not treated as direct possession of all Betsileo.')
add('LLG','SOUTH','unrecognized',royal,'Lalangina','Lalangina',[171,143,93],'Kent28pp947-948: independent Betsileo court, national militia and rice reforms, resistance to later Merina demands. Court retained separately from Isandra, no exact1776 ruler invented.')
add('MDN','SOUTH','unrecognized',BASE,'Manandriana','Manandriana',[151,165,126],'Kent28pp947-949: royal formation afterc1750, submission to Merina c1800. Northern Betsileo three-cell court envelope, no forced1776 subject status.')
add('RND','SOUTH','unrecognized',royal,'Arindrano','Arindrano',[162,134,111],'Kent28pp947-948: southern Betsileo royal formation distinct from Lalangina/Isandra, neighbouring Bara. Native southern highland envelope; internal/later Isandra hegemony not certified as permanent direct rule.')
add('ATM','SOUTH','unrecognized',royal,'Antemoro','Antemoro',[136,155,135],'Kent28pp923-926,953,958: Matitana coastal royal society, sorabe specialists, rice/overseas commerce and royal conflict with Ikongo. National culture malagasy is a native proxy; no POP religion conversion or blanket Islamic state imposed.')
add('BHK','NORTH','unrecognized',BASE,'Antambahoaka','Antambahoaka',[162,147,128],'Kent28pp955,958: distinct southeastern coastal royal formation outside Betsimisaraka/Merina, around Mananjary. Small native littoral envelope, detailed dynasty/chronology unresolved.')
add('ATF','SOUTH','unrecognized',royal,'Antefasy','Antefasy',[178,146,116],'Kent28pp957-958: Ambaky/Farafangana royal power and maritime trade, distinct from Antemoro and Antesaka. Two native coastal-interface cells, no exact succession date asserted.')
add('ASK','SOUTH','unrecognized',royal,'Antesaka','Antesaka',[149,121,146],'Kent28pp957-958: Nosipandra/Vangaindrano royal line and rice economy; independent political formation before later Merina expansion. Native coastal sector, not precise final boundaries under late18c rulers.')
add('MSR','SOUTH','unrecognized',BASE+[MIL],'Fiherenana','Fiherenana',[139,162,160],'Kent28p932 and regional southwest discussion: Andrevola royal power in Fiherenana valley distinct from Sakalava-Maroserana. Coastal valley/river envelope, not uniform control over all southern Masikoro communities.')
add('IKO','SOUTH','unrecognized',royal,'Ikongo','Ikongo',[140,147,103],'Kent28pp952-953: Zafirambo royal centre recorded since1668, local law/ritual specialists and fortified royal rock, conflicts with Antemoro. Rice/cattle/craft and royal guard model; no later Merina alliance at start.')
add('TNL','SOUTH','decentralized',RURAL,'Communautés tanala','Tanala Communities',[130,160,133],'Kent28pp952-953: plural forest communities outside distinct Ikongo royal centre, never one all-Tanala state. Native northern forest sector, rural/craft capabilities without national institutions.')
add('BAR','SOUTH','decentralized',RURAL,'Chefferies bara','Bara Chiefdoms',[165,149,114],'Kent28pp953-955: multiple Zafimanely/clan kings and strong local councils, no single sovereign over all Ibara. Plural political aggregate, not absence of chiefs; pastoral/rural craft, no post1800 consolidation.')
add('MHF','SOUTH','decentralized',RURAL,'Royaumes mahafaly','Mahafaly Kingdoms',[161,139,124],'Kent28pp939-941: four independent Mahafaly kingdoms and clan authorities, not a single national monarchy. Native southwest strip aggregated at available scale; internal royal authority acknowledged, unresolved internal borders not invented.')
add('ATY','SOUTH','decentralized',RURAL,'Chefferies antanosy','Antanosy Chiefdoms',[155,145,169],'Kent28pp958-959: many small local kings in Ambolo/Mandrare, no unified large Antanosy state. Native southeast envelope; FortDauphin settlement attempt1767-1770 not projected as continuous French territorial administration.')
add('TDY','SOUTH','decentralized',RURAL,'Confédération antandroy','Antandroy Confederation',[169,162,133],'Kent28pp959-960: Karimbola autonomy and weakening Zafimanara confederation, continued local leaders, no whole southern peninsula ruled from Imerina. Pastoral/craft capabilities, no specific collapse date forced.')
add('CMO','SOUTH','decentralized',BASE,'Sultanats des Comores','Comorian Sultanates',[126,161,145],'Kent28pp960-964: separate island sultanates and rival local courts, no Merina authority. One inherited native province covers the archipelago; explicit plural autonomous aggregate rather than a unified Comorian state. Ports/craft/commerce model, not a historical national constitution.')
COUNTRIES['CMO'].update(culture=['swahili','malagasy'],religion='sunni')
COUNTRIES['MAD']=dict(capital='STATE_NORTH_MADAGASCAR',kind='unrecognized',preserve_knowledge=True,new=False,basis='Existing MAD retained as Antananarivo royal core; no island-wide Merina dominion in1776. Original technologies retained, no automatic industrial or military grant. Ruler/precise court boundary not invented.')

# Every list manually compared to the coast, regional geography and dated text.
# The native grid exceeds the scale of individual royal hills near Antananarivo.
CELLS={
 'MAD':[42,37], 'AVR':[12,41], 'AHI':[7,26],
 'ATK':[58,31,9,21,23,35,39,44,47,14,22],
 'BOI':[3,4,18,29,36,48,52,56,60,62,76,80,101,110,114,17,25],
 'TMH':[34,43,8,16,50,10],
 'BSM':[13,20,28,6,1,54,53,49,0,30,59,24,57],
 'SNK':[15,51,27,2], 'BZN':[11,45,19],
 'ANR':[33,38,32,40],
 'MEB':[55,102,108,112,118,92,87,115,66,68,72],
 'MDN':[71,103,69], 'ISD':[90,113,70], 'LLG':[96,78], 'RND':[91,121],
 'TNL':[116], 'IKO':[88,119], 'BHK':[46,5], 'ATM':[93,120,77],
 'ATF':[98,94], 'ASK':[64,82], 'ATY':[65,99], 'TDY':[97,107,117],
 'MHF':[86,79,89,106,111], 'MSR':[81,63,73,95], 'BAR':[61,67,83,105,104,109,84,75,100,74],
 'CMO':[85],
}
def make_plan():
 rows=json.loads((LOT/'GEOMETRY_CELLS.json').read_text('utf8'));by={r['index']:r for r in rows};selected=[i for ids in CELLS.values() for i in ids]
 assert len(selected)==len(set(selected)),[i for i in selected if selected.count(i)>1]
 assert set(selected)==set(by),('unassigned',set(by)-set(selected),'extra',set(selected)-set(by))
 out=[]
 for tag,ids in CELLS.items():
  if tag=='MAD':continue
  rr=[by[i] for i in ids]
  for sid in dict.fromkeys(r['state'] for r in rr):
   out.append(dict(state=sid,source='MAD',target=tag,RGBs=[r['RGB'] for r in rr if r['state']==sid],historical_basis=COUNTRIES[tag]['basis'],precision='MANUAL_NATIVE_CELL_POLITICAL_APPROXIMATION_NOT_CADASTRAL'))
 return out
if __name__=='__main__':
 h.dump('PLAN.json',make_plan());h.dump('COUNTRY_PROFILES.json',COUNTRIES);print('Transferred',sum(len(r['RGBs']) for r in make_plan()),'groups',len(make_plan()),'new TAGs',len(COUNTRIES)-1)
