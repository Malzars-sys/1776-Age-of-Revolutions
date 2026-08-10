# HOTFIX-6A.6 — Sélection du prochain résidu global

## 1. Identification

- Date : 29 juillet 2026.
- Phase : `HOTFIX_6A6_RESIDUAL_GLOBAL_SCRIPT_SELECTION`.
- Nature : audit et sélection strictement documentaires.
- Branche : `hotfix-dlc-audit`.
- HEAD initial : `6e6083fbf349f76b99a1fbb991cc2058df2dc5d7`.
- Commit initial : `6e6083f Align Yugoslavia journal entry pinning with Victoria 3 1.13`.
- HEAD final attendu : inchangé, aucun commit automatique.

## 2. État Git initial

Le préflight obligatoire est conforme :

- racine exacte du fork ;
- branche `hotfix-dlc-audit` ;
- 6A.5F présente dans le HEAD et déjà commitée ;
- aucun fichier suivi modifié ;
- aucun fichier staged ;
- seuls `bject` et les sept fichiers de `docs/research/technology/` sont non suivis ;
- stash exact présent :
  `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` ;
- Victoria 3 fermé ;
- launcher Paradox fermé ;
- `git diff --check` propre.

Les hashes SHA-256 initiaux protégés sont :

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

## 3. Sources consultées

Les sources canoniques ont été lues intégralement :

- `HOTFIX_6A5F_YUGOSLAVIA_JE_PINNING_1_13_ALIGNMENT.md` ;
- `HOTFIX_6A5_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md` ;
- `HOTFIX_6A4F_BALKAN_NATIONAL_AWAKENING_1_13_ALIGNMENT.md` ;
- `HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
- `HOTFIX_MERGE_BLOCK_STATUS.csv` ;
- `HOTFIX_REPORT_INDEX.csv` ;
- `HOTFIX_GLOBAL_DIFFERENCE_INVENTORY.csv` ;
- `HOTFIX_C1AI_CONCURRENT_WORK_RECONCILIATION.md` ;
- les changelogs pertinents du fork et de la source hotfix ;
- les logs et rotations existants de la session 6A.5F.

Les comparaisons trois voies utilisent, en lecture seule :

1. le fork courant ;
2. `1776_Age_of_Revolutions_hotfix_source` ;
3. le vanilla Victoria 3 1.13.

Victoria 3 et le launcher n'ont été ni lancés ni contrôlés. Aucun nouveau log
runtime n'a été produit.

## 4. Inventaire actualisé

L'inventaire global contient 534 lignes, dont 161 anciennes lignes
`PENDING_REVIEW` reclassées exclusivement. Après clôture de 6A.5F :

| Catégorie exclusive | Lignes |
| --- | ---: |
| `REQUIRED_HOTFIX_DELTA` | 7 |
| `VANILLA_1_13_ALIGNMENT_REQUIRED` | 20 |
| `ALREADY_MERGED` | 14 |
| `INTENTIONAL_FORK_DIVERGENCE` | 3 |
| `OBSOLETE_HOTFIX_CONTENT` | 1 |
| `POST_MERGE_DESIGN_BACKLOG` | 10 |
| `PROTECTED_CONCURRENT_WORK` | 19 |
| `UNKNOWN_REQUIRES_REVIEW` | 87 |
| **Total** | **161** |

Il reste **114 lignes directement exploitables par une revue** :

- 7 deltas hotfix requis ;
- 20 alignements vanilla 1.13 ;
- 87 inconnus à examiner.

Ce nombre ne représente pas 114 correctifs. Le total historique de « 26 deltas
à haute confiance » reste `UNVERIFIED` : aucune liste canonique exacte de 26
lignes n'a été retrouvée.

Les deux chemins suivants sont clos et classés `ALREADY_MERGED` :

- `common/journal_entries/05_balkan_national_awakening.txt` ;
- `common/journal_entries/05_creation_of_yugoslavia.txt`.

Ils ne sont pas candidats.

## 5. Analyse des 389 erreurs de pinning restantes

Le fichier `debug.1.log` de la session 6A.5F contient exactement 389 erreurs :

```text
Unexpected token: should_be_pinned_by_default,
```

Elles concernent 146 fichiers uniques. La propriété rejetée est toujours
`should_be_pinned_by_default`. Aucune erreur ne vise la propriété Victoria 3
1.13 `should_be_pinned_by_default_uninvolved_or_context`.

### 5.1 Répartition par statut d'inventaire

| Statut rapproché | Fichiers | Occurrences | Exécutable maintenant |
| --- | ---: | ---: | --- |
| `INTENTIONAL_FORK_DIVERGENCE` | 104 | 242 | Non, divergence à préserver ou à réexaminer séparément |
| `VANILLA_1_13_ALIGNMENT_REQUIRED` | 20 | 105 | Oui, uniquement par micro-hunks prouvés |
| `PENDING_REVIEW` brut | 8 | 19 | Non sans résolution manuelle supplémentaire |
| `MERGED_STATIC_ONLY` brut | 10 | 19 | Non, blocs déjà fusionnés ou protégés |
| Hors inventaire des différences | 4 | 4 | Non sans nouvelle preuve trois voies |
| **Total** | **146** | **389** | — |

Les catégories brutes des lignes de log ne remplacent pas la classification
canonique des 161 résidus. Elles servent uniquement à éviter de promouvoir une
erreur isolée provenant d'un bloc protégé ou déjà fusionné.

### 5.2 Familles principales

| Famille ou fichier | Occurrences | Catégorie ou protection | Décision |
| --- | ---: | --- | --- |
| `00_tutorial.txt` | 52 | `VANILLA_1_13_ALIGNMENT_REQUIRED` | Trop large pour le prochain micro-lot |
| objectifs joueur `great_game` | 17 | `INTENTIONAL_FORK_DIVERGENCE` | Exclu |
| `05_prestige_goods.txt` | 16 | `INTENTIONAL_FORK_DIVERGENCE` | Exclu |
| `03_russia.txt` | 12 | `PROTECTED_CONCURRENT_WORK` | Russie protégée |
| objectifs joueur `hegemon` | 11 | `INTENTIONAL_FORK_DIVERGENCE` | Exclu |
| objectifs joueur `economic_dominance` | 10 | `INTENTIONAL_FORK_DIVERGENCE` | Exclu |
| `00_sick_man.txt` | 8 | `VANILLA_1_13_ALIGNMENT_REQUIRED` | Huit objets, lot trop large |
| `00_negotiation_quests_je.txt` | 7 | `INTENTIONAL_FORK_DIVERGENCE` | Exclu |
| `06_economic_regeneration.txt` | 7 | `INTENTIONAL_FORK_DIVERGENCE` | Exclu |
| `07_poland_lithuania_mod.txt` | 7 | rapprochement mixte / déjà fusionné | Pas de hunk autonome prouvé |
| `00_acw_entries.txt` | 6 | divergence/backlog Amérique | Révolution américaine protégée |
| `00_meiji_restoration.txt` | 6 | Japon fusionné/protégé | Exclu |
| `06_portugal_politics.txt` | 6 | `VANILLA_1_13_ALIGNMENT_REQUIRED` | Six objets, reporté |

Les huit fichiers `PENDING_REVIEW` bruts des logs sont notamment
`07_poland_lithuania_mod.txt`, des journal entries américaines, françaises,
sud-américaines, Hindustan/Durrani, Metternich et fascisme autrichien. Leur
rapprochement révèle des blocs mixtes, protégés, déjà fusionnés ou de backlog.
Les quatre fichiers hors inventaire n'ont qu'une erreur chacun, mais aucune
preuve de hunk suffisamment fermée.

### 5.3 Les 20 fichiers d'alignement 1.13

| Fichier | Occurrences | Objets concernés |
| --- | ---: | --- |
| `00_canada_australia.txt` | 4 | `je_australia_aus`, `je_australia_gbr`, `je_canada_can`, `je_canada_gbr` |
| `00_fascism.txt` | 3 | `je_fascism_1`, `je_fascism_2`, `je_modernization_program` |
| `00_german_unification.txt` | 5 | cinq objets d'unification allemande |
| `00_greek_nationalism.txt` | 1 | `je_greek_nationalism` |
| `00_italian_unification.txt` | 1 | `je_risorgimento` |
| `00_peoples_springtime_je.txt` | 2 | `je_red_summer`, `je_springtime_of_the_peoples` |
| `00_poland.txt` | 2 | `je_christ_of_nations`, `je_poland_lithuania` |
| `00_romania.txt` | 2 | `je_all_for_one`, `je_unite_the_principalities` |
| `00_sick_man.txt` | 8 | huit objets `je_sick_man_*` |
| `00_tutorial.txt` | 52 | 40 objets de tutoriel distincts |
| `01_coup.txt` | 1 | `je_ip4_coup` |
| `02_gran_colombia.txt` | 3 | `je_andean_federation`, `je_gran_colombia`, `je_la_plata` |
| `03_afghanistan.txt` | 2 | `je_consolidate_afghanistan`, `je_unify_afghanistan` |
| `03_korea.txt` | 3 | `je_donghak_movement`, `je_gyojo_shinwon`, `je_korean_rebellion` |
| `04_imperialism_of_promise.txt` | 1 | `je_imperialism_of_promise` |
| `05_eastern_question.txt` | 2 | `je_eastern_question_austria`, `je_eastern_question_russia` |
| `05_great_eastern_crisis.txt` | 1 | `je_great_eastern_crisis` |
| `06_portugal_politics.txt` | 6 | six objets portugais |
| `06_portuguese_colonialism.txt` | 2 | `je_portuguese_colonialism`, `je_the_pink_map` |
| `06_spanish_africa.txt` | 4 | quatre objets de conquête africaine |
| **Total** | **105** | — |

Tous ces fichiers existent dans le fork, la source hotfix et vanilla. Leur
présence dans les trois arbres ne justifie jamais un remplacement complet.

## 6. Comparaisons trois voies des candidats sérieux

### 6.1 Pinning italien — candidat sélectionné

- Chemin : `common/journal_entries/00_italian_unification.txt`.
- Objet : `je_risorgimento`.
- Fork : `should_be_pinned_by_default = yes`.
- Source hotfix :
  `should_be_pinned_by_default_uninvolved_or_context = yes`.
- Vanilla 1.13 :
  `should_be_pinned_by_default_uninvolved_or_context = yes`.
- Erreur runtime existante : une occurrence directe, près de la ligne 133.
- Taille future : 1 fichier, 1 objet, 1 hunk, 1 remplacement de ligne.
- Localisation : aucune.
- Dépendance : aucune nouvelle.
- Collision : faible.
- Rollback : remplacer la propriété 1.13 par l'ancienne ligne unique.

Deux écarts adjacents sont explicitement hors du futur hunk :

1. le fork conserve `year >= 1836` dans `possible`. La source hotfix et vanilla
   l'omettent, mais cette limite est une divergence 1776 intentionnelle et doit
   rester inchangée ;
2. la source hotfix ajoute
   `is_in_geographic_region = geographic_region_italy_old` dans
   `is_shown_in_lobby` et `is_shown_when_inactive`, alors que le fork et vanilla
   ne l'ont pas. Ces deux ajouts ne doivent pas être importés.

Le hunk de pinning est donc le seul point où source hotfix et vanilla convergent
sur une correction API nécessaire sans dette fonctionnelle concurrente dans le
même objet.

### 6.2 Merchant Banking GEN/VEN — reporté

- Chemins :
  `common/history/countries/gen - genoa.txt` et
  `common/history/countries/ven - venetia.txt`.
- Objets : blocs pays `c:GEN` et `c:VEN`.
- Fork : `law_traditionalism` active au point concerné.
- Source hotfix : `law_merchant_banking` active.
- Vanilla : fichiers absents ; GEN et VEN sont du contenu propre au mod.
- Taille future fermée possible : 2 fichiers, 2 objets, 2 hunks de remplacement.
- Runtime parser : aucune erreur directe.
- Priorité : P1, fonctionnalité hotfix annoncée mais absente.
- Dépendances déjà présentes dans le fork :
  définition de la loi, icône `merchant_banks.dds`, localisations anglaise et
  française.
- Preuve : changelog 2.3, annonce « Merchant Banking (Maritime Republics) ».
- Collision : faible à modérée.
- Runtime humain : nécessaire pour contrôler la loi de départ de GEN et VEN.
- Rollback : réactiver `law_traditionalism` dans chacun des deux blocs pays.

Le diff brut source ajoute aussi un nom spécifique aux propriétaires terriens
et retire `law_merchant_navy`. Ces écarts sont indépendants ; le second touche
une protection NAVY. Ils ne sont pas nécessaires à Merchant Banking et doivent
rester exclus. Le nom d'IG demeure une décision séparée.

### 6.3 Navigation Acts GBR et colonies — reporté

- Chemins :
  `gbr - great britain.txt`, `hbc - hudson bay company.txt`,
  `nbs - new brunswick.txt`, `ont - ontario.txt` et `ora - oranje.txt`.
- Objets : blocs pays `c:GBR`, `c:HBC`, `c:NBS`, `c:ONT`, `c:ORA`.
- Fork : `law_mercantilism_navigation_acts` absente ; mercantilisme standard
  conservé.
- Source hotfix : Navigation Acts active dans les cinq pays.
- Vanilla 1.13 : mercantilisme standard ; la variante est une fonctionnalité
  propre au hotfix.
- Taille future : 5 fichiers, 5 objets, 5 hunks.
- Runtime parser : aucune erreur directe.
- Priorité : P1.
- Dépendances déjà présentes : loi, icône et localisations.
- Preuve : même annonce 2.3 « Navigation Acts (Britain and its colonies) ».
- Collision : moyenne, car le fichier GBR contient un écart adjacent de loi
  navale et chevauche le bloc NAVY protégé.
- Runtime humain : nécessaire pour vérifier les cinq lois de départ.
- Rollback : rétablir `law_mercantilism` dans les cinq objets.

Le fichier BIC est absolument hors périmètre. Sa ligne
`activate_law = law_type:law_frontier_colonization` doit rester intacte et
`law_colonial_exploitation` ne doit jamais être restaurée.

## 7. Petits candidats de pinning exclus

| Candidat | Raison de l'exclusion |
| --- | --- |
| `00_greek_nationalism.txt` | Une erreur unique et pinning convergent, mais le même objet garde aussi l'API de loi obsolète `has_law = law_type:law_monarchy`, remplacée dans hotfix et vanilla par `country_has_monarchy_law = yes`. Un hunk unique ne fermerait pas proprement l'objet. |
| `01_coup.txt` | Une erreur unique, mais plusieurs changements de comportement, nettoyage et scope coexistent dans les comparaisons source/vanilla. |
| `04_imperialism_of_promise.txt` | Une erreur unique, mais autres écarts de rôle de personnage et de tooltip ; source hotfix et vanilla ne convergent pas entièrement. |
| `05_great_eastern_crisis.txt` | Une erreur unique, mais la sémantique 1.13 attend deux propriétés (`involved = yes`, `uninvolved_or_context = no`) et le fichier comporte d'autres changements de visibilité et de géographie. |
| `00_tutorial.txt` | 52 erreurs directes, mais 40 objets et un risque de lot massif contraire au mandat. |
| `00_sick_man.txt` | Huit erreurs dans huit objets ; trop large malgré la preuve API. |

## 8. Top 3

| Rang | Phase candidate | Fichiers | Objets | Hunks | Priorité | Preuve | Collision | Runtime |
| ---: | --------------- | -------: | -----: | ----: | -------- | ------ | --------- | ------- |
| 1 | `HOTFIX_6A6F_ITALIAN_UNIFICATION_JE_PINNING_1_13_ALIGNMENT` | 1 | 1 | 1 | P0 | 1 erreur parser directe ; hotfix = vanilla 1.13 | Faible | Humain requis après PASS statique |
| 2 | `HOTFIX_6A7F_GEN_VEN_MERCHANT_BANKING_STARTING_LAW` | 2 | 2 | 2 | P1 | Changelog 2.3, loi/icône/localisations déjà présentes | Faible à modérée ; écarts IG/NAVY adjacents exclus | Humain requis |
| 3 | `HOTFIX_6A8F_GBR_COLONIES_NAVIGATION_ACTS_STARTING_LAW` | 5 | 5 | 5 | P1 | Changelog 2.3, loi/icône/localisations déjà présentes | Moyenne ; GBR chevauche NAVY | Humain requis |

Merchant Banking figure avant Navigation Acts car il touche deux objets au lieu
de cinq et n'impose pas le fichier GBR. Le pinning italien l'emporte sur les
deux lois parce qu'il corrige une erreur parser Victoria 3 1.13 déjà observée,
avec un hunk convergent et un rollback d'une ligne.

## 9. Sous-bloc sélectionné

`NEXT_EXECUTION_PHASE = HOTFIX_6A6F_ITALIAN_UNIFICATION_JE_PINNING_1_13_ALIGNMENT`

- Priorité : P0.
- Futur fichier gameplay : exactement
  `common/journal_entries/00_italian_unification.txt`.
- Futur objet : exactement `je_risorgimento`.
- Futur hunk :

```diff
-	should_be_pinned_by_default = yes
+	should_be_pinned_by_default_uninvolved_or_context = yes
```

- Dépendances : aucune.
- Localisation : aucune.
- Risque de collision : faible.
- Remplacement du fichier complet : interdit.
- `year >= 1836` : doit rester strictement inchangé.
- Géographie de visibilité : doit rester strictement inchangée.
- Rollback exact : inversion du hunk ci-dessus.

## 10. Runtime futur exclusivement humain

Le correctif futur nécessitera un runtime humain, mais Codex devra s'arrêter
après le PASS statique avec :

`RUNTIME_OPERATOR_ACTION_REQUIRED`

La fiche condensée préparée dans le prochain prompt demandera un seul lancement :

1. partie neuve en 1776 avec le fork et ses dépendances ;
2. pays de culture principale nord-italienne ou sud-italienne, par exemple
   Naples si disponible ;
3. inspection de `Journal > Potentiel` et de l'entrée Risorgimento ;
4. confirmation que les conditions sont lisibles, sans clé brute ni anomalie
   de pinning ; la condition `year >= 1836` peut légitimement rester non remplie ;
5. progression d'au moins un jour ;
6. fermeture du jeu et du launcher ;
7. compte rendu humain avec date de fin, visibilité de l'entrée et anomalies ;
8. seulement après fermeture, analyse des logs existants pour confirmer que
   l'erreur ciblant `00_italian_unification.txt` passe de 1 à 0.

Codex ne devra jamais déclarer le runtime PASS sans ces observations humaines.

## 11. Protections et exclusions

Sont hors périmètre et intacts : DEI/VOC, Java, économie post-compagnie,
Balkan National Awakening, Yugoslavia 6A.5F, NAVY, lois navales, formations,
MARATH, SAT, KHP, Travancore, Inde, BIC, Sepoy, Bombay, ADMIN, Japon, Russie,
Autriche, Croatie, Slavonie, Suisse, révolutions américaine et française,
lettres de Kew, technologies, recherches technologiques, localisations
françaises générales, agriculture, alimentation, industrie, descripteurs,
launcher, sauvegardes et `bject`.

Les erreurs nombreuses des tutoriels, objectifs joueur, prestige goods, Russie,
`sick_man` et autres journal entries ne sont ni corrigées ni regroupées en lot.

## 12. Validations documentaires

- 161 résidus classés une seule fois.
- Somme des catégories : 161.
- Lignes directement exploitables : 114.
- Erreurs de pinning analysées : 389.
- Fichiers de log uniques : 146.
- Candidats publiés : exactement 3.
- Candidat sélectionné : exactement 1.
- Fichiers clos non réintroduits.
- Futur périmètre fermé à 1 fichier, 1 objet, 1 hunk.
- Runtime futur réservé à l'opérateur humain.
- Aucun fichier gameplay modifié.
- Aucun lancement ni contrôle du jeu ou du launcher.

## 13. Documents modifiés

Uniquement :

1. `docs/reports/hotfix/global_script/6A01_6A09/HOTFIX_6A6_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md` ;
2. `docs/reports/hotfix/INDEX.md` ;
3. `docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv` ;
4. `docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv` ;
5. `docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
6. `docs/reports/hotfix/_index/HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`.

## 14. État Git final et décision de commit

- HEAD final :
  `6e6083fbf349f76b99a1fbb991cc2058df2dc5d7`, identique au HEAD initial.
- Branche finale : `hotfix-dlc-audit`.
- `git diff --check` : propre.
- Index Git : vide.
- Documents de phase modifiés ou créés : exactement 6.
- Fichier gameplay modifié : 0.
- Entrée de statut inattendue : 0.
- Hashes protégés contrôlés : 8, divergence : 0.
- Stash NAVY-3C-3 : intact.
- Victoria 3 et launcher Paradox : fermés.

`git status --short` final :

```text
 M docs/reports/hotfix/INDEX.md
 M docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv
 M docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md
 M docs/reports/hotfix/_index/HOTFIX_NEXT_MERGE_PHASE_PROMPT.md
 M docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv
?? bject
?? docs/reports/hotfix/global_script/6A01_6A09/HOTFIX_6A6_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md
?? docs/research/technology/
```

Les deux entrées non suivies préexistantes `bject` et
`docs/research/technology/` restent protégées. Aucun commit n'est créé
automatiquement. La décision de commit appartient à l'opérateur humain après
lecture du diff documentaire.

## 15. Verdict

`HOTFIX_6A6_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE`

`NO_GAMEPLAY_CHANGED`

`GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`

`NEXT_EXECUTION_PHASE = HOTFIX_6A6F_ITALIAN_UNIFICATION_JE_PINNING_1_13_ALIGNMENT`
