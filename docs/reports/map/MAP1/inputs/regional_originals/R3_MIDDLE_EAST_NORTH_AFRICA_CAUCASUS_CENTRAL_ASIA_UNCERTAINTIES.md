# R3 — Incertitudes, arbitrages et transmission MAP-0

**Date de référence : 1776-01-01.** Recherche établie le 2026-10-10. Aucune modification des historiques ou de la carte; aucun push. Les CSV du mod ne sont pas une preuve historique.

## Couverture vérifiable
- **145 couples** `Owner_TAG + State_ID` exactement une fois, **93 États**, **56 TAG**; 4688 lignes du bitmap baseline de R3. Toutes recommandations et couverture possèdent un Change_ID stable.
- Statuts de couverture : `CHANGE_PROPOSED` 30, `REVIEWED_NO_CHANGE` 49, `UNRESOLVED` 66.
- 43 références historiques identifiées. `Mapping_Status=VERIFIED` : 0 ligne, faute de superposition géoréférencée; aucun RGB inventé. Mapping initial du mod NON validé.
- Un `REVIEWED_NO_CHANGE` signifie absence de correction **proposée dans ce lot**, jamais une vérification que tous les pixels de la State Region ont le même souverain.
- Les recommandations sont une **pré-analyse historique documentée**, pas un audit exhaustif province par province; certaines sources décrivent des structures générales et la confiance est alors limitée.

## Arbitrages historiques prioritaires (date, faits, limites, mode de vérification)

### Bassora (siège vs occupation) — R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0018
Le 1 janvier 1776 Bassora est assiégée mais non occupée par les Zand; prise en avril 1776. Références : `R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S003` ; `R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S004` ; `R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S005`. **Action :** confronter cartes administratives / listes de forts / fiscalité locale au bitmap puis valider l’interface avec le responsable secondaire si applicable.

### Khorasan afsharide vs Zand — R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0063
Shahrokh gouverne Mashhad jusqu’en 1795; ne pas projeter PER=Zand sur tout Khorasan. Références : `R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S006` ; `R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S005`. **Action :** confronter cartes administratives / listes de forts / fiscalité locale au bitmap puis valider l’interface avec le responsable secondaire si applicable.

### Empire Durrani / Kalat — R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0098
Kalat dispose d’un traité de suzeraineté et de très large autonomie; Pishin reste sous les Durrani. Références : `R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S020` ; `R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S019`. **Action :** confronter cartes administratives / listes de forts / fiscalité locale au bitmap puis valider l’interface avec le responsable secondaire si applicable.

### Khanats du Caucase — R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0013
Khanat d’Erevan avec fiscalité locale (meliks); ne pas interpréter suzeraineté culturelle persane comme PER directe. Références : `R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S009` ; `R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S008`. **Action :** confronter cartes administratives / listes de forts / fiscalité locale au bitmap puis valider l’interface avec le responsable secondaire si applicable.

### Frontière caucasienne russe — R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0117
Forte étude chronologique: création des postes Stavropol 1777, non 1776. Références : `R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S012`. **Action :** confronter cartes administratives / listes de forts / fiscalité locale au bitmap puis valider l’interface avec le responsable secondaire si applicable.

### Nord/Nil, Dongola — R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0028, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0029
Sources décrivent un mak de Dongola avant conquête Shayqiyya dans les années 1780; TUR doit être justifié par présence concrète. Références : `R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S034`. **Action :** confronter cartes administratives / listes de forts / fiscalité locale au bitmap puis valider l’interface avec le responsable secondaire si applicable.

### Galilée et Acre — R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0104
Zahir al-Umar est mort le 22 août 1775; reconquête locale à préciser en 1776. Références : `R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S036`. **Action :** confronter cartes administratives / listes de forts / fiscalité locale au bitmap puis valider l’interface avec le responsable secondaire si applicable.

### Pays kazakhs / Russie Qing — R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0118, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0119, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0120, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0121
Traités et reconnaissance de souveraineté ne prouvent pas l’impôt ni le garnisonnement des steppes. Références : `R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S017` ; `R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S016`. **Action :** confronter cartes administratives / listes de forts / fiscalité locale au bitmap puis valider l’interface avec le responsable secondaire si applicable.

### Kokand — R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0118, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0119, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0120, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0121
Les conquêtes de Kokand après 1799/1805 ne peuvent être rétroprojetées vers 1776. Références : `R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S013`. **Action :** confronter cartes administratives / listes de forts / fiscalité locale au bitmap puis valider l’interface avec le responsable secondaire si applicable.

### Bahrain et côte du Golfe — R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0001, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0002, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0003
1753-1783 domination persane de Bahrain insulaire; ne pas la confondre avec BHN sur littoral Arab Emirates. Références : `R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S030`. **Action :** confronter cartes administratives / listes de forts / fiscalité locale au bitmap puis valider l’interface avec le responsable secondaire si applicable.

### Régences Maghreb — R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0009
Deys et beys locaux; lien symbolique à la Porte à distinguer du contrôle effectif. Références : `R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S023` ; `R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S024` ; `R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S025`. **Action :** confronter cartes administratives / listes de forts / fiscalité locale au bitmap puis valider l’interface avec le responsable secondaire si applicable.

### Mauritanie et Sahara — R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0085, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0086, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0087, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0088, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0089, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0090
Emirats et réseaux de tribut sans frontière linéaire stable. Références : `R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S026` ; `R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S027`. **Action :** confronter cartes administratives / listes de forts / fiscalité locale au bitmap puis valider l’interface avec le responsable secondaire si applicable.

## Contradictions non résolues : conserver UNRESOLVED

1. **Cartes impériales vs études des pouvoirs effectifs** : cartes Chatelain 1719 et de la période 1740 (`R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S041`, `R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S042`) illustrent frontières revendiquées, caravanes et régions; elles sont antérieures à la rupture de 1747 et insuffisantes pour attester 1776. Privilégier travaux localisés et sources fiscales pour chaque ville.
2. **Caucase** : chancelleries géorgienne et iranienne expriment des droits revendiqués; les khans et meliks ont leurs propres systèmes fiscaux; aucun transfert R2/R3 sans carte d’implantation.
3. **Centres religieux vs souveraineté** : Sharifat du Hedjaz, imamat zaydite et confréries transsahariennes ne prouvent aucune occupation au-delà des zones administrées.
4. **Durrani** : Iranica Afghanistan et Kabul indiquent un transfert de la capitale en **1775**, mais l’article Kandahar v. indique **1774** (`R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S037`). La capitalité de Kaboul le 1776-01-01 est sûre; **année exacte contestée**, ne pas l’inscrire comme date unique.
5. **Khiva et Boukhara** : khans symboliques / ataliqs et inaqs effectifs. La souveraineté tributaire n’est pas un impôt uniforme sur Karakalpaks, Kazakhs et Turkmènes.
6. **Géoréférencement absent** : aucun fichier de polygones/provinces annotées géographiquement n’a permis de vérifier les tracés; **tous les couples sont MAPPING_REQUIRED**, y compris les non-changements. Utiliser `MAP_1776_BASELINE.csv` pour identifier les RGB candidats; jamais comme preuve de leur localisation historique.
7. **Interprétation des TAGs** : PER désigne une abstraction « Persia », IR1 un pashalik « Mamluk Iraq », MAS un nom « Mascara », CAUC un agrégat « Caucuses », ABB une unité « Arab Emirates »; aucun n’équivaut à un titulaire unifié prouvé en 1776.

## Registre de doublons techniques transmis sans arbitrage historique

- `MAP0-0018` — `STATE_AL_RIF` / `xA0B0C0` : Attributions écrites: MOR|SPA; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0019` — `STATE_AL_RIF` / `xCA9F75` : Attributions écrites: MOR|SPA; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0020` — `STATE_INNER_MOROCCO` / `x0FA44F` : Attributions écrites: MOR|TEK; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0021` — `STATE_INNER_MOROCCO` / `x4DE76B` : Attributions écrites: MOR|TEK; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0022` — `STATE_INNER_MOROCCO` / `x53C5EF` : Attributions écrites: MOR|TEK; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0023` — `STATE_INNER_MOROCCO` / `x88C527` : Attributions écrites: MOR|TEK; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0024` — `STATE_INNER_MOROCCO` / `x8ACEDE` : Attributions écrites: MOR|TEK; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0025` — `STATE_INNER_MOROCCO` / `x8DCD09` : Attributions écrites: MOR|TEK; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0026` — `STATE_INNER_MOROCCO` / `x9E582E` : Attributions écrites: MOR|TEK; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0027` — `STATE_INNER_MOROCCO` / `xE80E2E` : Attributions écrites: MOR|TEK; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0028` — `STATE_INNER_MOROCCO` / `xF414B2` : Attributions écrites: MOR|TEK; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0029` — `STATE_TRIPOLI` / `xAFD438` : Attributions écrites: TRI|ZWY|ZWY; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0030` — `STATE_TRIPOLI` / `xD5C61D` : Attributions écrites: TRI|ZWY|ZWY; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0044` — `STATE_MAURITANIA` / `x1C026D` : Attributions écrites: OUA|ADR; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0045` — `STATE_MAURITANIA` / `x1F8376` : Attributions écrites: OUA|ADR; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0046` — `STATE_MAURITANIA` / `x5F1D19` : Attributions écrites: OUA|ADR; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0047` — `STATE_MAURITANIA` / `xAC39A0` : Attributions écrites: OUA|ADR; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0048` — `STATE_MAURITANIA` / `xD34BB3` : Attributions écrites: OUA|ADR; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0049` — `STATE_MAURITANIA` / `xF1E6C3` : Attributions écrites: OUA|ADR; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0053` — `STATE_KUBAN` / `xBCF376` : Attributions écrites: CRI|CIR; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0061` — `STATE_NORTH_CAUCASUS` / `x019041` : Attributions écrites: CAUC|CHC; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0062` — `STATE_NORTH_CAUCASUS` / `x23F98B` : Attributions écrites: CAUC|CIR; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0063` — `STATE_NORTH_CAUCASUS` / `x2790A8` : Attributions écrites: CAUC|CIR; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0064` — `STATE_NORTH_CAUCASUS` / `x56FD87` : Attributions écrites: CAUC|CIR; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0065` — `STATE_NORTH_CAUCASUS` / `x668A47` : Attributions écrites: CAUC|CIR; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0066` — `STATE_NORTH_CAUCASUS` / `x83F33B` : Attributions écrites: CAUC|CIR; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0067` — `STATE_NORTH_CAUCASUS` / `xC05001` : Attributions écrites: CAUC|CIR; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0068` — `STATE_NORTH_CAUCASUS` / `xDA8EF4` : Attributions écrites: CAUC|CHC; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0112` — `STATE_AL_RIF` / `xA0B0C0` : Attributions écrites: MOR|SPA; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0113` — `STATE_AL_RIF` / `xCA9F75` : Attributions écrites: MOR|SPA; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0114` — `STATE_INNER_MOROCCO` / `x0FA44F` : Attributions écrites: MOR|TEK; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0115` — `STATE_INNER_MOROCCO` / `x4DE76B` : Attributions écrites: MOR|TEK; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0116` — `STATE_INNER_MOROCCO` / `x53C5EF` : Attributions écrites: MOR|TEK; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0117` — `STATE_INNER_MOROCCO` / `x88C527` : Attributions écrites: MOR|TEK; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0118` — `STATE_INNER_MOROCCO` / `x8ACEDE` : Attributions écrites: MOR|TEK; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0119` — `STATE_INNER_MOROCCO` / `x8DCD09` : Attributions écrites: MOR|TEK; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0120` — `STATE_INNER_MOROCCO` / `x9E582E` : Attributions écrites: MOR|TEK; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0121` — `STATE_INNER_MOROCCO` / `xE80E2E` : Attributions écrites: MOR|TEK; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0122` — `STATE_INNER_MOROCCO` / `xF414B2` : Attributions écrites: MOR|TEK; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0123` — `STATE_TRIPOLI` / `xAFD438` : Attributions écrites: TRI|ZWY|ZWY; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0124` — `STATE_TRIPOLI` / `xD5C61D` : Attributions écrites: TRI|ZWY|ZWY; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0138` — `STATE_MAURITANIA` / `x1C026D` : Attributions écrites: OUA|ADR; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0139` — `STATE_MAURITANIA` / `x1F8376` : Attributions écrites: OUA|ADR; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0140` — `STATE_MAURITANIA` / `x5F1D19` : Attributions écrites: OUA|ADR; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0141` — `STATE_MAURITANIA` / `xAC39A0` : Attributions écrites: OUA|ADR; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0142` — `STATE_MAURITANIA` / `xD34BB3` : Attributions écrites: OUA|ADR; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0143` — `STATE_MAURITANIA` / `xF1E6C3` : Attributions écrites: OUA|ADR; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0147` — `STATE_KUBAN` / `xBCF376` : Attributions écrites: CRI|CIR; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0156` — `STATE_NORTH_CAUCASUS` / `x019041` : Attributions écrites: CAUC|CHC; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0157` — `STATE_NORTH_CAUCASUS` / `x23F98B` : Attributions écrites: CAUC|CIR; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0158` — `STATE_NORTH_CAUCASUS` / `x2790A8` : Attributions écrites: CAUC|CIR; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0159` — `STATE_NORTH_CAUCASUS` / `x56FD87` : Attributions écrites: CAUC|CIR; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0160` — `STATE_NORTH_CAUCASUS` / `x668A47` : Attributions écrites: CAUC|CIR; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0161` — `STATE_NORTH_CAUCASUS` / `x83F33B` : Attributions écrites: CAUC|CIR; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0162` — `STATE_NORTH_CAUCASUS` / `xC05001` : Attributions écrites: CAUC|CIR; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.
- `MAP0-0163` — `STATE_NORTH_CAUCASUS` / `xDA8EF4` : Attributions écrites: CAUC|CHC; **UNRESOLVED**; ne pas déduire la souveraineté de la syntaxe conflictuelle.

## Autres issues MAP0 du registre R3, sans arbitrage historique

Au total 82 enregistrements MAP0 pertinents pour les State_ID de R3 : DUPLICATE_PROVINCE_OWNER: 56, ORPHAN_HISTORY_SELECTOR: 12, CATALOGUE_PAIR_MISMATCH: 12, CAPITAL_NOT_OWNED: 2. Les lignes techniques et les divergences de catalogue **ne démontrent aucune souveraineté**.
- `MAP0-0079` (CAPITAL_NOT_OWNED) — `STATE_AKMOLINSK` : UZH: capitale définie non possédée au départ; peut être remplacée par script.; analyse historique non tranchée par le constat technique; disposition du registre : DOCUMENT_ONLY.
- `MAP0-0080` (ORPHAN_HISTORY_SELECTOR) — `STATE_ALGIERS` : pops / FRA sans territoire correspondant.; analyse historique non tranchée par le constat technique; disposition du registre : DOCUMENT_ONLY.
- `MAP0-0081` (ORPHAN_HISTORY_SELECTOR) — `STATE_CONSTANTINE` : pops / FRA sans territoire correspondant.; analyse historique non tranchée par le constat technique; disposition du registre : DOCUMENT_ONLY.
- `MAP0-0082` (ORPHAN_HISTORY_SELECTOR) — `STATE_ORAN` : pops / FRA sans territoire correspondant.; analyse historique non tranchée par le constat technique; disposition du registre : DOCUMENT_ONLY.
- `MAP0-0084` (ORPHAN_HISTORY_SELECTOR) — `STATE_ALGIERS` : buildings / FRA sans territoire correspondant.; analyse historique non tranchée par le constat technique; disposition du registre : DOCUMENT_ONLY.
- `MAP0-0085` (ORPHAN_HISTORY_SELECTOR) — `STATE_CONSTANTINE` : buildings / FRA sans territoire correspondant.; analyse historique non tranchée par le constat technique; disposition du registre : DOCUMENT_ONLY.
- `MAP0-0086` (ORPHAN_HISTORY_SELECTOR) — `STATE_ORAN` : buildings / FRA sans territoire correspondant.; analyse historique non tranchée par le constat technique; disposition du registre : DOCUMENT_ONLY.
- `MAP0-0174` (CAPITAL_NOT_OWNED) — `STATE_AKMOLINSK` : UZH: capitale définie non possédée au départ; peut être remplacée par script.; analyse historique non tranchée par le constat technique; disposition du registre : DOCUMENT_ONLY.
- `MAP0-0175` (ORPHAN_HISTORY_SELECTOR) — `STATE_ALGIERS` : pops / FRA sans territoire correspondant.; analyse historique non tranchée par le constat technique; disposition du registre : DOCUMENT_ONLY.
- `MAP0-0176` (ORPHAN_HISTORY_SELECTOR) — `STATE_CONSTANTINE` : pops / FRA sans territoire correspondant.; analyse historique non tranchée par le constat technique; disposition du registre : DOCUMENT_ONLY.
- `MAP0-0177` (ORPHAN_HISTORY_SELECTOR) — `STATE_ORAN` : pops / FRA sans territoire correspondant.; analyse historique non tranchée par le constat technique; disposition du registre : DOCUMENT_ONLY.
- `MAP0-0180` (ORPHAN_HISTORY_SELECTOR) — `STATE_ALGIERS` : buildings / FRA sans territoire correspondant.; analyse historique non tranchée par le constat technique; disposition du registre : DOCUMENT_ONLY.
- `MAP0-0181` (ORPHAN_HISTORY_SELECTOR) — `STATE_CONSTANTINE` : buildings / FRA sans territoire correspondant.; analyse historique non tranchée par le constat technique; disposition du registre : DOCUMENT_ONLY.
- `MAP0-0182` (ORPHAN_HISTORY_SELECTOR) — `STATE_ORAN` : buildings / FRA sans territoire correspondant.; analyse historique non tranchée par le constat technique; disposition du registre : DOCUMENT_ONLY.
- `MAP0-0191` (CATALOGUE_PAIR_MISMATCH) — `STATE_GREATER_CAUCASUS` : CAUC; analyse historique non tranchée par le constat technique; disposition du registre : DOCUMENT_ONLY.
- `MAP0-0192` (CATALOGUE_PAIR_MISMATCH) — `STATE_GREATER_CAUCASUS` : GEO; analyse historique non tranchée par le constat technique; disposition du registre : DOCUMENT_ONLY.
- `MAP0-0195` (CATALOGUE_PAIR_MISMATCH) — `STATE_LOWER_EGYPT` : EGY; analyse historique non tranchée par le constat technique; disposition du registre : DOCUMENT_ONLY.
- `MAP0-0196` (CATALOGUE_PAIR_MISMATCH) — `STATE_LOWER_EGYPT` : TUR; analyse historique non tranchée par le constat technique; disposition du registre : DOCUMENT_ONLY.
- `MAP0-0197` (CATALOGUE_PAIR_MISMATCH) — `STATE_MATRUH` : EGY; analyse historique non tranchée par le constat technique; disposition du registre : DOCUMENT_ONLY.
- `MAP0-0198` (CATALOGUE_PAIR_MISMATCH) — `STATE_MATRUH` : TUR; analyse historique non tranchée par le constat technique; disposition du registre : DOCUMENT_ONLY.
- `MAP0-0199` (CATALOGUE_PAIR_MISMATCH) — `STATE_MIDDLE_EGYPT` : EGY; analyse historique non tranchée par le constat technique; disposition du registre : DOCUMENT_ONLY.
- `MAP0-0200` (CATALOGUE_PAIR_MISMATCH) — `STATE_MIDDLE_EGYPT` : TUR; analyse historique non tranchée par le constat technique; disposition du registre : DOCUMENT_ONLY.
- `MAP0-0202` (CATALOGUE_PAIR_MISMATCH) — `STATE_SINAI` : EGY; analyse historique non tranchée par le constat technique; disposition du registre : DOCUMENT_ONLY.
- `MAP0-0203` (CATALOGUE_PAIR_MISMATCH) — `STATE_SINAI` : TUR; analyse historique non tranchée par le constat technique; disposition du registre : DOCUMENT_ONLY.
- `MAP0-0205` (CATALOGUE_PAIR_MISMATCH) — `STATE_UPPER_EGYPT` : EGY; analyse historique non tranchée par le constat technique; disposition du registre : DOCUMENT_ONLY.
- `MAP0-0206` (CATALOGUE_PAIR_MISMATCH) — `STATE_UPPER_EGYPT` : TUR; analyse historique non tranchée par le constat technique; disposition du registre : DOCUMENT_ONLY.

Les événements `MAP0-0195` et suivants marquent notamment l’insertion des États EGY absents de l’ancien catalogue : conserver les couples actuels tels quels. Le candidat `georg3mx` **n’est pas fusionné dans main**; ne pas appliquer sa carte provisoire.

## Interfaces et transmission

- **R2_NORTHERN_CENTRAL_EASTERN_EUROPE** : Caucase, Kuban et frontières russes des steppes; R3 seul responsable de ses pixels. 20 couples en interface; exemples R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0005, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0006, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0013, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0015, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0023, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0024, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0025, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0041, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0068, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0069, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0099, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0100….
- **R4_SOUTH_ASIA** : Kalat, Quetta/Pishin, Pashtunistan/Khyber, Balkh et Herat. 9 couples en interface; exemples R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0017, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0020, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0045, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0055, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0056, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0098, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0105, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0115, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0116.
- **R7_SUBSAHARAN_AFRICA** : Dongola/Sennar, Nil, déserts et Fouta Toro, Sahara mauritanien. 20 couples en interface; exemples R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0028, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0029, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0030, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0031, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0032, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0033, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0034, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0035, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0047, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0048, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0049, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-0085….

**Règle de transmission :** les secondaires examinent le chevauchement mais ne produisent aucun duplicata R3; tout transfert R3→R2/R4/R7 doit être arbitré centralement par Change_ID et non par préséance automatique.

## OUTSIDE_BASELINE — signalements sans attribution

- Les entités historiques distinctes des TAGs actuellement listés en R3 — État afsharide de Mashhad, khanats d’Erevan/Qarabagh/Ganja, Khanat de Kalat, makks nubiennes — pourraient disposer d’un TAG dans **la nomenclature complète hors R3**. Vérifier avant toute demande de nouveau TAG.
- Les frontières des royaumes du Fouta, de Sennar et des corps d’armée russes hors des `State_ID` R3 appartiennent à R7/R2; **aucun couple externe** ajouté à `COVERAGE`.
- Le Gwadar omanais attesté à partir de **1784** (`R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S029`) ne doit pas être représenté comme possession OMA en 1776; l’attribution éventuelle aux provinces R4 doit être instruite par R4.

## Plan de mapping et décision centrale

1. Pour chaque `CHANGE_PROPOSED`, établir table d’identité entre toponyme historique et RGB du bitmap, avec source précise, carte géoréférencée, échelle, et l’avis R2/R4/R7 si requis.
2. Appliquer **A_EXISTING_PROVINCES** si la frontière tient dans les RGB ; sinon **B_STATE_REGIONS** si le moteur permet le compromis. **C_GEOMETRY** interdit en l’absence de démonstration d’insuffisance de A/B.
3. Les relations de sujet nécessitent revue à part ; aucune redistribution automatique de population/bâtiments/ports, aucune altération VEN/GEN.
4. Les problèmes sans résolution sont enregistrés `UNRESOLVED`; pas d’application à `main` sans décision humaine.

## Sources majeures opposées, biais et références de contrôle

| Problème | Sources de contrôle | Nature du désaccord |
|---|---|---|
| Égypte | R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S001 / R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S002 vs baseline EGY puppet | Lien ottoman juridique, pouvoirs mamelouks effectifs; « puppet » sous-décrit 1775–76 |
| Palestine | R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S036 vs cartes impériales R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S041 | Fin de l’autonomie Zahir août 1775, cartes antérieures statiques |
| Caucase | R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S009, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S008, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S010 vs R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S042 | Autonomies de khanats/meliks contre grande frontière perse revendiquée |
| 1776 puis avril 1776 | R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S003, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S004, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S005 | Siège de Bassora au 1er janvier, **prise seulement avril** |
| Khorasan | R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S006 vs R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S005 | Domination Zand ailleurs, Shahrokh Afshar à Mashhad |
| Sahara | R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S026, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S027 vs R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S041 | Réseaux fiscaux et parcours pastoraux contre limites colorées d’atlas |
| Khyber/Kalat | R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S021, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S020 vs R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S019 | Seigneurie impériale nominale, autonomie de chefs |
| Khiva/Kokand | R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S015, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S013 vs R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA-S042 | Frontières ultérieures et mosaïque des oasis en 1776 |

---
*Ce lot est limité par l’absence de cartographie 1776 géoréférencée du bitmap et par la documentation locale lacunaire de plusieurs déserts et zones de montagne. Les statuts reflètent cette incertitude; ils ne constituent pas une certification historique exhaustive.*
