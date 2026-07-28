# HOTFIX — QA runtime des formations militaires Victoria 3 1.13

## 1. Identification

- Phase : `MILITARY_FORMATIONS_1_13_RUNTIME_QA`
- Commit initial testé :
  `c6c9429f4f11f28fac744702fc8dc58aeb790563`
  (`Update military formations for Victoria 3 1.13`)
- Correctif runtime séparé :
  `3b02b2a` (`Correct military formation HQ regions after runtime QA`)
- Branche : `hotfix-dlc-audit`
- Version : Victoria 3 `1.13.0`, nom de version launcher `Matcha`,
  installation `Victoria 3 The Great Wave`
- Date du test : 28 juillet 2026

Cette phase est une validation autonome de la migration des formations. Elle
n’utilise aucune numérotation `6A` et ne commence pas
`HOTFIX_6A3F_DEI_TARGETED_FIX`.

## 2. Périmètre et protections

Le périmètre couvre les huit fichiers de formations du commit `c6c9429`, le
contrôle de fumée du fichier Afrique du Nord resté identique à son parent, le
correctif minimal de QG et la présente documentation.

Sont restés hors périmètre :

- `bject`, non suivi ;
- `docs/research/technology/`, non suivi ;
- `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla`,
  jamais inspecté, appliqué ou supprimé ;
- `HOTFIX-6A.3F` et `events/dei_breakup.txt`.

Le rapport statique original se trouve bien au chemin attendu
`docs/reports/hotfix/_index/army.md`. Le fichier
`03_military_formations_north_africa.txt` n’appartient pas à `c6c9429`.

## 3. Montage du jeu

Le launcher utilisait le playset dédié `hhhh`. Sa base de données et
`content_load.json` indiquaient exactement un mod activé :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork`

Les DLC n’étaient pas désactivés. Les logs de debug ont confirmé le montage du
même dossier fork. Aucun autre mod n’était chargé.

Une copie de sécurité externe de la base du launcher a été créée avant le test :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\launcher-v2_before_military_runtime_20260728.sqlite`

## 4. Nombre de lancements

Trois lancements complets ont été nécessaires :

1. lancement de `c6c9429`, qui a exposé des formations absentes ;
2. partie neuve après le correctif `3b02b2a`, contrôle des pays, création de la
   sauvegarde du 1er février et progression jusqu’au 1er mai ;
3. recharge dédiée, car la sauvegarde n’avait pas été rechargée avant la
   fermeture du deuxième lancement.

Toutes les ouvertures et manipulations du jeu ont été effectuées par
l’opérateur. Le troisième lancement a chargé la sauvegarde au 1er février 1776,
confirmé GBR, RUS et SWE nominaux, puis laissé passer trois mois avant fermeture.

## 5. Régression trouvée dans `c6c9429`

Le premier runtime a révélé douze formations utilisant un QG valide dans les
définitions 1.13, mais sans ancrage territorial pour le pays concerné. Le moteur
ne créait alors pas la formation. Ce défaut était visible dans l’interface mais
n’émettait pas de diagnostic ciblé dans `error.log`.

| Pays | Formation | QG dans `c6c9429` | QG corrigé |
|---|---|---|---|
| FRA | `2e_Corps_dArme` | `region_western_europe` | `region_southern_europe` |
| GBR | `Army_of_India` | `region_north_india` | `region_south_india` |
| RUS | `Chernomorskiy_Flot` | `region_eastern_europe` | `region_balkans` |
| SWE | `Kungliga_Svenska_Armn` | `region_eastern_europe` | `region_northern_europe` |
| DENNOR | `Hren` | `region_eastern_europe` | `region_northern_europe` |
| SC2 | `Ejrcito_de_la_Nueva_Granada` | `region_andes` | `region_gran_colombia` |
| SC2 | `Ejrcito_de_Venezuela` | `region_andes` | `region_gran_colombia` |
| TUR | `Anadolu_Ordusu` | `region_balkans` | `region_near_east` |
| DUR | 7e armée anonyme | `region_south_india` | `region_greater_persia` |
| DUR | 8e armée anonyme | `region_south_india` | `region_greater_persia` |
| BHV | `BhavnagarArmy` | `region_south_india` | `region_north_india` |
| SIN | `SindhArmy` | `region_south_india` | `region_north_india` |

Le correctif `3b02b2a` est limité à ces douze valeurs `hq_region` dans quatre
fichiers. Il ne modifie aucun nom, personnage, groupe d’unités, nombre d’unités
ou type d’unité. `c6c9429` n’a pas été amendé.

## 6. Contrôle de la partie neuve corrigée

Pays réellement observés pendant les deux premières sessions :

- Europe : GBR, FRA, SPA, RUS, AUS, PRU, SWE, DENNOR, NET, POR et SIC ;
- Amériques : USA, BRZ et SC2 ;
- Moyen-Orient et Inde : PER, TUR, DUR, BIC, BHV et SIN ;
- Asie : JAP ;
- Afrique du Nord : TUN, TRI et MAS ;
- Afrique subsaharienne : AGC.

Le tag saisi pour Maratha renvoyait `empty tag` et n’est donc pas compté comme
un pays contrôlé. Danemark-Norvège a finalement été sélectionné par
Ctrl-clic sur son territoire, après l’échec de la saisie d’un tag textuel.

Résultats principaux après `3b02b2a` :

| Pays | Résultat observé |
|---|---|
| GBR | 4 armées et 9 flottes créées et placées ; `Army_of_India` restaurée |
| FRA | 3 armées et 4 flottes ; le corps corrigé se trouve en Europe du Sud |
| SPA | 3 armées et 2 flottes au démarrage |
| RUS | 7 armées et 2 flottes ; Baltique et mer Noire présentes |
| SWE | 1 armée et 1 flotte en Europe du Nord |
| DENNOR | `Hæren` et `Kongelige Danske Marine` en Europe du Nord |
| TUR | 4 armées et 1 flotte |
| DUR | 8 armées créées ; noms anonymes hérités du script |
| BHV | 1 armée créée au QG de l’Inde du Nord |
| SIN | 1 armée créée au QG de l’Inde du Nord |
| SC2 | 3 armées créées, dont les deux armées corrigées |

Les contrôles du premier lancement avaient aussi confirmé les formations
présentes de AUS, PRU, NET, POR, SIC, USA, BRZ, PER, BIC, JAP, TUN, TRI, MAS et
AGC. Les formations manquantes de ce lancement sont celles corrigées ci-dessus.

## 7. Japon

La partie neuve contient :

- `Edo_Guard_Army`, 26 unités ;
- `Kinai_Guard_Army`, 20 unités ;
- `Kyushu_Guard_Army`, 12 unités.

Les trois armées totalisent donc 58 unités au démarrage. Les dix groupes
`combat_unit` restaurés sont présents statiquement dans le bloc JAP et ont
produit ces trois formations avec des types terrestres 1.13 valides au QG
`region_northeast_asia`.

La sauvegarde du 1er février conserve les trois objets de formation. Après un
mois d’IA et de nombreux changements de pays par l’opérateur, l’IA a redistribué
les unités entre les armées ; cette évolution dynamique n’est pas un échec
d’initialisation.

Verdict : `JAPAN_GUARD_ARMIES_RUNTIME_PASS`.

## 8. `Regular_Army`

USA charge avec 3 armées, dont `Regular_Army`, et 6 flottes. L’analyse de la
sauvegarde associe `Regular_Army` au QG terrestre
`region_atlantic_coast`.

`region_new_england` apparaît dans les trois sessions uniquement dans le
diagnostic préexistant et sans rapport
`common/ai_strategies/00_default_strategy.txt:4808`. Il n’apparaît pas comme QG
de la formation américaine et aucune erreur de formation ne le vise.

Verdict : `REGULAR_ARMY_ATLANTIC_COAST_RUNTIME_PASS`.

## 9. Espagne et amiraux

Au démarrage, SPA possède 3 armées et 2 flottes au bon emplacement. Les deux
créations ajoutées, `spanishnavy1_gen` et `spanishnavy2_gen`, matérialisent deux
amiraux espagnols ayant les traits attendus.

Au 1er février, l’IA a regroupé les deux flottes identiques en une seule
formation. La sauvegarde conserve les deux amiraux créés le 1er janvier :
l’un commande la flotte restante et l’autre est sans affectation après la
fusion. Il s’agit d’une réorganisation de l’IA postérieure à l’initialisation,
pas d’un échec du script.

Aucune erreur ne vise un des 24 anciens amiraux retirés et aucune erreur de
transfert vers leurs anciennes flottes n’apparaît.

## 10. Perse

PER possède bien 2 armées distinctes et aucune flotte. Les noms génériques sont
ceux des deux blocs successifs `c:PER`; aucun écrasement, doublon invalide ou
diagnostic de création n’a été observé.

Verdict : `PERSIAN_DUAL_FORMATION_RUNTIME_PASS`.

## 11. Afrique

Le contrôle de fumée Afrique du Nord confirme :

- TUN : 1 armée et 1 flotte ;
- TRI : 1 armée et 1 flotte ;
- MAS : 1 armée.

Les trois pays chargent leurs formations aux bons emplacements. Les noms
génériques de certaines armées sont du contenu existant et non une corruption
du fichier restauré.

Le contrôle subsaharien a utilisé le tag réellement défini AGC : `Armée
d’Angoche` est créée au QG d’Afrique de l’Est.

Verdict : `NORTH_AFRICA_FORMATIONS_SMOKE_PASS` et
`SUBSAHARAN_AFRICA_FORMATION_SMOKE_PASS`.

## 12. Sauvegarde, recharge et passage du temps

Sauvegarde dédiée :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\save games\qa_3b02b2a_military_1_13.v3`

Elle a été créée le 1er février 1776. Le deuxième lancement a progressé jusqu’au
1er mai avant fermeture. Le troisième lancement a rechargé cette sauvegarde au
1er février, puis a progressé de nouveau jusqu’au 1er mai.

Le journal serveur dédié confirme des ticks de `1776.2.1.6` à `1776.5.1.6`.
L’opérateur a confirmé après recharge que GBR, RUS et SWE étaient nominaux.
Aucun crash nouveau n’a été créé.

Verdict : `SAVE_RELOAD_AND_THREE_MONTHS_PASS`.

## 13. Analyse des logs

Les signatures liées aux fichiers de formations sont identiques dans le
premier lancement, le retest et la recharge. Aucune erreur restante ne vise :

- `create_military_formation` ou un QG corrigé ;
- un `ship_type` ou `combat_unit_type` inconnu ;
- `Edo_Guard_Army`, `Kinai_Guard_Army` ou `Kyushu_Guard_Army` ;
- `region_atlantic_coast` ;
- le transfert d’un ancien amiral vers une flotte supprimée.

Les erreurs nouvelles attribuables à `c6c9429` étaient les douze absences
fonctionnelles de la section 5. Elles n’avaient pas de ligne de log dédiée et
sont corrigées par `3b02b2a`.

Quatre signatures de dette antérieure restent volontairement non corrigées :

1. `create_character` retourne faux dans
   `05_military_formations_india.txt:206`, car le général bengali utilise
   `ideology = moderate` ;
2. `madras_army` est utilisé sans avoir été défini ;
3. `maitland_gen` est utilisé sans avoir été défini ;
4. `aylmer_gen` est utilisé sans avoir été défini.

Le fichier Europe crée Matthew Whitworth sous `colborne_gen`, scope déjà utilisé
par John Colborne, puis tente de transférer `aylmer_gen`. Le scope réutilisé
n’émet pas sa propre erreur mais fait partie de la même dette.

Impact observable : le général bengali invalide n’est pas créé ; les transferts
vers les scopes inexistants ne se produisent pas. Les armées BIC et
britanniques concernées existent néanmoins. Ces défauts doivent être corrigés
dans une phase séparée.

Les diagnostics d’anciennes APIs navales dans
`events/tech_events/naval_tech_events.txt`, les erreurs de stratégies IA et les
autres milliers de diagnostics généraux du mod sont préexistants ou étrangers
aux fichiers de formations.

## 14. Archives de preuve

Les logs de chaque étape sont conservés hors du dépôt :

- échec initial :
  `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\logs_archive\military_formations_qa_c6c9429_failed_20260728`
- partie neuve corrigée :
  `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\logs_archive\military_formations_qa_3b02b2a_pre_reload_20260728`
- recharge :
  `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\logs_archive\military_formations_qa_3b02b2a_reload_20260728`

Aucun nouveau dossier de crash n’a été produit. Le seul dossier trouvé était
antérieur à cette QA.

## 15. Fichiers et commits

Correctif gameplay `3b02b2a` :

- `common/history/military_formations/00_military_formations_europe.txt`
- `common/history/military_formations/02_military_formations_south_america.txt`
- `common/history/military_formations/04_military_formations_middle_east.txt`
- `common/history/military_formations/05_military_formations_india.txt`

La documentation de clôture comprend le présent rapport, l’addendum de
`army.md`, l’index global, le catalogue, la matrice de blocs et la roadmap.

## 16. Verdict final

- `MILITARY_FORMATIONS_1_13_RUNTIME_QA_COMPLETE`
- `MILITARY_FORMATIONS_HQ_RUNTIME_PASS`
- `JAPAN_GUARD_ARMIES_RUNTIME_PASS`
- `REGULAR_ARMY_ATLANTIC_COAST_RUNTIME_PASS`
- `PERSIAN_DUAL_FORMATION_RUNTIME_PASS`
- `NORTH_AFRICA_FORMATIONS_SMOKE_PASS`
- `SUBSAHARAN_AFRICA_FORMATION_SMOKE_PASS`
- `SAVE_RELOAD_AND_THREE_MONTHS_PASS`
- `PREEXISTING_MILITARY_FORMATION_DEBT_CONFIRMED`
- `HOTFIX_6A3F_NOT_STARTED`

Le périmètre formations de `c6c9429`, corrigé par `3b02b2a`, est validé en
partie neuve et après sauvegarde/recharge. Cette validation ne ferme ni le bloc
NAVY global, ni le runtime global final de la roadmap.
