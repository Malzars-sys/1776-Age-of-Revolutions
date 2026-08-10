# HOTFIX-6A.7 — Sélection du prochain résidu global

## 1. Identification

- Date : 29 juillet 2026.
- Phase : `HOTFIX_6A7_RESIDUAL_GLOBAL_SCRIPT_SELECTION`.
- Nature : sélection strictement documentaire.
- Branche : `hotfix-dlc-audit`.
- HEAD initial :
  `b80116cc226dbaacc51adb257448162969024272`.
- Commit initial :
  `b80116c Align Italian unification journal entry pinning with Victoria 3 1.13`.
- HEAD final attendu : identique, aucun commit automatique.

## 2. État Git initial

Le préflight est conforme :

- racine exacte du fork ;
- branche `hotfix-dlc-audit` ;
- rapport 6A.6F présent dans le HEAD ;
- 6A.6F commitée manuellement ;
- aucun fichier suivi modifié ;
- aucun fichier staged ;
- seuls `bject` et les sept fichiers de
  `docs/research/technology/` non suivis ;
- stash exact présent :
  `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` ;
- Victoria 3 et launcher Paradox fermés ;
- `git diff --check` propre.

État initial :

```text
?? bject
?? docs/research/technology/
```

Les huit hashes protégés sont enregistrés dans la section 14.

## 3. Sources consultées

Documents lus intégralement :

- `HOTFIX_6A6F_ITALIAN_UNIFICATION_JE_PINNING_1_13_ALIGNMENT.md` ;
- `HOTFIX_6A6_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md` ;
- `HOTFIX_6A5F_YUGOSLAVIA_JE_PINNING_1_13_ALIGNMENT.md` ;
- `HOTFIX_6A5_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md` ;
- `HOTFIX_6A4F_BALKAN_NATIONAL_AWAKENING_1_13_ALIGNMENT.md` ;
- `HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
- `HOTFIX_MERGE_BLOCK_STATUS.csv` ;
- `HOTFIX_REPORT_INDEX.csv` ;
- `HOTFIX_GLOBAL_DIFFERENCE_INVENTORY.csv`, 534 lignes ;
- `HOTFIX_C1AI_CONCURRENT_WORK_RECONCILIATION.md` ;
- changelogs complets du fork et de la source hotfix.

Les logs et rotations existants de la session 6A.6F ont été consultés en
lecture seule. Aucun lancement ni contrôle de Victoria 3 ou du launcher n'a été
effectué.

## 4. Inventaire actualisé

Après clôture de 6A.6F, les 161 anciennes lignes `PENDING_REVIEW` sont
reclassées exclusivement :

| Catégorie | Lignes |
| --- | ---: |
| `REQUIRED_HOTFIX_DELTA` | 7 |
| `VANILLA_1_13_ALIGNMENT_REQUIRED` | 19 |
| `ALREADY_MERGED` | 15 |
| `INTENTIONAL_FORK_DIVERGENCE` | 3 |
| `OBSOLETE_HOTFIX_CONTENT` | 1 |
| `POST_MERGE_DESIGN_BACKLOG` | 10 |
| `PROTECTED_CONCURRENT_WORK` | 19 |
| `UNKNOWN_REQUIRES_REVIEW` | 87 |
| **Total** | **161** |

Il reste **113 lignes directement exploitables par une revue** :

- 7 deltas hotfix requis ;
- 19 alignements vanilla 1.13 ;
- 87 inconnus.

Ce nombre ne représente pas 113 correctifs. Le total historique de 26 deltas à
haute confiance reste `UNVERIFIED`.

Sont clos et interdits comme candidats :

- `common/journal_entries/05_balkan_national_awakening.txt` ;
- `common/journal_entries/05_creation_of_yugoslavia.txt` ;
- `common/journal_entries/00_italian_unification.txt`.

## 5. Analyse des 388 erreurs de pinning

`debug.1.log` de 6A.6F contient exactement 388 erreurs :

```text
Unexpected token: should_be_pinned_by_default,
```

Elles concernent 145 fichiers uniques. La nouvelle propriété Victoria 3 1.13
ne génère aucune erreur.

### 5.1 Répartition recalculée

| Statut rapproché | Fichiers | Occurrences |
| --- | ---: | ---: |
| `INTENTIONAL_FORK_DIVERGENCE` | 104 | 242 |
| `VANILLA_1_13_ALIGNMENT_REQUIRED` | 19 | 104 |
| `PENDING_REVIEW` brut | 8 | 19 |
| `MERGED_STATIC_ONLY` brut | 10 | 19 |
| Hors inventaire | 4 | 4 |
| **Total** | **145** | **388** |

Les valeurs sont obtenues en rapprochant chaque chemin exact de `debug.1.log`
avec l'inventaire, puis en appliquant la liste canonique des 19 alignements
1.13.

### 5.2 Familles principales

| Famille | Occurrences | Décision |
| --- | ---: | --- |
| Tutoriel | 52 | Trop large, 40 objets distincts |
| Objectif `great_game` | 17 | Divergence intentionnelle |
| Prestige goods | 16 | Divergence intentionnelle |
| Russie | 12 | Travail protégé |
| Objectif `hegemon` | 11 | Divergence intentionnelle |
| Objectif `economic_dominance` | 10 | Divergence intentionnelle |
| `sick_man` | 8 | Huit objets, lot trop large |
| Negotiation quests | 7 | Divergence intentionnelle |
| Economic regeneration | 7 | Divergence intentionnelle |
| Poland-Lithuania mod | 7 | Bloc mixte/déjà fusionné |
| ACW | 6 | Révolution américaine protégée |
| Meiji | 6 | Japon protégé |
| Portugal politics | 6 | Six objets, reporté |

Une occurrence unique ne suffit pas non plus : Coup, Imperialism of Promise et
Great Eastern Crisis contiennent des écarts adjacents qui doivent être
considérés avant toute exécution.

## 6. Observation debug italienne close

Le suffixe `BUG_year_greater_or_equal missing perspective` reste classé comme
diagnostic de tooltip debug :

- localisation française normale présente ;
- préfixe `En ou après 1836` correctement rendu ;
- informations `Debug` visibles dans la même capture ;
- aucune erreur correspondante dans les logs ;
- `year >= 1836` protégé.

`00_italian_unification.txt` n'est pas rouvert.

## 7. Comparaisons trois voies

### 7.1 Alignement API de `je_greek_nationalism`

Chemin :

`common/journal_entries/00_greek_nationalism.txt`

Objet :

`je_greek_nationalism`

Deux divergences API exactes subsistent entre le fork et vanilla :

| API | Fork | Source hotfix | Vanilla 1.13 |
| --- | --- | --- | --- |
| Loi monarchique | `has_law = law_type:law_monarchy` | `country_has_monarchy_law = yes` | `country_has_monarchy_law = yes` |
| Pinning | `should_be_pinned_by_default = yes` | `should_be_pinned_by_default_uninvolved_or_context = yes` | `should_be_pinned_by_default_uninvolved_or_context = yes` |

Preuves :

- une erreur parser directe dans `debug.1.log`, près de la ligne 250 ;
- source hotfix et vanilla convergent sur les deux remplacements ;
- le diff fork/vanilla ne contient que ces deux corrections fonctionnelles,
  plus une ligne blanche de formatage à ne pas importer ;
- aucune localisation nouvelle ;
- aucun fichier protégé ;
- rollback de deux lignes.

La source hotfix ajoute en plus deux références à
`geographic_region_megali_greece` dans les blocs de visibilité. Vanilla ne les
contient pas. Ces changements source-only sont explicitement exclus :

- `is_shown_in_lobby` doit rester inchangé ;
- `is_shown_when_inactive` doit conserver le contrôle
  `any_scope_state = { is_greek_homeland = yes }`.

Taille future : 1 fichier, 1 objet, 2 hunks, 2 suppressions et 2 additions.

Hashes de référence :

| Arbre | SHA-256 |
| --- | --- |
| Fork | `41E56B210D8D990B3F848AA02010E6CE11E0B93A32532FC74A2E225E9A8AFF58` |
| Source hotfix | `76925B166C659F1DA986A445FE8343638465860628DFC5881DB4427CE1877517` |
| Vanilla | `E8ACC0F043E30C2578BD9A49375360534073D4562BBC31C6699FF6789BB0E7B9` |

Priorité : P0. Collision : faible. Runtime humain : requis.

### 7.2 Grande Crise orientale

Chemin :

`common/journal_entries/05_great_eastern_crisis.txt`

Objet :

`je_great_eastern_crisis`

Le fork contient une erreur parser directe sur l'ancien pinning. Source hotfix
et vanilla convergent sur :

```txt
should_be_pinned_by_default_involved = yes
should_be_pinned_by_default_uninvolved_or_context = no
```

Mais l'objet contient également cinq familles d'alignement adjacentes :

- deux références `geographic_region_balkans` vers
  `geographic_region_balkans_old` ;
- `region_balkans` vers `sr:region_balkans` ;
- ajout du bloc `should_show_when_not_involved` ;
- ajout de `can_revolution_inherit = yes`.

Le diff fork/vanilla représente six hunks fonctionnels, 23 additions et
4 suppressions. Un correctif de pinning isolé laisserait un objet encore
partiellement obsolète ; un alignement complet serait trop large pour succéder
au micro-scope italien sans audit dédié.

Priorité : P0. Collision : moyenne. Runtime humain : requis. Candidat reporté.

### 7.3 Merchant Banking pour GEN/VEN

Chemins :

- `common/history/countries/gen - genoa.txt` ;
- `common/history/countries/ven - venetia.txt`.

Objets : `c:GEN` et `c:VEN`.

| Arbre | État |
| --- | --- |
| Fork | `law_traditionalism` ×1 dans chaque pays |
| Source hotfix | `law_merchant_banking` ×1 dans chaque pays |
| Vanilla | fichiers absents, tags propres au mod |

La loi, son icône `merchant_banks.dds` et ses localisations anglaise et
française sont déjà présentes. Le changelog 2.3 annonce explicitement
« Merchant Banking (Maritime Republics) ».

Taille future : 2 fichiers, 2 objets, 2 hunks. Aucune erreur parser directe.
Priorité P1. Runtime humain requis.

Exclusions :

- ne pas ajouter le nom source-only des propriétaires terriens ;
- ne pas retirer `law_merchant_navy` ;
- ne toucher à aucun autre bloc ou à NAVY.

### 7.4 Navigation Acts

Chemins : GBR, HBC, NBS, ONT et ORA.

Le fork ne contient aucune activation de
`law_mercantilism_navigation_acts`. La source hotfix en contient une dans
chacun des cinq pays. Vanilla conserve ses propres lois de départ : HBC, NBS,
ONT et ORA utilisent le mercantilisme standard, tandis que GBR utilise le
protectionnisme dans la version 1.13 courante.

La loi, l'icône `regulation_acts.dds`, les localisations et la preuve du
changelog 2.3 existent. Le futur périmètre serait de 5 fichiers, 5 objets et
5 hunks. Le fichier GBR chevauche une différence de loi navale et le bloc NAVY
protégé. BIC est hors périmètre.

Priorité P1. Collision moyenne. Runtime humain requis. Candidat classé quatrième.

## 8. Autres petits candidats exclus

| Candidat | Raison |
| --- | --- |
| `01_coup.txt` | Une erreur directe, mais 10 hunks fork/vanilla et plusieurs changements de comportement/scope. |
| `04_imperialism_of_promise.txt` | Une erreur directe, mais trois hunks, changements de rôle/tooltip et divergence source/vanilla. |
| `00_tutorial.txt` | 52 erreurs, lot massif. |
| `00_sick_man.txt` | 8 erreurs dans 8 objets. |
| Résidus inconnus | Aucun inconnu ne fournit une preuve plus courte et plus convergente que le candidat grec. |

## 9. Top 3

| Rang | Phase candidate | Fichiers | Objets | Hunks | Priorité | Preuve | Collision | Runtime |
| ---: | --------------- | -------: | -----: | ----: | -------- | ------ | --------- | ------- |
| 1 | `HOTFIX_6A7F_GREEK_NATIONALISM_1_13_API_ALIGNMENT` | 1 | 1 | 2 | P0 | 1 erreur parser et 2 API convergentes hotfix/vanilla | Faible | Humain requis |
| 2 | `HOTFIX_6A8R_GREAT_EASTERN_CRISIS_1_13_AUDIT` | 1 | 1 | 6 | P0 | 1 erreur parser, mais objet largement obsolète | Moyenne | Humain requis après résolution |
| 3 | `HOTFIX_6A9F_GEN_VEN_MERCHANT_BANKING_STARTING_LAW` | 2 | 2 | 2 | P1 | Changelog 2.3 et dépendances déjà présentes | Faible à modérée | Humain requis |

Le candidat grec est sélectionné parce qu'il ferme toutes les divergences API
fork/vanilla de l'objet avec deux remplacements de ligne. Great Eastern Crisis
reste prioritaire sur le plan moteur, mais exige d'abord un audit de six hunks.
Merchant Banking reste le meilleur delta hotfix custom après les erreurs API.

Navigation Acts est quatrième : cinq fichiers et collision GBR/NAVY.

## 10. Sous-bloc sélectionné

`NEXT_EXECUTION_PHASE = HOTFIX_6A7F_GREEK_NATIONALISM_1_13_API_ALIGNMENT`

- Priorité : P0.
- Futur fichier gameplay : exactement
  `common/journal_entries/00_greek_nationalism.txt`.
- Futur objet : exactement `je_greek_nationalism`.
- Futurs hunks : exactement 2.
- Localisation nouvelle : aucune.
- Dépendance nouvelle : aucune.
- Risque de collision : faible.
- Remplacement complet du fichier : interdit.

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

Exclusions absolues :

- aucun changement de `is_shown_in_lobby` ;
- aucun changement de `is_shown_when_inactive` ;
- aucune importation de `geographic_region_megali_greece` ;
- aucune autre ligne modifiée.

Rollback : inversion exacte des deux hunks.

## 11. Runtime futur exclusivement humain

Après le PASS statique, Codex devra s'arrêter avec :

`RUNTIME_OPERATOR_ACTION_REQUIRED`

Fiche future condensée :

1. partie neuve en 1776 ;
2. choisir un pays de culture principale grecque ;
3. si aucun n'est directement jouable, libérer la Grèce depuis l'Empire
   ottoman et la jouer, sans console ;
4. ouvrir `Journal > Potentiel` et rechercher l'entrée de nationalisme grec ;
5. vérifier texte, conditions, absence de clé brute et absence d'anomalie de
   pinning ;
6. avancer d'au moins un jour ;
7. fermer Victoria 3 et le launcher ;
8. transmettre pays, dates, visibilité et observations ;
9. après fermeture, confirmer dans les nouveaux logs que l'erreur ciblée passe
   de 1 à 0 et qu'aucune erreur ne vise les deux nouvelles API.

Codex ne lancera ni le jeu ni le launcher et ne déclarera jamais le runtime PASS
sans les observations humaines.

## 12. Protections

Restent intacts et hors périmètre : DEI/VOC, Java, Balkan National Awakening,
Yugoslavia, Risorgimento, `00_italian_unification.txt`, NAVY, formations,
MARATH, SAT, KHP, Travancore, Inde, BIC, Sepoy, Bombay, ADMIN, Japon, Russie,
Autriche, Croatie, Slavonie, Suisse, révolutions américaine et française,
lettres de Kew, technologies, recherches, localisations françaises générales,
agriculture, alimentation, industrie, descripteurs, launcher, sauvegardes et
`bject`.

BIC conserve `law_frontier_colonization`. `law_colonial_exploitation` ne doit
jamais être restaurée.

## 13. Validations documentaires

- 161 résidus, somme des catégories cohérente.
- 113 lignes directement exploitables.
- 388 erreurs et 145 fichiers recalculés.
- Exactly 3 candidats dans le top 3.
- Exactly 1 candidat sélectionné.
- Aucun fichier clos réintroduit.
- Futur périmètre fermé à 1 fichier, 1 objet et 2 hunks.
- Prompt futur réservé au candidat grec.
- Runtime futur réservé à l'opérateur humain.
- Fichier gameplay modifié par 6A.7 : 0.

## 14. Hashes protégés

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

## 15. Documents modifiés

Uniquement :

1. `HOTFIX_6A7_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md` ;
2. `docs/reports/hotfix/INDEX.md` ;
3. `HOTFIX_REPORT_INDEX.csv` ;
4. `HOTFIX_MERGE_BLOCK_STATUS.csv` ;
5. `HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
6. `HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`.

## 16. État Git final et commit

Le HEAD final reste
`b80116cc226dbaacc51adb257448162969024272`. L'index Git est vide. L'état final
contient exactement les cinq documents suivis modifiés et le nouveau rapport
6A.7 non suivi, en plus des éléments protégés déjà présents :

```text
 M docs/reports/hotfix/INDEX.md
 M docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv
 M docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md
 M docs/reports/hotfix/_index/HOTFIX_NEXT_MERGE_PHASE_PROMPT.md
 M docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv
?? bject
?? docs/reports/hotfix/global_script/6A01_6A09/HOTFIX_6A7_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md
?? docs/research/technology/
```

`git diff --check` est propre, les CSV ont respectivement 22 et 17 colonnes,
les huit hashes protégés et le stash NAVY-3C-3 sont inchangés, et aucun
processus Victoria 3 ou Paradox n'est actif.

Aucun commit automatique n'est créé. La décision de commit appartient à
l'opérateur humain.

## 17. Verdict

`HOTFIX_6A7_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE`

`NO_GAMEPLAY_CHANGED`

`GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`

`NEXT_EXECUTION_PHASE = HOTFIX_6A7F_GREEK_NATIONALISM_1_13_API_ALIGNMENT`
