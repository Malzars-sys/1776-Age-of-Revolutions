# Bibliothèque des rapports hotfix

Cette bibliothèque conserve les audits, corrections, tests runtime, manifestes et clôtures du hotfix. Les documents sont classés d’abord par région, puis — pour l’Inde — par sujet.

- [Index global](INDEX.md) : navigation synthétique, rapports canoniques et états ouverts.
- [Inde](india/README.md) : vue régionale et chaîne Sepoy complète.
- [Japon](japan/README.md) : Sakoku, Tenpo, Ryukyu, Hokkaido/Ezo, Iwakura et Zaibatsu.
- [Mamluk Iraq](mamluk_iraq/README.md) : IR1, Ottomans, Perse et objectif secret.
- [Transversal](shared/README.md) : audit upstream et lois partagées.
- [`_index/`](_index/) : catalogue CSV, carte des déplacements, dépendances et audits de réorganisation/retrait.

`_index/` est réservé aux index globaux actifs. Les rapports militaires vivent dans [`runtime/military/`](runtime/military/) et les rapports 6A avec leurs CSV compagnons dans [`global_script/`](global_script/). Les anciennes mentions de chemins `_index` restent dans les manifestes historiques, mais ne constituent pas des destinations canoniques actuelles.

## Région, sujet et type

La région indique le périmètre géographique principal. Le sujet regroupe une fonctionnalité cohérente. Le type distingue notamment `STATIC_AUDIT`, `STATIC_SETUP`, `CORRECTION_REPORT`, `RUNTIME_TEST`, `FORENSIC_AUDIT`, `MANIFEST`, `RESULTS` et `CLOSURE`.

Pour trouver la dernière validation d’une fonctionnalité, partir de [INDEX.md](INDEX.md), puis suivre le rapport marqué `FINAL` ou `CURRENT` et son éventuel compagnon CSV. Le catalogue exhaustif est [`_index/HOTFIX_REPORT_INDEX.csv`](_index/HOTFIX_REPORT_INDEX.csv).

## Statuts historiques

- `FINAL` : résultat final du périmètre testé.
- `CURRENT` : référence active sans clôture régionale ultérieure.
- `SUPERSEDED` : étape remplacée par une correction ou validation ultérieure.
- `INTERMEDIATE` : étape utile de la chaîne, mais non canonique.
- `FAILED_TEST`, `INCONCLUSIVE` ou `BLOCKED` : preuve historique d’un échec, d’une incertitude ou d’un blocage.
- `REFERENCE` : audit ou cartographie toujours utile comme contexte.

Les anciens rapports sont conservés comme preuves historiques : leurs verdicts ne sont jamais réécrits. Un déplacement exige la mise à jour des index et la validation des liens. Les CSV compagnons restent dans le même dossier que leur Markdown.

`docs/research/technology/` est explicitement hors de cette bibliothèque.
