# HOTFIX-5C2E4C1E - Test runtime Sepoy A-1

## 1. Resume

Le scenario jetable A-1 a ouvert l'evenement reel `sepoy_mutiny_events.2` sur
BIC et seule l'option `2.a` a ete choisie. Les effets immediats ont termine,
l'evenement s'est ferme, l'interface est restee reactive et le pays joue est
devenu GBR. Aucun crash, gel ou erreur de log attribuable a Sepoy ou au
harnais A-1 n'a ete observe.

Le verdict est **`PARTIAL_A1_RUNTIME`**. Le comportement central est valide,
mais les proprietaires de plusieurs states redistribues aleatoirement n'ont
pas ete ouverts individuellement avant la fermeture du jeu. Ils restent donc
`NOT_OBSERVABLE` plutot que d'etre deduits comme des observations runtime.

## 2. Etat Git initial

- Racine : `C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork`.
- Branche : `hotfix-dlc-audit`.
- HEAD : `d305df7 Prepare Sepoy general breakup test` (HOTFIX-5C2E4C1D).
- Aucun fichier suivi modifie.
- Stash present : `stash@{0}: WIP NAVY-3C-3 Maratha Konkan Flotilla`.

## 3. Exception docs/research/technology

`docs/research/technology/` etait la seule exception non suivie avant le test.
Ses sept fichiers ont conserve leurs hashes de reference apres la session.

## 4. Verification de la copie C1D

- Copie presente avec exactement 952 fichiers.
- Aucun dossier `.git`.
- Aucune occurrence de `remote_file_id`.
- Les quatre fichiers du harnais racine et les quatre fichiers A-1 etaient
  presents, tous avec BOM UTF-8.
- Aucun autre fichier de scenario n'a ete trouve.
- Le fork et la copie n'ont pas ete actives simultanement.

## 5. Hashes avant lancement

| Controle | SHA-256 | Statut |
|---|---|---|
| Decision A-1 | `74642E139F07C58A8184759FB1140F2741D5622DA3A17B3810D017328E43E3A1` | conforme |
| Event A-1 | `82569A22DD65DED1385FAB993E6D9243C49558ECF46E744C3CE70EF353C9523A` | conforme |
| Localisation EN A-1 | `3A0ABAD442262E0F20E76C23BDBBB596D0914EBC8FCB373715663907695863E9` | conforme |
| Localisation FR A-1 | `791FEF8CD8240C88D7BD3AA2EB87CB99FCCD31A73529D428F6FD332BCAD720B3` | conforme |
| JE Sepoy | `DAEFCB59CCF6B303D2E39C948D8038006C1346AFE40A2B812D45EE4D947E361C` | conforme |
| Events Sepoy | `557936500AC585F7F69B9F5B063BDDA377AFF4A5AFAA06C70650C55D4AD612F7` | conforme |

## 6. Verification du playset

L'utilisateur a confirme que le playset jetable etait selectionne et que
seule l'entree `1776 Sepoy Functional Test (Disposable)` etait active. Le fork
principal et les autres copies de 1776 etaient desactives. L'absence de
`remote_file_id` confirme aussi l'absence d'association Workshop dans la copie.

## 7. Horodatage initial des logs

| Log | Derniere ecriture initiale | Taille | SHA-256 |
|---|---:|---:|---|
| `error.log` | `2026-07-15 02:35:09 +00:00` | 515068 | `46A0D9A75EBC00BAF6F35EF91BD728CAF61F69397825A8B4AEF319BEC4EA0626` |
| `game.log` | `2026-07-15 02:35:09 +00:00` | 365958 | `95C724CBA74A4FC29501666FB677E90157E344628B585D1D38F54FB87FF3D934` |
| `debug.log` | `2026-07-15 02:35:30 +00:00` | 391639 | `305D19A6A96618B06B83D80B8049D87D807961692E47E90538F33583A6F83055` |

## 8. Etat BIC initial

- Pays joue : BIC.
- Date : 1er janvier 1776, en pause.
- BIC etait une compagnie a charte de GBR.
- Sujets directs visibles : COO/Cooch Behar et JEY/Jeypore.
- Une JE non-Sepoy etait visible : `Bataille pour l'Inde`.
- Aucune JE Sepoy n'etait active.
- Les decisions racine et de preparation A-1 etaient visibles.

## 9. Capitales effectives de COO et JEY

- COO : Cooch Behar.
- JEY : Jeypore.

## 10. Releve territorial initial

La baseline et le controle visuel confirmaient des portions BIC dans
`STATE_EAST_BENGAL`, `STATE_BIHAR`, `STATE_WEST_BENGAL`, `STATE_AWADH`,
`STATE_BUNDELKHAND`, `STATE_CIRCARS` et `STATE_PEGU`. HYD et MARATH etaient
visibles. MUG etait present dans le setup statique C1D, mais n'a pas ete
confirme manuellement dans l'interface avant l'option.

## 11. Execution de la preparation

La decision `Preparer le test de dissolution Sepoy A-1` a ouvert l'avertissement
attendu. Seule l'option `Marquer cette session jetable comme prete` a ete
choisie. Le jeu est reste en pause.

## 12. Preuve d'absence de mutation pendant la preparation

La carte n'a pas change visiblement, BIC est reste le pays joue et sujet de
GBR, et COO/JEY sont restes ses sujets. Aucune JE Sepoy ni option territoriale
n'est apparue. Seule la decision d'ouverture destructive est devenue visible.

## 13. Sauvegarde pre-option

- Fichier : `HOTFIX_5C2E4C1E_A1_PRE_OPTION_1776_01_01.v3`.
- Creation : `2026-07-15 20:36:17 +00:00`.
- Taille : 7905889 octets.
- SHA-256 : `DB72163CD9E469DF8C09BDDC9B508F3D6FBB2C4B030E9D020FC79ABC1A44C870`.
- La sauvegarde n'a pas ete ecrasee par la preuve post-option.

## 14. Ouverture de l'evenement reel

La decision `Ouvrir l'evenement reel de dissolution Sepoy` a ouvert
`sepoy_mutiny_events.2`, localise `Le coup de grace`, sur BIC. Aucun effet
territorial n'avait encore ete execute a l'affichage de l'evenement.

## 15. Options observees

Les options visibles comprenaient :

- `2.a` : `L'Inde est perdue. Laissons Whitehall se disputer nos ressources restantes.`
- retraite vers Calcutta (`2.b`) ;
- retraite vers Bombay (`2.c`).

Les options de retraite n'ont pas ete choisies.

## 16. Selection manuelle exclusive de 2.a

L'utilisateur a clique uniquement la premiere option, identifiee dans le
script comme `sepoy_mutiny_events.2.a`. Aucune console ni selection automatique
n'a ete utilisee.

## 17. Fin des effets immediats

Les effets ont termine sans boucle visible, sans gel et sans crash.
L'evenement s'est ferme normalement et l'interface est restee reactive.

## 18. Pays joue apres resolution

Le pays joue est devenu GBR, conformement au `play_as = c:GBR` de l'option.
La date affichee est passee au 2 janvier 1776 pendant le traitement moteur,
sans avance manuelle du temps.

## 19. Statut final de BIC

BIC n'etait plus visible comme pays territorial apres resolution et le
passage a GBR a reussi. Cela est coherent avec l'annexion finale du reliquat
BIC par GBR. La preuve visuelle n'a revele aucun territoire sans owner.

## 20. Statut final de COO et JEY

COO et JEY existaient toujours apres la resolution, avec leurs marches propres
affiches et sans presentation comme sujets BIC. Leurs capitales sont restees
Cooch Behar et Jeypore. Le breakup n'a donc pas supprime les anciens sujets.

## 21. Transferts prioritaires

Le rendu global est coherent avec les branches prioritaires de l'option :
Circars vers HYD et reliquat BIC vers GBR. Le receveur d'Awadh n'a pas ete
ouvert individuellement ; la branche MUG reste donc non observee directement.

## 22. Redistribution generique

La redistribution a termine et la carte est restee entierement coloree. Le
receveur exact de chaque state aleatoire n'a toutefois pas ete releve. Aucun
receveur generique n'est classe invalide sur la seule base d'une variance
aleatoire.

## 23. Resultats state par state

| State (portion BIC initiale) | Resultat runtime | Evaluation |
|---|---|---|
| `STATE_EAST_BENGAL` | state colore, receveur non ouvert | `NOT_OBSERVABLE` |
| `STATE_BIHAR` | state colore, receveur non ouvert | `NOT_OBSERVABLE` |
| `STATE_WEST_BENGAL` | owner COO observe dans l'ecran `Poshchim Bongo` | `PASS` |
| `STATE_AWADH` | receveur non ouvert ; branche MUG attendue | `NOT_OBSERVABLE` |
| `STATE_BUNDELKHAND` | redistribue, receveur aleatoire non releve | `NOT_OBSERVABLE` |
| `STATE_CIRCARS` | rendu coherent avec le transfert prioritaire HYD | `PASS` |
| `STATE_PEGU` | non ouvert ; reliquat attendu chez GBR apres annexion | `NOT_OBSERVABLE` |

Aucun double ownership impossible ni state sans owner n'a ete visible.

## 24. Traitement du reliquat BIC

Le changement de pays vers GBR, la disparition territoriale de BIC et la fin
normale de l'effet confirment le traitement du reliquat. Pegu n'ayant pas ete
ouvert individuellement, son owner final reste une attente deterministe du
script plutot qu'une observation directe.

## 25. Sauvegarde post-option

- Fichier : `HOTFIX_5C2E4C1E_A1_POST_OPTION_1776_01_01.v3`.
- Creation : `2026-07-15 20:58:31 +00:00`.
- Taille : 8021077 octets.
- SHA-256 : `3A212C66985F5E12C22F2680E275F20A9144600260F1F4119F4980B980FA67C8`.
- Elle est distincte de la sauvegarde pre-option.

## 26. Fraicheur des logs

| Log | Derniere ecriture finale | Taille | SHA-256 |
|---|---:|---:|---|
| `error.log` | `2026-07-15 21:02:30 +00:00` | 24868 | `2625371C17606E17B3095E7E863912B94BDDC3CF53FB8DAD9EE5710975E39B64` |
| `game.log` | `2026-07-15 21:02:30 +00:00` | 107235 | `AB94AAA7BBC1AD8D43FA5239C1ECB402D3D04DEEDCEFD9093C436D0D45B2B9C0` |
| `debug.log` | `2026-07-15 21:02:42 +00:00` | 463211 | `66AB0FB90B368891DE78D3C9471F5F52F867ACB94D32D09BFD118D2119A3FFF3` |

Les trois hashes et horodatages differaient de l'etat initial. Le processus
`victoria3` etait arrete avant l'analyse.

## 27. Analyse des logs A-1

La recherche exacte dans les trois logs a retourne zero occurrence pour :

- `sepoy_mutiny_events.2` ;
- `zz_sepoy_test_a1` et `zz_sepoy_functional_test_a1` ;
- `random_scope_state`, `any_neighbouring_state`, `set_state_owner` ;
- `make_independent`, `play_as` ;
- les sept IDs de state cibles.

Il n'existe donc aucune erreur de script, scope, transfert ou boucle attribuable
a A-1 dans les logs de cette session.

## 28. Diagnostics globaux hors perimetre

`error.log` contient 120 erreurs `Invalid right side during comparison 'sr'`
dans d'autres JE, notamment `07_american_mod_jes.txt`,
`02_south_america_migration.txt`, `07_hindustan_is_durrani_mod.txt` et
`05_balkan_national_awakening.txt`. Il contient aussi cinq erreurs de variante
de loi dans `common/interest_groups/00_landowners.txt:459` et des erreurs GUI.
Ces lignes ne pointent ni les events Sepoy ni le harnais A-1. Des diagnostics
plus anciens de `debug.log` ont egalement ete exclus faute d'attribution A-1.

## 29. Resume du CSV

Le CSV associe chaque observation a son resultat, son niveau de determinisme
et sa preuve. Les effets centraux sont `PASS`; les owners non ouverts sont
`NOT_OBSERVABLE`.

## 30. Ecarts deterministes

Aucun ecart deterministe confirme n'a ete observe. La date a avance d'un jour
pendant les effets malgre la pause, ce qui est documente comme traitement
moteur plutot que comme echec fonctionnel.

## 31. Variance aleatoire observee

La boucle a redistribue les states sans blocage. L'identite de tous les
receveurs aleatoires n'a pas ete relevee, donc aucune variance precise ne peut
etre qualifiee au-dela de la redistribution coloree et terminee.

## 32. Verdict

**`PARTIAL_A1_RUNTIME`**

Tous les effets structurants ont reussi, mais le protocole exige un releve
state par state. L'absence d'observation directe pour East Bengal, Bihar,
Awadh, Bundelkhand et Pegu interdit un `PASS_A1_RUNTIME` strict.

## 33. Ce que le test valide

- preparation sans mutation visible du monde ;
- ouverture manuelle de l'event reel sur BIC ;
- disponibilite et execution exclusive de `2.a` ;
- fin de la boucle et des effets sans crash ni blocage ;
- passage du pays joue a GBR ;
- survie et autonomie apparente de COO/JEY avec capitales conservees ;
- annexion territoriale apparente du reliquat BIC ;
- absence d'erreur Sepoy/A-1 dans les logs ;
- integrite des fichiers avant et apres runtime.

## 34. Ce que le test ne valide pas

- l'owner/controller individuel de cinq des sept states apres redistribution ;
- l'identite exacte de chaque receveur aleatoire ;
- les options `2.b`, `2.c` ou `2.e` ;
- les autres scenarios A-2/A-3 ;
- une campagne prolongee apres le breakup.

## 35. Recommandation concernant A-2/A-3

Ne pas reutiliser les sauvegardes A-1 comme baseline. Avant A-2/A-3, effectuer
si necessaire un simple releve de la sauvegarde post-option pour fermer les
cinq owners `NOT_OBSERVABLE`, puis reconstruire chaque scenario depuis sa
baseline jetable propre.

## 36. Liste exacte des fichiers crees

- `docs/reports/hotfix/HOTFIX_5C2E4C1E_SEPOY_A1_RUNTIME_TEST.md` ;
- `docs/reports/hotfix/HOTFIX_5C2E4C1E_A1_RUNTIME_RESULTS.csv`.

## 37. Confirmation gameplay

Aucun fichier gameplay du fork ou de la copie n'a ete modifie. Seuls les deux
livrables de rapport C1E ont ete crees dans le fork.

## 38. Confirmation Sepoy et harnais

Les huit fichiers des deux harnais, les deux fichiers Sepoy, le
`descriptor.mod` de la copie et son marqueur ont conserve leurs hashes. La
copie contient toujours exactement 952 fichiers.

## 39. Confirmation docs/research/technology

Les sept fichiers de `docs/research/technology/` sont intacts et conservent
leurs hashes C1C1.

## 40. Confirmation du stash MARATH

Le stash `WIP NAVY-3C-3 Maratha Konkan Flotilla` est reste present, non applique
et non modifie. Aucun `git stash pop` ni commit automatique n'a ete execute.
