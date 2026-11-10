# Infrastructures britanniques et irlandaises, agriculture et revendications nenets

9 novembre 2026. **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Cinq fichiers fonctionnels modifiés ; aucun Git write, aucun fichier vanilla écrit. Les relevés du jeu décrivent l'état **avant** installation. Le nouveau départ n'est pas encore validé par le moteur.

## Diagnostic constaté

La partie est arrêtée au 1er janvier 1776. Les valeurs affichées sont arrondies : elles ne permettent pas de soustraire deux entiers pour obtenir un déficit exact. Exemple : Lancashire affiche 58 utilisés / 53 disponibles, mais son infobulle de solde affiche -4.

Le réseau des Lowlands a été effectivement ouvert en jeu : **2 niveaux, 2 000 employés, tous les postes pourvus, +14 d'infrastructure**. La capture `LOWLANDS_NETWORK_BEFORE.png` conserve ce témoin. Les scripts comportent pourtant deux déclarations de deux niveaux ; leur somme de quatre n'est donc pas la quantité chargée dans ce cas. Les anciens calculs additionnant les variantes ne suffisent pas à dimensionner le départ.

Les nouveaux niveaux visent les dernières déclarations existantes, sans supprimer les variantes antérieures, changer les PM routiers, les propriétaires, les réserves, les ports, l'incorporation ou les lois. Les canaux industriels restent dans Lancashire, Yorkshire et Midlands ; aucun chemin de fer actif n'est introduit.

| État | Utilisation / capacité affichées avant | Réseau, dernière déclaration avant | Après |
| --- | --- | ---: | ---: |
| Home Counties | 100 / 71 | 6 | 12 |
| Midlands | 67 / 44 | 5 | 9 |
| Lancashire | 58 / 53 | 5 | 7 |
| Yorkshire | 55 / 52 | 6 | 8 |
| East Anglia | 28 / 20 | 2 | 4 |
| Lowlands | 19 / 17 | 2 | 3 |
| Ulster | 11 / 10, accès 90 % | 1 | 2 |
| Munster | 10 / 10, accès 96 % | 1 | 2 |
| Leinster | 17 / 10, accès 57 % | 1 | 3 |

West Country (39 / 45) et pays de Galles (11 / 12) sont déjà excédentaires dans les relevés. Highlands et Connaught ne reçoivent pas d'ajout routier : aucun déficit n'y est attesté dans cette passe. Les trois relevés irlandais proviennent des captures du joueur ; les autres de la lecture directe du jeu. Aucun chiffre manquant n'est inventé.

Les **21 niveaux supplémentaires** produisent, à plein effectif avant les autres modificateurs, 147 points routiers et 8 points de canaux, avec la réduction d'incorporation applicable aux Lowlands. Le dimensionnement ne prend aucun crédit supplémentaire pour la population ou un multiplicateur positif. Il prévoit 0,1 d'utilisation supplémentaire par niveau pour les quartiers d'affaires, un point d'incertitude sur les valeurs d'utilisation affichées, et **2,6** d'utilisation supplémentaire dans Lancashire pour le niveau chimique et sa propriété.

Le scénario à 80 % d'emploi **des niveaux ajoutés**, avec la capacité déjà observée maintenue, couvre également ces besoins conservateurs. Le scénario à 50 % ne couvre pas tous les États : la correction ne constitue pas une garantie d'accès maximal si les réseaux se vident ou subissent des pénuries. Quantités nominales des réseaux ajoutés par semaine à plein effectif : bois +145, outils +16, fer +16, transport +105 ; emplois +27 400. Ce sont des flux de recettes, pas une prévision de budget ou de bénéfice.

## Industrie et agriculture

- Lancashire : usine chimique **2 → 3** niveaux dans sa déclaration actuelle. Ses PM, réserves et adresses de propriété sont conservés. Un seul niveau est ajouté, et non deux.
- Les élevages britanniques et irlandais des treize États métropolitains sélectionnent `pm_butchering_tools` dans leur groupe de base. **13 déclarations**, représentant **16 niveaux effectifs dans dix États**, sont corrigées. Les PM lainiers, clôtures, réfrigération et transports restent identiques. À plein effectif : outils +32 et viande +80 par semaine, avant modificateurs ; emplois de cette substitution inchangés.
- East Anglia : les deux déclarations de cultures de seigle passent de `pm_soil_enriching_farming` à `pm_simple_farming`. La dernière déclaration compte **sept niveaux** ; les autres régions céréalières gardent leurs PM. Vergers, outils, propriété et niveaux agricoles ne changent pas. À plein effectif pour ces sept niveaux : engrais -70 et grain -70 par semaine, avant modificateurs. Aucun amendement ou nouveau prérequis n'est introduit.
- Le choix d'East Anglia est une approximation régionale fondée sur l'amélioration agricole attestée dans le Norfolk avant 1776. Il ne prétend pas démontrer un classement national chiffré du rendement du seigle. Historic England, *North West Norfolk Farmstead and Landscape Statement*, p. 5, décrit les pratiques améliorées de la fin du XVIIe siècle et la mise en valeur du milieu du XVIIIe : https://historicengland.org.uk/research/results/reports/8095/NorthWestNorfolkChalkandLimestoneMixed .
- La correction orale du joueur a été interprétée comme l'annulation de la mine de soufre dans les Midlands. Aucun emplacement alternatif n'étant établi, aucune mine ou ressource sulfurée n'est ajoutée.

## Revendications russes

Ajout de **`add_claim = c:RUS`** aux régions **STATE_NENETSIA** et **STATE_OB**. Les portions NNT restent décentralisées. Les listes de provinces, propriétaires RUS/NNT, patries culturelles et toutes les autres données d'État sont conservées exactement après retrait des deux lignes ajoutées dans le contrôle sémantique.

Il s'agit du mécanisme de revendication coloniale demandé, pas d'une annexion ni d'un blocage mondial de la colonisation. Son efficacité dépend des règles natives de revendication et d'engagement régional ; la Russie conserve ses portions dans les deux régions. Le fonctionnement britannique/russe devra être confirmé dans une nouvelle partie. La documentation officielle d'introduction du mécanisme explique le blocage par revendication et intérêt : https://www.paradoxinteractive.com/games/victoria-3/news/dev-diary-75-diplomatic-improvements-in-1-2 . Ce texte ancien n'est pas présenté comme un test moteur 1.15.

Contexte historique réutilisé : `docs/reports/map/WORLD_1776_CLOSURE/RUSSIA-01/REPORT.md` et `SOURCES.md`, qui distinguent sujétion impériale et autonomie locale. Aucune progression WORLD/SERG, souveraineté, population, loi de colonisation ou travail territorial concurrent n'est modifié.

## Vérification et limites

- **56/56 contrôles ciblés** : niveaux, PM conservés hors groupe demandé, agriculture limitée, chimie, données d'État, scénarios de capacité, syntaxe et conservation des sources.
- Audit économique effectif : **26 204 références**, aucune cible manquante ou ambiguë, aucune erreur de parsing, aucun PM initial hors groupe ou prérequis de PM incompatible avec son bâtiment.
- **2 528 sources préexistantes** capturées : seuls les cinq fichiers annoncés diffèrent ; aucun nouveau fichier fonctionnel. Index et HEAD inchangés.
- Le contrôle TECH global des deux pays conserve des constats antérieurs, détaillés dans `TECH_AFTER.json` et comparés aux PM des préimages dans `TECH_NON_REGRESSION_R2.json`. Il ne doit pas être présenté comme un PASS global. Les trois ports irlandais restent notamment signalés pour `pm_basic_port` sans `enclosed_dock_systems` ; aucune activité ou panne de ces ports n'est déduite de ce seul signalement statique. Aucune technologie n'est attribuée pour masquer cette dette.
- Une première préparation a détecté, avant toute installation, des offsets incompatibles entre lecture normalisant CRLF et lecture conservant les octets. La préparation a été reprise en conservant les fins de ligne ; les cinq candidats ont ensuite été parsés, relus et installés sous garde d'empreinte. Aucun candidat invalide n'a été écrit dans le jeu.

Preuves : `OBSERVATIONS.json`, `BASELINE.json`, `before/`, `candidate/`, `PLAN.json`, diffs, `INSTALLATION_RECEIPT.json`, `SCOPE_VALIDATION.json`, audit économique et contrôles TECH. Aucun résultat moteur après installation ni acceptation humaine nouvelle n'est attesté.

Le premier rapprochement TECH reconstruisait toutes les sélections avec un autre ordre de lecteurs et produisait des écarts étrangers au lot ; il est conservé, mais ne sert pas de preuve de non-régression. R2 projette seulement les onze groupes effectivement modifiés sur leurs valeurs exactes avant intervention : mêmes six constats GBR et onze IREK, aucun constat ajouté ou retiré.
