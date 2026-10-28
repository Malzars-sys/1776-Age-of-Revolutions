# SAHEL-06-07 — Tchad et vallée du Nil

27 octobre 2026. Référence : **1er janvier 1776**. Statut : **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Consigne directe : « Donc tu peux passer à la suite, Chad et Neil. » Le périmètre reste cartographique, avec les seules initialisations nécessaires aux pays restaurés. Aucun test moteur ou joueur acquis.

## Corrections installées

- Lac Tchad : Mandara (MDR) distingué de Bornou/Baguirmi, sous tribut à Bornou ; Fitri/Yao (BIL) et Dar Sila (DLS) séparés de l'ancien aplatissement sous Ouaddaï. Wara, noyau royal du Ouaddaï, passe du territoire décentralisé TBI au WAD ; capitale régionale WAD déplacée vers CHAD. Baguirmi retrouve une enveloppe cohérente du Chari/Massenya/Bokoro. Le sud hors de ces noyaux revient aux communautés Sara (SRA décentralisé), sans royaume Sara unique inventé.
- Nil : Assouan et Kharga retournent à l'Égypte avec un corridor natif entre oasis et Nil. Le corridor des kashifs et garnisons nubiens (NUB), Dongola des makks Zubayr (DNG), les royaumes shayqiyya agrégés (SHQ) et les Abdallab (ABD) remplacent des portions du Soudan décentralisé générique. NUB est tributaire de l'Égypte ; ABD de Sennar.
- Soudan central : noyau Funj/Hamaj de Sennar (SNR), Musabbaat du Kordofan central (MSB), noyau montagnard de Taqali (TQL) et royaume shilluk (SLQ) restaurés. Les espaces pastoraux et périphériques non attribuables avec assez de certitude restent SD1. Aucun État moderne du Soudan n'est projeté en 1776.
- Darfour (DFR), franges septentrionales Kanem/Borkou hors unique cellule de Wara, côte ottomane, frontières éthiopiennes et royaumes haoussa antérieurs conservés. Ni révolte de Mandara vers 1781, ni conquête shayqiyya de Dongola des années 1780, ni annexion darfourienne de 1785/86, ni conquête égyptienne de 1820/21 anticipée.

**205 RGB natifs transférés, 22 groupes, sept régions. Aucun nouveau RGB, aucun pixel redessiné.** [PLAN.json](PLAN.json) et [GEOGRAPHIC_CROSSWALK.json](GEOGRAPHIC_CROSSWALK.json) donnent chaque cellule, propriétaires, coordonnées et fondement. Les indices des cartes d'inspection ne sont que des repères ; les RGB sont les identifiants canoniques.

Enveloppes politiques sur le maillage existant, **pas frontières cadastrales certifiées**. Les cartes UNESCO ont été effectivement vues : leurs routes en pointillés ne sont pas traitées comme frontières. Les localités servent à contrôler les noyaux, sans partage automatique par distance à la capitale. Aucun nouveau territoire centralisé déconnecté ou entouré uniquement de territoires décentralisés ; vérification géométrique sur pixels natifs et voisinage dans [GEOMETRY_PREFLIGHT.json](GEOMETRY_PREFLIGHT.json).

## Institutions et technologies nécessaires

11 TAG nouveaux et SRA natif réactivé. Monarchies/oligarchies de notables et liens tributaires sont des approximations du pouvoir des cours, lignages et kashifs ; ils ne certifient pas une administration uniforme de tous les villages. SHQ agrège plusieurs makks. Les successions exactes et la régence Funj/Hamaj ne font pas l'objet de nouveaux personnages. Aucun personnage, événement flavor, nouvelle troupe ou nouveau bâtiment ajouté.

| TAG | Entité | Type moteur | Technologies explicites |
|---|---|---|---:|
| MDR | Mandara | unrecognized | 7 |
| BIL | Fitri | unrecognized | 6 |
| DLS | Dar Sila | unrecognized | 6 |
| SNR | Sennar | unrecognized | 7 |
| ABD | Abdallab | unrecognized | 7 |
| SHQ | Shayqiyya | unrecognized | 7 |
| DNG | Dongola | unrecognized | 7 |
| NUB | Nubie ottomane | unrecognized | 7 |
| MSB | Musabbaat | unrecognized | 6 |
| TQL | Taqali | unrecognized | 6 |
| SLQ | Shilluk | unrecognized | 7 |
| SRA | Sara | decentralized | 4 |

Les profils sont justifiés individuellement dans [COUNTRY_PROFILES.json](COUNTRY_PROFILES.json) : agriculture, élevage, alimentation, ateliers, textile, échanges et établissements militaires traditionnels selon le pays. Aucun paquet technologique par âge, aucune modification des graphes TECH-R1/R2/R3 ou des recettes ECON-ALLOYS/quincaillerie. Une variante privée du mercantilisme, aux coefficients courants, utilise la gate international_relations pour ces seules cours ; pas d'assurance maritime artificiellement accordée. Les lois conditionnelles héritées de l'effet traditionnel ne valent pas attestation des lois actives en moteur.

Les 12 profils passent le contrat technique statique (pré requis, demandes de lois, bâtiments/PM explicites, unités) : [STARTING_TECH_NEW_COUNTRIES.json](STARTING_TECH_NEW_COUNTRIES.json). Sur huit pays existants, aucune nouvelle incompatibilité P0/P1 : [TECH_NON_REGRESSION.json](TECH_NON_REGRESSION.json). Les dettes héritées de Bornou, WAD, DFR ou SD1 restent signalées ; aucune connaissance tardive n'est ajoutée pour les masquer.

Les identifiants culturels Nubian/Shilluk/Daju/Mandara n'existent pas tous dans le catalogue courant. Proxies documentés : sudanese pour la Nubie et les Shayqiyya, nilotic pour Shilluk, fur pour Dar Sila, kanuri pour Mandara, baguirmi pour Fitri. **Nuba n'est pas utilisé comme synonyme de Nubien.** Aucune conversion des cohortes transférées.

## Populations et installations héritées

Monde : **837,328,539 → 837,328,539**, delta **0**. Sept totaux régionaux et chaque cohorte conservés (culture, religion et autres attributs explicites). Répartition par nombre de provinces transférées dans chaque portion source : **redistribution technique, pas recensement ou estimation de densité historique**. Un zéro national avant signifie TAG absent du scénario, pas absence historique d'habitants.

| TAG | Avant | Après |
|---|---:|---:|
| ABD | 0 | 174 025 |
| BGI | 131 592 | 75 869 |
| BIL | 0 | 12 924 |
| BOR | 807 079 | 725 557 |
| DLS | 0 | 35 111 |
| DNG | 0 | 22 255 |
| EGY | 3 625 694 | 3 628 872 |
| MDR | 0 | 88 101 |
| MSB | 0 | 109 626 |
| NUB | 0 | 20 531 |
| SD1 | 2 084 557 | 1 174 109 |
| SHQ | 0 | 22 253 |
| SLQ | 0 | 186 193 |
| SNR | 0 | 360 206 |
| SRA | 0 | 221 186 |
| TBI | 154 070 | 153 018 |
| TQL | 0 | 12 181 |
| WAD | 300 856 | 81 831 |

[POPULATION_BEFORE_AFTER.csv](POPULATION_BEFORE_AFTER.csv) détaille les portions. Tous les niveaux bâtis et PM sont conservés ; leurs parcelles suivent les nouveaux propriétaires. Une unique référence de recrutement du conscrit WAD passe de WADDAI, désormais sans portion WAD, à CHAD. Type, service et effectif inchangés. Aucun bâtiment affiné ou ajouté. Hubs, locators, terrains, ressources et traits régionaux restent inchangés et parfois partagés entre portions selon le moteur ; capitales visuelles, ressources, emploi et viabilité exigent le contrôle groupé en jeu.

## Sources, incertitudes et préservation

[SOURCES.md](SOURCES.md) distingue textes consultés, cartes vues et portée réelle. Dar Sila/Fitri et confins de WAD/BGI restent des approximations politiques ; chronologie d'unification de Taqali et liens Funj contestés, limites exactes des kashifs nubiens et juridictions pastorales non certifiées. Aucun tribut TQL, BIL ou DLS fixé sans preuve suffisante. NUB agrège des autorités héréditaires, non une province homogène. Le corridor Kharga–Égypte applique la règle de continuité du joueur et ne revendique pas une frontière désertique relevée. La présence territoriale restaurée ne certifie ni sa densité ni les souverains exacts au 1er janvier.

Cartes : [Tchad avant](CHAD_BEFORE.png), [Tchad après](CHAD_AFTER.png), [Nil avant](NILE_BEFORE.png), [Nil après](NILE_AFTER.png). Contrôle visuel du résultat installé effectué ; pas rendu du moteur.

Versions courantes préservées : SAHEL-01/02-05 hors cellules explicitement reprises ici (interface Bornou seulement), Balkans, Maghreb/Gibraltar, corridor de Siwa, Fezzan à 78 provinces, SERG, travaux américains NORTHWEST-01, TECH et ECON. [CONCURRENT_CHANGES.json](CONCURRENT_CHANGES.json) compare les empreintes et les blocs extérieurs aux sept régions. Aucun retour à une ancienne baseline, aucune écriture Git/vanilla/SERG.

## Contrôles et suite

Commandes exécutées : `world1776_sahel0607.py --apply --validate`, puis `--validate` après ajout du contrôle de corridor ; contrat collect_snapshot/audit_country par `world1776_sahel0607_closeout.py --tech` ; clôture avec `--evidence --reports --tracking --final`, puis `--reports --final` pour actualiser les résultats. **363/363 contrôles territoriaux statiques**, contrats techniques et contrôle de livraison séparés. [VALIDATION.json](VALIDATION.json), [DELIVERY_VALIDATION.json](DELIVERY_VALIDATION.json), [FILES_DELIVERED.json](FILES_DELIVERED.json) et [DELIVERY_MANIFEST.json](DELIVERY_MANIFEST.json). Les assertions anciennes imposant les propriétaires d'avant cette passe ne sont pas rejouées comme si ces transferts autorisés étaient des régressions.

Test moteur et joueur **NOT_RUN**. [GROUPED_RUNTIME_ITEMS.md](GROUPED_RUNTIME_ITEMS.md) complète le protocole groupé, sans demande intermédiaire. WORLD reste **10/320 (3,13 %)** : régions partielles, aucun nouveau critère régional ou humain acquis. Prochaine action : contrôle cartographique groupé de la bande sahélienne et du Nil, puis arbitrage des limites encore documentées. Aucune nouvelle région ni pack flavor lancé automatiquement.
