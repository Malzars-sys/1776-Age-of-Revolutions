# Pfau — Diagnostic causal, sans nouveau calage territorial accepté

Le modèle R4 de la feuilleXXXIX n'est pas réutilisé pour des transferts.

## Hypothèse nouvelle réellement testée

Une mauvaise orientation globale ou un mélange simple des axes pourrait-il expliquer les kilomètres d'écart ? R5 applique une rotation90/180/270° et une réflexion, **uniformément aux mêmes coordonnées source**, puis recalcule l'affine sur les trois anciens ancrages, sans absorber Inowrocław/Pakość dans l'ajustement.

Résultat : les contrôles réservés restent à **4250,79m et2127,62m**, et les prédictions entre cadres ne varient que d'environ2,3×10⁻¹¹m. Une affine absorbe ces rotations/reflets linéaires. L'échec ne se résout donc pas par une rotation générale, un signe d'axe ou une simple translation du repère. Ce test n'établit pas la projection historique et ne certifie pas les positions des églises.

Le format des images et les empreintes sont conservés : XXXIX est bien à4000×2822dans sa version acquise ; la conversion de lecture tournée180° reste(u=3999−x ;v=2821−y). Le calcul métrique emploie longitude/latitude en degrés dans un plan local en mètres, pas un passage involontaire degrés↔radians. Les tests mathématiques du nouveau code sont séparés de la preuve d'homologie.

## Ce que les données permettent, et ne permettent pas, d'identifier

Les trois paires d'ancrages Gniewkowo/Kruszwica/Strzelno impliquent environ15,77à16,41mètresparpixelsource. La paire provisoire Inowrocław–Pakość implique11,38mètresparpixel ; d'autres paires vont jusqu'à18,79. Un changement d'orientation ne change pas ces distances. Cela localise le problème dans la correspondance/figuration locale, pas dans le seul redressement de la page.

Cependant, des croix génériques d'églises et un toponyme ne démontrent pas quel édifice précis est représenté. Les points d'Inowrocław et de Pakość restent ambigus, et les identités exactes des trois anciennes croix d'ajustement ne sont pas toutes suffisamment établies. R5 **ne peut pas départager avec certitude** : mauvais édifice, symbole déplacé/généralisé ou déformation locale de la carte. Les distances ne sont donc pas annoncées comme une mesure certifiée de l'erreur de Pfau.

## Graduations, édition et raccords

Aucun graticule géodésique exploitable n'est identifié sur la feuille détaillée acquiseXXXIX. Le quadrillage des35sections de l'index est un découpage de feuilles, pas une preuve de coordonnées géographiques. Aucun méridien historique d'origine n'est supposé pour fabriquer de nouveaux points.

Les cinq feuilles utiles sont bien conservées ; aucun raccord physique commun n'est encore homologué de façon indépendante. Pas de mosaïque « géoréférencée » obtenue par collage visuel, pas de modèle par feuille ajusté à des noms de villages seuls. Les rotations de lecture ne garantissent pas un nord vertical exact.

Les relevés1772–1773 et la gravure/édition1778 ne sont pas interchangeables politiquement. Le manuscritAGAD AK103–107A reste catalogué1800–1815 dans l'inventaire consulté enR4 ; cette contradiction n'est pas escamotée.

## Action concrète suivante

Faire correspondre des objets physiques individualisés par leur configuration : plan de rue et position de l'église dans le bâti, pont et branches d'eau avec déplacement documenté, île ou site fixe plutôt qu'extrémité mobile de lac. Garder de nouveaux contrôles distribués horsajustement, notamment au voisinage de Pakość et de la limite méridionale, avant de recalculer. Si la lecture ne permet pas l'identification, conserver la portionC.

Pour N1146/1 : les deux rectos se recouvrent mais restent un seul objet ; les deux versos et la mire ne sont pas des cartes indépendantes. Le brouillon [1772], ses couleurs et les annotations de propriétés privées ne fournissent pas encore un tracé politique source→réel qualifié. Deutsch Krone/Kamin/Bromberg peuvent être réétudiés à partir de ces fichiers locaux ; la totalité du sud d'Inowrocław n'est pas couverte. **Aucune cellule supplémentaire n'est déduite d'une ligne non contrôlée** : les 77 anciennes candidates sont conservées en C pour la décision d'implémentation.

Preuves calculées : `PFAU_FRAME_AUDIT.json`. Ce fichier contient les variantes, résidus, distances entre paires et empreintes, pas un nouveau profil accepté. Aucun des anciens contrôles réservés n'est devenuFIT.
