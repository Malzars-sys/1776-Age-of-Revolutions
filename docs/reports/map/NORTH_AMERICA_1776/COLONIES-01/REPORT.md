# COLONIES-01 — politique coloniale et frontières de 1776

Travail des 26–27 octobre 2026. **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION** : corrections installées, test moteur et validation joueur à effectuer. Aucun commit, push, merge ou changement du vanilla.

## Résultat

**Treize Colonies :** loi initiale remplacée par `law_no_colonial_affairs` ; investissement initial dans l'institution coloniale retiré. La connaissance technique `colonization` est conservée. Les trois politiques de colonisation sont bloquées à l'adoption **et à l'imposition par une autre puissance** tant que les USA sont sujets, ou tant que leur guerre initiale d'indépendance contre Londres n'est pas terminée. Changer de suzerain ne suffit pas ; une fois indépendants, les choix normaux redeviennent possibles, sans adoption automatique ni date arbitraire. Les autres pays, dont HBC, Québec et Nouvelle-Écosse, ne sont pas soumis à ce verrou.

**Maritimes :** le Nouveau-Brunswick, séparé historiquement en 1784, est réuni à NVS au lancement. **40 provinces**, tous les habitants et toutes les unités sont conservés. Les deux portions sont fusionnées ; casernes 2 + 3 et réseau routier 1 + 2 sont consolidés avec PM, réserves et propriété compatibles, sans supprimer de niveaux. Les deux formations de deux fantassins irréguliers et trois fantassins de ligne subsistent. Un seul lien colonial NVS–GBR. Halifax était déjà le hub urbain correct ; aucune relocalisation inventée. Le TAG NBS reste défini pour des usages futurs, sans possession initiale.

**42 provinces retirées des extensions coloniales excessives :**

| Région | Transferts installés | Part américaine restante |
|---|---|---|
| Géorgie | 20 aux Muscogees, 3 aux Cherokees | 14 |
| New York | 12 aux Haudenosaunee, TAG IRO existant réactivé | 23 |
| Caroline du Nord | 6 aux Cherokees | 26 |
| Caroline du Sud | 1 aux Cherokees | 18 |

Les trois ensembles autochtones sont continus : **CHE 31, MSC 40, IRO 12 provinces** dans leur empreinte totale actuelle. Leurs homelands documentés sont complétés sans retirer les homelands coloniaux encore pertinents dans les parties occupées. Les anciens traités, occupations et marges contestées interdisent de représenter ces seuils comme un cadastre exact : **arbitrages de catégorie B**, explicités dans [SOURCES.md](SOURCES.md).

Savannah, Augusta, les terres cédées de 1773 autour de la future Wilkes County, New York, Albany, Charleston, Ninety Six, New Bern et Wilmington sont préservés. Les hubs administratifs tardifs Atlanta/Raleigh sont remplacés par **Savannah et New Bern**, dans des provinces américaines conservées. Les autres emplois et bâtiments coloniaux restent dans leur portion de State Region.

## Continuité avec le Canada

La chaîne **HBC → Québec, par l'ancien Haut-Canada → Treize Colonies** demeure physiquement continue. Au lieu de conserver artificiellement une bande américaine découpant le territoire haudenosaunee, le contact terminal est déplacé vers un autre bord direct Ontario–New York déjà disponible.

`FRONTIER/UPDATED_LAND_WITNESS.json` contient le nouveau chemin, 305 pixels côte à côte, sans territoire décentralisé ni passage maritime. Les contrôles d'impassabilité sont appliqués. Cette preuve physique ne certifie pas l'accès militaire accordé par le moteur pendant la guerre. **278 provinces et 108 626 habitants HBC ; 323 provinces et 90 000 habitants Québec : inchangés.**

L'ancien témoin HBC-04 est conservé comme preuve de sa version. Les assertions anciennes exigeant son point d'arrivée précis sont désormais dépassées par cette correction de frontière autorisée ; elles ne sont pas réécrites pour fabriquer un succès.

## Population et économie

Variation mondiale d'effectifs : **0** ; chaque identité de cohorte, religion explicite ou implicite et type de POP est conservé. Les colons restent dans les portions coloniales retenues. Les cohortes cherokees et iroquoises déjà présentes passent à leurs autorités restaurées ; une partie des cohortes muscogees est répartie de l'Alabama vers la Géorgie sous le même pays MSC.

Cette répartition est **technique, pas un nouveau recensement**. Le total conservé en Nouvelle-Écosse est 107 019 ; le profil iroquois n'a que 691 habitants dans les données héritées. Ces chiffres ne sont pas certifiés pour 1776. Aucune inflation autochtone du scénario HBC n'a été appliquée ailleurs, aucune culture n'a été convertie pour correspondre au drapeau.

Tous les actifs et unités sont conservés, avec seul changement de propriétaire NBS → NVS pour les actifs de la colonie absorbée. Pas de nouvelle usine, recette ou technologie européenne importée. IRO reçoit un profil agricole explicite, traitement alimentaire traditionnel et lois natives. Les ressources régionales ne sont pas redécoupées ; leur allocation effective entre portions doit être observée en jeu.

## Fichiers et preuves

Les listes exhaustives avec empreintes sont dans `CORE/PATCH.json`, `FRONTIER/PATCH.json` et `CUMULATIVE_VALIDATION.json`. Principaux fichiers :

- Histoires de pays USA, États, POPs, bâtiments et formations nord-américaines ; retrait du seul pacte colonial NBS.
- Nouvelle surcharge `common/laws/01_colonial_affairs.txt` et déclencheur `1776_usa_colonial_expansion.txt` ; localisations FR/EN du verrou et de la Nouvelle-Écosse.
- Définition IRO et nouvelle histoire `1776_haudenosaunee.txt`.
- Seuls hubs urbains Géorgie/Caroline du Nord dans les définitions régionales et le fichier city des locators ; localisations des deux sièges.

Préparation depuis les fichiers courants, empreintes vérifiées avant application, sauvegardes des seuls fichiers touchés. Le regroupement maritime est contrôlé avant la passe frontalière ; les modifications communes sont suivies par une chaîne de provenance et la validation cumulée. Les ajouts du verrou « tout suzerain / guerre non résolue » sont tracés dans les amendements de CORE.

**Contrôles :** 24 vérifications cumulées de livraison, conservation et références réussies, plus 8 tests du verrou couvrant dépendance britannique, changement de suzerain, guerre encore active et indépendance. Les résultats des étapes et le détail technologique sont archivés. IRO : **PASS_STATIC_ONLY**. USA et NVS : **FAIL_STATIC hérités**, distincts des contrôles réussis de cette correction ; notamment le centre de commerce NVS demande `organized_financial_institutions`, déjà absent de son profil avant la fusion. Aucun don global de technologies pour masquer ces dettes.

Cinq fichiers Fezzan ont changé entre les deux étapes par un travail concurrent : ils étaient déjà dans cet état avant la préparation frontalière et sont restés intacts. `CONCURRENT_FILES.json` conserve leurs empreintes ; ils ne sont ni attribués à cette mission ni restaurés.

## Limites de l'audit

Les grandes extensions clairement excessives sont corrigées, **pas chaque frontière autochtone de toute la côte Est homologuée**. Le Maine intérieur, certains secteurs de Pennsylvanie, les postes britanniques isolés de l'ouest de New York, les marges précises des cessions géorgiennes et les occupations militaires de 1776 restent à caler. Les villages de frontière et les actes de 1768/1770/1773 empêchent un simple recul uniforme sur les Appalaches de 1763.

La réunion administrative de la Nouvelle-Écosse ne certifie pas l'occupation de ses forêts ni le détail des juridictions insulaires, dont l'île Saint-Jean. Les populations héritées et les alliances internes des Six Nations nécessitent une étude distincte. Aucun transfert supplémentaire ne repose sur une carte ethnique contemporaine seule.

## Validation joueur

Commencer une **nouvelle partie en 1776**. Vérifier NVS seule sous Londres ; loi sans colonisation des Treize Colonies et infobulle bloquant les trois politiques. Vérifier aussi le refus d'imposition extérieure. Tester la levée du verrou après indépendance effective, son maintien en cas d'échec ou de guerre encore active ; HBC et les autres pays conservent leurs règles habituelles.

Comparer [la carte](FRONTIER/FRONTIERS_1776.png), ouvrir les trois pays autochtones, contrôler les anciens bâtiments et les sièges Savannah/New Bern. Vérifier la liaison canadienne, puis un mois de simulation et sauvegarde/rechargement. Aucun chargement moteur ni reçu humain n'est déclaré par les contrôles statiques.
