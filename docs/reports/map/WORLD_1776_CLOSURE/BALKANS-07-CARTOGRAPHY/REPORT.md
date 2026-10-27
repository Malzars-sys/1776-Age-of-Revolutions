# B07 — Vérification finale ciblée des frontières balkaniques

26 octobre 2026. Référence 1er janvier 1776. Périmètre autorisé : carte et propriétaires uniquement, aucun ajout de personnage ou bâtiment.

## Résultat

Une erreur ponctuelle est corrigée : la cellule insulaire isolée (4503,1065), anciennement VEN/x11A0E0, passe à RAG/xE8D201. Elle appartient au groupe des Élaphites, entre Mljet et la côte ragusaine ; identification au niveau de l’archipel, pas d’affirmation géodésique d’une île individuelle. La carte Carter reproduite par Allcock p.20 et la carte de Marinković p.17, déjà archivées en B02 et relues visuellement, montrent l’appartenance ragusaine. L’Encyclopédie croate confirme que les Élaphites font partie du territoire originel ragusain : https://www.enciklopedija.hr/clanak/dubrovacka-republika .

Un seul pixel existant recolorié ; aucun RGB, pays, terre ou mer nouveau. Les historiques d’États, populations, bâtiments, technologies, institutions et unités sont tous conservés. Les 30 000 habitants déjà calibrés de la portion RAG ne sont pas gonflés pour ce correctif : aucun recensement insulaire individuel n’est prétendu. Monde avant/après : 837 336 539, delta nul.

## Vérifications demandées

| Secteur | Conclusion cartographique |
| --- | --- |
| Lastovo | Appartenance à Raguse confirmée ; pas de terre identifiable à son emplacement relatif au sud de Korčula dans le bitmap actuel. Omission du fond géographique, pas une province existante à réattribuer. Aucune île fabriquée sur la mer. Source municipale : https://lastovo.hr/opcina-lastovo/povijest-lastova/ ; carte Carter/Allcock relue. |
| Pelješac–Korčula | Raccord terrestre artificiel du dessin natif confirmé. La partition politique B02 reste conservée ; le raccord n’est pas supprimé par un canal inventé. Il relève d’une réfection cohérente du littoral et des hauteurs, pas d’une nouvelle souveraineté démontrée. |
| Corfou | Composante de 62 pixels x4B79CA, VEN conservé. |
| Leucade, Céphalonie et Zante | Composantes de 23,76,47 pixels x405060, VEN conservé. |
| Ithaque | Non isolée de façon suffisamment sûre dans le dessin céphalonien ; aucune attribution distincte forcée. La municipalité confirme Venise 1500–1797 : https://www.ithaca.gr/en/home/culture-environment/educational-cultural-istitutions/ . |
| Paxos et Strophades | Pas de composante terrestre séparée sûrement identifiée dans les secteurs attendus. Limite de représentation, aucune annexion à partir d’un pixel continental supposé. Contexte vénitien des sept Ioniennes : N.N. Patricios, ICOMOS, https://www.icomos.org/public/publications/wash97.pdf (extrait indexé, PDF non archivé ici). |
| Cérigo | Les 33 pixels B04/xE8D215 restent VEN. |
| Anticythère / îlot oriental | Le pixel (4636,1237) de x0055D7 reste non identifié avec assez de certitude ; pas de transfert arbitraire. La notice du projet archéologique atteste le contexte vénitien de Cerigotto, mais ne résout pas ce pixel : https://antikytheraexcavation.gr/en/istoria/ . |

Les listes de composantes et boîtes dans COMPONENTS.json, et les diagnostics temporaires .asset-cache/BALKANS-07/, distinguent géométrie observée et identification historique. Les limites restantes sont exposées ; aucune clôture cartographique intégrale ou validation moteur n’est inventée.

## Contrôles et concurrence

14/14 contrôles statiques réussis : unique pixel autorisé, couleurs et dimensions, propriétaire des deux RGB existants, terre/mer, populations, état Git, hauteurs et autres fichiers fonctionnels conservés, anciennes preuves WORLD. Une première trace 13/14 est archivée : sept documents/logs de la campagne SERG de clôture ont évolué extérieurement. Leur contenu a été relu, leurs empreintes et copies exactes sont dans EXTERNAL_SERG_REVIEW.json ; aucune réinitialisation, attribution de travail ou validation humaine WORLD induite.

Pas d’écriture Git, vanilla ou suivi SERG. Les contenus B01–B06 et TECH/ECON sont conservés. Aucun point régional supplémentaire pour ce contrôle ciblé ; les anciens dénominateurs et preuves restent intacts.

## Suite autorisée

Le joueur a arrêté les ajouts flavor et demandé explicitement : « Fais donc ces vérifications cartographiques. On passe ensuite au Maghreb. » Cette autorisation permet la transition directe P1→P4 sans se faire passer pour une validation en jeu. Les anciens protocoles de test demeurent en attente. Italie et Afrique subsaharienne ne sont pas lancées. Les omissions du fond de carte sont conservées comme limites, sans relancer les recherches institutionnelles balkaniques.
