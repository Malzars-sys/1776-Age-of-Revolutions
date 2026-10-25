# Diagnostic bavarois indépendant

**Aucun profil territorial accepté.** Une seule affine locale longitude/latitude → pixel a été calculée, sans Miller, Homann, locator urbain ou déplacement de frontière. Le protocole `CONTROL_PROTOCOL.json` fixe les rôles avant le premier calcul. Il n’a pas été réoptimisé après examen du contrôle.

| Repère | Longitude / latitude de l’axe physique | Observation native (centre de cellule) | Rôle | Résidu |
| --- | --- | --- | --- | ---: |
| Lech–Danube | 10,937517 / 48,735276 | 4337,5 / 898,5 | FIT | 0 par interpolation |
| Inn–Danube | 13,481134 / 48,573195 | 4400,5 / 902,5 | FIT | 0 par interpolation |
| Salzach–Inn | 12,944214 / 48,206656 | 4385,5 / 912,5 | FIT | 0 par interpolation |
| Isar–Danube | 12,974935 / 48,804668 | 4384,5 / 894,5 | **CHECK exclu du calcul** | **4,674390 px** |

Les marqueurs natifs d’indice 1 sont associés par ordre et topologie des affluents, visibles sur `OFFICIAL_CONTEXT.png` et `NATIVE_RIVERS.png`, pas par la ville la plus proche. Les noms et identifiants des axes source sont dans `SOURCE_JUNCTIONS.json`. Lorsque plusieurs jonctions d’axes existent dans un confluent large, toutes sont conservées et leur moyenne sert au diagnostic ; elles ne sont pas maquillées en point géodésique unique.

Trois couples pour six paramètres donnent nécessairement des résidus FIT nuls : **aucune précision ne s’en déduit**. Moyenne et maximum sur l’unique point indépendant : **4,674390 pixels**, même valeur parce que n = 1. Ce n’est pas une borne maximale régionale. Le modèle prédit l’Isar à 4388,808 / 896,313, sans utiliser cette observation pour corriger le calcul.

En déplaçant seulement les trois observations FIT dans les quatre coins de leur cellule (64 configurations), le résidu du contrôle varie entre **3,410 et 6,004 pixels**, contrôle gardé fixe. Cette sensibilité n’inclut ni son propre rasterisation, ni le choix des axes, ni les changements des cours d’eau, ni les distorsions du jeu. Les variantes de jonctions source restent séparées dans les données ; elles ne sont pas une incertitude totale calculée.

## Causes et portée

- La topologie générale est reconnaissable, mais les tracés natifs sont généralisés et localement déformés. La superposition de contexte montre des écarts non constants le long d’une même rivière : une translation moyenne n’y répond pas.
- Le confluent n’est pas le centre de Passau. Les axes officiels et le raster n’ont ni la même date ni la même résolution. Une distance au cours d’eau voisin n’est jamais utilisée comme résidu de ville.
- L’Isar constitue un vrai contrôle physique indépendant, mais **un seul contrôle ne permet pas de valider une erreur dans tous les secteurs**. Il est lui-même au nord du triangle d’ajustement.
- Ilz, Regen, Naab et Loisach n’offrent pas ici de branches natives locales identifiées utilisables comme contrôles supplémentaires. L’Iller n’a pas de jonction d’extrémités nommées exactement partagée dans la fenêtre source retenue : pas de pseudo-observation créée.
- Freising, Werdenfels et Ratisbonne sont hors du triangle FIT. Passau est proche de son confluent FIT ; cela ne valide pas les limites du territoire au nord de la ville.

## Test de taille utile et décision

Le diagnostic d’aire de `GEOGRAPHIC_ASSESSMENT.json` est un **filtre d’ordre de grandeur**, pas un polygone historique : environ 900 km² correspondraient à 74,49 pixels sous cette affine. Même si toute cette aire formait un seul disque, son rayon intérieur maximal serait de 4,87 pixels. L’erreur observée au contrôle, 4,67 pixels, est déjà comparable à ce meilleur cas théorique ; l’ensemble historique est en réalité irrégulier et comprend des possessions détachées. Rien ne fournit une marge vérifiée pour sélectionner un noyau septentrional sûr de Passau.

Freising–Ismaning et les enclaves de Ratisbonne demandent une précision locale que cette expérience ne démontre pas ; Werdenfels est aussi une extrapolation importante. L’analyse ne transforme pas 4,67 pixels en un seuil universel pour tous les lots MAP, ni en rayon d’érosion arbitraire. Aucun transfert A/B n’est retenu.

## Pour reprendre utilement, sans répéter le même ajustement

1. Acquérir les planches territoriales adaptées de l’Atlas historique de Bavière (Freising 33, Passau 35, Stadtamhof–Donaustauf–Wörth 41) et dater les variations pertinentes ; elles sont identifiées bibliographiquement, pas annoncées comme déjà calées.
2. Obtenir des repères physiques **natifs indépendants** qui encadrent chaque noyau, notamment au nord de Passau : origine géographique documentée du relief ou correspondances de crêtes/vallées démontrées sur un DEM externe. Un sommet maximal du raster non identifié ne suffit pas.
3. Réserver des contrôles non ajustés des deux côtés du territoire. Vérifier l’incertitude par rapport aux marges du polygone source, et pas uniquement au centre d’une ville.
4. Si le dessin natif est irréductiblement schématique, préparer un arbitrage explicite de généralisation politique fondé sur ces planches, avec zones d’accord/désaccord visibles. Ne pas introduire silencieusement une transformation plus flexible interpolant les quatre confluents : elle supprimerait le seul contrôle disponible.

Les observations R4 sont réutilisables, mais `CALIBRATION.json` reste diagnostique et ne remplace aucun profil général. R3, Erfurt–Eichsfeld et les autres régions ne sont pas relancés.
