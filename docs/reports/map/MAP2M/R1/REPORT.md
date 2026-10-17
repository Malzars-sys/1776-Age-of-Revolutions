# MAP-2M-R1 — Recherche de recalage et correctif des centres de commerce

Date : 15 octobre 2026. Référence historique : 1er janvier 1776.

**Cartographie : MAP-2M_PARTIAL. Aucun transfert, aucun nouveau RGB.** Cette passe de recherche retrouve de nouvelles images exploitables mais ne valide pas une nouvelle transformation source→jeu. **Interface : correctif installé, contrôlé statiquement, non vérifié dans le moteur.**

## Résultats concrets

- Deux scans cadastraux d'Anklam de **1694**, C III a 1 et C III a 2, sont conservés pour recherche locale. Le pont, les bras et méandres de la Peene sont lisibles.
- La planche Homann avec l'encart **Charte welche den Netz District vorstellet** a été retrouvée et téléchargée à Berne : les quatre districts et le prolongement méridional d'Inowrocław sont lisibles. Cela lève le problème de lisibilité/couverture de cet encart, **pas celui de sa date exacte ni de son calage dans le jeu**.
- La notice de Kórnik précise **1793** pour l'exemplaire de l'atlas, malgré **A.1752 dans le titre**. Sa planche 25 contient le titre et l'encart recherchés. Aucune de ces deux dates n'est présentée comme la date certaine de conception ou d'impression de la planche Netze.
- Aucun scan intégral de Grund 1775 nouvellement accessible n'a été identifié. L'extrait Driesen–Landsberg déjà conservé reste distinct de la carte complète ; aucune commande payante, demande de reproduction ou sollicitation externe n'a été envoyée.

## Peene

Voir [le rapport du secteur](PEENE/REPORT.md), `PEENE/HOMOLOGUES.csv`, `PEENE/CALIBRATION.json`, `PEENE/CELL_CLASSIFICATION.csv` et `PEENE/COMPARISON.png`.

Les plans de 1694 sont utilisés pour la **géographie physique seulement**, et non pour reporter la souveraineté suédoise antérieure au traité de 1720 sur 1776. Le pont d'Anklam et le méandre représenté sur la seconde feuille n'ont pas de correspondants indépendamment identifiés dans le raster hydrographique natif examiné. Le couple Peene/Trebel près de Demmin n'y fournit pas non plus une confluence homologue vérifiable. Les feuilles cadastrales locales ne remplacent pas un contrôle côtier au Peenestrom.

Zéro nouveau repère source→jeu accepté, zéro contrôle indépendant nouveau : une moyenne et un maximum d'erreur indépendante **ne sont pas calculables**. Aucun nouvel ajustement sur les anciens points n'a été lancé. Le désaccord côtier précédent de 5,43 pixels est conservé comme diagnostic manuel ancien, pas comme une précision locale mesurée à Anklam.

Les **79 cellules initiales** sont toutes classées **incertaines**, non appliquées ; aucune sous-partie certaine n'est inventée. Anklam/Peendamm reste non résolu à la résolution du bitmap.

## Netze

Voir [le rapport du secteur](NETZE/REPORT.md), `NETZE/HOMOLOGUES.csv`, `NETZE/CALIBRATION.json`, `NETZE/CELL_CLASSIFICATION.csv` et `NETZE/COMPARISON.png`.

L'encart Homann offre des informations supplémentaires sur les districts et les confluences absentes de la lecture précédente. Sa composition est différente de l'enveloppe provinciale Güssefeld/Homann 1775. **Différence de dessin et même éditeur ne permettent ni d'affirmer ni de rejeter une indépendance de levé** : sa filiation géodésique n'est pas établie. Ce n'est pas automatiquement une seconde mesure indépendante.

La notice bernoise donne seulement **[nach 1730]**, incompatible avec une datation précise de cette version représentant les acquisitions de 1772. Le sujet implique une conception de cet état après ces acquisitions, mais ne prouve pas que l'exemplaire a été imprimé avant 1776. Aucune date certaine de 1772/1773 n'est déduite des annonces commerciales. Kórnik 1793 ne fournit pas ce terminus antérieur manquant.

Les symboles de Wałcz, Piła, Bromberg et Inowrocław sont relevés en coordonnées **du scan**. Ils ne sont pas assimilés à des centres certifiés du jeu. Le raccord Gwda–Noteć près d'Ujście n'a pas de branche homologue identifiable dans l'hydrographie native examinée ; le coude de la Vistule vers Fordon est trop général pour choisir le pixel exact et fournir seul un calage occidental ou méridional.

Zéro nouveau repère accepté et zéro contrôle indépendant : pas de nouvelle erreur moyenne/maximale chiffrable. Les 9,50 et 12,17 pixels précédents restent des divergences entre hypothèses non validées, non des erreurs de centres urbains mesurées. Les **162 cellules initiales** restent incertaines et non appliquées. Aucun masque supplémentaire de variation entre transformations prétendument plausibles n'est fabriqué : aucune nouvelle transformation suffisamment fondée n'a été acceptée.

## Correctif d'interface demandé

Fichier fonctionnel modifié : **`gui/building_details_panel.gui` uniquement**.

Cause : le composant compact positionne les icônes import/export à X=150, alors que la fiche détaillée affiche trois PMGs espacés de 72 pixels et larges de 70. Le troisième commence à X=144 et chevauche les biens échangés.

Correction limitée aux centres de commerce dans la fiche détaillée : retour à la ligne après **deux PMGs**, réservation d'une hauteur de **150 pixels** pour les deux rangées. Le PM de données organisées, troisième groupe actuel, passe donc en deuxième ligne. Les deux premiers boutons s'arrêtent à X=142, avant les biens à X=150. Les boutons et infobulles existants sont conservés. Les autres bâtiments et les modèles partagés des listes ne sont pas modifiés. `UI_FIX.json` fige les empreintes avant/après ; `building_details_panel.before.gui` conserve l'original local.

Il s'agit d'une vérification de structure et de géométrie déclarée, **pas d'un rendu du moteur**. En jeu : ouvrir un centre de commerce important, vérifier les trois PM, les survols, le changement de PM, les biens importés/exportés, les barres d'emploi/réserves et le bloc Marché mondial ; comparer aussi une usine ordinaire. Vérifier les échelles d'interface utilisées par le joueur. Aucune nouvelle partie n'est nécessaire pour tester une simple modification de disposition après son chargement par le jeu.

## Préservation et validations

`tools/validate_map2m_r1.py` compare l'ensemble des fichiers fonctionnels avec la référence immuable, **avec une seule exception explicite : l'empreinte précise du correctif GUI**. Il ne réécrit pas les anciennes baselines pour masquer ce changement intentionnel. Le validateur MAP-2M original reste un contrôle strict de son ancienne référence sans exception d'interface ; la validation de continuation est celle de R1.

- **24/24 contrôles de continuation réussis** : inventaire intégral conservé, bitmap, registre, candidats initiaux, HEAD/index, sources, empreinte immuable du correctif GUI et absence de fausse clôture.
- **8/8 tests statiques de disposition** : structure, visibilité complémentaire, ordre des PMGs, retour à la ligne, espace réservé, non-chevauchement géométrique, modèles partagés inchangés et limites du changement.
- **4/4 tests négatifs** de l'exception GUI : elle ne masque pas un autre changement, un ajout/suppression de fichier ou une nouvelle modification de cette même interface. Les **31/31 tests existants des outils MAP-2L** passent également, soit **43 tests d'outils** au total avec les huit tests de disposition.
- Les **341 cellules suédoises** restent intactes ; les six niveaux d'armes au Brandebourg ne changent pas. Population mondiale : **835 804 980**, sans ajout.
- Les **44 doublons RGB et 12 références invalides préexistants** restent signalés, non corrigés ou requalifiés.
- Aucun transfert de Thorn, aucun changement politique, économique, militaire ou démographique ; aucun commit, merge, reset, push ni modification de l'index Git.

Les comptes finaux exécutés figurent dans `VALIDATION.json`. Aucun test moteur nouveau, aucun `PASS_RUNTIME_USER_VALIDATED` accordé aux candidats ou au correctif d'interface.

## Sources et limites d'accès

- [GeoGREIF, notices des deux feuilles Anklam 1694](https://geogreif.uni-greifswald.de/search?coll_id=71Amt&map=overview&signatur=CI+) : Peder Wising, 1:8 333. **Scans et dérivés réservés à la recherche locale ; ne pas publier dans un dépôt public sans l'autorisation écrite requise par l'institution.**
- [Homann, exemplaire de Berne](https://ryhiner.ub.unibe.ch/de/world/volume/17/image/14614), [DOI institutionnel](https://doi.org/10.3931/e-rara-127588) : encart lisible, date exacte non établie. La page de métadonnées e-rara a renvoyé une vérification de navigateur ; pas de contournement. Le service d'image public lié par Berne est accessible.
- [Kórnik, notice de l'atlas](https://platforma.bk.pan.pl/pl/search_results/195777) : A V 018, édition 1793, planche 25. Lecteur public lié examiné ; le volume DjVu complet n'est pas téléchargé inutilement puisqu'un scan lisible de la planche est déjà disponible à Berne.
- [Grund 1775, notice de Berlin](https://kartenhighlights.staatsbibliothek-berlin.de/portfolio-item/grund-karte-der-neuen-provinz-westpreussen-1222-000-1775/) : lien conservé, pas de nouvel exemplaire intégral obtenu.

Les fichiers, empreintes et distinctions conception/planche/exemplaire sont dans `SOURCES.json`. Les coordonnées des nouveaux points sont des lectures manuelles du scan ; les rayons indicatifs de lecture ne sont **ni des intervalles statistiques ni des marges d'erreur en pixels du jeu**. Les cases Game_X/Y restent vides lorsqu'aucun homologue n'est reconnu.

Un appel ColGrep-Agent a été lancé pour la localisation, sans résultat exploité comme preuve ; les emplacements GUI et références utilisés ont été confirmés directement. Ni temps local fiable, ni tokens de tâche, ni économie exacte de quota ne sont mesurés. Aucun modèle, index ou réglage d'intégration modifié.

## Conditions encore nécessaires

Pour la Peene : homologues physiques réellement présents dans les deux supports près de Demmin–Anklam et raccord côtier précis du Peenestrom, ou une méthode documentée établissant leur absence et une simplification territoriale explicitement autorisée. Pour la Netze : datation fiable de l'état de planche pré-1776 et raccords occidentaux/méridionaux vérifiés, ou scan complet daté de Grund avec ces raccords. **La demande de recherche R1 ne vaut pas autorisation d'inventer ces points ni de transférer ses candidats.**
