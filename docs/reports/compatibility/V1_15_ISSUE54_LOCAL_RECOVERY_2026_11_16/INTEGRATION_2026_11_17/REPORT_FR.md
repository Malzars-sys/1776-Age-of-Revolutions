# Issue 54 — COMPACT appliqué au mod principal

Statut : **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Le correctif mesuré est installé localement. Son application a été explicitement autorisée par le joueur : « Je t'autorise. », en réponse à la question portant sur les deux changements du mod principal.

## Modification effectivement appliquée

Seules les deux expressions de visibilité de `gui/tech_tree.gui` sont remplacées par celles de COMPACT : filtres des lignes et des cartes de technologie. Aucun autre bloc du GUI n'est modifié. Les définitions historiques, coûts, prérequis, déblocages, technologies initiales et données économiques restent inchangés.

L'empreinte du fichier installé est **94fb72b75640fe1c8bbde01af235993225dff662d11974c8a267eaeca85ff9c0** : le fichier est identique octet par octet au candidat mesuré dans les deux passages COMPACT. L'encodage et les fins de ligne d'origine sont conservés. La différence Git comprend deux lignes retirées et deux ajoutées.

Une copie intégrale du fichier précédent est conservée dans `tech_tree.before.gui`, empreinte **d71f1b66cc5e939ba14e4cb50a95bb19a7cc2ee7f2126d887da3efec2d3d78ce**. Ce fichier n'a pas été utilisé pour restaurer d'autres données. Aucun changement concurrent n'a été écrasé : le contenu courant a été vérifié immédiatement avant l'écriture.

## Vérifications après application

- Le vérificateur de visibilité lancé sur le GUI principal passe 1168 cas et ses deux témoins négatifs : 291 technologies, 392 connexions, quarante alias masqués et deux cartes forcées conservés. Voir `VISIBILITY_AFTER.json`.
- `git --no-optional-locks diff --check -- gui/tech_tree.gui` réussit. Le contrôle ne réalise aucune écriture Git.
- Les empreintes immédiates avant/après des 4070 fichiers surveillés du dépôt ne changent que pour `gui/tech_tree.gui`. L'index Git et les travaux non commités existants sont préservés.
- Les quatre-vingts fichiers surveillés du profil normal et des sauvegardes sont identiques avant/après. Aucun réglage, playset, ancienne base ou sauvegarde n'a été réinstallé ou remplacé.
- Les trois fichiers du chantier Russie–Petite Horde kazakhe sont inchangés. Le hotfix séparé et les installations vanilla ne sont pas modifiés.

Les reçus techniques sont `BEFORE.json`, `APPLICATION_RECEIPT.json` et `VISIBILITY_AFTER.json`. Aucune opération de staging, commit, push, fusion, changement de branche ou publication n'est effectuée.

## Portée des observations en jeu

Les essais déjà acquis portent sur le candidat maintenant installé, en Steam 1.15.1 sans DLC de gameplay : valeurs stationnaires déclarées de 25–34 FPS pour COMPACT, contre 5–8 pour les témoins. Le joueur n'a remarqué aucun problème de technologies, liens ou boutons pendant ces essais. Les détails et limites restent dans [le bilan des mesures](../MANUAL_RESULTS_2026_11_17/REPORT_FR.md).

Le jeu n'a pas été relancé après l'application au mod principal. Le chargement avec ses playsets habituels et l'installation locale 1.15.0 avec DLC restent donc à observer séparément. L'autorisation d'application n'est pas transformée en certification exhaustive du fonctionnement, ni en nouvelle mesure de FPS ou de latence.

Le joueur peut utiliser son lancement habituel du mod. Un prochain retour peut confirmer l'affichage des trois branches, les liens et la sélection de recherche sur cette version installée. La latence exacte d'ouverture reste non mesurée. Aucun autre essai expérimental n'est appliqué automatiquement.
