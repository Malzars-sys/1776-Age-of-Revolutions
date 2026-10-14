# MAP‑2G — Asie orientale, 1er janvier 1776

## Résultat concret

Intégration locale limitée à R5 : **1 710 changements de propriétaire RGB dans 11 State Regions**, sans redessiner le bitmap. La majorité correspond à des changements de **niveau d’administration au sein de l’ensemble Qing**, pas à des conquêtes ou à la reconnaissance de pays historiquement indépendants. Un sélecteur de lac invalide est retiré séparément ; aucune définition de province n’est supprimée.

La demande finale est respectée : **aucun grand gouvernement dans la Chine centrale**. Pékin, Zhili, le bassin central, les provinces côtières et Canton demeurent directement CHI. Trois gouvernements éloignés seulement deviennent des sujets Qing :

| Ensemble | TAG réutilisé | Régions | RGB | Habitants conservés |
|---|---|---|---:|---:|
| Gouvernorat du Yungui | YUN | Yunnan, Guizhou | 130 | 8 100 000 |
| Gouvernement militaire d’Ili | XIN | Dzoungarie, Tian Shan/Tarim | 474 | 610 400 |
| Administration des bannières khalkhas | MGL | Ouliastaï, Ourga, Touva | 602 | 673 619 |

Le mécanisme natif **vassal** représente ici une autorité provinciale ou frontalière sous souveraineté Qing. C’est une **approximation de gameplay expressément autorisée**, avec finances et autonomie diplomatique propres au moteur ; ce n’est ni une indépendance du Yunnan, ni un retour du khanat dzoungar, ni une Mongolie de 1911. Les anciens TAGs inactifs sont réutilisés : aucun nouveau TAG n’est créé.

Les nouvelles administrations reçoivent les technologies de départ déjà inscrites pour les Qing et un cadre de lois comparable. Exception nécessaire : elles utilisent **Isolationnisme**, parent du Système de Canton, car cette dernière loi exige Guangdong. Canton et la capitale commerciale impériale restent CHI, sans modification de son historique ni de ses lois.

## Autres corrections intégrées

| Secteur | Changement | Limite assumée |
|---|---|---|
| Ezo / Hokkaidō | Les 3 RGB japonais du sud-ouest passent à EZO, renommé **Domaine de Matsumae**. Les 21 RGB précédemment EZO passent à AIN. | Les provinces du jeu donnent une approximation du Wajinchi ; les comptoirs et droits de pêche hors de ce noyau ne deviennent pas une administration japonaise uniforme. |
| Kouriles | Les 3 RGB méridionaux EZO passent aux communautés aïnoues. Les 2 groupes insulaires ALK passent à RUS, non incorporés. | Présences commerciales, postes et yasak russes, pas une administration uniforme de toutes les îles. Aucun traité russo-japonais du XIXe siècle n’est anticipé. |
| Tchoukotka | 474 RGB passent du TAG nord-américain ATB à CKC, **Communautés tchouktches**, décentralisé. | Les catégories culturelles génériques existantes sont conservées, sans inventer de recensement ou de nouvelle culture. Aucun rattachement russe de 1778. |
| Taïwan | Le RGB oriental/montagneux `x44797F` devient FRS, **Communautés autochtones de Taïwan**, décentralisé. Les 6 autres restent Qing. | La frontière est grossière. On répartit le groupe autochtone déjà existant, pas les habitants selon la seule superficie. Aucun Han ou Mandchou n’est envoyé artificiellement dans les montagnes. |

**Attention au nom de State Region :** les cinq anciens RGB EZO/ALK de `STATE_SAKHALIN` se trouvent en réalité dans les **Kouriles**, pas sur Sakhaline proprement dite. Les subdivisions aïnoue, ulta et sakhalinienne de l’île sont conservées. Les possessions de l’Alaska et l’identité du pays ALK ne changent pas.

Matsumae garde son dirigeant existant, Matsumae Michihiro, et son lien de vassalité japonais. Sa loi de république présidentielle est remplacée par la monarchie, compatible avec le domaine héréditaire représenté. Aucun personnage, général, formation ou effectif n’est réécrit.

Les nouvelles administrations organisées utilisent la génération native de dirigeants ; aucun titulaire nommé n’est inventé comme fait historique. Cinq bannières d’identification utilisent des composants vanilla : **elles ne sont pas présentées comme des drapeaux historiques authentifiés**.

## Ce qui reste correctement inchangé

- **Mandchourie et Amour** : les régions examinées sont déjà Qing ; pas de cessions russes de 1858/1860. L’administration locale et les réseaux autochtones restent plus complexes que cette attribution impériale générale.
- **Tibet** : gouvernement distinct, déjà vassal Qing ; pas d’annexion ou de frontière contemporaine imposée.
- **Joseon** : royaume distinct, déjà tributaire des Qing ; Yeongjo est conservé au 1er janvier 1776.
- **Japon central** : Tokugawa et ses unités conservés ; pas de création d’une multitude de domaines ni de réformes Meiji.
- **Ryūkyū** : royaume distinct, lien japonais existant conservé. Le RGB japonais correspond au groupe d’Amami ; Okinawa et Sakishima demeurent RYU. Le tribut parallèle aux Qing reste une limite diplomatique du modèle, sans second suzerain artificiel.
- **Sibérie intérieure** : villes et réseaux russes existants conservés. Pas d’annexion systématique des populations autochtones ni de redistribution conjecturale de milliers de RGB.

## Conservation démographique et économique

La population mondiale reste **835 804 980**, avant et après. Les 11 régions territoriales concernées totalisent **10 382 993 habitants**, exactement conservés. Toutes les cultures, religions explicites et implicites, tailles, statuts libres/esclaves et autres champs démographiques présents sont vérifiés. Aucun habitant n’est créé ou supprimé.

À Taïwan, **130 277** membres du groupe `yuanzhumin` existant passent à FRS ; **55 833** restent dans les plaines Qing. Les autres groupes restent CHI. Le rapport **70/30 est une allocation technique**, pas une estimation historique de 1776 : il conserve la présence autochtone des plaines et le peuplement chinois des basses terres. La population Qing de l’île devient 769 723, pour un total insulaire inchangé de 900 000.

Les bâtiments conservent leurs niveaux, PM, réserves déclarées et propriétaires économiques. Aucun niveau de route, port, administration ou caserne n’est ajouté pour équilibrer les nouveaux pays. Les installations taïwanaises existantes restent dans les basses terres Qing. Quatre références économiques CHI situées au Yunnan ont été réadressées au **Hunan**, toujours possédé par CHI, pour éviter des sièges orphelins. Aucun propriétaire économique ne change ; les conséquences de recrutement et de marché sont à vérifier en jeu.

**Toutes les unités nationales et leurs lieux de recrutement sont identiques à la baseline.** Aucune formation, flotte, réserve de conscription ou garnison n’a été transférée aux nouveaux gouvernements.

## Corrections techniques et protections

- Suppression de `xBD5671` dans le sélecteur de propriétaire du Gansu : c’est un lac absent des State Regions, pas une province terrestre transférée.
- Capitale AIN désormais effectivement possédée à Hokkaidō grâce à la correction territoriale, pas à un transfert motivé par la seule syntaxe.
- 9 références de hubs corrigées sur leurs locators existants : Taïwan 2, Sakhaline 3, Ryūkyū 4. Aucun locator physique déplacé et aucune géométrie de province changée.
- Couleur ULT corrigée de 256 à 255, sans autre changement de cette définition.
- Comparaison ciblée avec `georg3mx-map-rework` : **0 scope R5 différent** dans l’historique des États actuel ; aucun travail compatible n’a été effacé et aucune fusion réalisée.
- MAP‑2A/B/C/D/E/F, Avignon/Frioul, transit franco-pontifical, diplomatie Crimée/Pologne, recrutement perse et suppression de l’industrie alimentaire de Tabriz, réformes ottomanes, technologies, PM, biens, assets et correctifs IA protégés par baseline, comparaisons et empreintes.

## Sources et portée des preuves

Les quatre recherches R5 et leurs 84 lignes ont été réutilisées, sans relancer un audit mondial. Le manifeste CSV renvoie aux cas et aux sources ; les IDs abrégés `R5-Sxx` correspondent à `R5_EAST_ASIA-Sxx` dans `docs/reports/map/MAP1/inputs/regional_originals/R5_EAST_ASIA_SOURCES.csv`.

- **Administrations Qing** : [Qing Shi Gao, volume 198](https://24histories.com/qingshigao/198) / volumes 200 et 206, tableaux des gouverneurs et généraux frontaliers ; le [volume 206, lignes Qianlong 40–41](https://24histories.com/qingshigao/206) distingue Ili, Ouliastaï et les résidents. Institution documentée ; représentation par sujets et limites des State Regions restent un choix de jeu. Compléments R5-S01/S02/S03/S04/S22/S23/S26.
- **Ezo et Sakhaline** : Brett Walker, *The Conquest of Ainu Lands* (2001), R5-S07 ; [Morris‑Suzuki, Indigenous Diplomacy, partie 1](https://apjjf.org/2020/22/morris-suzuki), R5-S08, distingue réseaux autochtones, reconnaissance japonaise de 1771 et postes plus tardifs. Ces échanges ne prouvent pas une souveraineté exclusive sur chaque province.
- **Kouriles** : [Postnikov, Outline of the History of Russian Cartography, pp. 39–40](https://src-h.slav.hokudai.ac.jp/sympo/98summer/pdf/post36-42.pdf), notamment les instructions et voyages citant RGADA, fonds 7, dossier 2539 ; [Krasheninnikov, Description du Kamtchatka, 1755, Library of Congress](https://www.loc.gov/item/2018694160/). Ces sources documentent exploration et contacts, pas une frontière russe uniforme sur tous les groupes RGB. Les négociations de 1778–1779 ne sont pas importées au départ.
- **Tchoukotka** : [Zuev, négociations russo-tchouktches de 1778](https://ostrog.ucoz.ru/publikacii_3/4_107.htm), R5-S14 : calendrier distinguant la situation initiale, les décisions ultérieures de 1776 et les négociations de 1778.
- **Taïwan** : [Academia Sinica, Taiwan Historical Research 22(2), Chen et Ka, 2015](https://www.ith.sinica.edu.tw/quarterly_history_look.php?id=628&l=e), R5-S12 : dispositifs Ai de 1754, populations des plaines et frontière autochtone ; les tracés de 1784/1790 ne sont pas repris en 1776. Aucun pourcentage démographique 70/30 n’est attribué à ces travaux.
- **Frontière russo-Qing** : traité de Nertchinsk, R5-S15, et recherches R5-S16/S24/S28 ; carte de 1860 utilisée comme avertissement chronologique, pas comme frontière de 1776.
- **Joseon et Ryūkyū** : R5-S17 et S10/S11 ; souveraineté distincte, relations tributaires et limites du modèle natif conservées.

Les provinces existantes sont identifiées dans la géométrie native et les locators. **Une position de ville n’est jamais présentée comme une preuve suffisante de souveraineté sur tout son RGB.** Les choix appliqués sont des approximations documentées, conformément à la méthode cartographique autorisée.

## Validations et test joueur

**49 contrôles statiques passent**, détaillés dans `MAP2G_VALIDATION.json` : conservation des RGB terrestres et attributs démographiques, profils économiques et militaires, capitales, références, sujets, noms FR/EN, locators/hubs, protections des lots précédents et état Git principal. Les modèles logiques ottomans et d’infrastructures passent. Les 50 doubles attributions anciennes restent inchangées ; 12 références orphelines anciennes hors R5 restent documentées, sans nouvelle anomalie introduite. Les trois CSV ont été calculés et vérifiés avec le skill de tableaux : comparaison de toutes les cellules, tests de recalcul restaurés et revue visuelle ; cette validation ne remplace pas le moteur du jeu.

**Le jeu n’a pas été lancé ni manipulé par Codex.** Les contrôles statiques ne garantissent pas l’emploi, les budgets, l’accès au marché ou le chargement effectif des scripts. Une ancienne sauvegarde ne teste pas ces historiques.

Dans une **nouvelle partie du 1er janvier 1776**, vérifier :

1. Chine centrale directement Qing ; trois sujets éloignés seulement, avec noms, couleurs, lois et dirigeants affichés.
2. Mandchourie/Amour et frontière russo-Qing ; garnisons impériales inchangées.
3. Ouliastaï/Ourga/Touva, Ili et Yungui ; Tibet et Joseon distincts.
4. Domaine de Matsumae au sud d’Ezo et Ainu Mosir ailleurs ; Sakhaline autochtone ; groupes des Kouriles.
5. Communautés tchouktches, sans annexion russe anticipée ; Alaska inchangé.
6. Taïwan occidental/nord Qing, orient autochtone ; Taipei, Keelung et Takow du bon côté.
7. Ryūkyū/Okinawa/Sakishima distincts, Amami japonais ; Japon central inchangé.
8. Après un mois : accès au marché, recrutement et budgets des nouveaux gouvernements ; Hunan et ses sièges économiques ; petits territoires insulaires. Envoyer les logs si un problème apparaît.
9. Vérification visuelle rapide d’Avignon, Venise, Caucase, Inde et des journaux ottomans.

## Sauvegarde et opérations Git

Avant les modifications, **MAP‑2F validé avec finitions Arcot/Madras/Pondichéry/Kandy** est sauvegardé sur `backup/1776-checkpoints` : [`9383096b3bfd5a1354400878cc8052f8efe8301e`](https://github.com/Malzars-sys/1776-Age-of-Revolutions/commit/9383096b3bfd5a1354400878cc8052f8efe8301e). Restauration fraîche : 5 701 fichiers, SHA‑256 identiques, vérification Git réussie. Plus gros fichier : 43 598 540 octets, sous la limite GitHub ; pas de LFS ou stockage payant.

Points de restauration distincts conservés : MAP‑2F `9383096…`, MAP‑2E avec correctifs perses `4937748…`, MAP‑2D validé `cb40133…`, checkpoint MAP‑2D précédent `0e16427…`. MAP‑2A/B/C sont contenus dans ces états cumulés ; aucun point historique indépendant non reconstitué n’est inventé.

Après vérification, seules les deux copies Git temporaires `prepared`/`restored` et leur paquet d’envoi ont été supprimés : **4 996 342 025 octets**, environ **5,0 Go**, récupérés. Les preuves légères sont conservées dans `BACKUP_MAP2F_VERIFICATION.json` et `BACKUP_CLEANUP.json`. Aucune ancienne archive distincte ni aucun fichier du workspace principal n’a été supprimé.

**Aucun commit dans le workspace principal, aucun merge, aucun push sur main.** Le seul push concerne le checkpoint MAP‑2F sur la branche de sauvegarde autorisée. MAP‑2G reste local, à tester ; MAP‑2H n’a pas été commencé.
