# R8_NORTH_AMERICA_CARIBBEAN — INCERTITUDES, ARBITRAGES ET TRANSMISSION MAP-0

**État documentaire : 2026-10-10 — date historique de référence : 1776-01-01.** Recherche territoriale uniquement : aucun fichier de la carte, de population ou de bâtiments du mod n’a été modifié et aucune opération Git n’a été effectuée. Le candidat `georg3mx` n’est pas fusionné; les relevés marqués `COLLABORATOR_CANDIDATE` sont comparatifs et **non** la baseline active.

## 1. Couverture, méthode et limites de preuve
- **125 couples** State_ID × Owner_TAG audités, **93 State_ID distincts**, 50 notices bibliographiques, 125 Change_ID propres au périmètre. Couverture par statut : `REVIEWED_NO_CHANGE` = 25, `CHANGE_PROPOSED` = 28, `UNRESOLVED` = 72.
- **Aucune correction n’est intégrable géométriquement en l’état :** les 125 recommandations portent `Mapping_Status=MAPPING_REQUIRED`, et les colonnes `Province_ID` et `Province_IDs` sont vides. Les IDs RGB qui apparaissent dans **ce document** proviennent exclusivement du registre technique et ne sont jamais utilisés comme attribution politique validée.
- Méthode de travail : comparaison de la forme juridique (actes, chartes, traités), des présences mesurables (gouverneurs, missions, cabildos, présidios, forts, postes), des autorités politiques autochtones et des cartographies contemporaines. Un droit colonial allégué, une relation diplomatique ou une route commerciale ne valent **pas** preuve d’administration effective de toutes les terres environnantes.
- Le champ `Confidence` évalue la **thèse historique résumée**, pas le niveau de certitude du transfert RGB; l’incertitude de la carte demeure explicite. Une confiance `HIGH` peut donc coexister avec `MAPPING_REQUIRED`. Les statuts `REVIEWED_NO_CHANGE` conservent uniquement l’affiliation ou la situation institutionnelle défendable; ils ne valident pas chaque province du jeu.
- Les recommandations `NEW_TAG_REQUIRED` signalent des entités autochtones distinctes nécessaires à une représentation plus fidèle, mais ne créent **aucun** TAG. Les splits `YES` sont des besoins de modélisation, pas une preuve que chaque province existante peut isoler les acteurs. Ordre technique **A** provinces existantes, puis **B** State Regions; **C** géométrie non demandée à ce stade.
- Les arguments de type « carte impériale de 1775 » valent d’abord comme preuve de **revendications contemporaines**. Pour les territoires autochtones, un point administratif ou un traité seul ne permet pas d’en déduire une frontière continue. Les sources généralistes présentes dans le fichier SOURCES n’impliquent aucune localisation fine, laquelle est délibérément `UNRESOLVED`.

## 2. Priorités d’arbitrage historico-géographique

### Treize colonies, rupture progressive — `R8_NORTH_AMERICA_CARIBBEAN-0020`
La déclaration du 4 juillet 1776 est ultérieure, même si l’insurrection s’étend dès 1775. USA figure déjà comme colonie de GBR dans la baseline : le problème résiduel est la géographie des pouvoirs révolutionnaires, des garnisons britanniques et des souverainetés autochtones. Boston reste britannique jusqu’au 17 mars 1776; la prise de New York par les Britanniques survient plus tard. Les territoires aujourd’hui appelés Maine, West Virginia et District of Columbia ne sont pas des États distincts en 1776.
**Preuve, limites et contrôle contradictoire :** Archives nationales américaines S001; NPS S002; proclamation royale 1763 S003. NARA atteste la date d’adoption, non les frontières militaires locales.

### Alaska : autonomie locale vs marchands russes — `R8_NORTH_AMERICA_CARIBBEAN-0002`
Les expéditions russes post-1741 n’équivalent pas à une colonie territoriale couvrant l’Alaska. Three Saints Bay est fondée en août 1784, Russian-American Company en 1799. Les Aléoutiennes/Kodiak où passent les promyshlenniki doivent être examinées séparément de l’Alaska intérieur (ATB) et de nombreuses nations maritimes.
**Preuve, limites et contrôle contradictoire :** National Park Service S015 et Library of Congress S016; absence d’implantation coloniale générale en janvier 1776 ≠ absence de violences, de traite ou de séjours temporaires.

### Nunavut / Terre de Rupert / fort Cumberland — `R8_NORTH_AMERICA_CARIBBEAN-0079`
Le rattachement HBC déjà intégré dans main n’est **pas validé** par la seule charte de 1670. À York Factory (1684) et aux postes côtiers, la HBC possède des infrastructures; Cumberland House, Saskatchewan, est fondé en 1774, démontrant une présence localisée à l’intérieur. Les collectivités inuit, denées, cries et assiniboines ne deviennent pas des populations administrées sur l’ensemble de la zone par la charte.
**Preuve, limites et contrôle contradictoire :** Cavanagh, 2013 S011, Parks Canada S013 (section « Human history », Cumberland House 1774), S014; distinguer entreprise à charte et acteurs autochtones.

### Nouveau-Brunswick, juridiction coloniale — `R8_NORTH_AMERICA_CARIBBEAN-0065`
La création administrative du Nouveau-Brunswick date de 1784, non de 1776. Sa zone continentale relevait de Nouvelle-Écosse; `NVS` est l’équivalence institutionnelle existante. Ce transfert du tag NBS n’accorde toutefois pas à NVS les terres Wolastoqiyik et Mi’kmaq sans étude d’implantations locales.
**Preuve, limites et contrôle contradictoire :** Parks Canada S006 et Canadian Heritage S007 ; contrôle direct aux villages/forts distinct du statut juridique de toute la province moderne.

### Nord-Ouest des Grands Lacs — `R8_NORTH_AMERICA_CARIBBEAN-0081`
La vaste confédération autochtone souvent associée aux guerres du Nord-Ouest se forme plus tard; le TAG MICC aplati est anachronique s’il suppose une fédération politique unique. Le Quebec Act de 1774 élargit la juridiction coloniale sur certaines terres du bassin de l’Ohio, sans démontrer leur contrôle effectif. Shawnee, Miami, Haudenosaunee, Odawa, Ojibwe, Potawatomi et autres doivent être replacés par vallée et par fort.
**Preuve, limites et contrôle contradictoire :** Original du Quebec Act S004, analyses des conflits par NPS S022/S023; une loi sur les frontières impériales ne fait pas disparaître une souveraineté locale.

### Louisiane espagnole : aval et arrière-pays — `R8_NORTH_AMERICA_CARIBBEAN-0046`
La Louisiane est espagnole depuis la cession secrète de 1762, le transfert de pouvoir est en place depuis 1769. `LOU` dépend déjà de `SPA` dans la baseline, ce qui correspond au niveau supérieur. Nouvelle-Orléans/cabildo et forts du Mississippi ne suffisent pas pour assimiler les terres Quapaw, Osage et Caddo à des paroisses espagnoles pleinement taxées.
**Preuve, limites et contrôle contradictoire :** Library of Congress S018/S019, Encyclopedia of Arkansas S020/S021; séparer frontières impériales et juridictions autochtones.

### Nouveau-Mexique / Arizona / Californie — `R8_NORTH_AMERICA_CARIBBEAN-0072`
Spanish Santa Fe, villages du Rio Grande et présidios à maintenir, sans étendre SC1 sur toutes les montagnes/plaines. Les territoires Apache, Diné/Navajo et Comanche nécessitent une implantation localisée. Californie : San Diego/Monterey espagnols antérieurs; le Presidio de San Francisco est fondé le 27 juin 1776 et ne doit pas exister au 1 janvier. Les Provincias Internas seront formellement autorisées en mai 1776 : anachronisme de les dessiner déjà comme institution en janvier.
**Preuve, limites et contrôle contradictoire :** NPS El Camino Real S029, Anza S032, NPS Presidio SF S031, Chipman/Handbook of Texas S028; présence au poste ≠ toute la State Region.

### Texas et Florides : coexistence des souverainetés — `R8_NORTH_AMERICA_CARIBBEAN-0103`
Texas de Nouvelle-Espagne en 1776, mais garnisons espagnoles et établissements localisés (San Antonio, La Bahía) distincts de Comanchería, Caddo, Wichita et nations voisines. Florides orientale et occidentale sont britanniques depuis 1763; Floride actuelle ne reproduit pas exactement West/East Florida et les espaces seminoles restent distincts.
**Preuve, limites et contrôle contradictoire :** Donald E. Chipman S026, TSHA Comanche S027, Florida Department of State S037. Le territoire de West Florida historique déborde les frontières du State Florida moderne.

### Guatemala / Belize et côte des Mosquitos — `R8_NORTH_AMERICA_CARIBBEAN-0031`
Baymen établis dans la région du Belize, mais régime juridictionnel espagnol contesté et présence britannique d’abord centrée sur le bois et le littoral, non toute la région Guatemala. Royaume miskitu et relations avec les Britanniques représentent une diplomatie autonome; aucun protectorat uniforme sans recherche supplémentaire. Les traités hispano-britanniques de 1783 et 1786 **ne s’appliquent pas** au 1 janvier 1776.
**Preuve, limites et contrôle contradictoire :** Ben Fuggle S039; Caroline A. Williams S040; Claudia García S041; Stephen Webre S042. Thèses/abstracts insuffisants pour frontière RGB.

### Saint-Domingue, Florides et Antilles — `R8_NORTH_AMERICA_CARIBBEAN-0034`
Saint-Domingue occidental est français, Santo Domingo oriental espagnol; Haïti n’existe pas comme État indépendant avant 1804. L’accord frontalier du 29 février 1776, le procès-verbal du 28 août 1776 et le traité d’Aranjuez du 3 juin 1777 sont **postérieurs** à la date cible : ne pas leur appliquer rétrospectivement les bornes. Les cinq propriétaires de WEST_INDIES sont plausibles comme puissances insulaires, mais nécessitent identification **île par île** des RGB.
**Preuve, limites et contrôle contradictoire :** Archivo Histórico Nacional / PARES, sign. ESTADO,3373,Exp.3 S044; Smithsonian S045; cartes Bowen 1775 S048 et Prockter 1762 S049 (leurs légendes exposent les prétentions impériales).

### Groenland KGH — `R8_NORTH_AMERICA_CARIBBEAN-0029`
Le 1 janvier 1776, KGH devient effectivement une administration d’État du commerce groenlandais. Colonies/dépôts situés sur la côte occidentale, et non administration directe de chaque baie de l’Arctique/Est ou de l’intérieur inuit. Les 1781/1782 structures territoriales sont ultérieures.
**Preuve, limites et contrôle contradictoire :** Marianne Jensen, Trap Grønland S017, § Dansk handel, avec date explicite du 1 janvier 1776 et § Handelsstationer.

### Isthme Panamá — interface R9 — `R8_NORTH_AMERICA_CARIBBEAN-0086`
Isthme du Panama dépendant de la monarchie espagnole via l’espace administratif de Nouvelle-Grenade, non de la seule Capitainerie générale de Guatemala ni d’un État panaméen indépendant. Le contour Darién/Chocó et la souveraineté Guna/Kuna nécessitent un relevé spécifique avec R9. La coordination n’autorise aucun double rattachement de mission.
**Preuve, limites et contrôle contradictoire :** Sources S042, cartes S048; insuffisantes pour trancher les RGB du Darién; R9 interlocuteur secondaire.

## 3. Registre technique référencé (tous les incidents transmis)

Un conflit de fichiers est une **erreur technique d’allocation**, pas une preuve de contrôle en 1776. Les incidents du candidat collaborateur ne sont pas un second vote. Toutes les références demandées sont ci-dessous, avec leur diagnostic propre.

| Incident(s) | Baseline / secteur | Nature du problème | Disposition de recherche et lien |
|---|---|---|---|
| MAP0-0001 à MAP0-0003 ; MAP0-0095 à MAP0-0097 | Alaska, RGB `x5C9007`, `x63A92C`, `xF423DB` | `ALK` et `ATB` simultanément dans les écritures; blocage sur trois provinces | `R8_NORTH_AMERICA_CARIBBEAN-0002` et `R8_NORTH_AMERICA_CARIBBEAN-0003`; **UNRESOLVED** pour leur attribution RGB: localisation historique de chaque polygon manquante |
| MAP0-0004 ; MAP0-0098 | Yukon, `x26A0BA` | `ATB|ATB`: répétition du **même** propriétaire, pas deux souverains | `R8_NORTH_AMERICA_CARIBBEAN-0124`; déduplication technique distincte de recherche géographique |
| MAP0-0005 ; MAP0-0099 | Ontario, `x8D15CB` | `HBC|HBC`: répétition du **même** propriétaire | `R8_NORTH_AMERICA_CARIBBEAN-0083`; déduplication technique ne valide pas l’exclusivité HBC sur l’Ontario |
| MAP0-0006 à MAP0-0016 ; MAP0-0100 à MAP0-0110 | Nouveau-Mexique, 11 RGB, `SC1|COM` | Deux propriétaires écrits sur les mêmes provinces | `R8_NORTH_AMERICA_CARIBBEAN-0072` et `R8_NORTH_AMERICA_CARIBBEAN-0070`; **UNRESOLVED**, tenir compte pueblos Rio Grande, présidios, espaces comanches sur les plaines et circulation des peuples |
| MAP0-0087 ; MAP0-0183 | Chiapas | Sélecteur de bâtiments `UCA` sans contrôle initial `UCA` correspondant | `R8_NORTH_AMERICA_CARIBBEAN-0016`; **ne pas créer un État historique UCA depuis une ligne de bâtiments**; remettre à QA technique sans redistribution |
| MAP0-0201 | Nunavut | Catalogue antérieur `ATB` vs main actuel `HBC` | `R8_NORTH_AMERICA_CARIBBEAN-0079`; conserver HBC comme baseline mais ne pas l’ériger en vérité historique; statut de contrôle autochtone incertain province par province |

**Inventaire littéral des 11 RGB du Nouveau-Mexique (pour diagnostic seulement, pas pour `Province_ID`) :**
`x256AEE`, `x810C1A`, `x74C317`, `x9660D3`, `xE27DFB`, `x40B080`, `x418B71`, `x92D597`, `x2EE19C`, `xB7D6F2`, `xF9F60A`.

**Liste complète des identifiants du registre effectivement lus :** `MAP0-0001`, `MAP0-0002`, `MAP0-0003`, `MAP0-0004`, `MAP0-0005`, `MAP0-0006`, `MAP0-0007`, `MAP0-0008`, `MAP0-0009`, `MAP0-0010`, `MAP0-0011`, `MAP0-0012`, `MAP0-0013`, `MAP0-0014`, `MAP0-0015`, `MAP0-0016`, `MAP0-0087`, `MAP0-0095`, `MAP0-0096`, `MAP0-0097`, `MAP0-0098`, `MAP0-0099`, `MAP0-0100`, `MAP0-0101`, `MAP0-0102`, `MAP0-0103`, `MAP0-0104`, `MAP0-0105`, `MAP0-0106`, `MAP0-0107`, `MAP0-0108`, `MAP0-0109`, `MAP0-0110`, `MAP0-0183`, `MAP0-0201`.

## 4. Contradictions historiques et documentaire non résolues

1. **Québec / Ontario / pays d’Ohio :** l’Acte de Québec étend la juridiction de la Couronne britannique sur le papier; le même territoire conserve des nations et autorités autochtones. NPS/S022 insiste sur les nations de la région de l’Ohio, tandis que l’Acte S004 exprime une prétention impériale. Ce sont deux **natures de preuve complémentaires**, pas des polygones incompatibles à « voter ». Les deux couches ne peuvent être confondues en un TAG souverain simple.
2. **HBC / Nations autochtones :** l’article de Cavanagh S011 explicite les prétentions de souveraineté de la compagnie; les descriptions de Parks Canada S013 localisent physiquement York Factory et Cumberland House (1774) dans des territoires habités. Elles ne démontrent pas l’administration globale du bassin. Le besoin de mapping porte sur les postes vs les espaces autonomes.
3. **Grande-Bretagne / rébellion :** les archives NARA S001 rendent certaine l’absence de déclaration d’indépendance au 1 janvier 1776, mais elles ne prouvent pas que les gouverneurs britanniques exercent partout leurs pouvoirs. Le siège de Boston (NPS S002) impose une exception urbaine; des cartes militaires datées par semaine sont nécessaires.
4. **Alaska :** LoC S016 et NPS S015 datent l’établissement colonial permanent de 1784; ni source ne donne la localisation exhaustive des escales, hivernages, villages Unangan ou frontières Yupik/Alutiiq de janvier 1776. Une expédition de marchands n’autorise pas un transfert global vers RUS ni une exclusion de leur présence.
5. **Frontière Espagne–France à Hispaniola :** le traité et la délimitation documentés par PARES S044 sont établis **après** le 1 janvier 1776. Pour la date cible, produire un fond cartographique antérieur à l’accord de février ou un témoignage local et comparer avec les dispositions de 1773, au lieu de reproduire la frontière fixée en 1777.
6. **Guatemala / Honduras britanniques / Mosquitia :** textes de traités hispano-britanniques, poste de bûcherons et alliances miskitu ne sont pas interchangeables. Rechercher actes de 1763, registres de la coupe de bois, correspondance des surintendants britanniques et preuves d’autonomie diplomatique miskitu. Les travaux Fuggle S039, Williams S040 et García S041 sont complémentaires par leur échelle, mais ne cartographient pas la baseline jeu.
7. **Carte d’empire vs territoires autochtones :** Bowen 1775 (S048), Prockter 1762 (S049) et Tirion (S050) renseignent les couleurs et noms revendiqués. Elles ne décrivent pas à elles seules fiscalité, villages, migrations, gouvernement et garnisons; toujours confronter traités locaux et sources ethnohistoriques.
8. **Frontières indigènes de l’Ouest :** noms génériques `APC`, `NVJ`, `BNN`, `LKT`, `ARP`, `SLS`, `ABS`, `BLF`, `IRC`, `PWN`, `ATB` se chevauchent historiquement selon villages, sous-groupes, alliances et saisons. Aucune transition de souveraineté ne doit être créée en découpant une carte moderne par longitude. Une forte confiance sur la présence d’une nation n’équivaut pas à certitude sur chaque province.

## 5. Chronologie : événements de 1776 et postérieurs *à exclure* de l’état initial

| Date | Fait documenté et conséquence | Référence |
|---|---|---|
| 1776-01-01 | **État cible**; KGH acquiert le statut d’administration d’État du commerce groenlandais le même jour | S017 |
| 1776-01-30 | Gálvez devient ministre des Indes : nouvelle étape de réorganisation des provinces intérieures, non antérieure à la date cible | S028 |
| 1776-02-29 | Accord préliminaire franco-espagnol concernant la limite de Santo Domingo (date postérieure à la cible) | S044 |
| 1776-03-17 | Évacuation britannique de Boston | S002 |
| 1776-05 (jour à vérifier) | Autorisation royale des Provincias Internas, **après** janvier | S028 |
| 1776-06-27 | Anza arrive à la baie de San Francisco et installe le Presidio, **après** janvier | S031 |
| 1776-07-04 | Adoption de la Déclaration d’indépendance des colonies américaines | S001 |
| 1776-08-28 | Procès-verbal franco-espagnol de délimitation à Hispaniola | S044 |
| 1777-01-15 | Déclaration d’indépendance des New Hampshire Grants / Vermont (à distinguer du dossier colonial de 1776) | S008 |
| 1777-06-03 | Traité d’Aranjuez concernant la limite de Hispaniola | S044 |
| 1784 (août) | Première colonie russe permanente à Three Saints Bay / Kodiak | S015; S016 |
| 1784-08-16 | Création de la province de New Brunswick | S006 |
| 1799 | Compagnie russo-américaine reçoit son monopole et des attributions de gouvernement | S016 |
| 1804 | Indépendance d’Haïti; aucun effet sur le 1 janvier 1776 | S045 |

## 6. Transmission R9 et éléments OUTSIDE_BASELINE

- **Interlocuteur secondaire :** `R9_SOUTH_AMERICA` pour l’isthme de Panama, principalement `R8_NORTH_AMERICA_CARIBBEAN-0086`. `Cross_Region_Conflict=COORDINATION_REQUIRED`, `Secondary_Region_ID=R9_SOUTH_AMERICA` dans le CSV. À revoir : vallée du Tuira, frontière Darién/Chocó, golfe d’Urabá, San Blas/Kuna Yala et sites contrôlés par les Guna. Pas de duplication d’une recommandation R8 par R9.
- **OUTSIDE_BASELINE (au sens des couples listés pour R8, sans attribution nouvelle) :** baie du Honduras / Belize n’a pas de State_ID séparé dans les 93 États R8 et se trouve discuté sous `STATE_GUATEMALA` (`SC1|GBR`). Le nom **Nouvelle-Écosse** n’est pas un `State_ID` R8 autonome dans l’inventaire transmis, bien que le TAG `NVS` soit présent au Nouveau-Brunswick; il faut vérifier la représentation précise de l’aire de Halifax lors de la synthèse centrale. Les îles, territoires insulaires français, britanniques, néerlandais et danois non séparés en `State_ID` doivent être localisés dans `STATE_WEST_INDIES`, sans inventer de TAG ou RGB.
- **Hawaii** est attribué à R6 dans le contrat régional, hors champ R8; l’absence d’une ligne R8 ne constitue pas une omission. **R9** conserve les espaces continentaux sud-américains; les métropoles européennes restent responsables uniquement de leurs zones européennes dans les autres missions.
- **VEN / GEN** : aucune ligne de propriétaire VEN/GEN dans cet inventaire R8. Leurs historiques protégés de population et de bâtiments ne sont pas touchés. Aucune redistribution de pops, bâtiments, ports, capitales et sujets n’est autorisée par ce document.

## 7. Actions demandées à la synthèse centrale (non exécutées)

1. **Blocage cartographique :** joindre bitmap/provinces du jeu, positions des RGB, coordonnées des postes datés de 1776; associer une carte ancienne géoréférencée et chaque Province_ID **uniquement après vérification visuelle ou spatiale**. Les RGB mentionnés dans les incidents restent des références techniques.
2. **Arbitrage historique :** clarifier grandes colonies vs insurrection, HBC/Arctique, New Brunswick/Nova Scotia, Nouvelle-Espagne et nations locales, Alaska, Mosquitia/Belize et limites d’Hispaniola; consulter sources locales avant transferts.
3. **Contrôle intégrité :** résoudre collisions ALK–ATB sur trois RGB et SC1–COM sur onze RGB, indépendamment de l’histoire; éliminer doublons ATB|ATB au Yukon et HBC|HBC en Ontario; revoir sélecteur `UCA` au Chiapas; comparer la seule baseline main à toute proposition de modification.
4. **Technique / gameplay :** valider après mapping les `Requires_New_Tag` et `Requires_State_Split`; préférer A, puis B; C géométrie seulement si une preuve spatiale montre l’insuffisance des découpages existants. Soumettre séparément toute redistribution de population ou bâtiments.
5. **Interfaces :** demander à R9 une relecture de Darién–Chocó, puis consigner son avis sous le Change_ID R8 déjà attribué, sans créer un autre propriétaire de mission.

**État final :** dossier de recherche et de traçabilité produit; **aucun transfert de province n’est prêt pour intégration sans cartographie contrôlée**. Une ligne `REVIEWED_NO_CHANGE` signifie que l’entité historique ou la chaîne coloniale générale est défendable, **pas** que toutes les RGB occupées dans la baseline ont été certifiées.
