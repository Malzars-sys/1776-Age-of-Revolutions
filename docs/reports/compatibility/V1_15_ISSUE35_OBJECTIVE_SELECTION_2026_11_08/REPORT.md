# Mission 35 — sélection des objectifs

**IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**, 8 novembre 2026. Le correctif est installé dans `gui/objective_types.gui` du mod. Un seul fichier de jeu est ajouté ; aucun objectif ni texte joueur n’est modifié.

## Cause et correction

Le vanilla canonique 1.15 définit quatre objectifs, tutoriel compris. Le mod en définit cinq : tutoriel, bataille pour l’Inde, rivalités impériales, âge des révolutions et **Républiques marchandes**. Le sélecteur est hérité du vanilla via `frontend_bookmarks.gui` et `objective_selection_menu`.

Les cinq cartes imposaient chacune 320 unités de largeur. Avec les 340 unités du Bac à sable et les 8 unités d’espacement, leur budget nominal atteignait **1 948**, pour une rangée plafonnée à **1 680**. Les quatre cartes vanilla demandent 1 628 unités dans la même disposition. Cette divergence explique le dépassement structurel ; le chevauchement en jeu est le symptôme rapporté par le mainteneur.

La copie locale du fichier natif comprend cinq modifications bornées :

1. Retrait du minimum horizontal de 1 400 sur la rangée ; la largeur disponible peut être utilisée sur un écran plus étroit.
2. Cartes d’objectifs en expansion horizontale, sans minimum fixe de 320 ; le maximum natif de 320 reste conservé.
3. Bloc du titre explicitement contenu dans la largeur de sa carte.
4. Retrait de la largeur fixe de 250 des titres ; leur ajustement de police, taille minimale et élision natifs sont conservés.
5. Bac à sable dans une colonne réservée de 340 unités, au lieu de concurrencer les objectifs pour l’expansion horizontale.

Les cinq objectifs restent dans `GameSetup.GetObjectives`. Les 80 expressions dynamiques du fichier natif, leur ordre, les clics, conditions de disponibilité, infobulles, animations et panneaux de recommandation sont inchangés. L’icône historique `great_game.dds` référencée par l’objectif marchand existe encore dans le vanilla ; elle n’est pas supprimée ni remplacée.

## Vérifications

- Les cinq modifications inversées reproduisent exactement le texte du fichier natif : aucune autre modification de l’interface.
- Délimiteurs vérifiés ; expressions dynamiques et clics identiques au natif.
- Modèle de budget horizontal évalué pour sept largeurs d’interface, de 1 024 à 2 560 unités : aucune somme des largeurs attribuées ne dépasse la rangée dans ce modèle.
- 2 484 fichiers existants de scripts/données suivis par empreinte, dont les objectifs, lois, carte et corrections concurrentes : aucun changement observé pendant le contrôle.
- Vanilla conservé en lecture seule ; aucune opération Git d’écriture.

Les modèles supposent la répartition habituelle `hbox` / `expanding` / `preferred`. Ils ne constituent pas des captures moteur et ne certifient pas la lisibilité des polices à toutes les résolutions ou échelles. `BASELINE.json`, `CHANGES.patch` et `VALIDATION.json` contiennent les empreintes, remplacements exacts et budgets calculés ; `VALIDATION_R1.json` conserve le premier contrôle avant l’ajustement final du bloc de titre.

## Essai visuel restant

L’inventaire des fenêtres a confirmé que **Victoria 3 était fermé** pendant cette intervention. Aucun rendu après correctif, aucune résolution de reproduction ni absence de nouvelle erreur GUI ne sont donc certifiés. La préférence locale relevée est le français avec échelle GUI 1,5 ; ce réglage sur disque n’est pas une mesure du viewport de la capture initiale.

Au prochain lancement avec le mod : ouvrir Nouvelle partie et vérifier les cinq cartes et le Bac à sable ensemble ; sélectionner puis désélectionner les Républiques marchandes, vérifier les pays recommandés Gênes/Venise et le survol, puis revenir au Bac à sable. Relever résolution, échelle et langue réellement utilisées. Contrôler ensuite le même écran en anglais et à une autre échelle représentative, puis comparer les logs GUI au relevé antérieur.

L’essai peut rester dans les menus, sans démarrer ni remplacer une sauvegarde. Le statut Done attend la validation visuelle du mainteneur.
