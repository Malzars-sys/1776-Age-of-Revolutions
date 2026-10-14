# R4_SOUTH_ASIA — incertitudes, arbitrages et transmission

**Périmètre principal :** sous-continent indien, Baloutchistan/Quetta inclus dans R4, Ceylan, Himalaya de la liste canonique. **Date arrêtée : 1776-01-01.**

**Statut : étude documentaire et recommandations seulement.** Aucun fichier historique du mod, bitmap, carte, population, bâtiment ou dépôt Git n’a été modifié. La baseline provient du `main` existant; la branche candidate `georg3mx` n’est pas incluse. Les couples `Owner_TAG + State_ID` sont des identifiants d’inventaire, pas des conclusions. Les 54 couples ont été parcourus, mais cela ne vaut pas validation des frontières province par province.

## 1. Couverture et conformité

- **54 couples** différents, **29 State_ID** distincts : 23 `REVIEWED_NO_CHANGE`, 8 `CHANGE_PROPOSED`, 23 `UNRESOLVED`.
- **62 lignes de recommandation**, incluant **8 propositions supplémentaires** au sein de State_ID déjà listés, identifiées par un Change_ID distinct mais sans ajouter de couple canonique. **58 entrées bibliographiques** (certaines sont des références parallèles, et non des confirmations indépendantes).
- Toutes les recommandations sont datées `1776-01-01`; Province_ID / Province_IDs sont **vides** et `Mapping_Status=MAPPING_REQUIRED`. Aucune superposition vérifiée entre les cartes historiques et le bitmap RGB n’a été menée. **Aucune recommandation ne doit être intégrée avant cartographie.**
- `NEW_TAG_REQUIRED` exprime une lacune de représentation, **pas** un TAG créé. Des variantes régionales (Kalat, Ahom, Kandy, Carnatic, Thanjavur, Gaekwad, Jaipur/Jodhpur, etc.) nécessitent une recherche dans le registre global des TAGs avant toute décision. Même si un TAG historique existe ailleurs, son inclusion dans R4 ne peut pas être supposée.
- `REVIEWED_NO_CHANGE` signifie **pas de correction territoriale établie à ce stade**, et non confirmation définitive de chacun des RGB. Des lignes `UNRESOLVED` ne sont pas des transferts approuvés.

## 2. Corrections étayées et points majeurs à arbitrer

### 2.1 Compagnie des Indes orientales britannique et souverainetés mogholes

- **Bengale/Bihar/Awadh :** *diwani* obtenue en 1765 pour le Bengale, le Bihar et une Orissa fiscale nominale, avec réforme de perception en 1772–77. Distinguer administration/revenus des plaines, souveraineté moghole nominale, nawabs et frontières autonomes des hautes terres (Khasi, Jaintia, Tripura). Les droits de la Compagnie sur Bénarès datent de 1775 et ne créent pas une administration britannique sur toute l’Awadh. `STATE_AWADH/BIC` reste `UNRESOLVED` faute de vérification géographique; `STATE_BIHAR/BIC` ne doit pas être élargi sans preuve. Réfs : `R4_SOUTH_ASIA-S001`, `S051`, `S052`; Rennell `S002` comme outil cartographique ultérieur à la date cible.
- **Bombay** : le couple BIC manque dans le `STATE_BOMBAY` initial. Depuis 1668, l’île de Bombay est administrée par la Compagnie; Salsette est conquise en 1774 mais son titre demeure disputé jusqu’aux règlements ultérieurs. **`R4_SOUTH_ASIA-0056`** propose une enclave BIC aux lieux précis et sépare `DIRECT_ADMINISTRATION` des îles de Bombay de `MILITARY_CONTROL` à Salsette. Il faut raffiner cette ligne en deux en cas de mapping distinct, sans créer une superficie BIC arbitraire. Réfs : `S057`, `S048`.
- **Circars** : les traités de 1766/1768 reconnaissent à la Compagnie l’autorité sur quatre Circars côtiers, mais **Guntur** demeure sous Basalat Jang et ne passe sous son pouvoir qu’en **1789**. `R4_SOUTH_ASIA-0060` porte cette exception; contrôler les RGB `STATE_CIRCARS/BIC` avant correction. Réf : `S005`, traités originaux cités : Aitchison vol VIII, pp. 280, 283, 285. Le `STATE_CIRCARS/JEY` doit être distingué de l’administration des ports.
- **Jeypore** : le dossier historique est plus nuancé qu’une simple autonomie intacte. Le *Gazetteer* de W. Francis (1907) rapporte la concession fiscale de 1769 à Vizianagram et **la prise/destruction du fort de Jeypore le 11 mars 1775**, mais aussi le maintien de territoires montagneux par Vikrama Deo I; un rétablissement indirect avant 1777 est affirmé sans date. **En janvier 1776 : contrôle mixte/fluctuant à cartographier, pas absorption automatique de toutes les hautes terres par BIC.** Réf `S056`, section Jeypore Taluk, spécialement 1768–1784 (s’appuie sur consultations militaires de 1768, 1775 et rapports de 1784).
- **Orissa** : les Bhonsle du Nagpur tiennent la province côtière jusqu’en 1803, malgré la portée nominale de la *diwani* de 1765. Ne pas assimiler Cuttack/Puri/Balasore aux hautes terres de principautés tributaires. `STATE_ORISSA/NAG` : absence de transfert conclu, ne corriger que les doublons techniques dans un lot distinct. Réfs : `S003` p. 431, `S004`.

### 2.2 Baloutchistan, Quetta, Makran et Gwadar — interface R3

- **`R4_SOUTH_ASIA-0009` (DUR/Baluchistan)** : Kalat sous Mir Nasir Khan I exerce une administration locale forte. La lecture de l’accord de 1758 diffère entre l’*Encyclopaedia Iranica* (`S012/S038`, reconnaissance de suzeraineté durranie) et Sajidi–Hussain (`S039`, souveraineté du khanat). **`UNRESOLVED`** pour la relation de jure et l’étendue exacte de la souveraineté effective. Le contraste n’autorise pas à colorier tous les pixels comme possession directe durranie.
- **`R4_SOUTH_ASIA-0010` (OMA/Baluchistan)** : `S013/S054`, J. G. Lorimer, *Gazetteer of the Persian Gulf*, vol. I, **p. 602**, situe la concession de **Gwadar en 1784** et rapporte que, vers **1778**, les Gichki tenaient encore l’administration des districts côtiers, avec partage de revenus. Cela invalide **un contrôle omanais déjà en janvier 1776**, mais ne permet pas de décider qui, parmi Kalat/Gichki/chefferies de Makran, doit être représenté comme propriétaire unique. La concession de 1784 elle-même est controversée quant à sa nature perpétuelle. Vérifier le pixel OMA avant de changer.
- **`R4_SOUTH_ASIA-0047` (DUR/Quetta)** : Quetta/Shal, Pishin, Bolan : suzeraineté durranie et contrôle kalati local ne coïncident pas avec une ligne frontalière vérifiée. `Cross_Region_Conflict=DISPUTED` avec **R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA** pour les limites de l’Afghanistan principal, sans transfert de propriété de recherche à R3.

### 2.3 Pendjab, Delhi, Rajputana et domaine marathe

- **Pendjab `R4_SOUTH_ASIA-0045` / `-0046`** : Lahore pris par les *misls* en 1765 et Sirhind en 1764. En 1776, la confédération est plurielle, non l’empire sikh unifié de Ranjit Singh. Les garnisons durranies à l’ouest (Multan et secteurs proches) demandent un examen militaire. `STATE_HILL_PUNJAB/DUR` et `STATE_PUNJAB/DUR` ne peuvent être gardés sur la seule base d’une carte d’Empire durrani à son extension maximale. Réf `S014`.
- **Rajputana `R4_SOUTH_ASIA-0048`** : les cours de Jaipur, Jodhpur/Marwar, Mewar/Udaipur, Bikaner, Kota et Bundi ne sont pas de simples districts directement administrés par Scindia. Préconiser un découpage entre principautés, mais la documentation spécifique de 1776 (revenus, sanads, campagnes) reste faible; les sources `S046/S049` sont des synthèses secondaires et un article de presse discutant la cartographie, **pas des preuves de limites fiables**. Relever la faiblesse avant validation; aucun nouveau TAG concret n’est donné.
- **Malwa / Gujarat / Bundelkhand** : la confédération marathe combine Gaekwad, Scindia, Holkar, Peshwa, Bhonsle et chefs autonomes. Les droits fiscaux et l’occupation d’un fort ne valent pas souveraineté sur toute une région. `STATE_GUJARAT/BHV`, `STATE_BUNDELKHAND/BIC` sont des propositions **provisoires à remapper** (`S021/S022/S025/S026/S047`) ; l’absence de registre de 1776 implique une priorité de réexamen. Le fort de Gwalior et Gohad ont une chronologie distincte des fiefs de Malwa (`S027`).

### 2.4 Asie du Sud péninsulaire : Mysore, Carnatic, Travancore

- **Mysore `STATE_MYSORE/MYS`** : distinguer Wodeyar nominal et autorité militaire/fiscale effective de **Haider Ali**. Conserver un `MYS` ne signifie pas identifier un monarque Wodeyar comme contrôleur de fait; Malabar/Coorg demandent vérification des tributs et fortifications. Réf `S050` (thèse, auteur/scan non entièrement contrôlés).
- **Madras `R4_SOUTH_ASIA-0040` et `-0061`** : le TAG `PUD` correspond à la petite principauté de Pudukkottai, non à la quasi-totalité du Carnatic. Distinguer nabab d’Arcot **Muhammad Ali Wallajah**, royaume de Thanjavur et fort/présidence de la Compagnie à Madras; aucune ligne géométrique actuelle n’est vérifiée. `S020` étaye Pudukkottai et `S006` le comptoir français; il manque une source administrative contemporaine détaillée pour le partage Arcot/Thanjavur, donc **aucune intégration** de la proposition globale.
- **Tranquebar et Serampore** : Compagnie asiatique danoise en 1776, passage à la Couronne **en 1777**. Les établissements ne justifient pas de souveraineté sur `STATE_MADRAS`/`STATE_WEST_BENGAL` entiers. `R4_SOUTH_ASIA-0058` signale Serampore sous `DENNOR`, `STATE_MADRAS/DENNOR` celui de Tranquebar. Réfs `S007/S008/S009/S044`.
- **Présences françaises** : Pondichéry, Karaikal, Mahé, Chandernagore, et Machilipatnam mentionnés dans la compilation de Puducherry comme restaurés à la France en 1765 (`S006` p. 203). `R4_SOUTH_ASIA-0057` signale **Chandernagore** absent de la baseline du Bengale occidental. Toute attribution doit être limitée au territoire/canton du comptoir, non à ses arrière-pays. Les autres localités seront investiguées dans `OUTSIDE_BASELINE` ci-dessous.
- **Travancore et Cochin** : Raja de Travancore et Raja de Cochin gardent leurs juridictions; `NET` correspond aux forts comptoirs VOC, `COC` au pouvoir royal local. Ne pas placer la dépendance de Cochin à Mysore au 1er janvier en se fondant sur des événements de **l’automne 1776**, notamment l’attaque de Chetva en octobre (`S030/S053`). `R4_SOUTH_ASIA-0062` signale **Anjengo/Anchuthengu**, un fort de la Compagnie sans souveraineté sur le district entier; vérifier aussi date exacte de son passage en résidence (`S045`).
- **Ceylan** : l’administration maritime néerlandaise `DEI` se limite aux zones côtières/fiefs associées. Le **royaume de Kandy**, dans les hautes terres, reste indépendant; il manque dans la baseline comme propriétaire distinct. `R4_SOUTH_ASIA-0059` : TAG neuf potentiellement nécessaire mais mapping uniquement après analyse des limites VOC/Kandy. La présence `GBR` initiale reste `UNRESOLVED` : un port/bâtiment britannique n’établit pas une domination britannique en 1776; conquête de la côte néerlandaise en **1796**. `MLD` peut viser les Maldives (atolls), dont le sultan conserve une administration locale sous l’hégémonie diplomatique néerlandaise revendiquée, ce qui exige un contrôle du bitmap. Réfs `S010/S011` pour Ceylan, et `S058` pour les Maldives (prépublication non évaluée par les pairs).

### 2.5 Assam et interfaces himalayennes — contact R5

- **Assam `R4_SOUTH_ASIA-0055`** : le royaume **Ahom**, gouverné par Lakshmi Singha (1769–1780), manque parmi `KKI, MGH, NGA, TIP` ; le contrôle de la vallée du Brahmapoutre ne peut pas être assigné à l’un de ces quatre groupes. Première rébellion Moamoria 1769–70; ne pas rétroprojeter les rebellions de 1782 ou 1786. Réf `S055`, *District Census Handbook Kamrup*, introduction historique. La présence des Khasi/Jaintia/Naga, Kuki et Tripura dans les montagnes exige des unités de souveraineté locale (`S017–S019`) plutôt qu’un État ethnique unifié.
- **Bhoutan/Cooch Behar** : traité de 1774 (en particulier Chichacotta, Paglahaut, Kyranti, Maraghat, Luckeepur ; tribut cinq chevaux) après guerre de 1772–74. Distinguer les Duars, domaines du Druk Desi, protection fiscale de la Compagnie et gouvernance du Raja de Cooch Behar. Sources `S015/S016` et la transcription du traité ; superposition nécessaire. Une affirmation diplomatique de relation au Tibet ne suffit pas à identifier administration tibétaine. Région secondaire **R5_EAST_ASIA**.
- **Sikkim et Népal** : Phuntsog Namgyal II gouverne le Sikkim ; Pratap Singh Shah le royaume Gorkha/Népal. Les grandes frontières contemporaines (Sikkim/Népal/Tibet/Bhoutan) et les conquêtes Gorkha ultérieures ne valent pas carte de 1776; vérifier Rabdentse, Teesta, Duars, Chumbi et hauts cols (`S034/S035`). Ne transférer aucun de ces pixels à R5 sans revue de l’interface.

## 3. Contradictions et obstacles non résolus

| ID / ensemble | Contradiction ou lacune | Preuve indispensable pour trancher |
|---|---|---|
| `R4_SOUTH_ASIA-0009 / 0010 / 0047` | Kalat tributaire ou souverain; Pishin/Quetta/Makran et administration Gichki; `S012` contre `S039`, Lorimer `S013` sur recettes | Traité de Kalat 1758 original, cadastres/revenus, contrôles de forts, cartes XVIIIe à grande échelle; revue R3 |
| `R4_SOUTH_ASIA-0017 / 0024 / 0060` | Étendue des perceptions de BIC au Bundelkhand et Circars; Guntur exclu; Jeypore 1775 fort pris puis souveraineté mixte | Archives consultations Madras 1768–1777, revenue correspondence, comptes des zamindars, relevé Guntur |
| `R4_SOUTH_ASIA-0022 / 0059` | Ceylan DEI et GBR et enclave Kandy, Maldives mal rattachées | Cartes VOC 1770s avec capitaineries/coûtumes et citadelles; carte Kandy et Maldives; superposition RGB |
| `R4_SOUTH_ASIA-0031 / 0048` | Portée réelle des confédérations Gaekwad et Scindia sur les États indiens autonomes | Comptes de perception, traités Rajput, listes de thanadars et garrisons par district 1774–1776 |
| `R4_SOUTH_ASIA-0033 / 0045 / 0046` | Contrôle sikh/misl vs garnisons durranies au Pendjab et Hill Punjab | Journaux des campagnes, listes des forts, relevés de rajas et tributs, toponymie 1776 |
| `R4_SOUTH_ASIA-0049` | Règne exact Kalhora en janvier 1776 : Ghulam Nabi/Abdul Nabi ; chronologies incompatibles (`S032` secondaire indirect vs `S033` anonyme) | Chronique de cour / sanad durrani daté, étude prosopographique critique; laisser `UNRESOLVED` |
| `R4_SOUTH_ASIA-0055` | Royaume Ahom absent, mais où sont ses provinces et les autonomies du Barak/Assam? | Carte du régime paik/forts Ahom ca 1775 et correspondance avec états/couleurs RGB; revue R5 |
| `R4_SOUTH_ASIA-0056 / 0057 / 0058 / 0062` | Enclaves de taille inférieure aux provinces du mod; possible inadéquation de la géométrie | Image bitmap provinces sur carte géoréférencée et valeurs RGB existantes; essais méthode A, puis B; C seulement démontré |

### Registre MAP-0 : anomalies purement techniques

- **`MAP0-0031/0032/0033`** (`main`) et **`MAP0-0125/0126/0127`** (candidat) : `STATE_ORISSA`, même TAG **NAG** répété pour `xA0A8E0`, `xA15F01`, `x30C2D5`. Ce ne sont **pas** des preuves que Nagpur possède deux territoires ou qu’il faut faire un transfert : c’est un doublon de syntaxe à corriger dans une phase technique distincte.
- **`MAP0-0069/0070`** (`main`) et **`MAP0-0164/0165`** (candidat) : `STATE_EASTERN_HIMALAYAS`, `x84F73C` et `x665E5B` attribués à **TIB et BHU**. Bloque l’exploitation cartographique et exige relevé du lieu précis; ne tranche pas le contrôle de jure. Coordination R5 obligatoire.
- **`MAP0-0072`** et **`MAP0-0167`** : capitale de `COO` définie mais non possédée initialement; **`MAP0-0076`** et **`MAP0-0171`** : même anomalie pour `JEY`. Ne pas inférer le contrôle territorial de ces TAGs depuis un point de capitale. Vérifier scripts de démarrage.
- Les issues de `COLLABORATOR_CANDIDATE` ne reflètent pas un merge; **l’inventaire `main` est l’autorité technique de la mission**. La politique de protection `VEN/GEN` ne nécessite aucune action ici ; aucune donnée de population/bâtiment n’a été transférée.

## 4. OUTSIDE_BASELINE et lacunes sans attribution RGB

Territoires à faire arbitrer par la synthèse centrale : ne pas transformer ces lignes en propriétaires du mod avant identification d’un pixel et d’un TAG existant ou décision de création. Les cas 1–6 concernent potentiellement R4 et ne sont pas annexés à R3/R5.
- **Mahé (côte de Malabar, ~11.70°N 75.54°E)**, comptoir français restitué en 1765, absent des TAGs des États de Kerala étudiés; `S006`, sans province démontrée.
- **Karaikal (~10.93°N 79.84°E)** et possibles villages dépendants, possessions françaises mais non identifiées dans les couples de `STATE_MADRAS`; `S006`.
- **Machilipatnam / Masulipatam (~16.18°N 81.13°E)**, établissement français indiqué parmi les restitutions; vérifier droits de terrain versus usine commerciale et frontière avec `STATE_CIRCARS/BIC`; `S006`.
- **Fort St George / Madras (~13.08°N 80.29°E)**, centre de la Présidence BIC absent du propriétaire de `STATE_MADRAS` (actuellement DENNOR/FRA/PUD); documentation foncière administrative à apporter.
- **Thanjavur et royaume d’Arcot** au sud-est, juridictions politiques présentes mais non identifiées par TAG dans le baseline Madras; voir `-0040/-0061`.
- **Ahom de la vallée du Brahmapoutre** et **Kandy intérieur** : manquent comme propriétaires; signalements internes `-0055`, `-0059` évitent de perdre les cas de couverture.
- **Ladakh, Baltistan et enclaves périphériques du Cachemire** : hors contrôle direct des gouverneurs de la vallée; faire examiner les RGB `STATE_KASHMIR`, sans supposer le Tibet principal R5 ni l’Afghanistan principal R3.
- **Chefferies hors frontière linéaire des Khasi/Garo, Hill Tripura, Chittagong Hill Tracts, Naga, Kuki et Rajasthan** : ne pas les remplir par une souveraineté coloniale/fiscale supposée, faute d’administration vérifiable.

## 5. Chronologie postérieure au 1er janvier 1776 à ne pas rétroprojeter

| Date | Événement | Note |
|---|---|---|
| 1776-02-26 (selon une notice LOC contradictoire) | Carte Rennell du Bengale/Bihar datée après la référence | Le champ de datation LOC indique aussi 1792 sur d’autres métadonnées; inspecter l’exemplaire et la date de publication avant de l’utiliser |
| 1776-03-01 (à vérifier sur traité original) | Traité de Purandhar : régulation de la Première guerre anglo-marathe | Pas d’effet pré-1776; les textes secondaires ne suffisent pas pour attribuer Bassein/Salsette |
| 1776-10 (mois fourni, jour non établi) | Conflit de Haider Ali/Chetva sur côte Malabar | Le `S030/S053` est postérieur au 1er janvier ; ne pas projeter la soumission de Cochin |
| 1777 | Administration directe de la Couronne danoise à Serampore et Tranquebar | En 1776 les compagnies conservent les droits et l’organisation locale |
| 1778 (approx.) | Kalat obtient, d’après Lorimer, une part des revenus Gichki du Makran | Administration locale demeure alors Gichki; pas de recette Kalat acquise dès 1776 |
| 1782 | Traité de Salbai et reconnaissance plus durable des îles de Bombay/Salsette | Ne confondre titre et occupation de 1774 |
| 1784 | Concession de Gwadar à Sayyid Sultan b. Ahmad en exil | Réf `S013`, p602, droit exact disputé |
| 1789 | Compagnie prend le Guntur Circar sous forme d’administration fiscale/territoriale | Réf `S005` |
| 1796 | Prise britannique des provinces maritimes néerlandaises de Ceylan | Ne pas intégrer comme situation 1776 |
| 1803 | Conquête britannique de l’Orissa marathe; extension britannique en Inde centrale | Ne pas rétroprojeter sur `STATE_ORISSA` 1776 |
| 1815 | Convention de Kandy et fin de souveraineté du royaume de Kandy | Preuve a contrario de l’autonomie en 1776 |

## 6. Règles de passage à la synthèse et à la cartographie

1. **Vérifier la géographie** de chaque changement et de chaque `State_ID + Owner_TAG`, par coordonnées et noms de forts/villages, puis chercher les identifiants RGB existants. Ne jamais inventer un code `xRRGGBB`. Requêtes de superposition souhaitables : `STATE_BOMBAY`, `STATE_ASSAM`, `STATE_CEYLON`, `STATE_CIRCARS`, `STATE_WEST_BENGAL`, `STATE_MADRAS`, `STATE_EASTERN_HIMALAYAS`, `STATE_BALUCHISTAN`.
2. Commencer par **`A_EXISTING_PROVINCES`**, n’utiliser `B_STATE_REGIONS` que pour des frontières non représentables proprement en A, et ne demander `C_GEOMETRY` **qu’après la preuve** qu’aucun agrégat des provinces existantes n’est utilisable. Les drapeaux `Requires_State_Split` sont des alertes, pas des ordres.
3. Séparer **(a) fait historique**, **(b) correspondance à l’espace du jeu**, **(c) approximation jouable** et **(d) doute**. Les quatre rubriques sont distinctes dans les recommandations ; la date des changements postérieurs est placée en notes, jamais utilisée comme nouveau contrôle au 1776-01-01.
4. Refaire la qualification des points `UNRESOLVED` en produisant preuves contraires, ne pas arbitrer par majorité des sources. Donner priorité à l’administration fiscale effective, aux traités effectivement mis en oeuvre, aux fortifications et aux circonscriptions locales; les cartes d’Empire et du Raj ultérieur sont insuffisantes.
5. Confier **R3** l’examen d’interface Quetta/Shal/Pishin/Makran–Afghanistan; **R5** l’examen Tibet/Bhoutan/Sikkim, Assam extrême oriental et hauts cols. Ils commentent les mêmes Change_ID sans créer une recommandation géographique dupliquée.
6. **Validation centrale obligatoire** avant correction de capitale, province, sujets, bâtiments, population, chemins de fer, revenu de compagnie ou frontières. Aucune intégration automatique.

## 7. Limitations documentaires reconnues

- Cette recherche est une **préparation historique sourcée et un audit exhaustif au niveau des 54 couples**, **pas** une carte validée à l’échelle de tous leurs pixels. De nombreuses petites souverainetés n’ont pas d’acte précis de 1776 numérisé dans les sources accessibles.
- Des sources solides identifient le **contrôle général** (ex. Lorimer p.602, W. Francis et les consultations militaires citées, traité de 1774, Orissa Gazetteer p.431) ; d’autres entrées portent seulement un **contexte indirect** (`S022`, `S049`, `S050`, certains recensements et résumés encyclopédiques). Leur `Confidence`/texte `Unresolved_Uncertainty` doit primer sur une formulation géographique de synthèse.
- Les références répétées au **même** ouvrage dans `SOURCES.csv` ne sont **pas des corroborations indépendantes** (notamment S003/S041, S006/S029/S036, S010/S011 sur le même contexte, S013/S054, S019/S040). Certaines descriptions bibliographiques doivent être recontrôlées dans un catalogue avant une publication académique.
- Les noms des TAGs, leurs formes raccourcies et les noms des États sont des conventions du mod, non une preuve historique ou juridique. La description des entités historiques ne présume pas de leur reconnaissance comme État souverain moderne.

---

**Index automatique des lignes `UNRESOLVED` (pour priorisation) :**

- `R4_SOUTH_ASIA-0001` — STATE_AGRA / GAR : Kingdom of Garhwal; LOW (sources R4_SOUTH_ASIA-S035).
- `R4_SOUTH_ASIA-0002` — STATE_AGRA / MARATH : Maratha power and local Mughal/Jat domains; LOW (sources R4_SOUTH_ASIA-S025|R4_SOUTH_ASIA-S027).
- `R4_SOUTH_ASIA-0003` — STATE_ASSAM / KKI : Kuki clan territories; LOW (sources R4_SOUTH_ASIA-S017|R4_SOUTH_ASIA-S019).
- `R4_SOUTH_ASIA-0008` — STATE_AWADH / BIC : Benares zamindari / ceded Benares districts; MEDIUM (sources R4_SOUTH_ASIA-S051|R4_SOUTH_ASIA-S052).
- `R4_SOUTH_ASIA-0009` — STATE_BALUCHISTAN / DUR : Khanate of Kalat / Brahui-Baloch confederation; UNRESOLVED (sources R4_SOUTH_ASIA-S012|R4_SOUTH_ASIA-S039).
- `R4_SOUTH_ASIA-0015` — STATE_BOMBAY / SAT : Satara Chhatrapati court / Maratha local chiefs; LOW (sources R4_SOUTH_ASIA-S021).
- `R4_SOUTH_ASIA-0018` — STATE_CENTRAL_PROVINCES / HYD : Berar/Nizam estates and frontier districts; LOW (sources R4_SOUTH_ASIA-S005|R4_SOUTH_ASIA-S021).
- `R4_SOUTH_ASIA-0019` — STATE_CENTRAL_PROVINCES / MARATH : Peshwa-Maratha influence in Central India; LOW (sources R4_SOUTH_ASIA-S021|R4_SOUTH_ASIA-S027).
- `R4_SOUTH_ASIA-0021` — STATE_CEYLON / DEI : Dutch VOC maritime Ceylon; HIGH (sources R4_SOUTH_ASIA-S010|R4_SOUTH_ASIA-S011).
- `R4_SOUTH_ASIA-0022` — STATE_CEYLON / GBR : Kandyan kingdom or maritime anomaly (unmapped); UNRESOLVED (sources R4_SOUTH_ASIA-S010|R4_SOUTH_ASIA-S011).
- `R4_SOUTH_ASIA-0023` — STATE_CEYLON / MLD : Maldives Sultanate / atolls outside Lankan coast; LOW (sources R4_SOUTH_ASIA-S058).
- `R4_SOUTH_ASIA-0024` — STATE_CIRCARS / BIC : Four Northern Circars under Company grants; HIGH (sources R4_SOUTH_ASIA-S005).
- `R4_SOUTH_ASIA-0027` — STATE_EASTERN_HIMALAYAS / BHU : Bhutan Druk polity; MEDIUM (sources R4_SOUTH_ASIA-S015|R4_SOUTH_ASIA-S016).
- `R4_SOUTH_ASIA-0029` — STATE_EASTERN_HIMALAYAS / TIB : Tibetan monastic administration / Himalayan local authorities; LOW (sources R4_SOUTH_ASIA-S016|R4_SOUTH_ASIA-S028).
- `R4_SOUTH_ASIA-0030` — STATE_EAST_BENGAL / BIC : Eastern Bengal/Sylhet/Chittagong diwani and autonomous hill tracts; MEDIUM (sources R4_SOUTH_ASIA-S001|R4_SOUTH_ASIA-S018|R4_SOUTH_ASIA-S019).
- `R4_SOUTH_ASIA-0033` — STATE_HILL_PUNJAB / DUR : Hill rajas/Kangra Chamba and Punjab Sikh influence; LOW (sources R4_SOUTH_ASIA-S014|R4_SOUTH_ASIA-S027).
- `R4_SOUTH_ASIA-0034` — STATE_HIMALAYAS / NEP : Gorkha/Nepal Shah kingdom and independent Himalayan peripheries; MEDIUM (sources R4_SOUTH_ASIA-S034|R4_SOUTH_ASIA-S035).
- `R4_SOUTH_ASIA-0037` — STATE_KURNOOL / KNO : Pathan Nawab of Kurnool; LOW (sources R4_SOUTH_ASIA-S005|R4_SOUTH_ASIA-S020).
- `R4_SOUTH_ASIA-0045` — STATE_PUNJAB / DUR : Durrani western Punjab military enclaves; LOW (sources R4_SOUTH_ASIA-S014|R4_SOUTH_ASIA-S043).
- `R4_SOUTH_ASIA-0047` — STATE_QUETTA / DUR : Kalat Khanate border / Durrani Pishin and Shal; UNRESOLVED (sources R4_SOUTH_ASIA-S012|R4_SOUTH_ASIA-S039).
- `R4_SOUTH_ASIA-0049` — STATE_SINDH / SIN : Kalhora Sindh under internal succession stress; UNRESOLVED (sources R4_SOUTH_ASIA-S033|R4_SOUTH_ASIA-S032).
- `R4_SOUTH_ASIA-0053` — STATE_WEST_BENGAL / BIC : West Bengal / Company Bengal diwani with foreign enclaves; HIGH (sources R4_SOUTH_ASIA-S001|R4_SOUTH_ASIA-S002|R4_SOUTH_ASIA-S006|R4_SOUTH_ASIA-S008).
- `R4_SOUTH_ASIA-0054` — STATE_WEST_BENGAL / COO : Koch/Cooch Behar kingdom; MEDIUM (sources R4_SOUTH_ASIA-S015|R4_SOUTH_ASIA-S016).
