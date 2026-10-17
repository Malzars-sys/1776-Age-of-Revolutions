# MAP-2L — noyau de Minden appliqué, Ravensberg différé

14 octobre 2026. **PASS_STATIC_ENGINE_DEFERRED : 381/381 contrôles**. Le test manuel déclaré ensuite par le joueur concerne les territoires inspectés des lots précédents ; ce sous-lot n'est pas présenté comme testé en jeu.

## Modifications effectives

Dans `STATE_HANNOVER` (State_ID **69**), deux provinces initialement HAN sont subdivisées :

| Parent RGB | Avant | Portions transférées | Après |
|---|---|---|---|
| `xBBA504` | HAN, 108 cellules | `xBBA504`, 69 cellules du noyau de Minden | PRU 69 ; HAN 39, `xEDAA02` et `xEDAA03` |
| `x165E05` | HAN, 174 cellules | `xEDAA00` 5 et `xEDAA01` 2 cellules du même noyau | PRU 7 ; HAN 167, ancien RGB conservé |

**76 cellules HAN → PRU, quatre nouveaux RGB `xEDAA00`–`xEDAA03` ; 46 cellules recolorées.** Tous les pixels hors des deux masques sont inchangés. Il ne s'agit pas de livrer l'ensemble de Minden et Ravensberg à partir de deux noms de hubs.

Minden relève de Brandebourg-Prusse depuis le règlement de 1648, puis de son administration commune avec Ravensberg à partir de 1719 : [notice territoriale LWL](https://www.lwl.org/westfaelische-geschichte/portal/Internet/finde/langDatensatz.php?urlID=108&url_tabelle=tab_websegmente). Le diocèse ecclésiastique beaucoup plus étendu n'est pas utilisé comme frontière politique. Aucun pays indépendant Minden/Ravensberg, aucune annexion anticipée de 1802 ou 1815.

Les enveloppes conservatrices suivent les zones nommées sur la carte de Schenk 1710/1730 déjà conservée ; ce document plus ancien n'est pas adopté automatiquement pour toute souveraineté de 1776. Matrice régionale à quatre correspondances approximatives, conservée dans `TRACING.json` ; lecture des symboles documentée dans `*_READING.png` et tracés dans `SK_OVERLAY.png`.

## Approximations et parties non transférées

Le rapprochement du jeu et de la carte ancienne n'est pas un géoréférencement physique certifié. Résidus des locators : Osnabrück 2,26 px, Bielefeld 7,43 px, Minden 0,89 px, Paderborn 4,28 px. Contrôle Münster non utilisé dans l'ajustement : 3,12 px. Ce contrôle n'est pas un relevé de terrain indépendant. Aucun déplacement de sept pixels ou de locator n'est effectué.

L'enveloppe de Ravensberg examinée ne coupe **aucune cellule des deux parents admissibles**. Aucun transfert de Ravensberg n'est donc revendiqué. Le hub Bielefeld reste sur la portion HAN : le corriger seul en forçant une frontière serait injustifié. Les franges laissées HAN ne sont pas certifiées historiquement. Herford, Osnabrück, Schaumburg, les parents voisins et les parties méridionales du comté restent à résoudre séparément.

## Conservation et intégration

**33 956 habitants réalloués**, sans création : north_german par défaut 27 816, north_german catholiques 5 786, ashkenazi 236, dutch 118. Chaque profil est réparti une seule fois depuis la subdivision HAN intégrale figée avant ce sous-lot, par pondération de surface ; ce n'est pas un recensement historique propre à Minden. Population mondiale inchangée : **835 804 980**.

Tous les fichiers de bâtiments, niveaux, méthodes de production, propriétaires économiques, unités et recrutements restent inchangés. HAN et OLD conservent leurs subdivisions ; PRU reçoit une nouvelle subdivision dans la même région économique. Aucun gouvernement, loi, technologie ou capitale de pays n'est changé.

Les hubs gardent leur position et leur RGB : bois Minden `xBBA504` sur PRU, mine Bielefeld `x165E05` sur HAN. State_ID, ressources et prime_land inchangés. Terrains hérités des parents. Registre **423 → 427 RGB**, empreinte impériale **62 580 cellules** inchangée. Textes impériaux dépendants et cartes principale/journal régénérés.

Les vingt RGB et 1 081 cellules du lot précédent sont contrôlés intacts ; Belgique, Franconie, Mayence, Milan, mécanismes impériaux et autres modifications existantes sont conservés. Erfurt–Eichsfeld et Souabe ne sont pas modifiés.

Fichiers : `PLAN.json`, `IMPERIAL_FILES.json`, `TERRITORIAL_CHANGES.csv` détaillent chaque changement ; bitmap, terrains, historiques states/pops, régions, registre, sept textes compilés et textures. Outils indépendants : `tools/map2l_minden_ravensberg.py` et `tools/validate_map2l_minden_ravensberg.py`. La chaîne des migrations exactes est étendue, sans liste blanche de modifications arbitraires.

## Vérification

381/381 contrôles statiques ; dix tests unitaires des migrations ; carte native 16/16 hors moteur (helper HLSL uniquement). Même liste de **44 RGB doublement attribués et 12 erreurs de référence héritées**, aucune nouvelle régression. HEAD/main/origin/main restent sur le commit autorisé `f34a6b8`, sans staging dans le workspace.

À vérifier dans une nouvelle partie : subdivision PRU de Minden, frontières des trois fragments, populations locales, recrutement et bâtiments HAN conservés, registre/restitution et journal. Les nouveaux fragments de 2 et 5 cellules suivent le masque existant sans agrandissement ; vérifier leur lisibilité à la résolution du jeu.

Recherche : zéro appel ColGrep, chemins/outils déjà connus ; carte réutilisée, une vérification historique institutionnelle ciblée. Aucune économie de quota exacte ni consommation instrumentée de tokens revendiquée. Pas de reconstruction de l'index.
