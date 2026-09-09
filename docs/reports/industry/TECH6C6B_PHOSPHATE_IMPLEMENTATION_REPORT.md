# TECH6C6B — Implémentation des phosphates et de la production d’engrais

Date : 9 septembre 2026  
Branche : `tech6c-goods-buildings-pm-implementation`  
Jeu de référence : Victoria 3 `1.13.11`, branche `release/1.13.11`

## 1. Résultat

**TECH6C6B RESULT: PASS**

Le bien phosphate, sa mine plafonnée, sa méthode de base et les deux routes d’engrais sont implémentés. La carte finale contient 40 États non nuls sur 675, sans doublon ni divergence entre la matrice et les fichiers de carte. Le validateur TECH6C6B et le smoke final de chargement passent.

Une réserve distincte demeure sur l’économie initiale prussienne : le bâtiment concerné est situé dans la Ruhr, appartient à un quartier financier prussien de Brandebourg et utilise `pm_artificial_fertilizers`, mais la Prusse ne reçoit pas `applied_mineralogy` au départ et aucune mine de phosphate n’est créée par l’historique. Ce point est classé **REVIEW REQUIRED — DEFERRED BY USER DECISION**. Conformément à la consigne opérateur, aucune technologie de départ n’a été distribuée et aucun gisement arbitraire n’a été ajouté. Cette réserve ne remet pas en cause la complétude mécanique du nouveau bien.

## 2. Bien phosphate

`phosphates` représente la roche phosphatée et le concentré minéral commercial dans un seul bien de marché :

- prix de base : £30 ;
- catégorie : `industrial` ;
- commerce : `tradeable = yes` ;
- consommation directe des POP : aucune ;
- texture temporaire : `gfx/error_deer.dds`.

Aucun bien `phosphate_ore`, `phosphoric_acid`, `superphosphate` ou `guano` n’est créé.

## 3. Support du bien personnalisé

L’infrastructure unifiée reçoit exactement quatre types de modificateur :

- `goods_input_phosphates_add` ;
- `goods_input_phosphates_mult` ;
- `goods_output_phosphates_add` ;
- `goods_output_phosphates_mult`.

Le texticon `@phosphates!` utilise le cerf temporaire. Les localisations anglaise et française couvrent le bien, la mine, le PMG, le PM d’extraction, les quatre noms directs, les quatre alias `modifier_` et leurs descriptions. Les deux fichiers nouveaux sont encodés en UTF-8 BOM. Les noms vanilla des deux PM d’engrais sont conservés pour éviter des doublons de localisation.

## 4. Mine de phosphate

`building_phosphate_mine` suit l’architecture minimale acceptée :

| Propriété | Valeur |
|---|---|
| groupe | `bg_mining` |
| type de ville | `mine` |
| construction | `construction_cost_medium` |
| manipulation de terrain | `mining` |
| propriété | `self` |
| valeur IA | 1 000 |
| technologie | `applied_mineralogy` |
| ressource | plafonnée par État |
| PMG | `pmg_mining_equipment_building_phosphate_mine` |

Le PMG contient uniquement `pm_picks_and_shovels_building_phosphate_mine`. Aucun escalier artificiel de pompes, d’explosifs ou d’automatisation n’est ajouté dans ce lot.

Recette par niveau : **5 outils → 25 phosphates**, 500 commerçants et 4 500 manœuvres, soit 5 000 emplois, pollution 5. Aux prix locaux réels, la valeur d’entrée est £200, la sortie £750 et la marge brute avant salaires £550.

## 5. Carte mondiale finale

Les 45 candidats non nuls de TECH6C6A ont été revus avec la base mondiale de l’[USGS](https://pubs.usgs.gov/publication/ofr02156), le [modèle de teneur/tonnage USGS](https://pubs.usgs.gov/bul/b1693/html/bull6spx.htm), des rapports régionaux et des sources géologiques nationales. Les placements précis ont été privilégiés : la [source officielle égyptienne](https://emra.gov.eg/ca/about-us) place les phosphates dans la vallée du Nil et sur la côte de la mer Rouge ; le [rapport USGS sur l’Algérie](https://pubs.usgs.gov/myb/vol3/2017-18/myb3-2017-18-algeria.pdf) situe Djebel Onk à Tébessa ; l’[USGS Chine](https://pubs.usgs.gov/of/2002/0156/pdf/OF02-156A.pdf) documente notamment Yichang, Dawu et Zhongxiang au Hubei ; [Geoscience Australia](https://www.ga.gov.au/digital-publication/aimr2019/commodity-summaries) concentre les ressources économiques retenues dans le bassin Georgina et l’île Christmas ; et l’[évaluation USGS Europe–Asie centrale](https://pubs.usgs.gov/of/2005/1294/d/of2005-1294d.pdf) sépare Kola, Karatau et les gisements ouzbeks.

Résultat final :

| Mesure | Résultat |
|---|---:|
| États revus | 675 |
| États non nuls | 40 |
| États à zéro | 635 |
| potentiel total | 1 216 |
| LOW — 8 | 4 |
| MODEST — 16 | 8 |
| MEDIUM — 24 | 8 |
| HIGH — 36 | 10 |
| VERY_HIGH — 48 | 8 |
| WORLD_CLASS — 60 | 2 |
| fichiers de régions modifiés | 11 |
| divergences matrice/carte | 0 |
| entrées phosphate dupliquées | 0 |
| valeurs non phosphate changées par le générateur | 0 |

Les onze fichiers de carte concernés sont `03_north_africa`, `04_subsaharan_africa`, `05_north_america`, `07_south_america`, `08_middle_east`, `09_central_asia`, `10_india`, `11_east_asia`, `12_indonesia`, `13_australasia` et `15_russia`.

### Différences par rapport à TECH6C6A

| État | 6A | 6B | Décision |
|---|---:|---:|---|
| `STATE_SINAI` | 16 | 0 | grands phosphates égyptiens prouvés hors Sinaï |
| `STATE_ALGIERS` | 16 | 0 | Djebel Onk est représenté dans `STATE_CONSTANTINE` |
| `STATE_CAJAMARCA` | 36 | 24 | Bayóvar/Sechura est à Piura ; agrégation de jeu voisine conservée mais réduite |
| `STATE_NEJD` | 16 | 0 | Al Jalamid/Al Khabra/Umm Wu’al sont représentés par le nord saoudien, `STATE_HAIL` |
| `STATE_WESTERN_AUSTRALIA` | 16 | 0 | aucune ressource économique distincte retenue face à Georgina/Christmas |
| `STATE_WEST_KARELIA` | 36 | 0 | Khibiny et Kovdor sont regroupés dans `STATE_KOLA` |

Les 39 autres candidats préliminaires sont conservés à leur valeur initiale. La baisse nette est de 112 points, de 1 328 à 1 216.

## 6. Routes d’engrais avant/après

Le bâtiment `building_chemical_plant`, sa porte `industrial_acids` et `pmg_fertilizer_production` sont conservés. Les trois PM restent mutuellement exclusifs.

### Route A — `pm_artificial_fertilizers`

Avant : 30 soufre + 10 fer + 5 sel → 90 engrais ; 5 000 emplois ; pollution 5 ; marge brute £650.  
Après : **20 phosphates + 20 produits chimiques industriels + 10 charbon → 80 engrais** ; mêmes 5 000 emplois ; pollution 10 ; marge brute £700.

L’identifiant est conservé et aucun verrou propre au PM n’est ajouté : la porte reste celle du bâtiment, `industrial_acids`.

### Route B — `pm_improved_fertilizer`

Avant : 30 soufre + 30 fer + 10 sel → 140 engrais ; 5 000 emplois ; pollution 10 ; marge brute £1 200.  
Après : **30 phosphates + 25 produits chimiques industriels + 15 charbon → 120 engrais** ; mêmes 5 000 emplois ; pollution 15 ; marge brute £1 250.

L’identifiant et le verrou `improved_fertilizer` sont conservés.

`pm_nitrogen_fixation` est inchangé : 40 soufre + 20 produits chimiques industriels + 30 fer + 20 sel → 200 engrais, pollution 15, 5 000 emplois.

## 7. Compatibilité de départ prussienne

**Résultat : REVIEW REQUIRED — contrôle différé.**

Les données locales corrigent la formulation préliminaire 6A :

- le `building_chemical_plant` est créé dans `s:STATE_RUHR`, `region_state:PRU` ;
- ses deux niveaux sont possédés par `building_financial_district`, pays `c:PRU`, région `STATE_BRANDENBURG` ;
- il démarre avec `pm_artificial_fertilizers` ;
- `STATE_BRANDENBURG` est créé pour `c:PRU` ;
- la Prusse reçoit `effect_starting_technology_tier_4_tech`, qui contient `shaft_mining` mais pas `applied_mineralogy` ;
- Brandenburg ne reçoit aucun phosphate dans la carte finale, conformément à la géologie ;
- aucun historique ne crée de mine de phosphate ou de stock initial.

Le bâtiment reste défini et charge correctement, mais son nouveau PM ne dispose donc pas d’une offre initiale garantie. Le commerce futur et la construction de mines peuvent résoudre cette tension, mais la distribution des technologies de départ et le démarrage économique seront traités ensemble après l’achèvement de tous les nouveaux biens, comme demandé. Aucun correctif artificiel n’est appliqué ici.

## 8. Économie et offre/demande

Les prix vérifiés sont : outils £40, phosphates £30, produits chimiques industriels £40, charbon £30 et engrais £30.

| Route | Intrants | Sortie | Marge brute |
|---|---:|---:|---:|
| mine de phosphate | £200 | £750 | £550 |
| engrais A, ancien | £2 050 | £2 700 | £650 |
| engrais A, nouveau | £1 700 | £2 400 | £700 |
| engrais B, ancien | £3 000 | £4 200 | £1 200 |
| engrais B, nouveau | £2 350 | £3 600 | £1 250 |

Demande phosphate et équivalent en niveaux de mine :

| Usines | base | améliorée | mixte |
|---:|---:|---:|---:|
| 10 | 200 / 8 mines | 300 / 12 mines | 250 / 10 mines |
| 25 | 500 / 20 mines | 750 / 30 mines | 620 / 24,8 mines |
| 50 | 1 000 / 40 mines | 1 500 / 60 mines | 1 250 / 50 mines |

Le plafond théorique mondial est de 1 216 niveaux, soit 30 400 phosphates par cycle si tout était construit. Même 50 usines améliorées n’utilisent que 60 niveaux miniers. Comme les potentiels ne sont pas construits automatiquement, il n’existe pas de déséquilibre structurel manifeste : ni `PHOSPHATE_SUPPLY_TOO_LOW` ni `PHOSPHATE_SUPPLY_TOO_HIGH` n’est déclenché. L’adoption réelle reste un sujet de bêta joueurs.

## 9. Validation statique

| Contrôle | Résultat |
|---|---|
| `tools/tech6c6b_validate.py` | PASS |
| biens/bâtiments/PMG/PM uniques | PASS |
| références PMG | PASS |
| quatre types de modificateur | PASS |
| localisations EN/FR directes et alias | PASS |
| formes mal écrites `ggoods_`, `oods_`, `goods_phosphates_add` | 0 |
| accolades des fichiers ajoutés et de la carte | PASS |
| matrice : lignes/IDs/manquants/doublons | 675/675/0/0 |
| carte : doublons/divergences | 0/0 |
| ressources non phosphate touchées par le générateur | 0 |
| `git diff --check` | PASS, seulement avertissements LF/CRLF |
| branche | PASS |

Les validateurs historiques 5B et 5C ont aussi été exécutés. Ils signalent respectivement 40 « lignes non cuivre » et un hash de carte différent : ce sont des gardes de fin de phase conçues avant l’ajout volontaire des 40 ressources phosphate. Leurs contrôles cuivre/aluminium, topologie technologique et totaux propres restent intacts. Ils ne constituent pas un défaut TECH6C6B ; le validateur 6B compare désormais explicitement phosphate, carte et matrice.

## 10. Smoke de chargement

**STARTUP/PARSER SMOKE: PASS_LIMITED.**

Le lancement final a exécuté `victoria3.exe -gdpr-compliant -debug_mode` avec le `descriptor.mod` courant pendant environ 45 secondes. Le processus créé a été arrêté et aucun `victoria3.exe` n’est resté actif.

Journaux finaux :

| Journal | Frais | Taille | SHA-256 |
|---|---|---:|---|
| `error.log` | oui | 159 707 | `CEADF882C273EC1079A836F3F81FBF01A55AFA219238DCFB4A1DD42EEC66AF81` |
| `warning.log` | oui | 6 234 | `135128D08FCE880B36DC33639BEC85DA57AC22D5FAE27696A45554FD9EFCE855` |
| `debug.log` | oui | 187 856 | `A3E9CFF8C85B9135105A49F26962766B55C7C490010E327F28B5EF8D3D3BB0C0` |
| `game.log` | resté vide | 0 | `E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855` |

Le scan final trouve **0 occurrence ciblée** et **0 diagnostic générique** associant phosphate/TECH6C6B à un bien, modificateur, PM, PMG, texture, localisation ou parsing invalide. Un premier smoke avait détecté l’absence de BOM, puis un second des surcharges de noms vanilla ; les deux défauts ont été corrigés avant ce résultat final.

Ce smoke ne prouve pas l’arrivée au menu, une campagne, la rentabilité observée, les infobulles ni le comportement IA.

## 11. Fichiers créés

Gameplay :

- `common/goods/15_tech6c6b_phosphates.txt` ;
- `common/buildings/15_tech6c6b_phosphate_mine.txt` ;
- `common/production_method_groups/15_tech6c6b_phosphate_pmgs.txt` ;
- `common/production_methods/15_tech6c6b_phosphate_extraction.txt` ;
- `localization/english/tech6c6b_phosphates_l_english.yml` ;
- `localization/french/tech6c6b_phosphates_l_french.yml`.

Documentation et outils :

- `docs/reports/industry/TECH6C6B_PHOSPHATE_IMPLEMENTATION_REPORT.md` ;
- `docs/reports/industry/TECH6C6B_PHOSPHATE_GLOBAL_RESOURCE_MATRIX.csv` ;
- `docs/reports/industry/TECH6C6B_FERTILIZER_ECONOMIC_VALIDATION.csv` ;
- `docs/reports/industry/TECH6C6B_PHOSPHATE_CONSUMER_IMPLEMENTATION_MATRIX.csv` ;
- `tools/tech6c6b_build_phosphate_distribution.py` ;
- `tools/tech6c6b_validate.py`.

## 12. Fichiers modifiés

- `common/production_methods/01_industry.txt` — exactement deux blocs d’engrais ;
- `common/modifier_type_definitions/12_tech6c_custom_goods_modifier_types.txt` ;
- `gui/tech6c_goods_texticons.gui` ;
- `localization/english/tech6c_goods_modifiers_l_english.yml` ;
- `localization/french/tech6c_goods_modifiers_l_french.yml` ;
- onze fichiers `map_data/state_regions` listés à la section 5.

## 13. Exclusions et suite

Confirmé dans TECH6C6B : 0 nitrate, 0 mine de nitrate, 0 ressource nitrate, 0 guano, 0 changement Haber-Bosch, 0 recette d’explosifs, 0 munition, 0 PM agricole, 0 nouvelle technologie, 0 changement de topologie, 0 changement de `gui/tech_tree.gui`, 0 changement aux systèmes TECH6C5.

Portée recommandée de **TECH6C6C — NITRATES, EXPLOSIVES AND SYNTHETIC NITROGEN IMPLEMENTATION** : créer le bien nitrate et sa mine concentrée dans l’Atacama ; revoir ensemble les routes nitrate d’engrais et les recettes/noms des explosifs ; convertir `pm_nitrogen_fixation` en route Haber-Bosch sans nitrate miné ; réviser alors les historiques et technologies de départ de manière globale pour tous les nouveaux biens ; conserver les fermes et les munitions sur leurs biens transformés ; valider commerce, pénuries, substitution synthétique et adoption IA par la bêta joueurs.

**Aucun commit et aucun push n’ont été effectués.**
