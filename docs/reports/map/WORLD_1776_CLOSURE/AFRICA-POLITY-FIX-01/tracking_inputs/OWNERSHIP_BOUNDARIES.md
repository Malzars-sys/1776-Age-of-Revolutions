# Propriété des modifications — chantier autonome n° 2

Référence : 1er janvier 1776. Ce suivi est indépendant du chantier SERG.

## Répartition

Le chantier WORLD traite successivement les Balkans, l'Italie méridionale, les espaces subsahariens R7, le Maghreb attribué à R3 et les Amériques R8/R9. Les identifiants régionaux du catalogue MAP-1776 sont conservés ; le nom d'une phase ne remplace pas le Region_ID canonique.

Les recherches et installations existantes restent acquises dans leur périmètre réel. En particulier, les transferts MAP2D en Bessarabie et autour de la mer Noire ne sont pas rejoués depuis les CSV antérieurs. La nouvelle baseline est capturée sur le workspace courant.

## Interfaces réservées ou à arbitrer

Tous les territoires attribués à une tâche SERG restent réservés à ce chantier : territoires germaniques, possessions impériales italiennes, juridictions habsbourgeoises couvertes par ses tâches, et tous ses noyaux déjà installés. Aucun changement dans son suivi, ses 81 tâches, son dénominateur ou ses reçus.

Croatie, Slavonie, Banat, Transylvanie, Istrie, Dalmatie de contact et Frontière militaire sont des zones de recherche commune. Aucun transfert de cellule AUS/HUN/TRS ou de juridiction déjà réservée ne sera fait ici sans attribution explicite. Une suzeraineté habsbourgeoise n'établit pas à elle seule une appartenance au Saint-Empire.

Pour l'Italie, Naples et Sicile, Bénévent et Pontecorvo seront étudiés pendant la phase 2. Les possessions et enclaves couvertes par SERG ne seront pas reprises sous un autre nom. Les interfaces avec les États pontificaux seront isolées au niveau des cellules et juridictions.

## Premier lot BALKANS-01

- Écriture territoriale : seuls `x6090A0` et `x6960A0`, dans `STATE_WEST_AEGEAN_ISLANDS`, de VEN vers TUR.
- POPs et bâtiments : seul le rattachement politique de cette State Region. Effectifs, cultures, religion implicite de la culture grecque, professions et propriété économique sont conservés.
- Institutions : seules les activations initiales de deux lois anachroniques dans les historiques MOL et WAL. Les lois communes et les effets génériques ne sont pas modifiés.
- Monténégro : lecture et décision historique documentée, aucune cellule transférée, aucun TAG supprimé, aucune relation nouvelle créée.
- Îles ioniennes, Dalmatie, Istrie, possessions habsbourgeoises, anciennes corrections MAP2D et noyaux SERG : conservés.

## Fichiers partagés

`00_states.txt`, `01_south_europe.txt` des POPs et des bâtiments contiennent des modifications d'autres chantiers. Chaque écriture doit partir de leur contenu courant et porter uniquement sur le bloc de l'Égée occidentale. Vérifier l'empreinte immédiatement avant l'écriture ; en cas d'évolution, relire et adapter le patch. Ne jamais restaurer un fichier entier depuis la capture.

Les autres travaux sur les technologies, PM, infrastructures, Anzin, Saint-Gobain, fortifications, génie et Révolution américaine sont hors périmètre. Leurs fichiers sont inclus dans les contrôles de conservation. Toute différence concurrente est enregistrée dans `CONCURRENT_CHANGES.json`, sans écrasement ni attribution abusive au lot WORLD.

## Lot BALKANS-02 — Raguse et passages adriatiques

Périmètre d'écriture : 122 pixels du seul parent `x11A0E0`, avec trois RGB `xE8D201` (RAG), `xE8D202` (TUR/Neum) et `xE8D203` (TUR/Sutorina), toujours dans `STATE_DALMATIA`. Les masques exacts sont dans BALKANS-02/PIXEL_PATCH.json. Les anciens RGB gardent leurs propriétaires ; le parent perd uniquement les pixels du masque.

Les six fichiers partagés sont le bitmap, la définition régionale, les terrains, les historiques des États, des POPs et des bâtiments d'Europe du Sud. Seuls le bloc dalmate, l'enregistrement des nouvelles couleurs et les pixels déclarés sont autorisés. POP croate VEN -30 000 / RAG +30 000 ; pêche VEN 3 -> 2 et RAG +1. Quinze fichiers nouveaux spécifiques portent les autres capacités ragusaines.

Ne pas restaurer le bitmap complet depuis une ancienne baseline : toute future écriture doit préserver les pixels concurrents et contrôler l'empreinte courante. Les preuves SERG (873 fichiers dans la capture) et les zones AUS/HUN/TRS restent protégées. Les locators et les autres régions ne sont pas écrits. Les dix fichiers économiques et technologiques modifiés en parallèle sont attribués à leurs chantiers dans BALKANS-02/CONCURRENT_CHANGES.json.

## BALKANS-03 — 2026-10-25

B03 ne transfère aucun territoire : x8C6292 reste MON ; x90A0E0 reste VEN ; xF5F6C2, xA12F82, x446E84 restent TUR. Ni bitmap, état, POPs, ressources, terrain ni hub modifiés. Les deux retouches de fichiers partagés sont strictement internes aux blocs c:MON des histoires de pays et de formations.

Les possessions ragusaines et les passages B02 sont préservés par leurs derniers reçus, sans retour à B01. Le gouvernement natif surchargé garde tous les gouvernements hors MON identiques. Pas de modification fonctionnelle ou documentaire SERG ; mise à jour concurrente de cinq documents seulement observée et archivée dans B03/EXTERNAL_SERG_UPDATE.json. TECH-R1/R2/R3, ECON-ALLOYS et quincaillerie restent hors périmètre.

## BALKANS-04 — 2026-10-25

Écriture réservée WORLD dans ce lot : Butrinto xE8D211 (parent x7BE071, ALBANIA), Parga xE8D212 et Prévéza xE8D213 (parent x8050E0, THESSALIA), Vonitsa xE8D214 (parent x518791, ATTICA), Cérigo xE8D215 (composante insulaire de x0055D7, PELOPONNESE). VEN reçoit cinq nouveaux RGB, 41 pixels ; tous les anciens RGB restent à leur propriétaire. Masques dans BALKANS-04/PIXEL_PATCH.json.

Les POPs passent seulement des pools grecs TUR aux nouvelles portions VEN : 500 / 4 700 / 1 000 / 7 500 par région, total 13 700 sans variation mondiale. Hors listes de provinces, ressources, traits et hubs restent identiques. Quatre ports minimaux et un niveau de fortification dans les Ioniennes sont dans un historique nouveau ; aucun ancien PM, pays, loi ou armée n’est retouché.

Patchs sur versions courantes, y compris l’extension insulaire après vérification des reçus ; aucune restauration d’ancienne baseline. Aucune écriture de territoire ou de suivi SERG, aucun chevauchement TECH/ECON. Les interfaces B01/B02/B03 restent protégées.

## BALKANS-05 — 2026-10-26

Périmètre d’écriture : dans c:TUR du fichier militaire du Moyen-Orient, seuls le compte des hussards de rumeli_ordusu (4→2) et son nœud de deux fantassins irréguliers sont modifiés. Quatre fichiers propres ajoutent les deux maisons, leurs chefs, deux traits d’office et FR/EN. Aucun autre pays ou officier national modifié ; effectifs par région/type/service conservés.

Aucun RGB, souveraineté, POP, bâtiment, PM, technologie, recette, loi ou relation diplomatique écrit. Préserver les postes vénitiens et Cérigo B04, RAG, MON et tous les territoires SERG. Trois preuves SERG avaient changé extérieurement avant application ; référence dans B05/EXTERNAL_SERG_UPDATE.json, aucune écriture de leur suivi.

## BALKANS-06 — 2026-10-26

Ajouts propres uniquement : histoire de bâtiments pour deux capacités côtières TUR en ATTICA/PELOPONNESE, histoire civile d’Haseki, trait d’office et deux localisations. Aucun fichier fonctionnel partagé écrit. Crète exclue, toutes les autres attributions et données conservées. Les effets sont ceux du bâtiment naval commun à l’échelle de l’État moteur, pas des cellules de fort cadastrales.

Le total mondial courant inclut l’ajout extérieur HBC-06 de 2 400 000 habitants. Reçu observé et archivé côté B06 ; aucune reprise du chantier américain ou de son suivi, aucune compensation. Conserver toutes les installations SERG, TECH/ECON et B01–B05 ; aucun droit d’écrire leurs autres blocs induit.

## 26 octobre 2026 — Recentrage cartographique et B07

B07 écrit seulement le pixel insulaire (4503,1065), x11A0E0→xE8D201, dans le bitmap courant. Aucun historique, pays, POP, bâtiment, recette ou territoire SERG écrit. La transition autorisée au Maghreb concerne les frontières R3 ; les interfaces réservées SERG restent protégées. Les ajouts flavor sont différés.

## MAGHREB-01 — 26 octobre 2026

Écriture limitée à Ceuta (3973,1252) xA0B0C0→xE8D231, Melilla (4029,1264) xCA9F75→xE8D232 et Oran–Mers el-Kébir (4081/4082,1255) xB735DB→xE8D233. Les trois noyaux sont SPA ; anciens parents du Rif exclusivement MOR, parent oranais MAS conservé. Modification du seul bloc AL_RIF et ajout SPA dans ORAN ; enregistrement de trois RGB et de leurs terrains hérités. Aucun autre bloc, POP, ressource, hub, pays, bâtiment, recette, armée, technologie ou territoire SERG écrit.


## MAGHREB-01-GIBRALTAR — 26 octobre 2026

Seul champ écrit : strait_gibraltar.second_land_endpoint dans une surcharge de même chemin que le natif. Raccord à Ceuta SPA existante ; xBC6ED3 britannique et arrière-pays xA0B0C0 marocain conservés. Aucun territoire ou suivi SERG, carte, population, bâtiment, recette, PM ou technologie écrit.


## MAGHREB-02 — contrôle territorial jusqu’à l’Égypte, 26 octobre 2026

Audit en lecture seule des vingt régions listées dans MAGHREB-02/TERRITORIAL_INVENTORY.json. Aucun pixel, RGB, propriétaire, POP, institution, bâtiment, technologie, PM ou recette écrit. Les couleurs litigieuses et les points d’oasis sont des constats, non des périmètres de patch autorisés par une projection. Toutes les interfaces SERG restent réservées ; douze évolutions extérieures observées et archivées, aucune écriture de leur suivi.


## MAGHREB-03 — quatre résolutions installées, 26 octobre 2026

Écriture bornée aux nœuds INNER_MOROCCO/TRIPOLI/LIBYAN_DESERT de 00_states.txt, aux deux pools POP ZWY de Tripoli/désert libyen et au seul appel politique du profil FZN. Six ajouts propres : diplomatie FZN, surcharge de ses personnages 1836, effet politique propre, loi commerciale et FR/EN. Noyau/corridor FZN et vingt résolutions d’attribution dans le rapport. Aucun bitmap, terrain, ressource, hub, recette, PM ou graphe technologique écrit. Tous les autres territoires sont préservés ; le Nouveau-Brunswick concurrent est composé depuis sa version courante, pas rétabli. Règle de continuité propre à ce lot, aucun AGENTS.md modifié.

## SAHEL-01 — 27 octobre 2026

Seuls nœuds STATE_SENEGAL des historiques d’états/POPs et de la région native, cinq pixels existants et deux terrains hérités. Six fichiers nouveaux propres à WAA (définition, histoire, effet, loi et FR/EN). Aucun autre pays, région, ressource, hub, recette ou territoire SERG écrit. 00_states courant composé sur le contour Fezzan de 78 provinces et les changements américains présents, y compris la retouche Arkansas/Texas survenue après notre application ; reçus et version exacte archivés dans EXTERNAL_COMPOSITION_REVIEW.json. Aucune restauration d’une baseline antérieure. Le corridor autorisé traverse P3-01/02/04/06 et ses interfaces R3 ; aucune autre région subsaharienne lancée par cette demande.

## SAHEL-02-05 — 27 octobre 2026

Seuls huit nœuds régionaux Senegal/Eastern Mali/Timbuktu/Hausaland/Outer Hausaland/East Hausaland/Nigeria/North Cameroon des états, POPs et bâtiments listés dans FILES_DELIVERED.json ; c:MSN militaire (une référence de recrutement), c:CAY/JLF/BND/SRR/KBU politique et c:HAU (unique grant de capacité militaire traditionnelle). Définitions SGU/MSN et cinq autres royaumes dans une surcharge propre, 16 nouveaux TAG et GAO réactivé. Aucune frontière BOR/BRG/BMM, aucun pixel/terrain/hub/ressource, recette commune, graphe TECH ou suivi SERG écrit. Les versions courantes Fezzan/Siwa/Gibraltar, Balkans et Amérique du Nord sont protégées ; pas de reprise d'ancienne baseline. Ensemble de RGB exact : SAHEL-02-05/PLAN.json.

### SAHEL-02-05 — composition concurrente vérifiée

NORTHWEST-01 a installé 23 sorties pendant la clôture de ce lot, dont 16 nœuds d’états américains et un changement de pixels limité à l’Alaska. Entrées/sorties rapprochées des manifestes courants ; huit nœuds africains et pixels africains conservés. Aucune écriture fonctionnelle de réconciliation. Preuve : SAHEL-02-05/EXTERNAL_COMPOSITION_REVIEW.json. Contrôle courant 1613/1613, dont les vérifications de composition ; 460 contrôles antérieurs du noyau conservés. Aucun point ou reçu humain nouveau.

## SAHEL-06-07 — Tchad/Nil

Sept nœuds d'états BORNU/CHAD/WADDAI/EGYPTIAN_DESERT/DONGOLA/KORDOFAN/BLUE_NILE et leurs seules portions POP/bâtiments listées dans PROPOSED_SCOPES.json. Une référence conscrite WAD de WADDAI à CHAD ; capitale régionale WAD vers CHAD dans surcharge propre. 11 nouveaux TAG, SRA activé, trois liens tributaires. Aucune géométrie bitmap, hub/locator, terrain, ressource, recette commune, graphe TECH, caractère ou suivi SERG écrit. Les autres portions Bornou et la totalité de DFR/TUR/ETH restent identiques. Énumération canonique : SAHEL-06-07/PLAN.json ; entrées immédiates apply_inputs, version livrée FILES_DELIVERED.json.

## HORN-01 — périmètre installé

Cinq nœuds ERITREA/GONDER/AMHARA/OROMIA/SOMALILAND des états et leurs seules portions POP/bâtiments listées dans SCOPES.json. c:ETH militaire : trois références régionales vers GONDER, comptes/types/services conservés. Administrations ETH à total constant vers la cour. Treize histoires de TAG natifs réactivés ciblées ; cinq histoires nouvelles, définitions propres, effets/loi, trois liens tributaires, sept neutralisations de modèles de personnages 1836, noms FR/EN. Aucun nouveau personnage, province, pixel, terrain, ressource, locator ou recette commune. KENYA non écrit. Anciennes preuves et mises à jour américaines courantes préservées ; aucun suivi SERG ni vanilla ni Git écrit. Énumération canonique HORN-01/PLAN.json, reçus FILES_DELIVERED.json et réparations séparées.

## CONGO-01 — périmètre installé, 28 octobre

Six nœuds d'états/POPs CONGO/BAS_CONGO/NORTH_ANGOLA/SOUTH_ANGOLA/EAST_ANGOLA/GABON, portions de bâtiments SCOPES.json, seuls c:KSN/LNG/TKE/YKA d'histoire nationale ; définitions privées incluant seule capitale KON. Neuf TAG propres, loi/effet et FR/EN. Aucun pixel, terrain, locator, recette commune, militaire ou suiviSERG écrit. Versions américaines courantes préservées, dont retouche de libellé Sacramento rapprochée en EXTERNAL_COMPOSITION_REVIEW.json. Reçu initial FILES_MODIFIED.json et correction technique COMPATIBILITY_AND_LABEL_REPAIR.json conservés ; version finale FILES_DELIVERED.json.

## INTERIOR-01 — périmètre installé,28octobre2026

Onze nœuds d'états EAST_ANGOLA/KASAI/KATANGA/KAZEMBE/ZAMBIA/CONGO_ORIENTALE/UGANDA/TANGANYIKA/MOCAMBIQUE/ZAMBEZIA/LOURENCO_MARQUES, portions POP/bâtiments SCOPES.json. Huit nœuds d'histoire nationale existants ciblés, BMB natif surchargé dans son propre fichier, 23nouveaux TAG et5profils natifs activés, définitions/effets/loi propres,2pactes tributaires et FR/EN. Liste exhaustive PLAN.json ; entrées immédiates apply_inputs/, réparation séparée COMPATIBILITY_REPAIR.json, version finale FILES_DELIVERED.json. Aucun pixel, terrain, ressource, locator, personnage, recette commune, graphe TECH, militaire ou suiviSERG écrit. Kenya/Rift/Zanzibar et noyaux côtiers Congo-01 conservés. Les cellules Maseko et la portion TSW du Mozambique seulement sont concernées ; Botswana/Zimbabwe/Rozvi/sud restent à la passe australe. Travaux américains et autres portions partagées conservés.

## MADAGASCAR-01-AUDIT

Lecture seule des deux nœuds NORTH/SOUTH_MADAGASCAR, de MAD, de ses POP et de son nom dynamique. Aucune cellule, POP, technologie, loi, bâtiment, personnage, localisation ou relation écrit. Seuls les rapports de ce lot et le suivi WORLD sont actualisés. SERG/TECH/ECON/Amériques et lots africains conservés.

## MADAGASCAR-02 — périmètre installé

Seuls deux nœuds NORTH/SOUTH_MADAGASCAR des états et POP ; c:MAD de l’histoire nationale et militaire (une référence conscrite), MAD des noms dynamiques.26nouveauxTAG, définitions/effets/loi propres, lien BOI→ATK, FR/EN et surcharge native de personnage MAD. Aucun niveau bâti ni PM ni pixel/terrain/ressource/locator modifié. Liste RGB PLAN.json ; entrées immédiates apply_inputs/ ; FILES_DELIVERED.json référence finale. Autres pays des fichiers partagés, WORLD antérieur, SERG, TECH/ECON et Amériques conservés sans retour à une baseline.

## SOUTHERN-01 — périmètre installé

126RGB natifs,4nœuds ZULULAND/VRYSTAAT/TRANSVAAL/NORTHERN_CAPE des états/POPs/bâtiments, plus TRANSVAAL redistribution bâtie. Histoires BST/MSH/SWZ et grant TSW ; c:WBL seul neutralisé dans les formations, relation GBR→ORA seule retirée.3TAG nouveaux,4définitions existantes surchargées, histoire nativeMTB et personnagesBST/MTB masqués par fichiers propres ; loi/effets/tributMSH→MNC/FR-EN propres. Pas de pixel, terrain, ressource, locator ou recette commune. FILES_DELIVERED.json et préimages immédiates font référence ; autres nœuds et travauxWORLD/SERG/TECH/ECON/Amériques/Madagascar préservés, aucune baseline restaurée.
