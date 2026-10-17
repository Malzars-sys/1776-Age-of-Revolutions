# Suite conditionnée au choix du joueur

## Reproduction locale

Depuis la racine du dépôt, avec le Python disposant de Numpy et Pillow :

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python docs/reports/map/MAP2M/R7/arbitration.py options
python docs/reports/map/MAP2M/R7/arbitration.py source_views
python docs/reports/map/MAP2M/R7/arbitration.py evidence
python docs/reports/map/MAP2M/R7/arbitration.py images
python docs/reports/map/MAP2M/R7/arbitration.py validate
```

Ces commandes n'écrivent que dans R7. Elles utilisent les sources locales déjà acquises et ne relancent aucun ajustement. `capture` n'est pas à répéter : il refuse de remplacer la baseline et les règles initiales. Conserver toutes les baselines R1–R6.

## Si le joueur approuve A ou B

1. Enregistrer la décision explicite avec la variante, les pixels exacts du CSV, la catégorie **B_APPROVED_APPROXIMATION**, les sources et les simplifications. Ne jamais les transformer rétrospectivement en catégorie A certifiée.
2. Revérifier l'état du workspace avant installation ; préserver toute modification du joueur/collaborateur. Les chiffres de 360 ou 398 cellules suédoises sont des **prévisions**, pas la baseline actuelle de 357.
3. Préparer une modification limitée à ces pixels et aux seules dépendances réellement nécessaires. Les RGB source/cible existent déjà dans STATE_POMERANIA : ne pas inventer de province, TAG ou State_ID. Ne pas additionner A et B.
4. Examiner les sous-États PRU/SWE partagés, populations par culture/religion, bâtiments/PM, propriétaires économiques, infrastructures, unités et recrutements. Toute redistribution nécessaire doit être déterministe, conservatrice des totaux et déclarée comme allocation technique, pas population historique inventée. Ne pas annoncer cette étape accomplie pendant R7.
5. Conserver les protections Anklam/Peendamm, Demmin, Usedom/Wollin, Thorn et tous les autres lots. Le centre provisoire de Wolgast n'est pas un locator à déplacer sans vérification spécifique.
6. Relancer les validations cumulatives, produire le vrai avant/après installé et demander ensuite la vérification manuelle en nouvelle partie. Une validation statique de proposition n'est pas un test moteur.

## Bromberg : pas d'installation ni de nouveau recalage automatique

Le contre-contrôle Szubin révèle une question de datation/identification politique. La prochaine preuve utile serait un acte/tracé antérieur à janvier 1776 incluant le secteur méridional après 1773, ou une histoire de révision identifiant exactement les portions encore valables du liseré. Ce besoin est distinct d'une nouvelle recherche générale de cartes déjà examinées.

Sans cette preuve : conserver les 85 cellules PRU et les 142 PLC, les candidates C et Thorn inchangée. Ne pas employer un nom rouge de propriété ou le seul coude de la Vistule pour décider une souveraineté. Ne pas substituer des acquisitions de 1793 ou un tracé de 1777 à la date cible.

Aucun commit, merge, push, reset ou changement d'index/branche n'est autorisé par cette procédure. Attendre le choix du joueur avant toute mutation fonctionnelle.
