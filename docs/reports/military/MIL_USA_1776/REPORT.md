# MIL-USA-1776 — Armée américaine de départ

Date : 17 octobre 2026. Référence historique : 1er janvier 1776.

**Statut : MIL_USA_1776_READY_FOR_RUNTIME_VALIDATION.**

La configuration américaine emploie désormais douze bataillons d’infanterie à mousquet et un bataillon de canons de campagne, avec quinze bataillons de milices non levées. Aucun niveau technologique, aucune loi et aucune population n’ont été changés. Vingt-cinq contrôles statiques passent. Le passage observé de 80 à 19 conscrits n’a pas été reproduit dans le moteur ; la stabilité des nouveaux nombres reste à confirmer dans une nouvelle partie.

## Avant et après

| Élément | Avant | Après | Justification |
|---|---|---|---|
| Infanterie régulière | 17 bataillons d’infanterie de ligne | 12 bataillons d’infanterie à mousquet | Organisation continentale en renouvellement, technologie déjà acquise |
| Artillerie régulière | 1 bataillon de bombardes | 1 bataillon de canons de campagne | Unité du XVIIIe siècle déjà débloquée par `standardized_field_artillery` |
| Cavalerie régulière | 2 bataillons de hussards | 0 | Technologie absente ; deux mille cavaliers permanents ne représentent pas correctement janvier 1776 |
| Total régulier | **20 bataillons**, dont 17 d’infanterie | **13 bataillons** | Capacité maximale de 13 000 hommes, pas un décompte de présents sous les armes |
| Conscrits | 80 bataillons imposés ; 19 après recalcul selon le testeur | **15 bataillons à mousquet**, non levés | Plan régional fondé sur la population actuelle et les paramètres militaires existants |
| Technologie d’infanterie de ligne | Absente | Absente | Aucun retour sur l’arbre technologique |
| Lois américaines | Levées paysannes et autres lois actuelles | Identiques | Aucun changement pour gonfler le recrutement |
| Population américaine | **2 487 774 habitants** | Identique | Comparaison des historiques et empreintes |
| Washington et Hopkins | Commandements existants | Identiques | Aucun personnage créé, supprimé ou promu |
| Marine | 5 caravelles | Identique | Lot limité à la configuration terrestre |

## Diagnostic technique

Le TAG est `USA`. Le fichier `common/history/military_formations/01_military_formations_north_america.txt` définit explicitement les vingt réguliers dans le Connecticut : 17 fantassins de ligne, 2 hussards et 1 bombarde. Le même bloc ajoute 80 conscrits de ligne, répartis ainsi : New York 22, Pennsylvanie 15, Virginie 11, Caroline du Nord 9, Caroline du Sud 9, Géorgie 8 et Massachusetts 6. Ces nombres ne résultent pas d’une estimation de la population actuelle : ils sont littéralement écrits dans l’historique.

Il n’existe pas de déclaration américaine indépendante de caserne ou de centre de conscription dans les historiques effectifs de bâtiments. Le recrutement des unités historiques s’appuie sur le système natif des bâtiments recruteurs. `COMBAT_UNITS_PER_LEVEL = 1`, et les deux types de bâtiments ont `recruits_combat_units = yes`. Aucun second lot de casernes n’a été ajouté pour doubler les capacités.

La technologie `armament_standardization_inspection` est exigée par l’infanterie de ligne mais absente de l’historique américain. Les hussards exigent `horse_artillery`, également absente. L’infanterie à mousquet exige `light_infantry_tactics`, déjà acquise, et admet explicitement les conscrits sous levées paysannes. Les canons de campagne exigent `standardized_field_artillery`, déjà acquise. Tous les types terrestres retenus passent donc les contrôles de déblocage réels du mod.

Les fichiers permettent d’imposer directement un type dans `combat_unit`, sans condition technologique attachée à cette déclaration historique. L’affichage rapporté par le testeur montre que l’ancienne configuration a pu être instanciée. Cela ne démontre ni une exemption historique voulue ni le moment exact auquel le moteur vérifie chaque condition. Le correctif supprime l’incohérence dans les données plutôt que de compter sur une tolérance du chargeur.

Les commentaires de provenance des 80 conscrits mentionnent `CLEANUP-2D-3E-R2F EFFECTIVE CONSCRIPTS`. Le nom de l’ancien mod ne suffit donc pas à attribuer chacun de ces nombres à Tsar : la provenance vérifiable est leur déclaration actuelle et ce marqueur de maintenance.

## Répartition des réguliers

| Origine de recrutement | Infanterie à mousquet | Canons de campagne | Total |
|---|---:|---:|---:|
| Massachusetts | 8 | 1 | 9 |
| Connecticut | 2 | 0 | 2 |
| Pennsylvanie | 2 | 0 | 2 |
| Total | **12** | **1** | **13** |

Les États indiqués sont les origines administratives de recrutement du moteur, et non une reproduction de la position de chaque régiment. Les forces restent regroupées dans la formation existante `Continental Army`, au quartier général de la côte atlantique, sous Washington. On ne déploie pas artificiellement de nouvelles unités dans des provinces canadiennes non possédées.

La lettre de Washington à Hancock du [31 décembre 1775](https://founders.archives.gov/documents/Washington/03-02-02-0579) mentionne 9 650 engagements et transmet une estimation indirecte proche de 3 000 hommes dans le nord. Ce second renseignement ne constitue pas un état des présents après l’assaut de Québec. Treize bataillons de mille hommes maximum forment une abstraction arrondie de cet ordre de grandeur, sans transformer les établissements théoriques de vingt-sept régiments en vingt-sept mille hommes réellement disponibles. L’emploi effectif peut être inférieur au plafond.

L’[historique institutionnel de l’US Army](https://history.army.mil/Research/Reference-Topics/Army-Birthdays/Branch-Birthday/) situe l’autorisation d’un régiment de cavalerie continentale au 12 décembre 1776. Les petites unités montées coloniales ne justifient donc pas deux bataillons permanents de hussards dès janvier. Leur suppression n’affirme pas l’absence absolue de cavaliers dans les colonies.

## Plan de conscription

La loi conservée, `law_peasant_levies`, prévoit un taux de conscription de 4 %, des plafonds de 25 casernes et 25 centres par État, et une restriction du recrutement aux paysans. Le paramètre global du mod donne `WORKING_ADULT_RATIO_BASE = 0.30`. Le diviseur des centres est 1 000, et les unités retenues ont au maximum 1 000 hommes.

Pour dimensionner le plan, on utilise le scénario prudent `floor(max(0, population × 0,30 − réguliers × 1 000) × 0,04 / 1 000)`. La soustraction des réguliers ménage une réserve de recrutement ; ce scénario n’est pas présenté comme la formule exacte du moteur. Le calcul ne confond pas population totale et main-d’œuvre.

| État | Population écrite | Réguliers retenus | Estimation prudente de conscription | Conscrits configurés |
|---|---:|---:|---:|---:|
| New York | 191 493 | 0 | 2 | 2 |
| Pennsylvanie | 292 406 | 2 | 3 | 3 |
| Virginie | 476 609 | 0 | 5 | 5 |
| Caroline du Nord | 240 960 | 0 | 2 | 2 |
| Caroline du Sud | 157 698 | 0 | 1 | 1 |
| Géorgie | 42 993 | 0 | 0 | 0 |
| Massachusetts | 255 299 | 9 | 2 | 2 |
| Total configuré | | | **15** | **15** |

La Géorgie ne porte plus huit bataillons sur une petite population. Les petites colonies restantes ne reçoivent pas un bataillon entier par simple arrondi. Cela n’affirme pas l’absence historique de leur milice : le scénario évite de convertir chaque petite force locale en mille hommes dans le moteur. Les quinze bataillons représentent une capacité de renfort temporaire à l’échelle du pays, pas quinze mille miliciens tous présents à Boston au 1er janvier. Leur service reste `conscript` ; aucun ordre ne les active automatiquement.

Le besoin de milices pendant le renouvellement des engagements est documenté par les sources de la période ; voir [HISTORICAL_SOURCES.md](HISTORICAL_SOURCES.md). Leur effectif configuré vient du dimensionnement régional, pas du remplacement arbitraire de 80 par les 19 observés.

### Limite du diagnostic « 80 puis 19 »

Les volumes écrits dépassent largement ce que suggèrent les populations actuelles dans plusieurs régions. Le moteur recalcule les capacités des centres à partir de la main-d’œuvre, du taux et des plafonds, avec des effets possibles de statut territorial, d’obstination, d’emploi et d’éligibilité. Les descriptions vanilla du taux de conscription visent la **main-d’œuvre**, non tous les habitants. Les modificateurs d’États non incorporés ou récemment conquis peuvent réduire cette capacité.

Le nombre exact 19 reste une observation du testeur. Il ne découle pas de façon démontrée des seuls fichiers disponibles. L’emploi et les catégories sociales ne sont pas inscrits dans les créations de population américaines ; arrondis, distribution professionnelle et modificateurs effectivement actifs demandent un relevé moteur. Aucun script américain inspecté n’impose explicitement un passage de 80 à 19. Les contrôles statiques établissent une surallocation et des incompatibilités ; ils ne remplacent pas la reproduction de cette transition.

## Recrutement, commandement et ravitaillement

Les formations et rattachements de Washington et de l’amiral Esek Hopkins restent identiques. Les trois scopes de l’armée sont conservés : `dannys_army`, `regular_army`, `nabes_army`. Les treize réguliers et quinze conscrits forment un maximum de 28 bataillons, inférieur à la capacité de base de 30 d’un général de premier rang. Aucune formation américaine vide n’est créée.

Les méthodes natives de repli `pm_no_organization` et `pm_no_organization_conscription` sont disponibles sans technologie supplémentaire. Les méthodes supérieures d’instruction demandent leurs propres technologies ; le lot n’en débloque aucune. Les ratios d’instruction de base sont 97 soldats et 3 officiers pour 100 postes. Les qualifications et l’embauche effective restent à contrôler.

L’entretien de base des réguliers passe de 19 unités d’armes légères, 3 de céréales et 0,5 de fer à **12 unités d’armes légères et 1 d’artillerie**. Avec les quinze milices levées, la nouvelle capacité demande **27 armes légères et 1 artillerie**, hors options de mobilisation et modificateurs. Les salaires ne sont pas chiffrés en livres : ils dépendent des postes effectivement occupés et des règles économiques.

Les deux niveaux déclarés d’industrie d’armement en Pennsylvanie utilisent les mousquets, soit une production de base de 60 armes légères à plein emploi. Ce plafond n’est pas une preuve d’approvisionnement réalisé. Aucune fonderie d’artillerie américaine n’est déclarée dans les historiques effectifs : le nouveau bataillon de canons de campagne aura besoin d’une unité d’artillerie fournie par les mécanismes économiques existants. Les prises et les stocks historiques ne sont pas simulés par cette déclaration. Le ravitaillement est un point explicite du test, sans création d’usine ni de subvention de compensation.

## Guerre d’indépendance et non-régression

L’historique `common/history/diplomatic_plays/00_american_revolution.txt` crée déjà la guerre contre GBR avec `war = yes`, ainsi que ses soutiens et objectifs existants. Le journal `je_usa_independence` et son modificateur militaire sont préservés, y compris leurs bonus préexistants. Le lot ne remanie pas cette diplomatie.

La Grande-Bretagne conserve 51 bataillons réguliers, 10 conscrits et 97 navires dans les formations historiques effectives. Ce sont des totaux mondiaux, pas des forces simultanément déployées devant Boston. Le correctif réduit la puissance nominale américaine et remplace son infanterie par un palier moins performant ; il ne garantit pas une victoire américaine. La cohérence du conflit doit être observée en partie, sans donner de technologie future pour compenser cette correction.

Un seul fichier fonctionnel est modifié : `common/history/military_formations/01_military_formations_north_america.txt`, et uniquement sa définition d’armée américaine. Le contenu avant et après cette définition est conservé exactement, y compris flotte, personnages et autres pays. Les historiques de population, pays, bâtiments, diplomatie, les lois, technologies, définitions d’unités, carte et localisations sont protégés par empreintes. Les papeteries, la fiscalité prussienne, HRE-CENTRALIZATION et les travaux cartographiques ne sont pas écrits par ce lot. HEAD et l’index Git sont inchangés.

Les détails exécutés figurent dans `VALIDATION.json` ; les preuves initiales dans `BASELINE.json`, le plan dans `AUDIT.json` et la modification dans `CHANGES.patch`. Le [guide de validation moteur](RUNTIME_TEST_PLAN.md) est la dernière étape avant toute validation humaine du comportement en jeu.
