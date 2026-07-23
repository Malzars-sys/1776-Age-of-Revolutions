# HOTFIX-6A.2F — Correction ciblée Autriche–Croatie–Slavonie–Suisse

Date : 2026-07-23  
Périmètre : cinq fichiers gameplay fermés, validation statique complète, runtime unique invalide avant chargement du mod

## 1. Résumé

Les douze hunks exécutables ont été appliqués dans les cinq fichiers autorisés. Tous les contrôles statiques passent. L’unique lancement Victoria 3 n’a toutefois pas monté le fork : `debug.log` contient `No subdirs mounted for game dir from candidates: mod/1776_age_of_revolutions_fork.mod`, `game.log` est vide et aucune partie 1776 n’a été chargée. Verdict de phase : `FAIL_RUNTIME_LOGS`; les changements gameplay sont conservés pour un retest runtime seul avec le playset launcher correct.

## 2. Verdicts d’entrée

`READY_FOR_AUSTRIA_CROATIA_WEST_SWITZERLAND_TARGETED_FIX`; `HOTFIX_6A2R_TARGET_HUNK_RESOLUTION_COMPLETE`; `SWISS_POP_HUNK_SHOULD_BE_OMITTED`; `SHIPYARD_CROATIA_REQUIRED_COMPATIBLE`; `AUS_FLEET_REQUIRED_RECONSTRUCTED`; `AGRAM_MIGRATION_REQUIRED_MINIMAL`.

## 3. État Git initial

Racine exacte, branche `hotfix-dlc-audit`, HEAD `16da441 Resolve Austria Croatia and Swiss target hunks`. Arbre suivi propre, zéro staged, seule exception non suivie `docs/research/technology/`. Rapport 6A.2R présent dans HEAD, Russie identique à `991f6a1`, stash MARATH intact, jeu et launcher fermés.

## 4. Sources

Rapport 6A.2R, audit 6A.2, delta map, rapports NAVY utiles, fork, source hotfix et vanilla 1.13. Les sources hotfix/vanilla sont restées en lecture seule.

## 5. Méthode

Application par ancres exactes avec patch ciblé, puis vérifications par `Get-Content`, `Select-String`, `Get-FileHash`, `git diff` et comptages de blocs/accolades. Aucun `rg`, import complet, reset, restore, checkout, clean ou opération de stash.

## 6. Liste fermée des fichiers

Modifiés : `00_states.txt`, `pops/01_south_europe.txt`, `buildings/01_south_europe.txt`, `00_subject_relationships.txt`, `00_military_formations_europe.txt`. Aucun autre gameplay.

## 7. Hunk STATE_CROATIA

Owner `c:CRO` remplacé par `c:AUS`. Les huit provinces restent exactement `x71A041 x70DF00 x6D8BC6 xF021C0 x71A0C0 xB39050 xB339EC x458E4C`.

## 8. Hunk STATE_SLAVONIA

Owner `c:CRO` remplacé par `c:AUS`. Les sept provinces restent exactement `x51A021 x106020 x13318D x906121 x80CF00 x902161 x1A4DF9`.

## 9. Hunk suisse x90C0E0

`x90C0E0` est retirée de la liste SWI et placée seule dans un second `create_state` AUS de `STATE_EAST_SWITZERLAND`. La syntaxe valide du fichier et du bloc hotfix est un `create_state` frère direct; le wrapper `region_state:AUS` présenté comme exemple dans le prompt n’a pas été introduit dans l’historique des states.

## 10. Omission des 30 000

`common/history/pops/00_west_europe.txt` est byte-for-byte inchangé, SHA-256 `8A31C46D3402DB6FE13C2854D7D6EDC70C5B3B8D8443B82F1C5E02C2B84CA617`. Aucun bloc AUS de 30 000 n’a été ajouté; variation nette suisse attendue : 0, total 895 200.

## 11. Pops Croatia

Le seul scope `region_state:CRO` du bloc Croatia devient `region_state:AUS`. Cultures, religions, professions, tailles et commentaires sont inchangés.

## 12. Pops Slavonia

Le seul scope `region_state:CRO` du bloc Slavonia devient `region_state:AUS`. Aucun groupe de pop n’est modifié.

## 13. Buildings Croatia

Scope CRO→AUS et exactement huit ownerships existants CRO→AUS : administration, paper mill, university, deux manor houses agricoles, logging financial district, fishing wharf et port. L’ownership HUN, les niveaux, réserves, PMs et ordre existants sont préservés.

## 14. Shipyard Croatia

Un seul `building_shipyard` est inséré entre fishing wharf et port. Ownership financial district AUS, `levels=2`, `region="STATE_CROATIA"`, `reserves=1`, seul PM `pm_basic_shipbuilding`.

## 15. Buildings Slavonia

Scope CRO→AUS et unique manor-house ownership CRO→AUS. Ownership HUN et valeurs existantes inchangés.

## 16. Pactes CRO

Les deux seuls blocs AUS→CRO `crown_land` et `decrease_payments` sont supprimés. Le diff ne touche aucun autre pacte.

## 17. Flotte AUS

Une seule `K_K_Kriegsmarine` est créée sous AUS, HQ `region_balkans`, 1 `ship_type_ship_of_the_line` et 3 `ship_type_frigate`, tous en `STATE_CROATIA`. Aucun amiral, loi, technologie, administration ou localisation ajouté.

## 18. Generalkommando Agram

Le bloc fork est déplacé sous AUS avant Lemberg, sans changement interne : quatre entrées line infantry, comptes 2+12+4+6, total 24. Zéro cuirassier, zéro artillery. Le wrapper CRO vide est supprimé.

## 19. Tag CRO dormant

Le fichier pays et toutes les références de libération/événements restent présents. Seul le territoire initial, les pactes, scopes et formation sont migrés.

## 20. Protections NAVY

Seuls la flotte fermée et le déplacement byte-for-byte d’Agram touchent le fichier NAVY. Toutes les autres flottes, formations, lois et localisations NAVY restent hors diff.

## 21. Protections ADMIN

Les PM ADMIN sont inchangés; seuls scope et ownerships explicitement autorisés sont re-clés.

## 22. Protections MARATH

MARATH, SAT, KHP et les deux fichiers du stash n’ont pas été modifiés. Aucun contenu du stash n’a été inspecté ou appliqué.

## 23. Setup 1776 préservé

Fichiers pays, événements, journaux, localisations, cartes, strategic regions et autres states sont inchangés. `law_frontier_colonization` est conservée et aucune `law_colonial_exploitation` n’est restaurée.

## 24. Diff exact

Avant rédaction documentaire : exactement cinq chemins gameplay, 81 insertions et 58 suppressions. Le volume comprend le déplacement d’Agram, représenté comme suppression puis insertion identique.

## 25. Hashes avant et après

| Fichier | Avant | Après |
|---|---|---|
| states | `4168903A...53CFC` | `625C40C4...62067` |
| pops South Europe | `9922E405...0677` | `B26A2FF2...1E9A2` |
| buildings South Europe | `E9A35A76...9121C` | `DE9E0C60...A2380` |
| subject relationships | `564DC3B2...E801C` | `BA138EFF...3BCB1` |
| formations Europe | `D85E9FF7...35292` | `F170CF94...FEA33` |
| pops West Europe | `8A31C46D...CA617` | identique |

Les hashes complets figurent dans les sorties de validation de la phase.

## 26. Encodages et fins de ligne

Les cinq fichiers restent index et worktree LF selon `git ls-files --eol`. Aucun changement d’encodage ou fin de ligne globale; `git diff --check` passe.

## 27. Occurrences

Une portion AUS suisse, deux scopes pops AUS, huit ownerships Croatia migrés, un Slavonia migré, un shipyard nouveau, une flotte nommée, un Agram global et zéro wrapper CRO dans le fichier formations.

## 28. Accolades

Balance ouvrantes/fermantes égale à zéro dans chacun des cinq fichiers.

## 29. Tests statiques

`AUSTRIA_CROATIA_WEST_SWITZERLAND_TARGETED_FIX_STATIC_PASS`. Les 40 exigences sont satisfaites; le premier faux positif de comptage a été corrigé en distinguant huit ownerships migrés, un ownership AUS préexistant et un ownership shipyard créé.

## 30. Préparation runtime

Le launcher était fermé. Sa base, lue sans mutation, montrait `playset1` actif mais vide; le playset `hhhh` contenait uniquement le fork mais n’était pas actif. Pour respecter l’unicité, le lancement direct a tenté de passer uniquement `1776_age_of_revolutions_fork.mod` avec `-debug_mode`.

## 31. Lancement unique

Une seule ouverture de `victoria3.exe`, PID 4952, à 02:32:17. Aucun second lancement. La fermeture principale n’ayant pas terminé pendant le délai, le processus a été arrêté; aucun processus Victoria, dowser, Paradox ou launcher ne subsiste.

## 32. Résultats AUS

Non observables : aucune partie n’a été chargée avec le fork. Aucun PASS AUS n’est déclaré.

## 33. Résultats CRO

Non observables pour la même raison. Aucun PASS CRO n’est déclaré.

## 34. Résultats SWI

Non observables. Le résultat statique confirme seulement l’absence du hunk +30 000 et le transfert exact de province.

## 35. Résultats pops

Statique PASS; runtime non exécuté dans un setup mod chargé.

## 36. Résultats buildings

Statique PASS; runtime du port/shipyard/ownership non observé.

## 37. Résultats flotte

Statique PASS pour la syntaxe et la composition 1+3; apparition en jeu non observée.

## 38. Résultats Agram

Statique PASS pour l’unicité, l’owner de scope et le total 24; apparition sous AUS non observée.

## 39. Non-régression Russie

Le fichier Russie ne diffère pas de `991f6a1`. La non-régression runtime n’est pas revendiquée.

## 40. Non-régression blocs clos

Inde, Japon, Mamluk Iraq, BIC et Travancore ne sont pas dans le diff. Leur runtime n’a pas été atteint.

## 41. Analyse error.log

Nouveau fichier de 826 octets. Il contient sept diagnostics de parsing de la localisation française vanilla `NAVY_MAINTENANCE_COST_TOOLTIP` dans `gui/construction_panel.gui`. Le fork n’étant pas monté, ces diagnostics ne sont pas attribuables aux hunks 6A.2F. Aucun identifiant cible 6A.2F n’apparaît.

## 42. Analyse game.log

Fichier vide, SHA-256 du fichier vide `E3B0C442...B855`. Aucune preuve de setup, pays ou partie chargée.

## 43. Analyse debug.log

29 306 octets. Ligne 85 : `No subdirs mounted for game dir from candidates: mod/1776_age_of_revolutions_fork.mod`. Cette preuve invalide le runtime avant toute inspection fonctionnelle.

## 44. Erreurs préexistantes

Le problème de localisation `NAVY_MAINTENANCE_COST_TOOLTIP` est hors périmètre et observé sans mod monté. Il doit être traité comme diagnostic environnemental/vanilla, non comme régression 6A.2F.

## 45. Nouvelles erreurs

Nouvelle erreur bloquante de cette tentative : chemin de descripteur non monté au lancement direct. Aucune nouvelle erreur de state, pop, building, pacte, formation, HQ ou ship type du correctif ne peut être évaluée.

## 46. Risques restants

Tous les risques runtime restent ouverts : portion AUS vide, visibilité du shipyard, flotte, Agram, CRO dormant et non-régression RUS. Ils exigent un retest unique via playset launcher correctement actif.

## 47. Fichiers modifiés

Exactement les cinq gameplay autorisés, le présent rapport, la delta map et les cinq documents de navigation/statut autorisés.

## 48. Fichiers non modifiés

`pops/00_west_europe.txt`, autres gameplay/NAVY/ADMIN/MARATH, Russie, localisations, descripteurs, sauvegardes, harnais et sources externes.

## 49. Rollback disponible

Chaque hunk conserve le rollback exact de 6A.2R. Aucun rollback gameplay n’est appliqué : le runtime a échoué sur le montage du mod, pas sur le correctif, et tous les tests statiques passent.

## 50. Confirmation docs/research/technology/

Les sept fichiers non suivis sont restés hors périmètre et conservent leurs hashes observés avant la rédaction documentaire.

## 51. Confirmation stash MARATH

`stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` intact; aucun apply, pop, drop ou lecture de contenu.

## 52. Verdict final

- `AUSTRIA_CROATIA_WEST_SWITZERLAND_TARGETED_FIX_STATIC_PASS`
- `SWISS_POPULATION_NET_CHANGE_ZERO`
- `CROATIA_SLAVONIA_ABSORBED_BY_AUS_STATIC_PASS`
- `EAST_SWITZERLAND_SLIVER_TRANSFERRED_STATIC_PASS`
- `CRO_SUBJECT_RELATION_REMOVED_STATIC_PASS`
- `SHIPYARD_CROATIA_LEVEL_2_STATIC_PASS`
- `AUS_FLEET_1_SOL_3_FRIGATES_STATIC_PASS`
- `AGRAM_24_INFANTRY_MIGRATED_TO_AUS_STATIC_PASS`
- `RUSSIA_SUBJECTHOOD_STATIC_NON_REGRESSION_PASS`
- `FAIL_RUNTIME_LOGS`
- `RUNTIME_INVALID_MOD_NOT_LOADED`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`

Les verdicts `AUSTRIA_CROATIA_WEST_SWITZERLAND_TARGETED_FIX_RUNTIME_PASS` et `AUSTRIA_CROATIA_WEST_SWITZERLAND_TARGETED_FIX_COMPLETE` ne sont pas émis.
