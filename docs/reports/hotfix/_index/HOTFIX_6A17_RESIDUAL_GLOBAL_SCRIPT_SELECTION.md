# HOTFIX-6A.17 — Sélection documentaire du prochain résidu global

Date : 4 août 2026

Phase : `HOTFIX_6A17_RESIDUAL_GLOBAL_SCRIPT_SELECTION`

Branche : `hotfix-dlc-audit`

Nature : audit documentaire, statique, trois voies et sans runtime.

## 1. Décision

Une seule prochaine phase est sélectionnée :
`HOTFIX_6A17R_IMPERIALISM_OF_PROMISE_1_13_FUNCTIONAL_AUDIT`.

Il s'agit d'un audit en lecture seule d'un seul objet,
`je_imperialism_of_promise`, dans un seul fichier. L'audit devra séparer le
pinning, les deux API `has_role`, le jeu de rôles divergent, le tooltip de
bureaucratie et toutes les dépendances BIC/Inde. Il ne pourra modifier ni BIC,
ni l'Inde, ni aucun fichier gameplay.

6A.17 n'applique aucun hunk et ne commence pas 6A.17R.

## 2. Préflight et protections

| Contrôle | Résultat |
| --- | --- |
| Racine | `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork` |
| Branche | `hotfix-dlc-audit` |
| HEAD initial | `feb62d7086d710413fa9103b9aefc34fb3f4e171` |
| Message HEAD | `Audit Coup event APIs for 1.13` |
| Rapport 6A.16R dans `HEAD` | PASS |
| Dix verdicts 6A.16R dans `HEAD` | PASS |
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

- les rapports 6A.16R, 6A.16, 6A.15F, 6A.15R, 6A.14H et 6A.14R;
- la roadmap, le prompt précédent et les changelogs complets du fork et de la
  source hotfix;
- les cinq CSV canoniques avec `Import-Csv`, sans découpage naïf;
- le rapport canonique 6A.9R pour le candidat Tanzimat;
- les trois versions de `04_imperialism_of_promise.txt`;
- les versions fork et source de `00_interests.txt`, absent de vanilla;
- les journaux courants `error.1.log`, `error.log`, `game.log` et les rotations
  pertinentes, notamment `game.3.log`.

Les fichiers protégés, les localisations françaises générales, HBC, Navigation
Acts, ADMIN, BIC et les contenus Inde n'ont pas été ouverts.

## 4. Validation CSV

Le parseur CSV réel confirme :

| CSV | Données × colonnes avant 6A.17 | Lignes vides | Lignes mal formées | Doublons de clé |
| --- | ---: | ---: | ---: | ---: |
| `HOTFIX_MERGE_BLOCK_STATUS.csv` | `42 × 17` | 0 | 0 | 0 |
| `HOTFIX_REPORT_INDEX.csv` | `130 × 22` | 0 | 0 | 2 groupes historiques (`S`, `INDEX`) |
| `HOTFIX_MERGE_THREE_WAY_INVENTORY.csv` | `541 × 21` | 0 | 0 | 0 |
| `HOTFIX_GLOBAL_DIFFERENCE_INVENTORY.csv` | `534 × 22` | 0 | 0 | 0 |
| `HOTFIX_MERGE_REMAINING_WORK.csv` | `512 × 20` | 0 | 0 | 0 |

Les clés structurelles `block_id`, `phase_id` et `relative_path` sont toutes
remplies. Les vides restants concernent uniquement des champs optionnels :
rapports/commits absents, successeurs, CSV compagnons et tailles ou hashes d'un
arbre où le fichier est absent.

Le registre contient 19 lignes sans successeur avant 6A.17. Elles mêlent cinq
entrées `INDEX`, des preuves historiques, des clôtures terminales et 6A.16R;
elles ne constituent pas 19 phases exécutables. Les blocs P0/P1 encore ouverts
sont le conteneur global, les 87 résidus, HBC, la fusion finale et des
périmètres expressément protégés (Japon, technologies, révolutions américaine
et française, localisation globale). Ils ne supplantent pas les protections
de cette phase.

Après ajout de 6A.17, les deux registres documentaires deviennent
respectivement `43 × 17` et `131 × 22`. Les trois inventaires fonctionnels ne
sont pas réécrits.

## 5. Distribution résiduelle recalculée

Le recalcul part de la couche canonique exclusive des 161 lignes, puis vérifie
chaque fermeture postérieure dans les rapports, la matrice de blocs et les
inventaires. 6A.16R est un audit sans correction : il ne ferme ni ne déplace
aucune ligne de cette couche. Aucun nouveau changement gameplay n'est apparu
depuis. La distribution reste donc, après recalcul :

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

Le champ legacy `PENDING_REVIEW = 161` de l'inventaire de travail n'est pas une
classification exclusive et ne remplace pas cette couche canonique.

## 6. Méthode de triage

Chaque signal a été vérifié dans l'ordre imposé : présence dans le dernier
runtime, nature parser/PostValidate, fréquence, appartenance au fork,
comparaison fork/source/vanilla, taille, objets et hunks, isolation, impact,
dépendances, protections, besoin de design, rollback, runtime futur et gain
réel pour P0/P1. Un volume brut élevé n'est jamais considéré comme une preuve
d'atomicité.

## 7. Diagnostics courants et historiques

La dernière session survivante du 3 août 2026 va de 19:16 à 19:48 et est
répartie entre `error.1.log` et `error.log`; `game.log` est son journal de jeu.
Elle contient 6 046 enregistrements bruts, dont 413 en-têtes d'erreur script.

Pour les cinq candidats obligatoires, elle reproduit **zéro** erreur parser ou
PostValidate liée à leur chemin. Elle contient cependant 2 765 occurrences de
signaux secondaires classés :

| Signal courant | Occurrences | Décision |
| --- | ---: | --- |
| clé persistante vide, sans fichier | 2 408 | non bornable |
| cible `market` invalide, `trade_route_events.txt:28` | 261 | commun aux trois arbres, P2 |
| deux erreurs de localisation navales | 88 (`44 + 44`) | NAVY/UI protégé |
| JE `je_imperialism_of_promise` déjà présente sur une révolte | 4 | symptôme de transfert de JE, pas diagnostic des lignes 18/19/140 |
| JE `je_colonial_administration` déjà présente sur une révolte | 4 | ne démontre aucun défaut ADMIN |

Les preuves historiques documentées totalisent 107 occurrences ciblées : 10
Coup encore consignées par 6A.16R, 3 Imperialism of Promise, 91
`add_declared_interest` et 3 Tanzimat. Seules 12 sont encore directement
présentes dans les rotations disponibles : 10 Coup et les deux `has_role`
d'Imperialism dans `game.3.log`. Les 91 et les trois Tanzimat ne doivent donc
pas être présentées comme actuelles.

## 8. Coup, HBC et Navigation Acts

- Coup : 16 occurrences statiques subsistent, mais le dernier runtime en
  reproduit zéro et aucune preuve nouvelle indépendante ne satisfait 6A.16R.
  Aucune phase 6A.16F n'est sélectionnée.
- HBC : le verdict reste
  `HBC_DUPLICATE_HISTORY_UNKNOWN_REQUIRES_REVIEW`. Une décision humaine est
  toujours requise; aucune 6A.14HF n'est sélectionnée.
- Navigation Acts : HBC, GBR/NAVY, la visibilité des `chartered_company`, BIC
  et l'effet américain protégé continuent de bloquer 6A.14F.

## 9. Imperialism of Promise

### 9.1 Preuves trois voies

Chemin : `common/journal_entries/04_imperialism_of_promise.txt`.

Objet unique : `je_imperialism_of_promise`.

| Arbre | Octets | Lignes | SHA-256 |
| --- | ---: | ---: | --- |
| Fork | 2 912 | 142 | `80E38C181A5AEB547E8F98EBFD03844F3522CADC59426D9FC16588B908105C3B` |
| Source | 3 182 | 151 | `F97A929A3CC9FAA98A8CE3824A4A6196866AFBA18A89E477600DDA230153D7FC` |
| Vanilla | 3 143 | 150 | `AB08635DC8EAA5C3A1523F70693BADB58A607576B06C5EF979E682008B0D4C0C` |

Fork/source et fork/vanilla ont chacun trois hunks, `13+ / 5-` : rôles aux
lignes fork 18–19, tooltip de bureaucratie aux lignes 38–39 et pinning à la
ligne 140. Source/vanilla ne divergent fonctionnellement que sur
`has_role = character_role_ig_leader`, présent dans la source.

### 9.2 Groupes exclusifs

| Groupe | Preuve | Classification | Suite |
| --- | --- | --- | --- |
| Pinning ligne 140 | source/vanilla convergent exactement sur `should_be_pinned_by_default_uninvolved_or_context` | `VANILLA_1_13_ALIGNMENT_REQUIRED` | isolable, à auditer; aucune correction directe faute de diagnostic actuel |
| Deux `has_role` lignes 18–19 | deux erreurs historiques survivantes; API modernes dans source/vanilla | `VANILLA_1_13_ALIGNMENT_REQUIRED` | auditer scopes et sémantique |
| Ruler, prominence et rôle IG | source/vanilla divergent sur le chef d'IG | `UNKNOWN_REQUIRES_REVIEW` | décision fonctionnelle dans 6A.17R |
| Tooltip bureaucratie | source/vanilla convergent, aucun diagnostic actuel | `VANILLA_1_13_ALIGNMENT_REQUIRED` | groupe séparé, pas de copie implicite |
| BIC, Inde, géographie, progression, Sepoy et événements utilitaristes | dépendances protégées | `PROTECTED_CONCURRENT_WORK` | lecture de leurs rapports seulement; aucun changement |

Le pinning seul serait un hunk `1+/1-`. Une substitution ASCII en mémoire,
sans écriture, donne 2 934 octets et le hash théorique
`EF5200E0B9E7A58AF904C73CDD82F3CC4009FFE0CA9364952F793AB4F3E2A682`.
Le rollback futur serait le remplacement inverse exact. Cette preuve rend un
audit autonome utile, mais ne satisfait pas les critères renforcés d'une phase
corrective F.

## 10. `add_declared_interest`

Chemin : `common/history/interests/00_interests.txt`.

| Arbre | État | SHA-256 |
| --- | --- | --- |
| Fork | 4 415 octets, 158 lignes | `A528418D3C18379C1175E6B469C0313D0AF8C7CC04E80BBE6382F72A097F5DBD` |
| Source | 4 609 octets, 163 lignes | `0BD9ADC58439BB6F81D1B0165954E827C332CB4FCC687980055D4C6A0DF3C92A` |
| Vanilla | absent; aucune référence `add_declared_interest` trouvée | — |

L'objet racine `INTERESTS` contient 28 scopes pays et 91 effets actifs dans le
fork, contre 96 dans la source. Les écarts concernent surtout les régions de
GBR/BIC et une région portugaise, donc des périmètres protégés. Aucun effet
moderne n'est démontré par vanilla 1.13 et aucune occurrence n'est présente
dans les logs survivants.

L'inventaire trois voies classe ce fichier `MERGED_AND_VALIDATED`, en citant la
clôture Inde, tandis que l'inventaire global legacy le conserve en
`PENDING_REVIEW`. Ce conflit documentaire interdit de traiter les 91 lignes
comme une correction globale. Classification du problème d'API :
`UNKNOWN_REQUIRES_REVIEW`; sous-deltas Inde/BIC :
`PROTECTED_CONCURRENT_WORK`. Aucun remplacement atomique n'est prouvé.

## 11. Tanzimat

Le fork hérite `events/tanzimat_events.txt` de vanilla. Source et vanilla ont
le même hash
`F5DAABC9D36BEAE714E5BDFC3B156995B3EAE7758004CE3C7B8C3512BA80AD30`;
la copie source est donc `OBSOLETE_HOTFIX_CONTENT` et ne doit pas être importée.

Les huit pinning Sick Man sont déjà clos. Les trois anciens diagnostics d'ID
Tanzimat ne sont plus présents dans les rotations disponibles. Aucun scope ou
API technique actuel et séparable n'est démontré. L'activation reste
`OTTOMAN_TANZIMAT_1776_DEFERRED_ACTIVATION_DESIGN_BACKLOG`, donc
`POST_MERGE_DESIGN_BACKLOG`. Aucune activation et aucun audit 6A.17R Tanzimat
ne sont sélectionnés.

## 12. Localisation et ADMIN

Les seules erreurs de localisation actuelles sont
`BATTLE_SHIPS_BREAKDOWN_HEADER_ATTACKER` et
`BATTLE_SHIPS_BREAKDOWN_HEADER_DEFENDER`, répétées 44 fois chacune. Elles sont
navales/UI et entrent en collision avec NAVY; aucune clé de mod manquante ou
clé brute liée aux candidats n'est démontrée. Classification :
`PROTECTED_CONCURRENT_WORK`.

ADMIN reste `MERGED_STATIC_ONLY`. Les quatre mentions
`je_colonial_administration` sont des avertissements génériques de JE déjà
présente lors de révoltes, pas des diagnostics de bâtiments ou PM ADMIN.
Aucune réouverture n'est autorisée. Classification : `ALREADY_MERGED`, runtime
global encore différé.

## 13. Candidats supplémentaires crédibles

`events/trade_route_events.txt:28` produit 261 cibles `market` invalides dans
la session courante. Le fichier appartient au fork, mais le groupe fautif des
lignes 24–31 est identique dans fork, source et vanilla. Les trois seuls hunks
fork/source se trouvent plus loin et concernent Sakoku/isolationnisme; ils ne
peuvent pas expliquer la ligne 28. Le signal est donc
`UNKNOWN_REQUIRES_REVIEW`, priorité P2 de validation globale, sans phase 6A.17R.

Les 2 408 erreurs de clé vide n'indiquent aucun fichier. Les grands fichiers
d'événements et on_actions n'ont aucun diagnostic actuel plus précis et ne
sont pas atomiques. Aucun autre candidat crédible ne dépasse Imperialism of
Promise.

## 14. Matrice de preuves

| ID | Domaine | Fichiers / objets | Diagnostic | Dernier runtime | Historique | Occurrences | Fork / source / vanilla | Convergence | Hunks |
| --- | --- | --- | --- | --- | --- | ---: | --- | --- | ---: |
| IOP | JE | `04_imperialism_of_promise.txt` / 1 | pinning + `has_role` | 0 ciblé; 4 avertissements JE | 3 documentés; 2 survivants | 3 | oui/oui/oui | partielle | 3 |
| DI | histoire | `00_interests.txt` / `INTERESTS`, 28 pays | API non reconnue historiquement | 0 | 91 documentés, non survivants | 91 | oui/oui/non | aucune référence vanilla | API potentielle 91 lignes; diff pays non atomique |
| TAN | événements | hérité / chaîne Tanzimat | anciens IDs invalides | 0 | 3, non survivants | 3 | hérité/oui/oui | source=vanilla | 0 import utile |
| LOC | localisation UI | deux clés navales | data loc error | oui | non nécessaire | 88 | provenance globale | non attribuée au mod | non borné |
| ADM | runtime global | aucun objet ADMIN précis | aucun diagnostic ciblé | 0 | clôture statique | 0 | protégé | sans objet | 0 |
| TR1 | événement | `trade_route_events.txt` / `.1` | target `market` invalide ligne 28 | oui | non requis | 261 | oui/oui/oui | groupe fautif exact | 0 hunk divergent au diagnostic |
| COUP | événements | 2 fichiers / 7 objets | 10 `has_role`, 6 `is_ruler` statiques | 0 | 10 survivants | 16 statiques | oui/oui/oui | API partielle | 9 groupes |

## 15. Matrice de décision

| ID | Impact / dépendances | Protégé | Design | Classification dominante | Priorité | Runtime futur | Phase possible | Sélection |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IOP | éligibilité et présentation de la JE; BIC/Inde à exclure | dépendances seulement | oui pour rôle IG, non pour audit | `VANILLA_1_13_ALIGNMENT_REQUIRED` + groupes séparés | **P1 audit** | aucun pendant R | `HOTFIX_6A17R_IMPERIALISM_OF_PROMISE_1_13_FUNCTIONAL_AUDIT` | **oui** |
| DI | intérêts initiaux de 28 pays; Inde/BIC dans le diff | partiel | remplacement inconnu | `UNKNOWN_REQUIRES_REVIEW` | P1 inventaire, confiance faible | audit puis runtime massif | audit API possible plus tard | non |
| TAN | chaîne 1839+ incompatible 1776 | Sick Man/Crise clos | oui | `POST_MERGE_DESIGN_BACKLOG` | P3 | design dédié | audit technique non justifié | non |
| LOC | deux clés d'interface navale | NAVY et FR générale | provenance à établir | `PROTECTED_CONCURRENT_WORK` | P1 bloc, candidat exclu | navigation UI | audit loc interdit ici | non |
| ADM | aucun défaut minimal démontré | ADMIN | non applicable | `ALREADY_MERGED` | P2 validation | runtime global | aucune | non |
| TR1 | événement hérité identique; bruit fréquent | non | contexte moteur requis | `UNKNOWN_REQUIRES_REVIEW` | P2 | reproduction ciblée | aucune phase 6A.17R | non |
| COUP | APIs connues, preuve runtime manquante | deltas adjacents | oui partiellement | `VANILLA_1_13_ALIGNMENT_REQUIRED` | P0 bloqué | nouvelle preuve humaine | phases F interdites | non |

## 16. Justification de priorité

Imperialism of Promise ne gagne pas par son nombre d'erreurs, mais parce que :

1. la ligne P0/P1 des inventaires est encore ouverte;
2. un seul fichier et un seul objet sont concernés;
3. les trois hashes, trois hunks et cinq groupes fonctionnels sont connus;
4. le pinning est théoriquement isolable avec hash et rollback exacts;
5. la divergence source/vanilla sur le rôle IG justifie précisément un audit R;
6. l'audit peut rester documentaire et exclure totalement BIC/Inde;
7. aucun autre candidat obligatoire ne réunit à la fois périmètre, preuve et
   autonomie.

L'absence de diagnostic ciblé dans le dernier runtime interdit une correction
F directe. 6A.17R devra décider si un futur sous-delta peut satisfaire les
critères canoniques; elle ne devra pas présumer cette conclusion.

## 17. Prompt et documents

Le prompt autonome est remplacé par celui de
`HOTFIX_6A17R_IMPERIALISM_OF_PROMISE_1_13_FUNCTIONAL_AUDIT`.

6A.17 crée ou met à jour exactement six documents :

1. ce rapport;
2. `docs/reports/hotfix/INDEX.md`;
3. `HOTFIX_REPORT_INDEX.csv`;
4. `HOTFIX_MERGE_BLOCK_STATUS.csv`;
5. `HOTFIX_MERGE_COMPLETION_ROADMAP.md`;
6. `HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`.

## 18. État final validé

Le HEAD final reste
`feb62d7086d710413fa9103b9aefc34fb3f4e171`, avec le message
`Audit Coup event APIs for 1.13`. Les cinq documents canoniques autorisés sont
modifiés et ce rapport est le seul nouveau document de phase. Les huit
non-suivis protégés restent les seuls autres éléments signalés.

```text
 M docs/reports/hotfix/INDEX.md
 M docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv
 M docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md
 M docs/reports/hotfix/_index/HOTFIX_NEXT_MERGE_PHASE_PROMPT.md
 M docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv
?? docs/reports/hotfix/_index/HOTFIX_6A17_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md
```

`git diff --check` passe, l'index staged est vide, le stash et son objet sont
inchangés. Victoria 3, Dowser et tous les processus sous
`Paradox Interactive\launcher` sont fermés; Ankama Launcher est ignoré.

Aucun gameplay, loi, événement, journal entry, localisation ou histoire pays
n'est modifié. `01_coup.txt`, les deux événements Coup, HBC, Navigation Acts,
NAVY, ADMIN, GEN/VEN et BIC restent inchangés. BIC conserve
`activate_law = law_type:law_frontier_colonization`; aucune restauration de
`law_colonial_exploitation` n'a lieu.

## 19. Verdicts

```text
HOTFIX_6A17_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE
POST_6A16R_RESIDUAL_DIAGNOSTICS_REINDEXED
RESIDUAL_P0_P1_PRIORITY_MATRIX_COMPLETE
COUP_EVENT_APIS_REMAIN_UNSELECTED
HBC_AND_NAVIGATION_ACTS_REMAIN_BLOCKED
NO_GAMEPLAY_CHANGED
NO_RUNTIME_REQUIRED
NO_AUTOMATIC_COMMIT
STASH_NAVY_3C_3_INTACT
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
IMPERIALISM_OF_PROMISE_1_13_AUDIT_SELECTED
NEXT_EXECUTION_PHASE = HOTFIX_6A17R_IMPERIALISM_OF_PROMISE_1_13_FUNCTIONAL_AUDIT
```
