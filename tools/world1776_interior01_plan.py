"""Reviewed native-cell transfers; no nearest-capital or geometric partition."""
import json
import world1776_interior01_inspect as h
ROOT,LOT,ST=h.ROOT,h.LOT,h.ST
PREFIX='1776_world_interior01'
BASE=list(h.prior.p.BASE);RURAL=list(h.prior.p.RURAL);MIL=h.prior.p.MIL
COUNTRIES={}
def add(t,capital,kind,tech,fr,en,culture,color,basis,**kwargs):
 COUNTRIES[t]=dict(capital='STATE_'+capital,kind=kind,tech=tech,fr=fr,en=en,adj_fr=fr.lower(),adj_en=en,culture=culture,color=color,religion='animist',basis=basis,new=True,**kwargs)
add('KSC','KASAI','decentralized',RURAL,'Pays du Kasaï et du Sankuru','Kasai and Sankuru Communities',['fluvian_bantu','luba'],[147,152,118],'Outside the retained Bushong/Kuba royal core: plural local communities between Kasai/Sankuru/Lulua. UNESCO20pp643-651; native culture cohorts preserved, no unitary new monarchy.')
add('LKS','KASAI','decentralized',RURAL,'Luba du Kasaï','Kasai Luba',['luba'],[143,131,172],'UNESCO20p649,651: Luba migrations north into Kasai, not direct extension of the Upemba royal administration. Existing native ethnic portion retained as local communities, no forced tributary link.')
add('MIA','CONGO_ORIENTALE','decentralized',RURAL,'Communautés du Maniema','Maniema Communities',['luba','fluvian_bantu'],[128,157,150],'UNESCO20map20.3 and expansion chronologypp648-656: forest and northern communities outside the reviewed eighteenth-century Upemba core; not wholesale nineteenth-century royal expansion.')
add('LMP','KATANGA','decentralized',RURAL+['shaft_mining'],'Lamba et communautés du cuivre','Lamba and Copper Communities',['luba','lacustrine_bantu'],[168,141,117],'UNESCO20pp643-660: southeastern copper communities outside the Luapula court. Locally attested preindustrial copper shafts justify shaft_mining for inherited mine rights/PM; no engines or industrial tier granted.')
add('ZPL','ZAMBIA','decentralized',RURAL,'Communautés des plateaux du Zambèze','Zambezi Plateau Communities',['kavango_bantu','lacustrine_bantu'],[157,157,111],'Plural Ila/Tonga/Nkoya/Lala and adjoining plateau communities outside the early Luyana floodplain nucleus. Mainga SOAS thesis abstract and Hogan chapter5 distinguish valley nucleus from later expansion. Broad residual envelope is explicit, not a tribal cadastral claim.')
add('LVL','ZAMBIA','decentralized',RURAL,'Luvale et Lwena','Luvale and Lwena',['lunda','ovimbundu'],[144,162,132],'UNESCO20pp655,660-661: upper-Zambezi western communities and Lwena/Lunda contacts. Native river/locality envelope only; no single Luvale monarchy or automatic subject status.')
add('MLG','KAZEMBE','decentralized',RURAL,'Lungu et Mambwe','Lungu and Mambwe',['lacustrine_bantu'],[158,171,126],'North Zambia/Tanganyika local communities outside the small early Bemba nucleus; Roberts1970chronology abstract and UNESCO21regional framework. Not nineteenth-century Bemba conquests.')
add('BSI','KAZEMBE','decentralized',RURAL+['international_relations'],'Bisa','Bisa',['lacustrine_bantu'],[172,152,116],'UNESCO21pp691-692: Bisa routes and reputation explicitly attested by1775; autonomous ivory carriers outside direct Bemba or Kazembe annexation. No unified royal kingdom asserted.')
add('TBK','KAZEMBE','decentralized',RURAL,'Communautés tumbuka','Tumbuka Communities',['lacustrine_bantu'],[172,148,143],'UNESCO21regional chronology and metallurgypp692-693: northern Malawi Tumbuka communities. No attempt to date every Chikulamayembe succession or unify all local chiefdoms.')
add('NGD','KAZEMBE','unrecognized',BASE+[MIL],'Ngonde','Ngonde',['lacustrine_bantu'],[150,124,85],'UNESCO21pp684-685: Kyungu royal power at Karonga plain before1720 and consolidation under Kasyombe c1750. Two native northern-Malawi cells, no expansion under Mwangonde after1785. Mixed farming/craft, exchange and royal retainers.')
add('KNY','KATANGA','unrecognized',BASE+[MIL],'Kanyok','Kanyok',['luba'],[148,118,148],'UNESCO20p649,656: Kanyok royal authority under Luba overlordship before the crisis1780-1810. MweneDitu/Kanyok native nucleus; tributary status models autonomy without exact fiscal schedule.')
add('BUS','UGANDA','decentralized',BASE,'Principautés du Busoga','Busoga Principalities',['baganda','lacustrine_bantu','luo'],[155,143,173],'UNESCO26pp855,862: nine states existed by1750, remaining distinct from Buganda. Plural autonomous royal/chiefly aggregate, not the later single Kyabazinga institution. Agriculture, stock, craft/weaving and lake exchanges.')
add('GSK','TANGANYIKA','unrecognized',BASE+[MIL],'Gisaka','Gisaka',['ruanda'],[164,122,117],'UNESCO26pp876-889: independent Gisaka east of Rwanda and linked to Karagwe; native single-cell royal envelope, not nineteenth-century Rwandan annexation. The disconnected northern candidate was excluded before installation.')
add('BGE','TANGANYIKA','unrecognized',BASE+[MIL],'Bugesera','Bugesera',['ruanda','rundi'],[171,151,91],'UNESCO26pp886-890: Bugesera still a political neighbour; partition at opening of nineteenth century. One native southern-Rwanda cell approximates royal core, no ruler chronology claimed.')
add('BHA','TANGANYIKA','unrecognized',BASE+[MIL],'Buha du Nord','Northern Buha',['rundi','lacustrine_bantu'],[119,147,160],'UNESCO26p887: northern Buha Bahumbi court before decline in mid19c. Native Malagarazi/Buyungu envelope, not direct Nyamwezi government.')
add('BHS','TANGANYIKA','unrecognized',BASE+[MIL],'Buha du Sud','Southern Buha',['rundi','lacustrine_bantu'],[157,132,163],'UNESCO26p887: Ruguru/Heru/Bushingo southern royal line separate from northern Buha. Western Tanganyika/Malagarazi native-cell envelope; no later Vinza chiefdom founded1800.')
add('KIZ','TANGANYIKA','unrecognized',BASE,'Kiziba','Kiziba',['lacustrine_bantu','baganda'],[134,164,103],'UNESCO26pp887-888: Kiziba between Kagera and Victoria, royal polity independent of later Buganda interventions; local agrarian/pastoral/artisanal exchange.')
add('KYM','TANGANYIKA','unrecognized',BASE,'Kyamutwara et Ihangiro','Kyamutwara and Ihangiro',['lacustrine_bantu','baganda'],[170,138,94],'UNESCO26pp887-888: neighbouring royal powers on westVictoria coast, represented together at available two-cell scale. Not annexation by Karagwe or later Maruku/Bugabo fragmentations.')
add('UDI','ZAMBEZIA','unrecognized',BASE+[MIL],'Undi','Undi',['chewa'],[163,117,81],'UNESCO21pp678-687: Undi Chewa monarchy west/southwest of Kalonga, weakened but not abolished by eighteenth-century fragmentation. No Ngoni/Maseko state before migrations.')
add('LDU','MOCAMBIQUE','unrecognized',BASE+[MIL],'Lundu','Lundu',['chewa','sena'],[128,147,83],'UNESCO21pp677-687: Lundu lowerShire monarchy with reduced influence; no direct sovereignty over all Makua and Lomwe interior in1776.')
add('UTV','ZAMBEZIA','unrecognized',BASE+[MIL],'Uteve','Uteve',['shona'],[157,126,107],'UNESCO22pp714-719 and coastal trading context: Uteve hinterland of Sofala, independent African authority distinct from Portuguese coastal fort. No Tswana realm placed here.')
add('TCH','LOURENCO_MARQUES','decentralized',RURAL,'Tonga, Chopi et Tsonga','Tonga, Chopi and Tsonga',['tonga'],[132,156,132],'Mozambique southern coastal communities; HPIP Inhambane and Hedges Delagoa Bay thesis distinguish local authorities from forts. No nineteenth-century Gaza/Ngoni/Tswana monarchy; existing POP attributes preserved, cultural reconstruction remains open. Native tonga is a broad Southern Bantu country-culture proxy, not a claim of ethnic identity; tsonga is not a valid engine culture.')
add('TMP','LOURENCO_MARQUES','unrecognized',BASE+[MIL],'Tembe','Tembe',['tonga'],[152,132,169],'Mathebula2017 NewContree78pp42-57 abstract: Tembe royal power at its late18c apogee south of MaputoBay. Small native-bay envelope; local Mpfumo/Maputo subdivisions unresolved. Hedges and peer-reviewed2024 study distinguish commerce from a permanent Portuguese territorial post. Native tonga is a broad Southern Bantu country-culture proxy; no POP conversion or new culture.')
# Existing active countries: preserve their entire initial knowledge rather than
# rewriting inherited tiers. Only a private political call and category/capital.
EXISTING={
 'LND':('KATANGA','unrecognized','UNESCO20pp655-660: central Rund/MwataYamvo realm around Mussumba; loose tributary empire, not a uniform colonial province.'),
 'LBA':('KATANGA','unrecognized','UNESCO20pp648-656: eighteenth-century Upemba/Lualaba royal core, northern/eastern19c expansion excluded.'),
 'KZM':('KAZEMBE','unrecognized','UNESCO20pp659-660: Luapula/Mweru Kazembe court founded before1776, nominal imperial tribute with broad internal autonomy.'),
 'KBA':('KASAI','unrecognized','UNESCO20pp643-651 and Bushong/Kuba region: retain compact royal core, distinguish adjoining communities. Independent pre-existing state, not a detached province of a distant parent.'),
 'LZO':('ZAMBIA','decentralized','Mainga1968 SOAS abstract; Hogan2015ch5: Luyana kingship fromc17c, floodplain nucleus distinct from later expansive Lozi/Barotse sphere. Kingship historically attested; inherited decentralised engine classification retained for this territorial lot, so no central enclave or fictional corridor to Portugal is created. Institutional refinement remains open.'),
 'BMB':('KAZEMBE','unrecognized','Roberts1970 chronology: early Chitimukulu court probably17c; no precise ruler chronology or late18c/19c expansion imposed.'),
 'MRV':('KAZEMBE','unrecognized','UNESCO21pp678-687: Kalonga royal nucleus under eighteenth-century fragmentation, not all Maravi peoples or whole northernMozambique.'),
 'MTP':('ZAMBEZI','unrecognized','UNESCO22 Mutapa court survives, reduced after Portuguese penetration and Rozvi secession; no whole empire of the16c reinstalled.'),
 'MNC':('ZAMBEZIA','unrecognized','UNESCO22pp714-741: Manica/Manyika royal and trading authority, not unstructured empty land; Rozvi overlordship chronology left for southern phase.'),
}
# Native inactive community tags receive explicit locally scoped rural profiles.
ACTIVATE={
 'MKU':('MOCAMBIQUE',RURAL,'Makua/Makonde local chiefdoms after Maravi decline; Alpers2021JAMH5p8 records independence and trade disputes around MozambiqueIsland.'),
 'LMW':('MOCAMBIQUE',RURAL,'UNESCO21pp677-687: Lomwe/Lolo authorities rejecting Lundu suzerainty during eighteenth century, farming and iron/craft.'),
 'UYA':('MOCAMBIQUE',RURAL+['international_relations'],'UNESCO21pp689-692: Yao homeland east ofMalawi and ivory caravans to coast before1776, not later militarised slave states.'),
 'SNA':('MOCAMBIQUE',RURAL,'Sena/Shire-Zambezi local communities outside Crown posts and prazos; no single central monarchy claimed.'),
 'CHW':('ZAMBEZIA',RURAL,'UNESCO21pp678-687: Chewa local authorities outside reviewed Kalonga/Undi/Lundu courts; native plural aggregate, not empty land.'),
}
for t,(cap,kind,basis) in EXISTING.items():COUNTRIES[t]=dict(capital='STATE_'+cap,kind=kind,preserve_knowledge=True,basis=basis,new=False)
for t,why in {'BMB':'Roberts1970 Chitimukulu regional political contacts; UNESCO21 regional exchange before later expansion.','MNC':'UNESCO22pp714-719: Manyika court negotiations and commerce with Portuguese traders and neighbouring powers.'}.items():
 COUNTRIES[t].update(targeted_grants=['international_relations'],targeted_grant_basis=why+' Minimal early diplomatic/market capability for private trade customs, not commercial insurance or a modern foreign ministry.')
for t,(cap,tech,basis) in ACTIVATE.items():COUNTRIES[t]=dict(capital='STATE_'+cap,kind='decentralized',tech=tech,basis=basis,new=False,activate=True)

def make_plan():
 rows=json.loads((LOT/'GEOMETRY_CELLS.json').read_text('utf8'));by={r['index']:r for r in rows};used=set();out=[]
 def pick(source,target,ids,basis):
  if not ids:return
  rr=[by[i] for i in ids];assert all(r['owner']==source for r in rr),(source,target,[(r['index'],r['owner']) for r in rr]);assert not used&set(ids),(source,target,set(ids)&used);used.update(ids)
  for sid in dict.fromkeys(r['state'] for r in rr):out.append(dict(state=sid,source=source,target=target,RGBs=[r['RGB'] for r in rr if r['state']==sid],historical_basis=basis,precision='EXPLICIT_NATIVE_CELL_POLITICAL_ENVELOPE_NOT_CADASTRAL'))
 def rest(source,target,sid,basis):pick(source,target,[r['index'] for r in rows if r['owner']==source and r['state']=='STATE_'+sid and r['index'] not in used],basis)
 # Interior royal cores and autonomous communities.
 kuba={207,161,187,163,205,186,162,201,206,184,179,177,172,195}
 pick('KBA','KSC',[r['index'] for r in rows if r['owner']=='KBA' and r['index'] not in kuba],'Kasai/Sankuru communities beyond compact Bushong/Kuba nucleus; no whole modernKasai province made royal land.')
 pick('LBA','KNY',[181,204,151,285,291,243,274,261],'Kanyok/MweneDitu royal nucleus, autonomous tributary ofLuba before nineteenth-century emancipation.')
 rest('LBA','LKS','KASAI','Kasai Luba communities distinct from direct Upemba crown administration.')
 rest('LBA','MIA','CONGO_ORIENTALE','Maniema/northern forest communities, not premature royal expansion ofLuba.')
 luba=[224,225,239,271,280,272,258,226,279,247,232,249,270,229,295,220,230]
 pick('KZM','LBA',luba,'Upemba/Lualaba royal envelope around Kamina/lakes; Kazembe belongs at Luapula/Mweru, not entire centralShaba.')
 pick('KZM','HMB',[273,252,241,248,284,269,234,246,256,257,276,278,282,289,294],'Hemba/northern easternLualaba communities outside both the Luapula court and reviewed eighteenth-century Upemba core; no later Luba eastward expansion.')
 lamba=[213,215,219,238,235,263,212,266,268,227,288,251,283,277,262,259,286]
 pick('KZM','LMP',lamba,'Southeastern copper and Lamba communities outside reviewed Kazembe/Luba royal cores.')
 lozi={372,420,431,432,399,388,444,441,428,384,363,387,408,374,393,425,386,395,406}
 luvale=[451,419,378,382,383,367,376,369,418,440]
 pick('LZO','LVL',luvale,'UpperZambezi/Luvale-Lwena western communities outside early Luyana floodplain nucleus.')
 pick('LZO','ZPL',[r['index'] for r in rows if r['owner']=='LZO' and r['index'] not in lozi and r['index'] not in used],'Plateau and southern/western peripheral communities, not the later extensive Barotse realm.')
 bemba={314,354,345,331,312,338,341,307,299,313}
 pick('BMB','TBK',[326,353],'Northern Malawi/Rumphi Tumbuka local communities, not later Bemba expansion.')
 pick('MRV','TBK',[324,301,325],'Northern/central Malawi communities beyond Kalonga court.')
 pick('BMB','NGD',[300,351],'Ngonde/Kyungu nucleus at Karonga plain, not Bemba or Lungu sovereignty in1776.')
 pick('BMB','MLG',[297,302,308,316,318,321,334,344,304],'Northern Tanganyika/Mbala Lungu-Mambwe communities distinct from small early Bemba nucleus.')
 pick('BMB','UDI',[349,305,303,315,319],'EasternChewa interface around Undi plateau, not Bemba territorial colony in1776.')
 pick('BMB','BSI',[r['index'] for r in rows if r['owner']=='BMB' and r['index'] not in bemba and r['index'] not in used],'Bisa and adjoining southern ivory-route communities outside early Bemba nucleus; native plural frontier approximation.')
 # Interlacustrine boundaries: keep uncertain Buddu/royal chronologies open.
 pick('BUG','BUS',[583,592,594,607,611,621],'Busoga and adjacent eastern-Nile principalities, distinct from Buganda; no retrospective unifiedKyabazinga.')
 pick('KRG','KIZ',[625],'Kiziba on Kagera/Victoria interface, not directKaragwe province.')
 pick('KRG','KYM',[648,692],'Kyamutwara/Ihangiro lake-shore powers, no later Buganda empire or19c fragment kingdoms imposed.')
 pick('KRG','GSK',[651],'Gisaka eastern royal interface outside Rwanda/Karagwe, cells approximate.')
 pick('RWD','BGE',[652],'Bugesera southern interface before nineteenth-century partition; Kigali remainsRwanda.')
 pick('NYM','BHA',[667,630,686],'Northern Buha royal nucleus north ofMalagarazi outside Nyamwezi authorities.')
 pick('NYM','BHS',[664,701,682,678,685],'SouthernBuha Ruguru/Heru/Bushingo envelope, notlater Vinza chiefdom of1800.')
 # Maravi fragmentation and northernMozambique independent local societies.
 pick('MSK','POR',[865,896,901],'Zumbo and attached Zambezi corridor: Portuguese feira before1776, notMasekoNgoni state. Coarse native-cell corridor, notuniform control.')
 pick('MSK','UDI',[878,867,898],'Undi Chewa royal hinterland distinct from Maseko/Ngoni migrations after1776.')
 pick('MSK','LDU',[885,889],'ReducedLundu court at lowerShire, notMaseko state.')
 rest('MSK','CHW','ZAMBEZIA','Other localChewa chiefs outside reviewed courts, notNgoni migrants.')
 pick('MRV','LDU',[798,813],'LowerShire Lundu riverine core; no annexation ofwhole Makua/Lomwe interior.')
 pick('MRV','SNA',[784,817,847],'Sena/lowerZambezi local communities around river outside Portuguese posts.')
 yao=[794,792,826,803,789,845,844,852,836,827,858,793,841,810]
 pick('MRV','UYA',yao,'Yao homeland/caravan communities around Lichinga/eastMalawi, not directMaravi administration.')
 lomwe=[787,820,855,859,850,805,831,833,835,812,830,849]
 pick('MRV','LMW',lomwe,'Lomwe/Lolo southern-interior local authorities aftereighteenth-centuryMaravi fragmentation.')
 rest('MRV','MKU','MOCAMBIQUE','Remaining Makua and northernchiefdom envelope outside Portuguese possessions and specificYao/Lomwe/Shire nuclei; no ethnicity claimed for every village.')
 pick('AGC','MKU',[809,848,860,790],'Peripheralcoast communities outside retainedAngoche nucleus; coastaltrade reach doesnot imply direct rule.')
 # Mozambique southerncoast: retainEuropean presence only at attested sites.
 rest('TSW','UTV','ZAMBEZIA','Uteve/Sofala African hinterland, not Tswana state; Portuguese Sofala fort preserved.')
 pick('TSW','POR',[1108],'Inhambane fortifiedsettlement/municipality attestedbefore1776; existing coastalprovinceproxy broaderthan town.')
 pick('POR','TMP',[1122],'DelagoaBay localTembe envelope before permanentPortuguese settlement after1781; notAustrian factory before1777.')
 pick('TSW','TMP',[1116,1118,1141],'Tembe bay/southerninterface with localMaputo subdivisions notcadastered; no nineteenth-centuryGaza kingdom.')
 rest('TSW','TCH','LOURENCO_MARQUES','SouthernMozambique localTonga/Chopi/Tsonga communities outside Tembe andInhambane, not Tswana/Botswana territory.')
 return out

if __name__=='__main__':
 h.dump('PLAN.json',make_plan());h.dump('COUNTRY_PROFILES.json',COUNTRIES);print('Transfers',sum(len(r['RGBs']) for r in make_plan()),'groups',len(make_plan()),'newTags',sum(r.get('new',False) for r in COUNTRIES.values()))
