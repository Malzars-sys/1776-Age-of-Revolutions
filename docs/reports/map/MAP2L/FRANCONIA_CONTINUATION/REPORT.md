# MAP-2L — prolongement des subdivisions franconiennes

14 octobre 2026. Démarrage visé : 1er janvier 1776.

**Appliqué au mod : quatre provinces mixtes subdivisées, neuf nouveaux RGB, 185 cellules transférées.** Ce sous-lot fait avancer la carte ; il ne prétend pas achever toutes les principautés du Saint-Empire. Erfurt–Eichsfeld reste gelé, sans nouvelle optimisation ni translation.

## Corrections réellement appliquées

L'omission corrigée venait du premier lot : les enveloppes historiques conservées avaient été intersectées uniquement avec `STATE_FRANCONIA`. Leurs prolongements dans `STATE_BAVARIA` restaient donc intégralement bavarois, alors que la limite d'une région économique du jeu n'est pas une frontière politique de 1776.

Les quatre parents sont dans `STATE_BAVARIA`, ID numérique **71**, qui demeure une région économique partagée. Aucun State_ID, hub, ressource ou frontière de State Region n'est déplacé. Un RGB identifie un polygone du bitmap, pas un État historique.

| RGB parent | Avant | RGB transféré | Après | Cellules |
| --- | --- | --- | --- | ---: |
| x010AD7 | BAV | xEDA800 | ANS — Ansbach | 25 |
| x010AD7 | BAV | xEDA801 | EIC — Eichstätt | 23 |
| x318021 | BAV | xEDA802 | EIC — Eichstätt | 18 |
| x318021 | BAV | xEDA803 | EIC — Eichstätt | 18 |
| x82F4B9 | BAV | xEDA804 | FBM — Bamberg | 44 |
| xA7094D | BAV | xEDA807 | FBM — Bamberg | 44 |
| xA7094D | BAV | xEDA808 | NUR — Nuremberg | 13 |
| **Total** | | | | **185** |

Les quatre RGB parents restent présents sur leurs portions bavaroises : respectivement 52, 222, 216 et 127 cellules. Deux fragments bavarois séparés reçoivent `xEDA805` (5 cellules) et `xEDA806` (3 cellules), **sans changement de propriétaire**. Les 810 cellules des quatre parents sont intégralement conservées. Le bitmap change de couleur sur 193 cellules, dont 185 changent de contrôleur et 8 seulement d'identité technique.

La liste exhaustive avant/après est `TERRITORIAL_CHANGES.csv`. `GEOMETRY.json` conserve les cellules exactes, les composantes et les filiations RGB ; `REGISTRY_MIGRATION.json` conserve la transition exacte des droits impériaux.

## Justification et approximations

Cette passe réutilise **sans modifier leurs sommets ni leur matrice** les enveloppes de `../FRANCONIA/TRACING.json` et le calage de `../FRANCONIA/ALIGNMENT.json`. La carte Homann conservée est `../GEOMETRY/Homann_reading.jpg`, dérivée du document Stadtarchiv Nürnberg A4/IV nº 74. Les conclusions institutionnelles et la confrontation Le Rouge/Endres du dossier `../FRANCONIA/GEOGRAPHIC_EVIDENCE.md` restent le fondement historique ; aucune recherche générale n'a été recommencée.

- **Ansbach** : prolongement du territoire dessiné de Brandenburg-Ansbach. ANS représente déjà l'union personnelle avec Bayreuth depuis 1769, pas une cession à la Prusse, qui est postérieure à 1776. Bayreuth et ses allocations existantes restent intacts.
- **Bamberg** : prolongement des districts orientaux et méridionaux du Hochstift, distincts de la Bavière électorale. L'union de titulaire avec Würzburg ne fusionne pas leurs juridictions : FBM et WZB restent deux pays distincts.
- **Nuremberg** : prolongement oriental de l'enveloppe territoriale déjà dessinée de la ville libre, pas attribution par proximité de son centre urbain. Son statut impérial et son conseil existants sont conservés.
- **Eichstätt** : continuation du seul polygone septentrional déjà retenu du Hochstift, sous Raymund Anton von Strasoldo en 1776. Cela ne certifie pas toute sa frange méridionale ni la position de la ville historique.

La notice d'archives ne date pas assez précisément l'édition Homann pour prouver chaque limite au jour près. Le contrôle de Ratisbonne du modèle conservé diffère de **5,121 pixels** ; c'est un repère urbain du jeu, pas une mesure géodésique indépendante. L'application est donc une **approximation politique raisonnable à l'échelle du jeu**, expressément autorisée dans cette reprise, et non une frontière cadastrale ou une précision locale inférieure à trois pixels.

Aucune dilatation, translation de sept pixels, optimisation supplémentaire ou partition par ville la plus proche n'est utilisée. Une intersection marginale d'une cellule de Nuremberg dans `x82F4B9` n'est pas transférée. Les petits fragments existants d'une cellule aux autres frontières ne sont pas redécoupés. Les franges sans attribution démontrée restent à leur contrôleur courant **sans que cela certifie sa souveraineté historique**.

## Conservation et intégration

Population de la région économique Bavière : **1 358 763**, avant comme après. Répartition complémentaire depuis BAV :

| Pays receveur | Habitants transférés depuis BAV |
| --- | ---: |
| ANS | 9 102 |
| EIC | 21 481 |
| FBM | 32 040 |
| NUR | 4 734 |
| **Total** | **67 357** |

BAV conserve 1 291 406 habitants dans cette région. Les trois profils culture/religion sont répartis une seule fois depuis l'instantané immuable, par poids surfaciques et arrondis conservatifs. Ce n'est pas un recensement des districts historiques. Aucun habitant n'est ajouté ; population mondiale toujours **835 804 980**.

Tous les bâtiments, niveaux, méthodes de production et détenteurs économiques restent inchangés dans cette passe : les petites parts transférées ne déplacent aucun niveau entier. La subdivision BAV subsiste, donc ses propriétaires économiques et recrutements ne deviennent pas orphelins. Armées, marines, formations, capitales, lois et gouvernements sont conservés. Les quatre pays existaient déjà ; aucune création de pays ou population artificielle.

Le registre actif passe de **394 à 403 RGB**, avec la même étendue impériale de **62 580 cellules**. Les nouveaux RGB héritent des terrains de leurs parents. Les listes et effets impériaux dépendants sont recompilés, sans changement des règles de succession, d'élection ou de centralisation. Cartes principale et du journal régénérées. Les corrections belges, piémontaises, de Mayence et de Milan restent préservées.

### Fichiers

- Carte et historique : `map_data/provinces.png`, `map_data/province_terrains.txt`, `map_data/state_regions/00_west_europe.txt`, `common/history/states/00_states.txt`, `common/history/pops/00_west_europe.txt`.
- Registre : `docs/reports/map/MAP2L/IMPERIAL_DE_JURE_REGISTRY.json`, migration de ce sous-lot et ajout explicite à `tools/map2l_registry.py`.
- Dépendances impériales : `common/scripted_triggers/1776_imperial_constitution.txt`, `common/scripted_effects/1776_imperial_constitution.txt`, `common/power_bloc_identities/1776_imperial_federation.txt`, localisations françaises et anglaises `1776_imperial_feedback` et `1776_imperial_repairs`.
- Images régénérées : `gfx/interface/journal_entries/aor1776_hre_registered_map.dds`, `gfx/map/map_painting/aor1776_hre_mask.dds`, `gfx/map/map_painting/aor1776_hre_sentinel.dds`.
- Outils : `tools/map2l_franconia_continuation.py`, `tools/validate_map2l_franconia_continuation.py` et adaptation strictement cumulative du test `tools/validate_map2l_milan.py`.
- Traçabilité : fichiers de ce dossier ; note ciblée `../ERFURT_EICHSFELD/REPRISE_FUTURE.md`. Les fichiers de rapports de validation des lots précédents sont actualisés par leurs validateurs.

`PLAN.json` et `IMPERIAL_FILES.json` donnent les chemins textuels exacts. `HISTORY.patch` et `IMPERIAL.patch` gardent les changements générés ; une finition d'indentation des **seuls nouveaux blocs** a été effectuée après application. Les instantanés originaux et les bitmaps antérieurs ne sont pas réécrits.

## Vérifications

| Suite | Résultat |
| --- | ---: |
| Nouveau prolongement franconien | 418 / 418 |
| Belgique | 315 / 315 |
| Piémont | 232 / 232 |
| Franconie cumulative | 587 / 587 |
| Rhin central | 486 / 486 |
| Mayence–Palatinat | 631 / 631 |
| Possessions de Mayence | 617 / 617 |
| Prolongement méridional de Mayence | 492 / 492 |
| Milan | 439 / 439 |
| Carte principale, hors moteur | 16 / 16 |

Contrôles : provenance et sommets conservés, classification de chaque cellule des quatre parents, RGB à quatre voisins, attribution unique et State_ID valide, aucune suppression de RGB original, héritage des terrains, tous les locators conservés, propriétaires hors Bavière exactement inchangés depuis la baseline de cette passe, démographie/économie/unités conservées, migration et sorties du compilateur exactes, HEAD et index Git inchangés. Les cartes DDS restent sans ajout ni omission de cellule impériale ; le helper HLSL compile dans le harnais de test, **pas dans le moteur du jeu**.

L'ancien test spécifique de Milan affirmait que toute propriété non lombarde resterait éternellement identique à sa baseline. Il a été rendu cumulatif : seules les transitions exactes des migrations explicitement approuvées ultérieures sont acceptées. Les tests de continuité de Milan, de ses villes vénitiennes et de sa géométrie restent inchangés. Une première commande a aussi utilisé un nom inexistant de validateur piémontais ; elle a été corrigée en `map2l_piedmont.py validate`, avec résultat réussi. Ce sont des incidents de vérification, pas des nouvelles erreurs de la carte.

**Préexistant** : exactement les mêmes 44 RGB doublement attribués et 12 erreurs de références hors du lot. Des défauts d'espacement hérités restent présents dans le dépôt sale ; les nouvelles lignes blanches introduites par ce sous-lot ont été nettoyées, sans reformater les changements antérieurs.

**En jeu, encore à vérifier** : nouvelle campagne au 1er janvier 1776, limites des quatre pays dans la région Bavière, subdivisions partagées, carte de jure, journal, démographie et logs. Aucun jeu lancé, conformément à la demande d'attendre la fin des lots du Saint-Empire. Aucun commit, staging, merge, rebase ou push.

## Suite ouverte, indépendante d'Erfurt

Würzburg, Bayreuth et les autres tracés franconiens déjà validés ne sont pas réappliqués. Rothenburg, Hohenlohe, les franges secondaires et le sud non tracé d'Eichstätt restent à traiter avec leurs juridictions propres, pas par attribution automatique à un voisin. Le Rhin/Westphalie puis la Souabe restent les prochains secteurs : cette passe n'affirme pas les avoir terminés. Les anciens fichiers `UNRESOLVED.csv` sont des historiques de leurs sous-lots, pas des listes actuelles faisant disparaître les corrections ultérieures de Mayence.

Erfurt–Eichsfeld ne bloque plus cette progression. `REPRISE_FUTURE.md` énumère seulement les repères physiques homologues, l'hydrographie détaillée et les superpositions historiques nécessaires à sa reprise, sans nouvelles recherches ni nouvelle calibration.

## Recherche locale ColGrep

Un appel exploratoire à l'agent local configuré 2B, **104,175 secondes**, code de sortie 0 :

```powershell
& 'C:/Users/simeo/.cargo/bin/colgrep.exe' --agent 'Find retained historical source maps and territorial decisions for remaining Franconian fringes, Rhine/Westphalia or Swabian principalities that can support actual 1776 ownership corrections. Franconia REPORT and TRACING and applied Mainz lots are already known. Return up to four exact paths and line ranges for unimplemented sectors with sources, not generic readiness audits. Do not edit files or infer sovereignty.' ./docs/reports/map
```

Les chemins et plages retournés de `FRANCONIA/TRACING.json`, `FRANCONIA/REGISTRY_MIGRATION.json`, `EVIDENCE/BSB_SOURCE.json` et `RHINE_CENTRAL/REGISTRY_MIGRATION.json` ont été vérifiés par lecture des fichiers. Ils étaient pertinents mais déjà connus ; aucun dossier nouveau de Westphalie ou de Souabe n'a été identifié. Aucun second appel redondant. Les RGB et les fichiers de test sont vérifiés par recherches exactes ; bitmaps/DDS et CSV sont lus par les outils adaptés, sans supposer leur contenu couvert par l'index sémantique.

Pas de compteur fiable de tokens Codex par opération, pas de comparaison A/B et pas de décompte instrumenté complet des recherches classiques de cette passe. **Aucune économie exacte de quota ne peut être affirmée.** Pour cette recherche précise, l'appel local a surtout ajouté du temps sans fournir de nouveau chemin ; son utilité ne remplace pas l'analyse des tracés et les contrôles de conservation.

Actualisation incrémentale tentée à la fin, sans effacement ni reconstruction : `colgrep init .`, puis le chemin absolu explicite du même dépôt. Les deux commandes renvoient `Path does not exist`, alors que le chemin est lisible par les outils de fichiers. L'index n'est donc **pas déclaré actualisé** après ces modifications. Aucune configuration d'intégration n'est modifiée et aucune troisième tentative n'est lancée ; cette limitation de résolution de chemin devra être examinée séparément avant une nouvelle recherche sur les fichiers créés ici.

## Aperçus

`BEFORE_AFTER.png` montre la carte politique effective avant/après à l'échelle du bitmap. Orange = ANS, bleu = FBM, rouge = NUR, vert = EIC, gris = BAV. Les lignes noires sont les identités de provinces, pas une preuve de frontière historique au pixel près. `HOMANN_OVERLAY.png` situe les enveloppes réutilisées sur la source conservée. Ce ne sont pas des captures de Victoria 3.
