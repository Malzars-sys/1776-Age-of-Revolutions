# Bilan statique du papier et du bois

Les valeurs ci-dessous sont des variations de capacité de base à plein emploi, exprimées en unités de biens par semaine. Elles ne sont ni une mesure de la production embauchée au premier jour ni un calcul du prix d’équilibre.

## Marchés concernés

Les historiques actuels font de l’Autriche la fondatrice du bloc impérial et inscrivent la Prusse, la Saxe et la Bavière parmi ses membres. L’identité `identity_aor1776_imperial_federation` porte `power_bloc_customs_union_bool = yes`. Les scripts prévoient donc un marché douanier impérial commun. Le résultat effectivement créé par le moteur, les accès locaux au marché et les effets éventuels des règles de partie restent à constater en partie. L’appartenance à un bloc seule ne serait pas une preuve suffisante sans ce modificateur.

Sources locales : `common/history/power_blocs/00_power_blocs.txt` et `common/power_bloc_identities/1776_imperial_federation.txt`.

| Pays producteur | Papier supplémentaire | Bois supplémentaire consommé | Variation de bois produit | Bois dur supplémentaire |
|---|---:|---:|---:|---:|
| Autriche | +160 | +120 | 0 | 0 |
| Prusse, retrait de Prusse-Occidentale compris | +80 | +60 | −50 | +20 |
| Saxe | +80 | +60 | +80 | 0 |
| Bavière | 0 | 0 | 0 | 0 |
| Total de l’intervention | **+320** | **+240** | **+30** | **+20** |

À facteurs constants, la demande nette supplémentaire de bois ordinaire est de **210 unités par semaine** : 240 de consommation papetière nouvelle moins 30 de production forestière nette. Le complément saxon fournit 80 unités de bois pour une consommation papetière nouvelle de 60. Les trois niveaux forestiers de Basse-Silésie apportent 120 unités de bois. La sélection de bois dur dans les deux niveaux de Haute-Silésie fournit 20 unités de bois dur et retire 50 unités de bois ordinaire par rapport aux mêmes camps sans cette sélection.

Les cinq niveaux forestiers prussiens déplacés ne constituent pas une création nette de capacité forestière nationale. La Prusse doit absorber simultanément sa consommation supplémentaire de papier-bois et la réduction du bois ordinaire liée au bois dur. L’Autriche ajoute quatre niveaux de papeterie sans nouveaux camps de bûcherons dans cette mission. L’approvisionnement depuis le marché commun, les stocks disponibles, la concurrence d’autres industries et les prix locaux conditionneront l’embauche réelle.

## Demande existante et travail

Les administrations, universités et autres méthodes consommatrices existantes sont conservées. Aucune demande de papier n’est supprimée pour fabriquer artificiellement un surplus. La collecte supplémentaire de données industrielles est explicitement désactivée dans les quatre nouvelles papeteries ; elle n’introduit donc pas de consommation de papier supplémentaire dans cette estimation.

Les papeteries ouvrent 50 000 postes dans les quatre régions cibles et en retirent 10 000 en Prusse-Occidentale, soit 40 000 postes nets avant les effets d’automatisation. Les populations écrites sont recensées dans `REPORT.md`. Les fichiers de départ ne donnent pas le chômage, la répartition professionnelle finale ni les qualifications après initialisation. Un volume de population suffisant ne garantit donc pas l’embauche immédiate. Aucun ajout démographique, subvention imposée ou déblocage technologique n’a été utilisé pour contourner cette limite.

## Prix et protocole

Le prix initial observé du papier avant intervention n’a pas été relevé dans une partie de référence. Il reste **non mesuré**, de même que le prix après un mois. Il n’est pas déduit des seules capacités écrites. Les prix de base des biens sont inchangés.

Les fichiers `BUILDING_INPUTS_BEFORE.json` et `BUILDING_INPUTS_AFTER.json` conservent les capacités, populations, bâtiments et coefficients de demande/offre utilisés dans cet audit. Ils corrigent le choix de méthode implicite en tenant compte de `is_default`, plutôt que de supposer que la première méthode du groupe est toujours celle du moteur.

Les primes de rendement, taux d’emploi, qualifications, pénuries d’intrants, salaires, méthodes choisies ensuite par l’IA, échanges et variations d’accès au marché ne sont pas simulés. Le test décrit dans `RUNTIME_TEST_PLAN.md` doit vérifier si l’augmentation nominale de papier devient une production effective et si le besoin supplémentaire en bois reste supportable.
