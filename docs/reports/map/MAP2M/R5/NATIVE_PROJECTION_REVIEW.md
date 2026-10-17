# Passage géographique → bitmap natif

## Informations explicites trouvées

Ressources installées inspectées en lecture seule :

- `C:/Games/Victoria 3/game/map_data/default.map` : fichiers provinces/rivières/topologie, `wrap_x=yes`, RGB des mers et des lacs. Le mod ne fournit pas de `default.map` de remplacement.
- `heightmap.heightmap` : hauteur originale16384×7232, indirection, compression/tuiles ; le bitmap provincial et celui des rivières mesurent8192×3616. Le facteur2 est une relation de résolution, pas une projection géographique.
- `common/defines/00_graphics.txt:227–228` : position graphique d'équateur0,58 et répétition de texture. Ce n'est pas une formule latitude→Y.
- Recherche ciblée dans les defines et shadersFX : matrices de caméra et de rendu, pas de formule géodésique documentée dans les ressources inspectées. Cela ne démontre pas l'absence d'une formule dans un outil de production ou un code moteur non consulté.

L'ancienne hypothèse Miller isotrope, Greenwich au milieu et offset rigide n'est pas promue comme projection exacte. Le bouclage horizontal ne démontre pas à lui seul une longitude linéaire ou un méridien d'origine.

## Mesures natives et contrôle des biais

La terre/mer est lue depuis les RGB physiques de `default.map`, **pas les propriétaires politiques**. Les rivières natives sont extraites des indices3à11 de la paletteP effectivement inspectée, avec les petites largeurs incluses. Les images de lecture sont produites sans superposition d'un modèle préalable.

Les caps sont identifiés par leur forme et leur extrémum dans deux fenêtres distinctes, réelle et native ; aucun plus-proche-rivage à une prédiction n'est choisi pour minimiser un résidu. Les fenêtres et règles sont enregistrées. Leur caractère schématique est inclus dans les limites ; ce ne sont pas des observations géodésiques.

L'erreur d'identification initiale d'Usedom reste visible dans `NATIVE_CONTROL_OBSERVATIONS.json` et les premiers résultats. La fenêtre sélectionnait la pointe sud de Rügen. La correction est documentée par `USEDOM_IDENTIFICATION_REVIEW.png`, séparée dans `REVISED_CONTROL_OBSERVATIONS.json`, jamais utilisée comme ancrage et jamais comptée parmi les quatre contrôles originaux.

Le confluent Warta–Oder reste réservé. Un confluent distinct au sud-est, basseNarew/Bug–Vistule, devient un nouvel ancrage. Le nom de la voie continue est `Bug` dans NaturalEarth ; le réseau et sa jonction avec la Vistule sont identifiables dans le raster. Les formes et régularisations modernes ne constituent pas des limites politiques de1776.

## Modèles comparés et profil retenu

Comparaison : affine géographique6paramètres ; affine en coordonnées Miller6paramètres ; axes séparés géographiques4paramètres ; axes séparés en baseMiller4paramètres. Le choix d'une baseMiller dans deux variantes ne prouve pas qu'elle soit la projection du jeu. Les paramètres sont entièrement ajustés aux observations, sans imposer l'ancien offset.

Le profil de diagnostic le plus simple retenu est :

```text
X = 4092.4925269824366 + 23.057991056249843 × longitude_en_degrés
Y = 2410.485279266792  - 30.99674943247102  × latitude_en_degrés
```

Ce sont des coordonnées image, Xversladroite/Yverslebas. Les cellules ont des indices entiers ; leurs centres sont(X+0,5;Y+0,5). Les observations de côte peuvent être des arêtes, pas des centres de cellules. Le profil n'est pas une loi mondiale et ne doit pas servir à justifier la souveraineté d'une province.

Sur quatre contrôles d'origine exclus de l'ajustement : moyenne2,0756px ; maximum3,1867px. La correction d'Usedom est un cinquième diagnostic séparé à0,17px. Les sixparamètres des affines ne sont pas préférés pour leurs faibles résidus d'ajustement : le premier affine côtier échoue fortement au contrôle méridional, et même après ajout du nouvel ancrage il conserve un écart réservé maximal d'environ5,83px. Les variantes restent exportées.

Le choix utilise les résultats de validation, donc un test extérieur final indépendant de cette sélection demeure souhaitable. La moyenne observée n'est pas un intervalle statistique de confiance. L'intérieur de l'enveloppe convexe n'est pas uniformément certifié ; l'extérieur est une extrapolation. `query.py` refuse cette dernière par défaut.

## Sensibilité à six cibles — pas précision certifiée des villes

| Cible diagnostique | X/Y estimés | Retrait d'un ancrage, déplacement maximal | Perturbations de lecture, maximum | Désaccord maximal des4modèles |
| --- | --- | ---: | ---: | ---: |
| Anklam |4408,20 /741,12|1,32px|0,95px|0,88px|
| Wolgast |4410,14 /735,05|1,30px|0,94px|0,52px|
| Wałcz |4472,26 /759,29|1,29px|1,03px|1,18px|
| Kamin |4496,47 /751,23|1,34px|1,02px|0,47px|
| Bromberg |4507,54 /763,63|1,63px|1,05px|1,02px|
| Inowrocław |4513,53 /774,01|1,86px|1,10px|1,53px|

Ces maxima sont issus de sélections et perturbations finies, avec rayons de lecture déclarés pour chaque ancrage ; ils ne couvrent pas une mauvaise homologie ni tous les changements historiques de paysage. Ils ne doivent pas être additionnés puis appelés « confiance95% ». Les coordonnées arrondies des villes ci-dessus servent de diagnostics, pas de nouveaux pointsFIT/CHECK, et aucune attribution de RGB n'en découle.

Profil, paramètres, rôle des points, support convexe, comparaisons et sensibilité : `TRANSFORMATIONS.json`, `CONTROL_POINTS.csv`, `INDEPENDENT_VALIDATION.csv`. Images d'observations : `NATIVE_CONTROL_REVIEW.png` et images `NATIVE_*_READING.png`.
