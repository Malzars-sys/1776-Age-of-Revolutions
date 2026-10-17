# MAP-2M — Peene et Netze : livraison partielle, 15 octobre 2026

**Statut : MAP-2M_PARTIAL. Aucun transfert territorial nouveau appliqué.** Les conditions de clôture historique et géométrique ne sont remplies pour aucun des deux secteurs. Les contrôles de préservation réussis ne doivent pas être présentés comme la validation d'une frontière encore non résolue.

**Continuation R1 :** voir [le rapport de recherche et le correctif des centres de commerce](R1/REPORT.md). Deux plans cadastraux et l'encart Homann ont été retrouvés ; les frontières restent inchangées. R1 autorise séparément un seul changement fonctionnel, la disposition des PM de centres de commerce, contrôlé avec une exception GUI explicite plutôt qu'en réécrivant les baselines de cette livraison initiale. Aucun nouveau test moteur déclaré.

## Référence conservée

Les 341 cellules de `x567452`, `STATE_POMERANIA`, restent suédoises. Le test manuel annoncé par le joueur — sept points, nouvelle partie et un mois de simulation — est enregistré dans `../MAP2L/RUNTIME_USER_VALIDATION_PRUSSIAN_CORE.json`. Ce n'est pas un test moteur automatisé, et il ne s'étend pas aux propositions MAP-2M.

Les six niveaux d'armes au Brandebourg sont conservés. Le bitmap, les propriétaires, populations, cultures, religions, bâtiments, PM, propriétaires économiques, infrastructures, pays, gouvernements, formations et recrutements restent identiques à la référence acceptée. Aucun nouveau RGB n'est créé. Aucun commit, merge, reset, changement d'index ou push.

## A — Peene : non terminé

L'audit retrouve les provinces mixtes actuelles `xE1A03A` et `xA04121`, toutes deux prussiennes dans `STATE_POMERANIA`. Le noyau suédois acquis `x567452` est exclu des propositions.

Source prioritaire réutilisée : Mayer/Lotter, 1763, exemplaire de Greifswald conservé dans MAP-2L. Une copie plus lisible a été retrouvée à la Bayerische Staatsbibliothek ; **sa notice dit « nach 1763 »**, et non une date certaine de 1763. Elle sert à lire les lieux et comparer les contours, pas à remplacer subrepticement la source datée.

La Peene de Demmin à Anklam et le Peenestrom sont lisibles sur la carte ancienne. En revanche, ils ne sont pas dessinés dans l'hydrographie native examinée. Le calage hypothétique Darss–Greifswald–embouchure ne dispose pas de contrôles physiques homologues vérifiés au sud du triangle, là où se situe la frontière à transférer. Son contrôle côtier supplémentaire à Rügen diverge d'environ **5,43 pixels**. Ce nombre est un désaccord avec une lecture manuelle du littoral, **pas une erreur géodésique certifiée** et pas une marge de confiance.

Le modèle produit **79 cellules candidates**, explicitement **non approuvées et non appliquées**. Le résidu nul des trois points d'ajustement n'est pas une preuve d'exactitude. Wolgast et surtout Peendamm ne peuvent pas être attribués au bon pixel par simple déduction à partir de ce calage. Demmin, la partie prussienne d'Anklam, Usedom et Wollin ne sont pas transférés.

À obtenir pour terminer : au moins un raccord côtier/lagunaire sûr au Peenestrom et des repères homologues au sud du triangle, puis un contrôle indépendant proche de Demmin–Anklam. Il faut aussi décider à partir de la source où passe la distinction Anklam/Peendamm à l'échelle du jeu ; aucune cellule n'est agrandie ou déplacée arbitrairement pour la forcer.

Résultats séparés : `PEENE/REPORT.md`, `PEENE/VALIDATION.json`, `PEENE/CANDIDATE_CELLS.csv`, `PEENE/BEFORE_AFTER.png`.

## B — Netze : non terminé

La carte de **Grund, 1775, Kart. N 10051**, a été retrouvée à Berlin. L'image publique est seulement un **extrait Driesen–Landsberg** ; la notice précise **nord en bas**. La notice liée ne fournit pas de numérisation intégrale directement accessible : le lien de commande de reproduction n'a pas été utilisé et aucune demande externe n'a été envoyée. L'extrait ne couvre ni l'ensemble des quatre districts ni le sud d'Inowrocław.

Une carte complète des Prusses de **Güssefeld/Homann, cataloguée en 1775**, a été obtenue dans la collection Ryhiner. Elle constitue un recoupement antérieur à 1776, mais le contour provincial de Prusse-Occidentale ne doit pas être assimilé automatiquement à toutes les possessions de la monarchie prussienne, et la portion méridionale nécessaire pour le district d'Inowrocław n'est pas entièrement justifiée par l'enveloppe examinée.

Le calage provisoire sur les locators orientaux Dantzig–Bromberg–Thorn n'est pas validé vers l'ouest. Les positions calculées de Piła et Wałcz divergent de **9,50 et 12,17 pixels** d'une autre hypothèse géographique locale. Il s'agit de **désaccords entre modèles non validés**, pas de mesures d'erreur sur des centres urbains certifiés. À Piła, les hypothèses tombent même dans des provinces de propriétaires différents : ce n'est donc pas une petite différence sans effet politique.

Une enveloppe exploratoire produit **162 cellules candidates non approuvées et non appliquées**. Elle ne constitue pas le tracé complet de Deutsch Krone, Kamin, Bromberg et Inowrocław. La carte de Toeppen (1858, représentant 1772) est conservée, mais aucun transfert n'est fondé sur elle sans recoupement antérieur suffisant. Les accès tentés à Utz 1773 via RCIN et Gallica ont renvoyé respectivement une vérification de navigateur et HTTP 403 ; aucune restriction n'a été contournée.

L'anomalie de Bromberg reste donc ouverte : le locator natif nommé Bromberg est dans la province polonaise `xFCC7B7`, `STATE_POSEN`. La propriété prussienne historique de la ville est établie par les points de contrôle fournis ; ce qui manque est la correspondance fiable avec les cellules et la limite territoriale, pas la reconnaissance de la souveraineté historique. La propriété actuelle de Piła et d'Inowrocław ne peut pas être déclarée corrigée.

Dantzig (`x80A0A0`) reste polonaise. La province `x41A021` contenant le locator nommé Thorn reste dans son état antérieur prussien : **cette anomalie connue n'est pas corrigée dans MAP-2M**, conformément au gel de l'enclave pour le bloc suivant. Aucun territoire de Poznań ou Gniezno n'est annexé.

À obtenir pour terminer : le scan intégral de Grund 1775, ou une autre carte pré-1776 couvrant clairement les quatre districts et les limites méridionales, ainsi qu'un calage occidental indépendant fondé sur des repères identifiables dans le bitmap. Une simple position de ferme ou le nom d'une ville ne suffit pas.

Résultats séparés : `NETZE/REPORT.md`, `NETZE/VALIDATION.json`, `NETZE/CANDIDATE_CELLS.csv`, `NETZE/BEFORE_AFTER.png`.

## Contrôles et fichiers

`VALIDATION.json` sépare `static_preservation` des critères `geometry_complete` et `historical_attribution_complete`, qui restent faux. Chaque secteur possède sa propre baseline, sa validation et son bilan démographique. Les CSV de transferts sont vides, avec en-têtes ; les CSV de candidats ne doivent pas être importés dans l'historique. Les images comparent référence, hypothèse violette non appliquée et état effectif inchangé.

Les 44 doublons RGB et 12 références invalides hérités sont conservés séparément. Le validateur existant du premier correctif prussien est relancé ; ses résultats restent ceux d'une préservation de la référence et non d'un achèvement MAP-2M. Le joueur n'a pas de nouveau découpage MAP-2M installé à tester à ce stade.

Fichiers créés ou mis à jour : le présent dossier de preuves, les outils `tools/map2m_border_work.py` et `tools/validate_map2m_borders.py`, l'attestation manuelle MAP-2L, son gestionnaire et ses tests, le rapport validé du premier correctif et l'état de clôture documentaire. **Aucun fichier fonctionnel du mod n'est modifié.**

## Résultats techniques finaux

- Préservation MAP-2M : **26/26 contrôles réussis**, avec zéro cellule appliquée et zéro nouveau RGB.
- Réexécution du premier correctif prussien : **377/377 contrôles statiques réussis**. Ce résultat ne certifie pas les frontières candidates de MAP-2M.
- Tests des outils MAP-2L et des attestations : **31/31 réussis**.
- Population mondiale conservée : **835 804 980**. Les 341 cellules suédoises et les six niveaux d'armement du Brandebourg sont intacts.
- Aucun nouveau test moteur effectué. Les deux critères d'achèvement géométrique et historique restent faux ; la livraison reste **MAP-2M_PARTIAL**.

## Sources conservées

- [Mayer 1763, Université de Greifswald](https://www.uni-greifswald.de/universitaet/einrichtungen/kustodie/wissenschaftliche-sammlungen/sammlungsobjekt-des-quartals/geographische-kartensammlung-die-mayersche-karte/) : source prioritaire Peene.
- [Mayer, exemplaire BSB](https://www.digitale-sammlungen.de/de/view/bsb00074494?page=,1) : datation de notice « après 1763 », image de lecture complémentaire.
- [Grund 1775, notice de Berlin](https://kartenhighlights.staatsbibliothek-berlin.de/portfolio-item/grund-karte-der-neuen-provinz-westpreussen-1222-000-1775/) : extrait public seulement ; nord en bas dans la notice de catalogue liée.
- [Güssefeld/Homann 1775, Ryhiner](https://ryhiner.ub.unibe.ch/en/world/location/53/image/2828), [notice pérenne](https://doi.org/10.3931/e-rara-127582) : image complète conservée, distincte d'une certification du contour intégral de la Netze.

Les images et empreintes sont dans `EVIDENCE/SOURCES.json` et les deux `CANDIDATE_MODEL.json`. Aucun index ColGrep reconstruit : un appel au modèle local a retourné trois pistes déjà connues, vérifiées mais sans nouveau calage. Aucun gain exact de quota n'est prétendu.
