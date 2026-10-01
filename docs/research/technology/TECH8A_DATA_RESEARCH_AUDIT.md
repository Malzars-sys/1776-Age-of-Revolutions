# Données et laboratoire de recherche — audit Tech & Res

Date : 2026-09-27. Audit de conception uniquement : aucun bien « données » ni laboratoire n'est ajouté au mod 1776 par cette passe.

## Sources contrôlées

Installation locale de Tech & Res (Workshop `3472248460`) : `common/goods/ztr_new_goods.txt`, `common/production_methods/ztr_data_production_methods.txt`, `common/production_methods/ztr_unique_buildings_production_methods.txt`, `common/production_method_groups/ztr_data_production_method_groups.txt`, `common/production_method_groups/ztr_unique_buildings_production_method_groups.txt`, `common/buildings/ztr_digital_buildings.txt` et `common/buildings/ztr_unique_buildings.txt`. Le premier audit général est `TECH1C_TECH_RES_SYSTEM_AUDIT.md` dans ce dossier.

## Ce que fait réellement Tech & Res

| Bien | Prix de base | Source ou transformation constatée | Utilisation importante |
|---|---:|---|---|
| `raw_data` | 5 | Les PM numériques « on premises » et Internet de plusieurs secteurs en produisent 6–16 par niveau ; ils exigent souvent logiciels et `business_data`. | Les centres de données en consomment 300 ou 450 par niveau ; le centre de recherche avancé en consomme 800. |
| `organized_data` | 10 | Les PM de rapport manuel des bâtiments primaires/industriels en produisent déjà 0,5–1,5 par niveau, sans données brutes ; un centre de données convertit 300 `raw_data` en 300 `organized_data` (ou 450/450). | Les bureaux en consomment 40–70 ; les centres de recherche de base et moyens en consomment 100 et 300. |
| `business_data` | 30 | Les bureaux convertissent 40–70 `organized_data` en 55–120 `business_data` ; certaines universités en produisent 2–5. | Plusieurs PM d'optimisation industrielle en consomment 1–6 et certains génèrent en retour des données brutes ou organisées. |

Les trois biens sont déclarés en catégorie `luxury`. `raw_data` et `organized_data` portent `traded_quantity = 0`, mais pas `tradeable = no` : il ne faut pas déduire automatiquement leur comportement commercial en jeu. À l'inverse, `business_data` possède `traded_quantity = 10`. Ce sont des valeurs à tester, pas un modèle économique à recopier.

La chaîne n'est **pas** linéaire : la documentation manuelle produit directement des données organisées, alors que les données brutes apparaissent surtout avec l'informatique. Le centre de données assure une seconde voie `raw_data → organized_data`. Les bureaux et l'optimisation créent ensuite une boucle avec les données commerciales. C'est approprié à la période numérique de Tech & Res, mais anachronique si l'on le reprend littéralement en 1776.

Le `building_research_center` de Tech & Res est non extensible et réservé à l'État. Son PM de base consomme 100 données organisées, 50 papier, 25 imprimés et 25 composants électroniques pour `country_weekly_innovation_add = 10` ; les PM supérieurs consomment davantage et apportent 25 ou 50 innovation. La spécialisation « future studies » ajoute `country_weekly_innovation_max_add = 40`. D'autres spécialisations donnent +15 % de vitesse de recherche d'une catégorie. Ces spécialisations n'ont pas leur **propre** consommation supplémentaire de données : elles s'appuient seulement sur le PM de base sélectionné. L'obtention du bâtiment passe par décision/site/journal et un rattrapage scripté de l'IA, mécanisme complexe à éviter pour un laboratoire ordinaire.

## Recommandation pour 1776

1. Donner aux « données brutes » un sens historique : observations, relevés et registres issus des administrations, ports, universités, bureaux statistiques et éventuellement grandes exploitations. Démarrer avec des producteurs existants, sans attendre un nouveau bâtiment. Un PM de relevés bon marché doit garantir une offre initiale.
2. Faire des « données organisées » un vrai traitement : un PM de compilation aux bureaux statistiques ou universités consommerait données brutes + papier et emploierait commis/savants. Le ratio et le prix doivent laisser un chemin de démarrage rentable sans demande déjà présente du laboratoire.
3. Faire débloquer un laboratoire par `experimental_research_laboratories` (ère 5), puis y consommer les données organisées et des biens déjà produits. Le laboratoire pourrait ajouter au plafond d'innovation avec `country_weekly_innovation_max_add` et à la vitesse de recherche avec `country_tech_research_speed_mult` ou une spécialisation par catégorie. Ces clés existent dans les définitions de modificateurs du jeu. Le bonus fixe actuel de +5 au plafond sur la technologie devra alors être réexaminé pour éviter un cumul involontaire.
4. Séparer « plafond d'innovation » et « vitesse de recherche » dans l'équilibrage : le premier ne génère aucune innovation tout seul. Vérifier aussi l'interaction avec les universités, qui en produisent déjà. Les bonus devront dépendre des emplois effectifs et devenir faibles ou nuls si les données manquent.
5. Tester en jeu l'ordre de démarrage producteur → compilateur → laboratoire, les pénuries, le commerce des données, l'IA, les charges budgétaires et l'effet sur les pays peu alphabétisés. Ne pas reprendre les quantités massives, les biens numériques ou la construction forcée par événement de Tech & Res.

Décision de cette passe : **audit terminé, laboratoire non implémenté**. La création des biens, des PM et du bâtiment exige un chiffrage et un test de partie séparés.
