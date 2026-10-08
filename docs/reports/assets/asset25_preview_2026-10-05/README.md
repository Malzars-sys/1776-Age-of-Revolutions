# Lot 22 — génie, évacuation et forts casematés

**Aperçu courant : [révision 3](revision_v3/README.md)** — bouche et partie extérieure du canon supprimées, ouvertures secondaires conservées. La révision 2 a été rejetée pour le canon ; les deux autres icônes restent inchangées. Les planches initiales ci-dessous sont conservées pour l’historique, pas comme sélection courante.

Statut courant : **lot intégré et vérifié statiquement**, avec la révision 3 des forts casematés (bouche cachée). [Trois DDS natifs contrôlés](revision_v3/integration_static_validation.json) et [planche issue des DDS intégrés](revision_v3/LOT_22_DDS_INTEGRES_QA.png). Trois liens visuels modifiés uniquement ; gameplay inchangé. Jeu non relancé. Les contrôles d’aperçu ci-dessous décrivent la phase initiale et ne sont pas une validation moteur.

- Génie et pontons : tablier démontable porté par trois bateaux-pontons.
- Évacuation des blessés : ambulance hippomobile avec brancard à l’intérieur.
- Forts casematés : chambre de tir voûtée montrée en coupe, canon et couverture de terre.

## Aperçus à valider

- [Planche des trois icônes, avec miniatures 32 / 48 / 64 pixels](LOT_22_APERCU.png)
- [Vraie transparence sur damier](LOT_22_ALPHA_DAMIER.png)
- [Comparaison avec trois technologies Vanilla](LOT_22_COMPARAISON_VANILLA.png)

## Création et sources

Génération avec l’outil intégré imagegen, un appel par sujet, sans CLI/API. Les [prompts exacts](PROMPTS.md), la [provenance des originaux](source_provenance.json) et les [références historiques](historical_references.json) sont conservés.

La [Fondation Napoléon](https://www.napoleon.org/wp-content/themes/napoleon/annexes/hors-serie/premiere-campagne-italie/fr/lesecrits/colloques/eau.html) documente les ponts de bateaux des campagnes de la période. Le modèle des [Royal Museums Greenwich](https://www.rmg.co.uk/collections/objects/rmgc-object-68773), antérieur à 1852, sert seulement à comprendre les appuis, pas à dater exactement l’équipement de l’icône. L’[iconographie de l’ambulance de Larrey](https://www.napoleon.org/histoire-des-2-empires/iconographie/lambulance-volante-du-baron-larrey/) et le [bulletin du Musée du Génie, page 21](https://www.musee-du-genie-angers.fr/fpdb/16101216-bulletin40decembre2019.pdf) guident les deux autres concepts. Ce sont des interprétations simplifiées, pas des copies exactes de modèles ou de sites.

Les recherches d’images précèdent la génération. Aucun média distant n’a été téléchargé ou incorporé ; les échecs d’accès direct à certaines références secondaires sont signalés. Trois références natives du jeu ont été inspectées avant génération.

Après génération : copie des originaux, ajout mécanique de marges transparentes sans recadrage ni changement des pixels RGBA, réduction et planches de contrôle uniquement. Aucune peinture, recoloration ou modification de masque par script.

## Contrôles et périmètre

[Contrôle technique](preview_validation.json) : **1 265 fichiers de jeu protégés inchangés** depuis l’intégration du lot 21. [Revue visuelle](visual_review.json) : fonds clair/sombre, damier, géométrie générale et lecture réduite examinés. Aucun lancement ou contrôle du moteur n’est revendiqué.

Les coûts, recettes, déblocages, les sept anciens PM du laboratoire, la chaîne du cuivre et toutes les icônes déjà validées sont inchangés. Une approbation séparée est requise avant d’exporter et d’intégrer ce lot.

[Lot 21 intégré : forteresse de Vauban, normes d’armement, topographie militaire](../asset24_preview_2026-10-05/README.md).
