# MAGHREB-02 — Contrôle territorial du Maroc à l'Égypte

26 octobre 2026. **AUDIT_COMPLETE_TERRITORIAL_WORK_REMAINS**. Référence : 1er janvier 1776. Cette passe répond à la demande de rechercher les découpages encore nécessaires ; elle n'installe aucun nouveau territoire. Les tests en jeu Maghreb–Égypte sont regroupés, statut NOT_RUN. L'autorisation conditionnelle de passer en Afrique subsaharienne ne s'applique pas encore : des problèmes territoriaux subsistent.

## Résultat de la vérification

| Priorité | Secteur | Constat actuel et travail restant |
| --- | --- | --- |
| P0 | Interface Maroc–Tekna | Neuf provinces de STATE_INNER_MOROCCO sont déclarées simultanément MOR et TEK. Il faut déterminer le partage effectif, puis supprimer les doubles attributions. L'allégeance au sultan ne démontre pas une administration directe. |
| P0 | Arrière-pays de Tripoli | xAFD438 et xD5C61D sont déclarés TRI et ZWY ; chacun est même répété dans la liste ZWY. La géométrie est intérieure, pas celle du port de Tripoli : aucun transfert fondé sur le seul nom de l'État. |
| P1 | Fezzan | Le TAG FZN existe mais ne détient aucune province. Le point natif de Murzuq, xCA4E6B, est ZWY ; Sabha est également dans la portion ZWY. Les sources attestent le pouvoir local des Awlad Muhammad et ses rapports tributaires avec Tripoli au XVIIIe siècle. Un noyau territorial autour des oasis reste à rétablir, sans lui attribuer tout le désert libyen. |
| P1 | Siwa | Le point natif explicitement nommé Siwa, xE0D021 dans STATE_MATRUH, appartient directement à EGY. L'intégration égyptienne de 1820 est postérieure au scénario. Il reste à isoler l'oasis autonome ; le polygone natif entier n'est pas certifié comme son périmètre. |

Liste exacte des neuf RGB Maroc–Tekna : x0FA44F, x4DE76B, x53C5EF, x88C527, x8ACEDE, x8DCD09, x9E582E, xE80E2E, xF414B2. Les deux conflits tripolitains représentent 153 et 298 pixels ; leurs boîtes et toutes les attributions sont dans DUPLICATE_ASSIGNMENTS.json. Ces deux couleurs et les neuf couleurs marocaines sont des conflits existants, pas de nouvelles provinces créées par cet audit.

Ce sont des problèmes de répartition des territoires, distincts des personnages, des lois, des bâtiments ou des améliorations économiques. Les contours exacts des deux noyaux d'oasis restent à établir ; aucun masque cadastral arbitraire n'est proposé. Pour une future activation de FZN ou d'un pays de Siwa, vérifier les profils initiaux et leur compatibilité technique est une dépendance d'installation, pas un prétexte à reprendre le flavor.

## Couverture et limites

Vingt régions natives examinées : Marrakech, Fez, Rif, Maroc intérieur ; Oran, Alger, Constantine ; Tunisie ; Tripoli, Cyrénaïque et désert libyen ; Basse, Moyenne et Haute-Égypte, Matruh, Sinaï et désert égyptien ; interfaces Sahara, Sahara oriental et occidental. TERRITORIAL_INVENTORY.json contient toutes leurs portions, couleurs, répétitions et conflits. La carte de diagnostic utilise le dernier propriétaire déclaré en cas de doublon : elle ne représente pas un chargement moteur observé.

Aucune autre nouvelle frontière certaine n'est établie par cette passe. Cela ne certifie pas tous les polygones :

- Alger/Mascara/Constantine et la Kabylie restent représentés à leur échelle actuelle ; aucun nouveau pays n'est découpé à partir d'une seule subdivision administrative ou d'une source générale sur l'autonomie.
- Tunis, Djerba et le littoral de Tripoli restent conservés. La prise de Tabarka par Tunis en 1741 ne justifie aucune restitution génoise en 1776. Une concession française de commerce ou de pêche ne devient pas automatiquement une souveraineté française.
- Vélez et Alhucemas sont historiquement espagnols, mais leur correspondance avec les minuscules formes du fond doit être distinguée d'une annexion du littoral marocain. Cette limite de résolution ne justifie ni une côte inventée ni un agrandissement du Rif. Ceuta, Melilla, Oran et le raccord de Gibraltar déjà installés sont conservés.
- Kufra : les sources consultées divergent sur la chronologie de la conquête zuwayya (XVIIIe siècle ou milieu du XIXe). Le point natif al-Jawf est ZWY ; aucune correction automatique vers TBI n'est défendable à partir de la seule date de 1840. Incertitude maintenue, pas une correction impérative supplémentaire démontrée.
- Les espaces sahariens, nomades et le TAG décentralisé SD1 ne sont pas des preuves de frontières étatiques modernes. Pas d'annexion de tout le désert à l'Égypte ni de partage rectiligne inventé.

La première projection de diagnostic comportait deux points de calibration mal identifiés (Mascara confondue avec Oran, El Salloum avec Marsa Matruh). Elle est explicitement rejetée pour toute édition territoriale dans GEOGRAPHIC_SCREENING.json. Les rapprochements décisifs utilisent les libellés natifs et leurs locators, notamment Siwa et Murzuq ; aucune précision géodésique fictive n'est revendiquée.

## Conservation, preuves et suite

Aucun fichier fonctionnel écrit : zéro pixel, RGB, propriétaire, POP, institution, technologie, recette, PM, personnage ou bâtiment modifié par cette passe. Population mondiale capturée : **837 328 539 avant et après**, delta 0. Git/index, carte et noyaux précédents contrôlés. Les évolutions concurrentes Floride et suivi SERG sont archivées dans EXTERNAL_REVIEW.json, sans restauration de baseline ni validation de leur fonctionnement par WORLD.

Contrôles reproductibles : `python tools/world1776_maghreb02_audit.py`. VALIDATION.json porte le résultat courant. VALIDATION_RUN01.json conserve le premier résultat : deux assertions supposaient à tort que les seuls doublons étaient tripolitains ; le garde de conservation a aussi révélé des écritures indépendantes. Ces constats sont expliqués, pas effacés comme des erreurs de jeu.

La file TERRITORIAL_QUEUE.json reste ouverte. Prochaine passe proposée : délimitation et installation d'un noyau du Fezzan, puis Siwa et résolution sourcée des interfaces Maroc–Tekna/Tripoli. Aucun lancement de l'Afrique subsaharienne dans cet audit. Les vérifications moteur figurent dans GROUPED_RUNTIME_ITEMS.md, sans demande de test intermédiaire ni attestation fictive. Aucun nouveau point de progression régionale : WORLD reste à 10/320, zéro validation joueur.

Résultat final de l’exécution : **19/19 contrôles de reproduction et de conservation ciblée réussis**. Les quatre anomalies historiques/territoriales restent ouvertes ; ce résultat ne les transforme pas en territoires corrigés. Douze différences concurrentes sont identifiées et archivées ; leur préservation ne vaut pas validation de leur logique par WORLD.
