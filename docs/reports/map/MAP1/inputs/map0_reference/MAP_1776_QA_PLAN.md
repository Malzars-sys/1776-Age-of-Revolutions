# MAP-0 — Validation reproductible

Le mode inventaire réussit lorsque les fichiers de référence sont complets;
il **ne certifie pas une carte sans anomalies**. Le mode `--strict` refuse les
ERROR/BLOCKER enregistrés. Aucune anomalie n'est corrigée automatiquement.

## Tests réalisés le 2026-10-10

| Test | Résultat constaté |
|---|---|
| Fetch et divergences Git | Nouveau lot 3126bac/0e018d9 récupéré; anciennes corrections d909641/d5b7421 déjà dans main. |
| Merge isolé, non commité | Aucun conflit textuel / aucune entrée git ls-files -u; deux fichiers indexés. HEAD c891b1d, MERGE_HEAD 0e018d9. |
| git diff --check, candidat et principal | Réussi; cela ne détecte ni mauvaise propriété ni tokens Git collés. |
| Audit RGB et définition des régions | 40 875 couleurs, 675 États terrestres / 781 régions avec mers; aucune couleur non couverte. |
| Membership mod contre vanilla | Zéro liste de provinces différente; pas de géométrie ajoutée. |
| Appartenance/propriétaires et scopes | Anomalies documentées : 53 propriétaires incompatibles, 11 répétitions même propriétaire, 6 occurrences de mauvais scope, 9 sélecteurs historiques orphelins dans main. |
| Hubs, sorties navales, région stratégique | Aucune référence hors région/ID naval absent/affectation stratégique manquante ou multiple relevée par les contrôles implémentés. Pas un test de navigabilité. |
| Terrain et adjacencies.csv | Identifiants vérifiés sur 240 lignes de connexions explicites, sans anomalie d'ID relevée; contacts terrestres non recalculés. |
| Localisations de base | Toutes les clés des State_IDs et TAGs actifs trouvées en français et anglais. Noms dynamiques et syntaxe de toute localisation non certifiés. |
| Catalogue et allocation | Ancien catalogue retrouvé 1 043/675; 20 écarts de membres des couples. Nouvelle allocation : 1 043 couples, chaque État dans une seule région, neuf couples VEN/GEN inclus/protégés. |
| Baseline | 40 928 lignes uniques province/État/propriétaire, 40 875 provinces couvertes; propriétaires historiques proposés tous vides. |
| Fixtures et candidat | Détection des cinq tokens parasites dans create_state, doublon x867A90, delta wallon −37 881; normalisation RGB et exceptions géographiques testées. |
| Barrière stricte | Refuse la publication en présence des ERROR/BLOCKER observés; résultat non nul attendu, pas une erreur à masquer. |
| validate_diplomacy_ottoman_1776.py | Réussi : −10 administrations exactes, 72 permanents ottomans, Égypte, journaux/événements et conditions indépendantes, technologies/localisations; modèles 1 024 combinaisons administratives et 192 voies politiques. |
| validate_ai_regional_infrastructure_1776.py | Réussi : PM, top 10 PIB, égalités, pays petits, protection joueur, idempotence et aucun bâtiment ajouté. |
| validate_map_rework_history.cjs | Populations des huit États et références de bâtiments réussies, puis échec `Unit types/counts changed` : test figé sur d909641 alors que main contient les changements militaires/navals autorisés ultérieurs. Ne pas annuler ces changements pour satisfaire ce vieux test. La suite après cet assert n'a pas été exécutée. |
| Nouvelle partie / performances / sauvegarde | **Non exécutés** : MAP-0 est une préparation et le candidat est incohérent. Aucun jeu relancé ni sauvegarde modifiée. |

État du registre : main 59 BLOCKER, 9 ERROR et 41 REVIEW; candidat 66 BLOCKER,
11 ERROR et 22 REVIEW. Il s'agit de lignes de diagnostic, pas de nombres de bugs
indépendants. Le candidat répète aussi les problèmes hérités de main. Son absence
de comparaison au catalogue dans ces comptes explique certains écarts de REVIEW.

## Reproduction

Depuis la racine principale, Python disposant de Pillow :

```powershell
& 'C:/Users/simeo/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' tools/map_1776_audit.py --self-test --candidate 'C:/Users/simeo/.codex/worktrees/map-0-collaborator-integration/1776_Age_of_Revolutions_fork'
& 'C:/Users/simeo/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' tools/map_1776_prepare_prompts.py
```

L'auditeur réécrit uniquement les CSV/JSON de docs/reports/map. Ne pas utiliser
ces rapports comme fichier de jeu. `--game` permet de préciser une autre installation.
Pour une barrière de publication, ajouter `--strict` (code 2 attendu en l'état).
Conserver les résultats par révision et hash du raster avant toute correction;
une exécution après modification remplace les rapports calculés.

## Barrières avant chaque futur lot

1. Identifier main, candidat, ancêtre et état local. Établir une liste approuvée
   d'États/provinces/TAGs modifiables; empreintes des historiques, map_data et assets.
2. Parse structurel + grammaire contextualisée : accolades, IDs, doublons et tokens
   inattendus; les listes admettent des tokens nus, create_state pas des commandes Git.
3. Comparer les ensembles du bitmap, des régions, des propriétaires et impassables.
   Mers/lacs non possédés sont normaux; territoire terrestre non possédé exige revue.
4. Vérifier State_ID/ID numérique, TAG actif/capitale, scopes pops/bâtiments,
   cultures et religions disponibles, types de bâtiments et PM valides.
5. Comptabiliser tailles de pops **par culture/religion/territoire**, niveaux de
   bâtiments par type/PM et détenteur économique; conservation globale et locale.
   Toute perte/redistribution exige justification approuvée. Ne pas confondre
   propriété territoriale et investissements étrangers.
6. Vérifier recrutement, casernes, bases navales, HQ, ports/hubs/naval exits,
   ressources/arable/traits et centres urbains; tester les fichiers 98_* et effets
   de démarrage, pas seulement le premier historique rencontré.
7. Vérifier sujets, blocs, relations, traités, commerce, références de pays/État
   dans journal/événement/décision. La disparition de LUX exige notamment cette étape.
8. Contrôler la différence totale avec la révision avant lot : pays hors périmètre
   inchangés; VEN/GEN protégés sauf décision nominative. Aucun changement caché d'armée,
   technologie ou recette pour résoudre un conflit de carte.
9. Clés anglaises/françaises + format/BOM et affichage dynamique. Croiser les labels
   du jeu et les noms historiques retenus, sans effacer une distinction juridique.
10. Aucune ERROR/BLOCKER non arbitrée dans le manifeste du lot. Les anomalies anciennes
    restantes doivent être isolées et ne pas s'aggraver; inventaire réussi ≠ release prête.

## Extensions de validation à développer avant intégration A/B/C

Le nouvel auditeur fournit déjà inventaire et premiers contrôles. À ajouter :
manifestes de transferts avec conservation démographique/économique par composante;
diff de toutes les références militaires et politiques; contrôle de syntaxe moteur
complet; validation formelle des CSV de recommandations/sources/couverture; liens
historiques sourcés; comparaison des exports. Le vieux test map-rework doit être
séparé en assertions de carte stables et comparaisons militaires avec baseline
actuelle explicitement approuvée, sans simplement désactiver ses protections.

Pour C, construire un contrôle de connexité/composantes de chaque province,
contacts de pixels avec wrap_x, détroits et accès maritimes, intersections avec
rivières/relief, et validation des locators/splines/ressources dérivées. Préparer
un prototype via l'éditeur du jeu et sa chaîne d'export; ne pas écrire un binaire
nodes.dat ou splnet supposé. Mesurer temps de chargement, RAM, sauvegarde et vitesse
de simulation avant/après dans les mêmes conditions.

## Protocole en jeu ultérieur

Réserver deux profils mod identiques sauf le lot testé, noter version 1.13.11
ou la version réellement utilisée, révision, DLC et liste de mods. Utiliser des
**nouvelles parties** à 1776-01-01, pas une ancienne sauvegarde dont les provinces
sont déjà instanciées. Archiver les logs de chaque exécution avant la suivante.
Ne pas toucher à la partie actuelle de l'utilisateur sans autorisation.

À J0 en pause, capturer la même vue politique/debug pour Luxembourg/Wallonie,
Lombardie/Istrie/Tyrol, Silésie, Bessarabie/Dobroudja, Caucase, Nunavut/Alaska,
Afrique septentrionale et chaque lot futur. Relever propriétaires, province RGB,
États partagés, capitales, population par groupe, niveaux/PM/propriétaires de
bâtiments, ressources, infrastructure, ports, recrutement et HQ. Inclure des pays
témoins hors lot (France, Grande-Bretagne, Russie et au moins un sujet).

Après initialisation, contrôler Égypte/Empire ottoman, Pologne-Lituanie/Crimée,
blocs/sujets et ouverture indépendante des deux journaux ottomans. Avancer à J7,
J30 et J90 : absence d'États perdus, accès marché/naval, fonctionnement des ports,
finances/populations et règles IA d'infrastructure. Les chiffres budgétaires ne
doivent pas être promis identiques si des transferts approuvés les influencent.

Sauvegarder/recharger une nouvelle partie de test et vérifier l'intégrité; comparer
error.log et game.log, erreurs nouvelles séparées des erreurs anciennes. Pour B/C,
tester sélections/hubs, frontière terrestre, détroits, pathfinding et rendu. Si un
crash/territoire perdu/régression apparaît : suspendre le lot dans le worktree,
revenir au profil de référence sans destruction de fichiers, documenter et demander
arbitrage. Pas de push ni de merge final automatique.

## Matériel transmis aux neuf chercheurs

Un bloc autonome de MAP_1776_REGIONAL_PROMPTS.md accompagné de BASELINE.csv,
9_REGIONS.csv, RESEARCH_SCHEMA.md et KNOWN_ISSUES.csv. Les neuf allocations
géographiques totalisent 675 États, sans exclusion VEN/GEN et sans double
responsable principal. Les CSV de recommandations ne seront intégrables qu'après
synthèse historique centrale et mapping vérifié.
