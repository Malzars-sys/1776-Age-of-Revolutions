# Lot 22 — révision des forts casematés

Statut : **aperçu corrigé, en attente de validation**. Aucune intégration, aucun DDS exporté, aucun lancement du jeu.

La bouche du canon et l’embrasure principale ont été réalignées pour prolonger le tube visible à l’intérieur. Deux ouvertures secondaires en maçonnerie sont ajoutées. La voûte, la terre protectrice et l’affût en bois conservent le concept initial. Les deux autres icônes restent inchangées.

## Aperçus courants

- [Forts casematés corrigés](previews/casemated_fortifications_padded.png)
- [Planche complète et miniatures 32 / 48 / 64 px](LOT_22_APERCU.png)
- [Transparence sur damier](LOT_22_ALPHA_DAMIER.png)
- [Comparaison avec trois technologies vanilla](LOT_22_COMPARAISON_VANILLA.png)

## Création et contrôles

Retouche avec **imagegen intégré**, deux passes successives. [Prompts exacts](PROMPTS.md), [provenance](source_provenance.json), [revue visuelle](visual_review.json), [contrôle technique](preview_validation.json). La première passe est conservée dans `iterations` mais n’est pas sélectionnée : la bouche restait trop basse.

Après l’édition par imagegen : copies, marges transparentes et réductions mécaniques uniquement, sans peinture, recoloration ni modification du masque par script. Les pixels RGBA de la dernière sortie sont conservés à l’identique dans le PNG avec marges. Les deux autres masters sont conservés octet pour octet. **1 265 fichiers de jeu protégés inchangés** ; ce contrôle ne constitue pas un essai moteur.

[Références historiques conservées](historical_references.json) et [recherche complémentaire](reference_recheck.json). La documentation de l’[Association Vauban](https://www.association-vauban.org/les-successeurs/) sert de contexte aux batteries casematées ; l’image n’est pas une reconstitution exacte d’un site. Aucun média distant téléchargé ou utilisé comme entrée.

L’icône vanilla `concrete_fortifications.dds` n’est pas réutilisée : elle est déjà affectée à « Fortifications en béton » en ère XI dans le mod. Son affectation est inchangée. Les anciennes variantes restent conservées dans le [dossier parent](../README.md).
