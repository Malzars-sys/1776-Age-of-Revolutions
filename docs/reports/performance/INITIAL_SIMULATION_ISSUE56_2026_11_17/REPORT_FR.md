# Simulation initiale — bilan expérimental de l’issue 56

17 novembre 2026. Référence main : `bd776919f625016cb9e63b2359cc04796c681ef5`.
Issue : https://github.com/Malzars-sys/1776-Age-of-Revolutions/issues/56.
Le chantier d’interface technologique COMPACT reste distinct : https://github.com/Malzars-sys/1776-Age-of-Revolutions/issues/54.

## Résultat principal et statut

**Le ralentissement initial est reproduit. Aucune correction de simulation préservant le gameplay n’est validée.** Sur cette machine, les références du mod prennent 32–33 secondes pour simuler 14 jours au début de 1776, contre 10 secondes dans le témoin vanilla. En juillet, les prises sont proches : 9–10 secondes pour le mod, 10 secondes pour le vanilla. Un relevé du main en janvier 1777 prend 8 secondes ; cela ne prouve pas une supériorité générale du mod, car les mondes et les états simulés diffèrent.

La désactivation isolée de la reprogrammation quotidienne du garde impérial ne supprime pas cette phase lente. Elle donne 33 secondes au départ et suit presque la même accélération. Ce rappel ne semble donc pas expliquer l’écart initial d’environ trois fois avec le vanilla. Un petit coût reste possible : un seul passage diagnostic ne permet pas de certifier un gain de quelques pour cent.

L’explication précise reste ouverte entre l’évolution de l’état initial — IA, économie, emploi, marchés, état scripté ou caches sérialisés — et les recalculs/caches liés au chargement. Le contrôle consistant à recharger un monde déjà évolué n’a pas été terminé. Aucun résultat de ce contrôle n’est revendiqué.

## Environnement réellement utilisé

- PC Windows local : accès au système de fichiers, au dépôt et au bureau vérifié ; commandes PowerShell locales et contrôle graphique `@oai/sky` effectifs.
- Steam Victoria 3 **1.15.1 sans DLC de gameplay**, même exécutable dans tous les essais. SHA256 : `fb4ec0698afd3d3b1a785926d57bd5d68c95a4afd04b56f6bd45abd7a5672b15`.
- L’installation locale **1.15.0 avec DLC** n’a pas servi de témoin ni été lancée par cette enquête. Le joueur avait confirmé la fermeture de sa session avant les essais Steam.
- Même profil graphique : 1920×1080 fenêtré, élevé, MSAA×4, VSync désactivée. Réglages exacts archivés par essai ; SHA256 initial commun `49c2686a57d7950b21297338107b005791c813532954ed55fb3d13c35ef4df6c`.
- Vitesse 5 pour les fenêtres retenues, mode debug et module de télémétrie commun. Le témoin est donc le vanilla avec les mêmes sondes.
- 16 processeurs logiques, environ 32 Go physiques. Les autres applications n’ont pas été fermées ou contrôlées. Un instantané avant le monde vanilla indique environ 3,2 Go physiques libres ; la pression mémoire globale n’est pas certifiée constante.

Le main et le diagnostic utilisent une copie figée de 2 996 fichiers et une sauvegarde commune France au 1er janvier 1776, créée avant le premier tick. Le vanilla est une nouvelle France en 1836. Le pilote MAIN1 est aussi une nouvelle partie 1776 ; les références MAIN2/MAIN3 sont des rechargements de la sauvegarde initiale. Ces différences limitent une attribution causale à partir du seul contraste vanilla/mod.

## Méthode et précision

Des événements cachés inscrivent les bornes de fenêtres fixes de 14 jours et un heartbeat quotidien. Le temps retenu est l’heure **HH:mm:ss écrite par le moteur**, convertie en UTC. L’heure d’arrivée du journal est inutilisable : le jeu tamponne les écritures. Les fichiers `WINDOW_*.json` calculés à l’arrivée sont des diagnostics provisoires, parfois absurdes, et doivent être ignorés pour les performances. Les résultats exploitables sont les `ENGINE_RESULTS*.json` et les agrégats qualifiés de ce dossier.

La résolution de la différence de deux bornes est inférieure à une seconde. Elle représente une incertitude relative importante sur une fenêtre de 8–10 secondes. Le CPU et le working set du processus sont échantillonnés toutes les 500 ms puis alignés sur les bornes natives. Le CPU est soustrait entre bornes ; le démarrage, les menus, la création du monde et la compilation des shaders sont exclus. Les pourcentages CPU portent sur l’ensemble des 16 processeurs logiques. Ils sont approximatifs et ne constituent pas un profil interne des fonctions du moteur.

Le calendrier observé a 365 jours par an, y compris 1776/1836. Les fenêtres réelles commencent les **2 janvier, 1er février, 2 avril, 2 juillet et 2 janvier suivant**. Elles ne doivent pas être présentées comme des prises exactement au 1er avril ou au 1er juillet. Le premier jour partiel est exclu. Aucun FPS moyen ni latence d’interface n’a été inventé ; les compteurs ponctuels aperçus ne constituent pas une série fiable. L’arbre technologique est resté fermé.

L’absence de pause et l’état de premier plan ne sont pas certifiés automatiquement. Les captures ponctuelles ont montré l’horloge avancer, y compris derrière les événements. La RAM ci-dessous est le **working set résident**, pas toute l’allocation privée ni la mémoire globale du PC. Ses variations entre passages empêchent une conclusion fine sur la mémoire.

## Temps réel pour 14 jours simulés

| Fenêtre réelle du scénario | Vanilla 1836 | Main MAIN2 | Main répété MAIN3 | Diagnostic sans rappel quotidien HRE1 |
|---|---:|---:|---:|---:|
| 2–16 janvier | 10 s | 33 s | 32 s | 33 s |
| 1–15 février | 8 s | 25 s | 25 s | 24 s |
| 2–16 avril | 8 s | 14 s, exclu¹ | 13 s | 13 s |
| 2–16 juillet | 10 s | 10 s | 9 s | 10 s |
| 2–16 janvier suivant | 10 s | 8 s | exclu² | 8 s |

¹ MAIN2 : un choix d’événement a été effectué pendant la fenêtre d’avril. Cette prise est conservée brute mais exclue de la comparaison propre.

² MAIN3 : réduction de vitesse en fin de 1776 pour préparer une sauvegarde à date contrôlée ; aucun retour vérifié à vitesse 5 avant cette fenêtre. Le temps brut de **193 secondes** est conservé mais exclu. Le processus a ensuite quitté avec code 0 ; aucune sauvegarde 1777 n’a été trouvée dans le profil isolé. Cette prise ne constitue pas un retour du ralentissement initial.

Le pilote MAIN1 donne 39 secondes pour les mêmes 14 premiers jours dans une nouvelle partie. La collecte a ensuite rencontré une erreur de partage de fichier, puis fermé son seul enfant. Ce pilote est séparé des séries principales ; l’erreur du collecteur n’est pas une preuve de crash du jeu. La lecture partagée a été corrigée avant les autres séries.

## Débit, CPU et mémoire sur les prises principales

Les valeurs détaillées et les exclusions sont dans `BENCHMARKS.csv` et `BENCHMARK_QUALITY.json`. CPU en pourcentage de la machine ; RAM en Gio de working set moyen.

| Série | Débit janvier (jours/s) | CPU janvier | RAM janvier | Débit juillet (jours/s) | CPU juillet | RAM juillet |
|---|---:|---:|---:|---:|---:|---:|
| Vanilla | 1,400 | 30,2 % | 13,2 | 1,400 | 28,3 % | 13,6 |
| Main MAIN2 | 0,424 | 22,7 % | 9,1 | 1,400 | 24,1 % | 9,5 |
| Main MAIN3 | 0,438 | 22,5 % | 14,7 | 1,556 | 23,1 % | 13,5 |
| HRE1 | 0,424 | 22,1 % | 12,5 | 1,400 | 23,6 % | 12,7 |

Une consommation CPU globale plus faible ne signifie pas une simulation plus rapide : le mod avance beaucoup moins de jours par seconde en janvier. Les données ne permettent pas d’identifier un thread critique, une attente GPU ou une fonction IA précise. Les processus restent soumis à l’environnement Windows et aux autres applications.

## Contrôle ciblé du garde impérial

Un seul fichier diffère du runtime figé : `common/scripted_effects/1776_imperial_constitution.txt`. Le helper `aor1776_hre_schedule_membership_guard` ne reprogramme plus l’événement quotidien et écrit une trace de bypass. L’événement déjà en attente dans la sauvegarde peut agir une première fois ; le mensuel et les autres fonctions restent actifs. Les traces ont été observées dans le moteur, notamment au 2 janvier puis au 1er février. Le montage du diagnostic et ses empreintes sont archivés.

SHA256 source : `af7940c6fc8d9c2d0eb841d210c05fc29ad16475b989d2e7a8a679e54e26362f` ; diagnostic réellement lancé : `af4137bcc273140ea637782b005e3d99b8c01c0e58519feeb27393dc820bb0f0`.

Les heartbeats permettent des intervalles plus longs, avec moins d’erreur relative de chronométrage :

| Intervalle initial | Main MAIN2 | Main MAIN3 | HRE1 | Vanilla |
|---|---:|---:|---:|---:|
| 28 jours | 61 s | 61 s | 60 s | 18 s |
| 56 jours | 108 s | 109 s | 106 s | 37 s |

Le diagnostic est environ 2–3 % plus court sur 56 jours, mais une seule répétition diagnostique, la résolution temporelle et la variabilité de l’environnement ne suffisent pas à certifier ce petit effet. Il ne résout pas l’écart initial massif avec le vanilla. Le **contrôleur impérial mensuel n’a pas été isolé**, et n’est pas innocenté par cette expérience.

L’ablation change volontairement le fonctionnement du jeu : ce n’est pas une optimisation équivalente et elle ne doit pas être intégrée au mod normal.

## Classement des pistes et niveau de preuve

| Piste | Éléments observés | Conclusion / confiance |
|---|---|---|
| Évolution de l’état initial, IA et économie natives ou scriptées, caches persistants/recalculs | Forte accélération sur les premiers mois, reproduite sur deux références ; beaucoup plus faible dans le vanilla | Priorité d’investigation élevée ; famille plausible, fonction responsable non identifiée |
| Nombre de pays et d’objets à traiter | Scope `every_country` : 400 au pilote mod, 291 vanilla ; proxy statique incluant décentralisés : 646 contre 449 ; POP : 6 815 groupes contre 4 483 | Surcharge potentielle établie ; causalité et coût par système non mesurés. Aucun pays ne doit être supprimé pour servir de correctif |
| IA d’infrastructures régionales | Initialisation, puis hook mensuel par pays ; dix classements d’États, parcours d’infrastructures et tests de PM/approvisionnement | Hypothèse ciblée à tester. Le cooldown de 180 jours ne suspend pas le contrôleur entier et ne prouve pas une explication à six mois |
| HRE mensuel / journaux / quotas de naissance | Boucles et conditions récurrentes identifiées ; erreurs de journal impérial déjà présent observées | Coût non ventilé, expériences séparées nécessaires ; cadence seule insuffisante |
| Rappel quotidien HRE | Ablation chargée et exécutée ; courbe presque inchangée | Ne semble pas être la cause dominante dans cette configuration, confiance modérée ; petit coût éventuel non confirmé |
| Drapeaux hebdomadaires | Davantage de listes ; constantes graphiques de rafraîchissement identifiées | La cadence hebdomadaire des conditions de sélection n’est pas établie. Piste ouverte, sans responsabilité démontrée |
| Laboratoires | Surveillance rapprochée possible, mais aucun laboratoire initial dans l’inventaire | Faible priorité au départ tant que l’activation réelle n’est pas démontrée |

L’inventaire contient aussi 4 126 blocs de bâtiments contre 3 171 et 9 404 niveaux explicites contre 8 699. Il ne mesure pas le nombre de marchés ni de routes commerciales actifs. Des journaux lourds hérités du vanilla sont conditionnés par des DLC ou des dates ; leur simple présence ne prouve pas qu’ils s’exécutent en 1776 sans DLC. Les sites de boucles ne sont pas des millisecondes de CPU.

Voir `STATIC_FINDINGS_FR.md` pour les fichiers, lignes et fréquences détaillés, et `STATIC_INVENTORY_RECURRENT.json` pour l’inventaire. Les constantes graphiques des drapeaux ne doivent pas être confondues avec une cadence des triggers de sélection.

## Contrôles restant à faire

1. Créer une sauvegarde du monde après sa stabilisation puis la recharger dans un nouveau processus, avec mêmes réglages et dates de mesure. Le script `simperf56_warm_profile.py` et les fenêtres DAY 14/28/56 sont préparés, mais **ce test n’a pas été exécuté**. Un retour de lenteur orienterait vers les recalculs au chargement ; son absence vers l’état du monde ou des données/caches persistants, sans séparer automatiquement économie et IA.
2. Tester séparément le hook mensuel d’infrastructures et, selon le signal, les charges mensuelles HRE. Une variable par copie, traces de chargement et répétitions comparables.
3. Pour attribuer une fonction native précise, obtenir un profil moteur/threads ou des instruments plus fins. Répéter les petits écarts avant d’en tirer une optimisation.
4. Ne généraliser à la 1.15.0 avec DLC qu’après une série dédiée. Aucune validation de cette installation n’est fournie ici.

Ces contrôles peuvent être pris en charge par l’agent avec le contrôle Windows supporté ; ils ne nécessitent pas de modification du profil habituel. Le seul test de rechargement demande encore la création effective d’une sauvegarde tardive dans le laboratoire.

## Préservation et modifications effectives

Le contrôle final `PRESERVATION_AFTER.json` vérifie : **2 996/2 996 fichiers runtime normaux identiques**, **80/80 fichiers du profil normal et sauvegardes suivis identiques**, **3/3 fichiers diplomatiques protégés identiques**, index Git et HEAD inchangés, exécutable Steam inchangé, COMPACT identique à la version intégrée. Le fichier principal du lanceur est identique ; aucun playset normal n’a été modifié par le protocole. Le contrôle n’atteste pas un hash de tous les fichiers de chaque installation.

Les seuls ajouts dans le dépôt sont les outils de cette enquête et ses rapports/preuves. Les copies de runtime, configurations et sauvegardes d’essai sont dans le laboratoire Temp. Un seul fichier runtime a été modifié dans la copie de diagnostic, jamais dans le mod principal. Aucun changement de carte, de lois, de journaux du produit, de technologies ou de diplomatie Russie–Kazakh. Aucun commit, push, fusion, changement de branche ou nettoyage de travaux existants.

Le premier contrôle de préservation avait mal décodé les noms accentués sous le défaut Windows cp1252 ; il est conservé comme `PRESERVATION_AFTER_ENCODING_PROBE.json`. La vérification finale lit explicitement l’UTF-8 et recalcule les empreintes. Aucun fichier n’a été restauré ou déplacé dans le profil normal pour corriger cette erreur de lecture.

## Reproduction et preuves

- `REPRODUCING_FR.md` : procédure, réglages, interactions et limites.
- `BENCHMARKS.csv`, `BENCHMARK_QUALITY.json`, `BENCHMARKS_EXTENDED.json` : résultats et exclusions explicites.
- `runtime/*/LAUNCH.json`, `SETTINGS.json`, `CONTENT_LOAD.json`, `CONTINUOUS_CPU_RAM.csv`, journaux et `ENGINE_RESULTS*.json` : preuves par passage.
- `DIAGNOSTIC_PREPARATION.json`, `DIAGNOSTIC_TRACE_REVISION.json` : différence isolée et chargement.
- `UI_OBSERVATIONS.json` : interventions connues ; la réduction de vitesse MAIN3 et son exclusion sont également enregistrées dans BENCHMARK_QUALITY.
- `PRESERVATION_BEFORE.json` / `PRESERVATION_AFTER.json` : protection du travail existant.

La télémétrie conserve une alerte de métadonnée `short_description` au chargement, commune aux séries principales. Ses effets et événements sont montés et exécutés. Cette alerte et les erreurs de contenu déjà présentes doivent être séparées des coûts de simulation ; leur présence ne démontre pas la cause du ralentissement.

**Statut final de l’enquête : mesures acquises, cause précise encore ouverte, aucun correctif produit validé.** L’issue 56 doit rester ouverte pour les expériences discriminantes restantes.
