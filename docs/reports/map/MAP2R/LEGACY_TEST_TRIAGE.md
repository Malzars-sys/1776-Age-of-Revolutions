# Tests anciens : écarts conservés et distingués

Les tests et baselines des étapes antérieures ne sont pas modifiés pour masquer leur obsolescence. La reproduction différentielle mondiale depuis la baseline MAP2R passe ; elle protège tous les pixels hors des deux parents ANH et toutes les données hors du plan explicite.

## Échecs déjà recensés dans UNIT_TESTS.json de MAP2Q/R3

- `test_map2q_eutin.EutinGuards.test_exact_bitmap_and_negative_outside_edit`
- `test_map2q_eutin.EutinGuards.test_no_schwartau_or_oldenburg_corridor`
- `test_map2m_r8.InstalledBTests.test_exact_b_not_a_plus_b`
- `test_map2m_r8.InstalledBTests.test_wolgast_and_protected_rows_not_shifted`
- `test_map2m_r9.R9Guards.test_exact_two_cells_and_no_elsewhere_edit`
- `test_map2n_island.PoelTests.test_exact_scoped_edits_and_negative_guard`
- `test_map2n_completion.CompletionTests.test_exact_mainland_patch_and_negative_out_of_scope_edit`
- `test_map2o_east_frisia.EastFrisiaTests.test_exact_ledger_replay_preserves_every_other_right`

## Deux nouveaux écarts de snapshots dus à MAP2R

- `test_map2q_r3.Kaltenhof.test_exact_delta_and_negative_guard` attend que seules les quatre cellules R3 changent dans le monde entier. Les nouveaux enfants RGB d’Anhalt rendent cette attente obsolète ; les cellules R3 sont inchangées dans la comparaison mondiale MAP2R.
- `test_map2n_island.PoelTests.test_no_move_of_hubs_or_old_pomeranian_provinces` exige le même RGB sous TOUS les locators mondiaux. Le locator agricole d’Anhalt est physiquement immobile mais son RGB passe explicitement de x8A448C à xEDB304. Aucun hub poméranien n’est déplacé. Cette réassociation est enregistrée dans REGISTRY_MIGRATION.json et contrôlée sans dérogation globale.

## Résultats courants

11/11 tests MAP2R passent ; 16/19 tests des étapes Q passent ; 61/68 tests cumulatifs anciens passent. Zéro erreur d’exécution de test. Les dix échecs listés ne sont pas convertis artificiellement en PASS. Les nouvelles vérifications ciblées comparent l’état mondial à la baseline immédiate avec le delta exact autorisé.

Les 44 doublons de provinces et12 références invalides sont des anomalies de données antérieures, distinctes de ces assertions de snapshots. Leur liste exacte reste identique ; aucune nouvelle anomalie de ces catégories.
