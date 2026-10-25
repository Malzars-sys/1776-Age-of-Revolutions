# Équilibrage courant — quincaillerie

Statut : `IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION`. V1 archivée dans `V1_ARCHIVE/`.

Quantités par niveau pleinement employé et par semaine, sans débit, pénurie, impôt, frais financiers ou prix locaux. Prix du mod : quincaillerie 30, fer 40, cuivre 50, alliages 50, acier 50, plomb 40, aluminium 50 £. Salaires = emplois × poids de profession × salaire annuel d'ouvrier / 52. Le salaire de référence de 10 £ est une hypothèse, pas une observation du départ.

| Palier | Quincaillerie | Coût matière | Valeur produite | Emplois ajoutés | Ratio valeur/matière | Marge après salaires à 10 |
|---|---:|---:|---:|---:|---:|---:|
| Forgé/moulé | 20 | 360 | 600 | 500 | 1,667 | 139,04 |
| Cuivre/laiton | 40 | 640 | 1 200 | 850 | 1,875 | 382,12 |
| Usiné | 80 | 970 | 2 400 | 1 400 | 2,474 | 1 083,85 |
| Industrialisé | 160 | 1 860 | 4 800 | 2 200 | 2,581 | 2 334,23 |

Entrants, emplois, sorties et rendements augmentent. Les quatre marges restent positives à salaire 10 avec matières +25 %, le premier donnant +49,04 £. Si les matières montent de 25 % et le produit baisse simultanément de 25 %, le premier passe à −100,96 £. Aucun profit universel n'est promis.

Ce sont des marges du groupe secondaire : la manufacture entière conserve les autres coûts et recettes. Aucun meuble n'est produit par ce groupe. Le neutre enlève entièrement quincaillerie, matières et emplois associés.

Les paliers consomment 4/5/7/10 alliages ; une usine primitive à 20 n'approvisionne que 5/4/2,86/2 niveaux, avant toute autre demande. Les nouvelles sorties appellent donc un développement réel des usines et des mines. La quincaillerie doit trouver sa propre demande ; son prix peut baisser si le joueur produit trop.

## Cinq cas de calcul

Ce sont des hypothèses de niveaux, pas cinq pays simulés. Aucune quantité POP arbitraire n'est ajoutée.

| Cas | Usines alliages | Artillerie bronze | Quincaillerie : niveaux/palier | Offre alliages | Nouvelle demande industrielle d'alliages | Solde avant autres débouchés | Offre quincaillerie |
|---|---:|---:|---|---:|---:|---:|---:|
| Faible industrie, importation | 0 | 0 | 1 / forgé | 0 | 4 | −4 | 20 |
| Métallurgie européenne | 2 | 3 | 4 / cuivre | 40 | 32 | +8 | 160 |
| Puissance militaire | 4 | 10 | 5 / cuivre | 80 | 65 | +15 | 200 |
| Exportateur de quincaillerie | 6 | 2 | 20 / cuivre | 120 | 108 | +12 | 800 |
| Industrialisation V–VI | 20 | 10 | 40 / usiné | 400 | 320 | +80 | 3 200 |

Les industries avancées déjà présentes et les POPs s'ajoutent à la demande ci-dessus ; ces soldes ne sont pas des surplus mondiaux prédits. Pas d'estimation de retour sur investissement réel à partir de ces seules marges.

## Alliages préservés

Le procédé traditionnel conserve 20 alliages, 420 £ d'entrants, 580 £ de marge avant salaires et 2 200 emplois : +108,85 £ à salaire annuel 10. Son seuil salarial isolé reste environ 12,31 £/an. La combinaison initiale avec données industrielles donne +285,31 £ à salaire 10. Cette révision n'augmente pas ses entrants.

Les recettes avancées restent inchangées. Arc électrique : 90 alliages, 5 000 emplois, environ deux fois la productivité physique par emploi du procédé primitif ; sa marge isolée de −212,50 £ à salaire 10 était préexistante. Automatisation, autres groupes et prix peuvent la changer. Son rééquilibrage propre reste différé. Les procédés d'aluminium retirant 10/15 alliages restent compatibles avec la base de 20.

Données reproductibles : `HARDWARE_PM_MATRIX.csv`, `BASE_PRICE_STRESS.json`, `ALLOY_PRODUCTION_BEFORE_AFTER.csv`.
