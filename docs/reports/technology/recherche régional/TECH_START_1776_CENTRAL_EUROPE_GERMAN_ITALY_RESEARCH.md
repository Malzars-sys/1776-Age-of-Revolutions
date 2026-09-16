# Recherche technologique — Europe centrale, monde germanique et Italie — 1er janvier 1776

> **Statut du document : recherche uniquement.** Aucun fichier de gameplay n’est modifié, aucun code Victoria 3 n’est produit. La date de coupure est strictement le **1776-01-01**.

## 1. Périmètre

**41 TAG** du CSV pays entrent dans ce périmètre: 30 pour l’Europe centrale/monde germanique et 11 pour l’Italie. Les TAG espagnols/portugais/maltais classés « Southern Europe » dans le CSV sont exclus conformément à la consigne.

### Monde germanique / Europe centrale

- `ANH` — Anhalt
- `AUS` — Austria
- `BAD` — Baden
- `BAV` — Bavaria
- `BRA` — Brunswick
- `BRE` — Bremen
- `COB` — Saxe-Coburg-Gotha
- `FRM` — Frankfurt
- `HAM` — Hamburg
- `HAN` — Hanover
- `HEK` — Hesse-Kassel
- `HES` — Hesse
- `HOH` — Hohenzollern
- `HOL` — Holstein
- `LIP` — Lippe
- `LUB` — Lübeck
- `MEC` — Mecklenburg
- `MEI` — Saxe-Meiningen
- `MST` — Mecklenburg-Strelitz
- `NAS` — Nassau
- `OLD` — Oldenburg
- `PRU` — Prussia
- `SAX` — Saxony
- `SCH` — Schleswig
- `SCM` — Schaumburg-Lippe
- `SCW` — Schwarzburg
- `SWI` — Switzerland
- `WEI` — Saxe-Weimar
- `WLD` — Waldeck
- `WUR` — Württemberg

### Italie

- `GEN` — Most Serene Republic of Genoa
- `GR3` — Sicily
- `GR4` — Naples
- `LUC` — Lucca
- `MOD` — Modena
- `PAP` — Rome
- `PAR` — Parma
- `SAR` — Sardinia-Piedmont
- `SIC` — Two Sicilies
- `TUS` — Tuscany
- `VEN` — Venice

**Attention de setup :** le CSV contient simultanément `GR3` (Sicily), `GR4` (Naples) et `SIC` (Two Sicilies). Ils sont donc traités séparément. Les institutions napolitaines ne sont pas copiées automatiquement vers `GR3`.

## 2. Méthode et sources

- Les CSV joints font autorité pour les TAG, IDs technologiques, tiers, explicites, prérequis et effets gameplay. Aucun ID extérieur à `TECH_START_1776_TECHNOLOGIES.csv` n’est recommandé.
- Une technologie n’est retenue que si la capacité qu’elle représente dans le gameplay est historiquement disponible au cutoff; une invention ou un établissement isolé est noté `SECTORAL`/`FRONTIER` lorsque sa diffusion est limitée.
- Les prérequis manquants ne sont jamais ajoutés mécaniquement. Les incohérences arbre/réalité sont signalées dans `Prerequisite_Note`.
- Les sources privilégiées sont universités, publications académiques, musées techniques, archives/encyclopédies historiques et institutions patrimoniales. Les URL complètes sont conservées dans la matrice CSV.

### Références principales

- <https://www.cambridge.org/core/journals/journal-of-economic-history/article/economic-growth-in-germany-15001850/3FB21F575B6056CE6BCFF04C97FC1E49>
- <https://www.cambridge.org/core/books/abs/cultures-of-power-in-europe-during-the-long-eighteenth-century/military-culture-in-the-reich-c-16801806/F52FD6774258813E7A482606C91377B9>
- <https://www.cambridge.org/core/books/abs/globalized-peripheries/linen-and-merchants-from-the-duchy-of-berg-lower-saxony-and-westphalia-and-their-global-trade-in-eighteenthcentury-london/8C3BFA133DB7FDE29BE7CED56AB0662E>
- <https://cp.tu-berlin.de/history>
- <https://www.bundeswehr.de/en/organization/army/structure/branches/artillery>
- <https://dbmuseum.de/en/nuremberg/exhibitions/the-history-of-the-railway-in-germany>
- <https://82nd-and-fifth.metmuseum.org/toah/ht/10/euwc.html>
- <https://ww1.habsburger.net/en/chapters/theresian-reforms-battle-koeniggraetz>
- <https://doi.org/10.12987/yale/9780300178586.003.0005>
- <https://whc.unesco.org/en/list/618>
- <https://www.tandfonline.com/doi/full/10.1080/17581206.2024.2437551>
- <https://tu-freiberg.de/en/university/history>
- <https://books.fupress.com/chapter/promotion-of-high-quality-textiles-by-prize-competitions-during-the-enlightenment-in-saxony-from-raw/13603>
- <https://hls-dhs-dss.ch/de/articles/013931/2010-03-31/>
- <https://hls-dhs-dss.ch/fr/articles/008683/2008-06-05/>
- <https://www.treccani.it/enciclopedia/italia_(Dizionario-di-Storia)/>
- <https://www.treccani.it/enciclopedia/pietro-leopoldo-d-asburgo-lorena-granduca-di-toscana-poi-imperatore-del-sacro-romano-impero-come-leopoldo-ii_(Dizionario-Biografico)/>
- <https://www.museotorino.it/view/s/276a506f80994a3a943a5600e4b944ce>
- <https://en.chateauversailles.fr/royal-silks-europe/consortium-royal-residences-savoy>
- <https://www.treccani.it/enciclopedia/l-arsenale-di-venezia-e-i-cantieri-navali-della-marina_(Il-Contributo-italiano-alla-storia-del-Pensiero%3A-Tecnica)/>
- <https://www.research.unipd.it/handle/11577/1559630>
- <https://museo.accademialigustica.it/storia/>
- <https://www.museidigenova.it/en/textured-and-embroidered-fabrics>
- <https://www.esercito.difesa.it/en/organization/the-chief-of-general-staff-of-the-army/training-specialization-and-doctrine-command/training-command-and-application-school-of-the-army/military-academy/nunziatella/history-and-traditions/124245.html>
- <https://www.cambridge.org/core/books/abs/naples-in-the-eighteenth-century/arrogance-of-the-market-the-economy-of-the-kingdom-between-the-mediterranean-and-europe/E275AD8133C1ABA8555C21B6441255AC>

## 3. Diagnostic régional

Le principal résultat est l’**asymétrie**. La Prusse et l’Autriche possèdent des appareils militaires et administratifs beaucoup plus systématiques que la majorité des petits États du Reich. La Saxe se distingue par les mines, l’enseignement minier et les manufactures; le Wurtemberg par une proto-industrie textile exportatrice; le Hanovre par le Harz; Hesse-Kassel et Brunswick par des armées professionnelles visibles dès 1776. À l’inverse, les villes libres et de nombreuses principautés ne peuvent pas recevoir automatiquement toute la composante militaire/minière du tier 4.

La Suisse illustre encore mieux le problème d’un tier uniforme: ses régions textiles et horlogères sont économiquement sophistiquées, mais l’organisation militaire reste cantonale et la mécanisation textile industrielle appartient au tournant du XIXe siècle. Un setup explicite est donc préférable à une baisse ou hausse globale de tier.

En Italie, les écarts sont de nature différente. Le Piémont-Sardaigne dispose d’écoles d’artillerie/fortification et d’une industrie de la soie de premier ordre; Venise conserve l’Arsenal et une tradition manufacturière/navale; la Toscane est particulièrement avancée dans la réforme administrative, fiscale et agricole; Naples possède des académies militaires spécialisées; Gênes combine soie et école d’architecture. Les petits duchés, les États pontificaux et la Sicile séparée demandent des setups plus ciblés.

## 4. Analyse pays par pays

### ANH — Anhalt

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies frontière/sectorielles:** `light_infantry_tactics (FRONTIER)`, `regulated_small_arms (SECTORAL)`, `shaft_mining (SECTORAL)`, `standardized_field_artillery (FRONTIER)`
- **Prérequis problématiques:** codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft
- **Justification historique:** Principauté allemande de taille réduite: les sources sur le Reich montrent une grande diversité des armées, des administrations et des manufactures. Il ne faut pas déduire les technologies prussiennes du seul voisinage culturel; les nœuds militaires/miniers de frontière sont donc revus séparément.
- **Sources:** <https://www.amrevmuseum.org/germany-and-the-american-revolution> ; <https://www.cambridge.org/core/books/abs/cultures-of-power-in-europe-during-the-long-eighteenth-century/military-culture-in-the-reich-c-16801806/F52FD6774258813E7A482606C91377B9>
- **Confiance générale:** MEDIUM

### AUS — Austria

- **Current tier:** `tier_4`
- **Tier action:** `KEEP_TIER`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `light_infantry_tactics`, `organized_textile_production`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`, `systematic_administrative_statistics`, `urbanization`, `specialized_technical_academies`
- **Technologies à ADD:** `atmospheric_engine`, `scientific_fortification_siegecraft`
- **Technologies à REMOVE:** `romanticism`
- **Technologies à REVIEW:** `systematic_legal_codification`
- **Technologies frontière/sectorielles:** `light_infantry_tactics (FRONTIER)`, `systematic_legal_codification (FRONTIER)`, `atmospheric_engine (SECTORAL)`
- **Prérequis problématiques:** codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft | romanticism <- institutionalized_scientific_exchange | specialized_technical_academies <- institutionalized_scientific_exchange | `atmospheric_engine` resterait sans `coke_smelting`: divergence historiquement justifiée, à tolérer.
- **Justification historique:** Monarchie habsbourgeoise à forte capacité administrative et militaire, mais très hétérogène territorialement. Les réformes thérésiennes, l’artillerie, l’enseignement technique minier et l’exploitation minière avancée sont solides; `romanticism` est à retirer. Le moteur atmosphérique est réel mais sectoriel dans les terres habsbourgeoises et son rattachement au seul TAG AUS reste une abstraction de carte.
- **Sources:** <https://ww1.habsburger.net/en/chapters/theresian-reforms-battle-koeniggraetz> ; <https://doi.org/10.12987/yale/9780300178586.003.0005>
- **Confiance générale:** HIGH

### BAD — Baden

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies frontière/sectorielles:** `light_infantry_tactics (FRONTIER)`, `regulated_small_arms (SECTORAL)`, `shaft_mining (SECTORAL)`, `standardized_field_artillery (FRONTIER)`
- **Prérequis problématiques:** codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft
- **Justification historique:** État du sud-ouest germanique: agriculture, artisanat et proto-industrie peuvent être substantiels, mais les structures militaires et scientifiques ne doivent pas être automatiquement alignées sur Prusse/Autriche. Le setup est évalué fonction par fonction.
- **Sources:** <https://www.cambridge.org/core/journals/journal-of-economic-history/article/economic-growth-in-germany-15001850/3FB21F575B6056CE6BCFF04C97FC1E49> ; <https://www.cambridge.org/core/books/abs/cultures-of-power-in-europe-during-the-long-eighteenth-century/military-culture-in-the-reich-c-16801806/F52FD6774258813E7A482606C91377B9>
- **Confiance générale:** MEDIUM

### BAV — Bavaria

- **Current tier:** `tier_4`
- **Tier action:** `KEEP_TIER`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `light_infantry_tactics`, `organized_textile_production`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** —
- **Technologies frontière/sectorielles:** `light_infantry_tactics (FRONTIER)`, `regulated_small_arms (SECTORAL)`, `shaft_mining (SECTORAL)`, `standardized_field_artillery (FRONTIER)`
- **Prérequis problématiques:** codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft
- **Justification historique:** État du sud-ouest germanique: agriculture, artisanat et proto-industrie peuvent être substantiels, mais les structures militaires et scientifiques ne doivent pas être automatiquement alignées sur Prusse/Autriche. Le setup est évalué fonction par fonction.
- **Sources:** <https://www.cambridge.org/core/journals/journal-of-economic-history/article/economic-growth-in-germany-15001850/3FB21F575B6056CE6BCFF04C97FC1E49> ; <https://www.cambridge.org/core/books/abs/cultures-of-power-in-europe-during-the-long-eighteenth-century/military-culture-in-the-reich-c-16801806/F52FD6774258813E7A482606C91377B9>
- **Confiance générale:** MEDIUM

### BRA — Brunswick

- **Current tier:** `tier_4`
- **Tier action:** `KEEP_TIER`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `light_infantry_tactics`, `organized_textile_production`, `regulated_small_arms`, `shaft_mining`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `railways`
- **Technologies à REVIEW:** `standardized_field_artillery`
- **Technologies frontière/sectorielles:** `light_infantry_tactics (FRONTIER)`, `regulated_small_arms (SECTORAL)`, `shaft_mining (SECTORAL)`, `standardized_field_artillery (FRONTIER)`
- **Prérequis problématiques:** codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | railways <- high_pressure_steam,professional_civil_engineering,puddling_and_rolling | regulated_small_arms <- scientific_fortification_siegecraft
- **Justification historique:** Brunswick dispose d’un appareil militaire réel — ses troupes participent à la guerre d’Amérique à partir de 1776 — mais `railways` est un anachronisme absolu. La première ligne publique allemande n’ouvre qu’en 1835.
- **Sources:** <https://www.amrevmuseum.org/germany-and-the-american-revolution> ; <https://www.cambridge.org/core/books/abs/cultures-of-power-in-europe-during-the-long-eighteenth-century/military-culture-in-the-reich-c-16801806/F52FD6774258813E7A482606C91377B9>
- **Confiance générale:** HIGH

### BRE — Bremen

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies frontière/sectorielles:** `light_infantry_tactics (FRONTIER)`, `regulated_small_arms (SECTORAL)`, `shaft_mining (SECTORAL)`, `standardized_field_artillery (FRONTIER)`
- **Prérequis problématiques:** codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft
- **Justification historique:** Ville libre du Saint-Empire: administration urbaine, commerce et artisanats peuvent être développés sans qu’existent pour autant les mêmes arsenaux, mines et institutions militaires qu’en Prusse. Le tier 4 est donc remplacé par un setup explicite.
- **Sources:** <https://www.cambridge.org/core/journals/journal-of-economic-history/article/economic-growth-in-germany-15001850/3FB21F575B6056CE6BCFF04C97FC1E49> ; <https://www.cambridge.org/core/books/abs/cultures-of-power-in-europe-during-the-long-eighteenth-century/military-culture-in-the-reich-c-16801806/F52FD6774258813E7A482606C91377B9>
- **Confiance générale:** MEDIUM

### COB — Saxe-Coburg-Gotha

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies frontière/sectorielles:** `light_infantry_tactics (FRONTIER)`, `regulated_small_arms (SECTORAL)`, `shaft_mining (SECTORAL)`, `standardized_field_artillery (FRONTIER)`
- **Prérequis problématiques:** codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft
- **Justification historique:** Petit État thuringien/saxon situé dans une zone d’artisanat et de manufactures, mais distinct du puissant électorat de Saxe. Les capacités civiles de base sont plausibles; les nœuds militaires de frontière et la mine doivent rester explicites/à vérifier.
- **Sources:** <https://www.cambridge.org/core/journals/journal-of-economic-history/article/economic-growth-in-germany-15001850/3FB21F575B6056CE6BCFF04C97FC1E49> ; <https://www.cambridge.org/core/books/abs/cultures-of-power-in-europe-during-the-long-eighteenth-century/military-culture-in-the-reich-c-16801806/F52FD6774258813E7A482606C91377B9>
- **Confiance générale:** MEDIUM

### FRM — Frankfurt

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies frontière/sectorielles:** `light_infantry_tactics (FRONTIER)`, `regulated_small_arms (SECTORAL)`, `shaft_mining (SECTORAL)`, `standardized_field_artillery (FRONTIER)`
- **Prérequis problématiques:** codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft
- **Justification historique:** Ville libre du Saint-Empire: administration urbaine, commerce et artisanats peuvent être développés sans qu’existent pour autant les mêmes arsenaux, mines et institutions militaires qu’en Prusse. Le tier 4 est donc remplacé par un setup explicite.
- **Sources:** <https://www.cambridge.org/core/journals/journal-of-economic-history/article/economic-growth-in-germany-15001850/3FB21F575B6056CE6BCFF04C97FC1E49> ; <https://www.cambridge.org/core/books/abs/cultures-of-power-in-europe-during-the-long-eighteenth-century/military-culture-in-the-reich-c-16801806/F52FD6774258813E7A482606C91377B9>
- **Confiance générale:** MEDIUM

### GEN — Most Serene Republic of Genoa

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`, `specialized_technical_academies`
- **Technologies à ADD:** `scientific_fortification_siegecraft`
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies frontière/sectorielles:** `light_infantry_tactics (FRONTIER)`, `regulated_small_arms (SECTORAL)`, `shaft_mining (SECTORAL)`, `standardized_field_artillery (FRONTIER)`, `specialized_technical_academies (SECTORAL)`, `scientific_fortification_siegecraft (SECTORAL)`
- **Prérequis problématiques:** codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft | specialized_technical_academies <- institutionalized_scientific_exchange
- **Justification historique:** Gênes conserve une forte tradition textile de soie et fonde l’Accademia Ligustica en 1751, avec architecture civile et militaire. En revanche l’appareil militaire terrestre de type prussien n’est pas suffisamment démontré pour conserver tout le paquet tier 4 sans examen explicite.
- **Sources:** <https://museo.accademialigustica.it/storia/> ; <https://www.museidigenova.it/en/textured-and-embroidered-fabrics>
- **Confiance générale:** HIGH

### GR3 — Sicily

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies frontière/sectorielles:** `light_infantry_tactics (FRONTIER)`, `regulated_small_arms (SECTORAL)`, `shaft_mining (SECTORAL)`, `standardized_field_artillery (FRONTIER)`
- **Prérequis problématiques:** codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft
- **Justification historique:** La Sicile distincte ne doit pas hériter automatiquement des académies napolitaines simplement parce que SIC/GR4 les possèdent dans la réalité bourbonienne. Le tier générique surévalue probablement certains nœuds militaires/miniers: setup explicite recommandé.
- **Sources:** <https://www.treccani.it/enciclopedia/italia_(Dizionario-di-Storia)/> ; <https://en.chateauversailles.fr/news/exhibitions/royal-silks-europe>
- **Confiance générale:** MEDIUM

### GR4 — Naples

- **Current tier:** `tier_4`
- **Tier action:** `KEEP_TIER`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `light_infantry_tactics`, `organized_textile_production`, `regulated_small_arms`, `standardized_field_artillery`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** `scientific_fortification_siegecraft`, `specialized_technical_academies`
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `shaft_mining`, `state_dockyard_systems`
- **Technologies frontière/sectorielles:** `light_infantry_tactics (FRONTIER)`, `regulated_small_arms (SECTORAL)`, `shaft_mining (SECTORAL)`, `state_dockyard_systems (SECTORAL)`
- **Prérequis problématiques:** codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft
- **Justification historique:** Naples dispose avant 1776 d’une série d’académies d’artillerie, de génie et d’officiers; cela justifie des capacités militaires techniques explicites. L’économie reste plus agricole et commerciale que proto-industrielle uniforme. L’arsenal naval existe mais la grande modernisation de Castellammare est postérieure.
- **Sources:** <https://www.esercito.difesa.it/en/organization/the-chief-of-general-staff-of-the-army/training-specialization-and-doctrine-command/training-command-and-application-school-of-the-army/military-academy/nunziatella/history-and-traditions/124245.html> ; <https://www.cambridge.org/core/books/abs/naples-in-the-eighteenth-century/arrogance-of-the-market-the-economy-of-the-kingdom-between-the-mediterranean-and-europe/E275AD8133C1ABA8555C21B6441255AC>
- **Confiance générale:** HIGH

### HAM — Hamburg

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies frontière/sectorielles:** `light_infantry_tactics (FRONTIER)`, `regulated_small_arms (SECTORAL)`, `shaft_mining (SECTORAL)`, `standardized_field_artillery (FRONTIER)`
- **Prérequis problématiques:** codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft
- **Justification historique:** Ville libre du Saint-Empire: administration urbaine, commerce et artisanats peuvent être développés sans qu’existent pour autant les mêmes arsenaux, mines et institutions militaires qu’en Prusse. Le tier 4 est donc remplacé par un setup explicite.
- **Sources:** <https://www.cambridge.org/core/journals/journal-of-economic-history/article/economic-growth-in-germany-15001850/3FB21F575B6056CE6BCFF04C97FC1E49> ; <https://www.cambridge.org/core/books/abs/cultures-of-power-in-europe-during-the-long-eighteenth-century/military-culture-in-the-reich-c-16801806/F52FD6774258813E7A482606C91377B9>
- **Confiance générale:** MEDIUM

### HAN — Hanover

- **Current tier:** `tier_4`
- **Tier action:** `KEEP_TIER`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `light_infantry_tactics`, `organized_textile_production`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** —
- **Technologies frontière/sectorielles:** `light_infantry_tactics (FRONTIER)`, `regulated_small_arms (SECTORAL)`, `standardized_field_artillery (FRONTIER)`
- **Prérequis problématiques:** codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft
- **Justification historique:** Le Hanovre combine État territorial, armée et tradition minière du Harz. La mine justifie mieux `shaft_mining` que dans de nombreux petits États voisins; les nœuds militaires de frontière restent moins assurés que pour Prusse/Autriche.
- **Sources:** <https://www.uni-hannover.de/en/universitaet/profil/leibniz/gottfried-in-a-nutshell/gottfried-in-a-nutshell-10> ; <https://www.cambridge.org/core/books/abs/globalized-peripheries/linen-and-merchants-from-the-duchy-of-berg-lower-saxony-and-westphalia-and-their-global-trade-in-eighteenthcentury-london/8C3BFA133DB7FDE29BE7CED56AB0662E>
- **Confiance générale:** HIGH

### HEK — Hesse-Kassel

- **Current tier:** `tier_4`
- **Tier action:** `KEEP_TIER`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `light_infantry_tactics`, `organized_textile_production`, `regulated_small_arms`, `standardized_field_artillery`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `shaft_mining`
- **Technologies frontière/sectorielles:** `light_infantry_tactics (FRONTIER)`, `regulated_small_arms (SECTORAL)`, `shaft_mining (SECTORAL)`, `standardized_field_artillery (FRONTIER)`
- **Prérequis problématiques:** codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft
- **Justification historique:** Hesse-Kassel possède un appareil militaire exceptionnellement important pour sa taille et fournit des troupes professionnelles à la Grande-Bretagne en 1776. Les capacités militaires de base sont donc plus plausibles ici que dans la plupart des micro-États allemands.
- **Sources:** <https://www.amrevmuseum.org/germany-and-the-american-revolution> ; <https://www.cambridge.org/core/books/abs/cultures-of-power-in-europe-during-the-long-eighteenth-century/military-culture-in-the-reich-c-16801806/F52FD6774258813E7A482606C91377B9>
- **Confiance générale:** HIGH

### HES — Hesse

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies frontière/sectorielles:** `light_infantry_tactics (FRONTIER)`, `regulated_small_arms (SECTORAL)`, `shaft_mining (SECTORAL)`, `standardized_field_artillery (FRONTIER)`
- **Prérequis problématiques:** codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft
- **Justification historique:** Principauté allemande de taille réduite: les sources sur le Reich montrent une grande diversité des armées, des administrations et des manufactures. Il ne faut pas déduire les technologies prussiennes du seul voisinage culturel; les nœuds militaires/miniers de frontière sont donc revus séparément.
- **Sources:** <https://www.cambridge.org/core/journals/journal-of-economic-history/article/economic-growth-in-germany-15001850/3FB21F575B6056CE6BCFF04C97FC1E49> ; <https://www.cambridge.org/core/books/abs/cultures-of-power-in-europe-during-the-long-eighteenth-century/military-culture-in-the-reich-c-16801806/F52FD6774258813E7A482606C91377B9>
- **Confiance générale:** MEDIUM

### HOH — Hohenzollern

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies frontière/sectorielles:** `light_infantry_tactics (FRONTIER)`, `regulated_small_arms (SECTORAL)`, `shaft_mining (SECTORAL)`, `standardized_field_artillery (FRONTIER)`
- **Prérequis problématiques:** codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft
- **Justification historique:** État du sud-ouest germanique: agriculture, artisanat et proto-industrie peuvent être substantiels, mais les structures militaires et scientifiques ne doivent pas être automatiquement alignées sur Prusse/Autriche. Le setup est évalué fonction par fonction.
- **Sources:** <https://www.cambridge.org/core/journals/journal-of-economic-history/article/economic-growth-in-germany-15001850/3FB21F575B6056CE6BCFF04C97FC1E49> ; <https://www.cambridge.org/core/books/abs/cultures-of-power-in-europe-during-the-long-eighteenth-century/military-culture-in-the-reich-c-16801806/F52FD6774258813E7A482606C91377B9>
- **Confiance générale:** MEDIUM

### HOL — Holstein

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies frontière/sectorielles:** `light_infantry_tactics (FRONTIER)`, `regulated_small_arms (SECTORAL)`, `shaft_mining (SECTORAL)`, `standardized_field_artillery (FRONTIER)`
- **Prérequis problématiques:** codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft
- **Justification historique:** Principauté allemande de taille réduite: les sources sur le Reich montrent une grande diversité des armées, des administrations et des manufactures. Il ne faut pas déduire les technologies prussiennes du seul voisinage culturel; les nœuds militaires/miniers de frontière sont donc revus séparément.
- **Sources:** <https://www.cambridge.org/core/journals/journal-of-economic-history/article/economic-growth-in-germany-15001850/3FB21F575B6056CE6BCFF04C97FC1E49> ; <https://www.cambridge.org/core/books/abs/cultures-of-power-in-europe-during-the-long-eighteenth-century/military-culture-in-the-reich-c-16801806/F52FD6774258813E7A482606C91377B9>
- **Confiance générale:** MEDIUM

### LIP — Lippe

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies frontière/sectorielles:** `light_infantry_tactics (FRONTIER)`, `regulated_small_arms (SECTORAL)`, `shaft_mining (SECTORAL)`, `standardized_field_artillery (FRONTIER)`
- **Prérequis problématiques:** codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft
- **Justification historique:** Principauté allemande de taille réduite: les sources sur le Reich montrent une grande diversité des armées, des administrations et des manufactures. Il ne faut pas déduire les technologies prussiennes du seul voisinage culturel; les nœuds militaires/miniers de frontière sont donc revus séparément.
- **Sources:** <https://www.cambridge.org/core/journals/journal-of-economic-history/article/economic-growth-in-germany-15001850/3FB21F575B6056CE6BCFF04C97FC1E49> ; <https://www.cambridge.org/core/books/abs/cultures-of-power-in-europe-during-the-long-eighteenth-century/military-culture-in-the-reich-c-16801806/F52FD6774258813E7A482606C91377B9>
- **Confiance générale:** MEDIUM

### LUB — Lübeck

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies frontière/sectorielles:** `light_infantry_tactics (FRONTIER)`, `regulated_small_arms (SECTORAL)`, `shaft_mining (SECTORAL)`, `standardized_field_artillery (FRONTIER)`
- **Prérequis problématiques:** codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft
- **Justification historique:** Ville libre du Saint-Empire: administration urbaine, commerce et artisanats peuvent être développés sans qu’existent pour autant les mêmes arsenaux, mines et institutions militaires qu’en Prusse. Le tier 4 est donc remplacé par un setup explicite.
- **Sources:** <https://www.cambridge.org/core/journals/journal-of-economic-history/article/economic-growth-in-germany-15001850/3FB21F575B6056CE6BCFF04C97FC1E49> ; <https://www.cambridge.org/core/books/abs/cultures-of-power-in-europe-during-the-long-eighteenth-century/military-culture-in-the-reich-c-16801806/F52FD6774258813E7A482606C91377B9>
- **Confiance générale:** MEDIUM

### LUC — Lucca

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies frontière/sectorielles:** `light_infantry_tactics (FRONTIER)`, `regulated_small_arms (SECTORAL)`, `shaft_mining (SECTORAL)`, `standardized_field_artillery (FRONTIER)`
- **Prérequis problématiques:** codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft
- **Justification historique:** Lucca est une petite république marchande et manufacturière avec une longue tradition textile; sa taille politique ne doit pas effacer ses capacités artisanales, mais elle ne justifie pas le paquet militaire/minier complet du tier 4.
- **Sources:** <https://www.treccani.it/enciclopedia/italia_(Dizionario-di-Storia)/> ; <https://en.chateauversailles.fr/news/exhibitions/royal-silks-europe>
- **Confiance générale:** MEDIUM

### MEC — Mecklenburg

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies frontière/sectorielles:** `light_infantry_tactics (FRONTIER)`, `regulated_small_arms (SECTORAL)`, `shaft_mining (SECTORAL)`, `standardized_field_artillery (FRONTIER)`
- **Prérequis problématiques:** codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft
- **Justification historique:** Principauté allemande de taille réduite: les sources sur le Reich montrent une grande diversité des armées, des administrations et des manufactures. Il ne faut pas déduire les technologies prussiennes du seul voisinage culturel; les nœuds militaires/miniers de frontière sont donc revus séparément.
- **Sources:** <https://www.cambridge.org/core/journals/journal-of-economic-history/article/economic-growth-in-germany-15001850/3FB21F575B6056CE6BCFF04C97FC1E49> ; <https://www.cambridge.org/core/books/abs/cultures-of-power-in-europe-during-the-long-eighteenth-century/military-culture-in-the-reich-c-16801806/F52FD6774258813E7A482606C91377B9>
- **Confiance générale:** MEDIUM

### MEI — Saxe-Meiningen

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies frontière/sectorielles:** `light_infantry_tactics (FRONTIER)`, `regulated_small_arms (SECTORAL)`, `shaft_mining (SECTORAL)`, `standardized_field_artillery (FRONTIER)`
- **Prérequis problématiques:** codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft
- **Justification historique:** Petit État thuringien/saxon situé dans une zone d’artisanat et de manufactures, mais distinct du puissant électorat de Saxe. Les capacités civiles de base sont plausibles; les nœuds militaires de frontière et la mine doivent rester explicites/à vérifier.
- **Sources:** <https://www.cambridge.org/core/journals/journal-of-economic-history/article/economic-growth-in-germany-15001850/3FB21F575B6056CE6BCFF04C97FC1E49> ; <https://www.cambridge.org/core/books/abs/cultures-of-power-in-europe-during-the-long-eighteenth-century/military-culture-in-the-reich-c-16801806/F52FD6774258813E7A482606C91377B9>
- **Confiance générale:** MEDIUM

### MOD — Modena

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies frontière/sectorielles:** `light_infantry_tactics (FRONTIER)`, `regulated_small_arms (SECTORAL)`, `shaft_mining (SECTORAL)`, `standardized_field_artillery (FRONTIER)`
- **Prérequis problématiques:** codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft
- **Justification historique:** Modène possède des institutions d’Ancien Régime et des activités artisanales/manufacturières, mais les technologies militaires et minières de frontière ne doivent pas être inférées du seul tier. Setup explicite.
- **Sources:** <https://www.treccani.it/enciclopedia/italia_(Dizionario-di-Storia)/> ; <https://en.chateauversailles.fr/news/exhibitions/royal-silks-europe>
- **Confiance générale:** MEDIUM

### MST — Mecklenburg-Strelitz

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies frontière/sectorielles:** `light_infantry_tactics (FRONTIER)`, `regulated_small_arms (SECTORAL)`, `shaft_mining (SECTORAL)`, `standardized_field_artillery (FRONTIER)`
- **Prérequis problématiques:** codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft
- **Justification historique:** Principauté allemande de taille réduite: les sources sur le Reich montrent une grande diversité des armées, des administrations et des manufactures. Il ne faut pas déduire les technologies prussiennes du seul voisinage culturel; les nœuds militaires/miniers de frontière sont donc revus séparément.
- **Sources:** <https://www.cambridge.org/core/journals/journal-of-economic-history/article/economic-growth-in-germany-15001850/3FB21F575B6056CE6BCFF04C97FC1E49> ; <https://www.cambridge.org/core/books/abs/cultures-of-power-in-europe-during-the-long-eighteenth-century/military-culture-in-the-reich-c-16801806/F52FD6774258813E7A482606C91377B9>
- **Confiance générale:** MEDIUM

### NAS — Nassau

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies frontière/sectorielles:** `light_infantry_tactics (FRONTIER)`, `regulated_small_arms (SECTORAL)`, `shaft_mining (SECTORAL)`, `standardized_field_artillery (FRONTIER)`
- **Prérequis problématiques:** codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft
- **Justification historique:** Principauté allemande de taille réduite: les sources sur le Reich montrent une grande diversité des armées, des administrations et des manufactures. Il ne faut pas déduire les technologies prussiennes du seul voisinage culturel; les nœuds militaires/miniers de frontière sont donc revus séparément.
- **Sources:** <https://www.cambridge.org/core/journals/journal-of-economic-history/article/economic-growth-in-germany-15001850/3FB21F575B6056CE6BCFF04C97FC1E49> ; <https://www.cambridge.org/core/books/abs/cultures-of-power-in-europe-during-the-long-eighteenth-century/military-culture-in-the-reich-c-16801806/F52FD6774258813E7A482606C91377B9>
- **Confiance générale:** MEDIUM

### OLD — Oldenburg

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies frontière/sectorielles:** `light_infantry_tactics (FRONTIER)`, `regulated_small_arms (SECTORAL)`, `shaft_mining (SECTORAL)`, `standardized_field_artillery (FRONTIER)`
- **Prérequis problématiques:** codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft
- **Justification historique:** Principauté allemande de taille réduite: les sources sur le Reich montrent une grande diversité des armées, des administrations et des manufactures. Il ne faut pas déduire les technologies prussiennes du seul voisinage culturel; les nœuds militaires/miniers de frontière sont donc revus séparément.
- **Sources:** <https://www.cambridge.org/core/journals/journal-of-economic-history/article/economic-growth-in-germany-15001850/3FB21F575B6056CE6BCFF04C97FC1E49> ; <https://www.cambridge.org/core/books/abs/cultures-of-power-in-europe-during-the-long-eighteenth-century/military-culture-in-the-reich-c-16801806/F52FD6774258813E7A482606C91377B9>
- **Confiance générale:** MEDIUM

### PAP — Rome

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies frontière/sectorielles:** `light_infantry_tactics (FRONTIER)`, `regulated_small_arms (SECTORAL)`, `shaft_mining (SECTORAL)`, `standardized_field_artillery (FRONTIER)`
- **Prérequis problématiques:** codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft
- **Justification historique:** Les États pontificaux disposent d’administration, d’agriculture, d’artisanats et de réseaux urbains, mais le tier 4 donne des capacités militaires/minières trop uniformes pour être acceptées sans preuves locales. Setup explicite recommandé.
- **Sources:** <https://www.treccani.it/enciclopedia/italia_(Dizionario-di-Storia)/> ; <https://en.chateauversailles.fr/news/exhibitions/royal-silks-europe>
- **Confiance générale:** MEDIUM

### PAR — Parma

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies frontière/sectorielles:** `light_infantry_tactics (FRONTIER)`, `regulated_small_arms (SECTORAL)`, `shaft_mining (SECTORAL)`, `standardized_field_artillery (FRONTIER)`
- **Prérequis problématiques:** codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft
- **Justification historique:** Parme est un foyer du réformisme italien sous Du Tillot, mais sa taille et son appareil militaire ne justifient pas une copie des grands États. Conserver agriculture, textile/artisanat, diplomatie et administration; expliciter le reste.
- **Sources:** <https://www.treccani.it/enciclopedia/italia_(Dizionario-di-Storia)/> ; <https://en.chateauversailles.fr/news/exhibitions/royal-silks-europe>
- **Confiance générale:** MEDIUM

### PRU — Prussia

- **Current tier:** `tier_4`
- **Tier action:** `KEEP_TIER`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `light_infantry_tactics`, `organized_textile_production`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`, `systematic_administrative_statistics`, `urbanization`, `specialized_technical_academies`
- **Technologies à ADD:** `scientific_fortification_siegecraft`
- **Technologies à REMOVE:** `colonization`, `romanticism`
- **Technologies à REVIEW:** —
- **Technologies frontière/sectorielles:** `light_infantry_tactics (FRONTIER)`
- **Prérequis problématiques:** codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft | romanticism <- institutionalized_scientific_exchange | specialized_technical_academies <- institutionalized_scientific_exchange
- **Justification historique:** État militaire et administratif de premier rang dans l’espace germanique, avec standardisation de l’artillerie et institution technique minière à Berlin dès 1770. La Silésie apporte une forte proto-industrie textile. En revanche `romanticism` est trop tardif et `colonization` ne correspond pas à une institution coloniale active en 1776.
- **Sources:** <https://cp.tu-berlin.de/history> ; <https://www.bundeswehr.de/en/organization/army/structure/branches/artillery>
- **Confiance générale:** HIGH

### SAR — Sardinia-Piedmont

- **Current tier:** `tier_4`
- **Tier action:** `KEEP_TIER`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `light_infantry_tactics`, `organized_textile_production`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** `scientific_fortification_siegecraft`, `specialized_technical_academies`
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `turnpike_road_networks`
- **Technologies frontière/sectorielles:** `light_infantry_tactics (FRONTIER)`, `shaft_mining (SECTORAL)`, `turnpike_road_networks (SECTORAL)`
- **Prérequis problématiques:** codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft
- **Justification historique:** Le Piémont-Sardaigne est un cas de forte spécialisation: arsenaux et écoles d’artillerie/fortification très précoces à Turin, plus une industrie de la soie de premier plan. Il mérite des ADD explicites techniques/militaires plutôt qu’un simple bonus de tier.
- **Sources:** <https://www.museotorino.it/view/s/276a506f80994a3a943a5600e4b944ce> ; <https://en.chateauversailles.fr/royal-silks-europe/consortium-royal-residences-savoy>
- **Confiance générale:** HIGH

### SAX — Saxony

- **Current tier:** `tier_4`
- **Tier action:** `KEEP_TIER`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `light_infantry_tactics`, `organized_textile_production`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** `specialized_technical_academies`
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** —
- **Technologies frontière/sectorielles:** `light_infantry_tactics (FRONTIER)`, `regulated_small_arms (SECTORAL)`, `standardized_field_artillery (FRONTIER)`
- **Prérequis problématiques:** codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft
- **Justification historique:** Un des pôles manufacturiers et miniers les plus importants du monde germanique. La Bergakademie de Freiberg (1765) justifie une académie technique explicite. La puissance textile ne doit toutefois pas être confondue avec la filature mécanisée de type industriel, postérieure au cutoff.
- **Sources:** <https://tu-freiberg.de/en/university/history> ; <https://books.fupress.com/chapter/promotion-of-high-quality-textiles-by-prize-competitions-during-the-enlightenment-in-saxony-from-raw/13603>
- **Confiance générale:** HIGH

### SCH — Schleswig

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies frontière/sectorielles:** `light_infantry_tactics (FRONTIER)`, `regulated_small_arms (SECTORAL)`, `shaft_mining (SECTORAL)`, `standardized_field_artillery (FRONTIER)`
- **Prérequis problématiques:** codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft
- **Justification historique:** Principauté allemande de taille réduite: les sources sur le Reich montrent une grande diversité des armées, des administrations et des manufactures. Il ne faut pas déduire les technologies prussiennes du seul voisinage culturel; les nœuds militaires/miniers de frontière sont donc revus séparément.
- **Sources:** <https://www.cambridge.org/core/journals/journal-of-economic-history/article/economic-growth-in-germany-15001850/3FB21F575B6056CE6BCFF04C97FC1E49> ; <https://www.cambridge.org/core/books/abs/cultures-of-power-in-europe-during-the-long-eighteenth-century/military-culture-in-the-reich-c-16801806/F52FD6774258813E7A482606C91377B9>
- **Confiance générale:** MEDIUM

### SCM — Schaumburg-Lippe

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies frontière/sectorielles:** `light_infantry_tactics (FRONTIER)`, `regulated_small_arms (SECTORAL)`, `shaft_mining (SECTORAL)`, `standardized_field_artillery (FRONTIER)`
- **Prérequis problématiques:** codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft
- **Justification historique:** Principauté allemande de taille réduite: les sources sur le Reich montrent une grande diversité des armées, des administrations et des manufactures. Il ne faut pas déduire les technologies prussiennes du seul voisinage culturel; les nœuds militaires/miniers de frontière sont donc revus séparément.
- **Sources:** <https://www.cambridge.org/core/journals/journal-of-economic-history/article/economic-growth-in-germany-15001850/3FB21F575B6056CE6BCFF04C97FC1E49> ; <https://www.cambridge.org/core/books/abs/cultures-of-power-in-europe-during-the-long-eighteenth-century/military-culture-in-the-reich-c-16801806/F52FD6774258813E7A482606C91377B9>
- **Confiance générale:** MEDIUM

### SCW — Schwarzburg

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies frontière/sectorielles:** `light_infantry_tactics (FRONTIER)`, `regulated_small_arms (SECTORAL)`, `shaft_mining (SECTORAL)`, `standardized_field_artillery (FRONTIER)`
- **Prérequis problématiques:** codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft
- **Justification historique:** Petit État thuringien/saxon situé dans une zone d’artisanat et de manufactures, mais distinct du puissant électorat de Saxe. Les capacités civiles de base sont plausibles; les nœuds militaires de frontière et la mine doivent rester explicites/à vérifier.
- **Sources:** <https://www.cambridge.org/core/journals/journal-of-economic-history/article/economic-growth-in-germany-15001850/3FB21F575B6056CE6BCFF04C97FC1E49> ; <https://www.cambridge.org/core/books/abs/cultures-of-power-in-europe-during-the-long-eighteenth-century/military-culture-in-the-reich-c-16801806/F52FD6774258813E7A482606C91377B9>
- **Confiance générale:** MEDIUM

### SIC — Two Sicilies

- **Current tier:** `tier_4`
- **Tier action:** `KEEP_TIER`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `light_infantry_tactics`, `organized_textile_production`, `regulated_small_arms`, `standardized_field_artillery`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** `scientific_fortification_siegecraft`, `specialized_technical_academies`
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `shaft_mining`, `state_dockyard_systems`
- **Technologies frontière/sectorielles:** `light_infantry_tactics (FRONTIER)`, `regulated_small_arms (SECTORAL)`, `shaft_mining (SECTORAL)`, `state_dockyard_systems (SECTORAL)`
- **Prérequis problématiques:** codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft
- **Justification historique:** Le TAG SIC est traité comme setup composite des Deux-Siciles tel que le mod le définit, distinct du TAG GR3 Sicily. Les institutions militaires napolitaines peuvent justifier ses ADD explicites, mais ne doivent pas être copiées automatiquement vers GR3.
- **Sources:** <https://www.esercito.difesa.it/en/organization/the-chief-of-general-staff-of-the-army/training-specialization-and-doctrine-command/training-command-and-application-school-of-the-army/military-academy/nunziatella/history-and-traditions/124245.html> ; <https://www.cambridge.org/core/books/abs/naples-in-the-eighteenth-century/arrogance-of-the-market-the-economy-of-the-kingdom-between-the-mediterranean-and-europe/E275AD8133C1ABA8555C21B6441255AC>
- **Confiance générale:** HIGH

### SWI — Switzerland

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies frontière/sectorielles:** `light_infantry_tactics (FRONTIER)`, `regulated_small_arms (SECTORAL)`, `shaft_mining (SECTORAL)`, `standardized_field_artillery (FRONTIER)`
- **Prérequis problématiques:** codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft
- **Justification historique:** La Confédération combine une proto-industrie remarquable (coton, textile, horlogerie et artisanats régionaux) avec une organisation politique et militaire cantonale. Le tier 4 générique masque cette asymétrie; un setup explicite est nettement préférable.
- **Sources:** <https://hls-dhs-dss.ch/de/articles/013931/2010-03-31/> ; <https://hls-dhs-dss.ch/fr/articles/008683/2008-06-05/>
- **Confiance générale:** HIGH

### TUS — Tuscany

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `shaft_mining`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `light_infantry_tactics`, `regulated_small_arms`, `standardized_field_artillery`, `turnpike_road_networks`
- **Technologies frontière/sectorielles:** `light_infantry_tactics (FRONTIER)`, `regulated_small_arms (SECTORAL)`, `shaft_mining (SECTORAL)`, `standardized_field_artillery (FRONTIER)`, `turnpike_road_networks (SECTORAL)`
- **Prérequis problématiques:** codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft
- **Justification historique:** La Toscane de Pietro Leopoldo est surtout avancée par ses réformes administratives, fiscales, agricoles et commerciales. Cette modernité institutionnelle ne justifie pas automatiquement un paquet militaire prussien. Les routes sont à examiner sectoriellement; pas d’ADD automatique de `turnpike_road_networks`.
- **Sources:** <https://www.treccani.it/enciclopedia/pietro-leopoldo-d-asburgo-lorena-granduca-di-toscana-poi-imperatore-del-sacro-romano-impero-come-leopoldo-ii_(Dizionario-Biografico)/> ; <https://www.treccani.it/enciclopedia/toscana_(Enciclopedia-Italiana)/>
- **Confiance générale:** HIGH

### VEN — Venice

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `light_infantry_tactics`, `organized_textile_production`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`, `systematic_administrative_statistics`, `urbanization`, `specialized_technical_academies`
- **Technologies à ADD:** `scientific_fortification_siegecraft`, `state_dockyard_systems`
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `industrial_canals`, `scientific_naval_architecture`
- **Technologies frontière/sectorielles:** `light_infantry_tactics (FRONTIER)`, `regulated_small_arms (SECTORAL)`, `shaft_mining (SECTORAL)`, `scientific_naval_architecture (SECTORAL)`
- **Prérequis problématiques:** codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft | specialized_technical_academies <- institutionalized_scientific_exchange | `scientific_naval_architecture` dépend de `state_dockyard_systems`, lui-même recommandé ADD.
- **Justification historique:** Venise reste une puissance technique particulière: Arsenal d’État, administration militaire, industrie urbaine et Terraferma manufacturière. Son setup doit être naval/arsenal et manufacturier plutôt que calqué sur un État terrestre allemand. Les canaux vénitiens ne suffisent pas à eux seuls à prouver le nœud `industrial_canals` du jeu.
- **Sources:** <https://www.treccani.it/enciclopedia/l-arsenale-di-venezia-e-i-cantieri-navali-della-marina_(Il-Contributo-italiano-alla-storia-del-Pensiero%3A-Tecnica)/> ; <https://www.research.unipd.it/handle/11577/1559630>
- **Confiance générale:** HIGH

### WEI — Saxe-Weimar

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies frontière/sectorielles:** `light_infantry_tactics (FRONTIER)`, `regulated_small_arms (SECTORAL)`, `shaft_mining (SECTORAL)`, `standardized_field_artillery (FRONTIER)`
- **Prérequis problématiques:** codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft
- **Justification historique:** Petit État thuringien/saxon situé dans une zone d’artisanat et de manufactures, mais distinct du puissant électorat de Saxe. Les capacités civiles de base sont plausibles; les nœuds militaires de frontière et la mine doivent rester explicites/à vérifier.
- **Sources:** <https://www.cambridge.org/core/journals/journal-of-economic-history/article/economic-growth-in-germany-15001850/3FB21F575B6056CE6BCFF04C97FC1E49> ; <https://www.cambridge.org/core/books/abs/cultures-of-power-in-europe-during-the-long-eighteenth-century/military-culture-in-the-reich-c-16801806/F52FD6774258813E7A482606C91377B9>
- **Confiance générale:** MEDIUM

### WLD — Waldeck

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies frontière/sectorielles:** `light_infantry_tactics (FRONTIER)`, `regulated_small_arms (SECTORAL)`, `shaft_mining (SECTORAL)`, `standardized_field_artillery (FRONTIER)`
- **Prérequis problématiques:** codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft
- **Justification historique:** Principauté allemande de taille réduite: les sources sur le Reich montrent une grande diversité des armées, des administrations et des manufactures. Il ne faut pas déduire les technologies prussiennes du seul voisinage culturel; les nœuds militaires/miniers de frontière sont donc revus séparément.
- **Sources:** <https://www.amrevmuseum.org/germany-and-the-american-revolution> ; <https://www.cambridge.org/core/books/abs/cultures-of-power-in-europe-during-the-long-eighteenth-century/military-culture-in-the-reich-c-16801806/F52FD6774258813E7A482606C91377B9>
- **Confiance générale:** MEDIUM

### WUR — Württemberg

- **Current tier:** `tier_4`
- **Tier action:** `KEEP_TIER`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `light_infantry_tactics`, `organized_textile_production`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** —
- **Technologies frontière/sectorielles:** `light_infantry_tactics (FRONTIER)`, `regulated_small_arms (SECTORAL)`, `shaft_mining (SECTORAL)`, `standardized_field_artillery (FRONTIER)`
- **Prérequis problématiques:** codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft
- **Justification historique:** Le Wurtemberg possède une véritable proto-industrie textile exportatrice de longue durée et un État territorial actif, mais il ne faut pas transposer mécaniquement les capacités prussiennes. Le tier peut rester seulement avec une lecture sectorielle et des vérifications militaires ciblées.
- **Sources:** <https://www.cambridge.org/core/books/abs/state-corporatism-and-protoindustry/introduction/68CAD03765ED7BD77DC9A41C5F56541C> ; <https://www.cambridge.org/core/books/abs/cultures-of-power-in-europe-during-the-long-eighteenth-century/military-culture-in-the-reich-c-16801806/F52FD6774258813E7A482606C91377B9>
- **Confiance générale:** HIGH

## 5. Comparaison régionale

| Profil | TAG principaux | Lecture recommandée |
|---|---|---|
| Grandes monarchies militaro-administratives | PRU, AUS | Conserver le socle du tier 4 mais corriger explicitement les anachronismes et ajouter les parents réellement établis. |
| Pôles miniers/manufacturiers | SAX, HAN, WUR | Conserver/renforcer les capacités sectorielles prouvées; ne pas extrapoler à tout le militaire. |
| États militaires moyens | HEK, BRA, BAV | Armées réelles et parfois très professionnalisées; artillerie/industrie/mine à distinguer pays par pays. |
| Micro-États/villes du Reich | ANH, BAD, BRE, COB, FRM, HAM, HES, HOH, HOL, LIP, LUB, MEC, MEI, MST, NAS, OLD, SCH, SCM, SCW, WEI, WLD | `REPLACE_WITH_EXPLICIT_SETUP`: conserver les capacités civiles/artisanales communes, vérifier séparément armes, artillerie et mine. |
| Suisse | SWI | Forte proto-industrie, faible centralisation militaire: setup explicite asymétrique. |
| Piémont-Sardaigne | SAR | Soie + écoles d’artillerie/fortification: ADD techniques/militaires ciblés. |
| Venise | VEN | Arsenal d’État + manufactures + institutions militaires; setup naval/industriel spécifique. |
| Toscane | TUS | Réformes administratives/agricoles très fortes, mais pas de paquet militaire automatique. |
| Naples / Two Sicilies | GR4, SIC | Académies militaires spécialisées; prudence sur arsenaux modernes et diffusion au TAG GR3. |
| Gênes | GEN | Soie + académie d’architecture; capacité militaire terrestre à limiter/expliciter. |
| Petits États italiens | GR3, LUC, MOD, PAP, PAR | Agriculture/artisanat/admin plausibles, mais tier 4 militaire/minier à remplacer par setup explicite. |

## 6. Technologies frontière 1776

| Technologie | Verdict régional au 1776-01-01 |
|---|---|
| `atmospheric_engine` | **AUS: ADD (SECTORAL, MEDIUM)** pour le site habsbourgeois de Banská Štiavnica/Königsberg bei Schemnitz, actif dès 1721–22. Pas d’extension automatique à PRU/SAX/HAN. |
| `specialized_technical_academies` | **KEEP** PRU/AUS/VEN/GEN; **ADD** SAX/SAR/GR4/SIC. Les institutions sont datées avant 1776. |
| `scientific_fortification_siegecraft` | **ADD** PRU/AUS/SAR/VEN/GEN/GR4/SIC; ces cas disposent d’écoles, d’ingénieurs ou d’une organisation d’artillerie/fortification attestée. |
| `mechanized_spinning` | **Pas d’ADD régional recommandé.** La force textile de SAX, SWI, WUR, SAR, GEN ou VEN ne signifie pas mécanisation industrielle. La Suisse n’introduit la filature mécanique qu’au tournant de 1800; la Saxe suit également plus tard. |
| `turnpike_road_networks` | **REVIEW** SAR et TUS seulement: administrations routières/réformes réelles, mais correspondance imparfaite avec le nœud de jeu. Pas d’ADD automatique. |
| `industrial_canals` | **REVIEW** VEN seulement: les canaux vénitiens sont réels mais ne sont pas équivalents par définition au paquet de canaux industriels du jeu. |
| `improved_agricultural_implements` | Réformes agricoles attestées en Toscane, Prusse et Autriche, mais aucune preuve suffisamment précise ici d’une diffusion des outils correspondant au nœud; **pas d’ADD** dans cette vague. |
| `precision_boring` | Aucune preuve régionale suffisamment forte au cutoff pour un ADD. Ne pas l’accorder par proximité avec mines/métallurgie. |
| `coke_smelting` | Ne pas l’ajouter pour satisfaire `atmospheric_engine` en AUS: le moteur atmosphérique habsbourgeois ne démontre pas un secteur sidérurgique au coke. |

## 7. Anachronismes et attributions à retirer

1. **BRA — `railways`: REMOVE / HIGH / ANACHRONISTIC.** La première ligne publique allemande Nuremberg–Fürth ouvre en 1835. Le nœud débloque directement les premiers PM ferroviaires et ne peut pas être sauvé par une interprétation abstraite en 1776.
2. **PRU — `romanticism`: REMOVE / HIGH / ANACHRONISTIC.** Le romantisme allemand se cristallise à la fin du XVIIIe siècle; le nœud du jeu est trop tardif pour le 1er janvier 1776.
3. **AUS — `romanticism`: REMOVE / HIGH / ANACHRONISTIC.** Même verdict que pour PRU.
4. **PRU — `colonization`: REMOVE / HIGH / ABSENT.** L’ancien épisode colonial brandebourgeois avait cessé depuis des décennies; le nœud du jeu donne une institution coloniale active et des lois qui ne décrivent pas la Prusse de 1776.

`systematic_legal_codification` en AUS n’est **pas** retirée automatiquement: le Codex Theresianus de 1766 prouve un projet de codification systématique, mais il n’est jamais entré en vigueur. Verdict **REVIEW / FRONTIER**.

## 8. Prérequis

- `regulated_small_arms <- scientific_fortification_siegecraft`: le parent est recommandé ADD seulement là où les preuves sont indépendantes (PRU, AUS, SAR, VEN, GEN, GR4, SIC). Il n’est pas ajouté à tous les autres pays juste pour nettoyer l’arbre.
- `specialized_technical_academies <- institutionalized_scientific_exchange`: les académies de Freiberg, Berlin, Turin, Naples, etc. sont historiquement justifiées même si le parent du jeu manque. Ne pas ajouter automatiquement `institutionalized_scientific_exchange`.
- `codified_practical_knowledge <- institutionalized_scientific_exchange, periodical_print_networks`: ce nœud est un proxy abstrait sans déblocage direct; la dette de prérequis peut être tolérée jusqu’à une wave de refonte de l’arbre.
- `atmospheric_engine <- shaft_mining, coke_smelting`: pour AUS, `shaft_mining` est justifié; `coke_smelting` ne l’est pas. Le cas historique démontre précisément que la chaîne technologique du jeu est plus rigide que la réalité.
- `railways <- high_pressure_steam, puddling_and_rolling, professional_civil_engineering`: BRA doit perdre l’enfant, pas recevoir ses trois parents.

## 9. Incertitudes

- **Portée du TAG AUS:** le moteur atmosphérique de Banská Štiavnica se situe dans le royaume de Hongrie sous les Habsbourg. Si le setup AUS doit représenter uniquement les terres héréditaires autrichiennes les plus étroites, transformer cet ADD en REVIEW.
- **GR3/GR4/SIC:** le mod possède trois setups simultanés. La présente recherche refuse de dupliquer automatiquement les institutions napolitaines vers la Sicile séparée.
- **Petits États allemands:** les sources régionales prouvent une forte variété et parfois des armées importantes, mais pas le détail de chaque arsenal/mine. D’où de nombreux REVIEW plutôt que des REMOVE arbitraires.
- **Routes/canaux:** les termes du jeu sont des abstractions techniques. Une route entretenue par l’État ou un canal urbain ne suffit pas à satisfaire automatiquement les nœuds `turnpike_road_networks`/`industrial_canals`.
- **Codification autrichienne:** projet civil systématique en 1766 mais non promulgué; le nœud peut être retenu si l’on représente la capacité de codifier, ou écarté si l’on exige l’entrée en vigueur.

## 10. Recommandations pour l’implémentation

**Pas de code dans ce document.** Pour la future synthèse mondiale:

- Conserver le **tier 4** comme mécanisme de départ pour `AUS`, `PRU`, `BAV`, `SAX`, `BRA`, `HAN`, `HEK`, `WUR`, `SAR`, `GR4`, `SIC`, mais appliquer les ADD/REMOVE/REVIEW explicites de la matrice.
- Passer les **30 autres TAG** à `REPLACE_WITH_EXPLICIT_SETUP` plutôt que de changer leur numéro de tier: le problème est l’asymétrie interne du tier 4, pas un « niveau de civilisation » inférieur.
- Priorité d’implémentation régionale: **P0 BRA railways**, puis **PRU/AUS romanticism**, puis ajouts d’académies/fortification/arsenal réellement attestés, puis réécriture explicite des micro-États et de la Suisse.
- Aucun `CHANGE_TIER` n’est recommandé dans cette vague.

## Contrôle final et statistiques

- **TAG étudiés:** 41
- **KEEP:** 336
- **ADD:** 13
- **REMOVE:** 4
- **REVIEW:** 126
- **Pays avec CHANGE_TIER:** 0
- **Pays avec REPLACE_WITH_EXPLICIT_SETUP:** 30
- **Lignes de matrice:** 479
- **Principales incertitudes:** portée territoriale de AUS pour le moteur atmosphérique; articulation GR3/GR4/SIC; détail militaire/minier des micro-États; interprétation gameplay des routes/canaux; seuil de « codification » pour AUS.

### Vérifications effectuées

- Tous les 41 TAG régionaux identifiés dans le CSV pays sont présents.
- Toutes les technologies explicites actuelles de ces TAG ont une décision KEEP/REMOVE/REVIEW.
- Les anachronismes C/D distribués dans la région (`railways`, `romanticism`) sont explicitement retirés.
- Les technologies frontière pertinentes sont examinées sans ajouter mécaniquement leurs parents.
- Aucun Technology_ID absent du CSV technologies n’est utilisé.