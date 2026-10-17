# MAP2W-R1 — Fulda : preuves et limites

Référence : 1er janvier 1776. Cette passe n’est pas une reconstruction générale supplémentaire du Rhin ou de la Souabe.

## Institution et souverain

Le prince-évêché de Fulda est absent des définitions effectives au début du lot. La présence de HEK dans le bitmap n’est pas une preuve de souveraineté historique. Le noyau temporel de Fulda est une principauté ecclésiastique, distincte des landgraviats hessois et de l’électorat de Mayence. L’élévation épiscopale de 1752 ne transforme pas son diocèse entier en territoire souverain.

- HIL, LAGIS, introduction au district de Fulda : développement du territoire temporel, élévation en 1752 et sécularisation en 1803. [Notice institutionnelle](https://www.lagis-hessen.de/de/subjects/browse/district/631/sn/ol).
- Hochschule Fulda, Janis Oberholz, « Heinrich von Bibra », 6 août 2026, sous les références de Thomas Heiler : gouvernement de Heinrich VIII von Bibra de 1759 à 1788, retour effectif en 1763 après la guerre, réunification urbaine symbolisée par le déplacement du Paulustor en 1771. [Notice et références](https://www.hs-fulda.de/hlsb/en/forschen-publizieren/citizen-science/fulda-faces-fulda-places/heinrich-von-bibra).
- [Catholic Hierarchy](https://www.catholic-hierarchy.org/bishop/bbibrh.html) : naissance le 22 août 1711, élection le 22 octobre 1759. La date de naissance est un paramètre de personnage, pas un argument territorial.

Le nouveau TAG FUL représente ce prince-évêché. Il n’est ni électeur, ni sujet natif de l’empereur. La théocratie est une abstraction du gouvernement capitulaire ; le mode de succession natif « dictatorial » ne simule pas exactement l’élection canonique.

## Carte et correspondance

Friedrich Uhlhorn, *Hessen im Jahre 1789*, carte 22 du *Geschichtlicher Atlas von Hessen*, livraison 4, 1962 ; commentaire d’Ulrich Reuling, 1984, p. 152–159. [Notice permanente HIL](https://lagis.hessen.de/resolve/de/ga/40). Image et métadonnées conservées dans EVIDENCE. Attribution HIL, **CC BY-SA 4.0**, y compris les extraits annotés.

La carte distingue par couleur le Hochstift Fulda, les territoires hessois, les possessions de Würzburg et les juridictions chevaleresques. Les pointillés internes ne sont pas tous des frontières souveraines. Le polygone bleu est volontairement intérieur à la couleur de Fulda : il n’est pas le décalque exhaustif du pays ni celui de l’évêché spirituel.

1789 est postérieur de treize ans à la date jouée. L’usage est limité au noyau Fulda–Neuhof dont la continuité institutionnelle est établie sous le même souverain ; aucune acquisition de la sécularisation de 1802–1803 ou du partage de 1815 n’est importée. Les franges et les possessions détachées n’ont pas la même justification et restent différées. Cette inférence de continuité justifie une classe **B**, pas une frontière de classe A.

Six repères de la feuille sont ajustés au profil diagnostique existant, sans nouvelle optimisation de la projection du jeu : Fulda, Hünfeld, Neuhof, Geisa, Gersfeld et Schlitz. Les petits résidus d’ajustement de la feuille ne mesurent **pas** l’erreur indépendante de localisation dans le bitmap. Aucune précision native de deux pixels n’est revendiquée et aucune translation de 7,20 pixels n’est appliquée.

GEOMETRY.json contient le polygone source, sa transformation et chaque cellule incluse/exclue. Le polygone rencontre 40 cellules : 16 cellules de HEK et 23 de MEI deviennent FUL ; une cellule de WZB est **exclue** pour protéger le noyau de Würzburg. Geisa, Dermbach et l’enclave d’Herbstein ne sont pas intégrés.

Une première protection trop large avait exclu toutes les cellules MEI. La relecture de MAP2T/GEOMETRY.json a établi la distinction : `xD0C021`, propriétaire inchangé MEI, était un **résidu non certifié** de 204 cellules ; le correctif historique de Gotha est la cellule distincte `xEDB40F`, qui reste intacte. MAP2W ne réattribue que 23 cellules du résidu. Cette clarification est conservée dans REFINEMENT_CAPTURE.json, sans réécrire la baseline ou les anciens rapports.

La région économique native traverse le territoire historique : 16 cellules sont dans STATE_HESSE/74 et 23 dans STATE_SAXONY/73. C’est une dépendance technique du seul noyau de Fulda, **pas** une nouvelle reconstruction de la Thuringe. La capitale technique est STATE_SAXONY, où tombe désormais le repère diagnostique de Fulda. Aucun locator n’est créé ou déplacé.

## Démographie et installations

Les 20 047 habitants de FUL sont une redistribution technique proportionnelle aux cellules des deux donneurs : 14 240 viennent de HEK/Hesse et 5 807 de MEI/Saxe. Ce n’est pas une estimation de la population historique du prince-évêché. Aucun recensement de 1776 correspondant à ces 39 cellules n’a été identifié. Les profils culturels et religieux préexistants sont conservés, avec leurs défauts éventuels ; la religion catholique du gouvernement ne certifie pas celle de cette population technique.

Aucun niveau de bâtiment n’est ajouté, retiré ou transféré. Les installations existantes sont des données de région partagée, sans établissement de leur localisation historique dans le petit noyau. Le locator forestier reste dans HEK. Il serait trompeur de déplacer arbitrairement l’industrie hessoise ou d’inventer une administration pour rendre FUL rentable. Les marchés, la subsistance et la viabilité doivent être contrôlés en nouvelle partie.

Le drapeau est une approximation graphique provisoire : croix noire sur blanc, avec un motif natif existant. Il ne prétend pas restituer la bannière personnelle complète de Heinrich von Bibra.
