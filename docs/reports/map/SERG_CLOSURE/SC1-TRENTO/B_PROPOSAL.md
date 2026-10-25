# Choix du noyau politique B de Trente

Inventaire avant : quatre RGB, **1 039 cellules AUS** dans STATE_SOUTH_TYROL. x039D0F : 187 ; x1120FF : 87 ; xD040E0 : 462 ; **xD0BF60 : 303**. Populations : 308 000 nord-italiens et 183 000 sud-allemands, catholicisme par défaut, aucun métier déclaré. Les trois déclarations économiques et leurs propriétaires sont conservés, ainsi que les unités existantes. Ces agrégats ne donnent aucune répartition fiable entre les juridictions épiscopales et tyroliennes.

| Option | RGB / cellules / propriétaires | Population et registre | Décision et limites |
| --- | --- | --- | --- |
| A — restitution étendue suffisamment précise | Hypothèse xD0BF60 + x1120FF : 390 cellules AUS→TRT ; extension éventuelle vers les vallées d’autres RGB | Répartition des 491 000 habitants non établie pour ces ressorts ; transfert entier des titres AUS injustifié | Rejetée : xD0BF60 porte aussi le localisateur de Rovereto et x1120FF agrège la frange occidentale ; la carte de 1750 ne résout pas les enclaves. Aucun transfert de 390 ou de 1 039 cellules. |
| **B — noyau de résidence** | **12 cellules xD0BF60 AUS→TRT**, nouveau **xEDBD00** ; parent AUS **303→291**, connecté | **9 000 habitants nord-italiens transférés**, AUS 491 000→482 000 ; registre **575→576**, emprise impériale identique | **Retenue** : noyau connecté autour du point urbain natif de Trente, distinct du localisateur de Rovereto au sud et de Bolzano/Merano au nord. Approximation politique, pas calage cadastral. |
| C — statut juridique ou administration sans territoire | 0 cellule, propriété AUS maintenue | 0 habitant transféré ; pas de pays territorial vivant distinct | Insuffisant pour la souveraineté temporelle omise. Les composantes institutions et défense deviennent des sous-lots du noyau B, pas un bonus AUS remplaçant la principauté. |

Coordonnées natives, zéro-indexées :

`[4350,973] [4350,974] [4351,972] [4351,973] [4351,974] [4352,972] [4352,973] [4352,974] [4353,972] [4353,973] [4353,974] [4354,973]`.

Le choix suit un petit contour en escalier autour du centre de résidence. L’ancre native est un indice de localisation confronté à la carte historique et aux voisins, pas une vérité cadastrale. Les douze cellules portent toutes le parent AUS actuel ; elles ne touchent ni les noyaux validés ni les autres trois RGB du Sud-Tyrol. Aucun corridor vers une vallée éloignée n’est créé. L’emprise ne cherche pas à représenter tout le domaine de Trente par son seul point urbain.

## Capitale, population et conservation

TAG libre **TRT** ; TRE et TRN sont déjà définis et ne sont pas réutilisés. Capitale : portion TRT de STATE_SOUTH_TYROL. Le localisateur urbain existant de Trente se trouve à (4352.081055, 973.937744), cellule [4352,973]. **Seule sa référence city est liée au RGB enfant**, sans déplacer ses coordonnées ni toucher au localisateur farm de Rovereto [4347,981]. Les autres hubs, ressources, arables et traits restent inchangés.

9 000 correspond à l’ordre de grandeur de la résidence documenté pour 1767 ; ce n’est ni un ratio de surface, ni le nombre exact en 1776, ni un total princier. Les 9 000 sont soustraits à une déclaration nord-italienne AUS de 154 000, ramenée à 145 000 ; l’autre reste 154 000 et les deux groupes sud-allemands de 91 500 sont conservés. Religion et profession explicites ne sont pas ajoutées. La présence d’une garnison dans la source n’autorise aucune nouvelle unité ou ventilation ethnique.

Les anciens titres impériaux restent tous identiques, y compris celui du parent AUS. Un seul titre TRT s’ajoute sur les cellules déjà impériales ; ni électorat, ni ville libre, ni expansion physique. Massa-Carrare et les noyaux alpins validés restent protégés.

## Limites et reprise éventuelle

La livraison **TR-I-CORE** représente la résidence souveraine, avec prince, chancellerie et lien de défense, et doit être testée en jeu. Elle ne certifie pas les vallées de Non/Sole, Giudicarie, Riva/Ledro, Pergine, Fiemme, Val Venosta ou les juridictions féodales. Certaines sont épiscopales, certaines tyroliennes ou partagées, sans découpe homologuée ici. Une extension future doit confronter une carte juridictionnelle détaillée antérieure à 1776 aux trois RGB laissés intacts et au parent résiduel, avec population de périmètre comparable. Aucun périmètre moderne ou diocésain ne doit s’y substituer. Brixen et le Tyrol demeurent des tâches distinctes.
