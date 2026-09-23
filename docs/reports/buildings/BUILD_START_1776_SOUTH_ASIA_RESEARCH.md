# BUILD START 1776 — Recherche régionale — Asie du Sud

**Date absolue : 1776-01-01**  
**Région historique : Asie du Sud / sous-continent indien**  
**Recherche uniquement — aucun fichier gameplay modifié.**

## 1. Périmètre et méthode

- Catalogue technique R4 brut : 60 couples Owner/State.
- Périmètre historique conservé : **44 couples Owner_TAG + State_ID**, couvrant **23 State IDs**.
- Exclusions héritées du périmètre historique précédent : Afghanistan comme polity, Birmanie/Arakan/Pegu/Shan/Tenasserim/Kachin/Mandalay et Indian Ocean Territory. Les possessions locales explicitement dans le sous-continent (ex. Ceylan) restent traitées même si le propriétaire est extérieur.
- Aucune fusion de State_ID partagés : chaque ligne propriétaire/État est recherchée séparément.
- Seuls les bâtiments dont `Relevant_For_1776_Start_Research` commence par `YES` sont admissibles ; aucun auto-généré ni NO_POST_1776 n’est utilisé.
- La matrice ne contient que les recommandations positives. Les absences significatives sont documentées plus bas.

## 2. Diagnostic régional

Le sous-continent de 1776 n’est pas une économie homogène. Les concentrations les plus fortes retenues sont : Bengal (textiles, soie, sel, administration et commerce EIC), Gujarat (textiles/coton/commerce maritime), Coromandel (textiles, riz, ports), Malabar/Travancore (poivre, bois, ports et construction navale), Mysore (fiscal-militaire, armement, artisanat textile et bois), Awadh/Delhi/Agra (manufactures et arsenaux) et Ceylan VOC (cannelle, ports, administration et canaux).

Les niveaux ne représentent pas des usines modernes : ils agrègent un secteur organisé à l’échelle du State_ID. Les districts textiles en putting-out system peuvent donc atteindre 2–4 sans mécanisation. Inversement, une tradition métallurgique ou agricole diffuse ne suffit pas à créer un bâtiment spécialisé.

## 3. Centres de commerce

Les trade centers sont limités aux véritables hubs de redistribution/commerce longue distance. Les plus hauts niveaux proposés sont Calcutta/Hughli et Gujarat/Surat (3), puis plusieurs hubs nationaux ou exportateurs (2). Aucun simple port n’est automatiquement converti en trade center.

## 4. Infrastructure régionale

`building_railway` est utilisé uniquement comme infrastructure terrestre régionale. Toutes les lignes conservent **RAIL=pm_no_rail_network**. Les niveaux sont motivés par les routes structurées (Delhi–Agra, Agra–Malwa–Surat, Malwa, etc.) et, à Ceylan VOC seulement, par un réseau navigable de canaux suffisamment structuré pour être distingué des simples voies d’eau naturelles.

## 5. Technologie / bâtiments

Une recommandation historique n’est pas supprimée quand le TAG ne possède pas actuellement le gate technologique. `Tech_Distribution_Review=YES` signale exactement ces conflits pour la synthèse ultérieure. Cela touche notamment ports, administrations, arsenaux, plantations et certaines mines.

## 6. Owner/State sans recommandation positive

- `BIC + STATE_BUNDELKHAND` — East India / Bundelkhand: aucune activité spécialisée ne dépasse le seuil de preuve avec localisation propriétaire suffisante.
- `COO + STATE_WEST_BENGAL` — Cooch Behar / West Bengal: aucune activité spécialisée ne dépasse le seuil de preuve avec localisation propriétaire suffisante.
- `GAR + STATE_AGRA` — Garhwal / Agra: aucune activité spécialisée ne dépasse le seuil de preuve avec localisation propriétaire suffisante.
- `GBR + STATE_CEYLON` — Great Britain / Ceylon: aucune activité spécialisée ne dépasse le seuil de preuve avec localisation propriétaire suffisante.
- `HYD + STATE_CENTRAL_PROVINCES` — Hyderabad / Central Provinces: aucune activité spécialisée ne dépasse le seuil de preuve avec localisation propriétaire suffisante.
- `JEY + STATE_CIRCARS` — Jeypore / Northern Circars: aucune activité spécialisée ne dépasse le seuil de preuve avec localisation propriétaire suffisante.
- `KHP + STATE_BOMBAY` — Kolhapur / Bombay: aucune activité spécialisée ne dépasse le seuil de preuve avec localisation propriétaire suffisante.
- `KKI + STATE_ASSAM` — Kuki / Assam: aucune activité spécialisée ne dépasse le seuil de preuve avec localisation propriétaire suffisante.
- `KNO + STATE_KURNOOL` — Kurnool / Ceded Districts: aucune activité spécialisée ne dépasse le seuil de preuve avec localisation propriétaire suffisante.
- `MARATH + STATE_BUNDELKHAND` — Maratha Confederacy / Bundelkhand: aucune activité spécialisée ne dépasse le seuil de preuve avec localisation propriétaire suffisante.
- `MGH + STATE_ASSAM` — Khasi / Assam: aucune activité spécialisée ne dépasse le seuil de preuve avec localisation propriétaire suffisante.
- `MLD + STATE_CEYLON` — Maldives / Ceylon: aucune activité spécialisée ne dépasse le seuil de preuve avec localisation propriétaire suffisante.
- `NGA + STATE_ASSAM` — Naga / Assam: aucune activité spécialisée ne dépasse le seuil de preuve avec localisation propriétaire suffisante.
- `SAT + STATE_BOMBAY` — Satara / Bombay: aucune activité spécialisée ne dépasse le seuil de preuve avec localisation propriétaire suffisante.
- `TIP + STATE_ASSAM` — Tipperah / Assam: aucune activité spécialisée ne dépasse le seuil de preuve avec localisation propriétaire suffisante.

## 7. IMPORTANT_NON_RECOMMENDATIONS

| State | Industry | Decision | Reason | Source |
|---|---|---|---|---|
| GAR + STATE_AGRA | Broad Agra manufactures | NO_BUILDING | The Garhwal-owned fragment is too poorly localized inside the current split State_ID to transfer Agra-city evidence safely; industries are assigned only to the large Maratha-held instance. | https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mughal-india/A275FC7EFB9CF124D90302E92A994FCC |
| KKI/MGH/NGA/TIP + STATE_ASSAM | Tea plantations / industrial forestry | NO_BUILDING | Tea existed botanically, but large organized commercial tea plantations are nineteenth-century; no owner-specific 1776 concentration in the split upland instances was established. | https://www.cambridge.org/core/books/the-cambridge-economic-history-of-india/57937CDBBE6F4B5C474E0A7A59697AF3 |
| MYS + STATE_MYSORE | building_steel_mill | NO_BUILDING | Mysorean/Indian wootz and advanced metalworking do not equal the fork steel-mill node gated by coke_smelting and later industrial PMs. | https://southasia.stanford.edu/publications/guns-and-british-empire |
| HYD + STATE_HYDERABAD | building_artillery_foundry | NO_BUILDING | Hyderabad had arms manufacture, but the well-documented Raymond gunfoundry dates to 1785, after the strict cutoff; the broader arms-industry recommendation is retained instead. | https://southasia.stanford.edu/publications/guns-and-british-empire |
| DEI + STATE_CEYLON | building_tea_plantation | NO_BUILDING | Commercial tea plantation is post-1776; Dutch Ceylon’s exceptional export specialization in this period was cinnamon. | https://journals.sagepub.com/doi/10.1177/001946468502200102 |
| DEI + STATE_CEYLON | Active railway PM | NO_BUILDING | Regional Infrastructure is recommended only for road/canal capacity; rail must remain pm_no_rail_network. | TECHNICAL_PACK |
| BIC + STATE_EAST_BENGAL | building_silk_plantation level 3+ | NO_BUILDING | The strongest documented EIC raw-silk/reeling concentration is in western Bengal/Murshidabad-Hughli; East Bengal is represented primarily by cotton/muslin and rice. | https://www.cambridge.org/core/journals/journal-of-global-history/article/abs/bengali-raw-silk-the-east-india-company-and-the-european-global-market-17701833/B3794FCBAAADC654B77B258F5D3303DF |
| MLD + STATE_CEYLON | building_port / building_fishing_wharf | NO_BUILDING | The Maldives had major cowrie commerce, but the current split owner/state row has Has_Port_Access=NO; no manual port is proposed against the technical map constraint. | https://www.cambridge.org/core/books/abs/shell-money-of-the-slave-trade/prosperity-for-the-cowrie-commerce-eighteenth-century/49F882BCD031205E27CEAB0D76440F91 |
| GBR + STATE_CEYLON | British colonial buildings | NO_BUILDING | The tiny current split is not sufficient evidence to import the Dutch coastal-Ceylon system into the British owner line; no capability transfer across owner-state instances. | https://soas-repository.worktribe.com/output/387948/dutch-rule-in-maritime-ceylon-1766-1796 |
| DENNOR + STATE_MADRAS | building_port | NO_BUILDING | Tranquebar was coastal and commercial, but the current owner/state row has Has_Port_Access=NO; technical map constraint wins for manual port placement. | https://www.cambridge.org/core/journals/church-history/article/syncretism-of-piety-imagining-global-protestism-in-early-eighteenthcentury-boston-tranquebar-and-halle/F365F63D070826D244437D23F680B4B8 |
| NET/TRA + STATE_TRAVANCORE | building_port | NO_BUILDING | Historically coastal, but these current owner/state instances have Has_Port_Access=NO. Ports are therefore not manually proposed; trade/spice capacity is represented separately. | https://www.cambridge.org/core/books/abs/kerala-1956-to-the-present/before-independence/EE38A3443D329F4631CB21A67DE37178 |
| KHP/SAT + STATE_BOMBAY | Maratha naval complex | NO_BUILDING | The Maratha naval evidence cannot be safely copied to every split owner in STATE_BOMBAY; it is assigned only to MARATH, while smaller owner fragments remain unseeded absent local evidence. | https://academic.oup.com/reference/62399/reference-article-abstract/555376418 |
| BIC/MARATH + STATE_BUNDELKHAND | Specialized industry | NO_BUILDING | No sector reached the evidence threshold for a concentrated state-level building in these specific split instances; ordinary agrarian/craft activity remains abstracted. | https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5 |
| KNO + STATE_KURNOOL | Commercial farm/manufactory | NO_BUILDING | Evidence supports agriculture and crafts generally but not a sufficiently concentrated owner-specific sector at the Victoria state scale by the cutoff. | https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/south-india/BCDB8046E20E009465FE6CB9C25A37C5 |
| COO + STATE_WEST_BENGAL | Bengal export complexes | NO_BUILDING | Do not transfer Calcutta/Murshidabad/Dacca evidence to the small Cooch Behar owner-instance simply because it shares STATE_WEST_BENGAL. | https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D |

## 8. Points nécessitant prudence lors de la synthèse

- **Map rework** : toutes les instances conservées portent `INDIA_FUTURE_REWORK`; les niveaux sont donc historiquement documentés mais devront être remappés si les State IDs changent.
- **Ports** : aucune recommandation de port n’est faite sur une owner/state avec `Has_Port_Access=NO`, même lorsque l’enclave historique était côtière.
- **Mysore** : les arsenaux/armes sont retenus avant 1776, mais aucune technologie ou industrie explicitement dépendante des développements tipuéens des années 1780–1790 n’est importée.
- **Bengale** : la soie concentrée est placée en West Bengal; East Bengal reçoit la forte concentration coton/mousseline.
- **Ceylan** : cannelle = niveau 4 exceptionnel; thé exclu; canaux VOC distingués des simples voies d’eau naturelles.
- **Hyderabad** : armes oui à faible niveau; la grande gunfoundry de Raymond (1785) est explicitement postérieure au cutoff et n’est pas utilisée pour justifier une artillery foundry en 1776.

## 9. Contrôle final

- STATES COVERED = **44 Owner_TAG + State_ID** (23 State IDs)
- POSITIVE BUILDING ROWS = **159**
- TRADE CENTERS = **24**
- LEVEL 1 = **81**
- LEVEL 2 = **65**
- LEVEL 3 = **11**
- LEVEL 4-5 = **2**
- LEVEL 6+ = **0**
- TECH_DISTRIBUTION_REVIEW = **19**
- REVIEW CASES = **0**
- SERENISSIMA STATES SKIPPED = **0 in historical South Asia scope** (no VEN/GEN line survived the regional filter)
- Aucun `State_ID` ou `Building_ID` n’a été inventé; aucun bâtiment auto-généré ou `NO_POST_1776` n’est présent.
