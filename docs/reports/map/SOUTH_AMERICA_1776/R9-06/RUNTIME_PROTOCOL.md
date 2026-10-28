# R9-06 — Contrôles joueur différés

Statut : **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Version : `CURRENT_RUNTIME_MANIFEST.json`. Aucune validation positive n'est préremplie ; les contrôles ont été différés par le joueur.

1. Nouvelle partie **au 1er janvier 1776**, avec le mod courant. Une sauvegarde antérieure n'installe pas les nouvelles données d'histoire.
2. Vérifier les deux provinces wayuu et la présence de WYU, ses noms, son drapeau et son autonomie. Vérifier que Riohacha et la portion de Sinamaica/Maracaibo restent SC2.
3. Au démarrage, vérifier les **7 600 habitants de la portion WYU d'Antioquia** ; relever la date si le temps a déjà avancé. Vérifier les lois effectivement actives, la religion par défaut, l'alimentation, l'emploi et l'absence de clé brute. Aucun bâtiment industriel ou bataillon nouveau n'est prévu.
4. Vérifier Nassau/Berbice néerlandais, l'Approuague français, les trois provinces d'arrière-pays autonomes et l'absence de double propriétaire sur `x6C6251`. Comparer aux deux cartes avant/après.
5. Vérifier les accès réels au marché et le ravitaillement des portions néerlandaise et française. Les trajets de terre ont été vérifiés statiquement ; les convois, les droits d'accès, les prix et le fonctionnement économique doivent être observés dans le moteur.
6. Laisser tourner quelques mois en notant la durée effectivement jouée, puis sauvegarder/recharger. Relever famine, évolution des effectifs, comportement des pays et éventuels crashs. Conserver les logs datés ; distinguer dette antérieure et régression de ce lot.
7. Témoins de non-régression : Tabatinga et les raccords R9-05 ; Mapuche/Huilliches et Chiloé R9-04 ; Sacramento dans l'Uruguay partagé ; noyaux CENTRAL. Leurs propres protocoles restent en attente tant qu'ils n'ont pas été joués.

Les terres marronnes et les frontières ethniques fines restent réservées ; un chargement réussi ne les certifie pas historiquement.
