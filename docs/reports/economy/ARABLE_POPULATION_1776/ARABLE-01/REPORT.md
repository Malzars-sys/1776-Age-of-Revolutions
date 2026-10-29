# ARABLE-01 — Diagnostic de capacité et concordance avec les famines

Référence historique : **1er janvier 1776**. Diagnostic préparé le 29 octobre 2026. Le relevé et le tableau ci-dessous sont conservés comme état **avant stabilisation**. Le joueur a ensuite explicitement choisi le correctif provisoire d’Agra : **483 → 764 terres arables**, installé et contrôlé séparément. Voir [le reçu et le protocole après installation](PROVISIONAL_INSTALLATION.md). La population n’est pas historiquement confirmée ; aucun résultat moteur après correction n’est revendiqué.

## Résultat utilisable

[Le tableau interactif](delivery/TABLEAU.html) inventorie **1 405 entrées État–propriétaire** et rapproche **1 402 portions effectivement chargées** dans la partie ouverte. Les trois entrées supplémentaires sont des historiques de population français sans portion possédée à Alger, Constantine et Oran. Elles sont signalées comme incohérences de références à examiner, pas comme trois États actifs auxquels ajouter des terres.

La session observée est Victoria 3 **1.13.11**, au 1er janvier 1776, en pause. Une sauvegarde locale distincte a été créée depuis le jeu, cloud décoché, puis convertie en lecture seule avec le Rakaly déjà installé. L'original n'est pas réécrit ; son empreinte et sa copie archivée sont dans `SAVE_RECEIPT.json`. Le joueur a retrouvé sa carte, partie toujours en pause. Il n'y a eu ni relance, ni simulation après le départ, ni test d'un correctif démographique ou agricole.

Le registre moteur contient **61 crises alimentaires actives** :

| Situation au relevé | Portions |
|---|---:|
| Crise et saturation selon la capacité chargée | 31 |
| Crise sans saturation démontrée | 30 |
| Saturation sans crise déclarée | 221 |
| Ni crise ni saturation démontrée | 1 120 |

Ces catégories servent au tri des causes possibles. Ce ne sont pas des diagnostics historiques, des preuves de rentabilité ou une mesure de précision prédictive du modèle.

## Concordance avec la carte native

Le mode `mm_global_starvation` utilise la sécurité alimentaire du moteur. La présence du marqueur de crise et son entrée dans `famine_manager` sont conservées comme observations réelles. Les pourcentages sont importables séparément depuis une observation de l'interface datée et liée à l'empreinte de la sauvegarde.

Les seuils effectifs ont été lus dans le mod : sécurité alimentaire sous **0,4** pour la faim, sous **0,2** pour la grande famine. L'infobulle native déclare une crise lorsque **les deux** seuils de population sont atteints : au moins **35 %** affamés et au moins **15 %** en grande famine. Le diagnostic d'emploi ne remplace pas cette règle.

À Agra marathe, cinq comparaisons concordent : crise active, cohérence des pourcentages lus avec les seuils, terres, paysans et sans-emploi, en tenant compte des arrondis de l'interface. La source précise de chaque nombre figure dans `UI_OBSERVATIONS.json` et [AGRA_RESEARCH.md](AGRA_RESEARCH.md). Les **98 %**, **62 %** et **36 %** sont des lectures arrondies de l'interface, pas des fractions précises reconstituées depuis une couleur.

Une réserve importante a été détectée : les champs `food_security` des POPs de la sauvegarde initiale sont encore à zéro avec l'énumération `secured`, même pour Agra où l'interface et le registre de crises indiquent une famine. Leur cause interne n'est pas démontrée ; ils ne permettent pas de produire des pourcentages fiables à cette date. **Ils ne sont donc jamais convertis en 0 % de faim.** Les pourcentages non observés restent inconnus dans les exports, tandis que les 61 marqueurs de crise sont bien conservés. L'outil ne prétend pas reproduire exactement chaque nuance du dégradé de la carte pour ces autres portions.

Deux témoins montrent pourquoi la distinction est nécessaire : **Alxa**, en crise mais sans déficit global d'emploi selon le relevé ; **Zhejiang**, avec plus de trois millions de sans-emploi mais aucune crise déclarée. Bihar et les grands marchés européens montrent également qu'un emploi manquant et une famine ne sont pas équivalents. Aucun de ces cas n'est « corrigé » automatiquement.

## Méthode du diagnostic statique

- Lecture des définitions effectives du mod et du vanilla canonique, surcharges et `replace_path` pris en compte. Les collisions de définitions restent listées, sans être toutes traitées comme des erreurs.
- Calcul par **portion État–propriétaire**, indispensable pour les États partagés. La part des terres est estimée à partir des cellules possédées ; la valeur chargée du moteur devient prioritaire si une sauvegarde est fournie. La concordance 483 terres régionales / 444 marathes / 39 Garhwal est vérifiée à Agra.
- Les habitants incluent travailleurs et dépendants. En mode statique, trois scénarios **25 %, 30 %, 35 %** de travailleurs sont publiés ; ils ne sont pas des ratios historiques universels. En mode sauvegarde, les effectifs exacts des POPs remplacent ces hypothèses.
- La capacité par niveau vient des PM effectifs : **10 000 emplois** pour les rizières de subsistance, **5 000** pour les fermes ordinaires, et les autres formes sont lues dans leurs propres définitions. Les groupes de PM sont combinés ; les suppressions d'emplois dues à l'automatisation compensent les emplois de base avant de borner le résultat à zéro.
- Les bâtiments commerciaux agricoles et plantations consomment des terres. Tous les emplois non agricoles connus sont comptés séparément. Les exploitations productives européennes ne sont donc pas ignorées ; aucune exemption géographique arbitraire n'est codée.
- Les PM non spécifiés et les déclarations répétées de bâtiments donnent une **enveloppe**, pas un choix silencieux. Les variantes de l'enveloppe peuvent comprendre des techniques non disponibles : le diagnostic avertit qu'il s'agit d'une borne de capacité, pas d'un PM initial garanti. Les niveaux natifs permettent de résoudre le chargement réellement observé.
- Les emplois inconnus et références manquantes sont signalés. Certains propriétaires indépendants de bâtiments n'ont pas d'identifiant `workplace` : leur absence de lieu de travail ne signifie pas chômage. La statistique de sans-emploi du moteur, vérifiée dans l'interface, reste prioritaire. La capacité connue n'est jamais présentée comme inférieure aux effectifs déjà employés observés ; le complément non modélisé demeure explicite.
- L'export distingue aussi les sorties marchandes de grain à effectif plein, avant bonus, intrants et accès au marché. **Elles ne constituent pas un bilan alimentaire des habitants** : autoconsommation, revenus de subsistance, paniers, prix, importations et statut d'emploi peuvent changer l'accès à la nourriture. La capacité d'emploi ne garantit pas les embauches ni les qualifications.

## Agra et décisions historiques

Les **23 928 236 habitants** de la portion marathe viennent d'une hausse globale de l'Inde appliquée à des proportions provinciales héritées ; aucune estimation locale propre à 1776 n'était fournie. Le recensement historique consulté confirme la fragilité et les changements de périmètre des comptages anciens, mais **ne valide pas ce chiffre pour STATE_AGRA en 1776**. La famine de 1783–1784 ne peut pas être avancée au début du scénario par commodité.

Une nouvelle population précise n'est donc pas inventée. Si le joueur choisit de conserver le stock courant, un scénario transparent propose **483 → 764 terres régionales**, soit environ 258 niveaux de subsistance supplémentaires pour la portion marathe. Ce serait un réglage provisoire de gameplay, avec un effet durable sur le potentiel agricole futur. Il ne prouve pas la fin de toute faim paysanne. Préimages, empreintes et patch borné sont préparés ; aucune approbation n'est déduite du temps écoulé sans réponse.

Les prochaines passes doivent vérifier population **et périmètre**, capacité, crise historique éventuelle et fonctionnement économique réel avant de choisir entre correction démographique, terres, bâtiments, PM ou accès aux marchés. Voir [NEXT_PASSES.md](NEXT_PASSES.md).

## Vérifications exécutées et limites

Résultats machine : `VALIDATION.json`, `UNIT_TEST_RESULT.json`, `DASHBOARD_QA.json`, `UI_RECONCILIATION.json` et le diagnostic livré.

- **12 tests de calcul/interprétation réussis**, notamment habitants versus travailleurs, partage des terres, distinction des subsistances, héritage des groupes agricoles, niveaux et propriété, automatisation, inconnues et unités des observations.
- **8 contrôles du script réel du tableau réussis hors navigateur** : recherche, portions distinctes d'Agra, valeurs observées visibles, filtre retrouvant les 61 famines, conservation des 30 cas sans saturation, bascule statique et recherche vide.
- **5 comparaisons avec l'interface d'Agra réussies**, avec sa sauvegarde datée. Cela valide la concordance du relevé, pas un correctif qui n'est pas encore installé.
- **215 fichiers d'entrée contrôlés inchangés** depuis la lecture. Sauvegarde originale inchangée après conversion. Aucune écriture Git, modification du vanilla, modification de frontières ou réécriture d'ancienne baseline.
- **23 différences de population** entre historiques et sauvegarde sont publiées séparément ; certaines sont très petites, d'autres significatives, notamment Alxa. Elles peuvent venir de l'initialisation ou des versions chargées. Elles ne sont pas effacées ni déclarées automatiquement pertes de population. Les valeurs natives et historiques d'Agra concordent exactement.

L'aperçu du fichier HTML dans le navigateur intégré a été refusé par sa politique d'URL pour le protocole `file://`. Aucun contournement n'a été tenté. Le fonctionnement du script a été contrôlé hors navigateur ; **aucune validation visuelle du rendu HTML n'est revendiquée**. Le fichier autonome reste disponible pour une ouverture locale par le joueur.

## ColGrep et ressources

Un appel local `colgrep.exe --agent` a été tenté pour retrouver les audits de population, capacité de subsistance et preuves d'Agra. Il a échoué avant l'exécution du modèle, lors de la création du verrou d'index : accès refusé. Aucun changement de modèle, d'intégration ou reconstruction d'index. Repli sur `rg`, les outils connus et les sources historiques. **Zéro exécution 2B confirmée**, donc aucune économie de quota attribuable à ColGrep dans cette passe. Pas de compteur fiable de tokens par mission ou d'estimation comparative inventée.
