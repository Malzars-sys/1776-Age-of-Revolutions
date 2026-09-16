# TECH TREE 1776 — Audit global de topologie et de cohérence gameplay

Version auditée : Victoria 3 1.13.11  
État : proposition documentaire, aucune implémentation gameplay  
Sources : overlay effectif vanilla + mod, setups pays actuels et sept captures runtime du 13 septembre 2026.

## 1. Résumé exécutif

L’arbre contient exactement **287 définitions technologiques** : **244 nœuds recherchables** et **43 alias ou nœuds non recherchables**. La redistribution historique est cohérente, mais sa topologie n’est pas encore une architecture de gameplay satisfaisante.

Les symptômes visibles dans les captures sont confirmés par les fichiers : 39 racines recherchables, 4 nœuds isolés, 7 feuilles sans effet et 27 violations de causalité entre le bâtiment et ses PM. Les branches production, société, militaire et navale comportent trop de racines spécialisées. `industrial_acids` et `scientific_naval_architecture` portent chacun huit enfants, ce qui produit les faisceaux de lignes visibles en jeu.

La proposition conserve les spécialisations, mais les rattache à quelques troncs. Elle réutilise les nœuds généraux existants et ne propose que trois nouveaux IDs : un socle financier, un socle militaire et un socle naval. La simulation aboutit à 15 racines, 0 nœud isolé, 0 feuille sans effet et 0 violation bâtiment–PM.

Cette architecture ne doit pas être implémentée en une seule modification. Les gates de contenu, les nouveaux nœuds et les grants pays doivent être séparés en vagues contrôlables.

## 2. Métriques actuelles

| Mesure | Valeur actuelle |
|---|---:|
| Définitions totales | 287 |
| Technologies recherchables | 244 |
| Alias/non recherchables | 43 |
| Racines | 39 |
| Nœuds isolés | 4 |
| Feuilles sans effet | 7 |
| Arêtes | 317 |
| Cycles | 0 |
| Parents inconnus | 0 |
| Parents moyens | 1,299 |
| Enfants moyens | 1,299 |
| Maximum d’enfants | 8 |
| Arêtes négatives | 0 |
| Même era | 30 |
| Écart +1 | 111 |
| Écart +2 | 79 |
| Écart +3 | 50 |
| Écart supérieur à 3 | 47 |
| Couples bâtiment–PM examinés | 704 |
| Violations de causalité | 27 |

Les métriques topologiques excluent les 43 alias non recherchables. Le relevé par nœud conserve néanmoins les 287 définitions. Les comptes de départ couvrent les 474 TAG du plan actuel, y compris GAL, MLT et PPU conservés comme research gaps.

## 3. Principaux problèmes observés

Les suppressions d’arêtes précédentes ont correctement éliminé des causalités historiques artificielles, mais elles ont transformé des spécialités en points de départ indépendants. Les cas les plus visibles sont la minéralogie, les acides, les canaux, plusieurs institutions sociales, trois branches militaires et les trois fondations navales.

Les captures montrent également que l’interface ne dispose pas de couloirs stables : les enfants éloignés d’un root spécialisé tracent de longues lignes à travers les autres branches. Aucun fichier de coordonnées `position/x/y` propre aux technologies n’est présent dans l’overlay ; la disposition est donc largement dérivée du graphe et de l’ordre des nœuds. La priorité doit être de corriger le graphe avant toute retouche de disposition.

Enfin, certaines technologies tardives n’ont aucun contenu réel. Elles existent dans l’arbre et consomment un emplacement sans fournir d’unlock, de modifier ou de descendant utile.

## 4. Racines

Les 39 racines se répartissent en 14 production, 11 militaire et 14 société. Toutes ne sont pas mauvaises : `improved_husbandry`, `organized_workshops`, `shaft_mining`, `traditional_food_processing`, `periodical_print_networks` ou `systematic_administrative_statistics` peuvent servir de fondations.

Les racines trop spécialisées sont notamment :

- production : `applied_mineralogy`, `industrial_acids`, `industrial_canals`, `industrial_ceramics`, `sugar_refining`, `traditional_glassmaking`, `traditional_papermaking` ;
- société : `medical_degrees`, `organized_elementary_schooling`, `political_economy`, `stock_exchange`, `commercial_insurance_markets`, `institutionalized_public_credit`, `systematic_cadastral_surveying` ;
- militaire/naval : `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`, `permanent_engineer_services`, `permanent_military_hospitals`, `scientific_fortification_siegecraft`, `state_dockyard_systems`, `enclosed_dock_systems`, `scientific_naval_architecture` et `ship_classification_surveying`.

La proposition conserve 15 racines : six en production, sept en société et deux en militaire/naval. Cette pluralité est intentionnelle ; l’objectif n’est pas un graphe mondial unique.

## 5. Nœuds isolés

Quatre nœuds recherchables sont actuellement isolés :

- `codified_practical_knowledge` : 119 pays de départ, mais aucun parent, enfant, unlock ou modifier ;
- `scientific_fortification_siegecraft` : deux bâtiments lui étaient auparavant associés, mais l’overlay effectif ne lui donne plus de fonction recensée ;
- `systematic_cadastral_surveying` : 15 pays de départ, sans effet ;
- `traditional_glassmaking` : 62 pays de départ et gate du bâtiment verrerie, mais aucune connexion technologique.

Résolution proposée : faire de `codified_practical_knowledge` un tronc institutionnel, rattacher la fortification au tronc militaire, donner un bonus fiscal limité au cadastre et rattacher le verre aux ateliers organisés.

## 6. Feuilles inutiles

Sept feuilles sans enfant, unlock, contenu militaire/diplomatique ni modifier ont été trouvées :

- `codified_practical_knowledge` : devient un tronc ;
- `systematic_cadastral_surveying` : reçoit `state_tax_capacity_add = 10` ;
- `veterinary_science` : devient parent de `military_veterinary_services` ;
- `modern_lighthouse_optics` : reçoit `building_port_throughput_add = 0.05` ;
- `optical_telegraph_networks` : reçoit `country_influence_add = 25` ;
- `hydraulic_turbines` : fusion dans `professional_civil_engineering`, puis conservation éventuelle comme alias non recherchable jusqu’à l’existence d’un vrai PM hydraulique ;
- `standardized_military_rockets` : fusion avec la chaîne d’artillerie, car aucun contenu fusée n’existe actuellement.

L’audit a également révélé que `explosive_field_ammunition` ne sert qu’à conduire vers le nœud fusée vide. Les deux concepts sont donc proposés en fusion dans `standardized_field_artillery`, avec conservation des IDs comme alias si un scan de compatibilité l’exige.

## 7. Causalité bâtiments/PM

Les 704 associations effectives bâtiment–PM ont été contrôlées. Vingt-sept enfreignent la règle des trois eras. Elles concernent :

- automobile : 4 ;
- verrerie : 4 ;
- alimentation : 3 ;
- mine d’or : 3 ;
- plateforme pétrolière : 3 ;
- mine de phosphate : 3 ;
- académie des arts, fonderie d’artillerie, plantation de coton, industrie électrique, explosifs, centrale électrique et plantation de caoutchouc : 1 chacune.

Les corrections proposées ne transforment pas des technologies générales en dépendances sectorielles. Elles utilisent quatre mécanismes :

1. rattacher la technologie du procédé au socle du bâtiment lorsque le lien est général (`sugar_refining`, `distillation`, `crystal_glass`, `deep_mine_engineering`, `steam_turbine`, `camera`) ;
2. déplacer le gate du bâtiment lorsqu’il est conceptuellement faux (`building_artillery_foundry` vers `standardized_field_artillery`, suppression du gate `cotton_gin` sur la plantation elle-même) ;
3. ajouter un second gate cumulatif aux PM propres au bâtiment ;
4. créer une variante PM propre au bâtiment lorsque le PM générique est partagé, notamment pour la gestion scientifique des industries automobile/électrique et le transport ferroviaire du caoutchouc.

La simulation de cette stratégie donne 0 violation. Le CSV de causalité conserve chaque exception et chaque recommandation individuelle.

## 8. Production

La production ancienne doit être organisée autour de six couloirs :

- manufactures : `organized_workshops` ;
- alimentation : `traditional_food_processing` ;
- agriculture : `improved_husbandry` ;
- mines : `shaft_mining` ;
- textile : `organized_textile_production` ;
- transport : `turnpike_road_networks`.

Ces troncs restent indépendants. Ils évitent qu’une seule technologie donne automatiquement accès à tous les bâtiments de base.

`organized_workshops` reçoit comme enfants `traditional_papermaking`, `traditional_glassmaking` et `industrial_acids`, tout en conservant sa chaîne vers `precision_boring`. `traditional_food_processing` reçoit `sugar_refining` et `distillation`. `turnpike_road_networks` reçoit `industrial_canals` au titre de l’organisation des infrastructures, et non d’une causalité historique littérale.

## 9. Agriculture

`improved_husbandry` est déjà le bon tronc général. Il structure `organized_forestry`, `improved_agricultural_implements`, `advanced_crop_rotations` et `selective_breeding`.

Il ne faut pas rétablir `selective_breeding` comme parent obligatoire des rotations culturales. Les deux spécialisations restent sœurs. La proposition ne change pas cette décision.

`improved_agricultural_implements` conserve son PM outils et ses descendants. Aucun nouveau lien vers `organized_workshops` n’est proposé afin d’éviter que la fermeture des starts agricoles accorde automatiquement les ateliers de meubles et d’outils à trop de pays.

## 10. Mines et métallurgie

Structure proposée :

`shaft_mining` → `applied_mineralogy` et `atmospheric_engine`  
`shaft_mining` + `organized_workshops` → `coke_smelting`  
`atmospheric_engine` + `coke_smelting` + `organized_workshops` → `precision_boring`

Cette structure rattache de nouveau la minéralogie au monde minier, sans réintroduire l’erreur « pompe à feu exige fonte au coke ». `atmospheric_engine` reste accessible avec `shaft_mining` seul.

Les PM de pompe des mines d’or et de phosphate reçoivent un gate cumulatif `applied_mineralogy` propre à ces bâtiments. Les technologies générales de vapeur ne sont donc pas rendues dépendantes de la minéralogie.

## 11. Manufactures

`organized_workshops` est confirmé comme fondation manufacturière, mais pas comme super-parent universel. Il conserve les manufactures de meubles et d’outils, ouvre les branches papier/verre et sert au socle de la chimie ancienne.

`traditional_papermaking` reste spécialisé et gate le moulin à papier. `traditional_glassmaking` gate la verrerie et devient parent de `industrial_ceramics` et `crystal_glass`. `chemical_bleaching` passe en era 5 et dépend de `industrial_alkalis` plutôt que directement des acides. Cette disposition réduit les croisements et donne une progression matière → chimie → procédé.

## 12. Société et administration

`codified_practical_knowledge` devient le tronc de :

- `organized_elementary_schooling` ;
- `medical_degrees` ;
- `systematic_cadastral_surveying` ;
- `systematic_legal_codification` ;
- `political_economy`.

Ce lien représente la capacité de conserver, normaliser et transmettre les savoirs. Il ne suppose ni académie scientifique moderne ni presse périodique obligatoire.

`periodical_print_networks`, `systematic_administrative_statistics`, `institutionalized_scientific_exchange`, `international_relations` et `variolation_networks` restent des racines distinctes lorsque leur autonomie est utile au gameplay.

## 13. Finance

Il ne faut pas restaurer une chaîne linéaire crédit public → bourse → assurance. Les trois institutions sont sœurs sous un nouveau socle neutre : `organized_financial_institutions`.

Ce nœud era 1 représente tenue des comptes, crédit et intermédiation. Un petit `country_loan_interest_rate_add = -0.01` est proposé afin qu’il ne soit pas vide. Il ne représente pas une bourse moderne et n’accorde aucune des trois spécialisations à lui seul.

La fermeture simulée demande 34 grants de ce socle.

## 14. Médecine et éducation

`medical_degrees` et `organized_elementary_schooling` deviennent des enfants de `codified_practical_knowledge`, pas de l’échange scientifique institutionnalisé.

`veterinary_science` devient le parent civil de `military_veterinary_services`. Les académies techniques restent une branche spécialisée ; elles ne doivent pas être imposées comme parent universel des titres médicaux.

## 15. Militaire

Un nouveau `organized_military_establishments` era 1 est proposé. Il représente la capacité d’entretenir des forces permanentes et des services spécialisés. Le gate de la caserne peut y être déplacé, ce qui donne au nœud une fonction sans bonus numérique inventé.

Ses branches directes sont la fortification, les armes réglementaires, la tactique légère, l’artillerie standardisée, le génie permanent et les hôpitaux militaires. Elles restent sœurs : ni les armes, ni l’artillerie, ni la fortification ne deviennent le parent artificiel de toutes les autres.

`military_topographic_surveying` dépend ensuite du service du génie. La fonderie d’artillerie passe sur `standardized_field_artillery`, afin que le bâtiment et son PM de base soient disponibles ensemble.

La fermeture simulée nécessite 138 grants du socle militaire. C’est le principal risque de distribution : chaque pays irrégulier ou décentralisé doit être revu avant implémentation.

## 16. Naval

Un nouveau `organized_naval_establishments` era 1 réunit les capacités communes sans confondre les spécialisations. Ses enfants sont :

- `state_dockyard_systems` ;
- `enclosed_dock_systems` ;
- `scientific_naval_architecture` ;
- `ship_classification_surveying`.

Le socle commun shipyard/administration navale est proposé sur ce nouveau nœud. Les arsenaux, bassins fermés et connaissances d’architecture restent séparés.

Pour réduire le fan-out de `scientific_naval_architecture`, `marine_chronometry` et `standardized_naval_signals` passent sous `ship_classification_surveying`, tandis que l’arête directe redondante vers `iron_hull_construction` est supprimée. La fermeture demande 54 grants navals.

## 17. Technologies faibles ou inutiles

`organized_forestry` n’est pas vide, mais son unique PM ne suffit plus à lui donner une valeur durable depuis l’introduction du logging rudimentaire universel. Un bonus limité `building_logging_camp_throughput_add = 0.05` est proposé. Il améliore entrées et sorties sans créer artificiellement du bois.

Les quatre autres bonus proposés sont volontairement modestes : ports +5 %, influence +25, capacité fiscale d’État +10 et intérêt d’emprunt -1 %. Ils doivent faire l’objet d’un runtime économique avant validation.

Les nœuds sans contenu hydraulique ou fusée sont fusionnés plutôt que sauvés par un bonus sans justification.

## 18. Nouveaux nœuds généraux proposés

Seulement trois nouveaux IDs sont proposés :

| ID | Fonction | Grants estimés | Risque |
|---|---|---:|---|
| `organized_financial_institutions` | socle crédit/bourse/assurance | 34 | moyen |
| `organized_military_establishments` | socle forces/services permanents | 138 | moyen |
| `organized_naval_establishments` | socle chantiers/administration/savoirs navals | 54 | faible à moyen |

Les nœuds existants ne peuvent pas remplir ces rôles sans accorder immédiatement leur contenu spécialisé. Le CSV dédié détaille l’effet, l’abstraction et le risque de chacun.

## 19. Architecture globale proposée

La proposition ajoute 27 arêtes nettes : 317 → 344. L’augmentation est limitée et produit des branches plutôt qu’une chaîne linéaire. Les trois anciens nœuds sans contenu fusionnés compensent les trois nouveaux socles : le nombre de technologies recherchables simulé reste 244.

Le maximum d’enfants tombe de 8 à 7. Les branches `industrial_acids` et `scientific_naval_architecture` sont étagées à travers les alkalis, la distillation, la classification navale et les procédés intermédiaires. Quatre recommandations `LAYOUT_ONLY` décrivent ensuite des couloirs production, société, militaire et naval.

## 20. Impact sur la distribution pays

La fermeture de la proposition exige 310 relations pays-technologie supplémentaires :

- 226 grants de nouveaux socles classés `GAMEPLAY_ABSTRACTION` ;
- 84 grants de prérequis existants classés `STRUCTURAL_REQUIRED` ;
- 154 pays distincts reçoivent au moins un grant de gameplay abstraction ;
- 0 retrait structurel simulé.

Répartition principale : tronc militaire 138, tronc naval 54, alimentation traditionnelle 39, tronc financier 34, savoirs codifiés 16, ateliers organisés 14, routes à péage 8, puits de mine 3, verre traditionnel 2 et génie permanent 1.

Ces lignes ne sont pas autorisées pour implémentation automatique. Elles constituent une liste de revue pays par pays, particulièrement pour le socle militaire.

## 21. Compromis histoire/gameplay

Les nouvelles arêtes représentent une capacité générale, pas nécessairement une invention causale. Un pays ayant des hôpitaux militaires peut recevoir le socle « établissements militaires organisés » sans qu’une institution porte historiquement ce nom exact.

À l’inverse, les troncs ne donnent pas leurs spécialisations. Le socle financier ne donne pas automatiquement la bourse ; le socle naval ne donne pas automatiquement les bassins fermés ; les ateliers organisés ne sont pas imposés à toute l’agriculture.

Le compromis le plus important concerne les 138 grants militaires. Si la revue pays juge ce coût trop élevé, la solution correcte est de diviser la proposition en un tronc « organisation militaire » et un tronc « armement », pas de recréer une chaîne fortification → armes → tactique.

## 22. Métriques simulées après redesign

| Mesure | Actuel | Proposé |
|---|---:|---:|
| Nœuds recherchables | 244 | 244 |
| Racines | 39 | 15 |
| Isolés | 4 | 0 |
| Feuilles sans effet | 7 | 0 |
| Arêtes | 317 | 344 |
| Cycles | 0 | 0 |
| Parents inconnus | 0 | 0 |
| Parents/enfants moyens | 1,299 | 1,410 |
| Maximum d’enfants | 8 | 7 |
| Arêtes négatives | 0 | 0 |
| Même era | 30 | 40 |
| Écart +1 | 111 | 122 |
| Écart +2 | 79 | 88 |
| Écart +3 | 50 | 50 |
| Écart supérieur à 3 | 47 | 44 |
| Violations bâtiment–PM | 27 | 0 |
| Orphan unlock chains | 27 | 0 |

Les 44 arêtes longues restantes ne doivent pas être supprimées mécaniquement. Elles relient principalement des fondations anciennes à des spécialisations tardives dans un arbre étendu à douze eras. Une vague ultérieure doit les classer entre arêtes justifiées et besoins réels d’intermédiaires, sans créer de technologies décoratives.

## 23. Risques

- Distribution : le socle militaire touche beaucoup de pays et doit être contrôlé manuellement.
- Contenu partagé : trois PM nécessitent une variante propre au bâtiment avant d’ajouter un gate.
- Compatibilité : les trois IDs fusionnés doivent être scannés dans les événements, journaux, sauvegardes et mods dépendants.
- Économie : les quatre petits modifiers sont des valeurs de départ, pas des valeurs validées.
- Interface : la réduction du fan-out devrait améliorer l’affichage, mais seul un runtime après chaque vague peut confirmer le routage des lignes.
- Écart d’era : `chemical_bleaching` est proposé en era 5 pour éviter une nouvelle arête négative avec `industrial_alkalis`.

## 24. Ordre d’implémentation recommandé

1. Corriger d’abord les 27 causalités bâtiment–PM, avec vérification des PM partagés.
2. Implémenter les troncs production/agriculture/mines en réutilisant uniquement les IDs existants.
3. Transformer `codified_practical_knowledge` en tronc société et ajouter les quatre modifiers faibles.
4. Ajouter séparément le nœud financier, puis revoir ses 34 grants.
5. Ajouter le nœud naval, ses 54 grants et sa disposition.
6. Ajouter le nœud militaire en dernier, avec revue manuelle de ses 138 grants.
7. Fusionner les trois nœuds vides après scan de compatibilité.
8. Appliquer seulement ensuite les quatre actions `LAYOUT_ONLY` et effectuer un runtime visuel.
9. Recalculer toute la fermeture directe/transitive et la distribution historique avant validation finale.

## Résumé final

CURRENT TREE
- roots = 39
- isolated nodes = 4
- leaf/no-effect = 7
- total edges = 317
- PM/building causal violations = 27
- >3 era edges = 47

PROPOSED TREE
- roots = 15
- isolated nodes = 0
- leaf/no-effect = 0
- total edges = 344
- PM/building causal violations = 0
- >3 era edges = 44
- new general nodes = 3
- redefined nodes = 4

DISTRIBUTION
- countries needing GAMEPLAY_ABSTRACTION grants = 154
- total added structural grants = 310
- total removed structural grants = 0

NO GAMEPLAY FILE MODIFIED  
NO COMMIT  
NO PUSH
