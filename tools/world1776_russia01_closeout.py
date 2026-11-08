"""RUSSIA-01 scoped evidence and additive WORLD follow-up. Static, not engine proof."""
import argparse,json,re,shutil
from collections import Counter,defaultdict
from datetime import datetime,timezone
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import world1776_russia01_frontiers as f
import validate_starting_technology_1776 as tech
ROOT,LOT,b,n,ST=f.ROOT,f.LOT,f.b,f.n,f.ST
raw,dump,load=f.raw,f.dump,f.load
TRACK=['ROADMAP.md','ROADMAP_STATE.json','NEXT_ACTION.md','BLOCKERS.md','PROGRESS_HISTORY.md','OWNERSHIP_BOUNDARIES.md','CONCURRENT_CHANGES.json']

def technology():
 snap=tech.collect_snapshot();before=load('TECH_BEFORE.json');comparison=[]
 for old in before:
  new=tech.audit_country(old['TAG'],snap)
  a={json.dumps(x,sort_keys=True) for x in old['findings'] if x['priority'] in ['P0','P1']};z={json.dumps(x,sort_keys=True) for x in new['findings'] if x['priority'] in ['P0','P1']}
  comparison.append(dict(TAG=old['TAG'],introduced=[json.loads(s) for s in sorted(z-a)],inherited_remaining=[json.loads(s) for s in sorted(z&a)],resolved=[json.loads(s) for s in sorted(a-z)]))
 profile=tech.audit_country('NNT',snap,dict(required=f.NTECH,allowed=f.NTECH,historical_evidence='Nenets reindeer herding, household textile/leather work and local craft exchange: Vallikivi2024 introduction and Dartmouth historical discussion; no cereal, banking or uniform Russian tier.'))
 dump('STARTING_TECH_NEW_COUNTRY.json',profile);dump('TECH_NON_REGRESSION.json',comparison)
 print('NNT',profile['status'],profile['findings']);print('New existing P0/P1',[(z['TAG'],z['introduced']) for z in comparison if z['introduced']])

def graph_check():
 """Existing province graph, including unmodified Russian neighbors.

 Collapse unmodified regions only as external anchors. Any newly orphaned
 centralized province component in the changed regions is a failure.
 """
 a=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),dtype=np.uint32);pack=a[:,:,0]*65536+a[:,:,1]*256+a[:,:,2];del a
 before=load('APPLY_BEFORE.json')['inventory']['owners'];after=n.b4.inventory()['owners'];cells=load('FRONTIER_CELLS.json');changed={int(c['RGB'][1:],16) for c in cells if c['state'] in ['STATE_NENETSIA','STATE_OB']};adj=defaultdict(set)
 roi=pack[0:700,4800:6150]
 for a,z in [(roi[1:],roi[:-1]),(roi[:,1:],roi[:,:-1])]:
  mask=a!=z;aa=a[mask].astype(np.uint64);zz=z[mask].astype(np.uint64);pairs=np.unique((np.minimum(aa,zz)<<24)|np.maximum(aa,zz))
  for pair in pairs:
   x,y=int(pair>>np.uint64(24)),int(pair&np.uint64(0xffffff))
   if x in changed or y in changed:adj[x].add(y);adj[y].add(x)
 def components(owners,tag):
  land={int(c[1:],16) for c,p in owners.items() if p[0][1]==tag};remaining=land&changed;out=[]
  while remaining:
   z=remaining.pop();todo=[z];seen={z};anchors=set()
   while todo:
    p=todo.pop()
    for q in adj[p]&land:
     if q not in changed:anchors.add(q)
     elif q in remaining:remaining.remove(q);seen.add(q);todo.append(q)
   out.append(dict(cells=sorted('x'+format(v,'06X') for v in seen),outside_anchors=sorted('x'+format(v,'06X') for v in anchors)))
  return out
 old=components(before,'RUS');new=components(after,'RUS');old_orphans=set(c for row in old if not row['outside_anchors'] for c in row['cells']);new_orphans=set(c for row in new if not row['outside_anchors'] for c in row['cells'])
 native=components(after,'NNT');result=dict(russian_components_before=old,russian_components_after=new,new_centralized_orphan_cells=sorted(new_orphans-old_orphans),nenets_components=native,scope='Province4-neighbor land graph in changed regions, unmodified Russian neighbors serve as anchors; pre-existing Arctic island components retained, sea access not a land corridor.')
 dump('CONTINUITY.json',result)
 return result

def validate():
 before=load('APPLY_BEFORE.json');old={p:raw(LOT/'apply_inputs'/p) for p in f.EXISTING};expected,ledger=f.transform(old);expected.update(f.extras());checks=[]
 def ck(name,value,detail=None):checks.append(dict(check=name,passed=bool(value),detail=detail))
 for rel,txt in expected.items():
  ck('exact_authorized_patch.'+rel,raw(ROOT/rel)==txt)
  if rel.endswith('.txt'):ck('syntax.'+rel,bool(b.parse(raw(ROOT/rel))))
 inventory=n.b4.inventory();plan=load('PLAN.json');wanted={c:row for row in plan for c in row['RGBs']};changed={c for c in set(before['inventory']['owners'])|set(inventory['owners']) if before['inventory']['owners'].get(c)!=inventory['owners'].get(c)}
 ck('exact_344_owner_transfers',changed==set(wanted) and len(changed)==344)
 for c,row in wanted.items():ck('RGB.'+c,inventory['owners'].get(c)==[[row['state'],'NNT']] and before['inventory']['owners'].get(c)==[[row['state'],'RUS']])
 ck('no_new_duplicate_or_unassigned_RGB',inventory['odd']==before['inventory']['odd'])
 ck('global_population',inventory['world_population']==before['inventory']['world_population']==837328654)
 ck('git_identity_and_index',inventory['git']==before['inventory']['git'])
 for rel in f.POPS:
  def cohorts(text):
   out=Counter()
   for pop in b.walk(b.parse(text)):
    if pop.key=='create_pop':
     key=tuple(sorted((x.key,x.value) for x in pop.children() if x.key!='size'));out[key]+=int(pop.one('size'))
   return out
  ck('all_cohort_fields_conserved.'+rel,cohorts(raw(ROOT/rel))==cohorts(old[rel]))
 def remove_states(text):
  nodes=[b.one(text,'s:'+row['state']) for row in plan];return b.edits(text,[(z.start,z.end,'<OWNED>') for z in nodes])
 ck('all_other_state_nodes_byte_identical',remove_states(raw(ROOT/ST))==remove_states(old[ST]))
 for row in load('RUSSIAN_PARTS_BEFORE.json'):
  sid=row['state'];st=b.one(raw(ROOT/ST),'s:'+sid);p=next(z for z in st.children('create_state') if z.one('country')=='c:RUS')
  ck('unchanged_existing_state_type.'+sid,p.one('state_type','incorporated')==row['state_type'])
  ck('remaining_Russian_portion.'+sid,len(b.a.ids(p,'owned_provinces'))>0)
 ck('fifty_nine_portions_reviewed',len(load('RUSSIAN_PARTS_BEFORE.json'))==59)
 defs=b.a.catalog('common/country_definitions');ck('NNT_decentralized',defs['NNT'][0].one('country_type')=='decentralized');ck('NNT_capital_region_owned',any(p[0][0]=='STATE_NENETSIA' and p[0][1]=='NNT' for p in inventory['owners'].values()))
 ck('no_NNT_subject_pact',not any('c:NNT' in raw(p) for p in b.tech.effective('common/history/diplomacy')))
 native=raw(f.r.GAME/'common/laws/01_colonial_affairs.txt');a=b.one(native,'law_internal_colonization');z=b.one(raw(ROOT/('common/laws/'+f.PREFIX+'.txt')),'law_internal_colonization')
 ck('native_internal_law_exact',native[a.start:a.end]==raw(ROOT/('common/laws/'+f.PREFIX+'.txt'))[z.start:z.end])
 laws=b.a.catalog('common/laws');ck('restored_law_in_effective_catalog','law_internal_colonization' in laws)
 ndefs=raw(f.r.GAME/'common/defines/00_defines.txt');ours=raw(ROOT/('common/defines/zz_'+f.PREFIX+'.txt'))
 for name in ['COSSACK_HOST_BUILDING','COSSACK_HOST_ARABLE_LAND_FRACTION','COSSACK_HOST_REMOVAL_COOLDOWN_MONTHS','COSSACK_HOST_REMOVAL_RADICALIZATION_FACTOR','COSSACK_HOST_RECENT_REMOVAL_YEARS']:
  ck('native_define.'+name,b.one(ours,name).value==b.one(ndefs,name).value)
 country=raw(ROOT/f.r.COUNTRY);ck('internal_law_requested','activate_law = law_type:law_internal_colonization' in country);ck('Cossack_amendment_sponsor','type = amendment_cossacks sponsor = PREV.ig:ig_rural_folk' in country)
 ck('institution_level_one','institution = institution_colonial_affairs level = 1' in country)
 for state in f.HOSTS:
  st=b.one(raw(ROOT/ST),'s:'+state);ck('host_region_Russian.'+state,any(p.one('country')=='c:RUS' for p in st.children('create_state')))
 ck('four_native_host_effects',raw(ROOT/('common/history/buildings/99_'+f.PREFIX+'_cossacks.txt')).count('establish_cossack_host = yes')==4)
 for folder,keys in {'common/buildings':['building_cossack_host'],'common/production_methods':['pm_cossack_host','pm_cossack_recruitment'],'common/amendments':['amendment_cossacks']}.items():
  catalog=b.a.catalog(folder)
  for key in keys:ck('native_object_effective.'+key,key in catalog)
 atext,ztext=raw(ROOT/f.AI),raw(f.r.GAME/f.AI);anode,znode=b.one(atext,'cossack_host_scores'),b.one(ztext,'cossack_host_scores')
 ck('cossack_AI_field_exact',atext[anode.start:anode.end]==ztext[znode.start:znode.end])
 ck('new_profile_pass',load('STARTING_TECH_NEW_COUNTRY.json')['status']=='PASS_STATIC_ONLY')
 for row in load('TECH_NON_REGRESSION.json'):ck('no_new_P0_P1.'+row['TAG'],not row['introduced'],row['introduced'])
 for language in ['french','english']:
  path=ROOT/('localization/'+language+'/'+f.PREFIX+'_l_'+language+'.yml');ck('localization_BOM.'+language,path.read_bytes().startswith(b'\xef\xbb\xbf'))
  entries=[(p,line) for p in (ROOT/'localization'/language).rglob('*.yml') for line in raw(p).splitlines() if re.match(r'\s*NNT(?:_ADJ|_DEF)?:',line)]
  ck('localization_unique.'+language,len(entries)==3,[(str(p.relative_to(ROOT)),line) for p,line in entries])
 current=n.hashes();allowed={row['file'] for row in load('FILES_MODIFIED.json')};changes=[dict(file=p,before=before['protected'].get(p),after=current.get(p)) for p in set(before['protected'])|set(current) if before['protected'].get(p)!=current.get(p)]
 unexpected=[row for row in changes if row['file'] not in allowed];dump('CONCURRENT_CHANGES.json',dict(changes_since_immediate_preimage=changes,unexpected=unexpected,initial_survey_to_preimage=[dict(file=p,before=h,preimage=before['protected'].get(p)) for p,h in load('BEFORE.json')['protected'].items() if before['protected'].get(p)!=h],no_peer_edits_restored=True))
 ck('all_unrelated_functional_and_SERG_files_preserved',not unexpected,unexpected)
 ck('native_files_not_written',all(b.a.sha(f.r.GAME/p)==h for p,h in load('VERSION.json')['native'].items()))
 geo=graph_check();ck('no_new_centralized_orphan',not geo['new_centralized_orphan_cells'],geo['new_centralized_orphan_cells'])
 _,parts=n.demographics()
 for row in ledger:ck('exact_new_population.'+row['state'],parts[row['state'],'NNT']==row['target_after'] and parts[row['state'],'NNT']>0)
 result=dict(status='PASS' if all(z['passed'] for z in checks) else 'FAIL',passed=sum(z['passed'] for z in checks),total=len(checks),checks=checks,engine_validation='NOT_RUN',human_validation=False,scope='Installed Russian1776 decentralisation and native Cossack access only')
 dump('VALIDATION.json',result);print(result['status'],result['passed'],'/',result['total']);print([z for z in checks if not z['passed']])

def write_report(name,text):
 path=LOT/name
 if path.exists():assert raw(path)==text,'Do not silently replace an existing report: '+name
 else:path.write_text(text,encoding='utf8',newline='')

def reports():
 assert load('VALIDATION.json')['status']=='PASS'
 plan=load('PLAN.json');v=load('VALIDATION.json');before=load('APPLY_BEFORE.json');owners=n.b4.inventory()['owners'];_,parts=n.demographics()
 allrows=load('RUSSIAN_PARTS_BEFORE.json');reasons={
 'STATE_NENETSIA':('PARTIAL_DECENTRALISATION','111 cellules des toundras orientales ; Poustozersk/Petchora, Mezen, îles et arrière-pays russe conservés. Proxy de communautés, pas indépendance nationale démontrée.','N1,N2,N3,M1776'),
 'STATE_OB':('PARTIAL_DECENTRALISATION','233 cellules du Yamal/Gydan ; Obdorsk et axe du bas Ob conservés. Les terres khanties de la portion restante ne sont pas automatiquement libérées.','N1,N4,M1776'),
 'STATE_NORTHERN_NORWAY':('KEEP','Districts communs Neiden/Pasvik : installation nordique conservée ; fiscalités superposées ne prouvent pas un nouvel État indépendant.','NORDIC-01'),
 'STATE_WEST_KARELIA':('KEEP','Vieille-Finlande cédée en1721/1743 : institutions particulières sous administration russe, pas communauté à coloniser.','E1'),
 'STATE_KUOPIO':('KEEP','Nyslott/Savonlinna cédé en1743 ; ne pas rouvrir une acquisition effective pour le gameplay colonial.','E1,NORDIC-01'),
 'STATE_MOGILEV':('KEEP','Acquisition1772 et droit local maintenu : différence juridique sous pouvoir russe, sans nouvelle indépendance.','E2'),
 'STATE_VITEBSK':('KEEP','Même première partition1772 ; droits conservés ne suffisent pas à décentraliser.','E2'),
 'STATE_CHERNIHIV':('KEEP','Hetmanat aboli1764, organisation régimentaire jusqu’en1781 ; autonomie résiduelle sans évacuation du pouvoir russe.','E3'),
 'STATE_KHARKOV':('KEEP','Réforme de Sloboda1765 : ne pas rétablir les régiments autonomes comme pays libres.','E3'),
 'STATE_ROSTOV':('KEEP_COSSACK_ACCESS','Don : communauté militaire russe ; établissement cosaque natif, aucune cession à un pays décentralisé.','C1'),
 'STATE_SAMARA':('KEEP_COSSACK_ACCESS','Samara/Orenbourg et ligne fortifiée acquises ; implantation cosaque1748, aucune restitution générale de la région à des clans.','C1,CENTRAL-ASIA-01'),
 'STATE_URALSK':('KEEP_COSSACK_ACCESS','Yaïk/Ouralsk et Gouriev : deux noyaux russes conservés ; arrière-pays kazakh déjà distinct.','C1,CENTRAL-ASIA-01'),
 'STATE_AST​RAKHAN'.replace('\u200b',''):('KEEP_COSSACK_ACCESS','Astrakhan et ligne de la Volga ; régiment cosaque attesté1750.','C2'),
 'STATE_UFA':('KEEP','Bachkirie après les campagnes d’Orenbourg et la répression1773–1775 : droits communautaires ne justifient pas une indépendance générale en1776.','E4'),
 'STATE_CHELYABINSK':('KEEP','Ligne et établissements ouraliens conservés ; aucune frontière ethnique exclusive déduite des droits bachkirs.','E4'),
 'STATE_KALMYKIA':('KEEP','Après l’exode et l’abolition du khanat1771, ne pas recréer un khanat indépendant ; administrations d’oulous reconnues comme limite du modèle.','E5'),
 'STATE_SAKHALIN':('KEEP_KURIL_OUTPOSTS','Les deux RGB russes sont des îles Kouriles ; leur nom régional ne justifie ni annexion de Sakhaline ni transfert automatique.','SAKHALIN_CELL_READING.json,M1776'),
 'STATE_SEMIRECHE':('KEEP','Trois noyaux de l’Irtych, pas toute la Semiretchie ; délimitations antérieures conservées.','CENTRAL-ASIA-01'),
 'STATE_AKMOLINSK':('KEEP','Ligne russe et jüz distinguées par le lot précédent ; aucune nouvelle cession sans preuve locale.','CENTRAL-ASIA-01'),
 'STATE_DAGESTAN':('KEEP','Seul petit noyau russe existant conservé ; pas d’annexion régionale ni de suppression d’un poste sur une présomption.','MAP2D'),
 'STATE_STAVROPOL':('KEEP','Noyau de la ligne russe conservé ; peuples caucasiens voisins non réannexés.','MAP2D')}
 for sid in ['STATE_CHERSON','STATE_CRIMEA','STATE_TAURIDA']:reasons[sid]=('KEEP','Conquêtes/ports1774–1775 conservés ; aucune annexion générale du khanat de Crimée anticipant1783.','MAP2D,E3')
 for sid in ['STATE_SURGUT','STATE_TOBOLSK','STATE_TOMSK','STATE_UPPER_YENISEYSK','STATE_KRASNOYARSK','STATE_YAKUTSK','STATE_KOLYMA','STATE_OKHOTSK','STATE_IRKUTSK','STATE_BURYATIA','STATE_TRANS_BAIKAL','STATE_KAMCHATKA']:
  reasons[sid]=('KEEP_WITH_FRONTIER_LIMITS','Forts, collecte de l’iasak et administration russes attestés ; absence de peuplement dense non assimilée à une indépendance. Fin détail des hinterlands ouvert, aucun État indigène uniforme inventé.','S1,S2,M1776')
 for row in allrows:
  decision,reason,sources=reasons.get(row['state'],('KEEP','Portion existante conservée : aucun élément décisif de cette passe ne justifie une décentralisation ; pas de certification cadastrale globale.','M1776,baseline courante'))
  row.update(decision=decision,reason=reason,sources=sources,incorporation_change=False,transferred_RGBs=next((z['RGBs'] for z in plan if z['state']==row['state']),[]))
 dump('RUSSIAN_FRONTIER_DECISIONS.json',allrows)
 dump('USER_REQUEST.json',dict(date='2026-11-07',authority='Current direct user request and correction',correction_verbatim='Je voulais parler de décentraliser, pas désincorporer les territoires.',scope='Entire Russian frontier including European contacts; decentralised ownership, not incorporation-only changes',earlier_incorporation_candidate_list_abandoned_before_any_functional_write=True,runtime_attested=False))
 cells={c['RGB']:c for c in load('FRONTIER_CELLS.json')};dump('GEOGRAPHIC_CROSSWALK.json',[dict(cells[c],before='RUS',after='NNT',source_ids=row['source_ids']) for row in plan for c in row['RGBs']])
 dump('FILES_DELIVERED.json',[dict(file=z['file'],before=z['before'],after=b.a.sha(ROOT/z['file'])) for z in load('FILES_MODIFIED.json')])
 table=['| Région | RUS avant | RUS après | NNT après |','|---|---:|---:|---:|']
 for row in plan:
  oldpop=next(q['population'] for q in allrows if q['state']==row['state']);table.append(f"| {row['state'].removeprefix('STATE_')} | {oldpop} | {parts[row['state'],'RUS']} | {parts[row['state'],'NNT']} |")
 write_report('REPORT.md',f'''# RUSSIA-01 — Frontières russes et colonisation,1776

7 novembre2026 — **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. La correction explicite du joueur remplace la première interprétation : il s’agit de **décentralisation territoriale**, pas de désincorporation. Aucun des vingt candidats administratifs envisagés initialement n’a été installé comme tel.

**344 RGB existants passent de RUS à NNT**, agrégat décentralisé de communautés nenets :111 dans NENETSIA,233 dans OB. La toundra orientale de la Russie européenne et le Yamal/Gydan sont donc accessibles à la colonisation ; Poustozersk/Petchora, Mezen, Obdorsk, Berezov, les lignes fortifiées de l’Oural et les îles arctiques conservées restent russes. Aucun pixel, nouveau RGB, ressource, terrain, hub ou frontière d’un voisin n’est modifié. Liste exhaustive dans PLAN.json/GEOGRAPHIC_CROSSWALK.json ; carte CARTE_REPERES.png.

**Il s’agit d’une approximation de gameplay des communautés et du contrôle local**, pas de la découverte d’un État nenets souverain en1776. Le tribut, les lettres de sujétion et la répression de1746 sont documentés et contredisent une lecture d’indépendance juridique intégrale. La mobilité et l’administration très discontinue de l’intérieur motivent le choix décentralisé ; les limites précises des parcours saisonniers ne sont pas restituées. NNT n’est ni tributaire ni suzerain ; sa culture `ugrian` est le proxy indigène déjà présent dans ces pools, sans création d’une culture moderne ni conversion de POPs.

Les **59 portions russes** sont consignées dans RUSSIAN_FRONTIER_DECISIONS.json, y compris les frontières européennes, caucasiennes, kazakhes et pacifiques. Vieille-Finlande, territoires de1772, Ukraine, Don, Bachkirie et Kalmoukie ne sont pas transformés en peuples libres sur la seule base de leur statut particulier. Les administrations de l’iasak ne sont pas assimilées automatiquement à une absence de pouvoir russe. La Tchoukotka CKC est déjà décentralisée ; les jüz, polities caucasiennes, territoires Qing, Sakhaline indigène et le comptoir ALK sont préservés. Les deux cellules russes du fichier régional SAKHALIN sont kouriles. Cette passe ne certifie pas chaque cadastre frontalier.

La mécanique native1.15 est rendue accessible : loi **Colonisation interne**, amendement **Cosaques**, institution coloniale niveau1, cinq paramètres natifs et scores IA d’établissement/dissolution restaurés. Quatre commandes natives initialisent les implantations du Don, du Yaïk, d’Orenbourg et d’Astrakhan ; aucun corps militaire supplémentaire n’est recruté. Orenbourg est représenté par la vaste région moteur SAMARA : ce n’est pas la preuve que toute la région était une communauté cosaque. L’établissement réserve normalement20% des terres arables et son fonctionnement dépend des effectifs, de la capacité de la portion et du PM natif. Aucun corps de1851/1858/1860 n’est projeté en1776. Les effets réels et la croissance coloniale restent à tester.

{chr(10).join(table)}

Monde : **837328654 → 837328654**.4779 habitants passent dans les portions NNT ; cultures, religions explicites/implicites et autres champs sont conservés. Seul le pool indigène est réparti selon les comptes de cellules ; les pools russes/tatars restent sur les axes de peuplement. C’est une allocation technique, pas un recensement ou une mesure de densité par pixels. Aucun ancien bâtiment, PM, propriété ou régiment n’est déplacé. Les quatre implantations cosaques sont les seuls ajouts bâtis demandés au moteur.

Profil NNT explicite de quatre capacités anciennes : **PASS_STATIC_ONLY**. Aucun nouveau P0/P1 sur sept témoins ; dettes existantes conservées et publiées dans TECH_NON_REGRESSION.json, dont gate des cuirassiers russes et historique CKC absent. Aucun graphe TECH ou recette commune modifié.

**{v['passed']}/{v['total']} contrôles statiques réussis**, dont propriétés exactes, conservation de cohortes, statuts des59 portions, références1.15, absence de nouveau tribut et de nouvelle enclave centralisée. Le premier contrôle de continuité a relevé sept cellules côtières isolées : elles sont réintégrées à l’enveloppe nenets, avec réparation et premier échec archivés. Les îles russes préexistantes restent distinctes. Contrôle moteur, rendu des capitales/drapeaux, comportement IA, emplois et budget : **NOT_RUN**.

Cinq fichiers partagés ciblés et sept ajouts privés. Les sept fichiers économiques modifiés extérieurement entre le relevé initial et les préimages sont enregistrés, puis conservés. Tous les autres fichiers fonctionnels et preuves SERG sont identiques aux préimages immédiates. Aucun Git, vanilla ou suivi SERG écrit. WORLD reste10/320,3,13%, aucun point joueur ajouté.

Suite : contrôle russe groupé avec RUNTIME_PROTOCOL.md ; aucune autre région automatiquement engagée.
''')
 write_report('SOURCES.md','''# Sources et choix — RUSSIA-01

Consultées le7 novembre2026. Date politique :1er janvier1776. Les frontières de jeu suivent des cellules natives et une enveloppe de toundra relue sur la carte ; elles ne proviennent pas d’un cadastre précis de1776.

- **N1 — Laur Vallikivi, Words and Silences, Indiana University Press,2024**, [introduction](https://publish.iupress.indiana.edu/read/words-and-silences/section/5a77ae64-2fdc-4a04-b714-030e0c74dd3c), [notice éditeur](https://iupress.org/9780253068767/words-and-silences/). Passages historiques de l’introduction consultés via les extraits indexés ; corps HTML direct non restitué, aucune lecture intégrale du livre revendiquée. Forte variation du contact, Poustozersk1499, prélèvements d’iasak et relations commerciales auXVIIIe siècle ; certains intérieurs très tardivement parcourus par les étrangers. Motive une représentation discontinue, pas une souveraineté nationale indépendante de tous les Nenets.
- **N2 — William Mandel, Nenets National Okrug, Encyclopedia Arctica**, [manuscrit numérisé Dartmouth](https://collections.dartmouth.edu/arctica-beta/html/EA10-18.html), sections historiques pp010–015 et géographie pp001–003. Texte effectivement consulté. Signale la répression1746 et la sujétion tributaires : **contre-preuve explicite** d’une indépendance juridique générale. Les garanties de possession de toundra et les difficultés de contrôle distinguent droits locaux/contrôle territorial. Document duXXe siècle et vocabulaire soviétique : ses limites administratives et chiffres modernes ne sont pas transférés à1776.
- **N3 — Musée régional nenets**, [Poustozersk](https://naomuseum.ru/nao-zoom/Pustozersk-the_first_Russian_city_in_the_Arctic/), §§ sur fondation1499, rôle administratif et expéditions duXVIIIe siècle, texte consulté. Décisif pour garder le poste et l’axe de Petchora russes ; Naryan-Mar est un repère moteur moderne proche, pas une ville de1776.
- **N4 — Bibliothèque présidentielle**, [histoire du Yamal](https://www.prlib.ru/collections/682119), notice historique consultée : Obdorsk1595, Mangazeïa1601 et opérations d’iasak. Maintien des postes et du bas Ob russes. Ne prouve pas l’administration uniforme de toute la péninsule.
- **M1776 — Treskot/Schmidt, Carte de la Russie d’Asie,1776**, [exemplaire Berne/e-rara](https://www.e-rara.ch/bes_1/content/titleinfo/10462866), DOI10.3931/e-rara-33725. Réutilisation du scan déjà installé dans CENTRAL-ASIA-01/sources ; carte complète réellement vue. Figure un domaine impérial et ses routes/postes, pas la mesure de la soumission de chaque clan. Aucune citation de sa surface coloriée comme preuve d’occupation continue.
- **E1 — Archives nationales finlandaises**, [Vanha Suomi](https://portti.kansallisarkisto.fi/arkistojen-portti/vanha-suomi), passages sur1721/1743, administration1744 et réforme1784, texte consulté. Droit suédois maintenu sous souveraineté russe : raison de conserver les acquisitions et le lot NORDIC-01.
- **E2 — Igor Gushchinsky,2023**, [notice et résumé Lituanistika](https://www.lituanistika.lt/content/107131), article sur les provinces biélorusses/lituaniennes1772–1840, DOI10.15688/jvolsu4.2023.2.6. Résumé réellement consulté ; Statut lituanien et remplacement ultérieur. Pas de lecture intégrale revendiquée ; maintien d’un droit local ne vaut pas indépendance.
- **E3 — Internet Encyclopedia of Ukraine / CIUS**, [Autonomy](https://www.encyclopediaofukraine.com/display.asp?linkpath=pages%5CA%5CU%5CAutonomy.htm), [Slobidska Ukraine](https://www.encyclopediaofukraine.com/display.asp?linkpath=pages%5CS%5CL%5CSlobidskaUkraine.htm), sections duXVIIIe siècle consultées : Hetmanat1764/1781, réforme de Sloboda1765, destruction de la Sitch1775. Aucun rétablissement d’indépendance ou d’institution postérieure.
- **E4/C1 — V.A.Kuznetsov**, [Création de l’armée cosaque d’Orenbourg](https://history.milportal.ru/sozdanie-orenburgskogo-kazachego-vojska/?print=print), article historique consulté, et [Musée d’Orsk, catalogue ARTEFACT](https://ar.culture.ru/en/subject/znak-orenburgskogo-kazachego-voyska), contexte historique consulté :1748, ligne de forts et statut particulier. L’objet exposé est postérieur et n’est pas présenté comme une icône de1776. **Charles Steinwedel, Threads of Empire,2016**, [chapitres JSTOR](https://www.jstor.org/stable/j.ctt1bmzmbx), débuts des chapitres1–3 consultés, pas tout le livre : intégration de la Bachkirie et campagnes1730–1775. Aucune anticipation des cantons1798 ou du muftiat1789.
- **C2 — Association internationale d’histoire militaire**, [Astrakhanskoe kazache voisko](https://imha.ru/1144537423-astrahanskoe-kazache-voysko.html), paragraphe d’ouverture consulté : transformation en régiment1750. Les effectifs/stanitsas du début duXXe siècle ne servent pas à dimensionner le départ1776.
- **E5 — Gulnar T.Kendirbai,2018**, [DOI](https://doi.org/10.1163/22105018-12340110), résumé consulté sur1771 et pratiques de frontière intérieure. Accès complet refusé : pas de preuve de lecture de tout l’article. Le khanat aboli et les institutions d’oulous ne sont pas remplacés ici par un nouvel État indépendant.
- **S1 — Natalia Platonova,2007**, [notice et résumé éditeur](https://www.revues.armand-colin.com/histoire/histoire-economie-societe/histoire-economie-societe-42007/commissions-denquete-ladministration-siberienne-limpot-peuples-autochtones-russie), pp27–50, résumé consulté sur les commissions d’iasak1760s. **Y.Akimov,2023**, [résumé HSE](https://publications.hse.ru/chapters/808801834), pp140–167, DOI10.1515/9798887191478-009 : serment, tribut et otages. Administration indirecte ne signifie pas absence de toute autorité russe ; les régions entières ne sont pas libérées pour leur seule faible densité.
- **S2 — S.V.Bereznitsky,2019**, [Kunstkamera](https://journal.kunstkamera.ru/archive/2019_3/bereznickij_sv_metodika_sbora_etnograficheskih_materialov_komandira_anadyrskogo_ostroga_fridriha_plenisnera_v_xviii_v), DOI10.31250/2618-8619-2019-3(5)-189-199, résumé consulté sur Anadyr1649–1771 ; lien anglais a ensuite expiré. La Tchoukotka décentralisée existante est préservée ; pas de nouvelle forteresse russe à Anadyr après son évacuation.

**Technique1.15** : fichiers natifs copiés et empreintes VERSION.json/native_inputs ; version release/1.15.0, build du3 novembre2026. Loi, amendement, effet establish_cossack_host, PM et scores IA réellement lus localement. Seule la nouvelle loi, les paramètres masqués et le champ IA absent sont restaurés ; pas de copie complète des histoires russes1836. Les anciennes institutions, compagnies et journaux du nouveau DLC ne sont pas importés en bloc.

**Limite décisive.** La décentralisation nenets est un compromis de simulation entre sujétion impériale et autonomie quotidienne. Le jeu ne représente pas correctement un territoire à la fois tributaire diffus et colonisable. Le statut juridique de1746 n’est ni caché ni effacé ; aucune frontière ethnographique moderne n’est déclarée exacte pour1776. Les noms de culture, chiffres et petits hubs sont des données héritées, pas de nouvelles attestations historiques.
''')
 write_report('RUNTIME_PROTOCOL.md','''# Vérification russe groupée

Version : FILES_DELIVERED.json. Non exécutée par l’agent ; aucune attestation humaine ajoutée.

1. Nouvelle partie1776. CARTE_REPERES.png : communautés nenets décentralisées dans les deux régions ; Petchora et Obdorsk restent russes. Aucun tribut ni suzerain NNT. Vérifier le nom, la capitale et le drapeau générés.
2. Russie : loi Colonisation interne et amendement Cosaques actifs, institution coloniale niveau1. Inspecter le bouton d’établissement sur une portion frontalière russe et le PM de recrutement cosaque. Les quatre commandes initiales du Don/Yaïk/Orenbourg/Astrakhan doivent charger ; vérifier le cas de la très petite portion d’Ouralsk et sa capacité arable.
3. Essayer une colonie sur NNT depuis le voisin russe, puis contrôler la croissance effectivement apportée par le recrutement cosaque. Vérifier l’emploi, les terres réservées, le coût administratif et les tensions ; un bâtiment présent ne garantit pas une croissance si personne ne travaille.
4. Simulation d’un mois, sauvegarde/rechargement. Contrôler l’absence de nouvelle enclave russe et la conservation des postes, de CKC, des jüz et des polities caucasiennes. Témoin : voisin Qing/ALK et un pays européen inchangés.

Pas de test intermédiaire par sous-zone requis. Le profil NNT n’a pas de chef historique inventé ; les noms et placements automatiques restent à observer. Aucun autre territoire n’est lancé automatiquement après cette passe.
''')
 # Final readable map: only grounded historical settlement markers.
 hubs=load('FRONTIER_HUBS.json');labels={'Naryan-Mar':'Poustozersk (repère proche)','Obdorsk':'Obdorsk','Mezen':'Mezen'};hubs=[dict(h,Hub_Name=labels[h['Hub_Name']]) for h in hubs if h['Hub_Name'] in labels]
 f.render(owners,'INSTALLED',hubs=hubs)
 pic=Image.open(LOT/'NORTH_WEST_INSTALLED.png');canvas=Image.new('RGB',(pic.width,pic.height+145),'#fbf8ee');canvas.paste(pic,(0,70));d=ImageDraw.Draw(canvas);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',25);small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
 d.text((20,18),'1776 — Communautés nenets décentralisées',font=font,fill='#202d28')
 x0,y0,x1,y1=f.BOXES['NORTH_WEST']
 for number,x,y,label in [(1,5460,245,'Toundra européenne / Oural polaire'),(2,5705,170,'Yamal'),(3,5860,190,'Gydan')]:
  xx,yy=(x-x0)*2,70+(y-y0)*2;d.ellipse((xx-18,yy-18,xx+18,yy+18),fill='white',outline='#473a26',width=2);d.text((xx-8,yy-14),str(number),font=font,fill='black')
 d.text((20,pic.height+86),'1 Toundras au nord-est de la Petchora   2 Yamal   3 Gydan — ocre : NNT / vert : RUS',font=small,fill='#283c2e')
 d.text((20,pic.height+116),'Carte du mod, pas une capture moteur ; enveloppe politique approximative et contrôle impérial diffus.',font=small,fill='#54534a');canvas.save(LOT/'CARTE_REPERES.png')
 print('Reports,59 decisions,344 cells, final map and protocol written.')

def tracking():
 assert load('VALIDATION.json')['status']=='PASS';assert not (LOT/'TRACKING_PATCHES.json').exists(),'Do not replay tracking'
 world=f.r.WORLD;old={k:raw(world/k) for k in TRACK};sha={k:b.a.sha(world/k) for k in TRACK}
 for k in TRACK:
  dest=LOT/'tracking_inputs'/k;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(world/k,dest)
 state=json.loads(old['ROADMAP_STATE.json']);assert state['scope_version']=='1.0.3'
 state['scope_version']='1.0.4';state['scope_amendments'].append(dict(version='1.0.4',date='2026-11-07',authority='RUSSIA-01/USER_REQUEST.json',change='Explicit Russian frontier decentralisation, including European interfaces and native1.15 Cossack access; auxiliary outside legacy320 criteria.',criteria_total_unchanged=320))
 state['steering_history'].append(state['current_steering']);state['current_phase']='RUSSIA_AUXILIARY';state['current_steering']=dict(date='2026-11-07',authority='RUSSIA-01/USER_REQUEST.json',last_lot='RUSSIA-01',scope='Russian frontier decentralisation, not incorporation-only changes',next_pass='Grouped Russian runtime checks; no automatic new region',runtime_validation_timing='GROUPED_RUSSIA',intermediate_player_tests_requested=False,full_V_credit=False)
 state['phase_transition_gate']=dict(source='RUSSIA-01/USER_REQUEST.json',explicit_transition_authorized=True,authorized_next_phase='RUSSIA_AUXILIARY',rule='Direct user request after Ottoman pass; correction specifies decentralisation.',authorization_is_full_canonical_V_validation=False,partial_lot_tests_requested=False)
 state['lots'].append(dict(id='RUSSIA-01',date='2026-11-07',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',auxiliary_scope_outside_legacy_denominator=True,native_RGBs_transferred=344,existing_files_modified=5,new_files=7,new_TAGs=1,population_delta=0,receipt='RUSSIA-01/FILES_DELIVERED.json',runtime='NOT_RUN',credited_criteria=[]))
 static=sum(c['status']=='STATIC_VERIFIED' for p in state['phases'] for r in p['subregions'] for c in r['criteria'].values());human=sum(c['status']=='USER_VALIDATED' for p in state['phases'] for r in p['subregions'] for c in r['criteria'].values());assert(static,human,state['progress']['criteria_total'])==(10,0,320)
 dump('PROGRESS_CALCULATION.json',dict(technical_verified=static,runtime_full_criteria=human,criteria_total=320,technical_percent=round(100*static/320,2),new_points=0,auxiliary_lot_scored_in_legacy_register=False))
 out=dict(old);out['ROADMAP_STATE.json']=json.dumps(state,ensure_ascii=False,indent=2)+'\n'
 entry='\n\n## 7 novembre2026 — RUSSIA-01 installé\n\nDécentralisation expressément demandée, aucune désincorporation seule.344RGB natifs vers les communautés nenets,111 enRussie européenne/Oural polaire et233 auYamal/Gydan ; postes et lignes russes conservés, CKC déjà décentralisé inchangé.59portions examinées ; NNT est un compromis de contrôle local, les droits impériaux et la répression1746 restent documentés. Loi/amendement cosaque natifs1.15 restaurés, quatre commandes d’implantations anciennes, niveau colonial1 et scores IA natifs.4779habitants réaffectés, monde837328654 inchangé, cohortes/anciens stocks conservés. ProfilNNT PASS_STATIC_ONLY, aucun nouveauP0/P1 sur7témoins.532/532statiques ; réparation de7poches côtières et premier échec archivés.5fichiers partagés ciblés+7ajouts ; économie/TECH/SERG/Amériques préservés. Aucun moteur/joueur attesté. Rapport RUSSIA-01/REPORT.md ; test russe groupé ensuite, aucune autre région automatique. Extension auxiliaire1.0.4 ; WORLD10/320,3,13% inchangé.\n'
 for k in ['ROADMAP.md','PROGRESS_HISTORY.md']:out[k]=old[k]+entry
 out['OWNERSHIP_BOUNDARIES.md']=old['OWNERSHIP_BOUNDARIES.md']+'\n\n## RUSSIA-01 — 7 novembre2026\n\nSeuls344RGB existants RUS enNENETSIA/OB versNNT. Préserver les autres voisins et toutes les réservesSERG/DP. Aucun bitmap, hub, ressource ou terrain écrit. Dans les POPs, seul le pool ugrian des deux régions est scindé ; populations russes/tatares conservées. Seuls autres blocs partagés : histoirec:RUS (loi/amendement/institution), ajout du champ IA natif cossack_host_scores. Aucun graphe/recette commun modifié ; quatre effets natifs d’établissement dans un fichier propre. Sept changements économiques extérieurs observés avant préimages sont conservés. Réparation côtière séparée, aucune restauration de baseline.\n'
 out['BLOCKERS.md']=old['BLOCKERS.md']+'\n\n## RUSSIA-01 — limites et moteur\n\nNNT est une approximation coloniale de communautés à contrôle impérial discontinu ; la sujétion et1746 ne sont pas niées. Tracé saisonnier/cadastral, petits hubs, chef/drapeau et budget non certifiés. Culture ugrian héritée, allocation indigène technique, pas nouveau recensement. Cosaques : emplois/arable/PM/croissance et petite portion d’Ouralsk attendent moteur ; lois et objets1.15 passent les contrôles statiques, pas une observation de chargement. Dettes préexistantes RUS/CKC publiées, aucune attribution abusive au lot. Test russe groupé, aucun test intermédiaire par pays ou transition automatique.\n'
 out['NEXT_ACTION.md']=old['NEXT_ACTION.md']+'\n\n## Priorité courante — 7 novembre2026 : RUSSIA-01\n\nNouvelle consigne explicite russe installée. Voir REPORT.md, CARTE_REPERES.png et RUNTIME_PROTOCOL.md dansRUSSIA-01. Vérification groupée de la décentralisation nenets et de l’accès cosaque1.15 : colonies, emplois, terres réservées et croissance ; simulation d’un mois et sauvegarde/rechargement. Préserver CKC, lignes de forts, jüz, Caucasiens, Qing, ALK et réserves concurrentes. Aucun changement automatique des autres régions, ni attestation humaine inventée. Les anciennes prochaines actions ci-dessus restent des étapes historiques, pas des ordres de reprise.\n'
 con=json.loads(old['CONCURRENT_CHANGES.json']);con['RUSSIA-01']=dict(receipt='RUSSIA-01/CONCURRENT_CHANGES.json',functional_files=12,native_RGBs_transferred=344,pixels_recolored=0,population_delta=0,Git_writes=0,vanilla_writes=0,SERG_writes=0);out['CONCURRENT_CHANGES.json']=json.dumps(con,ensure_ascii=False,indent=2)+'\n'
 for k,text in out.items():
  assert b.a.sha(world/k)==sha[k],'Concurrent tracking change: '+k
  (world/k).write_bytes(text.encode('utf8'))
 dump('TRACKING_PATCHES.json',[dict(file=(world/k).relative_to(ROOT).as_posix(),before=sha[k],after=b.a.sha(world/k)) for k in TRACK]);print('Additive tracking, legacy10/320 unchanged.')

def final():
 assert load('VALIDATION.json')['status']=='PASS'
 receipts=load('FILES_DELIVERED.json');state=json.loads(raw(f.r.WORLD/'ROADMAP_STATE.json'))
 checks=dict(functional_receipts_current=all(b.a.sha(ROOT/z['file'])==z['after'] for z in receipts),canonical_lot_installed=any(z['id']=='RUSSIA-01' for z in state['lots']),legacy_progress_unchanged=state['progress']['technical_verified']==10 and state['progress']['criteria_total']==320 and state['progress']['runtime_user_validated']==0,tracking_receipts_current=all(b.a.sha(ROOT/z['file'])==z['after'] for z in load('TRACKING_PATCHES.json')),no_human_attestation_created=not list(LOT.glob('*USER_VALIDATED*')))
 dump('DELIVERY_CHECKS.json',checks);assert all(checks.values()),checks
 files=[ROOT/z['file'] for z in receipts]+[p for p in LOT.rglob('*') if p.is_file() and p.name!='DELIVERY_MANIFEST.json']+[f.r.WORLD/k for k in TRACK]+[ROOT/'tools'/p for p in ['world1776_russia01.py','world1776_russia01_frontiers.py','world1776_russia01_closeout.py']]
 dump('DELIVERY_MANIFEST.json',{p.relative_to(ROOT).as_posix():b.a.sha(p) for p in files});print('Final receipts and manifest verified; engine NOT_RUN.')

if __name__=='__main__':
 p=argparse.ArgumentParser()
 for key in ['tech','validate','reports','tracking','final']:p.add_argument('--'+key,action='store_true')
 a=p.parse_args()
 if a.tech:technology()
 if a.validate:validate()
 if a.reports:reports()
 if a.tracking:tracking()
 if a.final:final()
