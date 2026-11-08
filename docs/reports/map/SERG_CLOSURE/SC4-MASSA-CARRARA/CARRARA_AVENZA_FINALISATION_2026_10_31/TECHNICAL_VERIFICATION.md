# Vérifications techniques et conservation — 31 octobre 2026

## Exécutions nouvelles

| Ensemble | Résultat actuel | Preuve |
| --- | --- | --- |
| Contrôles ciblés de la carte et du suivi | **44/44 PASS** | `SCOPED_STATIC_RESULTS.json` |
| Tests existants Massa-Carrare | **10 PASS, 1 FAIL sur 11** | `EXISTING_TEST_RESULTS.json`, journal brut |
| Tests canoniques du suivi | **27 PASS, 1 SKIP sur 28 cas**, aucun échec | Même JSON et journal du validateur |
| Validateur canonique | **PASS**, 93/235, 39,57 %, 32/81 tâches qualifiées | `CANONICAL_CHECK.json` ; contrôle répété après l'actualisation documentaire |
| Moteur Victoria 3 | **NON EXÉCUTÉ** | Aucun nouveau reçu ni résultat moteur revendiqué |

Les anciens **134/134**, **411/416** et **11/11** de la livraison initiale sont des preuves historiques consultées. Ces suites cumulatives anciennes ne sont pas présentées comme réexécutées aujourd'hui.

Les 44 contrôles couvrent le bitmap réel, les listes exactes des huit et 108 cellules, les définitions et propriétaires uniques, les quatre simulations de découpe, la connexité locale et celle des 444 cellules MOD avant simulation, l'absence de perte, les effectifs mondiaux et les inventaires nationaux, les voisins MOD/GEN/LUC/TUS/PAR, le titre MCA unique et les neuf électeurs. Les scripts ciblés de carte, POPs, bâtiments et constitution passent l'analyse syntaxique. Aucune simulation de candidat n'est écrite dans le mod.

Population mondiale actuelle : **837 328 654 avant et après**, delta zéro. MCA/Émilie reste 10 000, le groupe MOD/Émilie reste 495 752. Ces valeurs sont nouvelles observations du workspace ; l'ancien total mondial de la passe initiale n'est pas réutilisé.

## Échec historique conservé

`test_current_chain_retains_salzburg_before_massa` attend que les deux derniers lots soient Salzbourg et Massa. La chaîne contient désormais les lots ultérieurs Ortenbourg et Teschen. C'est une attente de dernière couche devenue obsolète, pas une régression de Massa. Le test et sa trace restent intacts ; aucune réécriture pour afficher 11/11. Les dix autres contrats passent, dont les refus d'annexer Lucques, de transférer tout le parent, de changer le hub de Parme ou de créer une validation humaine.

Le SKIP canonique concerne le contrôle d'absence de modifications de l'état initial, déjà désactivé par la suite elle-même pour les évolutions autorisées. Aucun test du moteur, aucun emploi, PIB, rendement ou condition de construction n'est inféré de ces tests.

## Copie isolée et fins de ligne

La mission travaille sur `codex/sc4-massa-carrara-finalisation-20261031`, depuis `52c42808`. Le checkout isolé ne copie pas les modifications diplomatiques non commises du répertoire principal ; celles-ci sont inventoriées dans le baseline et restent intactes. La vérification des fichiers effectivement joués du répertoire principal est distincte de cette vérification du checkout, avec empreintes comparées avant publication des documents.

Le premier contrôle canonique du nouveau checkout a signalé quatre empreintes différentes dans l'ancien audit global. Le diagnostic prouve une conversion automatique LF vers CRLF du checkout : contenu normalisé identique, octets originaux encore présents à l'identique dans le répertoire principal et dans HEAD. Seules ces fins de ligne ont été ramenées aux octets canoniques, sans changer les textes, reçus ou dates. Résultat initial et quatre diagnostics conservés dans `WORKTREE_EOL_PREFLIGHT.json`. Le baseline de mission est ensuite capturé sur ces originaux conformes. Aucun manifeste historique n'a été ajusté pour masquer une différence.

## Reproduction

Depuis la racine de cette copie de travail :

```powershell
& 'C:\Users\simeo\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -B -X utf8 docs/reports/map/SERG_CLOSURE/SC4-MASSA-CARRARA/CARRARA_AVENZA_FINALISATION_2026_10_31/verify.py tests
& 'C:\Users\simeo\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -B -X utf8 docs/reports/map/SERG_CLOSURE/SC4-MASSA-CARRARA/CARRARA_AVENZA_FINALISATION_2026_10_31/verify.py scoped
```

Le vérificateur écrit seulement les nouvelles preuves de ce dossier. Aucun ancien installateur, générateur impérial ou réécrivain d'anciennes preuves n'est lancé. Les tests ont été exécutés avant l'ajout de l'événement documentaire ; le validateur et les contrôles de conservation du suivi sont revérifiés après cet ajout. Le gameplay reste identique dans les deux cas.

Les opérations Git réalisées pour isoler le travail sont la création du worktree et de la branche dédiée, expressément demandée. Aucun staging, commit, push, merge, reset, rebase ou modification du vanilla dans cette passe. Pas de PR fonctionnelle : aucun correctif ne justifie encore sa création.


## Vérification du répertoire principal du mod

Après les tests de la copie isolée, **15/15 contrôles de conservation** passent également dans le répertoire principal : propriétaires, POPs, bâtiments et unités des six pays ciblés, total mondial et dix dépendances fonctionnelles correspondent à la version vérifiée. Les fins de ligne du checkout sont normalisées uniquement pour cette comparaison de texte ; le bitmap est comparé octet par octet. Les modifications diplomatiques locales inventoriées au départ restent inchangées. Seuls ce nouveau dossier et les cinq vues/fichiers de suivi SERG ont été publiés dans le répertoire principal ; aucun fichier de gameplay. Le validateur canonique y donne PASS, 93/235 et 39,57 %. Preuves : `PRIMARY_WORKSPACE_CHECK.json`, `PRIMARY_PUBLICATION_CHECK.json`, `WORKSPACE_CONTEXT.json`.
