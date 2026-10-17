# Thorn — diagnostic affiné, correction non appliquée

**Aucune modification de Thorn dans R9.** Les153cellules de `x41A021`, les populations de `STATE_WEST_PRUSSIA`, les bâtiments et le locator natif sont inchangés. Le PNG avant/après montre réellement cette identité, pas une proposition présentée comme installée.

## Résultat nouveau exploitable

L'audit R8 est conservé, sans modification rétroactive. Son scénario technique d'une cellule `(4519,772)` était explicitement conditionnel, fondé sur le hub rural nommé Toruń, pas une attribution historique approuvée.

La comparaison R9 avec l'hydrographie native corrigée (largeurs3–15) montre cette ferme **au sud de la rivière**. La feuille Pfau45 conservée montre le noyau fortifié de Thorn et sa configuration riveraine. Le diagnostic géographique approximatif du centre urbain, passé dans le profil R5 figé, se situe vers **(4521.49,767.35)**, sur l'autre côté de la rivière native. L'écart avec la ferme est de l'ordre de cinq pixels. Il ne doit pas être masqué en renommant la ferme « centre historique certifié ».

`THORN_NATIVE_REVIEW.png` juxtapose les deux points et la rivière native, sans nouvel ajustement. La distance à la rivière n'est **pas** présentée comme une erreur certifiée de localisation de la ville ; elle permet seulement de constater la contradiction entre les deux représentations.

La souveraineté de Thorn polonaise en1776 est établie par le cadre de la mission et les conclusions R2 conservées. Le problème restant est le placement au pixel du noyau et le contour des possessions rurales, non le souverain de la ville.

## Arbitrage ciblé proposé, non appliqué

Deux abstractions urbaines peuvent être examinées à l'échelle du jeu, toutes deux près du diagnostic de rive nord, **jamais autour de la ferme par simple commodité** :

| Proposition | Cellules candidates PRU→PLC | Portée et limite |
| --- | --- | --- |
| U1 | (4521,767) | Une cellule urbaine illustrative, environ10km², pas le territoire historique complet |
| U2 | (4520,767) et (4521,767) | Deux cellules jointives, environ20km² ; plus d'espace de représentation, mais pas une preuve de juridiction sur la cellule supplémentaire |

Ces cellules sont bien dans `x41A021`. Les variantes ne sont pas cumulables. `THORN_ARBITRATION_PROPOSALS.csv` les enregistre **Applied=False**, sans RGB réservé ni changement d'historique. `THORN_ARBITRATION.png` est marqué NON APPLIQUÉ ; ce n'est pas le PNG des changements effectifs.

**Aucune de ces propositions n'est historiquement validée au pixel.** Le désaccord des profils et le placement de la rivière ne permettent pas d'affirmer que U1 ou U2 restitue à elle seule la limite de1776. Si le joueur accepte une abstraction urbaine explicite, il faudra encore vérifier la topologie du résultat et la représentation du hub. Sinon, il faut un contrôle physique local homologue avant sélection. R9 ne transfère donc pas une cellule pour satisfaire un chiffre attendu.

## Plan technique prêt pour une décision ultérieure

1. Sélectionner le noyau urbain accepté, ou une autre cellule après preuve locale. Ne pas attribuer automatiquement les153cellules.
2. Réserver un RGB libre et le rattacher à `STATE_WEST_PRUSSIA` (ID158), puis l'ajouter au `create_state` PLC déjà existant. Garder le résidu PRU.
3. Conserver `map_data/province_terrains.txt` cohérent ; le `tundra` hérité de l'ancien RGB reste une anomalie distincte, pas une raison de le recopier automatiquement.
4. Examiner le hub : **ne pas rebinder farm vers un RGB qui ne contient pas son point actuel**. Un éventuel déplacement du hub de cinq pixels nécessite une justification géographique propre ; sinon conserver la ferme et traiter son nom/sa représentation séparément, sans prétendre avoir corrigé la ville en interface.
5. Répartir seulement la population existante par la méthode déterministe déjà employée. Les325344habitants PRU et41521PLC sont des totaux État/propriétaire, pas des populations connues de Thorn. Ne pas créer un chiffre urbain arbitraire.
6. Vérifier les allocations des bâtiments, PM, détenteurs, routes, réserves et le recrutement prussien avant toute migration. Aucune propriété économique ou unité n'est préaffectée à une hypothèse dans R9.
7. Ne pas enregistrer cette ville polonaise dans le SERG par effet d'une subdivision technique.

Statut : **KNOWN_ANACHRONISM_UNCORRECTED / PLAYER_ARBITRATION_REQUIRED**. Il reste distinct de la clôture pratique de la Peene.
