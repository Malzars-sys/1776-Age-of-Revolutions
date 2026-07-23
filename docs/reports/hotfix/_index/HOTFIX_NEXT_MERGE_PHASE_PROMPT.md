# Phase HOTFIX-6A.3 — Audit ciblé DEI

FORK : `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork`

SOURCE HOTFIX, LECTURE SEULE : `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source`

VANILLA 1.13, LECTURE SEULE : `C:\Games\Victoria 3 The Great Wave\game`

## Verdicts d’entrée

- `AUSTRIA_CROATIA_WEST_SWITZERLAND_TARGETED_FIX_COMPLETE`
- `RUSSIA_SUBJECTHOOD_ALIGNMENT_COMPLETE`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`
- `NEXT_MERGE_BLOCK_IDENTIFIED`

## Objectif unique

Effectuer un audit trois voies ciblé du setup DEI afin d’identifier les deltas hotfix encore légitimes, déjà intégrés, obsolètes sous vanilla 1.13 ou incompatibles avec le fork 1776 et les phases NAVY. Cette phase est en lecture seule : aucun gameplay ne doit être modifié.

## État Git requis

Exiger branche `hotfix-dlc-audit`, zéro staged, stash MARATH intact, `docs/research/technology/` intact et aucun processus Victoria/launcher. L’arbre peut contenir le paquet non committé 6A.2F/6A.2F2 et ses documents autorisés; toute autre collision donne `BLOCKED_CONCURRENT_WORK_COLLISION`.

Ne faire aucun reset, restore, checkout de fichier, clean, stash apply/pop/drop ou commit automatique. Ne pas inspecter le contenu du stash.

## Paquet 6A.2 protégé

Ne modifier aucun des six fichiers gameplay déjà ouverts par 6A.2F/6A.2F2 :

- `common/history/states/00_states.txt`;
- `common/history/pops/01_south_europe.txt`;
- `common/history/buildings/01_south_europe.txt`;
- `common/history/diplomacy/00_subject_relationships.txt`;
- `common/history/military_formations/00_military_formations_europe.txt`;
- `common/history/pops/00_west_europe.txt`.

Préserver notamment les 30 000 habitants de Suisse orientale autrichienne, l’administration navale croate niveau 3, le shipyard niveau 2, la flotte 1+3, Agram 24 et les transferts territoriaux.

## Sources à lire

Lire les rapports C1AI, roadmap, inventaire global, statut des blocs, audit upstream DLC, rapport 6A.2F2 et rapports NAVY concernant DEI/VOC. Rechercher les lignes DEI exactes dans l’inventaire canonique avant d’ouvrir des fichiers supplémentaires.

## Audit trois voies

Comparer uniquement les fichiers DEI identifiés entre fork, source hotfix et vanilla 1.13. Pour chaque delta, consigner :

- chemin et hunk exact;
- valeur fork, hotfix et vanilla;
- preuve changelog ou fonctionnelle;
- dépendances pays, états, bâtiments, pops, diplomatie, formations, lois, technologies et localisation;
- chevauchement NAVY/ADMIN/BIC/Travancore/MARATH;
- classification et priorité;
- correction minimale éventuelle et rollback.

## Protections absolues

Ne pas modifier NAVY, BIC, Travancore, Inde close, Japon, Mamluk Iraq, Russie, localisations françaises, descripteurs, launcher, sauvegardes ou recherches technologiques. Conserver `activate_law = law_type:law_frontier_colonization` et ne jamais restaurer `law_colonial_exploitation`.

Ne pas confondre un fichier hotfix identique à vanilla avec un delta custom requis. Aucun remplacement complet de fichier global n’est autorisé.

## Livrables

Créer un rapport `docs/reports/hotfix/_index/HOTFIX_6A3_DEI_TARGETED_AUDIT.md` et, si plusieurs deltas existent, une delta map CSV dédiée. Mettre à jour uniquement les index et roadmap canoniques nécessaires. Aucun runtime pendant cet audit.

## Verdicts attendus

Publier un verdict par delta parmi :

- `ALREADY_MERGED_EQUIVALENT`;
- `REQUIRED_HOTFIX_DELTA`;
- `INTENTIONAL_1776_DIVERGENCE`;
- `VANILLA_1_13_ALREADY_PROVIDES`;
- `OBSOLETE_HOTFIX_CONTENT`;
- `NAVY_PROTECTED`;
- `ADMIN_PROTECTED`;
- `UNVERIFIED`.

Verdict de phase si l’audit est complet : `HOTFIX_6A3_DEI_TARGETED_AUDIT_COMPLETE`. Ne publier un prompt de correction que pour des hunks exacts dont les blockers sont explicitement résolus.

## Vérifications finales

Exécuter `git diff --check`, `git status --short`, les listes/statistiques de diff, staged vide et `git stash list`. Confirmer que zéro gameplay supplémentaire a changé, que les processus sont fermés et que les protections 6A.2 restent intactes. Ne pas committer automatiquement.
