# HOTFIX-6A.4 — Sélection du prochain résidu global

Date : 28 juillet 2026  
Phase : `SELECT_RESIDUAL_GLOBAL_SCRIPT_REVIEW`  
Branche : `hotfix-dlc-audit`  
HEAD initial : `f64fc9d71da0909d3ded6d6ba8cf1768157df2c2`

## 1. Verdict

`HOTFIX_6A4_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE`  
`NEXT_EXECUTION_PHASE = HOTFIX_6A4F_BALKAN_NATIONAL_AWAKENING_1_13_ALIGNMENT`  
`NO_GAMEPLAY_CHANGED`  
`GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`

Le prochain sous-bloc est l’alignement Victoria 3 1.13 de
`je_balkan_national_awakenings`, dans un seul fichier :

`common/journal_entries/05_balkan_national_awakening.txt`

La numérotation `6A.4` est cohérente avec les paquets clos `6A.2` et `6A.3`.
Le présent rapport sélectionne et ferme le périmètre ; la phase d’exécution
reçoit donc le suffixe `6A.4F`.

## 2. État Git initial

- racine : `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork` ;
- branche : `hotfix-dlc-audit` ;
- HEAD : `f64fc9d Complete DEI and VOC dissolution hotfix` ;
- aucun fichier suivi modifié ;
- aucun fichier staged ;
- non-suivis autorisés seulement : `bject` et les sept fichiers de
  `docs/research/technology/` ;
- stash intact :
  `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla`.

Victoria 3 était encore ouvert au premier contrôle, PID `31668`. Une fermeture
normale de sa fenêtre a été demandée, sans arrêt forcé. Le contrôle suivant a
confirmé l’absence de Victoria 3 et du launcher avant toute modification
documentaire.

## 3. Sources intégralement relues

- `HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
- `HOTFIX_MERGE_BLOCK_STATUS.csv` ;
- les 104 lignes de données de `HOTFIX_REPORT_INDEX.csv` ;
- `HOTFIX_NEXT_MERGE_PHASE_PROMPT.md` ;
- les 534 lignes de données de `HOTFIX_GLOBAL_DIFFERENCE_INVENTORY.csv` ;
- `HOTFIX_C1AI_CONCURRENT_WORK_RECONCILIATION.md` ;
- `HOTFIX_6A3F_DEI_TARGETED_FIX.md` ;
- `HOTFIX_MILITARY_FORMATIONS_1_13_RUNTIME_QA.md` ;
- `PHASE_ADMIN_2_GLOBAL_GOVERNMENT_ADMIN_PM_AUDIT.md` ;
- `HOTFIX_DLC_UPSTREAM_CHANGE_AUDIT.md` ;
- `HOTFIX_2_LAWS_MERCHANT_BANKING_NAVIGATION_ACTS.md` ;
- les changelogs du fork et de la source hotfix ;
- les versions fork, hotfix et vanilla 1.13 des meilleurs candidats ;
- le `error.log` courant, daté du 28 juillet 2026 à 23:51:25.

Sources externes en lecture seule :

- hotfix :
  `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source` ;
- vanilla 1.13 :
  `C:\Games\Victoria 3 The Great Wave\game`.

## 4. Inventaire réellement examiné

Les 161 lignes `PENDING_REVIEW` ont été relues. Le total historique de
« 26 deltas à haute confiance » reste `UNVERIFIED` : aucun registre canonique
de 26 chemins n’existe.

Classement final, exclusif et exhaustif :

| Catégorie | Lignes |
|---|---:|
| `REQUIRED_HOTFIX_DELTA` | 7 |
| `VANILLA_1_13_ALIGNMENT_REQUIRED` | 22 |
| `ALREADY_MERGED` | 12 |
| `INTENTIONAL_FORK_DIVERGENCE` | 3 |
| `OBSOLETE_HOTFIX_CONTENT` | 1 |
| `POST_MERGE_DESIGN_BACKLOG` | 10 |
| `PROTECTED_CONCURRENT_WORK` | 19 |
| `UNKNOWN_REQUIRES_REVIEW` | 87 |
| **Total** | **161** |

Les 87 lignes encore inconnues se répartissent ainsi :

| Domaine | Lignes |
|---|---:|
| événements | 73 |
| journal entries | 4 |
| country history | 1 |
| diplomatie | 1 |
| country definitions | 1 |
| customizable localization | 1 |
| government types | 1 |
| historique commun | 1 |
| on_actions | 1 |
| scripted buttons | 2 |
| static modifiers | 1 |

Elles restent des unités de revue, pas un lot exécutable.

## 5. Registre de classement

Les règles suivantes sont appliquées dans l’ordre. Tous les chemins non cités
après application des règles sont `UNKNOWN_REQUIRES_REVIEW`. Cette règle de
reste affecte explicitement chacune des 87 lignes restantes à une seule
catégorie.

### 5.1 `ALREADY_MERGED`

Égalité fonctionnelle après normalisation des fins de ligne, espaces,
commentaires seuls ou ordre de lignes sans changement d’objet, ou paquet clos :

- `common/coat_of_arms/coat_of_arms/03_new.txt`
- `common/company_types/02_new_companies.txt`
- `common/country_definitions/02_modded_countries.txt`
- `common/flag_definitions/07_NM_Flags.txt`
- `common/history/ai/00_secret_goals.txt`
- `common/history/countries/fra - france.txt`
- `common/history/countries/net - netherlands.txt`
- `common/history/countries/swe - sweden.txt`
- `common/history/pops/00_west_europe.txt`
- `common/history/pops/01_south_europe.txt`
- `common/journal_entries/07_poland_lithuania_mod.txt`
- `events/dei_breakup.txt`

### 5.2 `REQUIRED_HOTFIX_DELTA`

Les deux lois existent déjà dans le fork avec leurs icônes et localisations,
mais les activations de départ annoncées par le changelog 2.3 manquent encore :

- `common/history/countries/gen - genoa.txt`
- `common/history/countries/ven - venetia.txt`
- `common/history/countries/gbr - great britain.txt`
- `common/history/countries/hbc - hudson bay company.txt`
- `common/history/countries/nbs - new brunswick.txt`
- `common/history/countries/ont - ontario.txt`
- `common/history/countries/ora - oranje.txt`

Seuls les objets `law_merchant_banking` et
`law_mercantilism_navigation_acts` sont admis par ce classement. Les deltas de
lois navales présents dans les mêmes diffs restent protégés.

### 5.3 `VANILLA_1_13_ALIGNMENT_REQUIRED`

Ces 22 fichiers emploient encore au moins un
`should_be_pinned_by_default = ...` alors que la source hotfix et vanilla 1.13
emploient le champ `should_be_pinned_by_default_uninvolved_or_context`.

- `common/journal_entries/00_canada_australia.txt`
- `common/journal_entries/00_fascism.txt`
- `common/journal_entries/00_german_unification.txt`
- `common/journal_entries/00_greek_nationalism.txt`
- `common/journal_entries/00_italian_unification.txt`
- `common/journal_entries/00_peoples_springtime_je.txt`
- `common/journal_entries/00_poland.txt`
- `common/journal_entries/00_romania.txt`
- `common/journal_entries/00_sick_man.txt`
- `common/journal_entries/00_tutorial.txt`
- `common/journal_entries/01_coup.txt`
- `common/journal_entries/02_gran_colombia.txt`
- `common/journal_entries/03_afghanistan.txt`
- `common/journal_entries/03_korea.txt`
- `common/journal_entries/04_imperialism_of_promise.txt`
- `common/journal_entries/05_balkan_national_awakening.txt`
- `common/journal_entries/05_creation_of_yugoslavia.txt`
- `common/journal_entries/05_eastern_question.txt`
- `common/journal_entries/05_great_eastern_crisis.txt`
- `common/journal_entries/06_portugal_politics.txt`
- `common/journal_entries/06_portuguese_colonialism.txt`
- `common/journal_entries/06_spanish_africa.txt`

La JE balkanique ajoute une preuve plus forte : son autre écart appelle
`sr:region_danubia`, définition stratégique commentée en vanilla 1.13.

### 5.4 `INTENTIONAL_FORK_DIVERGENCE`

- `common/history/pops/13_australasia.txt`
- `common/history/states/00_states.txt`
- `map_data/state_regions/13_australasia.txt`

Ces trois overrides portent le setup 1776 et les corrections australiennes
protégées. Une divergence de hash n’autorise aucun remplacement.

### 5.5 `OBSOLETE_HOTFIX_CONTENT`

- `events/strike_events.txt`

Le fork est identique à vanilla 1.13. La source remplace une clé valide par
`pass_institution_or_else_2`, absente du hotfix, du fork et de vanilla dans
toutes les localisations consultées. Importer ce hunk créerait une clé brute.

### 5.6 `POST_MERGE_DESIGN_BACKLOG`

Toutes les lignes `region = america` ou `region = france` non déjà classées
`ALREADY_MERGED`, plus :

- `events/texan_war_of_independence_events.txt`
- `events/tech_events/trench_warfare.txt`

Ce groupe contient dix lignes. Il reste exclu par les backlogs Révolution
américaine, Révolution française et technologies.

### 5.7 `PROTECTED_CONCURRENT_WORK`

- `common/dynamic_country_names/00_dynamic_country_names.txt`
- `common/flag_definitions/00_flag_definitions.txt`
- `common/history/countries/dennor - denmark-norway.txt`
- `common/history/countries/sar - sardinia.txt`
- `common/history/countries/sic - two sicilies.txt`
- `common/history/countries/spa - spain.txt`
- `common/history/global/00_global.txt`
- `common/journal_entries/00_opium.txt`
- `common/journal_entries/05_austrian_fascism.txt`
- `common/journal_entries/05_metternich.txt`
- `common/journal_entries/06_new_imperialism_mod.txt`
- `common/journal_entries/07_hindustan_is_durrani_mod.txt`
- `common/scripted_buttons/00_new_colonial_admins.txt`
- `events/balkans_events/metternich.txt`
- `events/british_raj_events.txt`
- `events/opium_events.txt`
- `events/opium_wars_events.txt`
- `localization/english/mod_journal_entries_l_english.yml`
- `localization/english/mod_v2content_l_english.yml`

Les raisons sont NAVY, Inde/BIC/Sepoy/Bombay, Japon, Autriche ou paquets
DEI/localisation déjà validés. Les erreurs de présidences indiennes observées
dans le fichier de noms dynamiques ne rouvrent pas le bloc Inde pendant cette
phase.

## 6. Regroupement fonctionnel des résidus pertinents

| Domaine | Résidus exploitables | Décision |
|---|---|---|
| APIs de journal entries 1.13 | 22 fichiers, dont une erreur régionale prouvée | scinder fichier par fichier |
| lois et pays de départ | Merchant Banking, Navigation Acts | deux futurs paquets fermés |
| événements globaux | 73 inconnus, quelques petits hunks | revue ultérieure par famille |
| diplomatie / Treaty of London | plusieurs dépendances source-only | trop large pour la prochaine phase |
| Ibérie et Balkans narratifs | événements et JEs hétérogènes | revue régionale après l’API balkanique |
| pays hors blocs clos | Portugal et quelques définitions | provenance/design encore ambigus |
| setup et carte | états globaux et Australasie | divergence intentionnelle ou protégée |

## 7. Trois meilleurs candidats

| Rang | Sous-bloc | Fichiers gameplay | Importance | Confiance | Collision | Runtime |
|---:|---|---:|---|---|---|---|
| 1 | Balkan National Awakening 1.13 | 1 | P1, erreur répétée | très haute | très faible | oui, ciblé |
| 2 | Merchant Banking GEN/VEN | 2 | P1, fonctionnalité 2.3 absente | haute | faible si NAVY exclu | oui, ciblé |
| 3 | Navigation Acts GBR et colonies | 5 | P1, fonctionnalité 2.3 absente | haute | moyenne, GBR/BIC/NAVY | oui |

### Candidat 1 — sélectionné

Le `error.log` contient 51 occurrences de :

`common/journal_entries/05_balkan_national_awakening.txt:11`  
`Invalid right side during comparison 'sr'`

Le fork teste `sr:region_danubia`, supprimée comme région stratégique active en
1.13. La source hotfix remplace le bloc par
`is_in_geographic_region = geographic_region_balkans`. Cette région
géographique existe en vanilla 1.13 et encapsule `sr:region_balkans`, laquelle
contient désormais les anciens États danubiens. Le second hunk source/1.13
migre le champ de pinning.

### Candidat 2 — différé

Le changelog 2.3 et `HOTFIX_2_LAWS_MERCHANT_BANKING_NAVIGATION_ACTS.md`
prouvent l’intention. `law_merchant_banking`, son icône et ses localisations
existent, mais GEN et VEN commencent encore sous `law_traditionalism`.
L’ajout du nom unique des propriétaires terriens est séparé : sa localisation
anglaise manque dans le fork et sa traduction française doit être conçue sans
toucher aux localisations générales protégées.

### Candidat 3 — différé

Les activations Navigation Acts sont explicites pour GBR, HBC, NBS, ONT et ORA.
Le paquet touche toutefois cinq fichiers, le diff GBR est large et BIC est
absolument exclu. Il reste légitime mais moins atomique.

## 8. Sous-bloc sélectionné

Phase suivante :

`HOTFIX_6A4F_BALKAN_NATIONAL_AWAKENING_1_13_ALIGNMENT`

Fichier gameplay unique :

- `common/journal_entries/05_balkan_national_awakening.txt`

Objet unique :

- `je_balkan_national_awakenings`

Hunks fermés :

1. remplacer le test `capital/OR` contenant `region_balkans` et
   `region_danubia` par
   `is_in_geographic_region = geographic_region_balkans` ;
2. remplacer `should_be_pinned_by_default = yes` par
   `should_be_pinned_by_default_uninvolved_or_context = yes`.

Aucun autre champ de la JE ne doit changer.

## 9. Dépendances et protections

Dépendances vérifiées :

- `geographic_region_balkans` est défini par vanilla 1.13 dans
  `common/geographic_regions/06_new_strategic_regions.txt` ;
- cette région contient `sr:region_balkans` ;
- `region_balkans` est active dans
  `common/strategic_regions/europe_strategic_regions.txt` et contient les États
  anciennement répartis dans `region_danubia` ;
- le nouveau champ de pinning est l’API dominante de vanilla 1.13 et est déjà
  utilisé dans le fork.

Protections : aucun fichier Autriche/Croatie/Suisse, DEI/VOC, Russie, Japon,
Inde/BIC/Sepoy/Bombay, formations, NAVY, ADMIN, MARATH/SAT/KHP, technologie,
France, Amérique ou localisation ne doit être modifié.

## 10. Validation et rollback prévus

Validation statique :

- un seul objet `je_balkan_national_awakenings` ;
- accolades équilibrées ;
- zéro `sr:region_danubia` dans ce fichier ;
- une occurrence du trigger géographique ;
- zéro ancien champ de pinning dans cet objet et une occurrence du nouveau ;
- diff gameplay limité aux deux hunks exacts ;
- `git diff --check` propre et index vide.

Runtime nécessaire : oui. Un seul lancement consolidé doit charger le fork
1776 avec `ip3_content`, laisser passer au moins un jour, puis vérifier que le
log ne contient plus aucune erreur visant ce fichier. Aucun autre défaut global
ne doit être absorbé dans cette phase.

Rollback minimal : inverser seulement les deux hunks décrits ci-dessus, jamais
restaurer le fichier complet. Le rollback du premier hunk rétablit la dette
connue `region_danubia` et doit donc conduire à un verdict d’échec, pas à une
clôture.

## 11. Conclusion

Le choix réduit un risque runtime réellement observé, dans un seul objet et un
seul fichier, avec deux hunks vérifiables et sans collision avec les blocs
protégés. Aucun gameplay n’est modifié pendant `HOTFIX-6A.4`.
