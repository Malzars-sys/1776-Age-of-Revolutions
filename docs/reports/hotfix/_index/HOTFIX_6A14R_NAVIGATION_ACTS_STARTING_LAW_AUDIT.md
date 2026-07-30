# HOTFIX-6A.14R — Audit de la loi initiale Navigation Acts

Date : 30 juillet 2026

Phase : `HOTFIX_6A14R_NAVIGATION_ACTS_STARTING_LAW_AUDIT`

Branche : `hotfix-dlc-audit`

HEAD initial et final : `382a2b51b788e181228187c417e59fc052ed303d` —
`Apply GEN and VEN Merchant Banking starting law`

## 1. Décision

L'audit documentaire trois voies est terminé. Aucune correction gameplay,
aucun runtime, aucun staging et aucun commit n'ont été effectués.

Le périmètre théorique de cinq historiques pays publié par 6A.13 est bien
reproductible :

1. `common/history/countries/gbr - great britain.txt`;
2. `common/history/countries/hbc - hudson bay company.txt`;
3. `common/history/countries/nbs - new brunswick.txt`;
4. `common/history/countries/ont - ontario.txt`;
5. `common/history/countries/ora - oranje.txt`.

Il n'est toutefois pas exhaustif. La source hotfix contient aussi une
activation initiale dans BIC et une activation événementielle dans l'échec de
l'indépendance américaine. Le fork et la source contiennent en outre une
seconde histoire HBC, mal orthographiée `hubson`, qui cible le même objet
`c:HBC`.

Le périmètre fonctionnel réel est donc de **huit fichiers gameplay
pertinents** :

- six historiques pays contenant une activation Navigation Acts dans la
  source;
- une journal entry contenant une activation événementielle dans la source;
- une seconde histoire HBC sans Navigation Acts, mais concurrente pour le
  même objet et ses groupes de lois.

L'infrastructure de la loi est déjà intégrée. En revanche, l'objet HBC actif
et unique ne peut pas être démontré statiquement, et les deux définitions
appliquent des lois mutuellement divergentes. Ce conflit est le blocage
principal. GBR demeure en plus un fichier NAVY protégé; BIC et la chaîne
américaine sont également protégées.

Verdict principal :

`NAVIGATION_ACTS_STARTING_LAW_BLOCKED_BY_HBC_DEFINITION_CONFLICT`

La phase corrective `HOTFIX_6A14F_NAVIGATION_ACTS_STARTING_LAW_ALIGNMENT`
n'est pas sélectionnée.

## 2. Préflight Git et protections

| Contrôle | Résultat |
| --- | --- |
| Racine | fork exact |
| Branche initiale | `hotfix-dlc-audit` |
| HEAD initial complet | `382a2b51b788e181228187c417e59fc052ed303d` |
| Message du HEAD | exact |
| Index staged | vide |
| Fichiers suivis modifiés au départ | aucun |
| Stash attendu | présent, ligne exacte |
| Hash objet du stash avant | `518df704fa14599c0f254fae13859210663dd976` |
| Source hotfix | lecture seule |
| Vanilla 1.13 | lecture seule |

État Git initial exhaustif :

```txt
?? bject
?? docs/research/technology/TECH_TREE_BUILDING_AND_PRODUCTION_CANDIDATES.csv
?? docs/research/technology/TECH_TREE_INDUSTRIAL_CHAINS.md
?? docs/research/technology/TECH_TREE_INDUSTRIAL_HISTORY_DEEP_RESEARCH.md
?? docs/research/technology/TECH_TREE_INDUSTRIAL_INNOVATIONS_DATABASE.csv
?? docs/research/technology/TECH_TREE_RESEARCH_BIBLIOGRAPHY.md
?? docs/research/technology/TECH_TREE_RESOURCE_CANDIDATES.csv
?? docs/research/technology/TECH_TREE_VICTORIA3_GAP_ANALYSIS.md
```

Le contenu de `bject`, des sept fichiers technologiques et du stash n'a pas
été ouvert. Leurs noms ont seulement été relevés par le statut Git, comme
l'exige le contrôle d'entrée. Les hashes historiques publiés par 6A.13F ont
été lus dans le rapport canonique, mais ils n'ont pas été recalculés pendant
6A.14R afin de respecter l'interdiction d'inspection.

## 3. Sources documentaires lues

Les documents suivants ont été lus intégralement avant toute écriture :

- `HOTFIX_6A13_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md`;
- `HOTFIX_6A13F_GEN_VEN_MERCHANT_BANKING_STARTING_LAW.md`;
- `HOTFIX_MERGE_COMPLETION_ROADMAP.md`;
- `HOTFIX_MERGE_BLOCK_STATUS.csv`;
- `HOTFIX_REPORT_INDEX.csv`;
- `HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`;
- `HOTFIX_MERGE_THREE_WAY_INVENTORY.csv`;
- `HOTFIX_GLOBAL_DIFFERENCE_INVENTORY.csv`;
- `HOTFIX_MERGE_REMAINING_WORK.csv`;
- `HOTFIX_2_LAWS_MERCHANT_BANKING_NAVIGATION_ACTS.md`;
- `HOTFIX_DLC_UPSTREAM_CHANGE_AUDIT.md`;
- `PHASE_NAVY_1C_GREAT_POWER_NAVAL_LAWS.md`;
- `PHASE_NAVY_3C_2_BIC_NAVAL_DECISION.md`;
- les `Changelog.txt` complets du fork et de la source hotfix;
- les définitions, localisations, icône, historiques pays, relations de sujet
  et journal entry directement pertinents dans les trois arbres.

Le changelog source annonce explicitement :
`Navigation Acts (Britain and it's colonies)`. Cette annonce établit
l'intention hotfix, mais pas la validité de chaque activation concrète.

## 4. CSV : parse intégral et structure

Les CSV ont été chargés par `Import-Csv`, pas découpés par séparateur texte.
Une cellule structurelle nulle est une propriété absente ou `$null` après
parsing; une chaîne vide dans une colonne optionnelle est comptée séparément.

| CSV | Lignes de données | Colonnes | Cellules structurelles nulles | Cellules optionnelles vides |
| --- | ---: | ---: | ---: | ---: |
| `HOTFIX_MERGE_BLOCK_STATUS.csv` | 38 | 17 | 0 | 20 |
| `HOTFIX_REPORT_INDEX.csv` | 124 | 22 | 0 | 262 |
| `HOTFIX_MERGE_THREE_WAY_INVENTORY.csv` | 541 | 21 | 0 | 341 |
| `HOTFIX_GLOBAL_DIFFERENCE_INVENTORY.csv` | 534 | 22 | 0 | 314 |
| `HOTFIX_MERGE_REMAINING_WORK.csv` | 512 | 20 | 0 | 511 |

Ces dimensions décrivent la première lecture, avant écriture. Après ajout de
la ligne 6A.14R, `HOTFIX_REPORT_INDEX.csv` contient 125 lignes de données,
22 colonnes, 0 cellule structurelle nulle et 265 cellules optionnelles vides.
`HOTFIX_MERGE_BLOCK_STATUS.csv` reste à 38 × 17, avec 0 cellule structurelle
nulle et 20 cellules optionnelles vides.

En-têtes :

```txt
HOTFIX_MERGE_BLOCK_STATUS.csv
block_id | block_name | region | scope | status | files_total |
files_merged | files_pending | static_validation | runtime_validation |
canonical_report | canonical_commit | next_action | priority | merge_blocker |
post_merge_only | notes

HOTFIX_REPORT_INDEX.csv
phase_id | filename | title | region | topic | document_type |
primary_verdict | secondary_verdicts | historical_status | canonical |
superseded_by | predecessor | successor | markdown_path |
companion_csv_path | commit | created_or_recorded_date | runtime_or_static |
gameplay_changed | current_relevance | summary | notes

HOTFIX_MERGE_THREE_WAY_INVENTORY.csv
relative_path | present_in_fork | present_in_hotfix | present_in_vanilla |
size_fork | size_hotfix | size_vanilla | sha256_fork | sha256_hotfix |
sha256_vanilla | file_domain | region | feature | difference_type |
merge_status | intentional_local_preservation | runtime_validation_status |
recommended_action | priority | evidence | notes

HOTFIX_GLOBAL_DIFFERENCE_INVENTORY.csv
relative_path | present_in_fork | present_in_hotfix | present_in_vanilla |
size_fork | size_hotfix | size_vanilla | sha256_fork | sha256_hotfix |
sha256_vanilla | region | feature | file_domain | difference_type |
merge_status | intentional_fork_divergence | vanilla_1_13_adaptation |
runtime_validation_status | recommended_action | priority | evidence | notes

HOTFIX_MERGE_REMAINING_WORK.csv
relative_path | region | feature | file_domain | fork_status | hotfix_status |
vanilla_status | difference_type | merge_status |
intentional_fork_divergence | validated_static | validated_runtime |
protected_concurrent_work | required_for_merge | priority | recommended_phase |
recommended_action | evidence_report | evidence_commit | notes
```

Les lignes directement liées par leur contenu à Navigation Acts, GBR ou HBC
sont :

- une ligne `REMAINING_THREE_WAY_REVIEW` dans la matrice des blocs;
- six lignes historiques dans l'index des rapports, dont
  `HOTFIX_2_LAWS_MERCHANT_BANKING_NAVIGATION_ACTS` et 6A.13;
- quatre lignes dans chacun des trois inventaires globaux : BIC, GBR,
  `hbc - hudson...` et `06_usa_independence_mod.txt`.

Les inventaires ne contiennent aucune ligne pour NBS, ONT, ORA ni
`hbc - hubson...`, bien que la comparaison directe courante prouve leur
pertinence. Ils sont donc incomplets pour ce sous-périmètre précis et ne
peuvent pas remplacer la recherche trois voies directe.

## 5. Méthode de recherche

La méthode reproductible a été :

1. recherche récursive, par fichiers texte fonctionnels, de
   `law_navigation_acts`, `law_mercantilism_navigation_acts`,
   `navigation_acts`, `c:GBR` et `c:HBC`;
2. inventaire des fichiers d'histoire commençant par GBR, HBC, NBS, ONT, ORA
   et BIC;
3. recherche des définitions de tags, propriétaires d'États et pactes de
   sujet au départ;
4. extraction des lignes `activate_law` dans les trois arbres;
5. SHA-256 direct des fichiers candidats;
6. `git diff --no-index --ignore-cr-at-eol` pour compter les hunks et lignes
   du diff complet fork vers source et fork vers vanilla;
7. contrôle de la syntaxe de loi et des modificateurs contre les fichiers
   vanilla 1.13.

Les recherches dans le fork ont exclu `bject` et
`docs/research/technology/**`. Le stash n'a jamais été ouvert.

Résultats bruts utiles :

| Racine | lignes `c:GBR` | lignes `c:HBC` | lignes Navigation Acts |
| --- | ---: | ---: | ---: |
| Fork | 644 | 23 | 6 |
| Source hotfix | 682 | 23 | 12 |
| Vanilla 1.13 | 1160 | 28 | 0 |

Ces nombres bruts incluent des usages étrangers à la loi. La liste
fonctionnelle filtrée figure dans les sections suivantes.

## 6. Infrastructure de la loi

### 6.1 Identifiant exact

L'identifiant littéral `law_navigation_acts` n'est défini dans aucun des trois
arbres. L'identifiant réellement livré par le hotfix et intégré au fork est :

`law_mercantilism_navigation_acts`

Il est défini dans :

`common/laws/00_inject_laws.txt`

### 6.2 Groupe, parent et compatibilité

| Propriété | Valeur |
| --- | --- |
| Groupe | `lawgroup_trade_policy` |
| Parent | `law_mercantilism` |
| Technologie | `international_trade` |
| Icône | `gfx/interface/icons/law_icons/regulation_acts.dds` |
| `can_enact` | `always = yes` |
| Visibilité GBR | directe |
| Visibilité sujets | seulement `colony` ou `personal_union`, si GBR a la loi |

Le groupe, la technologie, la forme `parent`, les triggers, la pondération IA
et chacun des modificateurs utilisés ont des équivalents syntaxiques dans
vanilla 1.13. Les sept historiques pays examinés reçoivent le tier
technologique 4, et `international_trade` est une technologie d'ère 1.

La définition est donc **syntaxiquement compatible 1.13**, mais sa visibilité
est **fonctionnellement incomplète** pour le périmètre annoncé :

- HBC est `chartered_company`, type non accepté par `is_visible`;
- BIC est `chartered_company`, type non accepté par `is_visible`;
- ORA n'est pas sujet britannique;
- NBS et ONT sont des `colony` et satisfont le type, à condition que GBR ait
  déjà la loi;
- GBR satisfait directement la visibilité.

Une activation initiale peut être forcée par l'histoire, mais l'audit ne
dispose d'aucune preuve statique que l'interface, l'enactabilité et la
validation restent cohérentes pour une loi invisible. Cette réserve empêche
de déclarer les activations HBC, BIC et ORA compatibles.

### 6.3 Icône et localisations

| Élément | Fork | Source | Vanilla | Verdict |
| --- | --- | --- | --- | --- |
| Loi dans `00_inject_laws.txt` | présente, `FFD9C1079D5676306BA13B9C8FFAA0CEE42BDB6E774B4FB80FD69FABAEFB6BD5` | présente, `44553777A40020C885A3638D6BC2B6D1DDA998DDC651E1FC39A7A51EC830CDF0` | fichier absent | bloc ciblé déjà fusionné |
| `regulation_acts.dds` | `271A648E905522551CB6C86B5557A94DF679D5E956668B25D1CC0789D347E19F`, 485828 octets, magic `DDS ` | hash identique | absent | intégré |
| Localisation anglaise | `hotfix_laws_l_english.yml`, `05E3C39A068BC81FDCA5510AFE4B87D854A0ADC42F618AB6F92D285041BC4FD1` | clés dans `mod_v2content_l_english.yml`, fichier `A0A21C60581E16E3E1ED1F2B74B33A252D6841943DA1319B1C677698F4525B52` | absente | intégrée |
| Localisation française | `hotfix_laws_l_french.yml`, `F6B3B6A92046F5C08793237211A16EFDBABC709EEFDD4E89F4401969C0A8C003` | absente | absente | intégrée localement |

Les textes anglais « Navigation Acts » et français « Actes de navigation »
existent. Le bloc de loi ciblé et l'icône sont identiques à la source; les
différences de hash du fichier de loi proviennent d'autres blocs locaux et
hotfix. L'infrastructure est classée `ALREADY_MERGED` et ne doit pas être
modifiée.

## 7. Inventaire exhaustif des activations

### 7.1 Fork

Le fork ne contient aucune activation de
`law_mercantilism_navigation_acts`. Les cinq historiques théoriques et BIC
utilisent `law_mercantilism` ou aucune loi commerciale explicite; la journal
entry américaine ne réactive aucune loi commerciale en cas d'échec.

### 7.2 Source hotfix

La source contient exactement sept activations fonctionnelles :

| Fichier | Objet ou effet | Nature |
| --- | --- | --- |
| `gbr - great britain.txt:53` | `c:GBR` | loi initiale |
| `hbc - hudson bay company.txt:13` | `c:HBC` | loi initiale |
| `nbs - new brunswick.txt:18` | `c:NBS` | loi initiale |
| `ont - ontario.txt:18` | `c:ONT` | loi initiale |
| `ora - oranje.txt:13` | `c:ORA` | loi initiale |
| `bic - british east india company.txt:27` | `c:BIC` | loi initiale |
| `06_usa_independence_mod.txt:76` | `je_usa_independence_mod.on_fail` | effet événementiel |

La septième activation est exécutée sur le pays de la journal entry après
l'échec de la guerre d'indépendance; elle ne constitue pas une loi de départ.

### 7.3 Vanilla 1.13

Vanilla ne définit ni la loi ni aucune activation. Ses lois commerciales de
référence sont :

| Pays | Vanilla 1.13 |
| --- | --- |
| GBR | `law_protectionism` |
| HBC | `law_mercantilism` |
| NBS | `law_mercantilism` |
| ONT | `law_mercantilism` |
| ORA | `law_mercantilism` |
| BIC | aucune activation commerciale explicite |

La divergence source/vanilla est donc une intention custom du hotfix, pas une
adaptation exigée par Victoria 3 1.13.

## 8. Tags, chargement et cohérence 1776

| Tag | Définition disponible au montage | Territoire au départ dans le fork | Relation GBR | Cohérence de l'activation source |
| --- | --- | --- | --- | --- |
| GBR | fork `00_countries.txt` | oui | souverain | historiquement plausible |
| HBC | fork `00_countries.txt` | oui, plusieurs États | `chartered_company` | plausible historiquement, invisible avec le trigger actuel |
| NBS | fork `00_countries.txt` | oui | `colony` | Navigation Acts plausible pour le territoire, tag « New Brunswick » anachronique avant 1784 |
| ONT | fork `00_countries.txt` | oui | `colony` | Navigation Acts plausible pour le territoire, « Upper Canada/Ontario » anachronique avant 1791 |
| ORA | définition vanilla `01_africa.txt` | oui dans le fork | aucune sujétion britannique | incohérente et invisible; l'État libre d'Orange est postérieur à 1776 |
| BIC | fork `00_countries.txt` | oui | `chartered_company` | protégée, invisible avec le trigger actuel |

Chaque historique ciblé se trouve dans `common/history/countries`, enveloppé
par `COUNTRIES = { c:TAG ?= { ... } }`, et le tag possède un pays territorial
au départ. Les histoires sont donc des entrées de chargement réelles, sous
réserve du conflit HBC détaillé ci-dessous.

NBS et ONT sont des représentations anachroniques déjà assumées par le setup
1776 du fork. Cela ne suffit pas à rejeter Navigation Acts pour leur
territoire, mais empêche de présenter la substitution comme une simple
convergence vanilla 1.13.

## 9. GBR et collision NAVY

Dans le fork, GBR commence avec :

- `law_mercantilism` dans `lawgroup_trade_policy`;
- `law_professional_navy` dans `lawgroup_navy_model`.

La source commence avec :

- `law_mercantilism_navigation_acts`;
- `law_professional_navy`, déplacée de la ligne 58 à la ligne 62 sans
  changement d'identifiant.

Vanilla 1.13 commence avec :

- `law_protectionism`;
- `law_professional_navy`.

Navigation Acts appartient à `lawgroup_trade_policy`, tandis que
`law_professional_navy` et `law_merchant_navy` appartiennent à
`lawgroup_navy_model`. Il n'existe donc **aucun conflit de groupe de lois** :
la substitution commerciale ne désactive pas juridiquement une loi navale.

Il existe néanmoins une collision de fichier et de hunk :

- `gbr - great britain.txt` est le fichier gameplay modifié et validé par
  `PHASE_NAVY_1C_GREAT_POWER_NAVAL_LAWS`;
- le diff complet fork/source forme un seul hunk `2+/2-` qui mélange la
  substitution commerciale et le déplacement de
  `law_professional_navy`;
- l'inventaire trois voies classe déjà GBR `CONCURRENT_USER_WORK` et demande
  de préserver le fork;
- aucune égalité source ne permet un remplacement complet.

Le delta GBR est donc classé `PROTECTED_CONCURRENT_WORK`. L'audit n'a ni
absorbé ni modifié le hunk NAVY.

## 10. Double définition HBC

### 10.1 Définition `hubson`

| Propriété | Valeur |
| --- | --- |
| Chemin fork | `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork\common\history\countries\hbc - hubson bay company.txt` |
| Chemin source | `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source\common\history\countries\hbc - hubson bay company.txt` |
| Vanilla | absent |
| Type | histoire pays custom, nom de fichier mal orthographié |
| Objet | `COUNTRIES/c:HBC` |
| SHA-256 fork/source | `C88CB029FA2A0A32C549A6EA0A54802D614E5ED46DFADE4C0083F055826DE154` |
| Loi commerciale | `law_mercantilism` |
| Autres lois notables | `state_religion`, `law_cultural_exclusion`, `law_extraction_economy`, `law_slave_trade`, etc. |
| Autres effets | industrialists/landowners au pouvoir, politique conservatrice, écoles 1, colonial affairs 1 |
| Statut | actif comme entrée de fichier, mais rôle final incertain |

Le fichier est identique dans le fork et la source et provient de l'import
initial du fork. Il n'existe pas dans vanilla ni dans les trois inventaires
globaux.

### 10.2 Définition `hudson`

| Propriété | Valeur |
| --- | --- |
| Chemin fork | `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork\common\history\countries\hbc - hudson bay company.txt` |
| Chemin source | `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source\common\history\countries\hbc - hudson bay company.txt` |
| Chemin vanilla | `C:\Games\Victoria 3 The Great Wave\game\common\history\countries\hbc - hudson bay company.txt` |
| Type | histoire pays au nom canonique vanilla |
| Objet | `COUNTRIES/c:HBC` |
| SHA fork | `35377A3E896833E6DC9784440CDECBC3C8489043149C7B250EB5DF395FB9CC4F` |
| SHA source | `8D0C3B40CF258B97BD322DA6FDC1EE940AB523B28574ED4005D9180A89A1CD84` |
| SHA vanilla | `776EDBD71F79D43CB77459CB9FFE522967FAE5382EF6844BE7D9F8EA2B2CFE40` |
| Loi commerciale | fork/vanilla `law_mercantilism`; source Navigation Acts |
| Autres lois notables | séparation totale, ségrégation raciale, interventionnisme |
| Autres effets | technologie `mandatory_service`, colonial affairs 2, taxe sur le grain |
| Statut | actif comme entrée de fichier, candidat hotfix direct, rôle final incertain |

Fork et source ne diffèrent ici que par la loi commerciale (`1+/1-`).
Vanilla porte la même loi commerciale que le fork, mais un tier technologique
et une enveloppe d'effets différents.

### 10.3 Ordre et pertinence effective

Faits :

- les deux fichiers sont présents dans le fork monté et ciblent exactement
  `c:HBC`;
- ils activent des lois concurrentes dans plusieurs groupes;
- `hubson` est trié lexicalement avant `hudson`;
- aucun fichier vanilla ne peut supprimer l'un des deux fichiers à l'intérieur
  du même arbre de mod;
- l'inventaire courant ne connaît que `hudson`.

Inférence :

- si le moteur suit l'ordre lexical des noms dans ce dossier,
  `hudson` serait traité après `hubson`.

Incertitude :

- aucune documentation moteur suivie ni preuve runtime autorisée par 6A.14R
  n'établit l'ordre de traitement, la fusion ou la priorité finale des deux
  blocs `c:HBC`;
- l'opérateur `?=` est utilisé par les deux blocs et ne transforme pas les
  deux fichiers en deux tags distincts;
- il est impossible de prouver statiquement laquelle des lois concurrentes
  est finalement active.

Conclusion : **les deux fichiers sont fonctionnellement pertinents**, mais
aucun ne peut être déclaré définition active unique. `hudson` est le candidat
hotfix direct; `hubson` est une définition custom concurrente qui peut
modifier ou masquer le résultat. Le conflit n'est ni supprimé ni fusionné.

## 11. Tableau trois voies des fichiers candidats

Les compteurs de hunks et de lignes portent sur le diff complet
fork → source, avec CR ignoré en fin de ligne. Les deltas Navigation Acts
ciblés sont plus petits lorsque des différences adjacentes existent.

| Fichier relatif | Fork : présence / SHA-256 | Source : présence / SHA-256 | Vanilla : présence / SHA-256 | Objets | Diff fork→source | Classification | Risque / protection | Recommandation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `common/history/countries/gbr - great britain.txt` | oui `529BAC14E5A32410ACB6E122B9F30273E2C40C32611316E6A0D925E0594E2429` | oui `A3048265212C95CBC931ED2F07E057749C00A24C716AF0559A760B341883B7ED` | oui `D31CFDEB7537C22EF5B980DB5E1399B56BDDD0E89A653409EE86A550DC406E6B` | `c:GBR` | 1 hunk, `2+/2-` | `PROTECTED_CONCURRENT_WORK` | NAVY, `law_professional_navy` dans le même hunk | ne pas modifier |
| `common/history/countries/hbc - hudson bay company.txt` | oui `35377A3E896833E6DC9784440CDECBC3C8489043149C7B250EB5DF395FB9CC4F` | oui `8D0C3B40CF258B97BD322DA6FDC1EE940AB523B28574ED4005D9180A89A1CD84` | oui `776EDBD71F79D43CB77459CB9FFE522967FAE5382EF6844BE7D9F8EA2B2CFE40` | `c:HBC` | 1 hunk, `1+/1-` | `UNKNOWN_REQUIRES_REVIEW` | doublon HBC, visibilité incompatible `chartered_company` | bloquer tout alignement |
| `common/history/countries/hbc - hubson bay company.txt` | oui `C88CB029FA2A0A32C549A6EA0A54802D614E5ED46DFADE4C0083F055826DE154` | oui, hash identique | absent | `c:HBC` | 0 hunk | `UNKNOWN_REQUIRES_REVIEW` | définition concurrente et divergente | audit dédié du doublon avant toute loi |
| `common/history/countries/nbs - new brunswick.txt` | oui `8B25277D1227C1D6039BD32AB280E87A714BB2AA747DD731839FA8A554303D65` | oui `92B80CA4C4C18E3AF55E073D8A30AF2ED9A7461C44E5F61A9E4B95DA6E086747` | oui `5EA59501BEA86637DB83D2A2446842A53CCD44D6637169D1B88D32855B8B3D08` | `c:NBS` | 1 hunk, `1+/1-` | `REQUIRED_HOTFIX_DELTA` | delta borné, mais dépend de GBR et tag anachronique | conserver comme sous-delta prouvé, ne pas exécuter isolément |
| `common/history/countries/ont - ontario.txt` | oui `DC8CD2B377378D35FF1C018214EFF13FB217B3416B075ECFEE58306AD4E45A4A` | oui `06CE1BB96A4ACB77ACDEE03A9AF57B603DEFBCC3F7B867B1A392E32460343C26` | oui `56EBC935916927F20451453F219A3538F521D4CC737CE711C4224E804D9F36E6` | `c:ONT` | 1 hunk, `1+/1-` | `REQUIRED_HOTFIX_DELTA` | delta borné, mais dépend de GBR et tag anachronique | conserver comme sous-delta prouvé, ne pas exécuter isolément |
| `common/history/countries/ora - oranje.txt` | oui `3D4060CBE2D3A438D28B12569ADF10CE13352A490B7D7A4C0EC6C199E8632C14` | oui `5E259DD6E2A3FB4196BC7ADA92E7FA65D801A949450083A9ACF493240DC9864F` | oui `A8B60AC0892EA9A92F4C58EBF2DBEC5F3BC9FF979666E72491D8D1E1C7BAADC7` | `c:ORA` | 1 hunk, `1+/1-` | `OBSOLETE_HOTFIX_CONTENT` | ni sujet britannique ni visible, incohérent en 1776 | rejeter l'activation source |
| `common/history/countries/bic - british east india company.txt` | oui `37B836DBE9A273F1202B592533EB8C851B3657DBB63422F50AE11021437F580C` | oui `A11AE6BBD0E663336BB3E4282E18584543F9EDF332A97BAAD1D93DB112FE30A1` | oui `7C28DA10ED769885002244AB2279AB2B0CF828D2538B0D15F71E1C9D73607C3F` | `c:BIC` | 2 hunks, `2+/1-` | `PROTECTED_CONCURRENT_WORK` | Inde/BIC close; source réintroduit aussi `law_colonial_exploitation`; visibilité incompatible | préserver le fork et `law_frontier_colonization` |
| `common/journal_entries/06_usa_independence_mod.txt` | oui `FC2EF9E593D1DAB1910EB28896467D1CD74623C48950BB0FF76730418C02310D` | oui `B67AA92DE0515228FB709FB8782591664604123CD2DE42C33593875DFF1593BF` | absent | `je_usa_independence_mod.on_fail` | 3 hunks, `5+/1-` | `PROTECTED_CONCURRENT_WORK` | Révolution américaine protégée; autres différences adjacentes | ne pas rouvrir |

Chemins source et vanilla : les chemins relatifs ci-dessus sont résolus sous
les racines absolues publiées au préflight. Pour `hubson` et la journal entry,
le chemin vanilla correspondant est absent.

## 12. Forme détaillée des deltas

| Candidat | Delta Navigation Acts ciblé | Différences adjacentes |
| --- | --- | --- |
| GBR | `law_mercantilism` → Navigation Acts | déplacement sans effet de `law_professional_navy` |
| HBC `hudson` | même substitution | aucune autre différence fork/source |
| HBC `hubson` | aucune | définition complète concurrente |
| NBS | même substitution | aucune autre différence fork/source |
| ONT | même substitution | aucune autre différence fork/source |
| ORA | même substitution | aucune autre différence fork/source |
| BIC | ajout de Navigation Acts | `law_frontier_colonization` → `law_colonial_exploitation` dans la source |
| USA JE | ajout dans `on_fail` | événement français commenté et autres écarts dans trois hunks |

Le candidat théorique « cinq fichiers, cinq objets, cinq hunks, 5+/5- » est
donc uniquement le sous-ensemble publié par 6A.13. La recherche exhaustive
donne six activations de départ, une activation événementielle et une
définition HBC concurrente. Un remplacement complet est interdit pour chacun.

## 13. Classifications consolidées

| Delta ou infrastructure | Classification unique |
| --- | --- |
| Définition de loi | `ALREADY_MERGED` |
| Icône | `ALREADY_MERGED` |
| Localisation anglaise | `ALREADY_MERGED` |
| Localisation française | `ALREADY_MERGED` |
| GBR | `PROTECTED_CONCURRENT_WORK` |
| HBC `hudson` | `UNKNOWN_REQUIRES_REVIEW` |
| HBC `hubson` | `UNKNOWN_REQUIRES_REVIEW` |
| NBS | `REQUIRED_HOTFIX_DELTA` |
| ONT | `REQUIRED_HOTFIX_DELTA` |
| ORA | `OBSOLETE_HOTFIX_CONTENT` |
| BIC | `PROTECTED_CONCURRENT_WORK` |
| Échec de l'indépendance américaine | `PROTECTED_CONCURRENT_WORK` |

La divergence globale ne peut pas être classée
`VANILLA_1_13_ALIGNMENT_REQUIRED` : vanilla ne fournit pas cette loi. Elle ne
peut pas non plus être classée globalement `REQUIRED_HOTFIX_DELTA`, car trois
activations source sont invalides ou ambiguës et trois fichiers sont protégés.

## 14. Faits, inférences et incertitudes

### Faits observés

- l'infrastructure est présente et syntaxiquement 1.13;
- la source annonce Britain and its colonies;
- le fork n'active la loi nulle part;
- la source possède sept activations, dont six initiales;
- vanilla ne connaît pas la loi;
- HBC possède deux histoires concurrentes;
- HBC et BIC sont `chartered_company`, non admises par le trigger de
  visibilité;
- ORA n'est pas sujet britannique;
- GBR contient la loi NAVY protégée ajoutée par NAVY-1C;
- BIC conserve `law_frontier_colonization`.

### Inférences

- Navigation Acts est historiquement plausible pour GBR et les territoires
  britanniques nord-américains en 1776;
- le changement ORA ressemble à un remplacement hotfix trop large de
  `law_mercantilism`;
- `hudson` serait probablement traité après `hubson` sous un tri lexical.

### Incertitudes

- ordre et sémantique exacts de deux blocs HBC concurrents;
- comportement interface/validation d'une loi initiale invisible;
- intention précise derrière l'ajout événementiel américain;
- décision de design sur les tags NBS/ONT anachroniques.

### Fichiers protégés non inspectés

- contenu de `bject`;
- contenu des sept fichiers de `docs/research/technology/`;
- contenu du stash NAVY-3C-3.

## 15. Décision sur 6A.14F

Les conditions cumulatives d'une future correction ne sont pas remplies :

| Condition | Résultat |
| --- | --- |
| Delta hotfix légitime | partiel seulement |
| Objet actif et unique | échec HBC |
| Compatibilité 1.13 | syntaxe PASS, visibilité fonctionnelle échec/indéterminée |
| Aucune collision NAVY | échec GBR |
| Aucune ambiguïté HBC | échec |
| Périmètre exact et minimal | échec du scope théorique de cinq |
| Hashes reproductibles | PASS |
| Rollback chirurgical | possible par sous-delta, pas pour le paquet sûr |
| Aucun remplacement complet | possible en théorie |

`HOTFIX_6A14F_NAVIGATION_ACTS_STARTING_LAW_ALIGNMENT` n'est donc pas
sélectionnée. Une instruction future devrait d'abord autoriser un audit
spécifique du doublon HBC et une décision de design sur la visibilité des
`chartered_company`; elle ne devrait pas appliquer de loi pendant cet audit.

## 16. Contrôles de non-régression

| Contrôle | Résultat |
| --- | --- |
| Branche finale | `hotfix-dlc-audit`, inchangée |
| HEAD final | `382a2b51b788e181228187c417e59fc052ed303d`, inchangé |
| Message HEAD | inchangé |
| Index staged | vide |
| Hash stash après | `518df704fa14599c0f254fae13859210663dd976` |
| Stash ligne exacte | inchangée |
| GEN | `7FC780AB8A8793E1DD1B3E6A32022807CED720FB1BE3F3D63D9EC6FDE9F43327` |
| VEN | `51A65341A2E3947A3D7D71BC3E3B1F31DA5CCD9D000D200C75BFB9570010B6DB` |
| BIC | `37B836DBE9A273F1202B592533EB8C851B3657DBB63422F50AE11021437F580C` |
| BIC `law_frontier_colonization` | conservée |
| `law_colonial_exploitation` restaurée dans BIC | non |
| Fichiers NAVY/BIC/ADMIN/MARATH gameplay modifiés | 0 |
| Fichiers gameplay modifiés | 0 |
| Runtime lancé | non |
| `git diff --check` | PASS |

`bject` et les sept fichiers technologiques restent présents sous les mêmes
chemins non suivis. Aucun outil de cette phase ne les a ouverts ou écrits.
Cette non-interaction, le statut Git initial/final identique et l'absence de
commande de modification constituent la vérification autorisée; aucun nouveau
hash de contenu n'est prétendu.

## 17. Documentation écrite

Les cinq seuls documents créés ou modifiés sont :

1. ce rapport;
2. `docs/reports/hotfix/INDEX.md`;
3. `docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv`;
4. `docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv`;
5. `docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md`.

`HOTFIX_NEXT_MERGE_PHASE_PROMPT.md` reste inchangé, car aucune phase
corrective n'est sélectionnée.

## 18. État Git final

```txt
 M docs/reports/hotfix/INDEX.md
 M docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv
 M docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md
 M docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv
?? bject
?? docs/reports/hotfix/_index/HOTFIX_6A14R_NAVIGATION_ACTS_STARTING_LAW_AUDIT.md
?? docs/research/technology/TECH_TREE_BUILDING_AND_PRODUCTION_CANDIDATES.csv
?? docs/research/technology/TECH_TREE_INDUSTRIAL_CHAINS.md
?? docs/research/technology/TECH_TREE_INDUSTRIAL_HISTORY_DEEP_RESEARCH.md
?? docs/research/technology/TECH_TREE_INDUSTRIAL_INNOVATIONS_DATABASE.csv
?? docs/research/technology/TECH_TREE_RESEARCH_BIBLIOGRAPHY.md
?? docs/research/technology/TECH_TREE_RESOURCE_CANDIDATES.csv
?? docs/research/technology/TECH_TREE_VICTORIA3_GAP_ANALYSIS.md
```

## 19. Rollback documentaire

Le rollback de 6A.14R est uniquement documentaire :

1. supprimer ce nouveau rapport;
2. retirer sa ligne de `HOTFIX_REPORT_INDEX.csv`;
3. retirer son lien de `docs/reports/hotfix/INDEX.md`;
4. restaurer manuellement la ligne `REMAINING_THREE_WAY_REVIEW` antérieure;
5. retirer les paragraphes 6A.14R ajoutés à la roadmap.

Ne pas utiliser `git restore`, `git checkout`, `git reset` ou une copie
complète. Aucun rollback gameplay n'existe, puisque le gameplay n'a pas
changé.

## 20. Verdicts finaux

```txt
HOTFIX_6A14R_NAVIGATION_ACTS_STARTING_LAW_AUDIT_COMPLETE
NAVIGATION_ACTS_FIVE_FILE_THEORETICAL_SCOPE_RESOLVED
GBR_NAVY_COLLISION_AUDITED
HBC_DOUBLE_DEFINITION_AUDITED
NO_GAMEPLAY_CHANGED
NO_RUNTIME_REQUIRED
NO_AUTOMATIC_COMMIT
STASH_NAVY_3C_3_INTACT
NAVIGATION_ACTS_STARTING_LAW_BLOCKED_BY_HBC_DEFINITION_CONFLICT
NO_NEXT_EXECUTION_PHASE_SELECTED
```
