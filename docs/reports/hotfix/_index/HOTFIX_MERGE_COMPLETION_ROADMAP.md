# HOTFIX — Roadmap de fin du merge global

## 1. Résumé

Le bloc canonique reste `HOTFIX-6A_GLOBAL_SCRIPT_DELTAS`. La Russie est corrigée au commit `991f6a1`. Le paquet 6A.2 est clos par 6A.2F2. La phase DEI/VOC est close par `HOTFIX_6A3F_DEI_TARGETED_FIX_COMPLETE`, après validation statique, runtime des trois branches et sauvegarde/rechargement. La sélection 6A.4 a relu les 161 lignes `PENDING_REVIEW`, puis l’alignement balkanique 6A.4F a supprimé ses 51 erreurs propres. L’alignement de `je_yugoslavia` est clos : une Serbie libérée comme sujet ottoman peut accéder à la formation yougoslave, la session atteint le 25 janvier 1776 et l’erreur ciblée disparaît. Le prochain sous-bloc est la sélection documentaire 6A.6.

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

Le prochain travail est `HOTFIX_6A6_RESIDUAL_GLOBAL_SCRIPT_SELECTION`, strictement documentaire. Il doit comparer les résidus actualisés, publier trois candidats et sélectionner exactement un sous-bloc sans modifier de gameplay. Ne pas rouvrir DEI/VOC, Balkan National Awakening, Yugoslavia, NAVY, BIC, Travancore ou MARATH.

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

La prochaine phase atomique est
`HOTFIX_6A6F_ITALIAN_UNIFICATION_JE_PINNING_1_13_ALIGNMENT`. La sélection
6A.6 a analysé les 389 erreurs restantes de l’ancienne API dans 146 fichiers et
a publié exactement trois candidats. `je_risorgimento` est retenue : une erreur
parser directe, un fichier, un objet, un hunk et une convergence exacte entre
la source hotfix et vanilla 1.13. Les 161 anciennes lignes `PENDING_REVIEW`
restent réparties en 7 `REQUIRED_HOTFIX_DELTA`, 20
`VANILLA_1_13_ALIGNMENT_REQUIRED`, 14 `ALREADY_MERGED`, 3 divergences
intentionnelles, 1 contenu hotfix obsolète, 10 backlogs, 19 travaux protégés
et 87 inconnus. Les 114 lignes directement exploitables ne représentent pas
114 correctifs. Le total historique de 26 reste `UNVERIFIED`.

## 23. Pourquoi il vient ensuite

La comparaison trois voies de `00_italian_unification.txt` isole un remplacement
de propriété sans autre dette fonctionnelle dans le hunk. Merchant Banking
GEN/VEN et Navigation Acts GBR/HBC/NBS/ONT/ORA restent respectivement classés
2 et 3, mais ne disposent pas de l’erreur parser P0 et touchent davantage de
fichiers.

## 24. Fichiers concernés

La phase 6A.6F peut modifier uniquement
`common/journal_entries/00_italian_unification.txt`, l’objet
`je_risorgimento`, par un remplacement de ligne :
`should_be_pinned_by_default = yes` devient
`should_be_pinned_by_default_uninvolved_or_context = yes`. Le remplacement du
fichier complet est interdit. La limite intentionnelle `year >= 1836` et la
géographie actuelle doivent rester inchangées. Les paquets 6A.3F, 6A.4F et
6A.5F restent protégés.

## 25. Modèle recommandé

GPT-5.6 Thinking avec raisonnement élevé.

## 26. Besoin de runtime

La phase 6A.6F exigera un runtime exclusivement humain après le PASS statique.
Codex ne lancera ni Victoria 3 ni le launcher, ne contrôlera pas l’interface et
s’arrêtera avec `RUNTIME_OPERATOR_ACTION_REQUIRED`. L’opérateur inspectera une
partie neuve 1776 avec un pays de culture principale italienne, vérifiera
l’entrée potentielle Risorgimento, avancera d’au moins un jour, puis fermera le
jeu et le launcher avant toute analyse de logs.

## 27. Nombre minimal de lancements

Un seul lancement humain condensé est prévu pour 6A.6F. Aucun lancement ne doit
être effectué par Codex.

## 28. Phases suivantes probables

Après 6A.6F, Merchant Banking GEN/VEN et Navigation Acts
GBR/HBC/NBS/ONT/ORA restent respectivement les candidats classés 2 et 3. Ils ne
font pas partie du périmètre italien. Le contenu des lettres de Kew reste
séparé dans la future phase Révolution française/Napoléon.

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
`NEXT_EXECUTION_PHASE = HOTFIX_6A6F_ITALIAN_UNIFICATION_JE_PINNING_1_13_ALIGNMENT`
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
`NO_GAMEPLAY_CHANGED`
`GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`

## 37. Mise à jour DEI 6A.3F — 28 juillet 2026

Les hunks territoriaux et les sept alignements vanilla 1.13 sont appliqués. Le runtime monté a confirmé `CEY`, `SAF`, le nom `Java` et le retrait des reliquats VOC. Deux anomalies révélées par ce runtime ont été corrigées dans le même périmètre autorisé :

- le drapeau post-VOC de Java est désormais piloté par `jav_post_voc_flag_var`, sans réutiliser la variable de nom colonial `malaya_subject_var` ;
- `dei_breakup.2` remplace l’économie d’extraction après l’indépendance, sans laissez-faire et avec des seuils technologiques et politiques pour le Mouvement agraire et l’interventionnisme.

Le filewatcher charge trois événements sans erreur propre à `dei_breakup.2`. Le runtime confirme le drapeau Java et les choix économiques limités ; le texte économique a été développé au même format narratif que « Jour de l’indépendance ». Après choix du Mouvement agraire, le nom Java, son drapeau et la loi persistent après sauvegarde/rechargement. La branche Indonésie et l’option de refus sont également validées.

Le transfert britannique du Cap et de Ceylan alors que la VOC reste un sujet néerlandais n’a pas été ajouté. Il dépend historiquement des lettres de Kew et du cycle Révolution française/guerres napoléoniennes ; il est donc reporté à cette future phase et ne rouvre pas 6A.3F.
