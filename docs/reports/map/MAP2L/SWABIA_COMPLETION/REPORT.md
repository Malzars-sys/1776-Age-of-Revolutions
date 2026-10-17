# MAP-2L — Souabe, dernière passe majeure de juridictions

Date : 14 octobre 2026. Mod Victoria 3, version de référence 1.13 ; date historique 1 janvier 1776.

## Attestation manuelle reçue après cette passe

**PASS_RUNTIME_USER_VALIDATED** pour les modifications inspectées, selon les instructions transmises par le joueur : nouvelle partie et un mois sans problème signalé. Voir `../RUNTIME_USER_VALIDATION_SWABIA_COMPLETION.json`. Ce résultat n'est ni un test moteur automatisé, ni une certification historique exhaustive. Les contrôles statiques ci-dessous restent des résultats datés ; les limites historiques restent ouvertes. L'ancien addon industriel prussien est couvert séparément dans cette attestation, mais pas les micro-ajustements économiques ultérieurs ni `PRUSSIAN_BORDERS`. Les mentions de tests restant à faire plus bas décrivent l'état initial du présent rapport.

## Résultat cartographique appliqué

Six villes libres distinctes et une abbaye sont ajoutées. Le raccord autrichien concerne uniquement deux cellules de l’office de la Landvogtei, pas toute la Haute-Souabe.

| Territoire | TAG | Propriétaire précédent | Cellules transférées | Capitale / State Region |
|---|---|---|---:|---|
| Ville libre d’Augsbourg | SAC | BAV | 1 | STATE_BAVARIA |
| Ville libre de Kempten | SKI | SKE | 1 | STATE_BAVARIA |
| Reutlingen, noyau municipal et Wannweil | SRT | WUR | 3 | STATE_WURTTEMBERG |
| Biberach, noyau municipal | SBI | WUR | 1 | STATE_WURTTEMBERG |
| Memmingen, noyau municipal | SMM | WUR | 1 | STATE_WURTTEMBERG |
| Ravensbourg, noyau municipal | SRQ | BAD | 4 | STATE_BADEN |
| Weingarten, terres administrées par l’abbaye | SWG | WUR / BAD | 2 + 1 | STATE_WURTTEMBERG |
| Landvogtei autrichienne, raccord de l’office 9 | AUS | WUR | 2 | STATE_WURTTEMBERG |

Total : **16 cellules changent de propriétaire**. **13 nouveaux RGB**, `xEDB000`–`xEDB00C`, sont créés ; **21 cellules sont recolorées**, dont cinq raccords conservant leur propriétaire. Aucun ancien RGB n’est supprimé. Le registre passe de 485 à **498 RGB** ; l’étendue impériale reste exactement **62 580 cellules**.

La séparation Augsbourg / principauté épiscopale SAG ne modifie aucune des 47 cellules de SAG. Kempten est une exception précise, autorisée par le joueur : la cellule `[4324,928]` devient SKI ; SKE conserve les **seize autres cellules** de `xEDAD0D`, son gouvernement et ses **6 189 habitants**. Les validations antérieures ne permettent cette exception qu’à ce point, pour ce propriétaire et ce bénéficiaire.

Les deux cellules urbaines sont des **abstractions explicitement autorisées**, pas des limites municipales mesurées au pixel. Les noyaux supplémentaires sont des approximations géographiques conservatrices, non des restitutions cadastrales.

## Sources et souverainetés

Les sources conservées ont été réutilisées, sans nouvelle campagne mondiale :

- [Historischer Atlas von Baden-Württemberg, VI.13](https://www.leo-bw.de/media/kgl_atlas/current/delivered/bilder/HABW_06_13.jpg), Nüske / Kerkhoff, publication 1987, situation territoriale 1790. Les offices temporels nommés sont utilisés pour des noyaux compatibles avec 1776, **pas pour rétroprojeter toutes les frontières de 1790**. Le JPEG original est conservé dans SWABIA_FINISH/EVIDENCE.
- [Carte Homann conservée, catalogue e-rara](https://www.e-rara.ch/bes_1/content/titleinfo/29527171), vers 1693 : correspondance cartographique auxiliaire pour les villes, non preuve suffisante de toutes les souverainetés de 1776.
- [Augsbourg : territoire et administration](https://www.historisches-lexikon-bayerns.de/Lexikon/Augsburg,_Reichsstadt:_Territorium_und_Verwaltung) : ville libre distincte de l’évêché ; les propriétés privées ne deviennent pas un vaste territoire souverain municipal.
- [Kempten, ville impériale](https://www.historisches-lexikon-bayerns.de/Lexikon/Kempten,_Reichsstadt) : ville luthérienne politiquement distincte de la principauté abbatiale catholique. Aucun maire de 1785 n’est rétroprojeté en 1776.
- [Weingarten, notice institutionnelle LEO-BW](https://www.leo-bw.de/en-GB/detail-gis/-/Detail/details/DOKUMENT/labw_kloester/698/Benediktinerabtei%20Weingarten) : **Dominicus Schnizer, abbé de 1745 à 1784**, et non son successeur Anselm Rittler. Les droits de haute justice autrichiens et les terres administrées par l’abbaye se superposent historiquement. La représentation dans le jeu simplifie explicitement ces droits superposés ; elle ne supprime pas cette incertitude.

Le calage AN repose sur trois correspondances économiques/cartographiques Stuttgart–Ulm–Constance. Un ajustement exact sur ces trois points n’est **pas** une mesure indépendante de précision géographique. Le calage sud AT et le diagnostic Homann, dont le désaccord de Lindau, sont conservés. Aucun recalage d’Erfurt n’est relancé.

Les polygones sont enregistrés dans TRACING.json ; les intersections, les RGB et les cellules exactes figurent dans GEOMETRY.json et TERRITORIAL_CHANGES.csv. Esslingen n’est pas agrandie : son enveloppe conservatrice n’intersecte aucune cellule admissible.

## Données de départ et mécanismes

Population mondiale : **835 804 980 avant et après le découpage**. Cultures, religions explicites ou par défaut et attributs des populations sont conservés. Aucun nouvel habitant n’est créé.

Augsbourg reçoit 22 000 habitants déjà présents dans les profils bavarois : 12 000 du profil sud-germanique de religion par défaut et 10 000 protestants. Kempten reçoit 4 000 protestants du même État bavarois, **sans prélever les habitants de SKE ni les convertir**. Ces allocations urbaines sont des choix de représentation et de jouabilité, **pas un recensement historique de 1776**. Les autres transferts suivent les profils des subdivisions sources, sans affirmer leur exactitude confessionnelle ville par ville. URBAN_ALLOCATION_WEIGHTS.json et POPULATION_VALIDATION.csv rendent chaque opération traçable.

Pour le seul découpage souabe, niveaux mondiaux de bâtiments, méthodes de production, réserves, propriétaires économiques, unités, formations et recrutements sont conservés. Une industrie alimentaire bavaroise existante est transférée à SAC, et un des dix niveaux d’élevage du profil bavarois à SKI : aucun niveau n’est ajouté par ces transferts. Les détenteurs économiques existants sont maintenus.

Les six villes ont un conseil urbain et le statut de ville libre ; SWG a un gouvernement abbatial et aucun statut électoral. Les nouveaux pays ont des capitales possédées, des lois compatibles avec leurs technologies de départ, des couleurs, des drapeaux procéduraux et des descriptions françaises/anglaises. Les drapeaux ne sont pas présentés comme une certification héraldique. Les clés brutes précédemment corrigées pour Bade et Ulm restent corrigées.

Le registre, le bloc, les listes et interactions impériales, la carte du journal et le masque de la carte principale sont mis à jour. Aucun locator physique n’est déplacé ou réaffecté dans ce nouveau lot.

## Complément prussien expressément demandé

Cette addition est **séparée des invariants du découpage** : +3 niveaux d’usines d’armes en Brandebourg, soit 1 → 4 ; +10 niveaux de camps de bûcherons en Prusse, répartis en Brandebourg (+6, capacité régionale 6) et Poméranie (+4, capacité régionale 11). Aucun plafond forestier ni frontière n’est changé. Aucune population ou technologie n’est ajoutée.

La preuve différentielle indépendante se trouve dans PRUSSIAN_INDUSTRY_ADDON/VALIDATION.json et son PLAN.json. Les validations cumulatives du découpage sont exécutées **avant** cette augmentation volontaire de treize niveaux. Les suites anciennes qui exigent une conservation stricte des bâtiments ne doivent pas être présentées comme exécutées après l’addition ni voir leurs anciennes baselines réécrites pour la masquer.

## Validation et limites

### Fichiers et traçabilité

FINAL_RUNTIME_FILES.json donne le delta final des fichiers de jeu avec empreintes avant/après et distingue les nouveaux fichiers. PLAN.json détaille les historiques, États partagés, définitions des sept pays, lois, gouvernements, personnages, drapeaux, localisations et registre. IMPERIAL_FILES.json énumère les seize fichiers du système impérial recompilés. Les modifications prussiennes sont limitées au niveau d’armes dans `00_west_europe.txt` et au nouveau `99_1776_prussian_forestry_addon.txt`. Les bitmaps, terrains et textures cartographiques sont contrôlés séparément ; les rapports cumulatifs et outils de validation ne sont pas des données du moteur.

Le nouveau lot a passé **570/570 contrôles statiques** avant le complément industriel prussien. La carte principale a passé **16/16 contrôles hors jeu**, dont une compilation du seul helper HLSL ; ceci n’est pas une compilation du shader complet par Victoria 3 ni un test moteur.

Les **17 suites cumulatives** totalisent **14 633 contrôles réussis sur 14 643**. Les dix écarts restants concernent uniquement les anciennes baselines Git antérieures au commit autorisé `f34a6b8` ; **tous les contrôles de données passent**. Les résultats bruts, y compris leurs statuts FAIL Git historiques, restent dans les rapports concernés, NON_REGRESSION.json et CUMULATIVE_RUN.json.

Le complément prussien a ensuite passé **1 812/1 812 contrôles différentiels**, prouvant exactement les treize niveaux ajoutés et l’absence d’autre modification de données ou de fichiers de jeu depuis sa baseline. Les **23 tests unitaires** passent également. Les **44 doublons RGB et 12 références invalides hérités** ne sont pas réparés ni masqués. Les conseils urbains doivent encore être inspectés en jeu pour leur économie effective, leurs ressources et leurs infrastructures.

Le contrôle Git des espaces signale encore quatorze lignes vides indentées dans les historiques, dont des lignes préexistantes et des fragments introduits par les transferts. Ce sont des avertissements de présentation, pas des échecs de parsing ni de conservation ; aucune correction générale des fichiers du collaborateur n’a été faite.

SWABIA_FINISH reçoit **PASS_RUNTIME_USER_VALIDATED**, seulement pour les sept vérifications et le mois de simulation rapportés par le joueur. SWABIA_COMPLETION et le complément prussien restent **NOT_YET_TESTED**. Aucune certification historique de toutes les frontières, ni validation automatique du moteur, n’est donnée.

Les grandes passes souabes sont désormais appliquées à l’échelle du jeu, avec une liste fermée de résidus dans UNRESOLVED.csv : Montbéliard reste un cas important distinct ; Esslingen et quelques villes minuscules, possessions dispersées et droits superposés ne sont pas inventés. Cela ne signifie pas que toutes les cellules conservant BAD/WUR/BAV ont été historiquement certifiées.

Le checkpoint `cadb544c7de706707532e26bdf19998cf7601cec` est toujours présent sur `backup/1776-checkpoints` (lecture distante du 14 octobre 2026). Les attestations antérieures de restauration complète et incrémentale ont été relues ; aucun nouveau test complet de restauration n’a été refait, ni nouvelle archive ou publication créée. Les nouveaux lots ne sont **pas** inclus dans ce checkpoint. HEAD et l’index principal restent ceux de la baseline autorisée.

## ColGrep

Deux tentatives `colgrep --agent` : une échoue avant démarrage en accès restreint ; une exécution avec le chemin absolu termine avec code 0 en **218,66 secondes**, utilisant la configuration locale 2B existante. Elle renvoie surtout Luxembourg/Liège et des outils déjà connus, et n’apporte pas de source souabe exploitable. Ces résultats sont vérifiés et rejetés comme preuves historiques. Aucun changement de modèle, d’intégration ou reconstruction d’index.

Le compteur de tokens Codex par cette tâche n’est pas disponible. Les sorties non interactives ne permettent pas de certifier indépendamment l’utilisation du GPU ni les tokens internes du 2B. Aucune économie exacte de quota n’est revendiquée ; pour cette recherche, le gain pratique a été faible et aucun document utile n’a été évité grâce aux résultats du 2B.

## Nouveau contrôle en jeu

1. Nouvelle partie : SAC et SAG distincts, SKI et SKE distincts ; capitales et gouvernements cohérents.
2. Conseils, descriptions et drapeaux des six villes ; abbatiale SWG et Dominicus Schnizer.
3. Statut de ville libre et bloc pour les six villes, pas de voix électorale ni statut municipal pour SWG.
4. Populations, économies et infrastructures : surtout viabilité des villes de Biberach/Memmingen et fonctionnement des deux subdivisions de Kempten.
5. Registre, restitution ciblée et cartes impériales ; aucune disparition des lots précédents.
6. Prusse : quatre niveaux d’armes en Brandebourg, six camps de bûcherons en Brandebourg et quatre en Poméranie ; recrutement des salariés et approvisionnement.
7. Laisser passer un mois, conserver les erreurs héritées séparément des éventuelles nouvelles erreurs.

Aucun commit, merge, reset, push ou nouvelle région géographique.
