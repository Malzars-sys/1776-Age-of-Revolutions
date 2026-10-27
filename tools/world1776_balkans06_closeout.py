"""B06 evidence and additive WORLD tracking; no gameplay or reserved writes."""
import ast
import json
import shutil
import world1776_balkans06 as b

TRACK=['ROADMAP.md','ROADMAP_STATE.json','NEXT_ACTION.md','BLOCKERS.md','PROGRESS_HISTORY.md','OWNERSHIP_BOUNDARIES.md','CONCURRENT_CHANGES.json']

def main():
    assert not (b.LOT/'DELIVERY_MANIFEST.json').exists(),'Preserve existing closeout.'
    validation=b.load('VALIDATION.json');assert validation['status']=='PASS'
    base=b.load('APPLY_BASELINE.json');receipts=b.load('FILES_MODIFIED.json');pop=b.load('POPULATION_LEDGER.json');tech=b.load('TECH_AFTER.json')[0]
    original={n:(b.OUT/n).read_bytes() for n in TRACK}
    for n,data in original.items():
        p=b.LOT/'closeout_inputs'/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
    def doc(name,text):(b.LOT/name).write_text(text.strip()+'\n',encoding='utf8')
    def append(name,title,text):
        assert (b.OUT/name).read_bytes()==original[name],name+' changed concurrently'
        (b.OUT/name).write_text(original[name].decode('utf8').rstrip()+'\n\n## '+title+'\n\n'+text.strip()+'\n',encoding='utf8')
    # Verify and archive only the external receipt needed to explain the changed world baseline.
    external_root=b.ROOT/'docs/reports/map/NORTH_AMERICA_1776/HBC-06'
    hbc=json.loads((external_root/'FILES_MODIFIED.json').read_text('utf8'))['runtime_sha256']
    assert all(b.b.a.sha(b.ROOT/r)==h for r,h in hbc.items())
    for name in ['REPORT.md','FILES_MODIFIED.json','SOURCES.md']:
        dest=b.LOT/'external_reference/HBC-06'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(external_root/name,dest)
    older=json.loads((b.OUT/'BALKANS-05/BASELINE.json').read_text('utf8'))
    owner_delta=[{'RGB':r,'previous':v,'entry_B06':base['inventory']['owners'].get(r)} for r,v in older['inventory']['owners'].items() if base['inventory']['owners'].get(r)!=v]
    b.dump('EXTERNAL_HBC06_OBSERVATION.json',{'scope':'Observed independent work before B06 entry, not a WORLD phase-5 installation or approval','source_receipt':'external_reference/HBC-06/FILES_MODIFIED.json','all_nine_runtime_hashes_match':True,'previous_world':older['inventory']['world_population'],'entry_world':base['inventory']['world_population'],'external_world_delta':base['inventory']['world_population']-older['inventory']['world_population'],'owner_entry_differences':owner_delta,'human_validation_transferred':False,'other_task_authorship_claimed':False})
    sources=b.load('SOURCE_MANIFEST.json')
    sources.append({'url':'https://www.academia.edu/130311996/Local_Patriots_and_Ecumenical_Ottomans_The_Orthodox_Patriarchate_of_Constantinople_in_the_Ottoman_Configuration_of_Power_1768_1828','accessed':'2026-10-26','method':'Public author-uploaded transcription, linked from author profile','pages_consulted':'80–85; dated Mani ferman in note 538, printed p.83','original_PDF_archived':False,'notes':'SOURCES.md; McGill repository returned 403; original BOA document not independently inspected'})
    b.dump('SOURCE_MANIFEST.json',sources)
    doc('SOURCES.md','''# B06 — Sources et décisions datées

Référence : 1er janvier 1776. Consultation : 26 octobre 2026. Aucun catalogue non lu n’est utilisé comme preuve. Copies, empreintes et échecs HTTP/DNS : SOURCE_MANIFEST.json.

| Source réellement consultée | Localisation et fait retenu | Limite |
| --- | --- | --- |
| [Özer Küpeli, « Bir Voyvodanın Serencamı: Atina Voyvodası Haseki Ali Ağa », *Osmanlı İdaresinde Balkanlar*, I, 2020, pp.461–483](https://isamveri.org/pdfsbv/D292434/2020/2020_KUPELO.pdf) | PDF archivé, notamment pp.464–465 (PDF 6–7) : origine à Burdur, première voïvodie 1775–1776, examen critique de Benizelos et Skouzes ; références COA Cevdet Maliye 268/10972 et 268/10985. P.465 rendue et relue visuellement. | Registres originaux non consultés. L’auteur signale l’incertitude du jour d’arrivée et conteste le récit amoureux avec Esma ; aucune telle relation n’est installée. Achat de malikâne et délégation de voïvode ne sont pas confondus. |
| [Yusuf Ziya Karabıçak, *Local Patriots and Ecumenical Ottomans*, thèse McGill/EHESS, 2020](https://www.academia.edu/130311996/Local_Patriots_and_Ecumenical_Ottomans_The_Orthodox_Patriarchate_of_Constantinople_in_the_Ottoman_Configuration_of_Power_1768_1828) | Transcription publique de l’auteur, pp.80–85 : négociations locales, effets de la révolte et règlement du Magne ; note 538 : copie BOA A.DVN 2370/11 du 7 mars 1804 d’un ferman daté du 1–11 janvier 1777. | PDF original non archivé ; dépôt McGill bloqué. L’original BOA n’est pas consulté directement. Le règlement de Koutifaris ne justifie pas de le préinstaller le 1er janvier 1776 ; l’autonomie antérieure des clans reste à représenter plus finement. |
| [Ministère grec de la Culture, Palamidi](https://castleroute.culture.gov.gr/en/palamidi/) | Notice HTML archivée : construction commencée en 1711, reprise ottomane de Nauplie en 1715, place maintenue durant la seconde période ottomane. | Pas de nombre de soldats ou de pièces en 1776 ; un niveau régional est une calibration de capacité, pas un recensement des bastions. |
| [Ministère grec de la Culture, Antirrio](https://castleroute.culture.gov.gr/en/antirrio/) | Notice HTML archivée : ouvrage contrôlant l’entrée du golfe avec Rio, retour ottoman en 1701 et maintien jusqu’en 1829. | Les travaux tardifs apparentés à ceux d’Ali Pacha ne sont pas préinstallés en 1776. |
| [Ministère grec de la Culture, Nafpaktos](https://castleroute.culture.gov.gr/en/nafpaktos/) | Notice HTML archivée : retour ottoman après Karlowitz, arsenal/port fortifié, déclin commercial au XVIIIe siècle. | Aucun essor urbain moderne ni population nouvelle déduit de l’ancien rôle naval. |

La recherche Anastasopoulos 2007 a fourni une piste sur les bandes albanaises mais son PDF n’a pas été récupéré : échec conservé, aucune lecture intégrale prétendue. William Miller, 1907, et les résumés donnant 1776 pour les beys du Magne sont des repères contradictoires ; le ferman daté rapporté par Karabıçak prévaut pour éviter une rétroprojection. Aucun décompte militaire de bandes n’est transformé en armée ottomane loyale.

Les recommandations MAP1 R2-0065/0075/0077 ont été relues : simples revues macroscopiques, pas des frontières certifiées. Le bitmap actuel a été examiné pour le Péloponnèse ; les RGB agrégés ne suffisent pas à tracer la juridiction du Magne. Aucun découpage politique arbitraire n’est installé.

## Choix d’implémentation

Deux capacités côtières agrégées utilisent le bâtiment/PM déjà communs : ATTICA pour Lépante–Antirrio, PELOPONNESE pour Nauplie/Palamidi. Le moteur les place sur les hubs natifs et applique ses effets régionaux : ils ne garantissent ni maillage à chaque site ni verrou naval de toutes les passes réelles. La garnison de 1 000 emplois par niveau et ses intrants viennent du PM existant, pas d’un chiffre de source.

Haseki est un civil dans le vivier de personnages TUR, avec un trait d’office descriptif sans bonus ; le jeu n’acquiert pas de système de gouverneurs provinciaux par cet ajout. Âge 45 : calibration technique d’adulte, naissance inconnue. Groupe des propriétaires et idéologie traditionaliste : interprétations qualitatives. Aucun commandement militaire, leadership national ou relation romanesque ne lui est attribué.
''')
    protected=len(base['gameplay']);prior=len(base['prior_WORLD_proofs']);serg=len(base['SERG_proofs']);count=validation['total']
    doc('REPORT.md',f'''# BALKANS-06 — Grèce continentale et Péloponnèse

26 octobre 2026. Départ : 1er janvier 1776. Statut IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION ; moteur NOT_RUN ; aucune nouvelle validation joueur. **Crète exclue de l’autorisation actuelle** ; P1-06 reste incomplet.

## Corrections installées

- **Hacı Ali Haseki**, voïvode d’Athènes dans sa première période 1775–1776, entre dans le vivier civil ottoman. Culture turque, sunnite, groupe des propriétaires, idéologie traditionaliste. Le trait « Voïvode d’Athènes » est descriptif et sans bonus. Pas de général, souverain ou chef national de groupe ajouté ; les titulaires existants restent identiques. Âge technique 45, non une naissance établie. La source situe sa naissance à Burdur : aucun home_region athénien n’est inféré de sa fonction, et sa région natale de jeu n’est pas forcée sans correspondance géographique vérifiée.
- **Un niveau de fortification côtière TUR en ATTICA**, représentant la capacité régionale des places de Lépante–Antirrio.
- **Un niveau en PELOPONNESE**, représentant Nauplie/Palamidi. Les installations attestées existent avant 1776 ; les murailles athéniennes de 1778 et les ouvrages tardifs d’Ali Pacha ne sont pas ajoutés.

Cinq fichiers propres nouveaux, **aucun fichier fonctionnel partagé retouché**. Aucun pays, traité, loi, recette commune, technologie ou PM-type créé. Les bandes armées d’après-Orlov ne sont pas assimilées à des formations régulières nouvelles. Les forces ottomanes, leurs réserves et les maisons B05 restent intégralement identiques.

## Cellules et populations

**Zéro RGB/pixel/propriétaire modifié, zéro nouveau TAG, zéro transfert de POPs.** Les cinq RGB TUR du Péloponnèse (`x0055D7`, `x43409D`, `x61E57E`, `xBA3449`, `xC0D060`) et tous les RGB d’ATTICA/THESSALIA restent identiques. Cérigo `xE8D215`, Vonitsa `xE8D214`, Parga/Prévéza `xE8D212/xE8D213`, Butrinto `xE8D211`, les Ioniennes, MON et RAG sont conservés. Hubs, locators, terrains, ressources et arable ne sont pas écrits.

| Portion technique | Avant | Après |
| --- | ---: | ---: |
| ATTICA TUR / VEN | 541 293 / 1 000 | 541 293 / 1 000 |
| PELOPONNESE TUR / VEN | 181 316 / 7 500 | 181 316 / 7 500 |
| THESSALIA TUR / VEN | 958 024 / 4 700 | 958 024 / 4 700 |
| Monde | 837 336 539 | 837 336 539 |

Le total mondial d’entrée diffère de l’ancien reçu B05 (834 936 539) de **+2 400 000** : ajout externe du chantier HBC-06 en Amérique du Nord, documenté avant cette passe. Son reçu et les neuf empreintes fonctionnelles ont été vérifiés et archivés ici ; aucune approbation historique ou validation humaine n’en est déduite. Les changements d’attribution extérieurs sont observés séparément dans EXTERNAL_HBC06_OBSERVATION.json. Aucune compensation démographique hors lot.

Les totaux locaux sont ceux du scénario actuel, non des recensements certifiés de 1776. Les musulmans, autres minorités, réfugiés et pertes d’après-Orlov ne sont pas réestimés arbitrairement. L’autonomie des clans du Magne n’est pas niée par le maintien provisoire du cadre TUR : ses limites, obligations et institutions doivent encore être distinguées. Le règlement de Koutifaris cité par la thèse date de janvier 1777 et n’est pas appliqué au lancement.

## Capacités, technologies et limites du moteur

PM de base existant pour les deux niveaux : **1 800 emplois de soldats et 200 d’officiers**, 10 armes légères et 10 fer par semaine à plein emploi au total. Il s’agit de capacités et de besoins théoriques, pas d’une embauche ou d’un budget constaté. Les réserves sont initialisées avec la valeur conventionnelle 1. Aucun bataillon ou habitant créé. Les effets navals et de contrôle de détroit du PM restent inchangés ; ils portent sur l’État du moteur, pas sur un périmètre cadastral de chaque fort. Aucun bonus terrestre supplémentaire inventé.

Les **{len(tech['technologies'])} technologies TUR** restent identiques. Le bâtiment requiert scientific_fortification_siegecraft, déjà acquis ; le PM de base n’a pas de prérequis supplémentaire. Groupes, PM, intrants et emplois sont résolus. L’audit impérial reste FAIL_STATIC avant/après avec les trois mêmes observations héritées : gate horse_artillery des hussards, ressource régionale cuivre à Diyarbakır, profil historique impérial non certifié. Les deux nouveaux forts n’ajoutent aucune anomalie technologique. Ni graphe TECH ni recettes ECON modifiés.

Les gouverneurs de Morée/Thessalie, les notables et autorités religieuses, le Magne, l’insécurité et l’économie d’après-Orlov restent partiellement étudiés. Le civil Haseki ne commande pas fonctionnellement la province ; son futur et l’évolution de sa carrière suivent les mécaniques du jeu. Rendu des traits, vivier, placement des forts, embauche, salaires et effets navals attendent le test groupé. Aucun statut de région complète.

## Sources, contrôles et concurrence

Sources et passages vérifiés : SOURCES.md. Küpeli 2020 pour Athènes, Karabıçak 2020 pour les négociations et la chronologie du Magne, ministère grec de la Culture pour les places. Original BOA non consulté directement ; téléchargements manqués distingués des archives effectives. Aucune précision de frontière ou de naissance inventée.

**{count}/{count} contrôles statiques réussis** : sorties propres, parse/références, personnage civil sans leadership national, localisations FR/EN BOM sans collision, compatibilité des forts, recette conservée, POPs et propriétaires mondiaux/régionaux, armées entières, empreintes antérieures et Git. L’audit technologique FAIL_STATIC reste distinct de la non-régression du lot. Aucun moteur lancé.

Les **{protected} fichiers fonctionnels antérieurs**, **{prior} preuves WORLD** et **{serg} preuves SERG** de la capture d’application sont identiques. Les travaux TECH-R1/R2/R3, ECON-ALLOYS/quincaillerie, génie/fortifications, HBC-06 et SERG sont préservés. Aucune écriture Git, vanilla ou suivi SERG, aucun retour à une baseline ancienne.

**Progression inchangée : 10/80 Balkans (12,50 %), 10/320 WORLD (3,13 % arrondis), zéro nouvelle validation joueur.** Aucun critère entier de P1-06 n’est crédité pour ce noyau partiel qui exclut la Crète. Les huit critères gardent leur périmètre canonique ; aucun dénominateur retiré. Prochaine candidate : **BALKANS-07 — Crète, complément de P1-06** ; les obligations continentales restent ouvertes. Aucun test intermédiaire ; aucune autre région WORLD avant confirmation explicite du test balkanique groupé.
''')
    doc('TEST_MATRIX.md',f'''# B06 — Contrôles exécutés

| Exécution | Résultat et portée |
| --- | --- |
| `python tools/validate_starting_technology_1776.py --tag TUR --output .../TECH_BEFORE.json` | Sortie 1 : FAIL_STATIC, trois constats hérités |
| `python tools/world1776_balkans06.py --apply` | Cinq ajouts propres ; refuse une seconde application ; aucun fichier partagé écrit |
| Même audit vers TECH_AFTER.json | Sortie 1 : trois constats identiques ; nouveaux forts et PM compatibles |
| `python tools/world1776_balkans06.py --validate` | **{count}/{count}**, sortie 0 ; conservation et références du lot |

Le contrôle lit les données effectives mod/vanilla, les recettes communes, les historiques et les deux captures. Il ne lance aucun moteur et ne certifie ni le budget ni les frontières historiques. Les anciens tests B01–B05 ne sont pas réécrits pour faire disparaître les changements extérieurs. Le reçu B04 de 00_states.txt est daté avant HBC-06 ; la région grecque et la carte courantes sont conservées, pas restaurées depuis B04.
''')
    doc('GROUPED_RUNTIME_ITEMS.md','''# B06 — Ajouts au protocole balkanique final

NOT_RUN ; aucun test intermédiaire ni reçu humain.

1. Nouvelle partie TUR, 1776 : Hacı Ali Haseki dans le vivier civil, trait français/anglais correct, aucun chef national remplacé, pas de commandement militaire ajouté.
2. Un fort côtier TUR de base en ATTICA et un en PELOPONNESE ; ne pas confondre niveau régional et maillage exact de Palamidi/Antirrio. Observer placement, détroits et interactions avec les portions vénitiennes.
3. Suivre un mois d’embauche, qualifications, armes légères, fer, salaires et budget. Les 2 000 emplois sont une capacité, pas une présence garantie.
4. Contrôler Cérigo, Vonitsa, Prévéza/Parga, Butrinto, les Ioniennes, MON/RAG et les maisons B05 ; aucun territoire ou bataillon transféré. Crète témoin inchangé.
5. Sauvegarder/recharger : personnages, traits, niveaux, propriété, PM et erreurs de chargement. Joindre B01–B05 et les futures reprises dans un seul protocole groupé.

Le Magne, les notables, les garnisons exactes, l’après-Orlov et la démographie demeurent des obligations historiques. Aucune sortie de la phase Balkans avant confirmation explicite du joueur.
''')
    state=json.loads(original['ROADMAP_STATE.json']);score=sum(c['status']=='STATIC_VERIFIED' for p in state['phases'] for r in p['subregions'] for c in r['criteria'].values());assert score==10
    region=next(r for r in state['phases'][0]['subregions'] if r['id']=='P1-06')
    limits={'O':'Souveraineté agrégée conservée ; Magne et limites locales ouverts, Crète hors lot.','I':'Voïvode athénien représenté civilement ; pas de gouvernement provincial fonctionnel, autres titulaires et Crète ouverts.','D':'Conservation vérifiée ; démographie historique et minorités non reconstituées, Crète hors lot.','E':'Deux capacités côtières ajoutées ; budget, qualification, marché, ressources historiques et Crète ouverts.','T':'Deux forts compatibles ; trois constats impériaux hérités, profil régional complet/Crète non vérifié.','R':'Armées/diplomatie conservées ; bandes, garnisons et obligations locales non reconstituées, Crète hors lot.','S':'55 contrôles du noyau installé ; ni clôture statique régionale complète ni couverture de la Crète.'}
    for key,remaining in limits.items():region['criteria'][key]={'status':'PARTIAL','evidence':'BALKANS-06/REPORT.md','remaining':remaining,'runtime':'NOT_RUN'}
    region['criteria']['V']={'status':'NOT_STARTED','evidence':'BALKANS-06/GROUPED_RUNTIME_ITEMS.md','test_timing':'END_OF_BALKANS'}
    state['lots'].append({'id':'BALKANS-06','status':'IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION','scope':['Mainland Greece and Peloponnese only','Athenian voivode civil representation','Two Ottoman coastal defence capacities'],'excluded':['Crete'],'runtime':'NOT_RUN','test_timing':'END_OF_BALKANS','files_modified':5,'new_RGBs':0,'new_tags':0,'people_transferred':0,'world_population_delta':0,'new_combat_units':0,'new_politicians':1,'receipt':'BALKANS-06/FILES_MODIFIED.json','protocol':'BALKANS-06/GROUPED_RUNTIME_ITEMS.md','historical_research_status':'REGION_INCOMPLETE','credited_criteria':[]})
    assert (b.OUT/'ROADMAP_STATE.json').read_bytes()==original['ROADMAP_STATE.json']
    (b.OUT/'ROADMAP_STATE.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    title='BALKANS-06 — 2026-10-26'
    append('ROADMAP.md',title,'Grèce continentale et Péloponnèse : représentation civile d’Haseki, deux capacités de fortification côtière TUR, aucun RGB/POP/bataillon modifié. Crète exclue de cette autorisation ; aucun point pour un noyau partiel de P1-06. Progression inchangée : 10/80 (12,50 %), 10/320 (3,13 %), zéro validation joueur. Rapport BALKANS-06/REPORT.md. Prochaine candidate BALKANS-07 Crète ; obligations continentales ouvertes. Test balkanique groupé conservé.')
    append('PROGRESS_HISTORY.md',title,f'Entrée recalculée 10/80 et 10/320. État courant 837 336 539 habitants, dont +2 400 000 issus du chantier externe HBC-06, reçu vérifié sans validation WORLD induite. Aucun ancien total restauré. Cinq fichiers propres nouveaux : un civil historique athénien, son office sans bonus et FR/EN ; deux forts côtiers régionaux avec PM commun de base, 2 000 emplois de capacité et 10 armes légères/10 fer par semaine à plein emploi. Zéro RGB, POP, bataillon, loi, recette ou technologie modifié.\n\n{count}/{count} contrôles statiques propres. Audit TUR FAIL_STATIC avant/après, mêmes trois constats hérités ; forts compatibles, aucun grant. {protected} fichiers fonctionnels antérieurs, {prior} preuves WORLD et {serg} preuves SERG préservés. Aucun Git/vanilla/SERG écrit.\n\nCrète explicitement hors autorisation ; aucune réduction du dénominateur ou attribution d’un critère entier à ce noyau partiel. P1-06 reste incomplet, progression 10/80 et 10/320, validation humaine zéro. Prochaine candidate B07 Crète ; aucun lancement automatique, test groupé seulement en fin de Balkans.')
    append('BLOCKERS.md',title,'P1-06 reste incomplet. L’office athénien est un trait civil, pas un système de gouverneurs ; âge technique 45 non sourcé comme naissance. Capacités côtières agrégées, hubs/maillages et effets de détroit à observer ; garnisons exactes et budget non certifiés. Ni mur d’Athènes de 1778 ni réorganisation du Magne de janvier 1777 préinstallés. Autonomie antérieure du Magne, notables, titulaires de Morée/Thessalie, sécurité et démographie d’après-Orlov ouverts. Crète hors lot, à reprendre sur autorisation.\n\nDette technologique TUR inchangée : hussards/horse_artillery, avertissement cuivre de Diyarbakır, profil impérial non certifié. Aucune recette ou technologie commune altérée. Les obligations B01–B05 et le test balkanique groupé restent applicables ; aucun point supplémentaire ni attestation humaine.')
    append('OWNERSHIP_BOUNDARIES.md',title,'Ajouts propres uniquement : histoire de bâtiments pour deux capacités côtières TUR en ATTICA/PELOPONNESE, histoire civile d’Haseki, trait d’office et deux localisations. Aucun fichier fonctionnel partagé écrit. Crète exclue, toutes les autres attributions et données conservées. Les effets sont ceux du bâtiment naval commun à l’échelle de l’État moteur, pas des cellules de fort cadastrales.\n\nLe total mondial courant inclut l’ajout extérieur HBC-06 de 2 400 000 habitants. Reçu observé et archivé côté B06 ; aucune reprise du chantier américain ou de son suivi, aucune compensation. Conserver toutes les installations SERG, TECH/ECON et B01–B05 ; aucun droit d’écrire leurs autres blocs induit.')
    assert (b.OUT/'NEXT_ACTION.md').read_bytes()==original['NEXT_ACTION.md']
    (b.OUT/'NEXT_ACTION.md').write_text('''# Prochaine candidate WORLD — BALKANS-07

**Crète, complément de P1-06**, référence 1er janvier 1776. Candidate seulement, aucune nouvelle mission automatique. L’autorisation B06 portait sur Grèce continentale et Péloponnèse ; la Crète est restée intacte.

À la prochaine autorisation : administrations ottomanes de Candie/La Canée/Réthymnon, l’après-Daskalogiannis, les autorités locales et les communautés ; vérifier titulaires, fortifications et limites datées, sans projeter le XIXe siècle. Lire suivi, preuves B06 et empreintes courantes avant intervention. Ensuite seulement proposer les lots bulgares/macédoniens/thraces de la feuille de route.

Obligations continentales B06 : autonomie du Magne avant le règlement daté de janvier 1777, notables et gouverneurs de Morée/Thessalie, démographie et sécurité d’après-Orlov, budget/placement des deux capacités côtières, rendu du civil Haseki. Les obligations B01–B05 restent ouvertes.

Progression inchangée : **10/80 Balkans (12,50 %), 10/320 WORLD (3,13 %)**, zéro nouvelle validation joueur. Aucun critère entier crédité au noyau B06 qui exclut la Crète ; aucun dénominateur modifié.

Préserver VEN/Cérigo/postes B04, RAG/MON, maisons B05, SERG et TECH/ECON. Total mondial de référence courant 837 336 539, comprenant l’ajout indépendant HBC-06 ; ne pas revenir à 834 936 539. Aucun Git d’écriture, vanilla ou suivi SERG.

Test groupé à la fin du travail balkanique techniquement réalisable, sans tests intermédiaires. Aucune autre région WORLD avant confirmation explicite du joueur ; aucune attestation humaine fictive.
''',encoding='utf8')
    concurrent=json.loads(original['CONCURRENT_CHANGES.json']);concurrent['BALKANS-06']={'receipt':'BALKANS-06/CONCURRENT_CHANGES.json','protected_gameplay_unchanged':protected,'prior_WORLD_proofs_unchanged':prior,'SERG_proofs_unchanged':serg,'external_preexisting_work':'BALKANS-06/EXTERNAL_HBC06_OBSERVATION.json','shared_gameplay_files_written':0,'new_files':5,'new_RGBs':0,'world_population_delta_by_B06':0,'SERG_writes':0,'Git_writes':0,'vanilla_writes':0}
    assert (b.OUT/'CONCURRENT_CHANGES.json').read_bytes()==original['CONCURRENT_CHANGES.json']
    (b.OUT/'CONCURRENT_CHANGES.json').write_text(json.dumps(concurrent,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    b.dump('PROGRESS_CALCULATION.json',{'entry':{'Balkans':10,'WORLD':10},'credited':[],'reason':'P1-06 remains partial: current authorization excludes Crete and several regional obligations remain. No credit for a partial core.','Balkans':state['phases'][0]['progress'],'WORLD':state['progress'],'human_attestations_created':0})
    checks=[]
    def ck(key,value):checks.append({'check':key,'passed':bool(value)})
    for e in receipts:ck('receipt.'+e['file'],b.b.a.sha(b.ROOT/e['file'])==e['after'])
    for e in sources:
        if 'sha256' in e:ck('source.'+e['file'],b.b.a.sha(b.LOT/e['file'])==e['sha256'])
    for name in ['world1776_balkans06.py','world1776_balkans06_closeout.py']:
        ast.parse((b.ROOT/'tools'/name).read_text('utf8'));ck('python_syntax.'+name,True)
    ck('static_PASS',validation['passed']==count)
    ck('no_full_regional_credit',sum(c['status']=='STATIC_VERIFIED' for p in state['phases'] for r in p['subregions'] for c in r['criteria'].values())==10)
    ck('whole_P1_06_partial',all(c['status']!='STATIC_VERIFIED' for c in region['criteria'].values()))
    ck('zero_human_credit',state['progress']['runtime_user_validated']==0)
    ck('grouped_gate_preserved',state['phase_transition_gate']['next_region_requires_explicit_user_confirmation'] and not state['phase_transition_gate']['partial_lot_tests_requested'])
    ck('only_Balkans_started',all(p['status']=='NOT_STARTED' for p in state['phases'][1:]))
    ck('world_conserved',pop['world_before']==pop['world_after']==837336539)
    ck('Git_unchanged',b.b.a.git_state()==base['inventory']['git'])
    ck('SERG_unchanged',all(b.b.a.sha(b.ROOT/r)==h for r,h in base['SERG_proofs'].items()))
    ck('previous_WORLD_proofs_preserved',all(b.b.a.sha(b.ROOT/r)==h for r,h in base['prior_WORLD_proofs'].items()))
    ck('HBC_external_receipt_matches',all(b.b.a.sha(b.ROOT/r)==h for r,h in hbc.items()))
    delivery={'status':'PASS' if all(c['passed'] for c in checks) else 'FAIL','passed':sum(c['passed'] for c in checks),'total':len(checks),'checks':checks,'runtime':'NOT_RUN','human_attestations_created':0}
    b.dump('DELIVERY_CHECKS.json',delivery)
    b.dump('DELIVERY_MANIFEST.json',{'lot':'BALKANS-06','date':'2026-10-26','historical_date':'1776-01-01','status':'IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION','regional_status':'PARTIAL_CRETE_EXCLUDED','runtime':'NOT_RUN','functional_files':receipts,'tracking':{n:b.b.a.sha(b.OUT/n) for n in TRACK},'tools':{p.relative_to(b.ROOT).as_posix():b.b.a.sha(p) for p in (b.ROOT/'tools').glob('world1776_balkans06*.py')},'evidence':{p.relative_to(b.LOT).as_posix():b.b.a.sha(p) for p in b.LOT.rglob('*') if p.is_file() and p.name!='DELIVERY_MANIFEST.json'},'tests':{'static':f'{count}/{count}','delivery':f'{delivery["passed"]}/{delivery["total"]}','technology_contract':'FAIL_STATIC, three identical inherited findings'},'progress':{'Balkans':'10/80','WORLD':'10/320','new_human_validation':0}})
    print(json.dumps({k:v for k,v in delivery.items() if k!='checks'}));print([c for c in checks if not c['passed']])

if __name__=='__main__':main()
