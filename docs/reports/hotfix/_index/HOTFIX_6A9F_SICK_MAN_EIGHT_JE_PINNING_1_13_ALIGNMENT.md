# HOTFIX-6A.9F — Alignement Victoria 3 1.13 des huit pinning Sick Man

## 1. Identification

- Date : 29 juillet 2026.
- Phase :
  `HOTFIX_6A9F_SICK_MAN_EIGHT_JE_PINNING_1_13_ALIGNMENT`.
- Branche : `hotfix-dlc-audit`.
- HEAD initial :
  `deb2f1e216e26b8e9182c1ea9b0ab5fd7daca593`.
- HEAD au PASS statique :
  `deb2f1e216e26b8e9182c1ea9b0ab5fd7daca593`.
- Nature : correction API atomique, suivie d’un smoke parser humain.
- Statut courant : PASS statique et runtime humain acquis.

## 2. Préflight

Le préflight obligatoire passe :

- racine exacte du fork ;
- branche `hotfix-dlc-audit` ;
- rapport 6A.9R et ses neuf verdicts présents dans le HEAD ;
- 6A.9R commitée manuellement ;
- worktree suivi propre et index staged vide ;
- seuls `bject` et les sept fichiers de `docs/research/technology/` non suivis ;
- stash exact :
  `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` ;
- aucun processus Victoria 3, dowser ou Paradox.

État Git initial :

```text
?? bject
?? docs/research/technology/
```

## 3. Hashes protégés

| Élément | SHA-256 |
| --- | --- |
| `bject` | `A6D3772BDFBFA8E9987DE8753D52079062AAC7F3277FEE22C338AA4AF2D6171B` |
| `TECH_TREE_BUILDING_AND_PRODUCTION_CANDIDATES.csv` | `315CB857B94D547492E1F7C36E10A67EF53DBCBDA0FF63CBA4246DBA7B6FC6D5` |
| `TECH_TREE_INDUSTRIAL_CHAINS.md` | `88D090A496C1C3CDB8A04D24AA2E31369E6AB6FAD843052CBE4C26467F4AA410` |
| `TECH_TREE_INDUSTRIAL_HISTORY_DEEP_RESEARCH.md` | `0FE06A1843F5B67413E222ECFDABBF4E6957EAA2E97D466A018C59FA27DA4596` |
| `TECH_TREE_INDUSTRIAL_INNOVATIONS_DATABASE.csv` | `01A37C0BD8BE839EC59E11AA4742CB4D96824EEAFCEA94979839391D8798094D` |
| `TECH_TREE_RESEARCH_BIBLIOGRAPHY.md` | `C4EF474D8C1502DBC1D36A9D52473EE4B5E41C3D14A2081F1A526B9383FF1AF5` |
| `TECH_TREE_RESOURCE_CANDIDATES.csv` | `6E7A48765FB9C20A4F8992D1CCD32BB75340A7BD6FC00B365E503F930BFD8F9A` |
| `TECH_TREE_VICTORIA3_GAP_ANALYSIS.md` | `150256D3C56333CAF8C37A7631074110060678FC115DB24FC48F702DFD6840FA` |

Les huit hashes sont identiques avant et après la correction statique.

## 4. Hashes trois voies et non-régressions

| Preuve | SHA-256 | Résultat |
| --- | --- | --- |
| Fork `00_sick_man.txt` avant | `DC6AC302555035C574CFC61A91FBF667BE981FEFA2C1D8FA271A6F530B3054D8` | conforme |
| Fork `00_sick_man.txt` après | `B04C07388C944E5DA74CFCE142599797F582EA809412B9690170735BFA17B04A` | conforme |
| Source hotfix `00_sick_man.txt` | `E48405BFABB52F6CE757880E436C8D44C67111E246AF3215FD3F96EC4F3477F9` | inchangé |
| Vanilla `00_sick_man.txt` | `1EAD43BE40DAF22D585712442AFD379C893C3075007CDA0AADDB126CCF1DCA41` | inchangé |
| Histoire TUR fork | `81ABC8DEA9DE93EC6A4DD417FD05FD6859F3122758D2B27E712B1880013F9CA9` | inchangée |
| Grande Crise orientale fork | `96F65E2B3CC7129DD8D4AD41382F9F8DD97FB5FA24C66C05F129B1E31615F75A` | inchangée |
| Événements Sick Man source/vanilla | `D110D1FD83CD98E131D4C2769B606CC908F17844EFF88EF65F51FEBF313A0C2B` | inchangés |
| Événements Tanzimat source/vanilla | `F5DAABC9D36BEAE714E5BDFC3B156995B3EAE7758004CE3C7B8C3512BA80AD30` | inchangés |

L’histoire TUR conserve commentés `sick_man.1`, `sick_man_of_europe` et
`outmoded_bureaucracy`. BIC conserve
`activate_law = law_type:law_frontier_colonization` et ne contient pas
`law_colonial_exploitation`.

## 5. Snapshot structurel

| Mesure | Avant | Après | Attendu |
| --- | ---: | ---: | ---: |
| Octets | 8 703 | 8 879 | 8 879 |
| UTF-8 BOM | oui | oui | oui |
| LF | 501 | 501 | 501 |
| CRLF | 0 | 0 | 0 |
| Saut final | oui | oui | oui |
| Accolades ouvrantes | 117 | 117 | 117 |
| Accolades fermantes | 117 | 117 | 117 |
| Ancienne propriété | 8 | 0 | 0 |
| Nouvelle propriété | 0 | 8 | 8 |

## 6. Huit objets corrigés

| Objet | Ligne | Avant | Après |
| --- | ---: | --- | --- |
| `je_sick_man_main` | 91 | ancien pinning | pinning contexte/non impliqué |
| `je_sick_man_syria` | 178 | ancien pinning | pinning contexte/non impliqué |
| `je_sick_man_egypt` | 222 | ancien pinning | pinning contexte/non impliqué |
| `je_sick_man_economy` | 258 | ancien pinning | pinning contexte/non impliqué |
| `je_sick_man_education` | 306 | ancien pinning | pinning contexte/non impliqué |
| `je_sick_man_separatism` | 388 | ancien pinning | pinning contexte/non impliqué |
| `je_sick_man_army` | 449 | ancien pinning | pinning contexte/non impliqué |
| `je_sick_man_bureaucracy` | 499 | ancien pinning | pinning contexte/non impliqué |

Substitution exacte dans chacun :

```diff
-	should_be_pinned_by_default = yes
+	should_be_pinned_by_default_uninvolved_or_context = yes
```

## 7. Diff statique

Le diff gameplay est limité à :

- un fichier : `common/journal_entries/00_sick_man.txt` ;
- huit objets ;
- huit hunks unifiés `@@` ;
- huit suppressions et huit additions ;
- aucune autre ligne.

`git diff --check` est propre. L’index staged est vide. Aucune localisation,
condition, variable, pulse, visibilité, progression, pondération, activation
ou entrée n’a été modifiée.

## 8. Baseline parser et logs antérieurs

Le `debug.log` historique de 6A.8F contient huit diagnostics ciblés :

| Ligne du log | Ligne du fichier |
| ---: | ---: |
| 1164 | 91 |
| 1165 | 178 |
| 1166 | 222 |
| 1167 | 258 |
| 1168 | 306 |
| 1171 | 388 |
| 1174 | 449 |
| 1177 | 499 |

Les trois diagnostics d’événement Tanzimat aux lignes 1170, 1173 et 1176 sont
hors périmètre et ne doivent pas être attribués au pinning.

Snapshot des logs avant smoke :

| Log | Date locale | Octets | SHA-256 |
| --- | --- | ---: | --- |
| `debug.log` | `2026-07-29 16:24:34.403 +02:00` | 365 914 | `F3564DE8347C1F810C9C391B106348EB1B283D9B0564AEB0A5D34FBA6D35D5F7` |
| `debug.1.log` | `2026-07-29 16:10:42.535 +02:00` | 279 057 | `0BE1907A17A892DAFB37AD73FD9EB91C0D38A34A0283FAF6E2725D1233AA7056` |
| `error.log` | `2026-07-29 16:24:12.157 +02:00` | 218 757 | `7C7FC62D036A05E41FB962EE1F43C50003BFB97B7740286BEF66026BBA225CF0` |
| `game.log` | `2026-07-29 16:24:12.156 +02:00` | 457 827 | `B24B53F5031CAB981C89AF8E49CBB3F8AEA735EC1B6C02CA49F5B6E4DA054F1E` |
| `system.log` | `2026-07-29 16:06:51.748 +02:00` | 1 100 | `A44FA82BF05C0121E772B29EABBE40BE1E8B9D4B47B332D453C53317E849958B` |

## 9. Fiche opérateur — smoke parser unique

État préparé par Codex :

- PASS statique acquis ;
- Victoria 3, dowser et Paradox fermés ;
- hashes et timestamps des logs enregistrés ;
- aucun commit et aucun fichier staged.

Action humaine requise :

1. monter le fork `1776_Age_of_Revolutions_fork` et `dlc014_ip3` ;
2. lancer Victoria 3 depuis le launcher ;
3. commencer une partie neuve au 1er janvier 1776, sans console ;
4. atteindre l’écran de jeu ;
5. fermer normalement le jeu puis le launcher ;
6. confirmer explicitement à Codex que les deux sont fermés et indiquer si
   l’écran de jeu 1776 a été atteint.

Codex ne lance ni jeu ni launcher et n’analyse aucun nouveau log avant cette
confirmation. Aucun PASS runtime n’est autorisé sans compte rendu humain.

## 10. Résultat runtime

L’opérateur confirme : « écran 1776 atteint, jeu et launcher fermés ». Le
contrôle de processus effectué immédiatement après ce compte rendu ne trouve
aucun processus Victoria 3, dowser ou Paradox.

Preuves de montage dans le nouveau `debug.1.log` :

```text
53  National Awakening|dlc/dlc014_ip3/dlc014_ip3.dlc
68  1776 - Age of Revolutions ...\1776_Age_of_Revolutions_fork
80  Mounted Data: .../dlc/dlc014_ip3
87  Mounted Data: .../1776_Age_of_Revolutions_fork
```

| Diagnostic | Avant | Après |
| --- | ---: | ---: |
| Ancien pinning global | 386 | 378 |
| Pinning ciblé dans `00_sick_man.txt` | 8 | 0 |
| Nouvelle propriété dans `00_sick_man.txt` | 0 | 0 |
| Nouveau diagnostic de pinning dans le fichier | 0 | 0 |

Le nouveau `debug.log` ne contient plus que trois références à
`00_sick_man.txt` : `tanzimat_events.5`, `.10` et `.9`. Ce sont exactement les
trois diagnostics d’événements connus et exclus; aucun ne concerne le pinning.

Snapshot des nouveaux logs :

| Log | Date locale | Octets | SHA-256 |
| --- | --- | ---: | --- |
| `debug.log` | `2026-07-29 18:55:35.567 +02:00` | 472 823 | `78068296741B912AFC46A4E763ED393F35F7D00967E4F17EB98075BC8EB177F5` |
| `debug.1.log` | `2026-07-29 18:50:40.867 +02:00` | 158 358 | `456557E5AAD303159180496C024286C5966BCE5C3FB46401A86BB0746CA84559` |
| `error.log` | `2026-07-29 18:55:28.629 +02:00` | 236 501 | `B94DC10E06A68649CC91F7828CD4018A53A8DF31DE3AE0D6E9C09AB853EBB5C1` |
| `game.log` | `2026-07-29 18:55:28.629 +02:00` | 144 371 | `7BF100E41F31F7391CFA3907AE7D63B3C2E79AF10EC7B3FD65D84A7FA6042AA4` |
| `system.log` | `2026-07-29 18:47:16.559 +02:00` | 1 100 | `E67BB0321A458DA5D6A4249416EEF744F148FCC6DF33945D4382181E58DFBECD` |

Le smoke parser est donc conforme. La chaîne Tanzimat inactive n’a pas été
testée fonctionnellement et n’avait pas à l’être.

## 11. Exclusions

N’ont pas été modifiés : activation Tanzimat, histoire TUR, modificateurs,
Grande Crise orientale, autres écarts Syrie, diagnostics d’événements,
Grand Collapse, localisations, DEI/VOC, Java, Balkans clos, Merchant Banking,
Navigation Acts, NAVY, formations, MARATH, Inde, BIC, ADMIN, Japon, Russie,
Autriche, Suisse, révolutions, technologies, recherche, descripteurs, launcher,
sauvegardes et `bject`.

## 12. Rollback exact

Dans le fichier unique, remplacer les huit occurrences de :

```txt
should_be_pinned_by_default_uninvolved_or_context = yes
```

par :

```txt
should_be_pinned_by_default = yes
```

Le rollback restaure le hash
`DC6AC302555035C574CFC61A91FBF667BE981FEFA2C1D8FA271A6F530B3054D8`.
Ne jamais restaurer le fichier complet.

## 13. Documents et état Git

Le périmètre final contient le fichier gameplay unique et exactement six
documents de phase :

1. `HOTFIX_6A9F_SICK_MAN_EIGHT_JE_PINNING_1_13_ALIGNMENT.md` ;
2. `docs/reports/hotfix/INDEX.md` ;
3. `HOTFIX_REPORT_INDEX.csv` ;
4. `HOTFIX_MERGE_BLOCK_STATUS.csv` ;
5. `HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
6. `HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`.

Le HEAD final reste
`deb2f1e216e26b8e9182c1ea9b0ab5fd7daca593`. Aucun commit automatique ne sera
créé; la décision de commit appartient à l’opérateur humain.

État Git final :

```text
 M common/journal_entries/00_sick_man.txt
 M docs/reports/hotfix/INDEX.md
 M docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv
 M docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md
 M docs/reports/hotfix/_index/HOTFIX_NEXT_MERGE_PHASE_PROMPT.md
 M docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv
?? bject
?? docs/reports/hotfix/_index/HOTFIX_6A9F_SICK_MAN_EIGHT_JE_PINNING_1_13_ALIGNMENT.md
?? docs/research/technology/
```

Contrôles finaux : un fichier gameplay et six documents seulement ; diff
gameplay 8/8 dans huit hunks ; hash final et structure conformes ; CSV valides ;
`git diff --check` propre ; index staged vide ; hashes protégés et stash
intacts ; aucun processus interdit.

## 14. Verdicts statiques avant smoke

`HOTFIX_6A9F_SICK_MAN_EIGHT_JE_PINNING_1_13_STATIC_PASS`

`SICK_MAN_EIGHT_JE_PINNING_EIGHT_HUNK_1_13_ALIGNMENT_COMPLETE`

`OTTOMAN_TANZIMAT_START_DISABLED_IN_1776_PRESERVED`

`NO_TANZIMAT_ACTIVATION_CHANGED`

`RUNTIME_OPERATOR_ACTION_REQUIRED`

## 15. Verdicts runtime et clôture

`HOTFIX_6A9F_SICK_MAN_EIGHT_JE_PINNING_1_13_RUNTIME_PASS`

`SICK_MAN_EIGHT_JE_PINNING_PARSER_ERRORS_8_TO_0`

`HOTFIX_6A9F_SICK_MAN_EIGHT_JE_PINNING_1_13_ALIGNMENT_COMPLETE`

`OTTOMAN_TANZIMAT_1776_DEFERRED_ACTIVATION_DESIGN_BACKLOG`

`GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`

`NEXT_EXECUTION_PHASE = HOTFIX_6A10_RESIDUAL_GLOBAL_SCRIPT_SELECTION`
