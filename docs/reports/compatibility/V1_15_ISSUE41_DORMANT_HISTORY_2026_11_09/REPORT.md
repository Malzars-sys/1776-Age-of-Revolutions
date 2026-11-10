# Mission 41 — Historiques nationaux optionnels hérités

9 novembre 2026. **STATIC_QUALIFICATION_READY_FOR_REVIEW**. Jeu canonique consulté : Victoria 3 **1.15.0**. Aucun lancement ni résultat moteur n'est revendiqué.

## Résultat

Les quatre références signalées par l'audit 24 sont des blocs directs `c:TAG ?= { ... }` dans les historiques vanilla hérités. Leurs pays ne possèdent aucune définition effective dans le mod et ne figurent dans aucune instruction d'attribution initiale d'État. Leur absence ne justifie ni la création de quatre pays, ni l'importation de leurs lois et technologies vanilla de 1836 dans le scénario 1776.

L'audit confondait ces blocs optionnels avec des références obligatoires. Il les conserve désormais dans `optional_history_country_scopes`, avec cible, source, ligne et opérateur. Les quatre occurrences restent également visibles dans l'inventaire littéral général, qui ne prétend pas interpréter toute la portée des scripts. Aucun fichier de fonctionnement du jeu n'est modifié ou masqué.

| Cible réelle | Historique hérité | Opérateur | Décision |
| --- | --- | --- | --- |
| BKH | `common/history/countries/bko - bukey orda.txt:2` | `?=` | Conserver ; classer comme absence optionnelle |
| MNL | `common/history/countries/mnl - mingrelia.txt:2` | `?=` | Conserver ; classer comme absence optionnelle |
| SVN | `common/history/countries/svn - svaneti.txt:2` | `?=` | Conserver ; classer comme absence optionnelle |
| TKI | `common/history/countries/tki - tarki.txt:2` | `?=` | Conserver ; classer comme absence optionnelle |

Le nom du premier fichier contient BKO, mais son bloc et la définition native utilisent BKH : aucun renommage n'est effectué sur la foi du nom de fichier.

## Changement et limites

Seul `tools/compatibility/issue24_map_dlc_audit.py` est corrigé ; un outil de qualification en lecture seule est ajouté dans le même répertoire. La copie antérieure de l'auditeur, ses résultats d'origine et le patch sont conservés ici.

L'exception est structurelle et étroite : une clé `c:TAG`, l'opérateur `?=`, une valeur bloc et une définition absente, dans le parcours des historiques nationaux/globaux. Elle n'emploie aucune liste blanche de pays. Un appel obligatoire avec `=`, une référence de propriétaire initial ou un appel obligatoire imbriqué restent signalés. Aucune condition englobante n'est interprétée comme autorisation de supprimer une erreur.

Le parcours élargi des consommateurs non-journaux trouve **13 positions de référence dans sept fichiers hérités**, sans consommateur local : quatre blocs d'histoire ; huit positions dans quatre conditions de gouvernement/régence contenant chacune `exists = c:TAG` et une comparaison ; un appel optionnel dans un déclencheur d'IA. Ces neuf dernières positions sont conservées comme contexte, sans modifier ou certifier leur exécution. L'IA appartient au suivi 25 de Hawk. Les journaux 39, cultures 40 et arbitrages historiques restent hors mission.

Il s'agit d'une qualification du contrôle statique, et non de la correction d'un plantage reproduit. La présence de `?=` et son traitement comme garde optionnel sont analysés à partir de la syntaxe et des exemples canoniques installés ; aucun essai moteur ne certifie ici leur comportement. Les recherches documentaires externes n'ont fourni aucune page accessible à citer ; aucune preuve externe inexistante n'est revendiquée.

## Vérifications effectives

- **21/21 contrôles de qualification** réussis, dont l'identité de toutes les autres données de l'audit avant/après.
- **13/13 cas de régression** réussis : absence optionnelle/obligatoire, cible présente, pays arbitraire, scalaire, commentaire, texte cité, appel imbriqué, propriétaire initial, lignes et erreur de syntaxe.
- **4/4 contrefactuels** : remplacer en mémoire `?=` par `=` sur chacun des quatre blocs rétablit correctement une alerte obligatoire. Aucun témoin n'est installé dans les données actives.
- Audit complet avant : quatre `unresolved_countries` et 14 candidats d'attribution multiple ; après : quatre absences optionnelles explicitement listées et les **mêmes 14 candidats**. Résultat global toujours `FINDINGS_STATIC_ONLY`, sans certificat général de compatibilité.
- Inventaires inchangés : **1 074 définitions de pays, 646 propriétaires initialement mentionnés, 783 régions d'État, 324 cultures**. Aucune cible du lot n'apparaît dans les instructions de création des États.
- Contrôle vanilla séparé : **835 définitions de pays**, les quatre cibles présentes, aucune absence optionnelle ou erreur de parsing ; les 59 candidats d'attribution multiple du contrôle restent visibles.

Consulter `SOURCE_PROTECTION.json` pour les empreintes finales des **2 956 fichiers de fonctionnement préexistants**, l'index et HEAD. Les empreintes des fournisseurs des audits mod/vanilla sont également revérifiées. Aucun accès Git d'écriture ni changement du vanilla.

## Reproduction

Depuis la racine, avec le Python disponible :

```text
python -B tools/compatibility/issue24_map_dlc_audit.py --skip-pixels --output docs/reports/compatibility/V1_15_ISSUE41_DORMANT_HISTORY_2026_11_09/MAP_RECHECK_NEW.json
python -B tools/compatibility/issue41_dormant_history_audit.py --output docs/reports/compatibility/V1_15_ISSUE41_DORMANT_HISTORY_2026_11_09/QUALIFICATION_RECHECK_NEW.json
```

Utiliser un nouveau nom de sortie à chaque exécution. Le second outil contrôle les captures `MAP_BEFORE.json` et `MAP_AFTER.json` de cette livraison et vérifie que leurs fournisseurs n'ont pas dérivé ; une modification concurrente peut donc volontairement le faire échouer. Ne pas remplacer les preuves pour masquer cet échec.

Le protocole moteur reste séparé dans `RUNTIME_PROTOCOL.md`. La mission est prête pour revue de la qualification, reste ouverte et ne valide pas automatiquement les missions 24/25.
