# Reproduire les mesures locales de l'issue 56

## Référence et environnement

Utiliser le runtime du commit bd776919f625016cb9e63b2359cc04796c681ef5. Le laboratoire contient sa copie figée et FROZEN_MANIFEST.json. Ne pas restaurer ce commit dans un workspace partagé ou remplacer des travaux plus récents pour reproduire l'essai.

Exécutable Steam Victoria 3 1.15.1, SHA256 fb4ec0698afd3d3b1a785926d57bd5d68c95a4afd04b56f6bd45abd7a5672b15. Aucun DLC de gameplay. L'installation locale1.15.0 avec DLC n'est pas un témoin équivalent. Les paramètres exacts lancés sont conservés dans chaque runtime/TRIAL_date/SETTINGS.json et CONTENT_LOAD.json ; SHA256 commun des paramètres 49c2686a57d7950b21297338107b005791c813532954ed55fb3d13c35ef4df6c.

1920×1080, fenêtré, VSync désactivée, profil graphique élevé, MSAAx4, ombres4096, texture_streaming=false, langue française, vitesse5 pendant la simulation. Les paramètres sont ceux de l'essai, pas une recommandation de réglages pour jouer.

## Isolation

Le laboratoire est C:/Users/simeo/AppData/Local/Temp/aor1776_simperf56_20261117. Le processus est lancé directement avec --userdir=LAB/profiles/TRIAL et -debug_mode. Chaque profil possède ses propres réglages, sauvegardes, caches et liste de contenu. Aucune inscription au lanceur habituel n'est nécessaire.

MAIN2/MAIN3 montent main_frozen et la télémétrie commune. HRE1/HRE2 montent diagnostic_no_hre_daily_guard et la même télémétrie. Le témoin VANILLA1 monte seulement la télémétrie. Cette instrumentation signifie que le témoin est le vanilla avec les mêmes sondes, et pas un lancement sans aucune sonde.

DIAGNOSTIC_PREPARATION.json puis DIAGNOSTIC_TRACE_REVISION.json décrivent les empreintes successives du seul fichier modifié dans le diagnostic. Le corps du scheduler ne reprogramme plus de garde quotidien et écrit une trace de bypass. Vérifier cette trace, les montages VFS dans les journaux et les empreintes des fichiers ; ne pas se fier au seul nom de la fenêtre.

La sauvegarde commune France1776 est royaume de france_1776_01_01.v3, SHA256 387a363748cecd677229d4d03e98c6699830a1da471416491fb6233184d93ed2, réalisée avant le premier tick. Le premier événement de garde impérial déjà en attente peut encore être exécuté une fois dans la copie diagnostic. Les appels mensuels restent actifs.

## Lancement et interactions

Depuis le dépôt, le lanceur tools/performance/simperf56_start_trial.ps1 prend -Trial et -MaxSeconds. Il refuse de démarrer si un autre victoria3 visible est déjà ouvert et contrôle les empreintes de l'exécutable et des réglages. Exécuter avec accès au processus Windows réel ; une exécution restreinte qui ne voit pas les processus du bureau peut faussement conclure que le jeu est fermé.

Le contrôle de l'interface utilise @oai/sky. Sélectionner la fenêtre retournée de façon unique, lire son état et reprendre le handle à chaque relancement. Une capture puis une seule action puis une nouvelle capture. Les raccourcis clavier ne sont pas nécessaires : les clics du menu et du cadran fonctionnent.

- Mod depuis sauvegarde commune : Continuer, vérifier France et1janvier1776, sélectionner vitesse5, puis levierJouer à gauche du cadran.
- Vanilla : Nouvelle partie, Bac à sable, France, Jouer ; vérifier1janvier1836. Une sauvegarde initiale france_1836_01_01.v3 est disponible pour une éventuelle répétition depuis fichier. Régler ensuite vitesse5 et Jouer.
- Pour les comparaisons propres, ne choisir aucune option d'événement pendant l'année. Les popups observés n'interrompaient pas l'horloge. Consigner toute intervention, pause ou changement de vue ; exclure ou qualifier les fenêtres touchées. MAIN2 comporte une intervention dans sa fenêtre d'avril, voir UI_OBSERVATIONS.json.
- Ne pas ouvrir l'arbre technologique pendant les essais de simulation. Ne pas faire de grosses copies, compilations ou analyses locales durant les fenêtres mesurées.

La fermeture automatique intervient après réception des cinq bornes de fin. Le buffering peut retarder cette réception au-delà de la dernière date mesurée. Le collecteur ferme uniquement son enfant ; EXIT=-1 après ce nettoyage ne suffit pas à diagnostiquer un crash. -KeepAfterWindows conserve le jeu après les fenêtres afin de créer une sauvegarde tardive. Une requête LAB/requests/TRIAL.stop demande l'arrêt de cet essai ; conserver la requête pour preuve, ne pas la réutiliser sans examen.

## Dates et chronométrage

Les événements cachés écrivent des bornes à offsets1–15,31–45,91–105,182–196,366–380 jours. Le moteur observé suit des années de365 jours, y compris1776/1836 : les fenêtres réelles commencent les2 janvier,1 février,2 avril,2 juillet et2 janvier de l'année suivante. Chaque fenêtre contient14 jours simulés. Le premier jour partiel et la préparation en pause sont exclus. Ne pas présenter ces dates comme des mesures exactement au1eravril ou1erjuillet.

**Les journaux sont tamponnés : l'heure d'arrivée d'une ligne est invalide comme chronomètre de simulation.** Les fichiers WINDOW_*.json d'arrivée sont des diagnostics provisoires et peuvent contenir des valeurs absurdes. Les résultats utilisables sont ENGINE_RESULTS*.json, produits par tools/performance/simperf56_analyze.py à partir des heures HH:mm:ss inscrites par le moteur et du CSV CPU/RAM continu. La différence de deux heures natives a une erreur de résolution inférieure à1 seconde ; cette erreur relative devient importante sur une fenêtre de8–10 secondes.

L'observateur échantillonne le CPU cumulé du processus, son working set et ses threads à500ms. Le post-traitement aligne ces données en UTC sur les heures du moteur, avec le fuseau Paris UTC+1 vérifié en novembre2026. Il soustrait le CPU entre bornes de simulation ; aucun CPU de démarrage n'est attribué à une fenêtre. Les pourcentages représentent les16 processeurs logiques de la machine, pas un seul cœur. Les valeurs sont approximatives en raison de la résolution des bornes et de l'interpolation.

Le débit est jours simulés / secondes réelles. La RAM est le working set moyen/min/max sur la fenêtre, pas la mémoire totale du système ni sa seule allocation privée. Aucun FPS moyen n'est produit ; le compteur debug aperçu ponctuellement n'est pas une série de mesures fiable. Le premier plan et l'absence de pause ne sont pas certifiés automatiquement. L'état du monde et les événements peuvent diverger, même avec une sauvegarde initiale commune.

Analyser seulement les journaux archivés après fermeture du processus :

```powershell
# Avec un Python local déjà disponible :
python -B tools/performance/simperf56_analyze.py '<dossier runtime de cet essai>' --summary --output '<nouveau fichier ENGINE_RESULTS.json>'
```

Sur ce PC l'alias python du PATH n'est pas utilisable ; les exécutions archivées emploient le Python fourni par le runtime Codex déjà installé. Le script refuse d'écraser un résultat existant. Les fenêtres heartbeat de14/28/56 jours permettent aussi d'observer le premier intervalle après rechargement d'une sauvegarde tardive dont les marqueurs WINDOW ont déjà été consommés. Elles conservent leurs bornes DAY réelles et vérifient la continuité du calendrier du moteur.

## Portée des conclusions

Comparer les offsets du vanilla 1836 et du mod 1776 décrit les performances de deux mondes différents. Cela n'isole pas, à soi seul, le nombre de pays ou les scripts du mod. La paire main/diagnostic depuis la même sauvegarde est le contrôle plus ciblé. Une ablation qui améliore le débit prouve un coût de la fonction retirée dans ce contexte ; elle ne prouve pas qu'une suppression permanente préserverait le gameplay.

Un petit écart inférieur à la résolution et à la variabilité d'une série courte doit rester indéterminé. Répéter les mesures ou utiliser les endpoints DAY plus longs avant de proposer une optimisation. La télémétrie a une alerte de métadonnée short_description manquante au chargement, commune aux séries après le pilote ; ses effets et événements sont bien montés. Garder les mêmes octets d'instrumentation dans une série et traiter séparément une éventuelle correction de ce schéma.
