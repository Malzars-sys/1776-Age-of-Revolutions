# RUSSIA-01 — Frontières russes et colonisation,1776

7 novembre2026 — **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. La correction explicite du joueur remplace la première interprétation : il s’agit de **décentralisation territoriale**, pas de désincorporation. Aucun des vingt candidats administratifs envisagés initialement n’a été installé comme tel.

**344 RGB existants passent de RUS à NNT**, agrégat décentralisé de communautés nenets :111 dans NENETSIA,233 dans OB. La toundra orientale de la Russie européenne et le Yamal/Gydan sont donc accessibles à la colonisation ; Poustozersk/Petchora, Mezen, Obdorsk, Berezov, les lignes fortifiées de l’Oural et les îles arctiques conservées restent russes. Aucun pixel, nouveau RGB, ressource, terrain, hub ou frontière d’un voisin n’est modifié. Liste exhaustive dans PLAN.json/GEOGRAPHIC_CROSSWALK.json ; carte CARTE_REPERES.png.

**Il s’agit d’une approximation de gameplay des communautés et du contrôle local**, pas de la découverte d’un État nenets souverain en1776. Le tribut, les lettres de sujétion et la répression de1746 sont documentés et contredisent une lecture d’indépendance juridique intégrale. La mobilité et l’administration très discontinue de l’intérieur motivent le choix décentralisé ; les limites précises des parcours saisonniers ne sont pas restituées. NNT n’est ni tributaire ni suzerain ; sa culture `ugrian` est le proxy indigène déjà présent dans ces pools, sans création d’une culture moderne ni conversion de POPs.

Les **59 portions russes** sont consignées dans RUSSIAN_FRONTIER_DECISIONS.json, y compris les frontières européennes, caucasiennes, kazakhes et pacifiques. Vieille-Finlande, territoires de1772, Ukraine, Don, Bachkirie et Kalmoukie ne sont pas transformés en peuples libres sur la seule base de leur statut particulier. Les administrations de l’iasak ne sont pas assimilées automatiquement à une absence de pouvoir russe. La Tchoukotka CKC est déjà décentralisée ; les jüz, polities caucasiennes, territoires Qing, Sakhaline indigène et le comptoir ALK sont préservés. Les deux cellules russes du fichier régional SAKHALIN sont kouriles. Cette passe ne certifie pas chaque cadastre frontalier.

La mécanique native1.15 est rendue accessible : loi **Colonisation interne**, amendement **Cosaques**, institution coloniale niveau1, cinq paramètres natifs et scores IA d’établissement/dissolution restaurés. Quatre commandes natives initialisent les implantations du Don, du Yaïk, d’Orenbourg et d’Astrakhan ; aucun corps militaire supplémentaire n’est recruté. Orenbourg est représenté par la vaste région moteur SAMARA : ce n’est pas la preuve que toute la région était une communauté cosaque. L’établissement réserve normalement20% des terres arables et son fonctionnement dépend des effectifs, de la capacité de la portion et du PM natif. Aucun corps de1851/1858/1860 n’est projeté en1776. Les effets réels et la croissance coloniale restent à tester.

| Région | RUS avant | RUS après | NNT après |
|---|---:|---:|---:|
| NENETSIA | 23138 | 20130 | 3008 |
| OB | 4409 | 2638 | 1771 |

Monde : **837328654 → 837328654**.4779 habitants passent dans les portions NNT ; cultures, religions explicites/implicites et autres champs sont conservés. Seul le pool indigène est réparti selon les comptes de cellules ; les pools russes/tatars restent sur les axes de peuplement. C’est une allocation technique, pas un recensement ou une mesure de densité par pixels. Aucun ancien bâtiment, PM, propriété ou régiment n’est déplacé. Les quatre implantations cosaques sont les seuls ajouts bâtis demandés au moteur.

Profil NNT explicite de quatre capacités anciennes : **PASS_STATIC_ONLY**. Aucun nouveau P0/P1 sur sept témoins ; dettes existantes conservées et publiées dans TECH_NON_REGRESSION.json, dont gate des cuirassiers russes et historique CKC absent. Aucun graphe TECH ou recette commune modifié.

**532/532 contrôles statiques réussis**, dont propriétés exactes, conservation de cohortes, statuts des59 portions, références1.15, absence de nouveau tribut et de nouvelle enclave centralisée. Le premier contrôle de continuité a relevé sept cellules côtières isolées : elles sont réintégrées à l’enveloppe nenets, avec réparation et premier échec archivés. Les îles russes préexistantes restent distinctes. Contrôle moteur, rendu des capitales/drapeaux, comportement IA, emplois et budget : **NOT_RUN**.

Cinq fichiers partagés ciblés et sept ajouts privés. Les sept fichiers économiques modifiés extérieurement entre le relevé initial et les préimages sont enregistrés, puis conservés. Tous les autres fichiers fonctionnels et preuves SERG sont identiques aux préimages immédiates. Aucun Git, vanilla ou suivi SERG écrit. WORLD reste10/320,3,13%, aucun point joueur ajouté.

Suite : contrôle russe groupé avec RUNTIME_PROTOCOL.md ; aucune autre région automatiquement engagée.
