# INTERIOR-01 — Congo intérieur, Grands Lacs et Mozambique

**28 octobre 2026 — référence : 1er janvier 1776.** Statut **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Demande directe conservée dans USER_REQUEST.txt. Corrections territoriales et initialisation nécessaire ; aucun personnage ni raffinement des bâtiments. L'Afrique australe est la passe suivante, non commencée ici. Courbes et finition cosmétique reportées par le joueur.

## Territoires installés

**369 RGB natifs réattribués en 40 groupes, 11 régions moteur** : CONGO_ORIENTALE, EAST_ANGOLA, KASAI, KATANGA, KAZEMBE, LOURENCO_MARQUES, MOCAMBIQUE, TANGANYIKA, UGANDA, ZAMBEZIA, ZAMBIA. Aucun nouveau RGB, pixel recoloré, terrain, ressource ou locator modifié. Liste exhaustive dans [PLAN.json](PLAN.json), coordonnées dans [GEOGRAPHIC_CROSSWALK.json](GEOGRAPHIC_CROSSWALK.json), cartes [avant](BEFORE.png) / [après](AFTER.png). Les coordonnées servent à retrouver des cellules, pas à certifier un cadastre de 1776.

- **Lunda, Luba, Kazembe, Kuba** : noyau Luba recentré sur Upemba/Lualaba ; Kazembe sur Luapula/Mweru, distinct des communautés du cuivre et Hemba. La capitale régionale LND passe d'EAST_ANGOLA à KATANGA, autour de Mussumba/Kapanga. Le **Kanyok** a un noyau autonome et doit un tribut au Luba ; le **Kazembe** reste autonome, tributaire du Lunda. Les liens natifs traduisent une suzeraineté souple, sans certifier le taux d'un tribut historique. Le noyau Bushong/Kuba est distingué des communautés du Kasaï/Sankuru et Luba du Kasaï ; le Maniema n'est pas annexé par anticipation aux expansions luba ultérieures.
- **Zambèze et Malawi** : réduction des grandes enveloppes Barotse/Bemba/Maravi. Le noyau de la plaine Luyana est conservé, les communautés des plateaux et Luvale/Lwena sont séparées. Le Bemba garde un noyau ancien ; Lungu/Mambwe, Bisa, Tumbuka et Ngonde sont distingués, sans reproduire ses conquêtes du XIXe siècle. Le nom Maravi devient **Kalonga** pour sa cour résiduelle ; **Undi et Lundu**, ainsi que les communautés chewa, yao, makua, lomwe et sena, ne sont plus administrés comme une seule province maravi. L'enveloppe Maseko/Ngoni anachronique disparaît de ce secteur.
- **Grands Lacs** : Busoga séparé du Buganda comme ensemble de principautés, sans monarchie unitaire de Kyabazinga. Noyaux **Gisaka, Bugesera, Buha du Nord, Buha du Sud, Kiziba, Kyamutwara/Ihangiro** distingués. Ce dernier reste un agrégat de deux pouvoirs à la résolution disponible. Kigali reste rwandais. Buddu et les chronologies royales contradictoires ne servent pas de prétexte à inventer une nouvelle frontière.
- **Mozambique** : les enclaves et arrière-pays commerciaux sont distingués des royaumes africains. Ibo/Quirimbas, Mozambique/Mossuril, Quelimane, Sena/Tete et Sofala sont préservés ; Zumbo reçoit un raccord de trois cellules au corridor portugais existant. **Inhambane passe au Portugal** sur une cellule côtière attestant le poste antérieur à 1776 ; la province reste beaucoup plus vaste que le comptoir. **Delagoa/Maputo passe aux autorités du Tembe**, avant l'installation autrichienne de 1777 et le dispositif portugais de 1781–1782. Uteve est distingué de la possession portugaise de Sofala. La présence commerciale européenne antérieure n'est pas niée ; elle n'est pas assimilée à l'administration directe de toute la baie.

Tous les noyaux centralisés examinés sont contigus et ont un voisin centralisé ; aucune nouvelle enclave centralisée entourée uniquement de pays décentralisés. Les agrégats de communautés peuvent avoir plusieurs composants, explicités dans GEOMETRY_CHECK.json ; le Portugal garde ses établissements maritimes séparés. Les corridors de Zumbo et les contours royaux sur cellules entières sont des approximations politiques, non une preuve de contrôle de chaque village.

## Institutions et technologies

**23 nouveaux TAG et 5 TAG natifs activés**, soit **28 profils explicites contrôlés** ; neuf profils existants conservés. Aucun dirigeant ajouté. Deux pactes tributaires seulement : LND → KZM et LBA → KNY. La royauté luyana est historiquement attestée, mais **LZO conserve sa catégorie décentralisée native** dans ce lot cartographique : elle n'est pas transformée en enclave centralisée et aucun corridor arbitraire vers le Portugal n'est créé. C'est une limite du modèle politique, pas une négation de son histoire.

| TAG | Nom ajouté ou TAG natif | Catégorie moteur | Technologies connues | Capitale régionale |
|---|---|---|---:|---|
| KSC | Pays du Kasaï et du Sankuru | decentralized | 4 | KASAI |
| LKS | Luba du Kasaï | decentralized | 4 | KASAI |
| MIA | Communautés du Maniema | decentralized | 4 | CONGO_ORIENTALE |
| LMP | Lamba et communautés du cuivre | decentralized | 5 | KATANGA |
| ZPL | Communautés des plateaux du Zambèze | decentralized | 4 | ZAMBIA |
| LVL | Luvale et Lwena | decentralized | 4 | ZAMBIA |
| MLG | Lungu et Mambwe | decentralized | 4 | KAZEMBE |
| BSI | Bisa | decentralized | 5 | KAZEMBE |
| TBK | Communautés tumbuka | decentralized | 4 | KAZEMBE |
| NGD | Ngonde | unrecognized | 7 | KAZEMBE |
| KNY | Kanyok | unrecognized | 7 | KATANGA |
| BUS | Principautés du Busoga | decentralized | 6 | UGANDA |
| GSK | Gisaka | unrecognized | 7 | TANGANYIKA |
| BGE | Bugesera | unrecognized | 7 | TANGANYIKA |
| BHA | Buha du Nord | unrecognized | 7 | TANGANYIKA |
| BHS | Buha du Sud | unrecognized | 7 | TANGANYIKA |
| KIZ | Kiziba | unrecognized | 6 | TANGANYIKA |
| KYM | Kyamutwara et Ihangiro | unrecognized | 6 | TANGANYIKA |
| UDI | Undi | unrecognized | 7 | ZAMBEZIA |
| LDU | Lundu | unrecognized | 7 | MOCAMBIQUE |
| UTV | Uteve | unrecognized | 7 | ZAMBEZIA |
| TCH | Tonga, Chopi et Tsonga | decentralized | 4 | LOURENCO_MARQUES |
| TMP | Tembe | unrecognized | 7 | LOURENCO_MARQUES |
| LND | LND | unrecognized | 7 | KATANGA |
| LBA | LBA | unrecognized | 7 | KATANGA |
| KZM | KZM | unrecognized | 6 | KAZEMBE |
| KBA | KBA | unrecognized | 6 | KASAI |
| LZO | LZO | decentralized | 5 | ZAMBIA |
| BMB | BMB | unrecognized | 2 | KAZEMBE |
| MRV | MRV | unrecognized | 5 | KAZEMBE |
| MTP | MTP | unrecognized | 8 | ZAMBEZI |
| MNC | MNC | unrecognized | 6 | ZAMBEZIA |
| MKU | MKU | decentralized | 4 | MOCAMBIQUE |
| LMW | LMW | decentralized | 4 | MOCAMBIQUE |
| UYA | UYA | decentralized | 5 | MOCAMBIQUE |
| SNA | SNA | decentralized | 4 | MOCAMBIQUE |
| CHW | CHW | decentralized | 4 | ZAMBEZIA |

Les justifications individuelles figurent dans [COUNTRY_PROFILES.json](COUNTRY_PROFILES.json). Capacités rurales, artisanales, commerciales, militaires et minières sont distinguées. Les communautés du cuivre reçoivent uniquement la capacité minière préindustrielle nécessaire au modèle local ; aucun moteur ni industrie moderne. Les bâtiments nommés building_railway utilisent ici le PM de **réseau routier traditionnel**, avec réseau ferré et trains de voyageurs désactivés.

Les neuf anciens profils gardent toutes leurs connaissances. Deux seuls ajouts ciblés : **international_relations à BMB et MNC**, avant l'activation des lois, pour leurs contacts politiques/commerciaux documentés et la loi privée de coutumes commerciales. Cette loi reprend les effets du mercantilisme sans distribuer l'assurance commerciale. **Aucun graphe TECH, recette ou PM commun modifié.** Les dettes déjà présentes (dont certains centres de commerce et lois demandées) restent énumérées dans TECH_NON_REGRESSION.json ; elles ne sont pas certifiées fonctionnelles par ce lot. Le contrôle HMB supplémentaire porte sur les données reçues et sa version actuelle, sans fabriquer un audit antérieur.

La première exécution a révélé une culture inexistante, une mauvaise région capitale CHW et deux prérequis de loi. Correction conservée dans [COMPATIBILITY_REPAIR.json](COMPATIBILITY_REPAIR.json), anciens résultats dans RUN01_*.json. **tonga** sert de proxy moteur large aux cultures nationales TCH/TMP ; ce n'est pas une reconstruction de l'identité tsonga/chopi/tembe et aucune culture de POP n'a été changée. CHW a sa capitale en ZAMBEZIA, qu'il possède effectivement.

## Population et conservation

Population mondiale : **837,328,539 → 837,328,539**, delta **0**. Les onze totaux régionaux et chaque ventilation culturelle, religieuse et servile sont conservés. Répartition technique de chaque cohorte par nombre de provinces natives uniques de sa portion, avec arrondis entiers conservatifs : **ce ne sont pas des recensements historiques**. Les valeurs nationales ci-dessous ont le même périmètre global avant/après ; elles ne mesurent pas les seuls comptoirs ou capitales.

| TAG touché ou profil revu | Avant | Après |
|---|---:|---:|
| AGC | 34 626 | 14 839 |
| BGE | 0 | 120 319 |
| BHA | 0 | 39 339 |
| BHS | 0 | 65 566 |
| BMB | 198 664 | 38 393 |
| BSI | 0 | 91 160 |
| BUG | 721 157 | 432 694 |
| BUS | 0 | 288 463 |
| CHW | 0 | 38 990 |
| GSK | 0 | 19 364 |
| HMB | 315 840 | 405 230 |
| KBA | 755 760 | 230 015 |
| KIZ | 0 | 19 364 |
| KNY | 0 | 71 836 |
| KRG | 116 184 | 38 729 |
| KSC | 0 | 525 745 |
| KYM | 0 | 38 727 |
| KZM | 439 924 | 147 917 |
| LBA | 581 311 | 112 842 |
| LDU | 0 | 64 286 |
| LKS | 0 | 396 411 |
| LMP | 0 | 101 308 |
| LMW | 0 | 151 772 |
| LND | 421 868 | 421 868 |
| LVL | 0 | 7 907 |
| LZO | 123 061 | 28 713 |
| MIA | 0 | 101 531 |
| MKU | 0 | 386 572 |
| MLG | 0 | 34 555 |
| MNC | 310 200 | 310 200 |
| MRV | 867 902 | 68 150 |
| MSK | 194 952 | 0 |
| MTP | 183 300 | 183 300 |
| NGD | 0 | 7 680 |
| NYM | 550 746 | 445 841 |
| POR | 5 142 983 | 5 107 879 |
| RWD | 481 276 | 360 957 |
| SNA | 0 | 37 943 |
| TBK | 0 | 48 568 |
| TCH | 0 | 632 863 |
| TMP | 0 | 162 008 |
| TSW | 1 610 546 | 544 170 |
| UDI | 0 | 77 683 |
| UTV | 0 | 365 096 |
| UYA | 0 | 177 066 |
| ZPL | 0 | 86 441 |

Détails : [POPULATION_LEDGER.json](POPULATION_LEDGER.json), [CSV](POPULATION_BEFORE_AFTER.csv). Aucun habitant créé, supprimé, converti ou transféré entre catégories culturelles/religieuses. Niveaux bâtis et sélections explicites de PM, types et effectifs militaires conservés ; la propriété des portions territoriales est seule ventilée.

## Contrôles, concurrence et limites

- **631/631 contrôles statiques** dans VALIDATION.json : attribution exacte, unicité, capitales, cultures référencées, continuité des noyaux, cohortes, niveaux/PM et conservation hors blocs autorisés.
- **28 profils nouveaux/activés PASS_STATIC_ONLY** ; 24 témoins existants comparés, aucun nouveau P0/P1. Les deux grants ciblés sont les seules différences de connaissances autorisées. HMB est vérifié en complément comme receveur.
- **12 fichiers existants ciblés et 35 ajouts fonctionnels**. Hashes d'entrée immédiate, réparation et version finale conservés séparément. Anciennes installations WORLD, interfaces Congo-01/Corne, SERG, TECH/ECON et travaux américains préservés ; aucune écriture Git, vanilla ou suivi SERG, aucun retour à une ancienne baseline.
- Carte native irrégulière, agrégats pluriels, subdivisions de la baie de Maputo, empreinte exacte des prazos et datation de certaines expansions restent approximatifs. Les noms et points de hubs natifs ne sont pas tous révisés : en particulier le locator Inhambane et sa correspondance de cellule doivent être observés en jeu. Pas de certification cadastrale, démographique, budgétaire ou de contrôle provincial uniforme.
- Chargement, drapeaux, capitales affichées, lois effectivement actives, marchés, approvisionnement, fronts et sauvegarde/rechargement : **NOT_RUN**, à intégrer au **test africain groupé**. Aucun test intermédiaire demandé et aucun reçu humain ajouté. Le journal de preuves final est DELIVERY_VALIDATION.json ; empreintes dans DELIVERY_MANIFEST.json.

WORLD reste **10/320 (3,13 %)** : aucun critère entier nouveau pour cette restauration partielle. **Prochaine passe : Afrique australe et établissements néerlandais/VOC**, depuis la version courante. Rozvi/Zimbabwe, Botswana/Tswana, interfaces du sud et chronologies du Cap restent à examiner ; ils ne sont pas déclarés déjà restaurés.
