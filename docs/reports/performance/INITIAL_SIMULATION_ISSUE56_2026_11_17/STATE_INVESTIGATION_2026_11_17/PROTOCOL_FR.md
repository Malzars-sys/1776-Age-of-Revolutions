# Issue 56 — HRE mensuel et stabilisation du monde initial

Mission du 17 novembre 2026, après le rapport RELOAD_EXPERIMENT_2026_11_17.

Laboratoire externe : `C:/Users/simeo/AppData/Local/Temp/aor56_state_20261117`.
Toutes les nouvelles copies de runtime, sauvegardes, logs, captures de profilage et JSON volumineux restent dans ce dossier court. Le dépôt reçoit seulement les outils et synthèses compacts. Les preuves antérieures restent conservées à leur emplacement.

HRE mensuel : ordre prévu **HMC1 → HMM1 → HMM2 → HMC2**. C = runtime figé normal ; M = même runtime avec seulement le corps de `aor1776_hre_monthly_hook` remplacé par une trace. Initialisation, code quotidien HRE et IA régionale normaux. La répétition quotidienne déjà programmée continue ; l’appel de planification contenu dans le hook mensuel disparaît nécessairement avec celui-ci. Aucune ablation n’est une optimisation équivalente.

Même sauvegarde France du 1er janvier 1776, SHA256 `387a363748cecd677229d4d03e98c6699830a1da471416491fb6233184d93ed2`. Même exécutable Steam 1.15.1, pas de DLC de gameplay, mêmes paramètres et sonde DAY. Vitesse 5 vérifiée par le raccourci natif KP_5. Pas d’intervention pendant les 56 jours mesurés. Timestamps natifs du moteur, pas arrivée des logs. CPU continu 500 ms. Les temps de menus et chargement sont exclus.

Après ces prises : comparer les sauvegardes natives initiale, intermédiaire juin–juillet et mature avril 1777 ; distinguer données sérialisées, nombres d’objets, évolution économique et coûts d’exécution non observables. Les compteurs de groupes POP sérialisés ne sont pas des effectifs humains.

Chercher ensuite un contrôle discriminant sur l’IA native, séparément de toute ablation de scripts, avec preuve de son exécution. Le profilage constitue une prise distincte ; ne pas mélanger son surcoût aux benchmarks de référence. Aucune suppression de pays, POP ou contenu historique.

Préservation avant : `PRESERVATION_BEFORE.json` externe. Les outils et rapports préexistants, le runtime, profil normal, sauvegardes, index/HEAD, COMPACT, exécutable et fichiers Russie–Kazakh sont protégés par empreintes. Aucun Git d’écriture.
