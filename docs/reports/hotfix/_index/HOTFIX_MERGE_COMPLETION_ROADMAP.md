# HOTFIX — Roadmap de fin du merge global

## 1. Résumé

Le bloc canonique reste `HOTFIX-6A_GLOBAL_SCRIPT_DELTAS`. La Russie est corrigée au commit `991f6a1`. Le paquet 6A.2 est clos par 6A.2F2. La phase DEI/VOC est close par `HOTFIX_6A3F_DEI_TARGETED_FIX_COMPLETE`, après validation statique, runtime des trois branches et sauvegarde/rechargement. Les alignements 6A.4F à 6A.10F sont clos. Les deux pinning roumains sont alignés avec Victoria 3 1.13 ; la Valachie atteint le 2 janvier 1776 sans anomalie visible et les diagnostics ciblés passent de deux à zéro. La nouvelle baseline est de 376 diagnostics dans 141 fichiers. La prochaine phase est une sélection documentaire.

Verdicts :

- `MERGE_REMAINING_WORK_INDEXED`
- `MERGE_COMPLETION_ROADMAP_CREATED`
- `POST_MERGE_BACKLOG_SEPARATED`
- `NEXT_MERGE_BLOCK_IDENTIFIED`
- `GLOBAL_SCRIPT_DELTAS_WITH_RUSSIA_FIRST`
- `AUSTRIA_CROATIA_WEST_SWITZERLAND_AUDIT_COMPLETE`
- `HOTFIX_6A2R_TARGET_HUNK_RESOLUTION_COMPLETE`
- `AUSTRIA_CROATIA_WEST_SWITZERLAND_TARGETED_FIX_STATIC_PASS`
- `HOTFIX_6A2F2_SWISS_POP_NAVAL_BASE_STATIC_PASS`
- `AUSTRIA_CROATIA_WEST_SWITZERLAND_TARGETED_FIX_RUNTIME_PASS`
- `AUSTRIA_CROATIA_WEST_SWITZERLAND_TARGETED_FIX_COMPLETE`
- `HOTFIX_6A3_DEI_TARGETED_AUDIT_COMPLETE`
- `NO_REQUIRED_HOTFIX_DELTA_IDENTIFIED`
- `HOTFIX_6A3R_DEI_BREAKUP_HUNK_RESOLUTION_COMPLETE`
- `HOTFIX_6A3F_DEI_TARGETED_FIX_COMPLETE`
- `MILITARY_FORMATIONS_1_13_RUNTIME_QA_COMPLETE`
- `HOTFIX_6A4_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE`
- `HOTFIX_6A4F_BALKAN_NATIONAL_AWAKENING_1_13_COMPLETE`
- `HOTFIX_6A5_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE`
- `HOTFIX_6A5F_YUGOSLAVIA_JE_PINNING_1_13_STATIC_PASS`
- `HOTFIX_6A5F_YUGOSLAVIA_JE_PINNING_1_13_RUNTIME_PASS`
- `HOTFIX_6A5F_YUGOSLAVIA_JE_PINNING_1_13_COMPLETE`
- `HOTFIX_6A10_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE`
- `HOTFIX_6A10F_ROMANIA_TWO_JE_PINNING_1_13_ALIGNMENT_COMPLETE`
- `NO_GAMEPLAY_CHANGED`
- `SAFE_TO_RETIRE_DISPOSABLE_AFTER_C1AI_COMMIT`

## 2. Périmètre du merge

Le périmètre est l’intégration ciblée du contenu légitime de la source hotfix dans le fork 1.13, sans remplacer les adaptations 1776, les corrections locales validées, les localisations françaises, NAVY, ADMIN, MARATH, Travancore ou le workflow BIC.

## 3. Méthode de comparaison

Union récursive des fichiers fonctionnels du fork et de la source, hashes SHA-256 via `Get-FileHash`, présence et hash vanilla 1.13, puis inspection ciblée avec `Compare-Object` et `Select-String`. Sont exclus `.git`, métadonnées, rapports, recherche technologique, caches, sauvegardes, captures, temporaires, copie jetable et descripteurs.

Résultat canonique : 534 fichiers fonctionnels différents ou unilatéraux. Les égalités avec vanilla permettent de séparer copies upstream, overrides locaux et contenu réellement spécifique au hotfix. L’inventaire détaillé est `HOTFIX_GLOBAL_DIFFERENCE_INVENTORY.csv`.

## 4. Blocs terminés

- Infrastructure des lois Merchant Banking / Navigation Acts : intégrée par `d43e4f2` après les icônes `eca384e`; les activations de départ GEN/VEN et GBR/colonies restent des deltas séparés à exécuter.
- Mamluk Iraq : chaîne `7cc8068` → `a24fe7e`; verdict administratif `MAMLUK_IRAQ_COMPLETE`, validation statique, runtime à consolider globalement.
- Japon : chaîne `6dde080` → `2228ce8`, correction Ryukyu `72d03a3` et gate EZO `2228ce8`; verdict administratif `JAPAN_HOTFIX_COMPLETE`, validation statique, runtime à consolider globalement.
- Inde : `HOTFIX_5_INDIA_COMPLETE`, commit `50ed582`, avec `SEPOY_RUNTIME_VALIDATION_COMPLETE`, `BOMBAY_TRIGGER_ACCESS_CONFIRMED`, `WEST_BENGAL_RETREAT_TRANSFER_EXPECTED` et `NO_FURTHER_INDIA_GAMEPLAY_FIX_REQUIRED`.

## 5. Blocs partiellement terminés

- Autriche/Croatie/Suisse : paquet complet, contrôles statiques et runtime passés; 30 K habitants en Suisse autrichienne et 2,30 K / 2,30 K marins confirmés.
- DEI : paquet complet; CEY/SAF, Java, Indonésie, refus, drapeaux, nettoyages VOC, économie post-compagnie et persistance après rechargement validés.
- Runtime global : non exécuté pendant C1AI.
- Audit final de branche : à faire après les derniers blocs P0/P1.

## 6. Blocs non examinés

Le prochain travail est `HOTFIX_6A11_RESIDUAL_GLOBAL_SCRIPT_SELECTION`, strictement documentaire. Il doit rapprocher la baseline de 376 diagnostics et 141 fichiers de l'inventaire actualisé, publier exactement trois candidats et en sélectionner un seul sans modifier de gameplay. Ne pas rouvrir DEI/VOC, Balkan National Awakening, Yugoslavia, Risorgimento, nationalisme grec, Grande Crise orientale, Sick Man, Romania, NAVY, BIC, Travancore ou MARATH.

## 7. Contenu hotfix absent du fork

Les deltas Autriche/Croatie/Suisse sont décrits dans la delta map 6A.2. Pour DEI, aucun delta custom hotfix absent n’est prouvé; les sept écarts de l’événement sont identiques hotfix/vanilla 1.13. Aucun import massif n’est autorisé.

## 8. Divergences intentionnelles

Sont notamment intentionnels : setup 1776, relation `HYD -> PUD`, fichiers Japon locaux, tags SKH/ULT, localisations françaises, corrections Australasie, NAVY/ADMIN, BIC et `activate_law = law_type:law_frontier_colonization`.

## 9. Adaptations vanilla 1.13

Le fork conserve les APIs, régions stratégiques, formations, PM administratives et corrections cartographiques compatibles 1.13. Une égalité hotfix/vanilla face à un fork différent n’autorise jamais un remplacement complet.

## 10. Contenu hotfix obsolète

Les fichiers hotfix identiques à vanilla et absents du fork sont classés `OBSOLETE_HOTFIX_CONTENT` : le jeu les fournit déjà et une copie dans le mod augmenterait inutilement la surface d’override.

## 11. Travaux concurrents protégés

`docs/research/technology/` reste non suivi et intact. Le stash `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` reste intact. Aucun hunk de ces travaux n’appartient à C1AI ou 6A.

## 12. MARATH

Statut `CONCURRENT_USER_WORK`. Les collisions principales sont `common/history/buildings/10_india.txt` et `common/history/military_formations/05_military_formations_india.txt`. Le stash n’a été ni appliqué ni inspecté. MARATH n’appartient pas au bloc Russie.

## 13. NAVY

Statut `PROTECTED_EXISTING_WORK`. Les rapports `docs/reports/navy/` couvrent les phases 0 à 3C-2; le travail MARATH 3C-3 reste stashed. Les formations militaires, lois navales, bâtiments et localisations navales ne doivent pas être absorbés par le merge hotfix. Un audit spécifique ne sera ouvert que si un résidu hotfix précis l’exige après 6A.

La migration autonome des huit historiques de formations du commit `c6c9429`,
avec le correctif minimal de douze QG `3b02b2a`, a passé une partie neuve, une
sauvegarde/recharge et deux progressions de trois mois. Le rapport canonique est
`HOTFIX_MILITARY_FORMATIONS_1_13_RUNTIME_QA.md`. Cette preuve ne ferme pas le
bloc NAVY plus large et ne touche pas au stash MARATH.

## 14. ADMIN

Statut `MERGED_STATIC_ONLY` pour les corrections locales documentées par `PHASE_ADMIN_2_GLOBAL_GOVERNMENT_ADMIN_PM_AUDIT.md`. Les fichiers buildings divergent volontairement de la source; aucun remplacement complet n’est autorisé. La validation runtime appartient au runtime global consolidé.

## 15. Technologies

`docs/research/technology/` est `OUT_OF_SCOPE_RESEARCH`. La refonte générale des technologies est `POST_MERGE_DESIGN_BACKLOG`. Aucun changement technologique n’est requis par 6A.

## 16. Amérique

La refonte de la Révolution américaine, Liberty or Death, aide/dette française, Join Ongoing Wars et fédéralisation progressive sont `POST_MERGE_DESIGN_BACKLOG`. Les overrides hotfix américains restent inventoriés mais ne bloquent pas 6A.

## 17. France

États généraux, privilèges des ordres, crise fiscale/frumentaire, intervention française graduelle et chaîne complète de Révolution française sont `POST_MERGE_DESIGN_BACKLOG`. La localisation française existante est protégée.

## 18. Autres régions

Les annonces 2.3 sont corrigées : population suisse autrichienne +30 000 justifiée par le runtime, shipyard niveau 2, administration navale niveau 3, flotte AUS 1+3 entièrement pourvue et Agram 24. Le fork a été positivement monté par le launcher.

## 19. Localisations

Les fichiers français fork-only sont `INTENTIONAL_FORK_DIVERGENCE`. Les localisations Japon corrigées sont conservées. Aucune localisation n’est nécessaire pour le remplacement ciblé de la loi russe.

## 20. Diagnostics globaux connus

Les différences larges de `common/history/states/00_states.txt`, buildings, formations, journal entries et events mélangent setup 1776, vanilla 1.13 et hotfix. Elles exigent des hunks ciblés; le nom identique d’un fichier ne prouve jamais son intégration.

## 21. Copie jetable

Les 984 fichiers ont déjà été audités et aucun gameplay non fusionné n’y existe. Elle n’est utile ni à 6A ni à l’inventaire final. Recommandation unique : `SAFE_TO_RETIRE_DISPOSABLE_AFTER_C1AI_COMMIT`. C1AI ne la supprime pas.

## 22. Prochain bloc recommandé

`HOTFIX-6A_GLOBAL_SCRIPT_DELTAS` reste le conteneur.

La prochaine phase est
`HOTFIX_6A11F_PORTUGUESE_COLONIALISM_TWO_JE_PINNING_1_13_ALIGNMENT`. 6A.11 a
recalculé 376 diagnostics dans 141 fichiers, comparé exactement trois
candidats et sélectionné un correctif d'un fichier, deux objets et deux hunks.
Le conteneur compte toujours 21 fichiers appliqués et 5 encore en attente.
Les 161 anciennes lignes
`PENDING_REVIEW` restent réparties en
7 `REQUIRED_HOTFIX_DELTA`, 16 `VANILLA_1_13_ALIGNMENT_REQUIRED`,
18 `ALREADY_MERGED`, 3 divergences
intentionnelles, 1 contenu hotfix obsolète, 10 backlogs, 19 travaux protégés
et 87 inconnus. Les 110 lignes directement exploitables ne représentent pas
110 correctifs. Le total historique de 26 reste `UNVERIFIED`.

## 23. Pourquoi il vient ensuite

Romania est close et ne doit pas être rouverte. Le colonialisme portugais est
le plus petit alignement P0 encore prouvé : source et vanilla convergent sur
les deux propriétés modernes, tandis que toutes les différences fonctionnelles
adjacentes sont exclues. Merchant Banking, Navigation Acts, Coup, Imperialism
of Promise et les diagnostics Tanzimat restent des pistes séparées.

## 24. Fichiers concernés

6A.11F pourra modifier uniquement
`common/journal_entries/06_portuguese_colonialism.txt`, son rapport,
`docs/reports/hotfix/INDEX.md`, `HOTFIX_REPORT_INDEX.csv`,
`HOTFIX_MERGE_BLOCK_STATUS.csv` et cette roadmap. Deux substitutions d'API
seulement sont autorisées.

## 25. Modèle recommandé

GPT-5.6 Thinking avec raisonnement élevé.

## 26. Besoin de runtime

Un runtime humain condensé sera requis après tous les contrôles statiques.
Codex ne lancera ni ne pilotera le jeu.

## 27. Nombre minimal de lancements

Un lancement humain portugais pour 6A.11F.

## 28. Phases suivantes probables

Après 6A.11F, Merchant Banking GEN/VEN reste le prochain delta hotfix sérieux
et atomique. Navigation Acts requiert un audit distinct pour la divergence
vanilla et la collision GBR/NAVY. Coup, Imperialism of Promise et les trois
diagnostics Tanzimat conservent leurs dettes adjacentes. L'activation Tanzimat
propre à 1776 reste
`OTTOMAN_TANZIMAT_1776_DEFERRED_ACTIVATION_DESIGN_BACKLOG`.

## 29. Critères de fin du merge

Tous P0/P1 terminés; aucun `UNKNOWN_REQUIRES_REVIEW` bloquant; aucun gameplay légitime seulement dans la copie jetable; aucun fichier hotfix requis absent; divergences et adaptations 1.13 documentées; `git diff --check` propre; audit statique et runtime global passés; rapports indexés; copie retirée au bon moment; branche propre; stash MARATH et recherche technologique intacts; fusion finale préparée.

## 30. Audit global final

Rejouer l’inventaire hash, vérifier les références, doublons, encodages, accolades et changements attendus, puis confirmer que seuls les résidus documentés subsistent.

## 31. Runtime global final

Un lancement consolidé doit couvrir chargement 1776, RUS, IR1/TUR/PER, Japon, BIC/Sepoy, NAVY/ADMIN en non-régression et `error.log`. Tous les scénarios doivent être préparés avant l’ouverture du jeu. La QA formations 1.13 fournit déjà une preuve ciblée pour RUS, TUR/PER, Japon, BIC et les formations NAVY, mais ne remplace pas le smoke final après fermeture des blocs P0/P1.

## 32. Retrait de la copie jetable

Autorisé après commit manuel de C1AI : `SAFE_TO_RETIRE_DISPOSABLE_AFTER_C1AI_COMMIT`. Le retrait reste une action séparée et la copie ne doit jamais être intégrée au fork.

## 33. Fusion de branche

Après audit et runtime globaux, vérifier branche propre, stash intact, recherche intacte, puis préparer la fusion sans commit automatique dans les phases d’audit.

## 34. Backlog post-merge

Les refontes Amérique, France, technologies, agriculture/alimentation/industrie et fédéralisation des Treize Colonies sont séparées sous `POST_MERGE_DESIGN_BACKLOG` et ne bloquent pas le merge.

## 35. Risques

Principaux risques : remplacement complet de fichiers globaux, collision NAVY/ADMIN/MARATH, régression BIC vers `law_colonial_exploitation`, perte de localisation française, réouverture indue des blocs clos et confusion entre copie vanilla et contenu hotfix custom.

## 36. Verdict

`NEXT_MERGE_BLOCK = HOTFIX-6A_GLOBAL_SCRIPT_DELTAS`  
`NEXT_EXECUTION_PHASE = HOTFIX_6A11F_PORTUGUESE_COLONIALISM_TWO_JE_PINNING_1_13_ALIGNMENT`
`AUSTRIA_CROATIA_WEST_SWITZERLAND_TARGETED_FIX_COMPLETE`
`HOTFIX_6A3_DEI_TARGETED_AUDIT_COMPLETE`
`HOTFIX_6A3R_DEI_BREAKUP_HUNK_RESOLUTION_COMPLETE`
`HOTFIX_6A3F_DEI_TARGETED_FIX_COMPLETE`
`HOTFIX_6A4_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE`
`HOTFIX_6A4F_BALKAN_NATIONAL_AWAKENING_1_13_COMPLETE`
`HOTFIX_6A5_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE`
`HOTFIX_6A5F_YUGOSLAVIA_JE_PINNING_1_13_STATIC_PASS`
`HOTFIX_6A5F_YUGOSLAVIA_JE_PINNING_1_13_RUNTIME_PASS`
`HOTFIX_6A5F_YUGOSLAVIA_JE_PINNING_1_13_COMPLETE`
`HOTFIX_6A6_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE`
`HOTFIX_6A6F_ITALIAN_UNIFICATION_JE_PINNING_1_13_STATIC_PASS`
`HOTFIX_6A6F_ITALIAN_UNIFICATION_JE_PINNING_1_13_RUNTIME_PASS`
`ITALIAN_UNIFICATION_JE_PINNING_1_13_ALIGNED`
`ITALIAN_1776_YEAR_GATE_PRESERVED`
`GEOGRAPHY_UNCHANGED`
`HOTFIX_6A6F_ITALIAN_UNIFICATION_JE_PINNING_1_13_COMPLETE`
`HOTFIX_6A7_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE`
`HOTFIX_6A7F_GREEK_NATIONALISM_1_13_STATIC_PASS`
`HOTFIX_6A7F_GREEK_NATIONALISM_1_13_RUNTIME_PASS`
`GREEK_NATIONALISM_MONARCHY_TRIGGER_1_13_ALIGNED`
`GREEK_NATIONALISM_JE_PINNING_1_13_ALIGNED`
`GREEK_VISIBILITY_AND_GEOGRAPHY_UNCHANGED`
`HOTFIX_6A7F_GREEK_NATIONALISM_1_13_API_ALIGNMENT_COMPLETE`
`HOTFIX_6A8R_GREAT_EASTERN_CRISIS_1_13_AUDIT_COMPLETE`
`GREAT_EASTERN_CRISIS_SIX_HUNK_DECISION_RECORDED`
`HOTFIX_6A8F_GREAT_EASTERN_CRISIS_1_13_STATIC_PASS`
`HOTFIX_6A8F_GREAT_EASTERN_CRISIS_1_13_RUNTIME_PASS`
`GREAT_EASTERN_CRISIS_SIX_HUNK_1_13_ALIGNMENT_COMPLETE`
`GREAT_EASTERN_CRISIS_GEOGRAPHY_VISIBILITY_AND_PINNING_VALIDATED`
`OTTOMAN_TANZIMAT_1776_ROUTE_REQUIRES_DOCUMENTARY_AUDIT`
`HOTFIX_6A8F_GREAT_EASTERN_CRISIS_1_13_ALIGNMENT_COMPLETE`
`HOTFIX_6A9R_OTTOMAN_TANZIMAT_1776_ENTRY_CHAIN_AUDIT_COMPLETE`
`OTTOMAN_TANZIMAT_1776_ENTRY_CHAIN_DECISION_RECORDED`
`SICK_MAN_EIGHT_JE_PINNING_1_13_DECISION_RECORDED`
`OTTOMAN_TANZIMAT_START_DISABLED_IN_1776_PRESERVED`
`OTTOMAN_TANZIMAT_1776_DEFERRED_ACTIVATION_DESIGN_BACKLOG`
`SICK_MAN_EIGHT_JE_PINNING_CAN_BE_ALIGNED_INDEPENDENTLY`
`HOTFIX_6A9F_SICK_MAN_EIGHT_JE_PINNING_1_13_STATIC_PASS`
`SICK_MAN_EIGHT_JE_PINNING_EIGHT_HUNK_1_13_ALIGNMENT_COMPLETE`
`NO_TANZIMAT_ACTIVATION_CHANGED`
`HOTFIX_6A9F_SICK_MAN_EIGHT_JE_PINNING_1_13_RUNTIME_PASS`
`SICK_MAN_EIGHT_JE_PINNING_PARSER_ERRORS_8_TO_0`
`HOTFIX_6A9F_SICK_MAN_EIGHT_JE_PINNING_1_13_ALIGNMENT_COMPLETE`
`HOTFIX_6A10_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE`
`HOTFIX_6A10F_ROMANIA_TWO_JE_PINNING_1_13_STATIC_PASS`
`ROMANIA_TWO_JE_PINNING_TWO_HUNK_1_13_ALIGNMENT_COMPLETE`
`HOTFIX_6A10F_ROMANIA_TWO_JE_PINNING_1_13_RUNTIME_PASS`
`ROMANIA_TWO_JE_PINNING_PARSER_ERRORS_2_TO_0`
`ROMANIA_1776_VISIBILITY_GEOGRAPHY_AND_PROGRESSION_UNCHANGED`
`HOTFIX_6A10F_ROMANIA_TWO_JE_PINNING_1_13_ALIGNMENT_COMPLETE`
`HOTFIX_6A11_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE`
`NO_GAMEPLAY_CHANGED`
`GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`

## 37. Mise à jour DEI 6A.3F — 28 juillet 2026

Les hunks territoriaux et les sept alignements vanilla 1.13 sont appliqués. Le runtime monté a confirmé `CEY`, `SAF`, le nom `Java` et le retrait des reliquats VOC. Deux anomalies révélées par ce runtime ont été corrigées dans le même périmètre autorisé :

- le drapeau post-VOC de Java est désormais piloté par `jav_post_voc_flag_var`, sans réutiliser la variable de nom colonial `malaya_subject_var` ;
- `dei_breakup.2` remplace l’économie d’extraction après l’indépendance, sans laissez-faire et avec des seuils technologiques et politiques pour le Mouvement agraire et l’interventionnisme.

Le filewatcher charge trois événements sans erreur propre à `dei_breakup.2`. Le runtime confirme le drapeau Java et les choix économiques limités ; le texte économique a été développé au même format narratif que « Jour de l’indépendance ». Après choix du Mouvement agraire, le nom Java, son drapeau et la loi persistent après sauvegarde/rechargement. La branche Indonésie et l’option de refus sont également validées.

Le transfert britannique du Cap et de Ceylan alors que la VOC reste un sujet néerlandais n’a pas été ajouté. Il dépend historiquement des lettres de Kew et du cycle Révolution française/guerres napoléoniennes ; il est donc reporté à cette future phase et ne rouvre pas 6A.3F.
