# MIL-NAV-USA-1776

**IMPLEMENTED — READY_FOR_RUNTIME_VALIDATION.** Nouvelle partie recommandée ; aucune conversion d'anciens modèles de navires n'est imposée à une sauvegarde.

## Correction

Les cinq navires américains deviennent `ship_type_aor1776_armed_merchantman` : **marchands armés**, avec la formation, le QG, Hopkins et l'effectif de cinq navires conservés. Le nouveau type reprend les statistiques, coûts, capacité d'équipage, rôle de coque et caractéristiques économiques de la caravelle faible déjà utilisée par le mod. Il ne reçoit aucune puissance supplémentaire.

Le prérequis de coque devient organized_workshops, déjà possédé par USA. L'audit a aussi identifié enclosed_dock_systems sur les équipements de base d'origine : changer seulement le type n'aurait pas suffi. Cinq entrées d'équipement propres au mod reprennent les petits équipements existants, avec le même déblocage accessible ; les emplacements ne proposent que ces équipements contemporains. Aucun moteur à vapeur, blindage ou canon futur. Les anciennes caravelles, galères et leurs équipements restent inchangés pour tous les autres pays.

Le nouveau type reste techniquement sélectionnable par les pays possédant son prérequis ; il n'existe pas ici de filtre national de construction dont la compatibilité serait inventée. Son poids IA est nul pour éviter de modifier les choix navals mondiaux. Tester séparément le renouvellement de la flotte par l'IA américaine ; l'accessibilité manuelle de la coque ne garantit pas sa sélection par l'IA.

La capacité de base reste de 200 marins par coque, soit 1 000 pour cinq navires, avant autres effets. Les coûts de coque et de chaque équipement sont repris sans réduction ; le grain et le bois dur d'entretien restent ceux de la caravelle. Quatre niveaux d'administration navale sont déjà scriptés aux USA, avec les ports et chantiers existants : aucun bâtiment ou marin gratuit n'est ajouté. **L'expansion du bâtiment d'administration navale reste soumise à state_dockyard_systems**, absent au départ ; cela n'est pas maquillé par un déblocage technologique gratuit. Vérifier séparément le fonctionnement des niveaux existants et la construction/remplacement des nouvelles coques. La correction traite la coque et son équipement, sans modifier mondialement les institutions navales.

## Contexte

Le [Naval History and Heritage Command, Esek Hopkins](https://www.history.navy.mil/browse-by-topic/people/historical-figures/esek-hopkins.html) décrit une flotte initiale formée de bâtiments marchands transformés pour la guerre. Le nombre de cinq du mod est conservé comme abstraction déjà testée par le joueur, pas présenté comme l'inventaire historique exhaustif des huit bâtiments mentionnés par cette source. Une conversion marchande est plus défendable en janvier 1776 qu'un don de technologie de grands chantiers.

## Fichiers et validation

Nouveaux fichiers : common/ship_types/1776_usa_armed_merchantman.txt et common/ship_modifications/1776_usa_armed_merchantman.txt. Dans l'historique nord-américain, seul l'identifiant de type de l'unique contingent naval USA change. Les sept créations de commandants, tous les bataillons et toutes les autres formations restent identiques à la base de R2. Noms et description du navire, noms des équipements en FR/EN dans le fichier R2 dédié.

Le validateur R2 contrôle la disponibilité de la coque et des cinq équipements, les cinq options, les coûts/statistiques conservés et la modification unique de l'historique. Il ne simule pas la fabrication d'une coque.

En jeu : USA, nouvelle partie, Marine → flotte existante, cinq marchands armés, Hopkins ; inspecter les cinq équipements et l'absence de technologie manquante. Relever marins recrutés, frais et approvisionnement à la pause, J+1, J+7 et M+1. Sur une copie de test, construire un navire de remplacement, vérifier chantier, administration, équipage et coût ; ne pas donner une technologie en console dans la partie de référence. Vérifier une flotte française et portugaise pour confirmer qu'elles gardent leurs anciens types. Les sauvegardes antérieures conservent leurs anciennes coques et ne prouvent pas le comportement du nouvel historique.
