# MIL-FORT-ENGINEERS-1776 — Premier sous-lot A1

Date historique : **1er janvier 1776**. Livraison : **19 octobre 2026**.

Le premier sous-lot installe **12 niveaux simples**, répartis en **5 fortifications terrestres et 7 fortifications côtières**. Les États côtiers utilisent le bâtiment côtier existant, conformément à la dernière instruction du joueur. Aucun ouvrage ne reçoit les deux bâtiments.

| Pays | État du jeu / places retenues | Terrestres | Côtiers |
| --- | --- | ---: | ---: |
| France | Flandre française : Lille | 0 | 1 |
| France | Alsace-Lorraine : Strasbourg et Neuf-Brisach, regroupées | 1 | 0 |
| France | Franche-Comté : Besançon | 1 | 0 |
| France | Lorraine : Longwy | 1 | 0 |
| Grande-Bretagne | Home Counties : Portsmouth | 0 | 1 |
| Grande-Bretagne | Haute-Andalousie, subdivision britannique : Gibraltar | 0 | 1 |
| Espagne | Aragon : Jaca | 1 | 0 |
| Espagne | Estrémadure espagnole : Badajoz | 1 | 0 |
| Espagne | Basse-Andalousie : Cadix | 0 | 1 |
| Portugal | Alentejo : Elvas et Santa Luzia | 0 | 1 |
| Portugal | Beira : Almeida | 0 | 1 |
| Provinces-Unies | Hollande : Naarden | 0 | 1 |
| **Total** | **Un niveau par réseau régional retenu** | **5** | **7** |

Les ouvrages sont historiques ; leur conversion en un niveau régional est une convention de gameplay volontairement conservatrice. Cela ne signifie pas qu'une place occupait toute la région ou que toutes les places avaient la même garnison. Les sites intérieurs de Lille, Elvas ou Almeida sont représentés par le bâtiment côtier parce que leur **État économique** possède une côte. Ce bâtiment conserve ses effets navals : le changement ne lui ajoute pas les bonus terrestres du fort intérieur.

## Vérifications préalables

Le classeur `Pays_forts_et_genie_1776.xlsx` a été ouvert en lecture seule. Le recoupement des **466 pays présents** confirme **95** technologies de fortifications, **74** du génie, **69** pays ayant les deux et **100** au moins une. Les technologies ne sont pas des preuves historiques. Les 466 comparaisons figurent dans [TECHNOLOGY_CROSSCHECK.csv](TECHNOLOGY_CROSSCHECK.csv).

Les bâtiments, PM, technologies, unités, illustrations, restrictions côtières et mécanismes de bataille préexistants ont été relus et conservés. Les nouvelles implantations utilisent seulement le PM simple. Aucun fort renforcé ou avancé n'est accordé au départ.

## Génie et cas suspendus

**Aucun nouveau bataillon du génie n'est accordé dans A1.** Le bataillon du jeu peut recruter 1 000 hommes. Le service d'officiers espagnol ne constitue pas un tel bataillon ; la compagnie britannique de Gibraltar reste trop petite. La réforme française créant deux bataillons de pionniers est postérieure au 1er janvier 1776. Le régiment néerlandais est attesté, mais son effectif précis de 1776 reste à établir ; les compagnies françaises de mineurs et les organisations portugaises demandent également une recherche complémentaire. Cela n'empêche pas le recrutement ultérieur permis par les technologies existantes.

**Maastricht reste suspendue.** Le fort Saint-Pierre est admissible historiquement, mais le hub Maastricht correspond à `x0000DF`, dans la portion de `STATE_GELRE` attribuée à **BEO**. Le régime historique de condominium et la carte doivent être réconciliés. Aucun fort n'est distribué à un autre propriétaire ni placé ailleurs en compensation.

## État de livraison

Les deux nouveaux scripts sont isolés des historiques partagés. L'initialisation est limitée au premier jour du départ de 1776, avec protections contre les doubles appels et la réapparition d'un fort démoli. Les fichiers déjà présents du système militaire sont préservés ; les évolutions parallèles observées sur les fichiers et rapports du chantier autrichien/SERG sont consignées dans [EXTERNAL_CHANGES.json](EXTERNAL_CHANGES.json), sans restauration ni intervention sur ces fichiers.

Le résultat détaillé des contrôles se trouve dans [VALIDATION.json](VALIDATION.json). Les simulations de scripts sont **statiques**. Le démarrage réel du jeu, l'emploi, le budget, un mois de simulation et la sauvegarde/reprise restent à vérifier avec [PLAYER_TEST_PROTOCOL.md](PLAYER_TEST_PROTOCOL.md). Aucun reçu de validation utilisateur n'est créé.

Le sous-lot **A1** est livré pour ce test. Le reste du lot A, les autres continents et les déploiements du génie restent explicitement planifiés dans [REMAINING_WORK.md](REMAINING_WORK.md), conformément à la limite d'exécution demandée.

## Pièces de la livraison

- [FORTRESS_INVENTORY.csv](FORTRESS_INVENTORY.csv) : 85 entrées, dont candidats non encore étudiés clairement signalés.
- [ENGINEER_CORPS_INVENTORY.csv](ENGINEER_CORPS_INVENTORY.csv) : 75 pays à statut distinct ; aucune absence de preuve assimilée automatiquement à une classe D.
- [FORTRESS_PLACEMENT.csv](FORTRESS_PLACEMENT.csv), [ENGINEER_DEPLOYMENT.csv](ENGINEER_DEPLOYMENT.csv), [BEFORE_AFTER.csv](BEFORE_AFTER.csv).
- [HISTORICAL_SOURCES.md](HISTORICAL_SOURCES.md), [IMPLEMENTATION.md](IMPLEMENTATION.md), [BALANCE_REVIEW.md](BALANCE_REVIEW.md).
- [BASELINE.json](BASELINE.json), [SOURCE_HASHES.json](SOURCE_HASHES.json) : empreintes et références techniques pour la reprise.
