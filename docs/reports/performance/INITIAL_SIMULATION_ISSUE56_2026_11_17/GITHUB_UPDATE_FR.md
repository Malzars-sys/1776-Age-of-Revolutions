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

