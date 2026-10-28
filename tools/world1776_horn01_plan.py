"""Explicit political envelopes, 1776: no automatic geometric partition."""
import json
import world1776_horn01_inspect as h
ROOT,LOT,ST=h.ROOT,h.LOT,h.ST
PREFIX='1776_world_horn01'
BASE=list(h.prior.p.BASE);RURAL=list(h.prior.p.RURAL);MIL=h.prior.p.MIL
CENTRAL={
 'TGR':dict(capital='STATE_GONDER',tech=BASE+[MIL],basis='Tigrayan provincial lordship, highland agriculture, textiles/craft and armed retainers. University Hist.102 p107; northern regional core compared with Bahru p17 and Haberland. Not a modern ethnic-region boundary.'),
 'GJM':dict(capital='STATE_GONDER',tech=BASE+[MIL],basis='Gojjam lordship within the Blue Nile loop, provincial grain/cattle economy, craft and military retinue. Hist.102 pp107,117; regional approximation from river/locality comparison.'),
 'WLO':dict(capital='STATE_GONDER',tech=RURAL+['international_relations',MIL],basis='Wollo and adjoining Lasta chiefly networks; cereal/pastoral economy, craft, negotiation and retainers. Aggregate autonomy, not the later Yejju hegemony founded in 1786.'),
 'SHW':dict(capital='STATE_OROMIA',tech=BASE+[MIL],basis='Ankober/Menz/Yifat Shewan dynastic core under Asfa Wosen from 1775; Hist.102 p92. Excludes nineteenth-century expansion and the future Addis Ababa metropolis.'),
 'KFA':dict(capital='STATE_AMHARA',tech=BASE+[MIL],basis='Independent Kaffa court in the southwest, agricultural/textile/craft and exchange capability; Haberland pp802-805. Bonga core only, not modern Kaffa administrative province.'),
 'WLT':dict(capital='STATE_AMHARA',tech=BASE+[MIL],basis='Wolayta kingship attested before the eighteenth century, agrarian production and royal retainers; Haberland pp804-805. Oral dynastic legends do not certify each frontier.'),
 'AWS':dict(capital='STATE_GONDER',tech=RURAL+['international_relations',MIL],religion='sunni',basis='Awsa lower-Awash oasis polity, Afar court, agriculture/pastoralism, exchange and armed retainers; Haberland p789 and Hist.102. Not direct sovereignty over every Afar coastal sultanate.'),
 'HAR':dict(capital='STATE_OROMIA',tech=BASE+[MIL],basis='Independent Harar emirate and surrounding local authority, agriculture/crafts/textiles, caravan exchange and armed service; Hist.102 p92. Native Amhara culture is a catalogue proxy, not an ethnic claim.'),
 'YJR':dict(capital='STATE_AMHARA',tech=BASE+[MIL],new=True,fr='Yem',en='Yem',adj_fr='yem',adj_en='Yem',color=[173,118,161],culture=['sidama'],religion='animist',basis='Janjero/Yem court between Gibe and Omo systems, established before 1776; Haberland p805. Two-province core and native Sidama proxy, not full modern district or dynastic reconstruction.'),
 'HRI':dict(capital='STATE_SOMALILAND',tech=BASE+[MIL],new=True,fr='Hiraab',en='Hiraab',adj_fr='hiraab',adj_en='Hiraab',color=[197,157,133],culture=['somali'],religion='sunni',basis='Hiraab imamate/confederate authority and Mogadishu/central coast after Ajuran fragmentation; Kluijver thesis ch2 and Cassanelli ch4. Confederation, not homogeneous central administration.'),
}
DECENTRAL={
 'WLG':dict(capital='STATE_AMHARA',tech=RURAL,religion='animist',basis='Wallaga/Macha Oromo communities under Gadaa and local authorities before the nineteenth-century Leqa monarchies. Hist.102 pp114-116 and Mohammed Hassen SOAS thesis.'),
 'ARS':dict(capital='STATE_OROMIA',tech=RURAL,religion='animist',basis='Arsi and adjacent Oromo Gadaa communities east of the Rift; not a nineteenth-century monarchical state. Haberland regional narrative and Hist.102.'),
 'BRN':dict(capital='STATE_AMHARA',tech=RURAL,religion='animist',basis='Borana pastoral and Gadaa communities in the south, outside Gondarine direct government. Native tag, not a unitary sultanate.'),
 'OMO':dict(capital='STATE_AMHARA',tech=RURAL,religion='animist',basis='Plural southern/Omo communities outside reviewed royal cores. Native aggregate does not claim a single monarchy or ethnic homogeneity; Haberland pp802-805.'),
 'BJA':dict(capital='STATE_ERITREA',tech=RURAL,religion='sunni',basis='Beja/Bilen/Habab western lowlands, local authorities distinct from Asmara highlands and Ottoman harbours. Aggregate native tag; not a unified Beja kingdom.'),
 'OGD':dict(capital='STATE_OROMIA',tech=RURAL,religion='sunni',basis='Interior Somali pastoral communities outside Ethiopian direct authority; not a modern national boundary or ethnically uniform cadastral partition.'),
 'AFR':dict(capital='STATE_ERITREA',tech=RURAL+['international_relations'],new=True,fr='Pays afar',en='Afar Lands',adj_fr='afar',adj_en='Afar',color=[178,164,111],culture=['afar'],religion='sunni',basis='Plural Afar coastal and desert authorities outside Awsa royal core; maritime contacts and the inherited coastal anchorage. Ottoman claims do not establish direct highland administration.'),
 'HDY':dict(capital='STATE_AMHARA',tech=RURAL,basis='Autonomous Hadiya/Kambata highland communities, Hist.102 pp113-114; a plural local envelope, not revival of the vast medieval Hadiya kingdom.'),
}
COUNTRIES={**{t:dict(r,kind='unrecognized') for t,r in CENTRAL.items()},**{t:dict(r,kind='decentralized') for t,r in DECENTRAL.items()}}

def make_plan():
    rows=json.loads((LOT/'GEOMETRY_CELLS.json').read_text('utf8'));by={r['index']:r for r in rows};used=set();result=[]
    def pick(source,target,ids,basis):
        rr=[by[i] for i in ids];assert all(r['owner']==source for r in rr),(source,target,[(r['index'],r['owner']) for r in rr]);assert not used&set(ids)
        used.update(ids)
        for sid in dict.fromkeys(r['state'] for r in rr):result.append(dict(state=sid,source=source,target=target,RGBs=[r['RGB'] for r in rr if r['state']==sid],historical_basis=basis,precision='REVIEWED_NATIVE_POLITICAL_ENVELOPE_NOT_CADASTRAL'))
    pick('SD1','TGR',[6,8,13,16,17,26],'Asmara/Hamasien-Seraye highland nucleus adjoining Tigrayan lordship; no annexation of Ottoman Massawa harbour.')
    pick('SD1','AFR',[22],'Eastern Afar depression north of Awsa, not a detached Beja jurisdiction; plural local authority, no unitary Afar state asserted.')
    pick('SD1','BJA',[r['index'] for r in rows if r['state']=='STATE_ERITREA' and r['owner']=='SD1' and r['index'] not in used],'Remaining western Eritrean lowland local authorities, distinct from royal highlands; no modern Eritrean state projected backwards.')
    pick('ETH','TGR',[40,43,48,75,58,33,81,61,31,64,42,30,41,36,28],'Northern highland/Tigrayan provincial envelope, Mekele and access towards Asmara. Western Semien interfaces approximate, not a modern ethnic border.')
    pick('ETH','WLO',[38,45,53,56,63,69,44,68,70,49],'Wollo/Dessie-Lasta envelope east of the Gondarine core, retaining local autonomy; not the later Yejju empire.')
    pick('ETH','GJM',[78,50,67,47,34,51,73],'Gojjam nucleus within and along the Abbay/Blue Nile loop south of Lake Tana.')
    pick('ETH','SHW',[208,203,218,171,221,228,217],'Menz/Ankober/Yifat core: limited Shewa of 1776, no southern imperial conquests anticipated.')
    pick('ETH','AWS',[72,59,79,201,164,170],'Lower Awash/Asaita oasis royal core adjoining Afar country. Regional continuity is political approximation, not control of the entire coast.')
    pick('ETH','AFR',[5,7,18,20,21,66,158,173],'Coastal Afar and Awash-approach communities around the gulf, not Ethiopian direct rule or annexation by Awsa of every local sultanate.')
    pick('ETH','HAR',[152,174,187,204,166,207],'Harar/Charcar-Babile local and caravan hinterland, bounded native envelope touching Somali authorities; no whole Ogaden annexation.')
    pick('ETH','KFA',[126,139,146,127],'Bonga/Kaffa royal nucleus southwest of the Gibe communities, not future Jimma monarchy.')
    pick('ETH','WLT',[115,93,86,123],'Wolayta/Soddo royal nucleus west of the Rift; distinct from Kaffa and southern pastoral communities.')
    pick('ETH','YJR',[128,137],'Small Yem/Janjero royal nucleus between Gibe/Omo river systems; retained contact with neighbouring kingdoms.')
    pick('ETH','WLG',[118,122,35,148,114,83,117,133,124,107,143,175,206,234,109,105,111,142,113,87,89,90,91,92,94,97,98,102,108,112,131,136,140],'Wallaga and western/central Gibe and frontier communities; no Leqa-Naqamte, Jimma or Limmu-Enarya monarchies of the nineteenth century pre-installed. Western lowland jurisdictions remain approximate.')
    pick('ETH','HDY',[88,121,134],'Hadiya/Kambata highland local communities north of Wolayta, not disconnected portions of a single Omo state or a recreated medieval empire.')
    pick('ETH','OMO',[82,85,99,103,104,116,119,125,135,138,144,145,147,149],'Plural southwestern/Omo communities outside the Kaffa, Yem and Wolayta cores; no unified Sidama kingdom asserted.')
    pick('ETH','BRN',[84,95,96,100,101,106,110,120,129,130,132,141],'Southern Borana and adjacent pastoral communities, not Gondarine administration.')
    pick('ETH','ARS',[150,151,156,157,161,163,176,179,180,185,192,195,196,197,200,202,212,214,216,220,226,229,230,231],'Rift/eastern highland and Ittu Oromo communities with Gadaa authorities; boundaries follow reviewed native river/locality envelope, not later imperial provinces.')
    pick('ETH','OGD',[r['index'] for r in rows if r['owner']=='ETH' and r['index'] not in used and r['state']=='STATE_OROMIA'],'Remaining eastern Somali pastoral/interior envelope outside reviewed Harar and Oromo cores; not a claim of homogeneous tribal ownership.')
    # GLD keeps only its lower-Shabelle/Afgooye inland nucleus.
    gld_keep={263,289,344,352,307,295,318,296}
    hiraab_from_gld=[237,244,242,287,290,305,333,351]
    pick('GLD','HRI',hiraab_from_gld,'Mogadishu and central Benaadir/Hiraab coastal communities, separate from the inland Geledi court; no Omani direct annexation.')
    pick('GLD','OGD',[r['index'] for r in rows if r['owner']=='GLD' and r['index'] not in used and r['index'] not in gld_keep],'Interior and southern Somali communities outside the retained Geledi riverine nucleus, not its nineteenth-century expansion.')
    pick('MJT','HRI',[238,311,250,280,297,253,256,261,274,277,282,288,292,293,294,298,302,303,308,312,314,315,320,328,339,345,346,348,356,359],'Central Somali/Hobyo approaches before the nineteenth-century Majeerteen/Hobyo contest; Hiraab confederate envelope, not later Hobyo Sultanate.')
    return result

if __name__=='__main__':
    data=make_plan();h.dump('PLAN.json',data);h.dump('COUNTRY_PROFILES.json',COUNTRIES)
    print(len(data),'groups',sum(len(r['RGBs']) for r in data),'native cells',len(COUNTRIES),'profiles')
