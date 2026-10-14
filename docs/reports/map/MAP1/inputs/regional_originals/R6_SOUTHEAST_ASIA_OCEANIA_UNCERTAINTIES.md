# R6_SOUTHEAST_ASIA_OCEANIA — Incertitudes et transmission MAP-0/1

- **Date historique figée :** 1776-01-01. Recherche réalisée le 2026-10-10. Fichiers du mod non modifiés, aucune géométrie/ownership éditée et aucun push.
- **Périmètre réellement lu :** 130 couples (`State_ID`, `Owner_TAG`), 52 `State_ID`, 2 788 lignes de provinces terrestres (dont doublons techniques et province sans propriétaire). La liste de couples provient strictement du catalogue R6.
- **Couverture :** 130 / 130 (14 `CHANGE_PROPOSED`, 8 `REVIEWED_NO_CHANGE`, 108 `UNRESOLVED`). Le fichier RECOMMENDATIONS contient 130 entrées, une par couple, dont les entrées `UNRESOLVED` sont de véritables **fiches d’attente, pas des transferts proposés**.
- **Sources enregistrées :** 33 références avec documents et limitations décrites. Une référence contextuelle ne justifie pas en elle-même une province : aucune validation historique d’une attribution initiale fondée sur le seul TAG.
- **Géoréférencement :** 0 frontière provinciale vérifiée; toutes les lignes `Mapping_Status=MAPPING_REQUIRED`, `Province_ID` et `Province_IDs` vides. Les RGB de la baseline restent des identifiants techniques, jamais des noms géographiques inférés. Les RGB précis d’anomalies sont consignés ci-dessous, pas artificiellement rattachés à une correction historique.

## Résultats prioritaires (avec Change_ID et Source_ID)

| Zone | Change_ID(s) | Conclusion historique et conséquence pour le jeu | Preuve | État |
|---|---|---|---|---|
| ARAKAN / KKI | `R6_SOUTHEAST_ASIA_OCEANIA-0005` | Mrauk U est un royaume indépendant avant 1784–85; KKI/Kuki ne représente pas correctement son gouvernement littoral. R4 doit relire l’interface. | `R6_SOUTHEAST_ASIA_OCEANIA-S009|R6_SOUTHEAST_ASIA_OCEANIA-S010` | HIGH / CHANGE_PROPOSED |
| WEST_BORNEO / LAN | `R6_SOUTHEAST_ASIA_OCEANIA-0124` | Lanfang est fondé **en 1777** (après date cible); les associations minières plus anciennes ne doivent pas être baptisées Lanfang par anticipation. | `R6_SOUTHEAST_ASIA_OCEANIA-S011|R6_SOUTHEAST_ASIA_OCEANIA-S012` | HIGH / CHANGE_PROPOSED |
| NORTH_ISLAND / UNT | `R6_SOUTHEAST_ASIA_OCEANIA-0072` | La confédération **United Tribes date du 28 octobre 1835**; en 1776, les autorités sont des iwi/hapū distincts. | `R6_SOUTHEAST_ASIA_OCEANIA-S019|R6_SOUTHEAST_ASIA_OCEANIA-S017` | HIGH / CHANGE_PROPOSED |
| SOUTH_ISLAND / NTO | `R6_SOUTHEAST_ASIA_OCEANIA-0097` | Ngāti Toa gagne le sud de l’Île du Nord et le nord de l’Île du Sud dans les années 1820; Ngāi Tahu est présent dans l’Île du Sud depuis le début du XVIIIe siècle. | `R6_SOUTHEAST_ASIA_OCEANIA-S017|R6_SOUTHEAST_ASIA_OCEANIA-S018` | HIGH / CHANGE_PROPOSED |
| HAWAIIAN_ISLANDS / HAW | `R6_SOUTHEAST_ASIA_OCEANIA-0027` | Les aliʻi nui sont pluriels en 1776; unification progressive à partir de 1795, achevée en 1810. | `R6_SOUTHEAST_ASIA_OCEANIA-S021|R6_SOUTHEAST_ASIA_OCEANIA-S020` | HIGH / CHANGE_PROPOSED |
| SUNDA_ISLANDS / POR | `R6_SOUTHEAST_ASIA_OCEANIA-0102` | Timor portugais administré depuis Dili après déplacement de Lifau en 1769; alliance locale/topasses ≠ souveraineté sur toute l’île. | `R6_SOUTHEAST_ASIA_OCEANIA-S004|R6_SOUTHEAST_ASIA_OCEANIA-S005` | HIGH / CHANGE_PROPOSED |
| SUNDA_ISLANDS / DEI | `R6_SOUTHEAST_ASIA_OCEANIA-0101` | Kupang et Maubara montrent présence néerlandaise locale; alliés timorais conservent l’autonomie. | `R6_SOUTHEAST_ASIA_OCEANIA-S004|R6_SOUTHEAST_ASIA_OCEANIA-S005` | HIGH / CHANGE_PROPOSED |
| CENTRAL_JAVA / SRK | `R6_SOUTHEAST_ASIA_OCEANIA-0016` | Traité Giyanti 1755: cour Surakarta distincte de la VOC. | `R6_SOUTHEAST_ASIA_OCEANIA-S002|R6_SOUTHEAST_ASIA_OCEANIA-S001|R6_SOUTHEAST_ASIA_OCEANIA-S033` | HIGH / REVIEWED_NO_CHANGE |
| CENTRAL_JAVA / YOG | `R6_SOUTHEAST_ASIA_OCEANIA-0017` | Traité Giyanti 1755: sultanat Yogyakarta distinct de la VOC. | `R6_SOUTHEAST_ASIA_OCEANIA-S002|R6_SOUTHEAST_ASIA_OCEANIA-S001|R6_SOUTHEAST_ASIA_OCEANIA-S033` | HIGH / REVIEWED_NO_CHANGE |
| MINDANAO / MGD | `R6_SOUTHEAST_ASIA_OCEANIA-0045` | Sultanat de Maguindanao non soumis automatiquement à Espagne; RGB en conflit MGD/MND. | `R6_SOUTHEAST_ASIA_OCEANIA-S013` | MEDIUM / REVIEWED_NO_CHANGE |
| TASMANIA / WTI | `R6_SOUTHEAST_ASIA_OCEANIA-0104` | Les Palawa de Tasmanie ne sont pas les Anangu continentaux, et aucun contrôle colonial européen en 1776. | `R6_SOUTHEAST_ASIA_OCEANIA-S014|R6_SOUTHEAST_ASIA_OCEANIA-S015` | HIGH / CHANGE_PROPOSED |
| WESTERN_NEW_GUINEA / TID | `R6_SOUTHEAST_ASIA_OCEANIA-0122` | Les réseaux tributaires de Tidore restent distincts du contrôle néerlandais; établissement hollandais seulement en 1828. | `R6_SOUTHEAST_ASIA_OCEANIA-S022|R6_SOUTHEAST_ASIA_OCEANIA-S001` | MEDIUM / CHANGE_PROPOSED |
| BANGKOK / SIA | `R6_SOUTHEAST_ASIA_OCEANIA-0006` | Taksin gouverne à **Thonburi** en 1776; Bangkok/Rattanakosin est capitale à partir de 1782. | `R6_SOUTHEAST_ASIA_OCEANIA-S007|R6_SOUTHEAST_ASIA_OCEANIA-S030` | HIGH / REVIEWED_NO_CHANGE |
| LAOS / SIA | `R6_SOUTHEAST_ASIA_OCEANIA-0034` | La conquête siamoise de Vientiane est de 1778–79; ne pas anticiper sa suzeraineté sur 1776. | `R6_SOUTHEAST_ASIA_OCEANIA-S006|R6_SOUTHEAST_ASIA_OCEANIA-S007` | MEDIUM / CHANGE_PROPOSED |

## Dossiers critiques non résolus

### 1. Interface Vietnam–Siam–Cambodge et chronologie 1776

- **Vietnam central :** les rapports Trịnh–Nguyễn–Tây Sơn changent rapidement entre 1774 et 1778. Les `STATE_ANNAM`, `STATE_TONKIN` et `STATE_MEKONG` ne peuvent être traités comme une administration continue « Đại Nam ». `S026` situe des offensives Tây Sơn pendant 1775–77; `S027` situe la proclamation royale en **mars 1776**, donc après la date du mod. Aucun contour par RGB n’est validé.
- **CONTRADICTION documentaire explicite (non résolue) :** Robert Y. Eng (2020, `S011`, section *Hà Tiên*) écrit que l’élimination de la maison Nguyễn de Quảng Nam date de **1776**, tandis que Lê Đình Phụng (2012, `S026`) décrit des événements militaires en **1777**. Les campagnes, retraits et décès ne doivent pas être amalgamés en une date unique. Consulter annales Nguyễn/Trịnh contemporaines et chronologies des offensives Gia Định, puis statuer par localisation. Cet écart reste dans `Unresolved_Uncertainty` de `STATE_MEKONG / DAI`.
- **Hà Tiên :** `S011` rapporte la prise par Taksin en 1771 et son retrait en 1773; Mạc Thiên Tứ se replie à Cần Thơ. Les récits opposent statut de commandant cambodgien et chef de communauté chinoise (Sakurai/Kitagawa, cités par Eng). Chercher une polité portuaire attestée en 1776 **sans inventorier un TAG nouveau non existant**. En cas d’absence d’`Owner_TAG+State_ID` pertinent, signaler aux décideurs centraux, pas imputer arbitrairement à CAM, SIA ou DAI.
- **Cambodge :** Khin Sok, *Le Cambodge entre le Siam et le Viêtnam* (1991), chap. II « 1775–1794 » (`S008`) est identifié bibliographiquement mais son texte n’a pas été consulté. La frontière Cambodge–Siam et le contrôle des hautes terres KLO demeurent `UNRESOLVED`.
- **Lao :** la distinction Luang Prabang/Vientiane/Champasak/Siam doit précéder la campagne siamoise 1778–79 (`S006`). Les muang tributaires ne forment pas forcément des provinces directement administrées.

### 2. VOC, sultanats et compagnies (DEI/INDOP)

- La VOC gouverne de vrais centres tels Batavia et dispose de forts, ports et juridictions (`S001`, plan urbain **1770** `S003`), mais son réseau de traités, monopoles et interventions ne donne pas une administration uniforme de **Java, Sulawesi, Bornéo, Sumatra, Moluques ou Timor**. `DEI` ne doit pas être étendu automatiquement à l’intérieur. Les états `WEST_JAVA`, `CENTRAL_JAVA`, `EAST_JAVA`, `CELEBES`, `MOLUCCAS`, `SUNDA_ISLANDS` sont des priorités de superposition cartographique.
- **Java :** traité de Giyanti (13 février 1755), cours Surakarta et Yogyakarta distinctes (`S033`); vérifier aussi Mangkunegaran dès 1757. Les sources décrivent des domaines historiques très intriqués et non des frontières modernes constantes. Le plan de Batavia p.208 ne cartographie pas Java entière.
- **Timor :** Farram (`S004`, *Journal of Southeast Asian Studies* 50(2), pp.263–287) démontre des alliances et des principautés autonomes malgré les forts; un fort VOC à Maubara ne signifie pas une province néerlandaise uniforme. Tavares (`S005`) date le transfert de la capitale portugaise Lifau→Dili de 1769. Il faut localiser Kupang, Maubara, Dili, Lifau et les places topasses.
- **Bornéo occidental :** Eng (`S011`) date Heshun/Monterado en **1776 sans le mois** et Lanfang/Mandor en **1777**. L’exécution du mod au 1776-01-01 exige une source infra-annuelle avant même d’attribuer Heshun. `LAN` n’est pas fondé, mais ses **trois provinces** ne sont pas automatiquement distribuables à `PON`, `SMB` ou `INDOP`. Les sultanats contrôlent souvent **personnes et recettes**, non des polygones cadastraux (`S011`).
- **Sumatra :** l’EIC possède **Fort Marlborough à Bengkulu** (construit 1714–19, `S025`), et non la souveraineté sur toute Sumatra méridionale. L’archive BL IOR/G/35/18 (`S029`) commence en **1778** : ne pas la présenter comme preuve contemporaine directe de 1776.
- **Moluques/Papouasie :** Fidélité tributaires de Tidore ≠ juridiction néerlandaise directe sur l’intérieur occidental de Nouvelle-Guinée; l’établissement colonial néerlandais est bien postérieur (`S022`, 1828).

### 3. Monde philippin et contrôles techniques

- Rafael (`S013`, Oxford Research Encyclopedia, PDF **pp.2–5**) distingue l’administration espagnole des basses terres du contrôle inachevé des hauteurs et de Mindanao/Sulu, et documente les sultanats Maguindanao/Sulu au XVIIIe siècle. `PHI` ne doit pas faire disparaître les datus, ni `SUL` devenir une maîtrise directe de tout le nord Bornéo. Les étendues `LUZON`, `VISAYAS`, `MINDANAO`, `NORTH_BORNEO` sont `MAPPING_REQUIRED`.
- `STATE_MINDANAO` : x62D16D, xAA1CA3 et x585200 écrits deux fois MND (`MAP0-0034/35/36`), et xE90347 en conflit MND|MGD (`MAP0-0037`). Les problèmes sont dupliqués dans le candidat **non fusionné** `MAP0-0128/29/30/31`. Ne pas déduire une propriété historique d’une erreur de syntaxe. Pas d’arbitrage MND versus MGD avant localisation.
- `STATE_PEGU` : un RGB est donné BIC et un DENNOR. Une preuve d’implantation, date, garnison, recette et juridiction manque pour chaque puissance. Les deux fiches restent `UNRESOLVED`; collaboration R4.

### 4. Australie, Aotearoa et Pacifique

- `S014` (Horton/AIATSIS, carte **1996**) précise explicitement que les territoires de nations et langues ne sont **pas des frontières exactes ni fixes**, et que certaines localisations sont discutées. Des subdivisions historiques de 1776 ne peuvent être fabriquées au seul vu de cette carte. Le contrôle autochtone local n’implique pas un État national unifié par TAG.
- `S015` (journal Cook **1770-08-22**, revendication orientale) et `S016` (**1788-01-26**, Première flotte) doivent être séparés : en 1776 la Couronne britannique n’a pas d’administration coloniale effective à Sydney, Queensland, Tasmanie, etc. **Aucun remplissage européen des intérieurs**. La relation WTI/Anangu–Tasmanie doit être révisée au profit des sociétés palawa attestées, mais les 21 RGB ne sont pas attribués à des nations déterminées.
- `S017/S018/S019`: Ngāti Toa vers Cook Strait/South Island après **1820**, Ngāi Tahu en Île du Sud dès le XVIIIe, confédération United Tribes créée **1835**; trois anachronismes distincts à ne pas confondre.
- `S020/S021`: Hawaiʻi en 1776 demeure partagé entre aliʻi nui; les conquêtes de 1795 et soumission de Kauaʻi en 1810 sont **postérieures**. Trois RGB HAW ne permettent pas d’inventer trois frontières exactes.
- **Fiji, Tonga, Tahiti, Vanuatu, Nauru, Salomon, Bougainville, Kanak et Micronésie** : les cadres souverains autochtones nécessitent enquêtes insulaires et consultations ethnographiques locales. Les sources `S023/S024` ne prouvent pas des frontières pour 1776. `FJI` et `TNG` peuvent demeurer provisoirement comme représentations décentralisées, sans monarchie paninsulaire moderne.

### 5. Anomalies MAP0 non historiques

| Issue_ID main | Issue_ID candidat | State_ID / RGB | Nature | Traitement |
|---|---|---|---|---|
| MAP0-0034, 0035, 0036 | MAP0-0128, 0129, 0130 | MINDANAO: x62D16D, xAA1CA3, x585200 | MND répété | Déduplication technique hors recherche, sans validation historique |
| MAP0-0037 | MAP0-0131 | MINDANAO: xE90347 | MND et MGD écrits | Revue source du mod, aucune attribution décidée |
| MAP0-0050, 0051 | MAP0-0144, 0145 | TAHITI: xF1DBF3, x998293 | PLY répété | Technique, à dédupliquer indépendamment du diagnostic politique |
| MAP0-0073 | MAP0-0168 | ANNAM: capitale DGR non possédée | Définition capitale | Pas de conclusion géographique ni attribution DGR |
| MAP0-0089 | MAP0-0186 | WEST_MICRONESIA: **xEF50C0** | Province terrestre sans propriétaire écrit | **Ne pas attribuer automatiquement** à MCR ni PHI; recherche de l’île indispensable |

**Important :** les ID 0128–0186 indiqués correspondent au candidat collaborateur, pas à `main`. Le registre initial reste strictement celui de `main` et les anciennes appartenances R5 pour Indochine/R8 pour Hawaii sont des **erreurs de classement de recherche**, non des preuves de souveraineté.

### 6. Interfaces et transmission

- **R4_SOUTH_ASIA** : Arakan (royaume Mrauk U indépendant en 1776), Pegu, Mandalay, Tenasserim, Kachin, Shan States. Propriétaire de recherche **R6 uniquement**; R4 relit les interfaces montagnardes et côtières. Les Change_ID sont dans `RECOMMENDATIONS.csv` et marqués `COORDINATION_REQUIRED`.
- **R5_EAST_ASIA** : Tonkin (Trịnh et territoires Tai/SCT, frontière nord), interfaces laotiennes et vietnamiennes. Propriétaire **R6 uniquement**, même en présence d’une ancienne région source R5. Aucune recommandation R5 dupliquée.
- **VEN/GEN** : aucun couple R6 ne porte ces TAGs. Leur protection population/bâtiments reste en vigueur à l’échelle globale, sans transfert dans ce travail.
- **OUTSIDE_BASELINE** : aucune province ni TAG externe n’a été inventé. Des entités locales absentes (régimes de Hà Tiên, Heshun, nombreuses polities autochtones) sont à soumettre à la synthèse centrale si nécessaire à la représentation; elles ne deviennent pas de nouveaux couples de couverture ni une annexion à une autre mission.

### 7. Procédure de clôture restante pour l’équipe centrale

1. Préparer une superposition **province RGB↔toponyme↔carte datée** pour chaque ligne `MAPPING_REQUIRED` (commencer par Maubara/Kupang/Dili, Mandor/Monterado, Ha Tien, Chiang Mai, Batavia/Fort Rotterdam, xEF50C0). Ne jamais reprendre un RGB sans superposition vérifiable.
2. Obtenir des preuves administratives précises : traités, annuaires de garnison, impôts, registres VOC/EIC, chroniques locales, cartes d’époque contextualisées. Les 108 lignes `UNRESOLVED` ne sont pas « implicitement correctes ».
3. Traiter les 14 `CHANGE_PROPOSED` comme **propositions historiques** et non comme autorisation de changement. Lorsque A provinces existantes échoue réellement, étudier B State Regions, C Geometry uniquement si preuves d’insuffisance.
4. Réaliser revue R4/R5, puis arbitrer contradictions. Aucun transfert de population/bâtiment/capitale ni intervention sur la branche du collaborateur n’est autorisé par ces documents.

## Inventaire des 52 États — statut par couple

Codes : `C`=CHANGE_PROPOSED; `N`=REVIEWED_NO_CHANGE; `U`=UNRESOLVED. Les codes sont des **statuts de recherche**, pas une confirmation de contrôle territorial.

| State_ID | TAGs actuels et statut | Fiches / Change_IDs |
|---|---|---|
| STATE_ACEH | ACE=U · INDOP=U · SAK=U | `0001`, `0002`, `0003` |
| STATE_ANNAM | DAI=C | `0004` |
| STATE_ARAKAN | KKI=C | `0005` |
| STATE_BANGKOK | SIA=N | `0006` |
| STATE_BOUGAINVILLE | HLA=U | `0007` |
| STATE_CAMBODIA | CAM=U · KLO=U · SIA=U | `0008`, `0009`, `0010` |
| STATE_CELEBES | BTN=U · DEI=U · SLW=U · TID=U | `0011`, `0012`, `0013`, `0014` |
| STATE_CENTRAL_JAVA | DEI=U · SRK=N · YOG=N | `0015`, `0016`, `0017` |
| STATE_CHIANG_MAI | CMI=U | `0018` |
| STATE_EASTERN_NEW_GUINEA | PPU=U | `0019` |
| STATE_EAST_BORNEO | BLG=U · BNJ=U · INDOP=U · KTI=U | `0020`, `0021`, `0022`, `0023` |
| STATE_EAST_JAVA | DEI=U | `0024` |
| STATE_EAST_MICRONESIA | MCR=U | `0025` |
| STATE_FIJI | FJI=N | `0026` |
| STATE_HAWAIIAN_ISLANDS | HAW=C | `0027` |
| STATE_KACHIN | BUR=U | `0028` |
| STATE_KANAK | KNK=U | `0029` |
| STATE_LAOS | CHP=U · DAI=U · LUA=U · SCT=U · SIA=C | `0030`, `0031`, `0032`, `0033`, `0034` |
| STATE_LUZON | PHI=U · SUL=U | `0035`, `0036` |
| STATE_MALAYA | JOH=U · PRK=U · SEL=U · SIA=U | `0037`, `0038`, `0039`, `0040` |
| STATE_MANDALAY | BUR=U · KKI=U | `0041`, `0042` |
| STATE_MEKONG | DAI=C · DGR=U | `0043`, `0044` |
| STATE_MINDANAO | MGD=N · MND=U · PHI=U · SUL=U | `0045`, `0046`, `0047`, `0048` |
| STATE_MOLUCCAS | DEI=U · TID=N | `0049`, `0050` |
| STATE_NAKHON_RATCHASIMA | SIA=U | `0051` |
| STATE_NAURU | NRU=U | `0052` |
| STATE_NEW_SOUTH_WALES | KLN=U · KNC=U · KRI=U · PAA=U · WDJ=U · YUR=U | `0053`, `0054`, `0055`, `0056`, `0057`, `0058` |
| STATE_NORTHERN_TERRITORY | ARH=U · ARR=U · GRW=U · KNC=U · LRR=U · NYP=U · WRR=U · WTI=U · YGU=U | `0059`, `0060`, `0061`, `0062`, `0063`, `0064`, `0065`, `0066`, `0067` |
| STATE_NORTH_BORNEO | BLG=U · BRU=U · SUL=U | `0068`, `0069`, `0070` |
| STATE_NORTH_ISLAND | NTO=U · UNT=C | `0071`, `0072` |
| STATE_NORTH_SUMATRA | INDOP=U · JMB=U · SAK=U | `0073`, `0074`, `0075` |
| STATE_PEGU | BIC=U · BUR=U · DENNOR=U | `0076`, `0077`, `0078` |
| STATE_QUEENSLAND | ARR=U · GRW=U · KNC=U · MRA=U · PAA=U · PMA=U · WDJ=U · WKB=U | `0079`, `0080`, `0081`, `0082`, `0083`, `0084`, `0085`, `0086` |
| STATE_SHAN_STATES | BUR=U · SHS=U | `0087`, `0088` |
| STATE_SOLOMON_ISLANDS | BLA=U | `0089` |
| STATE_SOUTH_AUSTRALIA | KAU=U · KLN=U · KNC=U · MRN=U · PAA=U · WTI=U · YUR=U | `0090`, `0091`, `0092`, `0093`, `0094`, `0095`, `0096` |
| STATE_SOUTH_ISLAND | NTO=C · NTU=U | `0097`, `0098` |
| STATE_SOUTH_SUMATRA | INDOP=C | `0099` |
| STATE_SUNDA_ISLANDS | BAL=U · DEI=C · POR=C | `0100`, `0101`, `0102` |
| STATE_TAHITI | PLY=U | `0103` |
| STATE_TASMANIA | WTI=C | `0104` |
| STATE_TENASSERIM | BUR=U · SIA=U | `0105`, `0106` |
| STATE_TONGA | TNG=N | `0107` |
| STATE_TONKIN | DAI=C · SCT=U | `0108`, `0109` |
| STATE_VANUATU | VNT=U | `0110` |
| STATE_VICTORIA | KLN=U · KRI=U | `0111`, `0112` |
| STATE_VISAYAS | PHI=U | `0113` |
| STATE_WESTERN_AUSTRALIA | KTU=U · KYN=U · MRN=U · NNG=U · NYP=U · WRR=U · WTI=U | `0114`, `0115`, `0116`, `0117`, `0118`, `0119`, `0120` |
| STATE_WESTERN_NEW_GUINEA | PPU=U · TID=C | `0121`, `0122` |
| STATE_WEST_BORNEO | INDOP=U · LAN=C · PON=N · SMB=U · STG=U | `0123`, `0124`, `0125`, `0126`, `0127` |
| STATE_WEST_JAVA | DEI=U | `0128` |
| STATE_WEST_MICRONESIA | MCR=U · PHI=U | `0129`, `0130` |
