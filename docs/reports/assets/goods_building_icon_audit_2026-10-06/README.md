# Audit des icônes de biens et bâtiments — 6 octobre 2026

## Conclusion

**Il reste un seul placeholder hors cuivre : le bien Machines de précision.**
**Aucun bâtiment hors cuivre ne référence encore une image d'erreur.**

La passe ne peut donc pas être déclarée terminée : il reste le bien Machines de précision à illustrer. Génie routier a depuis été approuvé et intégré le 6 octobre.

## Périmètre et décompte

Contrôle des définitions actuelles, avec priorité aux fichiers du mod et repli vers les fichiers vanilla installés. Les réemplois vanilla présents ne sont pas comptés comme images manquantes.

| Famille | Définitions | Images vanilla présentes | Images du mod présentes | Placeholders | Décors vanilla cachés sans champ icon |
| --- | ---: | ---: | ---: | ---: | ---: |
| Biens | 71 | 53 | 16 | 2 | 0 |
| Bâtiments | 128 | 101 | 12 | 1 | 14 |

Les deux placeholders de biens sont Machines de précision et Cuivre. Le seul placeholder de bâtiment est Mine de cuivre. Le Cuivre et sa mine restent exclus du programme convenu.

Aucun chemin d'icône explicite introuvable, aucune texture vide et aucun échec de décodage du niveau principal DDS n'ont été détectés sur les 180 valeurs de chemin distinctes inventoriées (179 textures explicites et la valeur vide des décors cachés).

## Dernier bien à traiter

**Machines de précision** (`precision_machinery`).

- Définition : `common/goods/16_tech6c7_precision_machinery.txt`, bloc ligne 1, texture ligne 2.
- Texture actuelle : `gfx/error_deer.dds`, marquée `TEMP_ASSET`.
- Ce n'est pas une définition désactivée : les PM de production de machines de précision sont reliés au groupe `pmg_precision_machinery_production` de l'industrie d'outillage.
- Des consommateurs existent réellement : notamment les deux PM avancés du laboratoire (`common/production_methods/24_tech8c_research_laboratory.txt`, lignes 39 et 65), ainsi que divers procédés industriels.
- Aucun aperçu dédié existant n'a été trouvé parmi les fichiers dont le nom contient `precision_machinery` ; aucune création de ce bien n'a été lancée pendant cette vérification.

La localisation décrit des machines-outils et composants mécaniques de précision, notamment roulements, engrenages, valves et jauges. Une éventuelle illustration devra représenter le bien échangé, pas une scène de bâtiment ni un pictogramme de méthode de production.

## Exceptions à ne pas transformer en faux manques

Les 14 définitions vanilla sans champ `icon` appartiennent toutes à `bg_monuments_hidden`, ont `buildable = no` et proviennent de `common/buildings/08_monuments.txt` du jeu installé. Elles servent à des décors / monuments 3D cachés ; elles ne sont pas de nouveaux bâtiments industriels à illustrer.

Exemples : Arge Bam, Capitol Hill, Central Park, les têtes de l'île de Pâques, le château de Dracula. Le contrôle automatique a vérifié le groupe et le statut non constructible de chacune.

Une icône vanilla existante peut être un réemploi plutôt qu'une création propre au mod. Elle n'est pas, pour cette raison, une image d'erreur ou un fichier manquant. Ce rapport constate la présence des illustrations, pas une validation artistique de tous leurs sujets.

## Méthode et limites

- Résolution des définitions et textures du mod / jeu installé ; inspection de `texture` pour les biens et de `icon` pour les bâtiments.
- Décodage DDS et contrôle de l'alpha non vide pour toutes les textures explicites.
- Comparaison des pixels aux fichiers `gfx/error_*.dds` vanilla, y compris pour détecter d'éventuelles copies sous un autre nom.
- Vérification directe des trois références restantes à `error_deer.dds` dans les dossiers du mod.
- Inspection des consommateurs / producteurs de Machines de précision et des exceptions de monuments cachés.
- Aucun changement de recette, statistique, définition de jeu ou texture pendant cet audit.
- Pas d'essai moteur, ni de contrôle artistique exhaustif, ni de validation de toutes les mipmaps revendiqué.

Voir l'[inventaire complet](inventaire.csv), les [résultats et empreintes](audit.json) et la [nouvelle proposition Génie routier](../road_engineering_revision_2026-10-05/README.md).

## État final de la passe hors cuivre

1. Génie routier : ancien aperçu de pavés rejeté ; nouvel asset approuvé et intégré, avec couleurs natives et neuf mipmaps vérifiées.
2. Machines de précision : dernier bien avec image d'erreur, à illustrer.
3. Bâtiments : aucun autre placeholder ni chemin absent confirmé hors cuivre.

Ne pas relancer des lots de remplacement pour des icônes vanilla déjà présentes afin de remplir artificiellement le programme.
