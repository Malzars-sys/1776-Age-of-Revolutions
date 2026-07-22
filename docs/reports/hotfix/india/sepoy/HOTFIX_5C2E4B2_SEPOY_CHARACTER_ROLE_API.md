# HOTFIX-5C2E4B2 - API de role des personnages Sepoy

## 1. Resume

Les deux triggers `has_role = general` rejetes au PostValidate par Victoria 3
1.13 ont ete remplaces par l'API attestee dans les hunks homologues du hotfix
et de la vanilla The Great Wave :

```txt
has_role_of_type = general
```

Les deux remplacements se trouvent exclusivement dans
`sepoy_mutiny_events.10`. Aucun autre trigger, event, journal entry, region,
option, valeur, variable ou effet n'a ete modifie.

## 2. Etat Git initial

- Branche : `hotfix-dlc-audit`.
- HEAD initial : `2ca2a03 Update Sepoy journal pinning API`.
- Le commit HOTFIX-5C2E4B1 etait donc present.
- Aucun fichier suivi n'etait modifie.
- Seul `docs/research/technology/` apparaissait comme exception non suivie.
- Stash present et intact :
  `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla`.

## 3. Exception docs/research/technology

Les sept fichiers preexistants sous `docs/research/technology/` ont ete
inventories avec leur taille et leur empreinte SHA-256 avant la modification.
Ils n'ont ete ni modifies, ni ajoutes a Git, ni supprimes, ni renommes.

## 4. Deux occurrences identifiees

Le fichier `events/india_events/sepoy_mutiny_events.txt` contenait exactement
deux lignes correspondant a `has_role = general` :

| Ligne initiale | Event | Sous-bloc |
|---:|---|---|
| 2742 | `sepoy_mutiny_events.10` | `immediate -> if -> limit -> any_scope_character` |
| 2747 | `sepoy_mutiny_events.10` | `immediate -> if -> random_scope_character -> limit` |

`sepoy_mutiny_events.10` commence a la ligne 2721 et l'event suivant commence
a la ligne 2891. Les deux occurrences appartiennent donc sans ambiguite au
meme event cible.

## 5. Scopes et role fonctionnel

L'event est evalue depuis son scope pays. Dans son bloc `immediate` :

1. `any_scope_character` ouvre un scope personnage et verifie si le pays
   possede au moins un personnage dont le type de role est `general`.
2. Si ce test reussit, `random_scope_character` ouvre egalement un scope
   personnage ; son `limit` filtre les candidats sur le meme type de role.
3. Le personnage choisi est sauvegarde sous `sepoy_general_scope`.
4. Si aucun general n'existe, le bloc `else` conserve le comportement existant
   et sauvegarde le dirigeant comme solution de repli.

Les deux triggers sont donc bien evalues dans un **character scope**. La
correction ne change ni le groupe de personnages parcouru, ni le caractere
aleatoire de la selection, ni le scope sauvegarde, ni la solution de repli.

## 6. Comparaison fork / hotfix / vanilla

Fichiers compares :

- fork : `events/india_events/sepoy_mutiny_events.txt` ;
- hotfix :
  `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source\events\india_events\sepoy_mutiny_events.txt` ;
- vanilla :
  `C:\Games\Victoria 3 The Great Wave\game\events\india_events\sepoy_mutiny_events.txt`.

| Occurrence | Scope | Fork avant correction | Hotfix | Vanilla 1.13 | API attestee | Action |
|---|---|---|---|---|---|---|
| Test d'existence | Personnage dans `any_scope_character` | `has_role = general` | `has_role_of_type = general` | `has_role_of_type = general` | `has_role_of_type` | Remplacement exact |
| Filtre de selection | Personnage dans le `limit` de `random_scope_character` | `has_role = general` | `has_role_of_type = general` | `has_role_of_type = general` | `has_role_of_type` | Remplacement exact |

Les hunks hotfix et vanilla couvrant `immediate`, les deux tests, la sauvegarde
de scope et le fallback sont identiques caractere par caractere. La seule
divergence visee dans le fork etait le nom du trigger.

## 7. Recherche de l'API de role 1.13

La recherche a porte sur les events, scripted triggers et scripted effects de
la vanilla locale.

| Forme recherchee | Lignes | Fichiers |
|---|---:|---:|
| `has_role = general` exact | 0 | 0 |
| `has_role_of_type = general` exact | 182 | 47 |
| Tous les usages `has_role = ...` | 12 | 3 |
| Tous les usages `has_role_of_type = ...` | 577 | 79 |

Cette comparaison montre que `has_role` existe encore pour certains usages,
mais que la valeur de type `general` est exprimee avec
`has_role_of_type = general` en vanilla 1.13. De nombreux exemples vanilla
emploient cette syntaxe dans des scopes personnage, notamment dans
`events/commander_events.txt`.

La correction n'est donc pas fondee sur un renommage suppose : elle reproduit
exactement l'API et le scope des deux homologues officiels.

## 8. Decision appliquee

Les deux references convergeant, chaque ligne :

```txt
has_role = general
```

a ete remplacee par :

```txt
has_role_of_type = general
```

Apres correction :

- `has_role = general` exact : 0 occurrence dans le fichier ;
- `has_role_of_type = general` exact : 2 occurrences dans le fichier.

## 9. Diff exact

Le diff gameplay contient exactement :

```diff
@@ -2742 +2742 @@ sepoy_mutiny_events.10 = {
-                    has_role = general
+                    has_role_of_type = general
@@ -2747 +2747 @@ sepoy_mutiny_events.10 = {
-                    has_role = general
+                    has_role_of_type = general
```

Il comporte deux suppressions et deux ajouts. Aucune autre ligne n'apparait
dans le diff du fichier.

## 10. sepoy_mutiny_events.10 autrement inchange

Hormis les deux noms de trigger :

- l'ID de l'event est inchange ;
- son type, son placement, son image, ses textes et sa duree sont inchanges ;
- `any_scope_character` et `random_scope_character` sont inchanges ;
- `save_scope_as = sepoy_general_scope` est inchange ;
- le fallback vers `ruler` est inchange ;
- les conditions, options, modifiers, effets, valeurs et poids IA sont
  inchanges ;
- l'ordre de tous les blocs est inchange.

## 11. Options territoriales inchangees

`sepoy_mutiny_events.2`, `sepoy_mutiny_events.4` et leurs options territoriales
n'ont pas ete modifies. `STATE_WEST_BENGAL`, les transferts de states, les
radicaux, les selections territoriales et les changements de proprietaire sont
strictement inchanges.

## 12. Journal entry et pinning B1 inchanges

`common/journal_entries/04_sepoy_mutiny.txt` ne presente aucun diff pendant
HOTFIX-5C2E4B2.

La correction B1 reste presente :

- `should_be_pinned_by_default_involved = yes` : 2 occurrences ;
- `should_be_pinned_by_default_uninvolved_or_context = no` : 2 occurrences ;
- ancien champ autonome `should_be_pinned_by_default` : 0 occurrence.

La garde `possible = { always = no }`, les progress bars et toute l'activation
de la chaine restent inchangees.

## 13. Total regional global

Le recomptage des cinq anciens IDs dans `common/` et `events/`, commentaires
exclus et identifiants complets, donne toujours exactement **131** occurrences.

`events/india_events/sepoy_mutiny_events.txt` conserve un total exact de zero
ancien ID regional Sepoy.

## 14. Protocole du prochain test de chargement

1. Fermer completement Victoria 3.
2. S'assurer que les prochains logs seront frais, par horodatage ou en
   renommant les anciens logs avec accord de l'utilisateur.
3. Lancer le jeu avec le mod 1776 et ses seules dependances necessaires.
4. Atteindre le menu principal.
5. Charger ou demarrer une partie `BIC` en 1776.
6. Passer au moins un jour, idealement un mois.
7. Confirmer que `je_uneasy_raj` reste inactive.
8. Quitter proprement le jeu.
9. Examiner `error.log`, `game.log` et `debug.log` regeneres.

Le jeu n'a pas ete lance pendant HOTFIX-5C2E4B2.

## 15. Patterns de logs a verifier

Rechercher au minimum :

- `Unexpected token: should_be_pinned_by_default` ;
- `should_be_pinned_by_default_involved` ;
- `should_be_pinned_by_default_uninvolved_or_context` ;
- `PostValidate of trigger 'has_role' returned false` ;
- `has_role = general` ;
- `has_role_of_type = general` ;
- `04_sepoy_mutiny.txt` ;
- `sepoy_mutiny_events.txt` ;
- `Invalid scope` ;
- `PostValidate` ;
- `Parsing Error`.

Le resultat attendu est l'absence des quatre diagnostics Sepoy identifies en
HOTFIX-5C2E4A : deux tokens de pinning et deux PostValidate `has_role`.

## 16. Fichiers modifies ou crees

- Modifie : `events/india_events/sepoy_mutiny_events.txt`.
- Cree :
  `docs/reports/hotfix/HOTFIX_5C2E4B2_SEPOY_CHARACTER_ROLE_API.md`.

## 17. Confirmation du perimetre gameplay

Aucun autre fichier gameplay n'a ete modifie. En particulier :

- aucune journal entry ;
- aucune region ;
- aucun autre event ou trigger ;
- aucune option, valeur, variable ou effet ;
- aucune localisation ;
- aucun element relatif a `STATE_WEST_BENGAL`.

## 18. Confirmation docs/research/technology

Les sept fichiers concurrents sous `docs/research/technology/` n'ont pas ete
touches, ajoutes, supprimes ou renommes par cette phase.

## 19. Confirmation du stash MARATH

Le stash
`stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla`
reste present et intact. Aucun `git stash pop` n'a ete execute.

Aucun commit automatique n'a ete cree.
