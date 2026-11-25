## Mise à jour expérimentale — 17 novembre 2026, HRE mensuel et état initial

**Essais exécutés sur le PC Windows. Le HRE mensuel ne résout pas la lenteur ; le signal principal concerne l’IA. Aucun correctif préservant le gameplay n’est validé.**

### Contrôleur HRE mensuel seul : ordre normal–diagnostic–diagnostic–normal

Même S0 France du 1er janvier 1776, Steam 1.15.1 sans DLC de gameplay, même runtime figé avec COMPACT, réglages, sondes DAY et vitesse 5. Seul le corps de `aor1776_hre_monthly_hook` est neutralisé dans une copie externe. Définitions HRE quotidiennes et IA régionale normales. L’appel de planification contenu dans le hook mensuel disparaît nécessairement avec lui ; la chaîne quotidienne déjà programmée reste présente.

| Passage réel | 14 jours | 28 jours | 56 jours |
|---|---:|---:|---:|
| HMC1 normal | 35 s | 68 s | 122 s |
| HMM1 mensuel HRE désactivé | 36 s | 69 s | 122 s |
| HMM2R mensuel HRE désactivé | 37 s | 71 s | 125 s |
| HMC2 normal | 37 s | 71 s | 125 s |

**Bypass réellement exécuté** : traces natives aux 1er février, mars et avril dans les deux diagnostics, aucune dans les témoins. La fenêtre initiale de 56 jours inclut février ; les prises se poursuivent au-delà de 100 jours. HMM2 interrompu en pause avant simulation est exclu.

Les deux paires donnent exactement le même temps sur 56 jours. Cela affaiblit l’explication d’un gros surcoût net de ce contrôleur, sans exclure des coûts faibles, compensations ou autres effets HRE. Les ablations précédentes du quotidien HRE et du mensuel régional restent conservées ; elles ne démontrent pas que toutes leurs initialisations déjà appliquées dans S0 sont sans effet.

### Expérience suivante réellement exécutée : toute l’IA désactivée

Runtime normal et instrumentation commune aux deux passages : CPU par thread, interface de commandes isolée, invocation native TickTask. Aucun profilage Legacy des scripts pendant les premières fenêtres comparées.

| Passage comparable | 14 jours | 28 jours | 56 jours | CPU moyen sur 16 processeurs logiques |
|---|---:|---:|---:|---:|
| ENG_ON2, IA normale | 47 s | 87 s | 149 s | 20,93 % |
| ENG_OFF2, `disable_ai all` | 8 s | 15 s | 29 s | 17,67 % |

**Preuve en sauvegarde après exécution : 646 contrôleurs IA `enabled=no`, zéro `yes`**, contre 646 `yes` dans la source. Nouvelle sauvegarde distincte du 19 avril 1776, SHA256 `4f55dfaf2108b3f1ab24601e99efbcc94c0e3fbbf537df8427c9b5f21cb52273`. Aucun pays, POP ou contenu historique retiré.

Signal descriptif : environ **80,5 % de temps en moins**, débit **×5,14**, sur **une paire**. L’ordre inverse n’a pas encore été répété. Les décisions supprimées et scripts évalués par l’IA peuvent contribuer : ce contrôle ne localise pas une fonction C++, ne sépare pas économie/diplomatie/militaire, et n’est pas une optimisation jouable.

### Janvier puis juillet, même processus et même profilage

Une troisième campagne normale PROF_INIT active le profilage Legacy avant le premier tick, conservé dans les deux fenêtres. Une sauvegarde réelle du **1er juillet 1776** est créée, vérifiée et préservée, puis la simulation reprend.

| Monde dans PROF_INIT | 14 jours | 28 jours | 56 jours |
|---|---:|---:|---:|
| Janvier initial | 45 s | 85 s | 148 s |
| À partir du 2 juillet | 9 s | 18 s | 39 s |

CPU moyen sur 56 jours : 21,09 % dans les deux groupes. L’accélération apparaît donc déjà avant avril 1777. Les pauses d’avril et juillet sont exclues des fenêtres retenues. L’ancien contrôle mature avant/après deux redémarrages (33/33/31 s sur 56 jours) est conservé, pas présenté comme un nouvel essai.

### Sauvegardes normales : observations, sans attribution causale

Juillet et août sont deux branches normales distinctes issues de S0 ; avril 1777 vient de MATURE1. Ce n’est pas une trajectoire déterministe unique.

| Indicateur sérialisé | Janvier 1776 | Juillet 1776 | Avril 1777 |
|---|---:|---:|---:|
| Population, personnes | 837 119 763 | 844 171 394 | 855 592 042 |
| Objets POP | 31 475 | 26 133 | 28 217 |
| Bâtiments avec profit après réserves négatif | 2 188 | 950 | 1 226 |
| Main-d’œuvre salariée | 31 577 271 | 30 421 044 | 29 968 816 |
| Main-d’œuvre au chômage | 1 833 128 | 2 283 212 | 3 720 647 |
| États en déficit d’infrastructure | 40 | 199 | 234 |
| Entrées `country_goal` IA | 38 090 | 38 493 | 38 227 |
| Formations militaires enregistrées | 258 | 1 473 | 1 469 |

Les populations calculées indépendamment par pays et par État concordent. 465 ensembles de PM changent en juillet parmi 6 597 identifiants ayant conservé type et État ; 581 parmi 6 570 en avril 1777. Les listes de stratégies restent identiques entre janvier et juillet pour les 643 pays peuplés comparables. Les objectifs enregistrés ne se vident pas globalement ; ils ne sont pas une longueur de file exécutable démontrée.

Les sections natives `tasks` contiennent 34/267/272 entrées, avec des `update_index` ultérieurs dans les tâches de chômage, commerce d’esclaves et objectifs IA. Les cooldowns régionaux enregistrés passent de 75 à 25 puis 12 occurrences. Ces différences sont persistantes et observables, mais ne prouvent ni coût, ni cache causal, ni effet d’une date précise. Les objets sérialisés de marchés, guerres et traités ne sont pas des décomptes garantis d’objets actifs ; les échecs IA cumulés ne sont pas des taux de calcul.

### Profilage : obtenu, et limites

- Export Legacy initial réel : **4 994 lignes** (4 065 triggers, 863 script_values, 66 effets). Plus gros emplacement observé, `20_law_commitment.txt:108` : **2,049 s / 8 595 appels**, du départ au 3 avril. Score régional IA `00_default_strategy.txt:4526` : **0,745 s / 73 274 appels**. Le dump cumulatif de juillet conserve les 4 969 emplacements initiaux, tous monotones en temps et appels.
- La somme brute des lignes n’est **pas du CPU exclusif** : imbrication et couverture partielle. Les effets HRE/régionaux ne sont pas tous identifiables dans cet export. Aucun hotspot observé n’explique à lui seul l’écart, sans exonération générale des scripts. Aucun filtre de lois réordonné ni autre optimisation spéculative.
- CPU par thread réel : deux TID sans nom représentent environ 49 % du CPU échantillonné dans le contrôle initial. Sans noms, piles ou symboles, aucune attribution « thread économie/simulation ».
- `log_ticktask_performance` invoqué mais aucun `profiling.log` exploitable obtenu. **WPR échoue avant enregistrement avec 0xc5585011**, y compris après la seconde tentative hors des restrictions de l’outil d’exécution : Windows refuse l’activation de la politique de profilage. La revue automatique avait autorisé cette tentative ; elle ne certifie pas des droits administrateur Windows, non attestés ici. Aucun ETL CPU, aucun réglage de sécurité modifié ; WPR est inactif ensuite.

### Interprétation et prochaine expérience

L’explication **C, travail associé à l’IA réagissant au scénario initial**, gagne le plus de soutien. **A**, calculs nécessaires mais chers, reste compatible. **B**, répétitions scriptées, n’est pas expliquée par les trois contrôleurs testés, sans exclusion de tous les scripts. **D**, date/état temporaire ou persistant, reste plausible mais non séparée de l’évolution économique.

On ne sait pas encore distinguer travail nécessaire et tentatives redondantes. Ni cache, ni fréquence réduite, ni préinitialisation équivalente ne sont validés ; aucune possibilité de déplacer le coût vers le chargement n’est supposée.

**Suite recommandée, non encore exécutée :** répéter d’abord IA OFF → IA ON, même S0 et instrumentation, puis isoler uniquement les contrôleurs des pays décentralisés dans une copie de S0, sans supprimer pays/POPs/histoire. Les tables identifient 244 pays décentralisés peuplés, 400 autres pays peuplés et deux contrôleurs non classés dans cette table ; vérifier leur état réellement chargé. Une seule variable à chaque prise, ordre inverse si petit signal. Cette partition peut orienter vers le groupe des principales décisions économiques/diplomatiques ou vers l’autre groupe ; elle ne sera toujours pas une correction préservant le gameplay.

### Préservation, preuves et limites de mesure

Audit : **2 996/2 996 fichiers runtime du mod inchangés**, COMPACT inclus ; **79/80 fichiers suivis du profil normal inchangés**, toutes les sauvegardes suivies comprises. Seul écart binaire : `launcher-v2.sqlite`. Index/HEAD, exécutable, 3 fichiers Russie–Kazakh et preuves/outils antérieurs conservés. Aucun Git d’écriture.

**Lanceur examiné sans restauration :** base saine ; mêmes 7 playsets, 11 associations de mods et 51 associations DLC que la référence historique B2, positions et activations des liens identiques. Les cinq champs de sélection/usage/synchronisation diffèrent ; les autres champs de playsets sont identiques. La copie exacte de la base du début de mission n’étant pas disponible, ni le détail binaire ni son auteur ne sont attribués. Sélection actuelle laissée en place. Ce contrôle n’est pas artificiellement déclaré 80/80.

24 fenêtres finales vérifiées, timestamps natifs à une seconde, première journée partielle et pauses exclues, aucun FPS. L’ancienne référence 93 s, la série HRE 122–125 s et les contrôles ultérieurs 148–149 s reflètent des lots différents : **pas de comparaison transversale présentée comme gain**. La dernière ligne tronquée du log PROF_INIT est conservée brute et exclue uniquement dans une copie d’analyse séparée. Les processus instrumentés ont été fermés par leur lanceur après mesures/sauvegardes ; leur EXIT -1 est documenté.

Rapport local détaillé : `docs/reports/performance/INITIAL_SIMULATION_ISSUE56_2026_11_17/STATE_INVESTIGATION_2026_11_17/REPORT_FR.md`, avec CSV des mesures, synthèse JSON, qualité et audit. **Fichiers locaux non commités**, pas de lien blob prétendant qu’ils sont publiés.

Preuves volumineuses hors dépôt : `C:/Users/simeo/AppData/Local/Temp/aor56_state_20261117`. Sauvegarde juillet normale : `profiles/PROF_INIT/save games/royaume de france_1776_07_01.v3`, SHA256 `5bdd727a6e725be42677b51dc7e4a2f1d1e6bb54836d159d0384575fea0197fa`. Les anciens laboratoires restent intacts.

**Enquête ouverte. Aucun correctif de production, aucune suppression de contenu historique, aucune fusion spéculative.**
