# HOTFIX-6A.18Q — Validation runtime de l'historique des intérêts déclarés

Date : 4 août 2026

Branche : `hotfix-dlc-audit`

HEAD initial et final : `fe80c16c780f477cd9656df40ce5beeaddbc15d7`
Message du HEAD : `Audit declared interest history API for 1.13`

## 1. Résultat

Le runtime humain sous Victoria 3 `release/1.13.0` confirme le résultat B :

- `common/history/interests/00_interests.txt` est atteint par le chargeur;
- `add_declared_interest` est rejeté comme `Unknown effect`;
- l'action autrichienne valide vers `region_south_china` ne crée aucune
  implication au 1er janvier 1776;
- le témoin négatif `region_canada` ne crée lui non plus aucune implication;
- les intérêts visibles de l'Autriche proviennent uniquement du nouveau système
  1.13 d'implication régionale;
- aucune correction gameplay n'est appliquée dans cette phase.

Le constat fonctionnel et le diagnostic explicite se corroborent. L'ancien
effet n'est pas seulement silencieux : il n'est plus enregistré par le moteur
1.13.

## 2. Préflight et état d'entrée

Le préflight a passé avant l'ouverture humaine :

- racine exacte du fork;
- branche `hotfix-dlc-audit`;
- HEAD `fe80c16c780f477cd9656df40ce5beeaddbc15d7` avec le message exigé;
- rapport 6A.18R présent dans le HEAD avec ses douze verdicts;
- arbre suivi propre, index staged vide et `git diff --check` passant;
- seuls `bject` et les sept recherches technologiques protégées étaient non
  suivis;
- stash inchangé :
  `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla`;
- hash du stash : `518df704fa14599c0f254fae13859210663dd976`;
- Victoria 3, Dowser et le launcher Paradox étaient fermés.

Le fichier cible est resté inchangé :

```text
common/history/interests/00_interests.txt
SHA-256 A528418D3C18379C1175E6B469C0313D0AF8C7CC04E80BBE6382F72A097F5DBD
taille 4415 octets
```

## 3. Sélection des contrôles

Pays : Autriche (`AUS`).

Région positive : Sud de la Chine (`region_south_china`). Le bloc autrichien
contient exactement l'action active suivante à la ligne 126 :

```txt
add_declared_interest = region_south_china
```

La région existe dans le registre stratégique vanilla 1.13. Ni l'Autriche, ni
ses sujets BEO, GAL, HUN et TRS n'y possèdent d'État. Les possessions et les
deux revendications autrichiennes identifiées sont européennes. Aucun traité
ou historique commercial autrichien n'a été trouvé. La région n'est ni celle
de la capitale, ni une région voisine de la capitale.

Témoin négatif : Canada (`region_canada`). Cette région 1.13 valide est absente
du bloc autrichien, ne contient aucune possession ou revendication autrichienne
et ne correspond à aucun sujet autrichien.

Les éventuelles sources militaires n'ont pas été modifiées ni utilisées pour
le test. Les panneaux de région démontrent directement une implication
autrichienne nulle dans les deux contrôles.

## 4. Méthode d'observation

Le test a utilisé uniquement l'interface normale et ses panneaux :

1. nouvelle partie avec l'Autriche;
2. jeu maintenu en pause au 1er janvier 1776;
3. panneau Diplomatie, section Intérêts;
4. panneau de la région stratégique Sud de la Chine;
5. panneau de la région stratégique Canada.

Aucune commande console informative exacte n'ayant été démontrée, aucune
commande console n'a été utilisée. Aucun intérêt n'a été ajouté ou retiré et
le temps n'a pas progressé.

## 5. Observations UI et captures

L'opérateur confirme le fork activé et le bon hash. Les captures fournies dans
la conversation montrent l'Autriche au `1 janvier 1776`, en pause, ainsi que
la nouvelle liste d'implication 1.13.

Six intérêts autrichiens sont visibles :

| Région | Niveau | Implication |
| --- | --- | ---: |
| Balkans | Omniprésent IV | 6324 |
| Europe centrale | Influent III | 4176 |
| Europe de l'Est | Influent III | 3969 |
| Europe du Sud | Influent III | 3320 |
| Europe de l'Ouest | Investi II | 2300 |
| Europe du Nord | Investi II | 1500 |

Le Sud de la Chine est absent de cette liste. Son panneau affiche :
`Aucune implication Autrichienne`.

Le Canada est absent de cette liste. Son panneau affiche également :
`Aucune implication Autrichienne`.

L'interface ne montre plus de compteur d'anciens intérêts déclarés utilisés ou
disponibles. Elle affiche les niveaux et valeurs d'implication du nouveau
système.

Les captures restent des pièces fournies par l'opérateur; elles ne sont pas
copiées dans le dépôt.

## 6. Session de logs

La baseline de 60 fichiers a été capturée le 4 août 2026 à
`11:06:59Z`, avant le lancement. Les principaux fichiers courants étaient :

| Log | Taille avant | SHA-256 avant |
| --- | ---: | --- |
| `code_revisions.log` | 1133 | `8451065E4C94550523B0B4BC2EE12A4B4730E10A902AE9AEA72053F94CBA0F9D` |
| `system.log` | 1100 | `8259500C64CAE8626CA2AC4693617069AE21348745C637AC8C61EE94CC93F7DF` |
| `game.log` | 216575 | `0404C0BC2F72EC4372AB09C6F36BC232EA95FA2133F4F5FEEE374BC364EF3F59` |
| `error.log` | 103844 | `D4CB58ADE22D51A7749CB7408FEB401891798631A5FB9931C05623EB6AFB05F7` |
| `debug.log` | 227529 | `33CFE5B1880A6DDA87DAFCF732BED83A986D3AFA7E8A70790E3E3C0012791974` |
| `warning.log` | 6234 | `E3856863ED511228D607F042C9B6E8CEFD1B73E55FC0BD81C7CBF04F1D3253EB` |

La nouvelle session commence à `13:17:26` heure locale. Le journal de version
indique `release/1.13.0`. La transition vers la partie se termine à `13:25:53`,
le joueur est créé à `13:27:04`, puis la fermeture est enregistrée à
`13:35:01` et le retour `Game->Empty` à `13:35:02`.

Après la session :

| Log | Taille après | SHA-256 après |
| --- | ---: | --- |
| `code_revisions.log` | 1133 | `213E5D068DC164FF261BF9C815E3757A49A5056351A942A89F12860911FD0452` |
| `system.log` | 1100 | `E46B6FDC03C18851D6BB8FABB1471049226EF84097FA0ACE9DB8400F5714FEB7` |
| `game.log` | 427780 | `6D9F2D88FA999EAA819579830CFF513A8F8ACFE136C49ED6424D17C251B83A8D` |
| `error.log` | 124945 | `A43B489AAAA0610532DC167B76E0FAABE295BFEABDD5865E8F0EF39D0EE47938` |
| `debug.log` | 337201 | `9DE3CD6BE2E2A6CEBB3E647A9A97893059C4D4E920D5B02EB39DB12DD8881D3A` |
| `warning.log` | 6234 | `D16C70F44061CFC255E16683B9B9D279C4136E05078F19D5D8293C0761AF45BE` |

## 7. Diagnostics dédupliqués

Le diagnostic ciblé existe uniquement dans le `debug.log` courant :

```text
[13:24:15][jomini_effect.cpp:542]: Unknown effect add_declared_interest at common/history/interests/00_interests.txt:<ligne>
```

Déduplication par effet et fichier source :

| Effet | Fichier | Occurrences | Diagnostic dédupliqué |
| --- | --- | ---: | ---: |
| `add_declared_interest` | `common/history/interests/00_interests.txt` | 91 | 1 |
| `add_declared_interest` | `events/egyptian_crisis_events.txt` | 1 | 1 |
| `add_declared_interest` | `events/indochina.txt` | 1 | 1 |

Les 91 occurrences du fichier cible correspondent exactement aux 91 actions
actives de la baseline. La preuve positive du contrôle autrichien est :

```text
[13:24:15][jomini_effect.cpp:542]: Unknown effect add_declared_interest at common/history/interests/00_interests.txt:126
```

`game.log`, `error.log`, `warning.log`, `system.log` et
`dedicated_server.log` ne dupliquent pas ce diagnostic.

Deux erreurs `Unexpected token` mentionnent séparément `region_south_china` et
`region_canada` dans `common/ai_strategies/00_default_strategy.txt`. Elles ne
proviennent ni du fichier cible ni du bloc autrichien et ne sont pas utilisées
comme preuve de cette phase.

## 8. Comparaison et classification

| Contrôle | Historique attendu | Observation | Explication |
| --- | --- | --- | --- |
| Autriche / Sud de la Chine | action présente et région valide | aucune implication | effet rejeté explicitement à la ligne 126 |
| Autriche / Canada | action absente | aucune implication | témoin négatif conforme |

Le résultat correspond exactement au résultat B : positif absent, témoin
absent et diagnostic explicite ciblant l'effet et le fichier.

```text
DECLARED_INTEREST_LEGACY_EFFECT_RUNTIME_FAIL
DECLARED_INTEREST_HISTORY_API_INVALIDITY_CONFIRMED
```

Le chargeur historique atteint donc le fichier, mais aucune action n'est
exécutée parce que `add_declared_interest` est inconnu.

## 9. Conséquences

- Les 33 actions dont l'argument est une région stratégique 1.13 valide ne
  fonctionnent pas : le rejet porte sur l'effet avant toute sémantique de
  région.
- Les 58 actions utilisant 26 identifiants legacy ne fonctionnent pas non plus;
  leurs identifiants restent une dette séparée, mais leur remappage seul ne
  restaurerait aucun intérêt.
- Une correction directe n'est pas autorisée tant que le mécanisme 1.13
  d'initialisation d'une implication historique n'est pas démontré.
- Les cartographies protégées de GBR, BIC, Inde et Portugal restent inchangées.

Une seule prochaine phase est sélectionnée, sans être commencée :

```text
NEXT_EXECUTION_PHASE = HOTFIX_6A18R2_DECLARED_INTEREST_INITIALIZATION_MECHANISM_1_13_AUDIT
```

Elle doit rechercher le mécanisme 1.13 équivalent sans modifier les pays, les
régions, l'équilibrage ou le fichier gameplay testé.

## 10. Documents et contrôles finaux

Documents autorisés créés ou mis à jour :

- ce rapport;
- `docs/reports/hotfix/INDEX.md`;
- `HOTFIX_REPORT_INDEX.csv`;
- `HOTFIX_MERGE_BLOCK_STATUS.csv`;
- `HOTFIX_MERGE_COMPLETION_ROADMAP.md`;
- `HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`.

Aucun fichier gameplay, pays, loi, région ou intérêt n'est modifié. Aucun
commit n'est créé automatiquement. Le HEAD, l'index et le stash restent
inchangés. Victoria 3 et le launcher sont fermés après le runtime.

## 11. Verdicts

```text
HOTFIX_6A18Q_DECLARED_INTEREST_HISTORY_RUNTIME_VALIDATION_COMPLETE
DECLARED_INTEREST_POSITIVE_AND_NEGATIVE_CONTROLS_EXECUTED
DECLARED_INTEREST_RUNTIME_LOGS_DEDUPLICATED
NO_GAMEPLAY_CHANGED
NO_AUTOMATIC_COMMIT
STASH_NAVY_3C_3_INTACT
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
DECLARED_INTEREST_LEGACY_EFFECT_RUNTIME_FAIL
DECLARED_INTEREST_HISTORY_API_INVALIDITY_CONFIRMED
NEXT_EXECUTION_PHASE = HOTFIX_6A18R2_DECLARED_INTEREST_INITIALIZATION_MECHANISM_1_13_AUDIT
```
