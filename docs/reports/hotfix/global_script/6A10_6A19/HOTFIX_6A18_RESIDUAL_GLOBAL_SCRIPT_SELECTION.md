# HOTFIX-6A.18 — Sélection documentaire du prochain résidu global

Date : 4 août 2026

Phase : `HOTFIX_6A18_RESIDUAL_GLOBAL_SCRIPT_SELECTION`

Branche : `hotfix-dlc-audit`

Nature : réindexation documentaire, statique, trois voies et sans runtime.

## 1. Décision

Une seule prochaine phase est sélectionnée :
`HOTFIX_6A18R_DECLARED_INTEREST_HISTORY_API_1_13_AUDIT`.

L'audit devra déterminer, sans modifier le gameplay, si les 91 effets actifs
`add_declared_interest` du fichier historique sont encore exécutés par le
moteur 1.13, puis séparer l'API commune des cinq différences de cartographie
Inde/GBR/BIC/Portugal déjà protégées. Aucune API de remplacement n'est
présumée. 6A.18 n'applique aucun hunk et ne commence pas 6A.18R.

## 2. Préflight et protections

| Contrôle | Résultat |
| --- | --- |
| Racine | `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork` |
| Branche | `hotfix-dlc-audit` |
| HEAD initial | `574492dd0b72ede2b7dd73e4dc9192947f70b419` |
| Message HEAD | `Audit Imperialism of Promise for 1.13` |
| Rapport 6A.17R dans `HEAD` | PASS |
| Dix verdicts 6A.17R dans `HEAD` | PASS, une occurrence chacun |
| Fichiers suivis au départ | propres |
| Index staged | vide |
| `git diff --check` initial | PASS |
| Processus Victoria 3/Dowser/Paradox | aucun; Ankama ignoré |

État initial exact :

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

Ces huit éléments non suivis n'ont été ni inspectés ni modifiés.

Stash avant audit :

```text
stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla
518df704fa14599c0f254fae13859210663dd976
```

Le contenu du stash n'a pas été ouvert. Aucun `git add`, reset, restore,
checkout de fichier, clean, merge, rebase, amend, commit ou changement de
stash n'a été exécuté.

## 3. Sources lues

Ont été lus intégralement avant écriture :

- 6A.17R, 6A.17, 6A.16R, 6A.16, 6A.15F, 6A.15R, 6A.14H et
  6A.14R;
- la roadmap, le prompt historique, les changelogs complets du fork et de la
  source hotfix;
- les cinq CSV canoniques, avec `Import-Csv` et sans découpage naïf;
- les versions fork et source du seul fichier cible
  `common/history/interests/00_interests.txt`, absent de vanilla;
- les trois versions de `events/trade_route_events.txt` et les définitions de
  localisation vanilla strictement nécessaires à leur provenance;
- les logs courants et rotations pertinentes.

Les historiques pays BIC/Inde/GBR/Portugal, Coup, Imperialism, HBC, Navigation
Acts, Tanzimat, ADMIN, NAVY et les localisations du mod sont restés fermés. Le
fichier d'intérêts transversal exigé a seulement servi à partitionner ses
scopes protégés.

## 4. Validation des CSV

Le parseur CSV réel confirme la baseline attendue :

| CSV | Données × colonnes avant 6A.18 | Propriétés nulles | Doublons de clé |
| --- | ---: | ---: | ---: |
| `HOTFIX_MERGE_BLOCK_STATUS.csv` | `43 × 17` | 0 | 0 |
| `HOTFIX_REPORT_INDEX.csv` | `132 × 22` | 0 | 2 groupes historiques (`S`, `INDEX`) |
| `HOTFIX_MERGE_THREE_WAY_INVENTORY.csv` | `541 × 21` | 0 | 0 |
| `HOTFIX_GLOBAL_DIFFERENCE_INVENTORY.csv` | `534 × 22` | 0 | 0 |
| `HOTFIX_MERGE_REMAINING_WORK.csv` | `512 × 20` | 0 | 0 |

Après ajout de 6A.18, les deux registres documentaires deviennent
respectivement `44 × 17` et `133 × 22`. Les trois inventaires fonctionnels
restent à `541 × 21`, `534 × 22` et `512 × 20`.

Le fichier d'intérêts illustre un conflit de métadonnées : l'inventaire trois
voies le dit `MERGED_AND_VALIDATED`/P3, tandis que les inventaires global et
restant le laissent `PENDING_REVIEW`/P1 requis. Ce conflit ne ferme pas l'API;
il justifie l'audit sélectionné.

## 5. Distribution résiduelle

6A.17R est un audit sans correction. Il ne déplace donc aucune des 161 lignes
de la couche canonique exclusive :

| Classification | Lignes |
| --- | ---: |
| `REQUIRED_HOTFIX_DELTA` | 7 |
| `VANILLA_1_13_ALIGNMENT_REQUIRED` | 15 |
| `ALREADY_MERGED` | 19 |
| `INTENTIONAL_FORK_DIVERGENCE` | 3 |
| `OBSOLETE_HOTFIX_CONTENT` | 1 |
| `POST_MERGE_DESIGN_BACKLOG` | 10 |
| `PROTECTED_CONCURRENT_WORK` | 19 |
| `UNKNOWN_REQUIRES_REVIEW` | 87 |
| **Total** | **161** |

Le legacy `PENDING_REVIEW = 161` de l'inventaire de travail est un statut de
workflow, pas cette classification exclusive. Aucun audit sans correction
n'est compté comme une fermeture gameplay.

## 6. Méthode et déduplication

Chaque candidat a été vérifié dans l'ordre demandé : dernier runtime,
parser/PostValidate, fréquence dédupliquée, appartenance au fork, objet,
impact, comparaison trois voies, convergence, hunks, dépendances, protections,
design, rollback, test futur et contribution P0/P1.

La session courante est reconstruite avec `error.1.log` puis `error.log`. Les
messages identiques de `game.log` ne sont pas recomptés. `game.1.log` est une
rotation antérieure et sert uniquement de preuve historique. Pour les rafales
de JE, la clé de déduplication est `(horodatage, pays de révolte, type de JE)`;
pour les erreurs script, c'est `(horodatage, message, chemin, ligne)`.

## 7. Diagnostics actuels et historiques

Les deux journaux d'erreur courants contiennent 6 046 lignes, dont 413 erreurs
script sur 11 emplacements distincts. Les principaux signaux sont :

| Signal actuel | Occurrences dédupliquées | Attribution |
| --- | ---: | --- |
| clé persistante vide, fichier et ligne vides | 2 408 | non bornable |
| valeur de mauvais type dans `command_values.txt:373` | 656 | vanilla/moteur |
| divisions par zéro, surtout treaty articles | 502 | vanilla/moteur |
| rafales `already has a journal entry` | 539 | quatre transferts de révolte |
| `trade_route_events.txt:28`, cible `market` invalide | 261 | fork/source/vanilla identiques |
| `31_ship_transfer.txt:56`, cible `scope` invalide | 127 | vanilla seul |
| deux chaînes navales évaluées en erreur | 88 (`44 + 44`) | base vanilla, UI NAVY |

Les 413 emplacements script comprennent aussi 14 `<unknown>:0`, deux erreurs
`metro_events.txt:9` et neuf occurrences dispersées. Aucun autre candidat
crédible P0/P1 attribuable au portage n'en ressort.

Les preuves historiques ciblées restent à 107 : 91
`add_declared_interest`, 10 Coup, 3 Imperialism of Promise et 3 Tanzimat. Les
91 et les 3 Tanzimat ne subsistent dans aucun log disponible; 10 Coup et 2
`has_role` Imperialism ne survivent que dans une rotation ancienne. L'ancien
diagnostic de pinning Imperialism est documentaire/statique.

Les logs ont conservé pendant toute la phase leurs tailles, dates et hashes :

| Fichier | Taille | Dernière écriture | SHA-256 |
| --- | ---: | --- | --- |
| `error.1.log` | 524 200 | 2026-08-03 19:42:35.989 | `8C4DEEA53F2EE1225E9EAB6B8B7D3E85C7DE234B859EDC30C548995CD3E79D88` |
| `error.log` | 103 844 | 2026-08-03 19:48:33.909 | `D4CB58ADE22D51A7749CB7408FEB401891798631A5FB9931C05623EB6AFB05F7` |
| `game.1.log` | 228 982 | 2026-08-02 20:42:13.464 | `5AC79D97DAE3B0422A0E9C905BF146C7A492E90662E2F63DD1E8CB4152CA40CA` |
| `game.log` | 216 575 | 2026-08-03 19:48:33.909 | `0404C0BC2F72EC4372AB09C6F36BC232EA95FA2133F4F5FEEE374BC364EF3F59` |

## 8. `add_declared_interest`

Le fork contient 91 effets actifs, 28 scopes pays et 45 régions distinctes
dans une racine `INTERESTS`. La source contient 96 effets actifs, les mêmes 28
scopes et les mêmes 45 identifiants distincts. Vanilla 1.13 ne contient ni ce
fichier ni une occurrence de l'effet exact dans `common`, `events` ou
`map_data`.

| Arbre | Octets | SHA-256 |
| --- | ---: | --- |
| fork | 4 415 | `A528418D3C18379C1175E6B469C0313D0AF8C7CC04E80BBE6382F72A097F5DBD` |
| source hotfix | 4 609 | `0BD9ADC58439BB6F81D1B0165954E827C332CB4FCC687980055D4C6A0DF3C92A` |
| vanilla | absent | — |

Pays : `SWE`, `DUR`, `GBR`, `BIC`, `BAV`, `WUR`, `DENNOR`, `BAD`, `HAN`,
`SAX`, `TUR`, `RUS`, `SIC`, `BEL`, `EGY`, `CHL`, `ARG`, `SPA`, `CHI`, `FRA`,
`BRZ`, `USA`, `AUS`, `NET`, `PRU`, `POR`, `DEN` et `MEX`.

Régions : `region_anatolia`, `region_andes`, `region_arabic`,
`region_balkans`, `region_baltic`, `region_bombay`, `region_brazil`,
`region_canada`, `region_caribbean`, `region_central_america`,
`region_central_asia`, `region_central_india`, `region_congo`,
`region_danubia`, `region_dixie`, `region_dnieper`, `region_england`,
`region_ethiopia`, `region_france`, `region_gran_colombia`,
`region_great_plains`, `region_himalayas`, `region_iberia`,
`region_indochina`, `region_indonesia`, `region_italy`, `region_japan`,
`region_manchuria`, `region_mexico`, `region_niger`, `region_nile_basin`,
`region_north_africa`, `region_north_germany`, `region_north_india`,
`region_occitania`, `region_oceania`, `region_pacific_coast`, `region_persia`,
`region_rhine`, `region_senegal`, `region_south_china`,
`region_south_germany`, `region_south_india`, `region_southern_africa` et
`region_zanj`.

La recherche vanilla trouve les triggers
`has_interest_marker_in_region` et `can_have_declared_interest_here`, mais
aucun effet de création équivalent démontré. Ils ne sont pas des remplacements
autorisables. L'absence du fichier vanilla ne prouve pas non plus que l'effet
legacy est invalide : seule une preuve moteur ou un test fonctionnel borné
pourra trancher.

Le diff source vers fork est exactement limité à cinq actions liées à la
cartographie close : quatre anciennes régions Inde de `GBR` et `BIC` sont
remplacées par Nord/Sud Inde, et `POR` perd l'ancien intérêt Madras. Ces cinq
sous-deltas sont `PROTECTED_CONCURRENT_WORK`; ils ne doivent jamais être
restaurés. Le groupe API commun reste `UNKNOWN_REQUIRES_REVIEW`.

Si l'effet est ignoré, les intérêts initiaux annoncés de 28 pays peuvent ne
pas être créés, avec un impact potentiel majeur sur la disponibilité des
actions diplomatiques. Aucun log actuel ni écran runtime ne démontre que cet
impact se produit. La gravité prouvée reste donc `UNKNOWN_RUNTIME_IMPACT`, le
statut `REQUIRES_AUDIT` et la priorité P1.

## 9. Coup et Imperialism of Promise

- Coup conserve 16 occurrences statiques : 10 `has_role` et 6 `is_ruler`.
  Le dernier runtime en reproduit zéro; dix diagnostics ne survivent que dans
  une rotation. 6A.16R a déjà établi les formes modernes sans satisfaire la
  condition de correction. Impact potentiel majeur, impact prouvé
  `UNKNOWN_RUNTIME_IMPACT`, statut `REQUIRES_AUDIT`; aucune nouvelle phase
  Coup n'est sélectionnée.
- Imperialism conserve zéro diagnostic actuel, deux anciens `has_role` et une
  preuve historique/statique de pinning. Pinning et API sont isolables, mais
  ruler, prominence, chef IG et vivier ne le sont pas. BIC, Inde, Sepoy,
  géographie, progression et événements utilitaristes restent protégés.
  Impact prouvé `UNKNOWN_RUNTIME_IMPACT`, statut `REQUIRES_AUDIT`; aucune
  6A.17F n'est sélectionnée.

## 10. HBC et Navigation Acts

Le runtime HBC actuel est stable et n'affiche aucune clé brute. Cela ne résout
pas la composition potentiellement incohérente de lois, gouvernement et
institutions, ni l'intention canonique de deux historiques concurrents. Le
verdict reste `HBC_DUPLICATE_HISTORY_UNKNOWN_REQUIRES_REVIEW`, gravité
`DESIGN_ONLY` actuellement prouvée et statut
`REQUIRES_HUMAN_DESIGN_DECISION` P0.

Navigation Acts conserve son infrastructure fusionnée, mais son alignement de
départ croise HBC, `chartered_company`, GBR/NAVY, BIC et l'Amérique protégée.
Le verdict reste
`NAVIGATION_ACTS_STARTING_LAW_BLOCKED_BY_HBC_DEFINITION_CONFLICT`. Son blocage
est documentaire/de design, pas un crash prouvé. Ni 6A.14HF ni 6A.14F n'est
sélectionnée.

## 11. `trade_route_events.txt:28`

L'objet exact est l'événement pays `trade_route_events.1`. Dans son trigger,
`any_market` évalue `root.market = { ... }`; quand le lien `market` de `root`
est invalide, le trigger écrit l'erreur avant qu'un effet d'événement soit
exécuté. Les 261 occurrences dédupliquées sont toutes dans la session courante.
L'hypothèse la plus compatible est un pays sans marché valide, mais le log ne
fournit pas le pays et ne permet pas de l'affirmer pour chaque occurrence.

Le fork fait 8 852 octets, SHA-256
`F82D4404C1E37AC283E8EC8A8CA0E4CC7DB2D5C1E37D3B723C08D9351DBD4B65`, et
diffère de source/vanilla uniquement dans les événements 3 à 5 sur
Isolationism/Sakoku. Le fichier source et le vanilla installé sont identiques,
8 907 octets et SHA-256
`C24E1AC42290A1181FC087EA512951117EAFD498920FD4326DB3DCFC0D25BC4E`; le groupe
fautif de l'événement 1 est identique dans les trois arbres. Aucun override ou
correctif plus récent n'est présent dans les données vanilla 1.13 installées.

Le défaut peut empêcher cette occurrence d'événement de satisfaire son
trigger pour les racines concernées; il ne prouve ni l'échec de toutes les
routes commerciales ni un défaut introduit par le portage. Le groupe ligne 28
est `ALREADY_MERGED`, gravité `DEGRADED_BEHAVIOR`, statut `NON_BLOCKING`, P2.
L'audit commercial autorisé n'est pas sélectionné devant le candidat P1.

## 12. Localisations navales

Les clés `BATTLE_SHIPS_BREAKDOWN_HEADER_ATTACKER` et
`BATTLE_SHIPS_BREAKDOWN_HEADER_DEFENDER` sont absentes du fork et de la source
parce qu'elles sont héritées de la localisation navale de base vanilla. Elles
sont bien définies en anglais et en français, ainsi que dans neuf autres
langues; elles ne proviennent d'aucun DLC. Les 44 erreurs par clé sont des
échecs d'évaluation des expressions de projection de puissance contenues dans
les chaînes, pas des clés manquantes.

L'affichage du détail attaquant/défenseur d'une bataille navale peut être
dégradé, sans risque script démontré. Gravité `UI_ONLY`, statut
`PROTECTED_SCOPE`, classification `PROTECTED_CONCURRENT_WORK`, P2. NAVY et la
localisation française restent fermés.

## 13. Avertissements JE sur les révoltes

La session contient quatre rafales dédupliquées :

| Heure | Révolte | Types de JE |
| --- | --- | ---: |
| 19:20:19 | Révolte libérale (Salvador) | 135 |
| 19:20:56 | Révolte paysanne (Pérou du Nord) | 133 |
| 19:32:07 | Révolte d'esclaves (Hadiya) | 136 |
| 19:41:36 | Révolte libérale (Bolivie) | 135 |

Total : 539 avertissements dans le flux d'erreur, reflétés dans `game.log`.
Ils ne portent aucun chemin ni ligne et couvrent jusqu'à 137 types distincts.
Cette forme correspond à un transfert générique de JE lors de la création des
révoltes. Aucune perte observable de JE n'est prouvée par les logs seuls.
Gravité `LOG_NOISE`, statut `NON_BLOCKING`; aucune JE locale n'est sélectionnée.

## 14. Tanzimat et ADMIN

- Tanzimat : la session ne contient que le chargement normal du namespace et
  de neuf événements. Les trois diagnostics techniques restent historiques.
  Sick Man est clos. L'activation 1776 reste séparément
  `OTTOMAN_TANZIMAT_1776_DEFERRED_ACTIVATION_DESIGN_BACKLOG`, gravité
  `DESIGN_ONLY`, statut `POST_MERGE_BACKLOG`. Aucune activation n'est
  sélectionnée.
- ADMIN : aucun diagnostic actuel ne cite les chemins précis des bâtiments ou
  méthodes de production. Le statut reste `MERGED_STATIC_ONLY`, gravité
  runtime inconnue et statut de merge `PROTECTED_SCOPE`. Aucun fichier ADMIN
  n'est rouvert.

## 15. Candidats supplémentaires

`common/treaty_articles/31_ship_transfer.txt:56` produit 127 liens `scope`
invalides. Le fichier n'existe ni dans le fork ni dans la source et est hérité
du vanilla 1.13 : il peut dégrader localement la validation d'un transfert de
navires, mais ne constitue pas un résidu du portage. Les deux erreurs
`metro_events.txt:9` proviennent d'un fichier strictement identique dans les
trois arbres. Les 2 408 clés persistantes vides n'ont ni fichier ni ligne.

Ces signaux, les 656 mauvais types et les 502 divisions par zéro ont été
recherchés comme candidats additionnels. Aucun n'est à la fois attribuable au
fork, isolable et crédible comme P0/P1 de ce merge.

## 16. Matrice de priorité — preuves et provenance

`0c` signifie zéro diagnostic courant; `h` désigne une preuve historique.

| ID | Domaine | Fichier | Objet/scopes | Diagnostic | Dernier runtime | Historique | Occurrences dédupliquées | Fork | Source | Vanilla | Convergence | Hunks | Dépendances | Protection |
| --- | --- | --- | --- | --- | --- | --- | ---: | --- | --- | --- | --- | ---: | --- | --- |
| DI-API | diplomatie initiale | `00_interests.txt` | `INTERESTS`, 28 pays | effet legacy possible | 0c | 91h | 0c/91h | 91 | 96 | absent | API non démontrée | 1 groupe | moteur/intérêts | sous-scopes séparables |
| DI-MAP | cartographie intérêts | même fichier | GBR/BIC/POR/Inde | diff source/fork | 0c | statique | 5 actions | modernisé | legacy | absent | non | 3 groupes pays | clôtures Inde/Portugal | oui |
| COUP | politique | deux événements Coup | 7 objets, 9 groupes | API legacy | 0c | 10h | 0c/10h | 16 statiques | divergent | moderne | partielle | 9 | lobby/scopes | oui partielle |
| IOP | JE impérialisme | `04_imperialism_of_promise.txt` | 1 objet | rôles/pinning | 0c | 3h | 0c/3h | divergent | divergent | divergent | partielle | 3 | BIC/Inde | oui |
| HBC | histoire pays | deux historiques HBC | 1 tag composé | conflit d'intention | stable | audits | 0 erreur cible | composite | doublon | lignée unique | non | multiples | lois/institutions | oui |
| NAVACT | lois initiales | chaîne 6A.14R | 5 historiques/8 fichiers | bloqué HBC | 0c | audits | 0c | partiel | custom | absent | non | multiples | HBC/GBR/BIC | oui |
| TRADE-28 | commerce | `trade_route_events.txt:28` | événement 1 | cible `market` | oui | non requis | 261 | identique cible | identique | identique | oui | 0 cible | marché pays | non |
| NAVLOC | UI navale | `naval_battles_l_*.yml` | 2 clés | data loc | oui | non | 44+44 | hérité | hérité | présent | oui | 0 | data binding naval | oui |
| JE-REV | moteur JE | sans chemin | 4 révoltes | doublon transfert | oui | oui | 539 | non attribué | non attribué | moteur | n/a | 0 | création révolte | non |
| TAN-TECH | Tanzimat | événements | chaîne technique | ancien seulement | 0c | 3h | 0c/3h | divergent | divergent | vanilla | non bornée | n/a | setup 1776 | oui |
| TAN-DESIGN | Tanzimat | setup/chaîne | activation 1776 | aucun défaut actuel | 0c | audit 6A.9R | 0c | intentionnel | autre design | 1836 | non | design | Sick Man clos | oui |
| ADMIN | administration | chemins protégés | bâtiments/PM | aucun précis | 0c | statique | 0c | fusionné | source | variable | n/a | n/a | ADMIN | oui |
| SHIP-56 | traité naval | vanilla `31_ship_transfer.txt:56` | `ship_valid_trigger` | cible `scope` | oui | non | 127 | hérité | hérité | présent | oui | 0 | moteur traité | non |
| EMPTY | lecteur persistant | fichier vide | aucun objet | clé vide | oui | non | 2 408 | non attribué | non attribué | non attribué | inconnue | n/a | moteur | non |

## 17. Matrice de priorité — impact et décision

| ID | Impact gameplay | Étendue | Besoin de design | Classification canonique | Gravité gameplay | Statut de merge | Priorité | Phase potentielle | Sélection |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DI-API | intérêts initiaux possiblement absents | 28 pays/45 régions | non pour l'audit | `UNKNOWN_REQUIRES_REVIEW` | `UNKNOWN_RUNTIME_IMPACT` (potentiel majeur) | `REQUIRES_AUDIT` | P1 | `HOTFIX_6A18R_DECLARED_INTEREST_HISTORY_API_1_13_AUDIT` | **oui** |
| DI-MAP | cartographie diplomatique close | Inde/GBR/BIC/POR | oui/clos | `PROTECTED_CONCURRENT_WORK` | `DESIGN_ONLY` | `PROTECTED_SCOPE` | P0 protégé | aucune | non |
| COUP | mécanique Coup potentiellement cassée | feature | non pour API, oui adjacent | `UNKNOWN_REQUIRES_REVIEW` | `UNKNOWN_RUNTIME_IMPACT` | `REQUIRES_AUDIT` | P1 | audit déjà effectué | non |
| IOP | disponibilité/pinning potentiels | une JE | oui pour vivier | `UNKNOWN_REQUIRES_REVIEW` | `UNKNOWN_RUNTIME_IMPACT` | `REQUIRES_AUDIT` | P1 | audit déjà effectué | non |
| HBC | lois/institutions possiblement incohérentes | un pays | oui obligatoire | `UNKNOWN_REQUIRES_REVIEW` | `DESIGN_ONLY` | `REQUIRES_HUMAN_DESIGN_DECISION` | P0 | aucune autonome | non |
| NAVACT | lois initiales non résolues | chaîne multi-pays | oui via HBC | `UNKNOWN_REQUIRES_REVIEW` | `DESIGN_ONLY` | `BLOCKS_MERGE` | P0 | 6A.14F interdite | non |
| TRADE-28 | événement 1 omis pour racines invalides | local/répété | non | `ALREADY_MERGED` | `DEGRADED_BEHAVIOR` | `NON_BLOCKING` | P2 | `HOTFIX_6A18R_TRADE_ROUTE_INVALID_MARKET_TARGET_AUDIT` | non |
| NAVLOC | détail de bataille dégradé | UI navale | non | `PROTECTED_CONCURRENT_WORK` | `UI_ONLY` | `PROTECTED_SCOPE` | P2 | aucune | non |
| JE-REV | aucune perte observable prouvée | moteur/révoltes | non | `ALREADY_MERGED` | `LOG_NOISE` | `NON_BLOCKING` | P2 | aucune | non |
| TAN-TECH | impact ancien non reproduit | chaîne locale | partiel | `UNKNOWN_REQUIRES_REVIEW` | `UNKNOWN_RUNTIME_IMPACT` | `POST_MERGE_BACKLOG` | P2 | aucune | non |
| TAN-DESIGN | activation anachronique | empire ottoman | oui | `POST_MERGE_DESIGN_BACKLOG` | `DESIGN_ONLY` | `POST_MERGE_BACKLOG` | P3 | aucune | non |
| ADMIN | aucun impact actuel démontré | protégé | non démontré | `ALREADY_MERGED` | `UNKNOWN_RUNTIME_IMPACT` | `PROTECTED_SCOPE` | P2 | aucune | non |
| SHIP-56 | validation transfert naval locale | vanilla | non | `ALREADY_MERGED` | `DEGRADED_BEHAVIOR` | `NON_BLOCKING` | P2 | aucune portage | non |
| EMPTY | impact non attribuable | global moteur | inconnu | `UNKNOWN_REQUIRES_REVIEW` | `UNKNOWN_RUNTIME_IMPACT` | `UNKNOWN` | P2 non bornable | aucune | non |

Cette matrice sépare explicitement la gravité gameplay du statut de merge.
HBC/Navigation Acts bloquent documentairement sans crash prouvé; à l'inverse,
les 261 erreurs commerciales actuelles sont une dégradation réelle mais ne
bloquent pas l'intégration du fork puisqu'elles sont communes au vanilla.

## 18. Sélection et prompt produit

`DI-API` offre le meilleur rapport bénéfice/risque : P1 transversal, un seul
fichier connu, une racine connue, des scopes et régions exhaustifs, et un
audit possible sans modifier les cartographies protégées. Son incertitude
fonctionnelle interdit une correction F mais justifie exactement un audit R.

Le prompt courant est remplacé par un prompt autonome complet pour
`HOTFIX_6A18R_DECLARED_INTEREST_HISTORY_API_1_13_AUDIT`. Il exige preuve
moteur/statique, partition API/cartographie, comparaison trois voies, plan de
test futur seulement si nécessaire et interdit toute correction.

## 19. Documents écrits

- création de ce rapport;
- ajout de 6A.18 à `docs/reports/hotfix/INDEX.md`;
- ajout de 6A.18 à `HOTFIX_REPORT_INDEX.csv`;
- mise à jour des blocs globaux et ajout de la sélection 6A.18R dans
  `HOTFIX_MERGE_BLOCK_STATUS.csv`;
- ajout de la décision à `HOTFIX_MERGE_COMPLETION_ROADMAP.md`;
- remplacement de `HOTFIX_NEXT_MERGE_PHASE_PROMPT.md` par le prompt 6A.18R.

Aucun autre fichier n'est créé ou modifié.

## 20. État final

Le HEAD final reste `574492dd0b72ede2b7dd73e4dc9192947f70b419`, message
`Audit Imperialism of Promise for 1.13`. La branche reste
`hotfix-dlc-audit`. L'index staged est vide et `git diff --check` passe.

Les seuls changements du worktree sont les six documents autorisés. Les huit
éléments non suivis protégés restent exactement ceux du préflight. Aucun
fichier gameplay, loi, localisation, Coup, Imperialism, HBC, Navigation Acts,
BIC, Inde, NAVY, ADMIN ou Tanzimat n'a changé. Le stash et les processus sont
inchangés. Aucun runtime, launcher, sauvegarde ou console n'a été lancé.

## 21. Verdicts finaux

```text
HOTFIX_6A18_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE
POST_6A17R_RESIDUAL_DIAGNOSTICS_REINDEXED
GAMEPLAY_SEVERITY_AND_MERGE_BLOCKERS_SEPARATED
RESIDUAL_P0_P1_PRIORITY_MATRIX_COMPLETE
COUP_AND_IMPERIALISM_CORRECTIONS_REMAIN_UNSELECTED
HBC_AND_NAVIGATION_ACTS_REMAIN_BLOCKED
NO_GAMEPLAY_CHANGED
NO_RUNTIME_REQUIRED
NO_AUTOMATIC_COMMIT
STASH_NAVY_3C_3_INTACT
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
DECLARED_INTEREST_HISTORY_API_AUDIT_SELECTED
NEXT_EXECUTION_PHASE = HOTFIX_6A18R_DECLARED_INTEREST_HISTORY_API_1_13_AUDIT
```
