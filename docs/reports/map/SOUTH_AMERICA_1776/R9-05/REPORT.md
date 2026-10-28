# R9-05 — Amazonie et frontières espagnoles-portugaises

**IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION — 1er janvier 1776.** Installation du 28 octobre 2026. Les tests en jeu sont différés à la demande du joueur ; R9-04 et les lots antérieurs conservent leurs statuts et protocoles. Ce rapport traite un ensemble de noyaux documentés, pas une certification de toutes les limites amazoniennes.

## Corrections installées

| Région technique | Modification de propriétaire | Résultat |
|---|---|---|
| **Amazonas** | **43 provinces AP7 → BRZ** | Rétablissement des établissements et liaisons portugais sur l'axe du Solimões/Amazone, Barra, Barcelos, São Gabriel, Marabitanas et le poste/chantier du Rio Branco. **293 provinces restent autochtones.** |
| **Mato Grosso** | **12 provinces AP7 → BRZ** | Noyaux de Vila Bela et Cuiabá, liaison au territoire portugais de Goiás selon la règle de postes reliés. **285 provinces restent autochtones.** Pas d'attribution globale du Mato Grosso au Portugal. |
| **Pastaza / Maynas** | **73 provinces auparavant SC3**, désormais **61 AP7, 11 SC2 et 1 BRZ** | Missions replacées dans l'orbite de Quito/Nouvelle-Grenade ; forêts autonomes séparées du réseau missionnaire ; poste portugais de Tabatinga rétabli. Moyobamba/Cajamarca reste SC3. |
| **Pará** | **6 provinces BRZ → AP7** | Noyau riverain du moyen Tapajós retiré de la possession coloniale uniforme. Belém, Óbidos, Santarém, les hubs et les bâtiments initiaux restent portugais. Le reste du Pará n'est pas pour autant historiquement certifié. |

**134 provinces existantes réattribuées. Aucun nouveau RGB, pixel, pays, State_ID, bâtiment, niveau de bâtiment ou unité.** Les voies de liaison sont des compromis de gameplay sur des cellules existantes ; elles ne prouvent pas le contrôle colonial de toutes les terres bordant les fleuves. [Carte avant/après](R9_05_AVANT_APRES.png), [sources, décisions et réserves](SOURCES.md).

Les revendications des capitanies restent distinguées de l'administration réelle : BRZ revendique Amazonas, Mato Grosso et Pará ; SC2 revendique Pastaza/Maynas. Aucune revendication portugaise sur **tout** Pastaza n'est créée pour le seul poste de Tabatinga. Le traité de 1777 n'est pas appliqué comme frontière initiale.

Le TAG autochtone hérité AP7 porte désormais le nom **« Peuples amazoniens » / « Amazonian peoples »**, au lieu de « Kayapo ». Son territoire réunit déjà plusieurs peuples ; ce renommage évite de leur imposer un ethnonyme unique. Il ne transforme pas cet agrégat en État historique centralisé et ne résout pas toutes ses possessions ou cultures héritées.

## Population et économie

**127 721 habitants existants sont réattribués entre propriétaires, sans ajout, suppression ou migration entre State Regions.** Les cultures, religions explicites et statuts libres/esclaves sont conservés. [Ledger](POPULATION_LEDGER.json).

- Amazonas : 21 058 habitants associés aux portions portugaises ; les autres cohortes restent AP7.
- Mato Grosso : 21 552 habitants associés aux portions portugaises ; autres cohortes conservées AP7.
- Pastaza : **14 669 SC2, 50 450 AP7, 74 BRZ**. Les 74 de Tabatinga utilisent le stock enregistré de 1775 rapporté par Sampaio et cité par Coutinho, incluant les absents ; ce n'est pas un recensement exact de janvier 1776. Les 131 enregistrés séparément au Javari ne sont pas ajoutés à ce poste.
- Pará : 19 918 habitants d'une cohorte indigène existante réattribués à AP7. Les autres cohortes coloniales restent intactes.

Ce sont des allocations techniques de données régionales héritées, pas une nouvelle démographie ethnique de chaque mission. Les réserves concernant les périmètres des recensements et la répartition au sein des régions restent ouvertes. Tous les bâtiments antérieurs, y compris ceux des autres lots, gardent leurs niveaux, PM et propriétaires. Les nouvelles portions coloniales sont incorporées pour respecter la règle utilisateur des raccords ; aucune modernisation technologique ou industrielle n'est ajoutée.

## Fichiers du jeu modifiés

Seulement **4 fichiers** :

1. `common/history/states/00_states.txt` : seuls les quatre blocs régionaux ci-dessus, propriétaires et claims.
2. `common/history/pops/07_south_america.txt` : seuls les quatre blocs régionaux, réattributions de cohortes.
3. `localization/french/mod_v2content_l_french.yml` : seul le nom AP7.
4. `localization/english/mod_v2content_l_english.yml` : seul le nom AP7.

Outils : `tools/r905_geometry.py` pour la préparation géographique depuis la baseline ; `tools/r905.py` pour préparer, appliquer sous contrôle d'empreintes et vérifier. **Ne pas relancer la préparation géographique sur une version ultérieure pour écraser sa proposition archivée** : elle doit être relue depuis l'état courant et les nouveaux résultats conservés séparément. Les snapshots ne sont pas des restaurations à appliquer aveuglément.

Le ledger initial de Tabatinga a été corrigé avant livraison pour distinguer les périmètres de Javari et de Tabatinga. Les données et vérifications initiales sont conservées dans `TABATINGA_SCOPE_AMENDMENT/`, avec reçu des empreintes avant/après. La version livrée contient **74**, pas 205, dans la portion BRZ de Pastaza.

## Vérifications et résultats

`python tools/r905.py --verify` : **30/30 contrôles ciblés réussis**, détails dans [VALIDATION.json](VALIDATION.json).

- Syntaxe, exactitude des 134 changements, mêmes comptes d'attribution par RGB : aucune nouvelle province sans propriétaire ou nouvellement attribuée en double. Les anomalies mondiales héritées ne sont pas effacées pour obtenir ce résultat.
- Régions d'appartenance, portions non vides, capitales toujours possédées, absence de POPs orphelins après suppression de la portion SC3 de Pastaza.
- Effectifs et identités de cohortes identiques par région ; seules les réattributions du ledger sont autorisées. Tous les autres blocs d'États et de populations sont identiques.
- Bitmap, régions, ressources, terrains, locators, bâtiments, définitions et profils des pays, diplomatie et formations militaires préexistants inchangés. Aucun fichier runtime non listé n'a changé depuis la préparation (`CONCURRENT_FILES.json` vide).
- **56 nouvelles provinces portugaises** reliées au réseau de Belém par des terres jouables. Vérification par contacts latéraux de provinces puis **par les pixels réellement adjacents du raster**, en excluant 7 703 cellules/provinces déclarées infranchissables et 226 barrières d'adjacence spéciales recensées globalement. Sept témoins nommés, dont Vila Bela, Cuiabá, Tabatinga et São Gabriel, ont des trajets archivés dans `PIXEL_PATH_WITNESSES.json`. Aucun pont de terre ou passage diagonal n'est ajouté.
- **11 provinces missionnaires** ont une sortie terrestre vers des territoires espagnols préservés. Cette topologie ne garantit pas les droits militaires, les convois ou le calcul de marché du moteur.
- Hubs de Pará conservés chez BRZ ; marqueurs témoins R9-04, Sacramento et CENTRAL préservés, ainsi que tous les blocs hors des quatre régions. Les dossiers et preuves antérieurs ne sont pas réécrits. Les anciens manifestes qui comprenaient les fichiers partagés restent des preuves de leurs versions, pas les empreintes des nouveaux fichiers partagés R9-05.
- Audit technologique avant/après sur BRZ, AP7, SC2 et SC3 : **57 signalements préexistants, aucun ajouté ou supprimé** (18, 2, 19 et 18 respectivement). Les pays restent `FAIL_STATIC` pour cette dette antérieure ; le code retour 1 n'est pas masqué. [Comparaison](TECH_COMPARISON.json).
- Aperçu final construit à partir des propriétaires installés et du bitmap courant, puis examiné visuellement.

Pendant la recherche, un chantier concurrent d'intérieurs africains a modifié des profils, la démographie africaine, des textes et le fichier partagé de redistribution des bâtiments. Ces changements étaient **déjà présents dans PREPARE_RUNTIME.json** et ont été conservés lors de l'installation R9-05. La comparaison avec le premier instantané est archivée dans `CONCURRENT_BEFORE_PREPARE.json` ; aucune ancienne baseline n'a été restaurée. Le contrôle de non-régression global ci-dessus se rapporte à la préparation effective, pas à l'absence de tout travail concurrent depuis le début de la recherche.

**Aucune nouvelle partie, simulation, sauvegarde/rechargement ou validation du marché n'a été exécutée.** Les tests statiques et les trajets de pixels ne constituent pas une validation en jeu. Suivre [RUNTIME_PROTOCOL.md](RUNTIME_PROTOCOL.md) lorsque le joueur effectuera ses contrôles.

## Réserves et périmètre restant

La passe ne résout pas le détail du Guaporé/Bragança, les missions de Moxos/Chiquitos, le site ancien du Javari, toutes les implantations du Napo/Putumayo, les limites entre peuples, les autres secteurs du Pará ou les noms modernes hérités des hubs. L'Acre reste autonome ; aucun morcellement tribal n'est inventé à partir des distributions du XIXe–XXe siècle. La Paz et Santa Cruz ne sont pas redécoupés. Les marges sur les cartes et les proxys jouables restent documentés dans SOURCES.md.

**Aucun commit, push, changement de branche ou modification du vanilla.** Les corrections antérieures et les travaux concurrents déjà présents dans les fichiers partagés sont conservés. R9-06 — Guyanes et La Guajira — est la suite proposée de la feuille de route, à ouvrir sur demande distincte.

## Mesure de ColGrep

**Deux lancements de l'exécutable, une recherche aboutie.** Le premier a échoué avant recherche sur le verrou de cache hors du dépôt. Le second a utilisé le même modèle/configuration locale, avec accès autorisé au cache existant :

```powershell
& 'C:\Users\simeo\.cargo\bin\colgrep.exe' --agent "Locate existing R9 research and implementation evidence for Amazonia and Spanish-Portuguese effective territorial control on 1 January 1776, especially Rio Negro, Rio Branco, Solimoes, Maynas, Pastaza, Guapore and Mato Grosso. Locate prior territorial decisions, sources, current ownership and population mapping tools. Return a small set of precise file paths and line ranges. Read-only repository research; no file edits, no Git, no configuration changes." .
```

Recherche aboutie : **264,44 secondes**, environ **4 min 24 s**, code retour **0**. Commande complète, temps et sorties dans `COLGREP_METRICS.json` et `COLGREP_SEARCH.txt`.

**5 chemins/plages retournés**, tous existants et relus (`COLGREP_VERIFIED.json`). Trois dossiers utiles : Amazonas, Mato Grosso et Pastaza. Deux résultats hors cible : les sources de R9-04 et le dossier 0052 du Río Negro patagonien/Cuyo. Cette homonymie n'a pas été suivie ; elle aurait induit une erreur de région. Le modèle n'a pas fourni directement tout l'ensemble des fichiers runtime et outils de mapping nécessaires.

Les recherches `rg` exactes, les inventaires, la vérification des sources historiques, le choix des cellules et les tests sont restés nécessaires. Leur nombre total n'a pas été instrumenté automatiquement ; aucun chiffre exact n'est reconstitué arbitrairement. Aucun compteur de tokens Codex propre à cette tâche ou à chaque recherche n'est exposé. La sortie locale ne contient pas de télémétrie indépendante confirmant l'activité GPU ; aucune mesure de ce type n'est revendiquée. Aucun modèle, réglage d'intégration ou index complet n'a été reconstruit.

**Intérêt observé modeste dans ce lot** : quelques pistes utiles, presque quatre minutes et demie de latence, deux confusions à éliminer. Sans comparaison équivalente, aucune économie exacte de quota n'est mesurable ; cinq résultats retournés ne signifient pas cinq recherches économisées.
