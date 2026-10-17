# MAP-2Q-R3 — Schwartau et Kaltenhof installés, réserves maintenues

Date d'enregistrement : 16 octobre 2026. Situation cible : 1er janvier 1776.

**MAP2Q_R3_PARTIAL_INSTALLED_READY_FOR_SCOPED_RUNTIME_TEST**

Correction cartographique réelle livrée : **quatre cellules LUB → HLB**, deux nouveaux RGB, toujours dans `STATE_SCHLESWIG_HOLSTEIN` (66). Il s'agit d'enveloppes modestes **B**, pas de limites cadastrales certifiées. Le dossier reste partiel : il n'est pas déclaré `BISHOPRIC_CORE_GAMEPLAY_COMPLETE` tant que Ruppersdorf, Neuhof et les franges directes demeurent insuffisamment représentés. Les possessions ecclésiastiques distinctes restent `ECCLESIASTICAL_POSSESSIONS_PARTIAL`.

## Avant / après

| Représentation | Avant | Après |
|---|---|---|
| Noyau Schwartau–Rensefeld–Kaltenhof et raccord vers Ratekau | 3 cellules de x60809F / LUB | xEDB204 / HLB, 3 cellules |
| Enveloppe Offendorf–Ovendorf | 1 cellule de x60809F / LUB | xEDB205 / HLB, 1 cellule |
| Noyau d'Eutin accepté | 31 cellules / HLB | Identique |
| Population du noyau d'Eutin | 7 600, six blocs | Identique, blocs préservés exactement |
| Population nouvelle emprise | Dans les profils LUB | 1 606 réaffectés provisoirement, deux blocs séparés HLB |
| Population HLB totale | 7 600 | 9 206 |
| Population mondiale des historiques | 835 801 255 | 835 801 255 |
| Registre impérial | 508 RGB | 510 RGB, étendue géographique identique |

Le maintien du total mondial résulte ici d'un transfert technique, **pas d'une contrainte permanente**. Les 1 606 habitants ne sont pas un recensement historique de Kaltenhof. Les valeurs postérieures de l'Amt couvrent des périmètres différents ; leur utilisation aveugle aurait été trompeuse. Les six valeurs R2 ne sont ni multipliées ni recalculées.

Les images `SCHWARTAU_BEFORE_AFTER.png` et `KALTENHOF_BEFORE_AFTER.png` montrent les quatre cellules réellement installées. `SOURCE_SELECTION.png` conserve les enveloppes interprétées et les empreintes raster sur la carte de travail ; les hypothèses non retenues ne sont pas présentées comme des possessions installées.

## Justification et approximations

La souveraineté administrative épiscopale de l'Amt est étayée par NLA Best. 30, les histoires municipales et la description de Kohli, rapprochées des titres antérieurs à 1776 catalogués au LAS. La carte de vers 1819 sert uniquement de support géographique confronté aux changements documentés. Son territoire postérieur à 1803 n'est pas importé en bloc : Wilmsdorf acquis en 1804, les terres de la Großvogtei et les propriétés privées ne sont pas annexés par analogie.

Le calage est diagnostique, sans précision géographique indépendante certifiée. Les contours modestes sont interprétatifs. Les débords imposés par la cellule entière sont visibles ; pas d'agrandissement forcé des petites propriétés, pas de corridor entre l'enveloppe orientale et le noyau ni entre Kaltenhof et Eutin.

Sereetz et les franges de Ratekau ne sont pas déclarés intégralement restitués. Ruppersdorf et Neuhof restent ouverts. Le chapitre cathédral et le chapitre collégial sont audités séparément ; une option institutionnelle distincte est proposée, non installée. Voir HISTORICAL_EVIDENCE.md, SCHWARTAU_KALTENHOF_AUDIT.md et ECCLESIASTICAL_POSSESSIONS_AUDIT.md.

## Fichiers du jeu modifiés dans R3

- `map_data/provinces.png` : exactement quatre cellules recolorées.
- `map_data/province_terrains.txt` : deux terrains hérités de x60809F.
- `map_data/state_regions/00_west_europe.txt` : deux nouveaux RGB dans l'État 66 ; aucun hub déplacé.
- `common/history/states/00_states.txt` : attribution des deux RGB à HLB.
- `common/history/pops/00_west_europe.txt` : deux profils LUB réduits, deux blocs HLB ajoutés après les six blocs intacts d'Eutin.
- `common/scripted_triggers/1776_imperial_constitution.txt`, `common/scripted_effects/1776_imperial_constitution.txt`, `common/power_bloc_identities/1776_imperial_federation.txt` : prise en compte explicite des nouveaux droits.
- `localization/{english,french}/1776_imperial_feedback_l_*.yml` et `1776_imperial_repairs_l_*.yml` : listes/compteurs régénérés, pas de nouveaux droits hors périmètre.
- `gfx/interface/journal_entries/aor1776_hre_registered_map.dds` et sa source PNG : nouvelles limites internes. Le masque impérial de la carte principale reste identique.

Fichiers de suivi : registre actif `MAP2L/IMPERIAL_DE_JURE_REGISTRY.json`, manifeste et rapport courants MAP2Q, migration R3, outil reproductible `tools/map2q_r3.py`, tests ciblés `tools/test_map2q_r3.py`, ajout étroit du manifeste R3 à `tools/map2l_registry.py`. Les anciens rapports/baselines sont protégés ; seuls les pointeurs courants MAP2Q sont actualisés avec leurs versions précédentes archivées ici.

## Vérifications

- **609/609 contrôles statiques R3** : pixels et propriétaires mondiaux exacts au delta attendu, continuité des RGB, State_ID, terrains, locators, populations/profils, bâtiments, PM, propriétaires économiques, niveaux, unités et références.
- Reproduction des **57/57 fichiers impériaux avant intervention**, puis comparaison exacte des 57 sorties compilées après installation ; seuls sept fichiers texte impériaux nécessitent une évolution.
- Rejeu cumulatif exact du registre depuis la base MAP2L, le lot belge, l'extension piémontaise et les migrations ordonnées, jusqu'à 510 RGB.
- Noyau accepté, union OLD–HLB, prototype indépendant et toutes les cellules mondiales hors delta conservés. HEAD et index Git inchangés.
- **8/8 nouveaux tests ciblés R3 passent**, y compris les gardes négatives contre un pixel hors périmètre et l'ajout d'un corridor.
- Tests Q/R2 inchangés : **9/11 passent** ; deux anciens tests exigent encore l'image mondiale pré-R3 et Schwartau inchangé. Leurs échecs sont conservés, pas transformés en réussites.
- Six anciennes suites cumulatives : **62/68 passent** ; les mêmes six échecs de snapshots/registre déjà archivés avant R3 persistent. Détails dans UNIT_TESTS.json et TEST_RECONCILIATION.json. Les références anciennes ne sont pas réécrites.
- Les **44 doublons RGB et 12 erreurs de références préexistants** restent identiques ; aucune nouvelle anomalie de ces catégories n'est introduite.

Ces résultats sont des contrôles de données et tests hors moteur. **R2 est validé manuellement par le joueur ; R3 ne l'est pas encore.** La durée du test R2 n'étant pas fournie dans le prompt, elle n'est pas inventée.

## Arrêt et suite

Le périmètre réalisable est installé. Les incertitudes sont recensées dans UNRESOLVED.csv, sans nouvelle campagne générale de recherches. La vérification en nouvelle partie est décrite dans RUNTIME_TEST_PLAN.md.

L'inventaire R9 est repris dans HRE_REGIONS_INVENTORY_UPDATED.csv sans modifier le fichier historique. Un seul prochain chantier est proposé : **les principautés d'Anhalt**. Il n'est pas lancé automatiquement. Aucun commit, merge, reset, push, changement de branche ou modification de l'index n'a été effectué.
