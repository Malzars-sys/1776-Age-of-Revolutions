# MAP-2M-R3 — extension continentale appliquée, frontières encore partielles

15 octobre 2026. Situation visée : **1er janvier 1776**.

**Statut : MAP-2M-R3_PARTIAL.** Dix cellules supplémentaires sont effectivement transférées à la Suède. Ce résultat ne termine ni Wolgast–Peenestrom–Peendamm ni les quatre districts de la Netze. Aucun transfert supplémentaire de la Netze n'est suffisamment justifié dans cette passe. Ne pas annoncer l'ensemble prêt ou historiquement achevé.

## Référence R2 acceptée

`R2_USER_RUNTIME_VALIDATION.json` enregistre la confirmation du joueur : **PASS_RUNTIME_USER_VALIDATED pour les modifications R2 inspectées**. C'est une vérification manuelle, pas un test moteur automatisé. Aucune durée de simulation ni aucun journal absent ne sont inventés. Les anciens rapports restent des photographies chronologiques ; leur attente de validation est désormais complétée par cette attestation, pas réécrite rétroactivement.

Les 341 cellules suédoises initiales, les six ajouts R2 et les 85 cellules de Bromberg sont tous conservés. Les réglages économiques les plus récents font partie de la nouvelle référence, notamment Rhône à cinq niveaux d'armes et Canton à dix niveaux de centre de commerce.

## Modifications réellement installées

| Secteur | Avant R3 | Après R3 | Changement |
|---|---|---|---:|
| Intérieur continental entre Greifswald et l'approche occidentale de Wolgast | `xE1A03A`, PRU, STATE_POMERANIA | extension de `x567452`, SWE, même State_ID | 10 cellules |
| Bromberg, STATE_POSEN | `xEDB010` PRU : 85 ; `xFCC7B7` PLC : 142 | strictement identique | 0 |
| Autres portions de la Netze | référence R2 | strictement identique | 0 |

`x567452` passe de **347 à 357 cellules** ; `xE1A03A` de **343 à 333**. Aucun RGB, terrain, pays ou State_ID nouveau. Les couleurs sont des identifiants de provinces bitmap, pas des identifiants historiques de villes.

Les dix coordonnées X/Y et les propriétaires avant/après figurent dans `TERRITORIAL_CHANGES.csv` : X 4399–4404, Y 736–738, cellules sélectionnées individuellement, pas le rectangle complet. Les deux empreintes restent connexes par les quatre côtés. Aucun déplacement de locator.

Fichiers fonctionnels modifiés dans R3 :

- `map_data/provinces.png`
- `common/history/pops/00_west_europe.txt`

Les autres fichiers fonctionnels, y compris les historiques de bâtiments et de formations militaires, restent identiques à la référence R3. Les définitions et propriétaires des deux RGB existaient déjà : les réécrire n'était pas nécessaire.

## Peene : ce qui a débloqué la petite correction

La source politique demeure **Mayer/Lotter 1763 conservée à Greifswald**, confrontée à l'exemplaire BSB catalogué « après 1763 ». La souveraineté suédoise du continent au nord de cette frontière n'est pas déduite de données modernes. Les plans GeoGREIF de 1694 ne sont pas utilisés comme preuve de souveraineté en 1776 ; aucun nouveau homologue de leur pont n'est déclaré validé.

Le nouvel élément est le **service hydrographique officiel LUNG du Mecklembourg-Poméranie** : couche LAWA, route nommée Peene (fid 1518), Trebel (869), Ryck (1654), et polygones côtiers nommés Peenestrom. Contrairement au raster natif des rivières, ces données permettent de lire le cours de la Peene dans la zone considérée. La côte Natural Earth apporte un contrôle de silhouette indépendant du réseau fluvial utilisé dans R2.

Il n'y a **pas de nouvelle optimisation sur les mêmes points**. Le cadre physique R2 est conservé : hypothèse Miller avec décalage rigide [-1 ; +5,9], déjà déterminé au nord de la Vistule. Cinq comparaisons côtières réservées, non utilisées dans cet ajustement, donnent des distances à la silhouette côtière native de 1,044 ; 0,512 ; 1,871 ; 0,544 ; 0,548 pixel. Moyenne **0,904**, maximum **1,871 pixel**.

**Ce ne sont pas cinq centres urbains homologues certifiés, ni un intervalle d'erreur pour Wolgast ou Anklam.** Ce sont des distances à une côte généralisée, avec ambiguïtés de discrétisation. Elles ne certifient pas le modèle global ni les limites politiques. L'ancien désaccord côtier de 5,43 pixels reste un désaccord de l'ancienne lecture, pas une erreur urbaine mesurée.

La sélection retient seulement des cellules :

1. Intérieures aux deux lectures conservées de la carte de Mayer.
2. À au moins 1,5 pixel du contour de la seconde lecture historique.
3. À au moins trois pixels au nord de l'enveloppe physique de la Peene.
4. À au moins trois pixels à l'ouest de l'enveloppe du Peenestrom.
5. Dans une emprise de travail limitée et raccordées au noyau suédois existant.

Ces distances sont des **précautions de sensibilité**, pas des bornes d'erreur statistiquement mesurées. Le contour obtenu est un noyau conservateur de juridiction, pas la frontière fluviale intégralement reconstruite.

La première sélection aurait retenu 28 cellules. Le contrôle détaillé du Peenestrom en rejette **18**, trop proches du chenal/nord d'Usedom. `GEOMETRY_REVIEW.json` conserve cette exclusion. Les dix restantes forment une extension continentale ; aucune cellule à partir de X 4405 dans l'approche orientale ni à partir de Y 739 dans le secteur méridional contrôlé n'est modifiée. Demmin, la majeure partie d'Anklam et les approches d'Usedom/Wollin sont donc préservées. **Le centre de Wolgast n'est pas corrigé par ces dix cellules**, et aucune enclave agrandie de Peendamm n'est fabriquée.

Les courbes modernes servent de contraintes physiques larges, non de restitution des méandres de 1776. La concordance avec la carte historique et la distance aux berges sont examinées conjointement. La côte simplifiée du jeu ne permet pas de restituer proprement tout le chenal dans cette passe.

## Netze : résultats distincts par district

- **Deutsch Krone — Wałcz / Piła** : les deux anciens placements diagnostiques tombent déjà sur des provinces PRU de STATE_POMERANIA (`x0180A0`, et `xCDEAE4` pour l'une des lectures de Wałcz). Cela ne certifie pas les centres ni le district entier, mais ne justifie pas de les retirer à la Prusse. Les raccords ruraux restent ouverts.
- **Kamin** : pas de nouveau raccord physique occidental suffisamment contrôlé pour convertir la juridiction lisible dans les sources en cellules supplémentaires. Aucun nouveau centre pixel n'est inventé.
- **Bromberg / Fordon** : les 85 cellules acceptées et la subdivision PRU de STATE_POSEN restent exactement en place. L'hypothèse physique tombe dans `xEDB010`. Les 142 cellules résiduelles restent polonaises ; elles ne sont pas annexées en bloc à partir du nom d'une ferme.
- **Inowrocław** : l'hypothèse physique tombe dans `xC02121`, STATE_POSEN, PLC. Cette observation signale une zone à reconstruire ; elle n'autorise pas l'annexion de toute cette province. Le prolongement est lisible dans l'encart Homann, mais la date de cet état de planche et son raccord méridional précis restent insuffisamment établis pour le 1er janvier 1776.

`NETZE_POSITION_DIAGNOSTICS.csv` donne les lectures disponibles et leurs RGB actuels, explicitement comme **hypothèses non homologuées**. Les acquisitions de 1793 ne sont pas importées. Thorn `x41A021`, Dantzig `x80A0A0` et Poznań `x999CEE` sont gelées, cellule pour cellule. Gniezno et tout le secteur Netze restent inchangés dans R3.

### Catalogue de Berlin et Schmettau

Le catalogue GStA fourni a été téléchargé et lu. Tit. 50 Nr. 1 a décrit une table de bornage de **1772** ; Nr. 2 concerne des instructions de règlement de frontière de **1777** ; Nr. 10 mentionne Ostroveck/Skotnicki dans l'Amt Kruszwice sur **1776–1780**. Ces notices sont des pistes : **les manuscrits correspondants n'ont pas été consultés**. Elles ne permettent pas de dater précisément un tracé au 1er janvier 1776. Les notices de Thorn restent hors périmètre.

Les pistes Schmettau examinées n'ont pas livré de feuille cible accessible avec une date individuelle suffisante. L'intervalle général **1767–1787** ne vaut pas un état homogène de 1776. Aucun contour tardif n'est importé par défaut.

Grund 1775 conservé reste un extrait Driesen–Landsberg, pas un scan intégral couvrant les quatre districts. Güssefeld/Homann 1775 est réutilisé ; l'encart Homann à datation large n'est pas promu en seconde preuve datée antérieure au 1er janvier 1776. Il manque un raccord occidental/méridional contrôlé et une source datée couvrant la frontière avant les rectifications de 1776–1777. Les secteurs non démontrés sont laissés intacts.

## Démographie, économie et préservation

- Monde avant/après : **835 804 980 habitants**, aucun ajout ni suppression.
- Poméranie : **1 175 personnes PRU → SWE** : 1 043 nord-germaniques avec religion implicite conservée, 107 nord-germaniques catholiques, 20 polonaises, cinq ashkénazes. Tous les autres attributs des profils sont conservés.
- Allocation déterministe par surface de la subdivision source et plus forts restes, convention cartographique de jeu, **pas un recensement historique**.
- Les niveaux entiers de bâtiments restent tous dans leur subdivision d'origine après examen du calcul. Aucun bâtiment ajouté, supprimé ou déplacé ; PM, propriétaires économiques, infrastructures écrites, armées, unités et recrutements conservés.
- Six niveaux d'armes au Brandebourg, cinq au Rhône, dix de centre de commerce et cinq de port à Canton conservés. Tous les autres réglages économiques et la conversion chinoise en lanciers sont protégés par comparaison intégrale des fichiers fonctionnels et des inventaires.
- Registre impérial inchangé : extension spatiale d'un RGB déjà enregistré, aucun nouvel enregistrement de territoire Netze dans l'Empire. Belgique, Franconie, Rhin–Westphalie, Souabe et Erfurt–Eichsfeld inchangés.

Bilan par profil : `PEENE_POPULATION_VALIDATION.csv` et `NETZE_POPULATION_VALIDATION.csv`. Le second constate un delta nul, pas une redistribution fictive.

## Validations

`tools/map2m_r3.py validate` : **49/49 contrôles statiques réussis**. Comparaison exacte du raster avec la liste des dix cellules ; connexité ; couleurs et State_ID ; propriétaires uniques des RGB touchés ; références existantes ; inventaires démographiques, économiques et militaires ; tous les autres fichiers fonctionnels ; empreintes des anciens rapports ; HEAD et index Git.

`tools/map2m_r3.py tests` : **62/62 tests réussis**, dont six nouveaux tests R3, dix R2, quatre R1, dix-huit du registre, huit des attestations manuelles, huit de disposition des PM et huit des réglages économiques. `TESTS.json` conserve la sortie réelle. Ces tests ne lancent pas Victoria 3.

Les **44 doublons RGB et 12 références invalides hérités** sont inchangés et restent ouverts. Aucune ancienne baseline n'est modifiée pour masquer un écart. Les stricts contrôles de l'ancien bitmap R2 ne sont pas réécrits : R3 utilise une nouvelle comparaison différentielle limitée.

**Aucun test moteur R3 effectué.** Il faut une nouvelle partie et un mois de simulation pour vérifier les nouveaux transferts, l'accès au marché, la population et l'absence d'erreur nouvelle. Cette validation ne certifiera pas pour autant toute la frontière historique.

## Comparatifs, sources et reproductibilité

- `PEENE_BEFORE_AFTER.png` et `NETZE_BEFORE_AFTER.png` : référence R2 / état R3 réel ; contours turquoise = cellules R2 acceptées, rouge = dix ajouts R3, cadres violets = emprises indicatives encore ouvertes, non des frontières revendiquées.
- `PEENE_PHYSICAL_READING.png` : côte Natural Earth en vert, routes fluviales officielles en bleu, Peenestrom détaillé en violet. Points de villes rouges : cibles diagnostiques, pas contrôles certifiés.
- `SOURCES.json` : URL, empreintes, tailles, couches, plafonds de réponses WFS, licences et limites documentaires. L'attribution LUNG et la mention CC BY-SA annoncée sont conservées ; examiner la version et les modalités avant toute republication externe. Les scans GeoGREIF restreints ne sont ni republiés ni dérivés dans les comparatifs livrés.
- `BASELINE.json` immuable référence le bitmap R2 déjà conservé ; aucune archive complète volumineuse nouvelle. `PLAN.json`, `ORIGINAL_TEXT.json`, `EXPECTED_TEXT.json`, `HISTORY.patch` et le bitmap candidat permettent de vérifier les deltas et la redistribution.

Reproduction sans téléchargement : lancer `physical`, `geometry`, `evidence`, `validate` et `tests` sur `tools/map2m_r3.py`. `prepare` exige l'état original capturé ; `install-raster` refuse d'écraser un bitmap différent. Ne pas contourner ces gardes pour rejouer une préparation sur un workspace déjà modifié. Les écritures textuelles ont été appliquées par patch ; le PNG installé est exactement le candidat contrôlé.

Références principales : [Mayer, Greifswald](https://www.uni-greifswald.de/universitaet/einrichtungen/kustodie/wissenschaftliche-sammlungen/sammlungsobjekt-des-quartals/geographische-kartensammlung-die-mayersche-karte/), [LUNG WFS](https://umweltkarten.lung-mv.de/dienste/wg_gewaesser?SERVICE=WFS&REQUEST=GetCapabilities), [Natural Earth coastline](https://github.com/nvkelso/natural-earth-vector/blob/master/geojson/ne_10m_coastline.geojson), [GStA, catalogue des frontières](https://archivdatenbank.gsta.spk-berlin.de/midosasearch-gsta/MidosaSEARCH/ii_ha_gd_abt_9/xml/inhalt/GStA_ii_ha_gd_abt_9_2_42.htm), [Grund 1775, notice de Berlin](https://kartenhighlights.staatsbibliothek-berlin.de/portfolio-item/grund-karte-der-neuen-provinz-westpreussen-1222-000-1775/).

## ColGrep et Git

**Un appel ColGrep-Agent-2B tenté, environ 1,02 seconde, échec d'accès au dépôt avant exécution confirmée du modèle.** Aucun résultat local inventé, aucun changement de modèle, index ou intégration. Repli sur les fichiers connus, recherches exactes et scripts conservés. Compteurs de tokens par tâche et comptage fiable des recherches classiques indisponibles ; aucune économie de quota mesurée ou revendiquée. La commande et l'échec sont enregistrés dans `COLGREP.json`.

HEAD reste `f34a6b88db749a8be77ec558fd55ad196b45f72a` ; empreinte de l'index inchangée. Aucun commit, merge, push, reset, changement de branche ou écriture d'index.

## Vérification demandée au joueur

1. Nouvelle partie : vérifier l'extension de dix cellules au sud-est du noyau suédois, sans s'attendre encore à un Wolgast ou Peendamm achevé.
2. Vérifier que Demmin, Anklam, Usedom et Wollin restent du côté prussien dans les zones non modifiées ; les incertitudes du Peenestrom restent signalées.
3. Vérifier les subdivisions PRU/SWE de Poméranie après transfert de population et laisser passer un mois.
4. Confirmer que Bromberg R2, ses 142 cellules polonaises résiduelles, Thorn, Dantzig, Poznań, les bâtiments et les centres de commerce ne changent pas.

Le test peut accepter les **seuls dix ajouts R3**. Les lignes de `UNRESOLVED.csv` restent à traiter dans une passe explicitement documentée ; ne pas les fermer par la seule réussite du chargement.
