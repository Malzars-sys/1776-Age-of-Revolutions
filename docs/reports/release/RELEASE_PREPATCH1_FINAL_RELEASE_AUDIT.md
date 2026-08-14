# RELEASE-PREPATCH-1 — Audit final de release

## Verdict

```text
RELEASE_PREPATCH1 = PASS
STATIC_RELEASE_BLOCKERS = 0
DEFERRED_POST_RELEASE_COUNT = 9
RELEASE_READY = YES
```

Le contenu versionné à `HEAD` est prêt pour une phase de publication séparée. Ce verdict signifie qu'aucun bloqueur statique de release n'a été trouvé ; il ne signifie pas que la version, le changelog, le commit de release, le tag ou la publication ont déjà été confirmés ou exécutés.

## Baseline Git

```text
BRANCH = cleanup-post-release
HEAD = 538648fd0eb23ca7b14325e108ff682dea6f8fce
HEAD_SUBJECT = Organize pre-release documentation
PREFLIGHT_WORKTREE = CLEAN
PREFLIGHT_INDEX = EMPTY
PREFLIGHT_GIT_DIFF_CHECK = PASS

LAST_RELEASE_TAG = workshop-initial-release-20260810
LAST_RELEASE_TAG_DATE = 2026-08-10 19:18:18 +0200
RELEASE_BASELINE_COMMIT = 1e374f2f40252d229bc249600e3cbbe26085122d
RELEASE_TAG_IS_ANCESTOR_OF_HEAD = YES

COMMITS_SINCE_RELEASE = 23
FILES_CHANGED_SINCE_RELEASE = 276
INSERTIONS_SINCE_RELEASE = 52759
DELETIONS_SINCE_RELEASE = 5391
```

Le tag est annoté et porte le message `Initial Steam Workshop release`. Il constitue la dernière release fiable : les deux autres tags sont des points de sauvegarde pré-hotfix, pas des releases.

Répartition primaire des 276 chemins :

| Racine | Chemins |
|---|---:|
| `docs/` | 178 |
| `common/` | 61 |
| `localization/` | 22 |
| `tools/` | 11 |
| `gfx/` | 2 |
| `.gitignore` | 1 |
| `.metadata/` | 1 |

Le delta comprend 85 chemins appartenant aux familles gameplay gelées (`common`, `localization`, `gfx`). Aucun fichier `events/` ou `map_data/` ne diffère de la release initiale.

## Portée réelle du patch

### A. Compatibility / engine

- isolation VFS des historiques de personnages et de diplomatie afin d'empêcher le setup vanilla 1836 de contaminer le départ 1776 ;
- remplacement de l'ancienne copie de `00_defines.txt` par la baseline Victoria 3 1.13.9, avec un seul delta intentionnel : `START_DATE = 1776.1.1` ;
- restauration des constantes militaires/navales 1.13, suppression des anciennes clés `NMilitary` et conservation de `supported_version="1.13.*"`.

Le [rapport defines](../cleanup/CLEANUP2D3A_ENGINE_BASELINE_AND_DEFINES_REPAIR.md) valide statiquement la baseline 1.13.9. L'audit des rangs de commandement a ensuite vérifié les constantes concernées dans Victoria 3 1.13.10. La release ne revendique aucune compatibilité au-delà de la famille 1.13.

### B. Map / states

- aucun changement de `map_data/`, de géométrie, de province ou de state-region depuis la release initiale ;
- plusieurs abstractions politiques/cartographiques sont explicitement différées plutôt que maquillées par de faux dirigeants ou de fausses forces.

Les changements d'historiques de bâtiments et de population relèvent des catégories militaire et économique, pas d'une reconstruction de carte.

### C. Countries / politics

- isolation du setup politique 1776 et nouveaux gouvernements ciblés pour les dirigeants européens et non européens ;
- démarrage déterministe des cadres historiques BIC, DEI et HBC ;
- correction des régences Maratha, Saxe-Meiningen et Tibet, des titres affichés et du cas partagé George III/Irlande ;
- préservation des cas procéduraux ou structurels lorsque l'identité ou l'architecture politique n'est pas assez sûre.

La clôture Europe enregistre `CLEANUP2B3_RUNTIME = PASS`. La clôture non-Europe enregistre un runtime visuel PASS pour BIC, DEI, HBC, Tibet et Boukhara, avec zéro erreur gameplay attribuable à CLEANUP-2C.

### D. Historical rulers

- reconstruction des dirigeants majeurs, des pays européens résiduels et des pays actifs hors Europe ;
- classement exhaustif des 62 pays européens actifs, sans dirigeant procédural injustifié ;
- titres de gouverneurs, régents, maires, dirigeants de compagnies et souverains partagés adaptés au contexte de 1776 ;
- absence volontaire de faux souverain pour Luxembourg et de branches allemandes forcées lorsque le tag ne permet pas une identification sûre.

Autorités : [clôture européenne](../cleanup/CLEANUP2B3_COMPLETE_EUROPEAN_HISTORICAL_RECONSTRUCTION.md) et [clôture non européenne](../cleanup/CLEANUP2C1C_CHARTERED_COMPANY_TIBET_AND_TITLE_DUPLICATION_HOTFIX.md).

### E. Military

- reconstruction mondiale de 214 formations terrestres et réconciliation de leur infrastructure ;
- 2 557 unités régulières et 1 705 conscrits potentiels dans l'état final documenté ;
- correction de la matérialisation des unités, des régions de recrutement, de la conscription espagnole et des formations vides ;
- 79 généraux historiques et 135 procéduraux, exactement un général par formation ;
- 29 promotions minimales au rang 2 afin que la limite déterministe couvre les bataillons permanents.

Les rapports finaux enregistrent `STATIC_VALIDATION = PASS` et `RUNTIME = PASS` pour les généraux. Les effectifs n'ont pas été modifiés par la correction de rang.

### F. Naval

- reconstruction de 41 flottes totalisant 370 navires, avec HQ de départ valides ;
- réduction des forces navales anachroniques, suppression de la flotte prussienne vide et correction du doublon de la Real Armada ;
- 26 amiraux historiques fixes, avec rangs adaptés aux tailles de flotte, et conservation des commandements collectifs ou sans titulaire lorsqu'aucun individu sûr n'était justifié ;
- restauration de la flottille du Konkan : deux frégates, Anandrao Dhulap, véritable Administration navale et équipage `1000/1000`.

La [clôture des amiraux](../cleanup/CLEANUP2D6L_GLOBAL_HISTORICAL_ADMIRALS_1776_IMPLEMENTATION.md) enregistre `RUNTIME = PASS` et `SAVE_RELOAD = PASS`. La [clôture Maratha](../cleanup/CLEANUP1E_MARATH_FINAL_ACCEPTANCE.md) enregistre `MARATH_FINAL_RUNTIME = PASS`.

### G. Economy

- Merchant Banking recentré sur commerce, crédit, investissement privé et construction navale ;
- suppression du minting gratuit et de l'ancien modificateur national Centre of Commerce ;
- pénalités ciblées pour l'exploitation directe des mines et plantations non incorporées ;
- augmentation contrôlée des Trade Centers de Venise et Gênes, administration vénitienne renforcée et population génoise portée proportionnellement à 510 000 ;
- validation runtime finale après correction de la main-d'œuvre génoise.

La [clôture économique](../cleanup/CLEANUP2E4B_MERCHANT_REPUBLIC_RUNTIME_BALANCE_CORRECTION.md) enregistre `RUNTIME = PASS`.

### H. Buildings / monuments

- ajout du Rialto Commercial Complex à Venise et du Palazzo San Giorgio à Gênes ;
- effets locaux limités à `+10 %` de throughput des Trade Centers et `+10 %` d'avantage à l'export ;
- emplois réels : 700 au Rialto et 600 à San Giorgio ;
- icônes DDS dédiées et intégration à la règle d'effets des monuments.

Les modèles 3D et locators dédiés restent différés ; aucun fichier de carte n'a été ajouté pour ces monuments.

### I. Localization / presentation

- localisations anglaises et françaises pour gouvernements, titres, dirigeants, formations, généraux, amiraux et monuments ;
- correction de clés visibles, doublons de titres et noms de formations ;
- conservation de l'UTF-8 BOM là où le moteur l'exige.

### J. Documentation / research

- rapports de clôture, matrices de conversion et preuves runtime pour les rulers, formations, généraux, amiraux et républiques marchandes ;
- index documentaires consolidés ;
- recherche technologique conservée comme matériau de future conception, dont trois fichiers explicitement `PRELIMINARY / UNVERIFIED`.

```text
TECH_RESEARCH_USED_BY_RELEASE_GAMEPLAY = 0
UNVERIFIED_TECH_RESEARCH_FILES = 3
```

### K. Internal QA / hotfixes

- validateurs reproductibles pour généraux, amiraux, Merchant Banking et monuments ;
- matrices d'audit ligne par ligne et contrôles de non-régression ;
- aucun outil de QA n'est requis comme contenu joueur à l'exécution.

## Validation gameplay gelée

La méthode PREPATCH-2/3 trie tous les fichiers des cinq familles, associe chaque chemin relatif à son SHA-256 par une tabulation, joint les lignes par LF sans LF final, puis hash le manifeste UTF-8.

```text
GAMEPLAY_FILE_COUNT = 877
GAMEPLAY_TREE_SHA256 = 7319D86F6EB2AAB9181BD32A95D8D498FAFE1BDAEF57127EB83FF3E864C0A80F
GAMEPLAY_HASH_VALIDATION = PASS

INDUSTRIAL_CHAINS_SHA256 = 981A0C119D02C5A5F795C41800B678DDBEC9AD91890CDE4588DF36A98D011799
INDUSTRIAL_CHAINS_HASH_VALIDATION = PASS
```

## Audit des résidus explicites

La recherche statique a trouvé 46 lignes contenant `TODO`, `PLACEHOLDER`, `TEMP` ou `DEBUG`. Aucun `FIXME`, `WIP`, `TEST ONLY` ou `REMOVE ME` n'a été trouvé. Toutes ces lignes existaient avant le présent delta de release, sauf le commentaire `(Temp)` provenant de la baseline defines 1.13.9.

| Chemin et lignes | Contexte | Classification |
|---|---|---|
| `events/debug_events.txt:1,3,12,21,30,39,48,57,66,75,92,104,129,138,149,158,167,203,212,227,237,247,255,263,271` | 24 événements cachés, `orphan = yes`, appelables seulement comme outils de debug | `INTENTIONAL` |
| `common/coat_of_arms/coat_of_arms/03_new.txt:2` | commentaire décrivant un blason national générique de remplacement | `INTENTIONAL` |
| `common/on_actions/00_code_on_actions.txt:6356` | hack explicite empêchant les régents de produire des héritiers en attendant un support moteur | `INTENTIONAL` |
| `events/tibetan_expedition.txt:1019` | effet temporaire en jeu sur l'autorité, pas résidu de développement | `INTENTIONAL` |
| `common/defines/00_defines.txt:755` | commentaire upstream `(Temp)` sur la vitesse du réseau de déplacement | `INTENTIONAL` |
| `events/american_civil_war/acw_events.txt:226` | ciblage futur plus précis d'un amendement | `DEFERRED` |
| `events/japan_events/ryukyu_rivalry_events.txt:551` | vidéo japonaise provisoire à remplacer par une image plus adaptée | `DEFERRED` |
| `common/ai_strategies/00_default_strategy.txt:1661,2235,3398` | TODO upstream sur Official Nationality | `DEFERRED` |
| `common/amendments/00_amendments_enactment_04.txt:333,1207` | TODO upstream PRCAL-35135 | `DEFERRED` |
| `common/journal_entries/05_technocracy.txt:41` | même TODO upstream PRCAL-35135 | `DEFERRED` |
| `events/iberia_events/spanish_new_world_events.txt:296` | suivi Cultural Union Power Bloc PRCAL-41338 | `DEFERRED` |
| `events/peoples_springtime.txt:875,989` | remplacement futur du modificateur anti-révolution PRCAL-14137 | `DEFERRED` |
| `events/iberia_events/philippines_events.txt:3` | verrouillage DLC PRCAL-41476 | `DEFERRED` |
| `common/on_actions/00_code_on_actions.txt:1051` | déplacement futur de pulses vers les tags concernés | `DEFERRED` |
| `common/history/treaties/00_historical_treaties.txt:480` | relation Siam/Cambodge marquée pour correction upstream | `DEFERRED` |
| `common/history/pops/06_central_america.txt:341,380,402` | granularité démographique cubaine à revoir | `DEFERRED` |

```text
RESIDUE_HIT_LINES = 46
RESIDUE_INTENTIONAL = 29
RESIDUE_DEFERRED = 17
RESIDUE_DOCUMENTATION_ONLY = 0
RESIDUE_RELEASE_BLOCKERS = 0
```

## Anciens identifiants et marqueurs

| Contrôle | Résultat | Classification |
|---|---:|---|
| `designate_character_as_regent` | 0 | résolu |
| 12 anciennes clés `NMilitary` listées par CLEANUP-2D-3A | 0 | résolu |
| `modifier_centre_of_commerce_mod` | 0 | résolu |
| `fleet_scope_prussian_navy` | 0 | résolu |
| `Real_Armada_Espaola` | 0 | résolu |
| gouvernements bruts `gov_cleanup2c1_bic/dei/hbc` | 0 | résolu |
| `national_guard_preoccupied` | 0 | résolu |
| `building_naval_base` | 13 références conditionnelles | `DEFERRED` ; héritage antérieur à la release, aucun échec attribuable dans les runtimes finaux |
| `law_type:state_religion` | 17 historiques legacy | `DEFERRED` ; identifiant invalide connu, précédé dans ces fichiers par le macro politique conservateur qui active la loi valide |
| `institution = colonial_affairs` | 2 historiques legacy, HBC et ORG | `DEFERRED` ; la forme valide est `institution_colonial_affairs` |

Les deux historiques HBC produisent encore une composition de lois héritée et non canonisée. Le runtime documenté est stable et n'affiche aucune clé brute, mais le diagnostic historique a observé un échec PostValidate pour l'ancienne institution. Cette dette est rendue visible ci-dessous ; elle n'est pas corrigée dans une phase documentaire.

## DEFERRED_POST_RELEASE

1. **Carte et structures politiques** — Luxembourg, certaines branches allemandes et plusieurs tags non européens restent des abstractions temporaires ou des cas de map rework.
2. **Art des personnages** — portraits, vêtements historiques, DNA et autres assets visuels ne sont pas exhaustifs.
3. **Monuments 3D** — Rialto et San Giorgio sont fonctionnels en data/UI mais sans mesh, entity ou locator dédié.
4. **Future Tech Tree** — reconstruire et valider la recherche technologique, puis remplacer le grant temporaire Admiralty de Maratha par une progression navale adaptée.
5. **Nommage automatique des formations** — les noms ordinaux générés par le moteur ne disposent pas d'un pool scriptable par pays dans la baseline auditée.
6. **Merchant Banking** — pénalité des fermes non incorporées et rework AI différés faute de clé sûre ou de périmètre autorisé.
7. **Historiques legacy de pays** — canoniser HBC, les 17 anciennes activations `state_religion` et les deux IDs d'institution invalides dans une phase gameplay bornée.
8. **Références navales legacy** — auditer/remplacer les 13 usages de `building_naval_base` dans les événements et stratégies concernés.
9. **Backlog TODO hérité** — image Ryukyu, démographie cubaine et TODO upstream/PRCAL conservés sans régression constatée.

## Version et tag proposés

La version publique enregistrée dans `.metadata/metadata.json` est `2.2.0`, et le changelog historique emploie déjà `2.2.0`, `2.1.1`, `2.1.0`, etc. Les changements depuis la release initiale ajoutent de grandes fonctionnalités joueur sans rupture revendiquée du format : un incrément mineur est le plus cohérent.

```text
RECOMMENDED_RELEASE_VERSION = 2.3.0
RECOMMENDED_GIT_TAG = workshop-release-2.3.0-20260814
```

`v2.3.0` serait une alternative SemVer plus courte, mais `workshop-release-2.3.0-20260814` conserve la convention descriptive et datée du tag existant tout en ajoutant la version publique. Aucun fichier de version n'est modifié et aucun tag n'est créé pendant RELEASE-PREPATCH-1.

## Contrôles de phase

```text
COMMIT_CREATED = NO
TAG_CREATED = NO
PUSH_PERFORMED = NO
VICTORIA_3_LAUNCHED = NO
```
