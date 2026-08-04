# HOTFIX-6A.18R — Audit 1.13 de l'API historique des intérêts déclarés

Date : 4 août 2026

Phase : `HOTFIX_6A18R_DECLARED_INTEREST_HISTORY_API_1_13_AUDIT`

Nature : audit documentaire statique, trois voies, sans correction gameplay et
sans runtime.

## 1. Résultat

L'analyse statique ne fournit aucune preuve positive que
`add_declared_interest` soit encore enregistré comme effet script dans
Victoria 3 1.13. Le nom exact est absent des scripts, Markdown, tests, DLC et
métadonnées installés, des logs survivants, des chaînes ASCII/UTF-16 lisibles
des exécutables retail/debug et des symboles lisibles disponibles. Le dossier
vanilla `common/history/interests` est lui-même absent.

Cette preuve négative ne démontre toutefois ni la suppression formelle de
l'effet, ni l'ignorance du fichier par le chargeur, ni sa sémantique. Aucun
registre exhaustif lisible, aucune documentation 1.13 exacte et aucun
diagnostic actuel attribuable au fichier cible ne sont disponibles. L'effet
peut donc être encore valide mais inutilisé, reconnu avec une sémantique
modifiée, ou obsolète/ignoré/invalide. Le remplacement est **inconnu**.

Une seconde dette est statiquement démontrée sans trancher l'API : seulement
33 des 91 arguments actifs du fork sont encore des identifiants de région
stratégique 1.13; 58 actions, réparties sur 24 pays, utilisent 26 anciens noms
absents de `common/strategic_regions`. Cette incompatibilité de namespace ne
permet pas d'inventer un remappage et ne prouve pas comment un éventuel effet
legacy les traiterait.

Aucune correction et aucune phase suivante ne sont sélectionnées.

## 2. Branche, HEAD et préflight

| Contrôle | Résultat |
| --- | --- |
| Racine | `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork` |
| Branche | `hotfix-dlc-audit` |
| HEAD initial | `62af7245bfd1c2ffbc2a8e979b5d2455b199b650` |
| HEAD final | `62af7245bfd1c2ffbc2a8e979b5d2455b199b650` |
| Message | `Select declared interest history API audit` |
| Rapport 6A.18 dans HEAD | présent |
| Treize verdicts 6A.18 | présents |
| Changements suivis initiaux | aucun |
| Index staged initial | vide |
| `git diff --check` initial | PASS |
| Processus ciblés | aucun Victoria 3, Dowser ou launcher Paradox; Ankama ignoré |

État non suivi initial :

```text
?? bject
?? docs/research/technology/TECH_TREE_BUILDING_AND_PRODUCTION_CANDIDATES.csv
?? docs/research/technology/TECH_TREE_INDUSTRIAL_CHAINS.md
?? docs/research/technology/TECH_TREE_INDUSTRIAL_HISTORY_DEEP_RESEARCH.md
?? docs/research/technology/TECH_TREE_INDUSTRIAL_INNOVATIONS_DATABASE.csv
?? docs/research/technology/TECH_TREE_RESEARCH_BIBLIOGRAPHY.md
?? docs/research/technology/TECH_TREE_RESOURCE_CANDIDATES.csv
?? docs/research/technology/TECH_TREE_VICTORIA3_GAP_ANALYSIS.md
```

Leur contenu n'a pas été affiché, modifié, stagé, déplacé ou supprimé.

Stash protégé :

```text
stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla
518df704fa14599c0f254fae13859210663dd976
```

Son contenu n'a été ni ouvert ni appliqué.

## 3. Sources

Ont été lus avant écriture : 6A.18, 6A.17, 6A.17R et 6A.16R; la roadmap,
l'index, la matrice des blocs, l'index CSV, les trois inventaires canoniques,
le prompt courant, les changelogs complets fork/source, les logs courants et
rotations pertinentes, et les versions complètes fork/source du seul fichier
gameplay autorisé.

La recherche vanilla a couvert `common`, `events`, `map_data`,
`content_source`, `tools`, les DLC installés, les Markdown, les exemples/tests,
les localisations d'effets/triggers et les chaînes non exécutées des binaires
et symboles disponibles. Aucun exécutable du jeu ou du launcher n'a été lancé.

Les historiques pays, les fichiers gameplay géographiques du fork/source et
les périmètres Coup, Imperialism, HBC, Navigation Acts, Inde, BIC, Sepoy,
Bombay, Travancore, Japon, Russie, Autriche/Croatie/Suisse, DEI/VOC, Java,
Tanzimat, Merchant Banking, NAVY, ADMIN, révolutions, localisations générales,
descripteurs et sauvegardes sont restés fermés et inchangés.

## 4. Validation CSV

Tous les CSV ont été chargés intégralement par `Import-Csv -Encoding UTF8`.
Aucune découpe naïve sur les virgules n'a été utilisée.

| CSV | Données × colonnes avant 6A.18R | Propriétés nulles |
| --- | ---: | ---: |
| `HOTFIX_MERGE_BLOCK_STATUS.csv` | `44 × 17` | 0 |
| `HOTFIX_REPORT_INDEX.csv` | `133 × 22` | 0 |
| `HOTFIX_MERGE_THREE_WAY_INVENTORY.csv` | `541 × 21` | 0 |
| `HOTFIX_GLOBAL_DIFFERENCE_INVENTORY.csv` | `534 × 22` | 0 |
| `HOTFIX_MERGE_REMAINING_WORK.csv` | `512 × 20` | 0 |

Après documentation, la matrice reste `44 × 17`, l'index devient `134 × 22`
et les trois inventaires restent inchangés. Le conflit canonique est confirmé :
le trois-voies classe le fichier `MERGED_AND_VALIDATED`/P3 sur la preuve de
clôture Inde, tandis que les inventaires global et restant le classent
`PENDING_REVIEW`/P1 requis. Cette contradiction documentaire ne constitue pas
une preuve moteur.

## 5. Hashes et format du fichier cible

| Arbre | Octets | Lignes | Encodage | BOM | Fins de ligne | Saut final | SHA-256 |
| --- | ---: | ---: | --- | --- | --- | --- | --- |
| Fork | 4 415 | 158 | UTF-8 valide | `EF BB BF` | 158 LF, 0 CRLF/CR | oui | `A528418D3C18379C1175E6B469C0313D0AF8C7CC04E80BBE6382F72A097F5DBD` |
| Source hotfix | 4 609 | 163 | UTF-8 valide | `EF BB BF` | 163 LF, 0 CRLF/CR | oui | `0BD9ADC58439BB6F81D1B0165954E827C332CB4FCC687980055D4C6A0DF3C92A` |
| Vanilla 1.13 | absent | — | — | — | — | — | — |

Les deux fichiers ont 29 accolades ouvrantes et 29 fermantes. La racine
unique est `INTERESTS = {`, suivie de 28 blocs directs
`c:TAG ?= { ... }`. Les 91/96 effets sont directement placés dans ces scopes
pays, sans enveloppe intermédiaire. La syntaxe conditionnelle `c:TAG ?=` est
par ailleurs courante dans l'historique vanilla 1.13 (1 543 occurrences dans
1 110 fichiers), mais cela ne documente pas la signature de l'effet.

## 6. Pays et occurrences actives

Le fork et la source ont les mêmes 28 scopes et le même ordre. Le tableau
inventorie toutes les actions actives du fork; les lignes sont identiques dans
la source sauf GBR, BIC et POR, détaillés ensuite.

| Pays | Fork/source | Régions actives du fork |
| --- | ---: | --- |
| SWE | 1/1 | `region_north_germany` |
| DUR | 3/3 | `region_bombay`, `region_central_asia`, `region_central_india` |
| GBR | 11/13 | `region_france`, `region_south_china`, `region_nile_basin`, `region_occitania`, `region_indonesia`, `region_southern_africa`, `region_north_india`, `region_south_india`, `region_oceania`, `region_indochina`, `region_arabic` |
| BIC | 5/7 | `region_himalayas`, `region_persia`, `region_north_india`, `region_south_india`, `region_indochina` |
| BAV | 1/1 | `region_north_germany` |
| WUR | 1/1 | `region_north_germany` |
| DENNOR | 1/1 | `region_arabic` |
| BAD | 1/1 | `region_north_germany` |
| HAN | 1/1 | `region_south_germany` |
| SAX | 1/1 | `region_south_germany` |
| TUR | 3/3 | `region_dnieper`, `region_persia`, `region_italy` |
| RUS | 12/12 | `region_france`, `region_balkans`, `region_north_germany`, `region_south_germany`, `region_italy`, `region_anatolia`, `region_persia`, `region_arabic`, `region_baltic`, `region_japan`, `region_manchuria`, `region_rhine` |
| SIC | 2/2 | `region_balkans`, `region_zanj` |
| BEL | 1/1 | `region_iberia` |
| EGY | 4/4 | `region_north_africa`, `region_niger`, `region_zanj`, `region_congo` |
| CHL | 1/1 | `region_andes` |
| ARG | 1/1 | `region_brazil` |
| SPA | 3/3 | `region_occitania`, `region_italy`, `region_baltic` |
| CHI | 2/2 | `region_japan`, `region_indochina` |
| FRA | 7/7 | `region_england`, `region_dixie`, `region_nile_basin`, `region_indochina`, `region_senegal`, `region_danubia`, `region_zanj` |
| BRZ | 2/2 | `region_andes`, `region_gran_colombia` |
| USA | 9/9 | `region_canada`, `region_great_plains`, `region_central_america`, `region_caribbean`, `region_mexico`, `region_brazil`, `region_pacific_coast`, `region_gran_colombia`, `region_oceania` |
| AUS | 9/9 | `region_north_germany`, `region_anatolia`, `region_south_china`, `region_occitania`, `region_arabic`, `region_iberia`, `region_dnieper`, `region_zanj`, `region_ethiopia` |
| NET | 3/3 | `region_france`, `region_arabic`, `region_oceania` |
| PRU | 3/3 | `region_baltic`, `region_danubia`, `region_niger` |
| POR | 1/2 | `region_senegal` |
| DEN | 1/1 | `region_niger` |
| MEX | 1/1 | `region_great_plains` |

Il n'existe aucun scope pays dupliqué et aucun doublon du couple
`(pays, région)` dans aucun arbre.

## 7. Occurrences commentées

Les deux arbres ont exactement trois actions inactives, toutes vers
`region_oceania` : DENNOR, FRA et PRU. Elles se trouvent aux lignes fork
40/106/141 et source 44/110/145. Elles sont exclues des totaux actifs et ne
peuvent pas produire d'intérêt initial.

## 8. Régions stratégiques 1.13

Le fork possède 45 noms distincts. Dix-neuf existent encore exactement dans
le registre stratégique vanilla :

`region_andes`, `region_balkans`, `region_brazil`, `region_canada`,
`region_central_america`, `region_central_asia`, `region_gran_colombia`,
`region_great_plains`, `region_himalayas`, `region_indochina`,
`region_indonesia`, `region_nile_basin`, `region_north_africa`,
`region_north_india`, `region_oceania`, `region_pacific_coast`,
`region_south_china`, `region_south_india`, `region_southern_africa`.

Vingt-six en sont absents :

`region_anatolia`, `region_arabic`, `region_baltic`, `region_bombay`,
`region_caribbean`, `region_central_india`, `region_congo`, `region_danubia`,
`region_dixie`, `region_dnieper`, `region_england`, `region_ethiopia`,
`region_france`, `region_iberia`, `region_italy`, `region_japan`,
`region_manchuria`, `region_mexico`, `region_niger`,
`region_north_germany`, `region_occitania`, `region_persia`, `region_rhine`,
`region_senegal`, `region_south_germany`, `region_zanj`.

Le fichier vanilla `06_old_strategic_regions.txt` conserve des regroupements
historiques sous des clés différentes telles que
`geographic_region_france_old`; ses commentaires les décrivent comme
« Former ... SR ». Cette conservation géographique ne crée ni alias de
`region_france`, ni effet de remplacement. Les deux noms source-only
`region_madras` et `region_punjab` sont également absents du registre
stratégique 1.13.

Répartition des actions : fork `33` arguments présents / `58` absents;
source `29` présents / `67` absents. Les 24 pays du fork ayant au moins un
argument absent sont SWE, DUR, GBR, BIC, BAV, WUR, DENNOR, BAD, HAN, SAX, TUR,
RUS, SIC, BEL, EGY, SPA, CHI, FRA, USA, AUS, NET, PRU, POR et DEN. CHL, ARG,
BRZ et MEX n'ont que des clés stratégiques existantes.

## 9. Diff exact fork/source

Les 87 couples `(pays, région)` communs sont identiques. Le diff de paires
actives est exactement :

| Pays | Fork-only | Source-only | Delta net |
| --- | --- | --- | ---: |
| GBR | `region_north_india`, `region_south_india` | `region_punjab`, `region_central_india`, `region_bombay`, `region_madras` | -2 |
| BIC | `region_north_india`, `region_south_india` | `region_punjab`, `region_madras`, `region_central_india`, `region_bombay` | -2 |
| POR | — | `region_madras` | -1 |

Le diff physique porte donc sur 4 ajouts fork et 9 retraits source, soit un
net de 5 actions et `96 → 91`. Les « cinq cartographies protégées » de la
baseline désignent les quatre résultats fork Nord/Sud Inde (deux pour GBR,
deux pour BIC) et l'absence de Madras pour POR. Les treize lignes du diff
physique restent entièrement protégées; aucune ancienne région Inde n'est
restaurée.

## 10. Registre de l'effet et recherches vanilla

| Source de preuve | `add_declared_interest` exact | Résultat |
| --- | ---: | --- |
| Scripts `common`, `events`, `map_data` | 0 | absent |
| Markdown, exemples/tests, metadata, `content_source`, `tools`, DLC | 0 | absent |
| Localisation d'effets/triggers | 0 | absent |
| Exécutables retail/debug, ILK et autres binaires lisibles, ASCII | 0 | absent |
| Mêmes cibles, UTF-16 | 0 | absent |
| Logs survivants | 0 | absent |

Les binaires lisibles contiennent notamment `declared_interest`,
`declared_interests`, `declare_interest_command`, `create_interest_marker`,
`remove_interest_marker`, `set_interest_marker` et
`add_interest_marker_rank`. Ils contiennent aussi la signature lisible du
trigger `has_interest_marker_in_region = region scope/tag`. Les scripts et la
localisation exposent `can_have_declared_interest_here` et
`has_interest_marker_in_region`.

Ce sont des commandes, concepts ou triggers apparentés. Aucun n'est documenté
comme effet script équivalent à `add_declared_interest`, et aucune occurrence
script vanilla ne montre comment créer le même intérêt initial. Ils ne sont
donc pas des remplacements autorisables.

La recherche officielle Paradox accessible n'a fourni aucune documentation
exacte de l'effet ou de sa signature en 1.13. L'absence du nom exact dans des
chaînes lisibles est un indice de suppression/renommage, mais pas une preuve
exhaustive du registre moteur. Réponses statiques : existence exacte
**non démontrée**; scope pays accepté **non démontré par la signature**;
argument région stratégique accepté **non démontré**; remplacement
**inconnu**.

## 11. Chargement du fichier

Le dossier vanilla `common/history/interests` et son fichier sont absents. Le
nom racine `INTERESTS` et le chemin `history/interests` ne sont pas retrouvés
dans les métadonnées ou chaînes binaires lisibles. Le fork possède pourtant
une structure Clausewitz équilibrée et des scopes pays syntaxiquement usuels.

Il est donc impossible de classer positivement les 91 actions comme
« chargées » ou « ignorées ». Elles sont **potentiellement invalides** à deux
niveaux indépendants : effet non prouvé pour toutes les 91; argument
stratégique absent pour 58 si la valeur attendue est bien une région
stratégique 1.13. L'absence d'erreur actuelle ne constitue pas une preuve de
chargement ni d'exécution.

## 12. Diagnostics actuels et historiques

La session courante répartie entre `error.1.log`, `error.log` et `game.log`
contient zéro `add_declared_interest`, zéro chemin `00_interests.txt` et zéro
`common/history/interests`. Les 60 logs survivants ont été recherchés : même
résultat pour toutes les rotations.

Le manifeste initial des 60 logs compte 8 415 372 octets et porte le hash de
méthode
`948ED68191D6C350A60B61C616A77F555FFDB2C46E749EF56CFCF949DABDB744`.
Les quatre preuves courantes principales conservent les hashes publiés par
6A.18 : `error.1.log` `8C4DEE…9D88`, `error.log` `D4CB58…05F7`,
`game.1.log` `5AC79D…CA40` et `game.log` `0404C0…3F59`.

`game.3.log` contient 23 diagnostics anciens du trigger apparenté
`has_interest_marker_in_region` avec une région invalide : 2 Arabic, 1
Caucasus, 1 Dixie, 1 Italy, 1 Manchuria et 17 Persia. Ils visent d'autres
fichiers et lignes; aucun ne vise le fichier audité. Ils prouvent seulement
que ces anciens noms peuvent être rejetés par un trigger 1.13, pas comment
`add_declared_interest` se comporte.

Les 91 diagnostics cible n'existent plus dans aucun log disponible. Ils ne
sont connus que par les rapports 6A.16 à 6A.18, sans message, chemin/ligne ni
session encore vérifiables. Ils sont donc classés « preuve uniquement citée
dans les rapports », jamais « diagnostic actuel ».

## 13. Déduplication

La clé est `(session, timestamp, message, chemin, ligne)`. `error.1.log` et
`error.log` reconstruisent la session courante; `game.log` n'est pas ajouté
comme une nouvelle occurrence lorsqu'il reflète le même message. Les rotations
sont des sessions distinctes. Les 23 erreurs apparentées de `game.3.log` sont
conservées avec leur propre chemin et ligne. Le nombre documentaire 91 n'est
pas additionné aux logs actuels.

## 14. Trois hypothèses et impact

| Hypothèse | Compatibilité statique | Impact potentiel | Impact démontré |
| --- | --- | --- | --- |
| Effet encore valide mais inutilisé par vanilla | possible; absence vanilla expliquée par l'absence de besoin | 91 intérêts initiaux créés comme prévu pour 28 pays | aucun écran, registre ou log positif |
| Effet reconnu avec sémantique modifiée | possible; concepts `declared_interest` et marqueurs existent | création partielle, traitement différent des clés legacy, ou autre niveau d'intérêt | aucun |
| Effet obsolète, ignoré ou invalide | compatible avec l'absence exacte, les 91 preuves historiques et les 58 arguments legacy | tout ou partie des intérêts initiaux manque; disponibilité des actions diplomatiques réduite | aucun échec fonctionnel observé |

Si les 91 effets échouent tous, les 28 pays peuvent perdre les intérêts
déclarés supplémentaires attendus au jour 1. Les diplomatic plays exigeant un
marqueur d'intérêt, l'accès diplomatique, colonial ou militaire à certaines
régions peut être réduit. La portée maximale est donc majeure et
transversale. Elle reste `UNKNOWN_RUNTIME_IMPACT` : ni le nombre d'intérêts
réellement manquants ni une action diplomatique effectivement bloquée ne sont
démontrés.

## 15. Comparaison trois voies et classifications exclusives

| Groupe exclusif | Volume | Comparaison | Classification |
| --- | ---: | --- | --- |
| Couples actifs communs avec clé stratégique 1.13 | 29 | fork=source; vanilla sans fichier; API inconnue | `UNKNOWN_REQUIRES_REVIEW` |
| Couples actifs communs avec ancien nom absent du registre stratégique | 58 | fork=source; namespace 1.13 incompatible si l'effet attend un SR | `UNKNOWN_REQUIRES_REVIEW` |
| Cartographie GBR protégée | 2 fork-only / 4 source-only | Nord/Sud Inde contre quatre anciennes régions | `PROTECTED_CONCURRENT_WORK` |
| Cartographie BIC protégée | 2 fork-only / 4 source-only | Nord/Sud Inde contre quatre anciennes régions | `PROTECTED_CONCURRENT_WORK` |
| Cartographie POR protégée | 1 source-only | Madras volontairement absente du fork | `PROTECTED_CONCURRENT_WORK` |
| Trois lignes commentées communes | 3 | identiques et inactives | `ALREADY_MERGED` |
| Absence vanilla du fichier/chargeur documenté | 1 fichier | aucune conclusion positive possible | `UNKNOWN_REQUIRES_REVIEW` |

Les volumes actifs sont exclusifs : `29 + 58 + 4 = 91` côté fork. Les
éléments source-only ne sont pas comptés comme actions fork. Aucun groupe ne
reçoit deux classifications.

## 16. Gravité gameplay et statut de merge

| Groupe | Gravité gameplay | Statut de merge | Priorité |
| --- | --- | --- | --- |
| API/chargeur et 87 actions communes | `UNKNOWN_RUNTIME_IMPACT` (potentiel majeur) | `REQUIRES_AUDIT`, audit statique inconclusif | P1 |
| 58 arguments legacy communs | `UNKNOWN_RUNTIME_IMPACT` (risque partiel ou large) | `REQUIRES_REVIEW`, aucun remappage prouvé | P1 |
| GBR/BIC/POR | `DESIGN_ONLY` dans cet audit | `PROTECTED_SCOPE` | P0 protégé |
| Commentaires | `NO_GAMEPLAY_IMPACT` | `NON_BLOCKING` | P3 |

La gravité potentielle ne transforme pas une incertitude en défaut démontré.
Le bloc documentaire reste ouvert, mais aucune correction n'est prouvable.

## 17. Protocole futur minimal, non exécuté

Si une preuve runtime devient ultérieurement nécessaire et autorisée, un seul
protocole borné est proposé :

1. préparer hors jeu le montage exact du fork seul, vérifier son descripteur,
   le hash cible `A528418…F5DBD`, l'absence d'autre mod et un dossier de logs
   identifié;
2. sélectionner avant ouverture un couple existant `(pays non protégé, région
   stratégique 1.13)` dont les données statiques prouvent qu'il n'a aucune
   source naturelle d'intérêt; BRZ peut être candidat, mais ce prérequis doit
   être démontré avant de le retenir;
3. préparer pour le même pays un témoin négatif vers une région stratégique
   1.13 sans action dans `00_interests.txt`, également sans source naturelle;
4. ouvrir Victoria 3 une seule fois, sans BIC, GBR ni pays/périmètre Inde;
5. au jour 1 avant toute progression, relever séparément l'intérêt positif et
   le témoin négatif, leur source/type dans l'UI ou l'inspecteur autorisé, puis
   vérifier les diagnostics exacts du fichier et de l'effet;
6. fermer après ces contrôles et dédupliquer les logs par la méthode ci-dessus.

Le contrôle positif actif avec témoin négatif inactif prouverait une fonction
au jour 1. Deux absences sans diagnostic resteraient ambiguës; un diagnostic
explicite du registre ou du chemin serait requis pour conclure à l'invalidité.
Ce protocole n'est ni lancé ni demandé à l'opérateur pendant 6A.18R.

## 18. Critères d'une correction future

Une 6A.18F échoue dès les trois premiers critères : aucun effet 1.13 exact
n'est démontré, l'invalidité du legacy n'est pas démontrée par une preuve
actuelle et aucun remplacement sémantiquement équivalent n'est connu. Les 58
arguments legacy empêchent aussi de garantir pays, régions et nombre
d'intérêts inchangés. Aucun diff, hash final ou rollback de correction ne peut
donc être calculé honnêtement.

La décision est de conserver l'API historique non résolue et de ne
sélectionner aucune phase d'exécution suivante.

## 19. Documents

Documents autorisés créés ou mis à jour : ce rapport, `INDEX.md`,
`HOTFIX_REPORT_INDEX.csv`, `HOTFIX_MERGE_BLOCK_STATUS.csv` et la roadmap.
`HOTFIX_NEXT_MERGE_PHASE_PROMPT.md` reste inchangé comme preuve historique de
la sélection 6A.18. Les trois inventaires fonctionnels restent inchangés.

## 20. Contrôles finaux

La branche et le HEAD restent inchangés. Aucun fichier gameplay, loi,
localisation, descripteur ou sauvegarde n'est modifié. L'index staged reste
vide; aucun commit, merge, rebase ou changement de stash n'est effectué.
`git diff --check` passe. Les huit non-suivis initiaux restent présents. Coup,
Imperialism, HBC, Navigation Acts, BIC, Inde, NAVY, ADMIN, Tanzimat et tous les
périmètres protégés restent inchangés. BIC n'est pas rouvert et aucune
restauration de `law_colonial_exploitation` n'a lieu. Aucun processus Victoria
3, Dowser ou launcher Paradox n'est actif. Le manifeste des logs reste
inchangé; aucun runtime et aucun nouveau log ne sont produits.

## 21. Verdicts finaux

```text
HOTFIX_6A18R_DECLARED_INTEREST_HISTORY_API_1_13_AUDIT_COMPLETE
DECLARED_INTEREST_HISTORY_THREE_WAY_COMPARISON_COMPLETE
DECLARED_INTEREST_EFFECT_REGISTRY_AUDITED
DECLARED_INTEREST_COUNTRY_AND_REGION_SCOPES_CLASSIFIED
DECLARED_INTEREST_PROTECTED_MAPPINGS_SEPARATED
NO_GAMEPLAY_CHANGED
NO_RUNTIME_REQUIRED
NO_AUTOMATIC_COMMIT
STASH_NAVY_3C_3_INTACT
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
DECLARED_INTEREST_HISTORY_API_REMAINS_UNRESOLVED
NO_NEXT_EXECUTION_PHASE_SELECTED
```
