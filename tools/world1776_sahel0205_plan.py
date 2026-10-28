"""Explicit native-province political approximations, reviewed against sources.

No nearest-capital partition, generated rectangles, new bitmap or implicit apply.
Remaining() enumerates the already reviewed remainder of a named owner portion;
it is not a geographic interpolation. Every resulting RGB is written to PLAN.json.
"""
import world1776_sahel01 as old

ROOT = old.ROOT
LOT = old.b.OUT / 'SAHEL-02-05'
PREFIX = '1776_world_sahel0205'
BASE = old.TECHS
RURAL = ['improved_agricultural_implements', 'improved_husbandry',
         'traditional_food_processing', 'organized_workshops']
MIL = 'organized_military_establishments'

# Each profile has a local rationale; no tier effect or metropolitan copy.
# Non-granted textile specialisation in small states is an open review, not
# a historical assertion that their inhabitants could not weave.
COUNTRIES = {
 'BAO': dict(fr='Baol', en='Baol', color=[181,149,68], culture=['wolof'], religion='animist', capital='STATE_SENEGAL', tech=BASE, basis='Wolof cereal/cattle economy, weaving and metalcraft, royal commercial diplomacy; Becker/Martin 1975.'),
 'SLU': dict(fr='Saloum', en='Saloum', color=[99,147,111], culture=['mande','wolof'], religion='animist', capital='STATE_SENEGAL', tech=BASE, basis='Cereal/cattle economy, dyeing/weaving and salt/river trade; Guelwar monarchy and commercial treaties. Culture identifiers are inherited regional proxies, not Serer ethnography.'),
 'TMB': dict(fr='Tombouctou', en='Timbuktu', color=[191,151,97], culture=['songhai'], religion='sunni', capital='STATE_TIMBUKTU', tech=BASE+[MIL,'shaft_mining','organized_financial_institutions'], basis='Resident Arma/civic authority, Niger-Saharan trade, salt extraction and merchant credit/accounting, craft economy and military garrison. Parentless era-1 salt/merchant capabilities support inherited salt mine and ordinary exchange PM; no maritime insurance or modern central bank granted.'),
 'TDM': dict(fr='Kel Tademekkat', en='Kel Tademekkat', color=[162,135,83], culture=['tuareg'], religion='sunni', capital='STATE_TIMBUKTU', tech=['improved_agricultural_implements','improved_husbandry','international_relations','traditional_food_processing','organized_workshops',MIL], basis='Pastoral Tuareg confederation, dependent Niger-bank cultivators, caravan diplomacy and armed retainers. Country knowledge includes subject cultivators, not only the ruling pastoral elite; specialised textile organisation is not separately certified.'),
 'GAO': dict(fr='Gao', en='Gao', color=[62,175,151], culture=['songhai'], religion='sunni', capital='STATE_TIMBUKTU', tech=BASE+[MIL], basis='Existing Tag reactivated for local Arma and riverine communities, not the Songhay imperial footprint. Garrison, craft and Niger trade capabilities.'),
 'SNU': dict(fr='Chefferies sénoufo', en='Senufo Chiefdoms', color=[111,147,74], culture=['senufo'], religion='animist', capital='STATE_EASTERN_MALI', kind='decentralized', tech=RURAL+['organized_textile_production'], basis='Plural Senufo agricultural/ironworking/weaving communities; no Kenedugu/Sikasso kingdom projected back from nineteenth century.'),
 'KNN': dict(fr='Kano', en='Kano', color=[79,154,152], culture=['hausa'], religion='sunni', capital='STATE_EAST_HAUSALAND', tech=BASE+[MIL], basis='Kano walled towns, military establishments, organised weaving/dyeing and long-distance trade; UNESCO V chapter 16.'),
 'KTS': dict(fr='Katsina', en='Katsina', color=[127,139,184], culture=['hausa'], religion='sunni', capital='STATE_OUTER_HAUSALAND', tech=BASE+[MIL], basis='Katsina merchant and textile centre with walled royal administration and garrison; UNESCO V chapter 16.'),
 'DAU': dict(fr='Daura', en='Daura', color=[185,174,132], culture=['hausa'], religion='sunni', capital='STATE_OUTER_HAUSALAND', tech=RURAL+['international_relations',MIL], basis='Small established Hausa monarchy, agriculture/cattle, artisans, diplomacy and royal retainers. Specialised textile organisation not separately certified.'),
 'KEB': dict(fr='Kebbi', en='Kebbi', color=[181,146,125], culture=['hausa','songhai'], religion='sunni', capital='STATE_HAUSALAND', tech=RURAL+['international_relations',MIL], basis='Kebbi river agriculture, pastoral economy, craft trade and military monarchy; Lovejoy map and UNESCO V. No caliphal administration inferred.'),
 'ZAM': dict(fr='Zamfara', en='Zamfara', color=[169,136,91], culture=['hausa'], religion='sunni', capital='STATE_HAUSALAND', tech=RURAL+['international_relations',MIL], basis='Zamfara surviving royal districts, agricultural and military organisation, independent of the future caliphate; eighteenth-century map and account.'),
 'ZAZ': dict(fr='Zazzau', en='Zazzau', color=[202,145,60], culture=['hausa'], religion='sunni', capital='STATE_EAST_HAUSALAND', tech=RURAL+['international_relations',MIL], basis='Zazzau royal towns and tributary agricultural districts, cavalry/retainers and regional diplomacy; Lovejoy map.'),
 'NUP': dict(fr='Nupe', en='Nupe', color=[155,169,90], culture=['hausa','tiv'], religion='animist', capital='STATE_HAUSALAND', tech=BASE+[MIL], basis='Nupe monarchy, Niger trade, craft/weaving and military establishments. Native hausa/tiv IDs are broad compatibility proxies; no Nupe culture exists in the installed catalogue.'),
 'ZRM': dict(fr='Pays zarma', en='Zarma Country', color=[160,121,92], culture=['songhai'], religion='animist', capital='STATE_OUTER_HAUSALAND', kind='decentralized', tech=RURAL+[MIL], basis='Plural western Niger/Zarma communities, not a new united kingdom of Dosso; rural production and retained native military-site capacity.'),
 'GWR': dict(fr='Pays gbagyi', en='Gbagyi Country', color=[155,123,77], culture=['hausa','tiv'], religion='animist', capital='STATE_EAST_HAUSALAND', kind='decentralized', tech=RURAL+[MIL], basis='Plural Gbagyi/Gwari communities outside Zazzau core, not a centralised invented state. Broad native culture proxies retained as a model limitation.'),
 'BCH': dict(fr='Pays du plateau de Bauchi', en='Bauchi Plateau Peoples', color=[130,144,100], culture=['hausa','tiv'], religion='animist', capital='STATE_NIGERIA', kind='decentralized', tech=RURAL+[MIL], basis='Plural plateau and Benue communities before the nineteenth-century emirate; inherited traditional military-site capacity, no united Bauchi emirate.'),
 'BTA': dict(fr='Peuples de la haute Bénoué', en='Upper Benue Peoples', color=[148,132,113], culture=['equatorial_bantu','tiv'], religion='animist', capital='STATE_NORTH_CAMEROON', kind='decentralized', tech=RURAL+[MIL], basis='Plural Bata, Mbum, Chamba and neighbouring communities; geographic decentralised aggregate, not an Adamawa emirate or single ethnic state. Native culture proxies are imprecise.'),
}


def words(text):
    return text.split()


def make_plan(states):
    plan = []
    def add(sid, source, dest, values, basis):
        colors = words(values) if isinstance(values,str) else list(values)
        assert colors and len(colors)==len(set(colors))
        plan.append(dict(state=sid, source=source, target=dest, RGBs=colors, historical_basis=basis,
                         precision='POLITICAL_APPROXIMATION_NATIVE_PROVINCES_NOT_CADASTRAL'))
    def remaining(sid, source, used):
        n = old.b.one(states,'s:'+sid)
        return [c for c in old.ids(old.part(n,source),'owned_provinces') if c not in used]
    add('STATE_SENEGAL','JLF','CAY','xAACD3D','Coastal/Ndiambour district between Waalo and Baol, east of the existing Cayor coastal portion; Ross comparative map, eighteenth-century Wolof sources.')
    add('STATE_SENEGAL','JLF','BAO','x7B4218 xCBF5C9','Baol/Lambaye-Diourbel core south of Cayor and west of residual Jolof; whole native provinces, not a new union with Cayor.')
    sine = words('x969FBB x8587D6')
    add('STATE_SENEGAL','SRR','SLU',remaining('STATE_SENEGAL','SRR',sine),'Separate Saloum east/south of the small Sine coastal core. Sine/Saloum estuarine boundary and maritime outlet remain coarse in the native mesh.')
    segu = words('xA41A10 x29246C x4B74E2 x8CCD97 xF0EFBF xD7C2F6 x70AF40 x67D3E7 x2A6A2D x0EA985 x688F7B x941ED5 xD5F34F x8CA2B5')
    senufo = words('xA8CAD8 x8DC430 xAAB26B x320EE8 x98DE99 x852260 x1221EE x9090A0 x109020')
    add('STATE_EASTERN_MALI','MSN','SGU',segu,'Segou proper and its middle Niger/Bani/central Bambara-Min(i)anka districts. Includes the native Segou hub x2A6A2D. No annexation of the entire Macina.')
    add('STATE_EASTERN_MALI','MSN','SNU',senufo,'Southern Senufo settlement belt including native Sikasso hub; plural chiefdoms, not the later Kenedugu kingdom.')
    tmb = words('xB86B73 xF070C0 x761045')
    gao = words('x6F19B8 xFEBD07 x80932B x052B92 x006306 xCC9597 x71F041')
    add('STATE_TIMBUKTU','MSN','TMB',tmb,'Timbuktu resident Arma/civic core and Niger bank; not a Massina possession in 1776.')
    add('STATE_TIMBUKTU','MSN','GAO',gao,'Gao and nearby riverine districts, separate from Massina. Arma local government and Tuareg influence distinguished from later Massina conquest.')
    add('STATE_TIMBUKTU','MSN','TDM',remaining('STATE_TIMBUKTU','MSN',set(tmb+gao)),'Tuareg-dominated Niger-bend/Gourma approaches, including Araouane route. Kel Tademekkat political envelope is approximate and contested with other nomadic/local groups; not exclusive land ownership.')
    h_ke = words('x569FF1 x347C9D xB0475D x8E8AC1 x0384A9')
    h_go = words('x96C7B6 xA2E6F9 xE04A46 x0DF31F xC76E76')
    h_nu = words('x90F068 x81A7FC xA15613 x6F05D2 x5DFEA9 x34871E x40DF11 x80DF90')
    h_za = words('x858543 xB44A59 xCAC7F9')
    add('STATE_HAUSALAND','SOK','KEB',h_ke,'Western river-side Kebbi wedge beside Niger and west of Zamfara; Lovejoy 2013 and UNESCO V map 16.3.')
    add('STATE_HAUSALAND','SOK','HAU',h_go,'Rima/Gobir northern approach. Native Gusau/Sokoto locator labels are displaced relative to one another and are not treated as cadastral evidence.')
    add('STATE_HAUSALAND','SOK','NUP',h_nu,'Southern Niger/Nupe districts east of Borgu, south of Zamfara/Zazzau; Lovejoy map.')
    add('STATE_HAUSALAND','SOK','ZAZ',h_za,'Eastern approach connecting Zazzau core; political frontier follows native edges rather than a straight line.')
    add('STATE_HAUSALAND','SOK','ZAM',remaining('STATE_HAUSALAND','SOK',set(h_ke+h_go+h_nu+h_za)),'Remaining central Zamfara belt between Gobir, Kebbi and Zazzau; surviving kingdom, not Sokoto caliphate.')
    gobir_west=words('x7EB3BB xB42598 xB5EEFE x477B47 x8B7291 x91CA6F x6C8962 xD28E66 x3921D3 x4E40D7')
    katsina=words('x80D945 xC9BC55 xADFCBB x93455F x1622C1 xECC181 x48B5C1 x7C3FD8 x50D09F x081330')
    daura=words('xB6B510')
    add('STATE_OUTER_HAUSALAND','SOK','HAU',gobir_west,'Gobir western/northwestern districts adjoining existing Gobir portion, not all territory around Niamey.')
    add('STATE_OUTER_HAUSALAND','SOK','ZRM',remaining('STATE_OUTER_HAUSALAND','SOK',set(gobir_west)),'Western Niger/Zarma communities outside Hausa kingdoms; no united state imposed.')
    add('STATE_OUTER_HAUSALAND','HAU','KTS',katsina,'Katsina/Maradi corridor east of Gobir; Maradi is used as a geographic anchor, not as a 1776 Katsina royal capital.')
    add('STATE_OUTER_HAUSALAND','HAU','DAU',daura,'Small Daura northern core east of Katsina and north of Kano; native mesh limits precision.')
    k=words('xF70F67 xB7F026 x827ADE x8E01B6 xAADBE3 xECD153 x4673BA x8F3133 x1DC6EF x773FBF x49D423 xD01160')
    z=words('x51D020 x5095EC x63D6E9 x52057E x3CA7DC xF6F846 x1090E0')
    g=words('xE738D0 x933DAA x18BCE8 xCBCB87 x803692 x436974 xC92C8F xACB5CC x41DF90')
    add('STATE_EAST_HAUSALAND','SOK','KTS','xFECA58','Southern Katsina margin adjoining its northern core.')
    add('STATE_EAST_HAUSALAND','SOK','DAU','x47577A','Daura connection to its small northern core; not an enclave.')
    add('STATE_EAST_HAUSALAND','SOK','KNN',k,'Kano and allied/walled dependent towns including the native Kano anchor. Hadejia/eastern fringe remains a coarse envelope; Bornu portion is untouched.')
    add('STATE_EAST_HAUSALAND','SOK','ZAZ',z,'Zaria/Zazzau central districts south of Kano, including Kaduna region; no Sokoto successor emirate inferred.')
    add('STATE_EAST_HAUSALAND','SOK','GWR',g,'Southern Gbagyi/Gwari and plateau frontier, plural communities not united by a new monarchy.')
    bta=words('xA591CC x1873FD x598F55 x2601BC xB6CC2E')
    gwr=words('x3DD80C x0031D6 xC06090 xADFC7B')
    add('STATE_NIGERIA','SOK','BTA',bta,'Eastern upper Benue/Mubi approaches; separate from the future caliphate.')
    add('STATE_NIGERIA','SOK','GWR',gwr,'Gbagyi/Benue transition beside southern Zazzau; broad decentralised native-model aggregate.')
    add('STATE_NIGERIA','SOK','BCH',remaining('STATE_NIGERIA','SOK',set(bta+gwr)),'Plural Bauchi plateau/Benue communities before Fulani emirates. This native state-region envelope is a coarse aggregate, not one historical kingdom.')
    add('STATE_NORTH_CAMEROON','SOK','BTA',remaining('STATE_NORTH_CAMEROON','SOK',set()),'Remove the future Adamawa/Sokoto territorial extension; upper Benue communities remain decentralised. Existing Bamum and Bornu borders untouched.')
    return plan
