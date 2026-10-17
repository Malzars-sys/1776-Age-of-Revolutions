# HRE-CENTRALIZATION-01

> État initial conservé ci-dessous. Le retour utilisateur [FEEDBACK_R1](FEEDBACK_R1/REPORT.md) remplace les anciens taux et règles d’autonomie : État15 %, Électorat10 % ; réduction du Lien vers l’un des deux statuts selon la dignité électorale, augmentation vers le Lien sans indépendance. Les anciennes attestations statiques ne certifient pas ces nouveaux effets en jeu.

## Installé

Un seul **Lien impérial** reste défini dans la liste des types de sujets. L’ancienne deuxième définition « terre de la couronne impériale » est retirée. Son identifiant de pacte est conservé comme alias interne, sans nouveau type ni nouvelle ligne, pour limiter les références cassées. La compatibilité de sauvegardes déjà centralisées reste à tester.

Deux types distincts sont ajoutés : **État impérial** (`subject_type_imperial_estate`,10%) et **Électorat impérial** (`subject_type_imperial_elector`,5%). Ils conservent gouvernement, lois, souverain et couleurs. Ils utilisent un paiement natif unique et les obligations militaires natives des sujets non autonomes. Aucune conversion générale n’est activée au démarrage. Les types apparaissent dans le tableau de comparaison, mais ne sont pas attribués automatiquement aux pays.

Les noms, variantes `_no_icon`, concepts, descriptions et suffixes de notifications sont fournis en français et anglais. Les mots ouvrant des infobulles utilisent de vrais concepts du jeu, pas une simple coloration orange. Les descriptions expliquent le statut, la diplomatie, la guerre, les contributions et les privilèges sans vocabulaire de développement.

Les dernières consignes graphiques priment : bannière à médaillon rouge aux trois couronnes pour l’électorat ; grande couronne avec aigle pour l’État impérial. Les maîtres transparents et les textures128px sont dans [la liste des fichiers](IMPLEMENTED_FILES.md). Les [prompts de détourage](ASSET_PROMPTS.md) précisent la méthode intégrée utilisée.

## Verrous et succession

Les trois anciens boutons de conversion/annexion générale sont verrouillés dans l’interface ET leurs effets. L’ancienne annexion de tous les membres, électeurs compris, n’est plus exécutable par ces effets. Les principes, le bloc, le registre, les rétrocessions et les institutions sont conservés. Aucun arbre de réformes supplémentaire n’est créé.

Les deux types sont initialement non annexables : aucune chaîne de changement d’autonomie, `annex_on_country_formation=no`, gardes sur annexion, unification et réduction d’autonomie. Les interactions natives de prise d’État n’incluent pas ces types dans leur liste autorisée. Cela ne garantit pas une inviolabilité contre tout script ou toute conquête étrangère : voir [les limites](ENGINE_LIMITATIONS.md).

La dignité impériale reste élective. Les privilèges électoraux peuvent être accordés/révoqués par des effets autorisés centralisés, entre deux scrutins, puis synchronisés avec le type de sujet. Aucune scrutation quotidienne supplémentaire.

Le transfert de suzeraineté est préparé dans un **compagnon isolé, non activé**, avec armement explicite par console. Dans le mod principal, une élection impliquant des sujets impériaux natifs reste en attente plutôt que de changer de couronne avec des dépendances incohérentes. Les élections de la partie1776 sans ces sujets continuent par le chemin existant. La fiabilité du prototype doit être vérifiée avant toute conversion générale.

## Vérifié

- 254/254 contrôles statiques.
- 21/21 tests nouveaux, dont 16 contrats statiques et 5 modèles Python de transitions. Les modèles n’exécutent pas le moteur.
- 11/11 tests historiques MAP2R passent ; les dix échecs de snapshots plus anciens restent identiques à ceux déjà documentés par MAP2R. Aucun nouveau test en échec, aucune erreur d’exécution des suites.
- Historiques, propriétaires, pays, populations, bâtiments, PM, propriétaires économiques, unités, diplomatie initiale et registre identiques à la baseline immédiate. Population mondiale835801255 ;44 doublons RGB et12 références invalides préexistants inchangés.
- Aucune modification de l’installation du jeu, de HEAD ou de l’index. Aucun commit, merge ou push.

**Statut : STATIC_PASS_RUNTIME_PENDING. Aucun test moteur effectué.** Affichage, prélèvement réel, guerre, annexions et succession attendent les essais détaillés dans [RUNTIME_TEST_PLAN.md](RUNTIME_TEST_PLAN.md). Ne pas qualifier cette livraison de PASS_RUNTIME_USER_VALIDATED.

## Recherche locale

Une tentative ColGrep a échoué sur le verrou d’index, puis un appel local a abouti. Il a notamment retrouvé `tools/map2k_imperial_principles.py:240–251`, vérifié directement, ainsi que les drapeaux électoraux et valeurs de vote. Les fichiers vanilla ont été lus directement. Aucun modèle ou paramètre d’intégration changé ; aucune économie exacte de quota mesurée.
