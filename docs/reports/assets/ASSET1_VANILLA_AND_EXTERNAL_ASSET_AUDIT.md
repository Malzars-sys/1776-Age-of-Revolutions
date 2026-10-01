# ASSET PASS 1 — Audit des icônes Vanilla et des mods externes

Projet : 1776 — Age of Revolutions, version 2.4.0 Beta.
Cible : Victoria 3 1.13.11 (version du `C:/Games/Victoria 3/binaries/victoria3.exe` contrôlée localement).
Source du fork : working tree local, pas GitHub.
Nature : **audit uniquement** ; aucun asset, script, texte de localisation ou fichier GFX n'a été modifié par cette passe.

## Résultat à retenir

Le fork contient 291 définitions technologiques, dont 242 recherchables et 49 non recherchables. Parmi les 242 recherchables, 103 utilisent encore `gfx/error_manul.dds` (101) ou `gfx/error_deer.dds` (2). Les 178 technologies Vanilla sont toujours définies par identifiant dans le fork : 42 sont désormais non recherchables et servent d'alias de compatibilité. Leurs 42 textures sont potentiellement réaffectables dans le nouvel arbre, mais cinq restent utilisées ailleurs dans l'interface du fork. Le vivier sans cet autre usage est donc de **37 icônes**.

L'audit visuel/sémantique a retenu **5 correspondances EXCELLENT** et **11 GOOD**. Ce sont des propositions, pas des changements réalisés. Si ces 16 affectations sont retenues sans conflit, **87 technologies recherchables** ayant actuellement un placeholder restent à illustrer. Trois autres technologies ont une icône distincte copiée de Tech & Res : leur adéquation visuelle est bonne, mais leur statut de redistribution n'est pas établi.

## 1. Technologies Vanilla analysées

- 178 définitions dans `C:/Games/Victoria 3/game/common/technology/technologies/` ; 178 textures résolues et présentes dans `C:/Games/Victoria 3/game/gfx/`.
- 178 chemins de texture différents et aucun doublon binaire SHA-256 parmi les 178 fichiers.
- Une technologie est `STILL_ACTIVE_SAME_ROLE` selon les champs comparés (ID, catégorie, ère, texture et prérequis) ; 135 sont `STILL_ACTIVE_REWORKED` ; 42 sont `COMPATIBILITY_ONLY`. Aucun ID Vanilla n'a complètement disparu du fork.
- Les 42 alias ont `can_research = no` ; le classement `COMPATIBILITY_ONLY` a priorité sur « remplacée » dans le CSV. Plusieurs rôles sont effectivement assumés par de nouveaux nœuds, mais l'identifiant ancien existe toujours. Ainsi `REPLACED_BY_NEW_TECH` et `NOT_PRESENT_IN_FORK` valent zéro en tant que classes mutuellement exclusives, sans nier les remplacements conceptuels.
- L'inventaire complet, avec les chemins des définitions, textures, autres références et statut de réutilisation, est dans `ASSET1_VANILLA_TECH_ICON_INVENTORY.csv`.

## 2. Icônes Vanilla libérées, occupées ou à contrôler

| État | Nombre | Interprétation |
| --- | ---: | --- |
| `CURRENTLY_USED` | 136 | La texture figure sur une technologie encore recherchable ; la conserver pour ce rôle. |
| `USED_BY_OTHER_OBJECT` | 5 | Ancienne technologie non recherchable, mais texture visible dans un autre objet du fork. |
| `FREE_FROM_REMOVED_TECH` | 37 | Ancien ID conservé comme alias non recherchable, aucun autre emploi littéral trouvé. |

Les cinq textures encore reprises par un autre objet sont `manufacturies.dds`, `prospecting_tech.dds`, `mandatory_service.dds`, `bureaucracy.dds` et `academia.dds` : elles figurent dans des journal entries. « Libre » ne signifie donc pas « absent des fichiers » : les alias non recherchables gardent leur référence à l'ancienne texture. Toute réaffectation doit encore tester la présentation en jeu. Les références ont été cherchées dans les fichiers texte, GUI, GFX et événements du fork et de la Vanilla, par chemin DDS littéral ; les références calculées ou injectées par moteur ne peuvent pas être exclues ici.

Pour ces fichiers Vanilla présents, le mode technique recommandé est `REFERENCE_VANILLA_DIRECTLY` / `COPY_NOT_NEEDED`. Il n'y a aucune raison démontrée de dupliquer leur DDS dans le mod. Les cinq cas utilisés par un autre objet restent à revoir pour éviter une confusion visuelle.

## 3. Nouvel arbre du fork : états visuels et doublons

`ASSET1_FORK_TECH_ICON_INVENTORY.csv` recense les 291 définitions, noms anglais et français, ère, catégorie, prérequis, texture et statut. Les grands déblocages y sont repris du rapport de nœuds existant ; ce champ est indicatif pour l'audit d'icônes et doit être revérifié contre les scripts courants avant une modification de gameplay. Le périmètre visuel de référence est **242 technologies recherchables** :

- 136 utilisent directement une icône Vanilla présente : `GOOD_VANILLA_REUSE`.
- 3 utilisent chacune une icône locale distincte dont le hash correspond exactement à Tech & Res : `alloysworking`, `bauxite_processing`, `bayer_process`. Elles sont visuellement distinctes, mais ne doivent pas être réputées juridiquement validées.
- 103 ont une texture d'erreur/placeholder. Les 7 autres placeholders dans les 49 alias non recherchables ne sont pas inclus dans ce total prioritaire.

Il y a deux doublons de chemin entre technologies recherchables : `gfx/error_manul.dds` partagé par 101 nœuds et `gfx/error_deer.dds` partagé par 2 nœuds. Ce partage est intentionnel comme solution provisoire mais classé `PLACEHOLDER_DUPLICATION`, et non comme réutilisation finale. Aucun autre chemin n'est partagé par des technologies recherchables. Détail : `ASSET1_ACTIVE_TECH_ICON_DUPLICATES.csv`.

La capture antérieure de « Aucune production de produits chimiques industriels » montre également une icône générique ; il s'agit d'une méthode de production et non d'une technologie. Elle est donc signalée pour la passe PM suivante, sans toucher à son icône ici.

## 4. Correspondances Vanilla proposées

Les 26 essais explicites et leurs critères `Historical_Fit`, `Semantic_Fit`, `Visual_Fit`, `Confusion_Risk` sont dans `ASSET1_VANILLA_TECH_REUSE_CANDIDATES.csv`. Les prévisualisations ont été lues en mémoire à partir des DDS d'origine ; aucune image n'a été enregistrée ou créée dans le dépôt.

### EXCELLENT (5)

| Nouvelle technologie | Ancienne icône Vanilla | Justification |
| --- | --- | --- |
| `precision_boring` | `lathe.dds` | Tour mécanique réellement compatible avec l'alésage de précision. |
| `enclosed_dock_systems` | `drydock.dds` | Cale sèche protégée, sujet exact. |
| `standardized_field_artillery` | `artillery.dds` | Canon de campagne clairement lisible. |
| `periodical_print_networks` | `mass_communication.dds` | Pile de journaux imprimés, adaptée à la presse périodique. |
| `regulated_small_arms` | `gunsmithing.dds` | Arme d'époque et éléments d'armurerie. |

### GOOD (11)

`coke_smelting → steelworking`, `scientific_fortification_siegecraft → centralization`, `light_infantry_tactics → military_drill`, `permanent_military_hospitals → triage`, `hydrographic_surveying → navigation`, `institutionalized_public_credit → power_of_the_purse`, `organized_financial_institutions → banking`, `systematic_population_registration → central_archives`, `national_sovereignty → democracy`, `professional_civil_policing → law_enforcement`, `organized_military_establishments → standing_army`. Ces images transmettent le bon objet ou une métaphore proche ; leurs nuances et risques de confusion sont décrits ligne par ligne dans le CSV.

### REVIEW et rejets

Sept rapprochements ne sont que `POSSIBLE`, notamment le compas/carte de `navigation.dds` pour la chronométrie marine (aucun chronomètre visible) et la cale sèche pour le système général des arsenaux (conflit avec le candidat plus exact « bassins fermés »). `academia.dds` est visuellement adéquat aux académies techniques, mais sert toujours dans un journal entry ; il n'est pas classé GOOD pour cette raison. Trois rapprochements sont `POOR` ou `REJECT` : les flacons de médicaments ne représentent pas les acides industriels ; des jeunes pousses ne représentent pas l'élevage ; des billets ne représentent pas la métrologie. Aucun de ces trois ne doit être implémenté.

Après les 16 propositions fortes, les **87 nœuds restants** ont une spécification de sujet, composition, éléments historiques à privilégier/éviter et priorité dans `ASSET1_TECH_ICONS_REMAINING_TO_CREATE.csv`. Les `POSSIBLE` y restent comptés comme « à créer ou à résoudre » tant qu'un humain n'a pas validé la réutilisation.

## 5. Mods externes inspectés

Neuf dossiers Workshop Victoria 3 sont installés sous `C:/Program Files (x86)/Steam/steamapps/workshop/content/529340/`. L'inspection a commencé par les métadonnées, descripteurs, familles `gfx` et les sous-arbres pertinents, sans traiter tous les fichiers de tous les mods comme des candidats :

| ID | Mod local | DDS trouvés | Décision pour cette passe |
| --- | --- | ---: | --- |
| 2880120246 | Basileia Romaion 1736 (local 1.5.1, métadonnées 1.14.*) | 1 038 | 8 icônes technologiques d'époque retenues sous réserve de permission. |
| 3227982912 | Kuromi's AI 7.5 | 0 | Référence système, pas de candidat visuel. |
| 3385002128 | Community Mod Framework 1.65.0 | 192 | Icônes d'interface/modificateurs, pas de shortlist XVIIIe–XIXe ici. |
| 3472248460 | [1.13] Tech & Res 1.6' | 1 579 | 24 fichiers ciblés, droits à clarifier. |
| 3617930953 | 1776 original 2.3.1 | 20 | Source du fork, traitée séparément des candidats externes. |
| 3715913236 | La Gabelle 1.0.2 | 12 | 12 fichiers liés au sel/Gabelle couverts par l'autorisation documentée. |
| 3734242682 | Shaped by the Land | 0 | Pas de candidat DDS. |
| 3780935876 | Age of revolution /Fork [Steam Build] 2.4.0 | 66 | Autre distribution du projet, pas une source tierce. |
| 3786344818 | News Events | 167 | Icônes d'événements ; pas de shortlist techno/économie d'époque. |

Les trois mods utiles au présent périmètre figurent dans `ASSET1_EXTERNAL_MOD_CANDIDATES.csv`. Leurs pages Workshop ont été consultées : [La Gabelle](https://steamcommunity.com/sharedfiles/filedetails/?id=3715913236), [Tech & Res](https://steamcommunity.com/sharedfiles/filedetails/?id=3472248460), [Basileia Romaion](https://steamcommunity.com/sharedfiles/filedetails/?id=2880120246). Les noms/auteurs publics viennent de ces pages ; les versions et fichiers viennent des installations locales. Aucune licence de redistribution explicite n'a été trouvée sur les pages consultées de Tech & Res et Basileia. Cela n'est pas une preuve qu'aucune permission n'existe ailleurs.
Le [dépôt GitHub public de Tech & Res](https://github.com/mattia2110/tech-and-res) lié par sa page Workshop a également été ouvert : aucun fichier de licence ne figure dans sa liste racine visible au moment de l'audit. Son caractère public n'autorise pas à lui seul la redistribution de ses images.

## 6. Droits, copies existantes et preuves techniques

`ASSET1_EXTERNAL_ASSET_FILE_EVIDENCE.csv` détaille **44 chemins externes à extension `.dds` ciblés** : chemin exact, dimensions, format réel, canal alpha, taille et SHA-256. Leur existence a été vérifiée, sans aucune modification. Répartition : 12 La Gabelle, 24 Tech & Res, 8 Basileia. Deux fichiers Tech & Res déjà copiés dans le fork — `pm_hall_heroult_process.dds` et `pm_no_aluminium_production.dds` — portent en réalité une signature PNG RGBA malgré leur extension `.dds` ; ils sont classés `NO_INVALID_DDS` dans les preuves. Leur affichage en jeu demande un contrôle distinct avant toute reprise, sans correction dans cette passe.

- **La Gabelle — `GRANTED`.** `docs/workshop/STEAM_WORKSHOP_CREDITS.md` consigne l'autorisation explicite de Tokugawa_Mori du 2026-08-28 (« Yes, just go ahead! ») et le crédit. Dix des 12 DDS du paquet ont une copie locale strictement identique par SHA-256 ; les deux autres (`company_groupe_salins.dds`, `gabelle.dds`) ne sont pas présents sous le même chemin dans le fork. Aucune nouvelle demande n'est nécessaire pour les usages couverts par cet accord.
- **Tech & Res — `PERMISSION_REQUIRED`.** Vingt-deux DDS externes ont déjà un équivalent binaire exact dans le fork, correspondant à **23 fichiers locaux** car `building_alloys_plant.dds` y existe sous deux noms. Deux autres fichiers précis sont intéressants mais non copiés dans les résultats de comparaison : `building_pharmaceuticals_industry.dds` et `pm_handcraft_natural_medicinals.dds`. Les 24 fichiers ciblés demandent une clarification écrite du droit de redistribution. La page Workshop attribue certains morceaux de Tech & Res à d'autres mods ; Mattia10 doit aussi confirmer la provenance des fichiers visés. Le crédit Tech & Res est absent du fichier `docs/workshop/STEAM_WORKSHOP_CREDITS.md` inspecté.
- **Basileia — `PERMISSION_REQUIRED`.** Huit icônes technologiques pertinentes pour la période ont été vérifiées techniquement. Aucun hash identique n'a été détecté dans les fichiers locaux examinés. La page Workshop présente Alexedishi, Drogan et Smekens, sans permission de réutilisation explicite trouvée. L'installation locale se déclare en 1.14.* même si la page mentionne un support 1.13/1.14 : aucune compatibilité en jeu n'est présumée.
- **Vanilla.** Les DDS présents dans le jeu installé doivent être référencés directement ; une copie dans le mod n'est pas techniquement justifiée pour les 26 propositions évaluées.

L'existence de copies Tech & Res antérieures à cette passe est un **risque de publication existant**, pas une copie effectuée ici. Il ne faut pas présenter `EXTERNAL ASSETS COPIED = 0` comme si le dépôt n'en contenait aucun : ce zéro ne vaut que pour cette intervention. L'autorisation du fork original ne doit pas être étendue par supposition aux tiers Tech & Res ou Basileia. Tant que les réponses ne sont pas reçues, les fichiers concernés sont `DO_NOT_COPY` et la redistribution existante reste à clarifier avec le mainteneur.

## 7. Brouillons et suite recommandée

Deux brouillons anglais non envoyés sont dans `ASSET1_PERMISSION_REQUEST_DRAFTS.md` : un à Mattia10 pour 24 chemins précis, incluant la régularisation des 22 copies identiques déjà présentes ; un à l'équipe Basileia pour huit icônes. Il n'y a aucun brouillon La Gabelle, son accord étant déjà documenté.

Pour **ASSET PASS 2** :

1. Obtenir ou vérifier par écrit les droits Tech & Res **avant la publication** des copies déjà présentes. Confirmer la paternité de chaque fichier cité, ajouter ensuite un crédit correct ou préparer un remplacement indépendant si permission refusée.
2. Faire valider dans le jeu les 16 affectations Vanilla EXCELLENT/GOOD, en respectant une icône finale par technologie et les cinq usages non technologiques.
3. Produire les 87 spécifications restantes par priorité, en privilégiant des objets réellement datés 1776–1836. Les assets Basileia ne deviennent utilisables qu'après réponse claire des titulaires.
4. Traiter séparément les biens, bâtiments, PM et PMG, notamment la méthode « aucune production de produits chimiques industriels ». Cette passe ne modifie aucun de ces objets.

## 8. Périmètre et validation

- Fichiers produits : sept CSV d'inventaire/shortlist/preuves, ce rapport et un fichier de brouillons, tous sous `docs/reports/assets/`.
- Aucun fichier `common/`, `localization/`, `gfx/`, `gui/` ou image n'a été édité dans cette passe.
- Le working tree comportait **déjà** une modification de `gui/tech6c_goods_texticons.gui` ainsi que des documents de release non suivis avant cet audit ; ils ont été laissés intacts. La vérification de périmètre doit donc distinguer ces éléments préexistants des neuf fichiers ASSET1.
- Aucun auteur contacté ; aucun commit ; aucun push.
