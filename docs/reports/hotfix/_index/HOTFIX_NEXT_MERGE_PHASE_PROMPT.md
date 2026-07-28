# Phase HOTFIX-6A.4F — Alignement Victoria 3 1.13 de Balkan National Awakening

FORK : `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork`

SOURCE HOTFIX, LECTURE SEULE : `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source`

VANILLA 1.13, LECTURE SEULE : `C:\Games\Victoria 3 The Great Wave\game`

MODÈLE RECOMMANDÉ : GPT-5.6 Thinking avec raisonnement élevé.

## Verdicts d’entrée

- `HOTFIX_6A4_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE`
- `HOTFIX_6A3F_DEI_TARGETED_FIX_COMPLETE`
- `MILITARY_FORMATIONS_1_13_RUNTIME_QA_COMPLETE`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`
- `NO_GAMEPLAY_CHANGED`

Rapport d’entrée canonique :

`docs/reports/hotfix/_index/HOTFIX_6A4_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md`

## Objectif unique

Corriger uniquement les deux dettes Victoria 3 1.13 de
`je_balkan_national_awakenings` :

1. retirer la comparaison vers la région stratégique supprimée
   `sr:region_danubia` en adoptant le trigger géographique valide de la source
   hotfix ;
2. migrer le champ de pinning vers l’API 1.13.

Ne modifier aucun autre objet et ne commencer aucun autre résidu global.

## État Git requis

Exécuter avant toute modification :

```powershell
git rev-parse --show-toplevel
git branch --show-current
git status --short
git log -5 --oneline --decorate
git diff --check
git diff --cached --name-only
git stash list
```

Exiger :

- branche `hotfix-dlc-audit` ;
- rapport 6A.4 présent dans un HEAD propre, après commit manuel de la phase de
  sélection ;
- aucun fichier suivi modifié ;
- aucun fichier staged ;
- seuls `bject` et les sept fichiers de `docs/research/technology/` peuvent
  être non suivis ;
- stash exact
  `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` ;
- Victoria 3 et le launcher fermés.

Ne faire aucun reset, restore, checkout de fichier, clean, stash
apply/pop/drop, merge ou commit automatique. Ne pas inspecter le contenu du
stash.

## Sources obligatoires

Lire intégralement :

- `docs/reports/hotfix/_index/HOTFIX_6A4_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md` ;
- `docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
- `docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv` ;
- les versions fork, hotfix et vanilla 1.13 de
  `common/journal_entries/05_balkan_national_awakening.txt` ;
- vanilla
  `common/geographic_regions/06_new_strategic_regions.txt` ;
- vanilla
  `common/strategic_regions/europe_strategic_regions.txt`.

Consulter le dernier `error.log` en lecture seule pour enregistrer le nombre
initial d’occurrences de
`common/journal_entries/05_balkan_national_awakening.txt`. La preuve de
sélection en comptait 51 à la ligne 11.

## Liste exacte et fermée des fichiers modifiables

Gameplay :

- `common/journal_entries/05_balkan_national_awakening.txt`

Documentation :

- `docs/reports/hotfix/_index/HOTFIX_6A4F_BALKAN_NATIONAL_AWAKENING_1_13_ALIGNMENT.md`
- `docs/reports/hotfix/INDEX.md`
- `docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv`
- `docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv`
- `docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md`
- `docs/reports/hotfix/_index/HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`

Aucun autre fichier ne doit changer.

## Hunk 1 — région balkanique

Dans `je_balkan_national_awakenings`, remplacer exactement :

```txt
		capital = {
			OR = {
				region = sr:region_balkans
				region = sr:region_danubia
			}
		}
```

par :

```txt
		is_in_geographic_region = geographic_region_balkans
```

Justification fermée :

- `region_danubia` est commentée dans les régions stratégiques vanilla 1.13 ;
- `geographic_region_balkans` existe dans vanilla 1.13 ;
- elle contient `sr:region_balkans` ;
- `region_balkans` contient désormais les États autrefois danubiens ;
- la source hotfix emploie exactement ce trigger.

Ne modifier ni `possible`, ni `immediate`, ni les pulses, ni les conditions de
complétion.

## Hunk 2 — pinning 1.13

Dans le même objet, remplacer exactement :

```txt
	should_be_pinned_by_default = yes
```

par :

```txt
	should_be_pinned_by_default_uninvolved_or_context = yes
```

La source hotfix et vanilla 1.13 convergent sur ce champ. Ne migrer aucun autre
fichier de journal entries dans cette phase.

## Protections absolues

Ne toucher à aucun fichier ou objet relatif à :

- DEI/VOC, `events/dei_breakup.txt`, drapeau Java ou localisations économiques ;
- NAVY, lois navales, formations militaires ou événements technologiques
  navals ;
- MARATH, SAT, KHP ou Travancore ;
- Inde, BIC, Sepoy, Bombay ou noms dynamiques des présidences ;
- ADMIN ;
- Japon ;
- Russie ;
- Autriche, Croatie, Slavonie ou Suisse ;
- Révolution américaine ou française, lettres de Kew ;
- technologies ;
- localisations françaises générales ;
- agriculture, alimentation ou industrie générale ;
- `bject`, `docs/research/technology/`, descripteurs, launcher ou sauvegardes.

Préserver `activate_law = law_type:law_frontier_colonization` pour BIC.

## Contrôles statiques

Avant tout runtime, vérifier :

1. un seul objet `je_balkan_national_awakenings` ;
2. profondeur finale et minimale des accolades égales à `0` ;
3. zéro occurrence de `sr:region_danubia` dans le fichier modifié ;
4. une occurrence exacte de
   `is_in_geographic_region = geographic_region_balkans` dans l’objet ;
5. zéro `should_be_pinned_by_default =` dans l’objet ;
6. une occurrence exacte de
   `should_be_pinned_by_default_uninvolved_or_context = yes` ;
7. existence vanilla de `geographic_region_balkans` et de
   `sr:region_balkans` ;
8. diff gameplay limité aux deux hunks exacts ;
9. aucun changement hors liste fermée ;
10. `git diff --check` propre ;
11. `git diff --cached --name-only` vide.

Comparer le fichier modifié à HEAD par hunks. Ne jamais remplacer le fichier
global complet.

## Runtime consolidé

Le runtime est nécessaire pour fermer la phase, car la sélection repose sur une
erreur moteur répétée.

Après PASS statique uniquement :

1. archiver hors dépôt les logs courants ou noter leur horodatage de départ ;
2. ouvrir une seule fois Victoria 3 avec le playset montant exactement le fork
   et `ip3_content` disponible ;
3. charger une partie 1776 ou en créer une neuve ;
4. laisser passer au moins un jour afin que les JEs soient évaluées ;
5. confirmer l’absence de clé brute ou d’anomalie visible sur la JE si elle est
   accessible ;
6. fermer normalement le jeu ;
7. vérifier dans le nouveau `error.log` :
   - zéro occurrence de
     `common/journal_entries/05_balkan_national_awakening.txt` ;
   - zéro erreur `Invalid right side during comparison 'sr'` attribuée à cet
     objet ;
   - aucune nouvelle erreur visant
     `geographic_region_balkans` ou le champ de pinning.

Les erreurs d’autres fichiers sont hors périmètre. Ne lancer aucune seconde
session automatiquement. Si le fork monté n’est pas prouvé, déclarer le runtime
invalide.

## Rollback exact

En cas d’échec attribuable au patch :

1. remplacer uniquement
   `is_in_geographic_region = geographic_region_balkans` par l’ancien bloc
   `capital/OR` reproduit dans ce prompt ;
2. remplacer uniquement
   `should_be_pinned_by_default_uninvolved_or_context = yes` par
   `should_be_pinned_by_default = yes` ;
3. ne restaurer aucun fichier complet et ne toucher à aucune documentation
   antérieure.

Le rollback du premier hunk réintroduit la dette connue `region_danubia` :
publier alors un verdict d’échec, jamais un verdict de clôture.

## Livrables

- appliquer uniquement les deux hunks ;
- créer
  `HOTFIX_6A4F_BALKAN_NATIONAL_AWAKENING_1_13_ALIGNMENT.md` ;
- mettre à jour uniquement les cinq index/documentations autorisés ;
- publier les résultats statiques, runtime, le nombre d’erreurs avant/après et
  le diff final ;
- proposer ensuite une nouvelle phase de sélection résiduelle, sans commencer
  Merchant Banking ni Navigation Acts.

## Verdicts

Après PASS statique :

- `HOTFIX_6A4F_BALKAN_NATIONAL_AWAKENING_1_13_STATIC_PASS`
- `BALKAN_DANUBIA_INVALID_REGION_REMOVED`
- `BALKAN_JE_PINNING_1_13_ALIGNED`

Après runtime valide sans erreur propre :

- `HOTFIX_6A4F_BALKAN_NATIONAL_AWAKENING_1_13_RUNTIME_PASS`
- `HOTFIX_6A4F_BALKAN_NATIONAL_AWAKENING_1_13_COMPLETE`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`

Si le runtime n’est pas exécuté :

- `HOTFIX_6A4F_BALKAN_NATIONAL_AWAKENING_1_13_STATIC_PASS_RUNTIME_PENDING`

En cas d’échec, publier précisément :

- `HOTFIX_6A4F_BALKAN_NATIONAL_AWAKENING_1_13_STATIC_FAIL`, ou
- `HOTFIX_6A4F_BALKAN_NATIONAL_AWAKENING_1_13_RUNTIME_FAIL`.

Ne pas committer automatiquement.

## Vérifications finales

Exécuter :

```powershell
git diff --check
git status --short
git diff --name-only
git diff --name-status
git diff --stat
git diff --cached --name-only
git stash list
```

Confirmer :

- un seul fichier gameplay modifié ;
- seulement les documents autorisés ;
- aucun staged ;
- `bject` intact ;
- les sept fichiers de `docs/research/technology/` intacts ;
- stash NAVY-3C-3 intact ;
- DEI/VOC, formations militaires, NAVY et MARATH inchangés ;
- Victoria 3 et launcher fermés.
