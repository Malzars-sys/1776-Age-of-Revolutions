# Lot 14 — mines et soufflage à chaud

**Révision 2 approuvée et intégrée le 5 octobre 2026.** Voir `revision_v2/README.md` et `revision_v2/integration_static_validation.json` pour les trois fichiers convertis et contrôlés. La lampe est conservée à l'identique. Les aperçus et descriptions ci-dessous documentent la première proposition rejetée, conservée pour historique ; leur statut non intégré ne décrit pas la révision 2.

Statut : **trois aperçus prêts, NON intégrés**. Validation utilisateur requise avant export DDS ou modification de leur liaison dans le jeu.

Le lot 13 précédent (couture mécanisée, meunerie automatisée, papier continu) est intégré et contrôlé indépendamment ; voir `../asset16_preview_2026-10-05/integration_static_validation.json`.

## Aperçus

- `LOT_14_APERCU.png` : grand aperçu et lectures 32/48/64 px sur fonds clair et sombre.
- `LOT_14_COMPARAISON_VANILLA.png` : comparaison avec trois icônes TECHNOLOGY natives, décodées depuis le jeu installé.
- `LOT_14_ALPHA_DAMIER.png` : vérification des ouvertures et du fond transparent.

## Sujets

- Mines profondes (`deep_mine_engineering`, ère 4) : treuil minier en bois avec poulie, corde continue et seau.
- Sécurité minière (`mine_safety_engineering`, ère 5) : lampe Davy à toile métallique.
- Soufflage à chaud (`hot_blast_smelting`, ère 6) : chambre en fer chauffée au-dessus d'un foyer et conduits d'air connectés.

Les formes ont été choisies après recherche d'images et inspection des références historiques, documentées dans `historical_references.json`. Ce sont des illustrations conceptuelles historiquement informées, pas des reconstitutions techniques certifiées.

## Sources et règles

Mode : imagegen intégré ; trois générations distinctes, fond transparent. Prompts exacts : `PROMPTS.md` et `generation_plan.json`. Provenance, copies et empreintes : `generation_results.json`. Les sources originales générées sont conservées à leur emplacement initial et copiées sans modification dans `previews/`.

Maîtres bruts : 1254 × 1254. Sélection : 1574 × 1574 après ajout mécanique de marges transparentes, sans recadrage ni retouche artistique ; tous les pixels RGBA sources sont préservés. Preuve : `canvas_padding.json`.

Style : objets volumétriques peints, couleurs naturelles sans dominante bleue, une composition fonctionnelle dominante, aucun cadre, texte, décor ou ombre au sol. Les règles des PM ne s'appliquent pas aux technologies ; les sept anciennes icônes PM du laboratoire sont conservées.

## Vérification

`preview_validation.json` : PASS_TECHNICAL_PREVIEW_CHECKS ; les **1241 fichiers common/gfx** de départ sont identiques. Les coins transparents sont vérifiés à la taille maître et à 256 px. Aucun DDS du lot 14 n'est créé et aucune liaison de technologie n'est changée.

`visual_review.json` : trois planches inspectées visuellement ; lecture satisfaisante à 48/64 px, simplification attendue à 32 px.

Aucun test en moteur n'a été effectué pour ce lot. Aucun gameplay, coût, déblocage, fichier de cuivre ou asset approuvé n'a été modifié pendant ses aperçus.

Après approbation uniquement : DDS 256 × 256, neuf mipmaps, format natif **BGRA8 legacy A8R8G8B8**, puis contrôle indépendant du décodage et des couleurs avant intégration.
