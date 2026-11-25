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
- `log_ticktask_performance` invoqué mais aucun `profiling.log` exploitable obtenu. **WPR échoue avant enregistrement avec 0xc5585011**, y compris lors de l’essai élevé : Windows refuse l’activation de la politique de profilage. La revue automatique avait accepté l’élévation. Aucun ETL CPU, aucun réglage de sécurité modifié ; WPR est inactif ensuite.

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


---

## Historique conservé — bilan précédent

## Mise à jour expérimentale — 17 novembre 2026 : rechargement mature exécuté et répété

**Le ralentissement fort du début de campagne ne revient pas dans les deux rechargements testés du monde mature.** La cause précise de la lenteur initiale reste ouverte ; aucun correctif de production n’est validé. Enquête de simulation distincte de [#54 / COMPACT](https://github.com/Malzars-sys/1776-Age-of-Revolutions/issues/54).

### Contrôle prioritaire réellement exécuté

Une nouvelle France initiale commune a été simulée à vitesse 5 jusqu’au **21 avril 1777**, environ seize mois. La lenteur avait déjà disparu : 14 jours en 7 s dans la fenêtre de janvier 1777. Une sauvegarde réelle a été créée, vérifiée puis conservée intacte : `royaume de france_1777_04_21.v3`, version 1.15.1, 122 443 314 octets, SHA256 `879867ccd58f230c9eef2fbe04570171679cea015010e713be5c746707b732eb`.

Performance mesurée après sauvegarde et avant redémarrage, puis **fermeture complète et deux nouveaux processus indépendants** rechargeant exactement cette sauvegarde. Même exécutable Steam 1.15.1, même COMPACT/runtime figé, mêmes réglages, vitesse 5 et aucun DLC de gameplay. L’installation locale 1.15.0 avec DLC reste distincte et n’a pas été utilisée.

Les bornes DAY prennent les timestamps natifs du moteur, jamais l’arrivée tamponnée des logs. Départ au premier jour complet après S, mêmes dates dans les trois passages. Pause, préparation, menus, chargement et compilation des shaders exclus.

| Passage | 14 jours | 28 jours | 56 jours | 56 jours suivants |
|---|---:|---:|---:|---:|
| Monde mature, avant redémarrage | 9 s | 17 s | 33 s | 38 s |
| Monde mature, rechargement 1 | 9 s | 17 s | 33 s | 35 s |
| Monde mature, rechargement 2 | 8 s | 16 s | 31 s | 36 s |

Tranches successives de 14 jours pendant les 112 premiers jours :
- Avant redémarrage : 9 / 8 / 8 / 8 / 8 / 10 / 10 / 10 s.
- Rechargement 1 : 9 / 8 / 8 / 8 / 8 / 9 / 9 / 9 s.
- Rechargement 2 : 8 / 8 / 8 / 7 / 9 / 9 / 9 / 9 s.

**Aucun retour d’une phase lente longue, transitoire ou persistante, n’est observé dans les journées complètes mesurées.** Le premier jour partiel, les effets pendant la préparation en pause et les effets plus courts ne sont pas évalués. Pas de redémarrage Windows ni de purge des caches fichiers/shaders.

### Contrôle positif contemporain : le monde initial reste lent

Après les deux rechargements matures, un nouveau processus recharge la même sauvegarde initiale du 1er janvier 1776 que les références antérieures : **27 / 52 / 93 s pour 14 / 28 / 56 jours**, puis 51 s pour les 56 jours suivants. Tranches de 14 jours : 27 / 25 / 22 / 19 / 17 / 12 / 12 / 10 s.

L’écart reste donc lié au monde initial ou à son évolution persistante dans cette configuration ; un simple nouveau processus ne suffit pas à le reproduire dans le monde mature. Cela oriente vers l’état initial, les files/priorités IA, l’économie, les conditions datées, les variables temporaires ou des données/caches sérialisés, **sans identifier une fonction causale**.

CPU moyen sur les 56 premiers jours, en % des 16 processeurs logiques : avant redémarrage 18,9 %, rechargements 19,5 % et 19,8 %, témoin initial 22,7 %. RAM résidente moyenne : 8,37 / 16,26 / 16,15 / 16,34 Gio. La résidence Windows varie fortement et ne prouve pas une cause mémoire. Échantillonnage 500 ms ; résolution temporelle native <1 s ; applications tierces, mémoire globale et fréquences pas entièrement contrôlées.

### Expérience suivante choisie ET exécutée : mensuel régional seul

À partir de la même sauvegarde initiale, une copie diagnostique retire **uniquement le corps du child `aor1776_ai_regional_infrastructure_monthly`**, dans `common/on_actions/13_1776_ai_regional_infrastructure.txt`. Tous les autres fichiers du runtime sont identiques, notamment HRE quotidien/mensuel, pays, POP et contenu historique. Le parent natif et les autres enfants restent actifs. **Six traces du bypass mensuel ont été observées en jeu.**

| Intervalle initial | Témoin contemporain INIT_REF1 | Mensuel régional désactivé INFRA_M0 |
|---|---:|---:|
| 14 jours | 27 s | 28 s |
| 28 jours | 52 s | 53 s |
| 56 jours | 93 s | 96 s |
| 56 jours suivants | 51 s | 52 s |

**Aucun gain net observé.** Les +3,2 % de temps sur 56 jours ne démontrent pas une aggravation reproductible : une seule prise diagnostique, faible écart et variabilité. CPU moyen 22,4 %, RAM résidente 16,43 Gio. L’ablation inclut les conséquences des décisions retirées et ne mesure pas le coût CPU interne pur d’une fonction.

L’initialisation régionale avait déjà été appliquée avant la sauvegarde initiale commune. Ce test retire seulement l’activité mensuelle ultérieure ; il n’exonère ni l’initialisation ni ses effets persistants. Isoler celle-ci nécessiterait des nouvelles campagnes comparables, pas simplement supprimer un hook au rechargement.

Source SHA256 `f1b3ccf92a807581434f21dd902828a94ee2308fe433d530c04493a43975fdeb` ; diagnostic `4923839eb6a320c636a0cb74d355e559833103ad0e61a22a052fbafbf6d18048`. Cette suppression n’est pas une optimisation équivalente, n’est pas installée dans le mod principal et n’a pas été fusionnée.

### Suite recommandée, une variable à la fois

1. **Isoler le child HRE mensuel seul**, depuis la sauvegarde initiale, avec quotidien HRE et infrastructures régionales normaux. Le précédent contrôle quotidien ne couvre pas le mensuel.
2. Pour certifier un petit effet, répéter témoin/diagnostic dans l’ordre inverse. Une initialisation régionale séparée demande des nouvelles campagnes dès leur création.
3. Si les contrôles scriptés ne donnent pas de signal, profiler le moteur et les états persistants IA/emploi/marchés/variables datées. Aucun retrait de pays ou de contenu historique.

Les résultats sont en mode debug avec sondes identiques. Une validation 1.15.0 avec DLC serait une série séparée. Aucun FPS moyen n’est revendiqué.

### Préservation et preuves

Audit final : **2 996/2 996 fichiers runtime normaux, 80/80 fichiers suivis du profil normal et sauvegardes, 3/3 fichiers Russie–Kazakh, 233 preuves antérieures, index Git, HEAD, COMPACT et exécutable inchangés.** Aucun commit/push/fusion ni changement des installations normales. Les cinq processus d’essai sont fermés ; sauvegarde mature et profils isolés conservés.

Rapport détaillé et preuves préparés localement, sans commit :
`docs/reports/performance/INITIAL_SIMULATION_ISSUE56_2026_11_17/RELOAD_EXPERIMENT_2026_11_17/REPORT_FR.md`.

Dans ce dossier : `MATURE_SAVE.json`, `MATURE_BEFORE_RESTART.json`, `RELOAD1_RESULTS.json`, `RELOAD2_RESULTS.json`, `INIT_REF1_RESULTS.json`, `INFRA_M0_RESULTS.json`, `MEASUREMENTS.csv`, `SUMMARY.json`, variantes et audits avant/après. Les anciens bilans sont conservés ci-dessous pour historique : leur mention de rechargement non exécuté est désormais dépassée.

**Statut : expérience prioritaire accomplie et répétée ; cause initiale et correction équivalente encore à établir. L’issue reste ouverte.**

<details>
<summary>Bilan précédent conservé pour historique — avant le contrôle de rechargement</summary>

## Bilan expérimental du 17 novembre 2026 — problème reproduit, cause encore ouverte

Enquête de **simulation**, distincte de [#54 (interface technologique COMPACT)](https://github.com/Malzars-sys/1776-Age-of-Revolutions/issues/54). Aucun correctif de simulation préservant le gameplay n’est validé.

### Environnement et méthode

Tests effectués sur le PC Windows local, Steam **Victoria 3 1.15.1 sans DLC de gameplay**, arbre technologique fermé. Même exécutable, mêmes réglages graphiques et télémétrie, vitesse 5 pour les prises retenues. L’installation locale 1.15.0 avec DLC n’est pas utilisée comme témoin.

Référence main : `bd776919f625016cb9e63b2359cc04796c681ef5`. Copies de runtime et profils d’essai isolés ; référence et diagnostic depuis la même sauvegarde France initiale. Vanilla : nouvelle France en 1836, donc monde et date différents. Le pilote mod est une nouvelle partie ; les références principales mod sont des rechargements de la sauvegarde initiale.

Les mesures utilisent les **heures natives HH:mm:ss** des événements de borne, pas l’arrivée des journaux, qui sont tamponnés. CPU cumulé et working set du processus échantillonnés à 500 ms. Démarrage, compilation des shaders, création du monde et menus exclus. Résolution temporelle <1 s ; pourcentages CPU sur 16 processeurs logiques. Aucun FPS moyen inventé.

Le calendrier moteur observé a 365 jours : les fenêtres commencent les 2 janvier, 1er février, 2 avril, 2 juillet et 2 janvier suivant, et durent 14 jours simulés. Absence de pause et premier plan non certifiés automatiquement ; environnement Windows et mémoire globale non entièrement contrôlés.

### Temps réel pour 14 jours simulés

| Fenêtre | Vanilla 1836 | Main MAIN2 | Main répété MAIN3 | Sans rappel quotidien HRE1 |
|---|---:|---:|---:|---:|
| Janvier | 10 s | 33 s | 32 s | 33 s |
| Février | 8 s | 25 s | 25 s | 24 s |
| Avril | 8 s | exclu¹ | 13 s | 13 s |
| Juillet | 10 s | 10 s | 9 s | 10 s |
| Janvier suivant | 10 s | 8 s | exclu² | 8 s |

¹ MAIN2 avril : intervention sur un événement pendant la fenêtre ; brut 14 s conservé mais exclu.
² MAIN3 dernier janvier : vitesse réduite pour préparer une sauvegarde, sans retour vérifié à 5 ; brut 193 s conservé mais **inutilisable comme benchmark à vitesse 5**.

Le pilote de nouvelle partie mod donne 39 s sur les 14 premiers jours, puis a été interrompu par une erreur de lecture partagée du collecteur, corrigée avant les autres séries. Ce pilote n’est pas assimilé à un crash du jeu.

**Le ralentissement initial et son atténuation sont reproduits.** Le mod est environ 3,2–3,3 fois plus lent en janvier dans les références chargées, puis les prises de juillet deviennent proches. Il ne s’agit pas d’un gain mesuré de FPS.

### Ablation impériale ciblée

Un seul fichier diffère dans la copie diagnostic : `common/scripted_effects/1776_imperial_constitution.txt`. Le helper `aor1776_hre_schedule_membership_guard` ne reprogramme plus le garde quotidien et écrit une trace de bypass. Une première exécution déjà programmée peut subsister dans la sauvegarde ; le mensuel et les autres helpers restent actifs. Les traces du helper diagnostic sont effectivement observées en jeu.

| Intervalle initial | Main MAIN2 | Main MAIN3 | HRE1 | Vanilla |
|---|---:|---:|---:|---:|
| 28 jours | 61 s | 61 s | 60 s | 18 s |
| 56 jours | 108 s | 109 s | 106 s | 37 s |

Cette ablation **ne supprime pas le ralentissement initial**. Un petit coût de quelques pour cent reste possible, mais une seule série diagnostique et la variabilité ne permettent pas de valider ce gain. Le contrôleur mensuel HRE n’a pas été isolé. L’ablation retire une fonction de gameplay : **elle ne constitue pas une correction équivalente à intégrer**.

Source SHA256 `af7940c6fc8d9c2d0eb841d210c05fc29ad16475b989d2e7a8a679e54e26362f` ; candidat lancé `af4137bcc273140ea637782b005e3d99b8c01c0e58519feeb27393dc820bb0f0`.

### Pistes classées et limites

- **Évolution de l’état initial / IA / économie / caches persistants ou recalculs** : priorité élevée, sans fonction responsable identifiée. La lenteur persiste dans une sauvegarde initiale créée après les hooks de lobby ; la seule charge de démarrage ne l’explique pas.
- **Taille du monde** : `every_country` retourne 400 pays au pilote mod contre 291 vanilla. Proxies statiques incluant les décentralisés : 646 contre 449 ; groupes de POP : 6 815 contre 4 483 ; blocs de bâtiments : 4 126 contre 3 171. Ce ne sont pas des mesures de coût ni des comptes de marchés actifs.
- **IA d’infrastructures régionales** : initialisation et hook mensuel par pays, tris répétés d’États et examens de PM/approvisionnement ; prochaine ablation ciblée utile. Le cooldown de 180 jours ne suspend pas tout le contrôleur et ne prouve pas l’explication à six mois.
- **HRE mensuel, journaux et quotas** : charges récurrentes et avertissements de journaux déjà présents identifiés ; coût non ventilé. Plusieurs journaux lourds hérités sont bloqués par date ou DLC.
- **Rappel quotidien HRE** : ne paraît pas dominant dans cette configuration ; ne pas en déduire que tout HRE est innocenté.
- **Drapeaux** : hypothèse hebdomadaire non établie. Les constantes graphiques de 30 images et nettoyage après 20 mises à jour ne documentent pas la cadence des triggers de sélection.
- **Laboratoires** : aucun bâtiment initial trouvé ; faible priorité tant que l’activation effective n’est pas démontrée.

### Contrôles restant à exécuter

Le rechargement froid d’un monde après sa première année **n’a pas été terminé** : aucune sauvegarde 1777 n’a été créée avant la fermeture du dernier essai. Les outils et fenêtres DAY 14/28/56 sont prêts, mais aucun résultat de ce contrôle n’est revendiqué.

Ce test distinguera partiellement les recalculs au chargement de l’évolution du monde ou des caches sérialisés. Ensuite : ablation séparée de l’IA mensuelle d’infrastructures, éventuellement HRE mensuel, répétitions supplémentaires pour les petits écarts, profil moteur/threads si disponible. Validation distincte nécessaire pour la 1.15.0 avec DLC.

### Préservation et livrables

Contrôle final par empreintes : **2 996/2 996 fichiers runtime du mod identiques ; 80/80 fichiers suivis du profil normal et sauvegardes identiques ; 3/3 fichiers Russie–Kazakh identiques ; index Git, HEAD, exécutable Steam et COMPACT inchangés**. Aucun commit, push, fusion, changement de branche ni modification des installations normales.

Rapport et preuves préparés localement, sans commit :
`docs/reports/performance/INITIAL_SIMULATION_ISSUE56_2026_11_17/REPORT_FR.md`,
`BENCHMARKS.csv`, `BENCHMARK_QUALITY.json`, `BENCHMARKS_EXTENDED.json`, inventaire statique, procédure de reproduction et préservation avant/après.
Outils : `tools/performance/simperf56_*.py` et collecteur PowerShell.

21 fenêtres brutes : 18 utilisables avec limites, 1 pilote, 2 exclues ; les intervalles dérivés contaminés sont également marqués. Les chiffres d’arrivée des logs ne doivent pas être utilisés. L’issue reste à investiguer ; aucun correctif de gameplay validé n’est revendiqué.


<details>
<summary>État et plan initiaux conservés pour historique</summary>

Enquête distincte de #54 : débit de simulation pendant les premiers mois, arbre technologique fermé.

## Signalement et référence
Sarah Rose / Yekatarina rapporte une simulation nettement ralentie au début du scénario, puis une amélioration après environ six mois. Ce constat n'est pas encore un benchmark instrumenté. La piste des mises à jour hebdomadaires de drapeaux est une hypothèse.

Le main local et distant sont vérifiés à bd776919f625016cb9e63b2359cc04796c681ef5 (17 novembre 2026). COMPACT est présent dans main, notamment via 764095ed ; il reste préservé. Le workspace est propre au départ de cette mission.

## Environnements séparés
- Steam : 1.15.1, sans DLC de gameplay ; configuration prioritaire pour reproduire le signalement.
- Installation locale : 1.15.0 avec dossiers DLC ; série distincte, aucune équivalence supposée.
- Aucun changement de l'installation normale, des sauvegardes ou playsets.

## Travail prévu
- Inventorier les pays effectivement initialisés, les POPs/bâtiments/marchés et les systèmes IA.
- Examiner on_actions, événements, journaux, conditions fréquentes, drapeaux et initialisations ; distinguer fréquence déclarée et cadence moteur inconnue.
- Mesurer le temps réel nécessaire à des intervalles de simulation, jours simulés/seconde, CPU et RAM aux débuts des mois 0, 1, 3, 6 et 12 ; témoins vanilla et copies isolées de main.
- Ne pas confondre activité de démarrage et débit de simulation. Garder les résultats indisponibles comme non mesurés.
- Tester une variable à la fois dans des copies diagnostiques, puis proposer seulement une correction minimale étayée.
- La référence vanilla standard commence en 1836 ; toute adaptation de calendrier sera signalée, sans prétendre à des mondes identiques.

## Protections et critères
COMPACT, diplomatie Russie–Petite Horde kazakhe, carte, lois et contenu historique sont préservés. Aucun correctif expérimental n'est poussé ou fusionné sans accord du mainteneur.

Cette issue reste ouverte tant que les causes, mesures et limites ne sont pas documentées. Aucun gain de simulation ni correctif n'est revendiqué à la création. Les capacités de contrôle Windows et les instruments sont revérifiés avant les essais.

</details>


</details>
