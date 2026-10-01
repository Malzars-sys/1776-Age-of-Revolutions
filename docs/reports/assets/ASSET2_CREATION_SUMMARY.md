# ASSET PASS 2 — bilan de création

Audit du fork local au 24 septembre 2026, sans modification du jeu ni des textures.

## Méthode et périmètre

Les définitions `common/` du fork prévalent par identifiant sur Vanilla; seuls les PMG présents dans les bâtiments et les PM présents dans ces PMG sont comptés. Les technologies non recherchables sont exclues. Les textures sont résolues d'abord dans le fork, puis dans Vanilla. Les identités externes sont vérifiées par SHA-256. La liste ASSET1 sert de baseline technologique; aucun nouvel audit de réutilisation Vanilla n'a été effectué. Les nombres reflètent l'arbre de travail actuel, qui contenait déjà des modifications non commitées avant cette passe.

La baseline ASSET1 comptait 87 technologies à illustrer; l'arbre actuel en compte 66. Ce total inclut 4 entrées absentes de la baseline; les autres écarts correspondent à des visuels déjà réaffectés entre les deux passes.

`FINAL` signifie uniquement texture Vanilla finale ou copie externe autorisée. Les icônes génériques du jeu, les objets non visuels et les créations locales dont la sémantique reste à vérifier ne sont pas gonflés dans ce total. `PERMISSION PENDING` compte les objets actifs dépendant d'une copie Tech & Res, plus les candidats Basileia distincts. `NEEDS ORIGINAL ASSET` compte les originaux certains; les quatre candidats Basileia demanderaient eux aussi un original si l'autorisation est refusée.

## TECHNOLOGIES

### PRODUCTION

TOTAL OBJECTS = 94
FINAL = 57
VANILLA FINAL = 57
AUTHORIZED EXTERNAL = 0
PERMISSION PENDING = 6
NEEDS ORIGINAL ASSET = 30
REVIEW = 4

### MILITARY

TOTAL OBJECTS = 71
FINAL = 57
VANILLA FINAL = 57
AUTHORIZED EXTERNAL = 0
PERMISSION PENDING = 0
NEEDS ORIGINAL ASSET = 14
REVIEW = 0

### SOCIETY

TOTAL OBJECTS = 78
FINAL = 59
VANILLA FINAL = 59
AUTHORIZED EXTERNAL = 0
PERMISSION PENDING = 1
NEEDS ORIGINAL ASSET = 18
REVIEW = 0

## GOODS

### Tous les biens

TOTAL OBJECTS = 69
FINAL = 54
VANILLA FINAL = 53
AUTHORIZED EXTERNAL = 1
PERMISSION PENDING = 4
NEEDS ORIGINAL ASSET = 8
REVIEW = 7

## BUILDINGS

### agriculture

TOTAL OBJECTS = 19
FINAL = 18
VANILLA FINAL = 18
AUTHORIZED EXTERNAL = 0
PERMISSION PENDING = 0
NEEDS ORIGINAL ASSET = 0
REVIEW = 1

### extraction

TOTAL OBJECTS = 12
FINAL = 8
VANILLA FINAL = 7
AUTHORIZED EXTERNAL = 1
PERMISSION PENDING = 1
NEEDS ORIGINAL ASSET = 3
REVIEW = 1

### industry

TOTAL OBJECTS = 77
FINAL = 59
VANILLA FINAL = 58
AUTHORIZED EXTERNAL = 1
PERMISSION PENDING = 1
NEEDS ORIGINAL ASSET = 1
REVIEW = 3

### infrastructure

TOTAL OBJECTS = 13
FINAL = 11
VANILLA FINAL = 11
AUTHORIZED EXTERNAL = 0
PERMISSION PENDING = 0
NEEDS ORIGINAL ASSET = 1
REVIEW = 1

### military

TOTAL OBJECTS = 3
FINAL = 3
VANILLA FINAL = 3
AUTHORIZED EXTERNAL = 0
PERMISSION PENDING = 0
NEEDS ORIGINAL ASSET = 0
REVIEW = 0

### public/service

TOTAL OBJECTS = 3
FINAL = 3
VANILLA FINAL = 3
AUTHORIZED EXTERNAL = 0
PERMISSION PENDING = 0
NEEDS ORIGINAL ASSET = 0
REVIEW = 0

## PRODUCTION METHODS

### Toutes les PM actives

TOTAL OBJECTS = 488
FINAL = 397
VANILLA FINAL = 397
AUTHORIZED EXTERNAL = 0
PERMISSION PENDING = 12
NEEDS ORIGINAL ASSET = 70
REVIEW = 20

## PMG

### Tous les PMG actifs

TOTAL OBJECTS = 246
FINAL = 0
VANILLA FINAL = 0
AUTHORIZED EXTERNAL = 0
PERMISSION PENDING = 0
NEEDS ORIGINAL ASSET = 13
REVIEW = 13

## Points de décision

- Les 14 monuments cachés sans `icon` sont des entités de carte, pas 14 icônes à inventer.
- `pm_dummy` est un état technique non illustré; il ne constitue pas une création.
- Les 13 PMG actifs sans `texture` explicite restent en revue, car l'interface peut hériter de l'illustration des PM; ne pas commander d'images avant vérification en jeu.
- Le `background` d'un bâtiment est un fond de panneau générique distinct de son `icon`; aucune nouvelle illustration de panneau spécifique n'est déduite de ce champ.
- Les 25 fichiers Tech & Res (24 baseline + `coal_gasification.dds`) ont une propriété non confirmée; 23 sont déjà présents byte-identical dans le fork. La page Workshop crédite des tiers sans attribuer ces fichiers individuellement; aucune provenance tierce au niveau fichier n'est prouvée par les hachages des autres mods installés.
- Les quatre candidats Basileia prioritaires restent conditionnels; aucune image n'a été copiée.
- La Gabelle: permission déjà documentée; aucune nouvelle demande générale.

## Totaux

Objets actifs inventoriés: 1173.
Besoins visuels certains ou conditionnels: 162.
Originaux certains: 158.
Candidats externes Basileia conditionnels: 4.
Objets en revue: 50.
Les copies Tech & Res existantes sont en revue de permission; si elle est refusée, leur remplacement devra être planifié séparément pour chaque fichier distinct.
