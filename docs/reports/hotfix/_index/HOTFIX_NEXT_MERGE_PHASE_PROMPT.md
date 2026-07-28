# Phase HOTFIX-6A.3F — Correction ciblée DEI Cape/Ceylon et vanilla 1.13 — TERMINÉE

FORK : `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork`

SOURCE HOTFIX, LECTURE SEULE : `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source`

VANILLA 1.13, LECTURE SEULE : `C:\Games\Victoria 3 The Great Wave\game`

MODÈLE RECOMMANDÉ : GPT-5.6 Thinking avec raisonnement élevé.

> **Statut d’archive :** ce prompt a été exécuté. Ne pas relancer cette phase. Le rapport canonique de clôture est `HOTFIX_6A3F_DEI_TARGETED_FIX.md`.

## Verdicts d’entrée historiques déjà consommés

- `HOTFIX_6A3R_DEI_BREAKUP_HUNK_RESOLUTION_COMPLETE`
- `READY_FOR_DEI_TARGETED_FIX`
- `CEYLON_SHOULD_BECOME_INDEPENDENT`
- `CAPE_SHOULD_BECOME_INDEPENDENT`
- `NO_GAMEPLAY_CHANGED`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`

## Objectif unique

Appliquer dans `dei_breakup.1` les trois blocs territoriaux résolus et les sept alignements vanilla 1.13 admis, puis effectuer tous les contrôles statiques. Ne modifier aucun autre gameplay et ne pas committer automatiquement.

## État Git requis

Exécuter `git rev-parse --show-toplevel`, `git branch --show-current`, `git status --short`, `git log -1 --oneline`, `git diff --check`, `git diff --cached --name-only` et `git stash list`.

Exiger branche `hotfix-dlc-audit`, rapport 6A.3R présent, zéro fichier suivi modifié, zéro staged, stash MARATH intact, `docs/research/technology/` et `bject` intacts, Victoria 3 et launcher fermés. Ne faire aucun reset, restore, checkout, clean, stash apply/pop/drop ou commit. Ne pas inspecter le stash.

## Sources obligatoires

Lire intégralement :

- `docs/reports/hotfix/_index/HOTFIX_6A3R_DEI_BREAKUP_HUNK_RESOLUTION.md` ;
- `docs/reports/hotfix/_index/HOTFIX_6A3_DEI_TARGETED_AUDIT.md` ;
- `docs/reports/hotfix/_index/HOTFIX_6A3_DEI_TARGETED_AUDIT_DELTA_MAP.csv` ;
- les trois versions de `events/dei_breakup.txt`.

Ne pas utiliser `rg`. Extraire `dei_breakup.1` et `alk_breakup.1` par ancres et équilibre d’accolades avant toute modification.

## Liste fermée des fichiers modifiables

Gameplay :

- `events/dei_breakup.txt`

Documentation :

- `docs/reports/hotfix/_index/HOTFIX_6A3F_DEI_TARGETED_FIX.md`
- `docs/reports/hotfix/_index/HOTFIX_6A3_DEI_TARGETED_AUDIT_DELTA_MAP.csv`
- `docs/reports/hotfix/INDEX.md`
- `docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv`
- `docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv`
- `docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md`
- `docs/reports/hotfix/_index/HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`

Aucun autre fichier ne doit changer.

## Hunk territorial exact

Dans l’option `dei_breakup.1.a`, insérer exactement avant le `while` existant :

```txt
		# Release the non-Indonesian colonial territories before the breakup loop.
		if = {
			limit = {
				s:STATE_CEYLON = {
					any_scope_state = { owner = ROOT }
				}
			}
			if = {
				limit = { exists = c:CEY }
				s:STATE_CEYLON.region_state:DEI ?= { set_state_owner = c:CEY }
			}
			else = {
				create_country = {
					origin = ROOT
					tag = CEY
					state = s:STATE_CEYLON.region_state:DEI
				}
			}
			c:CEY ?= {
				if = {
					limit = { is_subject = yes }
					make_independent = yes
				}
			}
		}
		if = {
			limit = {
				s:STATE_CAPE_COLONY = {
					any_scope_state = { owner = ROOT }
				}
			}
			if = {
				limit = { exists = c:SAF }
				s:STATE_CAPE_COLONY.region_state:DEI ?= { set_state_owner = c:SAF }
			}
			else = {
				create_country = {
					origin = ROOT
					tag = SAF
					state = s:STATE_CAPE_COLONY.region_state:DEI
				}
			}
			c:SAF ?= {
				if = {
					limit = { is_subject = yes }
					make_independent = yes
				}
			}
		}
		if = {
			limit = { exists = c:SAF }
			s:STATE_EASTERN_CAPE.region_state:DEI ?= { set_state_owner = c:SAF }
		}
```

Ne transférer aucune province MLD, GBR, NAM ou XHO. Ne modifier aucun claim, traité, bâtiment, pop ou historique d’État.

## Sept alignements exacts

Dans `dei_breakup.1` seulement, faire correspondre exactement les groupes suivants au bloc DEI de la source hotfix/vanilla 1.13 :

1. insérer le bloc `ig:ig_devout` Sunni Ulema lignes hotfix 107–112 avant `change_tag = JAV` ;
2. remplacer le nettoyage cultures/personnages JAV par les lignes hotfix 115–136 ;
3. utiliser `trigger_event = { id = independence.2 days = 1 }` ligne hotfix 137 ;
4. insérer le bloc `ig:ig_devout` Sunni Ulema lignes hotfix 155–160 pour IDN ;
5. remplacer le nettoyage cultures/religion/personnages IDN par les lignes hotfix 162–182 ;
6. utiliser le délai d’un jour ligne hotfix 183 ;
7. utiliser le délai d’un jour dans l’option de refus ligne hotfix 195.

Après application, la partie située de `ig:ig_industrialists` de l’option `a` jusqu’à la fin de `dei_breakup.1` doit être identique à vanilla 1.13, à l’exception du hunk territorial ajouté avant le `while` et de toute différence strictement antérieure déjà documentée. Ne remplacer ni le fichier complet ni `alk_breakup.1`.

## Rollback exact

- territoire : supprimer les trois blocs `if` ajoutés avant `while` ;
- Ulema JAV/IDN : supprimer seulement les deux blocs `ig:ig_devout` ;
- JAV : restaurer le bloc fork `remove_primary_culture = cu:dutch`, ajout javan, religion sunnite, `state_religion_switch_effect` et `kill_character` ;
- IDN : restaurer le bloc fork `remove_primary_culture = cu:dutch`, huit cultures et `kill_character`, sans reset sunnite ;
- délais : retirer uniquement `days = 1` des trois appels.

## Protections absolues

Ne toucher ni NAVY, `Koloniale_Marine`, ADMIN, BIC, Travancore, Inde, MARATH/SAT/KHP, Japon, Mamluk Iraq, Russie, Autriche/Croatie/Suisse, localisations françaises, descripteurs, launcher, sauvegardes, `docs/research/technology/` ou `bject`. Préserver les six fichiers gameplay 6A.2. Conserver `activate_law = law_type:law_frontier_colonization` pour BIC et ne jamais restaurer `law_colonial_exploitation`.

`alk_breakup.1` est hors périmètre et doit rester byte-for-byte identique à HEAD.

## Tests statiques avant jeu

Vérifier :

- équilibre d’accolades et unicité de `dei_breakup.1`/`alk_breakup.1` ;
- égalité byte-for-byte de `alk_breakup.1` avec HEAD ;
- présence unique des trois blocs territoriaux ;
- existence des tags CEY/SAF et des trois state scopes ;
- présence exacte des deux blocs Ulema, deux nettoyages et trois délais ;
- absence de `kill_character` dans le bloc DEI corrigé ;
- aucune modification hors liste fermée ;
- `git diff --check` propre et staged vide.

## Runtime unique

Un runtime n’est autorisé qu’après PASS statique. Préparer toutes les observations avant lancement et condenser en une seule ouverture : charger le fork 1776, déclencher l’option `a`, vérifier CEY/SAF indépendants et les owners exacts, vérifier MLD/GBR/NAM/XHO, pops/bâtiments/claims/traités, cultures/religion/Ulema/personnages JAV, puis exploiter des sauvegardes préparées pour IDN/refus si disponibles. Scanner `error.log`. Si le montage du fork n’est pas prouvé, déclarer le runtime invalide sans second lancement automatique.

## Livrables et verdicts

Créer `HOTFIX_6A3F_DEI_TARGETED_FIX.md`, mettre à jour la delta map et uniquement les index autorisés. Toujours publier :

- `HOTFIX_6A3F_DEI_TARGETED_FIX_STATIC_PASS` si tous les contrôles statiques passent ;
- `DEI_TERRITORIAL_RELEASE_HUNKS_APPLIED` ;
- `DEI_VANILLA_1_13_ALIGNMENT_APPLIED` ;
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`.

Ne publier `HOTFIX_6A3F_DEI_TARGETED_FIX_COMPLETE` qu’après runtime valide ; sinon publier précisément le statut runtime restant. Ne pas committer automatiquement.

## Vérifications finales

Exécuter `git diff --check`, `git status --short`, `git diff --name-only`, `git diff --name-status`, `git diff --stat`, `git diff --cached --name-only`, `git stash list` et le contrôle des processus. Confirmer le diff gameplay limité à `events/dei_breakup.txt`, zéro staged, protections intactes, `docs/research/technology/` et `bject` intacts, stash MARATH intact.

## Addendum courant — extension runtime autorisée le 28 juillet 2026

Les instructions initiales ci-dessus décrivent le périmètre d’entrée historique. Le runtime a depuis confirmé CEY/SAF et a révélé deux dépendances du setup 1776. L’opérateur a explicitement autorisé l’extension suivante :

- `common/flag_definitions/00_flag_definitions.txt` : drapeau Java post-VOC séparé du nom dynamique Malaisie ;
- `localization/english/mod_v2content_l_english.yml` et `localization/french/mod_v2content_l_french.yml` : localisation de `dei_breakup.2` ;
- `events/dei_breakup.txt` : nettoyage VOC et événement économique post-compagnie.

Le statut final est `HOTFIX_6A3F_DEI_TARGETED_FIX_COMPLETE`. Ne pas recommencer l’audit ni lancer le jeu automatiquement. Le runtime confirme le drapeau Java, l’événement économique, l’absence d’interventionnisme lorsque les Industriels sont faibles et le servage actif, puis la persistance du Mouvement agraire, du nom et du drapeau après sauvegarde/rechargement. Les branches Indonésie et refus sont validées. Les textes économiques français et anglais ont été développés au format narratif de « Jour de l’indépendance ».

La chaîne historique des lettres de Kew et la prise britannique du Cap et de Ceylan sont hors périmètre. Elles sont reportées au futur contenu Révolution française/Napoléon.
