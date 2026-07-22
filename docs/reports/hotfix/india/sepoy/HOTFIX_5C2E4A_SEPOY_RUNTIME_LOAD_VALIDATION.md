# HOTFIX-5C2E4A - Validation de chargement Uneasy Raj / Sepoy Mutiny

## 1. Resume

La validation fonctionnelle de chargement est positive : Victoria 3 atteint le menu principal, une partie avec la Compagnie des Indes orientales (`BIC`) démarre en 1776, un mois complet s'écoule sans crash et le jeu se ferme proprement. L'utilisateur confirme explicitement que `je_uneasy_raj` ne s'active pas spontanement.

La validation regionale est egalement positive : les cinq anciens identifiants de regions ont un total exact de zero occurrence dans les deux fichiers Sepoy et dans les trois logs examines.

La validation des logs n'est toutefois pas entierement acquise. `debug.log` contient quatre diagnostics propres a la chaine Sepoy :

- deux erreurs de lecture `Unexpected token: should_be_pinned_by_default` dans `common/journal_entries/04_sepoy_mutiny.txt`, lignes 430 et 619 ;
- deux echecs de PostValidate du trigger `has_role` dans `events/india_events/sepoy_mutiny_events.txt`, lignes 2742 et 2747.

Ces diagnostics n'ont pas empeche le chargement ni un mois de simulation. Ils doivent etre corriges dans une phase separee avant de declarer la chaine totalement propre pour Victoria 3 1.13.

**Verdict HOTFIX-5C2E4A : validation fonctionnelle reussie, validation regionale reussie, validation des logs partielle.**

## 2. Etat Git initial

- Branche : `hotfix-dlc-audit`.
- Commit de reference HOTFIX-5C2E4 : `a66c07a Audit final Sepoy runtime validation`.
- Aucun fichier suivi n'etait modifie au debut de la phase.
- Seule exception non suivie : `docs/research/technology/`.
- Stash detecte et laisse intact : `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla`.

## 3. Exception concurrente docs/research/technology

Le dossier non suivi `docs/research/technology/` etait present avant le test. Sept fichiers concurrents y ont ete inventories et haches avant la validation. Aucun n'a ete lu pour modifier son contenu, ajoute a Git, supprime ou renomme par cette phase.

Ce dossier ne fait pas partie du resultat HOTFIX-5C2E4A et reste une exception concurrente autorisee.

## 4. Verification statique

### Anciens identifiants regionaux

Comptage par identifiant complet, afin de ne pas confondre par exemple `region_bombay` avec l'identifiant valide `geographic_region_bombay_old` :

| Fichier | Bengal | Bombay | Central India | Madras | Punjab | Total |
|---|---:|---:|---:|---:|---:|---:|
| `common/journal_entries/04_sepoy_mutiny.txt` | 0 | 0 | 0 | 0 | 0 | 0 |
| `events/india_events/sepoy_mutiny_events.txt` | 0 | 0 | 0 | 0 | 0 | 0 |

Identifiants verifies :

- `region_bengal` ;
- `region_bombay` ;
- `region_central_india` ;
- `region_madras` ;
- `region_punjab`.

### Garde de demarrage

`je_uneasy_raj` conserve sa garde inactive :

```txt
possible = {
	always = no # For now
}
```

### Invariants proteges

- Aucun changement de date n'a ete effectue pendant cette phase.
- Aucune condition technologique n'a ete modifiee.
- Aucune loi de `BIC` n'a ete modifiee.
- `STATE_WEST_BENGAL` est reste inchange dans l'option `sepoy_mutiny_events.2.e`, ligne 1422.
- Aucun trigger, event, journal entry ou fichier gameplay n'a ete modifie.

## 5. Date et heure du lancement

- Processus `victoria3` detecte au lancement : **14 juillet 2026 vers 20:27:03 UTC**.
- Lecture des fichiers Sepoy pendant le chargement : **20:31:27**.
- PostValidate des scripts : **20:31:57**.
- Simulation observee en jeu : du **1er janvier 1776** au **1er fevrier 1776**.
- Fermeture propre confirmee par l'utilisateur.

## 6. Fraicheur des logs

Les logs ont ete regeneres pendant ce lancement et sont posterieurs au demarrage du processus :

| Log | Derniere ecriture UTC | Taille |
|---|---|---:|
| `debug.log` | 2026-07-14 20:40:14.379 | 523 528 octets |
| `error.log` | 2026-07-14 20:39:33.687 | 170 036 octets |
| `game.log` | 2026-07-14 20:39:33.687 | 475 601 octets |

`error.log` est donc bien frais et correspond au test manuel confirme.

## 7. Resultat du menu principal

**Reussi.** L'utilisateur confirme que le jeu se lance correctement et atteint le menu principal.

## 8. Resultat du chargement BIC

**Reussi.** Une nouvelle partie avec `BIC` en 1776 a ete lancee sans crash.

## 9. Resultat apres un jour

**Reussi au-dela du minimum demande.** La partie a simule un mois complet, jusqu'au 1er fevrier 1776, sans crash.

## 10. Etat de je_uneasy_raj

**Inactive.** L'utilisateur confirme explicitement que `je_uneasy_raj` ne s'active pas spontanement pendant le mois teste. La garde `possible = { always = no }` remplit donc son role au chargement et durant cette courte simulation.

## 11. Resultats des recherches de logs

### Anciens IDs Sepoy

Le comptage par identifiant complet donne zero occurrence dans `error.log`, `game.log` et `debug.log` pour chacun des cinq anciens IDs. Aucun `Invalid strategic region` ou `Unknown strategic region` ne leur est associe.

### Diagnostics propres aux fichiers Sepoy

| Log | Diagnostic | Fichier et ligne | Nombre |
|---|---|---|---:|
| `debug.log` | `Unexpected token: should_be_pinned_by_default` | `common/journal_entries/04_sepoy_mutiny.txt:430` | 1 |
| `debug.log` | `Unexpected token: should_be_pinned_by_default` | `common/journal_entries/04_sepoy_mutiny.txt:619` | 1 |
| `debug.log` | `PostValidate of trigger 'has_role' returned false` | `events/india_events/sepoy_mutiny_events.txt:2742` | 1 |
| `debug.log` | `PostValidate of trigger 'has_role' returned false` | `events/india_events/sepoy_mutiny_events.txt:2747` | 1 |

Aucun diagnostic Sepoy ne mentionne :

- `STATE_WEST_BENGAL` ou `STATE_BOMBAY` comme erreur ;
- `random_scope_state` ;
- `set_state_owner` ;
- une boucle `while` ;
- une erreur de scope propre aux remplacements regionaux ;
- l'execution de `sepoy_mutiny_events.2` ou `sepoy_mutiny_events.4`.

## 12. Analyse des erreurs

### should_be_pinned_by_default

Les lignes 430 et 619 portent chacune :

```txt
should_be_pinned_by_default = yes
```

Le lecteur 1.13 les signale comme tokens inattendus. L'impact apparent est non bloquant pendant ce test, mais ces deux erreurs constituent bien des erreurs de chargement provenant du fichier de journal Sepoy. Elles empechent de conclure a une validation totale des logs.

### has_role

Les lignes 2742 et 2747 appartiennent a `sepoy_mutiny_events.10` et utilisent :

```txt
has_role = general
```

Le moteur les rejette au PostValidate. La chaine etant inactive en 1776, ce trigger n'a pas ete execute fonctionnellement, mais il devra faire l'objet d'une correction syntaxique dediee et comparee a la vanilla 1.13.

### Erreurs `Invalid right side during comparison 'sr'`

`error.log` contient 864 occurrences, toutes attribuees a `common/journal_entries/01_natural_borders_of_france.txt` :

- ligne 128 : 288 occurrences ;
- ligne 129 : 288 occurrences ;
- ligne 130 : 288 occurrences.

Elles ne proviennent ni de `04_sepoy_mutiny.txt` ni de `sepoy_mutiny_events.txt`. Elles necessitent une phase separee et ne doivent pas etre corrigees dans HOTFIX-5C2E4A.

## 13. Differences non regionales detectees

| Motif | Resultat | Classification | Suite |
|---|---|---|---|
| `region_persia` | 1 erreur de lecture dans `common/ai_strategies/00_default_strategy.txt`, vers les lignes 4733-4747 | Erreur runtime/chargement hors Sepoy | Phase separee |
| `region_greater_persia` | 0 occurrence exacte dans les logs | Aucune erreur | Aucune action |
| `has_role = general` | Deux PostValidate Sepoy, lignes 2742 et 2747 | Erreur de validation non regionale | Phase Sepoy dediee |
| `has_role_of_type = general` | 0 occurrence dans les logs | Aucune erreur observee | Verifier la syntaxe vanilla avant correction |
| `KNO` | 0 occurrence exacte dans les logs | Aucune erreur | Aucune action |

Les recherches simples sur `KNO` peuvent produire de faux positifs dans le mot anglais `Unknown`. Le comptage rapporte ici uniquement le token exact `KNO`.

## 14. Observation sur « Bataille pour l'Inde »

Pendant l'initialisation de la partie BIC, l'utilisateur a vu l'entree/objective vanilla « Renforcer la domination coloniale » etre remplacee par l'objectif du mod « Bataille pour l'Inde ».

La lecture statique indique que ce comportement est intentionnel :

- `objective_battle_for_india` utilise le sous-objectif `sg_consolidate_india` ;
- le bloc `on_start` de ce sous-objectif ajoute `je_battle_for_india_goal` ;
- l'ajout intervient lorsque l'objectif selectionne est initialise apres l'entree dans la partie.

La transition visible pendant le chargement n'est donc pas une activation de `je_uneasy_raj`. Elle correspond au remplacement du journal d'objectif par le sous-objectif choisi. Aucun changement n'est recommande dans cette phase. Un audit UX distinct des objectifs serait necessaire uniquement si l'on souhaite masquer cette transition visuelle ou avancer son initialisation.

## 15. Ce que le test valide

- Le menu principal est accessible.
- Une partie `BIC` en 1776 se charge.
- Un mois passe sans crash.
- `je_uneasy_raj` reste inactive.
- Les cinq anciens IDs regionaux Sepoy sont absents des sources ciblees et des logs.
- Aucun echec regional Sepoy lie aux remplacements HOTFIX-5C2E1 a HOTFIX-5C2E3 n'apparait au simple chargement.
- Aucun probleme `random_scope_state`, `set_state_owner` ou boucle Sepoy n'apparait pendant le test passif.

## 16. Ce que le test ne valide pas

- Les options `sepoy_mutiny_events.2.a`, `.2.b`, `.2.c` et `.2.e`.
- Le trigger fonctionnel de `STATE_WEST_BENGAL`.
- Les transferts territoriaux et changements de proprietaire.
- La creation, la propagation et la resolution de la revolte.
- Les selections de capitales et de pays revoltes.
- Le comportement de `sepoy_mutiny_events.10` une fois la chaine active.
- La compatibilite de `should_be_pinned_by_default` et `has_role`, que les logs rejettent deja statiquement.

## 17. Etapes fonctionnelles restantes

1. Ouvrir une micro-phase de correction limitee aux deux occurrences de `should_be_pinned_by_default`, apres comparaison avec la syntaxe vanilla 1.13.
2. Ouvrir une micro-phase distincte pour les deux triggers `has_role = general` de `sepoy_mutiny_events.10`.
3. Relancer exactement le meme test BIC et exiger zero diagnostic provenant des deux fichiers Sepoy.
4. Tester ensuite la chaine active dans une sauvegarde ou un scenario controle, sans modifier sa garde chronologique dans cette phase.
5. Tester separement chaque option `.2.a`, `.2.b`, `.2.c` et `.2.e`, puis les transferts territoriaux.
6. Traiter `01_natural_borders_of_france.txt` et `region_persia` dans des phases independantes.

## 18. Liste exacte des fichiers crees

- `docs/reports/hotfix/HOTFIX_5C2E4A_SEPOY_RUNTIME_LOAD_VALIDATION.md`

Aucun autre fichier n'a ete cree par cette phase.

## 19. Confirmation d'absence de modification gameplay

Aucun fichier sous `common/`, `events/`, `map_data/` ou `localization/` n'a ete modifie. `STATE_WEST_BENGAL`, les lois BIC, les dates, les technologies et les triggers existants sont restes strictement inchanges.

## 20. Confirmations finales de perimetre

- `docs/research/technology/` n'a pas ete modifie, ajoute, supprime ou renomme par cette phase.
- Le stash `WIP NAVY-3C-3 Maratha Konkan Flotilla` reste present et n'a pas ete applique.
- Aucun changement BIC, Durrani, Famines, Railway, NAVY, ADMIN ou MARATH n'a ete effectue.
- Aucun commit automatique n'a ete cree.
