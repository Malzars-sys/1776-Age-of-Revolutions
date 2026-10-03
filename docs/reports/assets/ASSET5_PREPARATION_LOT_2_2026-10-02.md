# Lot 2 proposé : phosphate et traitement des minerais

Date : 2 octobre 2026. Statut : préparation uniquement. Aucun visuel généré,
aucun DDS exporté et aucune définition de gameplay modifiée pendant cette passe.

## Point de départ vérifié

Les quinze illustrations des trois unités militaires sont intégrées : cinq
mousquetiers, cinq bombardes V3 et cinq canons de campagne. Les sept assets
fournis du calcaire/ciment sont aussi intégrés. Quatre propositions du premier
lot attendent encore leur accord propre : cimenterie, ciment naturel, ciment
hydraulique et ciment Portland. Leur création n'est pas à recommencer d'office.

Le cahier des charges ASSET4 plaçait le phosphate/extraction en tête de la
suite. Les définitions actuelles confirment ce besoin : le bien, la mine,
Minéralogie appliquée et les deux PM de traitement du phosphate sont encore
provisoires. Levé géologique emploie un aperçu Morgenröte dont l'autorisation
de redistribution reste non établie dans le registre ASSET3 ; le lot propose
une création originale, pas une copie ou adaptation de cet asset tiers.

## Six images nouvelles

| Famille | Objet | Composition proposée |
|---|---|---|
| Bien | Phosphates | Roches mates brun-sable/ocre gris, isolées ; distinctes du calcaire pâle et du soufre jaune. |
| Bâtiment | Mine de phosphate | Extraction, treuil et wagonnet discrets ; phosphate au premier plan dans un cadre métallique patiné. |
| Technologie | Minéralogie appliquée | Échantillons de minerais et petite loupe d'observation ; objets peints, sans cadre ni décor. |
| Technologie | Levé géologique | Feuille montrant une coupe des couches rocheuses et petit compas, sans texte lisible. |
| PM | Tri manuel | Main stylisée sélectionnant des fragments ; méthode active, donc pas un pictogramme barré. |
| PM | Concentration des minerais | Bac/crible de séparation et fragments triés ; même famille visuelle que Tri manuel. |

Le bien fixe la forme et la palette du phosphate représenté devant la mine.
Les technologies montrent le savoir-faire, les PM le procédé : un même tas de
roches ne doit pas devenir l'unique image des quatre familles.

## Ordre de fabrication

1. Phosphates : valider la matière et sa lecture au marché.
2. Mine : reprendre le bien validé, tout en conservant la grammaire des
   bâtiments vanilla.
3. Minéralogie appliquée : valider la grammaire des technologies.
4. Concentration des minerais : valider la grammaire des PM.
5. Tri manuel : dériver une méthode nettement distincte, pas un état inactif.
6. Levé géologique : conserver le langage des technologies, sans ressembler à
   Minéralogie appliquée.

Présenter les pilotes avant les dérivés et l'intégration. Aucun lancement de
génération n'est compris dans cette préparation.

## Raccordements et réemplois

La mine est débloquée par `applied_mineralogy` ; la concentration par
`geological_surveying`. Les technologies restent respectivement en ère III et
VI dans le code. Ce travail visuel ne change ni ces ères ni leurs prérequis.

Les pompes atmosphérique, à condensation et Diesel, les explosifs et le
transport possèdent déjà leurs références vanilla. Ils restent en place.
Il n'y a pas de commande pour une nouvelle technologie « Phosphate » : cet
identifiant n'existe pas comme nœud dédié dans la chaîne vérifiée.

Les deux PM génériques pourraient ensuite servir aux mines de charbon, fer,
plomb, soufre et or : dix autres PM provisoires vérifiés. Cela permettrait
de couvrir seize objets avec six images, sans dix créations supplémentaires.
Ces raccordements sont une extension proposée séparément, pas une mutation
automatique autorisée par ce brief. Les mines de cuivre et de bauxite ne sont
pas comprises dans cette liste de raccordements.

Les identifiants, définitions consommatrices, textures actuelles, prérequis et
chemins futurs sont dans le [manifeste du lot](ASSET5_LOT_2_PHOSPHATE_MINERAIS_2026-10-02.json).
Les six chemins de sortie étaient libres lors de la vérification. Une future
intégration doit vérifier à nouveau leur disponibilité et cibler les
identifiants explicitement, sans remplacement global dans un fichier partagé.

## Direction artistique et réception

Références vanilla réexaminées dans la planche ASSET4 : fer/soufre pour les
biens ; mines de charbon/fer pour le bâtiment ; technologies d'objets peintes ;
pics et pelles/pompes pour le bas-relief des PM. Les nouveaux PM utilisent
une palette ocre/beige patinée. Le violet déjà choisi pour les PM du ciment
n'est pas modifié ; il ne devient pas automatiquement la palette de ce lot.

Masters PNG carrés d'au moins 1024 pixels. Exports proposés : 256 × 256 et neuf
mipmaps pour biens, bâtiment et technologies ; 208 × 208 et huit mipmaps pour
les PM. Alpha réel pour les objets ; scène opaque dans le cadre du bâtiment
et transparence uniquement à l'extérieur. Aucun fond noir factice.

Contrôler les biens/PM à 32 et 48 pixels, les technologies à 48/64 et le bâtiment
à 48/64/96. Deux sujets au maximum par pictogramme, contours propres, pas de
texte, chiffres de niveau, médaillon technologique intégré, filigrane ou cadre
de bâtiment autour d'un bien. Les périodes exactes des appareils seront
documentées avant création si le rendu requiert un modèle historique précis.

Après accord : exports DDS, décodage indépendant, références résolues et
comparaison des définitions pour prouver que seules les images changent.
Les recettes, emplois, prix, technologies et statistiques sont hors périmètre.

## Hors périmètre et suite

La chaîne cuivre reste exclue. Les unités validées et les assets du laboratoire
ne sont pas refaits. Pas de modification de modèle 3D dans ce lot d'icônes.
Après le phosphate : produits pétroliers/raffinerie, puis autres technologies
et transports provisoires, selon le programme ASSET4.
