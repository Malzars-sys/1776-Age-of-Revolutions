# Lot 6 — deux retouches et une proposition

Date : 4 octobre 2026. Mode : **imagegen intégré**, deux éditions distinctes. Statut actuel : **les deux retouches et la tribune sont validées et intégrées ; contrôles sur fichiers réussis, sans essai moteur**. [Bilan d'intégration](../README.md). L'[accord initial sur les deux retouches](user_approval.json) reste conservé ; les mentions d'attente et de « proposition non générée » ci-dessous décrivent les étapes antérieures.

- [Régime constitutionnel](constitutional_government_padded.png) : la couronne est posée sur un livre fermé ; le parchemin, le sceau et les rubans ont disparu.
- [Souveraineté populaire](national_sovereignty.png) : ajout d'une cocarde bleu-blanc-rouge ; la hampe reste en place. La demande initiale de la retirer a été remplacée par la dernière instruction du joueur.
- Mouvements réformistes : **proposition non générée** d'une tribune d'orateur en bois, sans personnage ni texte, pour évoquer les réunions publiques et les campagnes de réforme. L'ancienne pétition n'est pas sélectionnée pour intégration.

## Vérification

[Aperçu et lecture à 32 / 48 / 64 px](APERCU.png), [comparaison avant/après et deux références vanilla](COMPARAISON.png), [transparence sur damier](ALPHA_DAMIER.png).

Les objets restent lisibles à 48 et 64 pixels ; le livre, la couronne et la cocarde se distinguent. Comparaison faite avec Démocratie et Académie vanilla. Ce sont des icônes de technologie peintes en volume, pas des PM plats. Leur traitement reste plus détaillé que certains exemples natifs : le jugement artistique définitif revient au joueur.

Les deux masters et les réductions 256 px ont un canal alpha réel et quatre coins entièrement transparents. Le fichier couronne/livre brut avait une trace d'alpha de 1/255 dans un coin ; le dérivé sélectionné ajoute uniquement 16 px transparents sur chaque côté. Le contrôle vérifie que tous les pixels du rendu original sont inchangés. Aucune peinture, recoloration ou suppression de fond manuelle. Le fichier brut est conservé dans `constitutional_government.png`.

Les empreintes des **1 217 fichiers de `common` et `gfx` sont inchangées**. Pas de DDS exporté, pas de changement de gameplay, pas de modification des PM du laboratoire et aucun essai en jeu revendiqué. [Contrôle technique](preview_validation.json).

## Sources et provenance

- [Prompts complets et dernière instruction sur la hampe](generation_requests.json).
- [Originaux générés et copies conservées](generation_results.json).
- Les masters sélectionnés sont enregistrés dans ce dossier ; les originaux imagegen restent à leur emplacement de génération.
- Les réductions se trouvent dans `target_size_png/`.

Une recherche d'images a précédé les éditions. Le bonnet avec cocarde a été observé dans la [photographie de l'objet de Strasbourg de 1793](https://commons.wikimedia.org/wiki/File:Bonnet_phrygien_d'une_section_du_club_des_Jacobins_%C3%A0_Strasbourg_(1793).jpg) et dans [la présentation du bonnet de liberté par Age of Revolution](https://ageofrevolution.org/200-object/phrygian-cap/). Ces références informent la forme de la cocarde ; elles ne sont ni téléchargées ni copiées dans l'asset. La couronne sur un livre est une composition symbolique demandée par le joueur, pas la prétendue reproduction d'un objet historique précis.

Attendre la validation des deux retouches et le choix du concept des mouvements réformistes. L'export futur restera en BGRA8 natif avec alpha et contrôle des couleurs en jeu.
