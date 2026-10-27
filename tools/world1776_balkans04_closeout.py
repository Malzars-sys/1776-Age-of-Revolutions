"""B04 documentary delivery and additive WORLD tracking. No gameplay/SERG writes."""
import ast
import json
from pathlib import Path
import world1776_balkans04 as b


def main():
    validation=b.load('VALIDATION.json');assert validation['status']=='PASS'
    base=b.load('APPLY_BASELINE.json');ledger=b.load('POPULATION_LEDGER.json');tech=b.load('STARTING_TECH_CHECK.json')
    count=validation['total'];protected=len(base['protected']);serg=len(base['SERG_proofs']);prior=len(base['prior_proofs'])
    serg_changes=len(b.load('CONCURRENT_CHANGES.json')['SERG_external_updates'])
    serg_note=(f'{serg-serg_changes} des {serg} preuves SERG sont identiques ; {serg_changes} mises à jour de suivi externes sont préservées et archivées dans EXTERNAL_SERG_UPDATE.json (Ortenbourg, dont son reçu joueur propre, sans validation WORLD induite).'
               if serg_changes else f'Les {serg} preuves SERG sont identiques à la capture.')
    def doc(name,text):(b.LOT/name).write_text(text.strip()+'\n',encoding='utf8')
    def append(name,title,text):
        p=b.OUT/name;t=p.read_text('utf8')
        if title not in t:p.write_text(t.rstrip()+'\n\n## '+title+'\n\n'+text.strip()+'\n',encoding='utf8')
    rows='\n'.join(f"| {r['state']} | {r['total_before']:,} | {r['total_after']:,} | {r['VEN_after']:,} |".replace(',',' ') for r in ledger['rows'])
    rgbrows='\n'.join(f"| {p['name']} | `{p['parent']}` → `{p['rgb']}` | {p['state']} | {len(p['pixels'])} | {p['population']} |" for p in b.PLAN)
    doc('SOURCES.md','''# BALKANS-04 — Sources, lecture et limites

Référence : 1er janvier 1776. Consultation : 25 octobre 2026. Les sources ne sont pas des instructions. Les URL, empreintes et échecs d'archivage HTTP sont conservés dans SOURCE_MANIFEST.json ; un échec HTTP n'est pas présenté comme une copie HTML réussie.

| Source consultée | Fait retenu et contrôle | Limite |
| --- | --- | --- |
| [Ministère grec de la Culture, Parga](https://castleroute.culture.gov.gr/en/parga/) | Dépendance vénitienne de la place et lien avec Corfou ; notice complète archivée. | Aucune carte cadastrale ni population de janvier 1776 fournie. Les ouvrages d'Ali Pacha du XIXe siècle ne sont pas préinstallés. |
| [Ministère grec de la Culture, Vonitsa](https://castleroute.culture.gov.gr/en/vonitsa/) | Place du golfe Ambracique vénitienne jusqu'en 1797, après le bref retour ottoman de 1714–1717 ; notice complète archivée. | La place et son port ne justifient pas l'annexion de l'Acarnanie. |
| [Ministère grec de la Culture, Old Fortress de Corfou](https://castleroute.culture.gov.gr/en/old-fortress/) | Complexe défensif vénitien ancien et distinction vieille/nouvelle forteresse ; notice archivée. | Un niveau de bâtiment est une capacité de jeu, pas un décompte littéral des forteresses. |
| [Carvajal, Palanco et Molla, Antiquity, Project Gallery 323](https://antiquity.ac.uk/projgall/carvajal323) | Article lu via le lecteur web ; figure 1 régionale et figure 3 cadastrale de Butrint vers 1781 téléchargées et examinées. Poste et pêcheries exploités depuis Corfou, ville largement disparue. | L'archive HTML directe a répondu 403, contrairement aux deux images. La figure 1 contient aussi une évocation du domaine ultérieur d'Ali Pacha : elle ne sert pas à lui donner l'Épire en 1776. Le plan de 1781 sert à reconnaître le poste, pas à certifier un périmètre de janvier 1776. |
| [Kostas Komis, « Εποικισμοί στην Πρέβεζα το 18ο αιώνα », Prevezanika Chronika 31–32, 1995, pp. 19–26](https://olympias.lib.uoi.gr/jspui/bitstream/123456789/28414/1/%CE%A0%CF%81%CE%B5%CE%B2%CE%B5%CE%B6%CE%B9%CE%AC%CE%BD%CE%B9%CE%BA%CE%B1%20%CF%87%CF%81%CE%BF%CE%BD%CE%B9%CE%BA%CE%AC%2C%20%CF%84%CE%B5%CF%8D%CF%87%CE%BF%CF%82%2031-32-1995.pdf) | PDF numérisé archivé, sommaire et pp. 22–23 rendus puis lus visuellement : recensement situé vers 1780, 390 ménages et environ 1 700 personnes ; références aux archives de Leucade et au provveditore. PDF p. 24 = imprimé p. 23. | Ce n'est pas un recensement certifié du 1er janvier 1776 ni de toute la juridiction rurale. L'OCR local est absent ; les images, non une extraction textuelle vide, ont été examinées. |
| [Ancien site de la municipalité de Kythira, histoire](https://kythira.gr/oldsite/pages/culture/history_3.htm) | Notice grecque archivée ; continuité vénitienne après 1715–1718 et jusqu'en 1797. | Les présentations de longue durée simplifient les épisodes médiévaux ; seule la période pertinente est retenue. |
| [Kythera.gr, History](https://www.kythera.gr/en/history/) | Notice archivée : ordre de grandeur de 7 500 habitants à la fin de la période vénitienne. | Portail patrimonial, pas registre démographique daté de 1776 ; chiffre utilisé comme calibration explicitement signalée. |
| [Kyriaco Nikias, Legal Sources from the Venetian East, 2023](https://rg.lhlt.mpg.de/index.php/rg/article/download/2051/2300?inline=1) | Revue scientifique archivée ; compétences des conseils locaux, bailo, provveditori et reggimenti. | Ce n'est ni un atlas des limites ni une liste vérifiée des titulaires de janvier 1776. |

Les anciennes recommandations MAP1, leurs sources proposées et les preuves B01/B02/B03 ont été confrontées aux fichiers actuels. La notice CDC sur les mesures sanitaires a été consultée comme contexte ; son téléchargement direct bloqué n'est pas utilisé comme preuve de frontières et aucun bonus sanitaire n'est ajouté.

Les coordonnées géographiques de diagnostic sont approximatives. L'hypothèse Miller native, avec décalage visuel local, n'est pas un système géodésique certifié. Les quatre postes sont des noyaux politiques côtiers ancrés dans les lieux attestés ; aucune frontière d'arrière-pays n'est extrapolée. Cérigo est identifiée par sa composante insulaire préexistante complète, séparée du continent.
''')
    doc('REPORT.md',f'''# BALKANS-04 — Possessions ioniennes et places de l'Épire

Livraison : 25 octobre 2026. Référence : 1er janvier 1776.
Statut : IMPLEMENTED_STATIC_VERIFIED_WITH_HISTORICAL_OBLIGATIONS. Moteur : NOT_RUN. Aucune validation joueur WORLD nouvelle.

## Corrections installées

Les quatre postes continentaux sont distingués de leur arrière-pays ottoman et attribués à Venise. Cérigo/Cythère est également rendue à Venise : son île était dessinée séparément, mais rattachée à TUR. Les deux RGB ioniens déjà vénitiens — Corfou et le groupe natif Leucade/Céphalonie/Zante — restent identiques.

| Possession | Parent et RGB nouveau | Région native | Pixels transférés | POPs réaffectées |
| --- | --- | --- | ---: | ---: |
{rgbrows}

Total : **5 RGB nouveaux, 41 pixels terrestres** (8 pour les postes, 33 pour Cérigo), zéro terre ou côte créée, zéro TAG nouveau. Le continent du parent péloponnésien et son petit îlot oriental non identifié restent ottomans. Les terrains sont hérités des parents. Les quatre noyaux de deux pixels sont des approximations politiques, pas des frontières cadastrales.

Une revue insulaire a permis d'ajouter Cérigo au lot après l'installation des quatre postes. L'extension a utilisé les versions courantes et leurs reçus : KYTHERA_EXTENSION.json. Aucun fichier complet n'a été restauré depuis une ancienne baseline. Cérigo reste dans la région native STATE_PELOPONNESE ; aucun découpage administratif régional ni hub ottoman n'est déplacé.

## Démographie

**13 700 habitants** sont réaffectés des pools grecs TUR vers VEN. Les cultures, religions implicites/explicites, professions et tous les autres pools sont conservés. Monde : **834 936 539 → 834 936 539**, variation nulle.

| Région | Total avant | Total après | Population VEN ajoutée |
| --- | ---: | ---: | ---: |
{rows}

L'effectif de Prévéza reprend l'ordre de grandeur d'un recensement situé vers 1780, rendu et vérifié dans Komis. Les 7 500 de Cérigo reprennent une indication de fin de période vénitienne ; les autres valeurs sont des calibrations modestes. Aucun de ces chiffres n'est présenté comme un recensement exact de janvier 1776. Butrinto désigne le poste et son environnement de pêcheries ; aucune grande ville repeuplée n'est inventée. Voir POPULATION_LEDGER.json et SOURCES.md.

## Institutions, bâtiments et technologies

Administration directe VEN, dans le cadre existant du Stato da Mar ; pas de nouvelle république ionienne, protectorat britannique ou pays autonome anachronique. Lois, souverain, diplomatie et formations militaires de Venise restent inchangés. Les compétences locales des conseils et provveditori sont documentées ; aucun titulaire de janvier non vérifié n'est inventé.

Quatre mouillages minimaux sont ajoutés, un par nouvelle portion VEN des régions natives, avec le PM existant pm_anchorage. Un niveau de fortification navale de base dans les Ioniennes représente le complexe corfiote. Il ajoute 1 000 emplois de garnison, les mouillages 400 emplois : **1 400 emplois de capacité**, non une embauche attestée. La fortification consomme 5 armes légères et 5 fer à plein emploi ; les mouillages n'ajoutent pas d'intrants. Les anciennes installations ioniennes et tous leurs PM restent identiques.

Les **27 technologies VEN** sont conservées et leurs prérequis fermés. Les bâtiments, groupes et PM sont résolus, leurs gates satisfaits ; scientific_fortification_siegecraft est déjà acquis. Aucun grant, graphe technologique, recette commune ou gate n'est modifié. Aucun nouveau bâtiment-type ou PM-type n'est créé.

## Limites historiques et moteur

Les ressources, terres arables et traits restent partagés selon les régions natives ; cette passe ne les répartit pas historiquement entre les petits postes et l'arrière-pays. Les hubs partagés et le placement des ports minoritaires, l'accès au marché, les qualifications, le budget et les effectifs effectifs restent à vérifier au test groupé. La fortification corfiote produit des effets à l'échelle de la région ionienne du moteur, pas un périmètre de siège cadastral.

Ithaque n'est pas distinguée proprement de la géométrie céphalonienne. Paxos, les Strophades, Anticythère et l'îlot oriental du parent péloponnésien demandent une identification plus sûre ; aucune terre nouvelle ou attribution arbitraire n'est créée pour les forcer. Les limites exactes des juridictions et les minorités ne sont pas closes. Les obligations B01/B02/B03, dont Lastovo, Krka partagé, recteur ragusain, fiscalité monténégrine et budgets, demeurent ouvertes.

## Vérification, concurrence et suivi

**{count}/{count} contrôles statiques réussis**, notamment conservation de tous les anciens propriétaires, cellules hors masques, POPs mondiales et profils culturels/religieux, ressources et hubs hors listes de provinces, prérequis et PM, pixels ragusains, Cyclades et huit reçus fonctionnels B03. Les résultats ne valent pas validation moteur.

Les {protected} fichiers fonctionnels protégés hors lot et {prior} preuves des trois lots WORLD précédents sont identiques à la capture d'application. {serg_note} TECH-R1/R2/R3, ECON-ALLOYS/quincaillerie et les installations concurrentes SERG sont préservés. Cinq fichiers partagés sont modifiés dans les seuls scopes annoncés ; un historique de bâtiments spécifique est nouveau. Aucun suivi SERG, fichier vanilla ou état Git n'est écrit par cette tâche.

Progression d'entrée vérifiée : 7/80 Balkans et 7/320 WORLD. Seuls T et S de P1-03 gagnent du crédit : **9/80 Balkans (11,25 %) et 9/320 WORLD (2,81 %)**. O/I/D/E/R restent partiels ; V non commencé. Aucune région close ni attestation humaine créée.

Prochaine passe : **BALKANS-05 — Albanie et Épire ottomanes**, en conservant les possessions vénitiennes restaurées. Rester dans les Balkans. Test joueur groupé uniquement à la fin du travail techniquement réalisable, puis confirmation explicite avant toute autre région.
''')
    doc('TEST_MATRIX.md',f'''# BALKANS-04 — Contrôles exécutés

Résultat propre : {count}/{count}, détails dans VALIDATION.json. Pas de moteur.

| Domaine | Vérification | Limite |
| --- | --- | --- |
| Mutations ciblées | Six fichiers fonctionnels reconstruits exactement ; extérieur des régions ciblées identique | Le parseur n'est pas le chargeur natif |
| Géométrie | 41 pixels autorisés, cinq RGB uniques, terrains hérités, deux pixels connexes par poste et île entière de 33 pixels | Huit pixels sont des noyaux politiques, pas un cadastre |
| Mer et arrière-pays | Tous les pixels anciens hors masques identiques, accès côtier vérifié, continent de Cérigo conservé | Navigation et rendu à tester |
| POPs | Totaux locaux/mondial et profils culture/religion/profession conservés, 13 700 réaffectés | Calibrations historiques signalées |
| Institutions | Aucun changement de loi, souverain, armée ou pacte ; VEN existant seulement | Titulaires locaux et autonomie fine non simulés |
| Économie et technologies | Quatre mouillages, un fort ; PM et gates résolus ; 27 technologies à prérequis fermés | Qualifications, marché, budget et hubs minoritaires non testés |
| Non-régression | Cyclades, pixels RAG/Neum/Sutorina, reçus B03 et archives précédentes ; {protected} fichiers protégés | Les autres mécaniques ne sont pas réauditées |
| SERG | {serg-serg_changes} preuves identiques et {serg_changes} mises à jour externes documentées ; ni écriture réservée ni suivi écrit par B04 | Aucun reçu joueur WORLD ajouté |

Commande de lecture reproductible : `python tools/world1776_balkans04.py --validate`. `--apply` et `--extend-kythera` sont des installations uniques et refusent un second passage. Le contrôle ne réécrit aucun ancien reçu B01/B02/B03.
''')
    doc('GROUPED_RUNTIME_ITEMS.md','''# B04 — Points pour le test balkanique final

Statut NOT_RUN ; aucune demande de test intermédiaire, aucune attestation.

À intégrer au protocole consolidé en fin de travaux balkaniques techniquement réalisables :

1. Nouvelle partie 1776 : quatre postes continentaux et Cérigo vénitiens ; arrière-pays ottoman, Corfou et autres îles inchangés.
2. Contrôler les quatre portions VEN des régions natives, leurs 13 700 habitants réaffectés et la population mondiale conservée.
3. Vérifier les quatre mouillages, leurs hubs minoritaires, le placement de la fortification ionienne et la navigation ; aucun hub ottoman n'a été déplacé dans les fichiers.
4. Observer embauche, qualifications, intrants du fort, marché et budget de Venise pendant un mois ; ne pas déduire la viabilité des seuls effectifs théoriques.
5. Sauvegarder/recharger et vérifier propriété, bâtiments, PM, populations et erreurs de chargement.
6. Joindre la revue des petites îles et les obligations B01/B02/B03 au même test ; aucune clôture historique des Ioniennes présumée.

Aucune autre région WORLD avant confirmation explicite du joueur sur le test balkanique groupé.
''')
    b.dump('GEOGRAPHIC_CROSSWALK.json',{'historical_date':'1776-01-01','posts':b.PLAN,'pixels':41,'new_RGBs':5,
        'coastline_changed':False,'territorial_precision':'FOUR_POLITICAL_COASTAL_CORES_PLUS_EXISTING_KYTHERA_ISLAND',
        'diagnostic_only':{'geographic_points':'Approximate WGS84 targets in PLAN; not surveyed coordinates.',
        'model':'tools/georeference/model.py native_miller_hypothesis + local visual Y shift about 5.5 px',
        'projection_certified':False,'certified_error_bound_px':None,
        'installation_basis':'Attested fixed coastal posts, source regional/cadastral images, existing native coastline; two-pixel political cores without inferred hinterland borders. Kythera uses its entire separate native component.'},
        'small_islands_unresolved':['Paxos','Ithaca separate geometry','Strophades','Antikythera','Eastern one-pixel islet of x0055D7'],
        'original_Ionian_RGBs_preserved':['x4B79CA','x405060'],'Kythera_selection':'KYTHERA_SELECTION.json'})
    b.dump('BUILDING_CAPACITY.json',{'new_anchorages':4,'anchorage_jobs_each':100,'Corfiot_fort_levels':1,'fort_jobs':1000,
        'total_new_capacity_jobs':1400,'fort_inputs_at_full_employment':{'small_arms':5,'iron':5},
        'existing_buildings_modified':False,'new_building_or_PM_types':False,'budget_or_hiring_simulated':False})
    state=json.loads((b.OUT/'ROADMAP_STATE.json').read_text('utf8'))
    first=not any(l['id']=='BALKANS-04' for l in state['lots'])
    score=sum(c['status']=='STATIC_VERIFIED' for p in state['phases'] for r in p['subregions'] for c in r['criteria'].values())
    assert score==(7 if first else 9)
    region=next(r for r in state['phases'][0]['subregions'] if r['id']=='P1-03')
    for k in ['O','I','D','E','R']:
        region['criteria'][k]={'status':'PARTIAL','evidence':'BALKANS-04/REPORT.md',
            'remaining':{'O':'Noyaux des postes approximatifs ; petites îles et limites des juridictions ouvertes.',
            'I':'Dépendance VEN confirmée ; offices locaux et titulaires de janvier non simulés.',
            'D':'Conservation vérifiée ; chiffres datés exacts et minorités non reconstitués.',
            'E':'Ressources/hubs régionaux partagés ; marché, qualifications et budget non testés.',
            'R':'Armées et pactes préservés ; garnisons historiques complètes et obligations locales non quantifiées.'}[k]}
    for k,path in [('T','STARTING_TECH_CHECK.json'),('S','VALIDATION.json')]:
        region['criteria'][k]={'status':'STATIC_VERIFIED','evidence':'BALKANS-04/'+path,'runtime':'NOT_RUN',
            'scope':'Installed four coastal cores, existing Kythera island and explicit starting assets only; no cadastral or regional historical closure.'}
    region['criteria']['V']={'status':'NOT_STARTED','evidence':'BALKANS-04/GROUPED_RUNTIME_ITEMS.md','test_timing':'END_OF_BALKANS'}
    if first:state['lots'].append({'id':'BALKANS-04','status':'IMPLEMENTED_STATIC_VERIFIED_WITH_HISTORICAL_OBLIGATIONS',
        'scope':['Four Venetian Epirote coastal posts','Existing Kythera island / Cerigo','Corfu defensive capacity'],
        'runtime':'NOT_RUN','test_timing':'END_OF_BALKANS','files_modified':6,'new_RGBs':5,'new_tags':0,
        'pixels_recolored':41,'people_transferred':13700,'world_population_delta':0,
        'receipt':'BALKANS-04/FILES_MODIFIED.json','protocol':'BALKANS-04/GROUPED_RUNTIME_ITEMS.md','historical_research_status':'REGION_INCOMPLETE'})
    for p in state['phases']:
        n=sum(c['status']=='STATIC_VERIFIED' for r in p['subregions'] for c in r['criteria'].values())
        p['progress']['technical_verified']=n;p['progress']['technical_percent']=round(100*n/p['progress']['criteria_total'],2)
    state['progress']['technical_verified']=sum(p['progress']['technical_verified'] for p in state['phases'])
    state['progress']['technical_percent']=round(100*state['progress']['technical_verified']/320,2)
    assert state['progress']['technical_verified']==9 and state['progress']['runtime_user_validated']==0
    (b.OUT/'ROADMAP_STATE.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    title='BALKANS-04 — 2026-10-25'
    append('ROADMAP.md',title,'Quatre noyaux de places vénitiennes et Cérigo restaurés : 5 RGB, 41 pixels terrestres, 13 700 POPs réaffectées, delta mondial nul. Quatre mouillages et un niveau de fortification corfiote, technologies existantes conservées. T/S seulement crédités : 9/80 Balkans (11,25 %), 9/320 WORLD (2,81 %), zéro validation joueur nouvelle. Rapport BALKANS-04/REPORT.md ; prochaine passe BALKANS-05 Albanie/Épire ottomanes, sans quitter les Balkans.')
    append('PROGRESS_HISTORY.md',title,f'Entrée recalculée : 7/80 et 7/320, aucun reçu humain WORLD nouveau. Installation de quatre noyaux côtiers (8 pixels), puis de la composante insulaire existante de Cérigo (33 pixels), sur versions courantes avec empreintes avant écriture. Cinq fichiers partagés, un nouvel historique de bâtiments, aucun TAG. 13 700 habitants grecs TUR→VEN par réaffectation ; monde 834 936 539 avant/après, autres cultures/religions/professions conservées.\n\nQuatre mouillages minimaux et un niveau de fortification corfiote ; 27 technologies VEN inchangées, gates/PM compatibles, aucune recette commune modifiée. {count}/{count} contrôles réussis, {protected} fichiers fonctionnels hors lot et {prior} preuves WORLD précédentes identiques. {serg_note} Aucun test moteur ni validation joueur WORLD ; aucun fichier vanilla/Git/SERG écrit par cette tâche.\n\n+2 critères uniquement T/S de P1-03 : 9/80 (11,25 %) et 9/320 (2,81 %). O/I/D/E/R partiels ; petites îles, limites fines, ressources/hubs partagés et économie ouverts. Prochaine action B05 Albanie et Épire ottomanes. Test joueur groupé en fin des travaux balkaniques techniquement réalisables ; aucune autre région avant confirmation explicite.')
    append('BLOCKERS.md',title,'Les quatre postes et Cérigo sont installés, sans annexion de leur arrière-pays. Restent les limites des juridictions et les noyaux côtiers approximatifs, les petites îles non identifiées sûrement, les titulaires locaux de janvier, les minorités, la démographie datée et les garnisons complètes. Les 1 700 de Prévéza sont un ordre de grandeur voisin de 1780, les 7 500 de Cérigo une indication de fin de période vénitienne ; les autres effectifs sont des calibrations.\n\nRégions natives partagées : ressources, terres arables, traits et hubs non redistribués. Placement des ports minoritaires, qualifications, marché et budget à contrôler lors du test balkanique groupé. Cérigo conserve sa région native STATE_PELOPONNESE. Aucune frontière, terre ou armée fictive n’est ajoutée pour masquer ces limites. Obligations B01/B02/B03 toujours ouvertes ; pas de test intermédiaire.')
    append('OWNERSHIP_BOUNDARIES.md',title,'Écriture réservée WORLD dans ce lot : Butrinto xE8D211 (parent x7BE071, ALBANIA), Parga xE8D212 et Prévéza xE8D213 (parent x8050E0, THESSALIA), Vonitsa xE8D214 (parent x518791, ATTICA), Cérigo xE8D215 (composante insulaire de x0055D7, PELOPONNESE). VEN reçoit cinq nouveaux RGB, 41 pixels ; tous les anciens RGB restent à leur propriétaire. Masques dans BALKANS-04/PIXEL_PATCH.json.\n\nLes POPs passent seulement des pools grecs TUR aux nouvelles portions VEN : 500 / 4 700 / 1 000 / 7 500 par région, total 13 700 sans variation mondiale. Hors listes de provinces, ressources, traits et hubs restent identiques. Quatre ports minimaux et un niveau de fortification dans les Ioniennes sont dans un historique nouveau ; aucun ancien PM, pays, loi ou armée n’est retouché.\n\nPatchs sur versions courantes, y compris l’extension insulaire après vérification des reçus ; aucune restauration d’ancienne baseline. Aucune écriture de territoire ou de suivi SERG, aucun chevauchement TECH/ECON. Les interfaces B01/B02/B03 restent protégées.')
    (b.OUT/'NEXT_ACTION.md').write_text('''# Prochaine passe WORLD — BALKANS-05

**Albanie et Épire ottomanes**, référence : 1er janvier 1776. B04 installé : voir BALKANS-04/REPORT.md et DELIVERY_CHECKS.json.

Reprendre les autorités et juridictions de Scutari et de l'Épire, leurs rapports avec la Porte, le contrôle effectif, les clans et les institutions locales. Dater chaque titulaire ; ne pas projeter le gouvernement ultérieur d'Ali Pacha sur janvier 1776. Sélectionner un sous-lot P0/P1 cohérent, indépendamment testable, à partir du workspace courant.

Conserver les quatre postes vénitiens, Cérigo et les îles ioniennes ; ne pas assimiler un poste à tout son arrière-pays. Respecter les interfaces SERG et les travaux TECH-R1/R2/R3 et ECON-ALLOYS/quincaillerie. Lire le suivi complet et les preuves récentes, vérifier empreintes et concurrence ; aucun retour à une baseline ancienne, aucune écriture Git/vanilla/SERG.

Obligations ouvertes B04 : petits archipels non identifiés sûrement, limites fines, titulaires locaux, démographie/minorités, ressources et hubs partagés, marché/budget. Les obligations B01/B02/B03 restent à reprendre avant clôture balkanique.

Progression : **9/80 Balkans (11,25 %) ; 9/320 WORLD (2,81 %) ; zéro nouvelle validation joueur.**

Achever les travaux balkaniques techniquement réalisables, puis préparer le protocole consolidé incluant B04/GROUPED_RUNTIME_ITEMS.md. Aucun test intermédiaire demandé. Ne passer à aucune autre région avant confirmation explicite du test balkanique groupé ; aucune attestation humaine fictive.
''',encoding='utf8')
    concurrent=json.loads((b.OUT/'CONCURRENT_CHANGES.json').read_text('utf8'))
    concurrent['BALKANS-04']={'receipt':'BALKANS-04/CONCURRENT_CHANGES.json','protected_gameplay_unchanged':protected,
        'SERG_proofs_unchanged':serg-serg_changes,'SERG_external_tracking_updates':serg_changes,
        'SERG_external_receipt':'BALKANS-04/EXTERNAL_SERG_UPDATE.json' if serg_changes else None,
        'prior_WORLD_proofs_unchanged':prior,'SERG_writes':0,'git_writes':0,'vanilla_writes':0,
        'existing_owners_changed':0,'new_RGBs':5,'pixels_recolored':41,'world_population_delta':0,'old_baseline_restored':False}
    (b.OUT/'CONCURRENT_CHANGES.json').write_text(json.dumps(concurrent,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    b.dump('PROGRESS_CALCULATION.json',{'entry':{'Balkans':7,'WORLD':7},'credited':['P1-03/T','P1-03/S'],
        'Balkans':state['phases'][0]['progress'],'WORLD':state['progress'],'human_attestations_created':0})
    # Delivery checks are distinct from the gameplay/static validator.
    checks=[]
    def check(k,v):checks.append({'check':k,'passed':bool(v)})
    check('static_validation_PASS',validation['status']=='PASS' and validation['passed']==validation['total'])
    receipt=b.load('FILES_MODIFIED.json');check('six_functional_files',len(receipt)==6)
    for e in receipt:check('current_receipt.'+e['file'],b.b.a.sha(b.ROOT/e['file'])==e['after'])
    check('world_population_conserved',ledger['world_before']==ledger['world_after']==834936539)
    check('13700_reallocated',ledger['politically_reallocated']==13700)
    check('41_pixels',sum(len(p['pixels']) for p in b.PLAN)==41)
    check('all_canonical_docs_present',all((b.OUT/n).exists() for n in ['ROADMAP.md','ROADMAP_STATE.json','NEXT_ACTION.md','BLOCKERS.md','PROGRESS_HISTORY.md','OWNERSHIP_BOUNDARIES.md','CONCURRENT_CHANGES.json']))
    check('nine_technical_criteria',sum(c['status']=='STATIC_VERIFIED' for p in state['phases'] for r in p['subregions'] for c in r['criteria'].values())==9)
    check('phase_gate_preserved',state['phase_transition_gate']['next_region_requires_explicit_user_confirmation'] and not state['phase_transition_gate']['partial_lot_tests_requested'])
    check('zero_player_validation',state['progress']['runtime_user_validated']==0)
    check('other_phases_not_started',all(p['status']=='NOT_STARTED' for p in state['phases'][1:]))
    for e in b.load('SOURCE_MANIFEST.json'):
        if 'sha256' in e:check('source_hash.'+e['file'],b.b.a.sha(b.LOT/e['file'])==e['sha256'])
    for name in ['world1776_balkans04.py','world1776_balkans04_closeout.py']:
        ast.parse((b.ROOT/'tools'/name).read_text('utf8'));check('python_syntax.'+name,True)
    delivery={'status':'PASS' if all(c['passed'] for c in checks) else 'FAIL','passed':sum(c['passed'] for c in checks),'total':len(checks),'checks':checks,'runtime':'NOT_RUN','human_attestations_created':0}
    b.dump('DELIVERY_CHECKS.json',delivery)
    manifest={'scope':'BALKANS-04','historical_date':'1776-01-01','status':'IMPLEMENTED_STATIC_VERIFIED_WITH_HISTORICAL_OBLIGATIONS',
        'runtime':'NOT_RUN','functional_files':receipt,'tools':{p.relative_to(b.ROOT).as_posix():b.b.a.sha(p) for p in (b.ROOT/'tools').glob('world1776_balkans04*.py')},
        'tracking':{n:b.b.a.sha(b.OUT/n) for n in ['ROADMAP.md','ROADMAP_STATE.json','NEXT_ACTION.md','BLOCKERS.md','PROGRESS_HISTORY.md','OWNERSHIP_BOUNDARIES.md','CONCURRENT_CHANGES.json']},
        'evidence':{p.relative_to(b.LOT).as_posix():b.b.a.sha(p) for p in b.LOT.rglob('*') if p.is_file() and p.name!='DELIVERY_MANIFEST.json'},
        'tests':{'static_passed':validation['passed'],'static_total':count,'delivery_passed':delivery['passed'],'delivery_total':delivery['total']},
        'progress':{'Balkans':'9/80','WORLD':'9/320','new_human_validation':0}}
    b.dump('DELIVERY_MANIFEST.json',manifest)
    print(json.dumps({k:v for k,v in delivery.items() if k!='checks'}));print([c for c in checks if not c['passed']])

if __name__=='__main__':main()
