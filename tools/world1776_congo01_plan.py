"""Explicit reviewed native-cell envelopes; not cadastral boundaries."""
import json
import world1776_congo01_inspect as h
ROOT,LOT,ST=h.ROOT,h.LOT,h.ST
PREFIX='1776_world_congo01'
BASE=list(h.prior.p.BASE);RURAL=list(h.prior.p.RURAL);MIL=h.prior.p.MIL
COAST=[t for t in BASE if t!='improved_husbandry']
COUNTRIES={
 'LNG':dict(capital='STATE_CONGO',kind='unrecognized',tech=COAST,basis='Vansina pp636-637: Loango crown and council still exist in 1776; succession collapse after1787 is not projected backwards. Coastal agriculture, raffia weaving, craft and commerce; no automatic pastoral or military grant.'),
 'TKE':dict(capital='STATE_CONGO',kind='unrecognized',tech=['improved_agricultural_implements','international_relations','traditional_food_processing','organized_workshops'],basis='Vansina pp604,636: Tio/Makoko kingdom, autonomous magnates and river commerce; civil war fromc1780 is later. Craft gate is capability, not assertion of local iron smelting; no textile/pastoral blanket grant.'),
 'YKA':dict(capital='STATE_BAS_CONGO',kind='unrecognized',tech=BASE+[MIL],basis='Vansina p642: Kwango Yaka kingdom formed1740-1760, conquering eastward before1776; royal and military organisation, agricultural and textile/craft exchange. Native territorial envelope remains approximate.'),
 'KSN':dict(capital='STATE_EAST_ANGOLA',kind='unrecognized',tech=BASE+[MIL],basis='Vansina pp618-621,642: Kasanje kingdom and Imbangala armed caravans on the upperKwango, distinct from Matamba and Portuguese Kwanza posts; mixed cultivation/husbandry/craft and commerce.'),
 'SYO':dict(capital='STATE_BAS_CONGO',kind='unrecognized',tech=BASE+[MIL],new=True,fr='Soyo',en='Soyo',adj_fr='soyo',adj_en='Soyo',color=[181,111,92],culture=['bakongo'],religion='catholic',basis='Vansina pp620-621 and Thornton chapter discussed in scholarly synthesis: autonomous Soyo survived the Kongo collapse; Mpinda/Soyo south of river. Agriculture, weaving/craft, maritime exchange and organised royal forces; no claim of modern Portuguese protection.'),
 'KKG':dict(capital='STATE_CONGO',kind='unrecognized',tech=COAST,new=True,fr='Kakongo',en='Kakongo',adj_fr='kakongo',adj_en='Kakongo',color=[174,149,76],culture=['bakongo'],religion='animist',basis='Vansina pp634-636: Kakongo court and Malemba trade after1750. Independent coastal polity north of Ngoyo, regional agri/textile/craft exchange; no claim to a livestock sector.'),
 'NGY':dict(capital='STATE_CONGO',kind='unrecognized',tech=COAST,new=True,fr='Ngoyo',en='Ngoyo',adj_fr='ngoyo',adj_en='Ngoyo',color=[134,113,159],culture=['bakongo'],religion='animist',basis='Vansina pp635-636: Ngoyo court and Cabinda port before Portuguese incursion1783. Small north-bank estuary polity, agriculture, raffia craft and commerce; no1783 occupation in1776.'),
 'MTM':dict(capital='STATE_EAST_ANGOLA',kind='unrecognized',tech=BASE+[MIL],new=True,fr='Matamba',en='Matamba',adj_fr='matamba',adj_en='Matamba',color=[158,91,112],culture=['ovimbundu'],religion='catholic',basis='Vansina pp614-620,641-642: Matamba court separate from Kasanje, upper interior east of Kwanza presidios; native Ovimbundu is catalogue proxy for Mbundu, not ethnic correction. Royal Christianity coexisted with local cults; agriculture, craft and armed service.'),
 'MBL':dict(capital='STATE_SOUTH_ANGOLA',kind='unrecognized',tech=BASE+[MIL],new=True,fr='Bailundo',en='Bailundo',adj_fr='bailundo',adj_en='Bailundo',color=[136,142,62],culture=['ovimbundu'],religion='animist',basis='Vansina p642: Mbailundu and Bihe royal development accelerated by campaigns from1772; highland cultivation, cattle, textiles, crafts, armed retinues and caravan exchanges. Small Bailundo nucleus north of Huambo, not all later kingdom.'),
 'BIE':dict(capital='STATE_EAST_ANGOLA',kind='unrecognized',tech=BASE+[MIL],new=True,fr='Bié',en='Bié',adj_fr='bié',adj_en='Bié',color=[179,139,66],culture=['ovimbundu'],religion='animist',basis='Vansina pp641-642: Bihé kingdom sheltering quimbares after1772; Cuito/Bié plateau east of Bailundo, agrarian/pastoral/textile/craft exchanges and royal armed service, no nineteenth-century expansion envelope.'),
 'DMB':dict(capital='STATE_NORTH_ANGOLA',kind='decentralized',tech=RURAL,new=True,fr='Dembos',en='Dembos',adj_fr='dembo',adj_en='Dembo',color=[131,162,119],culture=['bakongo','ovimbundu'],religion='animist',basis='Vansina pp604,635 and Africana Studia25p42: independent connected Ndembu authorities around Encoje, not direct Kongo or Portuguese administration. Mixed indigenous cultivation/craft, native culture proxies; no single sovereign Dembo monarchy.'),
 'KIS':dict(capital='STATE_EAST_ANGOLA',kind='decentralized',tech=RURAL,new=True,fr='Kisama et Libolo',en='Kisama and Libolo',adj_fr='kisama',adj_en='Kisama',color=[123,160,153],culture=['ovimbundu'],religion='animist',basis='Vansina regional map641 and Kwanza occupation history: plural independent local authorities south of Kwanza outside Portuguese posts and Ovimbundu royal nuclei. Native regional rural/craft profile, not a unitary Kisama state or complete ethnic partition.'),
 'MYU':dict(capital='STATE_GABON',kind='decentralized',tech=['improved_agricultural_implements','traditional_food_processing','organized_textile_production','organized_workshops'],new=True,fr='Mayumba et chefferies côtières',en='Mayumba and Coastal Chiefdoms',adj_fr='mayumba',adj_en='Mayumba',color=[168,158,107],culture=['bakongo'],religion='animist',basis='Vansina p636: distant Mayumba provinces seceded from Loango from1750. Southern Gabon coastal/local chiefdom aggregate only; inherited native Bakongo proxy, agriculture/raffia/craft, no unified new Mayumba monarchy.'),
}

# Domestic small stock is directly attested in the contemporary coastal account.
# This closes the local agricultural parent, not a grant of a later pastoral tier.
for t in ['LNG','TKE','KKG','NGY','MYU']:
 if 'improved_husbandry' not in COUNTRIES[t]['tech']:COUNTRIES[t]['tech'].append('improved_husbandry')
 COUNTRIES[t]['basis']+=' Dependency clarification: Proyart1776, chapterVI,p32(PDF38), records pigs/goats/sheep and fowl in the coastal kingdoms; small-stock capability closes the agricultural parent. For Tio interior this is a documented regional inference, not attestation of a large cattle sector.'

def make_plan():
 rows=json.loads((LOT/'GEOMETRY_CELLS.json').read_text('utf8'));by={r['index']:r for r in rows};used=set();result=[]
 def pick(source,target,ids,basis):
  rr=[by[i] for i in ids];assert all(r['owner']==source for r in rr),(source,target,[(r['index'],r['owner']) for r in rr]);assert not used&set(ids);used.update(ids)
  for sid in dict.fromkeys(r['state'] for r in rr):result.append(dict(state=sid,source=source,target=target,RGBs=[r['RGB'] for r in rr if r['state']==sid],historical_basis=basis,precision='NATIVE_CELL_POLITICAL_APPROXIMATION_NOT_CADASTRAL'))
 pick('LNG','KKG',[17,20],'Kakongo/Malemba coastal nucleus north of Cabinda; Vansina634-636. Native-cell envelope cannot certify coastal cadastral limits.')
 pick('LNG','NGY',[23],'Ngoyo/Cabinda north-bank coastal nucleus before1783; Vansina635-636.')
 pick('KON','NGY',[66],'North-bank estuary hinterland adjoining Ngoyo, not direct royal Kongo domain; river-locality comparison.')
 pick('KON','SYO',[86,65,134,119],'Mpinda/Soyo south-bank mouth and neighbouring coastal district, distinct from MbanzaKongo crown; boundary approximate.')
 pick('LNG','MYU',[r['index'] for r in rows if r['state']=='STATE_GABON' and r['owner']=='LNG'],'Northern coastal chiefdom aggregate after Mayumba secession fromLoango c1750; no precise cultural boundary asserted.')
 pick('KON','DMB',[126,118],'Ndembu local authorities south of royal Kongo core; not all Kongo-speaking lands under the crown.')
 pick('KSN','DMB',[317],'Ndembu eastern interface beside Matamba and Encoje, native-cell approximation.')
 pick('KON','POR',[136],'Encoje1759 small presidio represented by existing native cell; scope is fortified node and attached corridor, not uniform provincial control.')
 pick('KSN','POR',[231,199,305,320,264,315,235,252,238],'Connected Kwanza presidio corridor Muxima/Massangano/Cambambe/Ambaca/PungoAndongo, established before1776. Native-cell corridor is an explicit coarse political approximation, not title to all intervening villages.')
 pick('KSN','MTM',[212,245,250],'Matamba royal nucleus north/east of Kwanza posts, separate from Kasanje upperKwango market.')
 pick('YKA','MTM',[80,95],'Matamba northern interface adjoining native upperKwango nucleus, not Yaka nineteenth-century southward extension.')
 pick('CHK','KSN',[278,318,280,236],'Kasanje/Casanje upperKwango nucleus east of Kwanza posts, not all broad Chokwe interior.')
 pick('KSN','KIS',[239,284,294,246,213,259,251,323,338,332,297,271],'Local Kisama/Libolo and southern-Kwanza chiefdoms outside royal Kasanje and Portuguese posts; no all-interior colonial sovereignty.')
 pick('KSN','MBL',[269],'Northern Bailundo plateau interface adjoining Mbailundu nucleus; no full late19c sphere.')
 pick('OVM','MBL',[176,164,180,179,181],'Bailundo royal plateau core north of Huambo, one of two major kingdoms developing by1772; not whole Ovimbundu ethnic envelope.')
 pick('CHK','BIE',[258,243,324,260,254,288],'Bihé/Cuito highland royal nucleus east of Bailundo, distinct from later broad Chokwe expansion.')
 pick('POR','OVM',[143,156],'Portuguese coastal title narrowed away from inland districts north of Benguela; NovoRedondo coastal node retained.')
 pick('OVM','POR',[168,152,193,195],'Benguela-Caconda1769 attached road/presidio corridor on native cells, contiguous as explicitly required by player; broader than actual garrison reach, not all plateau.')
 return result

if __name__=='__main__':
 h.dump('PLAN.json',make_plan());h.dump('COUNTRY_PROFILES.json',COUNTRIES);print('Plan',sum(len(r['RGBs']) for r in make_plan()),'native RGBs',len(make_plan()),'groups')
