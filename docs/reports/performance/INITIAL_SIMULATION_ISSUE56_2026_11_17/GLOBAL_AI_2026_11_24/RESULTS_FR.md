# Ralentissement initial et IA des pays sous Victoria 3 1.15.2

En passant les 646 contrôleurs d'IA à l'état inactif, les 56 premiers jours sont passés de 211 à 35 secondes, soit un débit de simulation environ six fois supérieur. Avec les 646 contrôleurs actifs et la probabilité de considérer un changement de méthode de production à zéro, ils ont pris 212 secondes. Le nombre de bâtiments dont les méthodes différaient de celles du départ a pourtant baissé de 333 à 30 au 1er avril.

| Condition | 14 j | 28 j | 56 j | IA active en avril | Ordres publics en file | Ordres privés en file | Bâtiments avec des méthodes différentes en avril |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Témoin normal du 24 novembre (`GON1`) | 62 s | 124 s | 211 s | 646 | 1 220 | 22 | 333 sur 6 592 |
| Contrôleurs inactifs (`GOF1`) | 8 s | 16 s | 35 s | 0 | 0 | 8 | 29 sur 6 631 |
| Probabilité de considérer un changement de méthode à zéro (`GPM1`) | 66 s | 125 s | 212 s | 646 | 1 237 | 25 | 30 sur 6 592 |

Les trois passages ont utilisé l'exécutable Steam 1.15.2, le mod figé à `bd776919f625016cb9e63b2359cc04796c681ef5` et les réglages de la [série du 23 novembre](../NATIVE_CATEGORIES_2026_11_23/RESULTS_FR.md). Ils sont partis de la sauvegarde française du 1er janvier 1776, à vitesse 5 sur le deuxième écran. Le témoin et l'essai sur les méthodes ont chargé une sauvegarde identique octet pour octet. Pour l'essai avec IA inactive, la substitution inverse des 646 valeurs `ai.enabled` restitue exactement la sauvegarde d'origine. Les identifiants, les objectifs et les autres données des contrôleurs sont identiques au départ.

Le chronomètre repose sur les marqueurs quotidiens du moteur, du 2 janvier au 16 janvier, au 30 janvier et au 27 février. Les jours sont consécutifs, la résolution est d'une seconde et aucune écriture d'autosauvegarde n'a été observée dans ces fenêtres. Le contrôle du temps écoulé ne permet pas de certifier l'absence de toute pause transitoire. Les trois passages se sont fermés automatiquement après l'enregistrement de l'autosauvegarde du 1er avril. Celle-ci confirme les réglages d'IA, le maintien des mêmes 646 contrôleurs et des 400 objectifs `change_production_methods`. Les files relevées en avril comptent les ordres en attente ou en cours à cette date.

La variante `GPM1` ajoute un fichier de laboratoire qui passe `NAI.PRODUCTION_METHOD_CHANCE_TO_CHANGE` de 0,1 à 0 et un affichage de contrôle en pause. La capture du jeu confirme la valeur effective et le maintien des trois autres interrupteurs économiques à 1. Les nombres de bâtiments comparent les méthodes enregistrées au départ et en avril pour un même identifiant, un même type et un même État, avec au moins un niveau et des méthodes enregistrées aux deux dates. Les 6 592 bâtiments retenus sont les mêmes dans les deux essais avec IA active. Les 29 différences avec IA inactive et les 30 différences dans `GPM1` concernent toutes des chemins de fer. Les instantanés permettent de constater des configurations différentes en avril. Ils ne donnent ni la fréquence des changements intermédiaires ni le coût de l'évaluation de chaque méthode.

Le témoin du 23 novembre avait pris 121 secondes sur 56 jours. Son autosauvegarde et celle du témoin de ce lot ont la même taille de 125 400 901 octets. La comparaison binaire trouve 22 octets différents, tous dans l'en-tête ou les deux champs de temps réel. Le débit absolu variait donc sensiblement entre les deux sessions, même avec le même état de partie enregistré en avril. Le contraste de 176 secondes avec l'IA inactive confirme le signal déjà observé sur la version antérieure. L'écart d'une seconde dans l'essai sur les méthodes ne démontre aucun gain.

Le coût propre des calculs de rentabilité du moteur reste indéterminé. Le fichier `game/common/defines/00_ai.txt` de l'installation Steam décrit les coefficients de rentabilité et la probabilité de considérer une autre méthode, sans documenter l'ordre d'exécution de ces calculs. La [tentative de profilage native](../STATE_INVESTIGATION_2026_11_17/REPORT_FR.md) avait été arrêtée par Windows avant la capture, code `0xc5585011`. Aucune optimisation préservant le gameplay n'est validée pour ce ralentissement.

## Reproduction et preuves

Les scripts de préparation et d'analyse se trouvent dans `tools/performance`. Utiliser `simperf56_global_ai_prepare_20261124.py` pour les deux premiers profils. Dans le laboratoire `aor56_global_ai_20261124`, lancer chaque profil avec `run_profile_trial.ps1 -Trial ESSAI -MaxSeconds 1200 -KeepAfterWindows -StopAfterHeartbeatDays 100`. Associer `simperf56_native_day_archive_20261123.py` et `simperf56_autosave_watch_20261118.py` en pointant leur répertoire de laboratoire sur ce lot. Après le passage `GON1`, utiliser `simperf56_pm_chance_20261124.py prepare` et lancer `GPM1` de la même façon. Après chaque fermeture, exécuter `simperf56_native_results_20261123.py ESSAI --lab CHEMIN_DU_LABORATOIRE`. Quand les trois reçus sont disponibles, exécuter `simperf56_pm_chance_20261124.py compare`.

- Exécutable Steam SHA-256 `57c4950e9f1046d61729e8faeedbbdbb7aa30ff2a45788217285eb735491ad36`.
- Sauvegarde de départ du témoin SHA-256 `da7a264a810564f4fd1c595397d884563b359bf6629f8f021c314476e3cb4fd3`.
- Autosauvegarde `GON1` SHA-256 `aba1117efb3a4fa8d45f3e0244b5ccd99363cf43e69de1159503ae2c3bc63638`.
- Autosauvegarde `GOF1` SHA-256 `bb462b2b7d6fdeaad8479db54806e5998587dda1c987498e7e72f407e7c18a7a`.
- Autosauvegarde `GPM1` SHA-256 `72cfc1ee3f6894f96f10cb6fdd09d78ebc1e38cd491acb570a0d2de68f51e021`.

Le laboratoire conserve `SETUP.json`, les trois reçus `*_RESULTS.json`, `PM_CHOICES_APRIL.json`, `WITNESS_NAC2_GON1_BYTE_DIFF.json` et la capture `evidence/GPM1_PM_DEFINE.png`.
