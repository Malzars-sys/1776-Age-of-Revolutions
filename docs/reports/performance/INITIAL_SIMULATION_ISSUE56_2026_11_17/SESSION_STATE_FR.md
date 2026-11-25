# État final du bilan — 17 novembre 2026

**Lire REPORT_FR.md et BENCHMARK_QUALITY.json en priorité.** Les notes ci-dessous sont l'historique de préparation, pas un ordre de reprise. Les jeux d'essai sont fermés ; aucune fenêtre Victoria 3 n'est présente au contrôle final. L'issue #56 a été mise à jour et reste ouverte : cause précise non attribuée, aucun correctif produit validé.

21 fenêtres brutes : 18 utilisables avec limites, 1 pilote, 2 exclues. MAIN3 est terminé : ses quatre premières fenêtres donnent 32/25/13/9 secondes ; son dernier janvier (193 secondes) est exclu après réduction de vitesse. Aucun fichier de sauvegarde 1777 n'a été créé : contrôle WARM1 non exécuté. Les résultats et limites sont détaillés dans le rapport. Les 2 996 fichiers runtime, 80 fichiers du profil normal/sauvegardes, 3 fichiers Russie-Kazakh, l'index Git, HEAD, COMPACT et l'exécutable sont préservés par empreintes. Aucun commit/push/fusion.

Publication vérifiée : https://github.com/Malzars-sys/1776-Age-of-Revolutions/issues/56 ; texte conservé dans GITHUB_UPDATE_FR.md. Une reprise ultérieure doit partir des exclusions et du statut final, sans réutiliser les mesures d'arrivée des logs ni considérer le contrôle de rechargement comme déjà effectué.

---

## Historique de session (états dépassés conservés)

La mission est active : poursuivre les véritables mesures, ne pas terminer sur cette note. Issue dédiée #56 ; main de référence bd776919f625016cb9e63b2359cc04796c681ef5. Le produit normal reste intact.

## Pilote conservé

`runtime/MAIN1_20261117T015301024Z` : France 1776 créée, sauvegarde commune locale effectuée avant tout tick. À vitesse 5, fenêtre du 2 au 16 janvier : 14 jours / 39 secondes natives, CPU processus environ 20,69 % des 16 processeurs logiques, working set moyen 8254 Mio. Voir ENGINE_RESULTS_PILOT.json. Résultat pilote seulement ; la collecte a rencontré un verrou de fichier dans ReadAllText, puis son nettoyage a fermé son seul enfant. EXIT.json -1 n'est donc pas une preuve de crash du jeu. Aucun arrêt de l'installation normale.

Les journaux sont tamponnés. **Ne jamais utiliser les WINDOW_*.json calculés à l'arrivée des lignes comme résultats définitifs.** `simperf56_analyze.py` emploie l'heure native HH:mm:ss des lignes (précision <1 seconde sur la différence), et aligne les échantillons CPU/RAM continus à 500 ms de `simperf56_observe.ps1`. Ce dernier exige la visibilité réelle sur le processus : exécution locale avec accès étendu, comme le lanceur. Le CPU de démarrage est exclu par différence entre bornes de simulation.

400 pays dans `every_country` au pilote, pas 646 : ce scope exclut les 246 décentralisés comptés dans le proxy statique. Ne pas présenter ces nombres comme deux mesures contradictoires ou comme deux comptes runtime identiques. Nombre des marchés non mesuré ; le compteur d'identifiants markets_counter dans la sauvegarde ne serait pas leur nombre actif.

## Série en cours

`runtime/MAIN2_20261117T022325277Z`, profil MAIN2, processus d'essai 10896, session exec 34170, limite 5400 secondes. Collecteur corrigé pour ouvrir les journaux partagés. Observateur continu démarré automatiquement, fichier CSV vérifié. À 02:29:52 UTC : chargement de la sauvegarde après clic Continuer réussi, pas encore désenclenché la pause. Il faut observer la France au 1er janvier, cliquer vitesse 5 puis le levier Jouer à gauche du cadran. Les coordonnées sont à reprendre d'une capture fraîche (ancienne vue : vitesse 5 x924,y56 ; Jouer x866,y60).

Contrôle Windows via @oai/sky dans node_repl. **Utiliser exclusivement `globalThis.aor56liveWindow` et `globalThis.aor56liveState`**, avec références explicites globalThis ; d'anciennes variables lexicales `simWindow56` / `simState56` désignent encore l'ancien handle et ont produit des captures périmées et erreurs de premier plan. Fenêtre réelle actuelle retournée : id1184936, application Steam victoria3.exe. Toujours sélectionner à nouveau après fermeture/relaunch. APIs d'entrée → une action puis capture ; screenshots affichés automatiquement, ne pas réémettre les données pour inspection.

## Copies préparées

Laboratoire : C:/Users/simeo/AppData/Local/Temp/aor1776_simperf56_20261117.

- main_frozen : 2996 fichiers runtime, empreintes de main vérifiées.
- diagnostic_no_hre_daily_guard : seul le corps de aor1776_hre_schedule_membership_guard est vide. Un événement déjà prévu dans la sauvegarde peut agir une fois ; ensuite arrêt du cycle quotidien. Mensuel, HRE initial, histoire et autres helpers inchangés. **Diagnostic qui change le fonctionnement, jamais un correctif équivalent à intégrer.**
- MAIN2, MAIN3, HRE1, HRE2 : mêmes réglages et même sauvegarde France 1776, SHA256 387a363748cecd677229d4d03e98c6699830a1da471416491fb6233184d93ed2. HRE1/HRE2 montent la copie diagnostic seule + télémétrie ; MAIN2/3 le main figé + télémétrie.
- VANILLA1 : réglages communs, télémétrie seule ; nouvelle France en 1836 à créer par l'interface. Comparaison des offsets, mondes et dates différents à expliciter.
- Métadonnée id manquante de la télémétrie corrigée après le pilote, avant MAIN2 et toutes les séries futures ; anciennes octets archivés. Scripts d'événements inchangés. Voir DIAGNOSTIC_PREPARATION.json.

Ordre souhaité : MAIN2 année entière → VANILLA1 année entière → HRE1 année entière. Selon les résultats, répétitions initiales HRE2/MAIN3 pour vérifier le signal, ou séries entières si nécessaire. Chaque série se termine au marqueur NEXT_JANUARY END ; les fenêtres font 14 jours. Le buffering peut retarder la fermeture : surveiller la date réelle ; si la fin dépasse quelques semaines, demander l'arrêt via requests/TRIAL.stop (uniquement le processus possédé). Ne pas attendre indéfiniment.

Ne pas effectuer de grosses copies/analyses pendant une fenêtre chronométrée. Les copies de variantes et caches sont déjà préparées. L'analyse finale utilise les logs copiés après fermeture, pas la lecture Python directe d'un fichier de journal encore verrouillé.

## Corrections aux anciennes notes

Le PLAN_FR.md initial décrit un état dépassé. Les constantes exactes sont NCountry.JOURNAL_ENTRY_UPDATE_ACTIVE=4, INACTIVE=14 et NGraphics.COA_FLAGS_FRAMES_BETWEEN_UPDATES=30, cleanup20. Elles ne prouvent pas une cadence hebdomadaire du choix des drapeaux.

## À livrer

Rapport français complet, classement avec fréquences/sources/confiance et distinction hypothèses/mesures, tableau comparatif réel, scripts et limites de reproduction, mise à jour de #56 autorisée. Comparer les empreintes finales avec PRESERVATION_BEFORE.json (runtime normal, COMPACT, Russie-KZH, index, profil/sauvegardes ordinaires, exécutable). Aucune écriture Git ni modification de vanilla autorisée. Aucun correctif sans signal mesuré et équivalence fonctionnelle ; si diagnostic invalide l'hypothèse, le dire sans inventer une solution.

## Complément acquis à 02:45 UTC — prioritaire sur l'ancien état ci-dessus

MAIN2 terminé automatiquement après réception des cinq fenêtres, session34170 terminée, enfant fermé par le collecteur. EXIT -1 est la fermeture forcée prévue après CloseMainWindow, pas une preuve de crash. ENGINE_RESULTS.json est le résultat définitif à utiliser : 14 jours / **33,25,14,10,8 secondes** pour janvier1776, février, avril, juillet, janvier1777. CPU environ22.7,22.0,23.8,24.1,19.4 % des16LP ; working set moyen9304,9563,9620,9746,9920Mio. Natif montre bien une accélération, encore sans cause identifiée.

Le calendrier du moteur n'a PAS de29février : offsets91/182/366 → 2avril,2juillet,2janvier1777. Garder les mêmes événements pour toutes les séries afin de comparer le même protocole ; écrire les dates effectivement mesurées, ne pas prétendre avoir testé exactement le1er. Toutes les fenêtres font bien14jours. La précision de1seconde devient relative importante sur8–10secondes ; ne pas revendiquer un petit gain sur une seule prise.

**Limites de MAIN2 :** choix par défaut d'un événement français vers02:33:57UTC (vue9mars) puis second choix vers02:34:25UTC (vue2avril). La seconde action est DANS la fenêtre d'avril (02:34:23–37UTC) : signaler cette fenêtre comme contaminée par intervention UI. Les événements ne mettent pas en pause : la date avançait pendant leur affichage. Un popup Congrès est revenu et restait visible plus tard, sans autre intervention. Pour la comparaison propre HRE1/MAIN3 : **ne choisir aucune option d'événement**, laisser le jeu tourner après le lancement. MAIN2 demeure un premier relevé longitudinal avec limites, pas une paire causale parfaite.

VANILLA1 lancé, processus19404, session exec62370, dossier `runtime/VANILLA1_20261117T024042103Z`, début02:40:42UTC. Même exe/réglages/télémétrie. À02:44:48UTC : initialisation avec compilation des shaders (831indiqués), avant menu. Pas encore créé la France1836. Le contrôleur réel est lié via **globalThis.aor56liveWindow / globalThis.aor56liveState**, références explicites. Ne jamais employer les anciens identifiants lexicaux nus. Le handle courant est re-sélectionné après chaque lancement depuis sky.list_windows. Ne pas faire une nouvelle sélection à partir d'une ancienne variable `simWindow56`.

La métadonnée de télémétrie corrigée id ne remplit pas encore tout le schéma : erreur startup Expected member(short_description) reste commune à MAIN2/VANILLA1 et aux futures séries. Scripts montés et exécutés, aucune erreur runtime d'instrumentation vue. Ne pas changer ce module au milieu de la série ; séparer cette alerte du diagnostic du mod.

**Prochaine séquence à poursuivre :**
1. Vanilla1 : menu Nouvelle partie → Bac à sable → France → Jouer ; vitesse5 puis levierJouer à gauche du cadran. Laisser les popups sans réponse pendant l'année. Observer ponctuellement seulement. Attendre la clôture après les5marqueurs, analyser les logs natifs avec simperf56_analyze.py.
2. HRE1 : copie isolée avec sauvegarde commune, menu Continuer. Même vitesse5, aucune réponse aux événements. Année complète.
3. MAIN3 : refaire l'année depuis la sauvegarde commune, aucune option d'événement, **lancer avec -KeepAfterWindows** (ajouté au script mais ne change pas Vanilla1 déjà en cours). Cette option empêche l'arrêt automatique après la dernière fenêtre afin de préparer une sauvegarde du monde après un an. Le main3 sera la référence propre à confronter à HRE1 ; MAIN2 a des interventions UI.
4. Après les cinq fenêtres de MAIN3, mettre en pause via levier puis sauvegarder sous le nom par défaut daté1777, uniquement dans le profil isolé. Vérifier le fichier puis fermer ce jeu proprement ou via sa requête d'arrêt. Créer un profil WARM1 avec même fichier runtime/réglages/caches et copie de cette sauvegarde1777 ; nouveau processus froid. Mesurer les premières14/28journées à partir des **heartbeats DAY** (les dix marqueurs WINDOW ne seront plus planifiés, car ils sont déjà consommés dans la sauvegarde). Le collecteur peut continuer jusqu'à une requête d'arrêt ou MaxSeconds ; observer le passage d'au moins30–60jours. Comparer au débit de fin d'année avant sauvegarde. Une lenteur qui revient après rechargement orienterait vers recalculs/caches au chargement ; une lenteur qui ne revient pas vers l'évolution de l'état du monde. Ce test discriminant est préparé mais PAS effectué, ne pas conclure avant données.
5. Selon signal HRE, répétitions courtes HRE2/MAIN3 initiales ou variante ciblée complémentaire ; ne pas transformer un bruit de1seconde en optimisation. Aucun fix produit si cause incertaine.

Commandes de lancement des jeux/observateur exigent `sandbox_permissions=require_escalated` pour voir le processus Windows réel. Les lectures ordinaires Get-Process dans une exécution restreinte ne le voient pas, même si le jeu fonctionne. Cela n'indique pas que le jeu a disparu. Toutes les ouvertures sont `--userdir=LAB/profiles/TRIAL -debug_mode`, jamais les profils habituels.

## Complément acquis à 03:10 UTC — état actif à poursuivre

**VANILLA1 terminé**, session62370 fermée. ENGINE_RESULTS.json généré : fenêtres14jours **10,8,8,10,10secondes**. CPU30.2,30.2,27.9,28.3,29.4% des16LP ; working set moyen13551,13777,13826,13904,14080Mio. every_country retourne291pays (449moins158décentralisés), contre400pour le mod. Cette comparaison constate surtout un écart initial qui disparaît plus tard, sans en isoler la cause. Vanilla est une nouvelle partie1836, MAIN2 une sauvegarde1776 chargée ; le pilote MAIN1 nouveau monde faisait39secondes pour la même fenêtre initiale. Pas de choix d'événement effectué dans Vanilla1 après désenclenchement de pause. Savevanillaavanttick conservée france_1836_01_01.v3 (76,9Mo), utile si répétition souhaitée.

Le PC possède32Go physiques (32013.57Mio),16LP. HOST_MEMORY_PRE_VANILLA.json à02:49:59UTC indiquait3250Mio libres avant création du monde vanilla ; ne pas prétendre avoir contrôlé ou fermé les applications tierces. Le working set seul n'est pas toute l'allocation privée. Ne pas inférer une absence de pression mémoire globale à partir de sa seule croissance dans le jeu.

**HRE1 en cours**, processus37288, session exec7366, dossier `runtime/HRE1_20261117T030027389Z`, profilHRE1, lancé03:00:27UTC. Continuer cliqué et France1janvier1776 vérifiée ; vitesse5 et unpause retour03:07:32UTC. Ne choisir aucune option d'événement pendant l'année. Au dernier contrôle03:09:24UTC : fenêtre initiale native04:07:29–04:08:02 locale, soit**33secondes**, identique à MAIN2. Ne pas finaliser l'interprétation avant fin d'année et MAIN3 propre.

**Révision du diagnostic avant son premier lancement** : `simperf56_trace_diagnostic.py` a ajouté une seule ligne debug_log dans le scheduler désormais sans reprogrammation. DIAGNOSTIC_TRACE_REVISION.json archive l'ancien candidat57459627... et le nouveau SHA256 **af4137bcc273140ea637782b005e3d99b8c01c0e58519feeb27393dc820bb0f0**. Un seul fichierruntime diffère toujours. Trace effectivement vue à1776.1.2 puis1776.2.1 : `SIM56|DIAG|HRE_GUARD_BYPASSED`. Cela prouve que le helper diagnostic s'exécute, et non seulement que la fenêtre a un nom. Mensuel toujours actif. Instrumentationcommune inchangée. Le candidat ne doit pas être confondu avec une optimisation de gameplay équivalente.

`simperf56_analyze.py` amélioré : métriques identiques aux anciens résultats du pilote et MAIN2 (régression numérique vérifiée). Il ajoute des fenêtres14/28/56jours à partir des vrais événementsDAY et vérifie leur continuité selon un calendrier moteur365jours. **Pour WARM1, utiliser heartbeat_windows / FIRST_AFTER_LOAD_14, _28, _56**, puisque les WINDOW originaux seront consommés dans la sauvegarde. OptionCLI --summary évite de vider tout le JSON dans la conversation. Les sorties existantes ENGINE_RESULTS.json ne sont pas écrasées ; créer ENGINE_RESULTS_EXTENDED.json si besoin.

Deux documents techniques rédigés : STATIC_FINDINGS_FR.md et REPRODUCING_FR.md (à relire/polir les espaces françaises à la fin). UI_OBSERVATIONS.json conserve les interventions MAIN2 et les conditions des séries. Ils ne remplacent pas le futur REPORT_FR.md final qui devra intégrer toutes les mesures et le classement final.

**Prochaines actions prioritaires** : finirHRE1 → lancerMAIN3 avec -KeepAfterWindows, même save commune, zérochoixd'événement → sauvegarde tardive1777 après fenêtres → profilWARM1 et rechargement froid, mesurer au moins28–56journées DAY → préservation finale / tableau et éventuellement graphique Matplotlib si disponible / rapport français / update issue56 / finaluserconcise. Si aucun coût n'est attribué avec assez de certitude, ne fabriquer aucun correctif. Ne pas clore l'issue comme résolue seulement parce que les benchmarks sont acquis.
