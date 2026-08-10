# HOTFIX-6A.18Q2 — QA runtime combinée des événements d'intérêt déclaré

## 1. Phase et résultat

- phase : `HOTFIX_6A18Q2_COMBINED_DECLARED_INTEREST_EVENT_RUNTIME_QA`;
- date : 4 août 2026;
- branche : `hotfix-dlc-audit`;
- HEAD initial et final :
  `9d11bb22bb710b3bf2b375aed1f47a24ee01b89c`;
- message du HEAD : `Remove obsolete Indochina interest logic`;
- runtime : une seule ouverture humaine de Victoria 3;
- gameplay, localisation et descripteurs : inchangés;
- commit automatique : aucun;
- résultat de l'arbre de décision : `B`.

Le fork et `dlc014_ip3` montent, une nouvelle partie autrichienne atteint le
3 janvier 1776, les six implications naturelles restent identiques et aucun
ancien intérêt n'apparaît ailleurs. La nouvelle session contient zéro
diagnostic pour les trois identifiants legacy, zéro chargement de l'ancien
fichier et zéro erreur attribuable aux corrections F1, F2 ou F3.

La commande console imposée `event egyptian_crisis_events.4` n'a toutefois pas
pu être prouvée avant l'ouverture. Conformément au protocole, aucune commande
alternative n'a été improvisée et l'impulsion égyptienne de 2500 n'est donc pas
validée sémantiquement.

## 2. Préflight

| Contrôle | Résultat |
| --- | --- |
| racine | fork exact |
| branche | `hotfix-dlc-audit` |
| HEAD | `9d11bb22bb710b3bf2b375aed1f47a24ee01b89c` |
| message HEAD | exact |
| rapport R3/F3 dans le HEAD | présent, 15 verdicts sur 15 |
| arbre suivi initial | propre |
| staged initial | vide |
| non suivis initiaux | `bject` et sept recherches technologiques |
| `git diff --check` initial | PASS |
| stash | ligne et objet exacts |
| processus Victoria 3, Dowser et launcher | zéro |

Le stash protégé reste :

```text
stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla
518df704fa14599c0f254fae13859210663dd976
```

## 3. Baselines statiques

| Cible | Résultat |
| --- | --- |
| `events/egyptian_crisis_events.txt` | SHA-256 `E637C1F8EF27BBEBCB43C516EB5F0E6C943ECC7A51FC1A06FCD73999547489F7` |
| bloc égyptien | `add_involvement`, `sr:region_near_east`, valeur 2500 |
| `events/indochina.txt` | SHA-256 `70965044236460BFD2ADE5EDE18A0BEF6DC2E1EEAFB496423E027E80091B28A9` |
| métadonnées Indochine | 9494 octets, 509 lignes, accolades 137/137 |
| `common/history/interests/00_interests.txt` | absent |
| `common/history/interests/` | absent |
| identifiants legacy actifs dans `common/` et `events/` | 0 |

## 4. Vérification de la commande console

L'exécutable 1.13 installé enregistre explicitement :

```text
testevent
Tests an event
event name
<country_TAG/province_ID>
```

Il ne fournit pas la même preuve pour la forme exigée
`event egyptian_crisis_events.4`. Aucun `console_history.txt` actuel n'existe;
les anciennes notes du dépôt qualifient les essais `event <id> <TAG>` de
probables mais non prouvés.

L'objet `egyptian_crisis_events.4` est statiquement autonome : il est de type
`country_event`, n'a pas de trigger et son `immediate` sauvegarde
`scope:egyptian_crisis_state` depuis la Syrie égyptienne ou, à défaut, depuis
la capitale de l'Égypte. Cette autonomie ne prouve pas la commande console.

Le protocole interdisant d'improviser une autre commande, ni `event` ni
`testevent` n'ont été exécutés. L'option `.4.a` et l'augmentation de 2500 ne
sont pas déclarées validées en jeu.

## 5. Manifeste des logs

### Avant l'ouverture

Capture UTC : `2026-08-04T15:30:02.0420090Z`.

```text
files = 60
bytes = 8760588
manifest SHA-256 = 2B111126A04FF174C9FAB754E50B814DCC1F0AAEA6C5DCD367622BD1BA643089
```

Le manifeste est le SHA-256 des lignes triées
`nom|taille|LastWriteTimeUtc ISO-8601|SHA-256`, jointes par LF.

### Après fermeture

Capture UTC : `2026-08-04T15:47:38.9808540Z`.

```text
files = 60
bytes = 8133027
manifest SHA-256 = 7BA49774EC0F4A121F3A313D4E5DD438C60674E048A9A195A745C672B0883EE3
```

Le changement de manifeste et les dates à partir de `15:33:14Z` isolent une
nouvelle session. Elle occupe 28 fichiers courants ou rotations pour
6 445 872 octets. Les rotations `.1` à `.5` créées pendant ce lancement sont
incluses; elles ne sont pas confondues avec les sessions plus anciennes.

## 6. Montage et progression

Les logs prouvent :

- moteur `release/1.13.0`;
- jeu monté depuis `C:/Games/Victoria 3 The Great Wave/game`;
- `dlc014_ip3` monté;
- seul mod utilisateur listé et monté :
  `1776_Age_of_Revolutions_fork`;
- progression enregistrée de `1776.1.1.6` à `1776.1.3.6`;
- pause finale le 3 janvier 1776.

Le warning de version du descripteur, `1.12.5` contre `1.13.0`, est antérieur
et extérieur aux corrections F1, F2 et F3.

## 7. Observations humaines

L'opérateur humain confirme une nouvelle partie avec l'Autriche, le fork monté,
une progression jusqu'au 3 janvier et la fermeture du jeu et du launcher.

| Région | Baseline F1 | Observation Q2 | Résultat |
| --- | ---: | ---: | --- |
| Balkans | 6324 | 6324 | PASS |
| Europe centrale | 4176 | 4176 | PASS |
| Europe de l'Est | 3969 | 3969 | PASS |
| Europe du Sud | 3320 | 3320 | PASS |
| Europe de l'Ouest | 2300 | 2300 | PASS |
| Europe du Nord | 1500 | 1500 | PASS |

La capture fournie montre les six valeurs exactes. Une seconde capture montre
`Aucune implication Autrichienne` au Sud de la Chine. L'opérateur indique
qu'aucun nouvel intérêt n'apparaît ailleurs, ce qui conserve aussi le Canada
comme contrôle négatif.

## 8. Déduplication des diagnostics ciblés

La session commence à `15:33:14Z`. Les recherches couvrent ses 28 fichiers,
notamment `debug.2.log` pour le montage, `debug.1.log` pour le parsing, les
rotations `error.*` et `game.*`, puis les fichiers courants de fermeture.

| Cible | Diagnostics de la session | Résultat |
| --- | ---: | --- |
| `add_declared_interest` | 0 | PASS |
| `num_declared_interests` | 0 | PASS |
| `max_num_declared_interests` | 0 | PASS |
| `00_interests.txt` | 0 | PASS |
| `common/history/interests` | 0 | PASS |
| `File not found` | 0 | PASS |
| `Could not open` | 0 | PASS |
| erreur sur `add_involvement` | 0 | PASS parser |
| erreur sur `region_near_east` | 0 | PASS parser |
| diagnostic sur `events/indochina.txt` | 0 | PASS |

La déduplication ciblée emploie le tuple
`(session, timestamp, message, chemin, ligne)`. Les 91 rejets de l'ancien
fichier, le rejet égyptien, le trigger indochinois et son effet sont présents
uniquement dans les rotations historiques. Le total historique de 94 devient
zéro dans Q2.

## 9. Diagnostics voisins séparés

Trois diagnostics portent un nom voisin sans être causés par F1, F2 ou F3 :

| Heure | Diagnostic | Chemin / ligne | Preuve historique |
| --- | --- | --- | --- |
| `17:39:14` | PostValidate `has_interest_marker_in_region` | `events/egyptian_crisis_events.txt:82` | identique à `14:59:46` et `13:24:25` |
| `17:39:14` | PostValidate `has_interest_marker_in_region` | `events/egyptian_crisis_events.txt:104` | identique à `14:59:46` et `13:24:25` |
| `17:38:39` | `Unexpected token: should_be_pinned_by_default` | `common/journal_entries/01_indochina.txt:82` | identique à `14:59:01` et `13:23:41` |

Les deux premiers visent les gardes de l'événement `.1`, pas le bloc
`add_involvement` de `.4.a` à la ligne 187. Le troisième vise une journal entry
séparée, pas `events/indochina.txt` ni `indochina.3`. Ils restent dans la revue
globale et ne constituent pas une régression Q2.

Les cinq `Unknown effect` de la session concernent uniquement
`every_country_in_iberia`, `generate_new_eic_government_leader` et `name`. Les
310 `Unknown trigger type` concernent `is_ruler`, `is_heir`, les anciennes API
navales, `has_port`, `any_country_in_iberia` et `value`. Aucun n'appartient au
système d'intérêts déclaré.

## 10. Résultat B

Le parsing combiné est propre, F1 ne régresse pas et F3 passe son contrôle
runtime. La sémantique de F2 reste incomplète parce que l'événement égyptien
n'a pas été déclenché et que l'augmentation exacte de 2500 n'a pas été
observée.

Le bloc complet ne reçoit donc pas `DECLARED_INTEREST_BLOCK_COMPLETE`, aucun
verdict de résultat A n'est émis et aucune phase suivante n'est sélectionnée.

```text
DECLARED_INTEREST_EVENT_PARSER_RUNTIME_PASS
EGYPTIAN_CRISIS_RUNTIME_SEMANTIC_VALIDATION_INCOMPLETE
INDOCHINA_LEGACY_REMOVAL_RUNTIME_PASS
NO_NEXT_EXECUTION_PHASE_SELECTED
```

## 11. Documentation

Six fichiers Markdown/CSV sont créés ou modifiés :

1. le présent rapport;
2. `docs/reports/hotfix/INDEX.md`;
3. `HOTFIX_REPORT_INDEX.csv`;
4. `HOTFIX_MERGE_BLOCK_STATUS.csv`;
5. `HOTFIX_MERGE_COMPLETION_ROADMAP.md`;
6. `HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`.

Aucun fichier gameplay, de localisation, de descripteur, de sauvegarde ou de
recherche protégée n'est modifié.

## 12. État final

- branche et HEAD inchangés;
- hashes égyptien et indochinois inchangés;
- ancien fichier et ancien dossier toujours absents;
- zéro identifiant legacy actif;
- uniquement cinq documents suivis modifiés et le présent rapport non suivi;
- index staged vide;
- stash intact;
- huit non-suivis protégés intacts;
- Victoria 3, Dowser et launcher Paradox fermés;
- `git diff --check` PASS;
- aucun commit automatique.

## 13. Verdicts finaux

```text
HOTFIX_6A18Q2_COMBINED_DECLARED_INTEREST_EVENT_RUNTIME_QA_COMPLETE
DECLARED_INTEREST_COMBINED_RUNTIME_LOGS_DEDUPLICATED
DECLARED_INTEREST_NATURAL_INVOLVEMENT_NON_REGRESSION_CHECKED
NO_GAMEPLAY_CHANGED
NO_AUTOMATIC_COMMIT
STASH_NAVY_3C_3_INTACT
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
DECLARED_INTEREST_EVENT_PARSER_RUNTIME_PASS
EGYPTIAN_CRISIS_RUNTIME_SEMANTIC_VALIDATION_INCOMPLETE
INDOCHINA_LEGACY_REMOVAL_RUNTIME_PASS
NO_NEXT_EXECUTION_PHASE_SELECTED
```
