# Prototype : vrai mode de carte du Saint-Empire

Ce mod compagnon tente une coloration **sur la carte principale**, pas dans
l'atlas du journal. Il ajoute « Territoires de jure du Saint-Empire (prototype) »
au sélecteur natif. Les territoires enregistrés sont jaunes ; les autres terres
sont grises. Les possessions étrangères restent jaunes si elles sont de jure
impériales. L'icône est celle fournie pour la carte.

Le prototype n'est pas activé automatiquement. Aucun changement aux sauvegardes,
à la diplomatie, aux votes ou aux règles du mod principal.

## Activation et essai en jeu

1. Fermer le jeu normalement. Le prototype est installé comme mod local dans
   `Documents/Paradox Interactive/Victoria 3/mod/aor1776_hre_map_prototype/`.
   Le dossier voisin `mod/` est la source de cette copie de test : si on modifie
   le prototype, il faudra aussi mettre à jour la copie installée.
2. Dans le launcher, sélectionner **« 1776 — Test carte impériale »** : il contient
   le mod principal local « Age of revolution /Fork » en première position et
   « 1776 — Carte impériale (PROTOTYPE) » en seconde position, tous deux activés.
   Aucun autre mod n'est ajouté à ce playset. Les autres playsets et le playset
   précédemment sélectionné restent inchangés.
3. Relancer le jeu, ouvrir une partie de test, puis le sélecteur de cartes en bas
   à droite. Chercher **Territoires de jure du Saint-Empire (prototype)** sous T.
4. Vérifier le jaune sur les terres impériales et le gris en France/Scandinavie.
   Vérifier Lübeck/Holstein même lorsqu'ils sont sous domination étrangère.
   Vérifier que le jaune suit bien les frontières et n'est pas inversé nord/sud.
5. Tester plusieurs zooms, puis revenir à « États », « Infamie » et « PIB mondial » :
   ces modes doivent conserver leur rendu habituel, sans le masque jaune.
6. Ne pas enregistrer sur la sauvegarde principale pour ce premier essai. Envoyer
   une capture du sélecteur et du rendu. Si le mode manque, ou si la carte est
   magenta/cyan, envoyer aussi `logs/error.log` et `logs/graphics.log` de cette
   relance (les anciens journaux ne prouvent pas que ce prototype a été chargé).

Pour revenir en arrière : désactiver uniquement ce compagnon dans le launcher,
puis relancer. Ne pas supprimer les caches, les sauvegardes ni les fichiers vanilla.

## Ce qui est réellement testé

`VALIDATION.json` distingue les contrôles hors jeu de l'essai moteur restant.
Le masque est dérivé des **278 RGB du registre de jure**, à la résolution exacte
du bitmap du mod : aucun échantillonnage qui éliminerait les petites provinces.
Les deux textures sont relues pour vérifier chaque pixel. Le test contrôle aussi
l'absence de collision avec les textures vanilla et compile le nouveau code HLSL
avec le compilateur Direct3D de Windows dans un petit banc d'essai.

Cela **ne valide pas encore** l'enregistrement du mode par Victoria 3, le chargement
de son tableau de textures, la compilation Paradox complète, ni l'orientation
visuelle en jeu. `mask_preview.png` n'est qu'une vérification du masque, pas une
capture du moteur. Le nom de statut reste `PASS_OFFLINE_NATIVE_GAME_TEST_PENDING`.

## Mécanisme et limites

Le mode emploie un type de coloration natif connu (`countries`) et les propriétés
de textures présentes dans les fichiers installés de Victoria 3 1.13.9. Une
signature magenta/cyan dans son premier emplacement distingue ce mode des autres.
Le shader charge alors le masque impérial depuis le deuxième emplacement. Il ne
rajoute aucun emplacement de texture au moteur. Le shader vanilla est conservé
hors d'un include et d'un appel au début de la fonction de coloration.

Il s'agit d'un affichage des **droits de jure fixes du scénario**, indépendant du
propriétaire actuel. Ce n'est pas un nouveau filtre natif général qui lit en direct
tous les modificateurs d'État. Si le registre ou le bitmap change, il faut régénérer
le masque. Les emplacements et le sens des UV restent des hypothèses à valider
dans le moteur ; aucune promesse de compatibilité avec une autre version.

Le prototype remplace un shader partagé : conflit possible avec un autre mod de
carte, et recompilation graphique au lancement. C'est précisément pourquoi il
reste séparé du mod principal jusqu'à validation en jeu.

## Reproduction

Depuis la racine du projet, exécuter `tools/prototype_map2k_main_map.py --emit-patch`
et appliquer le patch émis pour préparer le descripteur et la copie du shader natif.
Exécuter ensuite `tools/prototype_map2k_main_map.py --build-test` pour produire les
DDS et le rapport. Les scripts ne changent pas le playset et ne lancent pas le jeu.

Sources techniques de cet essai : fichiers installés
`game/gfx/map/map_modes/map_modes.txt`, `game/gfx/FX/coloroverlay.fxh`,
`game/gfx/FX/lowspec_terrain.fxh` et les includes Jomini de l'installation locale.

Essai hors jeu du 13 octobre 2026 : **16 contrôles réussis**, 60 289 pixels
impériaux exactement reproduits ; 91 textures natives contrôlées sans collision
de signature. Le petit banc Direct3D compile le code ajouté sans diagnostic.
Le compagnon est activé dans son playset de test uniquement : sélectionner ce
playset dans le launcher pour l'utiliser. Aucun essai en jeu n'est confirmé.
