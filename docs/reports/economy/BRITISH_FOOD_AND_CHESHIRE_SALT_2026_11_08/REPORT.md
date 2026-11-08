# Home Counties : réduction alimentaire et sel du Cheshire

8 novembre 2026 — `IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION`.

Les Home Counties demandent désormais **4 niveaux d'industrie alimentaire**, dans la plage de deux à six indiquée par le joueur. **Trois niveaux de mine de sel** sont ajoutés en Grande-Bretagne, dans le gisement existant de la région moteur du Lancashire représentant le bassin du Cheshire. Les trois niveaux de salines d'East Anglia sont conservés.

## Diagnostic et changements

Le joueur observe douze niveaux alimentaires déficitaires, notamment à cause du sel. Deux blocs identiques de douze niveaux existaient dans les historiques : l'un dans `00_west_europe.txt`, l'autre dans `98_build_start_1776_world_redistribution.txt`. Le premier passe à quatre et le doublon tardif est retiré. Il reste ainsi **une seule déclaration de quatre niveaux**, sans dépendre de la manière dont le moteur traite les créations répétées d'un même bâtiment.

Tous les autres champs du bâtiment conservé restent identiques : propriétaire britannique, réserves et méthodes de production. Aucun autre bâtiment des deux fichiers partagés n'est modifié. Les fonderies des Midlands, les autres changements économiques récents et les travaux territoriaux concurrents sont préservés.

Le gisement de sel du Lancashire possédait déjà **30 niveaux découverts**, mais aucune mine construite n'était déclarée en Grande-Bretagne. Trois niveaux sont ajoutés dans `common/history/buildings/99_1776_cheshire_salt.txt`, avec propriété britannique et réserves initiales de 1. La distribution des ressources n'est pas modifiée.

Les mines utilisent explicitement les pioches et pelles, sans explosifs, sans automatisation à vapeur, avec les charrettes routières, sans traitement supplémentaire du sel et sans collecte de données brutes. Un PM est sélectionné pour chacun des six groupes. GBR possède déjà `shaft_mining`, et aucun prérequis supplémentaire n'est accordé.

## Appui historique

L'extraction de sel en Grande-Bretagne est bien antérieure à 1776. Le **British Geological Survey**, *Geology of the Country around Stockport and Knutsford*, section **Rock salt and brine**, décrit la découverte de sel gemme à Marbury en 1670, suivie d'une phase d'exploitation minière, parallèlement à l'exploitation des saumures. Passage effectivement consulté le 8 novembre 2026 : [mémoire du BGS](https://webapps.bgs.ac.uk/Memoirs/docs/B01555.html), paragraphe commençant par « Salt production in Cheshire ».

Le document patrimonial du **Vale Royal Borough Council**, *Marston (Lion Salt Works), Revised Conservation Area Appraisal*, page PDF 3, section **1.1 Origins and development of the settlement**, confirme l'extraction par des techniques minières simples après la découverte de 1670, et le rôle de la Weaver devenue navigable en 1732. Il distingue les couches découvertes en 1779 et 1781, qui ne justifient pas une exploitation déjà généralisée au 1er janvier 1776. [Document de la collectivité](https://www.cheshirewestandchester.gov.uk/documents/planning-and-building-consultancy/total-environment/conservation-and-design/conservation-area-appraisals/MarstonConservationArea.pdf), texte effectivement consulté.

La notice du [musée Lion Salt Works](https://lionsaltworks.westcheshiremuseums.co.uk/about-us/history-of-the-museum/) corrobore l'ouverture de mines dans la région de Northwich au XVIIe siècle. Le musée actuel correspond à un établissement fondé en 1894 : cet établissement précis n'est pas projeté en 1776.

Le classement préexistant `TECH6A2_SALT_RESOURCE_DISCOVERY_IMPLEMENTATION_REPORT.md` attribue déjà le gisement connu du Cheshire à cette vaste région moteur. Il s'agit d'une représentation régionale de gameplay, pas d'une frontière historique du Lancashire ni d'un placement cadastral exact de Northwich. **Trois niveaux** sont un choix d'équilibrage, pas un dénombrement de trois puits historiques.

## Effet nominal de la chaîne

Quantités du jeu par niveau à effectif plein, sans économies d'échelle, autres modificateurs, pénuries ou variations de recrutement. Les recettes ne sont pas modifiées.

| Élément | Avant | Après |
| --- | ---: | ---: |
| Niveaux alimentaires observés par le joueur / demandés après correction | 12 observés | 4 demandés |
| Demande de sel de ces boulangeries | 60 | 20 |
| Production de produits alimentaires de ces boulangeries | 600 | 200 |
| Mines de sel construites au Lancashire | 0 | 3 |
| Production de sel supplémentaire des mines | 0 | 60 |
| Outils supplémentaires pour les mines | 0 | 6 |
| Salines préexistantes d'East Anglia | 3 | 3 |

Chaque boulangerie explicitement sélectionnée demande 5 unités de sel et produit 50 unités de produits alimentaires. Chaque niveau minier produit 20 unités de sel pour 2 outils. Les modes inactifs de conserve, distillerie et alimentation épicée ne rajoutent pas de sel au bâtiment alimentaire ciblé.

Le calcul avant/après alimentaire utilise les **douze niveaux rapportés par le joueur**, sans additionner artificiellement les deux déclarations historiques comme s'il avait observé vingt-quatre niveaux. La réduction de demande et l'apport minier améliorent ensemble le solde physique nominal de sel de 100 unités par rapport à ce point de départ. Les besoins des POPs, des autres bâtiments, des marchés et des échanges ne sont pas remplacés par cette différence locale.

Le déficit observé par le joueur n'est pas transformé en promesse de rentabilité après correction. Emploi des mines, prix du sel, débouchés alimentaires, salaires et accès au marché restent à vérifier en jeu.

## Infrastructure

Le modèle déclaratif existant de l'infrastructure britannique a été relancé en lecture seule. Avec les trois niveaux miniers, il estime une demande à plein effectif de **91,3**, contre **94,081** de capacité, soit une marge nominale de **2,781** dans le Lancashire. Les nouveaux bâtiments ajoutent six points d'usage d'infrastructure.

La marge est faible. Le modèle utilise les déclarations historiques, dont deux déclarations routières pour un total déclaré de dix niveaux, et ne certifie pas l'interprétation de ces doublons par le moteur. Aucune route, canal ou technologie supplémentaire n'est ajouté silencieusement. L'accès au marché effectif des mines doit être contrôlé dans la nouvelle partie. Détail dans `LANCASHIRE_INFRASTRUCTURE.json`.

## Contrôles et preuves

**41 contrôles statiques réussis** :

- Une seule déclaration alimentaire britannique aux Home Counties, niveau quatre.
- Une déclaration minière britannique au Lancashire, niveau trois.
- Trois niveaux de salines préexistants conservés en East Anglia.
- Tous les autres champs analysés des deux fichiers historiques partagés sont identiques aux préimages, hors les deux changements alimentaires prévus.
- Production minière compatible avec le gisement déjà découvert ; aucune modification des ressources, recettes, lois, technologies ou populations.
- Un PM connu et compatible sélectionné par groupe minier, sans technologie initiale nouvelle.
- **1 026 fichiers protégés** inchangés lors du contrôle.
- Aucun nouveau constat du validateur de technologies sur GBR, IREK et FRA. Leurs dettes antérieures restent présentes : respectivement 6, 11 et 6 constats ; le statut global historique `FAIL_STATIC` n'est pas présenté comme corrigé par cette passe.
- `git diff --check` ne relève pas d'erreur sur les deux historiques modifiés.

Preuves : `BASELINE.json`, `before/`, `TECH_BEFORE.json`, `INSTALLATION.json`, `CHANGES.patch`, `LANCASHIRE_INFRASTRUCTURE.json`, `VALIDATION.json`. Aucun Git d'écriture ni changement du vanilla. Les anciens rapports sont conservés.

## Contrôle moteur restant

Ces changements concernent l'initialisation : lancer une **nouvelle partie 1776** après rechargement du mod. Vérifier les quatre niveaux alimentaires des Home Counties, les trois niveaux miniers au Lancashire, leurs PM, emploi, entrées d'outils, sorties de sel et accès au marché. Puis laisser l'économie recruter et stabiliser les prix, vérifier le budget alimentaire et sauvegarder/recharger.

Aucun test moteur, niveau d'emploi réel, prix ou bénéfice post-correction n'a été observé pendant cette passe.
