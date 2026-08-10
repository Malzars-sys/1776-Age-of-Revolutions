# HOTFIX-6A.16R — Audit fonctionnel 1.13 des API d'événements Coup

## 1. Phase, date et verdict

- Phase : `HOTFIX_6A16R_COUP_EVENT_APIS_1_13_FUNCTIONAL_AUDIT`.
- Date : 3 août 2026.
- Nature : audit documentaire statique, sans correction gameplay ni runtime.
- Branche : `hotfix-dlc-audit`.
- HEAD initial et final :
  `1784fd426998fc62e484d2048960e009eff03ccb`.
- Message : `Select post-6A15F residual global script phase`.

Les seize occurrences obsolètes restent présentes dans le fork : dix
`has_role` et six `is_ruler`, dans deux fichiers et sept objets. Les formes
modernes sont respectivement `has_role_of_type` et
`is_ruler_of_own_country`. La convergence n'est toutefois pas uniforme : une
branche `ip4_coup.2` est supprimée par la source, et plusieurs changements de
sélection ou de validité entourent les API.

Surtout, les rotations encore disponibles ne reproduisent plus les six
diagnostics `is_ruler` dans le dernier runtime. La condition 5 de sélection
d'une correction atomique n'est donc pas satisfaite. Aucune future phase
corrective n'est sélectionnée.

## 2. Préflight Git et protections

Le préflight a confirmé :

- racine exacte du fork et branche `hotfix-dlc-audit`;
- HEAD et message exacts;
- rapport 6A.16 présent dans HEAD avec ses dix verdicts;
- aucun changement suivi initial et index staged vide;
- `git diff --check` initial PASS;
- uniquement `bject` et les sept recherches technologiques non suivis;
- aucun processus `victoria3.exe`, `dowser.exe` ou appartenant à
  `Paradox Interactive\launcher`;
- Ankama Launcher ignoré par la détection précise.

État initial :

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

Ces huit chemins et leur contenu n'ont pas été inspectés. Le stash protégé
était :

```text
stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla
518df704fa14599c0f254fae13859210663dd976
```

Il n'a été ni ouvert, ni appliqué, ni modifié.

## 3. Sources lues intégralement

Ont été lus avant conclusion : les rapports 6A.16, 6A.15R et 6A.15F, la
roadmap, le prompt autonome, les deux CSV parsés par `Import-Csv`, les trois
versions des deux fichiers événementiels, les changelogs complets du fork et
de la source, ainsi que les logs courants et rotations pertinentes.

Les dépendances Coup vanilla héritées suivantes ont aussi été lues en lecture
seule :

| Dépendance | Octets | SHA-256 |
| --- | ---: | --- |
| `common/scripted_effects/00_victoria_ip4_scripted_effects.txt` | 52013 | `5F9A1C57060030102CBDC1F8C80E1C69E7BC115A259F9A82E9EE9F0D77FA73AD` |
| `common/scripted_progress_bars/00_ip4_victoria_progress_bars.txt` | 2585 | `DA2C2ACA01848A91B000739CD7A9E07B751E1EF8A5B31913C4ABEBF979F29DD1` |
| `common/on_actions/00_on_actions_monthly.txt` | 4434 | `AFC9A539B7B0B11634AD2EA36055DAE61B6F8F8415B14CF8C1CB3F9E23D9DF23` |
| `common/diplomatic_actions/57_orchestrate_coup.txt` | 10753 | `0C0CA9CF8095A067AE80F5ED2297D52BDD376E59E8B02711DF742E589039C3A6` |
| `common/scripted_triggers/00_ep2_victoria_scripted_triggers.txt` | 8794 | `E66A5223C367A2C137E09248239F61C916E4EE40D2F02EAFC8301722C05EEAB6` |
| `common/scripted_effects/00_victoria_ep2_scripted_effects.txt` | 54784 | `59505B659A8292B58948BA5F9BDF41B7E1871A89C62FAB0F7B9F0C895D798DA5` |
| `common/political_lobbies/00_political_lobbies.txt` | 44357 | `5018B2BEECAB24F1A7F361095CBE76EE90A2D22B4DC759B22235D7068B403091` |
| `common/character_interactions/00_character_interactions.txt` | 27137 | `9E85AD2B353F730F4CDB9DD57C0A7709E31D171CEF7743468E354D2BDA09E832` |
| `common/character_interactions/01_additional_interactions.txt` | 28391 | `742334173B75F83592797D6A6A74BCB1A1631DF601E39C63C24EC61C15503142` |
| `common/decisions/ip4_portugal_decisions.txt` | 7814 | `ACE9D665053F76B403F6F561966C92B58C9C9EE88F68D31BCC201DC20A1C2257` |

Tous ont un BOM UTF-8, des fins LF et des accolades équilibrées. Aucun fichier
vanilla n'a été copié dans le fork.

## 4. Preuves d'entrée et structure trois voies

| Fichier | Version | Octets | Lignes | SHA-256 |
| --- | --- | ---: | ---: | --- |
| `events/iberia_events/ip4_coup_events.txt` | fork | 15957 | 706 | `8DD5A07F60A3E1C623CF48495B062AFE0388602E256CBA8384CD8540067B5AD2` |
| idem | source | 19827 | 887 | `F806A772F86EB379EBC7ED05F7808A5B16C0CACFC0CD784E94B6AA1FB9C8C9D4` |
| idem | vanilla | 19955 | 897 | `22A7B94EE4A0CB4DA7C31DA2F488CEB845473EBDF44EB32ED649F56200886E92` |
| `events/agitators_events/coup_events.txt` | fork | 25485 | 1301 | `88D1B0AE45F296A84FBB997C3F089423A2240790742291DDE359A9509DA5F3CE` |
| idem | source | 25870 | 1306 | `AEE3D155D3C347AC5338468F5814CC5DAAFCBB9862E801D3287643587D525990` |
| idem | vanilla | 25652 | 1301 | `F1CD65506555E45D1C08C27EAA96EE6939F94D313DC44DFC2B20DD4E3106CB7F` |

Les six fichiers sont UTF-8 avec BOM, LF, saut final et accolades
équilibrées. Le premier possède `217/217`, `274/274`, `277/277` accolades;
le second `367/367`, `369/369`, `366/366`.

Objets :

- fork IP4 : `ip4_coup.1` à `.4`; source et vanilla ajoutent `.11`;
- trois versions du second fichier : `coup_pulse_events.1` à `.10` et
  `coup_aftermath_events.1` à `.4`;
- objets ciblés : `ip4_coup.1`, `ip4_coup.2`, `coup_pulse_events.1`, puis
  `coup_aftermath_events.1` à `.4`, soit sept objets.

## 5. Diffs complets

Les hunks sont comptés avec `git diff --no-index --unified=0`.

| Fichier | Comparaison | Numstat | Hunks | Hunks API ciblés | Hunks non API |
| --- | --- | --- | ---: | ---: | ---: |
| IP4 | fork → source | `265+/84-` | 37 | 5 | 32 |
| IP4 | fork → vanilla | `249+/58-` | 33 | 6 | 27 |
| IP4 | source → vanilla | `30+/20-` | 7 | 1 | 6 |
| Coup pulses/aftermath | fork → source | `18+/13-` | 12 | 6 | 6 |
| Coup pulses/aftermath | fork → vanilla | `13+/13-` | 9 | 6 | 3 |
| Coup pulses/aftermath | source → vanilla | `1+/6-` | 6 | 0 | 6 |

IP4 comporte des changements communs de loyauté, raison valide, immunité et
`.11`, mais aussi des divergences source/vanilla de cancellation, tri,
capitale, seuil d'échec, radicaux et exil. Le second fichier converge sur les
huit noms d'API; la source seule ajoute deux exclusions d'héritier, remplace
la retraite par un retrait de rôle et exclut trois fois les cultures
primaires. Source et vanilla ajoutent toutes deux deux validations de
personnage et rendent optionnel l'accès au groupe d'intérêt.

## 6. Baseline et méthode de déduplication des logs

La baseline validée héritée reste `373 diagnostics dans 139 fichiers`; la
réindexation 6A.16 reste `1 189 diagnostics script actuels`. Cet audit ne les
additionne pas à nouveau à travers les rotations.

Méthode :

1. identifier la dernière session par horodatage interne et rotation;
2. normaliser chaque diagnostic par `(message, chemin, ligne)`;
3. ne compter qu'une fois les miroirs éventuels entre types de log;
4. distinguer présence statique actuelle, reproduction dans le dernier
   runtime, rotation ancienne et preuve seulement consignée par un rapport;
5. ne pas additionner les mêmes diagnostics entre rotations.

Le dernier runtime survivant est `game.log`, du 3 août 2026 de `19:13:35` à
`19:48:33`, SHA-256
`0404C0BC2F72EC4372AB09C6F36BC232EA95FA2133F4F5FEEE374BC364EF3F59`.
Il charge `coup_events.txt`, mais contient zéro diagnostic ciblé.

La dernière rotation survivante qui contient les erreurs ciblées est
`game.3.log`, diagnostic horodaté `18:40:57`–`18:40:58` le 2 août 2026,
dernier écrit `18:41:06`, SHA-256
`C4B7DEE73D133C8EC57B94628D81BBCE6DA97CC02555F3786BCA7E25109586B5`.
Elle contient dix diagnostics `has_role` uniques : deux dans
`coup_events.txt` et huit dans IP4.

Le rapport 6A.15R consignait auparavant les seize diagnostics dans trois
rotations `debug.1`, `.3` et `.5`, huit par fichier et par rotation. Ces noms
ont depuis tourné ou été remplacés : aucune rotation disponible ne contient
désormais la chaîne `is_ruler`. Les six occurrences restent statiquement
actuelles dans le fork, mais leur message historique n'est plus
indépendamment reproductible depuis les logs survivants.

## 7. Carte des seize diagnostics

| Fichier | Objet | Lignes fork | API | Rôle/valeur | Dernier runtime | Historique 6A.15R | Rotation survivante | Statut |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | --- |
| IP4 | `ip4_coup.1` | 30, 31 | `has_role` | general, admiral | 0 | 6 | 2 | actuel statique, log ancien |
| IP4 | `ip4_coup.1` | 56, 57 | `has_role` | general, admiral | 0 | 6 | 2 | actuel statique, log ancien |
| IP4 | `ip4_coup.2` | 321, 332 | `has_role` | admiral, general | 0 | 6 | 2 | actuel statique, log ancien |
| IP4 | `ip4_coup.2` | 426, 432 | `has_role` | general, admiral | 0 | 6 | 2 | actuel statique, log ancien |
| pulses | `coup_pulse_events.1` | 29, 40 | `has_role` | general, general | 0 | 6 | 2 | actuel statique, log ancien |
| pulses | `coup_pulse_events.1` | 30, 41 | `is_ruler` | no, no | 0 | 6 | 0 | actuel statique, preuve historique consignée |
| aftermath | `.1`, `.2`, `.3`, `.4` | 967, 1062, 1171, 1253 | `is_ruler` | yes × 4 | 0 | 12 | 0 | actuel statique, preuve historique consignée |

Messages normalisés :

- `has_role trigger [ Invalid database object '<role>' ]`;
- `Unknown trigger type: is_ruler` selon la preuve consignée par 6A.15R.

Total statique actuel : 16, soit `10 has_role / 6 is_ruler`. Total dans le
dernier runtime : 0. Total unique dans la rotation survivante pertinente :
10. La colonne historique compte trois captures par occurrence consignées par
6A.15R, sans les additionner à la rotation survivante. Aucun de ces
diagnostics n'est attribuable à vanilla ou à un autre mod :
les chemins et lignes correspondent aux overrides du fork.

## 8. Les neuf groupes fonctionnels

| ID | Fichier/objet | Lignes | Scope et branche | Effet en aval |
| --- | --- | --- | --- | --- |
| IP4-HR-T | IP4 `.1` | 30–31 | personnage de `any_scope_character`, trigger pays | rend le coup initial éligible |
| IP4-HR-S | IP4 `.1` | 56–57 | personnage de `ordered_scope_character.limit` | choisit et sauvegarde `golpista_general` et son IG |
| IP4-HR-P | IP4 `.2` | 321, 332 | `scope:golpista_general`, trigger de l'option `.2.b` | ouvre l'échec préventif selon marine/armée et seuils de force |
| IP4-HR-R | IP4 `.2` | 426, 432 | `scope:golpista_general`, branche `retire_golpista_var` | retire exactement les rôles general/admiral après échec |
| CP-HR-T | pulse `.1` | 29 | personnage de `any_scope_character` | rend le pulse d'accusation éligible |
| CP-HR-S | pulse `.1` | 40 | personnage de `random_scope_character.limit` | sauvegarde `accused_general` et son IG |
| CP-IR-T | pulse `.1` | 30 | même personnage, valeur `no` | exclut le dirigeant de sa propre sélection |
| CP-IR-S | pulse `.1` | 41 | même personnage aléatoire, valeur `no` | exclut le dirigeant du personnage sauvegardé |
| CA-IR-L | aftermath `.1`–`.4` | 967, 1062, 1171, 1253 | personnage de `random_scope_character.limit`, valeur `yes` | sauvegarde le dirigeant comme `coup_leader` pour les options et modificateurs |

## 9. Audit `has_role`

Dans tous les cas, le scope appelant est un personnage et les rôles restent
`general` ou `admiral`. La forme 1.13 prouvée est
`has_role_of_type = <même rôle>`. L'attribution/retrait du rôle en aval reste
distincte : les substitutions théoriques ne modifient aucun
`remove_character_role`.

- IP4-HR-T : source et vanilla convergent exactement sur les deux noms d'API
  et rôles. Loyauté, raison valide et immunité sont des changements adjacents
  communs, non requis pour la substitution.
- IP4-HR-S : même convergence sur les deux lignes, mais la source trie par
  `commander_coup_strength` et vanilla conserve `popularity`. La sélection de
  personnage ne doit donc jamais être absorbée dans un correctif API.
- IP4-HR-P : vanilla remplace les deux noms, alors que la source supprime les
  deux tests et remplace toute la formule par une comparaison de résistance.
  C'est une convergence partielle, non atomique.
- IP4-HR-R : source et vanilla remplacent les deux noms et conservent les
  mêmes retraits de rôles. Ce groupe est structurellement isolable.
- CP-HR-T et CP-HR-S : source et vanilla convergent sur
  `has_role_of_type = general`. Les ajouts communs
  `character_is_valid_for_events` et l'accès `interest_group ?=` ainsi que
  l'exclusion d'héritier source-only restent séparés.

## 10. Audit `is_ruler`

Les six scopes sont des personnages issus des itérateurs du pays événement.
Source et vanilla utilisent exactement
`is_ruler_of_own_country = no` dans le pulse et `= yes` dans les quatre
aftermath. Le pays de référence demeure donc le propre pays du personnage;
aucun passage à `ROOT` n'est introduit.

Les deux exclusions d'héritier sont source-only. Les deux
`character_is_valid_for_events = yes` sont communes source/vanilla, mais
modifient l'ensemble des personnages éligibles et ne sont pas nécessaires au
renommage. Aucun test de validité ou d'exil n'est ajouté aux aftermath. Les
quatre sélections `coup_leader` sont par ailleurs identiques autour du nom
d'API.

Structurellement, les six renommages forment un candidat d'un fichier et six
lignes. Ils ne sont pas sélectionnables pendant cette phase, car le diagnostic
`is_ruler` n'est pas reproduit dans le dernier runtime disponible.

## 11. Matrice de classification

| Groupe | Occ. | Fork → source → vanilla | Convergence | Risque / dépendances | Hunk minimal | Hash théorique | Classe | Atomique | Phase | Sélection |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IP4-HR-T | 2 | `has_role` → `has_role_of_type` → idem | exacte sur API, adjacence partielle | éligibilité du coup; loyauté/raison/immunité séparées | 1 hunk, 2 lignes | inclus avec IP4-HR-S : `856CAC430CAFA486ACF579E5A4E40216459AD2D498048783829A7F7F36DD07E0` | `VANILLA_1_13_ALIGNMENT_REQUIRED` | structurellement oui; critère runtime non | `HOTFIX_6A16F_IP4_COUP_HAS_ROLE_API_1_13_ALIGNMENT` | non |
| IP4-HR-S | 2 | idem | exacte sur API, tri divergent | choix du meneur, IG et scopes sauvegardés | 1 hunk, 2 lignes | même hash quatre lignes | `VANILLA_1_13_ALIGNMENT_REQUIRED` | non comme paquet fonctionnel avec tri | idem | non |
| IP4-HR-P | 2 | ancien → branche absente → moderne vanilla | partielle | disponibilité de `.2.b`, formules armée/marine | 2 hunks, 2 lignes | `9581488803E132A46EF56B645CF9F93C6359EA71ACF79428DDAAB54BC148959B` | `UNKNOWN_REQUIRES_REVIEW` | non | aucune | non |
| IP4-HR-R | 2 | ancien → moderne → moderne | exacte | retrait du même rôle après échec | 2 hunks, 2 lignes | `C38E5A0C3ACCDB91854B5939EA5EE314BCB85FC083483B5E590A6E46E673BCAD` | `VANILLA_1_13_ALIGNMENT_REQUIRED` | structurellement oui; critère runtime non | `HOTFIX_6A16F_IP4_COUP_HAS_ROLE_API_1_13_ALIGNMENT` | non |
| CP-HR-T | 1 | ancien → moderne → moderne | exacte sur API | éligibilité pulse; validité/héritier séparés | 1 hunk, 1 ligne | avec CP-HR-S : `314F742B128D93FA83651A7285C1BBCEF71C91260F5F9610E9D3825E66062278` | `VANILLA_1_13_ALIGNMENT_REQUIRED` | structurellement oui; critère runtime non | `HOTFIX_6A16F_COUP_PULSE_HAS_ROLE_API_1_13_ALIGNMENT` | non |
| CP-HR-S | 1 | ancien → moderne → moderne | exacte sur API | choix aléatoire et IG optionnel séparés | 1 hunk, 1 ligne | même hash deux lignes | `VANILLA_1_13_ALIGNMENT_REQUIRED` | structurellement oui; critère runtime non | idem | non |
| CP-IR-T | 1 | ancien → moderne → moderne | exacte sur API | exclusion du ruler; héritier/validité séparés | 1 hunk, 1 ligne | avec les six `is_ruler` : `B4698C06645076DD5B36D7443314AE1A0FAE7C08444408FAFE5CF41868487683` | `VANILLA_1_13_ALIGNMENT_REQUIRED` | structurellement oui; preuve runtime absente | `HOTFIX_6A16F_COUP_EVENT_IS_RULER_API_1_13_ALIGNMENT` | non |
| CP-IR-S | 1 | ancien → moderne → moderne | exacte sur API | sélection du général accusé | 1 hunk, 1 ligne | même hash six lignes | `VANILLA_1_13_ALIGNMENT_REQUIRED` | structurellement oui; preuve runtime absente | idem | non |
| CA-IR-L | 4 | ancien → moderne → moderne | exacte, voisinage identique | sauvegarde `coup_leader`, puis quatre branches de modificateurs | 4 hunks, 4 lignes | même hash six lignes | `VANILLA_1_13_ALIGNMENT_REQUIRED` | structurellement oui; preuve runtime absente | idem | non |

Le remplacement des huit `has_role` IP4 produirait théoriquement
`8CC678405D8CEE58F360E2FD6DC8E66F030CA63035045E635C9BE0464DCCBCB7`.
Le remplacement combiné des huit API du second fichier produirait
`D4B94EB4F9D3FFF5B93518FEF2A6A6ED7C014D4B58A051333CE61B6B8ACB0268`.
Ces hashes sont des preuves de bornage, pas une autorisation de correction.

Rollback théorique chirurgical : sur les seules lignes énumérées, remplacer
`has_role_of_type =` par `has_role =`, ou
`is_ruler_of_own_country =` par `is_ruler =`; aucun autre hunk.

## 12. Deltas fonctionnels adjacents différés

| Delta | Source/vanilla | Effet | Classification |
| --- | --- | --- | --- |
| loyauté, raison valide, immunité IP4 | commun | change l'éligibilité initiale | `VANILLA_1_13_ALIGNMENT_REQUIRED` |
| tri `commander_coup_strength` | source-only | change le meneur choisi | `UNKNOWN_REQUIRES_REVIEW` |
| cancellation avec IG, mort, exil | source-only | change l'invalidation | `UNKNOWN_REQUIRES_REVIEW` |
| formule d'échec préventif | source/vanilla divergentes | change l'accès à `.2.b` | `UNKNOWN_REQUIRES_REVIEW` |
| capitale, radicaux, exil | source/vanilla divergentes | change les effets | `UNKNOWN_REQUIRES_REVIEW` |
| `is_heir_of_own_country = no` | source-only | exclut les héritiers du pulse | `UNKNOWN_REQUIRES_REVIEW` |
| `character_is_valid_for_events` | commun | filtre les personnages invalides/exilés | `VANILLA_1_13_ALIGNMENT_REQUIRED` |
| `interest_group ?=` | commun | évite un accès IG obligatoire | `VANILLA_1_13_ALIGNMENT_REQUIRED` |
| retrait du rôle au lieu de retraite | source-only | maintient le personnage sans son rôle | `UNKNOWN_REQUIRES_REVIEW` |
| exclusions de cultures primaires aftermath `.3` | source-only | change états/cultures éligibles | `UNKNOWN_REQUIRES_REVIEW` |
| lois et effets de victoire hérités | déjà exécutables, dont `activate_law = scope:coup_desired_law.type` | résultat du coup | `ALREADY_MERGED` |
| puissance 1776 de Merchant Banking | hors hotfix, signalée par le runtime humain | futur équilibrage | `POST_MERGE_DESIGN_BACKLOG` |

Aucune pondération, sélection, loi, capitale, radical, exil, pulse ou aftermath
n'est absorbé dans un remplacement d'API.

## 13. Lobby, sponsor et cleanup séparés

La chaîne `ip4_coup.11` → `orchestrate_coup` → `coup_lobby` →
`relevant_lobby` / `coup_lobby_country` / `coupist_lobby_country` →
`coup_sponsor` → pacte et cleanup est indépendante des seize noms d'API.
Les dépendances héritées lisent ces variables dans l'action diplomatique, les
lobbies et les effets de victoire, mais aucun renommage étudié ne les écrit,
ne les supprime ou ne les requiert.

Le cooldown centralisé, l'invalidation, les scopes sponsor et les variables de
raison restent également hors périmètre. Aucune correction lobby n'est
sélectionnée.

`COUP_LOBBY_SPONSOR_CLEANUP_DELTAS_SEPARATED`

## 14. Test des 22 conditions de sélection

Les fichiers, objets, lignes, hashes initiaux, formes modernes, diffs et
rollbacks sont connus. La convergence minimale est exacte pour plusieurs
groupes, sans loi, cooldown, lobby, sponsor, cleanup, scope, rôle, pondération
ou effet à modifier.

La condition obligatoire 5 échoue néanmoins : le dernier runtime survivant
contient zéro diagnostic ciblé, et les six messages `is_ruler` ne sont plus
présents dans les rotations disponibles. Une preuve historique consignée ne
remplace pas la reproduction demandée dans le dernier runtime. Puisque les 22
conditions sont cumulatives, aucun candidat n'est sélectionnable.

## 15. Documents écrits et CSV

Documents de cette phase :

- création du présent rapport;
- mise à jour de `docs/reports/hotfix/INDEX.md`;
- mise à jour de `HOTFIX_REPORT_INDEX.csv`;
- mise à jour de `HOTFIX_MERGE_BLOCK_STATUS.csv`;
- mise à jour de `HOTFIX_MERGE_COMPLETION_ROADMAP.md`.

`HOTFIX_NEXT_MERGE_PHASE_PROMPT.md` reste inchangé comme preuve historique,
car aucune future correction n'est sélectionnée.

Les CSV ont été parsés avec un vrai parseur, jamais découpés naïvement :

- block status : `42 × 17` avant et après, en-têtes inchangés, aucune ligne
  mal formée, aucune cellule structurelle nulle, 20 cellules optionnelles
  vides, zéro doublon de `block_id`;
- report index : `129 × 22` avant, `130 × 22` après, en-têtes inchangés,
  aucune ligne mal formée ni cellule structurelle nulle; les doublons
  historiques de clé sont limités à `S` et `INDEX`; la nouvelle phase est
  unique, précédée par 6A.16 et sans successeur.

## 16. Contrôles finaux

Les contrôles finaux ont confirmé : branche et HEAD inchangés, index staged
vide, stash final
`518df704fa14599c0f254fae13859210663dd976` inchangé, `git diff --check`
PASS, aucun processus Victoria 3/Paradox, et seulement les cinq documents
autorisés modifiés/créés en plus des huit chemins non suivis protégés.

Hashes gameplay à préserver :

- IP4 fork :
  `8DD5A07F60A3E1C623CF48495B062AFE0388602E256CBA8384CD8540067B5AD2`;
- pulses/aftermath fork :
  `88D1B0AE45F296A84FBB997C3F089423A2240790742291DDE359A9509DA5F3CE`;
- `common/journal_entries/01_coup.txt` :
  `37C2669619CD26C30450F41082716BF30CA12949AA5FEE59BA0D25D498339602`.

Aucun fichier gameplay, loi, lobby, scope, cooldown ou cleanup n'a été
modifié. Aucun runtime, staging, commit, merge ou opération sur le stash n'a
été exécuté.

## 17. Verdicts finaux

```text
HOTFIX_6A16R_COUP_EVENT_APIS_1_13_FUNCTIONAL_AUDIT_COMPLETE
COUP_EVENT_APIS_THREE_WAY_COMPARISON_COMPLETE
COUP_EVENT_API_GROUPS_CLASSIFIED
COUP_LOBBY_SPONSOR_CLEANUP_DELTAS_SEPARATED
NO_GAMEPLAY_CHANGED
NO_RUNTIME_REQUIRED
NO_AUTOMATIC_COMMIT
STASH_NAVY_3C_3_INTACT
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
NO_NEXT_EXECUTION_PHASE_SELECTED
```
