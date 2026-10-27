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
