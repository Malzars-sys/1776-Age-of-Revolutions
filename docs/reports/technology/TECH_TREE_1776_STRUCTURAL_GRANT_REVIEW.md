# TECH TREE 1776 — Revue structurelle des grants

## 1. Résumé

Les **310 grants ont été examinés individuellement**. Le CSV source couvre **193 pays au total**. La valeur « 154 pays » du résumé précédent correspond uniquement aux pays recevant au moins un des trois nouveaux troncs `GAMEPLAY_ABSTRACTION`, et non à l'union des 310 lignes. Le candidat est topologiquement solide, mais trois contenus placés directement sur des troncs généraux et deux arêtes vers des parents spécialisés rendaient certains grants trop généreux.

La recommandation finale retient un tronc militaire unique mais entièrement neutre, conserve les troncs naval et financier sans contenu direct, redéfinit `turnpike_road_networks` en infrastructure terrestre organisée, retire les arêtes manufacturières qui accordaient meubles/outils et retire `shaft_mining` comme parent de la minéralogie appliquée.

| Décision | Lignes |
|---|---|
| ACCEPT | 43 |
| ACCEPT_GAMEPLAY_ABSTRACTION | 16 |
| REDEFINE_PARENT | 234 |
| REPLACE_PARENT | 0 |
| SPLIT_TRUNK | 0 |
| REMOVE_EDGE | 17 |
| COUNTRY_EXCEPTION | 0 |
| RESEARCH_NEEDED | 0 |

## 2. Analyse des 310 grants

| Parent ajouté | Lignes | Décisions dominantes |
|---|---|---|
| organized_military_establishments | 138 | REDEFINE_PARENT: 138 |
| organized_naval_establishments | 54 | REDEFINE_PARENT: 54 |
| traditional_food_processing | 39 | ACCEPT: 39 |
| organized_financial_institutions | 34 | REDEFINE_PARENT: 34 |
| codified_practical_knowledge | 16 | ACCEPT_GAMEPLAY_ABSTRACTION: 16 |
| organized_workshops | 14 | REMOVE_EDGE: 14 |
| turnpike_road_networks | 8 | REDEFINE_PARENT: 8 |
| shaft_mining | 3 | REMOVE_EDGE: 3 |
| traditional_glassmaking | 2 | ACCEPT: 2 |
| permanent_engineer_services | 1 | ACCEPT: 1 |
| ship_classification_surveying | 1 | ACCEPT: 1 |

Chaque ligne du CSV principal contient le TAG, le pays, la région, les enfants déclencheurs, le contenu direct du parent, toutes les branches sœurs devenues accessibles, un coût collatéral et une décision finale. Il ne reste aucune ligne non examinée.

## 3. Socle militaire

Le tronc unique produisait 138 grants. Parmi eux, les cas les plus sensibles sont ceux déclenchés uniquement par `light_infantry_tactics` dans des régions comprenant des confédérations, émirats ou entités décentralisées. Exemples : ABB (Arab Emirates), ABU (Trucial States), ACE (Aceh), ARG (Argentina), BHN (Bahrain), CHT (Chitral), ECU (Ecuador), HBC (Hudson's Bay Company), HDJ (Hedjaz), IQU (Iquicha), JOH (Johore), KAF (Kafiristan), KAL (Kalat), KAT (Kathiri), KBB (Kathiri), LAH (Lahej), MAH (Mahra), MAK (Makran), MBB (Mahra), MICC (Michigan Tribal Confederation).

La caserne est la source principale du coût collatéral : une tactique légère ou une capacité artisanale d'armes ne prouve pas l'existence d'un appareil permanent complet. La solution recommandée ne crée aucune exception pays : elle corrige le sens du tronc lui-même et le rend purement structurel.

| Combinaison déclencheuse (15 principales) | Pays |
|---|---|
| light_infantry_tactics | 28 |
| light_infantry_tactics;regulated_small_arms | 17 |
| light_infantry_tactics;permanent_engineer_services;permanent_military_hospitals;regulated_small_arms;scientific_fortification_siegecraft;standardized_field_artillery | 17 |
| light_infantry_tactics;permanent_engineer_services;regulated_small_arms;scientific_fortification_siegecraft;standardized_field_artillery | 14 |
| light_infantry_tactics;standardized_field_artillery | 12 |
| light_infantry_tactics;regulated_small_arms;scientific_fortification_siegecraft;standardized_field_artillery | 7 |
| regulated_small_arms;scientific_fortification_siegecraft;standardized_field_artillery | 6 |
| scientific_fortification_siegecraft | 6 |
| regulated_small_arms | 5 |
| light_infantry_tactics;regulated_small_arms;standardized_field_artillery | 4 |
| light_infantry_tactics;permanent_engineer_services;scientific_fortification_siegecraft;standardized_field_artillery | 3 |
| regulated_small_arms;scientific_fortification_siegecraft | 3 |
| permanent_engineer_services;regulated_small_arms;scientific_fortification_siegecraft;standardized_field_artillery | 2 |
| light_infantry_tactics;permanent_engineer_services;standardized_field_artillery | 2 |
| permanent_engineer_services;permanent_military_hospitals;scientific_fortification_siegecraft | 1 |

Le fichier `TECH_TREE_1776_MILITARY_TRUNK_TRIGGER_AUDIT.csv` contient les 138 lignes intermédiaires et les six indicateurs obligatoires.

## 4. Comparaison une/deux branches militaires

| Option | Racines | Arêtes | Grants militaires | Pays | Unlocks collatéraux | Contradictions | Violations PM | Fanout max |
|---|---|---|---|---|---|---|---|---|
| MILITARY_A_SINGLE_TRUNK | 15 | 344 | 138 | 138 | 138 | 40 | 0 | 7 |
| MILITARY_B_ORGANIZATION_PLUS_ARMAMENT | 16 | 344 | 232 | 138 | 0 | 0 | 0 | 7 |
| MILITARY_C_REDEFINED_PURE_SINGLE_TRUNK | 15 | 344 | 138 | 138 | 0 | 0 | 0 | 7 |

Le compteur de contradictions de l'option A est un proxy conservateur : 40 pays ne possèdent qu'un seul enfant spécialisé, alors que le tronc leur donnerait directement une caserne. Les deux options pures ramènent ce compteur à zéro car elles n'accordent aucun contenu gameplay.

**Option retenue : C — un tronc unique redéfini et pur.** Les données montrent 94 pays cumulant des déclencheurs d'organisation et d'armement, mais seulement six pays avec armement seul. Créer un second tronc ajouterait 94 grants dupliqués pour un gain sémantique limité. `organized_military_establishments` devient donc un socle abstrait de pratiques et d'organisation militaires, sans caserne, bâtiment, PM ou bonus direct.

## 5. Socle naval

Les 54 pays ont déjà au moins une spécialisation navale issue de la SECOND PASS. Le concept de capacité navale organisée est donc acceptable. En revanche, déplacer le shipyard ou l'administration navale sur le tronc créerait un coût collatéral réel. Le tronc naval doit rester pur; `state_dockyard_systems`, `enclosed_dock_systems`, `scientific_naval_architecture` et `ship_classification_surveying` gardent leurs contenus spécialisés.

## 6. Socle financier

Les 34 grants sont compatibles avec une capacité générale de comptabilité, crédit et intermédiation. Le bonus `country_loan_interest_rate_add = -0.01` est **REMOVE** : il transforme un parent structurel largement distribué en avantage macroéconomique gratuit. Les enfants rendent déjà le nœud utile.

## 7. `organized_workshops`

Les 14 lignes ont un coût collatéral **UNACCEPTABLE** : elles accorderaient à la fois `building_furniture_manufactory` et `building_tooling_workshop` pour justifier papier, verre ou acides. Recommandation : retirer les trois arêtes `traditional_papermaking`, `traditional_glassmaking` et `industrial_acids` vers `organized_workshops`. Le nœud conserve furniture/tooling et reste parent de `precision_boring`; la bonne causalité existante n'est pas cassée.

## 8. Alimentation

Les 39 grants de `traditional_food_processing` sont acceptés. Raffinage du sucre ou distillation organisée impliquent raisonnablement une base générale de transformation alimentaire, et `building_food_industry` est un collatéral cohérent.

## 9. Savoirs codifiés

Les 16 grants sont acceptés comme abstraction gameplay. « Conserver, formaliser et transmettre des savoirs pratiques » est un socle neutre pour école élémentaire, médecine, cadastre, droit et économie politique. Aucun parent presse/échange scientifique n'est réintroduit.

## 10. Infrastructure / turnpikes / canaux

Les 8 grants ne sont pas acceptables sous le nom mondial de « routes à péage ». Recommandation : conserver l'ID pour la compatibilité mais le redéfinir/localiser comme infrastructure terrestre organisée. Ses PM routiers restent compatibles et `industrial_canals` peut garder cette dépendance générale sans nouveau quatrième tronc.

## 11. Mines

Les trois grants de `shaft_mining` sont refusés : `applied_mineralogy` ne justifie pas l'ouverture simultanée de sept filières minières. L'arête est retirée. `applied_mineralogy` reste une racine spécialisée utile, reliée à ses descendants et déblocages, donc ni isolée ni feuille vide. Les deux grants de verrerie, le grant de génie et le grant de classification navale sont acceptés.

## 12. Petits modifiers

| Technologie | Décision | Valeur finale | Motif |
|---|---|---|---|
| organized_forestry | KEEP | +0.05 throughput camps de bûcherons | Renforce directement le rôle productif du nœud. |
| systematic_cadastral_surveying | KEEP | +10 state tax capacity | Effet borné, lisible et causalement lié au cadastre. |
| modern_lighthouse_optics | KEEP | +0.05 throughput ports | Donne une utilité terminale sectorielle cohérente. |
| optical_telegraph_networks | REDUCE | +10 country influence | 25 est trop généreux pour une feuille; 10 reste perceptible. |
| organized_financial_institutions | REMOVE | aucun modifier | Le tronc a déjà trois enfants utiles. |

## 13. Fusions / compatibilité

Le scan exact du mod et de vanilla trouve `hydraulic_turbines`, `standardized_military_rockets` et `explosive_field_ammunition` uniquement dans leurs définitions/localisations du mod; la seule référence structurelle interne supplémentaire est `standardized_military_rockets -> explosive_field_ammunition`. Aucun événement, journal, scripted effect, trigger ou fichier IA ne les référence. Décision : **MERGE_AND_ALIAS**. Les IDs doivent rester comme aliases `can_research = no` pour les sauvegardes et mods internes; ne pas les supprimer physiquement.

## 14. Architecture finale recommandée

Le plan final n'ajoute aucun nœud au candidat, transforme trois troncs en nœuds purs, retire quatre arêtes trop coûteuses et redéfinit un ID d'infrastructure. Le détail exhaustif est dans le CSV d'architecture finale.

## 15. Métriques finales

| Métrique | Candidat | Final recommandé |
|---|---|---|
| roots | 15 | 19 |
| isolated_nodes | 0 | 0 |
| leaf_no_effect | 0 | 0 |
| edges | 344 | 340 |
| max_child_count | 7 | 7 |
| cycles | 0 | 0 |
| building_pm_causality_violations | 0 | 0 |
| cross_era_gt3 | 44 | 44 |

Les nouvelles racines sont des spécialisations utiles (`traditional_papermaking`, `traditional_glassmaking`, `industrial_acids`, `applied_mineralogy`) et non des nœuds isolés ou vides.

## 16. Distribution finale simulée

- GAMEPLAY_ABSTRACTION_GRANTS : **226**
- STRUCTURAL_REQUIRED_GRANTS : **67**
- TOTAL_STRUCTURAL_GRANTS : **293**
- COUNTRIES_AFFECTED (union de tous les grants) : **184**
- COUNTRIES_AFFECTED par les troncs GAMEPLAY_ABSTRACTION : **154**

| Technologie ajoutée | Grants |
|---|---|
| organized_military_establishments | 138 |
| organized_naval_establishments | 54 |
| traditional_food_processing | 39 |
| organized_financial_institutions | 34 |
| codified_practical_knowledge | 16 |
| turnpike_road_networks | 8 |
| traditional_glassmaking | 2 |
| permanent_engineer_services | 1 |
| ship_classification_surveying | 1 |

## 17. Points nécessitant encore décision humaine

- Valider les noms anglais/français du concept général réutilisant l'ID `turnpike_road_networks`.
- Confirmer visuellement que les couloirs doctrine, armement et services issus du tronc militaire unique restent lisibles dans l'arbre runtime.
- Confirmer en runtime les quatre petits modifiers conservés/réduits; aucune valeur n'est implémentée par cette passe.
- Décider la durée de conservation des aliases après une politique explicite de compatibilité des sauvegardes.

## 18. Ordre d'implémentation par vagues

1. Tronc militaire unique redéfini et pur, puis fermeture pays recalculée.
2. Troncs naval et financier rendus purs.
3. Retrait des arêtes `organized_workshops` et `shaft_mining` refusées.
4. Redéfinition/localisation de l'infrastructure terrestre organisée.
5. Arêtes acceptées alimentation, savoirs, verre, génie et classification navale.
6. Petits modifiers, fusions avec aliases, puis validation statique et runtime.
7. Distribution pays finale seulement après validation de l'architecture.

---

Audit/simulation uniquement : aucun fichier gameplay n'a été modifié par cette revue; aucun commit, push ou PR.
