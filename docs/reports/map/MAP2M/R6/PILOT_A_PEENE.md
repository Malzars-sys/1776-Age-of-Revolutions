# Pilote A — Wolgast occidental et Peenestrom

**Partiel : 18 anciennes candidates B, aucune A, aucun transfert.** Pas de reprise générale de Demmin–Anklam ni des 149 candidates nouvelles de R5.

## Lecture locale

`MAYER1763_WOLGAST_DETAIL.png` montre le chenal, Wolgast côté continental et Usedom de l'autre côté. `A_MAINLAND_BANK.png` suit sept observations de la rive occidentale dans le scan original de 949×768 : (711,501), (712,510), (711,519), (710,528), (707,537), (701,543), (694,549). Rayon de lecture : quatre pixels source. Il s'agit d'une rive interprétée, pas d'un bornage du thalweg.

La reproduction BSB plus lisible reste une reproduction de la famille Mayer, dont l'état est seulement indiqué « après 1763 » ; elle ne remplace pas la datation de la source principale. Le plan urbain d'Anklam ne sert pas d'ancrage à Wolgast. Les données LUNG décrivent la morphologie moderne, sans présumer des rives de 1763/1776.

## Contrôle natif et raccord

La correction de palette de R6 inclut toutes les largeurs 3–15. Malgré cela, aucun chenal de rivière ne traverse la fenêtre du détroit ; le contour d'eau du raster ne permet pas d'identifier ses deux rives. Le contrôle réservé `A_WOLGAST_NARROWS` reste non mesurable. Les pixels côtiers présents dans la fenêtre ne sont pas adoptés comme homologues de remplacement.

Le modèle R5 est figé et son support est vérifié. Les nouvelles lectures source ne disposent pas d'un calage source→réel indépendant accepté : elles ne sont donc pas projetées comme de nouvelles limites validées. Les anciennes variantes restent des diagnostics, même lorsqu'elles donnent toutes la même appartenance d'une cellule. L'accord entre hypothèses ne remplace pas une preuve manquante.

Les sections horizontales LUNG au voisinage de Wolgast donnent des largeurs projetées sous le pixel (voir `MODERN_CHANNEL_SECTIONS.csv`). Elles ne mesurent ni l'erreur d'une ville ni une frontière historique. Une frontière politique généralisée reste techniquement possible sans chenal visible, mais ce serait une abstraction à faire approuver.

## Peendamm

Le modèle R5 place les cinq repères du plan d'Anklam dans une étendue de 0,152×0,203 pixel ; le moulin passe juste dans la cellule voisine des autres repères. Cette coupure de grille n'est pas une délimitation de l'enclave. Le périmètre et la surface historiques de tout Peendamm ne sont pas établis par la position du moulin. Une cellule locale représente environ 10,18 km² : l'attribuer en entier au seul motif de ce point serait disproportionné et non justifié.

**Décision : pas d'enclave agrandie, pas de nouveau RGB.** Une proposition de frontière continentale simplifiée, conservant l'abstraction de Peendamm, doit rester distincte d'une restitution précise et attendre l'accord du joueur.

## Suite utile et limite de R6

Pour une restitution géométrique : homologuer des objets locaux stables et distribués sur la source et dans des données géographiques, puis conserver de nouveaux contrôles natifs réellement observables. Ne pas refaire le même ajustement des caps du nord. Si la priorité devient la lisibilité politique à cette résolution, demander l'autorisation d'une généralisation explicite plutôt que promettre un nouveau recalage miraculeux.
