# TECH-3A.1 — Vanilla Auto-Layout Cleanup

Status : `PASS_STATIC` · Branche : `technology-rework` · Baseline HEAD : `50d0ee9` · Victoria 3 : `1.13.9`

## 1. État initial

Le graphe TECH-3A contenait 276 technologies : 118 nœuds protégés TECH-3A et 158 définitions vanilla conservées pour compatibilité. Les trois vues totalisaient 10 composantes : Production `87+2+1`, Military `77+9+1+1`, Society `65+30+3`.

Les causes principales du mauvais auto-layout étaient :

- une composante Production séparée `manufacturies → distillation` ;
- une composante Military séparée de neuf anciennes technologies autour de `standing_army` ;
- deux composantes Society séparées : administration/finance/urbanisation (30 nœuds) et immunisation (3 nœuds) ;
- le placement mécanique en `era_7` de nœuds pré-1836 (`manufacturies`, `enclosure`, `lathe`, `crystal_glass`, entre autres) ;
- deux bandes entièrement vides, `era_8` et `era_10`, dues au remapping provisoire vanilla vers 7/9/11/12 ;
- 181 arêtes dont l'écart absolu d'ère dépassait une bande.

Les preuves complètes par nœud figurent dans `TECH3A1_GRAPH_BEFORE.csv`. Dans cet audit, un « lien cross-era » signifie un écart absolu supérieur à une ère ; un lien entre deux ères adjacentes n'est pas compté comme long.

## 2. Corrections appliquées

### Production

- `manufacturies` : `era_7 → era_6` ; `mechanized_workshops` exige désormais aussi `manufacturies`. La composante `manufacturies/distillation` rejoint ainsi le graphe principal par une arête logique et adjacente.
- `enclosure` : `era_7 → era_6`. `intensive_agriculture` reste en `era_7`, ce qui transforme leur relation en progression entre bandes adjacentes.
- `lathe` : `era_7 → era_5` ; `crystal_glass` : `era_7 → era_6`. La chaîne devient `cotton_gin` (4) → `lathe` (5) → `crystal_glass` (6), sans modifier ses prérequis.
- La première couche topologique des groupes provisoires 9 et 11 passe respectivement en 8 et 10.

### Military

- `triage` exige désormais `standing_army` en plus de `logistics`. Cette arête de même ère fusionne la composante vanilla de neuf nœuds avec la composante principale.
- La même subdivision topologique 9→8 et 11→10 est appliquée aux seules technologies de compatibilité.

### Society

- `centralization` exige désormais `nationalism` en plus de `tech_bureaucracy`. Cette arête de même ère relie la composante administration/finance/urbanisation au graphe principal.
- `pharmaceuticals` passe de l'ère 7 à 6 et exige aussi `organized_immunization_campaigns`. La branche protégée variolisation/vaccination/immunisation rejoint ainsi la famille médicale principale par une arête 5→6.
- La même subdivision topologique 9→8 et 11→10 est appliquée aux seules technologies de compatibilité.

La subdivision systémique concerne uniquement les nœuds vanilla temporaires qui n'avaient aucun prérequis dans leur propre groupe provisoire. Elle déplace 29 frontières de l'ère 9 vers 8 et 32 frontières de l'ère 11 vers 10. Leurs dépendants de même groupe restent en 9 ou 11. La règle remplit les deux bandes vides, raccourcit les arêtes entrantes et n'introduit aucune inversion d'ère.

## 3. Technologies volontairement inchangées

- Les prérequis et ères des 118 technologies TECH-3A protégées restent identiques à l'index canonique.
- `distillation` conserve `manufacturies` et l'ère 7 ; le retiming de son parent et le nouveau pont suffisent.
- `intensive_agriculture` conserve `enclosure` et l'ère 7 ; déplacer son parent d'une bande suffit sans réécrire la chaîne chimie/agriculture héritée.
- `sericulture` reste isolée : elle est `can_research = no`, terminale et destinée à une acquisition initiale/régionale, pas à une chaîne de recherche normale.
- `mysorean_iron_cased_rocketry` reste isolée : technologie régionale/événementielle `can_research = no`, explicitement protégée.
- `military_veterinary_services` reste isolée dans la vue Military : son prérequis Society `veterinary_science` est un lien intercatégorie protégé et la technologie est terminale. Ajouter un lien militaire purement visuel serait artificiel.
- Aucune catégorie n'a été changée et aucune technologie n'a été supprimée.

## 4. Comparaison avant/après

| Mesure | Avant | Après |
|---|---:|---:|
| Technologies | 276 | 276 |
| Composantes Production | 3 (`87+2+1`) | 2 (`89+1`) |
| Composantes Military | 4 (`77+9+1+1`) | 3 (`86+1+1`) |
| Composantes Society | 3 (`65+30+3`) | 1 (`98`) |
| Composantes totales | 10 | 6 |
| Nœuds isolés dans leur catégorie | 3 | 3, tous justifiés |
| Arêtes de même catégorie | 341 | 345 |
| Degré moyen de même catégorie | 2,471 | 2,500 |
| Liens avec écart d'ère > 1 | 181 | 163 |
| Ères occupées | 10/12 | 12/12 |

Distribution finale des nœuds : ères 1–12 = `13, 6, 19, 28, 34, 23, 53, 29, 10, 32, 6, 23`.

Le registre `TECH3A1_LAYOUT_CHANGES.csv` contient les 69 technologies modifiées : 66 changements d'ère, 4 changements de liste de prérequis, avec `pharmaceuticals` présent dans les deux groupes. Aucun changement de catégorie et aucune suppression.

## 5. Validations statiques

Résultats :

- parsing structurel : 6 fichiers technology, accolades équilibrées, UTF-8 BOM conservé ;
- définitions : 276, IDs uniques : 276, doublons : 0 ;
- catégories invalides : 0 ; ères invalides : 0 ;
- prérequis manquants : 0 ; cycles : 0 ; inversions d'ère introduites : 0 ;
- technologies custom attendues : 118/118 ; mismatch avec l'index canonique : 0 ;
- prérequis custom modifiés : 0 ;
- IDs ajoutés/supprimés : 0/0 ;
- hash du contenu hors `era`, `category` et `unlocking_technologies` modifié : 0 ;
- effets/modifiers/on_researched modifiés : 0 ;
- 1 038 références de listes technologiques vérifiées dans le gameplay vanilla+mod ; références vers un ID absent : 0 ;
- changements réels non inscrits au registre : 0 ; lignes de registre sans changement réel : 0 ;
- fichiers GUI modifiés : 0.

## 6. Validation runtime

Un smoke test caché a lancé Victoria 3 1.13.9 avec le mod final. Le processus n'a pas crashé, a monté `common/technology/eras`, a poursuivi le chargement des assets et atteint les fichiers `events/tech_events`. Les journaux contiennent **0** erreur visant `common/technology`, le fichier de compatibilité ou l'un des huit nœuds ayant reçu une correction manuelle.

Le journal contient par ailleurs des doublons de localisation TECH-3A/vanilla ainsi que des erreurs de triggers dans des événements India/naval déjà hors du périmètre TECH-3A.1. Elles ne sont pas causées par ce nettoyage et n'ont pas été modifiées ici.

L'interface n'a pas atteint un état visible avant l'arrêt borné du processus. L'ouverture des trois vues, la sélection d'une technologie distante et la chaîne automatique n'ont donc **pas** été observées. La validation runtime interactive reste `NOT_RUN`, et aucune validation visuelle n'est revendiquée.

## 7. Risques restants

- Les 61 déplacements systématiques vers 8/10 abaissent le coût de recherche d'une bande pour ces technologies de compatibilité ; risque de pacing `LOW_MEDIUM`, à contrôler en jeu.
- Les quatre nouveaux prérequis modifient l'accès futur à des nœuds vanilla temporaires, mais pas leurs effets/unlocks ni l'état déjà enregistré dans une sauvegarde. Les IDs restent stables.
- 163 arêtes sautent encore plus d'une ère. Beaucoup proviennent des ponts protégés TECH-3A et du remapping post-1836 encore provisoire ; les réécrire uniquement pour l'esthétique serait hors des règles.
- L'auto-layout reste natif et non déterministe depuis les données seules : l'amélioration métrique est démontrée, l'amélioration visuelle doit être confirmée humainement aux résolutions et facteurs de scaling utilisés.

## 8. Recommandation de revue humaine

Ouvrir successivement Production, Military et Society, comparer les grandes bandes 7–11 et vérifier en priorité :

1. `manufacturies`, `distillation`, `enclosure`, `intensive_agriculture`, `lathe` et `crystal_glass` ;
2. la jonction `standing_army → triage` ;
3. les jonctions `nationalism → centralization` et `organized_immunization_campaigns → pharmaceuticals` ;
4. la lisibilité des nouvelles bandes 8 et 10 ;
5. une sélection distante et la file automatique de prérequis dans chaque catégorie.

Si la revue visuelle reste insuffisante, corriger seulement les familles encore problématiques à partir des CSV ; ne pas rouvrir la décision `USE_VANILLA_AUTO_LAYOUT` et ne pas modifier les 118 prérequis protégés sans erreur objective.
