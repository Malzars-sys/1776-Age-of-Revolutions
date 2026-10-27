# Feuille de route canonique — clôture territoriale du SERG

**SERG TERRITORIAL 1.0 — PROGRESSION : 35,32 %**

Périmètre `1.0.0` — référence historique : 1er janvier 1776. Indicateur de jalons acceptés, pas pourcentage de frontières exactes.

## Résolution actuelle — Luxembourg administratif

Un niveau ordinaire BEO/Wallonie installé, trois niveaux flamands conservés ; contrat BUILD réconcilié. Rapport : [REPORT.md](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_CLOSURE/SC2-LUXEMBOURG-VALIDATION/ADMIN_R1_2026_10_26/REPORT.md>). Statut : `PASS_RUNTIME_USER_VALIDATED`. Reçu humain limité à cette tâche : [RUNTIME_USER_ATTESTATION_2026_10_26.json](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_CLOSURE/SC2-LUXEMBOURG-VALIDATION/RUNTIME_USER_ATTESTATION_2026_10_26.json>).

Prochaine action limitée aux validations groupées : [PLAYER_TEST_PROTOCOL_GROUPED.md](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_CLOSURE/SC2-LUXEMBOURG-VALIDATION/ACCEPTANCE_2026_10_26/PLAYER_TEST_PROTOCOL_GROUPED.md>). La matrice antérieure reste une archive ; aucun nouveau territoire autorisé.

## Priorité actuelle — campagne de levée des blocages

Création systématique de nouveaux territoires suspendue selon [USER_MISSION.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_CLOSURE/CLOSURE_CAMPAIGN_2026_10_26/USER_MISSION.txt>). Auditer et clore les installations existantes avant toute nouvelle expansion. Aucun changement du périmètre, des 81 tâches ou des 235 points.

Audit des huit installations : [INSTALLED_VALIDATIONS.md](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_CLOSURE/CLOSURE_CAMPAIGN_2026_10_26/INSTALLED_VALIDATIONS.md>). Matrice des blocages : [BLOCKED_MATRIX.md](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_CLOSURE/CLOSURE_CAMPAIGN_2026_10_26/BLOCKED_MATRIX.md>). Tâche de clôture traitée : `SC2-TESCHEN` ; décision proposée, aucune approbation présumée.

## Protocole obligatoire de chaque passe SERG

1. Lire ce fichier, puis [ROADMAP_STATE.json](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_CLOSURE/ROADMAP_STATE.json>), [NEXT_ACTION.md](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_CLOSURE/NEXT_ACTION.md>) et [BLOCKERS.md](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_CLOSURE/BLOCKERS.md>), puis les seuls rapports du sous-lot choisi.
2. Vérifier branche/HEAD/index en lecture, état réel des fichiers, dernier sous-lot installé, reçu utilisateur et travaux concurrents. Si le suivi contredit le mod, documenter l’écart avant de corriger. Aucune restauration depuis une ancienne baseline.
3. Choisir selon priorité P0/P1, dépendances, cohérence géographique, contrôle indépendant et risque de conflit. Ne pas refaire un noyau accepté hors régression démontrée; un blocage local ne gèle pas les autres régions.
4. Dans une mission territoriale autorisée : réutiliser les sources, vérifier les attributions, installer seulement les corrections défendables, puis contrôles cumulatifs et protocole manuel borné. Pas de rapport de préparation indéfiniment répété.
5. Mettre à jour l’état et les preuves, ajouter un événement à l’historique sans effacer les précédents, recalculer le pourcentage et régénérer les vues. Un test statique ne vaut jamais reçu humain.
6. Le rapport final commence par la ligne de progression ci-dessus; préciser phase/sous-lot/statut, installé/validé, blocages, avant/après, prochaine action et test attendu. `READY_FOR_SCOPED_RUNTIME_VALIDATION` est le libellé de livraison; le statut structuré correspondant reste `IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION`.

La mission d’initialisation (`SERG_CLOSURE_ROADMAP_INITIALIZED`) n’a installé aucun territoire. Lecture et génération ne lancent aucun chantier géographique. État courant de Salzbourg : `PASS_RUNTIME_USER_VALIDATED`.

## Socle initial et calcul courant

État courant : 25 jalons justifiés; **83 / 235 points**, 81 tâches définies dans une liste finie. 7 tâches installées attendent un reçu spécifique.

À l’initialisation : 19 noyaux/jalons antérieurs acceptés, 60/235 points = 25,53 %. Indicateur auparavant absent; aucune nouvelle correction ni validation humaine pendant cette seule mission. L’historique conserve ensuite les évolutions.

`progression = 100 × Σ poids des tâches terminales justifiées / Σ poids de toutes les tâches du périmètre`

Les statuts de recherche, blocage ou installation non testée apportent **zéro** point. Pondération fixe : 1 = contrôle borné/petite juridiction; 2 = correction locale ou arbitrage; 3 = principauté/ensemble local significatif; 4 = groupe de juridictions ou cohérence institutionnelle; 5 = grand ensemble régional; 6 = grand déficit de couverture ou approbation finale. Le champ `weight_basis` précise les socles consolidés. C’est un barème de gestion explicite, non une mesure du travail scientifique ou des habitants.

Les 19 socles sont crédités uniquement pour les noyaux installés et inspectés, avec rapprochement des rapports, reçus et contrôles de l’audit. Peene, Eutin et Poel ne sont pas crédités une fois par passe incrémentale; RBI et RCI constituent un seul socle Ratisbonne. Les franges et les corrections ultérieures restent des tâches distinctes. Le nombre de RGB du registre ne constitue pas le dénominateur.

Arrondi à deux décimales, demi vers le haut; un arrondi numérique ne peut afficher 100 avant les critères finaux. Le jalon final de six points est inaccessible sans reçu final, toutes les dépendances acceptées et approbation explicite de l’utilisateur sur ce périmètre. `SERG_TERRITORIAL_1_0_COMPLETE` est interdit avant cet accord.

## Sept phases et rapprochement de l’ancien plan

| Phase | Tâches | Points acceptés / total | Origine audit |
| --- | ---: | ---: | --- |
| 1 — Salzbourg et principautés ecclésiastiques alpines | 12 | 14 / 32 | CL1 : juridictions alpines et périphéries R4 |
| 2 — Possessions impériales des Habsbourg | 11 | 22 / 37 | CL1 : territoires habsbourgeois et Teschen |
| 3 — Allemagne septentrionale et juridictions manquantes | 14 | 18 / 44 | CL3; socles MAP2N/Q/R/T/U |
| 4 — Italie impériale | 8 | 0 / 23 | CL2; le rang change, pas le contenu historique |
| 5 — Corrections occidentales et centrales restantes | 18 | 14 / 45 | CL4 + CL5; Montbéliard/Oettingen de CL6 |
| 6 — Petites juridictions significatives et arbitrages | 10 | 15 / 29 | CL6 hors Montbéliard/Oettingen; Goslar de CL3 |
| 7 — Cohérence impériale et validation finale | 8 | 0 / 25 | CL7; pas développement obligatoire de mécaniques futures |

L’ordre demandé prévaut : l’ancien CL1 est scindé entre phases 1 et 2; CL2 devient phase 4; CL3 devient phase 3 (Goslar en 6); CL4/CL5 deviennent phase 5; Montbéliard/Oettingen de CL6 passent en 5, le reste en 6; CL7 devient 7. Le contenu de couverture n’est pas supprimé par ce réordonnancement.

## Tâches et critères vérifiables

Chaque fiche complète est conservée dans [ROADMAP_STATE.json](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_CLOSURE/ROADMAP_STATE.json>) : ID stable, région/secteurs historiques, juridiction, problème, priorité, sources avec lignes vérifiables, avant/résultat attendu, dépendances, profil et critères d’acceptation, rapports, contrôles, reçu et incertitudes. Les profils communs ci-dessous s’ajoutent au critère propre à chaque fiche.

**legacy_core** : Correction présente vérifiée par audit actuel; Reçu humain déjà existant, limité aux noyaux inspectés; Aucune frontière périphérique ou durée de simulation ajoutée au reçu.

**territorial** : Souveraineté datée et correspondance politique défendable; Avant/après RGB, propriétaires, capitales et références documentés; Populations historiques au périmètre comparable; économie, propriété et unités cohérentes; Corrections justifiées installées, tests statiques et non-régression; sinon décision explicite sans changement; Nouvelle partie et mois pour tout nouveau correctif; validation indépendante.

**runtime_only** : Ne pas refaire l’installation; Contrôle statique de conservation au moment du test; Reçu humain spécifique au sous-lot réellement inspecté.

**no_functional_change** : Vérification documentaire/technique bornée, preuve explicite; Aucune correction nécessaire démontrée, ou changements suivis dans tâche territoriale distincte; NA ne signifie pas étape ignorée; validation technique adaptée, pas moteur inventé.

**final_closure** : Toutes les autres tâches obligatoires dans état terminal justifié; Aucun P0/P1 bloquant ni grand secteur non audité; Protocole final réel nouvelle partie 1776 et simulation, selon périmètre; Approbation explicite du responsable de projet, liée au test final et à cette version de périmètre.

### Phase 1 — Salzbourg et principautés ecclésiastiques alpines

#### BASE-PASSAU — Passau : noyau PAS inspecté

P1 · poids 3 · `PASS_RUNTIME_USER_VALIDATED` · profil `legacy_core`.

Région/périmètre : Passau : noyau politique. Dépendances : aucune.

Acceptation : Conserver les seuls noyaux antérieurement inspectés, sans réouverture hors régression prouvée

Source de départ : [docs/reports/map/MAP2W/R4/POLITICAL_REPRESENTATION/PASSAU/REPORT.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/MAP2W/R4/POLITICAL_REPRESENTATION/PASSAU/REPORT.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### BASE-FREISING — Freising : noyau FSI inspecté

P1 · poids 2 · `PASS_RUNTIME_USER_VALIDATED` · profil `legacy_core`.

Région/périmètre : Freising : noyau politique. Dépendances : aucune.

Acceptation : Conserver les seuls noyaux antérieurement inspectés, sans réouverture hors régression prouvée

Source de départ : [docs/reports/map/MAP2W/R4/POLITICAL_REPRESENTATION/FREISING_REGENSBURG/REPORT.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/MAP2W/R4/POLITICAL_REPRESENTATION/FREISING_REGENSBURG/REPORT.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### BASE-REGENSBURG — Ratisbonne : ville RCI et noyaux RBI inspectés

P1 · poids 3 · `PASS_RUNTIME_USER_VALIDATED` · profil `legacy_core`.

Région/périmètre : Ratisbonne : ville et évêché. Dépendances : aucune.

Acceptation : Conserver les seuls noyaux antérieurement inspectés, sans réouverture hors régression prouvée

Source de départ : [docs/reports/map/MAP2W/R4/POLITICAL_REPRESENTATION/FREISING_REGENSBURG/REPORT.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/MAP2W/R4/POLITICAL_REPRESENTATION/FREISING_REGENSBURG/REPORT.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC1-SALZBURG — Noyau fonctionnel du prince-archevêché de Salzbourg

P0 · poids 6 · `PASS_RUNTIME_USER_VALIDATED` · profil `territorial`.

Région/périmètre : Salzbourg. Dépendances : aucune.

Acceptation : Noyau B défendable, pays/capitale/gouvernement/titulaire/démographie cohérents; aucune annexion de toute Autriche ou Bavière; test indépendant.

Source de départ : [docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC1-TRENTO — Principauté épiscopale de Trente

P1 · poids 3 · `BLOCKED` · profil `territorial`.

Région/périmètre : Tyrol et principautés de Trente/Brixen. Dépendances : SC1-SALZBURG.

Acceptation : Distinguer droits tyroliens et domaine épiscopal au 1 janvier; ne pas anticiper le changement de titulaire en cours de 1776.

Source de départ : [docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC1-BRIXEN — Principauté épiscopale de Brixen

P1 · poids 3 · `BLOCKED` · profil `territorial`.

Région/périmètre : Tyrol et principautés de Trente/Brixen. Dépendances : SC1-SALZBURG.

Acceptation : Établir juridiction temporelle et dépendances, pas le diocèse ni tout SOUTH_TYROL.

Source de départ : [docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC1-BERCHTESGADEN — Prévôté princière de Berchtesgaden

P1 · poids 2 · `BLOCKED` · profil `territorial`.

Région/périmètre : Bavière et enclaves restantes. Dépendances : SC1-SALZBURG.

Acceptation : Noyau temporel et population comparables; pas tout un RGB alpin attribué depuis une ville.

Source de départ : [docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC1-FREISING-OUTLIERS — Werdenfels, Burgrain et Ismaning hors noyau FSI

P1 · poids 3 · `BLOCKED` · profil `territorial`.

Région/périmètre : Freising : noyau politique. Dépendances : aucune.

Acceptation : Nouvelles preuves permettant une approximation politique sans corridor traversant Munich; FSI 14 cellules protégé.

Source de départ : [docs/reports/map/MAP2W/R4/POLITICAL_REPRESENTATION/FREISING_REGENSBURG/UNRESOLVED.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/MAP2W/R4/POLITICAL_REPRESENTATION/FREISING_REGENSBURG/UNRESOLVED.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC1-REGENSBURG-OUTLIERS — Hohenburg et périphéries épiscopales de Ratisbonne

P1 · poids 2 · `BLOCKED` · profil `territorial`.

Région/périmètre : Ratisbonne : ville et évêché. Dépendances : aucune.

Acceptation : Distinguer domaines médiats homonymes, protéger RBI/RCI; immunités intra-urbaines P2 séparées.

Source de départ : [docs/reports/map/MAP2W/R4/POLITICAL_REPRESENTATION/FREISING_REGENSBURG/UNRESOLVED.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/MAP2W/R4/POLITICAL_REPRESENTATION/FREISING_REGENSBURG/UNRESOLVED.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC1-PASSAU-OUTLIERS — Possessions périphériques de Passau

P1 · poids 2 · `BLOCKED` · profil `territorial`.

Région/périmètre : Passau : noyau politique. Dépendances : aucune.

Acceptation : Préserver PAS 40 cellules; établir limites de 1765 et possessions non cédées avant 1782, sans copier 1791.

Source de départ : [docs/reports/map/MAP2W/R4/POLITICAL_REPRESENTATION/FREISING_REGENSBURG/UNRESOLVED.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/MAP2W/R4/POLITICAL_REPRESENTATION/FREISING_REGENSBURG/UNRESOLVED.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC1-REGENSBURG-DEMOGRAPHY — Population historique de la représentation de Ratisbonne

P1 · poids 2 · `BLOCKED` · profil `territorial`.

Région/périmètre : Ratisbonne : ville et évêché. Dépendances : aucune.

Acceptation : RCI 713 est technique; estimation au périmètre comparable, religion étayée; pas compensation mondiale ni population de convenance.

Source de départ : [docs/reports/map/MAP2W/R4/POLITICAL_REPRESENTATION/FREISING_REGENSBURG/UNRESOLVED.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/MAP2W/R4/POLITICAL_REPRESENTATION/FREISING_REGENSBURG/UNRESOLVED.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC1-ORTENBURG — Arbitrage d’Ortenbourg

P1 · poids 1 · `BLOCKED` · profil `territorial`.

Région/périmètre : Bavière et enclaves restantes. Dépendances : aucune.

Acceptation : Confirmer souveraineté, noyau représentable et distinction des possessions médiates avant toute création.

Source de départ : [docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.


### Phase 2 — Possessions impériales des Habsbourg

#### BASE-BELGIUM — Belgique, Liège et Stavelot : noyaux inspectés

P1 · poids 5 · `PASS_RUNTIME_USER_VALIDATED` · profil `legacy_core`.

Région/périmètre : Liège, Stavelot et Pays-Bas autrichiens : noyaux. Dépendances : aucune.

Acceptation : Conserver les seuls noyaux antérieurement inspectés, sans réouverture hors régression prouvée

Source de départ : [docs/reports/map/MAP2L/BELGIUM/IMPLEMENTATION.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/MAP2L/BELGIUM/IMPLEMENTATION.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC2-BOHEMIA — Audit territorial de la Bohême

P0 · poids 6 · `PASS_RUNTIME_USER_VALIDATED` · profil `territorial`.

Région/périmètre : Bohême. Dépendances : aucune.

Acceptation : Audit daté suffisant des grands contours et juridictions; le TAG AUS et la bibliographie macro ne suffisent pas.

Source de départ : [docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/REGIONAL_COVERAGE.csv:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/REGIONAL_COVERAGE.csv>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC2-MORAVIA — Moravie hors réparations MAP2A

P0 · poids 3 · `PASS_RUNTIME_USER_VALIDATED` · profil `territorial`.

Région/périmètre : Moravie et Silésie autrichienne. Dépendances : aucune.

Acceptation : Conserver x71E080/xF0E080; contrôler les autres contours, pas refonte des réparations acquises.

Source de départ : [docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/REGIONAL_COVERAGE.csv:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/REGIONAL_COVERAGE.csv>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC2-AUSTRIAN-SILESIA — Silésie autrichienne et frontière impériale

P0 · poids 3 · `NOT_APPLICABLE_VERIFIED` · profil `territorial`.

Région/périmètre : Moravie et Silésie autrichienne. Dépendances : aucune.

Acceptation : Partition avant 1776; ne pas assimiler région économique à souveraineté; scopes MAP2A protégés.

Source de départ : [docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/REGIONAL_COVERAGE.csv:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/REGIONAL_COVERAGE.csv>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC2-AUSTRIA — Haute et Basse Autriche

P0 · poids 5 · `BLOCKED` · profil `territorial`.

Région/périmètre : Autriche, Styrie, Carinthie et Carniole. Dépendances : aucune.

Acceptation : Examen territorial indépendant des possessions intercalées et des limites extérieures à l’Empire.

Source de départ : [docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/REGIONAL_COVERAGE.csv:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/REGIONAL_COVERAGE.csv>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC2-INNER-AUSTRIA — Styrie, Carinthie et Carniole

P0 · poids 4 · `PASS_RUNTIME_USER_VALIDATED` · profil `territorial`.

Région/périmètre : Autriche, Styrie, Carinthie et Carniole. Dépendances : aucune.

Acceptation : Trois pays historiques distingués, interface Hongrie/Croatie documentée; pas Slovénie moderne rétroprojetée.

Source de départ : [docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/REGIONAL_COVERAGE.csv:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/REGIONAL_COVERAGE.csv>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC2-TYROL — Comté du Tyrol, hors nouvelles principautés de phase 1

P0 · poids 3 · `NOT_STARTED` · profil `territorial`.

Région/périmètre : Tyrol et principautés de Trente/Brixen. Dépendances : SC1-TRENTO, SC1-BRIXEN.

Acceptation : Réconcilier domaines habsbourgeois/épiscopaux; ne pas refaire les noyaux validés.

Source de départ : [docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/REGIONAL_COVERAGE.csv:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/REGIONAL_COVERAGE.csv>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC2-ANTERIOR-AUSTRIA — Autriche antérieure et interface adriatique

P0 · poids 3 · `BLOCKED` · profil `territorial`.

Région/périmètre : Autriche antérieure et frontière adriatique. Dépendances : aucune.

Acceptation : Fribourg/Nellenburg/Landvogtei conservés; autres possessions impériales distinguées des territoires cédés et vénitiens.

Source de départ : [docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/REGIONAL_COVERAGE.csv:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/REGIONAL_COVERAGE.csv>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC2-TESCHEN — Teschen et registre x9061E0

P1 · poids 2 · `BLOCKED` · profil `territorial`.

Région/périmètre : Moravie et Silésie autrichienne. Dépendances : aucune.

Acceptation : 179 cellules AUS en WEST_GALICIA hors registre; établir la portion impériale sans intégrer toute la Galicie.

Source de départ : [docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/SUPPLEMENTAL_CHECKS.json:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/SUPPLEMENTAL_CHECKS.json>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC2-MAP2A-VALIDATION — Portée manuelle des corrections MAP2A

P1 · poids 2 · `IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION` · profil `runtime_only`.

Région/périmètre : Moravie et Silésie autrichienne; Milanais–Crémonais et Trois Ligues. Dépendances : aucune.

Acceptation : Quatre RGB existants et dépendances inchangées; test scoped absent de l’audit; aucune nouvelle correction.

Source de départ : [docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/COMPLETED_LOTS.csv:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/COMPLETED_LOTS.csv>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC2-LUXEMBOURG-VALIDATION — Portée manuelle Luxembourg sous BEO

P1 · poids 1 · `PASS_RUNTIME_USER_VALIDATED` · profil `runtime_only`.

Région/périmètre : Luxembourg : intégration à BEO. Dépendances : aucune.

Acceptation : Transfert xD001A0 BEO, quatre groupes et 137881 habitants historiques de transfert, formation/général conservés ; une administration BEO/Wallonie unique dans le contrat BUILD réconcilié, trois niveaux flamands conservés, aucun nouveau tracé.

Source de départ : [docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/COMPLETED_LOTS.csv:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/COMPLETED_LOTS.csv>). Rapports, autres sources et incertitudes : fiche JSON du même ID.


### Phase 3 — Allemagne septentrionale et juridictions manquantes

#### BASE-EUTIN — Eutin–Schwartau : HLB et union OLD–HLB inspectés

P1 · poids 3 · `PASS_RUNTIME_USER_VALIDATED` · profil `legacy_core`.

Région/périmètre : Eutin et Schwartau, noyaux HLB. Dépendances : aucune.

Acceptation : Conserver les seuls noyaux antérieurement inspectés, sans réouverture hors régression prouvée

Source de départ : [docs/reports/map/MAP2Q/R3/REPORT.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/MAP2Q/R3/REPORT.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### BASE-SWEDISH-MECKLENBURG — Wismar–Poel–Neukloster inspectés

P1 · poids 3 · `PASS_RUNTIME_USER_VALIDATED` · profil `legacy_core`.

Région/périmètre : Wismar–Poel–Neukloster. Dépendances : aucune.

Acceptation : Conserver les seuls noyaux antérieurement inspectés, sans réouverture hors régression prouvée

Source de départ : [docs/reports/map/MAP2N/REPORT.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/MAP2N/REPORT.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### BASE-PEENE — Poméranie suédoise, Peene et Wolgast inspectés

P1 · poids 3 · `PASS_RUNTIME_USER_VALIDATED` · profil `legacy_core`.

Région/périmètre : Poméranie impériale, Peene et Wolgast. Dépendances : aucune.

Acceptation : Conserver les seuls noyaux antérieurement inspectés, sans réouverture hors régression prouvée

Source de départ : [docs/reports/map/MAP2M/R9/REPORT.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/MAP2M/R9/REPORT.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### BASE-ANHALT — Quatre noyaux d’Anhalt inspectés

P1 · poids 3 · `PASS_RUNTIME_USER_VALIDATED` · profil `legacy_core`.

Région/périmètre : Anhalt : quatre principautés. Dépendances : aucune.

Acceptation : Conserver les seuls noyaux antérieurement inspectés, sans réouverture hors régression prouvée

Source de départ : [docs/reports/map/MAP2R/REPORT.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/MAP2R/REPORT.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### BASE-SAXONY — Saxe et duchés thuringiens MAP2T inspectés

P1 · poids 4 · `PASS_RUNTIME_USER_VALIDATED` · profil `legacy_core`.

Région/périmètre : Saxe et duchés ernestins. Dépendances : aucune.

Acceptation : Conserver les seuls noyaux antérieurement inspectés, sans réouverture hors régression prouvée

Source de départ : [docs/reports/map/MAP2T/REPORT.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/MAP2T/REPORT.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### BASE-REUSS — Compléments Reuss et Sondershausen MAP2U inspectés

P1 · poids 2 · `PASS_RUNTIME_USER_VALIDATED` · profil `legacy_core`.

Région/périmètre : Reuss et Schwarzbourg-Sondershausen. Dépendances : aucune.

Acceptation : Conserver les seuls noyaux antérieurement inspectés, sans réouverture hors régression prouvée

Source de départ : [docs/reports/map/MAP2U/REPORT.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/MAP2U/REPORT.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC3-HOLSTEIN — Holstein royal, Schleswig et liens danois

P1 · poids 4 · `NOT_STARTED` · profil `territorial`.

Région/périmètre : Holstein royal et exclusion du Schleswig. Dépendances : aucune.

Acceptation : Règlement de 1773, Eutin distinct, Holstein impérial/Schleswig extérieur; aucun regroupement automatique.

Source de départ : [docs/reports/map/MAP1/inputs/regional_originals/R2_NORTHERN_CENTRAL_EASTERN_EUROPE_RECOMMENDATIONS.csv:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/MAP1/inputs/regional_originals/R2_NORTHERN_CENTRAL_EASTERN_EUROPE_RECOMMENDATIONS.csv>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC3-MECKLENBURG — Mecklembourg hors possessions suédoises

P1 · poids 3 · `NOT_STARTED` · profil `territorial`.

Région/périmètre : Mecklembourg hors possessions suédoises. Dépendances : aucune.

Acceptation : Contrôler Schwerin/Strelitz et limites; protéger Wismar/Poel/Neukloster.

Source de départ : [docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC3-BRUNSWICK-HARZ — Hanovre, Brunswick et Harz

P1 · poids 5 · `NOT_STARTED` · profil `territorial`.

Région/périmètre : Hanovre, Brunswick et principautés du Harz. Dépendances : aucune.

Acceptation : Branches et juridictions indépendantes dont Quedlinburg à qualifier; préparer Goslar sans doubler la correction SC6-GOSLAR.

Source de départ : [docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC3-HILDESHEIM — Hochstift Hildesheim

P1 · poids 3 · `NOT_STARTED` · profil `territorial`.

Région/périmètre : Hanovre, Brunswick et principautés du Harz. Dépendances : aucune.

Acceptation : Institution distincte avant 1802/1803, pas absorption HAN/BRA/PRU par défaut; noyau et administration cohérents.

Source de départ : [docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC3-BRANDENBURG — Brandebourg, Magdebourg et Halberstadt

P1 · poids 4 · `NOT_STARTED` · profil `territorial`.

Région/périmètre : Brandebourg, Neumark, Magdebourg–Halberstadt. Dépendances : aucune.

Acceptation : Possessions impériales de PRU seulement; conserver Anhalt/T/U et économie existante.

Source de départ : [docs/reports/map/MAP2M/R9/PRUSSIAN_HRE_BORDERS_AUDIT.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/MAP2M/R9/PRUSSIAN_HRE_BORDERS_AUDIT.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC3-SILESIA-LUSATIA — Silésie prussienne, Glatz et Lusaces

P1 · poids 3 · `NOT_STARTED` · profil `territorial`.

Région/périmètre : Silésie prussienne, Glatz et Lusaces. Dépendances : aucune.

Acceptation : Partition 1742/1763, pas acquisitions 1815; diagnostics MAP1B ne sont pas limites certifiées.

Source de départ : [docs/reports/map/MAP2M/R9/PRUSSIAN_HRE_BORDERS_AUDIT.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/MAP2M/R9/PRUSSIAN_HRE_BORDERS_AUDIT.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC3-SWEDISH-DEPENDENCIES — Arbitrage des dépendances LUB/MEC/MST

P1 · poids 2 · `NOT_STARTED` · profil `territorial`.

Région/périmètre : Villes de Lübeck, Hambourg et Brême. Dépendances : aucune.

Acceptation : Choix de gameplay hérité distingué du droit historique; aucune suppression automatique des liens sans décision.

Source de départ : [docs/reports/map/MAP2K/MAP2K_EXECUTIVE_SUMMARY.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/MAP2K/MAP2K_EXECUTIVE_SUMMARY.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC3-NORTHERN-JURISDICTIONS — Villes hanséatiques et juridictions septentrionales restantes

P1 · poids 2 · `NOT_STARTED` · profil `territorial`.

Région/périmètre : Villes de Lübeck, Hambourg et Brême; Hanovre, Brunswick et principautés du Harz. Dépendances : aucune.

Acceptation : Pays présents conservés, frontières et petites temporalités examinées; Goslar et Hildesheim réservés à leurs tâches.

Source de départ : [docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.


### Phase 4 — Italie impériale

#### SC4-EXISTING-ITALIAN-STATES — Statut impérial de MOD/PAR/TUS/LUC

P0 · poids 6 · `BLOCKED` · profil `territorial`.

Région/périmètre : Modène, Parme et Toscane. Dépendances : aucune.

Acceptation : Ces TAG existent; audit juridique et territorial réel, exclusions pontificales; aucune création depuis un inventaire incomplet.

Source de départ : [docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC4-SAVOY-NICE — Savoie et Nice

P0 · poids 3 · `BLOCKED` · profil `territorial`.

Région/périmètre : Savoie, Nice et fiefs ligures. Dépendances : aucune.

Acceptation : Droits et frontières de 1776 établis; pas île de Sardaigne impériale par simple appartenance SAR au bloc.

Source de départ : [docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC4-LIGURIAN-FIEFS — Gênes et fiefs ligures

P0 · poids 3 · `BLOCKED` · profil `territorial`.

Région/périmètre : Savoie, Nice et fiefs ligures. Dépendances : aucune.

Acceptation : GEN actif; statuts propres des fiefs et enclaves, pas impérialité automatique de toute la république.

Source de départ : [docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC4-PIOMBINO — Principauté de Piombino et île d’Elbe partagée

P0 · poids 3 · `BLOCKED` · profil `territorial`.

Région/périmètre : Modène, Parme et Toscane. Dépendances : aucune.

Acceptation : Réutiliser R1-0023; distinguer Portoferraio, Porto Longone et juridictions princières.

Source de départ : [docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC4-MASSA-CARRARA — Massa-Carrare

P0 · poids 3 · `BLOCKED` · profil `territorial`.

Région/périmètre : Modène, Parme et Toscane. Dépendances : aucune.

Acceptation : Réutiliser R1-0024/0025; arbitrer mariage dynastique vs institutions territoriales, sans fusion automatique MOD.

Source de départ : [docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC4-MILAN-OUTLIERS — Possessions habsbourgeoises italiennes hors liaison acquise

P1 · poids 2 · `NOT_STARTED` · profil `territorial`.

Région/périmètre : Milanais–Crémonais et Trois Ligues. Dépendances : aucune.

Acceptation : Conserver Crémonais 64 cellules et Trois Ligues SWI; contrôler autres limites datées, pas recul du correctif.

Source de départ : [docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC4-MILAN-VALIDATION — Portée manuelle Milanais–Crémonais

P1 · poids 2 · `IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION` · profil `runtime_only`.

Région/périmètre : Milanais–Crémonais et Trois Ligues. Dépendances : aucune.

Acceptation : Liaison AUS installée; pas reçu spécifique suffisant retrouvé; test indépendant.

Source de départ : [docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/COMPLETED_LOTS.csv:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/COMPLETED_LOTS.csv>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC4-PIEDMONT-VALIDATION — Portée manuelle de l’inclusion piémontaise

P1 · poids 1 · `IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION` · profil `runtime_only`.

Région/périmètre : Piémont : inclusion impériale limitée. Dépendances : aucune.

Acceptation : Neuf RGB SAR inscrits, pas Sardaigne; ne pas rejouer le découpage pour obtenir un reçu.

Source de départ : [docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/COMPLETED_LOTS.csv:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/COMPLETED_LOTS.csv>). Rapports, autres sources et incertitudes : fiche JSON du même ID.


### Phase 5 — Corrections occidentales et centrales restantes

#### BASE-RHINE-WESTPHALIA — Münster/Paderborn/Juliers–Berg : noyaux inspectés

P1 · poids 3 · `PASS_RUNTIME_USER_VALIDATED` · profil `legacy_core`.

Région/périmètre : Münster, Paderborn, Juliers–Berg : premiers noyaux. Dépendances : aucune.

Acceptation : Conserver les seuls noyaux antérieurement inspectés, sans réouverture hors régression prouvée

Source de départ : [docs/reports/map/MAP2L/RHINE_WESTPHALIA/REPORT.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/MAP2L/RHINE_WESTPHALIA/REPORT.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### BASE-OSNABRUCK — Osnabrück/Niederstift/Lingen–Tecklenburg inspectés

P1 · poids 3 · `PASS_RUNTIME_USER_VALIDATED` · profil `legacy_core`.

Région/périmètre : Osnabrück, Niederstift, Lingen–Tecklenburg. Dépendances : aucune.

Acceptation : Conserver les seuls noyaux antérieurement inspectés, sans réouverture hors régression prouvée

Source de départ : [docs/reports/map/MAP2L/RHINE_WESTPHALIA_COMPLETION/REPORT.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/MAP2L/RHINE_WESTPHALIA_COMPLETION/REPORT.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### BASE-EMDEN — Emden : approximation côtière PRU inspectée

P1 · poids 2 · `PASS_RUNTIME_USER_VALIDATED` · profil `legacy_core`.

Région/périmètre : Emden et noyau côtier de Frise orientale. Dépendances : aucune.

Acceptation : Conserver les seuls noyaux antérieurement inspectés, sans réouverture hors régression prouvée

Source de départ : [docs/reports/map/MAP2O/REPORT.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/MAP2O/REPORT.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### BASE-RHINE-CENTRAL — Neckar et noyaux du Rhin central inspectés

P1 · poids 2 · `PASS_RUNTIME_USER_VALIDATED` · profil `legacy_core`.

Région/périmètre : Rhin central, noyaux palatins et électoraux. Dépendances : aucune.

Acceptation : Conserver les seuls noyaux antérieurement inspectés, sans réouverture hors régression prouvée

Source de départ : [docs/reports/map/MAP2L/RHINE_CENTRAL/REPORT.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/MAP2L/RHINE_CENTRAL/REPORT.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### BASE-NASSAU-FULDA — Noyaux R2-B Hesse–Nassau–Fulda explicitement inspectés

P1 · poids 4 · `PASS_RUNTIME_USER_VALIDATED` · profil `legacy_core`.

Région/périmètre : Fulda et branches de Nassau installées. Dépendances : aucune.

Acceptation : Conserver les seuls noyaux antérieurement inspectés, sans réouverture hors régression prouvée

Source de départ : [docs/reports/map/MAP2W/R2B/REPORT.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/MAP2W/R2B/REPORT.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC5-PRUSSIAN-WEST — Gueldre, Clèves, Mark et Ravensberg

P1 · poids 4 · `NOT_STARTED` · profil `territorial`.

Région/périmètre : Clèves, Mark, Ravensberg et Gueldre prussienne. Dépendances : aucune.

Acceptation : Partage de 1713 et limites importantes; Minden acquis conservé, pas acquisitions XIXe.

Source de départ : [docs/reports/map/MAP2L/RHINE_WESTPHALIA_COMPLETION/UNRESOLVED.csv:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/MAP2L/RHINE_WESTPHALIA_COMPLETION/UNRESOLVED.csv>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC5-JEVER — Jever sous Anhalt-Zerbst

P1 · poids 2 · `BLOCKED` · profil `territorial`.

Région/périmètre : Frise orientale méridionale et Jever. Dépendances : aucune.

Acceptation : Titre AZR établi mais contour OLD candidat non résolu; noyau B justifié ou report autorisé, jamais tout OLD.

Source de départ : [docs/reports/map/MAP2S/JEVER_HISTORICAL_EVIDENCE.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/MAP2S/JEVER_HISTORICAL_EVIDENCE.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC5-EAST-FRISIA-SOUTH — Leer et Rheiderland

P1 · poids 2 · `BLOCKED` · profil `territorial`.

Région/périmètre : Frise orientale méridionale et Jever. Dépendances : aucune.

Acceptation : 319 cellules Emden PRU conservées; nouvelles preuves d’intersection, pas 1240 erreurs supposées.

Source de départ : [docs/reports/map/MAP2P/REPORT.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/MAP2P/REPORT.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC5-WESTPHALIAN-ESTATES — Dortmund et temporalités/comtés westphaliens

P1 · poids 4 · `NOT_STARTED` · profil `territorial`.

Région/périmètre : Lippe et Schaumbourg-Lippe; Petits comtés, abbayes et Dortmund. Dépendances : aucune.

Acceptation : Gage de Bentheim, Corvey abbaye, Essen/Werden, Steinfurt/Rietberg; pas pays automatique pour chaque enclave.

Source de départ : [docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC5-HESSE-RHINE — Worms/Spire, Hombourg et Hanau

P1 · poids 4 · `NOT_STARTED` · profil `territorial`.

Région/périmètre : Hesses, Waldeck, Francfort et juridictions rhénanes restantes. Dépendances : aucune.

Acceptation : Villes, évêchés et apanages distingués; aucune principauté souveraine déduite d’un nom dynastique.

Source de départ : [docs/reports/map/MAP2W/R2B/UNRESOLVED_R2B.csv:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/MAP2W/R2B/UNRESOLVED_R2B.csv>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC5-NASSAU-FULDA-OUTLIERS — Franges de Nassau et Fulda

P1 · poids 2 · `NOT_STARTED` · profil `territorial`.

Région/périmètre : Fulda et branches de Nassau installées; Hesses, Waldeck, Francfort et juridictions rhénanes restantes. Dépendances : aucune.

Acceptation : Noyaux R1/R2A/R2B protégés, pas Nassau unifié 1806 ni acquisitions tardives.

Source de départ : [docs/reports/map/MAP2W/R2B/UNRESOLVED_R2B.csv:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/MAP2W/R2B/UNRESOLVED_R2B.csv>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC5-MONTBELIARD — Comté de Montbéliard

P1 · poids 2 · `BLOCKED` · profil `territorial`.

Région/périmètre : Montbéliard, Oettingen et franges souabes. Dépendances : aucune.

Acceptation : Quatre seigneuries françaises après 1748 distinguées; aucune rétroprojection du traité 1786.

Source de départ : [docs/reports/map/MAP2L/SWABIA_COMPLETION/UNRESOLVED.csv:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/MAP2L/SWABIA_COMPLETION/UNRESOLVED.csv>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC5-OETTINGEN — Branches d’Oettingen

P1 · poids 2 · `NOT_STARTED` · profil `territorial`.

Région/périmètre : Montbéliard, Oettingen et franges souabes. Dépendances : aucune.

Acceptation : Titulaires et grandes possessions établis sans annexion des noyaux souabes voisins.

Source de départ : [docs/reports/map/MAP2L/SWABIA_COMPLETION/UNRESOLVED.csv:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/MAP2L/SWABIA_COMPLETION/UNRESOLVED.csv>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC5-BELGIAN-FRINGES — Limbourg, Maastricht et franges belges

P1 · poids 2 · `NOT_STARTED` · profil `territorial`.

Région/périmètre : Limbourg, Maastricht, Bouillon et franges belges. Dépendances : aucune.

Acceptation : Condominiums et statuts distincts; BEO/LGE/STM déjà validés protégés.

Source de départ : [docs/reports/map/MAP2L/BELGIUM/IMPLEMENTATION.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/MAP2L/BELGIUM/IMPLEMENTATION.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC5-ERFURT — Arbitrage Erfurt–Eichsfeld

P1 · poids 3 · `BLOCKED` · profil `territorial`.

Région/périmètre : Erfurt–Eichsfeld. Dépendances : aucune.

Acceptation : Pas nouvelle optimisation sur mêmes points ni translation 7,20 px; preuves nouvelles ou report P1 explicitement approuvé.

Source de départ : [docs/reports/map/MAP2L/ERFURT_EICHSFELD/REPORT.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/MAP2L/ERFURT_EICHSFELD/REPORT.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC5-MINDEN-VALIDATION — Portée manuelle Minden

P1 · poids 1 · `IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION` · profil `runtime_only`.

Région/périmètre : Minden : correction de 76 cellules. Dépendances : aucune.

Acceptation : 76 cellules PRU installées; ne pas étendre le reçu voisin; aucune reconstruction supplémentaire.

Source de départ : [docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/COMPLETED_LOTS.csv:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/COMPLETED_LOTS.csv>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC5-COLOGNE-VALIDATION — Portée manuelle duché de Westphalie/Vest

P1 · poids 1 · `IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION` · profil `runtime_only`.

Région/périmètre : Duché de Westphalie et Vest de Cologne. Dépendances : aucune.

Acceptation : 84 cellules KCL et EDAB00–07 protégés; test du seul sous-lot.

Source de départ : [docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/COMPLETED_LOTS.csv:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/COMPLETED_LOTS.csv>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC5-MAINZ-VALIDATION — Portée manuelle des trois couches Mayence

P1 · poids 2 · `IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION` · profil `runtime_only`.

Région/périmètre : Mayence Rheingau–Bergstraße–Spessart–Tauber. Dépendances : aucune.

Acceptation : Rheingau/Spessart/Bergstraße/Tauber inspectés, Erfurt exclue.

Source de départ : [docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/COMPLETED_LOTS.csv:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/COMPLETED_LOTS.csv>). Rapports, autres sources et incertitudes : fiche JSON du même ID.


### Phase 6 — Petites juridictions significatives et arbitrages

#### BASE-FRANCONIA — Franconie principale et continuation inspectées

P1 · poids 6 · `PASS_RUNTIME_USER_VALIDATED` · profil `legacy_core`.

Région/périmètre : Franconie : noyaux principaux et continuation. Dépendances : aucune.

Acceptation : Conserver les seuls noyaux antérieurement inspectés, sans réouverture hors régression prouvée

Source de départ : [docs/reports/map/MAP2L/FRANCONIA_CONTINUATION/REPORT.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/MAP2L/FRANCONIA_CONTINUATION/REPORT.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### BASE-SWABIA — Première Souabe : noyaux inspectés

P1 · poids 3 · `PASS_RUNTIME_USER_VALIDATED` · profil `legacy_core`.

Région/périmètre : Souabe : première passe. Dépendances : aucune.

Acceptation : Conserver les seuls noyaux antérieurement inspectés, sans réouverture hors régression prouvée

Source de départ : [docs/reports/map/MAP2L/SWABIA/REPORT.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/MAP2L/SWABIA/REPORT.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### BASE-SWABIA-FINISH — Salem/Waldburg/Constance : finition inspectée

P1 · poids 3 · `PASS_RUNTIME_USER_VALIDATED` · profil `legacy_core`.

Région/périmètre : Salem, Waldburg, Constance : finition. Dépendances : aucune.

Acceptation : Conserver les seuls noyaux antérieurement inspectés, sans réouverture hors régression prouvée

Source de départ : [docs/reports/map/MAP2L/SWABIA_FINISH/REPORT.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/MAP2L/SWABIA_FINISH/REPORT.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### BASE-SWABIA-CITIES — Villes libres/Weingarten : dernières corrections inspectées

P1 · poids 3 · `PASS_RUNTIME_USER_VALIDATED` · profil `legacy_core`.

Région/périmètre : Villes libres, Weingarten et raccord autrichien. Dépendances : aucune.

Acceptation : Conserver les seuls noyaux antérieurement inspectés, sans réouverture hors régression prouvée

Source de départ : [docs/reports/map/MAP2L/SWABIA_COMPLETION/REPORT.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/MAP2L/SWABIA_COMPLETION/REPORT.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC6-HOHENLOHE — Branches significatives de Hohenlohe

P1 · poids 4 · `BLOCKED` · profil `territorial`.

Région/périmètre : Hohenlohe, Castell, Wertheim et villes secondaires. Dépendances : aucune.

Acceptation : Candidats R3 retirés, aucune réinstallation sur référentiel refusé; B politique étayé ou arbitrage autorisé.

Source de départ : [docs/reports/map/MAP2W/R3/CALIBRATION/REPORT.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/MAP2W/R3/CALIBRATION/REPORT.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC6-CASTELL-WERTHEIM — Castell et Wertheim

P1 · poids 3 · `BLOCKED` · profil `territorial`.

Région/périmètre : Hohenlohe, Castell, Wertheim et villes secondaires. Dépendances : aucune.

Acceptation : Branches de 1776 et droits partagés; aucun titre ou acquisition de 1803/1813 rétroprojeté.

Source de départ : [docs/reports/map/MAP2W/R3/CALIBRATION/REPORT.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/MAP2W/R3/CALIBRATION/REPORT.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC6-FRANCONIAN-CITIES — Rothenburg, Schweinfurt, Windsheim, Weißenburg

P1 · poids 3 · `BLOCKED` · profil `territorial`.

Région/périmètre : Hohenlohe, Castell, Wertheim et villes secondaires. Dépendances : aucune.

Acceptation : Noyaux politiques représentables ou report explicitement accepté; pas quatre cellules automatiquement autorisées.

Source de départ : [docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC6-GOSLAR — Ville impériale de Goslar

P1 · poids 1 · `NOT_STARTED` · profil `territorial`.

Région/périmètre : Hanovre, Brunswick et principautés du Harz. Dépendances : SC3-BRUNSWICK-HARZ.

Acceptation : Ne pas lui attribuer le Rammelsberg brunswickois depuis 1552; coordination avec SC3-BRUNSWICK-HARZ.

Source de départ : [docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC6-SWABIAN-ARBITRATIONS — Dernières juridictions significatives franconiennes/souabes

P1 · poids 2 · `NOT_STARTED` · profil `territorial`.

Région/périmètre : Franges franconiennes et possessions dispersées; Montbéliard, Oettingen et franges souabes. Dépendances : aucune.

Acceptation : Noyaux déjà validés protégés; micro-enclaves P2 reportées sans devenir des frontières historiquement corrigées.

Source de départ : [docs/reports/map/MAP2L/SWABIA_COMPLETION/UNRESOLVED.csv:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/MAP2L/SWABIA_COMPLETION/UNRESOLVED.csv>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC6-SWABIA-CONTINUATION-VALIDATION — Portée manuelle Fürstenberg/Ellwangen

P1 · poids 1 · `IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION` · profil `runtime_only`.

Région/périmètre : Fürstenberg et Ellwangen : continuation. Dépendances : aucune.

Acceptation : Le reçu FINISH ne couvre pas automatiquement toute la continuation; contrôle borné sans reconstruire SFU/SEW.

Source de départ : [docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/COMPLETED_LOTS.csv:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/COMPLETED_LOTS.csv>). Rapports, autres sources et incertitudes : fiche JSON du même ID.


### Phase 7 — Cohérence impériale et validation finale

#### SC7-MEMBERS-ELECTORS — Membres, neuf électeurs, gouvernements et souverains

P1 · poids 3 · `NOT_STARTED` · profil `no_functional_change`.

Région/périmètre : Petites juridictions non cerclées et chevalerie. Dépendances : aucune.

Acceptation : Listes et dignités cohérentes, droits territoriaux séparés du TAG; absence de correction nécessaire démontrée ou corrections validées.

Source de départ : [docs/reports/hre/HRE_CENTRALIZATION_01/REPORT.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/hre/HRE_CENTRALIZATION_01/REPORT.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC7-REGISTRY — Registre territorial et périmètre impérial final

P1 · poids 3 · `NOT_STARTED` · profil `no_functional_change`.

Région/périmètre : Petites juridictions non cerclées et chevalerie; Moravie et Silésie autrichienne. Dépendances : aucune.

Acceptation : Chaîne approuvée, Teschen et exclusions vérifiés; pas SERG = possessions de toutes les dynasties.

Source de départ : [docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/SUPPLEMENTAL_CHECKS.json:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/SUPPLEMENTAL_CHECKS.json>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC7-INSTITUTIONS — Sujets, transitions, sécession et successions réellement utilisés

P1 · poids 4 · `NOT_STARTED` · profil `territorial`.

Région/périmètre : Petites juridictions non cerclées et chevalerie. Dépendances : aucune.

Acceptation : Taux 15/10, sortie impériale et scénarios actifs testés; prototype isolé non activé n’est pas automatiquement à développer.

Source de départ : [docs/reports/hre/HRE_CENTRALIZATION_01/REPORT.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/hre/HRE_CENTRALIZATION_01/REPORT.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC7-DEMOGRAPHY-ECONOMY — Populations, bâtiments, PM, propriété et unités

P1 · poids 3 · `NOT_STARTED` · profil `no_functional_change`.

Région/périmètre : Petites juridictions non cerclées et chevalerie. Dépendances : aucune.

Acceptation : Invariants ou changements historiques explicites tracés; pas obligation de conserver une population mondiale artificielle.

Source de départ : [docs/reports/map/MAP2W/R4/POLITICAL_REPRESENTATION/FREISING_REGENSBURG/UNRESOLVED.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/MAP2W/R4/POLITICAL_REPRESENTATION/FREISING_REGENSBURG/UNRESOLVED.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC7-NONREGRESSION — Non-régression cartographique et dette technique

P1 · poids 3 · `NOT_STARTED` · profil `no_functional_change`.

Région/périmètre : Petites juridictions non cerclées et chevalerie. Dépendances : aucune.

Acceptation : 44 doublons/12 références hérités et vieux snapshots classés; aucun test bloquant inexpliqué.

Source de départ : [docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/DIAGNOSTIC_SUMMARY.json:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/DIAGNOSTIC_SUMMARY.json>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC7-P2-REGISTER — Registre final des B et P2 reportés

P1 · poids 1 · `NOT_STARTED` · profil `no_functional_change`.

Région/périmètre : Petites juridictions non cerclées et chevalerie; Liechtenstein et autres exceptions alpines. Dépendances : aucune.

Acceptation : Décisions explicites et portée conservées; P2 ne bloque pas le cadastre, mais un crash réel n’est pas masqué.

Source de départ : [docs/reports/map/MAP2M/R9/REPORT.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/MAP2M/R9/REPORT.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC7-P1-DECISIONS — Revue des P0/P1 et des secteurs obligatoires

P1 · poids 2 · `NOT_STARTED` · profil `no_functional_change`.

Région/périmètre : Petites juridictions non cerclées et chevalerie. Dépendances : aucune.

Acceptation : Chaque P1 traité ou report non bloquant approuvé; aucun P0 ou grand secteur sans audit esquivé.

Source de départ : [docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

#### SC7-FINAL-APPROVAL — Validation finale en jeu et approbation de clôture

P1 · poids 6 · `NOT_STARTED` · profil `final_closure`.

Région/périmètre : Petites juridictions non cerclées et chevalerie. Dépendances : BASE-PASSAU, BASE-FREISING, BASE-REGENSBURG, BASE-BELGIUM, BASE-EUTIN, BASE-SWEDISH-MECKLENBURG, BASE-PEENE, BASE-ANHALT, BASE-SAXONY, BASE-REUSS, BASE-RHINE-WESTPHALIA, BASE-OSNABRUCK, BASE-EMDEN, BASE-RHINE-CENTRAL, BASE-NASSAU-FULDA, BASE-FRANCONIA, BASE-SWABIA, BASE-SWABIA-FINISH, BASE-SWABIA-CITIES, SC1-SALZBURG, SC1-TRENTO, SC1-BRIXEN, SC1-BERCHTESGADEN, SC1-FREISING-OUTLIERS, SC1-REGENSBURG-OUTLIERS, SC1-PASSAU-OUTLIERS, SC1-REGENSBURG-DEMOGRAPHY, SC1-ORTENBURG, SC2-BOHEMIA, SC2-MORAVIA, SC2-AUSTRIAN-SILESIA, SC2-AUSTRIA, SC2-INNER-AUSTRIA, SC2-TYROL, SC2-ANTERIOR-AUSTRIA, SC2-TESCHEN, SC2-MAP2A-VALIDATION, SC2-LUXEMBOURG-VALIDATION, SC3-HOLSTEIN, SC3-MECKLENBURG, SC3-BRUNSWICK-HARZ, SC3-HILDESHEIM, SC3-BRANDENBURG, SC3-SILESIA-LUSATIA, SC3-SWEDISH-DEPENDENCIES, SC3-NORTHERN-JURISDICTIONS, SC4-EXISTING-ITALIAN-STATES, SC4-SAVOY-NICE, SC4-LIGURIAN-FIEFS, SC4-PIOMBINO, SC4-MASSA-CARRARA, SC4-MILAN-OUTLIERS, SC4-MILAN-VALIDATION, SC4-PIEDMONT-VALIDATION, SC5-PRUSSIAN-WEST, SC5-JEVER, SC5-EAST-FRISIA-SOUTH, SC5-WESTPHALIAN-ESTATES, SC5-HESSE-RHINE, SC5-NASSAU-FULDA-OUTLIERS, SC5-MONTBELIARD, SC5-OETTINGEN, SC5-BELGIAN-FRINGES, SC5-ERFURT, SC5-MINDEN-VALIDATION, SC5-COLOGNE-VALIDATION, SC5-MAINZ-VALIDATION, SC6-HOHENLOHE, SC6-CASTELL-WERTHEIM, SC6-FRANCONIAN-CITIES, SC6-GOSLAR, SC6-SWABIAN-ARBITRATIONS, SC6-SWABIA-CONTINUATION-VALIDATION, SC7-MEMBERS-ELECTORS, SC7-REGISTRY, SC7-INSTITUTIONS, SC7-DEMOGRAPHY-ECONOMY, SC7-NONREGRESSION, SC7-P2-REGISTER, SC7-P1-DECISIONS.

Acceptation : Nouvelle partie 1776, mois et contrôles adaptés, puis accord explicite du responsable pour SERG_TERRITORIAL_1_0_COMPLETE.

Source de départ : [docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/COMPLETED_LOTS.csv:1](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/COMPLETED_LOTS.csv>). Rapports, autres sources et incertitudes : fiche JSON du même ID.

## Mises à jour additives et stabilité du périmètre

Ne jamais réinitialiser le suivi. Pour chaque passe : modifier les seules fiches concernées, conserver les reçus anciens, ajouter un événement daté et sourcé dans `events` (ID unique; `changes` avec `task_id`, `before`, `after`; résultats/progression avant-après). Les preuves de décision et les reçus nouveaux sont des fichiers distincts dans le rapport du sous-lot; aucun faux test moteur. Puis exécuter le validateur, régénérer les vues, vérifier le diff et ajouter le bilan à l’événement. Les vues sont dérivées de l’historique intégral, pas un journal libre effacé à chaque passe.

Nouvelle erreur P0/P1 : conserver l’ancienne tâche, ajouter ou étendre explicitement le périmètre avec justification. Versionner `scope_version`, créer un nouveau manifeste immuable `scopes/<version>.json` avec `previous_version`, ajouter un événement `SCOPE_CHANGE` contenant `before_weight`, `after_weight`, `before_percent`, `after_percent`, `reason`. L’ancien dénominateur et la baisse éventuelle restent visibles. Aucun retrait de tâche pour améliorer le score. Un cas P2 révélant un crash doit être reclassé.

Schéma de preuve des futurs états terminaux : un PASS a un rapport d’implémentation, un rapport statique JSON (`task_ids`, `passed = total > 0`, `failed` vide), et un reçu humain (`status`, `task_ids`, `source`, `new_game_date`, `simulation_months`, `automated_engine_test: false`). Les reçus hérités sont acceptés tels quels, sans leur inventer un mois de simulation. Un NA exige une décision sourcée (`no_correction_required: true`, `approved_by: user`, `reason`, `evidence`) et des contrôles adaptés. Un report P1 exige `nonblocking_1_0: true` et la même autorité; jamais un P0 ou une validation finale reporté. Ce garde-fou mécanique vérifie des pièces, pas leur vérité historique : lecture et responsabilité de l’agent restent indispensables.

### Outils de lecture et vues

`python -B -X utf8 tools/serg_closure_roadmap.py check` : état, preuves, dépendances, périmètre, historique et vues; lecture seule.

`python -B -X utf8 tools/serg_closure_roadmap.py observe` : changements depuis l’instantané initial; lecture seule. Une future correction autorisée changera normalement les empreintes; documenter ces différences, ne pas les restaurer.

`python -B -X utf8 tools/serg_closure_roadmap.py render` : régénère uniquement ces rapports et `PROGRESS_SNAPSHOT.json`, sans changer état, reçus, historique ou fichiers du jeu. `init` refuse toute réinitialisation. Utiliser le Python disponible sans installer de dépendance.

## Référence unique, protection et démarrage

[Ancien CL1–CL7](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/CLOSURE_ROADMAP.md>) reste une source historique figée de l’audit, pas une seconde feuille opérationnelle. Les CSV originaux, l’inventaire des 158 entrées et les critères sont reliés par les sources et empreintes de `source_manifest`; ils ne sont pas recopiés comme une nouvelle vérité territoriale.

Conserver noyaux validés de Franconie, Rhénanie, Souabe, territoires suédois, Anhalt, Thuringe/Reuss, Fulda/Nassau, Passau/Freising/Ratisbonne. Protéger le chantier américain, accords franco-américains, obligations, Minutemen, événements/unités, Saint-Gobain/Anzin et modifications françaises. Pas de Git en écriture ni de vanilla modifié dans cette mission.

Le renvoi court de `AGENTS.md` est limité aux futures passes SERG. La [documentation officielle des instructions de dépôt](https://learn.chatgpt.com/docs/agent-configuration/agents-md) décrit leur chargement au démarrage d’une session, selon leur portée et les éventuels overrides; ce n’est pas un hook d’exécution. Aucun nouveau lancement de session n’a été testé ici. Ligne de démarrage de secours à inclure dans tout nouveau prompt SERG :

> Lis `docs/reports/map/SERG_CLOSURE/ROADMAP.md`, puis `ROADMAP_STATE.json`, `NEXT_ACTION.md` et `BLOCKERS.md`; vérifie le workspace et les anciennes passes avant de choisir le sous-lot autorisé; actualise le suivi et les preuves à la fin, sans refaire les noyaux validés.

Liens : [PROGRESS_HISTORY.md](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_CLOSURE/PROGRESS_HISTORY.md>) · [CLOSURE_CHECKLIST.md](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_CLOSURE/CLOSURE_CHECKLIST.md>) · [DEFERRED_P2.md](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_CLOSURE/DEFERRED_P2.md>) · [BLOCKERS.md](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_CLOSURE/BLOCKERS.md>) · [NEXT_ACTION.md](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_CLOSURE/NEXT_ACTION.md>) · [INITIAL_STATE.json](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/map/SERG_CLOSURE/INITIAL_STATE.json>).
