# HOTFIX-6A.4F — Alignement Victoria 3 1.13 de Balkan National Awakening

Date : 29 juillet 2026

Phase : `HOTFIX_6A4F_BALKAN_NATIONAL_AWAKENING_1_13_ALIGNMENT`

Branche : `hotfix-dlc-audit`

HEAD initial :
`0c98edc2fbc4ccd50603f955d8b1c4ab691fd55e Select Balkan National Awakening 1.13 alignment`

## 1. Verdict

`HOTFIX_6A4F_BALKAN_NATIONAL_AWAKENING_1_13_STATIC_PASS`

`BALKAN_DANUBIA_INVALID_REGION_REMOVED`

`BALKAN_JE_PINNING_1_13_ALIGNED`

`HOTFIX_6A4F_BALKAN_NATIONAL_AWAKENING_1_13_RUNTIME_PASS`

`HOTFIX_6A4F_BALKAN_NATIONAL_AWAKENING_1_13_COMPLETE`

`GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`

Les deux incompatibilités Victoria 3 1.13 de
`je_balkan_national_awakenings` ont été corrigées dans un seul fichier. Le
runtime monté ne contient plus aucune erreur visant cet objet ou son fichier.

## 2. État Git initial

- racine :
  `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork` ;
- branche : `hotfix-dlc-audit` ;
- HEAD :
  `0c98edc2fbc4ccd50603f955d8b1c4ab691fd55e Select Balkan National Awakening 1.13 alignment` ;
- rapport 6A.4 présent dans le HEAD ;
- aucun fichier suivi modifié ;
- aucun fichier staged ;
- huit fichiers non suivis autorisés seulement : `bject` et les sept fichiers
  de `docs/research/technology/` ;
- stash intact :
  `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` ;
- Victoria 3 et le launcher fermés avant modification.

## 3. Sources consultées

Sources intégralement lues :

- `HOTFIX_6A4_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md` ;
- `HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
- `HOTFIX_MERGE_BLOCK_STATUS.csv` ;
- les versions fork, source hotfix et vanilla 1.13 de
  `common/journal_entries/05_balkan_national_awakening.txt` ;
- vanilla
  `common/geographic_regions/06_new_strategic_regions.txt` ;
- vanilla
  `common/strategic_regions/europe_strategic_regions.txt`.

Le `error.log` courant du 28 juillet 2026 à 23:51:25 a également été consulté.

## 4. Mesure initiale des erreurs

Avant correction :

- taille de `error.log` : 150 683 octets ;
- SHA-256 :
  `B181AB2803A529FA802BDB5564ACB57734FD2D97003E966BD5CD8062050BCD7E` ;
- erreurs visant directement
  `common/journal_entries/05_balkan_national_awakening.txt` : **51** ;
- erreurs associées
  `Invalid right side during comparison 'sr'` : **51** ;
- ligne source signalée : **11**.

## 5. Hunks appliqués

Premier hunk :

```diff
-		capital = {
-			OR = {
-				region = sr:region_balkans
-				region = sr:region_danubia
-			}
-		}
+		is_in_geographic_region = geographic_region_balkans
```

Second hunk :

```diff
-	should_be_pinned_by_default = yes
+	should_be_pinned_by_default_uninvolved_or_context = yes
```

Aucun autre champ de l’objet n’a changé.

## 6. Justification vanilla 1.13

Vanilla 1.13 définit une fois `geographic_region_balkans` dans
`common/geographic_regions/06_new_strategic_regions.txt`. Son bloc contient
exactement `sr:region_balkans`.

`common/strategic_regions/europe_strategic_regions.txt` contient une définition
active unique de `region_balkans` et zéro définition active de
`region_danubia`. Cette dernière ne subsiste que dans un bloc commenté.

La région balkanique active contient 36 États. Les 14 États de l’ancien bloc
danubien commenté sont tous présents dans cette région active : aucun État
danubien ne manque. La source hotfix emploie exactement le trigger
géographique retenu. La source hotfix et vanilla 1.13 convergent également sur
le nouveau champ de pinning.

## 7. Validations statiques

| Contrôle | Résultat |
|---|---:|
| Objets actifs `je_balkan_national_awakenings` dans le mod | 1 |
| Profondeur finale des accolades | 0 |
| Profondeur minimale | 0 |
| Occurrences actives de `sr:region_danubia` | 0 |
| Trigger `geographic_region_balkans` exact | 1 |
| Ancien champ de pinning dans l’objet | 0 |
| Nouveau champ de pinning exact | 1 |
| Définitions vanilla de `geographic_region_balkans` | 1 |
| Définitions vanilla actives de `region_balkans` | 1 |
| Définitions vanilla actives de `region_danubia` | 0 |
| Anciens États danubiens absents de `region_balkans` | 0 sur 14 |
| `git diff --check` | PASS |
| Index Git | vide |

Le diff gameplay est limité aux deux hunks fermés : deux insertions et sept
suppression de lignes. Le BOM UTF-8, les fins de ligne LF et le saut de ligne
final ont été conservés.

## 8. Préparation du runtime

Avant lancement :

- `content_load.json` contenait exactement un mod activé :
  `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork` ;
- `disabledDLC` était vide ;
- le répertoire vanilla `dlc/dlc014_ip3` était présent ;
- les dates, tailles et hashes des anciens `error.log`, `game.log` et
  `debug.log` ont été enregistrés ;
- la sauvegarde de continuation était en version 1.13.0, mais l’opérateur a
  créé une partie neuve en 1776.

## 9. Protocole runtime

Nombre de lancements complets : **1**.

Victoria 3 a été lancé une fois en `-debug_mode`. L’opérateur humain a pris la
main après le chargement, sans seconde ouverture. La Serbie n’existant pas
dans le setup du mod, la Valachie a été choisie. Ce choix est valide :
`STATE_WALLACHIA` appartient à `region_balkans`.

La partie a avancé du 1er janvier au 13 janvier 1776. Le
`dedicated_server.log` enregistre le passage de `1776.1.1` à `1776.1.13`,
soit plus que le minimum d’un jour requis.

## 10. Preuve du montage du fork et du DLC

`debug.1.log` contient :

- ligne 68 : le mod
  `1776 - Age of Revolutions, Total Conversion Mod` associé au chemin exact du
  fork ;
- ligne 87 : `Mounted Data` sur
  `C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork` ;
- une ligne `Mounted Data` distincte pour
  `C:/Games/Victoria 3 The Great Wave/game/dlc/dlc014_ip3`.

Le runtime est donc valide et ne reçoit pas le verdict
`RUNTIME_INVALID_MOD_NOT_MOUNTED`.

## 11. Résultat visible de la JE

La JE est restée inactive parce que la Valachie n’avait pas encore recherché
le nationalisme. Elle était néanmoins visible dans l’onglet **Potentiel** sous
le titre localisé **Éveil national**.

La capture fournie par l’opérateur confirme :

- aucune clé de localisation brute ;
- conditions d’activation et de fin lisibles ;
- statut de protectorat correctement reconnu ;
- description des effets lisible ;
- aucune anomalie évidente d’épinglage.

La ligne magenta affichant l’identifiant interne
`je_balkan_national_awakenings` est l’information normale du mode debug et non
une localisation manquante.

## 12. Analyse des logs après correction

Après fermeture normale du jeu :

- processus Victoria 3 et launcher : absents ;
- `error.log` courant : 249 829 octets ;
- `game.log` courant : 263 629 octets ;
- `debug.log` courant : 441 503 octets.

Le volume des erreurs a fait tourner `error.log`, `game.log` et `debug.log`.
Tous les fichiers de rotation créés pendant la session ont donc été inclus
dans le contrôle.

Résultat cumulé sur les logs de session :

- références à `05_balkan_national_awakening.txt` : **0** ;
- erreurs `Invalid right side during comparison 'sr'` attribuées au fichier :
  **0** ;
- erreurs visant `je_balkan_national_awakenings` : **0** ;
- erreurs visant `geographic_region_balkans` : **0** ;
- erreurs visant
  `should_be_pinned_by_default_uninvolved_or_context` : **0**.

Le nombre d’erreurs propres passe donc de **51 avant correction à 0 après
correction**.

## 13. Diagnostics hors périmètre

Les rotations `error*.log` de cette session contiennent 14 672 occurrences de
`Invalid right side during comparison 'sr'`, réparties entre 27 emplacements,
mais aucune ne vise le fichier balkanique corrigé.

Les principaux diagnostics restants concernent notamment :

- `common/journal_entries/01_natural_borders_of_france.txt` ;
- `common/journal_entries/00_major_railroads.txt` ;
- `common/journal_entries/07_american_mod_jes.txt` ;
- `common/journal_entries/02_south_america_migration.txt` ;
- `common/scripted_buttons/00_new_colonial_admins.txt` ;
- `common/ai_strategies/00_default_strategy.txt` ;
- `common/dynamic_country_names/00_dynamic_country_names.txt`.

Les anciens champs de pinning signalés dans de nombreux autres fichiers sont
également hors périmètre. Aucun de ces diagnostics n’a été corrigé ou absorbé
par 6A.4F.

## 14. Fichiers modifiés

Gameplay :

- `common/journal_entries/05_balkan_national_awakening.txt`.

Documentation :

- `docs/reports/hotfix/global_script/6A01_6A09/HOTFIX_6A4F_BALKAN_NATIONAL_AWAKENING_1_13_ALIGNMENT.md` ;
- `docs/reports/hotfix/INDEX.md` ;
- `docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv` ;
- `docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv` ;
- `docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
- `docs/reports/hotfix/_index/HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`.

## 15. Rollback exact

En cas de régression attribuable ultérieurement au patch :

1. remplacer uniquement
   `is_in_geographic_region = geographic_region_balkans` par :

   ```txt
   capital = {
   	OR = {
   		region = sr:region_balkans
   		region = sr:region_danubia
   	}
   }
   ```

2. remplacer uniquement
   `should_be_pinned_by_default_uninvolved_or_context = yes` par
   `should_be_pinned_by_default = yes` ;
3. ne restaurer aucun fichier complet.

Ce rollback réintroduirait volontairement la dette `region_danubia` et
imposerait un verdict d’échec.

## 16. Protections confirmées

Aucun fichier DEI/VOC, NAVY, formations militaires, MARATH/SAT/KHP,
Inde/BIC/Sepoy/Bombay, ADMIN, Japon, Russie, Autriche/Croatie/Suisse,
Révolution américaine ou française, technologie, localisation générale,
agriculture, alimentation, industrie, descripteur, launcher ou sauvegarde n’a
été modifié.

`activate_law = law_type:law_frontier_colonization` reste préservé pour BIC.
`bject`, les sept fichiers de `docs/research/technology/` et le stash
NAVY-3C-3 restent intacts.

## 17. État Git final et décision de commit

Le diff final contient uniquement le fichier gameplay et les six documents
autorisés ci-dessus. Les non-suivis préexistants restent les seuls autres
éléments affichés :

```text
 M common/journal_entries/05_balkan_national_awakening.txt
 M docs/reports/hotfix/INDEX.md
 M docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv
 M docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md
 M docs/reports/hotfix/_index/HOTFIX_NEXT_MERGE_PHASE_PROMPT.md
 M docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv
?? bject
?? docs/reports/hotfix/global_script/6A01_6A09/HOTFIX_6A4F_BALKAN_NATIONAL_AWAKENING_1_13_ALIGNMENT.md
?? docs/research/technology/
```

L’index Git reste vide. Aucun reset, restore, checkout, clean, merge, opération
de stash ou commit automatique n’a été exécuté.

La phase est prête pour un commit manuel ultérieur. Le prochain prompt ouvre
uniquement `HOTFIX_6A5_RESIDUAL_GLOBAL_SCRIPT_SELECTION` : il ne commence ni
Merchant Banking ni Navigation Acts.
