# Vérification technique réellement exécutée — 29 octobre 2026

## Résultats nouveaux

| Contrôle | Résultat | Preuve |
| --- | --- | --- |
| Contrôles ciblés de la version actuelle | **30/30 PASS** | `SCOPED_STATIC_RESULTS.json`, `CURRENT_SCOPE.json` |
| Suite existante `test_serg_sc2_teschen` | **16 PASS, 2 FAIL sur 18**, aucune erreur d'exécution | `EXISTING_TEST_RESULTS.json`, `test_serg_sc2_teschen.log` |
| Suite existante `test_serg_closure_roadmap` | **27 PASS, 1 SKIP sur 28 cas**, aucun échec | Même JSON, `test_serg_closure_roadmap.log` |
| Validateur canonique courant | **PASS**, 93/235, 39,57 %, 32/81, 23 tâches bloquées | `CANONICAL_CHECK.json` |
| Conservation du périmètre Teschen pendant la recherche | **PASS** : aucune dérive de dépendance fonctionnelle ciblée ; 58 fichiers protégés inchangés | `CONSERVATION_CHECK.json` |
| Moteur Victoria 3 / nouvelle validation humaine | **NON EXÉCUTÉ / aucune réception créée** | Aucun résultat moteur revendiqué |

Les 123 contrôles de `../VALIDATION.json` sont une **preuve ancienne consultée**, non une nouvelle exécution de 123 tests. Leur fichier et les anciens résultats restent intacts.

### Ce que contrôlent les 30 vérifications

- Liste exacte des 179 cellules identique à la livraison, propriété unique `AUS`, région physique `STATE_WEST_GALICIA`.
- 581 titres uniques ; les 580 lignes antérieures sont conservées et seul `x9061E0` est ajouté pour AUS. Extension de masque impérial égale aux seules 179 cellules ; migration de propriété vide.
- Aucune inclusion de toute la région galicienne dans les ensembles du compilateur ou dans les dérogations de membre. Exception provinciale exacte `('x9061E0','STATE_WEST_GALICIA','AUS')`.
- Commande de restitution limitée à `x9061E0`, absence des deux provinces galiciennes voisines dans cette restitution, condition provinciale du titulaire légitime présente.
- Neuf électeurs d'origine dans la définition et dans le déclencheur compilé : KMZ, KTR, KCL, AUS, KPF, SAX, PRU, BAV, HAN.
- Sept groupes de population totalisant 135 753, déclarations de bâtiments et recrutement militaire de Teschen identiques au snapshot installé. Propriétaires voisins Moravie/Haute-Silésie/Galicie occidentale également conservés.
- Analyse syntaxique de huit scripts actuels ciblés ; en-têtes et BOM des localisations impériales françaises/anglaises. Cette analyse ne prétend pas exécuter les commandes du jeu.
- Maintien du blocage P1, de l'attente de TE-R-CORE et de l'absence de reçu Teschen ; progression canonique conservée.

Le relevé des bâtiments reste un relevé de **déclarations** : le textile de niveau 2 apparaît dans le fichier de base et dans l'overlay BUILD. Ce n'est pas une preuve de quatre niveaux exécutés par le moteur. Aucun niveau, PM, propriétaire de bâtiment ou réserve n'a été réécrit.

## Deux échecs de la suite existante : interprétation bornée

1. `test_physical_and_demographic_histories_unchanged` exige l'empreinte **globale** du bitmap et de plusieurs historiques du 25 octobre. Il échoue dès le bitmap, dont l'empreinte a changé depuis cette livraison. Des travaux ultérieurs sont documentés dans le dépôt et le manifeste relève les différences actuelles ; ce test n'établit pas une régression Teschen. La liste exacte des cellules, la propriété et les données sémantiques Teschen sont revérifiées sur la version actuelle. Les autres assertions de cette méthode, après le premier échec, **ne sont pas présentées comme exécutées**.
2. `test_progress_scope_and_next_candidate_are_bounded` attend encore 82/235 et 24/81. Le validateur constate 93/235 et 32/81 après les réceptions acquises. Cette assertion de snapshot est obsolète ; le test et son échec brut sont conservés. Les assertions suivantes de cette méthode ne sont pas revendiquées comme exécutées.

Le SKIP canonique est celui déjà prévu par le test d'absence d'écriture de l'état initial ; il est documenté dans le journal. Aucun test ancien n'a été corrigé, retiré ou relabellisé PASS pour afficher une suite entièrement verte.

## Conservation, concurrence et première exécution du nouveau vérificateur

Le `BASELINE.json` de cette recherche capture le validateur initial, les empreintes des fichiers protégés, les fichiers fonctionnels et Git HEAD/branche/index. Ceux-ci ne sont pas restaurés depuis un ancien état.

Les anciennes empreintes globales de la livraison Teschen diffèrent sur de nombreux fichiers partagés modifiés depuis le 25 octobre : le détail est conservé dans `older_delivery_runtime_differences`, sans imputer ces évolutions à la mission présente ni toutes les certifier. La comparaison sémantique ciblée montre la conservation du périmètre Teschen.

Pendant la réévaluation, six chemins musicaux présents dans le snapshot initial sont devenus absents : deux OGG `cantus_firmus_monks*` et quatre fichiers de `music/main_themes/`. Ils sont hors dépendances Teschen. Ils restent consignés avec leurs anciennes empreintes dans `outside_teschen_drift` ; aucune restauration ou modification de ces travaux concurrents n'a été faite. Il n'est donc **pas affirmé que tout le workspace est inchangé**.

La première exécution du nouveau vérificateur a donné **28/30** : elle choisissait la première ligne contenant KMZ, qui était une liste de membres et non la liste des électeurs ; elle exigeait aussi à tort l'immobilité de tous les fichiers fonctionnels malgré la concurrence musicale. Ces résultats bruts restent dans `FIRST_RUN_*.json`. Le vérificateur a été corrigé pour sélectionner la ligne d'attribution du privilège électoral et contrôler les dépendances Teschen tout en conservant la dérive globale intégrale. Le nom du fichier militaire européen a également été rendu explicite. La seconde exécution donne 30/30. Aucun fichier du mod n'a été changé pour obtenir ce résultat.

## Reproduction et effets d'écriture

Depuis la racine du dépôt, avec le Python du runtime disponible :

```powershell
& 'C:\Users\simeo\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -B -X utf8 docs/reports/map/SERG_CLOSURE/SC2-TESCHEN/REASSESSMENT_2026_10_29/verify.py tests
& 'C:\Users\simeo\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -B -X utf8 docs/reports/map/SERG_CLOSURE/SC2-TESCHEN/REASSESSMENT_2026_10_29/verify.py scoped
```

Ces commandes écrivent seulement leurs nouveaux résultats dans ce dossier de recherche. Elles n'appellent ni l'installateur, ni `serg_sc2_teschen.validate()`, qui réécrit des preuves anciennes, ni la génération des vues canoniques. Les assertions négatives des tests existants utilisent des données simulées en mémoire. Pas de Git d'écriture, de changement de branche, de vanilla modifié ou de lancement du jeu.

## Nature des problèmes restants

| Type | État constaté |
| --- | --- |
| Incompatibilité de script Teschen démontrée | Aucune détectée par ces contrôles bornés ; le moteur n'est pas exécuté. |
| Régression de propriété/POP/bâtiments/recrutement Teschen | Aucune détectée. |
| Restriction de construction ou rentabilité | Aucune nouvelle mesure ou conclusion ; hors correction de registre et hors mission économique. |
| Incertitude historique | Correspondance géographique et démographie comparables encore substantielles ; voir les rapports dédiés. |
| Panne observée en jeu pendant cette mission | Aucune partie exécutée, donc aucune panne ni réussite moteur nouvellement observée. |
| Réception humaine TE-R-CORE | Toujours absente. Le reçu MAP2A et l'observation partielle ne la remplacent pas. |
