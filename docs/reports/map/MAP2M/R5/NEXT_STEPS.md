# Suite ciblée et reproduction locale

## Ce qui est disponible maintenant

Profil régional natif empirique, inverse et domaine : `TRANSFORMATIONS.json`. Données de contrôle natives distinctes des sources politiques : `CONTROL_POINTS.csv`. Originaux et correction séparée d'Usedom : `NATIVE_CONTROL_OBSERVATIONS.json`, `REVISED_CONTROL_OBSERVATIONS.json`. Quatre vrais contrôles d'origine, plus un contrôle révisé explicitement séparé : `INDEPENDENT_VALIDATION.csv`.

R3/R4 et tous les fichiers fonctionnels sont préservés. Ne pas relancer la capture en remplaçant une référence. Il n'y a pas de transfert prêt à importer : `TERRITORIAL_CHANGES.csv` est vide et les244candidates ne contiennent aucunA.

## Commandes de lecture du profil

Depuis le dépôt, avec le même Python disposant deNumpy/Pillow :

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python docs/reports/map/MAP2M/R5/query.py geo 13.692 53.856
python docs/reports/map/MAP2M/R5/query.py pixel 4408.2 741.1
```

Les résultats sont approximatifs. Une requête extérieure au support convexe est refusée par défaut ; le suffixe `--allow-extrapolation` ne sert qu'à une lecture diagnostique explicitement consentie, pas à étendre la validité historique.

## Reproduction des calculs, sans réseau

Les sources requises restent dansR3/R4 ; aucune nouvelle acquisition extérieure, aucun changement de modèleColGrep ou d'intégration n'est nécessaire.

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python docs/reports/map/MAP2M/R5/work.py scout
python docs/reports/map/MAP2M/R5/work.py geo_read
python docs/reports/map/MAP2M/R5/work.py controls
python docs/reports/map/MAP2M/R5/work.py native_fit
python docs/reports/map/MAP2M/R5/work.py revised_controls
python docs/reports/map/MAP2M/R5/work.py revised_fit
python docs/reports/map/MAP2M/R5/review.py models
python docs/reports/map/MAP2M/R5/review.py pfau_audit
python docs/reports/map/MAP2M/R5/review.py mayer
python docs/reports/map/MAP2M/R5/review.py border_screen
python docs/reports/map/MAP2M/R5/finish.py images
python docs/reports/map/MAP2M/R5/finish.py anklam_chain
python docs/reports/map/MAP2M/R5/finish.py unresolved
python docs/reports/map/MAP2M/R5/finish.py validate
```

`work.py capture` est volontairement absent de cette liste : il sert seulement à la capture initiale et refuse de remplacer `BASELINE.json`. Les étapes ci-dessus n'écrivent que dansR5. Elles ne modifient niR4 ni les fichiers du jeu.

## Prochaine action utile par obstacle

1. **Natif :** employer ce profil pour localiser grossièrement des objets ; fixer de nouveaux contrôles finaux avant toute nouvelle sélection de modèle. Conserver ceux horsajustement, et noter les zones extrapolées. Ne pas annoncer une précision uniforme de2pixels.
2. **Peene :** lire des homologues physiques sur les cartes conservées au voisinage deDemmin/Anklam/Wolgast. Le contrôle doit porter sur le même objet et non sur la rivière la plus proche. Garder la distinction côte/bras d'eau, frontière historique et cellule réalisable. Ne pas allouer une province entière àPeendamm.
3. **Pfau :** résoudre les identités des édifices d'Inowrocław/Pakość par une configuration de rues/eau et un site historique déterminé. L'audit élimine une simple rotation comme cause unique ; il ne tranche pas identitécontre déformation. Ne pas refitter les trois mêmes croix provisoires ou absorber les deux contrôles pour obtenir un joli score.
4. **N1146/1 :** les deux rectos intégraux sont déjà acquis dansR4. Identifier précisément la ligne souveraine, distinguer les annotations privées et les ajouts. Recaler séparément les deux rectos sur de vrais objets physiques, vérifier des raccords non utilisés pour l'ajustement. Pas de collage àl'œil, pas de frontière1777 substituée à1776.
5. **Inowrocław méridional :** la couverture politique datée reste lacunaire. Le nouveau profil natif seul n'autorise pas de transfert à partir d'un nom de ville.

## Condition d'une future installation

Reclasser A seulement une portion réunissant souveraineté datée, ligne lue sur une source, géoréférencement contrôlé indépendamment et décision stable à l'échelle des cellules. Vérifier ensuite RGB/State_ID partagés, propriétaires, population/cultures/religions, bâtiments/PM/propriétaires économiques, unités/recrutements et références. Conserver les 357/85/142 cellules de référence tant qu'aucune correction précise n'est justifiée.

Ni la vérification mathématique du profil ni les empreintes d'intégrité ne remplacent un lancement deVictoria3. Une future partie devra tester les seules modifications réellement installées ; il n'y en a aucune dansR5. Aucun commit, merge, reset, push ou changement d'index/branche ne fait partie de cette suite.
