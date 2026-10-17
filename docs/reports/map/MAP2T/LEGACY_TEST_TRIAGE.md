# Tests de photographies anciennes

Les17 tests ciblés et60 tests de contrats cumulatifs passent. Les49 tests historiques supplémentaires donnent42 succès,7 échecs,0 erreur. Aucun test ni baseline ancien n’est modifié pour obtenir un succès.

Deux assertions MAP2R attendent le monde entier de l’étape Anhalt et exactement trois pays supplémentaires depuis leur ancienne baseline. MAP2T ajoute six pays et change121 cellules en Saxe; ces attentes globales ne sont plus applicables. Tous les pixels hors STATE_SAXONY, y compris Anhalt, sont contrôlés identiques à la baseline immédiatement antérieure.

Les tests Q-R3/R8/R9 comparent aussi des bitmaps mondiaux arrêtés avant les lots postérieurs. L’attente R8 de la couleur E1A03A à Wolgast(4410,735) est déjà différente dans la baseline MAP2T et reste identique pendant ce lot. Le test O de registre attend l’ancien registre avant les migrations ultérieures, tandis que le nouveau contrôle effectue la relecture chronologique complète jusqu’à MAP2T. Les secteurs Q/M/O ne changent pas dans le présent bitmap. Ces échecs sont conservés comme diagnostics, pas convertis silencieusement en PASS.

## Identifiants des sept échecs

- `test_map2r_anhalt.AnhaltDeltaTests.test_exact_bitmap_and_no_external_change`
- `test_map2r_anhalt.AnhaltDeltaTests.test_four_tags_and_only_three_new_countries`
- `test_map2q_r3.Kaltenhof.test_exact_delta_and_negative_guard`
- `test_map2m_r8.InstalledBTests.test_exact_b_not_a_plus_b`
- `test_map2m_r8.InstalledBTests.test_wolgast_and_protected_rows_not_shifted`
- `test_map2m_r9.R9Guards.test_exact_two_cells_and_no_elsewhere_edit`
- `test_map2o_east_frisia.EastFrisiaTests.test_exact_ledger_replay_preserves_every_other_right`

Les sorties réelles et traces restent dans UNIT_TESTS.json. Les contrôles différentiels de VALIDATION.json protègent les secteurs antérieurs sans exiger que le monde reste figé à leur date de livraison.
