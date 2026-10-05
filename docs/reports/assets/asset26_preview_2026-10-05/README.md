# Lot 23 — aperçus à valider

**Version intégrée : [révision 3](revision_v3/README.md), avec un théodolite et un bicorne pour le Corps du génie.** Les trois icônes finales ont été approuvées et intégrées le 5 octobre 2026 ; couleurs et alpha des DDS vérifiés indépendamment. Les fichiers et descriptions ci-dessous documentent uniquement la version initiale au gabion, conservée comme historique.

Le lot précédent (22) est intégré, avec la bouche du canon des forts casematés masquée. Le lot 23 final est lui aussi intégré ; aucun essai moteur n'est revendiqué.

## Trois propositions

- **Services vétérinaires** : coffre de soins, flacons, bandage et fer à cheval. L'icône déjà approuvée de Science vétérinaire reste inchangée.
- **Corps du génie** : gabion en osier rempli de terre et pelle de sapeur, au lieu du fantassin actuellement réutilisé.
- **Artillerie à cheval** : attelage, avant-train et canon léger, au lieu du bicorne actuellement réutilisé.

## Fichiers sélectionnés

- [Services vétérinaires](previews/military_veterinary_services_padded.png)
- [Corps du génie](previews/permanent_engineer_services_padded.png)
- [Artillerie à cheval](previews/horse_artillery_padded.png)
- [Planche du lot](LOT_23_APERCU.png), [transparence](LOT_23_ALPHA_DAMIER.png), [comparaison vanilla](LOT_23_COMPARAISON_VANILLA.png).

Création avec **l'outil imagegen intégré**, un appel par icône, sur fond réellement transparent. Les originaux sont conservés dans `previews/*non padded*.png`; les chemins exacts des sorties, prompts et empreintes sont enregistrés dans [source_provenance.json](source_provenance.json). [PROMPTS.md](PROMPTS.md) contient les trois consignes intégrales.

Seule une marge transparente a été ajoutée, sans retoucher les pixels ni recolorer les images. Les fichiers sélectionnés font 1542 × 1542 pixels. Les feuilles de contrôle présentent les réductions 32, 48 et 64 pixels, sur fonds clair et sombre.

## Références et limites

Recherche d'images réelles effectuée avant génération ; aucune photographie distante téléchargée ou envoyée à la génération. Références détaillées et limites dans [historical_references.json](historical_references.json).

- Soins équins : [Museum of Military Medicine](https://www.museumofmilitarymedicine.org.uk/galleries/history-of-queen-alexandras-royal-army-nursing-corps), [coffret médical du Science Museum Group](https://collection.sciencemuseumgroup.org.uk/objects/co184839). Le coffret est une référence médicale d'époque, pas une trousse vétérinaire militaire identifiée.
- Génie : [manuel d'artillerie, Bibliothèques de Reims](https://www.bm-reims.fr/Default/doc/SYRACUSE/852080/memoires-d-artillerie-recueillis-par-m-surirey-de-saint-remy-tome-deuxieme?_lg=fr-FR), gravures de gabions trouvées en recherche d'images.
- Artillerie : [National Army Museum](https://www.nam.ac.uk/explore/cavalry-roles), [système Gribeauval, Musée de l'Armée](https://www.musee-armee.fr/collections/explorer-les-collections/portofolios/le-systeme-gribeauval.html). La paire de chevaux est une simplification graphique, pas la représentation d'un attelage réglementaire complet.

Les silhouettes restent lisibles en petite taille ; le canon de l'attelage est surtout identifiable à 48/64 pixels. Les textures et petits détails disparaissent à 32 pixels. Voir [visual_review.json](visual_review.json).

## Contrôles

[Validation technique](preview_validation.json) : réussie. Les **1268 fichiers protégés** de gameplay et de graphismes sont inchangés depuis le début de ce nouveau lot. Aucun DDS du lot 23 n'a été exporté ; aucun coût, effet ou déblocage n'a été modifié. Les PM du laboratoire et les autres icônes approuvées sont conservés.

Le jeu n'a pas été relancé. L'intégration future devra partir des sources sélectionnées ci-dessus et du format DDS natif vérifié, afin d'éviter l'ancien problème de canaux de couleur.
