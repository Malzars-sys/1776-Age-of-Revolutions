"""Proofs and additive WORLD tracking for CENTRAL-ASIA-01; never engine proof."""
import argparse,json,shutil,re,csv
from collections import Counter
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import world1776_centralasia01_install as i
ROOT,LOT,ST=i.ROOT,i.LOT,i.ST;b=i.b;raw=i.raw;dump=i.dump;load=i.load
TRACK=['ROADMAP.md','ROADMAP_STATE.json','NEXT_ACTION.md','BLOCKERS.md','PROGRESS_HISTORY.md','OWNERSHIP_BOUNDARIES.md','CONCURRENT_CHANGES.json']

def audit_tech():
 snap=i.tech.collect_snapshot()
 new=[i.tech.audit_country(t,snap,dict(required=r['tech'],allowed=r['tech'],historical_evidence=r['basis'])) for t,r in i.PROFILES.items()]
 old=load('STARTING_TECH_BEFORE.json');after=[i.tech.audit_country(r['TAG'],snap) for r in old];comparison=[]
 for a,z in zip(old,after):
  x={json.dumps(f,sort_keys=True) for f in a['findings'] if f['priority'] in ['P0','P1']};y={json.dumps(f,sort_keys=True) for f in z['findings'] if f['priority'] in ['P0','P1']}
  comparison.append(dict(TAG=a['TAG'],introduced=[json.loads(v) for v in sorted(y-x)],resolved=[json.loads(v) for v in sorted(x-y)],inherited_remaining=[json.loads(v) for v in sorted(x&y)]))
 dump('STARTING_TECH_NEW_COUNTRIES.json',new);dump('STARTING_TECH_EXISTING_AFTER.json',after)
 dump('TECH_NON_REGRESSION.json',dict(new_profiles_all_pass=all(r['status']=='PASS_STATIC_ONLY' for r in new),existing_comparison=comparison,shared_graph_changes=0,shared_recipe_changes=0,human_validated=False))
 print('NEW PROFILES',[(r['TAG'],r['status'],r['findings']) for r in new]);print('NEW P0/P1',[(r['TAG'],r['introduced']) for r in comparison if r['introduced']])

def portion_totals(text):
 out=Counter()
 for n in b.walk(b.parse(text)):
  if n.key.startswith('s:STATE_'):
   for p in n.children():
    for pop in p.children('create_pop'):out[n.key[2:],p.key.split(':',1)[-1]]+=int(pop.one('size'))
 return out

def military(text):
 out=Counter()
 for node in b.walk(b.parse(text)):
  if node.key.startswith('c:'):
   for unit in b.walk([node]):
    if unit.key=='combat_unit':out[node.key,unit.one('type'),unit.one('service_type','regular')]+=int(unit.one('count','1'))
 return out

def validate():
 before=load('APPLY_BEFORE.json');plan=load('PLAN.json');scope=before['scope'];old={r:raw(LOT/'apply_inputs'/r) for r in scope};expected=i.transform(old,plan);checks=[]
 def ck(k,v,d=None):checks.append(dict(check=k,passed=bool(v),detail=d))
 for rel,wanted in expected.items():
  current=raw(ROOT/rel);ck('scoped_output_exact.'+rel,current==wanted)
  def outside(text):
   nodes=[b.one(text,k) for k in scope[rel]];return b.edits(text,[(n.start,n.end,'<OWNED_NODE>') for n in nodes])
  ck('all_outside_nodes_identical.'+rel,outside(current)==outside(old[rel]))
  if '/history/pops/' in rel:ck('all_cohorts_and_fields_conserved.'+rel,i.m.pop_cohorts(old[rel])==i.m.pop_cohorts(current))
  if '/history/buildings/' in rel:
   a=i.m.building_inventory(old[rel]);z=i.m.building_inventory(current)
   # One explicit compatibility change on two existing trade declarations.
   correction=Counter()
   for key,value in a.items():
    building,pms=key
    if building.strip('"')=='building_trade_center' and 'pm_trade_center_trade_quantity_normal' in [p.strip('"') for p in pms]:
     # Count transferred Tajik/Kokand trade centres only, below.
     pass
   count=0
   for node in b.walk(b.parse(old[rel])):
    if node.key=='s:STATE_TAJIKISTAN':
     for p in node.children('region_state:KOK'):
      for item in p.children('create_building'):
       if item.one('building').strip('"')=='building_trade_center':
        levels=sum(int(f.value) for f in b.walk([item]) if f.key=='levels');pms=tuple(sorted(i.m.s.ids(item,'activate_production_methods')))
        correction[item.one('building'),pms]-=levels
        correction[item.one('building'),tuple(sorted(p.replace('pm_trade_center_trade_quantity_normal','pm_trade_center_trade_quantity_limited') for p in pms))]+=levels;count+=levels
   ck('all_building_levels_conserved.'+rel,sum(a.values())==sum(z.values()))
   ck('PM_unchanged_except_declared_caravan_compatibility.'+rel,dict(a+correction)==dict(z),dict(transferred_trade_levels=count))
 now=i.c.n.b4.inventory();want=dict(before['inventory']['owners'])
 for row in plan:
  for color in row['RGBs']:
   ck('exact_donor.'+color,want.get(color)==[[row['state'],row['source']]])
   want[color]=[[row['state'],row['target']]]
 ck('exact_global_172_RGB_delta',want==now['owners']);ck('world_population_conserved',now['world_population']==before['inventory']['world_population'],now['world_population'])
 ck('Git_identity_index_unchanged',now['git']==before['inventory']['git'])
 ck('no_new_duplicate_ownership',{k for k,v in now['owners'].items() if len(v)>1}<={k for k,v in before['inventory']['owners'].items() if len(v)>1})
 reserved=set(load('OWNERSHIP_BOUNDARIES.json')['reserved_owners']);ck('all_Durrani_and_peer_RGBs_preserved',all(now['owners'].get(k)==v for k,v in before['inventory']['owners'].items() if any(t in reserved for s,t in v)))
 ck('all_explicit_military_types_counts_services_conserved',military(old[i.ARMY])==military(raw(ROOT/i.ARMY)))
 cat=b.a.catalog('common/country_definitions');cult=b.a.catalog('common/cultures');relig=b.a.catalog('common/religions')
 for tag,r in i.PROFILES.items():
  n,path=cat[tag];ck('definition_uses_own_file.'+tag,path==ROOT/'common/country_definitions'/f'{i.PREFIX}.txt')
  ck('declared_political_type.'+tag,n.one('country_type')==r['kind']);ck('capital_region_owned.'+tag,any([r['capital'],tag] in v for v in now['owners'].values()))
  ck('cultures_and_religion_exist.'+tag,set(r['culture'])<=set(cult) and r['religion'] in relig)
 for tag,capital in i.CAPITALS.items():ck('correct_regional_capital.'+tag,cat[tag][0].one('capital')==capital and any([capital,tag] in v for v in now['owners'].values()))
 for rel,text in i.additional().items():
  ck('private_file_exact.'+rel,raw(ROOT/rel)==text)
  if rel.endswith('.txt'):b.parse(raw(ROOT/rel));ck('script_parses.'+rel,True)
  if rel.endswith('.yml'):
   ck('localization_BOM.'+rel,(ROOT/rel).read_bytes().startswith(b'\xef\xbb\xbf'))
   keys=re.findall(r'^\s+([^\s:]+):\d+ ',text,re.M);ck('no_duplicate_keys_in_file.'+rel,len(keys)==len(set(keys)))
 rows=i.geometry(now['owners'],'INSTALLED')
 for r in rows:
  ck('one_native_cell_component.'+r['TAG'],len(r['components'])==1,r['components'])
  if r['TAG'] in i.PROFILES and i.PROFILES[r['TAG']]['kind']!='decentralized':ck('no_central_enclave_among_decentralized_only.'+r['TAG'],any(cat[t][0].one('country_type')!='decentralized' for t in r['neighbors']),r['neighbors'])
 dip=raw(ROOT/i.DIP);node=b.one(dip,'c:RUS');ck('Russian_Junior_nominal_pact',any(p.one('country')=='c:KZH' and p.one('type')=='aor1776_kazakh_nominal_protection' for p in node.children('create_diplomatic_pact')))
 ck('no_Russian_Middle_Senior_protectorate',not any(p.one('country') in ['c:OZH','c:UZH'] for p in b.walk([node]) if p.key=='create_diplomatic_pact'))
 edited={r['file'] for r in load('FILES_MODIFIED.json')};protected=i.c.n.hashes();outside=[dict(file=r,before=v,after=protected.get(r)) for r,v in before['protected'].items() if r not in edited and protected.get(r)!=v]
 new_outside=[r for r in protected if r not in before['protected'] and r not in edited]
 ck('all_other_protected_files_unchanged',not outside and not new_outside,dict(changed=outside,new=new_outside))
 peer=load('EXTERNAL_COMPOSITION_REVIEW.json');ck('peer_DP03_all_final_outputs_preserved',all(b.a.sha(LOT/'apply_inputs'/r['file'] if r['file'] in scope else ROOT/r['file'])==r['after'] for r in peer['files']))
 tc=load('TECH_NON_REGRESSION.json');ck('all_six_explicit_new_profiles_pass',tc['new_profiles_all_pass']);ck('no_new_P0_P1_in_existing_countries',all(not r['introduced'] for r in tc['existing_comparison']))
 totals_before=Counter();totals_after=Counter()
 for rel in old:
  if '/history/pops/' in rel:totals_before.update(portion_totals(old[rel]));totals_after.update(portion_totals(raw(ROOT/rel)))
 ledger=[dict(state=s,TAG=t,before=totals_before[s,t],after=totals_after[s,t],delta=totals_after[s,t]-totals_before[s,t]) for s,t in sorted(set(totals_before)|set(totals_after)) if totals_before[s,t]!=totals_after[s,t]]
 dump('POPULATION_LEDGER.json',dict(method='Proportional native-province count per donor cohort, exact largest-remainder conservation; technical allocation, not historical census or pixel population.',world_before=before['inventory']['world_population'],world_after=now['world_population'],rows=ledger))
 dump('CONCURRENT_CHANGES.json',dict(peer_review='EXTERNAL_COMPOSITION_REVIEW.json',outside_scope_changes=outside,new_outside_scope_files=new_outside,Git_writes=0,vanilla_writes=0,SERG_writes=0,old_baseline_restored=False))
 result=dict(status='PASS' if all(r['passed'] for r in checks) else 'FAIL',passed=sum(r['passed'] for r in checks),total=len(checks),checks=checks,automated_engine_test=False,human_validated=False)
 dump('VALIDATION.json',result);print('STATIC',result['status'],result['passed'],'/',result['total']);print('FAILURES',[r for r in checks if not r['passed']])
 return result['status']=='PASS'

def map_image():
 owners=i.c.n.b4.inventory()['owners'];a=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32);packed=a[:,:,0]*65536+a[:,:,1]*256+a[:,:,2]
 lut=np.zeros((1<<24,3),dtype=np.uint8)+207;lut[:]=(224,234,240)
 for color,parts in owners.items():lut[int(color[1:],16)]=i.PALETTE.get(parts[0][1],[211,208,193])
 out=Image.new('RGB',(2300,1610),'#f5f0e5');d=ImageDraw.Draw(out);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',25);small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',21);title=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',35)
 d.text((35,20),'ASIE CENTRALE — propriétés installées au départ de 1776',font=title,fill='#292d2b')
 d.text((35,70),'Repères géographiques ; contours de provinces conservés. Frontières fines et interface durranie non certifiées.',font=small,fill='#55564d')
 def panel(box,xy,scale):
  x0,y0,x1,y1=box;pp=packed[y0:y1,x0:x1];rgb=lut[pp];edge=np.zeros(pp.shape,bool);edge[1:]|=pp[1:]!=pp[:-1];edge[:,1:]|=pp[:,1:]!=pp[:,:-1];rgb[edge]=(76,79,70)
  # Country borders dominate; internal province seams remain faint reference.
  rgb=lut[pp];political=np.zeros(pp.shape,bool);political[1:]|=np.any(rgb[1:]!=rgb[:-1],axis=2);political[:,1:]|=np.any(rgb[:,1:]!=rgb[:,:-1],axis=2)
  rgb[edge&~political]=(rgb[edge&~political].astype('uint16')*3+np.array([145,145,130]))//4;rgb[political]=(57,63,54)
  pic=Image.fromarray(rgb).resize((int((x1-x0)*scale),int((y1-y0)*scale)),Image.Resampling.NEAREST);out.paste(pic,xy)
  return lambda x,y:(int(xy[0]+(x-x0)*scale),int(xy[1]+(y-y0)*scale))
 overview=panel((5100,680,6020,1245),(30,125),1.5);detail=panel((5610,1035,5835,1235),(1440,125),3.5)
 def mark(project,x,y,n):
  xx,yy=project(x,y);d.ellipse((xx-17,yy-17,xx+17,yy+17),fill='#fff8d9',outline='#292d2b',width=2);d.text((xx-8,yy-13),str(n),font=small,fill='#292d2b')
 for x,y,num in [(5233,764,1),(5347,811,1),(5267,823,2),(5279,942,2),(5920,846,3),(5669,1105,4),(5677,1135,5),(5708,1162,6),(5682,1193,7),(5730,1208,8),(5790,1090,9)]:mark(overview,x,y,num)
 for x,y,num in [(5669,1105,4),(5677,1135,5),(5708,1162,6),(5682,1193,7),(5730,1208,8),(5790,1090,9)]:mark(detail,x,y,num)
 d.text((1440,855),'Agrandissement des vallées',font=font,fill='#292d2b')
 names=[('RUS','Russie'),('KZH','Petite jüz'),('OZH','Jüz moyenne'),('UZH','Grande jüz'),('KHI','Khiva'),('BUK','Boukhara'),('KOK','Kokand'),('TRM','Communautés turkmènes'),('DUR','Durrani — périmètre réservé')]
 for z,(tag,label) in enumerate(names):
  xx=40+(z%3)*460;yy=1010+(z//3)*42;d.rectangle((xx,yy,xx+27,yy+27),fill=tuple(i.PALETTE[tag]),outline='#45483e');d.text((xx+38,yy),label,font=small,fill='#292d2b')
 legend=['1  Samara et Orenbourg : Russie','2  Yaïk / Ouralsk et Gouriev : ports et forts russes','3  Irtych : trois noyaux fortifiés russes','4  Tachkent : agrégat des quatre quartiers autonomes','5  Oura-Tépa et Khodjent : domaine local distinct','6  Karategin : vallée de Garm','7  Koulab : noyau autonome à l’est de Hissar','8  Choughnan–Rouchan : vallées du Pamir','9  Clans kirghiz : hautes terres hors de Kokand']
 for z,line in enumerate(legend):d.text((40+(z//5)*1130,1170+(z%5)*54),line,font=font,fill='#292d2b')
 d.text((40,1490),'Osh reste dans la portion de Kokand ; les confins locaux et les allégeances du Pamir restent approximatifs.',font=small,fill='#55564d')
 d.text((40,1530),'Carte de contrôle issue du bitmap courant du mod — pas une carte historique indépendante ni une capture du moteur.',font=small,fill='#55564d')
 out.save(LOT/'CARTE_REPERES.png')

def reports():
 v=load('VALIDATION.json');assert v['status']=='PASS';plan=load('PLAN.json');before=load('APPLY_BEFORE.json');ledger=load('POPULATION_LEDGER.json');cells={r['RGB']:r for r in load('GEOMETRY_CELLS.json')}
 dump('USER_REQUEST.json',dict(date='2026-10-29',verbatim="a Passe à l'Isycentral. Mais fais attention, un autre sous-agent est en train de modifier l'Empire d'Urani. Il y aura peut-être des conflits.",interpretation='Asie centrale; Empire durrani concurrent',authority='Direct user message',runtime_validation_implied=False))
 dump('GEOGRAPHIC_CROSSWALK.json',dict(historical_date='1776-01-01',new_RGBs=0,pixels_recolored=0,precision='Political approximation on native province polygons, not cadastral boundaries',cells=[dict(cells[color],before=r['source'],after=r['target'],basis=r['historical_basis']) for r in plan for color in r['RGBs']]))
 files=[dict(file=r['file'],before=r['before'],after=b.a.sha(ROOT/r['file'])) for r in load('FILES_MODIFIED.json')];dump('FILES_DELIVERED.json',files)
 dump('SOURCE_MANIFEST.json',[dict(file=p.relative_to(LOT).as_posix(),sha256=b.a.sha(p),size=p.stat().st_size) for p in (LOT/'sources').rglob('*') if p.is_file()])
 # Preserve the exact peer projection used as a diagnostic, without editing its dossier.
 peer=ROOT/'docs/reports/map/DURRANI_PUNJAB_1776/DP-03/RIVER_MODELS_REVISED.json';dest=LOT/'sources/DP03_RIVER_MODELS_REVISED_readonly_copy.json'
 if not dest.exists():shutil.copy2(peer,dest)
 lines=['| Région / pays | Avant | Après |','|---|---:|---:|']
 for row in ledger['rows']:lines.append(f"| {row['state'].removeprefix('STATE_')} / {row['TAG']} | {row['before']:,} | {row['after']:,} |".replace(',',' '))
 source='''# Sources consultées — CENTRAL-ASIA-01

Consultation du 29 octobre 2026. Référence politique : 1er janvier1776. Les passages publiés plus tard et les cartes de repérage ne valent pas cadastre à cette date.

- **Treskot/Schmidt, Carte de la Russie d’Asie,1776**, exemplaire numérisé de Berne : [e-rara](https://www.e-rara.ch/bes_1/content/titleinfo/10462866), [DOI](https://doi.org/10.3931/e-rara-33725). PDF téléchargé, seconde page rendue et détail des steppes réellement vu. Permet de comparer Volga/Yaïk, lignes fortifiées et steppes ; prétentions impériales et dates de publication ne prouvent pas l’administration uniforme ni l’état exact au1erjanvier. Copies et empreintes dans sources/ et SOURCE_MANIFEST.json.
- **V.A.Kuznetsov, Création de l’armée cosaque d’Orenbourg**, [Voenno-istoricheskiy zhurnal](https://history.milportal.ru/sozdanie-orenburgskogo-kazachego-vojska/?print=print), §§ sur Samara et la fondation1743–44 : article d’historien fondé sur archives, texte consulté. **Kh.Mukhametov/Kh.Tabyldiev**, [Forteresse de Gouriev](https://taisoigan.kz/tarikh-lketanu/article_post/staryy-dobryy-guryev-4), §§1753,1764–69 et ligne du Yaïk : compilation locale d’historiens avec témoignage de Pallas ; vocabulaire politique daté à distinguer des faits de garnison.
- **Institut d’histoire et d’ethnologie du Kazakhstan**, [Abylai Khan](https://iie.kz/?p=26133), passage sur l’élection1771, la reconnaissance russe1778 et le refus de cérémonie. Appuie la distinction entre prétention sur les trois jüz et sujétion effective. Récit institutionnel national ; les affirmations d’unité ne sont pas appliquées comme annexion générale. **Portail historique national**, [Semipalatinsk1718](https://e-history.kz/en/calendar/show/27352), ancien site déplacé en1778. **Publication de documents1719–20**, [Oskemen](https://oskemen.info/5979-arhivnye-dokumenty-17191720-godov-o-vybore-mesta-i-osnovanii-ust-kamenogorskoy-kreposti.html) : cite Miller et les rapports de Likharev ; noyaux russes, pas tout leur hinterland.
- **T.Beisembiev et S.Levi**, [Kokand Khanate](https://www.iranicaonline.org/articles/kokand-khanate/),2023, sections «Initial stage» et expansion ultérieure : base ferganienne, domaines Yüz distincts et conquête ultérieure de Tachkent. Ne pas appliquer le maximum des années1830 à1776. Khodjent et les confins d’Oura-Tépa restent contestés : le domaine installé est une enveloppe politique, non une datation certaine de chaque changement de mains.
- **Y.Bregel**, [Central Asia vii](https://www.iranicaonline.org/articles/central-asia-vii/),2000,Vol.V/2,pp193–205, paragraphes sur les principautés et leur absorption ultérieure. Motive les autonomies de Karategin/Koulab ; ne suffit pas à tracer leurs limites détaillées. Hissar et le delta d’Aral restent ouverts ; aucune frontière déduite d’une simple mention de rébellion.
- **O.D.Chekhovich**, «Skazanie o Tashkente», Pismennye pamyatniki Vostoka1968,édition1970, [introduction publiée](https://www.vostlit.info/Texts/Dokumenty/M.Asien/XVIII/1780-1800/Taskent/pred.htm),pp172–177 : quatre quartiers à gouvernements distincts, décisions communes, réunification vers1784. Il s’agit d’une édition critique d’une tradition manuscrite tardive confrontée aux témoignages russes. Le nom local de fichier contenant «Pospelov1800» est un mauvais raccourci de téléchargement : le texte consulté est cette introduction de Chekhovich, pas le récit intégral de Pospelov.
- **D.Saparaliyev**, traduction A.Isakov, «XVIII.Yüzyılda Kırgızlar ile Özbeklerin Sosyal ve Siyasi İlişkileri», Akademik Bakış4/8,2011,pp139–160, [PDF éditeur](https://dergipark.org.tr/tr/download/article-file/73950). Pages142,144,148 et155 lues ; documents du XVIIIe siècle et témoignages sur les pouvoirs kirghiz indépendants d’Osh-Alay/hautes terres. Article engagé dans une controverse contemporaine : ne pas en déduire de frontière ethnique exclusive ; Osh reste un compromis de vallée ferganienne.
- **J.-H.Grevemeyer**, [Darvaz](https://www.iranicaonline.org/articles/darvaz/),1994, paragraphes géographiques et dynastiques ; [figure3](https://www.iranicaonline.org/img/v7f1/fig3_p66.jpg) téléchargée et vue. Carte du milieu du XIXe siècle utilisée seulement pour l’ordre des vallées. Darvaz autonome et Choughnan/Rouchan liés généralement au Badakhshan : aucun lien1776 certain avec DUR inféré. Le noyau principal de Darvaz recoupe le périmètre réservé, donc pas de nouveau TAG Darvaz installé. La cellule Rouchan/Vanj reste une approximation à reprendre conjointement.

**Géographie technique.** Bitmap et locators actuels inspectés, GEOMETRY_CELLS.json et comparaison à MAP1_HUB_LOCATOR_CHECKS.csv. Le modèle physique DP-03 copié en lecture seule fournit un contrôle de vraisemblance au nord de son domaine d’ajustement ; extrapolation non certifiée et aucun classement automatique des propriétaires par latitude ou distance. Les villes servent de repères, pas de preuve de souveraineté. Le défaut de Gouriev et le nom trompeur SEMIRECHE sont explicitement corrigés sans déplacer les locators partagés.

**Pistes non consultées intégralement.** Livre UNESCO inaccessible, catalogues LOC/NLR refusés et certains miroirs indisponibles : aucune preuve de lecture de ces ouvrages. Le PDF e-rara accessible remplace la piste de carte non vue ; aucun document refusé ne sert d’autorité décisive.
'''
 (LOT/'SOURCES.md').write_text(source,encoding='utf8')
 report=f'''# CENTRAL-ASIA-01 — Asie centrale, première passe territoriale

**IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION** — référence1erjanvier1776. Installation du29octobre2026. **Aucun test moteur ni reçu joueur nouveau.** Les corrections portent sur les appartenances territoriales et leurs dépendances indispensables, sans personnages ni contenu flavor.

## Corrections installées

**172 provinces natives**, dans7 régions, changent de propriétaire. Aucun nouveau RGB, pixel ou État géographique. Liste exacte dans PLAN.json et GEOGRAPHIC_CROSSWALK.json ; CARTE_REPERES.png montre où regarder.

- Samara/Orenbourg :76 provinces de KZH à RUS. Ouralsk et le port dessiné de Gouriev :2 provinces de KZH à RUS. Trois noyaux d’Irtych — Koriakov/Pavlodar, Semipalatinsk, Oust-Kamenogorsk — passent de OZH à RUS. Ce sont des approximations natives de juridiction fortifiée, pas la preuve d’un contrôle russe de toute la steppe.
- Kokand perd ses extensions prématurées :27 provinces du Syr-Daria et3 des approches de Tachkent vers les jüz ; Tachkent2, Oura-Tépa/Khodjent6, Karategin6, noyau oriental de Koulab2, Choughnan–Rouchan5 et hautes terres kirghizes39 sont distingués. Une province bukharane rejoint le noyau de Koulab. Kokand conserve son noyau ferganien et la cellule d’Osh ; les prétentions locales restent ouvertes.
- **Cinq nouveaux TAG** :TSH,URT,QTG,KLB,SHG ; **KYR réactivé comme agrégat décentralisé de clans**, pas comme État moderne. Les cinq noyaux urbains/royaux sont non reconnus. Tachkent utilise l’oligarchie pour représenter ensemble ses quatre quartiers indépendants, sans anticiper leur unification1784. Aucune nouvelle biographie ou armée n’est créée.
- Capitales régionales :OZH→AKMOLINSK, UZH→SYRDARYA. Le nom interne SEMIRECHE couvre ici le nord-est autour de Semipalatinsk et ne justifie donc pas un transfert massif à la Grande jüz. L’ancrage régional n’affirme pas l’existence d’une capitale fixe dans une ville fondée ultérieurement.
- OZH/UZH ne sont plus des protectorats russes de lancement. KZH garde une **protection nominale privée**, sans paiement, service militaire automatique ou interdiction de guerre/diplomatie propre. Cette relation de jeu traduit une allégeance indirecte ; elle ne certifie pas un contrôle russe effectif de tous ses clans. Les souhaits d’autonomie devenus sans objet sont retirés pour OZH/UZH. Les autres pactes, dont UBD/Alaska et Kalat, restent identiques.

## Institutions et technologies

Six profils explicites anciens, différenciés par les secteurs représentés ; **6/6 PASS_STATIC_ONLY**. Les courts noyaux ruraux n’obtiennent ni banque moderne ni industrie pour satisfaire artificiellement les gates. La loi privée de droits caravaniers reprend les effets du mercantilisme natif et son seul prérequis diplomatique ancien ; aucune recette ou arête technologique commune n’est refondue. Les catégories politiques utilisent un remplacement explicite pour KYR/OZH/UZH, ce qui évite le défaut de doublons africain déjà corrigé.

Lois demandées contrôlées statiquement ; lois effectivement chargées, noms générés, capitales exactes, drapeaux générés et économies restent à observer dans le moteur. Les pays existants conservent leurs dettes techniques héritées ; **aucun nouveau P0/P1 sur10 témoins**.

## Populations et stocks

Monde : **{ledger['world_before']:,} → {ledger['world_after']:,}**, delta0. Chaque cohorte conserve culture, religion, profession et autres champs. Répartition par comptes de provinces et plus forts restes : allocation technique, **pas un recensement historique**, pas une densité calculée à partir des pixels. Aucun champ de culture ou de religion n’est réécrit. Les confessions implicites restent à observer au chargement ; le proxy national chiite du Choughnan ne constitue pas un recensement ismaélien.

{chr(10).join(lines)}

Tous les niveaux bâtis existants sont conservés. Les services et petites productions de la portion tajike quittée par Kokand sont réattribués aux portions restantes ; ranchs aux communautés pastorales. Ce placement est nécessaire au transfert, sans prétendre restituer des établissements précis. Deux déclarations commerciales transférées utilisent le PM **commerce limité** déjà disponible, au lieu du PM normal verrouillé par les institutions financières organisées. Pas de changement de recette ; les autres PM sont conservés. Les doublons de déclarations préexistants ne sont ni effacés ni certifiés comme niveaux réellement chargés.

Trois conscrits KZH recrutés en Samara sont référencés vers AKTOBE ; un conscrit KOK de la portion tajike vers FERGANA. Tous comptes/types/services et personnages existants sont conservés. OZH garde sa portion SEMIRECHE et sa référence militaire : aucun déplacement inutile.

## Géographie, sources et incertitudes

SOURCES.md distingue la carte1776 réellement vue, les articles historiques et les cartes ultérieures de repérage. Les frontières installées sont des **approximations politiques natives**. Aucun lissage cosmétique ni frontière rectiligne nouvelle. Les six nouveaux profils correspondent à des noyaux connectés ; aucun nouveau pouvoir centralisé isolé au milieu de seules communautés décentralisées.

Le contrôle visuel a corrigé une première sélection erronée de Gouriev : xD1364F est le pointeur minier situé45pixels à l’est du port ; il est rendu à KZH et **xEFFD2B**, le port dessiné, va à RUS. Le premier résultat statique et le plan initial restent archivés dans audit_history/INITIAL ; réparation séparée GURIEV_LOCATOR_REPAIR.json. Un contrôle de syntaxe ou de conservation ne prouve pas à lui seul l’exactitude historique d’une sélection.

Restent ouverts : Darvaz/Badakhshan au contact de DUR ; l’allégeance exacte des vallées pamiriennes ; confins de Hissar, Chahrisabz, Merv/Khiva et autonomie de l’Aral ; limite entre jüz et portée des droits Qing ; cadastre des oasis, position exacte des petites cours et caractère contemporain de Khodjent. Boukhara/Khiva/Turkmènes et les portions Qing sont conservés lorsqu’aucune preuve datée ne justifie un nouveau contour. Cette conservation n’est pas une homologation historique intégrale.

## Concurrence et preuves

**DP-03 installé pendant la recherche est préservé** :18 sorties et6 changements de cellule du Pendjab/Cachemire rapprochés du manifeste et archivés, puis application sur préimages courantes. Aucune portion DUR ou nouveau pays DP, aucun suivi Durrani/Pendjab ni SERG écrit. Afrique et Scandinavie, TECH-R1/R2/R3, ECON-alloys/quincaillerie et Amériques protégés par empreintes et comparaison des nœuds extérieurs ; pas de restauration d’ancienne baseline.7 fichiers existants ciblés +13 ajouts privés. Aucun Git ou vanilla écrit.

Le premier accès au fichier d’états a échoué avant toute écriture ; préimages vérifiées identiques, échec archivé failed_attempt_01, puis installation autorisée avec le même périmètre et contrôles d’empreinte. Aucun changement extérieur écrasé. Après la correction de Gouriev, un contrôle textuel a relevé un ordre différent des listes malgré des propriétaires identiques : échec conservé dans audit_history, ordre harmonisé sans nouveau transfert. Les libellés du pacte et de sa rupture sont complétés dans le même reçu CANONICAL_ORDER_AND_UI_REPAIR.json. Les25clés de chaque langue n’introduisent aucun doublon dans le mod ; preuve SCOPED_LOCALIZATION_AUDIT.json.

**{v['passed']}/{v['total']} contrôles statiques PASS** sur la version finale : propriétaires exacts, continuité de provinces, non-enclavement, réserves durranies, cohortes, niveaux/PM, unités, références, profils et empreintes des fichiers extérieurs. Commandes : Python de l’environnement, tools/world1776_centralasia01_install.py --preflight puis --apply ; tools/world1776_centralasia01_closeout.py --tech --validate. La réparation géographique est un patch indépendant et ne rejoue jamais l’application initiale.

Validation moteur **NOT_RUN**. Protocole groupé dans RUNTIME_PROTOCOL.md ; aucun test intermédiaire par micro-lot exigé. WORLD conserve son registre historique **10/320**,3,13%, aucun point humain nouveau ; extension auxiliaire1.0.3 sans modification du dénominateur. Aucun passage automatique à une autre région.
'''.replace('837,328,654','837 328 654')
 for a,z in [('référence1erjanvier1776','référence : 1er janvier 1776'),('du29octobre2026','du 29 octobre 2026'),('dans7 régions','dans 7 régions'),('sur10 témoins','sur 10 témoins'),('Les25clés','Les 25 clés'),('7 fichiers existants ciblés +13','7 fichiers existants ciblés + 13'),('**10/320**,3,13%','**10/320**, 3,13 %')]:report=report.replace(a,z)
 (LOT/'REPORT.md').write_text(report,encoding='utf8')
 (LOT/'RUNTIME_PROTOCOL.md').write_text('''# Contrôle groupé — Asie centrale

Version : FILES_DELIVERED.json. Non exécuté par l’agent. Les observations de l’Afrique ne valent pas test de cette version et le passage à l’Asie ne certifie pas les tests nordiques.

1. Nouvelle partie au1erjanvier1776. CARTE_REPERES.png : Samara/Orenbourg et trois forts d’Irtych russes, Ouralsk et port dessiné de Gouriev russes ; arrière-pays kazakh distinct.
2. Deux jüz OZH/UZH indépendantes de la Russie, KZH sous protection nominale ; absence de tribut/ralliement militaire automatique. Capitales dans les portions possédées, sans exiger les noms d’une ville moderne.
3. Tachkent et Oura-Tépa/Khodjent distincts ; Karategin, Koulab et Choughnan–Rouchan présents ; clans kirghiz décentralisés ; Kokand encore ferganien avec Osh. Aucun tribut imposé à un suzerain décentralisé.
4. Vérifier lois effectives, noms/drapeaux générés, POPs et marchés. Les six profils passent les contrôles statiques, mais leur budget et leur emploi n’ont pas été simulés. Vérifier les petits réseaux routiers/commerce limité sans pénurie due à un PM verrouillé.
5. Simulation d’un mois, puis sauvegarde/rechargement ; relever erreurs et éventuels fronts/accès bloqués. Vérifier aussi un témoin d’Afrique, de Scandinavie et les pays DP-03 au Cachemire/Pendjab.

Un constat partiel reste partiel ; durée/version/rechargement ne sont jamais supposés. Confins Darvaz/Badakhshan et petites limites historiques nécessitent une coordination avec le lot durrani, pas une annexion improvisée. Aucun test par principauté demandé.
''',encoding='utf8')
 map_image();print('Reports, map and final functional receipts written.')

def tracking():
 assert not (LOT/'TRACKING_PATCHES.json').exists(),'Do not replay tracking.'
 world=i.c.WORLD;old={k:raw(world/k) for k in TRACK};sha={k:b.a.sha(world/k) for k in TRACK}
 for k in TRACK:
  p=LOT/'tracking_inputs'/k;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(world/k,p)
 state=json.loads(old['ROADMAP_STATE.json']);state['scope_version']='1.0.3';state['scope_amendments'].append(dict(version='1.0.3',date='2026-10-29',authority='CENTRAL-ASIA-01/USER_REQUEST.json',change='Explicit Central Asian cartographic pass outside legacy regional scoring register; Durrani interfaces reserved.',criteria_total_unchanged=320))
 state['steering_history'].append(state['current_steering']);state['current_phase']='CENTRAL_ASIA_AUXILIARY'
 state['current_steering']=dict(date='2026-10-29',authority='CENTRAL-ASIA-01/USER_REQUEST.json',last_lot='CENTRAL-ASIA-01',scope='Central Asian territorial kernels, Durrani interface excluded',next_pass='Grouped runtime checks; joint Darvaz/Badakhshan review only if explicitly assigned, no automatic new region',runtime_validation_timing='GROUPED_CENTRAL_ASIA',intermediate_player_tests_requested=False,full_V_credit=False)
 state['phase_transition_gate']=dict(source='CENTRAL-ASIA-01/USER_REQUEST.json',explicit_transition_authorized=True,authorized_next_phase='CENTRAL_ASIA_AUXILIARY',rule='Direct user request for Central Asia with Durrani concurrent work reserved.',authorization_is_full_canonical_V_validation=False,partial_lot_tests_requested=False)
 state['lots'].append(dict(id='CENTRAL-ASIA-01',date='2026-10-29',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',auxiliary_scope_outside_legacy_denominator=True,native_RGBs_transferred=172,existing_files_modified=7,new_files=13,population_delta=0,new_TAGs=5,reactivated_TAGs=1,receipt='CENTRAL-ASIA-01/FILES_DELIVERED.json',runtime='NOT_RUN',credited_criteria=[]))
 assert state['progress']['technical_verified']==10 and state['progress']['criteria_total']==320
 v=load('VALIDATION.json');entry=f'\n\n## 29 octobre2026 — CENTRAL-ASIA-01 installé\n\nAsie centrale autorisée directement, interfaces durranies réservées.172RGB natifs,7régions : noyaux russes Samara/Yaïk/Irtych, réduction des extensions ultérieures de Kokand, cinq nouveaux noyaux politiques et clans kirghiz réactivés. OZH/UZH indépendants de RUS, KZH sous protection nominale sans prélèvement ni guerre automatique ; capitales régionales corrigées. Six profils PASS_STATIC_ONLY ; aucun nouveauP0/P1 sur10témoins, graphe/recettes communs conservés. Monde837328654 inchangé, cohortes/niveaux/unités conservés, deux déclarations commerciales transférées sur le PM limité compatible.7fichiers ciblés+13ajouts. DP-03 concurrent rapproché18sorties/6RGB, préimages courantes et autres lots préservés ; aucun suiviSERG/DP/Git/vanilla écrit. Réparation Gouriev distincte, preuves initiales conservées. {v["passed"]}/{v["total"]}statiques, aucun test moteur. Rapport CENTRAL-ASIA-01/REPORT.md ; frontières natives et Darvaz/Badakhshan/allégeances restent approximatifs. Portée auxiliaire1.0.3, WORLD10/320(3,13%) inchangé, aucun crédit humain.\n'
 out=dict(old);out['ROADMAP_STATE.json']=json.dumps(state,ensure_ascii=False,indent=2)+'\n'
 for k in ['ROADMAP.md','PROGRESS_HISTORY.md']:out[k]=old[k]+entry
 out['BLOCKERS.md']=old['BLOCKERS.md']+'\n\n## CENTRAL-ASIA-01 — limites ouvertes\n\nDarvaz/Badakhshan réservé à l’interface durranie ; aucune nouvelle relation de vassalité pamirienne sans preuve1776. Limites de jüz, Qing, Hissar/Aral et petites oasis non cadastrales. SEMIRECHE interne ne signifie pas automatiquement Grande jüz ; Gouriev utilise le vrai port dessiné, son pointeur minier erroné reste une dette de locator non déplacé. Noms/capitales/drapeaux, lois effectives, emploi/budgets et simulation/sauvegarde attendent le contrôle groupé. Aucun test intermédiaire par pays, aucune reprise flavor ou autre région automatique. Scandinavie non attestée en moteur ; Afrique acceptée pour le moment inchangée.\n'
 out['OWNERSHIP_BOUNDARIES.md']=old['OWNERSHIP_BOUNDARIES.md']+'\n\n## CENTRAL-ASIA-01 — périmètre installé\n\nPLAN.json :172RGB natifs dans7régions. Sept fichiers existants, seuls nœuds SCOPES.json ; seuls c:KZH/KOK militaires et c:RUS/OZH/UZH diplomatiques. Cinq TAG nouveaux, KYR activé, capitales OZH/UZH surcharges explicites ; effets/loi/relation/FR-EN privés. Aucun bitmap, terrain, ressource, locator, personnage ou recette/graphe commun. Portions DUR/DP et leurs rapports/suivis strictement réservés ; Darvaz principal exclu. Préimages immédiates/FILES_DELIVERED.json et réparation Gouriev séparée font foi. DP-03 présent dans la version appliquée, Afrique/Scandinavie/Amériques/SERG/TECH/ECON conservés. Aucun retour à une baseline antérieure.\n'
 out['NEXT_ACTION.md']='''# Prochaine action — après CENTRAL-ASIA-01

La consigne directe autorisait l’Asie centrale avec réserve de l’Empire durrani. Première passe territoriale livrée : lire CENTRAL-ASIA-01/REPORT.md, SOURCES.md, PLAN.json, GEOGRAPHIC_CROSSWALK.json, POPULATION_LEDGER.json, VALIDATION.json, FILES_DELIVERED.json et GURIEV_LOCATOR_REPAIR.json.

172RGB natifs, cinq nouveaux TAG et KYR réactivé ; populations/cohortes/niveaux et comptes militaires conservés. Test groupé futur suivant CARTE_REPERES.png et RUNTIME_PROTOCOL.md, aucun test par micro-lot. Pas de validation joueur fictive ni de clôture historique intégrale. Darvaz/Badakhshan et les allégeances pamiriennes restent réservés à une coordination avec le chantier durrani ; ne modifier aucun de ses nœuds ou suivis sur la seule base de cette prochaine action.

DP-03 concurrent préservé avec18sorties/6changements territoriaux rapprochés. Afrique reste acceptée pour le moment ; test moteur scandinave toujours non attesté. Lissage et contenu flavor différés. Aucun autre secteur lancé automatiquement, aucun suiviSERG écrit. Portée auxiliaire1.0.3, registre historique320critères inchangé.
'''
 con=json.loads(old['CONCURRENT_CHANGES.json']);con['CENTRAL-ASIA-01']=dict(receipt='CENTRAL-ASIA-01/CONCURRENT_CHANGES.json',functional_files=20,native_RGBs_transferred=172,pixels_recolored=0,population_delta=0,peer_composition='CENTRAL-ASIA-01/EXTERNAL_COMPOSITION_REVIEW.json',Git_writes=0,vanilla_writes=0,SERG_writes=0);out['CONCURRENT_CHANGES.json']=json.dumps(con,ensure_ascii=False,indent=2)+'\n'
 assert all(b.a.sha(world/k)==sha[k] for k in TRACK),'Concurrent tracking change; reread.'
 for k,text in out.items():
  assert b.a.sha(world/k)==sha[k],k;i.save(world/k,text)
 dump('TRACKING_PATCHES.json',[dict(file=(world/k).relative_to(ROOT).as_posix(),before=sha[k],after=b.a.sha(world/k)) for k in TRACK]);print('Additive tracking recorded; legacy320 denominator unchanged.')

def final():
 assert load('VALIDATION.json')['status']=='PASS'
 state=json.loads(raw(i.c.WORLD/'ROADMAP_STATE.json'));static=sum(c['status']=='STATIC_VERIFIED' for p in state['phases'] for r in p['subregions'] for c in r['criteria'].values());human=sum(c['status']=='USER_VALIDATED' for p in state['phases'] for r in p['subregions'] for c in r['criteria'].values())
 assert static==10 and human==0 and state['progress']['criteria_total']==320
 dump('PROGRESS_CALCULATION.json',dict(technical_verified=static,criteria_total=320,runtime_full_criteria=human,technical_percent=3.13,auxiliary_lot_scored_in_legacy_register=False,new_points=0))
 files=[ROOT/r['file'] for r in load('FILES_DELIVERED.json')]+[p for p in LOT.rglob('*') if p.is_file() and p.name!='DELIVERY_MANIFEST.json']+[i.c.WORLD/k for k in TRACK]+[ROOT/'tools'/n for n in ['world1776_centralasia01.py','world1776_centralasia01_install.py','world1776_centralasia01_closeout.py']]
 dump('DELIVERY_MANIFEST.json',{p.relative_to(ROOT).as_posix():b.a.sha(p) for p in files});print('Final manifests recorded; runtime NOT_RUN.')

if __name__=='__main__':
 p=argparse.ArgumentParser()
 for k in ['tech','validate','reports','tracking','final']:p.add_argument('--'+k,action='store_true')
 a=p.parse_args()
 if a.tech:audit_tech()
 if a.validate and not validate():raise SystemExit(1)
 if a.reports:reports()
 if a.tracking:tracking()
 if a.final:final()
