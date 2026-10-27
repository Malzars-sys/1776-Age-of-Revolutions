# SERG TERRITORIAL 1.0 — PROGRESSION : 34,89 %

Campagne de levée des blocages, 26 octobre 2026. **82/235 points avant/après, 24/81 tâches qualifiées.** Aucun nouveau territoire ou sous-lot fonctionnel créé ; aucune attestation complète ajoutée.

## Résultat de l’audit des installations

Les huit tâches ont été rapprochées du workspace actuel, de leurs géométries et des reçus antérieurs. Leur potentiel cumulé est de **11 points**, non encore créditables. Aucun dossier entièrement terminal mais oublié du calcul n’a été démontré.

Le contrôle strict donne **133 réussites sur 135**, avec deux écarts concentrés sur les anciennes déclarations d’administration luxembourgeoise. Les noyaux politiques, POPs et unités du transfert Luxembourg restent présents. Le recalibrage BUILD ultérieur explique la configuration actuelle de trois administrations en Flandre et zéro dans la portion BEO de Wallonie. La matrice runtime finale contient encore un objectif LUX/Wallonie de niveau 1, malgré l’absence d’État LUX initial. La tâche Luxembourg est donc reclassée BLOCKED P1 ; les sept autres validations restent en attente de reçu. Les deux écarts restent visibles ; ils ne sont pas appelés deux contrôles réussis et aucune ancienne baseline n’est restaurée.

[Audit structuré des huit tâches](INSTALLED_VALIDATION_AUDIT.json) · [réconciliation Luxembourg](LUXEMBOURG_SCOPE_RECONCILIATION.json) · [protocole groupé](PLAYER_TEST_PROTOCOL_GROUPED.md).

Les anciens prompts MAP-2F/MAP-2I indiquent des tests en jeu pour des lots antérieurs, sans donner à MAP2A la durée et la portée détaillée aujourd’hui manquantes. L’approbation de l’intégration luxembourgeoise n’est pas une attestation de tous ses mécanismes. Les reçus MAP2L limitent explicitement leurs lots ; Minden est exclu du reçu antérieur, et SWABIA_CONTINUATION n’est pas validé automatiquement par FINISH. Aucun reçu n’est étendu.

## Blocages classés et tâche effectivement traitée

La [matrice des 24 tâches BLOCKED après le reclassement Luxembourg](BLOCKED_MATRIX.md) distingue ce qui est installé, les obligations essentielles, les sources, les besoins techniques et humains, les conflits possibles et les actions de clôture. Ses points sont conditionnels. Elle ne requalifie pas toutes les lacunes en précision cadastrale facultative.

**SC2-TESCHEN seule est traitée** après cet audit. MAP2A et TE-R-CORE sont conservés, sans recréer territoire, POPs, bâtiments ou recrutement. La nouvelle information humaine est une observation en jeu de portée limitée, enregistrée séparément ; aucun mois, sauvegarde/rechargement, nouvelle partie ou date effective n’est ajouté.

La [décision proposée](TESCHEN_PROPOSED_CLOSURE_DECISION.json) et son [examen détaillé](TESCHEN_CLOSURE_REVIEW.md) permettent de trancher la conservation B dans le périmètre de la tâche. La réserve démographique reste exposée : aucune population historique comparable n’est fabriquée. **La tâche reste BLOCKED P1 et ne gagne aucun point** tant que la décision et les critères humains ne sont pas réellement satisfaits. Une procédure sans correction supplémentaire ne sert pas à contourner le test du registre précédemment installé.

## Suite et protections

La prochaine action est le retour groupé sur les contrôles manquants, avec les décisions de portée Luxembourg/Teschen. La prochaine réconciliation recommandée est SC2-LUXEMBOURG-VALIDATION, pour son conflit de portée administrative ; elle n’est pas traitée en clôture ici. **SC3-HOLSTEIN et la création systématique de nouveaux territoires restent suspendus.**

Toutes les preuves anciennes sont préservées. Les travaux WORLD, TECH, ECON et autres sont comparés aux empreintes de début de passe et leurs évolutions conservées. Aucun fichier fonctionnel du mod ou du vanilla n’est écrit. Le seul ajustement de code partagé concerne l’affichage du suivi afin de présenter la campagne active au lieu d’une invitation à créer un nouveau territoire ; ni calcul des points ni critères terminaux ne sont assouplis.

## Contrôles effectivement exécutés

- Audit des huit installations, réexécuté après les évolutions concurrentes : **133/135**, avec les deux attentes historiques d’administration Luxembourg absentes. Statut strict FAIL conservé, réconciliation requise.
- Contrats de la campagne : **16/16** ; non-régression du validateur et du rendu : **27 réussis sur 28, aucun échec et un test déjà désactivé** car réservé au cliché immuable de l’initialisation. Les critères terminaux et la formule des points sont inchangés.
- Conservation Teschen : **12/13** ; les 179 cellules, le titre AUS, les sept fichiers livrés et les limites de l’observation humaine passent. Le treizième contrôle, égalité de tout le workspace fonctionnel avec le début de passe, échoue en raison de modifications concurrentes conservées : ce n’est pas un résultat moteur ni un défaut territorial Teschen.
- Vérification complémentaire des régions contenant les titres impériaux : **4/4**, soit 612 affectations de propriétaires, 480 groupes de population, 294 déclarations de bâtiments et 119 déclarations d’unités identiques au début de passe. Cette comparaison ne certifie pas chaque frontière du bitmap ; les cellules des huit lots et de Teschen font l’objet des contrôles bornés ci-dessus.

Les différences concurrentes et leurs empreintes figurent dans [CONCURRENT_CHANGES.json](CONCURRENT_CHANGES.json). Au relevé final, 23 fichiers fonctionnels diffèrent du début de passe et neuf anciennes pièces WORLD ont évolué ; aucune de ces écritures n’a été réalisée ou restaurée par cette campagne. Les anciennes preuves SERG imbriquées, HEAD, branche et index Git sont inchangés. Les résultats détaillés figurent dans [FINAL_CHECKS.json](FINAL_CHECKS.json) et [TEST_RESULTS.json](TEST_RESULTS.json).

Aucun lancement moteur n’a été effectué par l’agent. Les résultats antérieurs de 530 tests appartiennent à la passe Teschen précédente ; ils ne sont pas présentés comme exécutés de nouveau ici.
