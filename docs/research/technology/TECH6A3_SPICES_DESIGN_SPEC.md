# TECH6A-3 — SPICES — DESIGN & IMPLEMENTATION SPECIFICATION

**Projet :** Victoria 3 — 1776 Age of Revolutions  
**Branche cible :** `tech6a3-spices-implementation`  
**Cutoff historique absolu :** `1776-01-01`  
**Vanilla autoritative :** Victoria 3 **1.13.9**  
**Statut :** design figé pour implémentation Codex — **aucune décision de balance ou de géographie ne doit être laissée à Codex**.

---

## 0. Résumé exécutable

```text
GOOD_ID = spices
GOOD_CATEGORY = luxury
BASE_PRICE = 60
TRADEABLE = yes
PRESTIGE_FACTOR = 10
CONVOY_COST_MULTIPLIER = 0.25
TRADED_QUANTITY = 10
OBSESSION_CHANCE = 3.0

BUILDING_ID = building_spice_plantation
RESOURCE_GROUP_ID = bg_spice_plantations
BASE_PMG_ID = pmg_base_building_spice_plantation

BASE_PM_OUTPUT = 20 spices
BASE_PM_EMPLOYMENT = 9000 laborers + 1000 farmers
BASE_PM_TECH_GATE = NONE

ADVANCED_PM_OUTPUT = 45 spices
ADVANCED_PM_INPUT = 5 engines
ADVANCED_PM_EMPLOYMENT = 6000 laborers + 1000 farmers + 500 machinists
ADVANCED_PM_TECH_GATE = mechanized_irrigation

POP_NEED = popneed_luxury_food
POP_WEIGHT = 2.00
POP_MAX_SUPPLY_SHARE = 0.50
POP_MIN_SUPPLY_SHARE = 0.02

FOOD_INDUSTRIES_ADDITIVE_CHAIN:
pm_spiced_food_preparations = 5 spices + 5 coffee -> 20 groceries
pm_refined_spiced_food_preparations = 10 spices + 15 coffee -> 45 groceries

RESOURCE_REGIONS_WITH_POTENTIAL = 28
STARTING_PRODUCER_REGIONS_1776 = 18
TOTAL_SPICE_POTENTIAL = 442
TOTAL_STARTING_PLANTATION_LEVELS_1776 = 87

PRESTIGE_SPICE_ASSET = generic_spices_prestige.dds
PRESTIGE_GOOD_OBJECTS = DEFERRED
STARTING_TECH_ASSIGNMENT = DEFERRED
```

---

## 1. Décisions de périmètre figées

`spices` est le **deuxième et dernier nouveau bien public V1**, après `salt`.

Il représente un panier de denrées aromatiques tropicales et subtropicales à très forte valeur :
- poivre noir/blanc ;
- clou de girofle ;
- muscade et macis ;
- cannelle/casse ;
- cardamome ;
- piment de la Jamaïque / allspice ;
- vanille ;
- aromates comparables lorsqu'ils relèvent du même commerce de luxe.

Il **ne représente pas** toutes les herbes culinaires communes ni les aromates tempérés ordinaires. L'objectif économique est un bien de luxe rare, très désiré, géographiquement concentré et historiquement structurant pour le commerce mondial.

### Contraintes non négociables
- Ne pas modifier le sel ni la Gabelle.
- Ne pas ajouter copper / industrial chemicals / cement / pharmaceuticals.
- Ne pas attribuer de starting technologies pays par pays dans TECH6A-3.
- Ne pas créer une industrie autonome dédiée aux épices.
- Ne pas recopier aveuglément la carte Basileia Romaion à 131 régions : elle sert de **référence d'architecture et de couverture**, pas d'autorité historique pour le setup 1776.
- Utiliser exclusivement les syntaxes/structures effectivement valides en vanilla 1.13.9 pour les fichiers finaux.

---

## 2. Référence Basileia Romaion auditée

La référence `AndHope/Basileia-Romaion` contient déjà un prototype cohérent :

### Good
```txt
spices = {
    texture = "gfx/interface/icons/goods_icons/spices.dds"
    cost = 60
    category = luxury
    tradeable = yes
    prestige_factor = 10
    convoy_cost_multiplier = 0.25
    traded_quantity = 10
    obsession_chance = 3.0
}
```

### Building group
```txt
bg_spices_plantations = {
    parent_group = bg_plantations
    default_building = building_spices_plantation
}
```

### Base PM Basileia
```text
15 spices
4000 laborers
800 farmers
100 clergymen
= 4900 emplois
```

### Automatic irrigation Basileia
```text
45 spices
5 engines
3000 laborers
500 machinists
800 farmers
100 clergymen
= 4400 emplois
```

### Food Industries Basileia
- `pm_sweeteners`: `goods_input_spices_add = 5`
- `pm_baking_powder`: `goods_input_spices_add = 10`
- Basileia possède aussi un `pm_spiced_food` séparé ; TECH6A-3 en reprend le principe sous la forme d'une chaîne additive distincte, avec les valeurs fixées en section 8.

### POP need Basileia
`popneed_luxury_food`: weight `1.0`, max supply share `0.25`, min `0`.

**Décision 1776 :** réutiliser les bons choix structurels dans une chaîne Food Industries séparée, mais rendre la plantation ancienne **beaucoup moins productive** et la demande POP **beaucoup plus forte**.

---

## 3. Balance du bien `spices`

### Paramètres figés

```txt
cost = 60
category = luxury
tradeable = yes
prestige_factor = 10
convoy_cost_multiplier = 0.25
traded_quantity = 10
obsession_chance = 3.0
```

### Justification
- `60` maintient un prix de base comparable aux biens de luxe élevés et reprend le prototype Basileia.
- Le prix élevé ne suffit pas : la rareté doit venir d'abord de la **faible productivité des plantations**.
- `convoy_cost_multiplier = 0.25` représente un produit de forte valeur pour un volume physique faible.
- `obsession_chance = 3.0` est cohérent avec un produit culturellement prestigieux et fortement désirable.
- Le marché doit pouvoir connaître des prix très élevés sans qu'on truque directement le prix maximal : le mécanisme doit émerger d'une demande forte et d'une offre difficile.

---

## 4. Plantation : doctrine de rendement

Le joueur a explicitement fixé le principe suivant :

> Les premières plantations d'épices doivent avoir un rendement exécrable : énormément de main-d'œuvre pour une quantité minuscule de produit.

### Comparateurs du dépôt actuel

| Plantation / PM de base | Output / niveau | Emplois / niveau | Output pour 1000 emplois |
|---|---:|---:|---:|
| Coffee | 20 | 7000 | 2.86 |
| Cotton | 45 | 8000 | 5.63 |
| Dye | 30 | 7000 | 4.29 |
| Opium | 20 | 5000 | 4.00 |
| Tea | 20 | 7000 | 2.86 |
| Tobacco | 30 | 7000 | 4.29 |
| Sugar | 25 | 10000 | 2.50 |
| Basileia spices | 15 | 4900 | 3.06 |
| **TECH6A-3 spices** | **20** | **10000** | **2.00** |

Le PM de base proposé est donc :
- ~53 % moins productif par travailleur que le tabac ;
- nettement moins productif que toutes les plantations comparées ;
- assez mauvais pour que la rareté persiste même avec des dizaines de niveaux ;
- mais pas nul au point de rendre systématiquement le bâtiment impossible à rentabiliser lorsque le prix du marché est élevé.

---

## 5. PM et PMG figés

Codex doit conserver l'architecture vanilla 1.13.9 des plantations et uniquement créer les IDs nécessaires au nouveau bâtiment.

### 5.1 PM de base

ID recommandé :
`pm_spice_cultivation`

```text
output: 20 spices
employment:
  9000 laborers
  1000 farmers
technology gate: NONE
engine input: NONE
```

**Important :** pas de gate technologique sur le PM de base. La culture du poivre, de la cannelle, de la muscade et du girofle précède largement 1776. Un gate rendrait les starting plantations incohérentes avant la future passe globale de starting technologies.

### 5.2 PM avancé

ID recommandé :
`pm_mechanized_spice_cultivation`

```text
unlocking technology: mechanized_irrigation
output: 45 spices
input: 5 engines
employment:
  6000 laborers
  1000 farmers
  500 machinists
```

Même après mécanisation :
- 7500 travailleurs restent nécessaires ;
- la plantation demeure plus intensive en travail qu'une culture industrielle banale ;
- le gain d'output est important mais ne transforme pas les épices en produit de masse.

### 5.3 PMG
ID :
`pmg_base_building_spice_plantation`

Ordre :
1. `pm_spice_cultivation`
2. `pm_mechanized_spice_cultivation`

Les PMG d'ownership / harvesting secondaires doivent reprendre **exactement** ceux utilisés par une plantation vanilla 1.13.9 comparable. Codex doit copier l'architecture, pas inventer de nouveau système de propriété.

---

## 6. Bâtiment figé

ID :
`building_spice_plantation`

Resource/building group :
`bg_spice_plantations`

Parent :
`bg_plantations`

Icône fournie par l'utilisateur :
`gfx/interface/icons/building_icons/building_spice_plantation.dds`

Good icon :
`gfx/interface/icons/goods_icons/spices.dds`

Le bâtiment doit :
- consommer l'arable resource `bg_spice_plantations` selon la syntaxe vanilla 1.13.9 ;
- être rural/agricole ;
- être compatible avec l'investissement autonome et les ownership PM standards des plantations ;
- autoriser l'esclavage uniquement si l'héritage du groupe vanilla correspondant le permet déjà ; ne pas ajouter une règle spéciale juste pour les épices ;
- ne pas recevoir de production gratuite via modifier de state.

---

## 7. Demande POP : luxe extrêmement demandé

Basileia utilisait seulement :

```txt
weight = 1.0
max_supply_share = 0.25
min_supply_share = 0
```

Pour le design 1776, cela est trop faible.

### Valeurs figées

Ajouter `spices` dans `popneed_luxury_food` :

```txt
entry = {
    goods = spices
    weight = 2.00
    max_supply_share = 0.50
    min_supply_share = 0.02
}
```

### Pourquoi
- `weight = 2.00` en fait l'un des substituts les plus désirés du panier de nourriture de luxe.
- `max_supply_share = 0.50` autorise les marchés riches et bien approvisionnés à consommer énormément d'épices.
- `min_supply_share = 0.02` crée une petite demande structurelle sans imposer un plancher mondial énorme à une ressource volontairement rare.
- Ne pas ajouter `spices` à `basic_food` : le bien doit rester un **luxe**, contrairement au sel.

Le résultat recherché est un produit dont les marchés européens/asiatiques riches cherchent activement à importer davantage, avec un prix souvent supérieur au prix de base avant expansion des plantations.

---

## 8. Productive sinks

Ajouter une chaîne de PM **indépendante et additive** au bâtiment Food Industries, en plus des chaînes de base, de mise en conserve, de distillerie et d'automatisation :

```text
pmg_spiced_food_building_food_industry:
    pm_no_spiced_food

    pm_spiced_food_preparations:
        unlocking technology: distillation
        input: 5 spices
        input: 5 coffee
        output: 20 groceries

    pm_refined_spiced_food_preparations:
        unlocking technology: baking_powder
        input: 10 spices
        input: 15 coffee
        output: 45 groceries
```

Cette chaîne est additive : elle ne remplace pas le PM de base des industries alimentaires. Elle crée un débouché industriel significatif tout en laissant les recettes existantes intactes.

### Interdictions
- Ne pas modifier les outputs actuellement équilibrés de Food Industries.
- Ne pas ajouter d'input spices directement à `pm_sweeteners` ou `pm_baking_powder`.
- Ne pas toucher aux inputs de sel existants.
- Ne pas créer `canned_food` ou une nouvelle industrie.

---

## 9. Carte 1776 : doctrine

Le CSV associé est **autoritatif** pour TECH6A-3.

Catégories :
- `A_CORE_1776` : grand centre historique avéré au cutoff, fort potentiel et starting production.
- `B_SECONDARY_1776` : production réelle/plausible commercialement en 1776, mais secondaire.
- `C_POTENTIAL_ONLY` : climat/histoire régionale justifient le potentiel, mais **starting_level_1776 = 0** pour éviter l'anachronisme.
- `D_EXCLUDE_1776` : exclusion explicite malgré une réputation moderne liée aux épices.

### Totaux cibles du CSV
```text
regions with potential = 28
starting producer regions = 18
total potential = 442
starting levels = 87
```

La concentration doit être forte :
1. Moluques ;
2. Ceylan ;
3. Malabar / Travancore ;
4. Sumatra / Aceh ;
5. péninsule malaise ;
6. pôles secondaires Java/Bornéo ;
7. exceptions américaines historiquement justifiées : Jamaica allspice, Veracruz vanilla.

### Anachronismes explicitement évités
- **Zanzibar :** aucun starting level. Le grand clou de girofle est postérieur à 1776.
- **Grenade / West Indies :** aucune muscade de départ ; la muscade est introduite à Grenade en 1843.
- **Madagascar :** potentiel climatique seulement, pas de grand centre exportateur artificiellement projeté en 1776.
- **Siam :** potentiel mais pas de production de masse au départ ; l'expansion majeure du poivre arrive surtout après le cutoff.
- **Cambodge :** pas de niveau initial sur la seule base de l'industrie poivrière du XIXe siècle.

---

## 10. Starting buildings

Codex doit créer les `building_spice_plantation` historiques correspondant **exactement** à la colonne `starting_level_1776` du CSV.

Ne jamais :
- transformer tout le potentiel en starting buildings ;
- normaliser les niveaux entre régions ;
- donner automatiquement un PM avancé ;
- ajouter des starting technologies pour rendre le PM de base disponible.

Tous les starting buildings utilisent le PM de base.

---

## 11. Prestige spices

L'utilisateur fournit :
`gfx/interface/icons/goods_icons/prestige_goods/generic_spices_prestige.dds`

### Décision TECH6A-3
**L'asset doit être installé et référencé/tenu prêt, mais les objets de prestige goods spécifiques sont différés.**

Raison :
les variantes historiquement intéressantes seraient notamment :
- Banda Nutmeg ;
- Moluccan Cloves ;
- Ceylon Cinnamon ;
- Malabar Pepper.

Mais le système de prestige goods de Victoria 3 est lié à l'architecture company/prestige appropriée. Créer quatre variantes sans une passe dédiée aux compagnies imposerait de fabriquer des déclencheurs/entreprises arbitraires.

Donc :
```text
PRESTIGE_ICON_ASSET = IMPLEMENT
PRESTIGE_GOOD_OBJECTS = DEFER
```

Codex ne doit pas inventer de compagnies ou de prestige-good conditions dans TECH6A-3.

---

## 12. Texticon

Créer un fichier propre au mod pour le texticon `spices`, indépendant de `gui/tech6a_salt_texticons.gui` (asset local La Gabelle).

Il doit pointer vers :
`gfx/interface/icons/goods_icons/spices.dds`

Le texticon doit être visible dans :
- lignes input/output de PM ;
- tooltips ;
- market UI là où le système texticon est utilisé.

---

## 13. Fichiers que Codex est autorisé à créer/modifier

Les noms exacts peuvent suivre les conventions TECH6A actuelles, mais le contenu doit respecter cette spec.

Attendus :
- good `spices` ;
- building group `bg_spice_plantations` ;
- building `building_spice_plantation` ;
- PMG `pmg_base_building_spice_plantation` ;
- PMs `pm_spice_cultivation`, `pm_mechanized_spice_cultivation` ;
- pop need luxury food ;
- chaîne additive Food Industries `pmg_spiced_food_building_food_industry` ;
- state region arable resources d'après le CSV ;
- starting buildings d'après le CSV ;
- modifier type definition `goods_output_spices_add` / `goods_input_spices_add` si nécessaire selon 1.13.9 ;
- localisation EN + FR ;
- GUI texticon propre ;
- DDS fournis par l'utilisateur.

### No-touch
- Gabelle ;
- sel ;
- France tax setup ;
- country starting technologies ;
- balance des outputs Food Industries déjà validée ;
- autres goods différés.

---

## 14. QA statique exigée de Codex

```text
SPICES_GOOD_DEFINED = YES
SPICES_BASE_PRICE = 60
SPICES_CATEGORY = luxury
SPICE_PLANTATION_DEFINED = YES
SPICE_BASE_OUTPUT = 20
SPICE_BASE_EMPLOYMENT = 10000
SPICE_ADV_OUTPUT = 45
SPICE_ADV_EMPLOYMENT = 7500
SPICES_POP_WEIGHT = 2.00
SPICES_POP_MAX_SHARE = 0.50
SPICES_POP_MIN_SHARE = 0.02
PM_SPICED_FOOD_INPUTS = 5 spices + 5 coffee
PM_SPICED_FOOD_OUTPUT = 20 groceries
PM_REFINED_SPICED_FOOD_INPUTS = 10 spices + 15 coffee
PM_REFINED_SPICED_FOOD_OUTPUT = 45 groceries
RESOURCE_REGIONS_WITH_POTENTIAL = 28
STARTING_REGIONS_1776 = 18
STARTING_LEVELS_1776 = 87
INVALID_STATE_REGION_IDS = 0
INVALID_PM_REFS = 0
INVALID_PMG_REFS = 0
INVALID_GOOD_REFS = 0
GABELLE_FILES_TOUCHED = 0
SALT_BALANCE_CHANGED = NO
STARTING_TECH_ASSIGNMENT = DEFERRED
RUNTIME = USER_REQUIRED
COMMIT = NO
PUSH = NO
```

---

## 15. Checklist runtime utilisateur

Après implémentation, vérifier :
1. `spices` visible dans le marché avec bonne icône.
2. texticon visible dans les PM.
3. plantation construisible uniquement dans les state regions du CSV avec potentiel > 0.
4. Moluques, Ceylan, Travancore, Aceh/Sumatra présents dès 1776 aux niveaux indiqués.
5. Zanzibar/Madagascar/Siam/Cambodge sans plantation initiale.
6. West Indies sans potentiel épices spécifique dans cette phase.
7. base PM : 20 output / 10 000 emplois.
8. advanced PM : 45 output / 5 engines / 7 500 emplois.
9. demande POP élevée et visible.
10. chaîne Food Industries indépendante : 5 épices + 5 café -> 20 aliments, puis 10 épices + 15 café -> 45 aliments.
11. prix initial élevé mais marché fonctionnel.
12. aucun impact sur la Gabelle et le sel.

---

## 16. Sources et références

### Référence mod / architecture
- **BR-01** — AndHope/Basileia-Romaion, commit `7d5c50035a47207f58a4c676d5f7be05e4c19973`:
  - `common/goods/br_goods.txt`
  - `common/building_groups/br_building_groups.txt`
  - `common/buildings/br_building_plantations.txt`
  - `common/production_method_groups/br_pmg_plantations.txt`
  - `common/production_methods/br_pm_agro.txt`
  - `common/production_methods/br_pm_industry.txt`
  - `common/pop_needs/br_pop_needs.txt`

### Histoire
- **HIST-01** — World History Encyclopedia, *European Discovery & Conquest of the Spice Islands*  
  https://www.worldhistory.org/article/1872/european-discovery--conquest-of-the-spice-islands/
- **HIST-02** — World History Encyclopedia, *Dutch East India Company*  
  https://www.worldhistory.org/Dutch_East_India_Company/
- **HIST-03** — Cambridge / Itinerario, *Reflections on the Arabian Seas in the Eighteenth Century* — cite environ 24 million lb de poivre Kerala/Canara vers 1760.  
  https://www.cambridge.org/core/journals/itinerario/article/reflections-on-the-arabian-seas-in-the-eighteenth-century/D494C3A529E15F12FF7B33691A182661
- **HIST-04** — Cambridge, *The Rise of the English Shipping Industry...*, East Indian Trade — poivre du Malabar comme marchandise majeure.  
  https://www.cambridge.org/core/books/abs/rise-of-the-english-shipping-industry-in-the-seventeenth-and-eighteenth-centuries/east-indian-trade/3316BBBD60BDDC23CC6D42E19797C0E9
- **HIST-05** — Cambridge, *The Acheh Treaty of 1819* — contrôle des districts poivriers du nord de Sumatra, vital pour la politique britannique fin XVIIIe.  
  https://www.cambridge.org/core/journals/journal-of-southeast-asian-history/article/abs/acheh-treaty-of-18191/066DBC3CDD502945AF2E728082C83D0E
- **HIST-06** — Cambridge, étude Matelieff — grands marchés de poivre à Banten, Palembang, Jambi, Johor, Patani, Kedah, Aceh.  
  https://www.cambridge.org/core/journals/journal-of-southeast-asian-studies/article/value-of-admiral-matelieffs-writings-for-studying-the-history-of-southeast-asia-c16001620/24224B3B48EDB0CD6DE9B5A77BACECAB
- **HIST-07** — Cambridge, *The Making and Unmaking of a Presidency: British Bencoolen* — rôle du poivre sumatranais et pénuries Malabar à la fin du XVIIIe.  
  https://www.cambridge.org/core/journals/journal-of-british-studies/article/making-and-unmaking-of-a-presidency-envisioning-empire-in-british-bencoolen-16851825/4C0CA8C6BF1E88181DA0CEACBC33C47A
- **HIST-08** — Cambridge / Itinerario, *Networks vs. the State...* — culture chinoise du poivre à Johor dans les années 1720, Bintan dès les années 1760; Siam surtout années 1790+.  
  https://www.cambridge.org/core/journals/itinerario/article/networks-vs-the-state-or-all-under-heaven-chinese-migrants-technological-circulation-and-the-early-modern-qing-empire/F833CFA8E489D1AE6080DCF7E025749E
- **HIST-09** — Kew, *Pimenta dioica* — allspice indigène Amérique centrale/Caraïbes, surtout cultivé/exporté de Jamaïque.  
  https://powo.science.kew.org/taxon/urn:lsid:ipni.org:names:196799-2/general-information
- **HIST-10** — University of the West Indies — Jamaica historiquement grand producteur de pimento/allspice.  
  https://www.mona.uwi.edu/principal/sites/default/files/principal/development/abstracts/2007/new-initiatives.pdf
- **HIST-11** — Smithsonian Institution, *Vanilla planifolia* — plus ancienne preuve historique de culture vers 1760 par les Totonaques à Papantla, Veracruz.  
  https://www.si.edu/object/vanilla-planifolia:ofeo-sg_2007-0281C
- **HIST-12** — Cambridge, *History and Sociology of the Chinese in Cambodia Prior to the French Protectorate* — prudence: grand poivre de Kampot clairement attesté plus tard, donc potentiel sans départ 1776.  
  https://www.cambridge.org/core/journals/journal-of-southeast-asian-history/article/abs/history-and-sociology-of-the-chinese-in-cambodia-prior-to-the-french-protectorate/EEA08E57942DC5116776CCE2FE0B01B5
- **HIST-13** — Cambridge, *Anglo-French Rivalry in Southeast Asia 1763–93* — commerce des épices de l'archipel et réseaux vers Siam/Tonkin.  
  https://www.cambridge.org/core/journals/journal-of-southeast-asian-studies/article/abs/anglofrench-rivalry-in-southeast-asia-176393-some-repercussions/9806035589F5E53AE8D5897FD81BBA35
- **HIST-14** — World History Encyclopedia / Met Museum — diffusion postérieure des clous de girofle vers Zanzibar; ne pas rétroprojeter le boom du XIXe en 1776.  
  https://www.worldhistory.org/article/1872/european-discovery--conquest-of-the-spice-islands/  
  https://www.metmuseum.org/de/exhibitions/arts-of-africa/inside-the-exhibition
- **HIST-15** — Gouvernement de Grenade, Compendium Agriculture — muscade introduite à Grenade en **1843**.  
  https://stats.gov.gd/wp-content/uploads/2021/04/Compendium-2020-Final.pdf

---

## 17. Note pour Codex

Ce document et `TECH6A3_SPICES_RESOURCE_MAP.csv` sont des **spécifications d'implémentation**, pas une invitation à ré-auditer le design.

Codex doit :
1. inspecter le vanilla 1.13.9 uniquement pour reproduire la **syntaxe valide** et les chemins exacts ;
2. appliquer les nombres, IDs fonctionnels, PM balance, besoins POP et carte décidés ici ;
3. signaler toute impossibilité technique réelle avant de substituer une autre architecture ;
4. ne pas « améliorer » les valeurs de rendement ou de demande ;
5. ne pas ajouter de régions au CSV sans validation utilisateur.
