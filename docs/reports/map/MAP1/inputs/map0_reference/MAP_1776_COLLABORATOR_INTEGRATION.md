# MAP-0 — Récupération et intégration contrôlée du collaborateur

Audit du 2026-10-10. Scénario : 1776-01-01. **Pas de push, pas de merge final,
pas de modification des frontières ou des historiques dans main.**

## État de départ et protection

Dépôt : `https://github.com/Malzars-sys/1776-Age-of-Revolutions.git` (origin).
Branche de travail : `main`, HEAD `c891b1d9bb2a21bc42409acbdccc268518110260`,
identique à origin/main lors de cet audit. Retouches locales préexistantes conservées :

- `docs/reports/assets/source_registry.json`
- `gfx/interface/icons/building_icons/1776_chemical_plant.dds`
- `assets/icon_sources/chemical_plant_overhead_2026-10-10.png`
- `docs/reports/assets/chemical_plant_revision_2026-10-10/`

Elles ne sont ni stashed, ni regroupées dans un commit MAP-0. Aucun reset/clean.
Les journaux ottomans, diplomatie, populations, bâtiments, technologies et assets
du checkout principal sont restés inchangés par cette mission.

## Comparaison après fetch

`git fetch origin --prune` effectué. La branche distante collaborateur est passée
de `d5b7421` à `0e018d9b292ec263d424500a47279d895cf1020a`.
Ancêtre commun avec main : `d8b1c7e43d8e499e77e5826829fb6f2f816bcff5`.

Main seul depuis cet ancêtre :

- `a62be0b` — asset chekpoint ready to starte the ma)p rework
- `4b299b1` — ottoman je first draft
- `c891b1d` — ottoman ajustement and fix ai road

Collaborateur seul :

- `3126bac3ff6263add707e7d09c737d118ade9db3` — Transfer Luxembourg to Wallonia and adjust population
- `0e018d9b292ec263d424500a47279d895cf1020a` — merge d'origin/main dans sa branche. Ce merge contient les changements de 3126bac, il ne constitue pas une deuxième refonte indépendante.

Travaux anciens déjà intégrés à main :

- `d909641e48a0ddf872d5238962a02e0983256294` — WIP map changes before troubleshooting
- `d5b74211f00eaf15b5ae27824a4c07817945cf86` — fix: map and technology corrections

Leur lot de propriétaires, comparé entre d909641^ et d5b7421, touche **519
provinces dans 8 State_IDs** : Dobroudja, Nunavut, Suisse orientale, Grand Caucase,
Bessarabie, Istrie, Lombardie et Tyrol du Sud. Il ne modifie pas map_data.
On observe notamment le regroupement du Nunavut sous HBC, CAUC→GEO au Grand
Caucase, CRI→MOL en Bessarabie, et les subdivisions AUS/VEN d'Istrie, Lombardie et
Tyrol. Ce sont des modifications constatées, pas une validation historique.
Les anciens fichiers de pops touchés sont 00_west_europe, 01_south_europe,
05_north_america, 09_central_asia et 15_russia; les bâtiments touchés sont
01_south_europe, 02_east_europe, 09_central_asia, 15_russia et
98_build_start_1776_world_redistribution. Ne pas les réappliquer intégralement :
main contient ensuite des ajustements autorisés qui seraient perdus.

## Candidat nouveau réellement préparé

Worktree géré et attaché à cette conversation :
`C:/Users/simeo/.codex/worktrees/map-0-collaborator-integration/1776_Age_of_Revolutions_fork`.

Branche : `codex/map-0-collaborator-integration`, créée depuis c891b1d.
Commande d'intégration : `git merge --no-commit --no-ff origin/georg3mx-map-rework`.
Git n'a signalé aucun conflit textuel. **Le merge est suspendu avant commit** :
HEAD reste c891b1d, MERGE_HEAD vaut 0e018d9. Aucun commit d'intégration créé.
Deux fichiers dans l'index, 8 insertions et 29 suppressions :

- `common/history/states/00_states.txt`
- `common/history/pops/00_west_europe.txt`

Le candidat n'est pas la baseline publiée. Celle-ci provient du checkout principal.
Ne pas lancer le jeu avec ce candidat avant résolution des anomalies ci-dessous.

## Conflits sémantiques du nouveau lot

| Zone | Changement observé | Décision nécessaire |
|---|---|---|
| Wallonie / Luxembourg | xD001A0 passe LUX→BEO. State Region inchangée; LUX perd sa seule province. | Valider l'autorité historique et le choix de représentation avant disparition de LUX. |
| Populations wallonnes | Suppression de 137 881 habitants dans region_state:LUX; +60 000 wallons et +40 000 germanophones dans BEO. Total net **−37 881**. | Justifier/rectifier la conservation et la composition; ce n'est pas un simple transfert conservatif. |
| Lombardie | x9AC196 quitte VEN pour AUS; x867A90 reste chez VEN mais est aussi ajouté à AUS. | Résoudre le doublon avec preuve historique; ne pas rétablir arbitrairement un propriétaire. |
| Bessarabie | `git status` et `git fetch origin` sont collés littéralement dans create_state. | Retirer les tokens accidentels dans un correctif ciblé approuvé; le parseur de braces seul ne suffit pas. |
| Dépendances LUX | Deux sélecteurs de bâtiments region_state:LUX subsistent (00_west_europe et 98_build_start_1776_world_redistribution). | Décider leur migration, propriétaire et niveaux; ne pas les supprimer en bloc. |
| Autres références LUX | Capitale Wallonie, historique de pays, formation militaire, relations, traité de transit PRU/LUX et conditions globales. | Examiner la disparition effective du pays et les références directes/conditionnelles. |

Détail des pops supprimés : wallonian 81 113; north_german catholiques 56 156;
north_german sans religion explicite 447; ashkenazi 165. Leur somme vaut 137 881.
Ces effectifs sont ceux écrits dans les fichiers, pas des chiffres historiques validés.

Le nouveau lot affecte trois provinces : xD001A0, x9AC196 et x867A90. Aucune
géométrie, State Region, méthode de production, technologie ou définition de
bâtiment n'est changée dans ce delta. Pourtant ses dépendances de bâtiments et
de pays deviennent invalides : l'absence de conflit Git ne signifie pas cohérence.

## Statut et prochaine décision

Récupération terminée; intégration locale préparée, **validation sémantique refusée
en l'état**. Les problèmes préexistants de main sont séparés de ceux du candidat
dans MAP_1776_KNOWN_ISSUES.csv. Les fronts ottomans/diplomatiques restent protégés.
VEN/GEN ne sont pas exclus de la recherche, mais leurs historiques particuliers
ne doivent pas subir de redistribution générale.

Décisions à prendre avant finalisation : Luxembourg et sa population/dépendances,
répartition lombarde, suppression ciblée des tokens accidentels. Aucun de ces
arbitrages n'a été appliqué. Conserver le worktree en attente, sans oubli de son
merge non commité; main reste utilisable avec son état antérieur.
