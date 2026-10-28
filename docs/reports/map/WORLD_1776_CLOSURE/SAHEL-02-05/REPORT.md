# SAHEL-02-05 — Sénégambie, Mali et royaumes haoussa

27 octobre 2026. Référence : **1er janvier 1776**. Statut : **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Frontières et souverainetés ; Tchad et Nil différés sur la dernière consigne du joueur. Aucun test joueur acquis pour ce lot.

## Corrections installées

- Sénégambie : deux provinces du Baol (BAO) détachées du Jolof ; district côtier/Ndiambour rendu au Cayor ; Sine (SRR) séparé du Saloum (SLU). Cayor, Jolof, Boundou, Sine et Kaabu sont représentés comme royaumes non reconnus, plutôt que territoires décentralisés. Les noyaux Waalo/Fouta, Saint-Louis britannique et Gorée française de SAHEL-01 restent identiques.
- Mali : Ségou retrouve son noyau, dont le hub natif x2A6A2D, et sa capitale régionale passe à EASTERN_MALI. Le Macina des Ardo conserve son noyau et son autonomie sous tribut à Ségou ; il n'est pas assimilé à la Diina de 1818. Les communautés sénoufo (SNU) restent décentralisées au sud, sans inventer le royaume ultérieur de Sikasso. Tombouctou (TMB), Gao (GAO réactivé) et les approches sous influence Kel Tademekkat (TDM) remplacent l'extension prématurée du Macina dans TIMBUKTU. Kaarta reste distinct et inchangé.
- Haoussa : l'extension initiale de Sokoto, postérieure à 1776, est répartie entre Gobir (HAU), Kebbi (KEB), Zamfara (ZAM), Katsina (KTS), Daura (DAU), Kano (KNN), Zazzau (ZAZ) et Nupe (NUP), avec des communautés voisines décentralisées ZRM/GWR/BCH/BTA. Aucun émirat futur de Bauchi ou d'Adamawa préinstallé. La définition dormante de SOK est conservée pour les contenus ultérieurs. Bornou (BOR), Borgu (BRG), Bamum et les frontières tchadiennes ne changent pas.

**225 RGB existants réattribués, 26 groupes de transfert, aucun nouveau RGB ni pixel recoloré.** Huit régions natives touchées. Aucun terrain, ressource, trait régional, hub ou locator modifié. Le détail exhaustif cellule/propriétaire/coordonnées/raison est dans [PLAN.json](PLAN.json) et [GEOGRAPHIC_CROSSWALK.json](GEOGRAPHIC_CROSSWALK.json). Il s'agit d'enveloppes politiques sur le maillage existant, pas de frontières cadastrales certifiées.

## Institutions et compatibilité initiale

16 TAG nouveaux et GAO réactivé. Aucun nouveau personnage. Les monarchies sont initialisées avec les lois traditionnelles et une oligarchie de notables, approximation du pouvoir royal et des lignages ; les cinq agrégats communautaires restent décentralisés. Une variante commerciale privée, aux mêmes coefficients que le mercantilisme courant, est limitée à ces royaumes et débloquée par international_relations. Elle évite d'accorder artificiellement l'assurance maritime. Les profils antérieurs gardent leurs autres lois et connaissances ; leurs restrictions héritées restent signalées.

Le Macina reçoit seulement religion animiste de sa définition pré-Diina, relation tributaire et suppression des quatre modèles natifs de personnages du XIXe siècle. Hamadou-Amina III déjà présent est conservé ; aucun remplacement de dirigeant ajouté. Une référence de recrutement d'un unique conscrit MSN passe de Tombouctou à EASTERN_MALI, sans changer type, service ou effectif.

Les nouveaux profils comportent 5 à 9 connaissances locales explicites : agriculture, élevage, ateliers, alimentation, textile et diplomatie selon le pays ; capacité militaire traditionnelle lorsque les installations héritées l'exigent. Tombouctou conserve ses établissements de sel et de commerce avec shaft_mining et organized_financial_institutions, capacités de premier âge sans parent dans le graphe courant. Gobir reçoit seulement organized_military_establishments pour ses casernes héritées. Aucun paquet technologique par niveau, aucune modification de graphe TECH-R1/R2/R3 ou de recette ECON-ALLOYS/quincaillerie.

| TAG | Pays / agrégat | Type moteur | Technologies |
|---|---|---|---:|
| BAO | Baol | unrecognized | 6 |
| SLU | Saloum | unrecognized | 6 |
| TMB | Tombouctou | unrecognized | 9 |
| TDM | Kel Tademekkat | unrecognized | 6 |
| GAO | Gao | unrecognized | 7 |
| SNU | Chefferies sénoufo | decentralized | 5 |
| KNN | Kano | unrecognized | 7 |
| KTS | Katsina | unrecognized | 7 |
| DAU | Daura | unrecognized | 6 |
| KEB | Kebbi | unrecognized | 6 |
| ZAM | Zamfara | unrecognized | 6 |
| ZAZ | Zazzau | unrecognized | 6 |
| NUP | Nupe | unrecognized | 7 |
| ZRM | Pays zarma | decentralized | 5 |
| GWR | Pays gbagyi | decentralized | 5 |
| BCH | Pays du plateau de Bauchi | decentralized | 5 |
| BTA | Peuples de la haute Bénoué | decentralized | 5 |

Profils et justifications : [COUNTRY_PROFILES.json](COUNTRY_PROFILES.json). Les 17 profils nouveaux/réactivés passent le contrat statique avec prérequis fermés. Sur les huit pays existants, aucune nouvelle incompatibilité P0/P1 ; les demandes héritées d'esclavage pour dettes et de mercantilisme sans leurs gates restent ouvertes, sans leur attribuer des connaissances constitutionnelles ou d'assurance pour masquer la dette technique. La certification historique exhaustive de leurs anciens profils n'est pas prétendue.

## Populations et bâtiments

Monde avant/après : **837,328,539 → 837,328,539**, variation **0**. Toutes les cohortes, religions/cultures explicites et statuts d'esclavage sont conservés. Allocation par nombre de provinces transférées au sein de chaque portion source : règle technique de conservation, **pas estimation de densité ni recensement historique**. Les zéros nationaux du tableau signalent un TAG auparavant inactif dans le scénario, pas un territoire historiquement inhabité. Aucun changement démographique historique revendiqué.

| TAG | Habitants avant | Habitants après |
|---|---:|---:|
| BAO | 0 | 26 696 |
| BCH | 0 | 416 716 |
| BTA | 0 | 815 974 |
| CAY | 84 600 | 97 948 |
| DAU | 0 | 97 495 |
| GAO | 0 | 73 312 |
| GWR | 0 | 733 879 |
| HAU | 376 129 | 409 890 |
| JLF | 106 784 | 66 740 |
| KEB | 0 | 222 159 |
| KNN | 0 | 904 421 |
| KTS | 0 | 296 619 |
| MSN | 1 172 650 | 404 470 |
| NUP | 0 | 355 452 |
| SGU | 206 800 | 521 389 |
| SLU | 0 | 62 039 |
| SNU | 0 | 202 235 |
| SOK | 5 102 622 | 0 |
| SRR | 86 856 | 24 817 |
| TDM | 0 | 146 624 |
| TMB | 0 | 31 420 |
| ZAM | 0 | 444 319 |
| ZAZ | 0 | 660 877 |
| ZRM | 0 | 120 950 |

Ventilation par État dans [POPULATION_BEFORE_AFTER.csv](POPULATION_BEFORE_AFTER.csv). Tous les niveaux et toutes les recettes/PM préexistants sont conservés. Le rattachement politique des établissements suit les portions nouvelles ; les installations existantes du noyau Macina restent au Macina, les établissements de sel/textile/commerce de Tombouctou suivent TMB. Aucun bâtiment supplémentaire ni raffinement de production. Ressources et hubs restent régionaux et partagés selon le moteur ; leur allocation exacte et les budgets demandent l'observation en jeu.

## Sources et limites

[SOURCES.md](SOURCES.md) distingue les cartes réellement vues, les passages consultés et leurs dates. Les cartes comparatives c.1780/c.1800 guident les voisinages sans transformer leurs contours en cadastre de 1776. Les villes haoussa, le Niger et les noyaux royaux servent d'ancrages ; aucun partage par distance à une capitale ou frontière rectangulaire générée.

Cartes de contrôle : [Sénégambie avant/après](SENEGAMBIA_BEFORE_AFTER.png), [Mali avant/après](MALI_BEFORE_AFTER.png), [Haoussa avant/après](HAUSA_BEFORE_AFTER.png). Les couleurs des provinces servent à localiser le résultat installé, pas à prouver une source historique.

La Gambie (deux provinces SIL), les limites fines Galam/Khasso, l'estuaire Sine/Saloum et les franges exactes des royaumes restent ouverts. Les interfaces touarègues sont mobiles et disputées : TDM est une approximation politique, aucune exclusivité foncière ni suzeraineté uniforme imposée à Gao/Tombouctou. Cultures sérère, nupe, gbagyi et certains peuples de la Bénoué absentes du catalogue : identifiants régionaux natifs utilisés comme proxies ; aucune précision ethnographique ou conversion des POPs inventée. Les agrégats décentralisés ne représentent pas un État unifié.

## Vérifications et concurrence

1613/1613 contrôles statiques territoriaux/conservation réussis ; premier passage 361/361 archivé, puis détection supplémentaire d'un champ Sine mal décalé et de branches conditionnelles non pertinentes. Réparation bornée et traçable dans [COMPATIBILITY_REPAIR.json](COMPATIBILITY_REPAIR.json), sans effacer le résultat initial. Les 17 contrats des nouveaux profils passent ; les dettes anciennes sont séparées dans [TECH_NON_REGRESSION.json](TECH_NON_REGRESSION.json).

Versions courantes conservées hors nœuds attribués, y compris Amérique du Nord, SERG, Maghreb/Gibraltar, Siwa et Fezzan à 78 provinces, Balkans, fortifications/génie et TECH/ECON. Empreintes et comparaison hors portée dans [CONCURRENT_CHANGES.json](CONCURRENT_CHANGES.json). 13 fichiers fonctionnels existants modifiés, 24 ajouts ; aucun Git d'écriture, aucun vanilla ni suivi SERG écrit.

Une installation concurrente NORTHWEST-01 est arrivée après le premier contrôle de livraison. Ses 23 sorties courantes correspondent exactement à son manifeste, ses entrées aux versions que nous avions préservées ; 16 nœuds américains sont modifiés, sans changement d'un de nos huit nœuds africains. Les pixels retouchés sont exclusivement au nord-ouest de l'Amérique. Aucune restauration ni écriture fonctionnelle lors de la réconciliation : [EXTERNAL_COMPOSITION_REVIEW.json](EXTERNAL_COMPOSITION_REVIEW.json). Les 460 contrôles antérieurs du noyau sont complétés par les comparaisons de composition courante. Une ancienne assertion exigeait un ensemble de doubles propriétaires strictement identique ; elle est corrigée pour interdire toute nouvelle double attribution tout en permettant les résolutions externes prouvées par la comparaison exacte des propriétaires. Le premier résultat de composition est conservé dans VALIDATION_EXTERNAL_FIRST_RUN.json.


Commandes effectivement exécutées : installation avec `world1776_sahel0205.py --apply --validate`, réparation avec `--repair-compatibility --validate`, contrats collect_snapshot/audit_country, puis contrôles de livraison. Les outils réutilisés ne lancent pas le moteur. Les anciennes assertions d'ownership MSN/SOK ne sont pas présentées comme tests actuels de ces frontières.

Tests en jeu **NOT_RUN** ; [GROUPED_RUNTIME_ITEMS.md](GROUPED_RUNTIME_ITEMS.md) prépare le contrôle groupé, sans demande intermédiaire. WORLD reste **10/320, 3,13 %** ; aucun point pour une région partiellement couverte et aucune attestation humaine créée.

Prochaine action : contrôle cartographique groupé de ce lot et des limites signalées ; Tchad puis Nil restent pour une passe ultérieure. Pas de flavor entrepris.
