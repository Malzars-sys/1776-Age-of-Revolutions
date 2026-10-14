# R2 — UNCERTAINTIES / Transmission centrale

**Date historique recherchée : 1776-01-01.** Contrat MAP-0/1 du 2026-10-10. **Audit partiel, non prêt à intégrer automatiquement.** Date de consultation des sources : 2026-10-10. Aucun fichier historique, carte ni dépôt Git n'a été modifié.

## Contrôle de couverture et limites

- Couples uniques dans `MAP_1776_9_REGIONS(2).csv` avec `Region_ID=R2_NORTHERN_CENTRAL_EASTERN_EUROPE` : **164**, State_ID distincts : **136**, TAGs distincts : **45**.
- Le CSV COVERAGE comporte exactement une ligne par couple ; **REVIEWED_NO_CHANGE=24**, **CHANGE_PROPOSED=11**, **UNRESOLVED=129**.
- **165** fiches de recommandation couvrent les **164 couples** (certaines propriétés ont plusieurs fiches en raison d'un partage). Elles référencent **45** entrées bibliographiques. **Aucun couple n'est omis**, MAIS de nombreuses fiches sont seulement un *criblage macro-historique* à confiance LOW : elles demeurent `UNRESOLVED` et la couverture ne signifie pas validation du territoire.
- **Aucun Province_ID n'est certifié historiquement.** L'inventaire fournit des RGB bitmap et du découpage actuel, **pas une table toponymique de ces RGB**. Pour toute modification frontalière, `Province_ID` et `Province_IDs` sont laissés vides avec `Mapping_Status=MAPPING_REQUIRED`. Les autres champs PROPOSED portent sur le statut ou sur des constats macro-historiques, pas sur une validation de géométrie.
- Une ligne du registre d'anomalies est un constat de code : elle ne démontre pas un souverain de 1776. Les données géographiques du bitmap et les attributions de `create_state` peuvent diverger.
- Source `R2_NORTHERN_CENTRAL_EASTERN_EUROPE-SRC-0016` (atlas 1780, édition 1903) est **postérieure de quatre ans** et insuffisante pour conclure seule sur les micro-enclaves de 1776. Des recommandations à confiance LOW s'appuient sur cette vue d'ensemble uniquement et **ne valent pas validation**.

## Points bloquants par priorité

### P0 — Haute/Basse Silésie, MORAVIA et WEST_GALICIA

- **R2_NORTHERN_CENTRAL_EASTERN_EUROPE-0001 / -0002** : la partition austro-prussienne de 1742 est confirmée après 1763 (SRC-0001, Kuzio-Podrucki 2022, pp. 9–23). La Silésie dite autrichienne ne se réduit pas à une ligne droite dans le jeu : Opava/Troppau, Cieszyn/Teschen, Krnov/Jägerndorf. Attribution à la Prusse sans comparaison topographique non justifiée.
- **`x71E080` et `xF0E080`** : `MAP_1776_BASELINE` donne `State_ID=STATE_MORAVIA`, `Ownership_History_State_IDs=STATE_UPPER_SILESIA`, et `Current_Province_Owners=AUS|PRU`; doublon de propriétaire dans les écritures d'histoire. Le groupe d'anomalies **MAP0-0054 à -0059** se répète sous **MAP0-0149 à -0154**. Il faut corriger à la synthèse technique le mapping State_ID et le chevauchement, **sans trancher l'histoire depuis ces fichiers**.
- **`x9061E0`** : `State_ID=STATE_WEST_GALICIA`, `Ownership_History_State_IDs=STATE_UPPER_SILESIA`, propriétaire AUS dans la baseline; **MAP0-0060** puis **MAP0-0155**. Aucune raison de déduire qu'il s'agit géographiquement de Haute-Silésie sans superposition du bitmap.
- Basse-Silésie : noyau prussien attesté, mais vérifier enclaves/duchés et raccordement entre State Regions (recommandation -0003).

### P0 — Bukovine, Bessarabie, Dobroudja

- **Bukovine** : SRC-0003 (Ungureanu 2026, pp.49–72) et SRC-0004 (Welisch 1990, pp.16–19). Occupation autrichienne de 1774; conventions d'Istanbul des **7 et 12 mai 1775**; **frontière encore en commission au 1er janvier 1776**. La convention de Balamutca/Palamutka **2 juillet 1776** n'est pas rétroactive. Vérifier villages du raya de Hotin restitués ensuite (recommandation associée à STATE_BUKOVINA).
- **Bessarabie** : l'ensemble `MOL` n'est pas équivalent à une Moldavie administrée d'un seul tenant. Traité 1774 art.16 mentionne forteresses/rayas séparés et Budjak. Tracer Hotin, Tighina/Bender, Akkerman, Kili, Ismail et pâturages tatars; **R3 consulte l'interface**. Les désaccords MAP0-0187–0188 comparent catalogue historique du mod et MAIN, pas le candidat non fusionné. **MAP0-0090 à MAP0-0094** sont les jetons parasites `git`, `status`, `fetch`, `origin`, uniquement syntaxiques (aucune signification territoriale).
- **Dobroudja** : la carte Janvier datée 1750 par la Library of Congress (SRC-0024, Library of Congress, carte) et les arrangements de 1774 soutiennent une souveraineté ottomane générale. **MAP0-0189** est une divergence catalogue initial/MAIN mentionnant RUS, non une preuve; préserver les forteresses/ports réels et distinguer delta du Danube.

### P1 — Crimée et mer Noire

- SRC-0005, -0006, -0007, -0026 et -0031: khanat indépendant de jure dès le traité de Küçük Kaynarca du **21 juillet 1774**, sous forte influence russe; **annexion russe le 19 avril 1783**, sans anticiper. Forteresses russes **Kerch et Yeni-Kale** et exception Kinburn; **Ochakiv/Otchakov** reste une place ottomane, non incluse indistinctement dans le khanat. La steppe de STATE_CHERSON peut chevaucher plusieurs dominations. Les forteresses ne justifient jamais l'annexion de toute la State Region.
- La politique de Şahin Giray débute en **1777** ; pas de projection comme souverain de 1776. Les approches russes et ottomanes peuvent diverger sur de jure, présence de soldats et influence ; cette incertitude reste documentée.

### P1 — Première partition de Pologne et régions germaniques

- SRC-0002 : première partition 1772 (ratification 1773), **Danzig/Gdańsk et Thorn/Toruń restent polonaises jusqu'en 1793**, contrairement aux autres principales terres de Prusse royale. Territoires du district de Netze/Noteć prennent le chemin de Prusse. **Galicie d'après 1772** habsbourgeoise ; les nouvelles conquêtes de **Galicie occidentale de 1795** sont absentes en 1776. L'appellation State_ID n'est pas une raison d'appliquer les frontières de 1795.
- Courlande : SRC-0018, duché de **Peter von Biron** (1769–1795), sous suzeraineté de Pologne-Lituanie, pas province directe; distinguer Piltene/Pilten du duché et représenter vassalité. Russie n'annexe qu'en 1795.
- Riga/Tallinn/Tartu : SRC-0017, Bartlett 1993, pp.233–236. Après capitulations 1710 et traité de Nystad 1721, souveraineté russe **avec droits corporatifs des chevaleries**; `UBD` ne prouve pas une souveraineté balte indépendante. Le partage graphique UBD/RUS exige une décision d'architecture des sujets.
- **Rhineland BAV** : le Palatinat reste gouverné par Charles-Théodore et n'est uni à la Bavière qu'à la mort de Maximilien III le **30 décembre 1777** (SRC-0019 et -0020); une correction géographique est nécessaire uniquement si les 2 RGB BAV correspondent bien au Palatinat.
- **Franconia BAV** : administrations multiples, margraviats Ansbach/Bayreuth, principautés ecclésiastiques et villes libres. Réunion simplifiée sous BAV suspecte. L'atlas de **1780** ne donne pas de preuve parcellaire suffisante en 1776 : recommandation à faire confirmer, pas d'assignation arbitraire.
- **Banat / Temeswar** : SRC-0033 (Kulcsár, Archives nationales hongroises, 2010), administration habsbourgeoise distincte en **1776**, **réincorporation civile à la Hongrie seulement en 1778**. `STATE_BANAT:HUN` nécessite donc correction ciblée vers AUS / Frontière militaire après géoréférencement; ne pas appliquer la situation 1778 à 1776.
- **Croatie/Slavonie** : SRC-0034/-0035 (Lazanin 2024 pp.277–308, Radošević 2019 pp.93–128) séparent comitats civils, privilèges locaux et Frontière militaire dirigée depuis Vienne. Aucun découpage RGB militaire attesté à ce stade.
- **Poméranie suédoise et Wismar** : la zone Stralsund/Greifswald/Rügen demeure suédoise (SRC-0010 à -0012); l’enclave **Wismar, Poel, Neukloster** demeure suédoise en 1776 : la convention originale de Malmö de 1803 (SRC-0045, art. XVII) acte sa remise en gage ultérieure à Mecklenburg. Les deux nécessitent isolation de provinces SWE à l’intérieur de groupes initialement PRU/MEC.
- **Schleswig/Holstein** : échange de 1773 (SRC-0013); Christian VII est le duc des deux territoires en 1776. Holstein demeure partie du Saint-Empire, Schleswig relevant de couronne danoise. **Hochstift Lübeck/Eutin** est une entité territoriale distincte de la ville libre de Lübeck (SRC-0015). La présence d'un TAG LUB n'autorise pas à les fusionner.
- **Hambourg, Brême et Lübeck** : cités impériales libres en 1776 (SRC-0014), mais leurs possessions autour des villes sont à distinguer des duchés et juridictions ecclésiastiques.

### P1 — Balkans et frontières des sujets

- Moldavie/Valachie : SRC-0008 (Oncescu 2018 pp.97–104), SRC-0009 (Zane 1976 pp.323–355), SRC-0006 traité 1774 : principe de **tribut, suzeraineté ottomane et gouvernement intérieur princier**; ne pas convertir en pashaliks directs.
- Monténégro : institutions des **vladikas et clans montagneux**, villes/forteresses ottomanes et baies vénitiennes, limites mouvantes. Les conclusions d'une carte étatique ottomane de 1750 ne doivent pas être appliquées comme contrôle militaire exact sur les hauteurs.
- Les 16 State Regions ottomanes complémentaires ont un **premier repérage macroscopique seulement**, d'après Janvier (SRC-0024, carte datée 1750 par la Library of Congress) ; il manque fiscalité, cadis, garnisons et frontières de chaque district. La carrière rebelle de Pazvantoğlu et la recentralisation de Selim III sont **postérieures** et n'expliquent pas directement 1776. Ne pas marquer une confirmation totale.

### P2 — Marges nordiques et Russie européenne

- Russie, Nenetsia/Kola/Ural/Tartaria: carte Treskot/Schmidt de 1776 (SRC-0032, Library of Congress, G7000 1776 .T7), source d’époque utile pour les prétentions et toponymes mais non pour le contrôle administratif réel. Absence de frontière continue défendable sur de grandes régions de toundra, taïga et pâturage; les autorités locales et forteresses doivent être situées, pas extrapolées du TAG RUS.
- Kalmoukie : SRC-0021, Maksimov 2008 pp.121–198 : l'exode et abolition du khanat **1771**, administration impériale via gouverneur d'Astrakhan et ulus restant avec autorités propres. Ne pas réintroduire le khanat politiquement en 1776.
- Samara KZH : SRC-0022 Campbell 2017 pp.13–30. Les allégeances/protections de 1731 ne prouvent pas une domination russe administrée sur toutes les estives kazakhes. R3 décide interface steppes asiatiques; R5 seulement la limite de Sibérie. Décrire les forts individuellement.
- Scandinavie et Finlande : SRC-0040 (Merovuo 2017, traité d'Åbo 1743) et SRC-0041 (Agence finlandaise du patrimoine, fortifications de Kymijoki) documentent le recul de la frontière suédo-russe et sa matérialisation par postes. Le tracé du jeu n'a PAS été superposé; les fortifications postérieures à 1776 citées dans les notices ne doivent pas être rétroprojetées. Les terres d'usage sâme restent à étudier; plusieurs couples restent UNRESOLVED.

## Notes techniques du registre d'anomalies

IDs explicitement relus : MAP0-0054, MAP0-0055, MAP0-0056, MAP0-0057, MAP0-0058, MAP0-0059, MAP0-0060, MAP0-0078, MAP0-0083, MAP0-0090, MAP0-0091, MAP0-0092, MAP0-0093, MAP0-0094, MAP0-0149, MAP0-0150, MAP0-0151, MAP0-0152, MAP0-0153, MAP0-0154, MAP0-0155, MAP0-0173, MAP0-0179, MAP0-0187, MAP0-0188, MAP0-0189, MAP0-0190, MAP0-0193, MAP0-0204.

- **MAP0-0078 = MAP0-0173** : capitale PLC en `STATE_WEST_GALICIA` non possédée ; anomalie de capital, non preuve de propriétaire historique.
- **MAP0-0083 = MAP0-0179** : `buildings / RUS` orphelin à `STATE_BREST` ; ne pas créer territoire russe sur cette base.
- **MAP0-0190 / -0193 / -0204** : écarts catalogue initial/MAIN pour Suisse orientale, Istrie, Tyrol du Sud; ils demandent inspection technique et accords avec R1, non inférence souveraine.
- `georg3mx` est un candidat non fusionné ; **les quatre pièces fournies reflètent le main actuel** et ne documentent pas son état final. Aucune opération Git n'a été faite ici.
- Les possessions **VEN/GEN** peuvent être auditées historiquement, mais **population et bâtiments spécifiques restent protégés**. La recherche R2 n'a déplacé aucune donnée.

## Contradictions à transmettre telles quelles

| Sujet | Preuve A | Preuve B / limite | Décision |
|---|---|---|---|
| Silésie deux RGB | Actes de 1742 et 1763 = partition prusso-autrichienne (SRC-0001) | fichiers `MORAVIA`/`UPPER_SILESIA` et doublon AUS-PRU n'ont pas de toponymes | **UNRESOLVED**, géoréférencer bitmap et restituer la frontière des duchés |
| Bukovine | conventions de mai 1775 (SRC-0003) | frontière définitive seulement juillet 1776 | **UNRESOLVED** dans la bande de Hotin pour le 01/01 |
| Bessarabie | rayas de la Porte et Moldavie autonome (SRC-0006/0008) | 14 RGB MOL non localisés; statut du Budjak mobile | **UNRESOLVED** jusqu'à analyse de forts, fiscalité, frontières |
| Crimée | indépendance de jure du khanat (SRC-0005/0006) | garnisons, forteresses et intervention russes (SRC-0026/0031) | **UNRESOLVED** sur certaines forteresses, distinguer contrôle physique et droit |
| Courlande | fief du souverain de Pologne-Lituanie (SRC-0018) | gouvernement ducal autonome et influence russe | **SUBJECT proposé**, pas PLC direct, tracé encore requis |
| Baltique `UBD` | autonomie juridique nobiliaire (SRC-0017) | souveraineté extérieure incontestablement russe dans la même source | Réviser modèle de souveraineté, **ne pas prendre autonomie pour État souverain** |
| Poméranie | administration suédoise Greifswald/Stralsund (SRC-0010 à -0012) | baseline POMERANIA ne comprend que PRU | **MAPPING_REQUIRED**, isoler territoire suédois sans inventer des RGB |
| Banat au 01/01/1776 | Archives hongroises SRC-0033: incorporation seulement 1778 | TAG initial HUN + frontière militaire probable; pas de table RGB | **CHANGE_PROPOSED AUS**, localisation et répartition civile/militaire non résolues |
| Wismar | Convention de Malmö 1803 SRC-0045 reconnaît Wismar Poel Neukloster comme suédois avant gage | le catalogue MECKLENBURG ne montre que MEC/MST | **CHANGE_PROPOSED SWE**, localiser zones précises |
| Allemagne 1780 | atlas de 1780 détaille États | date cible 1776; nombreuses micro-annexions possibles | **UNRESOLVED** sauf sources 1776 précises |

## OUTSIDE_BASELINE / transmission inter-régionale

Cette section ne crée ni State_ID ni RGB et ne recommande aucun territoire hors mission :

1. **Poméranie suédoise dans STATE_POMERANIA** : la provenance des RGB ne recense que PRU, mais Greifswald, Stralsund, Rügen/partie nord de Vorpommern étaient suédois en 1776 (SRC-0010 à -0012). Ce cas est une **propriété absente** du couple initial, pas un nouveau State_ID. À cartographier avant tout changement et à relier à la synthèse centrale.
2. **Wismar suédoise dans STATE_MECKLENBURG** : ville, île de Poel et Neukloster sous suzeraineté suédoise en 1776, même si le catalogue ne recense que MEC et MST ; source primaire rétroactive SRC-0045, convention 1803. L'absence de SWE dans ce State_ID est un problème de couverture d'owner et non un nouveau State_ID.
3. **Khanat de Crimée / littoral de la mer Noire** : forteresses Kerch, Yeni-Kale, Kinburn, Ochakiv et limites des groupes Nogaïs : partage d'expertise **R3**. R3 ne duplique pas la recommandation R2.
4. **Petite Horde kazakhe et versants asiatiques** : espaces nomades dépassant la Russie européenne : **R3** pour les steppes d'Asie centrale, **R5** pour bord sibérien. Ne pas prolonger les tracés européens.
5. **Istrie, Trentin/Tyrol méridional, ports vénitiens du Monténégro** : interface **R1**, sans second chef pour les mêmes couples.

## Tâches avant intégration

1. Obtenir table `xRRGGBB → carte avec toponyme / coordonnées`, géoréférencer état géographique et superposer cartes de 1776 ; traiter x71E080/xF0E080/x9061E0 en premier.
2. Pour les couples sans recherche individualisée dans COVERAGE, produire preuves ponctuelles datées (actes, fiscalité, unités judiciaires, garnisons, traité, carte d'époque) ; statut actuel UNRESOLVED **ne vaut pas absence de changement**.
3. Examiner archives et cartes des limites de l'Istrie, du Tyrol, de Silésie autrichienne et des forteresses bessarabiennes; distinguer l'état au 1776-01-01 des conventions intervenues plus tard dans l'année.
4. Validation de la synthèse centrale des changements de sujets/TAGs, capitaux, population, bâtiments et forts; **méthode A puis B ; C seulement après preuve d'impossibilité**.
