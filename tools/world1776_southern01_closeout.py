"""Southern Africa evidence, guarded tracking and final delivery checks."""
import json,csv,shutil,argparse
from collections import Counter
from decimal import Decimal,ROUND_HALF_UP
import world1776_southern01 as h
import world1776_sahel0205_closeout as old
import localization_duplicate_audit as loc
ROOT,LOT=h.ROOT,h.LOT
WORLD=LOT.parent
TRACK=['ROADMAP.md','ROADMAP_STATE.json','NEXT_ACTION.md','BLOCKERS.md','PROGRESS_HISTORY.md','OWNERSHIP_BOUNDARIES.md','CONCURRENT_CHANGES.json']
def doc(n,t):h.save(LOT/n,t)
def read(p):return json.loads(p.read_text('utf-8-sig'))
def write(p,v):h.save(p,json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def evidence():
    before=h.load('APPLY_BEFORE.json');plan=h.load('PLAN.json');a=Counter();z=Counter()
    for path in h.b.tech.effective('common/history/pops'):
        rel=path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else None
        z.update(old.portions(h.raw(path)))
        a.update(old.portions(h.raw(LOT/'apply_inputs'/rel) if rel in before['scope'] else h.raw(path)))
    states={r['state'] for r in plan};tags={r['source'] for r in plan}|{r['target'] for r in plan}|set(h.p.COUNTRIES)
    rows=[dict(state=s,country=t,before=a[s,t],after=z[s,t],delta=z[s,t]-a[s,t]) for s,t in sorted(set(a)|set(z)) if s in states]
    ledger=dict(world_before=sum(a.values()),world_after=sum(z.values()),delta=sum(z.values())-sum(a.values()),portions=rows,countries=[dict(TAG=t,before=sum(v for (s,c),v in a.items() if c==t),after=sum(v for (s,c),v in z.items() if c==t)) for t in sorted(tags)],state_totals=[dict(state=s,before=sum(v for (c,t),v in a.items() if c==s),after=sum(v for (c,t),v in z.items() if c==s)) for s in sorted(states)],historical_population_correction=False,method='Conservative splitting of each inherited cohort by enumerated unique native provinces in each source portion, integer remainder allocation. Not historical density/census; cultures, religions and slave attributes unchanged.')
    h.dump('POPULATION_LEDGER.json',ledger)
    with (LOT/'POPULATION_BEFORE_AFTER.csv').open('w',encoding='utf-8-sig',newline='') as stream:
        w=csv.DictWriter(stream,fieldnames=['state','country','before','after','delta']);w.writeheader();w.writerows(rows)
    cells={r['RGB']:r for r in h.load('GEOMETRY_CELLS.json')};cross=[]
    for r in plan:
        for c in r['RGBs']:
            cell=cells[c];cross.append(dict(RGB=c,state=r['state'],before=r['source'],after=r['target'],pixels=cell['pixels'],bbox=cell['bbox'],centroid=cell['centroid'],historical_basis=r['historical_basis'],precision=r['precision']))
    h.dump('GEOGRAPHIC_CROSSWALK.json',dict(cells=cross,new_RGBs=0,pixels_recolored=0,historical_date='1776-01-01',coordinates_are_navigation_not_cadastre=True))
    h.geometry(h.raw(LOT/'apply_inputs'/h.ST));(LOT/'BEFORE.png').write_bytes((LOT/'PROPOSED.png').read_bytes())
    h.geometry(h.raw(ROOT/h.ST));(LOT/'AFTER.png').write_bytes((LOT/'PROPOSED.png').read_bytes())

def delivered():
 rows={r['file']:dict(r) for r in h.load('FILES_MODIFIED.json')}
 for name in ['COMPATIBILITY_REPAIR.json','COMPATIBILITY_REPAIR_R2.json']:
  for r in h.load(name)['files']:
   if r['file'] in rows:rows[r['file']]['after']=r['after']
   else:rows[r['file']]=dict(r)
 return rows

def reports():
 pop=h.load('POPULATION_LEDGER.json');v=h.load('VALIDATION.json');rows=delivered()
 h.dump('FILES_DELIVERED.json',list(rows.values()))
 # Formation deltas use explicit unit nodes, keeping the indirect conscription
 # effects distinct. Only the WBL node is intentionally neutralised.
 before=h.load('APPLY_BEFORE.json');oldunits=Counter();newunits=Counter()
 def units(text):
  out=Counter()
  for n in h.b.walk(h.b.parse(text)):
   if not n.key.startswith('c:'):continue
   for u in h.b.walk([n]):
    if u.key=='combat_unit':out[(n.key,u.one('type'),u.one('service_type') or 'regular',u.one('state_region'))]+=int(u.one('count') or 1)
  return out
 for path in h.b.tech.effective('common/history/military_formations'):
  rel=path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else None
  text=h.raw(path);newunits.update(units(text));oldunits.update(units(h.raw(LOT/'apply_inputs'/rel) if rel in before['scope'] else text))
 delta=[dict(country=k[0],type=k[1],service=k[2],state=k[3],before=oldunits[k],after=newunits[k],delta=newunits[k]-oldunits[k]) for k in sorted(set(oldunits)|set(newunits)) if oldunits[k]!=newunits[k]]
 h.dump('MILITARY_DELTA.json',dict(explicit_units_before=sum(oldunits.values()),explicit_units_after=sum(newunits.values()),delta=delta,indirect_conscription_effects_preserved=['MSH','MTB'],rationale='Only the one WBL irregular regular battalion belonging to a later territorial government is removed. No Boer/Griqua formation transferred to indigenous chiefs; all other explicit unit nodes preserved.'))
 def num(n):return f'{n:,}'.replace(',',' ')
 populations='\n'.join('| '+r['TAG']+' | '+num(r['before'])+' | '+num(r['after'])+' |' for r in pop['countries'])
 regions='\n'.join('| '+r['state']+' | '+num(r['before'])+' | '+num(r['after'])+' |' for r in pop['state_totals'])
 doc('REPORT.md',f'''# SOUTHERN-01 — Afrique australe au1erjanvier1776

**28octobre2026 — IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION.** Consigne directe : «tu peux passé à l'afrique austral». Passe cartographique et initialisation nécessaire ; aucun nouveau personnage, flavor, recette ou raffinement des bâtiments. Test africain groupé, sans demande intermédiaire.

## Corrections installées

**126provinces natives réattribuées dans4régions moteur**, sans nouveau RGB ni pixel redessiné. Détail intégral : PLAN.json et GEOGRAPHIC_CROSSWALK.json ; illustrations BEFORE.png et AFTER.png. Les indices de travail sont ceux de GEOMETRY_CELLS.json, pas de nouveaux identifiants moteur.

- ORA/Orange et TRN/Transvaal cessent d'être des propriétaires initiaux : leurs territoires reviennent aux ensembles locaux sotho, tswana et du Haut-Veld.
- PHL/Philippolis et WBL/Waterboer cessent d'être des États initiaux. Un agrégat autonome des **communautés de l'Orange** (KQO) distingue les pouvoirs locaux de ces formations ultérieures.
- Les22cellules tswana du Natal passent aux **chefferies nguni** (NST). Aucun empire de Shaka n'est installé.
-38cellules du Karoo passent de TSW aux communautés SAN ; deux cellules riveraines supplémentaires passent à KQO. Les18cellules tswana au nord du secteur NorthernCape sont conservées.
- Les **chefferies du Haut-Veld** HVD reçoivent les11cellules de TRN et21de l'enveloppe MTB. MTB conserve7cellules du secteur Pretoria/Wonderboom, devient explicitement un agrégat ndébélé et a désormais une capitale dans TRANSVAAL. La culture nationale shona de ce proxy est retirée ; aucune culture de POP n'est convertie.
- BST représente des **chefferies sotho autonomes**, et non un État national de Moshoeshoe anticipé. SWZ conserve son noyau politique sous le nom **Ngwane**.
- MSH représente le pouvoir royal **Rozvi**, avec un lien tributaire vers MNC/Manyika ; Mutapa reste distinct. Ses60RGB ne changent pas de propriétaire. L'enveloppe large inclut des marges et des autorités tributaires : elle n'est pas une certification d'administration directe uniforme.

**Cap/VOC :** les48cellules DEI de CAPE_COLONY/EASTERN_CAPE sont conservées. La progression des fermes et la juridiction effective ne sont pas synonymes ; les sources ne justifient pas une nouvelle ligne cadastrale automatique. DEI reste le proxy politique VOC avec ses autres possessions ; aucun redécoupage de Java ou changement de souveraineté néerlandaise.

Les frontières Xhosa/Rharhabe/Gcaleka ne sont pas artificiellement alignées sur le Kei en1776 : Peires2012 montre des implantations et une chronologie plus mobiles. Thembu/Mpondo, Venda/Pedi, nord du noyau Ngwane, Chobe/Luyana et subdivisions namibiennes restent des limites à préciser, sans nouveaux partages conjecturaux. Cela interdit une clôture exhaustive de P3-08.

## Population

Monde courant : **{num(pop['world_before'])} → {num(pop['world_after'])}**, delta **{pop['delta']}**. La baseline capturée dès le début vaut déjà837328654, soit115de plus que le précédent reçu Madagascar ; cet écart est antérieur à cette passe, non attribué ici et non compensé. Aucune variation mondiale n'est produite par SOUTHERN-01.

| Région moteur | Avant | Après |
|---|---:|---:|
{regions}

| Pays ou agrégat | Avant | Après |
|---|---:|---:|
{populations}

Toutes les cohortes culturelles/religieuses/serviles sont conservées. La ventilation par nombre de provinces natives, avec restes entiers conservatifs, est technique ; elle n'est pas un recensement de1776. Des populations boers/griqua héritées subsistent dans les pools : aucun peuplement de1776 de ces proportions n'est attesté par ce transfert. Pas d'assimilation ni de compensation démographique cachée.

## Institutions, technologies et armées

**3TAG nouveaux** NST/HVD/KQO et4profils existants ajustés : MSH, BST, MTB, SWZ. Agrégats autonomes en catégorie décentralisée ; pouvoir royal rozvi et noyau ngwane non reconnus, avec monarchie. Catégorie décentralisée ne signifie pas absence de chefs, de rois locaux ou d'organisation. Les cours précises ne sont pas inventées. Les modèles natifs1836 de personnages BST/MTB sont neutralisés ; NgwaneIII déjà présent est conservé. Les demandes initiales du journal ultérieur du Haut-Veld de BST/SWZ sont retirées dans leurs seules histoires.

Connaissances anciennes conservées, explicitement résolues pour les4profils réinitialisés. Ajouts ciblés : international_relations pour MSH/SWZ ; organized_military_establishments pour MSH et, après contrôle des casernes héritées, HVD/KQO/BST/TSW. Les premières capacités représentent échanges et cadres armés locaux, pas une industrie d'armement. Les autres nouveautés ont leurs profils agricoles, pastoraux et artisanaux motivés dans COUNTRY_PROFILES.json.

Le premier contrôle de compatibilité a détecté les casernes conservées sans leur gate chez4destinataires. COMPATIBILITY_REPAIR.json trace la correction ; COMPATIBILITY_REPAIR_R2.json retire un grant NST involontaire issu d'une liste de capacités partagée dans l'outil. Les échecs et le premier contrôle statique sont archivés, pas présentés comme résultats finaux. **3profils nouveaux PASS_STATIC_ONLY, aucune connaissance antérieure retirée et aucun nouveau P0/P1 sur16témoins.** Dettes techniques anciennes non masquées ; aucun graphe TECH ou recette commune modifié.

Niveaux des bâtiments, PM et pools mondiaux conservés. Un seul bataillon régulier irrégulier de WBL est retiré avec ce gouvernement territorial ultérieur ; aucun transfert artificiel vers un chef local. Toutes les autres unités explicites sont identiques et les appels de conscription MSH/MTB conservés. MILITARY_DELTA.json donne les comptes réels. Emploi, coûts, marchés, mobilisation et viabilité ne sont pas des observations moteur.

## Contrôles et concurrence

**{v['passed']}/{v['total']} contrôles statiques**, plus les vérifications finales de livraison dans DELIVERY_VALIDATION.json : propriétaires et unicité des RGB, conservation des cohortes/niveaux/PM, capitales, contiguïté des pouvoirs centralisés et voisinage centralisé de SWZ/MSH, technologies et fichiers témoins. Les agrégats tswana peuvent avoir plusieurs composantes : ce sont des communautés distinctes, pas une nouvelle enclave centralisée. Aucun corridor arbitraire créé.

**{len(rows)}fichiers fonctionnels livrés :10existants ciblés,12ajouts.** Préimages immédiates et empreintes dans apply_inputs/, repair_inputs/ et FILES_DELIVERED.json. Hors nœuds autorisés, les fichiers partagés sont conservés. Madagascar, INTERIOR-01, autres passes WORLD, SERG, TECH/ECON et Amériques sont protégés ; aucun changement extérieur entre survey et installation. Pas d'écriture Git, vanilla, bitmap, terrain, ressource, hub/locator ou suiviSERG. Les anciens reçus restent historiques et ne sont pas rejoués comme des tests actuels.

Sources et limites : SOURCES.md, GEOGRAPHIC_LIMITATIONS.md. Les noms de hubs sont des repères natifs, certains ultérieurs ; leur présence ne prouve pas une souveraineté de1776. Drapeaux, capitales/hubs rendus, lois effectives, budgets, fronts et sauvegarde restent à observer au test africain groupé.

**WORLD :10/320(3,13%),0validation humaine créditée.** Aucun critère entier gagné sur un noyau partiel. Prochaine action : contrôle cartographique africain groupé et reprise des seuls points concrets qui en résultent. Aucun autre continent ni lissage général lancé automatiquement.
''')
 doc('SOURCES.md','''# Sources — SOUTHERN-01

Consultation28octobre2026, référence1erjanvier1776. Les sources fournissent des autorités/ensembles géographiques ; les listes RGB sont une interprétation manuelle explicite. Ni catalogue, ni nom moderne de hub n'est une preuve cadastrale.

1. DonaldDenoon, «L'Afrique australe», Histoire générale de l'Afrique, V, UNESCO, pp743-764. PDF local sources/UNESCO_DENOON_SOUTHERN.pdf, extrait textuel et carte23.1 p744 consultés ; passages de travail pp747-754,758,760-764. https://bokundoli.org/wp-content/uploads/2021/12/T5-25.pdf . Carte de géographie régionale couvrant XVIe-XVIIIe siècles, pas carte politique au1janvier1776. Communautés, cultures matérielles, pastoralisme, autorités et frontières du Cap sont distingués ; carte utilisée avec les côtes et fleuves natifs, sans copier des limites contemporaines.

2. H.H.K.Bhila, «La région au sud du Zambèze», même volume, pp697-741. PDF conservé dans INTERIOR-01/sources/UNESCO_SOUTH_ZAMBEZI.pdf ; pp714-718 et carte22.8 p715 réellement relues. https://bokundoli.org/wp-content/uploads/2021/12/T5-24.pdf . Centre rozvi Butwa/Danangombe/Khami, extension et gouvernement par tribut. Manyika conserve son territoire et ses autorités dans un pacte tributaire ; Mutapa n'est pas annexé. Les marges de l'enveloppe MSH restent ouvertes.

3. PhilipBonner, Kings,Commoners and Concessionaires, CambridgeUP,1983, chapitre2 pp9-13 consultées et passage p25. https://sahistory.org.za/sites/default/files/archive-files3/philip_bonner_kings_commoners_and_concessionairbook4you.pdf . Les Ngwane s'établissent à Shiselweni dans les années1760-1770, avant l'expansion septentrionale ; ne justifie ni un royaume swazi moderne intégral ni la suppression de leur autonomie. Trois provinces natives conservées, pas d'extension inventée pour assurer un voisinage.

4. CarolynHamilton et JohnWright, «Rethinking the Political Order in the KwaZulu-Natal Region in the Eighteenth and Early Nineteenth Centuries: Fluidity,Mobility,and Flexibility», HistoryinAfrica, publication30mars2026, DOI10.1017/hia.2025.10012. Résumé et sections mobilité/mosaïque politique réellement consultés, pas ouvrage entier revendiqué. https://www.cambridge.org/core/journals/history-in-africa/article/rethinking-the-political-order-in-the-kwazulunatal-region-in-the-eighteenth-and-early-nineteenth-centuries-fluidity-mobility-and-flexibility/7345F47BDB92714B8BBFCCEDCE6383D2 . Appuie une représentation plurielle et met en garde contre des États tribaux figés ; ne fournit pas les contours exacts NST/HVD.

5. University of the Free State, The Forgotten Highway Route, entrée «Griquatown», bibliothèque/ICDF. Page effectivement lue : https://pokello.ufs.ac.za/s/the-forgotten-highway-route/page/griquatown . San/Korana avant l'implantation missionnaire1800-1804, nom Griquatown1813 et construction du pouvoir Waterboer ultérieurs. KQO n'est pas un nouvel État griqua unifié.

6. South African History Online, «The Ndebele in history»,2011, mise à jour20juillet2026, section EarlyHistory lue : https://sahistory.org.za/article/ndebele-history . Synthèse secondaire : Wonderboom/Mnyamana, divisions Manala/Ndzundza, distinction des amaKhumalo de Mzilikazi arrivés ultérieurement. Noyau natif de7cellules retenu, précision politique faible. Rapport HIA Mahwelereng2023 et chapitre universitaire Pretoria ne sont connus que par extraits indexés (accès direct403) : pistes, pas lectures intégrales ni preuves indépendantes revendiquées.

7. JeffPeires, «He Wears Short Clothes! Rethinking Rharhabe(c.1715-c.1782)», JournalofSouthernAfricanStudies38(2),2012,pp333-354, DOI10.1080/03057070.2012.666143. Texte auteur en ligne consulté : résumé, tableau3 et discussion des implantations/Kei et des expéditions. https://www.researchgate.net/publication/254311583_'He_Wears_Short_Clothes'_Rethinking_Rharhabe_c1715-c1782 . La séparation territoriale simple transkei/ciskei après1775 n'est pas un contour sûr : Gcaleka est encore à l'ouest du Kei peu après et les implantations changent. Aucune nouvelle ligne Xhosa n'est installée sur cette seule convention.

Pistes non promues : thèses Guelke/Giliomee sur la frontière du Cap, sources Pedi chronologiquement divergentes, datation interne des royaumes ovambo et Chobe/Luyana. Pas de grant de souveraineté ou de nouveau personnage sur la foi d'un résultat de recherche isolé.
''')
 doc('GEOGRAPHIC_LIMITATIONS.md','''# Limites géographiques et politiques

126transferts sur cellules préexistantes ; aucun lissage de pixels ou subdivision arbitraire. Les enveloppes suivent la géographie côtes/fleuves/plateaux vérifiée sur NATIVE_PROVINCES_AND_RIVERS.png et les cartes régionales des sources. Ce sont des approximations politiques, pas un atlas cadastral.

Cap : frontière mobile de fermes, commandos, droits coloniaux et communautés khoi/san ; les48provincesDEI sont conservées sans certification de contrôle uniforme. Nom Graaff-Reinet ultérieur ne démontre pas absence de fermes en1776. Aucun nouveau pays du Cap créé ; DEI reste un proxyVOC à capitale javanaise.

TSW : sous-ensembles locaux autonomes, dont une composante au sud séparée ; pas une nation tswana centralisée. NST : autorités nguni locales, sans rétablir les futurs empires de Shaka ou Dingiswayo. KQO : Kora/San et communautés riveraines, frontières internes et chronologie des implantations mixtes non closes. SAN : conservation technique de groupes multiples, pas absence d'organisation ni assimilation des POPs.

MTB : noyau du secteur Pretoria retenu, frontières Manala/Ndzundza et autres communautés non cadastrées ; HVD agrège plusieurs autorités. BST : autorités sotho de plaines/montagnes et voisins, pas Moshoeshoe. PDI/VND gardent des agrégats natifs à préciser ; royautés locales reconnues historiquement sans prétendre que la catégorie moteur est exhaustive. SWZ : noyau ngwane conservé, secteur nord approximatif ; voisinage TMP reste effectif sans corridor neuf.

MSH : pouvoir rozvi et tribut Manyika, pas propriété directe de tous les villages des60cellules. Les marges occidentales, septentrionales et du bas-veld sont approximatives. Le locator de capitale ne représente pas nécessairement Danangombe : aucun hub déplacé sous couvert de frontière. Les cellules MTP/MNC/POR/TMP/TCH de la passe précédente sont conservées.

XHO : chronologie des lieux de Phalo/Gcaleka/Rharhabe mobile, séparation au Kei non installée ; Thembu/Mpondo restent agrégés dans le contour natif faute de rapprochement daté suffisant. Chobe/Luyana, Nama/Herero/Ovambo : données conservées, découpages précis encore ouverts. Ce lot ne certifie pas qu'il ne reste plus d'erreurs en Afrique australe.

Hubs, noms de lieux, drapeaux, lois effectivement actives, marchés, fronts, rendus et sauvegarde ne sont pas validés par les statiques. Tests joueur africains groupés, aucune attestation créée.
''')
 doc('GROUPED_RUNTIME_ITEMS.md','''# Éléments du test africain groupé — NOT_RUN

Pas de test intermédiaire demandé. Lors du test africain groupé, sur nouvelle partie1776 : vérifier l'absence initiale d'ORA/TRN/PHL/WBL et la présence de NST/HVD/KQO ; communautés sotho/ndébélé, nom Ngwane, pouvoir rozvi et tribut Manyika. Contrôler les témoins Cap/VOC, Mutapa/Manyika, Tembe/Mozambique et Madagascar ; carte, capitales/hubs et drapeaux, lois effectives, casernes/PM transférés et absence d'enclave centralisée nouvelle. Observer marchés, mobilisation, fronts et budgets pendant une simulation adaptée, puis sauvegarder/recharger. Aucun résultat ni durée n'est prérempli.
''')
 doc('USER_REQUEST.txt',"tu peux passé à l'afrique austral\n\nPortée héritée : frontières/initialisation nécessaire, pas de flavor ; lissage différé ; autonomie permise, aucune nouvelle enclave centralisée au milieu de décentralisés ; test africain groupé ; pas de Git/vanilla/SERG.\n")
 doc('REPRODUCE.md','''# Reproduction sans réinstaller

Python du runtime, UTF-8 : tools/world1776_southern01.py --tech --validate puis tools/world1776_southern01_closeout.py --final. Lire les diagnostics avant tout nouveau patch. Ne pas rejouer --apply, --preflight, --tracking ou la capture survey ; leurs données d'entrée sont historiques. Les réparations sont des événements conservés, FILES_DELIVERED.json donne la composition finale. --evidence/--reports ne vaut pas exécution moteur.
''')

def tracking():
 assert not (LOT/'TRACKING_PATCHES.json').exists()
 hashes={n:h.b.a.sha(WORLD/n) for n in TRACK}
 for n in TRACK:dest=LOT/'tracking_inputs'/n;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(WORLD/n,dest)
 data=read(WORLD/'ROADMAP_STATE.json');assert not any(r['id']=='SOUTHERN-01' for r in data['lots'])
 for phase in data['phases']:
  for region in phase['subregions']:
   if region['id']!='P3-08':continue
   for k,c in region['criteria'].items():
    if c['status'] in ['STATIC_VERIFIED','USER_VALIDATED']:continue
    if k=='V':c.update(evidence='SOUTHERN-01/GROUPED_RUNTIME_ITEMS.md')
    else:c.update(status='PARTIAL',evidence='SOUTHERN-01/REPORT.md',remaining='126cellules et noyaux politiques installés ; frontièreVOC, subdivisions locales, démographie historique, institutions fines et moteur non clos. Aucun point entier.')
  count=sum(c['status']=='STATIC_VERIFIED' for r in phase['subregions'] for c in r['criteria'].values());phase['progress'].update(technical_verified=count,technical_percent=float((Decimal(count)*100/Decimal(phase['progress']['criteria_total'])).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)))
 assert sum(p['progress']['technical_verified'] for p in data['phases'])==10
 data['lots'].append(dict(id='SOUTHERN-01',date='2026-10-28',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',existing_files_modified=10,new_files=12,new_tags=3,native_RGBs_transferred=126,new_RGBs=0,pixels_recolored=0,world_population_delta=0,receipt='SOUTHERN-01/FILES_DELIVERED.json',credited_criteria=[],runtime='NOT_RUN'))
 data['steering_history'].append(data['current_steering']);data['current_steering']=dict(date='2026-10-28',authority='SOUTHERN-01/USER_REQUEST.txt',last_lot='SOUTHERN-01',scope='Southern African territorial corrections installed, no cadastral closure claimed',next_pass='Grouped African cartographic review; act on concrete findings, no automatic new region',cosmetic_smoothing_deferred=True,autonomous_subjects_authorized=True,runtime_validation_timing='GROUPED_AFRICA',intermediate_player_tests_requested=False,full_V_credit=False)
 entry='''\n\n## SOUTHERN-01 —28octobre2026\n\nAfrique australe autorisée directement :126RGB natifs réattribués dans4régions, aucun pixel nouveau. Républiques boers/Philippolis/Waterboer retirées du départ, communautés Orange/Haut-Veld/Nguni distinguées ; Karoo SAN, autorités sotho/ndébélé autonomes, noyau Ngwane et pouvoir rozvi/tribut Manyika. CapVOC conservé, frontières Xhosa et marges non certifiées.3TAG nouveaux,10fichiers ciblés+12ajouts,202statiques et3profilsPASS_STATIC_ONLY ; aucun P0/P1 introduit sur16témoins. Monde courant837328654inchangé, cohortes/niveaux/PM conservés ; un bataillonWBL du gouvernement ultérieur retiré, autres unités explicites conservées. Anciennes connaissances conservées, grants précoces bornés, pas de graphe/recette commune ni nouveau personnage. Sources/limites/repairs et reçus SOUTHERN-01/REPORT.md. Test africain groupéNOT_RUN, WORLD10/320(3,13%),aucun crédit humain. Aucun autre secteur lancé.\n'''
 assert all(h.b.a.sha(WORLD/n)==v for n,v in hashes.items())
 write(WORLD/'ROADMAP_STATE.json',data)
 for n in ['ROADMAP.md','PROGRESS_HISTORY.md']:h.save(WORLD/n,h.raw(WORLD/n).rstrip()+entry)
 h.save(WORLD/'BLOCKERS.md',h.raw(WORLD/'BLOCKERS.md').rstrip()+'''\n\n## SOUTHERN-01 — limites restantes\n\nInstallation cartographique partielle, pas de clôture P3-08. FrontièreVOC mouvante, marges rozvi, noyau Ngwane septentrional, contours internes des chefferies/agrégats, Xhosa/Thembu/Mpondo, Pedi/Venda et Chobe/Namibie non cadastrés. POPs hérités boers/griqua conservés techniquement sans attestation de peuplement1776. Hubs/capitales/drapeaux, lois effectives, budgets, mobilisation, fronts et sauvegarde attendent le test africain groupé. Écart mondial115antérieur à cette passe conservé, pas de compensation. Aucun point entier ni attestation humaine.\n''')
 h.save(WORLD/'OWNERSHIP_BOUNDARIES.md',h.raw(WORLD/'OWNERSHIP_BOUNDARIES.md').rstrip()+'''\n\n## SOUTHERN-01 — périmètre installé\n\n126RGB natifs,4nœuds ZULULAND/VRYSTAAT/TRANSVAAL/NORTHERN_CAPE des états/POPs/bâtiments, plus TRANSVAAL redistribution bâtie. Histoires BST/MSH/SWZ et grant TSW ; c:WBL seul neutralisé dans les formations, relation GBR→ORA seule retirée.3TAG nouveaux,4définitions existantes surchargées, histoire nativeMTB et personnagesBST/MTB masqués par fichiers propres ; loi/effets/tributMSH→MNC/FR-EN propres. Pas de pixel, terrain, ressource, locator ou recette commune. FILES_DELIVERED.json et préimages immédiates font référence ; autres nœuds et travauxWORLD/SERG/TECH/ECON/Amériques/Madagascar préservés, aucune baseline restaurée.\n''')
 h.save(WORLD/'NEXT_ACTION.md','''# Prochaine action — après SOUTHERN-01\n\nPasse australe installée sur instruction directe. Lire SOUTHERN-01/REPORT.md, SOURCES.md, GEOGRAPHIC_LIMITATIONS.md, PLAN.json, POPULATION_LEDGER.json, TECH_NON_REGRESSION.json, VALIDATION.json, DELIVERY_VALIDATION.json et FILES_DELIVERED.json.126RGB,3TAG nouveaux ; aucun contrôle moteur/humain inventé. Cap conservé ; enveloppes et subdivisions locales ouvertes, pas de certification exhaustive.\n\nSuite : vérification cartographique africaine groupée et reprise des anomalies concrètes signalées, sur version courante. Pas de test intermédiaire réclamé, autre continent ni lissage général lancé automatiquement. Préserver Madagascar/INTERIOR/Congo/Corne/Sahel/Maghreb/Balkans, SERG et chantiers TECH/ECON/Amériques. WORLD10/320(3,13%),aucun point entier nouveau.\n''')
 concurrent=read(WORLD/'CONCURRENT_CHANGES.json');concurrent['SOUTHERN-01']=dict(receipt='SOUTHERN-01/CONCURRENT_CHANGES.json',existing_functional_files_modified=10,new_files=12,native_RGBs_transferred=126,world_population_delta=0,Git_writes=0,vanilla_writes=0,SERG_writes=0,old_baseline_restored=False);write(WORLD/'CONCURRENT_CHANGES.json',concurrent)
 h.dump('TRACKING_PATCHES.json',[dict(file='docs/reports/map/WORLD_1776_CLOSURE/'+n,before=hashes[n],after=h.b.a.sha(WORLD/n)) for n in TRACK])

def final():
 rows=delivered();checks=[]
 def ck(k,v,d=None):checks.append(dict(check=k,passed=bool(v),detail=d))
 for r,rec in rows.items():ck('delivered_hash.'+r,h.b.a.sha(ROOT/r)==rec['after'])
 h.dump('FILES_DELIVERED.json',list(rows.values()));ck('22_functional_files',len(rows)==22)
 ck('static_pass',h.load('VALIDATION.json')['status']=='PASS')
 for r in h.load('STARTING_TECH_NEW_COUNTRIES.json'):ck('profile.'+r['TAG'],r['status']=='PASS_STATIC_ONLY')
 for r in h.load('TECH_NON_REGRESSION.json')['existing_country_comparison']:
  ck('no_new_P0_P1.'+r['TAG'],not r['introduced']);ck('knowledge_preserved.'+r['TAG'],not r['knowledge_removed'])
 pop=h.load('POPULATION_LEDGER.json');ck('world_population',pop['delta']==0)
 for r in pop['state_totals']:ck('region_population.'+r['state'],r['before']==r['after'])
 ck('all_profiles_populated',all(any(r['TAG']==t and r['after']>0 for r in pop['countries']) for t in h.p.COUNTRIES))
 colors=[c for r in h.load('PLAN.json') for c in r['RGBs']];ck('126_unique_transfers',len(colors)==len(set(colors))==126)
 military=h.load('MILITARY_DELTA.json');ck('only_WBL_unit_delta',len(military['delta'])==1 and military['delta'][0]['country']=='c:WBL' and military['delta'][0]['delta']==-1,military['delta'])
 sets={};language=[]
 for lang in ['french','english']:
  entries=loc.entries(lang,replacement=True);own={k:v for k,v in entries.items() if any(path.name==h.PREFIX+'_l_'+lang+'.yml' for path,n,t in v)};sets[lang]=set(own)
  language.extend(dict(check=lang+'.'+k,passed=len(v)==1) for k,v in own.items());ck('localization_BOM.'+lang,(ROOT/f'localization/{lang}/replace/{h.PREFIX}_l_{lang}.yml').read_bytes().startswith(b'\xef\xbb\xbf'))
 language.append(dict(check='same_bilingual_keys',passed=sets['french']==sets['english']));h.dump('LOCALIZATION_CHECK.json',dict(status='PASS' if all(r['passed'] for r in language) else 'FAIL',checks=language,render_runtime='NOT_RUN'));ck('localization',all(r['passed'] for r in language))
 data=read(WORLD/'ROADMAP_STATE.json');technical=[r['id']+'/'+k for phase in data['phases'] for r in phase['subregions'] for k,c in r['criteria'].items() if c['status']=='STATIC_VERIFIED'];human=[r['id']+'/'+k for phase in data['phases'] for r in phase['subregions'] for k,c in r['criteria'].items() if c['status']=='USER_VALIDATED']
 ck('canonical_progress',len(technical)==10 and not human and data['progress']['technical_verified']==10 and data['progress']['criteria_total']==320);h.dump('PROGRESS_CALCULATION.json',dict(credited=technical,user_validated=human,numerator=10,denominator=320,percent=3.13,newly_credited=[],partial_regions_receive_no_credit=True))
 outside=[r for r,v in h.load('APPLY_BEFORE.json')['protected'].items() if r not in rows and h.b.a.sha(ROOT/r)!=v];ck('all_outside_protected_preserved',not outside,outside)
 needed=['REPORT.md','SOURCES.md','GEOGRAPHIC_LIMITATIONS.md','PLAN.json','COUNTRY_PROFILES.json','GEOGRAPHIC_CROSSWALK.json','POPULATION_LEDGER.json','POPULATION_BEFORE_AFTER.csv','MILITARY_DELTA.json','VALIDATION.json','TECH_NON_REGRESSION.json','STARTING_TECH_NEW_COUNTRIES.json','STARTING_TECH_EXISTING_AFTER.json','LOCALIZATION_CHECK.json','CONCURRENT_CHANGES.json','COMPATIBILITY_REPAIR.json','COMPATIBILITY_REPAIR_R2.json','BEFORE.png','AFTER.png','FILES_DELIVERED.json','TRACKING_PATCHES.json','PROGRESS_CALCULATION.json','GROUPED_RUNTIME_ITEMS.md','USER_REQUEST.txt','REPRODUCE.md']
 for n in needed:ck('evidence.'+n,(LOT/n).is_file())
 result=dict(status='PASS' if all(r['passed'] for r in checks) else 'FAIL',passed=sum(r['passed'] for r in checks),total=len(checks),checks=checks,automated_engine_test=False,human_validated=False);h.dump('DELIVERY_VALIDATION.json',result)
 files=[ROOT/r for r in rows]+[LOT/n for n in needed]+[LOT/'DELIVERY_VALIDATION.json']+[WORLD/n for n in TRACK]+[ROOT/'tools'/('world1776_southern01'+s+'.py') for s in ['','_plan','_inspect','_closeout']]+list((LOT/'sources').iterdir());h.dump('DELIVERY_MANIFEST.json',{p.relative_to(ROOT).as_posix():h.b.a.sha(p) for p in files if p.is_file()})
 print('Delivery',result['status'],result['passed'],'/',result['total']);print('FAIL',[r for r in checks if not r['passed']]);return result['status']=='PASS'

if __name__=='__main__':
 parser=argparse.ArgumentParser()
 for k in ['evidence','reports','tracking','final']:parser.add_argument('--'+k,action='store_true')
 a=parser.parse_args()
 if a.evidence:evidence()
 if a.reports:reports()
 if a.tracking:tracking()
 if a.final:raise SystemExit(0 if final() else 1)
