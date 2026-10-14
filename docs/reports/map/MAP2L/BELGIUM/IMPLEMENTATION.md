# Lot belge impérial — appliqué le 13 octobre 2026

## Résultat et périmètre

Deux États impériaux autonomes sont désormais définis au démarrage : la principauté de Liège (`LGE`) et Stavelot-Malmedy (`STM`). Les Pays-Bas autrichiens (`BEO`) conservent les autres possessions représentées dans le lot. Liège possède aussi sa partie de Looz dans la région économique de Flandre.

Les quatorze provinces natives sont subdivisées en 51 identités, soit 37 nouvelles couleurs de provinces. Les frontières souveraines ont été redessinées ; les deux grandes régions économiques natives sont conservées. Les provinces restent dans leur région d’origine et chaque nouveau morceau hérite du terrain de sa province parente. Les locators existants restent sur leur couleur déclarée ; celui de Liège appartient désormais à Liège.

L’intégration comprend les gouvernements ecclésiastiques, les noms français et anglais, les dirigeants identifiés, l’appartenance initiale au bloc, les liens impériaux et les mécanismes de rétrocession. Les titres électoraux existants sont inchangés : ces deux États ne reçoivent pas un titre électoral supplémentaire. Les pacts et dépendances historiques préexistants ne sont pas modifiés.

## Conservation des données

- Population mondiale : 835 804 980 habitants, avec conservation de chaque culture, religion et profil écrit par région économique.
- Répartition des anciens pools belges : 2 560 935 habitants restent à BEO ; 298 989 sont attribués à Liège ; 13 236 à Stavelot-Malmedy. Allocation démographique de jeu proportionnelle aux surfaces, pas un recensement historique de ces principautés.
- Les 137 881 habitants du pool luxembourgeois précédemment rétabli sont entièrement conservés sous BEO.
- Tous les niveaux de bâtiments, méthodes de production et autres attributs pondérés par niveau sont conservés. L’administration civile wallonne attribuée à Liège passe à son gouvernement ; les détenteurs économiques privés restent inchangés.
- Aucune formation ni unité militaire ajoutée ou retirée. Les nouveaux États peuvent développer leurs forces en jeu ; aucun contingent historique non documenté n’a été inventé.

## Carte impériale et registres

Le registre MAP2K d’origine est conservé octet pour octet. Le registre actif MAP2L enregistre 315 identités impériales, avec les bénéficiaires propres à chaque territoire. Les scripts de restitution et les compteurs du journal ont été recompilés à partir de ce registre.

La carte jaune principale et la carte du journal ont été régénérées. L’étendue impériale est exactement la même qu’avant cette passe ; seul le découpage interne et la souveraineté locale changent. Les deux nouveaux membres sont inclus dans les filtres constitutionnels, sans devenir des sujets autrichiens et sans malus de cohésion pour leur indépendance.

## Précision et limites explicites

La géométrie est une **approximation documentée à l’échelle du jeu**. Les contours sont issus de l’atlas historique de Wallonie de 1789, confronté au corpus Ferraris des années 1770 pour l’existence des juridictions. Ce n’est pas un relevé cadastral certifié au 1er janvier 1776. Le calage conserve les proportions et n’agrandit pas les enclaves pour les rendre visibles ; les artefacts d’un pixel isolé sont abstraits.

Le calage utilise les symboles de Bruxelles et Liège ; la lecture indépendante approximative de la confluence de Namur donne un écart d’environ 1,02 pixel du jeu. Les localités et enveloppes natives restent elles-mêmes simplifiées. Aucune extension vers des provinces appartenant à un autre pays n’est imposée : le condominium de Maastricht et les fragments étrangers ne sont pas arbitrés par ce lot. Bouillon et Saint-Hubert conservent leur représentation actuelle, en attente d’un examen juridique et géographique séparé.

Les bannières ecclésiastiques sont des signes d’identification procéduraux utilisant les éléments natifs, pas des drapeaux territoriaux historiques certifiés. L’identité de François-Charles de Velbrück et de Jacques de Hubin est sourcée ; l’âge de Hubin (68 ans) est une estimation de gameplay, pas une naissance vérifiée.

## Vérifications et démarrage

`VALIDATION.json` distingue les contrôles statiques et les modèles de régression d’un essai réellement effectué dans le moteur. Le test graphique hors jeu vérifie le masque, les textures et le compilateur de la fonction graphique ; il ne prouve pas à lui seul que le moteur accepte les nouveaux pays et toutes les nouvelles provinces.

**Pour tester : redémarrer complètement le jeu et commencer une nouvelle partie avec le mod principal. Ne pas utiliser une ancienne sauvegarde comme test de ce redécoupage**, puisqu’elle conserve les pays et historiques précédents. Aucune sauvegarde, configuration du lanceur, sélection de playset ni dépôt distant n’a été modifiée par cette passe.

La Franconie, les possessions rhénanes détaillées et le reste du rework impérial ne sont pas terminés.

## Sources

- [Atlas historique de Wallonie, Liège et Pays-Bas autrichiens en 1789](https://connaitrelawallonie.wallonie.be/histoire-et-symboles/histoire/atlas-historique/principaute-de-liege-et-pays-bas-autrichiens-la), Institut Destrée / SEGEFA, carte 2013 : géométrie de comparaison, limites chronologiques indiquées ci-dessus.
- [SPW, Ferraris 1770–1778](https://geoportail.wallonie.be/catalogue/b8b9e555-a4d1-49bf-940d-31bbbf7613fc.html) : extraits conservés dans `EVIDENCE`, avec leurs paramètres et empreintes ; cette carte topographique ne tranche pas seule les souverainetés contestées.
- [Université de Liège, mandement de François-Charles de Velbrück de 1772](https://donum.uliege.be/handle/2268.1/2513) : prince-évêque et année de naissance 1719.
- [P. George, documents sur le trésor de Stavelot-Malmedy, 1987](https://orbi.uliege.be/bitstream/2268/101442/1/bcrh_0001-415x_1987_num_153_3_1290.pdf) : notice de Jacques de Hubin, élu le 27 novembre 1766, mort le 22 décembre 1786.
