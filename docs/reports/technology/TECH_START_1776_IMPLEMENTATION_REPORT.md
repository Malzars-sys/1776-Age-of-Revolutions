# TECH START 1776 — Fermeture complète des prérequis

Date de validation : 12 septembre 2026  
Cible : Victoria 3 1.13.11  
Working tree local autoritaire, sans commit ni push.

## Résultat final

- 474 TAG reconstruits : **474 MATCH / 0 MISMATCH**.
- 471 TAG soumis à la fermeture stricte : **0 prérequis direct manquant** et **0 prérequis transitif manquant**.
- GAL, MLT et PPU restent inchangés faute de recherche régionale suffisante et sont rapportés séparément.
- 0 technologie inconnue.
- 0 grant explicite dupliqué.
- 0 technologie C/D distribuée au départ.
- 0 `railways`, 0 `romanticism`, 0 `joint_stock_companies`.
- 2 610 relations pays-technologie finales.
- Par rapport à l’état audité avant l’implémentation : 389 pays changés, 387 ADD et 1 198 REMOVE.

La correction stricte a réécrit 247 setups de pays par rapport à l’implémentation intermédiaire. Les paliers génériques qui contenaient eux-mêmes des enfants sans parents ont été remplacés par des listes explicites lorsque nécessaire.

## Réexamen des 61 refus

Le tableau exhaustif demandé se trouve dans [TECH_START_1776_PREREQUISITE_CLOSURE_DECISIONS.csv](./TECH_START_1776_PREREQUISITE_CLOSURE_DECISIONS.csv). Il contient exactement 61 lignes et les colonnes : TAG, Technology, Old decision, Missing prerequisite closure, Added prerequisites, Final decision et Reason.

Les dix technologies enfants réexaminées sont toutes classées A ou B, de même que les parents envisagés. La décision ne repose donc pas sur une exclusion mécanique C/D : elle tient compte des capacités débloquées par les parents (camps de bûcherons, institutions et lois, mines, armes/artillerie, fortifications, aciéries et fabriques d’outils).

Résultat :

- 20 technologies restaurées avec leurs prérequis;
- 41 technologies maintenues retirées pour fermeture historiquement excessive;
- 20 grants de prérequis accompagnent directement ces 20 restaurations;
- 27 grants de prérequis sont ajoutés au total par rapport au plan régional canonique : les 20 précédents, plus 7 fermetures de technologies déjà retenues ailleurs dans le plan;
- 26 de ces 27 grants sont nouveaux par rapport à l’implémentation intermédiaire, car `organized_forestry` avait déjà été conservée pour GBR.

### Restaurations

| Technologie | TAG | Préreququis ajouté | Décision |
|---|---|---|---|
| `traditional_papermaking` | BUK, CHI, HYD, JAI, JAP, KAS, KOR, MARATH, MUG, NET, PAN, TIB | `organized_forestry` | Parent A, fermeture courte; le déblocage des camps de bûcherons reste proportionné à la capacité papetière retenue. |
| `specialized_technical_academies` | GR4, SAR, SAX, SIC | `institutionalized_scientific_exchange` | Le réseau savant est cohérent avec les académies techniques retenues. |
| `industrial_canals` | FRA, NET | `turnpike_road_networks` | Le parent est employé comme abstraction du socle d’ingénierie routière, conformément à la correction. |
| `advanced_crop_rotations` | BEO | `selective_breeding` | Chaîne agronomique B courte et plausible dans les Pays-Bas autrichiens. |
| `military_topographic_surveying` | BIC | `permanent_engineer_services` | Le parent n’a pas de déblocage direct disproportionné et représente les corps de relevé de la Compagnie. |

Pays concernés par au moins une restauration : BEO, BIC, BUK, CHI, FRA, GR4, HYD, JAI, JAP, KAS, KOR, MARATH, MUG, NET, PAN, SAR, SAX, SIC et TIB.

### Maintiens du retrait

| Technologie | Nombre | TAG | Motif principal |
|---|---:|---|---|
| `atmospheric_engine` | 5 | AUS, BEL, BEO, FRA, SPC | La fermeture imposerait `coke_smelting`, non justifiée localement en 1776. |
| `codified_practical_knowledge` | 13 | ASH, BNY, BRZ, BUG, GRE, IR1, KBA, LAN, LNG, MAD, RWD, TIB, TUN | La fermeture ajouterait simultanément presse périodique et échange scientifique institutionnalisé. |
| `light_infantry_tactics` | 19 | ARG, ECU, GR5, HAI, HBC, IQU, MICC, MKT, NBS, ONT, ORG, PRA, PRG, SC2, SC4, SEQ, UBD, UCA, VNZ | La fermeture ajouterait industrie d’armes, artillerie et fortifications malgré le retrait régional de `regulated_small_arms`. |
| `standardized_field_artillery` | 3 | GR5, HAI, UBD | Même cascade militaire disproportionnée. |
| `applied_mineralogy` | 1 | SC2 | `shaft_mining` ouvrirait toute la suite de bâtiments miniers, explicitement rejetée pour ce pays. |

Les 41 lignes concernent 37 TAG : ARG, ASH, AUS, BEL, BEO, BNY, BRZ, BUG, ECU, FRA, GR5, GRE, HAI, HBC, IQU, IR1, KBA, LAN, LNG, MAD, MICC, MKT, NBS, ONT, ORG, PRA, PRG, RWD, SC2, SC4, SEQ, SPC, TIB, TUN, UBD, UCA et VNZ.

## Fermetures supplémentaires du plan

Sept parents ferment des technologies qui n’appartenaient pas aux 61 refus :

- `institutionalized_scientific_exchange` pour AUS, GEN, PRU, TUR et VEN afin de fermer `specialized_technical_academies`;
- `selective_breeding` pour BEL afin de fermer `advanced_crop_rotations`;
- `organized_forestry` pour GBR afin de fermer `coke_smelting`.

Toutes les autres dettes héritées des paliers ont été supprimées en retirant l’enfant et, par propagation, ses descendants devenus invalides. Aucun parent non validé historiquement n’a été créé pour conserver artificiellement un palier.

## Cas demandés

### Industrial Canals

FRA et NET récupèrent `industrial_canals` avec `turnpike_road_networks`. GBR conserve déjà la chaîne complète. Résultat final : FRA, GBR et NET.

### Atmospheric Engine

| TAG | Décision | Justification |
|---|---|---|
| AUS | retrait maintenu | Pas de diffusion locale de fonte au coke suffisamment établie en 1776. |
| BEL | retrait maintenu | La métallurgie au coke belge moderne est postérieure au cutoff. |
| BEO | retrait maintenu | Même territoire industriel historique et même fermeture au coke excessive. |
| FRA | retrait maintenu | La première production française au coke retenue par la recherche est postérieure à 1776. |
| SPC | retrait maintenu | Les projets espagnols au coke appartiennent aux décennies suivantes. |
| GBR | conservée | `shaft_mining`, `coke_smelting` et `organized_forestry` ferment entièrement la chaîne. |

### Joint-Stock Companies

`joint_stock_companies` reste absente de tous les départs, y compris DEI. Sa fermeture exige notamment `postal_savings`, technologie C postérieure à 1776, puis `institutionalized_public_credit`; elle déclenche aussi `commercial_insurance_markets`. L’existence de la VOC ne justifie donc pas ce nœud de gameplay et sa cascade institutionnelle.

## Smoke tests

| Technologie | Pays finaux |
|---|---|
| `industrial_canals` | FRA, GBR, NET |
| `atmospheric_engine` | GBR |
| `coke_smelting` | GBR |
| `precision_boring` | GBR |
| `mechanized_spinning` | GBR |
| `joint_stock_companies` | aucun |
| `railways` | aucun |
| `romanticism` | aucun |

## Pays non reconstruits

GAL, MLT et PPU conservent exactement leur état pré-phase, comme demandé.

- GAL conserve deux relations directes manquantes : `codified_practical_knowledge -> periodical_print_networks` et `regulated_small_arms -> scientific_fortification_siegecraft`.
- MLT conserve trois relations directes manquantes : `codified_practical_knowledge -> institutionalized_scientific_exchange`, `codified_practical_knowledge -> periodical_print_networks` et `regulated_small_arms -> scientific_fortification_siegecraft`.
- PPU ne présente aucune relation directe manquante.

Ces cinq relations sont uniquement signalées; elles ne font pas échouer la phase de fermeture des 471 pays reconstruits.

## Contrôles régionaux et validation

Le relevé [TECH_START_1776_SANITY_CASES.csv](./TECH_START_1776_SANITY_CASES.csv) donne le palier effectif, les grants explicites et le set final des 48 pays de contrôle régionaux.

Le validateur [tech_start_1776_implementation.py](../../../tools/tech_start_1776_implementation.py) exige désormais :

- 474 MATCH / 0 MISMATCH;
- 0 UNKNOWN_TECH;
- 0 DUPLICATE_EXPLICIT_GRANT;
- 0 CLASS_C_OR_D_STARTING_TECH;
- 0 MISSING_DIRECT_PREREQUISITE parmi les 471 pays reconstruits;
- 0 MISSING_TRANSITIVE_PREREQUISITE parmi les 471 pays reconstruits.

La correction n’a modifié ni l’arbre technologique, ni ses prérequis, ni TECH6D, ni TECH7A, ni les PM, ni les bâtiments. Le PM d’outils de subsistance créé lors de la phase précédente est resté inchangé.

`git diff --check` doit réussir sans erreur d’espace; les avertissements LF/CRLF globaux du working tree peuvent toujours être affichés. Aucun commit, push ou PR n’a été créé.
