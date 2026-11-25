# Issue 56 — rechargement d’un monde mature et contrôle mensuel régional

17 novembre 2026. Rapport de suivi du bilan initial, conservé sans réécriture.
Référence : main `bd776919f625016cb9e63b2359cc04796c681ef5`.
Issue : https://github.com/Malzars-sys/1776-Age-of-Revolutions/issues/56.

## Conclusion du contrôle prioritaire

**Le ralentissement fort du début de campagne ne revient pas dans les deux rechargements testés du monde mature.** Le processus a été entièrement fermé entre chaque passage. Les mêmes dates simulées et la même sauvegarde sont comparées ; il ne s’agit pas d’une comparaison de démarrages du programme.

| Passage | 14 jours | 28 jours | 56 jours |
|---|---:|---:|---:|
| Sans redémarrage | 9 s | 17 s | 33 s |
| Nouveau processus 1 | 9 s | 17 s | 33 s |
| Nouveau processus 2 | 8 s | 16 s | 31 s |

Les premières fenêtres restent dans le même ordre de grandeur que les suivantes. Il n’apparaît pas ici de phase lente transitoire longue après chargement, ni de ralentissement persistant comparable aux premiers mois de 1776. Ce constat porte sur les journées complètes mesurées après la reprise : **le premier jour partiel, la préparation en pause, la durée de chargement et les effets plus courts ne sont pas évalués par ces fenêtres**.

Un contrôle positif contemporain recharge ensuite le monde initial de 1776 : 27 s pour les 14 premiers jours et 93 s pour 56 jours. Le monde initial reste donc nettement plus lent alors que les fichiers et shaders ont déjà été utilisés pendant les essais. Le simple redémarrage d’un processus ne suffit pas à reproduire cette lenteur dans le monde mature.

Cela oriente vers une propriété persistante du scénario initial et de son évolution : état économique, emploi, marchés, priorités/files IA, situation militaire ou diplomatique, variables temporaires, conditions de date, données ou caches sérialisés. **Cela ne prouve pas que l’économie ou une fonction IA précise est la cause.** Des caches de fichiers et de shaders sont conservés ; ce test n’est pas un redémarrage du PC avec purge de tous les caches.

## Sauvegarde, environnement et indépendance des processus

- Monde créé dans MATURE1 depuis la sauvegarde commune France 1776, puis simulé sans choix d’événement à vitesse 5.
- Sauvegarde mature réelle : **21 avril 1777** (`1777.4.21`), environ seize mois après le départ, 122 443 314 octets. La phase lente avait disparu : fenêtre de janvier 1777 à 7 secondes pour 14 jours.
- Fichier : `royaume de france_1777_04_21.v3` ; version vérifiée **1.15.1** ; SHA256 `879867ccd58f230c9eef2fbe04570171679cea015010e713be5c746707b732eb`. Le fichier est conservé intact et toutes ses copies vérifiées.
- Après sauvegarde, reprise sans redémarrage pour mesurer DAY S+1 puis les 14/28/56 jours suivants, et les tranches ultérieures. Les pauses de sauvegarde se trouvent avant S+1.
- Fermeture complète du processus MATURE1 (PID16504), puis nouveaux processus RELOAD1 (PID32668) et RELOAD2 (PID30228), sans chevauchement. Les journaux LAUNCH/EXIT sont archivés et la disparition des fenêtres a été contrôlée.
- Même Steam **Victoria 3 1.15.1 sans DLC de gameplay**, même runtime figé, COMPACT, paramètres et sondes. L’installation locale 1.15.0 avec DLC est restée distincte et n’a pas été utilisée.
- Réglages initiaux SHA256 `49c2686a57d7950b21297338107b005791c813532954ed55fb3d13c35ef4df6c` ; exécutable SHA256 `fb4ec0698afd3d3b1a785926d57bd5d68c95a4afd04b56f6bd45abd7a5672b15`.
- Vue carte France harmonisée en passant par Menu puis Reprendre, sans choisir d’option d’événement. Vitesse 5 avant chaque reprise. Quelques expirations de capture graphique ont été résolues avant mesure par réinitialisation du contrôleur et nouvelle observation ; aucun clic aveugle n’a servi à poursuivre.

## Persistance sur les tranches suivantes

J correspond au jour de sauvegarde S ; la première borne est S+1. Chaque ligne mesure 14 jours entiers aux mêmes dates dans les trois passages.

| Tranche | Sans redémarrage | Rechargement 1 | Rechargement 2 |
|---|---:|---:|---:|
| J+1 à J+15 | 9 s | 9 s | 8 s |
| J+15 à J+29 | 8 s | 8 s | 8 s |
| J+29 à J+43 | 8 s | 8 s | 8 s |
| J+43 à J+57 | 8 s | 8 s | 7 s |
| J+57 à J+71 | 8 s | 8 s | 9 s |
| J+71 à J+85 | 10 s | 9 s | 9 s |
| J+85 à J+99 | 10 s | 9 s | 9 s |
| J+99 à J+113 | 10 s | 9 s | 9 s |

Les 56 jours suivants, au-delà de la première fenêtre de 56 jours, prennent 38 s, 35 s et 36 s. Il n’y a pas de retour d’une phase de plusieurs mois à environ trois fois le temps initial mature.

## CPU et RAM

Pour les 56 premiers jours de chaque contexte, CPU sur l’ensemble des 16 processeurs logiques et RAM en Gio de working set résident moyen :

| Passage | Jours simulés/s | CPU processus | RAM résidente (Gio) |
|---|---:|---:|---:|
| MATURE1 | 1,697 | 18,9 % | 8,37 |
| RELOAD1 | 1,697 | 19,5 % | 16,26 |
| RELOAD2 | 1,806 | 19,8 % | 16,15 |
| INIT_REF1 | 0,602 | 22,7 % | 16,34 |
| INFRA_M0 | 0,583 | 22,4 % | 16,43 |

Le working set diffère fortement entre processus. Il dépend de la résidence des pages et de Windows ; il ne représente pas toute l’allocation privée et ne démontre pas une cause mémoire. Les applications tierces, la mémoire globale, les fréquences CPU/GPU et le premier plan ne sont pas entièrement contrôlés. Les petits écarts de quelques pour cent ne sont pas présentés comme des gains certains. Aucun FPS moyen fiable n’a été collecté.

## Expérience suivante choisie et exécutée : IA régionale mensuelle seule

Le monde mature reste rapide après redémarrage, tandis que le monde initial rechargé reste lent. L’expérience suivante vise donc un travail périodique dans cet état initial, en priorité le contrôleur mensuel d’infrastructures régional. INIT_REF1 et INFRA_M0 repartent du même fichier initial, SHA256 `387a363748cecd677229d4d03e98c6699830a1da471416491fb6233184d93ed2`.

Une seule différence de runtime : `common/on_actions/13_1776_ai_regional_infrastructure.txt`. Seul le corps du child `aor1776_ai_regional_infrastructure_monthly` est retiré. Le hook natif et ses autres enfants, l’initialisation régionale, le HRE quotidien et mensuel, la carte, les pays, les lois, la technologie et l’histoire restent inchangés dans les fichiers.

Source SHA256 `f1b3ccf92a807581434f21dd902828a94ee2308fe433d530c04493a43975fdeb` ; diagnostic `4923839eb6a320c636a0cb74d355e559833103ad0e61a22a052fbafbf6d18048`. **6 traces de bypass mensuel ont été effectivement observées**, en plus de la vérification du montage et des empreintes. Le coût de ces traces est inclus.

| Intervalle initial | Témoin contemporain | Mensuel régional désactivé |
|---|---:|---:|
| 14 jours | 27 s | 28 s |
| 28 jours | 52 s | 53 s |
| 56 jours | 93 s | 96 s |

Aucun gain net observé : 96 secondes avec ablation contre 93 pour le témoin sur 56 jours, soit 3,2 % de temps supplémentaire dans cette prise. Cette unique comparaison ne démontre pas une aggravation fiable de quelques pour cent. Elle ne soutient pas la suppression de ce contrôleur comme solution à la forte lenteur initiale.

Le coût net comprend les conséquences des décisions retirées ; il ne s’agit pas d’un profil CPU interne de cette seule fonction. L’ablation n’est **pas** une correction préservant le gameplay. Elle n’est ni intégrée, ni fusionnée, ni proposée comme optimisation prête à installer.

L’initialisation régionale avait déjà été appliquée avant la sauvegarde initiale commune. Ce test ne retire que son activité mensuelle ultérieure ; il n’exonère ni cette initialisation ni ses conséquences persistantes. Pour isoler l’initialisation elle-même, il faudrait une comparaison dédiée de nouvelles campagnes, et non désactiver son hook en rechargeant une sauvegarde où ses effets sont déjà présents.

## Incertitudes et portée

Les bornes sont les timestamps natifs HH:mm:ss des logs, avec erreur de résolution inférieure à une seconde sur une différence. Les arrivées des lignes sont tamponnées et ne servent jamais de chronomètre. Les fichiers WINDOW d’arrivée restent des diagnostics provisoires ; seuls les résultats d’analyse native sont utilisés.

CPU cumulé et working set sont suivis à 500 ms puis alignés sur les bornes UTC (Paris UTC+1 en novembre 2026). Aucun CPU de démarrage, compilation de shaders ou menu n’est attribué à une fenêtre de simulation. Le calendrier moteur compte 365 jours ; les sondes vérifient la continuité des dates. Les contrôles n’ont pas le pouvoir statistique de certifier un petit effet et ne séparent pas l’ensemble des mécanismes persistants. Les décisions IA peuvent diverger après rechargement malgré le même point de départ.

Les essais sont en mode debug et comportent les mêmes sondes DAY. L’alerte de métadonnée commune et les erreurs héritées restent à distinguer des nouvelles erreurs éventuelles du diagnostic. Cette étude ne valide pas les performances de l’autre installation 1.15.0 avec DLC.

## Prochaines étapes recommandées

1. Isoler **le child mensuel HRE seul**, dans une autre copie depuis la sauvegarde initiale, en gardant les routines quotidiennes et le contrôleur régional normal. La précédente ablation quotidienne n’exonère pas tout le HRE. Ne pas combiner les deux suppressions.
2. Si le contrôle régional donne un signal reproductible, distinguer les tris d’États, remises à zéro de variables, invalidations et choix de PM ; chercher ensuite seulement une réduction équivalente de calculs. Une répétition dans l’ordre inverse est nécessaire pour les petits écarts.
3. Si les contrôles scriptés n’expliquent pas l’écart, profiler les traitements natifs IA/emploi/marchés et les files ou données persistantes du départ. Examiner aussi les conditions de date et les variables à durée limitée. Le rechargement rapide ne prouve pas une initialisation économique précise.
4. Une série 1.15.0 avec DLC doit rester séparée. Aucune suppression artificielle de pays, POP ou contenu historique pour obtenir un meilleur chiffre.

## Préservation et fichiers produits

Audit final : 2996/2996 fichiers runtime normaux identiques ; 80/80 fichiers suivis du profil et des sauvegardes normaux identiques ; trois fichiers Russie–Kazakh, index Git et exécutable inchangés. Les 233 preuves antérieures protégées sont conservées. L’analyseur préparé a reçu un argument facultatif d’ancres DAY ; sa version précédente exacte est archivée et la régression des anciennes mesures vérifiée. Aucun travail préexistant n’a été supprimé.

La configuration de préparation est étendue par profils uniques avec archivage avant chaque ajout. Aucun Git d’écriture, aucun commit/push/fusion, aucune modification des installations normales ni du mod principal. Les diagnostics sont exclusivement dans le laboratoire Temp.

Preuves : `MATURE_SAVE.json`, profils, LAUNCH/EXIT et logs par passage ; `MATURE_BEFORE_RESTART.json`, `RELOAD1_RESULTS.json`, `RELOAD2_RESULTS.json`, `INIT_REF1_RESULTS.json`, `INFRA_M0_RESULTS.json`, `MEASUREMENTS.csv`, `INFRA_MONTHLY_VARIANT.json`, audit avant/après et protocole. La sauvegarde mature est désormais disponible pour répéter les contrôles sans refaire toute l’année.

**Statut : contrôle de rechargement exécuté et répété ; l’enquête sur la cause initiale reste ouverte. Aucun correctif de production validé.**
