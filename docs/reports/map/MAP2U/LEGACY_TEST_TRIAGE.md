# Tests figés d’étapes antérieures

22/22 tests MAP2U et 60/60 contrats cumulatifs passent. Les 66 tests antérieurs donnent52 succès,14 échecs,0 erreur. Aucun ancien test ou baseline n’est modifié.

Sept échecs étaient déjà consignés par MAP2T. Quatre assertions MAP2T attendaient le monde entier avant MAP2U, exactement six pays supplémentaires depuis leur capture, aucune modification d’une autre région ou les seules définitions de pays de ce stade. Une assertion MAP2R supplémentaire exigeait que toutes les cellules prussiennes mondiales restent inchangées: elle rencontre les 16 cellules PRU→SSO autorisées, sans altération des quatre Anhalt. Ce ne sont pas de nouvelles pertes silencieuses: le bitmap mondial est vérifié exactement contre la transformation MAP2U, et les noyaux antérieurs sont contrôlés séparément.

L’attente ancienne à Wolgast et les anciennes photographies de registre restent signalées, pas réécrites. Les 44 doublons RGB et 12 références invalides hérités ne sont pas corrigés ni augmentés ici.

Deux échecs économiques supplémentaires proviennent des trois fichiers de bâtiments modifiés parallèlement dans le workspace. Leurs deltas observés figurent dans EXTERNAL_BUILDINGS_OBSERVED.json: aucune ancienne baseline n’est modifiée pour les masquer. Le nouveau contrôle économique conserve exactement la baseline plus ces seuls deltas attestés par les empreintes des trois fichiers, sans autorisation générale de modifier l’économie.

## Échecs effectivement observés

- `test_map2t_saxony.SaxonDeltaTests.test_all_economic_and_military_data_unchanged`
- `test_map2t_saxony.SaxonDeltaTests.test_country_changes_exact`
- `test_map2t_saxony.SaxonDeltaTests.test_exact_declared_bitmap`
- `test_map2t_saxony.SaxonDeltaTests.test_no_other_state_touched`
- `test_map2t_saxony.SaxonDeltaTests.test_only_six_approved_new_tags`
- `test_map2r_anhalt.AnhaltDeltaTests.test_all_economy_and_units_preserved`
- `test_map2r_anhalt.AnhaltDeltaTests.test_exact_bitmap_and_no_external_change`
- `test_map2r_anhalt.AnhaltDeltaTests.test_four_tags_and_only_three_new_countries`
- `test_map2r_anhalt.AnhaltDeltaTests.test_jever_and_all_prussian_cells_unchanged`
- `test_map2q_r3.Kaltenhof.test_exact_delta_and_negative_guard`
- `test_map2m_r8.InstalledBTests.test_exact_b_not_a_plus_b`
- `test_map2m_r8.InstalledBTests.test_wolgast_and_protected_rows_not_shifted`
- `test_map2m_r9.R9Guards.test_exact_two_cells_and_no_elsewhere_edit`
- `test_map2o_east_frisia.EastFrisiaTests.test_exact_ledger_replay_preserves_every_other_right`

Traces complètes et durées: UNIT_TESTS.json. Statique différentiel: VALIDATION.json.
