# HOTFIX-6A.6F — Alignement Victoria 3 1.13 du pinning de `je_risorgimento`

## 1. État de la phase

- Date : 29 juillet 2026.
- Phase : `HOTFIX_6A6F_ITALIAN_UNIFICATION_JE_PINNING_1_13_ALIGNMENT`.
- Branche : `hotfix-dlc-audit`.
- HEAD initial : `f121f5c37b1fe3e9d375a3bd0ff8059a83c1d770`.
- Nature du présent rapport : correction statique et validation runtime humaine.
- Runtime : terminé par l'opérateur humain.
- Victoria 3 et launcher Paradox : fermés lors de la reprise documentaire.

Verdicts courants :

`HOTFIX_6A6F_ITALIAN_UNIFICATION_JE_PINNING_1_13_STATIC_PASS`

`HOTFIX_6A6F_ITALIAN_UNIFICATION_JE_PINNING_1_13_RUNTIME_PASS`

`HOTFIX_6A6F_ITALIAN_UNIFICATION_JE_PINNING_1_13_COMPLETE`

## 2. État Git initial

Le préflight est conforme :

- racine exacte du fork ;
- branche `hotfix-dlc-audit` ;
- rapport 6A.6 présent dans le HEAD ;
- 6A.6 commitée manuellement dans `f121f5c` ;
- aucun fichier suivi modifié ;
- aucun fichier staged ;
- seuls `bject` et les sept fichiers de `docs/research/technology/` non suivis ;
- stash exact présent :
  `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` ;
- `git diff --check` propre ;
- aucun processus Victoria 3 ou launcher Paradox.

État initial :

```text
?? bject
?? docs/research/technology/
```

## 3. Sources consultées

Documents canoniques lus intégralement :

- `HOTFIX_6A6_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md` ;
- `HOTFIX_6A5F_YUGOSLAVIA_JE_PINNING_1_13_ALIGNMENT.md` ;
- `HOTFIX_6A5_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md` ;
- `HOTFIX_6A4F_BALKAN_NATIONAL_AWAKENING_1_13_ALIGNMENT.md` ;
- `HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
- `HOTFIX_MERGE_BLOCK_STATUS.csv` ;
- `HOTFIX_REPORT_INDEX.csv` ;
- `HOTFIX_GLOBAL_DIFFERENCE_INVENTORY.csv`, 534 lignes ;
- `HOTFIX_C1AI_CONCURRENT_WORK_RECONCILIATION.md` ;
- les changelogs complets du fork et de la source hotfix.

Comparaison gameplay en lecture seule :

1. fork courant ;
2. source `1776_Age_of_Revolutions_hotfix_source` ;
3. vanilla Victoria 3 1.13.

Les logs `error`, `game`, `debug`, `dedicated_server` et leurs rotations
existantes ont été consultés sans produire de nouveau runtime.

## 4. Comparaison trois voies

Objet exact : `je_risorgimento`.

Fichier exact :
`common/journal_entries/00_italian_unification.txt`.

| Arbre | État avant correction |
| --- | --- |
| Fork | `should_be_pinned_by_default = yes` exactement une fois |
| Source hotfix | `should_be_pinned_by_default_uninvolved_or_context = yes` exactement une fois |
| Vanilla 1.13 | `should_be_pinned_by_default_uninvolved_or_context = yes` exactement une fois |

La source hotfix et vanilla convergent donc exactement sur la propriété et sa
valeur. Le remplacement complet du fichier reste interdit : la source hotfix
contient deux conditions géographiques absentes de vanilla, et le fork contient
une limite de date intentionnelle absente des deux références.

## 5. Diagnostic runtime historique de référence

La session 6A.5F contient une erreur directe dans `debug.1.log` :

```text
[10:20:01][pdx_persistent_reader.cpp:268]: Error: "Unexpected token: should_be_pinned_by_default, near line: 133" in file: "common/journal_entries/00_italian_unification.txt" near line: 133
```

Comptage de référence :

- erreur ancienne ciblant le fichier italien : 1 dans `debug.1.log` ;
- référence au chemin italien : 1 ;
- erreur visant
  `should_be_pinned_by_default_uninvolved_or_context` : 0.

Une rotation plus ancienne, `debug.3.log`, contient la même erreur historique.
Elle ne devra pas être confondue avec les logs du futur lancement humain.

## 6. Hunk gameplay appliqué

Un seul hunk a été appliqué dans un seul objet :

```diff
-	should_be_pinned_by_default = yes
+	should_be_pinned_by_default_uninvolved_or_context = yes
```

Statistiques du diff gameplay :

- fichier : 1 ;
- objet : 1 ;
- hunk : 1 ;
- suppression : 1 ;
- addition : 1 ;
- autre ligne modifiée : 0.

## 7. Divergence 1776 préservée

La ligne :

```txt
		year >= 1836
```

est conservée exactement une fois dans `possible`.

Sa représentation UTF-8 hors fin de ligne reste :

```text
09-09-79-65-61-72-20-3E-3D-20-31-38-33-36
```

Le hash SHA-256 du bloc `possible` est identique avant et après :

`B1DAE6A4863B482EF218B4514386B16073250731C6A47CBC8AB2B380B3130D24`

L'entrée peut donc légitimement rester potentielle ou inactive en 1776.

## 8. Géographie et visibilité préservées

Le fork contient toujours zéro occurrence de :

```txt
is_in_geographic_region = geographic_region_italy_old
```

Les deux blocs de visibilité sont byte-for-byte inchangés :

| Bloc | SHA-256 avant et après |
| --- | --- |
| `is_shown_in_lobby` | `E44878E104025D8DD90540840FB1C880A807252EAE15135BA9C0B27332AE6C35` |
| `is_shown_when_inactive` | `FC3AE9D9D79FB2F7936DD33561232B08FABF2C02367FA275025DEA41394043DC` |

Les deux ajouts géographiques propres à la source hotfix n'ont pas été importés.

## 9. Hashes et encodage

### Avant

| Arbre | SHA-256 |
| --- | --- |
| Fork | `C7FE858F8D736EFE56B75FA146B417E017DF1999D215A453EBF1B073CF196388` |
| Source hotfix | `9515EE785F32B69DD06883136C40D4E39F17376049685D29F992ABD536238A52` |
| Vanilla 1.13 | `1C7BA000D79B68973D8A4C7AAECB49FCF6CD4685022582F7BF7B0A258FD01E8C` |

### Après

| Arbre | SHA-256 |
| --- | --- |
| Fork | `2FB4CE01C9529B89EFAB126D6912D15181720DB34322C4B7F1EC868426132D87` |
| Source hotfix | `9515EE785F32B69DD06883136C40D4E39F17376049685D29F992ABD536238A52` |
| Vanilla 1.13 | `1C7BA000D79B68973D8A4C7AAECB49FCF6CD4685022582F7BF7B0A258FD01E8C` |

Encodage et fins de ligne du fork :

| Propriété | Avant | Après |
| --- | --- | --- |
| Encodage | UTF-8 avec BOM | UTF-8 avec BOM |
| Fins de ligne | 134 LF, 0 CRLF | 134 LF, 0 CRLF |
| Saut de ligne final | présent | présent |
| Taille | 2 426 octets | 2 448 octets |

La source hotfix et vanilla sont inchangés.

## 10. Validations statiques

| Contrôle | Résultat |
| --- | --- |
| Définition active de `je_risorgimento` | 1 |
| Profondeur finale des accolades | 0 |
| Profondeur minimale | 0 |
| Ancien champ dans l'objet | 0 |
| Nouveau champ dans l'objet | 1 |
| Nouveau champ dans la source hotfix | 1 |
| Nouveau champ dans vanilla | 1 |
| `year >= 1836` | 1, inchangé |
| Géographie hotfix ajoutée au fork | 0 |
| Blocs de visibilité | inchangés |
| Diff gameplay | 1 suppression, 1 addition |
| Fichiers gameplay modifiés | 1 |
| Objets gameplay modifiés | 1 |
| Hunks gameplay | 1 |
| Localisation modifiée | 0 |
| Source hotfix/vanilla modifiés | 0 |
| `git diff --check` | PASS |
| Index Git | vide |
| Stash NAVY-3C-3 | intact |
| Victoria 3 / launcher | fermés |

## 11. Fichiers autorisés de la phase

Gameplay :

- `common/journal_entries/00_italian_unification.txt`.

Documentation :

- `HOTFIX_6A6F_ITALIAN_UNIFICATION_JE_PINNING_1_13_ALIGNMENT.md` ;
- `docs/reports/hotfix/INDEX.md` ;
- `HOTFIX_REPORT_INDEX.csv` ;
- `HOTFIX_MERGE_BLOCK_STATUS.csv` ;
- `HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
- `HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`.

Aucun autre fichier n'est modifié.

## 12. Protections confirmées

Les huit hashes protégés ont été enregistrés avant modification :

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

DEI/VOC, Balkan National Awakening, Yugoslavia 6A.5F, formations militaires,
NAVY, MARATH, BIC, Merchant Banking, Navigation Acts, Russie, Japon, Inde,
technologies, localisations et tous les autres blocs protégés sont intacts.

## 13. Fiche remise à l'opérateur humain

Un seul lancement doit couvrir le test.

### Avant le lancement

- Vérifier la présence des verdicts statiques ci-dessous.
- Monter le fork et ses dépendances habituelles.
- Démarrer une partie neuve au 1er janvier 1776.

### Dans le jeu

1. Choisir un pays de culture principale nord-italienne ou sud-italienne ;
   utiliser Naples si disponible et pertinent.
2. Ouvrir `Journal > Potentiel`.
3. Rechercher `Risorgimento` ou l'entrée d'unification italienne.
4. Vérifier :
   - titre, description et conditions lisibles ;
   - aucune clé de localisation brute ;
   - aucune anomalie visible de pinning ;
   - aucun effet visible inattendu ;
   - `year >= 1836` peut rester non remplie en 1776.
5. Avancer d'au moins un jour.
6. Noter les dates initiale et finale.
7. Prendre une capture si possible.
8. Fermer Victoria 3 puis le launcher Paradox.

### Compte rendu demandé

- pays et cultures principales pertinentes ;
- dates initiale et finale ;
- entrée visible ou non dans `Potentiel` ;
- titre et conditions lisibles ou non ;
- éventuelle clé brute ;
- éventuelle anomalie de pinning ;
- éventuel effet inattendu ;
- état de la condition `year >= 1836` ;
- capture éventuelle ;
- confirmation explicite que le jeu et le launcher sont fermés.

Une absence cohérente avec les cultures ou conditions d'affichage est un
contrôle négatif, pas un échec de parsing. Ne pas effectuer automatiquement un
second lancement.

## 14. État Git au handoff statique

Le HEAD reste `f121f5c37b1fe3e9d375a3bd0ff8059a83c1d770`. Aucun commit automatique
n'est créé et aucun fichier n'est staged.

```text
 M common/journal_entries/00_italian_unification.txt
 M docs/reports/hotfix/INDEX.md
 M docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv
 M docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md
 M docs/reports/hotfix/_index/HOTFIX_NEXT_MERGE_PHASE_PROMPT.md
 M docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv
?? bject
?? docs/reports/hotfix/global_script/6A01_6A09/HOTFIX_6A6F_ITALIAN_UNIFICATION_JE_PINNING_1_13_ALIGNMENT.md
?? docs/research/technology/
```

Contrôles de portée :

- fichiers de phase : 7, soit 1 gameplay et 6 documents ;
- entrée inattendue : 0 ;
- index Git : vide ;
- `git diff --check` : propre ;
- hashes protégés contrôlés après modification : 8, divergence : 0 ;
- source hotfix et vanilla : hashes inchangés ;
- stash NAVY-3C-3 : intact ;
- processus Victoria 3/launcher Paradox : 0.

## 15. Verdict statique

`HOTFIX_6A6F_ITALIAN_UNIFICATION_JE_PINNING_1_13_STATIC_PASS`

`RUNTIME_OPERATOR_ACTION_REQUIRED`

Attendre le compte rendu humain. Ne pas commencer une autre phase et ne pas
publier de PASS runtime.

## 16. Compte rendu de l'opérateur humain

L'opérateur a communiqué :

- pays joué : Naples ;
- partie neuve : 1er janvier 1776 ;
- date finale : 2 janvier 1776 ;
- entrée `Risorgimento` visible dans `Journal > Potentiel` ;
- possibilité de formation de l'Italie visible ;
- condition `year >= 1836` non remplie, conformément au scénario 1776 ;
- aucune anomalie visible de pinning signalée ;
- une ligne magenta
  `BUG_year_greater_or_equal missing perspective...` visible dans le tooltip ;
- fermeture normale du jeu.

La capture fournie montre également :

- le titre `Risorgimento` correctement localisé ;
- les conditions de technologie, rang et date ;
- les informations debug `OnPulse` et identifiant `je_risorgimento` ;
- le panneau de formation de l'Italie et ses régions requises.

Lors de la reprise, le contrôle des processus confirme zéro processus Victoria 3
ou launcher Paradox.

## 17. Preuve du montage et de la progression

`debug.1.log` de la session humaine prouve :

- ligne 68 : mod
  `1776 - Age of Revolutions, Total Conversion Mod` associé au chemin exact du
  fork ;
- ligne 80 : montage de
  `C:/Games/Victoria 3 The Great Wave/game/dlc/dlc014_ip3` ;
- ligne 87 : `Mounted Data` sur
  `C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork`.

`dedicated_server.log` enregistre :

- `1776.1.1.6` ;
- `1776.1.1.12` ;
- `1776.1.1.18` ;
- `1776.1.2`.

La progression minimale d'au moins un jour est donc prouvée.

Le descripteur du mod reste déclaré `1.12.5` face au jeu `1.13.0`. Ce diagnostic
préexistant est hors périmètre et n'empêche pas le montage positif.

## 18. Analyse des logs après correction

Les nouveaux journaux sont identifiés par leurs heures de modification entre
11:44 et 11:51 le 29 juillet 2026. Les rotations antérieures à 10:27 sont
conservées comme référence et ne sont pas comptées comme nouvelles erreurs.

| Diagnostic | Avant | Après |
| --- | ---: | ---: |
| Anciennes erreurs globales `should_be_pinned_by_default` | 389 | 388 |
| Erreurs visant `00_italian_unification.txt` | 1 | 0 |
| Références au chemin italien dans les nouveaux debug logs | 1 | 0 |
| Erreurs visant le nouveau champ 1.13 | 0 | 0 |
| Références à `je_risorgimento` dans les logs | 0 | 0 |

La baisse de 389 à 388 correspond exactement à la disparition de l'unique
erreur du fichier italien. Les 388 diagnostics restants appartiennent à d'autres
fichiers et restent hors périmètre.

## 19. Diagnostic du tooltip de date en mode debug

La ligne visible :

```text
En ou après 1836 (BUG_year_greater_or_equal missing perspective...)
```

n'est pas une clé de localisation française absente :

- vanilla déclare `year_greater_or_equal` dans
  `common/trigger_localization/00_trigger_localization.txt` ;
- vanilla français fournit
  `TRIGGER_YEAR_GREATER_THAN_OR_EQUAL: "En ou après $NUM$"` ;
- le préfixe affiché `En ou après 1836` est correctement localisé ;
- la même capture montre deux lignes supplémentaires explicitement préfixées
  `Debug`, confirmant l'affichage des diagnostics développeur ;
- aucun nouveau log ne contient `BUG_year_greater_or_equal`,
  `missing perspective` ou une erreur de la nouvelle propriété.

Conclusion prudente : le suffixe magenta est un diagnostic de tooltip exposé
par le mode debug, pas une régression de localisation ni de pinning. Sans mode
debug, le texte normalement attendu est la partie localisée
`En ou après 1836`. Aucun changement de `year >= 1836` n'est autorisé ou
nécessaire dans 6A.6F.

## 20. Décision runtime

Les preuves minimales sont réunies :

- observations humaines reçues ;
- fork exact et `dlc014_ip3` positivement montés ;
- progression du 1er au 2 janvier 1776 ;
- entrée Risorgimento visible ;
- formation de l'Italie visible ;
- aucune anomalie de pinning signalée ;
- erreur ciblée passée de 1 à 0 ;
- aucune erreur sur la propriété Victoria 3 1.13.

La phase est close. La prochaine phase doit être une nouvelle sélection
documentaire résiduelle, sans commencer directement Merchant Banking,
Navigation Acts ou une autre migration.

Après déplacement du fichier italien de
`VANILLA_1_13_ALIGNMENT_REQUIRED` vers `ALREADY_MERGED`, la classification des
161 anciennes lignes devient : 7 deltas hotfix requis, 19 alignements vanilla
1.13, 15 déjà fusionnés, 3 divergences intentionnelles, 1 contenu obsolète,
10 backlogs, 19 travaux protégés et 87 inconnus. Il reste 113 lignes directement
exploitables par une revue, sans que ce nombre représente 113 correctifs.

`HOTFIX_6A6F_ITALIAN_UNIFICATION_JE_PINNING_1_13_RUNTIME_PASS`

`ITALIAN_UNIFICATION_JE_PINNING_1_13_ALIGNED`

`ITALIAN_1776_YEAR_GATE_PRESERVED`

`GEOGRAPHY_UNCHANGED`

`HOTFIX_6A6F_ITALIAN_UNIFICATION_JE_PINNING_1_13_COMPLETE`

`GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`

`NEXT_EXECUTION_PHASE = HOTFIX_6A7_RESIDUAL_GLOBAL_SCRIPT_SELECTION`

## 21. État Git final et commit

Le HEAD reste `f121f5c37b1fe3e9d375a3bd0ff8059a83c1d770`. Le diff gameplay reste
limité au remplacement d'une propriété dans `je_risorgimento`. Aucun commit
automatique n'est créé ; la décision de commit appartient à l'opérateur humain.

```text
 M common/journal_entries/00_italian_unification.txt
 M docs/reports/hotfix/INDEX.md
 M docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv
 M docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md
 M docs/reports/hotfix/_index/HOTFIX_NEXT_MERGE_PHASE_PROMPT.md
 M docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv
?? bject
?? docs/reports/hotfix/global_script/6A01_6A09/HOTFIX_6A6F_ITALIAN_UNIFICATION_JE_PINNING_1_13_ALIGNMENT.md
?? docs/research/technology/
```

- `git diff --check` : propre ;
- index Git : vide ;
- commit automatique : aucun ;
- fichiers de phase : exactement 1 gameplay et 6 documents ;
- entrée inattendue : 0 ;
- hashes protégés : 8 contrôlés, 0 divergence ;
- source hotfix et vanilla : inchangés ;
- stash NAVY-3C-3 : intact ;
- Victoria 3 et launcher Paradox : fermés.
