# MAP-0 — Neuf missions indépendantes prêtes à transmettre

Aucune mission n’a été lancée. Chaque bloc est autonome et doit être envoyé avec les quatre fichiers de référence cités. Les listes sont calculées depuis l’inventaire actuel, non depuis des frontières historiques supposées.


## R1_WESTERN_EUROPE

```text
Mission autonome : R1_WESTERN_EUROPE — Europe occidentale

Tu es responsable de la recherche territoriale au 1er janvier 1776 (1776-01-01) pour le mod Victoria 3 « 1776 Age of Revolutions ». Tu recherches, tu ne modifies ni fichiers historiques ni carte, et tu ne pousses aucun changement. Les valeurs initiales du mod et les noms de TAGs ne sont pas des conclusions historiques.

PIÈCES À RECEVOIR : MAP_1776_BASELINE.csv, MAP_1776_9_REGIONS.csv, MAP_1776_RESEARCH_SCHEMA.md, MAP_1776_KNOWN_ISSUES.csv. Utilise uniquement les lignes Region_ID=R1_WESTERN_EUROPE comme périmètre principal. Les IDs RGB sont ceux du bitmap du jeu, pas des numéros arbitraires. Les lignes d’un même State_ID avec plusieurs Owner_TAG restent distinctes.

PÉRIMÈTRE : Îles Britanniques et Irlande, France, Pays-Bas historiques, péninsule Ibérique, Italie et îles attribuées dans le périmètre ci-dessous; aucune colonie extra-européenne par sa seule métropole.
L’inventaire comprend 82 couples pays/État et 73 State_IDs distincts. TAGs existants à auditer dans ce seul périmètre : AUS, BEO, FRA, GBR, GEN, GR3, IREK, LUC, LUX, MLT, MOD, NET, PAP, PAR, POR, SAR, SIC, SPA, TUS, VEN.
Interlocuteurs secondaires prévus : R2_NORTHERN_CENTRAL_EASTERN_EUROPE. Une métropole qui possède ailleurs ne t’attribue pas ces territoires. Les mers et lacs sont une référence technique, pas des territoires politiques à attribuer à un pays.

PROBLÈMES DÉJÀ OBSERVÉS : Luxembourg/Wallonie xD001A0 : identifier souveraineté et administration au 1er janvier; ne pas assimiler une province du jeu à un duché sans mapping. Lombardie : x867A90 est doublonnée AUS/VEN dans le candidat non intégré, x9AC196 y change de propriétaire. Auditer Venise et Gênes, leurs enclaves, les possessions et dépendances italiennes; préserver leurs historiques particuliers.
Références du registre à lire : MAP0-0148 | MAP0-0178 | MAP0-0185 | MAP0-0194 | MAP0-0207 | MAP0-0208
Un conflit de syntaxe ou de fichier n’est pas une preuve historique. Le candidat georg3mx n’est pas fusionné dans main; la baseline représente main actuel.

FORMES DE SOUVERAINETÉ ET DIFFICULTÉS : Unions dynastiques, principautés, enclaves, juridictions et possessions discontinues. Distinguer souveraineté du souverain, administration provinciale et occupation. Cartes composites des Pays-Bas et frontières italiennes peuvent amalgamer plusieurs dates.
PRIORITÉS : Priorité : Luxembourg/Wallonie, Lombardie, frontière alpine avec R2, enclaves italiennes et autorités locales. Les retouches fiscales, industrielles et militaires existantes ne constituent pas une preuve territoriale.

Pour chaque territoire, distinguer administration directe, occupation militaire peu administrée, dépendance/vassalité, protectorat/tribut/influence, compagnie à autorité territoriale, autonomie/souveraineté autochtone, revendication seule, contrôle disputé ou fluctuant, et zone sans frontière précise défendable. Examiner présence administrative, fiscalité, juridiction, garnisons, fortifications, implantations permanentes, traités et structures politiques locales. Un comptoir n’équivaut pas à souveraineté sur toute une State Region. Dater séparément les changements survenus après le 1er janvier, même dans l’année 1776.

SOURCES : atlas historiques argumentés, travaux universitaires spécialisés, traités/documents administratifs contemporains, cartes d’époque avec date et biais, travaux sur les souverainetés locales et autochtones. Pour chaque correction importante, cite au moins une preuve précise. Fournis auteur, titre, date, URL ou référence bibliographique, pages/cartes pertinentes; une URL seule ou une carte moderne non justifiée ne suffit pas. Signale les contradictions et compare la nature des preuves; ne tranche pas silencieusement.

LIVRABLES : R1_WESTERN_EUROPE_RECOMMENDATIONS.csv conforme à toutes les colonnes et valeurs contrôlées du schéma joint; R1_WESTERN_EUROPE_SOURCES.csv; R1_WESTERN_EUROPE_UNCERTAINTIES.md; R1_WESTERN_EUROPE_COVERAGE.csv avec une ligne pour chaque couple listé, y compris REVIEWED_NO_CHANGE. Cartes annotées facultatives mais utiles. Chaque changement doit distinguer conclusion historique, correspondance géographique proposée, approximation de gameplay et incertitude non résolue.

Si tu ne peux pas faire correspondre une frontière aux provinces du jeu, laisse Province_ID/Province_IDs vides, utilise Mapping_Status=MAPPING_REQUIRED et décris précisément la zone (toponymes, coordonnées, limites, carte/page). N’invente aucun ID ni nouveau TAG. Préfère A_EXISTING_PROVINCES, puis B_STATE_REGIONS; ne demande C_GEOMETRY qu’avec preuve que les provinces existantes sont insuffisantes. Indique Requires_New_Tag et Requires_State_Split sans créer l’entité.

INCERTITUDES ET TRANSMISSION : attribue Change_ID stable, Source_IDs vérifiables et Confidence justifiée. Toute contradiction reste UNRESOLVED; renseigne Cross_Region_Conflict et Secondary_Region_ID, décris les sources opposées et transmets à la synthèse centrale. L’interlocuteur secondaire relit l’interface mais ne duplique pas ta recommandation. Une nouvelle zone extérieure au périmètre est signalée OUTSIDE_BASELINE pour attribution centrale, pas annexée à ta mission. VEN et GEN sont recherchés normalement mais leurs historiques particuliers de population/bâtiments sont protégés. Ne redistribue pas ces données. Aucun résultat n’est automatiquement intégré.

LISTE EXHAUSTIVE DES ÉTATS ET PROPRIÉTAIRES ACTUELS À AUDITER :
STATE_ABRUZZO : SIC
STATE_ALENTEJO : POR
STATE_ALSACE_LORRAINE : FRA
STATE_APULIA : SIC
STATE_AQUITAINE : FRA
STATE_ARAGON : SPA
STATE_ASTURIAS : SPA
STATE_AUVERGNE_LIMOUSIN : FRA
STATE_AZORES : POR
STATE_BALEARIC_ISLANDS : GBR | SPA
STATE_BASQUE_COUNTRY : SPA
STATE_BEIRA : POR
STATE_BRITTANY : FRA
STATE_BURGUNDY : FRA
STATE_CALABRIA : SIC
STATE_CAMPANIA : SIC
STATE_CATALONIA : SPA
STATE_CHAMPAGNE : FRA
STATE_CONNAUGHT : IREK
STATE_CORSICA : FRA
STATE_EAST_ANGLIA : GBR
STATE_EMILIA : LUC | MOD | PAR
STATE_ENTRE_DOURO_E_MINHO : POR
STATE_ESTREMADURA : POR
STATE_EXTREMADURA : SPA
STATE_FLANDERS : BEO
STATE_FRANCHE_COMTE : FRA
STATE_FRENCH_LOW_COUNTRIES : FRA
STATE_FRIESLAND : NET
STATE_GALICIA : SPA
STATE_GELRE : BEO | NET
STATE_GUYENNE : FRA
STATE_HIGHLANDS : GBR
STATE_HOLLAND : NET
STATE_HOME_COUNTIES : GBR
STATE_ILE_DE_FRANCE : FRA
STATE_LANCASHIRE : GBR
STATE_LANGUEDOC : FRA
STATE_LAZIO : PAP
STATE_LEINSTER : IREK
STATE_LEON : SPA
STATE_LOMBARDY : AUS | VEN
STATE_LORRAINE : FRA
STATE_LOWER_ANDALUSIA : SPA
STATE_LOWLANDS : GBR
STATE_MAINE_ANJOU : FRA
STATE_MALTA : MLT
STATE_MIDLANDS : GBR
STATE_MUNSTER : IREK
STATE_MURCIA : SPA
STATE_NEW_CASTILE : SPA
STATE_NORMANDY : FRA
STATE_OLD_CASTILE : SPA
STATE_ORLEANS : FRA
STATE_PICARDY : FRA
STATE_PIEDMONT : GEN | SAR
STATE_POITOU : FRA
STATE_PROVENCE : FRA | SAR
STATE_RHONE : FRA
STATE_ROMAGNA : PAP
STATE_SARDINIA : SAR
STATE_SAVOY : SAR
STATE_SICILY : GR3
STATE_TUSCANY : TUS
STATE_ULSTER : IREK
STATE_UMBRIA : PAP
STATE_UPPER_ANDALUSIA : GBR | SPA
STATE_VALENCIA : SPA
STATE_VENETIA : VEN
STATE_WALES : GBR
STATE_WALLONIA : BEO | LUX
STATE_WEST_COUNTRY : GBR
STATE_YORKSHIRE : GBR
```


## R2_NORTHERN_CENTRAL_EASTERN_EUROPE

```text
Mission autonome : R2_NORTHERN_CENTRAL_EASTERN_EUROPE — Europe septentrionale, centrale et orientale

Tu es responsable de la recherche territoriale au 1er janvier 1776 (1776-01-01) pour le mod Victoria 3 « 1776 Age of Revolutions ». Tu recherches, tu ne modifies ni fichiers historiques ni carte, et tu ne pousses aucun changement. Les valeurs initiales du mod et les noms de TAGs ne sont pas des conclusions historiques.

PIÈCES À RECEVOIR : MAP_1776_BASELINE.csv, MAP_1776_9_REGIONS.csv, MAP_1776_RESEARCH_SCHEMA.md, MAP_1776_KNOWN_ISSUES.csv. Utilise uniquement les lignes Region_ID=R2_NORTHERN_CENTRAL_EASTERN_EUROPE comme périmètre principal. Les IDs RGB sont ceux du bitmap du jeu, pas des numéros arbitraires. Les lignes d’un même State_ID avec plusieurs Owner_TAG restent distinctes.

PÉRIMÈTRE : Scandinavie et Islande, territoires germaniques et suisses, Europe centrale/orientale, Balkans et Russie européenne; exclure les territoires extra-européens de ces souverains.
L’inventaire comprend 164 couples pays/État et 136 State_IDs distincts. TAGs existants à auditer dans ce seul périmètre : ANH, AUS, BAD, BAV, BRA, BRE, COB, CRI, DENNOR, FRM, GAL, HAM, HAN, HEK, HES, HOH, HOL, HUN, KZH, LIP, LUB, MEC, MEI, MOL, MON, MST, NAS, OLD, PLC, PRU, RUS, SAX, SCH, SCM, SCW, SWE, SWI, TRS, TUR, UBD, VEN, WAL, WEI, WLD, WUR.
Interlocuteurs secondaires prévus : R1_WESTERN_EUROPE, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA, R5_EAST_ASIA. Une métropole qui possède ailleurs ne t’attribue pas ces territoires. Les mers et lacs sont une référence technique, pas des territoires politiques à attribuer à un pays.

PROBLÈMES DÉJÀ OBSERVÉS : Travaux déjà intégrés : Dobroudja, Suisse orientale, Bessarabie, Istrie et Tyrol du Sud. Le nouveau candidat contient des commandes Git parasites en Bessarabie; elles ne sont pas des données historiques. Hautes/Basses Silésies : plusieurs provinces sont attribuées dans le mauvais State_ID et certains propriétaires se superposent; examiner le registre des anomalies.
Références du registre à lire : MAP0-0054 | MAP0-0055 | MAP0-0056 | MAP0-0057 | MAP0-0058 | MAP0-0059 | MAP0-0060 | MAP0-0078 | MAP0-0083 | MAP0-0090 | MAP0-0091 | MAP0-0092 | MAP0-0093 | MAP0-0094 | MAP0-0149 | MAP0-0150 | MAP0-0151 | MAP0-0152 | MAP0-0153 | MAP0-0154 | MAP0-0155 | MAP0-0173 | MAP0-0179 | MAP0-0187 | MAP0-0188 | MAP0-0189 | MAP0-0190 | MAP0-0193 | MAP0-0204
Un conflit de syntaxe ou de fichier n’est pas une preuve historique. Le candidat georg3mx n’est pas fusionné dans main; la baseline représente main actuel.

FORMES DE SOUVERAINETÉ ET DIFFICULTÉS : Saint-Empire et juridictions imbriquées, unions personnelles, couronnes et sujets habsbourgeois, autonomie provinciale ottomane, rapports russes avec Crimée et Pologne-Lituanie. Ne pas projeter les réorganisations napoléoniennes ou les frontières de 1836.
PRIORITÉS : Priorité : Silésie, subdivisions impériales et enclaves, Istrie/Tyrol, Bessarabie/Dobroudja, Europe ottomane. Coordonne le Caucase et les marches des steppes avec R3, la limite de mission de Sibérie avec R5.

Pour chaque territoire, distinguer administration directe, occupation militaire peu administrée, dépendance/vassalité, protectorat/tribut/influence, compagnie à autorité territoriale, autonomie/souveraineté autochtone, revendication seule, contrôle disputé ou fluctuant, et zone sans frontière précise défendable. Examiner présence administrative, fiscalité, juridiction, garnisons, fortifications, implantations permanentes, traités et structures politiques locales. Un comptoir n’équivaut pas à souveraineté sur toute une State Region. Dater séparément les changements survenus après le 1er janvier, même dans l’année 1776.

SOURCES : atlas historiques argumentés, travaux universitaires spécialisés, traités/documents administratifs contemporains, cartes d’époque avec date et biais, travaux sur les souverainetés locales et autochtones. Pour chaque correction importante, cite au moins une preuve précise. Fournis auteur, titre, date, URL ou référence bibliographique, pages/cartes pertinentes; une URL seule ou une carte moderne non justifiée ne suffit pas. Signale les contradictions et compare la nature des preuves; ne tranche pas silencieusement.

LIVRABLES : R2_NORTHERN_CENTRAL_EASTERN_EUROPE_RECOMMENDATIONS.csv conforme à toutes les colonnes et valeurs contrôlées du schéma joint; R2_NORTHERN_CENTRAL_EASTERN_EUROPE_SOURCES.csv; R2_NORTHERN_CENTRAL_EASTERN_EUROPE_UNCERTAINTIES.md; R2_NORTHERN_CENTRAL_EASTERN_EUROPE_COVERAGE.csv avec une ligne pour chaque couple listé, y compris REVIEWED_NO_CHANGE. Cartes annotées facultatives mais utiles. Chaque changement doit distinguer conclusion historique, correspondance géographique proposée, approximation de gameplay et incertitude non résolue.

Si tu ne peux pas faire correspondre une frontière aux provinces du jeu, laisse Province_ID/Province_IDs vides, utilise Mapping_Status=MAPPING_REQUIRED et décris précisément la zone (toponymes, coordonnées, limites, carte/page). N’invente aucun ID ni nouveau TAG. Préfère A_EXISTING_PROVINCES, puis B_STATE_REGIONS; ne demande C_GEOMETRY qu’avec preuve que les provinces existantes sont insuffisantes. Indique Requires_New_Tag et Requires_State_Split sans créer l’entité.

INCERTITUDES ET TRANSMISSION : attribue Change_ID stable, Source_IDs vérifiables et Confidence justifiée. Toute contradiction reste UNRESOLVED; renseigne Cross_Region_Conflict et Secondary_Region_ID, décris les sources opposées et transmets à la synthèse centrale. L’interlocuteur secondaire relit l’interface mais ne duplique pas ta recommandation. Une nouvelle zone extérieure au périmètre est signalée OUTSIDE_BASELINE pour attribution centrale, pas annexée à ta mission. VEN et GEN sont recherchés normalement mais leurs historiques particuliers de population/bâtiments sont protégés. Ne redistribue pas ces données. Aucun résultat n’est automatiquement intégré.

LISTE EXHAUSTIVE DES ÉTATS ET PROPRIÉTAIRES ACTUELS À AUDITER :
STATE_ALAND : SWE
STATE_ALBANIA : TUR
STATE_ANHALT : ANH | PRU
STATE_ARKHANGELSK : RUS
STATE_ASTRAKHAN : RUS
STATE_ATTICA : TUR
STATE_AUSTRIA : AUS
STATE_BADEN : BAD
STATE_BANAT : HUN
STATE_BAVARIA : BAV
STATE_BEKES : HUN
STATE_BESSARABIA : MOL
STATE_BOHEMIA : AUS
STATE_BOSNIA : TUR
STATE_BRANDENBURG : PRU
STATE_BREST : PLC
STATE_BRUNSWICK : BRA | HAN | PRU
STATE_BUKOVINA : AUS
STATE_BULGARIA : TUR
STATE_CENTRAL_HUNGARY : HUN
STATE_CHERNIHIV : RUS
STATE_CHERSON : CRI
STATE_CHUVASHIA : RUS
STATE_COURLAND : PLC
STATE_CRETE : TUR
STATE_CRIMEA : CRI
STATE_CROATIA : AUS
STATE_DALMATIA : VEN
STATE_DELVIDEK : HUN
STATE_DOBRUDJA : TUR
STATE_EASTERN_NORWAY : DENNOR
STATE_EASTERN_SERBIA : TUR
STATE_EASTERN_THRACE : TUR
STATE_EAST_AEGEAN_ISLANDS : TUR
STATE_EAST_GALICIA : GAL
STATE_EAST_KARELIA : RUS
STATE_EAST_PRUSSIA : PRU
STATE_EAST_SWITZERLAND : SWI
STATE_ELBE : BRE | HAM | HAN
STATE_FRANCONIA : BAV
STATE_GALICH : RUS
STATE_GOTALAND : SWE
STATE_GOTLAND : SWE
STATE_GREATER_POLAND : PLC
STATE_HANNOVER : HAN | OLD
STATE_HESSE : FRM | HEK | HES | NAS | WLD
STATE_ICELAND : DENNOR
STATE_INGRIA : RUS
STATE_IONIAN_ISLANDS : VEN
STATE_ISTRIA : AUS | VEN
STATE_JUTLAND : DENNOR
STATE_KALMYKIA : RUS
STATE_KAUNAS : PLC
STATE_KAZAN : RUS
STATE_KHARKOV : RUS
STATE_KIEV : PLC
STATE_KOLA : RUS
STATE_KOSOVO : TUR
STATE_KUOPIO : SWE
STATE_KURSK : RUS
STATE_LESSER_POLAND : PLC
STATE_LOWER_SILESIA : PRU
STATE_MACEDONIA : TUR
STATE_MAZOVIA : PLC
STATE_MECKLENBURG : MEC | MST
STATE_MINSK : PLC
STATE_MOGILEV : RUS
STATE_MOLDAVIA : MOL
STATE_MONTENEGRO : MON | TUR | VEN
STATE_MORAVIA : AUS
STATE_MOSCOW : RUS
STATE_NENETSIA : RUS
STATE_NIZHNY_NOVGOROD : RUS
STATE_NORRLAND : SWE
STATE_NORTHERN_NORWAY : DENNOR
STATE_NORTHERN_THRACE : TUR
STATE_NORTHERN_TRANSYLVANIA : TRS
STATE_NORTH_RHINE : PRU
STATE_NOVGOROD : RUS
STATE_ORYOL : RUS
STATE_OSTROBOTHNIA : SWE
STATE_OULU : SWE
STATE_PELOPONNESE : TUR
STATE_PERM : RUS
STATE_POMERANIA : PRU
STATE_POSEN : PLC
STATE_PSKOV : RUS
STATE_RHINELAND : BAV | PRU
STATE_RIGA : RUS | UBD
STATE_ROSTOV : RUS
STATE_RUHR : PRU
STATE_RUTHENIA : HUN
STATE_RYAZAN : RUS
STATE_SAMARA : KZH
STATE_SAXONY : COB | MEI | SAX | SCW | WEI
STATE_SCANIA : SWE
STATE_SCHLESWIG_HOLSTEIN : HOL | LUB | SCH
STATE_SKOPIA : TUR
STATE_SLAVONIA : AUS
STATE_SLOVAKIA : HUN
STATE_SLOVENIA : AUS
STATE_SMOLENSK : RUS
STATE_SOUTHERN_TRANSYLVANIA : TRS
STATE_SOUTH_TYROL : AUS | VEN
STATE_STYRIA : AUS
STATE_SVEALAND : SWE
STATE_TALINN : UBD
STATE_TAMBOV : RUS
STATE_TARTARIA : RUS
STATE_TARTU : UBD
STATE_TAURIDA : CRI
STATE_THESSALIA : TUR
STATE_TRANSDANUBIA : HUN
STATE_TVER : RUS
STATE_TYROL : AUS
STATE_UFA : RUS
STATE_UPPER_SILESIA : AUS | PRU
STATE_URAL : RUS
STATE_UUSIMAA : SWE
STATE_VILNIUS : PLC
STATE_VITEBSK : RUS
STATE_VOLHYNIA : PLC
STATE_VYATKA : RUS
STATE_WALLACHIA : WAL
STATE_WESTERN_NORWAY : DENNOR
STATE_WESTERN_SERBIA : TUR
STATE_WESTERN_THRACE : TUR
STATE_WESTPHALIA : LIP | PRU | SCM
STATE_WEST_AEGEAN_ISLANDS : VEN
STATE_WEST_GALICIA : GAL
STATE_WEST_KARELIA : RUS
STATE_WEST_PRUSSIA : PLC | PRU
STATE_WEST_SWITZERLAND : SWI
STATE_WURTTEMBERG : HOH | WUR
STATE_YAROSLAVL : RUS
STATE_ZEALAND : DENNOR
```


## R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA

```text
Mission autonome : R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA — Moyen-Orient, Afrique du Nord, Caucase et Asie centrale

Tu es responsable de la recherche territoriale au 1er janvier 1776 (1776-01-01) pour le mod Victoria 3 « 1776 Age of Revolutions ». Tu recherches, tu ne modifies ni fichiers historiques ni carte, et tu ne pousses aucun changement. Les valeurs initiales du mod et les noms de TAGs ne sont pas des conclusions historiques.

PIÈCES À RECEVOIR : MAP_1776_BASELINE.csv, MAP_1776_9_REGIONS.csv, MAP_1776_RESEARCH_SCHEMA.md, MAP_1776_KNOWN_ISSUES.csv. Utilise uniquement les lignes Region_ID=R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA comme périmètre principal. Les IDs RGB sont ceux du bitmap du jeu, pas des numéros arbitraires. Les lignes d’un même State_ID avec plusieurs Owner_TAG restent distinctes.

PÉRIMÈTRE : Anatolie, Levant, Égypte et Afrique septentrionale, Sahara selon la liste, péninsule Arabique, Perse, Caucase et Asie centrale; Afghanistan confié principalement à cette région, interface baloutche avec R4.
L’inventaire comprend 145 couples pays/État et 93 State_IDs distincts. TAGs existants à auditer dans ce seul périmètre : ABB, ADG, ADR, AHG, AIT, AJJ, ARB, BHN, BRK, BUK, CAUC, CHC, CHI, CIR, CMB, CON, CRI, DLM, DUR, EGY, FTR, GEO, HDJ, IR1, JBB, KBB, KHI, KOK, KZH, LAH, MAS, MBB, MOR, MZB, NBB, OMA, OUA, OZH, PER, POR, RGB, RUS, SD1, SPA, TBI, TEK, TRI, TRM, TRZ, TUA, TUG, TUN, TUR, UZH, ZAI, ZWY.
Interlocuteurs secondaires prévus : R2_NORTHERN_CENTRAL_EASTERN_EUROPE, R4_SOUTH_ASIA, R7_SUBSAHARAN_AFRICA. Une métropole qui possède ailleurs ne t’attribue pas ces territoires. Les mers et lacs sont une référence technique, pas des territoires politiques à attribuer à un pays.

PROBLÈMES DÉJÀ OBSERVÉS : Greater Caucasus a été réattribué CAUC→GEO dans les travaux antérieurs. L’Égypte a maintenant des couples EGY distincts du catalogue ancien. Les provinces métropolitaines britanniques ou russes ne relèvent pas de cette mission. Toutes les références de sujets doivent être comparées à l’autorité réellement attestée.
Références du registre à lire : MAP0-0018 | MAP0-0019 | MAP0-0020 | MAP0-0021 | MAP0-0022 | MAP0-0023 | MAP0-0024 | MAP0-0025 | MAP0-0026 | MAP0-0027 | MAP0-0028 | MAP0-0029 | MAP0-0030 | MAP0-0044 | MAP0-0045 | MAP0-0046 | MAP0-0047 | MAP0-0048 | MAP0-0049 | MAP0-0053 | MAP0-0061 | MAP0-0062 | MAP0-0063 | MAP0-0064 | MAP0-0065 | MAP0-0066 | MAP0-0067 | MAP0-0068 | MAP0-0079 | MAP0-0080 | MAP0-0081 | MAP0-0082 | MAP0-0084 | MAP0-0085 | MAP0-0086 | MAP0-0112 | MAP0-0113 | MAP0-0114 | MAP0-0115 | MAP0-0116 | MAP0-0117 | MAP0-0118 | MAP0-0119 | MAP0-0120 | MAP0-0121 | MAP0-0122 | MAP0-0123 | MAP0-0124 | MAP0-0138 | MAP0-0139 | MAP0-0140 | MAP0-0141 | MAP0-0142 | MAP0-0143 | MAP0-0147 | MAP0-0156 | MAP0-0157 | MAP0-0158 | MAP0-0159 | MAP0-0160 | MAP0-0161 | MAP0-0162 | MAP0-0163 | MAP0-0174 | MAP0-0175 | MAP0-0176 | MAP0-0177 | MAP0-0180 | MAP0-0181 | MAP0-0182 | MAP0-0191 | MAP0-0192 | MAP0-0195 | MAP0-0196 | MAP0-0197 | MAP0-0198 | MAP0-0199 | MAP0-0200 | MAP0-0202 | MAP0-0203 | MAP0-0205 | MAP0-0206
Un conflit de syntaxe ou de fichier n’est pas une preuve historique. Le candidat georg3mx n’est pas fusionné dans main; la baseline représente main actuel.

FORMES DE SOUVERAINETÉ ET DIFFICULTÉS : Autorités provinciales ottomanes, beyliks, pouvoirs mamelouks, tribus et confédérations, fiscalité saharienne, khanats et rapports tributaires. Ne pas considérer une suzeraineté nominale, une caravane, un fort ou une revendication impériale comme administration uniforme. Contradictions probables entre atlas impériaux et études locales.
PRIORITÉS : Priorité : articulation Égypte/Porte, régences maghrébines, Caucase, khanats et steppes, autonomie d’Arabie, frontières afghanes. Coordonner Nil/Sahel avec R7 et Caucase/Balkans avec R2 sans reprendre leurs territoires.

Pour chaque territoire, distinguer administration directe, occupation militaire peu administrée, dépendance/vassalité, protectorat/tribut/influence, compagnie à autorité territoriale, autonomie/souveraineté autochtone, revendication seule, contrôle disputé ou fluctuant, et zone sans frontière précise défendable. Examiner présence administrative, fiscalité, juridiction, garnisons, fortifications, implantations permanentes, traités et structures politiques locales. Un comptoir n’équivaut pas à souveraineté sur toute une State Region. Dater séparément les changements survenus après le 1er janvier, même dans l’année 1776.

SOURCES : atlas historiques argumentés, travaux universitaires spécialisés, traités/documents administratifs contemporains, cartes d’époque avec date et biais, travaux sur les souverainetés locales et autochtones. Pour chaque correction importante, cite au moins une preuve précise. Fournis auteur, titre, date, URL ou référence bibliographique, pages/cartes pertinentes; une URL seule ou une carte moderne non justifiée ne suffit pas. Signale les contradictions et compare la nature des preuves; ne tranche pas silencieusement.

LIVRABLES : R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA_RECOMMENDATIONS.csv conforme à toutes les colonnes et valeurs contrôlées du schéma joint; R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA_SOURCES.csv; R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA_UNCERTAINTIES.md; R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA_COVERAGE.csv avec une ligne pour chaque couple listé, y compris REVIEWED_NO_CHANGE. Cartes annotées facultatives mais utiles. Chaque changement doit distinguer conclusion historique, correspondance géographique proposée, approximation de gameplay et incertitude non résolue.

Si tu ne peux pas faire correspondre une frontière aux provinces du jeu, laisse Province_ID/Province_IDs vides, utilise Mapping_Status=MAPPING_REQUIRED et décris précisément la zone (toponymes, coordonnées, limites, carte/page). N’invente aucun ID ni nouveau TAG. Préfère A_EXISTING_PROVINCES, puis B_STATE_REGIONS; ne demande C_GEOMETRY qu’avec preuve que les provinces existantes sont insuffisantes. Indique Requires_New_Tag et Requires_State_Split sans créer l’entité.

INCERTITUDES ET TRANSMISSION : attribue Change_ID stable, Source_IDs vérifiables et Confidence justifiée. Toute contradiction reste UNRESOLVED; renseigne Cross_Region_Conflict et Secondary_Region_ID, décris les sources opposées et transmets à la synthèse centrale. L’interlocuteur secondaire relit l’interface mais ne duplique pas ta recommandation. Une nouvelle zone extérieure au périmètre est signalée OUTSIDE_BASELINE pour attribution centrale, pas annexée à ta mission. VEN et GEN sont recherchés normalement mais leurs historiques particuliers de population/bâtiments sont protégés. Ne redistribue pas ces données. Aucun résultat n’est automatiquement intégré.

LISTE EXHAUSTIVE DES ÉTATS ET PROPRIÉTAIRES ACTUELS À AUDITER :
STATE_ABU_DHABI : ABB | BHN | OMA
STATE_ADANA : TUR
STATE_AKMOLINSK : OZH | RUS
STATE_AKTOBE : KZH
STATE_ALEPPO : TUR
STATE_ALGIERS : MAS
STATE_AL_RIF : MOR | SPA
STATE_ANKARA : TUR
STATE_ARMENIA : PER
STATE_AYDIN : TUR
STATE_AZERBAIJAN : PER
STATE_BAGHDAD : IR1
STATE_BALKH : DUR
STATE_BASRA : IR1
STATE_CANARY_ISLANDS : SPA
STATE_CENTRAL_HIGHLANDS : DUR
STATE_CONSTANTINE : AIT | CON
STATE_CYPRUS : TUR
STATE_DAGESTAN : CAUC | CHC
STATE_DEIR_EZ_ZOR : IR1
STATE_DIYARBAKIR : TUR
STATE_DONGOLA : SD1 | TUR
STATE_EAST_SAHARA : ADG | AHG | AJJ | CMB | TUG
STATE_EGYPTIAN_DESERT : SD1
STATE_ELIZAVETPOL : PER
STATE_ERZURUM : TUR
STATE_FARS : PER
STATE_FERGANA : KOK
STATE_FEZ : MOR
STATE_GREATER_CAUCASUS : GEO
STATE_HAIL : JBB | NBB
STATE_HEDJAZ : HDJ
STATE_HERAT : DUR
STATE_HUDAVENDIGAR : TUR
STATE_INNER_MAURITANIA : ADR | OUA | RGB
STATE_INNER_MOROCCO : MOR | TEK
STATE_IRAKAJEMI : PER
STATE_ISFAHAN : PER
STATE_JETISY : CHI
STATE_KABUL : DUR
STATE_KANDAHAR : DUR
STATE_KARS : TUR
STATE_KASTAMONU : TUR
STATE_KERMAN : PER
STATE_KHIVA : KHI | KZH | TRM
STATE_KHORASAN : PER
STATE_KHUZESTAN : ARB
STATE_KIRGHIZIA : CHI | KOK
STATE_KONYA : TUR
STATE_KUBAN : CIR | CRI
STATE_LARISTAN : BHN | OMA | PER
STATE_LEBANON : TUR
STATE_LIBYA : TBI | TRI | ZWY
STATE_LIBYAN_DESERT : AJJ | TBI | ZWY
STATE_LOWER_EGYPT : EGY
STATE_LURISTAN : PER
STATE_MADEIRA : POR
STATE_MARRAKECH : MOR
STATE_MATRUH : EGY
STATE_MAURITANIA : ADR | BRK | DLM | FTR | OUA | TRZ
STATE_MAZANDARAN : PER
STATE_MERZ : BUK | KHI | TRM
STATE_MIDDLE_EGYPT : EGY
STATE_MOSUL : IR1
STATE_NEJD : NBB
STATE_NORTHERN_BALUCHISTAN : DUR
STATE_NORTH_CAUCASUS : CAUC | CHC | CIR
STATE_OMAN : OMA
STATE_ORAN : MAS
STATE_PALESTINE : TUR
STATE_PASHTUNISTAN : DUR
STATE_PERSIAN_KURDISTAN : PER
STATE_SAHARA : CMB | MZB | RGB | TEK | TUA
STATE_SEMIRECHE : OZH
STATE_SEMNAN : PER
STATE_SINAI : EGY
STATE_SISTAN : DUR | OMA
STATE_STAVROPOL : CAUC
STATE_SYRDARYA : KOK | KZH | OZH | UZH
STATE_SYRIA : TUR
STATE_TABRIZ : PER
STATE_TAJIKISTAN : BUK | KOK
STATE_TRABZON : TUR
STATE_TRANSJORDAN : TUR
STATE_TRIPOLI : TRI | ZWY
STATE_TUNISIA : TUN
STATE_TURKMENIA : KHI | TRM
STATE_UPPER_EGYPT : EGY
STATE_URALSK : KZH | TRM
STATE_URMIA : PER
STATE_UZBEKIA : BUK
STATE_WEST_SAHARA : DLM | RGB | TEK
STATE_YEMEN : HDJ | KBB | LAH | MBB | ZAI
```


## R4_SOUTH_ASIA

```text
Mission autonome : R4_SOUTH_ASIA — Asie du Sud

Tu es responsable de la recherche territoriale au 1er janvier 1776 (1776-01-01) pour le mod Victoria 3 « 1776 Age of Revolutions ». Tu recherches, tu ne modifies ni fichiers historiques ni carte, et tu ne pousses aucun changement. Les valeurs initiales du mod et les noms de TAGs ne sont pas des conclusions historiques.

PIÈCES À RECEVOIR : MAP_1776_BASELINE.csv, MAP_1776_9_REGIONS.csv, MAP_1776_RESEARCH_SCHEMA.md, MAP_1776_KNOWN_ISSUES.csv. Utilise uniquement les lignes Region_ID=R4_SOUTH_ASIA comme périmètre principal. Les IDs RGB sont ceux du bitmap du jeu, pas des numéros arbitraires. Les lignes d’un même State_ID avec plusieurs Owner_TAG restent distinctes.

PÉRIMÈTRE : Sous-continent indien, Pakistan/Baloutchistan selon la liste, Ceylan et interfaces himalayennes; les régions birmanes sont confiées à R6, Tibet principal à R5, Afghanistan principal à R3.
L’inventaire comprend 54 couples pays/État et 29 State_IDs distincts. TAGs existants à auditer dans ce seul périmètre : AWA, BHU, BHV, BIC, COC, COO, DEI, DENNOR, DUR, FRA, GAR, GBR, GWA, HYD, JEY, KHP, KKI, KNO, MARATH, MGH, MLD, MUG, MYS, NAG, NEP, NET, NGA, OMA, PAN, POR, PUD, SAT, SIK, SIN, TIB, TIP, TRA.
Interlocuteurs secondaires prévus : R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA, R5_EAST_ASIA. Une métropole qui possède ailleurs ne t’attribue pas ces territoires. Les mers et lacs sont une référence technique, pas des territoires politiques à attribuer à un pays.

PROBLÈMES DÉJÀ OBSERVÉS : De nombreux États sont partagés entre TAGs : ne pas fusionner BIC, souverainetés locales et autres compagnies. Les modifications antérieures de populations acceptées et propriété financière britannique ne prouvent pas un contrôle territorial historique.
Références du registre à lire : MAP0-0031 | MAP0-0032 | MAP0-0033 | MAP0-0069 | MAP0-0070 | MAP0-0072 | MAP0-0076 | MAP0-0125 | MAP0-0126 | MAP0-0127 | MAP0-0164 | MAP0-0165 | MAP0-0167 | MAP0-0171
Un conflit de syntaxe ou de fichier n’est pas une preuve historique. Le candidat georg3mx n’est pas fusionné dans main; la baseline représente main actuel.

FORMES DE SOUVERAINETÉ ET DIFFICULTÉS : Compagnies à autorité fiscale ou militaire, souveraineté moghole nominale et administration effective, confédération marathe, principautés, pouvoirs sikhs et comptoirs côtiers. Délimiter comptoir, district fiscal, zone militaire et État autonome. Cartes rétrospectives du Raj sont insuffisantes.
PRIORITÉS : Priorité : possessions et revenus effectifs de BIC au 1er janvier, entités locales, enclaves européennes, frontières du Bengale, Punjab, Mysore, Sri Lanka et Himalaya. Séparer les transformations postérieures dans l’année 1776.

Pour chaque territoire, distinguer administration directe, occupation militaire peu administrée, dépendance/vassalité, protectorat/tribut/influence, compagnie à autorité territoriale, autonomie/souveraineté autochtone, revendication seule, contrôle disputé ou fluctuant, et zone sans frontière précise défendable. Examiner présence administrative, fiscalité, juridiction, garnisons, fortifications, implantations permanentes, traités et structures politiques locales. Un comptoir n’équivaut pas à souveraineté sur toute une State Region. Dater séparément les changements survenus après le 1er janvier, même dans l’année 1776.

SOURCES : atlas historiques argumentés, travaux universitaires spécialisés, traités/documents administratifs contemporains, cartes d’époque avec date et biais, travaux sur les souverainetés locales et autochtones. Pour chaque correction importante, cite au moins une preuve précise. Fournis auteur, titre, date, URL ou référence bibliographique, pages/cartes pertinentes; une URL seule ou une carte moderne non justifiée ne suffit pas. Signale les contradictions et compare la nature des preuves; ne tranche pas silencieusement.

LIVRABLES : R4_SOUTH_ASIA_RECOMMENDATIONS.csv conforme à toutes les colonnes et valeurs contrôlées du schéma joint; R4_SOUTH_ASIA_SOURCES.csv; R4_SOUTH_ASIA_UNCERTAINTIES.md; R4_SOUTH_ASIA_COVERAGE.csv avec une ligne pour chaque couple listé, y compris REVIEWED_NO_CHANGE. Cartes annotées facultatives mais utiles. Chaque changement doit distinguer conclusion historique, correspondance géographique proposée, approximation de gameplay et incertitude non résolue.

Si tu ne peux pas faire correspondre une frontière aux provinces du jeu, laisse Province_ID/Province_IDs vides, utilise Mapping_Status=MAPPING_REQUIRED et décris précisément la zone (toponymes, coordonnées, limites, carte/page). N’invente aucun ID ni nouveau TAG. Préfère A_EXISTING_PROVINCES, puis B_STATE_REGIONS; ne demande C_GEOMETRY qu’avec preuve que les provinces existantes sont insuffisantes. Indique Requires_New_Tag et Requires_State_Split sans créer l’entité.

INCERTITUDES ET TRANSMISSION : attribue Change_ID stable, Source_IDs vérifiables et Confidence justifiée. Toute contradiction reste UNRESOLVED; renseigne Cross_Region_Conflict et Secondary_Region_ID, décris les sources opposées et transmets à la synthèse centrale. L’interlocuteur secondaire relit l’interface mais ne duplique pas ta recommandation. Une nouvelle zone extérieure au périmètre est signalée OUTSIDE_BASELINE pour attribution centrale, pas annexée à ta mission. VEN et GEN sont recherchés normalement mais leurs historiques particuliers de population/bâtiments sont protégés. Ne redistribue pas ces données. Aucun résultat n’est automatiquement intégré.

LISTE EXHAUSTIVE DES ÉTATS ET PROPRIÉTAIRES ACTUELS À AUDITER :
STATE_AGRA : GAR | MARATH
STATE_ASSAM : KKI | MGH | NGA | TIP
STATE_AWADH : AWA | BIC
STATE_BALUCHISTAN : DUR | OMA
STATE_BIHAR : BIC
STATE_BOMBAY : KHP | MARATH | POR | SAT
STATE_BUNDELKHAND : BIC | MARATH
STATE_CENTRAL_PROVINCES : HYD | MARATH | NAG
STATE_CEYLON : DEI | GBR | MLD
STATE_CIRCARS : BIC | JEY
STATE_DELHI : MUG
STATE_EASTERN_HIMALAYAS : BHU | SIK | TIB
STATE_EAST_BENGAL : BIC
STATE_GUJARAT : BHV | POR
STATE_HILL_PUNJAB : DUR
STATE_HIMALAYAS : NEP
STATE_HYDERABAD : HYD
STATE_KASHMIR : DUR
STATE_KURNOOL : KNO
STATE_MADRAS : DENNOR | FRA | PUD
STATE_MALWA : GWA | MARATH
STATE_MYSORE : MYS
STATE_ORISSA : NAG
STATE_PUNJAB : DUR | PAN
STATE_QUETTA : DUR
STATE_RAJPUTANA : GWA
STATE_SINDH : SIN
STATE_TRAVANCORE : COC | NET | TRA
STATE_WEST_BENGAL : BIC | COO
```


## R5_EAST_ASIA

```text
Mission autonome : R5_EAST_ASIA — Asie orientale

Tu es responsable de la recherche territoriale au 1er janvier 1776 (1776-01-01) pour le mod Victoria 3 « 1776 Age of Revolutions ». Tu recherches, tu ne modifies ni fichiers historiques ni carte, et tu ne pousses aucun changement. Les valeurs initiales du mod et les noms de TAGs ne sont pas des conclusions historiques.

PIÈCES À RECEVOIR : MAP_1776_BASELINE.csv, MAP_1776_9_REGIONS.csv, MAP_1776_RESEARCH_SCHEMA.md, MAP_1776_KNOWN_ISSUES.csv. Utilise uniquement les lignes Region_ID=R5_EAST_ASIA comme périmètre principal. Les IDs RGB sont ceux du bitmap du jeu, pas des numéros arbitraires. Les lignes d’un même State_ID avec plusieurs Owner_TAG restent distinctes.

PÉRIMÈTRE : Chine, Mongolie et Tibet selon la liste, Corée, Japon, Ryukyu et Sibérie/Extrême-Orient attribués ici; l’Indochine et le Siam sont confiés à R6, l’Alaska à R8.
L’inventaire comprend 84 couples pays/État et 75 State_IDs distincts. TAGs existants à auditer dans ce seul périmètre : AIN, ALK, ATB, CHI, EZO, JAP, KOR, KZH, OZH, POR, RUS, RYU, SKH, TIB, ULT.
Interlocuteurs secondaires prévus : R2_NORTHERN_CENTRAL_EASTERN_EUROPE, R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA, R4_SOUTH_ASIA, R6_SOUTHEAST_ASIA_OCEANIA. Une métropole qui possède ailleurs ne t’attribue pas ces territoires. Les mers et lacs sont une référence technique, pas des territoires politiques à attribuer à un pays.

PROBLÈMES DÉJÀ OBSERVÉS : Gansu contient une attribution historique de xBD5671, classé comme lac dans default.map et hors de sa State Region. Les revendications russes et l’autorité des TAGs autochtones de Sibérie doivent être distinguées du mapping existant.
Références du registre à lire : MAP0-0052 | MAP0-0071 | MAP0-0146 | MAP0-0166
Un conflit de syntaxe ou de fichier n’est pas une preuve historique. Le candidat georg3mx n’est pas fusionné dans main; la baseline représente main actuel.

FORMES DE SOUVERAINETÉ ET DIFFICULTÉS : Administration Qing et frontières à juridictions différentes, rapports tributaires coréens et ryukyuans, gouvernement shogunal/domaines, souverainetés aïnues, contrôle russe à implantation inégale. Ne pas confondre tribut, hommage, échanges et annexion. Comparer cartographie officielle et travaux locaux.
PRIORITÉS : Priorité : marches Qing/Tibet/Mongolie, côte mandchoue, Hokkaido/Sakhaline et populations locales, Sibérie. Coordonner Himalaya avec R4, Yunnan/Tonkin avec R6, steppes avec R3 et frontière de mission transouralienne avec R2.

Pour chaque territoire, distinguer administration directe, occupation militaire peu administrée, dépendance/vassalité, protectorat/tribut/influence, compagnie à autorité territoriale, autonomie/souveraineté autochtone, revendication seule, contrôle disputé ou fluctuant, et zone sans frontière précise défendable. Examiner présence administrative, fiscalité, juridiction, garnisons, fortifications, implantations permanentes, traités et structures politiques locales. Un comptoir n’équivaut pas à souveraineté sur toute une State Region. Dater séparément les changements survenus après le 1er janvier, même dans l’année 1776.

SOURCES : atlas historiques argumentés, travaux universitaires spécialisés, traités/documents administratifs contemporains, cartes d’époque avec date et biais, travaux sur les souverainetés locales et autochtones. Pour chaque correction importante, cite au moins une preuve précise. Fournis auteur, titre, date, URL ou référence bibliographique, pages/cartes pertinentes; une URL seule ou une carte moderne non justifiée ne suffit pas. Signale les contradictions et compare la nature des preuves; ne tranche pas silencieusement.

LIVRABLES : R5_EAST_ASIA_RECOMMENDATIONS.csv conforme à toutes les colonnes et valeurs contrôlées du schéma joint; R5_EAST_ASIA_SOURCES.csv; R5_EAST_ASIA_UNCERTAINTIES.md; R5_EAST_ASIA_COVERAGE.csv avec une ligne pour chaque couple listé, y compris REVIEWED_NO_CHANGE. Cartes annotées facultatives mais utiles. Chaque changement doit distinguer conclusion historique, correspondance géographique proposée, approximation de gameplay et incertitude non résolue.

Si tu ne peux pas faire correspondre une frontière aux provinces du jeu, laisse Province_ID/Province_IDs vides, utilise Mapping_Status=MAPPING_REQUIRED et décris précisément la zone (toponymes, coordonnées, limites, carte/page). N’invente aucun ID ni nouveau TAG. Préfère A_EXISTING_PROVINCES, puis B_STATE_REGIONS; ne demande C_GEOMETRY qu’avec preuve que les provinces existantes sont insuffisantes. Indique Requires_New_Tag et Requires_State_Split sans créer l’entité.

INCERTITUDES ET TRANSMISSION : attribue Change_ID stable, Source_IDs vérifiables et Confidence justifiée. Toute contradiction reste UNRESOLVED; renseigne Cross_Region_Conflict et Secondary_Region_ID, décris les sources opposées et transmets à la synthèse centrale. L’interlocuteur secondaire relit l’interface mais ne duplique pas ta recommandation. Une nouvelle zone extérieure au périmètre est signalée OUTSIDE_BASELINE pour attribution centrale, pas annexée à ta mission. VEN et GEN sont recherchés normalement mais leurs historiques particuliers de population/bâtiments sont protégés. Ne redistribue pas ces données. Aucun résultat n’est automatiquement intégré.

LISTE EXHAUSTIVE DES ÉTATS ET PROPRIÉTAIRES ACTUELS À AUDITER :
STATE_ALTAI : CHI
STATE_ALXA : CHI
STATE_AMUR : CHI
STATE_BEIJING : CHI
STATE_BURYATIA : RUS
STATE_BUSAN : KOR
STATE_CHELYABINSK : KZH | OZH | RUS
STATE_CHONGQING : CHI
STATE_CHUGOKU : JAP
STATE_CHUKOTKA : ATB
STATE_DZUNGARIA : CHI
STATE_EASTERN_HUBEI : CHI
STATE_FORMOSA : CHI
STATE_FUJIAN : CHI
STATE_GANSU : CHI
STATE_GUANGDONG : CHI | POR
STATE_GUANGXI : CHI
STATE_GUIZHOU : CHI
STATE_HENAN : CHI
STATE_HINGGAN : CHI
STATE_HOKKAIDO : EZO | JAP
STATE_HOKUSHINETSU : JAP
STATE_HUNAN : CHI
STATE_IRKUTSK : RUS
STATE_JIANGSU : CHI
STATE_JIANGXI : CHI
STATE_KAMCHATKA : RUS
STATE_KANSAI : JAP
STATE_KANTO : JAP
STATE_KOLYMA : RUS
STATE_KRASNOYARSK : RUS
STATE_KYOTO : JAP
STATE_KYUSHU : JAP
STATE_LHASA : TIB
STATE_NANJING : CHI
STATE_NGARI : TIB
STATE_NINGXIA : CHI
STATE_NORTHERN_ANHUI : CHI
STATE_NORTHERN_MANCHURIA : CHI
STATE_OB : RUS
STATE_OKHOTSK : RUS
STATE_OUTER_MANCHURIA : CHI
STATE_PYONGYANG : KOR
STATE_QINGHAI : CHI
STATE_RYUKYU_ISLANDS : JAP | RYU
STATE_SAKHALIN : AIN | ALK | EZO | SKH | ULT
STATE_SARIWON : KOR
STATE_SEOUL : KOR
STATE_SHANDONG : CHI
STATE_SHANXI : CHI
STATE_SHAOZHOU : CHI
STATE_SHENGJING : CHI
STATE_SHIKOKU : JAP
STATE_SICHUAN : CHI
STATE_SOUTHERN_ANHUI : CHI
STATE_SOUTHERN_MANCHURIA : CHI
STATE_SURGUT : RUS
STATE_SUZHOU : CHI
STATE_TIANSHAN : CHI
STATE_TOBOLSK : RUS
STATE_TOHOKU : JAP
STATE_TOKAI : JAP
STATE_TOMSK : RUS
STATE_TRANS_BAIKAL : RUS
STATE_TUVA : CHI
STATE_ULIASTAI : CHI
STATE_UPPER_YENISEYSK : RUS
STATE_URGA : CHI
STATE_WESTERN_HUBEI : CHI
STATE_XIAN : CHI
STATE_YAKUTSK : RUS
STATE_YANGHO : KOR
STATE_YUNNAN : CHI
STATE_ZHEJIANG : CHI
STATE_ZHILI : CHI
```


## R6_SOUTHEAST_ASIA_OCEANIA

```text
Mission autonome : R6_SOUTHEAST_ASIA_OCEANIA — Asie du Sud-Est et Océanie

Tu es responsable de la recherche territoriale au 1er janvier 1776 (1776-01-01) pour le mod Victoria 3 « 1776 Age of Revolutions ». Tu recherches, tu ne modifies ni fichiers historiques ni carte, et tu ne pousses aucun changement. Les valeurs initiales du mod et les noms de TAGs ne sont pas des conclusions historiques.

PIÈCES À RECEVOIR : MAP_1776_BASELINE.csv, MAP_1776_9_REGIONS.csv, MAP_1776_RESEARCH_SCHEMA.md, MAP_1776_KNOWN_ISSUES.csv. Utilise uniquement les lignes Region_ID=R6_SOUTHEAST_ASIA_OCEANIA comme périmètre principal. Les IDs RGB sont ceux du bitmap du jeu, pas des numéros arbitraires. Les lignes d’un même State_ID avec plusieurs Owner_TAG restent distinctes.

PÉRIMÈTRE : Indochine et Siam, Birmanie, péninsule malaise, archipels indonésiens et philippins, Nouvelle-Guinée, Australasie et Pacifique, y compris Hawaii; chaque territoire exact est listé ci-dessous.
L’inventaire comprend 130 couples pays/État et 52 State_IDs distincts. TAGs existants à auditer dans ce seul périmètre : ACE, ARH, ARR, BAL, BIC, BLA, BLG, BNJ, BRU, BTN, BUR, CAM, CHP, CMI, DAI, DEI, DENNOR, DGR, FJI, GRW, HAW, HLA, INDOP, JMB, JOH, KAU, KKI, KLN, KLO, KNC, KNK, KRI, KTI, KTU, KYN, LAN, LRR, LUA, MCR, MGD, MND, MRA, MRN, NNG, NRU, NTO, NTU, NYP, PAA, PHI, PLY, PMA, PON, POR, PPU, PRK, SAK, SCT, SEL, SHS, SIA, SLW, SMB, SRK, STG, SUL, TID, TNG, UNT, VNT, WDJ, WKB, WRR, WTI, YGU, YOG, YUR.
Interlocuteurs secondaires prévus : R4_SOUTH_ASIA, R5_EAST_ASIA. Une métropole qui possède ailleurs ne t’attribue pas ces territoires. Les mers et lacs sont une référence technique, pas des territoires politiques à attribuer à un pays.

PROBLÈMES DÉJÀ OBSERVÉS : Une province de STATE_WEST_MICRONESIA, xEF50C0, n’a pas de propriétaire écrit au départ. L’affectation à un chercheur n’est pas une proposition de propriétaire. L’ancienne région source classait à tort les États indochinois dans R5 et Hawaii dans R8.
Références du registre à lire : MAP0-0034 | MAP0-0035 | MAP0-0036 | MAP0-0037 | MAP0-0050 | MAP0-0051 | MAP0-0073 | MAP0-0089 | MAP0-0128 | MAP0-0129 | MAP0-0130 | MAP0-0131 | MAP0-0144 | MAP0-0145 | MAP0-0168 | MAP0-0186
Un conflit de syntaxe ou de fichier n’est pas une preuve historique. Le candidat georg3mx n’est pas fusionné dans main; la baseline représente main actuel.

FORMES DE SOUVERAINETÉ ET DIFFICULTÉS : Mandala politique, tribut et autonomie locale, compagnies commerciales et ports, pouvoirs insulaires, souverainetés autochtones d’Australie et du Pacifique. Aucun remplissage colonial automatique des intérieurs ou des îles. Des frontières linéaires modernes peuvent être historiquement indéfendables.
PRIORITÉS : Priorité : autorité effective de DEI, districts côtiers et comptoirs, rapports politiques indochinois, Timor/Moluques/Philippines, absence ou faiblesse du contrôle européen en Océanie. Coordonner Birmanie avec R4, Tonkin avec R5.

Pour chaque territoire, distinguer administration directe, occupation militaire peu administrée, dépendance/vassalité, protectorat/tribut/influence, compagnie à autorité territoriale, autonomie/souveraineté autochtone, revendication seule, contrôle disputé ou fluctuant, et zone sans frontière précise défendable. Examiner présence administrative, fiscalité, juridiction, garnisons, fortifications, implantations permanentes, traités et structures politiques locales. Un comptoir n’équivaut pas à souveraineté sur toute une State Region. Dater séparément les changements survenus après le 1er janvier, même dans l’année 1776.

SOURCES : atlas historiques argumentés, travaux universitaires spécialisés, traités/documents administratifs contemporains, cartes d’époque avec date et biais, travaux sur les souverainetés locales et autochtones. Pour chaque correction importante, cite au moins une preuve précise. Fournis auteur, titre, date, URL ou référence bibliographique, pages/cartes pertinentes; une URL seule ou une carte moderne non justifiée ne suffit pas. Signale les contradictions et compare la nature des preuves; ne tranche pas silencieusement.

LIVRABLES : R6_SOUTHEAST_ASIA_OCEANIA_RECOMMENDATIONS.csv conforme à toutes les colonnes et valeurs contrôlées du schéma joint; R6_SOUTHEAST_ASIA_OCEANIA_SOURCES.csv; R6_SOUTHEAST_ASIA_OCEANIA_UNCERTAINTIES.md; R6_SOUTHEAST_ASIA_OCEANIA_COVERAGE.csv avec une ligne pour chaque couple listé, y compris REVIEWED_NO_CHANGE. Cartes annotées facultatives mais utiles. Chaque changement doit distinguer conclusion historique, correspondance géographique proposée, approximation de gameplay et incertitude non résolue.

Si tu ne peux pas faire correspondre une frontière aux provinces du jeu, laisse Province_ID/Province_IDs vides, utilise Mapping_Status=MAPPING_REQUIRED et décris précisément la zone (toponymes, coordonnées, limites, carte/page). N’invente aucun ID ni nouveau TAG. Préfère A_EXISTING_PROVINCES, puis B_STATE_REGIONS; ne demande C_GEOMETRY qu’avec preuve que les provinces existantes sont insuffisantes. Indique Requires_New_Tag et Requires_State_Split sans créer l’entité.

INCERTITUDES ET TRANSMISSION : attribue Change_ID stable, Source_IDs vérifiables et Confidence justifiée. Toute contradiction reste UNRESOLVED; renseigne Cross_Region_Conflict et Secondary_Region_ID, décris les sources opposées et transmets à la synthèse centrale. L’interlocuteur secondaire relit l’interface mais ne duplique pas ta recommandation. Une nouvelle zone extérieure au périmètre est signalée OUTSIDE_BASELINE pour attribution centrale, pas annexée à ta mission. VEN et GEN sont recherchés normalement mais leurs historiques particuliers de population/bâtiments sont protégés. Ne redistribue pas ces données. Aucun résultat n’est automatiquement intégré.

LISTE EXHAUSTIVE DES ÉTATS ET PROPRIÉTAIRES ACTUELS À AUDITER :
STATE_ACEH : ACE | INDOP | SAK
STATE_ANNAM : DAI
STATE_ARAKAN : KKI
STATE_BANGKOK : SIA
STATE_BOUGAINVILLE : HLA
STATE_CAMBODIA : CAM | KLO | SIA
STATE_CELEBES : BTN | DEI | SLW | TID
STATE_CENTRAL_JAVA : DEI | SRK | YOG
STATE_CHIANG_MAI : CMI
STATE_EASTERN_NEW_GUINEA : PPU
STATE_EAST_BORNEO : BLG | BNJ | INDOP | KTI
STATE_EAST_JAVA : DEI
STATE_EAST_MICRONESIA : MCR
STATE_FIJI : FJI
STATE_HAWAIIAN_ISLANDS : HAW
STATE_KACHIN : BUR
STATE_KANAK : KNK
STATE_LAOS : CHP | DAI | LUA | SCT | SIA
STATE_LUZON : PHI | SUL
STATE_MALAYA : JOH | PRK | SEL | SIA
STATE_MANDALAY : BUR | KKI
STATE_MEKONG : DAI | DGR
STATE_MINDANAO : MGD | MND | PHI | SUL
STATE_MOLUCCAS : DEI | TID
STATE_NAKHON_RATCHASIMA : SIA
STATE_NAURU : NRU
STATE_NEW_SOUTH_WALES : KLN | KNC | KRI | PAA | WDJ | YUR
STATE_NORTHERN_TERRITORY : ARH | ARR | GRW | KNC | LRR | NYP | WRR | WTI | YGU
STATE_NORTH_BORNEO : BLG | BRU | SUL
STATE_NORTH_ISLAND : NTO | UNT
STATE_NORTH_SUMATRA : INDOP | JMB | SAK
STATE_PEGU : BIC | BUR | DENNOR
STATE_QUEENSLAND : ARR | GRW | KNC | MRA | PAA | PMA | WDJ | WKB
STATE_SHAN_STATES : BUR | SHS
STATE_SOLOMON_ISLANDS : BLA
STATE_SOUTH_AUSTRALIA : KAU | KLN | KNC | MRN | PAA | WTI | YUR
STATE_SOUTH_ISLAND : NTO | NTU
STATE_SOUTH_SUMATRA : INDOP
STATE_SUNDA_ISLANDS : BAL | DEI | POR
STATE_TAHITI : PLY
STATE_TASMANIA : WTI
STATE_TENASSERIM : BUR | SIA
STATE_TONGA : TNG
STATE_TONKIN : DAI | SCT
STATE_VANUATU : VNT
STATE_VICTORIA : KLN | KRI
STATE_VISAYAS : PHI
STATE_WESTERN_AUSTRALIA : KTU | KYN | MRN | NNG | NYP | WRR | WTI
STATE_WESTERN_NEW_GUINEA : PPU | TID
STATE_WEST_BORNEO : INDOP | LAN | PON | SMB | STG
STATE_WEST_JAVA : DEI
STATE_WEST_MICRONESIA : MCR | PHI
```


## R7_SUBSAHARAN_AFRICA

```text
Mission autonome : R7_SUBSAHARAN_AFRICA — Afrique subsaharienne

Tu es responsable de la recherche territoriale au 1er janvier 1776 (1776-01-01) pour le mod Victoria 3 « 1776 Age of Revolutions ». Tu recherches, tu ne modifies ni fichiers historiques ni carte, et tu ne pousses aucun changement. Les valeurs initiales du mod et les noms de TAGs ne sont pas des conclusions historiques.

PIÈCES À RECEVOIR : MAP_1776_BASELINE.csv, MAP_1776_9_REGIONS.csv, MAP_1776_RESEARCH_SCHEMA.md, MAP_1776_KNOWN_ISSUES.csv. Utilise uniquement les lignes Region_ID=R7_SUBSAHARAN_AFRICA comme périmètre principal. Les IDs RGB sont ceux du bitmap du jeu, pas des numéros arbitraires. Les lignes d’un même State_ID avec plusieurs Owner_TAG restent distinctes.

PÉRIMÈTRE : Afrique au sud des périmètres sahariens convenus, espaces sahéliens listés ici, Corne orientale attribuée, Madagascar, Cap-Vert et îles de l’océan Indien attribuées ici; aucun rattachement par métropole.
L’inventaire comprend 196 couples pays/État et 71 State_IDs distincts. TAGs existants à auditer dans ce seul périmètre : ACH, ADG, ADR, AGC, AIR, AJJ, AJR, ANK, ASH, ATR, AUL, AYI, BEN, BGI, BLE, BMB, BMM, BND, BNG, BNY, BOB, BOR, BRD, BRG, BST, BUG, CAY, CHK, DAH, DAK, DEI, DENNOR, DFR, DFT, DIN, DIO, DLA, DNK, ETH, EWE, FNG, FRA, FTJ, FTR, GBR, GGO, GLD, HAU, HHE, HMB, HRO, IBO, ISQ, JLF, KBA, KBD, KBU, KKY, KNG, KON, KRG, KRT, KRU, KSN, KZM, LBA, LGA, LND, LNG, LUO, LZO, MAD, MBS, MDK, MJK, MJT, MNB, MNC, MOS, MRV, MSH, MSI, MSK, MSN, MTB, MTP, NAM, NET, NUE, NYM, OMA, ORA, ORM, OUA, OVB, OVM, OYO, PDI, PHL, POR, RGB, RWD, SAN, SD1, SGU, SIL, SKM, SKY, SNG, SOK, SRR, SSU, SWZ, TBI, TGI, TKE, TMN, TPS, TRK, TRN, TSW, TUR, VND, WAD, WBL, WSG, WTU, XHO, YKA, ZND.
Interlocuteurs secondaires prévus : R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA. Une métropole qui possède ailleurs ne t’attribue pas ces territoires. Les mers et lacs sont une référence technique, pas des territoires politiques à attribuer à un pays.

PROBLÈMES DÉJÀ OBSERVÉS : La mission inclut des zones autrefois stockées dans 03_north_africa.txt : ce fichier n’est pas une frontière historique. Country_Type=decentralized décrit le moteur, pas l’absence de souveraineté. Vérifier la portée territoriale des compagnies et ports européens plutôt que recopier la couleur actuelle.
Références du registre à lire : MAP0-0038 | MAP0-0039 | MAP0-0040 | MAP0-0041 | MAP0-0042 | MAP0-0043 | MAP0-0074 | MAP0-0075 | MAP0-0077 | MAP0-0132 | MAP0-0133 | MAP0-0134 | MAP0-0135 | MAP0-0136 | MAP0-0137 | MAP0-0169 | MAP0-0170 | MAP0-0172
Un conflit de syntaxe ou de fichier n’est pas une preuve historique. Le candidat georg3mx n’est pas fusionné dans main; la baseline représente main actuel.

FORMES DE SOUVERAINETÉ ET DIFFICULTÉS : Royaumes, cités, chefferies et confédérations, réseaux tributaires et mobiles, souverainetés pastorales, comptoirs, colonies permanentes limitées, juridictions portuaires. Attention aux projections coloniales du XIXe siècle et aux sources excluant les pouvoirs locaux.
PRIORITÉS : Priorité : contrôle côtier réel, États et autorités locales, Sahel/Nil, Corne, Cap, Madagascar et îles. Signaler les zones sans frontière linéaire défendable; coordonner Sahara/Nil avec R3 sans attribuer tous les espaces à une métropole.

Pour chaque territoire, distinguer administration directe, occupation militaire peu administrée, dépendance/vassalité, protectorat/tribut/influence, compagnie à autorité territoriale, autonomie/souveraineté autochtone, revendication seule, contrôle disputé ou fluctuant, et zone sans frontière précise défendable. Examiner présence administrative, fiscalité, juridiction, garnisons, fortifications, implantations permanentes, traités et structures politiques locales. Un comptoir n’équivaut pas à souveraineté sur toute une State Region. Dater séparément les changements survenus après le 1er janvier, même dans l’année 1776.

SOURCES : atlas historiques argumentés, travaux universitaires spécialisés, traités/documents administratifs contemporains, cartes d’époque avec date et biais, travaux sur les souverainetés locales et autochtones. Pour chaque correction importante, cite au moins une preuve précise. Fournis auteur, titre, date, URL ou référence bibliographique, pages/cartes pertinentes; une URL seule ou une carte moderne non justifiée ne suffit pas. Signale les contradictions et compare la nature des preuves; ne tranche pas silencieusement.

LIVRABLES : R7_SUBSAHARAN_AFRICA_RECOMMENDATIONS.csv conforme à toutes les colonnes et valeurs contrôlées du schéma joint; R7_SUBSAHARAN_AFRICA_SOURCES.csv; R7_SUBSAHARAN_AFRICA_UNCERTAINTIES.md; R7_SUBSAHARAN_AFRICA_COVERAGE.csv avec une ligne pour chaque couple listé, y compris REVIEWED_NO_CHANGE. Cartes annotées facultatives mais utiles. Chaque changement doit distinguer conclusion historique, correspondance géographique proposée, approximation de gameplay et incertitude non résolue.

Si tu ne peux pas faire correspondre une frontière aux provinces du jeu, laisse Province_ID/Province_IDs vides, utilise Mapping_Status=MAPPING_REQUIRED et décris précisément la zone (toponymes, coordonnées, limites, carte/page). N’invente aucun ID ni nouveau TAG. Préfère A_EXISTING_PROVINCES, puis B_STATE_REGIONS; ne demande C_GEOMETRY qu’avec preuve que les provinces existantes sont insuffisantes. Indique Requires_New_Tag et Requires_State_Split sans créer l’entité.

INCERTITUDES ET TRANSMISSION : attribue Change_ID stable, Source_IDs vérifiables et Confidence justifiée. Toute contradiction reste UNRESOLVED; renseigne Cross_Region_Conflict et Secondary_Region_ID, décris les sources opposées et transmets à la synthèse centrale. L’interlocuteur secondaire relit l’interface mais ne duplique pas ta recommandation. Une nouvelle zone extérieure au périmètre est signalée OUTSIDE_BASELINE pour attribution centrale, pas annexée à ta mission. VEN et GEN sont recherchés normalement mais leurs historiques particuliers de population/bâtiments sont protégés. Ne redistribue pas ces données. Aucun résultat n’est automatiquement intégré.

LISTE EXHAUSTIVE DES ÉTATS ET PROPRIÉTAIRES ACTUELS À AUDITER :
STATE_AMHARA : ETH
STATE_BAS_CONGO : KON | YKA
STATE_BENIN : BEN
STATE_BLUE_NILE : SD1
STATE_BORNU : BOR
STATE_BOTSWANA : LZO | SAN | TSW
STATE_CAPE_COLONY : DEI | NAM
STATE_CAPE_VERDE : POR
STATE_CHAD : BOR | TBI | WAD
STATE_CONGO : BOB | LNG | TKE
STATE_CONGO_ORIENTALE : HMB | LBA | LGA | MNB | ZND
STATE_DAHOMEY : BRG | DAH
STATE_DARFUR : DFR
STATE_EASTERN_CAPE : DEI | XHO
STATE_EASTERN_MALI : MSN
STATE_EAST_ANGOLA : CHK | KSN | LND | LZO
STATE_EAST_HAUSALAND : SOK
STATE_EQUATEUR : BNG | BOB
STATE_EQUATORIA : DFT | DNK | NUE | TPS
STATE_ERITREA : ETH | SD1 | TUR
STATE_GABON : FNG | LNG
STATE_GOLD_COAST : ASH | DENNOR | NET | SIL
STATE_GONDER : ETH
STATE_GUINEA : FTJ | KBU | MDK | POR | SSU
STATE_HAUSALAND : BRG | SOK
STATE_HEREROLAND : HRO | OVB | SAN
STATE_INDIAN_OCEAN_TERRITORY : FRA | GBR
STATE_IVORY_COAST : AYI | BLE | FRA | KNG
STATE_KASAI : KBA | LBA
STATE_KATANGA : KZM | LBA | LND
STATE_KAZEMBE : BMB | KZM | MRV
STATE_KENYA : AJR | AUL | KKY | MBS | MJK | OMA | ORM | SKY | WTU
STATE_KORDOFAN : SD1
STATE_LIBERIA : KRU | MDK
STATE_LINDI : GGO | HHE | SNG
STATE_LOURENCO_MARQUES : POR | TSW
STATE_MOCAMBIQUE : AGC | MRV | POR | TGI
STATE_NAMAQUALAND : NAM | SAN
STATE_NIGER : AIR | AJJ | DIN | TBI
STATE_NIGERIA : SOK
STATE_NIGER_DELTA : IBO
STATE_NORTHERN_CAPE : SAN | TSW | WBL
STATE_NORTH_ANGOLA : KON | POR
STATE_NORTH_CAMEROON : BMM | SOK
STATE_NORTH_MADAGASCAR : MAD
STATE_OROMIA : ETH
STATE_OUTER_HAUSALAND : BOR | HAU | SOK
STATE_RIFT_VALLEY : LUO | MSI | TRK
STATE_SENEGAL : BND | CAY | DIO | FRA | FTR | JLF | KBU | POR | SIL | SRR
STATE_SIERRA_LEONE : MDK | SIL | TMN
STATE_SOMALILAND : GLD | ISQ | MJT | WSG
STATE_SOUTH_ANGOLA : HRO | OVB | OVM | POR
STATE_SOUTH_CAMEROON : DLA | FNG | POR | SIL
STATE_SOUTH_MADAGASCAR : MAD
STATE_TANGANYIKA : BRD | KRG | MSI | NYM | RWD | SKM
STATE_TIMBUKTU : ADG | ADR | ATR | MSN | OUA | RGB
STATE_TOGO : ASH | EWE
STATE_TRANSVAAL : MTB | PDI | SWZ | TRN | VND
STATE_UBANGI_SHARI : DAK | ZND
STATE_UGANDA : ACH | ANK | BNY | BUG
STATE_VOLTA : KNG | MOS
STATE_VRYSTAAT : BST | ORA | PHL
STATE_WADDAI : BGI | BOR | WAD
STATE_WESTERN_MALI : KRT | SGU
STATE_WINDWARD_COAST : BLE | KBD | KRU
STATE_YORUBA_STATES : OYO
STATE_ZAMBEZI : MNC | MSH | MTP
STATE_ZAMBEZIA : MNC | MSK | MTP | POR | TSW
STATE_ZAMBIA : BMB | LZO
STATE_ZANZIBAR : OMA
STATE_ZULULAND : BST | TSW
```


## R8_NORTH_AMERICA_CARIBBEAN

```text
Mission autonome : R8_NORTH_AMERICA_CARIBBEAN — Amérique du Nord et Caraïbes

Tu es responsable de la recherche territoriale au 1er janvier 1776 (1776-01-01) pour le mod Victoria 3 « 1776 Age of Revolutions ». Tu recherches, tu ne modifies ni fichiers historiques ni carte, et tu ne pousses aucun changement. Les valeurs initiales du mod et les noms de TAGs ne sont pas des conclusions historiques.

PIÈCES À RECEVOIR : MAP_1776_BASELINE.csv, MAP_1776_9_REGIONS.csv, MAP_1776_RESEARCH_SCHEMA.md, MAP_1776_KNOWN_ISSUES.csv. Utilise uniquement les lignes Region_ID=R8_NORTH_AMERICA_CARIBBEAN comme périmètre principal. Les IDs RGB sont ceux du bitmap du jeu, pas des numéros arbitraires. Les lignes d’un même State_ID avec plusieurs Owner_TAG restent distinctes.

PÉRIMÈTRE : Amérique du Nord, Groenland, Alaska, Mexique, Amérique centrale et Caraïbes; Hawaii relève de R6. Ne pas répartir les colonies britanniques, françaises, espagnoles ou danoises entre missions européennes.
L’inventaire comprend 125 couples pays/État et 93 State_IDs distincts. TAGs existants à auditer dans ce seul périmètre : ABS, ALK, APC, ARP, ATB, BLF, BNN, COM, CUB, DENNOR, FRA, GBR, GR5, GR7, HAI, HBC, IRC, LKT, LOU, MICC, MKT, NBS, NET, NVJ, NVS, NZP, ONT, PCO, PWN, QUE, SC1, SC2, SLS, SML, SPA, USA, UTE.
Interlocuteurs secondaires prévus : R9_SOUTH_AMERICA. Une métropole qui possède ailleurs ne t’attribue pas ces territoires. Les mers et lacs sont une référence technique, pas des territoires politiques à attribuer à un pays.

PROBLÈMES DÉJÀ OBSERVÉS : Nunavut a été regroupé sous HBC dans des travaux déjà intégrés. Des attributions contradictoires existent en Alaska, Nouveau-Mexique et ailleurs : voir le registre. x26A0BA au Yukon et x8D15CB en Ontario sont aussi répétés pour le même propriétaire, ce qui n’est pas le même type de conflit. Chiapas comporte un sélecteur de bâtiment UCA sans territoire initial correspondant.
Références du registre à lire : MAP0-0001 | MAP0-0002 | MAP0-0003 | MAP0-0004 | MAP0-0005 | MAP0-0006 | MAP0-0007 | MAP0-0008 | MAP0-0009 | MAP0-0010 | MAP0-0011 | MAP0-0012 | MAP0-0013 | MAP0-0014 | MAP0-0015 | MAP0-0016 | MAP0-0087 | MAP0-0095 | MAP0-0096 | MAP0-0097 | MAP0-0098 | MAP0-0099 | MAP0-0100 | MAP0-0101 | MAP0-0102 | MAP0-0103 | MAP0-0104 | MAP0-0105 | MAP0-0106 | MAP0-0107 | MAP0-0108 | MAP0-0109 | MAP0-0110 | MAP0-0183 | MAP0-0201
Un conflit de syntaxe ou de fichier n’est pas une preuve historique. Le candidat georg3mx n’est pas fusionné dans main; la baseline représente main actuel.

FORMES DE SOUVERAINETÉ ET DIFFICULTÉS : Colonies, rébellion et administrations britanniques, compagnies de commerce, forts et revendications à faible contrôle, souverainetés autochtones, alliances/confédérations, frontières espagnoles. Ne pas projeter l’indépendance de juillet 1776 sur le 1er janvier ni les futurs traités sur les souverainetés présentes.
PRIORITÉS : Priorité : colonies américaines au jour exact, Louisiane, frontières canadiennes/HBC, Alaska, Nord-Ouest et nations autochtones, Mexique et Caraïbes. Coordonner l’isthme avec R9; ne pas valider l’extension HBC par son seul TAG.

Pour chaque territoire, distinguer administration directe, occupation militaire peu administrée, dépendance/vassalité, protectorat/tribut/influence, compagnie à autorité territoriale, autonomie/souveraineté autochtone, revendication seule, contrôle disputé ou fluctuant, et zone sans frontière précise défendable. Examiner présence administrative, fiscalité, juridiction, garnisons, fortifications, implantations permanentes, traités et structures politiques locales. Un comptoir n’équivaut pas à souveraineté sur toute une State Region. Dater séparément les changements survenus après le 1er janvier, même dans l’année 1776.

SOURCES : atlas historiques argumentés, travaux universitaires spécialisés, traités/documents administratifs contemporains, cartes d’époque avec date et biais, travaux sur les souverainetés locales et autochtones. Pour chaque correction importante, cite au moins une preuve précise. Fournis auteur, titre, date, URL ou référence bibliographique, pages/cartes pertinentes; une URL seule ou une carte moderne non justifiée ne suffit pas. Signale les contradictions et compare la nature des preuves; ne tranche pas silencieusement.

LIVRABLES : R8_NORTH_AMERICA_CARIBBEAN_RECOMMENDATIONS.csv conforme à toutes les colonnes et valeurs contrôlées du schéma joint; R8_NORTH_AMERICA_CARIBBEAN_SOURCES.csv; R8_NORTH_AMERICA_CARIBBEAN_UNCERTAINTIES.md; R8_NORTH_AMERICA_CARIBBEAN_COVERAGE.csv avec une ligne pour chaque couple listé, y compris REVIEWED_NO_CHANGE. Cartes annotées facultatives mais utiles. Chaque changement doit distinguer conclusion historique, correspondance géographique proposée, approximation de gameplay et incertitude non résolue.

Si tu ne peux pas faire correspondre une frontière aux provinces du jeu, laisse Province_ID/Province_IDs vides, utilise Mapping_Status=MAPPING_REQUIRED et décris précisément la zone (toponymes, coordonnées, limites, carte/page). N’invente aucun ID ni nouveau TAG. Préfère A_EXISTING_PROVINCES, puis B_STATE_REGIONS; ne demande C_GEOMETRY qu’avec preuve que les provinces existantes sont insuffisantes. Indique Requires_New_Tag et Requires_State_Split sans créer l’entité.

INCERTITUDES ET TRANSMISSION : attribue Change_ID stable, Source_IDs vérifiables et Confidence justifiée. Toute contradiction reste UNRESOLVED; renseigne Cross_Region_Conflict et Secondary_Region_ID, décris les sources opposées et transmets à la synthèse centrale. L’interlocuteur secondaire relit l’interface mais ne duplique pas ta recommandation. Une nouvelle zone extérieure au périmètre est signalée OUTSIDE_BASELINE pour attribution centrale, pas annexée à ta mission. VEN et GEN sont recherchés normalement mais leurs historiques particuliers de population/bâtiments sont protégés. Ne redistribue pas ces données. Aucun résultat n’est automatiquement intégré.

LISTE EXHAUSTIVE DES ÉTATS ET PROPRIÉTAIRES ACTUELS À AUDITER :
STATE_ALABAMA : COM
STATE_ALASKA : ALK | ATB
STATE_ALBERTA : BLF | IRC
STATE_ARIZONA : APC | NVJ
STATE_ARKANSAS : COM
STATE_BAHAMAS : GBR
STATE_BAJA_CALIFORNIA : SC1
STATE_BAJIO : SC1
STATE_BERMUDA : GBR
STATE_BRITISH_COLUMBIA : ATB
STATE_CALIFORNIA : APC
STATE_CENTRAL_CUBA : CUB
STATE_CHIAPAS : SC1
STATE_CHIHUAHUA : SC1
STATE_COLORADO : ARP | UTE
STATE_CONNECTICUT : USA
STATE_COSTA_RICA : SC1
STATE_DELAWARE : USA
STATE_DISTRICT_OF_COLUMBIA : USA
STATE_DURANGO : SC1
STATE_EASTERN_CUBA : CUB
STATE_FLORIDA : GBR | SML
STATE_GEORGIA : USA
STATE_GREENLAND : DENNOR | GR7
STATE_GUATEMALA : GBR | SC1
STATE_GUERRERO : SC1
STATE_HAITI : HAI
STATE_HONDURAS : SC1
STATE_IDAHO : BNN | NZP
STATE_ILLINOIS : MICC
STATE_INDIANA : MICC
STATE_IOWA : LKT
STATE_JALISCO : SC1
STATE_JAMAICA : GBR
STATE_KANSAS : COM | PWN
STATE_KENTUCKY : COM
STATE_LOUISIANA : LOU
STATE_MAINE : USA
STATE_MANITOBA : HBC | IRC
STATE_MARYLAND : USA
STATE_MASSACHUSETTS : USA
STATE_MEXICO : SC1
STATE_MICHIGAN : MICC
STATE_MINNESOTA : LKT
STATE_MISSISSIPPI : COM
STATE_MISSOURI : COM
STATE_MONTANA : ABS | BLF | LKT | SLS
STATE_NEBRASKA : LKT | PWN
STATE_NEVADA : BNN
STATE_NEWFOUNDLAND : GBR
STATE_NEW_BRUNSWICK : NBS | NVS
STATE_NEW_HAMPSHIRE : USA
STATE_NEW_JERSEY : USA
STATE_NEW_MEXICO : APC | COM | NVJ | SC1
STATE_NEW_YORK : USA
STATE_NICARAGUA : MKT | SC1
STATE_NORTHWEST_TERRITORIES : ATB
STATE_NORTH_CAROLINA : USA
STATE_NORTH_DAKOTA : LKT
STATE_NUNAVUT : HBC
STATE_OAXACA : SC1
STATE_OHIO : MICC
STATE_OKLAHOMA : COM
STATE_ONTARIO : HBC | ONT
STATE_OREGON : ATB
STATE_PANAMA : SC2
STATE_PENNSYLVANIA : USA
STATE_PUERTO_RICO : PCO
STATE_QUEBEC : HBC | QUE
STATE_RHODE_ISLAND : USA
STATE_RIO_GRANDE : SC1
STATE_SANTO_DOMINGO : GR5
STATE_SAN_SALVADOR : SC1
STATE_SASKATCHEWAN : HBC | IRC
STATE_SINALOA : SC1
STATE_SONORA : SC1
STATE_SOUTH_CAROLINA : USA
STATE_SOUTH_DAKOTA : LKT
STATE_TENNESSEE : COM
STATE_TEXAS : COM | SC1
STATE_UTAH : NVJ | UTE
STATE_VERACRUZ : SC1
STATE_VERMONT : USA
STATE_VIRGINIA : USA
STATE_WASHINGTON : ATB
STATE_WESTERN_CUBA : CUB
STATE_WEST_INDIES : DENNOR | FRA | GBR | NET | SPA
STATE_WEST_VIRGINIA : USA
STATE_WISCONSIN : MICC
STATE_WYOMING : ABS | ARP | BNN | LKT | SLS
STATE_YUCATAN : SC1
STATE_YUKON_TERRITORY : ATB
STATE_ZACATECAS : SC1
```


## R9_SOUTH_AMERICA

```text
Mission autonome : R9_SOUTH_AMERICA — Amérique du Sud

Tu es responsable de la recherche territoriale au 1er janvier 1776 (1776-01-01) pour le mod Victoria 3 « 1776 Age of Revolutions ». Tu recherches, tu ne modifies ni fichiers historiques ni carte, et tu ne pousses aucun changement. Les valeurs initiales du mod et les noms de TAGs ne sont pas des conclusions historiques.

PIÈCES À RECEVOIR : MAP_1776_BASELINE.csv, MAP_1776_9_REGIONS.csv, MAP_1776_RESEARCH_SCHEMA.md, MAP_1776_KNOWN_ISSUES.csv. Utilise uniquement les lignes Region_ID=R9_SOUTH_AMERICA comme périmètre principal. Les IDs RGB sont ceux du bitmap du jeu, pas des numéros arbitraires. Les lignes d’un même State_ID avec plusieurs Owner_TAG restent distinctes.

PÉRIMÈTRE : Amérique du Sud et îles attribuées à ses State_IDs, Guyanes, bassins amazoniens, Andes, Brésil, cône Sud et Patagonie; l’Amérique centrale appartient à R8.
L’inventaire comprend 63 couples pays/État et 53 State_IDs distincts. TAGs existants à auditer dans ce seul périmètre : AP7, BRZ, FRA, GBR, GNI, IQU, NET, PAT, SC2, SC3, SC4, SLK, THL.
Interlocuteurs secondaires prévus : aucun prédéfini; signaler toute interface découverte. Une métropole qui possède ailleurs ne t’attribue pas ces territoires. Les mers et lacs sont une référence technique, pas des territoires politiques à attribuer à un pays.

PROBLÈMES DÉJÀ OBSERVÉS : STATE_PASTAZA référence un bâtiment region_state:SC2 sans territoire correspondant au départ. Les TAGs BRZ, SC2/SC3/SC4 et les autres noms du scénario ne sont pas une preuve d’indépendance historique : rechercher l’autorité et représenter séparément les dépendances.
Références du registre à lire : MAP0-0017 | MAP0-0088 | MAP0-0111 | MAP0-0184
Un conflit de syntaxe ou de fichier n’est pas une preuve historique. Le candidat georg3mx n’est pas fusionné dans main; la baseline représente main actuel.

FORMES DE SOUVERAINETÉ ET DIFFICULTÉS : Administration ibérique, capitaineries et juridictions, missions, implantation fluviale, souverainetés autochtones, zones de revendication et traités contestés. Comparer frontières de droit, présence permanente et souveraineté locale; une carte coloniale peut représenter une prétention plutôt qu’un contrôle.
PRIORITÉS : Priorité : frontière luso-espagnole au 1er janvier, Guyanes, Amazonie, Andes et intérieur, Patagonie et contrôles locaux. Ne pas utiliser une division administrative créée plus tard en 1776 comme état initial; coordonner l’isthme avec R8.

Pour chaque territoire, distinguer administration directe, occupation militaire peu administrée, dépendance/vassalité, protectorat/tribut/influence, compagnie à autorité territoriale, autonomie/souveraineté autochtone, revendication seule, contrôle disputé ou fluctuant, et zone sans frontière précise défendable. Examiner présence administrative, fiscalité, juridiction, garnisons, fortifications, implantations permanentes, traités et structures politiques locales. Un comptoir n’équivaut pas à souveraineté sur toute une State Region. Dater séparément les changements survenus après le 1er janvier, même dans l’année 1776.

SOURCES : atlas historiques argumentés, travaux universitaires spécialisés, traités/documents administratifs contemporains, cartes d’époque avec date et biais, travaux sur les souverainetés locales et autochtones. Pour chaque correction importante, cite au moins une preuve précise. Fournis auteur, titre, date, URL ou référence bibliographique, pages/cartes pertinentes; une URL seule ou une carte moderne non justifiée ne suffit pas. Signale les contradictions et compare la nature des preuves; ne tranche pas silencieusement.

LIVRABLES : R9_SOUTH_AMERICA_RECOMMENDATIONS.csv conforme à toutes les colonnes et valeurs contrôlées du schéma joint; R9_SOUTH_AMERICA_SOURCES.csv; R9_SOUTH_AMERICA_UNCERTAINTIES.md; R9_SOUTH_AMERICA_COVERAGE.csv avec une ligne pour chaque couple listé, y compris REVIEWED_NO_CHANGE. Cartes annotées facultatives mais utiles. Chaque changement doit distinguer conclusion historique, correspondance géographique proposée, approximation de gameplay et incertitude non résolue.

Si tu ne peux pas faire correspondre une frontière aux provinces du jeu, laisse Province_ID/Province_IDs vides, utilise Mapping_Status=MAPPING_REQUIRED et décris précisément la zone (toponymes, coordonnées, limites, carte/page). N’invente aucun ID ni nouveau TAG. Préfère A_EXISTING_PROVINCES, puis B_STATE_REGIONS; ne demande C_GEOMETRY qu’avec preuve que les provinces existantes sont insuffisantes. Indique Requires_New_Tag et Requires_State_Split sans créer l’entité.

INCERTITUDES ET TRANSMISSION : attribue Change_ID stable, Source_IDs vérifiables et Confidence justifiée. Toute contradiction reste UNRESOLVED; renseigne Cross_Region_Conflict et Secondary_Region_ID, décris les sources opposées et transmets à la synthèse centrale. L’interlocuteur secondaire relit l’interface mais ne duplique pas ta recommandation. Une nouvelle zone extérieure au périmètre est signalée OUTSIDE_BASELINE pour attribution centrale, pas annexée à ta mission. VEN et GEN sont recherchés normalement mais leurs historiques particuliers de population/bâtiments sont protégés. Ne redistribue pas ces données. Aucun résultat n’est automatiquement intégré.

LISTE EXHAUSTIVE DES ÉTATS ET PROPRIÉTAIRES ACTUELS À AUDITER :
STATE_ACRE : AP7
STATE_ALTO_PARAGUAY : GNI
STATE_AMAZONAS : AP7
STATE_ANTIOQUIA : SC2
STATE_ANTOFAGASTA : SC3
STATE_ARAUCANIA : SC3 | SLK | THL
STATE_AREQUIPA : SC3
STATE_BAHIA : BRZ
STATE_BAJO_PARAGUAY : SC4
STATE_BOLIVAR : SC2
STATE_BUENOS_AIRES : PAT | SC4
STATE_CAJAMARCA : SC3
STATE_CAUCA : SC2
STATE_CEARA : BRZ
STATE_CHACO : GNI | SC4
STATE_CORRIENTES : SC4
STATE_CUNDINAMARCA : SC2
STATE_ECUADOR : SC2
STATE_GOIAS : BRZ
STATE_GUAVIARE : SC2
STATE_GUAYANA : AP7 | FRA | NET
STATE_ICA : IQU | SC3
STATE_JUJUY : SC4
STATE_LA_PAMPA : SC4
STATE_LA_PAZ : AP7
STATE_LIMA : SC3
STATE_LOS_RIOS : SC3
STATE_MARANHAO : BRZ
STATE_MATO_GROSSO : AP7
STATE_MINAS_GERAIS : BRZ
STATE_MIRANDA : SC2
STATE_PARA : BRZ
STATE_PARAIBA : BRZ
STATE_PARANA : BRZ
STATE_PASTAZA : SC3
STATE_PATAGONIA : PAT | THL
STATE_PERNAMBUCO : BRZ
STATE_PIAUI : BRZ
STATE_POTOSI : SC3
STATE_RIO_DE_JANEIRO : BRZ
STATE_RIO_GRANDE_DO_NORTE : BRZ
STATE_RIO_GRANDE_DO_SUL : BRZ
STATE_RIO_NEGRO : PAT | SC4
STATE_SANTA_CATARINA : BRZ
STATE_SANTA_CRUZ : SC3
STATE_SANTA_FE : GNI | SC4
STATE_SANTIAGO : SC3
STATE_SAO_PAULO : BRZ
STATE_SOUTH_ATLANTIC_ISLANDS : GBR
STATE_TARAPACA : SC3
STATE_TUCUMAN : SC4
STATE_URUGUAY : SC4
STATE_ZULIA : SC2
```
