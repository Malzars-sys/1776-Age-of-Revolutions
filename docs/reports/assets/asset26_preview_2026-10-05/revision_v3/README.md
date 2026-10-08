# Lot 23 — révision 3 : théodolite et bicorne

**Trois icônes approuvées et intégrées le 5 octobre 2026.** Le Corps du génie utilise la version finale avec bicorne noir à bordure dorée et cocarde, près du pied du théodolite. Les deux autres icônes conservent exactement leurs masters initiaux.

Le chapeau est inspiré du [bicorne attribué au général Bertrand, Musée du Génie](https://www.musee-du-genie-angers.fr/fpdb/20182017-9-bicornedugeneralbertrand.pdf). La référence établit le lien avec un officier du génie de l'époque napoléonienne, **pas un modèle exclusivement réservé au génie**. Aucun insigne de corps inventé. Il s'agit d'une interprétation stylisée, pas d'une reconstruction certifiée.

## Fichiers sélectionnés

- [Corps du génie — théodolite et bicorne](previews/permanent_engineer_services_padded.png)
- [Lot complet](LOT_23_APERCU.png), [transparence sur damier](LOT_23_ALPHA_DAMIER.png), [comparaison vanilla](LOT_23_COMPARAISON_VANILLA.png)
- [Prompt exact de l'édition](PROMPTS.md), [provenance et chemins des sources](source_provenance.json), [plan complet](generation_plan.json).

Édition avec **imagegen intégré** à partir du master local de la révision 2, inspecté avant édition. Aucun visuel distant envoyé à l'outil. Le nouveau PNG original est conservé dans [previews/permanent_engineer_services.png](previews/permanent_engineer_services.png). La génération peut redessiner légèrement l'instrument ; elle n'est pas présentée comme identique pixel par pixel au précédent.

Le master sélectionné est carré, 1542 × 1542, avec véritable alpha. Après génération, seule une marge transparente a été ajoutée et le groupe centré mécaniquement : les pixels générés sont préservés intégralement. Les versions sans chapeau et au gabion restent conservées dans leurs dossiers historiques.

## Contrôles

[Validation technique réussie](preview_validation.json) : 1268 fichiers gameplay/gfx inchangés, deux masters retenus strictement identiques, aucun DDS exporté. [Revue visuelle](visual_review.json) : silhouette du chapeau lisible à 48/64 px, couleurs naturelles sur fonds clair/sombre, alpha vérifié sur damier. Une partie du pied gauche est masquée par le bicorne, les trois jambes restent cohérentes. Les détails du galon se simplifient à 32 px.

L'approbation exacte et les empreintes des trois masters sont enregistrées dans [user_approval.json](user_approval.json). Trois DDS natifs BGRA8, 256 × 256 et neuf mipmaps, sont reliés aux trois technologies dans `20_tech3a_military.txt` ; aucune autre ligne de gameplay n'est changée. [Validation indépendante des exports](integration_static_validation.json) : couleurs et alpha identiques aux PNG réduits à chaque mipmap, 1267 autres fichiers protégés inchangés. [Planche décodée des DDS intégrés](LOT_23_DDS_INTEGRES_QA.png), inspectée sur fonds clair/sombre et en miniature.

Le jeu n'a pas été relancé. Aucun changement de gameplay, aucune modification des PM du laboratoire. Les contrôles de prévisualisation ci-dessus sont conservés comme preuves de la phase antérieure à l'intégration.
