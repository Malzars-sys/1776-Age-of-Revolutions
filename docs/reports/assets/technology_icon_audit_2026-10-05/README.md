# Audit des icônes de technologies — 5 octobre 2026

**Mise à jour du 6 octobre :** Génie routier a été refait, approuvé puis intégré. L'inventaire ci-dessous reste l'instantané du 5 octobre, avant cette intégration. Il ne reste désormais aucun placeholder de technologie active hors cuivre ; voir la [validation du nouvel asset](../road_engineering_revision_2026-10-05/integration_static_validation.json).

## Conclusion

L'inventaire précédent confondait parfois « icône vanilla générique » et « icône manquante ». Ce sont deux sujets différents : une image vanilla existante n'entre pas dans la liste des illustrations à créer par défaut.

Sur **243 technologies actives**, **241 disposent déjà d'une vraie image** :

- 168 références résolues dans les fichiers du jeu vanilla ;
- 73 références résolues dans les fichiers du mod ;
- 2 références à l'image d'erreur `gfx/error_manul.dds`.

Aucun chemin d'image actif introuvable, aucune image active vide et aucun échec de décodage du niveau principal DDS n'ont été détectés.

## Les deux véritables placeholders actifs

| Technologie | Définition actuelle | Situation / suite minimale |
| --- | --- | --- |
| Génie routier (`improved_road_engineering`) | `10_tech3a_production.txt` : bloc ligne 739, texture ligne 742 | L'image d'erreur est encore branchée. L'aperçu corrigé des pavés existe déjà ; pas besoin de relancer sa création. |
| Doublage en cuivre (`copper_sheathing`) | `25_tech3a_naval.txt` : bloc ligne 108, texture ligne 111 | L'image d'erreur est encore branchée. La chaîne cuivre reste exclue du programme d'assets jusqu'à nouvelle instruction. |

### Génie routier : aperçu existant mais non intégré

Aperçu corrigé :
`docs/reports/assets/asset8_flat_revision_2026-10-03/previews/improved_road_engineering_cobblestones.png`.

SHA-256 vérifié :
`b4d86bab13462957ca682b2b49779e20f83efc178233b307e6f3166a7a1b8579`.

Le plan de révision porte encore `WAITING_USER_APPROVAL`. Le fichier cible `gfx/interface/icons/invention_icons/1776_improved_road_engineering.dds` n'existe pas ; la technologie pointe toujours vers l'image d'erreur. Il faudra reprendre cet aperçu, confirmer sa validation si nécessaire, puis exporter et brancher le DDS selon les règles de couleurs natives. Ne pas reprendre le premier aperçu rejeté avec coupe empierrée / outil.

L'exclusion cuivre est documentée dans le [cahier des charges](../ASSET4_CAHIER_DES_CHARGES_ET_LOT_1_2026-10-01.md), notamment ses consignes de périmètre et de lots suivants.

## Le dernier lot proposé n'est pas un lot d'images manquantes

| Technologie | Image réellement utilisée | État |
| --- | --- | --- |
| Sociétés savantes (`specialized_professional_societies`) | `rationalism.dds` | Vanilla présent et décodable |
| Médecine anatomoclinique (`clinicopathological_medicine`) | `psychiatry.dds` | Vanilla présent et décodable |
| Principes actifs (`active_principle_pharmacy`) | `pharmaceuticals.dds` | Vanilla présent et décodable |

En particulier, **Médecine anatomoclinique utilise bien `psychiatry.dds`**, fourni par le jeu. Son nom de fichier ne signifie pas qu'il manque une icône.

Les trois nouveaux aperçus du lot 26 (`asset29_preview_2026-10-05`) ne sont pas intégrés. Ils restent conservés, mais ne constituent plus des priorités pour compléter les images absentes. Aucun remplacement ni retour arrière n'a été effectué pendant cet audit.

## Définitions désactivées : ne pas les commander comme de nouvelles icônes

Le mod contient 292 définitions au total. **49 ont `can_research = no`** et ne sont pas à compter comme technologies actives à illustrer. Parmi elles, sept gardent une image d'erreur :

- Turbines hydrauliques (`hydraulic_turbines`).
- Verrerie traditionnelle (`traditional_glassmaking`).
- Fusées mysoréennes (`mysorean_iron_cased_rocketry`).
- Munitions explosives (`explosive_field_ammunition`).
- Fusées militaires (`standardized_military_rockets`).
- Savoirs codifiés (`codified_practical_knowledge`).
- Établissements navals organisés (`organized_naval_establishments`).

Leur éventuelle activation serait une autre modification du mod, pas une tâche d'illustration autorisée par cet audit.

## Images existantes dont la provenance n'est pas une absence

Vaccination et Imprimerie mécanisée utilisent respectivement `preview_morgenroete_vaccination.dds` et `preview_morgenroete_mechanized_printing.dds`. Ces fichiers sont présents dans le mod et décodables. Le préfixe « preview » ou leur provenance externe ne les transforme pas en technologies sans image. Un éventuel remplacement artistique ou de provenance doit être décidé séparément.

## Méthode et limites

- Inventaire des huit fichiers actuels de `common/technology/technologies`, en conservant les modifications locales existantes.
- Prise en compte du `replace_path` de ce dossier dans `descriptor.mod` : ne pas ajouter artificiellement les définitions vanilla remplacées.
- Résolution des textures avec priorité au mod, puis recherche dans l'installation locale du jeu : `C:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game`.
- Vérification des 242 chemins distincts utilisés par les technologies actives : existence, décodage RGBA du niveau principal DDS, alpha non vide et comparaison des pixels aux images d'erreur vanilla pour repérer d'éventuelles copies sous un autre nom.
- Aucune duplication d'identifiant de technologie détectée. Chaque technologie active possède exactement un champ `texture`.
- Ce contrôle constate la présence d'une image ; il ne prétend pas valider artistiquement chaque icône, ses couleurs en moteur, toutes ses mipmaps, ni son rendu en jeu.
- Aucun lancement du jeu, génération, export ou changement des définitions / textures pendant cette passe. Seuls ces nouveaux rapports ont été ajoutés.

Voir l'[inventaire complet](inventaire.csv) et les [résultats / empreintes des définitions](audit.json).

## Règle de sélection pour la suite

Ne sélectionner comme « image à créer » qu'une technologie active avec un vrai placeholder, un chemin absent ou une texture inutilisable. Une icône vanilla générique mais présente, une copie externe existante ou une définition désactivée ne suffit pas à justifier une nouvelle création.

Dans le périmètre actuel, il reste donc **un branchement à terminer (Génie routier, aperçu existant)**, et **aucune nouvelle illustration de technologie obligatoire à générer**. Doublage en cuivre reste recensé mais exclu.
