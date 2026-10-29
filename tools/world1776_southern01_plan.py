"""Reviewed native-cell envelopes for southern Africa, 1776; no nearest-city partition."""
import json
import world1776_southern01_inspect as h
ROOT,LOT,ST=h.ROOT,h.LOT,h.ST
PREFIX='1776_world_southern01'
BASE=list(h.prior.p.BASE);RURAL=list(h.prior.p.RURAL);MIL=h.prior.p.MIL
COUNTRIES={}
def add(t,capital,kind,tech,fr,en,cultures,color,basis,new=True):
 COUNTRIES[t]=dict(capital=capital,kind=kind,tech=list(tech),fr=fr,en=en,adj_fr=fr.lower(),adj_en=en,culture=cultures,religion='animist',color=color,basis=basis,new=new)
add('NST','STATE_ZULULAND','decentralized',BASE,'Chefferies nguni','Nguni Chiefdoms',['nguni'],[163,137,93],"Denoon23pp750-754; Hamilton/Wright2026 sections moving political mosaic and dynamic sovereignty; Bonner1983pp9-13. Northern Nguni farming and chiefly communities between Drakensberg and ocean; no unified Shaka empire in1776 and no Tswana sovereignty over Natal. Plural native coastal envelope; individual Mthethwa/Ndwandwe/Hlubi borders not invented.")
add('HVD','STATE_TRANSVAAL','decentralized',BASE,'Chefferies du Haut-Veld','Highveld Chiefdoms',['tswana','sotho','nguni'],[143,155,120],"Denoon23map23.1,pp750-754; Hamilton/Wright2026 mobility and political mosaics, archaeological references to Highveld stone settlements. Local Sotho/Tswana/Nguni authorities replace Transvaal republic and broad later Matabele envelope. Not a single Highveld state or cadastral tribal map; agriculture, cattle, local metal and textile crafts/exchanges.")
add('KQO','STATE_NORTHERN_CAPE','decentralized',RURAL,'Communautés de l’Orange','Orange River Communities',['khoisan','tswana'],[175,140,107],"Denoon23pp749,761 and map23.1; University Free State Griquatown heritage entry: San/Korana before mission1800-1804, Griqua state/name1813, Waterboer later. Plural Kora/San and neighbouring communities of middle Orange-Vaal; no Philippolis or Waterboer state in1776. Khoisan/Tswana national proxies only, inherited Griqua/Boer POP identities not converted.")
add('MSH','STATE_ZAMBEZI','unrecognized',[], 'Rozvi','Rozvi',['shona'],[174,143,104],"Bhila22pp714-718,map22.8 after Beach1984p38: Changamire royal formation centred on Butwa/Danangombe/Khami with extensive tributary authority; Manyika subordinate, Mutapa distinct. Retained native60-cell envelope is broad and includes uncertain western/northern margins. Court/army/craft/markets justify only early diplomatic and military capabilities, not industrial grants.",False)
COUNTRIES['MSH'].update(preserve_knowledge=True,targeted_grants=['international_relations','organized_military_establishments'])
add('BST','STATE_VRYSTAAT','decentralized',[], 'Chefferies sotho','Sotho Chiefdoms',['sotho'],[151,133,168],"Denoon23map23.1,pp750-754; no unified Moshoeshoe Basotho kingdom in1776. Plural Sotho authorities on Caledon/Drakensberg and adjacent Highveld. Existing knowledge and formations retained; later national polity/journal not projected backwards.",False)
COUNTRIES['BST'].update(preserve_knowledge=True)
add('MTB','STATE_TRANSVAAL','decentralized',[], 'Chefferies ndébélé','Ndebele Chiefdoms',['nguni'],[157,122,98],"Denoon23pp750-754; SAHRIS Mahwelereng HIA2023 historical background on earlier Transvaal Ndebele, not Mzilikazi's nineteenth-century northern kingdom. Native Pretoria/Wonderboom sector retained as coarse southern-Ndebele envelope; wider Highveld not treated as an already united Matabele kingdom. Correct capital region; national Shona removed, no POP conversion.",False)
COUNTRIES['MTB'].update(preserve_knowledge=True)
add('SWZ','STATE_TRANSVAAL','unrecognized',[], 'Ngwane','Ngwane',['nguni'],[198,174,89],"Bonner1983pp9-13: Ngwane in Shiselweni1760s-1770s; later expansion north not dated1776. Retain existing three-cell political nucleus and NgwaneIII rather than erase autonomy. Native northern extent is unresolved, explicitly not certified as cadastral or modern Swazi border.",False)
COUNTRIES['SWZ'].update(preserve_knowledge=True,targeted_grants=['international_relations'])

# Reviewed compatibility repair: inherited barracks remain installed. This early
# capability models locally organised armed followings, not later national armies.
for t in ['HVD','KQO']:
 COUNTRIES[t]['tech'].append(MIL)
 COUNTRIES[t]['basis']+=' Organised chiefly/Orange-frontier armed followings (Denoon23pp750-754,761-762) justify the early military-establishments gate of inherited barracks; no industrial arms-production grant.'
COUNTRIES['BST']['targeted_grants']=[MIL]
for t,fr,en in [('NST','nguni','Nguni'),('HVD','du Haut-Veld','Highveld'),('KQO','de l’Orange','Orange River'),('MSH','rozvi','Rozvi'),('BST','sotho','Sotho'),('MTB','ndébélé','Ndebele'),('SWZ','ngwane','Ngwane')]:
 COUNTRIES[t].update(adj_fr=fr,adj_en=en)

CELLS={
 'NST':[250,251,252,254,255,256,257,259,260,261,263,264,265,267,268,269,270,272,273,274,276,278],
 'HVD':[311,318,326,335,344,346,354,358,359,361,363,367,331,351,375,323,314,320,366,355,362,316,334,348,372,317,374,341,327,365,313,360],
 'KQO':[280,292,294,298,300,307,308,462,467,469,471,491,508,523,537,540,504],
 'BST':[281,289,291,293,295,297,302,303,306],
 'TSW':[279,282,283,284,287,296,304,305],
 'SAN':[488,464,482,459,487,539,498,528,475,509,473,465,474,517,519,531,536,533,466,538,479,526,494,516,480,502,522,534,463,499,457,530,515,495,485,513,470,512],
}
BASES={
 'BST':'Sotho plural Highveld/Caledon political envelope, Denoon23map23.1 and pp750-754; eastern Free State cells, not a Moshoeshoe nation.',
 'TSW':'Western Highveld Tswana communities, Denoon23map23.1 and pp750-754; no Boer Orange republic in1776. Local chiefly plurality, native cells not precise chiefdom borders.',
 'SAN':'Denoon23map23.1,pp747-749,758-763: arid Karoo San/Khoi communities and fluid frontier; no Tswana territorial authority across Karoo. Preserve all inherited cohorts, no ethnic reclassification of inhabitants.'}
DEACTIVATED=['ORA','TRN','PHL','WBL']
WITNESSES=['MSH','BST','MTB','SWZ','TSW','SAN','XHO','PDI','VND','MNC','MTP','TMP','TCH','DEI','NET','POR']
def make_plan():
 rows=json.loads((LOT/'GEOMETRY_CELLS.json').read_text('utf8'));by={r['index']:r for r in rows};selected=[i for ids in CELLS.values() for i in ids]
 assert len(selected)==len(set(selected))
 out=[]
 for t,ids in CELLS.items():
  rr=[by[i] for i in ids]
  for sid,src in dict.fromkeys((r['state'],r['owner']) for r in rr):
   assert src!=t
   out.append(dict(state=sid,source=src,target=t,RGBs=[r['RGB'] for r in rr if r['state']==sid and r['owner']==src],historical_basis=COUNTRIES[t]['basis'] if t in COUNTRIES else BASES[t],precision='NATIVE_CELL_POLITICAL_APPROXIMATION_NOT_CADASTRAL'))
 return out
if __name__=='__main__':
 h.dump('PLAN.json',make_plan());h.dump('COUNTRY_PROFILES.json',COUNTRIES);print('Transfers',sum(len(r['RGBs']) for r in make_plan()),'groups',len(make_plan()))
