# Protocole groupé — installations SERG déjà présentes

26 octobre 2026. **Aucun territoire à reconstruire pour obtenir un reçu.** Les huit lignes totalisent 11 points possibles, sous réserve des critères, de la portée réellement vérifiée et du validateur. Aucun point n’est accordé par ce document.

## Conditions communes

Utiliser une nouvelle partie au **1er janvier 1776** sur la version actuelle du mod. Si votre partie répond déjà à ces conditions, il suffit de le préciser et de compléter les seuls contrôles non effectués. Inspecter les pays avec vos moyens habituels ; ne pas modifier leurs provinces, habitants ou bâtiments pour provoquer artificiellement un résultat.

Un seul mois complet peut couvrir les huit lots inspectés dans la même partie. Signaler séparément une ligne non inspectée ou inaccessible ; un retour global ne doit pas étendre la portée d’un ancien reçu. Les contrôles purement statiques déjà réalisés ne sont pas à reproduire comme comptages de pixels en jeu.

| Tâche | Contrôles visuels/fonctionnels encore à attester |
| --- | --- |
| SC2-MAP2A-VALIDATION, 2 points | Quatre corrections : Trois Ligues représentées sous SWI en Lombardie (`x9AC196`), deux portions silésiennes AUS sans double propriétaire et rattachées à Moravie (`x71E080`, `xF0E080`), portion autrichienne de Teschen correctement rattachée techniquement (`x9061E0`). Contrôler habitants, bâtiments et recrutement associés ; Bergame reste VEN. Le registre Teschen plus récent est une vérification distincte ci-dessous. |
| SC2-LUXEMBOURG-VALIDATION, 1 point | Luxembourg sous BEO, aucun État LUX initial, BEO terre de la Couronne d’AUS ; formation luxembourgeoise et général présents, trois unités conservées. La population transférée est de 137 881 dans les scripts, mais **ne pas attendre l’ancien total national BEO de 2 907 881**, antérieur à d’autres découpages. L’administration demande d’abord la revue décrite ci-dessous. |
| SC4-MILAN-VALIDATION, 2 points | Raccord autrichien Milanais–Crémonais présent et continu ; maintien des voisins vénitiens et suisses. Le test ne certifie pas toute la frontière lombarde. |
| SC4-PIEDMONT-VALIDATION, 1 point | SAR membre du bloc impérial, seuls les neuf RGB piémontais enregistrés par ce lot ; l’île de Sardaigne reste exclue. Ne pas assimiler appartenance du pays et ensemble de ses terres. |
| SC5-MINDEN-VALIDATION, 1 point | Noyau de Minden sous PRU, voisinage et mécanismes impériaux cohérents ; le sous-lot de 76 cellules reste distinct de Ravensberg. |
| SC5-COLOGNE-VALIDATION, 1 point | Portions du duché de Westphalie et du Vest sous Cologne/KCL ; maintien des voisins prussiens et absence de restitution de toute la Westphalie à Cologne. |
| SC5-MAINZ-VALIDATION, 2 points | Les trois couches de Mayence : Rheingau/Spessart, Bergstraße et Tauber. Propriétaires, noms et mécanismes impériaux cohérents ; Erfurt est exclue de cette attestation. |
| SC6-SWABIA-CONTINUATION-VALIDATION, 1 point | Noyaux distincts de Fürstenberg/SFU et Ellwangen/SEW, propriétaires et capitales cohérents, maintien des voisins. Les anciens reçus SWABIA_FINISH et SWABIA_COMPLETION ne remplacent pas cette ligne. |

## Point à trancher avant de clôturer Luxembourg

L’intégration initiale conservait deux déclarations d’administration, dont le cumul moteur n’était pas établi. Le recalibrage BUILD ultérieur prévoit **BEO : trois niveaux en Flandre et zéro en Wallonie** ; les deux anciens blocs ont disparu. Les autres éléments du transfert sont conservés statiquement.

La matrice runtime finale contient aussi un objectif LUX/Wallonie de niveau 1, alors que LUX n’a pas d’État initial. Cet objectif doit être réconcilié avec BUILD/ECON ; ce n’est pas une administration BEO actuellement installée.

Indiquer si la clôture doit porter sur cette allocation administrative actuelle, ou si vous souhaitez un ajustement coordonné avec BUILD/ECON. Un test réussi de cette version ne sera pas présenté comme preuve que les deux anciens blocs sont toujours présents. Aucun bâtiment n’est réinstallé par cette passe.

## Teschen : compléter seulement ce qui manque

Votre vérification du résultat en jeu est enregistrée. Pour compléter TE-R-CORE, préciser si elle a été faite dans une nouvelle partie en 1776 et si **un mois puis sauvegarde/rechargement** ont été effectués sans anomalie. Sinon, compléter ces étapes. Confirmer que la portion autrichienne est reconnue impériale, que les portions galiciennes voisines ne sont pas ajoutées et que les neuf électeurs restent conservés.

La décision de conservation B de [TESCHEN_CLOSURE_REVIEW.md](TESCHEN_CLOSURE_REVIEW.md) demeure distincte. Ni ce test ni cette décision ne valident automatiquement tout MAP2A ou un recensement historique.

## Retour utile

Pour chaque ligne réellement inspectée : nom de tâche, réussite/échec, anomalie éventuelle. Préciser une fois les conditions communes réellement remplies : nouvelle partie/version, mois complet. Pour Teschen, préciser aussi sauvegarde/rechargement. Une date effective, une capture ou une mesure économique n’est pas exigée et ne sera pas inventée.

La tâche Luxembourg est actuellement BLOCKED pour conflit de portée administrative. Les sept autres lignes peuvent être testées indépendamment de cet arbitrage ; ne pas attendre sa résolution pour communiquer leurs résultats.
