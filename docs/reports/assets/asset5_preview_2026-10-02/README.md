# Lot 2 — six propositions d'assets phosphate–minerais

**Mise à jour : lot intégré le 2 octobre 2026 après approbation utilisateur, avec la mine V4 au lever du soleil.** Voir le [bilan d'intégration et sa réserve d'opacité](INTEGRATION_2026-10-02.md) et la [planche des DDS décodés](LOT_2_DDS_INTEGRES_QA.png). Les sections ci-dessous décrivent la préparation historique ; leurs mentions « non intégré » et « export bloqué » ne sont plus le statut de livraison courant.

Création : 2 octobre 2026, mode intégré **imagegen**, dix appels (six sujets, trois corrections ciblées et une variante d'ambiance). Statut : **aperçus artistiques à valider, aucune intégration**. Cuivre et quatre propositions ciment du lot précédent hors périmètre.

## Aperçus

- [Planche du lot](LOT_2_APERCU.png), avec lectures réduites : biens/PM 32 et 48 px ; technologies 48 et 64 px ; bâtiment 48, 64 et 96 px.
- [Comparaison avec deux références vanilla par famille](LOT_2_COMPARAISON_VANILLA.png), sur fonds clair et sombre.
- Masters PNG : [Phosphates](previews/phosphates.png), [Mine de phosphate, V3](previews/phosphate_mine_v3.png), [Minéralogie appliquée](previews/applied_mineralogy.png), [Levé géologique](previews/geological_surveying.png), [Tri manuel](previews/manual_ore_sorting.png), [Concentration des minerais, V2](previews/ore_concentration.png).
- [Mine : contraste avant/après V2–V3](MINE_CONTRASTE_V2_V3.png), avec miniatures à taille réelle en 48, 64 et 96 px. [Prompt de cette retouche](MINE_CONTRASTE_V3_PROMPT.json).
- Essai séparé, non sélectionné : [mine au lever du soleil, V4](previews/phosphate_mine_v4_sunrise.png), [comparaison V3 / lever du soleil](MINE_AMBIANCE_V3_LEVER_DE_SOLEIL.png) et [prompt et contrôle](MINE_LEVER_DE_SOLEIL_V4_PROMPT.json). Seul le ciel lointain reçoit une ambiance d'aube ; le site conserve ses ombres froides et le minerai son identité chaude. V3 reste la version du manifeste et de la planche du lot. L'intérieur de V4 reste légèrement translucide (alpha 249–253), sans correction programmatique, et son export reste bloqué.
- Les PNG réduits en 256 px (biens, technologies, bâtiment) et 208 px (PM) sont dans `target_size_png/`. Ce ne sont pas des DDS intégrés.

## Références et provenance

[Références réelles et décisions](REFERENCES_REELLES.md), [plan initial et prompts](generation_plan.json), [manifeste des aperçus et prompts effectivement utilisés](preview_manifest.json). Le manifeste conserve également les versions non retenues : le crible trop volumétrique, la mine V1 plus translucide et la mine V2 insuffisamment contrastée. Les fichiers sources générés ont été copiés ici sans supprimer leurs originaux.

Les dix références natives locales, inspectées puis utilisées pour le style, sont répertoriées dans `native_references.json`. Les documents web renseignent les sujets ; aucune image distante ni illustration de mod tiers n'a été téléchargée ou fournie au générateur.

## Contrôles et réserve technique

Les six masters sont carrés, 1254 × 1254, avec vraie transparence extérieure ; alpha conservé tel que généré. Les miniatures et les deux fonds ont été inspectés visuellement. Pictogrammes simplifiés pour les PM ; minerai identique entre le bien et la mine ; objets conceptuels sans médaillon pour les technologies.

**Révision de contraste V3 :** le site d'extraction est désormais gris-bleu sombre, avec des détails secondaires atténués. Le tas de phosphate conserve son identité beige/brune et sa place au premier plan ; la séparation de sa silhouette est contrôlée à 48, 64 et 96 px. Les cinq autres masters restent identiques, vérification par empreinte.

**Réserve avant export de la mine :** l'intérieur du cadre demeure très légèrement translucide (alpha 247–253 dans la zone centrale de V3, au lieu de 255). Les coins sont réellement transparents. Cet aperçu permet la validation artistique, mais ne constitue pas un fichier final prêt à intégrer. Aucune correction programmatique de l'alpha n'a été appliquée ; la génération intégrée conserve son alpha. Le défaut est déclaré dans `preview_validation.json`, et l'export DDS reste interdit tant qu'il n'est pas réglé.

Les 1 194 fichiers de `common/` et `gfx/` présents au début du travail ont les mêmes empreintes à la fin. Aucun nouveau fichier n'y a été créé. Les six futurs chemins DDS restent absents. Aucun changement des recettes, emplois, prix, technologies, statistiques, références de textures ou contenu cuivre. Aucun test moteur revendiqué.

Prochaine étape : validation ou retouches artistiques par l'utilisateur ; résolution de la réserve d'opacité ; puis export et branchement des seules images explicitement approuvées. La réutilisation éventuelle des deux PM sur d'autres mines reste une extension séparée à confirmer.
