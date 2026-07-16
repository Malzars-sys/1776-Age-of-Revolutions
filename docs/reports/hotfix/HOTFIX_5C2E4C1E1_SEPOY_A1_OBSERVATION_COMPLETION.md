# HOTFIX-5C2E4C1E1 - Complément d'observation Sepoy A-1

## 1. Résumé

La sauvegarde post-option produite en C1E a été chargée une seule fois avec la
copie jetable du mod. L'événement `sepoy_mutiny_events.2` n'a pas été rejoué,
aucune option n'a été sélectionnée et le temps n'a pas été avancé. Les sept
régions étatiques ont été ouvertes directement dans l'interface, y compris les
encadrés des régions divisées.

Les transferts prioritaires, génériques et le reliquat britannique sont
cohérents. COO et JEY existent toujours, disposent de leur propre capitale et
de leur propre marché, et ne sont plus sujets de BIC. BIC ne possède plus de
territoire. La sauvegarde est restée strictement inchangée.

**Verdict : `PASS_A1_RUNTIME_OBSERVATION_COMPLETE`.**

## 2. État Git initial

- Racine : `C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork`.
- Branche : `hotfix-dlc-audit`.
- HEAD : `53a7f48 Test Sepoy general breakup runtime`.
- Le commit HOTFIX-5C2E4C1E est présent.
- Aucun fichier suivi n'était modifié au début de C1E1.
- Stash présent et non appliqué : `WIP NAVY-3C-3 Maratha Konkan Flotilla`.

## 3. Exception docs/research/technology

`docs/research/technology/` était et reste la seule exception non suivie
préexistante. Ce dossier n'a été ni modifié, ni copié, ni utilisé comme
livrable de cette phase.

## 4. Vérification de la copie

La copie `1776_Age_of_Revolutions_sepoy_test` contient exactement 952 fichiers,
aucun dossier `.git` et aucune occurrence de `remote_file_id`. Les huit fichiers
des deux harnais sont présents. Les contrôles suivants ont conservé leurs
SHA-256 de référence :

| Contrôle | SHA-256 |
|---|---|
| Décision racine | `E8CC4B78AB7447A5CED31C525B99814542C82AEEE5C47C530446870772C120FF` |
| Event racine | `E69B386716B7E33BC311CF3450C89B0605A0E92AA6C74B689591171810D156EE` |
| Localisation EN racine | `93BF3B0FEF1FD871ABE77ED8CA4EBDCD7258ED7F085F9928B6E103D4F0BFA6EF` |
| Localisation FR racine | `59EAC034463C9976944AF8E170912ED4C3C20329E08D749EC0FD901096B67C87` |
| Décision A-1 | `74642E139F07C58A8184759FB1140F2741D5622DA3A17B3810D017328E43E3A1` |
| Event A-1 | `82569A22DD65DED1385FAB993E6D9243C49558ECF46E744C3CE70EF353C9523A` |
| Localisation EN A-1 | `3A0ABAD442262E0F20E76C23BDBBB596D0914EBC8FCB373715663907695863E9` |
| Localisation FR A-1 | `791FEF8CD8240C88D7BD3AA2EB87CB99FCCD31A73529D428F6FD332BCAD720B3` |
| JE Sepoy | `DAEFCB59CCF6B303D2E39C948D8038006C1346AFE40A2B812D45EE4D947E361C` |
| Events Sepoy | `557936500AC585F7F69B9F5B063BDDA377AFF4A5AFAA06C70650C55D4AD612F7` |
| `descriptor.mod` | `1921791546626A938E18EEADC765538120325AFA87E0EA309C2C3C6502175B40` |
| Marqueur de sécurité | `280066169F9D9D7020FEF4342264D18C5B1613CA40B74D519ADD4E7F3492838A` |

Aucun nouveau fichier de scénario n'a été trouvé.

## 5. Vérification de la sauvegarde

- Fichier : `HOTFIX_5C2E4C1E_A1_POST_OPTION_1776_01_01.v3`.
- Taille avant et après : `8 021 077` octets.
- LastWriteTime UTC avant et après : `2026-07-15T20:58:31.9880636Z`.
- SHA-256 avant et après :
  `3A212C66985F5E12C22F2680E275F20A9144600260F1F4119F4980B980FA67C8`.

La sauvegarde n'a donc pas été réécrite.

## 6. Vérification du playset

L'utilisateur a confirmé et illustré que `playset1` contenait uniquement
`1776_Age_of_Revolutions_sepoy_test`, activé. Le fork principal et les autres
versions 1776 n'étaient pas actifs simultanément.

## 7. Chargement post-option

Seule la sauvegarde post-option C1E a été chargée. Aucune sauvegarde pré-option
n'a été ouverte, aucune console n'a été utilisée et aucune décision ou option
Sepoy n'a été rejouée.

## 8. Pays et date après chargement

- Pays joué : `GBR`, Grande-Bretagne.
- Date : 2 janvier 1776.
- Jeu en pause pendant les observations.
- Aucune fenêtre Sepoy ouverte.
- Interface et carte fonctionnelles.

## 9. Observation East Bengal

`STATE_EAST_BENGAL`, localisé **Purbo Bongo**, appartient à `COO`, Cooch Behar.
Le panneau indique un État de Cooch Behar, sans occupation visible. Le
controller suit donc l'owner. COO est un receveur générique valide : culture
primaire bengalie, `heritage_gangetic`, groupe sud-asiatique, capitale effective
Cooch Behar en Inde du Nord.

## 10. Observation Bihar

`STATE_BIHAR` appartient à `NAG`, Nagpur. Le controller suit l'owner. NAG est
un receveur générique valide : culture primaire marathe,
`heritage_deccani`, groupe sud-asiatique, capitale configurée dans
`STATE_CENTRAL_PROVINCES`, zone admise par le filtre. Aucun owner nul n'est
visible.

## 11. Observation West Bengal

`STATE_WEST_BENGAL`, localisé **Poshchim Bongo**, appartient à `COO`, Cooch
Behar. Le résultat C1E est reconfirmé textuellement. Cooch Behar est devenu la
capitale effective de COO et le pays possède son propre marché.

## 12. Observation Awadh

`STATE_AWADH` est divisé entre :

- `AWA`, Awadh, pour la portion locale préexistante ;
- `MUG`, Hindoustan, pour **Awadh moghol**, ancienne portion BIC.

Le transfert BIC vers MUG correspond à la branche prioritaire du code lorsque
AWA et MUG existent. Les controllers suivent les owners respectifs.

## 13. Observation Bundelkhand

`STATE_BUNDELKHAND` appartient à `MARATH`, Confédération marathe. Le controller
suit l'owner. MARATH est un receveur générique valide : culture primaire
marathe, `heritage_deccani`, capitale dans `STATE_BOMBAY` en Inde du Sud et
voisinage admissible attesté par le setup statique C1D.

## 14. Observation Circars

`STATE_CIRCARS`, localisé **Circars septentrionaux**, est divisé entre :

- `HYD`, Hyderabad, pour **Andhra**, ancienne portion BIC ;
- `JEY`, Jeypore, pour sa portion préexistante.

Le transfert prioritaire vers HYD a donc été exécuté. Les controllers suivent
les owners respectifs.

## 15. Observation Pegu

`STATE_PEGU`, localisé **Pégou**, est divisé entre :

- `BUR`, Birmanie ;
- `GBR`, Grande-Bretagne, pour **Pégou britannique**, ancienne portion BIC ;
- `DENNOR`, Danemark-Norvège.

La condition de transfert prioritaire vers BUR n'étant pas satisfaite pour la
portion BIC dans ce setup, celle-ci est restée dans le reliquat annexé par GBR.
Le résultat est cohérent avec le code. Aucun controller incohérent n'est
visible.

## 16. Tableau récapitulatif des owners/controllers

| State region | Owner(s) observé(s) | Controller(s) | Traitement de l'ancienne portion BIC |
|---|---|---|---|
| `STATE_EAST_BENGAL` | `COO` | `COO` | générique valide |
| `STATE_BIHAR` | `NAG` | `NAG` | générique valide |
| `STATE_WEST_BENGAL` | `COO` | `COO` | transfert confirmé vers COO |
| `STATE_AWADH` | `AWA`, `MUG` | mêmes owners | priorité MUG |
| `STATE_BUNDELKHAND` | `MARATH` | `MARATH` | générique valide |
| `STATE_CIRCARS` | `HYD`, `JEY` | mêmes owners | priorité HYD |
| `STATE_PEGU` | `BUR`, `GBR`, `DENNOR` | mêmes owners | reliquat GBR |

## 17. Validation des receveurs génériques

| State | Receveur | Culture | Héritage | Capitale admissible | Classement |
|---|---|---|---|---|---|
| East Bengal | `COO` | bengali | `heritage_gangetic` | oui, Inde du Nord | `VALID_RANDOM_RECEIVER` |
| Bihar | `NAG` | marathi | `heritage_deccani` | oui, zone indienne admise | `VALID_RANDOM_RECEIVER` |
| Bundelkhand | `MARATH` | marathi | `heritage_deccani` | oui, Inde du Sud | `VALID_RANDOM_RECEIVER` |

Les trois pays satisfont le groupe d'héritage sud-asiatique, possèdent une
capitale admissible et ne sont ni nuls ni invalides.

## 18. Statut diplomatique de COO

COO existe après dissolution. Son owner principal est Cooch Behar, sa capitale
effective est Cooch Behar et l'interface affiche **Marché cooch behari** comme
marché propre. Aucun overlord n'est affiché et BIC a disparu territorialement.
COO est donc réellement indépendant et n'a pas reçu de nouvel overlord par le
même effet.

## 19. Statut diplomatique de JEY

JEY existe après dissolution. Son owner principal est Jeypore, sa capitale
effective est Jeypore et l'interface affiche **Marché jeypore** comme marché
propre. Aucun overlord n'est affiché et BIC a disparu territorialement. JEY est
donc réellement indépendant et n'a pas reçu de nouvel overlord par le même
effet.

## 20. Statut final de BIC

BIC n'apparaît plus comme pays territorial. Aucun des sept states ciblés ne
porte BIC comme owner ou controller. L'entrée économique de la Compagnie des
Indes orientales dans le panneau des compagnies n'est pas un pays territorial
et ne contredit pas ce résultat.

## 21. Traitement final du reliquat par GBR

GBR est le pays joué après l'option 2.a. La portion **Pégou britannique** est
directement observée comme propriété de GBR. L'annexion du reliquat BIC et le
changement de pays joué sont donc confirmés.

## 22. Absence de state invalide

Les sept régions ont au moins un owner textuel. Les régions divisées listent
explicitement tous leurs owners. Aucun state sans owner, pays invalide,
controller discordant ou occupation incohérente n'a été observé.

## 23. Analyse des logs de chargement

Les logs de cette session documentent uniquement le chargement et
l'observation, pas une seconde exécution de l'event 2.

- zéro occurrence `sepoy` dans `error.log` ;
- zéro référence au harnais C1E/C1E1 ;
- zéro `Invalid scope` ;
- zéro `Parsing Error` ;
- zéro `invalid state` ou `invalid country` ;
- zéro erreur de chargement de sauvegarde ;
- 39 lignes `PostValidate`, toutes hors Sepoy et hors harnais ;
- 313 blocs `Script system error`, dont 293 sont la dette répétitive
  `Invalid right side during comparison 'sr'` à
  `common/ai_strategies/00_default_strategy.txt:2836`.

Les autres erreurs ponctuelles pointent des domaines globaux préexistants
(Meiji, notifications navales, anciens bâtiments, pays historiques et GUI).
Aucune Script location ne pointe vers les deux fichiers Sepoy ou les huit
fichiers de harnais.

## 24. Confirmation que l'event n'a pas été rejoué

La session a commencé sur la sauvegarde post-option, avec GBR déjà joué et
l'événement fermé. Aucune décision, option, console ou commande de temps n'a
été utilisée. Les observations ne créent donc aucune nouvelle variance
aléatoire.

## 25. Résumé du CSV

Le CSV complémentaire contient les sept régions, BIC, GBR, COO, JEY, la
sauvegarde, l'absence d'owner nul et l'absence de modification de sauvegarde.
Les transferts prioritaires sont `PASS`, les trois receveurs génériques sont
`VALID_RANDOM_RECEIVER` et les contrôles d'intégrité sont `PASS`.

## 26. Verdict

**`PASS_A1_RUNTIME_OBSERVATION_COMPLETE`**

Tous les owners manquants ont été observés directement, les transferts
prioritaires correspondent au code, les receveurs génériques sont valides,
COO et JEY sont indépendants, BIC n'a plus de territoire, le reliquat est
détenu par GBR et la sauvegarde est inchangée.

## 27. Mise à jour du niveau de confiance A-1

Le niveau de confiance passe de `PARTIAL_A1_RUNTIME` à un PASS fonctionnel
complet pour le scénario A-1 et son option 2.a. Le présent complément ne
réexécute pas le comportement : il complète la preuve visuelle du résultat
déjà produit en C1E.

## 28. Recommandation pour A-2 et A-3

A-2 et A-3 peuvent être préparés dans des phases séparées, avec leur propre
copie ou état jetable, leur propre sauvegarde baseline et un protocole
d'observation state par state défini avant exécution. Aucun travail A-2/A-3
n'a été commencé ici.

## 29. Liste exacte des fichiers créés

- `docs/reports/hotfix/HOTFIX_5C2E4C1E1_SEPOY_A1_OBSERVATION_COMPLETION.md` ;
- `docs/reports/hotfix/HOTFIX_5C2E4C1E1_A1_OWNER_COMPLETION.csv`.

## 30. Confirmation gameplay et harnais

Aucun fichier gameplay, événement, journal entry, localisation de jeu,
harnais ou descripteur n'a été modifié. La copie jetable est intacte.

## 31. Confirmation de la sauvegarde

La taille, le LastWriteTime et le SHA-256 de la sauvegarde post-option sont
strictement identiques avant et après la session.

## 32. Confirmation docs/research/technology

`docs/research/technology/` demeure l'exception non suivie préexistante et n'a
pas été modifié pendant C1E1.

## 33. Confirmation du stash MARATH

Le stash `WIP NAVY-3C-3 Maratha Konkan Flotilla` reste présent, non appliqué et
intact. Aucun `git stash pop` et aucun commit automatique n'ont été exécutés.
