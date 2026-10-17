# MAP-2M-R2 — corrections installées, périmètre partiel

15 octobre 2026 — situation historique visée : 1er janvier 1776.

**Statut : MAP-2M_PARTIAL.** Deux corrections fonctionnelles sont installées. Elles ne constituent pas l'achèvement de la frontière de la Peene ni des quatre districts de la Netze. Validation statique réussie ; aucun lancement du moteur. Nouvelle partie et mois de simulation à effectuer par le joueur.

## Avant / après effectif

| Secteur | Ancien RGB / propriétaire | Après | Cellules transférées |
|---|---|---|---:|
| Approche continentale occidentale de la Peene | `xE1A03A`, PRU | extension de `x567452`, SWE | 6 |
| Intérieur du secteur de Bromberg | `xFCC7B7`, PLC | nouvelle province `xEDB010`, PRU, `STATE_POSEN` (ID 160 existant) | 85 |

**91 cellules effectivement modifiées.** Le noyau suédois initial de 341 cellules reste intégralement présent, sans recoloration : son RGB en compte maintenant 347. `xE1A03A` conserve 343 de ses 349 cellules sous la Prusse. Aucun nouveau RGB n'est nécessaire pour cette extension contiguë.

La province polonaise de Bromberg était trop grande pour être transférée entièrement : **142 de ses 227 cellules restent polonaises**. Le nouveau RGB, vérifié libre dans le raster, les définitions et les terrains, couvre seulement 85 cellules. Il hérite du terrain `plains`. Le locator de ferme nommé Bromberg reste à **X 4507,717 ; Y 767,086** : il n'est pas déplacé pour faire réussir la correction. Son champ `farm` est réaffecté au nouveau RGB contenant sa position.

Cartes : [Peene avant/après](PEENE_BEFORE_AFTER.png), [Netze avant/après](NETZE_BEFORE_AFTER.png). Rouge : cellules modifiées ; bleu : Prusse ; jaune : Suède ; rose : Pologne. Les images proviennent des rasters réels avant/après, pas de l'ancien masque hypothétique. Coordonnées et attributions exactes : `TERRITORIAL_CHANGES.csv`.

## Sources et décision géographique

### Peene

Réemploi de **Mayer/Lotter 1763, Greifswald**, et de la lecture complémentaire BSB dont la notice dit « après 1763 ». Les plans **GeoGREIF C III a 1 / C III a 2, 1694** servent à reconnaître le pont et le lit de la Peene, pas à attribuer la souveraineté de 1776. Aucun homologue du pont ou du méandre n'a été retrouvé dans le raster natif : aucun point cadastral nouveau n'est déclaré validé.

L'ancienne transformation n'est pas appliquée directement. Une seconde lecture utilise trois repères côtiers manuels : cap du Darss, extrémité nord de Rügen, raccord côtier au nord d'Usedom. Les coordonnées et deux matrices sont conservées dans `GEOMETRY_REVIEW.json`. Ce sont des lectures à l'échelle du jeu, pas des relevés géodésiques certifiés.

La sélection retient uniquement l'intersection intérieure des deux lectures, avec retrait de deux pixels par rapport à leurs contours hypothétiques. Ce retrait est une **précaution de sensibilité**, pas une erreur de calibration mesurée. Toute la partie orientale à partir de X 4404 est laissée intacte pour éviter la confusion entre continent et nord d'Usedom. Cette limite de travail n'est **pas présentée comme le tracé de la Peene**. Après cette exclusion et le contrôle de contiguïté avec le noyau existant, seules six cellules restent retenues.

L'attribution de cette petite extension continentale à la Suède est une approximation conservatrice de la juridiction visible sur Mayer, loin d'une reconstruction cadastrale complète. `xA04121`, Demmin, la majeure partie d'Anklam, Usedom et Wollin ne sont pas transférés. **Wolgast, le Peenestrom et Peendamm restent à résoudre** ; leur souveraineté historique n'est pas assimilée à une correspondance pixel déjà prouvée.

### Netze

Source politique principale : **Güssefeld/Homann, carte cataloguée en 1775**, conservée dans `../EVIDENCE/GUESSEFELD_1775.jpg`. L'extrait **Grund 1775** est conservé mais ne couvre pas Bromberg et n'est pas invoqué comme sa preuve directe. L'encart Homann retrouvé dans R1 confirme la lecture administrative du secteur, sans être promu en source datée avec certitude avant 1776. Aucun contour de 1793 ou 1815 n'est importé.

Un diagnostic physique nouveau confronte la Vistule de **Natural Earth 1:10m déjà conservée** au raster natif. Seul un décalage rigide de l'hypothèse Miller est ajusté sur le tronçon au nord de 53,30° N. La bande 53,00–53,30° N, couvrant le secteur de Bromberg/Fordon, est exclue avant ajustement : **19 sommets, distance moyenne au tracé 1,138 pixel, maximum 2,661 pixels**. Ce sont des distances à une rivière généralisée et des observations corrélées, **pas des erreurs de localisation certifiées de 19 villes ou repères homologues indépendants**. L'Oder, tenu à l'écart, donne moyenne 2,158 et maximum 12,100 pixels : ce diagnostic ne justifie donc pas une extrapolation précise à l'ensemble de la Poméranie ou de la Netze.

Le second placement de la carte ancienne utilise les coordonnées géographiques arrondies de Dantzig, Bromberg et Thorn projetées dans ce cadre physique, plutôt que leurs seules fermes natives. Les coordonnées de localités ne sont pas des frontières. Les 85 cellules retenues sont dans l'intérieur commun de cette lecture et de la précédente, avec une précaution d'un pixel autour des contours. La juridiction datée du secteur, son contexte à l'ouest de la Vistule, la concordance du cadre physique et les positions de Bromberg sont examinés conjointement. **La présence de la ferme n'est pas utilisée pour transférer toute la province**.

Cette correction installe un noyau prussien de Bromberg, avec une limite conservatrice de travail, **pas le contour certifié du district complet**. Les trois autres districts et les franges de Bromberg ne sont pas déclarés reconstruits. Thorn `x41A021` et Dantzig `x80A0A0` restent strictement inchangés ; Poznań reste polonaise.

## Démographie et économie

- Monde avant/après : **835 804 980** habitants, sans ajout.
- Répartition déterministe par surface de la subdivision source, avec méthode des plus forts restes déjà utilisée par MAP-2L : **705 personnes PRU → SWE en Poméranie**, **32 111 personnes PLC → PRU dans STATE_POSEN**.
- Cultures, religions effectives, types de population et tous les autres attributs des profils conservés. Cette allocation est une convention de jeu, pas un recensement historique de Bromberg ou d'une bande côtière.
- Aucun bâtiment ou niveau ajouté, supprimé ou déplacé dans cette passe. Le calcul entier conserve chaque petit niveau dans sa subdivision source ; méthodes, réserves, propriétés économiques et infrastructures écrites restent identiques.
- Pays, capitales, gouvernements, unités et recrutements inchangés. Les six niveaux d'armes du Brandebourg et les corrections économiques récentes, y compris les cantons chinois, sont préservés.
- Les lignes du registre impérial restent identiques : extension spatiale d'un RGB déjà suédois enregistré ; **la nouvelle portion de STATE_POSEN n'est pas ajoutée aux territoires impériaux de jure**. Les mécanismes et fichiers graphiques impériaux ne sont pas réécrits.

## Fichiers fonctionnels modifiés

1. `map_data/provinces.png`
2. `map_data/province_terrains.txt`
3. `map_data/state_regions/02_east_europe.txt`
4. `common/history/states/00_states.txt`
5. `common/history/pops/00_west_europe.txt`
6. `common/history/pops/02_east_europe.txt`

Les cinq textes sont conservés avant/après dans `ORIGINAL_TEXT.json` / `EXPECTED_TEXT.json`. `BASELINE.json` photographie l'état sale du workspace **après les corrections économiques autorisées précédemment**, sans remplacer les baselines MAP-2M/R1. Le bitmap antérieur accepté est référencé par empreinte ; aucune archive complète volumineuse n'est créée.

## Contrôles

`tools/map2m_r2.py validate` : **52/52 contrôles réussis**. Comparaison exacte de toutes les cellules, des inventaires effectifs et des empreintes des autres fichiers fonctionnels. Un seul RGB ajouté, présence dans une seule région, propriétaire unique, terrain valide et composantes connexes contrôlées ; anciens RGB conservés, aucun nouvel orphelin ou doublon. Les **44 doublons RGB et 12 références invalides hérités** restent inchangés et ouverts.

Les contrôles de source du validateur prussien antérieur ont été exécutés sans écrire ses rapports. Onze passent ; trois hypothèses anciennes sont maintenant volontairement obsolètes : raster strictement identique, noyau strictement limité à 341 cellules et aucun autre fichier de région modifié. Les écarts sont détaillés dans `LEGACY_SOURCE_CHECKS.json`, et remplacés par les contrôles différentiels précis de R2, pas par une réécriture de l'ancienne référence.

Le contrôle d'espaces Git signale aussi des lignes blanches indentées préexistantes dans les modifications locales antérieures. Les lignes introduites par R2 ont été nettoyées séparément ; les lignes des autres lots sont conservées. L'avertissement Git LF/CRLF du fichier de régions dépend du réglage existant et n'est pas une erreur de syntaxe de carte.

Les **56/56 tests d'outils réussis** sont conservés séparément dans `TESTS.json` : 10 tests R2, 4 tests négatifs R1, 18 du registre, 8 des attestations manuelles, 8 de disposition des centres de commerce et 8 des réglages économiques. La disposition des centres de commerce a été déclarée vérifiée et acceptée par le joueur dans la demande R2 : cette validation manuelle antérieure est enregistrée séparément du présent travail cartographique dans `USER_VALIDATION_SCOPE.json`. **Aucun test moteur automatisé et aucun PASS_RUNTIME_USER_VALIDATED attribué à R2.**

HEAD et index Git inchangés. Aucun commit, merge, reset, push ou changement de branche.

## Contrôle demandé en nouvelle partie

1. Vérifier les petites extensions contiguës au sud du noyau suédois ; Rügen et Greifswald conservées, aucune acquisition d'Usedom.
2. Vérifier Bromberg du côté prussien dans STATE_POSEN et les 142 cellules restantes de `xFCC7B7` du côté polonais ; ferme et infobulles accessibles sans déplacement du locator.
3. Vérifier la nouvelle subdivision prussienne : population, subsistances, accès au marché, infrastructure et absence de référence cassée. Aucun nouveau bâtiment artificiel n'a été injecté pour lui fabriquer une économie.
4. Confirmer Thorn inchangée, Dantzig et Poznań polonaises, six niveaux d'armes au Brandebourg et interface des centres de commerce inchangée.
5. Laisser passer un mois et relever crashs ou erreurs nouvelles. Ce test ne clôturera pas à lui seul les frontières historiques encore ouvertes.

`UNRESOLVED.csv` détaille les secteurs non terminés. **Ne pas annoncer MAP-2M_READY_FOR_RUNTIME_VALIDATION pour l'ensemble du périmètre.**

## Références et délégation

Sources locales et empreintes : références originales `../EVIDENCE/SOURCES.json`, `../R1/SOURCES.json`, Mayer `../../MAP2L/PRUSSIAN_BORDERS/MAYER_SOURCE.json`. Les scans GeoGREIF restent réservés à la recherche locale ; aucune publication de scan ou dérivé n'a été effectuée.

- [Mayer, collection Greifswald](https://www.uni-greifswald.de/universitaet/einrichtungen/kustodie/wissenschaftliche-sammlungen/sammlungsobjekt-des-quartals/geographische-kartensammlung-die-mayersche-karte/)
- [Grund 1775, notice de Berlin et extrait](https://kartenhighlights.staatsbibliothek-berlin.de/portfolio-item/grund-karte-der-neuen-provinz-westpreussen-1222-000-1775/)
- [Güssefeld/Homann, image institutionnelle conservée](https://www.e-rara.ch/i3f/v30/29730664/full/4000,/0/default.jpg)
- [Homann, exemplaire de Berne à datation non résolue](https://ryhiner.ub.unibe.ch/de/world/volume/17/image/14614)
- [Coordonnées de Bydgoszcz, GeoNames](https://www.geonames.org/3102014/bydgoszcz.html) : contrôle des coordonnées arrondies, pas preuve de souveraineté.

ColGrep : **un appel tenté, échec d'accès au dépôt** avant résultat exploitable (environ 0,93 seconde). Aucun lancement réussi du modèle 2B confirmé. Repli sur recherches exactes et scripts existants, sans modification de l'index ColGrep ni de l'intégration. Compteur de tokens par tâche inaccessible ; aucune économie chiffrée revendiquée.
