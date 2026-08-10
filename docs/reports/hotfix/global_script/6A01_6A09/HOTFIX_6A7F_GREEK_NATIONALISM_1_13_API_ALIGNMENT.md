# HOTFIX-6A.7F — Alignement des API Victoria 3 1.13 du nationalisme grec

## 1. État de la phase

- Date : 29 juillet 2026.
- Phase : `HOTFIX_6A7F_GREEK_NATIONALISM_1_13_API_ALIGNMENT`.
- Branche : `hotfix-dlc-audit`.
- HEAD initial :
  `07de008c16bd30d672a4fab063e85a3e265b2dcc`.
- Nature du présent rapport : correction statique et validation runtime
  humaine.
- Runtime : terminé par l’opérateur humain.
- Victoria 3 et launcher Paradox : fermés lors de la reprise documentaire.

Verdicts courants :

`HOTFIX_6A7F_GREEK_NATIONALISM_1_13_STATIC_PASS`

`HOTFIX_6A7F_GREEK_NATIONALISM_1_13_RUNTIME_PASS`

`GREEK_NATIONALISM_MONARCHY_TRIGGER_1_13_ALIGNED`

`GREEK_NATIONALISM_JE_PINNING_1_13_ALIGNED`

`GREEK_VISIBILITY_AND_GEOGRAPHY_UNCHANGED`

`HOTFIX_6A7F_GREEK_NATIONALISM_1_13_API_ALIGNMENT_COMPLETE`

## 2. État Git initial

Le préflight est conforme :

- racine exacte du fork ;
- branche `hotfix-dlc-audit` ;
- rapport 6A.7 présent dans le HEAD ;
- verdicts d’entrée présents dans le HEAD ;
- 6A.7 commitée manuellement dans `07de008` ;
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

- `HOTFIX_6A7_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md` ;
- `HOTFIX_6A6F_ITALIAN_UNIFICATION_JE_PINNING_1_13_ALIGNMENT.md` ;
- `HOTFIX_6A6_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md` ;
- `HOTFIX_6A5F_YUGOSLAVIA_JE_PINNING_1_13_ALIGNMENT.md` ;
- `HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
- `HOTFIX_MERGE_BLOCK_STATUS.csv` ;
- `HOTFIX_REPORT_INDEX.csv` ;
- `HOTFIX_GLOBAL_DIFFERENCE_INVENTORY.csv`, 534 lignes de données ;
- `HOTFIX_C1AI_CONCURRENT_WORK_RECONCILIATION.md` ;
- les changelogs du fork et de la source hotfix.

Comparaison gameplay intégrale :

1. fork courant ;
2. source `1776_Age_of_Revolutions_hotfix_source`, lecture seule ;
3. vanilla Victoria 3 1.13, lecture seule.

Les logs `error`, `game`, `debug`, `dedicated_server` et leurs rotations
existantes ont été consultés sans lancer le jeu et sans produire de nouveaux
logs.

## 4. Comparaison trois voies

Objet exact : `je_greek_nationalism`.

Fichier exact :
`common/journal_entries/00_greek_nationalism.txt`.

| API | Fork avant correction | Source hotfix | Vanilla 1.13 |
| --- | --- | --- | --- |
| Loi monarchique | `has_law = law_type:law_monarchy` | `country_has_monarchy_law = yes` | `country_has_monarchy_law = yes` |
| Pinning | `should_be_pinned_by_default = yes` | `should_be_pinned_by_default_uninvolved_or_context = yes` | `should_be_pinned_by_default_uninvolved_or_context = yes` |

La source hotfix et vanilla convergent exactement sur les deux substitutions.
Le remplacement complet du fichier reste interdit : la source hotfix contient
deux conditions `geographic_region_megali_greece` absentes de vanilla et du
fork.

## 5. Hashes des trois versions

### Avant correction

| Arbre | SHA-256 |
| --- | --- |
| Fork | `41E56B210D8D990B3F848AA02010E6CE11E0B93A32532FC74A2E225E9A8AFF58` |
| Source hotfix | `76925B166C659F1DA986A445FE8343638465860628DFC5881DB4427CE1877517` |
| Vanilla 1.13 | `E8ACC0F043E30C2578BD9A49375360534073D4562BBC31C6699FF6789BB0E7B9` |

### Après correction

| Arbre | SHA-256 |
| --- | --- |
| Fork | `1938E6AB97C9F85424961BD35675D474CB7F65F0CFD74EB9879ADF66DCE80B50` |
| Source hotfix | `76925B166C659F1DA986A445FE8343638465860628DFC5881DB4427CE1877517` |
| Vanilla 1.13 | `E8ACC0F043E30C2578BD9A49375360534073D4562BBC31C6699FF6789BB0E7B9` |

La source hotfix et vanilla sont inchangées.

## 6. Erreur runtime historique

`debug.1.log` de la session 6A.6F contient exactement une erreur ciblée :

```text
[11:44:36][pdx_persistent_reader.cpp:268]: Error: "Unexpected token: should_be_pinned_by_default, near line: 250" in file: "common/journal_entries/00_greek_nationalism.txt" near line: 250
```

Cette occurrence constitue la référence avant correction. Les rotations
historiques ne devront pas être confondues avec les futurs logs produits par
l’opérateur.

## 7. Snapshot de visibilité

Les deux blocs ont été enregistrés avant édition.

### `is_shown_in_lobby`

```txt
	is_shown_in_lobby = {
		country_has_primary_culture = cu:greek
	}
```

SHA-256 avant et après :

`A33ADDFB4103B02E5F59C17A5A51037E7B105E6E1F3E1F3C597F021C83B382C0`

### `is_shown_when_inactive`

```txt
	is_shown_when_inactive = {
		AND = {
			country_has_primary_culture = cu:greek
			any_scope_state = {
				is_greek_homeland = yes
			}
		}
	}
```

SHA-256 avant et après :

`9AC6692B5A1D76573FB2DD44D1B7B9D310DFE02688E01E36AF9093E3D773C240`

Les deux blocs sont byte-for-byte inchangés.

## 8. Comptes avant correction

Dans l’objet unique :

| Propriété | Occurrences |
| --- | ---: |
| `has_law = law_type:law_monarchy` | 1 |
| `should_be_pinned_by_default = yes` | 1 |
| `country_has_monarchy_law = yes` | 0 |
| `should_be_pinned_by_default_uninvolved_or_context = yes` | 0 |

Autres invariants :

- définition active de `je_greek_nationalism` : 1 ;
- `geographic_region_megali_greece` : 0 ;
- `is_greek_homeland = yes` : 5 ;
- profondeur finale des accolades : 0 ;
- profondeur minimale : 0.

## 9. Hunks gameplay appliqués

Hunk 1 :

```diff
-			has_law = law_type:law_monarchy
+			country_has_monarchy_law = yes
```

Hunk 2 :

```diff
-	should_be_pinned_by_default = yes
+	should_be_pinned_by_default_uninvolved_or_context = yes
```

Statistiques exactes :

- fichier gameplay : 1 ;
- objet : 1 ;
- hunks : 2 ;
- suppressions : 2 ;
- additions : 2 ;
- autre ligne modifiée : 0.

## 10. Comptes après correction

| Propriété | Occurrences |
| --- | ---: |
| `has_law = law_type:law_monarchy` | 0 |
| `should_be_pinned_by_default = yes` | 0 |
| `country_has_monarchy_law = yes` | 1 |
| `should_be_pinned_by_default_uninvolved_or_context = yes` | 1 |

La définition de l’objet reste unique. La profondeur finale et la profondeur
minimale des accolades restent à 0.

## 11. Encodage et fins de ligne

| Propriété | Avant | Après |
| --- | --- | --- |
| Encodage | UTF-8 avec BOM | UTF-8 avec BOM |
| Fins de ligne | 251 LF, 0 CRLF | 251 LF, 0 CRLF |
| Saut de ligne final | présent | présent |
| Taille | 5 935 octets | 5 956 octets |

Aucun reformatage ou changement de ligne blanche n’a été effectué.

## 12. Géographie préservée

- `geographic_region_megali_greece` : 0 avant, 0 après ;
- `is_greek_homeland = yes` : 5 avant, 5 après ;
- bloc `any_scope_state` de visibilité : inchangé ;
- autre condition, effet, durée ou technologie modifié : 0.

Les deux ajouts géographiques propres à la source hotfix n’ont pas été
importés.

## 13. Validations statiques

| Contrôle | Résultat |
| --- | --- |
| Définition active de `je_greek_nationalism` | 1 |
| Profondeur finale des accolades | 0 |
| Profondeur minimale | 0 |
| Ancienne loi | 0 |
| Ancien pinning | 0 |
| Nouvelle loi | 1 |
| Nouveau pinning | 1 |
| Hunks gameplay | 2 |
| Suppressions/additions | 2 / 2 |
| Fichiers gameplay modifiés | 1 |
| Objets gameplay modifiés | 1 |
| Autres lignes gameplay modifiées | 0 |
| Blocs de visibilité | hashes inchangés |
| Géographie Megali importée | 0 |
| `is_greek_homeland = yes` | 5, inchangé |
| Localisation modifiée ou requise | 0 |
| Encodage et fins de ligne | inchangés |
| Source hotfix/vanilla modifiées | 0 |
| `git diff --check` | PASS |
| Index Git | vide |
| Stash NAVY-3C-3 | intact |
| Victoria 3 / launcher | fermés |

## 14. Protections générales

Les huit hashes protégés restent :

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

DEI/VOC, Java, Balkan National Awakening, Yugoslavia, Risorgimento, Grande
Crise orientale, Coup, Imperialism of Promise, Merchant Banking, Navigation
Acts, formations militaires, NAVY, MARATH, BIC, technologies et tous les
autres blocs exclus sont intacts.

BIC conserve `law_frontier_colonization`. `law_colonial_exploitation` n’a pas
été restaurée.

## 15. Rollback exact

En cas de régression imputable aux hunks, inverser uniquement :

```diff
-			country_has_monarchy_law = yes
+			has_law = law_type:law_monarchy
```

```diff
-	should_be_pinned_by_default_uninvolved_or_context = yes
+	should_be_pinned_by_default = yes
```

Ne jamais restaurer le fichier complet et ne pas utiliser `reset`, `restore` ou
`checkout`.

## 16. Fichiers autorisés de la phase

Gameplay :

- `common/journal_entries/00_greek_nationalism.txt`.

Documentation :

- `HOTFIX_6A7F_GREEK_NATIONALISM_1_13_API_ALIGNMENT.md` ;
- `docs/reports/hotfix/INDEX.md` ;
- `HOTFIX_REPORT_INDEX.csv` ;
- `HOTFIX_MERGE_BLOCK_STATUS.csv` ;
- `HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
- `HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`.

Aucun autre fichier n’est modifié.

## 17. Fiche remise à l’opérateur humain

Un seul lancement doit couvrir le test.

### Avant le lancement

- Vérifier les deux verdicts statiques de la section 19.
- Monter le fork et `dlc014_ip3`.
- Préparer une partie neuve au 1er janvier 1776.

### Dans le jeu

1. Lancer Victoria 3 depuis le launcher habituel.
2. Démarrer une partie neuve en 1776.
3. Choisir un pays de culture principale grecque.
4. Si aucun n’est directement jouable, libérer la Grèce depuis l’Empire
   ottoman et la jouer, sans console.
5. Noter le pays, ses cultures principales, son statut monarchique éventuel et
   la date initiale.
6. Ouvrir `Journal > Potentiel`.
7. Rechercher l’entrée de nationalisme grec.
8. Vérifier :
   - titre, description et conditions lisibles ;
   - aucune clé brute ;
   - aucune anomalie visible de pinning ;
   - aucun effet inattendu ;
   - condition monarchique correctement interprétée si elle est visible.
9. Avancer d’au moins un jour.
10. Noter la date finale et prendre une capture si possible.
11. Fermer normalement Victoria 3 puis le launcher Paradox.

### Compte rendu demandé

- pays joué ;
- cultures principales ;
- statut monarchique éventuel ;
- dates initiale et finale ;
- entrée visible ou `RUNTIME_ENTRY_INACCESSIBLE` ;
- titre, description et conditions lisibles ou non ;
- éventuelle clé brute ;
- éventuelle anomalie de pinning ;
- comportement visible de la condition monarchique ;
- éventuel effet inattendu ;
- capture éventuelle ;
- confirmation explicite que le jeu et le launcher sont fermés.

Ne pas effectuer automatiquement un second lancement.

## 18. État Git au handoff statique

Le HEAD reste `07de008c16bd30d672a4fab063e85a3e265b2dcc`. Aucun commit
automatique n’est créé et aucun fichier n’est staged.

```text
 M common/journal_entries/00_greek_nationalism.txt
 M docs/reports/hotfix/INDEX.md
 M docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv
 M docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md
 M docs/reports/hotfix/_index/HOTFIX_NEXT_MERGE_PHASE_PROMPT.md
 M docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv
?? bject
?? docs/reports/hotfix/global_script/6A01_6A09/HOTFIX_6A7F_GREEK_NATIONALISM_1_13_API_ALIGNMENT.md
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

## 19. Verdict statique au handoff

`HOTFIX_6A7F_GREEK_NATIONALISM_1_13_STATIC_PASS`

`RUNTIME_OPERATOR_ACTION_REQUIRED`

Attendre le compte rendu humain. Ne pas commencer une autre phase et ne pas
publier de PASS runtime ou de verdict `COMPLETE`.

## 20. Compte rendu de l’opérateur humain

L’opérateur a :

1. commencé avec l’Empire ottoman ;
2. fait progresser la partie du 1er au 30 janvier 1776 ;
3. libéré la Grèce comme pays indépendant le 30 janvier ;
4. sélectionné et joué la Grèce ;
5. ouvert `Journal > Potentiel` ;
6. fourni une capture de l’entrée `Éveil national` ;
7. fermé proprement Victoria 3 puis confirmé la fermeture du launcher.

Observations humaines issues du compte rendu et de la capture :

| Contrôle | Observation |
| --- | --- |
| Pays joué | Grèce indépendante |
| Culture pertinente | grecque |
| Date initiale de session | 1er janvier 1776 |
| Libération et prise de contrôle de la Grèce | 30 janvier 1776 |
| Date finale prouvée par les logs | 30 janvier 1776, tick 18 |
| Entrée potentielle | visible |
| Titre | `Éveil national`, lisible |
| Description et effets | lisibles |
| Conditions | lisibles |
| Clé brute | aucune |
| Anomalie visible de pinning | aucune |
| Effet inattendu | aucun signalé |
| Condition monarchique | non observable dans cette fiche potentielle |

La fiche montre notamment :

- technologie `nationalisme` non encore recherchée ;
- condition de loi de sujétion non encore remplie ;
- branche alternative satisfaite parce que la Grèce n’est le sujet d’aucune
  autre nation ;
- durée affichée de 120 mois ;
- bonus de propagande nationaliste transfrontalière lisible.

L’absence d’affichage de la condition monarchique dans cette fiche n’est pas un
échec : cette condition appartient à la branche d’achèvement ambitieuse et non
au résumé potentiel visible au moment de la capture.

## 21. Montage, progression et fermeture

La session runtime nouvelle est séparée des rotations historiques :

- baseline 6A.6F : `debug.3.log`, dernière écriture à 11:44 ;
- nouvelle session grecque : `debug.1.log` puis `debug.log`, de 13:21 à
  13:36 ;
- progression : `dedicated_server.log`.

Preuves de montage dans `debug.1.log` :

```text
[13:21:48][virtualfilesystem_physfs.cpp:460]: Mounted Data: C:/Games/Victoria 3 The Great Wave/game/dlc/dlc014_ip3
[13:21:48][virtualfilesystem_physfs.cpp:460]: Mounted Data: C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork
```

Preuves temporelles :

```text
[13:28:29][jominiapplication.cpp:539]: Processing Tick: 1776.1.1.6
[13:31:43][jominiapplication.cpp:539]: Processing Tick: 1776.1.30.18
```

`dedicated_server.log` contient 119 ticks de la session. La progression dépasse
largement le minimum d’un jour.

Preuve de fermeture propre :

```text
[13:35:57][application.cpp:1861]: Quit: Quit from inside game
```

Lors de l’analyse, le nombre de processus Victoria 3 et Paradox est 0.

## 22. Analyse des logs après correction

| Diagnostic | Baseline 6A.6F | Session 6A.7F |
| --- | ---: | ---: |
| Anciennes erreurs globales `should_be_pinned_by_default` | 388 | 387 |
| Erreur visant `00_greek_nationalism.txt` | 1 | 0 |
| Erreur visant `should_be_pinned_by_default_uninvolved_or_context` | 0 | 0 |
| Erreur visant `country_has_monarchy_law` | 0 | 0 |
| Nouvelle erreur propre au fichier grec | 0 | 0 |

La diminution globale de 388 à 387 correspond exactement à la disparition de
l’unique erreur grecque. Les autres 387 diagnostics globaux sont hors
périmètre et ne rouvrent pas 6A.7F.

## 23. Décision runtime

Les preuves minimales sont toutes réunies :

- fork exact monté ;
- `dlc014_ip3` monté ;
- progression du 1er au 30 janvier 1776 ;
- Grèce indépendante effectivement jouée ;
- entrée potentielle visible et lisible ;
- aucune clé brute ;
- aucune anomalie visible de pinning ;
- erreur ciblée passée de 1 à 0 ;
- aucune erreur sur les deux nouvelles API ;
- fermeture propre du jeu et du launcher.

Verdicts :

`HOTFIX_6A7F_GREEK_NATIONALISM_1_13_RUNTIME_PASS`

`GREEK_NATIONALISM_MONARCHY_TRIGGER_1_13_ALIGNED`

`GREEK_NATIONALISM_JE_PINNING_1_13_ALIGNED`

`GREEK_VISIBILITY_AND_GEOGRAPHY_UNCHANGED`

`HOTFIX_6A7F_GREEK_NATIONALISM_1_13_API_ALIGNMENT_COMPLETE`

`GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`

## 24. État Git final et commit

Le HEAD reste `07de008c16bd30d672a4fab063e85a3e265b2dcc`. Aucun commit
automatique n’est créé et aucun fichier n’est staged.

```text
 M common/journal_entries/00_greek_nationalism.txt
 M docs/reports/hotfix/INDEX.md
 M docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv
 M docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md
 M docs/reports/hotfix/_index/HOTFIX_NEXT_MERGE_PHASE_PROMPT.md
 M docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv
?? bject
?? docs/reports/hotfix/global_script/6A01_6A09/HOTFIX_6A7F_GREEK_NATIONALISM_1_13_API_ALIGNMENT.md
?? docs/research/technology/
```

Le prochain sous-bloc préparé est strictement documentaire :

`NEXT_EXECUTION_PHASE = HOTFIX_6A8R_GREAT_EASTERN_CRISIS_1_13_AUDIT`

La décision de commit de 6A.7F appartient à l’opérateur humain. Ne pas commencer
6A.8R avant ce commit manuel.
