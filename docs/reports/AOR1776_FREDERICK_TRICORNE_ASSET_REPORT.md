# Frédéric II — intégration du tricorne

État au 7 octobre 2026 : fichiers intégrés et contrôles statiques réussis,
avec **ajustement approuvé en jeu ; finitions et canne à valider en jeu**. Aucun commit, push,
merge ou changement du Steam Build/Workshop. Branche :
`codex/frederick-tricorne`.

## Source et licence

- Archive fournie : `bust-of-frederick-the-great.zip`, conservée dans
  `docs/portraits/sources/bust_of_frederick_the_great_original.zip`.
- SHA-256 : `9b1b574abbd9620eacb55c66a9eb1664b3d307008faa0a10911c2814f6f47f44`.
- Modèle : [Bust of Frederick the Great](https://sketchfab.com/3d-models/bust-of-frederick-the-great-15651df5efec42bb8e3ce70772adaf0d),
  de [christian.schulz.nuernberg](https://sketchfab.com/christian.schulz.nuernberg).
- Licence confirmée par les métadonnées de l'auteur sur Sketchfab :
  [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
  Conserver l'attribution, les liens et la description des adaptations ;
  distribuer cette adaptation artistique sous la même licence. Cela ne
  constitue pas une relicence des autres fichiers du mod.
- L'OBJ soudé contient 141 146 triangles ; le tricorne extrait en contient
  37 934. La sélection utilise une limite anatomique courbe, conserve les UV
  source sur la sauvegarde du maillage et ne redistribue pas le visage/buste
  dans le modèle destiné au jeu. Le zip source original reste intact.

## Références natives et préparation

Installation inspectée : `C:/Games/Victoria 3`, version 1.13.11 selon le
journal du jeu. Référence technique principale :
`game/gfx/models/portraits/attachments/male_headgear/european_military/05/male_headgear_european_military_05.mesh`.
Le bicorne natif comporte 2 124 triangles, 1 383 sommets après séparation
UV/normales et 61 bones ; fixation rigide à `bn_h_skull`, index 29. Autres
références mesurées : `european_common/01` (960 triangles) et
`european_common/03` (884 triangles). Pas de LOD sur la référence principale.

La version sans finitions du tricorne comporte **2 888 triangles**, **3 183 sommets
séparés** et un matériau. Le maillage de travail comporte 1 446 sommets.
La réduction de la surface externe réserve un budget pour une fine doublure
ouverte en dessous ; les détails sont transférés par une normal map. La
distance maximale mesurée des sommets externes simplifiés à la surface
extraite et ajustée est de 0,132 cm : ce n'est pas une borne de Hausdorff globale.

Le script importe les références, reprend leur armature et affecte chaque
sommet au groupe exact `bn_h_skull`, poids 1. Les 61 matrices inverses natives
sont réinjectées à l'export et comparées au fichier original. Les géométries
natives de référence ne sont pas incluses dans le modèle livré ni dans le
`.blend` livré. Celui-ci conserve le tricorne extrait original, sa version
haute résolution ajustée et sa version optimisée, avec leurs UV et le rig.

Matériau : `portrait_attachment`, présent dans le shader de cette installation.
Trois DDS 1024×1024 avec 11 niveaux de mipmaps : diffuse feutre anthracite
granuleux, normale tangentielle G/A selon le décodeur natif, properties
G=35 pour le spéculaire, B=0 pour le métal, A=230 pour la rugosité. L'alpha
diffuse vaut 255 partout. Le shader d'attachment réinitialise lui-même le
canal R des properties ; R=0 ne prouve donc pas une absence de SSS. La texture
photographique du buste n'est pas utilisée comme matériau final du chapeau.

## Intégration du portrait et correction de l'absence

Chaîne : `aor1776_headgear` / template `aor1776_frederick_tricorne` →
accessory `aor1776_frederick_tricorne_headgear` → entity
`aor1776_frederick_tricorne_entity` → mesh
`aor1776_frederick_tricorne_mesh`.

Le gène est un accessoire spécial non héritable, avec un choix vide et un
choix tricorne masculin. Le modifier est limité à un personnage historique,
masculin, adulte portant la variable `aor1776_frederick_tricorne`. Seul
Frédéric II reçoit ce marqueur dans son `on_created`. Aucun gène facial,
DNA de perruque ni autre personnage n'est modifié pour ajouter le chapeau.
L'accessory ne définit pas de tag `no_hair`, afin de conserver la perruque.
Pas de copie complète d'un gros fichier de gènes headgear Vanilla.

Les premières captures reçues le 7 octobre montraient la perruque sans chapeau.
Le démarrage du jeu a néanmoins chargé `aor1776_frederick_tricorne_mesh`
(`debug.1.log`, 6 octobre, 23:56:01). Aucune erreur de lien propre au tricorne
n'apparaît dans les journaux de ce démarrage, en dehors des avertissements
d'encodage corrigés ici. Les erreurs de lien et de rechargement de gènes
du démarrage précédent ne prouvent pas une erreur persistante après restart.

La règle personnalisée utilisait `mode = replace` pour un gène spécial absent
du DNA. Elle utilise maintenant **`mode = add`**, conformément aux définitions
des couvre-chefs dans `01_headgear.txt` de cette installation. Cette différence
était une cause probable du non-affichage ; la capture suivante confirme
désormais que le chapeau apparaît avec la perruque. Les trois définitions nouvelles gene/accessory/modifier
sont désormais en UTF-8 BOM pour supprimer leurs avertissements d'encodage.

Il existe également une cause distincte possible : `autosave_exit.v3` du
6 octobre, 23:52:54, ne porte pas le marqueur sur Frédéric (personnage 3220).
Une sauvegarde créée avant cet ajout ne rejoue pas `on_created`. L'utilisateur
ne sait plus si les captures proviennent de cette sauvegarde ou d'une nouvelle
partie. Cette sauvegarde a été lue, jamais modifiée.

## Fichiers du lot tricorne

Créés pour ce lot, indépendamment des changements déjà présents :

1. `tools/blender/extract_frederick_tricorne.py`
2. `tools/test_frederick_tricorne.py`
3. `docs/portraits/sources/bust_of_frederick_the_great_original.zip`
4. `docs/portraits/frederick_tricorne_work.blend`
5. `docs/reports/AOR1776_FREDERICK_TRICORNE_ASSET_REPORT.md`
6. `common/genes/aor1776_tricorne_accessory_gene.txt`
7. `gfx/portraits/accessories/aor1776_frederick_tricorne.txt`
8. `gfx/portraits/portrait_modifiers/zzz_aor1776_frederick_tricorne.txt`

Sous `gfx/models/portraits/attachments/male_headgear/prussian/aor1776_frederick_tricorne/` :

9. `male_headgear_frederick_tricorne.mesh`
10. `male_headgear_frederick_tricorne.asset`
11. `male_headgear_frederick_tricorne_diffuse.dds`
12. `male_headgear_frederick_tricorne_normal.dds`
13. `male_headgear_frederick_tricorne_properties.dds`
14. `LICENSE.txt`

Fichiers existants modifiés pour ce lot : `.gitignore` (source zip autorisé,
backups `.blend1` ignorés), `docs/portraits/README.md` (instructions et état)
et `common/history/characters/cleanup2b1 - major rulers 1776.txt` (trois lignes
pour le marqueur de Frédéric, en plus des changements antérieurs de perruques).
Le correctif de non-affichage du 7 octobre ne modifie que l'encodage des trois
définitions, le mode d'ajout du modifier et les tests/documentations. Un
contrôle séparé du `.blend` a détecté que la purge des références avait aussi
supprimé les sauvegardes haute résolution, car leurs objets étaient renommés
mais pas leurs datablocks. Le script corrige désormais leurs noms ; le
`.blend` a été réparé depuis le cache avec `--mode work`. Cela n'a pas réécrit
les mesh/textures utilisés par le jeu ni modifié la position du chapeau.

## Reconstruction et contrôles

```powershell
python tools/blender/extract_frederick_tricorne.py --mode build --integrate
python tools/blender/extract_frederick_tricorne.py --mode preview
python tools/test_frederick_tricorne.py
python tools/test_frederick_wig.py
python tools/test_historical_wigs.py
```

Installer Blender, IO PDX Mesh et Python/Pillow ; adapter `--game`, `--blender`
et `--pdx` si nécessaire. Sans `--integrate`, le build utilise le cache pour
les fichiers runtime ; il régénère néanmoins le `.blend` de travail. Les
préviews et extractions restent dans `.asset-cache/`, non versionnées.

Contrôles du correctif : 10 tests tricorne réussis, 8 tests de perruque réussis,
4 tests d'attribution des perruques réussis ; lecture du PDX, vérification
des indices et poids, matrices natives, fichiers et identifiants, shader,
textures opaques avec mipmaps, choix du personnage et encodage.
La lecture du `.blend` vérifie les trois maillages de travail, leurs UV, les
sauvegardes haute résolution et les DDS réellement empaquetés, sans géométrie
native de référence. Les fichiers runtime de perruque et chapeau et les DNA
ont des SHA-256 identiques avant et après ce correctif.

`git diff --check` ne signale pas d'erreur de whitespace. Ces contrôles statiques ne
valident ni le rendu réel ni l'exécution du modifier dans le moteur.

État global des fichiers déjà suivis, relevé avec `git diff --stat` :

```text
24 files changed, 552 insertions(+), 191 deletions(-)
```

Ce total inclut les travaux antérieurs (économie, armées, PM et portraits) ;
il n'est pas le diff du tricorne et exclut les nouveaux fichiers non suivis.
Le contrôle SHA-256 sur les 57 fichiers préexistants modifiés/non suivis du
début de ce correctif confirme que 51 restent identiques. Les six exceptions
sont précisément les trois définitions du tricorne, le `.blend`, son script
et le README. Seuls le rapport et le fichier de tests ont été ajoutés pendant
ce correctif. Rien n'a été stagé ou commité.

## Ajustement après la capture en jeu

La capture `codex-clipboard-1503b660-aa97-4d78-9019-55e8fc8fc5cd.png`
confirme l'activation, mais montre le chapeau posé au sommet de la perruque,
trop petit en hauteur et trop court sur les côtés. Le premier ajustement
25/33/18, base 50 cm, restait trop haut. L'utilisateur a ensuite fourni le
tableau `codex-clipboard-fa855fcb-a4c0-4ace-98cd-59e6909c747b.png` et demandé
des côtés plus larges, sans boucle traversant le feutre, ainsi qu'un sommet
plus pointu. Révision finale intégrée :

- Échelles source X/profondeur/hauteur : 27,5/36/24 au lieu de 19/24/14.
- Base : 44,5 cm ; la remontée automatique de 0,7 cm est supprimée. Le bord
  latéral le plus bas passe de 55,14 à 44,46 cm. L'ouverture frontale centrale
  reste vers 49,6 cm, juste au-dessus des sourcils de la tête neutre native
  (environ 48,4–48,7 cm), au lieu d'environ 53,8 cm au premier ajustement.
- Décalage de profondeur : 3,5 cm au lieu de 5 cm. Il ménage le front sans
  remonter le chapeau ; un essai plus bas sans ce recul avait 26 contacts
  avec la tête et a été rejeté, sans remplacer le runtime.
- Une élévation centrale de 4 cm, à profil triangulaire resserré au carré,
  accentue la pointe. Son influence est nulle sur la couture d'ouverture :
  le sommet monte sans faire remonter le bord sur le front.
- Encombrement final : 46,25 cm de largeur, 34,17 cm de profondeur et 22,69 cm
  de hauteur, contre 31,95 / 22,72 / 11,06 cm pour la version en jeu rejetée.
- Une correction radiale locale de la calotte utilise l'enveloppe géométrique
  de la perruque inchangée. Elle ne déplace pas la couture frontale ; dans
  cette version élargie, 202 sommets haute résolution sont ajustés, au maximum
  de 0,073 cm. Elle empêche une boucle supérieure de traverser le feutre.
- La normal map est recalculée, la doublure et l'ouverture restent ouvertes,
  et les poids/matrices rigides natifs sont conservés.
- Aucune modification du maillage de la perruque, du DNA ou des règles
  d'activation déjà confirmées. Le script et le `.blend` reproduisent ce fit.

La tête neutre n'a aucune intersection de surface avec le chapeau. Le BVH
compte 155 couples de triangles en contact avec la perruque, entre environ
47,48 et 49,03 cm : ils restent au voisinage du bord latéral bas et ne sont
pas éliminés en remontant tout le chapeau. Aucune intersection mesurée ne
subsiste au niveau de la boucle supérieure qui traversait la calotte.
Cela n'est pas une preuve automatique d'un bon ajustement. Les quatre
diagnostics visuels hors jeu ont été inspectés : chapeau assis sur le front,
côtés étendus, pointe rehaussée, pas de boucle visible à travers le feutre,
visage et boucles latérales dégagés. Ces previews utilisent une tête neutre,
pas les déformations faciales de Frédéric ni le moteur de rendu de Victoria 3.

Le nouveau modèle et les trois textures ont été synchronisés depuis le cache
et comparés par SHA-256. Le `.blend` a ensuite été repacké avec les fichiers
runtime intégrés. Seuls le mesh du chapeau et sa normal map changent parmi les
fichiers runtime ; diffuse et properties restent identiques. Les dix tests
tricorne contrôlent aussi les nouvelles dimensions, la hauteur de la pointe
et la couture frontale basse dans le `.blend` ; les tests de perruques
restent applicables. Les previews restent ignorées, sans nouvelle image
de diagnostic ajoutée au dépôt. Aucun commit/push ni modification de partie.

Après cette intégration : **10 tests tricorne + 8 tests perruque + 4 tests
d'attribution historique réussis**. Les 59 fichiers modifiés/non suivis
préexistants ont été comparés au début de l'ajustement : 52 sont identiques.
Les sept exceptions sont uniquement le mesh et la normal map du tricorne,
son script, son `.blend`, son fichier de tests, le README et ce rapport.
Toutes les définitions de portrait, les DNA, les fichiers de perruque,
les changements économiques et les PM restent inchangés. Aucun fichier
supplémentaire visible dans Git n'a été créé par ces essais.

## Validation visuelle restante

1. Recharger les assets de portrait ou redémarrer le jeu avec ce fork activé.
   La partie où le chapeau apparaît a déjà le marqueur : une nouvelle campagne
   n'est plus nécessaire pour cette modification du mesh et de la normal map.
2. Ouvrir Frédéric dans la fiche personnage et le portrait national ; confirmer
   la présence du chapeau et la conservation de la perruque.
3. Dans `portrait_editor`, appliquer le template spécial
   `aor1776_frederick_tricorne` pour distinguer un problème de modifier d'un
   problème de modèle. Cette manipulation n'a pas encore été testée en jeu.
4. Contrôler les nouveaux journaux, sans confondre les erreurs antérieures
   de hot-reload avec le dernier démarrage.
5. Contrôler la frange, le nœud noir et la canne selon les nouvelles captures,
   notamment face/profil et en mouvement.

La capture `codex-clipboard-106ccde6-522a-456d-8dda-a16b49be95f1.png` et le
message « Le chapeau est parfait » approuvent désormais le fit. Cette approbation
ne concerne pas encore les finitions ajoutées ensuite. Aucun contrôle du jeu,
changement de partie ou redémarrage n'a été effectué pendant cette révision.

## Finitions et canne — 7 octobre 2026

Les positions et UV des 2 888 triangles de feutre approuvés restent identiques.
Le test compare le SHA-256 des triangles canonisés, à cinq décimales :
`0637e8ad078b936b8e90167c370d12e68132486a454f09e9b4b9186479184089`.
La hauteur, largeur, assise, calotte, perruque et DNA ne sont pas réajustés.

Le premier essai de liseré lisse ressemblait à une simple ligne blanche.
Après le retour de l'utilisateur, il est remplacé par une frange claire :
432 brins coniques irréguliers de 0,45 à 0,85 cm, sur une petite sous-couche
de 0,17 cm de rayon. Les changements de bord replié sont séparés pour ne pas
tracer de corde en zigzag à travers un panneau. C'est de la géométrie opaque,
sans shell transparent, effet émissif ni override de shader. Ce rendu imite
visuellement la frange du tableau ; il n'établit pas sa matière historique.
Les 232 brins arrière approuvés sont conservés ; 200 sont ajoutés sur la crête
avant, suite au retour de l'utilisateur. Les deux bords repliés ont leur propre
chemin de frange ; les sections qui coïncident ne sont pas doublées.
Frange : 2 592 triangles. Nœud : 898 triangles. Total chapeau : **6 378 triangles**,
un seul matériau, trois DDS 1024px avec mipmaps complets. Le feutre conserve
son atlas ; seules les zones réservées sont utilisées pour les finitions.

Le nœud fourni remplace entièrement le nœud procédural provisoire. Source :
[Ribbon Bow](https://sketchfab.com/3d-models/ribbon-bow-4df59dfe3a474b07a408c037eacb6a6f)
de Maggatron, compte MaggaModels, sous
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Métadonnées API
vérifiées le 7 octobre 2026. Archive intacte :
`docs/portraits/sources/ribbon_bow_original.zip`, SHA-256
`aecdf0cdfdf19e822e40bed034d94392e01e9ee920de7045cc681ee6df88b239`.
Le FBX source comporte 48 212 triangles ; le build en conserve 898, soit environ
98,1 % de réduction, sous la limite de 1 000. Les boucles restent volumétriques.
Le nœud est recoloré noir mat, orienté à 65°, ajusté au relief et fixé à la bosse
(ancrage Blender 6,2 / −10,066 / 60 cm). Auteur, licence et changements sont
ajoutés au LICENSE du chapeau ; l'ensemble dérivé reste CC BY-SA 4.0.
L'archive de ruban source reste CC BY 4.0.

La canne est une création procédurale originale d'après le tableau, suite au
choix explicite de l'utilisateur. Le modèle BlenderKit « Walking Stick »
d'Alex Sandr n'est ni téléchargé ni incorporé, et l'extension n'est pas installée.
Canne : 1 808 triangles, un matériau, trois DDS 512px et 10 mipmaps ; bois brun,
poignée courbe claire, petits raccords métalliques. Ancrage rigide `bn_r_prop`,
origine au centre de la prise. Aucun skin/squelette n'est nécessaire au prop.
Les previews des frames 1/76/151 de l'animation native montrent la tige dans
la main fermée ; elles ne sont pas une validation du moteur ni une reproduction
exacte de la pose peinte.

Nouveaux fichiers :

- `tools/blender/build_frederick_cane.py`, `tools/test_frederick_cane.py` et
  `docs/portraits/frederick_cane_work.blend` (un seul maillage original et DDS packed).
- Gene `common/genes/aor1776_cane_accessory_gene.txt`, accessory et modifier
  `gfx/portraits/accessories/aor1776_frederick_cane.txt`,
  `gfx/portraits/portrait_modifiers/aor1776_frederick_cane.txt`.
- `gfx/portraits/portrait_animations/animations.txt` : définition native 1.13.11
  conservée, avec un seul idle ajouté, limité à Frédéric historique adulte.
  Toutes les autres règles sont comparées à l'original par le test. Reprendre
  les changements natifs lors d'une mise à jour ; cet override peut entrer en
  conflit avec un autre mod modifiant le même fichier.
- Dossier `gfx/models/portraits/attachments/props/aor1776_frederick_cane/` :
  mesh, asset, trois DDS, PROVENANCE. Aucune géométrie/texture/animation binaire
  native n'est redistribuée. Le modifier du prop est choisi uniquement avec
  la pose native compatible, sans ajouter aussi la canne vanilla.
- Le zip source du ruban est autorisé dans `.gitignore`. Tous les rendus,
  extractions et déclinaisons restent dans le cache ignoré.

Reconstruction complémentaire :

```powershell
python tools/blender/build_frederick_cane.py --integrate
python tools/blender/build_frederick_cane.py --mode preview
python tools/test_frederick_cane.py
```

Les nouvelles finitions et la canne ne sont pas encore testées dans Victoria 3.
Le jeu et la sauvegarde n'ont pas été manipulés. Aucun commit/push, merge,
Steam Build ou Workshop n'a été effectué.

Contrôle final de ce lot : **10 tests tricorne, 7 tests canne, 8 tests perruque
et 4 tests perruques historiques réussis**. Lecture PDX/native, budget de 898
triangles du nœud, empreinte du feutre, franges, matrices/poids, canne rigide,
pose scoped, tous les autres blocs d'animation natifs conservés, mipmaps,
licences/source masters et sources Blender empaquetées vérifiés.
Les quatre fichiers binaires du chapeau ont été synchronisés et comparés
par SHA-256 ; le `.blend` pointe vers les DDS runtime, pas vers un essai du cache.

Parmi les 59 fichiers modifiés/non suivis préexistants au début des finitions,
48 sont identiques. Les 11 exceptions sont uniquement `.gitignore`, le mesh
et les trois DDS du chapeau, son LICENSE, script, `.blend`, tests, README et
ce rapport. Les 14 fichiers nouveaux sont le zip source du ruban et les 13
fichiers de la canne. Aucun DNA, changement économique, PM, fichier de perruque
ni définition antérieure du tricorne n'est changé pendant ce lot. Aucun rendu
PNG ni sauvegarde `.blend1` n'est ajouté aux fichiers visibles dans Git.
`git diff --check` réussit et l'index est vide. Ces contrôles ne valident pas
le rendu ni le choix de pose dans le moteur du jeu.
