# HOTFIX-6A.1 — Alignement Russie / Subjecthood

Date : 2026-07-22  
Périmètre : correction gameplay ciblée et validation statique

## 1. Résumé

La Russie du fork activait encore `law_national_supremacy`, alors que le changelog hotfix 2.3, la source hotfix et vanilla 1.13 concordent sur `law_subjecthood`. Un seul hunk a remplacé cette activation. Aucun autre élément du setup RUS n’a changé.

## 2. Verdict d’entrée

`NEXT_MERGE_BLOCK = HOTFIX-6A_GLOBAL_SCRIPT_DELTAS`  
`NEXT_EXECUTION_PHASE = HOTFIX_6A_RUSSIA_SUBJECTHOOD_ALIGNMENT`

## 3. État Git initial

Racine exacte du fork, branche `hotfix-dlc-audit`, HEAD `0b08991 Reconcile global merge roadmap`, aucun fichier suivi modifié, aucun staged et seule exception non suivie `docs/research/technology/`. Le stash attendu était intact et aucun processus Victoria 3, dowser ou Paradox Launcher n’était actif.

## 4. Sources comparées

- fork : `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork\common\history\countries\rus - russia.txt`;
- hotfix, lecture seule : `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source\common\history\countries\rus - russia.txt`;
- vanilla 1.13, lecture seule : `C:\Games\Victoria 3 The Great Wave\game\common\history\countries\rus - russia.txt`.

SHA-256 : fork avant `A194CDED60E6C433775F4EA047DF1BCF8A6FC41CA0C85C755E7BDFF5CE8BC601`; fork après `7A5F1B1F60ACB4FEC9C600EACF33A0B03A382384ED3D7F57808E3A1D51DB6976`; hotfix `185154B5E9B1D3047B8B037E7113711561A5A6E00DD9F9AAD22B410BCB70E447`; vanilla `62D22FBF9CFC21AEE0F45AB2FFF33339492DB08FD7C343E0B1F97218DF674157`.

## 5. Changelog hotfix

`Changelog.txt`, ligne 8 : `Russia racial law is now subjecthood`. Cette annonce vise la loi de citizenship russe, pas une relation diplomatique de sujet.

## 6. Bloc Laws du fork

Avant correction, ligne 18 :

```text
activate_law = law_type:law_national_supremacy # needed so that e.g. Poles are discriminated against
```

Une occurrence active, aucune occurrence active de `law_subjecthood` et aucune occurrence active de `law_professional_navy`.

## 7. Bloc Laws de la source hotfix

Ligne 18 :

```text
activate_law = law_type:law_subjecthood # needed so that e.g. Poles are discriminated against
```

La source ajoute aussi `activate_law = law_type:law_professional_navy` ligne 25; ce second delta est exclu.

## 8. Bloc Laws de la vanilla 1.13

Vanilla active `law_subjecthood` ligne 18 et `law_professional_navy` ligne 21. La définition `law_subjecthood = {` existe dans `common/laws/00_citizenship.txt`, ligne 5. La localisation vanilla existe notamment en anglais (`Subjecthood`) et en français (`Sujétion`), donc aucune localisation mod n’est nécessaire.

## 9. Différences RUS complètes

Fork contre hotfix : remplacement citizenship plus ajout hotfix de `law_professional_navy`; toutes les autres lignes correspondent. Fork contre vanilla : les technologies de départ, colonisation, droits des femmes, modificateur, date de compagnie et plusieurs détails 1776 divergent intentionnellement. Les trois fichiers ne sont pas déclarés entièrement identiques après correction.

## 10. Hunk Subjecthood

Le hunk légitime est le remplacement ciblé de `law_national_supremacy` par `law_subjecthood`, même position et même commentaire.

## 11. Delta NAVY exclu

`law_professional_navy` reste absent du setup actif du fork avant comme après. Le delta hotfix/vanilla n’a pas été importé et demeure réservé à NAVY.

## 12. Setup 1776 préservé

Ordre des lois, `law_colonial_resettlement`, ligne commentée `law_frontier_colonization`, censure, taxation et setup général restent inchangés. `law_colonial_exploitation` n’a pas été introduite.

## 13. Technologies préservées

Tier 4, `line_infantry`, `colonization`, commentaire `corporate_charters` et `law_enforcement` sont inchangés.

## 14. Compagnies et modificateurs préservés

`modifier_colonial_efforts_mod`, `company_russian_american_company`, date `1769.7.8`, `STATE_INGRIA` et `ALK` sont inchangés.

## 15. Relations de sujet hors périmètre

Aucun fichier diplomatique ou de relation de sujet n’a été modifié. Le changement de loi n’exige aucune création ou modification de pacte diplomatique.

## 16. Modification appliquée

Un seul fichier gameplay et un seul hunk. Ligne 18 après correction :

```text
activate_law = law_type:law_subjecthood # needed so that e.g. Poles are discriminated against
```

## 17. Diff exact

```diff
-		activate_law = law_type:law_national_supremacy # needed so that e.g. Poles are discriminated against
+		activate_law = law_type:law_subjecthood # needed so that e.g. Poles are discriminated against
```

`git diff --numstat` : `1  1  common/history/countries/rus - russia.txt`.

## 18. Encodage et fins de ligne

UTF-8 avec BOM avant et après. 47 lignes, 47 fins LF, zéro CRLF avant et après. Taille passée de 1 484 à 1 477 octets uniquement parce que `law_subjecthood` est sept octets plus court que `law_national_supremacy`.

## 19. Validation des occurrences

Après correction dans le setup RUS : `law_subjecthood=1`, `law_national_supremacy=0`, `law_professional_navy=0`. Le fork référençait déjà `law_subjecthood` dans ses amendements et de nombreux setups pays, sans erreur connue.

## 20. Validation des accolades

Sept accolades ouvrantes et sept fermantes avant et après; équilibre conservé.

## 21. Validation Git

Le diff gameplay contient exactement une suppression et une addition. `git diff --check` est propre et aucun fichier n’est staged.

## 22. Décision runtime

Option 2 : report au runtime global consolidé. Le hunk est minimal, les deux sources concordent, la loi et ses localisations existent dans vanilla 1.13, aucune dépendance additionnelle n’est requise et la validation statique est propre.

## 23. Résultat runtime ou report

`RUSSIA_SUBJECTHOOD_RUNTIME_DEFERRED_TO_GLOBAL`.

Checklist RUS obligatoire du runtime global : charger 1776 avec le fork approprié seul; inspecter RUS; confirmer `Subjecthood`; vérifier les autres lois et l’absence de régression NAVY; fermer le jeu; analyser `error.log`, `game.log` et `debug.log` pour `law_subjecthood`, `law_national_supremacy`, `rus - russia.txt`, `RUS`, `Invalid scope`, `Invalid right side`, `Script system error`, `Unexpected token` et `PostValidate`. Un seul lancement consolidé, sans sauvegarde persistante.

## 24. Risques restants

Validation visuelle et logs encore différés; risque résiduel limité à une erreur runtime non visible statiquement. Le delta `law_professional_navy` reste volontairement non traité.

## 25. Fichiers modifiés

- gameplay : `common/history/countries/rus - russia.txt`;
- rapport : `docs/reports/hotfix/global_script/6A01_6A09/HOTFIX_6A_RUSSIA_SUBJECTHOOD_ALIGNMENT.md`;
- navigation : `docs/reports/hotfix/INDEX.md` et `docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv`.

## 26. Confirmation NAVY

Aucun fichier NAVY ou formation militaire modifié. `law_professional_navy` non importée.

## 27. Confirmation ADMIN

Aucun fichier ADMIN ou bâtiment modifié.

## 28. Confirmation MARATH

Aucun fichier MARATH modifié ou inspecté comme contenu de cette phase.

## 29. Confirmation docs/research/technology/

Le répertoire non suivi préexistant reste intact et hors périmètre.

## 30. Confirmation stash MARATH

`stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` est resté intact; aucun apply, pop ou drop.

## 31. Verdict final

- `RUSSIA_SUBJECTHOOD_ALIGNMENT_STATIC_PASS`
- `RUSSIA_SUBJECTHOOD_RUNTIME_DEFERRED_TO_GLOBAL`
- `RUSSIA_SUBJECTHOOD_ALIGNMENT_COMPLETE`
