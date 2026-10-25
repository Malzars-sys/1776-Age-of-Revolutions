# SERG — audit général de clôture

18 octobre 2026. Date historique : **1er janvier 1776**.

**SERG_GLOBAL_CLOSURE_AUDIT_COMPLETE** signifie audit livré, **pas reconstruction territoriale terminée**. Le statut **SERG — TERRITORIAL VERSION 1.0 COMPLETE n’est pas justifié actuellement**.

## Conclusion décisionnelle

Les principales reconstructions occidentales sont réellement installées. Recommencer la Franconie, la Belgique, les lots Rhin–Westphalie ou les quatre passes de Souabe ferait perdre du temps et risquerait d’écraser le travail existant.

Cependant, il ne reste pas seulement quelques micro-enclaves. De grands secteurs habsbourgeois, plusieurs ensembles septentrionaux et l’Italie impériale n’ont pas reçu un audit territorial comparable. Des recherches macro, économiques ou dynastiques existent : elles ne sont ni ignorées ni assimilées à une reconstitution politique achevée.

Organisation recommandée : **six lots géographiques groupés, puis un lot final de cohérence et de validation**. C’est un découpage minimal pratique des problèmes actuellement connus, pas un minimum mathématique, une durée promise ou la garantie de six petits correctifs. Aucun de ces lots ne commence avec cet audit.

## 1. Dépôt actuel et protections

- Branche : main.
- HEAD : 9b1764e3f43a7e9bd6ef4bee7eef9f9182d069b6.
- Workspace initial déjà modifié, avec fichiers non suivis et travaux USA/France/SERG concurrents : capture intégrale de son statut dans BASELINE.json.
- **2 362 fichiers fonctionnels protégés**, empreinte de l’index et HEAD inchangés au contrôle final; aucune différence fonctionnelle observée. Voir PROTECTION_CHECK.json.
- Aucune migration, installation cartographique, compilation impériale, modification de vanilla ou opération Git d’écriture exécutée.

### Preuves d’installation fraîches

**573/573 entrées du registre actif** correspondent au propriétaire et à la région réellement écrits au démarrage. Les **326 affectations géométriques finales** de la chaîne approuvée correspondent aux propriétaires actuels et aux cellules explicitement enregistrées. Les trente migrations sont appliquées **en mémoire**, seulement pour lire leur ordre et déterminer les affectations finales; aucun installateur n’est exécuté.

Les anciens parents remplacés par une couche ultérieure ne sont pas faussement comptés comme corrections perdues. Pour les lignes sans liste de coordonnées, les contrôles supplémentaires vérifient cardinalité/propriétaire, sans inventer un contrôle de position. La Belgique antérieure à cette chaîne, Piémont, Luxembourg et MAP2A font l’objet de contrôles complémentaires. Détails dans REGISTRY_CHECKS.json, EFFECTIVE_GEOMETRY_CHECKS.json et SUPPLEMENTAL_CHECKS.json.

Ce résultat ne certifie pas l’exhaustivité historique du registre : les attributions gelées de gameplay restent distinguées des frontières étudiées.

### Dette technique, séparée des régressions

Les **44 doublons RGB et 12 références invalides hérités** sont identiques à la baseline R4-B/C, et non créés ici. La référence de propriétaire économique VEN en Autriche figure parmi ces douze; elle n’est pas déclarée réparée.

La dernière suite cumulative R4-B/C reste **258/260**, dont **37/37 nouveaux tests** réussis. Les deux échecs sont les anciennes assertions « Passau dernière couche », conservées dans TESTS.json. Ils ne sont ni effacés ni rebaptisés PASS; le contrôle actuel de la chaîne R4B/R4C est distinct. Cet audit ne prétend pas rejouer toutes les anciennes suites.

Population mondiale écrite : **835 801 255**. Aucun habitant, bâtiment, PM, propriétaire économique, formation, recrutement ou gouvernement modifié. Les tableaux lisent les données présentes; les effets de chargement et de simulation ne sont pas exécutés.

## 2. Chronologie reconstruite, sans confondre dossiers et réalisations

| Séquence | Ce qui existe réellement | Limite |
|---|---|---|
| MAP1, MAP1B, MAP1C | Ingestion R1/R2, dossiers et diagnostics Luxembourg/Lombardie/Silésie | Pas des transferts installés; les maintiens proposés n’étaient pas des frontières certifiées |
| Luxembourg → BEO, puis MAP2A | xD001A0 sous BEO; Trois Ligues représentées par SWI; deux doubles propriétaires silésiens supprimés; Teschen rescopé | Les approximations ne deviennent pas des cadastres |
| MAP2B–2I | Résumés et corpus parcourus, principalement chantiers extérieurs au SERG | Aucun redécoupage HRE supplémentaire déduit du seul préfixe MAP |
| MAP2K | Quatre électorats actifs supplémentaires, cinq anciens RGB réattribués; neuf dignités électorales et cadre impérial | Le registre gelé n’est pas une preuve historique province par province |
| MAP2L Belgique et Piémont | LGE/STM et subdivisions belges; SAR au bloc, neuf RGB piémontais au registre | Antérieurs aux trente migrations explicites, donc non omis du bilan |
| MAP2L Franconie → continuation | Ansbach–Bayreuth, Würzburg, Bamberg, Nuremberg, fragments Eichstätt/Cobourg; prolongements dans Bavière | Hohenlohe et toutes les franges BAV ne sont pas résolus |
| MAP2L Rhin/Mayence/Westphalie | Neckar, Rheingau, Bergstraße, Spessart, Tauber; Münster/Paderborn/Juliers–Berg; Minden, duché/Vest de Cologne; Osnabrück/Niederstift/Lingen/Tecklenburg | Erfurt–Eichsfeld et petites juridictions restent distincts |
| MAP2L Souabe, continuation, finition, completion | Pays ecclésiastiques, Hohenzollern, Ulm, Fürstenberg/Ellwangen, Salem, Waldburg, Constance, villes libres et Weingarten | Montbéliard, Oettingen et possessions dispersées restent ouverts |
| Frontières prussiennes puis MAP2M | Noyau suédois 341 cellules; R2/R3/R8/R9 retouches, Peene/Wolgast; Bromberg 85 cellules | Netze/Thorn extérieurs au SERG ne sont pas annoncés terminés |
| MAP2N | Poel reconstruite, Wismar et Neukloster; souveraineté suédoise territoriale | Poel regroupée techniquement en Poméranie, pas adhésion de toute la Suède |
| MAP2O/P | Emden 319 cellules PRU installé; audit méridional sans correction supplémentaire | Les 1 240 cellules d’enveloppes C ne sont pas 1 240 erreurs prouvées |
| MAP2Q/R2/R3 | HLB distinct de LUB, union OLD–HLB; Eutin 7600, puis Schwartau/Kaltenhof et total HLB 9206 | Le chiffre 11325 est obsolète; les possessions du chapitre ne sont pas toutes reconstruites |
| MAP2R/S | Quatre principautés d’Anhalt installées; audit Jever sans transfert | Jever reste à corriger, pas passée à AZR par la seule présence de ce TAG |
| MAP2T/U | Duchés saxons, Reuss et Schwarzbourg-Sondershausen, compléments septentrionaux | Les anciens inventaires pré-T/U ne prouvent plus l’absence de ces pays |
| HRE-CENTRALIZATION et suites | Types de sujets, taux 15 %/10 %, transitions et lentille installés | Succession des sujets natifs : prototype isolé non activé; validation moteur complète non fournie |
| MAP2W R1/R2-A/R2-B | Fulda, Nassau-Orange/Weilbourg/Sarrebruck et raccords | Pas Hesse/Nassau intégralement terminés |
| MAP2W R3 et CALIBRATION | Diagnostic et candidats entièrement retirés | Aucun HLN/HKI, xEDB900–903 ou migration R3 active |
| MAP2W R4 puis méthode politique | Premier blocage géographique, puis noyau PAS installé en B | Le premier rapport bloqué n’est plus l’état du noyau PAS |
| MAP2W R4-B/C | FSI 14 cellules; RBI 14 cellules; RCI 2 cellules | Noyaux validés par le joueur, possessions périphériques ouvertes |

Les corpus hors MAP ont aussi été recherchés : feuille de route mondiale, recherches de bâtiments et technologies d’Europe centrale/Italie, sources de personnages, allocations militaires impériales et dossiers institutionnels HRE. Ils apportent du contexte, pas une preuve de reconstruction de chaque frontière. SOURCE_AND_REPORT_INDEX.md distingue ces pistes de la documentation d’installation.

## 3. Mesure de couverture — trois dimensions séparées

L’inventaire délimité pour cet audit comprend **54 sous-secteurs dans 11 macro-ensembles** et **158 lignes de juridictions, possessions ou groupes de branches**. Il ne prétend pas recenser chaque seigneurie immédiate de 1776.

| Statut de sous-secteur | Lignes |
|---|---:|
| VALIDÉ EN JEU | 19 |
| INSTALLÉ — NON VALIDÉ | 7 |
| PARTIELLEMENT TRAITÉ | 15 |
| AUDITÉ — BLOQUÉ OU DIFFÉRÉ | 7 |
| NON AUDITÉ | 6 |
| AUDITÉ — CONFORME | 0 |

Le zéro « conforme » est délibéré : un maintien, une recherche bloquée ou la présence d’un grand pays ne suffisent pas à qualifier un secteur entier de conforme.

- **Recherche historique :** six sous-secteurs sans audit territorial détaillé suffisant retrouvé; plusieurs autres n’ont qu’un examen partiel. « NON AUDITÉ » ne signifie pas aucune bibliographie de contexte.
- **Représentation :** 117 lignes d’inventaire ont un TAG actif et des RGB techniques identifiés. Certaines sont des agrégations sous souverain commun : ce ne sont pas 117 pays territorialement complets.
- **Pas d’addition abusive :** plusieurs lignes partagent un TAG ou un ensemble RGB. Les populations par TAG et cellules techniques ne doivent pas être additionnées comme des juridictions disjointes.
- **Absences distinctes confirmées :** douze lignes, dont un groupe Hohenlohe, pas douze États souverains dénombrés exhaustivement. Les autres « absents ou abstraits à vérifier » hérités ne sont pas promus en certitudes.
- **Abstractions d’inventaire :** neuf lignes explicitement abstraites ou à arbitrer, auxquelles s’ajoutent les limites B et reports suivis dans le tableau dédié.
- **Installations :** 43 interventions documentées : trente couches territoriales approuvées, retouches de couleurs existantes, extension de registre, démographie et institutions sont distinguées. Ce n’est pas un nombre de pays ou de frontières.
- **Validation manuelle :** 29 de ces lignes sont associées à un reçu, parfois général. Ce ne sont pas 29 campagnes indépendantes ni 29 certifications historiques.
- **Problèmes :** trois P0 — une absence majeure, Salzbourg, et deux blocages de couverture, Habsbourg et Italie; **21 P1 et dix P2**. La priorité décrit le travail de clôture, pas seulement les bugs.

Aucun dénominateur historique exhaustif ou superficie impériale certifiée n’est disponible : **aucun pourcentage global n’est calculé**. Les indicateurs techniques, historiques et manuels ne sont pas fusionnés.

## 4. Régions réellement traitées

### Noyaux inspectés, à préserver

Belgique/Liège/Stavelot; Franconie principale et continuation; premiers noyaux Rhin–Westphalie et Rhin central; Osnabrück/Niederstift/Lingen–Tecklenburg; première Souabe, finition Salem/Waldburg et villes/Weingarten; Poméranie suédoise/Peene/Wolgast et Wismar–Poel–Neukloster; Emden; Eutin/Schwartau; Anhalt; Saxe/Thuringe/Reuss; Fulda et branches Nassau selon portée des reçus; noyaux Passau, Freising, ville et évêché de Ratisbonne.

**Aucune grande macro-région n’est déclarée intégralement terminée par ce seul bilan.** Les noyaux validés et les franges ouvertes peuvent coexister dans le même State_ID.

### Couches présentes sans attestation spécifique suffisante

Minden; duché de Westphalie/Vest; trois couches détaillées de Mayence; continuation souabe entière; intégration luxembourgeoise; liaison Milanais–Crémonais; inclusion piémontaise. Les attestations voisines ne les couvrent pas automatiquement. Pour Fürstenberg/Ellwangen, la préservation des noyaux par des passes ultérieures ne constitue pas un reçu pour toute la couche de continuation.

### Secteurs partiels et différés

Jever et sud de Frise orientale; Gueldre/Clèves/Mark/Ravensberg; petits comtés et temporalités westphaliennes; Hombourg/Hanau et franges rhénanes; Hohenlohe/Castell/Wertheim et villes franconiennes secondaires; Montbéliard/Oettingen; possessions extérieures de Freising/Ratisbonne/Passau; enclaves d’Anhalt/Thuringe et franges belges.

Erfurt–Eichsfeld reste gelé : ni nouveau calage ni translation de 7,20 pixels. Les repères physiques, hydrographie locale et limites mayençaises identifiables manquent toujours.

### Grands ensembles insuffisamment examinés

Mecklembourg hors possessions suédoises; Bohême; cœur Autriche/Styrie/Carinthie/Carniole; Savoie/Nice et fiefs ligures; Modène/Parme/Toscane et juridictions voisines; ensemble des cas non cerclés/chevalerie. Hanovre/Harz, Brandebourg et Silésie ont des dossiers partiels, non un statut fictif « jamais étudiés ».

La remise en ordre MAP2A de la Silésie autrichienne et la liaison lombarde MAP2L sont prises en compte : elles ne permettent pas de peindre Habsbourg ou Italie tout entière comme reconstruite.

## 5. Lacunes historiques et institutionnelles

**Salzbourg** : absence politique distincte majeure P0. **Trente, Brixen, Berchtesgaden et Hildesheim** : juridictions ecclésiastiques attestées, représentation à traiter/arbitrer en P1. Ce ne sont pas des terres simplement AUS/BAV/HAN par défaut. **Hohenlohe**, **Dortmund**, **Rothenburg, Schweinfurt, Windsheim, Weißenburg** et **Goslar** n’ont pas de représentation politique distincte identifiée; viabilité et contours restent à instruire, pas une cellule automatiquement autorisée pour chaque ville.

Sources indépendantes précises dans HISTORICAL_GAPS.md et dans chaque ligne de l’inventaire. L’existence d’une souveraineté ne prouve jamais à elle seule l’appartenance d’un RGB entier.

**Écart de registre démontré : x9061E0**, 179 cellules AUS, STATE_WEST_GALICIA. MAP2A l’a conservé comme approximation de Teschen, mais il est absent du registre impérial actuel, contrairement aux deux RGB autrichiens rescopés vers MORAVIA. Le filtre de régions de tools/map2k_imperial_system.py:15 n’inclut pas WEST_GALICIA. Il faut instruire la portion impériale de cette représentation, **pas ajouter toute la Galicie**. Le présent audit ne certifie pas que les 179 cellules reproduisent exactement le duché historique.

Les dépendances natives suédoises LUB/MEC/MST ont été conservées explicitement comme choix de gameplay dans MAP2K. Cette conservation n’est pas une certification historique : arbitrage requis pour une clôture 1.0. Les scénarios de conversion et succession des nouveaux sujets impériaux demandent un protocole moteur distinct.

**MOD, PAR, TUS, LUC et GEN existent déjà.** LUC n’est pas un pays manquant parce qu’il n’apparaît pas dans le registre actuel. Piombino et Massa-Carrare figuraient déjà dans R1; les qualifications dynastiques, impériales et les frontières restent à résoudre, notamment la différence entre mariage d’Este et institutions Cybo-Malaspina. Un pays de toute l’Italie du Nord n’est pas automatiquement un État impérial pour l’ensemble de ses possessions.

## 6. Démographie, gouvernements et niveaux de preuve

COUNTRY_FACTS.json et l’inventaire relisent les définitions effectives, capitales, historiques de pays/personnages, lois gouvernementales directement écrites, populations et possessions. Une loi peut être activée par un effet natif; absence de déclaration directe ne signifie pas absence de gouvernement. Le type visuel choisi par le moteur n’est pas simulé.

Eutin 7600 est une estimation historique explicitement acceptée; HLB totalise 9206 après Schwartau. Les autres allocations surfaciques sont techniques et provisoires. **RCI 713** et sa composition confessionnelle héritée doivent être examinés séparément, malgré le test runtime réussi. L’ancienne conservation mondiale ne doit pas empêcher une future estimation historique étayée; aucun chiffre ou compensation n’est inventé ici.

Les titulaires inconnus restent inconnus. Les noms dynastiques de 1826, titres princiers tardifs ou acquisitions de 1793/1803 ne sont pas appliqués rétroactivement.

## 7. Attestation reçue dans cette mission

RUNTIME_USER_ATTESTATION.json consigne votre confirmation explicite : **R2-B, Passau, Freising, les deux juridictions de Ratisbonne**, nouvelle partie en 1776, un mois de simulation et contrôles adaptés.

**Test manuel humain, jamais test moteur automatisé.** Pas de détail d’inspection, date du test, hash mesuré par le joueur ou validation des périphéries inventés. Les mentions « non testé » des anciens rapports restent des états de livraison datés, complétés par ce reçu additif et son index, non des refus de votre confirmation.

## 8. Carte et réutilisation

SERG_COVERAGE_MAP.png distingue les corrections associées aux reçus, couches installées non validées, résidus partiels et secteurs sans audit détaillé. Les repères numérotés correspondent à la colonne Repere_carte du CSV.

**Les repères sont des secteurs, pas des positions de villes calibrées.** Les hachures ne sont pas de nouvelles frontières. Le fond est le registre technique courant, non un périmètre historique indépendant certifié; le secteur Teschen hors registre est signalé comme partiel. Le fond clair ne prouve pas l’exclusion historique de toute terre non enregistrée.

La Suède propre, la Sardaigne insulaire, la Hongrie, la Prusse extérieure et Netze/Thorn ne deviennent pas impériaux du seul fait du TAG de leur souverain. La Bohême hors cercles ne devient pas le cercle autrichien. Les appartenances contestées ou non étudiées restent qualifiées comme telles.

## 9. ColGrep et contrôles de livraison

Deux tentatives ColGrep-Agent local : une refusée sur le verrou d’index, une aboutie après accès autorisé. Les pistes R9/HRE_REGIONS_PROGRESS.md, MAP2L/RUNTIME_USER_VALIDATION.json et FRANCONIA/REPORT.md ont été vérifiées. Le bilan R9 retrouvé était utile mais daté : il contient des lacunes résolues depuis par N/Q/R/T/U/W. L’agent local n’a pas décidé des classifications.

Pas de changement de modèle ni reconstruction volontaire d’index. Temps total de recherche locale et tokens Codex non relevés par compteur fiable : **aucune économie exacte annoncée**.

Les six CSV ont été construits comme tableaux typés, relus cellule par cellule après export et réimportation avec l’outil tableur. Leur structure sépare recherches, propriétaires, abstractions et validations; ils ne remplacent pas les preuves historiques. CSV_VALIDATION.json conserve dimensions et empreintes. La carte a été inspectée visuellement.

VALIDATION.json rassemble **821/821 contrôles frais de livraison et de protection**, dont les références, tableaux, affectations présentes, reçus, carte et métriques. Les vérifications complémentaires d’anciens RGB et de cardinalités passent à **77/77**. Ce ne sont ni 821 tests moteur ni une validation historique globale. Aucun changement fonctionnel n’a été réalisé.
