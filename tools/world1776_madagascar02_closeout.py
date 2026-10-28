"""Malagasy territorial evidence and bounded delivery checks, no engine claims."""
import json,csv,shutil,argparse
from collections import Counter,deque
from decimal import Decimal,ROUND_HALF_UP
import world1776_madagascar02 as h
import world1776_sahel0205_closeout as old
import localization_duplicate_audit as loc
ROOT,LOT=h.ROOT,h.LOT
WORLD=LOT.parent
TRACK=['ROADMAP.md','ROADMAP_STATE.json','NEXT_ACTION.md','BLOCKERS.md','PROGRESS_HISTORY.md','OWNERSHIP_BOUNDARIES.md','CONCURRENT_CHANGES.json']
def doc(name,text):h.save(LOT/name,text)
def write(path,value):h.save(path,json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def read(path):return json.loads(path.read_text('utf-8-sig'))
def delivered():
    rows={r['file']:dict(r) for r in h.load('FILES_MODIFIED.json')}
    for r in h.load('FORMAT_PRESERVATION.json')['files']:rows[r['file']]['after']=r['after']
    for r in h.load('ROYAL_TIER_REPAIR.json')['files']:rows[r['file']]['after']=r['after']
    return rows

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

def reports():
    pop=h.load('POPULATION_LEDGER.json');v=h.load('VALIDATION.json');tech=h.load('TECH_NON_REGRESSION.json')
    known={r['TAG']:r['technologies'] for r in h.load('STARTING_TECH_NEW_COUNTRIES.json')+h.load('STARTING_TECH_EXISTING_AFTER.json')}
    profiles='\n'.join('| '+t+' | '+r.get('fr','Antananarivo')+' | '+r['kind']+' | '+str(len(known[t]))+' |' for t,r in h.p.COUNTRIES.items())
    populations='\n'.join('| '+r['TAG']+' | '+f"{r['before']:,}".replace(',',' ')+' | '+f"{r['after']:,}".replace(',',' ')+' |' for r in pop['countries'])
    doc('REPORT.md',f'''# MADAGASCAR-02 — restauration politique de1776

**28 octobre2026 — IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION.** Autorisation directe : «Ok, corrige Marina.», suivie de «fini». Référence : **1er janvier1776**. Frontières et initialisation nécessaire uniquement ; aucun nouveau personnage ni raffinement de bâtiments. Lissage cosmétique et test africain groupé restent différés.

## Corrections installées

Le pays MAD possédait les deux régions moteur entières, soit122RGB. **120 provinces natives sont réattribuées dans28groupes ; MAD en conserve2.** Aucun pixel recoloré, nouveau RGB, terrain, ressource ou locator. Énumération complète : [PLAN.json](PLAN.json), coordonnées/propriétaires : [GEOGRAPHIC_CROSSWALK.json](GEOGRAPHIC_CROSSWALK.json), cartes [avant](BEFORE.png) et [après](AFTER.png).

MAD représente désormais **Antananarivo** ; **Ambohimanga et Ambohidratrimo** sont séparés. **Boina, Menabe, Antankarana, Isandra, Lalangina, Manandriana, Arindrano, Ikongo, Antemoro, Antambahoaka, Antefasy, Antesaka et Fiherenana** ont des noyaux royaux distincts. Les profils **Tsimihety, Sihanaka, Bezanozano, Betsimisaraka, Imamo/Andratsay, Tanala, Bara, Mahafaly, Antanosy et Antandroy** représentent des ensembles locaux autonomes. Les agrégats pluriels reconnaissent leurs chefs/cours : catégorie décentralisée ne signifie pas absence d'organisation.

La province native **x606CE0**, rattachée à SOUTH_MADAGASCAR, couvre aussi les **Comores**. Elle devient l'agrégat autonome **Sultanats des Comores**. L'audit précédent parlait trop globalement de122provinces de l'île : la géométrie distingue121provinces continentales/littorales malgaches et cette province d'archipel. Pas de souveraineté merina sur les Comores, ni d'union politique comorienne moderne affirmée. Les cours insulaires restent agrégées faute de subdivision native séparée.

Un seul lien tributaire est installé : **Boina → Antankarana**. Les autres tributs, influences et hégémonies ne deviennent pas des annexions ou pactes généraux sans précision suffisante. Les cours merina ne sont donc pas subordonnées mécaniquement à un destinataire sakalava non établi. Les détails sont exposés dans SOURCES.md et GEOGRAPHIC_LIMITATIONS.md.

## Institutions et connaissances initiales

**26TAG nouveaux,27profils dont MAD conservé.** Les royaumes ont une monarchie non reconnue, les agrégats locaux des institutions de chefferies autonomes. Aucun roi daté ou personnage ajouté. Le modèle natif de personnage MAD_ranavalona_hova, hérité du scénario1836, est neutralisé dans une surcharge propre ; aucune généalogie de remplacement n'est inventée.

| TAG | Nom | Catégorie moteur | Technologies connues |
|---|---|---|---:|
{profiles}

COUNTRY_PROFILES.json motive chaque capacité : agriculture/élevage, transformation alimentaire, artisanat, textile, échanges et organisation militaire sont distingués selon les pouvoirs. Les échanges côtiers ne donnent ni assurance commerciale ni fabrication industrielle d'armes. Loi privée de coutumes commerciales avec prérequis international_relations pour les royaumes concernés ; aucun changement d'un effet commun. **MAD garde exactement ses technologies héritées.** Graphe TECH, recettes et PM communs inchangés.

Les26nouveaux profils sont **PASS_STATIC_ONLY**. La comparaison MAD/FRA/POR n'introduit aucun P0/P1 ; les dettes natives de MAD, notamment les conditions de recrutement de certaines unités, restent documentées dans TECH_NON_REGRESSION.json. Aucune technologie distribuée pour dissimuler ces dettes. Les lois demandées et PM explicites sont vérifiés ; les défauts moteur et lois réellement actives ne sont pas certifiés.

## Population et armée

Monde : **{pop['world_before']:,} → {pop['world_after']:,}**, delta **{pop['delta']}**. Les deux totaux régionaux et toutes les cohortes culturelles, religieuses et serviles sont conservés. La ventilation par nombre de provinces natives uniques, avec arrondis conservatifs, est **technique**, pas un recensement de1776. Les chiffres comoriens héritent du pool statistique natif de SOUTH_MADAGASCAR ; aucune conversion de POP ni reconstruction démographique de l'archipel.

| Pays/agrégat | Avant | Après |
|---|---:|---:|
{populations}

Détails : POPULATION_LEDGER.json et POPULATION_BEFORE_AFTER.csv. Cultures nationales moteur malagasy et, pour les Comores, swahili/malagasy sont des proxys documentés. Aucun profil culturel de POP n'est réécrit.

Les niveaux bâtis et PM ne sont pas modifiés : les portions natives des historiques de bâtiments examinées sont vides. Armée existante conservée par nombre/type/service ; les neuf conscrits référencés au sud sont rattachés au nord où MAD possède encore une portion. Aucun régiment créé, retiré ou attribué arbitrairement aux nouveaux royaumes. Manpower, budgets et capacité effective de mobilisation après le partage ne sont pas des résultats observés.

## Contrôles et concurrence

VALIDATION.json : **{v['passed']}/{v['total']} contrôles statiques**, dont delta exact des propriétaires mondiaux, absence de nouveau doublon, cultures référencées, capitales régionales possédées, continuité des noyaux et préservation hors blocs autorisés. Aucun nouveau noyau centralisé isolé dans des seuls pays décentralisés. Petites dépendances côtières héritées d'Antankarana et archipels sont distingués des poches continentales ; Imamo/Andratsay reste explicitement plural et non contigu.

**5fichiers existants ciblés et33ajouts fonctionnels.** Seuls deux nœuds d'états, deux nœuds POP, c:MAD de l'histoire nationale et militaire, et MAD des noms dynamiques sont modifiés. Les autres nations de ces fichiers sont conservées. Les versions WORLD antérieures, SERG, TECH/ECON et Amériques restent protégées ; aucun Git, vanilla ou suiviSERG écrit. Pas de retour à une ancienne baseline. FILES_MODIFIED.json est le reçu immédiat, FILES_DELIVERED.json et DELIVERY_MANIFEST.json la version livrée. Contrôle documentaire final : DELIVERY_VALIDATION.json.

Les noyaux sont des approximations sur cellules entières. À l'échelle native, les trois collines royales merina ne peuvent pas toutes être localisées exactement ; aucun cadastre fictif créé pour y remédier. Les noms/points de hubs natifs parfois inadéquats ne sont pas déplacés. Les frontières internes des agrégats, conditions tributaires restantes, installations européennes ponctuelles et densités historiques restent ouverts. Voir GEOGRAPHIC_LIMITATIONS.md.

Chargement, portraits/drapeaux, capitales affichées, marchés, budgets, fronts, simulation et sauvegarde/rechargement : **NOT_RUN**, intégrés au **test africain groupé**, aucun test intermédiaire demandé. Aucun reçu humain nouveau. WORLD reste **10/320 (3,13%)** ; aucun critère entier crédité pour une restauration partielle. L'Afrique australe/VOC est la suite demandée, non commencée par ce lot.
''')
    doc('SOURCES.md','''# Sources consultées — MADAGASCAR-02

Référence1janvier1776 ; consultation28octobre2026. Les noms ethniques sont des aides de localisation, jamais une preuve suffisante de souveraineté ou de frontières.

1. **R.K.Kent**, «Madagascar et les îles de l'océan Indien», Histoire générale de l'Afrique,V,ch.28,p.921–967. [PDF public](https://bokundoli.org/wp-content/uploads/2021/12/T5-30.pdf), copie intégrale/extraction sources/UNESCO_KENT_MADAGASCAR.pdf/.txt. Passages ciblés effectivement lus dans : p.921–923,932–938,939–960 et960–962 ; pas de lecture intégrale du volume revendiquée. Carte28.1,p.922/PDF2 rendue et examinée dans MAP_28_1_ETHNIC_CONTEXT.png : localisation/coastlines seulement, **carte ethnique, pas cadastre1776**.

Repères vérifiables : p.944–947, cours sakalava/antankarana, autonomie tsimihety et tribut de1775 ; p.947–951, formations betsileo et cours merina avant consolidation ; p.951–953, Alaotra/Ankay et centre royal d'Ikongo ; p.955–960, pouvoirs de l'est et du sud ; p.960–962, sultanats des Comores. Ces pages motivent les noyaux et leurs différences de statut, pas des polygones exacts. Les hégémonies et chronologies dynastiques incertaines ne deviennent pas des dates ou annexion automatiques.

2. **Gerald M.Berg**, «Sacred Acquisition: Andrianampoinimerina at Ambohimanga,1777–1790», Journal of African History29(2),1988,p.191–211. [Extrait public Cambridge](https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/sacred-acquisition-andrianampoinimerina-at-ambohimanga-17771790/EBA65FD0322C0EA8D5B77EBE801598F8), consulté lors de MADAGASCAR-01-AUDIT, réutilisé ; article intégral non lu. Son analyse place une première réussite politique à Ambohimanga en1783. Les datations1783,1777–1778 et1787 selon les études ne sont pas arbitrairement unifiées. Aucune arrivée au pouvoir datée ni personne nouvelle installée.

3. **UNESCO/ICOMOS**, [évaluation patrimoniale Ambohimanga2001](https://whc.unesco.org/document/1118), et [fiche officielle](https://whc.unesco.org/en/list/950/), passages historiques consultés à l'audit : existence des cours/fortifications, pas limites provinciales. Le nom natif du jeu «Royaume Mérina» est analysé comme un consommateur de localisation, non comme une source historique.

4. MAP1/R7 dossiers0111 et0144, audit MADAGASCAR-01-AUDIT, ancienne bibliographie Ellis2007 et notice Larousse : pistes et reçus conservés ; aucun propriétaire ancien ou catalogue non consulté utilisé comme baseline. Ellis intégral non lu ; aucun découpage1776 dérivé du seul titre1715–1750. La notice Larousse comporte une chronologie incohérente et n'a pas servi à attribuer un souverain. BASELINE.json/APPLY_BEFORE.json et apply_inputs enregistrent le vrai workspace.

Le modèle 1776 installé est une **interprétation politique bornée** de ces lectures et des provinces disponibles. Les champs basis de COUNTRY_PROFILES.json et historical_basis de PLAN.json rattachent chaque choix à ses passages. Le pays décentralisé CMO regroupe plusieurs cours faute de subdivision native : aucune union comorienne sous un sultan unique n'est affirmée.
''')
    doc('GEOGRAPHIC_LIMITATIONS.md','''# Limites géographiques et politiques

- Échelle minimale : provinces natives. Antananarivo, Ambohimanga et Ambohidratrimo sont des cours proches, plus proches que certains diamètres de provinces. Leurs secteurs central/nord/ouest sont distingués politiquement ; leurs collines exactes et un cadastre de1776 ne sont pas certifiés. Deux provinces par noyau retenues, pas de découpage pixel arbitraire.
- La carte28.1 situe populations et milieux ; elle ne trace pas les domaines royaux. Les rivières et interfaces orientent les enveloppes, tandis que le texte daté fonde leur statut. Les bords natifs restent irréguliers ; lissage reporté.
- La province x606CE0 englobe plusieurs îles Comores et îlots, rattachés statistiquement à SOUTH_MADAGASCAR. CMO est un agrégat de sultanats autonomes, de type moteur décentralisé, pas un État comorien unifié. Les subdivisions entre cours et une démographie comorienne propre restent à faire. L'audit antérieur est précisé sans effacer son reçu.
- Les noms/locators natifs, notamment les points nommés Majunga et Morondava, ne sont pas considérés comme des preuves de juridiction. Ils présentent des décalages par rapport à la géographie historique ; aucun hub/locator n'est déplacé ici. Une capitale moteur est une région possédée, pas une localisation palatiale validée.
- Boina/Menabe et centres betsileo : hégémonies, frontières exactes et degré de soumission des communautés périphériques ouverts. Seul tribut Antankarana–Boina installé ; pas d'annexion automatique depuis une influence commerciale. Les tributs sihanaka et merina ne sont pas généralisés à des pactes dont les parties/conditions1776 restent insuffisamment établies.
- Mahafaly, Bara, Antanosy, Antandroy, Betsimisaraka et Imamo/Andratsay agrègent des cours/communautés dont les frontières internes ne sont pas prétendues restaurées. Catégorie décentralisée marque l'absence de souveraineté unitaire du TAG, pas l'absence de rois locaux. Ikongo est distingué des autres Tanala.
- Antongil/Benyowsky, Sainte-Marie et Fort-Dauphin : activités/postes/prétentions européens ne sont pas assimilés à une administration uniforme d'un grand arrière-pays. Périmètres ponctuels non redessinés faute de preuve cadastrale ; aucune reprise française fictive de tout un État.
- Populations par culture/religion/statut et total conservés, ventilation technique aux provinces uniques. Densités réelles et rattachement des communautés ne sont pas des recensements vérifiés. Les cadres militaires hérités sont conservés, pas rééquilibrés historiquement ou économiquement.
''')
    doc('GROUPED_RUNTIME_ITEMS.md','''# Test africain groupé — MADAGASCAR-02

NOT_RUN ; aucun reçu humain ajouté, aucun test intermédiaire demandé.

Nouvelle partie1776 : vérifier Antananarivo/MAD restreint, Ambohimanga et Ambohidratrimo séparés, Boina/Menabe/Antankarana et lien tributaire, noyaux betsileo et de l'est/sud, autonomie des ensembles locaux, absence de possession merina aux Comores. Vérifier noms affichés, capitales possédées, portraits/drapeaux génériques et absence du modèle Ranavalona1836.

Contrôler technologies, lois réellement actives, construction/recrutement et ressources. L'armée MAD conserve ses nombres/types/services, les conscrits du sud sont référencés au nord ; observer mobilisation/manpower après partage sans présumer la viabilité. Observer marchés/budgets/ravitaillement/fronts, simuler puis sauvegarder/recharger. Témoins INTERIOR-01/Congo/Corne/Nil/Sahel, Amériques et SERG. Consigner uniquement version, durée et observations réellement testées ; pas de succès prérempli. Courbes irrégulières et hubs signalés dans GEOGRAPHIC_LIMITATIONS.md.
''')
    doc('USER_REQUEST.txt','''«Ok, corrige Marina.» puis «fini».
Autorisation : corriger le découpage merina/Madagascar confirmé par MADAGASCAR-01-AUDIT avant l'Afrique australe. Référence1janvier1776, royaumes organisés distingués des communautés autonomes ; aucune décentralisation uniforme. Périmètre sur les deux régions et la province native comorienne qu'elles incluent. Frontières et initialisation nécessaire, aucun nouveau personnage ni raffinement des bâtiments. Lissage reporté, test africain groupé, aucun reçu humain déduit de l'autorisation. Git/vanilla/suiviSERG non écrits, travaux concurrents préservés.
''')
    doc('REPRODUCE.md','''# Reproduction en lecture seule

`python tools/world1776_madagascar02.py --tech --validate`

`python tools/world1776_madagascar02_closeout.py --final`

Ne pas relancer --apply, --tracking ou le survey initial. Les entrées immédiates et reçus ne sont pas une ancienne baseline à réinstaller. Un changement concurrent doit être rapproché de son manifeste, jamais annulé pour satisfaire un ancien test. --evidence ne régénère que les bilans/cartes du lot ; aucun moteur lancé. Les reçus historiques restent des preuves de leurs versions passées.
''')
    h.dump('AUDIT_RESOLUTION.json',dict(source_audit='MADAGASCAR-01-AUDIT',M01='RESOLVED_NATIVE_SCALE:120transfers,MADretains2',M02='IMPLEMENTED_WITH_SPATIAL_APPROXIMATION:3nearbycourts',M03='PARTIAL_MODEL:royalcoresandpluralautonomousaggregates',M04='PARTIAL:Antankarana_Boina_pact_only_other_obligations_uncertain',historical_full_closure=False,human_validated=False))

def tracking():
    assert not (LOT/'TRACKING_PATCHES.json').exists(),'Tracking already updated.'
    hashes={n:h.b.a.sha(WORLD/n) for n in TRACK}
    for n in TRACK:
        dest=LOT/'tracking_inputs'/n;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(WORLD/n,dest)
    data=read(WORLD/'ROADMAP_STATE.json');assert not any(r['id']=='MADAGASCAR-02' for r in data['lots'])
    for phase in data['phases']:
        for region in phase['subregions']:
            if region['id']!='P3-09':continue
            for k,c in region['criteria'].items():
                if c['status'] in ['STATIC_VERIFIED','USER_VALIDATED']:continue
                if k!='V':c.update(status='PARTIAL',evidence='MADAGASCAR-02/REPORT.md',remaining='Noyaux sur cellules natives installés ; cadastre, démographie historique, représentation politique fine et moteur non clos. Aucun point entier.')
                else:c.update(evidence='MADAGASCAR-02/GROUPED_RUNTIME_ITEMS.md')
        count=sum(c['status']=='STATIC_VERIFIED' for r in phase['subregions'] for c in r['criteria'].values());phase['progress'].update(technical_verified=count,technical_percent=float((Decimal(count)*100/Decimal(phase['progress']['criteria_total'])).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)))
    total=sum(p['progress']['technical_verified'] for p in data['phases']);assert total==10 and data['progress']['criteria_total']==320
    data['progress'].update(technical_verified=10,technical_percent=3.13)
    for row in data['lots']:
        if row['id']=='MADAGASCAR-01-AUDIT':row['followup_resolution']='MADAGASCAR-02/AUDIT_RESOLUTION.json'
    data['lots'].append(dict(id='MADAGASCAR-02',date='2026-10-28',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',existing_files_modified=5,new_files=33,new_tags=26,reviewed_new_profiles=26,native_RGBs_transferred=120,new_RGBs=0,pixels_recolored=0,world_population_delta=0,receipt='MADAGASCAR-02/FILES_DELIVERED.json',credited_criteria=[],runtime='NOT_RUN'))
    data['steering_history'].append(data['current_steering']);data['current_steering']=dict(date='2026-10-28',authority='MADAGASCAR-02/USER_REQUEST.txt',last_lot='MADAGASCAR-02',scope='Madagascar political correction installed before southern Africa',next_pass='Southern Africa and Dutch/VOC settlements, from current workspace',cosmetic_smoothing_deferred=True,autonomous_subjects_authorized=True,runtime_validation_timing='GROUPED_AFRICA',intermediate_player_tests_requested=False,full_V_credit=False)
    entry='''\n\n## MADAGASCAR-02 —28octobre2026\n\nCorrection autorisée après l’audit :120RGB natifs réattribués,2conservés par MAD/Antananarivo ;26TAG nouveaux, trois noyaux merina distincts et pouvoirs royaux/autonomes différenciés. Une province native couvre les Comores : agrégat autonome séparé de MAD, sans union moderne affirmée. Un lien tributaire Antankarana–Boina, aucune annexion des autres tributaires incertains.5fichiers existants ciblés+33ajouts ;26profilsPASS_STATIC_ONLY,311contrôles statiques. Populations/cohortes/armées conservées, référence conscrite déplacée vers le nord encore possédé ; modèle de personnage1836 neutralisé sans nouveau personnage. Rapports/sources/limites MADAGASCAR-02/REPORT.md. Aucun pixel/ressource/hub/recette commune/Git/vanilla/suiviSERG écrit. Test africain groupéNOT_RUN, aucun point ou reçu humain nouveau ; WORLD10/320(3,13%). Suite australe/VOC non lancée ici.\n'''
    assert all(h.b.a.sha(WORLD/n)==v for n,v in hashes.items())
    write(WORLD/'ROADMAP_STATE.json',data)
    for n in ['ROADMAP.md','PROGRESS_HISTORY.md']:h.save(WORLD/n,h.raw(WORLD/n).rstrip()+entry)
    h.save(WORLD/'BLOCKERS.md',h.raw(WORLD/'BLOCKERS.md').rstrip()+'''\n\n## MADAGASCAR-02 — limites après correction\n\nLes attributions unifiées de l’audit sont remplacées par les noyaux documentés dans MADAGASCAR-02 ; ses anciens reçus restent historiques. Courbes natives, collines royales plus petites que les provinces, hubs natifs mal placés et frontières internes des agrégats non clos. CMO reste un agrégat de cours insulaires, pas un royaume centralisé moderne. Tributs restants, densités, manpower/budgets, capitales/lois effectives et simulation/sauvegarde à vérifier au test africain groupé. Aucun point entier ni reçu humain.\n''')
    h.save(WORLD/'OWNERSHIP_BOUNDARIES.md',h.raw(WORLD/'OWNERSHIP_BOUNDARIES.md').rstrip()+'''\n\n## MADAGASCAR-02 — périmètre installé\n\nSeuls deux nœuds NORTH/SOUTH_MADAGASCAR des états et POP ; c:MAD de l’histoire nationale et militaire (une référence conscrite), MAD des noms dynamiques.26nouveauxTAG, définitions/effets/loi propres, lien BOI→ATK, FR/EN et surcharge native de personnage MAD. Aucun niveau bâti ni PM ni pixel/terrain/ressource/locator modifié. Liste RGB PLAN.json ; entrées immédiates apply_inputs/ ; FILES_DELIVERED.json référence finale. Autres pays des fichiers partagés, WORLD antérieur, SERG, TECH/ECON et Amériques conservés sans retour à une baseline.\n''')
    h.save(WORLD/'NEXT_ACTION.md','''# Prochaine action — après MADAGASCAR-02\n\nCorrection Madagascar installée sur demande directe. Lire MADAGASCAR-02/REPORT.md, SOURCES.md, GEOGRAPHIC_LIMITATIONS.md, PLAN.json, AUDIT_RESOLUTION.json, VALIDATION.json, TECH_NON_REGRESSION.json et FILES_DELIVERED.json. Les cours proches et les agrégats locaux ne sont pas des frontières cadastrales certifiées ; les reçus de l’audit restent historiques.\n\nSuite demandée : Afrique australe et établissements néerlandais/VOC, dans une passe depuis le workspace courant. Aucun autre secteur lancé ici. Préserver Madagascar, INTERIOR-01, Congo/Corne/Nil/Sahel/Maghreb/Balkans, SERG, TECH/ECON et Amériques. Frontières et initialisation nécessaire uniquement ; aucun flavor ou lissage cosmétique automatique.\n\nTest africain groupé, aucun test intermédiaire demandé, aucune validation humaine inventée. WORLD10/320(3,13%), aucun critère entier nouveau.\n''')
    concurrent=read(WORLD/'CONCURRENT_CHANGES.json');concurrent['MADAGASCAR-02']=dict(receipt='MADAGASCAR-02/CONCURRENT_CHANGES.json',existing_functional_files_modified=5,new_files=33,native_RGBs_transferred=120,new_RGBs=0,pixels_recolored=0,world_population_delta=0,Git_writes=0,vanilla_writes=0,SERG_writes=0,old_baseline_restored=False);write(WORLD/'CONCURRENT_CHANGES.json',concurrent)
    h.dump('TRACKING_PATCHES.json',[dict(file='docs/reports/map/WORLD_1776_CLOSURE/'+n,before=hashes[n],after=h.b.a.sha(WORLD/n)) for n in TRACK])

def final():
    rows=delivered();checks=[]
    def ck(k,v,d=None):checks.append(dict(check=k,passed=bool(v),detail=d))
    for rel,r in rows.items():ck('delivered_hash.'+rel,h.b.a.sha(ROOT/rel)==r['after'])
    h.dump('FILES_DELIVERED.json',list(rows.values()));ck('38_functional_files',len(rows)==38)
    ck('territorial_static_pass',h.load('VALIDATION.json')['status']=='PASS')
    for r in h.load('STARTING_TECH_NEW_COUNTRIES.json'):ck('profile.'+r['TAG'],r['status']=='PASS_STATIC_ONLY')
    for r in h.load('TECH_NON_REGRESSION.json')['existing_country_comparison']:ck('no_new_P0_P1.'+r['TAG'],not r['introduced'])
    before={r['TAG']:r for r in h.load('STARTING_TECH_BEFORE.json')}
    for r in h.load('STARTING_TECH_EXISTING_AFTER.json'):ck('existing_knowledge_preserved.'+r['TAG'],r['technologies']==before[r['TAG']]['technologies'])
    old_army=h.raw(LOT/'apply_inputs'/h.ARMY);new_army=h.raw(ROOT/h.ARMY)
    def signature(text):
        n=h.b.one(text,'c:MAD')
        return Counter((u.one('type'),u.one('service_type'),u.one('count')) for u in h.b.walk([n]) if u.key=='combat_unit')
    ck('army_counts_types_services_conserved',signature(old_army)==signature(new_army))
    ck('no_recruitment_in_lost_south', 's:STATE_SOUTH_MADAGASCAR' not in new_army[h.b.one(new_army,'c:MAD').start:h.b.one(new_army,'c:MAD').end])
    char=h.load('CHARACTER_INPUT.json');node=h.b.one(h.raw(ROOT/char['file']),'c:MAD');ck('no_1836_ruler_template_installed',not node.children('create_character'))
    ck('no_blanket_MAD_owner',sum([s,'MAD'] in rows for rows in h.prior.m.state_owners(h.raw(ROOT/h.ST)).values() for s in ['STATE_NORTH_MADAGASCAR','STATE_SOUTH_MADAGASCAR'])==2)
    definitions=h.b.a.catalog('common/country_definitions');ck('royal_tiers_are_kingdoms',all(definitions[t][0].one('tier')=='kingdom' for t,r in h.p.COUNTRIES.items() if r['kind']=='unrecognized'))
    pop=h.load('POPULATION_LEDGER.json');ck('population_world',pop['delta']==0)
    for r in pop['state_totals']:ck('population_region.'+r['state'],r['before']==r['after'])
    ck('all_profiles_populated',all(any(r['TAG']==t and r['after']>0 for r in pop['countries']) for t in h.p.COUNTRIES))
    colors=[c for r in h.load('PLAN.json') for c in r['RGBs']];ck('120_unique_transfers',len(colors)==len(set(colors))==120)
    language=[];sets={}
    for lang in ['french','english']:
        allkeys=loc.entries(lang,replacement=True);own={k:v for k,v in allkeys.items() if any(path.name==h.PREFIX+'_l_'+lang+'.yml' for path,n,t in v)};sets[lang]=set(own)
        language.extend(dict(check=lang+'.'+k,passed=len(v)==1) for k,v in own.items())
    language.append(dict(check='same_bilingual_keys',passed=sets['french']==sets['english']))
    h.dump('LOCALIZATION_CHECK.json',dict(status='PASS' if all(r['passed'] for r in language) else 'FAIL',checks=language,render_runtime='NOT_RUN'));ck('localization',all(r['passed'] for r in language))
    certified={}
    outside=[r for r,v in h.load('APPLY_BEFORE.json')['protected'].items() if r not in rows and h.b.a.sha(ROOT/r)!=v and h.b.a.sha(ROOT/r)!=certified.get(r)]
    ck('outside_files_preserved_or_sourced_external',not outside,outside)
    data=read(WORLD/'ROADMAP_STATE.json');technical=[r['id']+'/'+k for phase in data['phases'] for r in phase['subregions'] for k,c in r['criteria'].items() if c['status']=='STATIC_VERIFIED'];human=[r['id']+'/'+k for phase in data['phases'] for r in phase['subregions'] for k,c in r['criteria'].items() if c['status']=='USER_VALIDATED']
    ck('canonical_progress',len(technical)==10 and not human and data['progress']['technical_verified']==10 and data['progress']['criteria_total']==320)
    h.dump('PROGRESS_CALCULATION.json',dict(credited=technical,user_validated=human,numerator=10,denominator=320,percent=3.13,newly_credited=[],partial_regions_receive_no_credit=True))
    needed=['REPORT.md','SOURCES.md','PLAN.json','GEOGRAPHIC_CROSSWALK.json','POPULATION_LEDGER.json','POPULATION_BEFORE_AFTER.csv','COUNTRY_PROFILES.json','STARTING_TECH_NEW_COUNTRIES.json','STARTING_TECH_EXISTING_AFTER.json','TECH_NON_REGRESSION.json','VALIDATION.json','CONCURRENT_CHANGES.json','LOCALIZATION_CHECK.json','BEFORE.png','AFTER.png','GROUPED_RUNTIME_ITEMS.md','FILES_DELIVERED.json','TRACKING_PATCHES.json','PROGRESS_CALCULATION.json','AUDIT_RESOLUTION.json','GEOGRAPHIC_LIMITATIONS.md','USER_REQUEST.txt','REPRODUCE.md','FORMAT_PRESERVATION.json','ROYAL_TIER_REPAIR.json']
    for n in needed:ck('evidence.'+n,(LOT/n).is_file())
    result=dict(status='PASS' if all(r['passed'] for r in checks) else 'FAIL',passed=sum(r['passed'] for r in checks),total=len(checks),checks=checks,automated_engine_test=False,human_validated=False);h.dump('DELIVERY_VALIDATION.json',result)
    files=[ROOT/r for r in rows]+[LOT/n for n in needed]+[LOT/'DELIVERY_VALIDATION.json']+[WORLD/n for n in TRACK]+[ROOT/'tools'/('world1776_madagascar02'+s+'.py') for s in ['', '_plan','_inspect','_closeout']]+[p for p in (LOT/'sources').iterdir() if p.is_file()]
    h.dump('DELIVERY_MANIFEST.json',{p.relative_to(ROOT).as_posix():h.b.a.sha(p) for p in files})
    print('Delivery',result['status'],result['passed'],'/',result['total']);print('FAIL',[r for r in checks if not r['passed']]);return result['status']=='PASS'

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    for k in ['evidence','reports','tracking','final']:parser.add_argument('--'+k,action='store_true')
    args=parser.parse_args()
    if args.evidence:evidence()
    if args.reports:reports()
    if args.tracking:tracking()
    if args.final:raise SystemExit(0 if final() else 1)
