# MAP-1 — Candidat du collaborateur

Date : 10 octobre 2026. **Refusé en l'état, aucune correction appliquée.**

Le candidat reste dans son worktree, avec HEAD `c891b1d9bb2a21bc42409acbdccc268518110260`
et MERGE_HEAD `0e018d9b292ec263d424500a47279d895cf1020a`. Le contrôle en lecture seule
retrouve deux fichiers préparés, 8 insertions et 29 suppressions. Aucun merge terminé.
La baseline MAP-1 est celle de `main`, pas celle de ce candidat.

## Luxembourg et Wallonie

Le transfert envisagé de `xD001A0`, LUX vers BEO, supprimerait le seul territoire
écrit de LUX. Ce RGB compte 47 pixels. Le locator vanilla Luxembourg tombe dans
ce polygone; la définition du hub city vise cependant `x5180A0`. Un point urbain
ne suffit pas à reconstruire les limites du duché et du comté de Chiny.

Les [Archives nationales du Luxembourg](https://anlux.public.lu/fr/actualites/2016/Carte.html)
signalent deux cartes de Bergé datées de 1776, CP-A-45 et CP-A-46. Leur notice
ne prouve pas le tracé au 1er janvier; le dossier explicatif est daté du 2 mai.
Les fichiers cartographiques complets n'ont pas été récupérés pour un calage.
Voir [aperçu et questions P0-001](MAP1_GEOGRAPHIC_EVIDENCE/MAP1-P0-001.md).

### Conservation démographique

| Culture | Religion explicitement écrite | Population actuelle LUX | Sort du candidat |
|---|---|---:|---|
| wallonian | non précisée | 81 113 | supprimée |
| north_german | catholic | 56 156 | supprimée |
| north_german | non précisée | 447 | supprimée |
| ashkenazi | non précisée | 165 | supprimée |
| Total | | 137 881 | |

Le candidat ajoute 60 000 wallons et 40 000 germanophones chez BEO. La différence
est **100 000 − 137 881 = −37 881 habitants**. Il modifie également la composition
au lieu de déplacer les quatre enregistrements à l'identique. La religion absente
doit rester absente dans l'inventaire; ce rapport ne lui attribue pas un défaut moteur.

Proposition sécurisée, non exécutée : garder LUX pendant l'arbitrage. Si son absorption
est explicitement approuvée ensuite, déplacer les quatre enregistrements sans changer
taille, culture, religion ni autres attributs, et réconcilier le total de WALLONIA
ainsi que les totaux mondiaux. Une redistribution démographique différente exige
une justification et une approbation distinctes.

### Conservation des bâtiments et références

Deux commandes écrites visent encore `region_state:LUX` :

- `common/history/buildings/00_west_europe.txt:4355` : administration, propriété nationale LUX, 1 niveau de propriété écrit.
- `common/history/buildings/98_build_start_1776_world_redistribution.txt:17144` : même type, 1 niveau de propriété écrit.

Les deux activent `pm_simple_organization`, `pm_hereditary_bureaucrats`,
`pm_religious_bureaucrats`. **Ce ne sont pas deux niveaux effectifs certifiés** :
les commandes de création et leur ordre d'application doivent être contrôlés en jeu.
Ne pas effacer ni fusionner automatiquement ces commandes. Une migration approuvée
doit préserver leur contenu, leurs PM, réserves et propriétaires économiques,
avec traitement explicite de l'effet additif/remplacement.

Les références LUX comprennent capitale, historique du pays, recrutement/formation,
relations et transit PRU/LUX. Les pointeurs exacts sont filtrables dans
[MAP1_DEPENDENCY_REFERENCES.csv](MAP1_DEPENDENCY_REFERENCES.csv). Leurs occurrences
sont lexicales : elles ne prouvent pas que toutes les branches de script s'exécutent.
L'inventaire structuré figure dans
[STATE_WALLONIA.json](MAP1_DEPENDENCY_DOSSIERS/STATE_WALLONIA.json).

## Lombardie

Dans main, `x867A90` (428 pixels) et `x9AC196` (79 pixels) sont chacun VEN uniquement.
Le candidat laisse `x867A90` chez VEN tout en l'ajoutant à AUS : doublon nouveau.
Il déplace également `x9AC196` vers AUS. Ce petit polygone est au nord-est du groupe,
pas une identification automatique de Mantoue.

Refuser le doublon ne décide pas entre AUS et VEN. Ne pas corriger les propriétaires
selon l'ordre des fichiers ou seulement selon les noms Bergamo/Brescia. Il faut
une correspondance documentée des cours d'eau, villes et juridictions au 1er janvier.
Voir [P0-002](MAP1_GEOGRAPHIC_EVIDENCE/MAP1-P0-002.md).
Préserver les inventaires AUS/VEN avant toute recomposition, sans déplacer tout
un State_ID pour corriger seulement deux RGB.

## Bessarabie

Les tokens `git status` et `git fetch origin` collés dans `create_state` sont des
anomalies syntaxiques indépendantes des droits de MOL, CRI et TUR. Une future
correction doit uniquement retirer ces tokens, sans changer `owned_provinces`,
les bâtiments ni les populations. Aucun patch runtime n'est appliqué à MAP-1.
L'incident doit être contrôlé dans main et dans le candidat, pas supposé résolu
par un merge sans conflit. Voir [P0-004](MAP1_GEOGRAPHIC_EVIDENCE/MAP1-P0-004.md).

## Décision d'intégration

Conserver le worktree suspendu. Ne pas publier ni lancer ce candidat comme version
validée. Les anomalies préexistantes de main et les régressions propres au candidat
restent séparées dans le registre MAP-0. Aucune disparition de TAG, répartition
démographique, réparation syntaxique ou frontière n'est autorisée par ce rapport.
