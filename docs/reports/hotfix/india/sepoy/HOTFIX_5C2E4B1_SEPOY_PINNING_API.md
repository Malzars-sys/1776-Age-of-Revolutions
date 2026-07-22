# HOTFIX-5C2E4B1 - API de pinning Uneasy Raj / Sepoy Mutiny

## 1. Resume

Les deux lignes `should_be_pinned_by_default = yes` rejetees par Victoria 3
1.13 ont ete remplacees par l'API utilisee a l'identique dans les journal
entries homologues du hotfix et de la vanilla The Great Wave :

```txt
should_be_pinned_by_default_involved = yes
should_be_pinned_by_default_uninvolved_or_context = no
```

La correction porte uniquement sur `je_uneasy_raj` et `je_sepoy_mutiny` dans
`common/journal_entries/04_sepoy_mutiny.txt`. Aucun event, trigger, region,
parametre d'activation ou autre element gameplay n'a ete modifie.

## 2. Etat Git initial

- Branche : `hotfix-dlc-audit`.
- HEAD initial : `fc56ffb Validate Sepoy runtime loading`.
- Le commit HOTFIX-5C2E4A etait donc present.
- Aucun fichier suivi n'etait modifie.
- Seul `docs/research/technology/` apparaissait comme exception non suivie.
- Stash present et intact :
  `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla`.

## 3. Exception docs/research/technology

Les sept fichiers preexistants sous `docs/research/technology/` ont ete
inventories avec leur taille et leur empreinte SHA-256 avant la modification.
Ils n'ont ete ni modifies, ni ajoutes a Git, ni supprimes, ni renommes.

## 4. Deux occurrences identifiees

| Occurrence initiale | Journal entry | Position et role |
|---|---|---|
| Ligne 430 | `je_uneasy_raj` | Champ de premier niveau, place apres `weight = 100` et juste avant la fermeture de la JE. Les blocs `possible`, `complete`, `fail`, progress bars, pulses et `on_*` sont tous anterieurs. |
| Ligne 619 | `je_sepoy_mutiny` | Champ de premier niveau, place apres `weight = 100` et juste avant la fermeture de la JE. Les blocs `complete`, `fail` et `on_*` sont anterieurs. |

Avant correction, chaque objet contenait exactement :

```txt
should_be_pinned_by_default = yes
```

Le fichier contenait exactement deux occurrences de ce champ obsolete.

## 5. Comparaison fork / hotfix / vanilla

Fichiers compares :

- fork : `common/journal_entries/04_sepoy_mutiny.txt` ;
- hotfix :
  `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source\common\journal_entries\04_sepoy_mutiny.txt` ;
- vanilla :
  `C:\Games\Victoria 3 The Great Wave\game\common\journal_entries\04_sepoy_mutiny.txt`.

| JE | Fork avant correction | Hotfix | Vanilla 1.13 | API 1.13 valide | Action |
|---|---|---|---|---|---|
| `je_uneasy_raj` | Ancien champ unique `should_be_pinned_by_default = yes` | Paire `involved = yes` / `uninvolved_or_context = no`, lignes 416-417 | Meme paire, lignes 416-417 | Paire attestee | Remplacer uniquement l'ancien champ par la paire |
| `je_sepoy_mutiny` | Ancien champ unique `should_be_pinned_by_default = yes` | Paire identique, lignes 609-610 | Meme paire, lignes 609-610 | Paire attestee | Remplacer uniquement l'ancien champ par la paire |

Le hotfix et la vanilla contiennent d'autres differences autour de ces objets,
par exemple `can_revolution_inherit = yes` dans `je_uneasy_raj`. Elles n'ont
pas ete importees, car elles sont hors du perimetre de HOTFIX-5C2E4B1.

## 6. Recherche de l'API de pinning 1.13

La recherche recursive dans
`C:\Games\Victoria 3 The Great Wave\game\common\journal_entries` donne :

- zero ligne utilisant exactement l'ancien champ autonome
  `should_be_pinned_by_default = ...` ;
- 13 lignes utilisant `should_be_pinned_by_default_involved` ;
- 395 lignes utilisant
  `should_be_pinned_by_default_uninvolved_or_context` ;
- aucune API nommee `pinning` ou `default_pinned` dans ce dossier.

Une recherche brute de la sous-chaine `should_be_pinned_by_default` trouve
408 lignes, car elle est incluse dans les deux noms d'API valides. Elle ne
constitue pas une preuve de conservation de l'ancien champ. Le controle par
ligne exacte confirme que ce dernier est absent de la vanilla 1.13.

Les deux objets homologues hotfix et vanilla emploient exactement la meme
paire et les memes valeurs. Le remplacement est donc directement atteste ;
aucune API n'a ete inventee ou extrapolee.

## 7. Decision appliquee

Le **cas 2, remplacement atteste**, a ete retenu.

Chaque ligne obsolete a ete remplacee par :

```txt
should_be_pinned_by_default_involved = yes
should_be_pinned_by_default_uninvolved_or_context = no
```

Cette paire conserve l'intention de pinning pour le pays implique tout en
indiquant explicitement que les pays non impliques ou de contexte ne doivent
pas recevoir l'epingle par defaut.

Apres correction :

- ancien champ autonome : 0 occurrence ;
- `should_be_pinned_by_default_involved = yes` : 2 occurrences ;
- `should_be_pinned_by_default_uninvolved_or_context = no` : 2 occurrences.

## 8. Diff exact

Le diff gameplay contient uniquement les deux remplacements suivants :

```diff
-	should_be_pinned_by_default = yes
+	should_be_pinned_by_default_involved = yes
+	should_be_pinned_by_default_uninvolved_or_context = no
```

Ce hunk apparait une fois a la fin de `je_uneasy_raj` et une fois a la fin de
`je_sepoy_mutiny`. Aucune autre ligne du fichier n'a change.

## 9. Activation des journal entries inchangee

La garde de `je_uneasy_raj` est conservee :

```txt
possible = {
	always = no # For now
}
```

Les gardes de date et de technologie commentees, l'ajout contextless commente,
les conditions `complete` et `fail`, les hidden triggers, les pulses, les
timers et les poids `weight = 100` sont inchanges.

La correction ne rend donc pas la chaine accessible plus tot et ne modifie pas
son comportement chronologique.

## 10. Progress bars inchangees

Toutes les progress bars Bengal, Bombay et Madras, leurs variables, leurs
seuils et leurs calculs sont inchanges. Le diff ne touche que les champs de
pinning situes apres les blocs fonctionnels des deux journal entries.

## 11. Events et has_role inchanges

`events/india_events/sepoy_mutiny_events.txt` ne presente aucun diff.

Les deux occurrences de `has_role = general` signalees aux lignes 2742 et
2747 restent strictement inchangees. Leur traitement demeure reserve a
HOTFIX-5C2E4B2.

`STATE_WEST_BENGAL`, les selections de states, les transferts territoriaux et
les effets des events n'ont pas ete modifies.

## 12. Total regional global

Le recomptage des cinq anciens IDs dans `common/` et `events/`, commentaires
exclus et identifiants complets, donne toujours exactement **131** occurrences.

| Fichier | Occurrences |
|---|---:|
| `common/ai_strategies/00_default_strategy.txt` | 43 |
| `common/scripted_buttons/00_new_colonial_admins.txt` | 40 |
| `common/history/military_formations/05_military_formations_india.txt` | 23 |
| `common/dynamic_country_names/00_dynamic_country_names.txt` | 10 |
| `common/journal_entries/07_hindustan_is_durrani_mod.txt` | 6 |
| `common/character_templates/country_bic.txt` | 2 |
| `common/history/interests/00_interests.txt` | 2 |
| `common/history/military_formations/04_military_formations_middle_east.txt` | 2 |
| `common/journal_entries/00_player_objectives_great_game.txt` | 2 |
| `common/history/military_formations/00_military_formations_europe.txt` | 1 |
| **Total** | **131** |

Les deux fichiers Sepoy conservent chacun un total exact de zero ancien ID.

## 13. Test de chargement recommande

1. Fermer completement Victoria 3.
2. Lancer le jeu avec le mod 1776 et ses seules dependances necessaires.
3. Atteindre le menu principal puis charger une partie `BIC` en 1776.
4. Passer au moins un jour, idealement un mois.
5. Confirmer que `je_uneasy_raj` reste inactive.
6. Quitter proprement le jeu.
7. Verifier dans les logs frais l'absence de
   `Unexpected token: should_be_pinned_by_default` pour
   `04_sepoy_mutiny.txt`.
8. Ne pas confondre ce resultat avec les deux erreurs `has_role`, attendues
   jusqu'a HOTFIX-5C2E4B2.

## 14. Fichiers modifies ou crees

- Modifie : `common/journal_entries/04_sepoy_mutiny.txt`.
- Cree : `docs/reports/hotfix/HOTFIX_5C2E4B1_SEPOY_PINNING_API.md`.

## 15. Confirmation du perimetre gameplay

Aucun autre fichier gameplay n'a ete modifie. En particulier :

- aucun event ou trigger `has_role` ;
- aucune region north/south ;
- aucune activation, date ou technologie ;
- aucune progress bar ou variable ;
- aucune localisation ;
- aucun fichier relatif a `STATE_WEST_BENGAL`.

## 16. Confirmation docs/research/technology

Les sept fichiers concurrents sous `docs/research/technology/` n'ont pas ete
touches, ajoutes, supprimes ou renommes par cette phase.

## 17. Confirmation du stash MARATH

Le stash
`stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla`
reste present et intact. Aucun `git stash pop` n'a ete execute.

Aucun commit automatique n'a ete cree.
