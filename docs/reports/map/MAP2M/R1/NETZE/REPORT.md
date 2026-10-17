# Netze — R1

**MAP-2M_PARTIAL ; 0 transfert, 0 nouveau RGB. Thorn inchangé.**

Une image complète lisible de la planche Homann a été retrouvée à Berne, DOI e-rara-127588. L'encart distingue bien Deutsch Krone, Kamin, Bromberg et Inowrocław, y compris le prolongement méridional absent de la précédente lecture. **La couverture de la source est améliorée, pas son recalage dans le jeu.**

Datation : la notice bernoise indique [nach 1730], trop large ; l'état représentant les acquisitions de 1772 ne peut pas être simplement daté de 1730, mais sa présence ne prouve pas une impression avant 1776. Aucune année certaine n'est visible dans les éléments examinés de la planche. La notice Kórnik A V 018 décrit une édition d'atlas **1793**, malgré A.1752 dans le titre, et liste l'encart à la planche 25. Date de conception, édition de la planche et date de cet exemplaire restent distinctes. Les datations commerciales 1772/1773 ne sont pas retenues comme certification de ces deux exemplaires. Aucun scan intégral de Grund 1775 obtenu.

L'encart diffère graphiquement de Güssefeld/Homann 1775 et apporte des détails administratifs supplémentaires ; son indépendance de levé n'est pas établie. Il ne fournit donc pas automatiquement une observation géodésique indépendante de cette source du même éditeur.

`HOMOLOGUES.csv` relève les symboles de Wałcz, Piła, Bromberg, Inowrocław, la confluence d'Ujście et la piste du coude de Fordon. Les villes ne sont pas promues en homologues physiques par leur seul nom. La branche de la Gwda manque dans le raster hydrographique natif examiné ; le coude de la Vistule n'est pas assez spécifique pour choisir une correspondance ponctuelle et ne fournit pas les raccords indépendants occidentaux et méridionaux demandés.

**0 nouveau point accepté ; 0 contrôle indépendant ; aucune nouvelle transformation forcée.** L'erreur indépendante moyenne/maximale n'est pas mesurable. Les divergences antérieures de 9,50 et 12,17 pixels sont conservées comme désaccords entre hypothèses, pas comme erreur mesurée sur les centres de Piła/Wałcz. Aucun résidu d'ajustement nul n'est utilisé pour déclarer le problème résolu.

`CELL_CLASSIFICATION.csv` conserve les **162 candidats**, tous UNCERTAIN et Applied=False. Aucune cellule certaine de transfert n'est déclarée ; aucune acquisition de 1793, aucune modification de Thorn ni de Dantzig. Bromberg dans le jeu reste une anomalie ouverte, non corrigée à partir du seul nom de sa ferme. Le district méridional est désormais visible sur une source, mais aucune extension de masque n'est approuvée.

`COMPARISON.png` est une juxtaposition explicitement non recalée. Voir `../SOURCES.json` pour les empreintes et distinctions de date, et `../VALIDATION.json` pour les contrôles de préservation ; le seul changement fonctionnel autorisé dans cette passe est l'interface des centres de commerce.
