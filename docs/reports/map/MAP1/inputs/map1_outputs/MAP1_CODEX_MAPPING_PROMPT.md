# CODEX — MAP-1A/B, reconstruction géographique vérifiable des frontières au 1er janvier 1776

## Entrées

Le ZIP `MAP1_WORLD_1776_HANDOFF.zip` contient :

- `map1_outputs/WORLD_BORDERS_1776_MASTER.csv` : 1 005 dossiers avec provenance, sans transfert validé.
- `map1_outputs/WORLD_BORDERS_1776_MAPPING_QUEUE.csv` : 410 dossiers prioritaires à localiser ou arbitrer.
- `map1_outputs/WORLD_BORDERS_1776_CONFLICTS.csv` : distinctions recherche/technique.
- `map1_outputs/MAP1_PRIORITY_ARBITRATION.csv` : 20 dossiers prioritaires.
- `map1_outputs/WORLD_BORDERS_1776_SOURCES.csv` : 374 références.
- `map1_outputs/WORLD_BORDERS_1776_COVERAGE.csv` : 1 043 couples.
- `map1_outputs/MAP1_SYNTHESIS_AND_ARBITRATION.md` : méthodologie et limites.
- `map0_reference/MAP_1776_BASELINE.csv`, `MAP_1776_9_REGIONS.csv`, `MAP_1776_RESEARCH_SCHEMA.md`, `MAP_1776_KNOWN_ISSUES.csv`, ainsi que les rapports MAP-0.
- `regional_originals/` : 36 fichiers régionaux (9 × recommandations, sources, couverture et incertitudes), sans double comptage de R8.

## Mission et interdictions

**Phase de cartographie et arbitrage, sans modification du monde en jeu.** Ne pas éditer `common/history`, `map_data`, `gfx/map`, `localization`, pops, bâtiments, armées, diplomatie ou technologies. Ne pas créer de TAG, ajouter/supprimer de provinces, changer de propriétaires, fusionner dans `main`, ni pousser sur GitHub. Aucun reset/clean/stash destructif. Préserver l'état du dépôt et l'ancien worktree du merge georg3mx, toujours non approuvé.

L'objectif est de rendre les conclusions historiques **géographiquement actionnables** par des humains à l'étape suivante, pas d'appliquer les recommandations sans contrôle.

## Étape 1 — Ingestion et exactitude

1. Inspecter les fichiers transmis, UTF-8 BOM et séparateurs CSV. Comparer nombre de lignes/colonnes, Check SHA-256 des originaux avec `MAP1_INPUT_MANIFEST.csv`.
2. Valider 1 005 `Change_ID` uniques, 374 `Source_ID` uniques, 1 043 couples de couverture, références sources valides, 9 régions et absence de doublon R8.
3. Comparer les provinces du tableau MAP-0 à la géométrie installée du jeu 1.13.11. Bitmap rapporté 8192×3616, 40 875 identifiants RGB; SHA-256 MAP-0 `e3911fd80a40c6b297a68f66e898d9b187863b64483a9608123606143ee2ea78`. Stopper et demander accord si hashes/baseline changent.
4. Ne pas confondre TAG propriétaire actuel avec preuve historique. `Confidence=HIGH` n'atteste pas la précision RGB. Les 23 `Mapping_Status=PROPOSED` ne sont pas VERIFIED.

## Étape 2 — Produire un index géographique des provinces existantes

En mode lecture seule :

- Extraire de `map_data/provinces.png` les frontières, boîtes englobantes, centres et contours des provinces terrestres, en tenant compte des projections et des raccordements de la carte (notamment `wrap_x`), sans inventer une projection géographique simpliste.
- Joindre chaque RGB à son State_ID, à chaque Owner_TAG historique courant, à son groupe de régions, à sa taille pixel, et aux anomalies du registre. Une province propriétaire double reste deux attributions dans l'audit jusqu'à arbitrage.
- Construire une indexation spatiale de recherche (par état, bande géographique, ville/hub identifié, toponyme ou coordonnées si disponibles), assortie d'un niveau de confiance géographique.
- Générer pour les 20 dossiers P0 un aperçu lisible avec les contours de provinces, labels RGB et zones historiques discutées. Inclure légende, provenance et date de chaque carte d'époque lorsque superposée.
- Ne jamais prétendre que l'alignement d'une carte ancienne est exact sans points d'ancrage et contrôle de distorsion; ne pas attribuer de coordonnées GPS à des RGB à partir d'une projection non validée.

## Étape 3 — Correspondance des 410 dossiers prioritaires

Pour chaque ligne de `WORLD_BORDERS_1776_MAPPING_QUEUE.csv` :

1. Récupérer les sources par `Source_IDs`, lire la conclusion historique, `Geographic_Location`, les incertitudes et le statut de région.
2. Déterminer les provinces RGB possibles par superposition/validation topographique : villes, côtes, fleuves, relief, limites et anciens lieux administratifs. Si l'alignement reste incertain, `MAPPING_REQUIRED`, pas de RGB inventé.
3. Documenter les cartes ou sources précises (auteur, date, page, légende, biais, points d'ancrage). Préciser si la source est postérieure à 1776, et si elle décrit une revendication plutôt qu'une administration de fait.
4. Distinguer la propriété souveraine, le contrôle effectif, l'autonomie et le compromis gameplay; maintenir séparées ces colonnes.
5. Comparer les propositions des interlocuteurs secondaires et les 150 lignes interrégionales signalées; remonter tout désaccord sans fusion silencieuse.
6. Donner des décisions `MAPPING_VERIFIED`, `MAPPING_PROPOSED`, `MAPPING_REQUIRED` **avec justification visuelle**; ne pas cocher VERIFIED sans représentation du polygone exact et correspondance documentée.
7. En cas de source non probante ou de problème de localisation, fournir la question exacte à renvoyer au chef régional. Les 75 besoins de TAG mentionnés ne prouvent pas l'existence de 75 nouveaux pays à créer.

## Étape 4 — Arbitrages P0 et problèmes techniques

Traiter d'abord `MAP1_PRIORITY_ARBITRATION.csv` : Luxembourg/Wallonie (xD001A0, effet sur LUX et sa population), Lombardie (x867A90/x9AC196), Silésie, Bessarabie (tokens Git), Bassora, Khorasan, Bombay/Salsette, Northern Circars/Guntur, Mandchourie extérieure, Mindanao, West Micronesia xEF50C0, Kenya, Tanganyika, Alaska, Nunavut, Nouveau-Mexique, Guyanes x6C6251, Rio Grande do Sul, Uruguay, Pastaza.

Pour chaque cas, séparer la **réparation syntaxique indépendante de la décision territoriale**. Aucun choix de propriétaire ne doit être déduit d'une erreur de script. Ne pas intégrer le candidat de merge georg3mx : remettre un rapport de correction de ses anomalies et une proposition sécurisée pour préserver pops, bâtiments et références du Luxembourg.

## Étape 5 — Préparer le manifeste d'intégration, toujours non exécutable

Créer `MAP1_GEOGRAPHIC_MATCHES.csv` avec au minimum : `Change_ID`, `State_ID`, `Research_Current_Owner_TAG`, `Research_Proposed_Owner_TAG`, `Verified_Province_IDs`, `Mapping_Status`, `Evidence_Source_IDs`, `Historical_Conclusion`, `Geographic_Proof_Artifact`, `Mapping_Method`, `Mapping_Confidence`, `Historical_Review_Status`, `Technical_Review_Status`, `Cross_Region_Review_Status`, `Decision_Notes`.

Créer `MAP1_TRANSFER_PROPOSALS.csv` en y incluant seulement les dossiers historiquement et géographiquement **proposables**, mais garder `Apply_To_Mod=NO` et `Approved_By_User=NO`. Vérifier les TAG réellement définis dans le dépôt; les valeurs `NEW_TAG_REQUIRED` ne sont pas des TAGs. Ne pas fournir de commande qui exécuterait ces transferts.

Pour tout transfert hypothétique, faire figurer les dépendances : propriété des provinces, State Regions, populations culture/religion, bâtiments/niveaux/méthodes/propriété économique, capitales, hubs/ports/naval exits, formations/recrutement, souveraineté/sujets/pactes/traités, journaux/décisions, localisations. Prévoir conservation exacte des inventaires, sauf changement documenté et explicitement approuvé.

Comparer A (réaffectation), B (scission/recomposition des États) et C (géométrie raster). Proposer C seulement si les polygones existants ne permettent pas une approximation historique acceptable, et **sans l'exécuter**.

## Étape 6 — Livrables obligatoires

Dans `docs/reports/map/` ou un worktree isolé sous dossier MAP1 :

1. `MAP1_BASELINE_PROVINCE_INDEX.csv` — correspondance pixel/State/Owner et anomalies (sans modifications).
2. `MAP1_GEOGRAPHIC_MATCHES.csv` — mapping candidat avec preuve, statut explicite.
3. `MAP1_TRANSFER_PROPOSALS.csv` — transferts proposés non exécutables (`Apply_To_Mod=NO`).
4. `MAP1_GEOGRAPHIC_EVIDENCE/` — aperçus annotés des 20 P0, métadonnées géoréférencement et sources.
5. `MAP1_UNRESOLVED_AND_CROSS_REGION.csv` — doublons, controverses et recherches ciblées manquantes.
6. `MAP1_COLLABORATOR_MERGE_DECISIONS.md` — Luxembourg, Lombardie, Bessarabie; bilan pops/bâtiments.
7. `MAP1_RELEASE_GATES.md` — barrières QA avant MAP-2 : unicité propriétaires/province; conservation démographique/économique; validation jeu 1.13.11; tests de mod après accord.
8. `MAP1_EXECUTIVE_SUMMARY.md` — chiffres de mapping vérifiés/encore en attente, liste d'arbitrages à l'utilisateur et premiers lots régionaux candidats.

## Arrêt et retour utilisateur

Ne pas deviner les frontières. Ne pas transformer les 264 `REVIEWED_NO_CHANGE` en provinces vérifiées. Ne pas rétroprojeter 1777, 1783, 1802, 1836, 1858/1860 sur le départ du 1er janvier 1776.

**STOP à la remise du rapport MAP-1.** Aucune refonte géographique, pas de merge/push. Nous demanderons séparément l'autorisation MAP-2 pour intégrer les transferts, après étude des éléments encore en suspens.
