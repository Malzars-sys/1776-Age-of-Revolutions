# R7_SUBSAHARAN_AFRICA — Incertitudes, limites et transmission MAP-0/1

**Date d'arrêt historique : 1776-01-01.** Dossier établi le 2026-10-10, uniquement à partir des lignes R7 de l'inventaire fourni et des sources bibliographiques référencées dans `R7_SUBSAHARAN_AFRICA_SOURCES.csv`. La baseline main est un **inventaire technique**, et non une preuve de souveraineté. Aucun travail effectué dans le répertoire du mod, aucun changement de province, aucune modification d'historiques protégés et aucun push.

## Mesure exacte de couverture et avertissement d'état

- 71 State_ID et 196 couples originaux State_ID + Owner_TAG ; 196 lignes distinctes de recommandations **provisoires**, 196 lignes de couverture. Les 4 366 entrées RGB agrégées ne sont pas une cartographie vérifiée des pouvoirs.
- Statuts: REVIEWED_NO_CHANGE = 2; CHANGE_PROPOSED = 49; UNRESOLVED = 145. Un couple UNRESOLVED est **inventorié et problématisé, mais pas historiquement tranché**. Aucun pourcentage d'achèvement scientifique ne peut être déduit du total des 196 lignes.
- 0 attribution de Province_ID ou Province_IDs dans les recommandations: la correspondance historique/RGB n'a pas été vérifiée avec une superposition géographique. Tous les transferts restent `MAPPING_REQUIRED`. Les RGB restent visibles uniquement dans les pièces du mod et références d'incident.
- Les corrections concernent surtout l'existence historique d'une formation politique, le statut de ses forts/comptoirs et la nature de la relation. **Ce ne sont pas des propositions de pixels approuvées.** `Requires_State_Split=YES` désigne un besoin de différenciation politique à expertiser, pas une décision d'implémentation.
- Les ouvrages généraux utilisés pour les lignes UNRESOLVED exposent l'environnement historique, **pas des preuves de souveraineté sur les provinces attribuées au TAG**. Leur citation ne transforme pas UNRESOLVED en validation.

## Correctifs prioritaires et contre-anachronismes

| Domaine | Diagnostic daté et conclusion historique | Décision jouable / mapping manquant | Sources |
|---|---|---|---|
| Sénégal et interface atlantique | 1776 : Gorée revenue à la France en 1763, Saint-Louis britannique jusqu'en 1779; autonomie des royaumes Cayor, Waalo, Futa-Toro, Bundu, Jolof. | Repérer îles/forts individuellement avant d'attribuer GBR/FRA; FRA sur une State Region entière exclu. | S007–S008 |
| Futa Toro | Révolution islamique **au cours de 1776**; impossible de faire de son issue politique une réalité sûre au **1er janvier**. | UNRESOLVED jusqu'à datation mensuelle et évaluation des souverains Deniyanke / Torodbe. | S007–S008 |
| Hausaland et marges | La capitale et le califat de Sokoto surgissent au XIXe siècle à la suite du djihad débuté **en 1804**; leurs couleurs sur toute l'aire haoussa en 1776 sont anachroniques. | Séparer les pouvoirs Kano, Katsina, Zazzau, Gobir et voisins; demander un nouveau TAG uniquement lorsqu'aucun TAG existant ne convient et que la géographie est démontrée. | S002–S003 |
| Massina | La Diina de Hamdullahi est fondée **en 1818**; des populations et chefferies peules existaient auparavant. | Ne pas assimiler le TAG MSN au califat ultérieur, ni déclarer le delta « sans État »; recenser les pouvoirs antérieurs. | S029 |
| Oyo–Dahomey | Oyo réel, Dahomey réel; tribut et diplomatie ne sont pas une annexion directe. La **première attestation explicite de protection d’Oyo sur Badagry/Porto Novo est 1777** et contraste avec une reconstruction extrapolée à 1730. | Dépendance tribut possible, extension exacte et certains littoraux UNRESOLVED. | S004, note 8 |
| Gold Coast | Forts néerlandais/danois et britanniques, mais droits fonciers et administration africaine restent essentiels; les Fante façonnent les relations avec la compagnie britannique. | Pas d'attribution d’une State Region entière à un fort; vérifier emprises de Christiansborg, Elmina, Cape Coast. | S005–S006 |
| Sierra Leone | La colonie de Freetown est fondée **en 1787**, après la date cible. La couleur SIL dans cinq États n’est pas une juridiction coloniale de 1776. | Ports marchands, îles et sociétés locales restent à distinguer par RGB. | S041, pp.349–372 |
| Côte d’Ivoire | Fort français d'Assinie 1701–1703, abandonné bien avant 1776; déplacement des groupes côtiers documenté de façon lacunaire. | Le RGB FRA ne doit pas être considéré comme une province française étendue. | S030 |
| Angola | Les Portugais tiennent Luanda, Benguela et certains corridors militaro-commerciaux, non tout le Kongo / plateau Ovimbundu. | Pas de rattachement par métropole; limiter les portions POR aux zones réellement administrées. | S001 |
| Zambèze et Mozambique | Tete capitale de l'administration des Rios de Sena depuis **1767**; prazos et forts portugais aux limites mouvantes, souverainetés karanga/maravi ailleurs. | A sur les vrais ports, fortifications et prazos attestés; aucune interprétation de « capitania » comme contrôle continu. | S009–S011 |
| Baie de Delagoa | Compagnie autrichienne arrive à Lourenço Marques en **1778**, expulsée en **1781**; le présidio portugais est postérieur. | POR en 1776 non prouvé; confirmer toponymie exacte de son RGB. | S009 |
| Corne / Érythrée | Les Ottomans gardent surtout Massawa et Suakin et s'appuient sur relais côtiers; hautes terres distinctes. La politique éthiopienne est fragmentée depuis **1769** (Zemene Mesafint). | SPLIT_CONTROL côtes/hinterlands, sans annexion du highland à TUR. Interface avec R3. | S012–S014 |
| Nil bleu / Kordofan | Funj/Sennar existe; « The Sudan » n’est pas une unité souveraine moderne en 1776; Kordofan entre royaumes et aristocraties. | Cartographier seulement zones de perception du tribut/garnisons; conflits Funj/Darfour non arbitrés. | S015 |
| Mombasa / Zanzibar | Dynastie Mazrui gouverne Mombasa (environ 1735–1837); l’expansion Busaidi centralisatrice est XIXe et ne doit pas être rétroprojetée à 1776. | MBS local; OMA côte et Zanzibar à expertiser île par île, port par port. | S020–S021 |
| Madagascar | Sakalava, Betsimisaraka, Merina et royaumes méridionaux; « Madagascar » n'est pas une seule monarchie en 1776. Unification par Andrianampoinimerina à partir d’environ **1787**. | Plusieurs pouvoirs à délimiter: requiert sous-unités existantes d’abord; 1776 reste incertain pour des lignages. | S018–S019 |
| Afrique australe | VOC réelle au Cap; pas de frontière fixe de Fish River au 1er janvier 1776 (ligne postérieure en 1778). Les républiques ORA et TRN sont créées en 1854 / 1852; formation Basotho unifiée et Ndebele/Mzilikazi postérieures. | Nombreuses couleurs anachroniques. Reconstitution pouvoirs pastoraux avant frontières linéaires du XIXe. | S023–S028, S039 |
| Sud-centre africain | Mwata Yamvo / Lunda et Mwata Kazembe vers Luapula/Mweru attestés; frontières de tribut non linéaires; pouvoirs Luba distincts. | Ne pas effacer les souverainetés en raison du type « decentralized ». | S016–S017, S033 |
| Haut-Oubangui | Dar al-Kuti est un sultanat fondé seulement **vers 1830**. | DAK 1776 inexistant en tant qu'État: identifier Dar Runga, Banda et Zande à date. | S036 |
| Cap-Vert | Les principales îles du Cap-Vert sont des établissements portugais durables depuis le XVe siècle. | Maintien POR de principe ; vérification des 4 RGB insulaires nécessaire. | S032 |
| Îles indiennes | Seychelles : occupation française permanente commencée en 1770, administration à Mahé 1778; cela ne prouve pas l'identité des 3 RGB actuels FRA/GBR de `STATE_INDIAN_OCEAN_TERRITORY`. | Empêcher tout résultat sans identification de Maurice, Réunion, Seychelles, Sainte-Hélène, Rodrigues, etc. | S031 |

## Incidents techniques de MAP_1776_KNOWN_ISSUES à dissocier de l'histoire

Ces incidents sont présents dans l'inventaire `main` et réapparaissent comme incidents techniques dans le candidat collaborateur non fusionné. **Ne pas inférer une souveraineté à partir d'un doublon ou d'une capitale non possédée.**

- `MAP0-0038`, miroir `MAP0-0132`: `STATE_SOMALILAND`, `x2D75F4`, `MJT|MJT`: répétition interne identique, pas une rivalité politique prouvée.
- `MAP0-0039`, `MAP0-0040`, miroirs `MAP0-0133`, `MAP0-0134`: `STATE_KENYA` `x9A78B7` (`SKY|MJK`), `x5C1ADA` (`SKY|WTU`): doubles propriétaires au niveau code; arbitrage nécessitant localité historienne et province bitmap.
- `MAP0-0041` à `MAP0-0043`, miroirs `MAP0-0135` à `MAP0-0137`: `STATE_TANGANYIKA` `xF56448`, `xE5BCC5`, `xAEEF76` (`NYM|MSI`), conflit technique non historique.
- `MAP0-0074` (miroir 0169) : capital DIO hors `STATE_SIERRA_LEONE`; `MAP0-0075` (miroir 0170) : GR7 hors `STATE_BLUE_NILE`; `MAP0-0077` (miroir 0172) : MTB hors `STATE_ZAMBEZI`. Il s'agit de références de définition pays; ces TAGs ne deviennent pas pour autant propriétaires des State_ID en question.
- La présence autrefois d’une ligne dans `03_north_africa.txt` ne change pas son `Region_ID` autoritaire R7. La source de géométrie est technique, non géopolitique. 

## Conflits historiques à garder explicitement UNRESOLVED

1. **Dahomey–Oyo / Badagry–Porto Novo**: Law 1971 note 8 relève la première source de « protection » de 1777 (mémoire de Baud-Dauchiron daté **23 juillet 1777**, AN France, C6/26), tandis qu’Akinjogbin 1967 pp. 91–92 suppose une vassalité remontant à 1730. Cette divergence empêche de représenter comme prouvée l'administration d'Oyo au littoral le 1776-01-01. `Cross_Region_Conflict=NONE` (interne R7); `Confidence=UNRESOLVED` pour le segment côtier exact.
2. **Statut de l'est du Cap**: Giliomee 1979 pp.290–337 parle de « frontier » fluctuante dès 1770, la synthèse SAHO situe une ligne Fish River officielle en 1778. Ne pas convertir la limite tardive en limite 1776. La présence de trekboers hors districts n’est pas administration directe de VOC.
3. **Oman–Mazrui**: Berg 1968 décrit une indépendance mombasaise sous Mazrui, Bhacker 1991 note la nature ambiguë des dépendances dans les territoires omanais. Une suzeraineté nominale peut coexister avec autonomie urbaine; aucun RGB sous OMA transférable en bloc.
4. **Futa Toro en 1776**: révolution interne et chronologie exacte du **1er janvier** non datées de façon assez serrée dans les sources consultées; conserver UNRESOLVED et demander textes contemporain 1775–1777.
5. **Darfour/Funj/Kordofan/Érythrée**: situer postes fiscaux et gouverneurs avec documents contemporains; privilégier contrôles locaux mouvants sur cartes d'États successeurs.
6. **Mascareignes et Seychelles**: le nom `INDIAN_OCEAN_TERRITORY` agrège sans préciser les îles, et la colonie française seychelloise ne peut justifier l'emplacement des RGB GBR; cartographie fondamentale manquante.

## Interface confiée à R3 (sans répliquer leurs recommandations)

`STATE_ERITREA`, `STATE_BLUE_NILE`, `STATE_KORDOFAN`, `STATE_EQUATORIA`, `STATE_CHAD`, `STATE_WADDAI`, `STATE_NIGER`, `STATE_TIMBUKTU` sont étiquetés `COORDINATION_REQUIRED` avec `Secondary_Region_ID=R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA` **uniquement dans les recommandations qui portent leur interface**. Chercher décision commune sur oasis/nomadisme Toubou/Touareg, hauts affluents du Nil, Massawa et hauts plateaux; les 196 couples restent tous en responsabilité R7. Il n’y a pas de « conflit tranché » `DISPUTED` faute de recommandation formelle R3 identifiée.

## OUTSIDE_BASELINE — à transmettre, pas à annexer

- **Saint-Louis sous GBR en 1776** : `STATE_SENEGAL` n'a actuellement aucun couple GBR. Rechercher si les RGB FRA représentent Saint-Louis ou Gorée; si absence de province correctement localisée, demander au coordinateur l'ajout via intégration/choix existant plutôt que produire une ligne R7 inventée GBR. Le cas est **OUTSIDE_BASELINE** à ce stade.
- **Royaumes Hausa de Kano/Katsina/Zazzau** : États historiquement distincts non représentés par les TAGs du sous-inventaire R7 (à comparer au registre des TAGs global avant création). Ce sont des demandes de nomenclature centrale, pas des nouveaux TAGs créés dans ces fichiers.
- **Chefferies Fante** sur la côte ghanéenne et **royautés malgaches distinctes** : vérifier tags existants hors R7 et géométrie; pas d'ajouts hors catalogue réalisés.

## Pièces prioritaires à collecter avant toute intégration

1. Couche vectorielle des polygones Province_ID xRRGGBB au 1er janvier du mod, et ancrages toponymiques, avec masques d’îles/forts; pas seulement la liste des RGB.
2. Tables de forts et garnisons datées 1775–1777 pour Saint-Louis/Gorée/Gambia, Gold Coast, Luanda/Benguela, Ilha de Moçambique/Sena/Tete, Massawa, Cap/VOC.
3. Atlas régionaux précoloniaux annotés 1750–1800, sources dynastiques ou manuscrits pour Borno/Hausa/Macina/Oyo, Buganda, Lunda/Kazembe et Madagascar.
4. Confrontation des souverainetés **de jure** et **effectives**, y compris calendriers postérieurs pendant 1776: aucun événement 1777, 1778, 1779, 1781, 1787 ou XIXe ne doit être inclus dans l'état au 1776-01-01.
5. Relecture technique de chaque `MAPPING_REQUIRED`; ne pas demander `C_GEOMETRY` sans preuve d’insuffisance des provinces et State Regions existantes. Vérifier ensuite population, capitales et bâtiments **hors de ce mandat**; VEN et GEN ne sont pas présents dans ces 196 lignes.

## Documentation complémentaire utilisée pour interpréter une priorité (non probante au niveau province)

Freetown fondée en **1787** : étude « Socioeconomic Status and Group Belonging: Evidence from Early-Nineteenth-Century Colonial West Africa », *Social Science History*, Cambridge Core, https://www.cambridge.org/core/journals/social-science-history/article/A58ACF8614CA073966E40DF313470D64, introduction et Figure 1 (1831). Cet article justifie la prudence pour SIL, pas l'attribution des terres à un acteur moderne. **Inscrite sous **S041** dans le registre SOURCES et reliée aux lignes SIL.

Aucune recommandation n'est intégrée automatiquement.
