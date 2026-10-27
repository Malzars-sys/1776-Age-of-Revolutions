# HBC-05 — raccords en blocs compacts

25 octobre 2026. Demande du joueur : « des carrés » pour rendre les raccords moins artificiels, avec annotation des deux zones à élargir. **Proposition géométrique mise à jour ; aucune intégration au jeu.**

**Complément demandé sur le dernier dessin :** l'encoche à l'ouest du raccord de la baie James est remplie avec **13 provinces HBC supplémentaires**. La proposition active compte désormais **278 provinces HBC et 103 ONT**. `USER_NOTCH_INFILL.json` conserve le contour interprété et les RGB ajoutés ; `BEFORE_NOTCH_INFILL.json` conserve la sélection de 265 provinces avant ce complément. Aucun ancien territoire proposé n'est retiré, le Haut-Canada est inchangé et tous les ajouts restent connectés.

Le raccord HBC est élargi en bloc de provinces entières autour du fond de la baie James et du contact avec le Haut-Canada. Le côté nord du Haut-Canada est également épaissi. Le résultat conserve les contours des provinces existantes au lieu de dessiner de nouveaux petits carrés dans le bitmap : les enveloppes sont une interprétation visuelle du dessin du joueur, pas des limites historiques ou des carrés géographiques exacts.

Premier élargissement, avant le complément de l'encoche :

| Pays proposé | Avant | Après | Provinces supplémentaires |
|---|---:|---:|---:|
| HBC | 233 | 265 | 32 |
| Haut-Canada (`ONT`) | 94 | 103 | 9 |

Les ajouts sont sélectionnés dans deux enveloppes du référentiel de diagnostic, enregistrées dans `COMPACT_BLOCKS.json`. Les provinces sont conservées entières, sur la base de leurs centres dans les enveloppes, avec priorité aux possessions ONT existantes et à toute la sélection HBC antérieure. Les nouvelles provinces détachées sont rejetées ; aucun poste isolé n'est ajouté.

Les neuf provinces ajoutées à ONT sont actuellement HBC et se trouvaient **hors des 233 provinces HBC conservées** de la précédente proposition. Leur future attribution à ONT est une concession de gameplay demandée pour épaissir le raccord ; aucun autre pays n'est amputé. Elle ne transfère ni la population protégée de HBC ni ses bâtiments à ONT. Les anciennes populations et données économiques restent dans les portions HBC conservées selon le plan HBC-03.

L'aperçu affiche **tout le Haut-Canada en rose uniforme**. La bande rose claire et le trait blanc de HBC-04 représentaient le témoin de trajet à travers des possessions déjà ONT ; ils n'étaient pas deux limites territoriales à reproduire. Leur suppression de la vue politique corrige cette ambiguïté. Les autres terres sont distinguées de l'eau dans le contexte visuel.

## Contrôles

Les vingt contrôles de `VALIDATION.json` passent :

- population HBC inchangée (**108 626**), effectifs par culture/religion et commandes économiques conservés, portions HBC portant les POPs/bâtiments toujours existantes dans les historiques actuels ;
- toutes les anciennes provinces HBC et ONT conservées dans leur pays proposé, aucun double propriétaire, aucune prise de terre d'un pays tiers ;
- passage ONT protégé et témoin complet HBC → ONT → USA toujours valides sous les propriétaires proposés, avec contacts par bords, absence de province infranchissable et respect des adjacences natives actuelles ;
- États cibles du plan de conservation HBC-03 toujours présents dans le pays proposé, ajouts connectés aux blocs et aucun fichier du jeu modifié pendant le calcul.

Le complément vérifie aussi que les 265 provinces HBC précédentes restent sélectionnées, que les 103 provinces ONT sont exactement inchangées et que le remplissage demandé est présent. Le contour du dessin est traduit en une enveloppe visuelle en pixels, puis en provinces entières selon leurs centres ; il ne s'agit pas d'une nouvelle limite historique attestée.

La continuité des cinq postes et les contacts témoins de HBC-04 ne sont pas amputés : la nouvelle proposition conserve toute l'ancienne sélection et le parcours protégé. Les nouveaux ajouts sont en outre contrôlés par recherche de connectivité dans les provinces franchissables du pays proposé. Le fichier `PROVINCES.csv` sépare propriétaire actuel, propriétaire proposé et rôle de chaque province.

Les données du bitmap ne sont pas modifiées. La population du Haut-Canada n'est pas recalculée automatiquement en fonction de cette surface supplémentaire. Les 21 commandes d'historique économique HBC restent protégées, sans les confondre avec 21 bâtiments distincts ou un total de niveaux certifié par le moteur.

Reste à faire : les affectations et la démographie des terres retirées à HBC, les précisions historiques encore ouvertes dans les dossiers antérieurs, l'implantation puis les tests moteur du marché et du déplacement des formations. La demande esthétique n'a ni étendu l'arc à Kuujjuarapik ni créé de poste supplémentaire. Aucun commit. Aucune recherche historique nouvelle ni appel ColGrep nécessaire : les fichiers et dépendances étaient déjà localisés.
