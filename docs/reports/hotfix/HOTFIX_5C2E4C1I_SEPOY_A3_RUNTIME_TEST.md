# HOTFIX-5C2E4C1I - Test runtime Sepoy A-3

## 1. Resume

Le scenario A-3 a ete execute cinq fois depuis une sauvegarde pre-option
immuable. A chaque execution, seule l'option 2.a de
`sepoy_mutiny_events.2` a ete choisie. L'ancienne portion BIC de
`STATE_BUNDELKHAND` a ete attribuee cinq fois a `MARATH`, qui appartient bien
a l'ensemble autorise `{ MARATH, NAG }`. Chaque boucle s'est terminee, BIC a
ete annexee, le pays joue est devenu GBR et aucun crash, blocage, owner nul ou
troisieme receveur n'a ete observe.

**Verdict : `PASS_A3_RUNTIME`.**

## 2. Etat Git initial

- Racine : `C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork`.
- Branche : `hotfix-dlc-audit`.
- HEAD : `6d84956 Prepare Sepoy two-receiver test` (HOTFIX-5C2E4C1H).
- Aucun fichier suivi n'etait modifie.
- Le stash MARATH etait present et n'a pas ete applique.

## 3. Exception docs/research/technology/

Les sept fichiers non suivis deja presents sous `docs/research/technology/`
etaient l'unique exception concurrente. Ils n'ont ete ni modifies, ni deplaces,
ni ajoutes a Git pendant le test.

## 4. Verification de la copie C1H

La copie jetable
`C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_sepoy_test`
a ete controlee avant et apres le runtime :

- 960 fichiers exactement ;
- aucun dossier `.git` ;
- aucune occurrence `remote_file_id` ;
- 16 fichiers de harnais exactement : racine, A-1, A-2 et A-3 ;
- aucun scenario B/C/E/F ;
- 25/25 entrees du manifeste C1H conformes en taille et SHA-256, y compris le
  descripteur launcher situe hors de la copie ;
- les deux fichiers Sepoy de la copie identiques a ceux du fork.

## 5. Verification du playset

L'utilisateur a confirme manuellement que le playset Sepoy jetable etait
selectionne, que `1776 Sepoy Functional Test (Disposable)` etait le seul mod
actif, que le fork principal etait desactive et qu'aucune autre copie 1776 ou
association Workshop n'etait active.

## 6. Horodatage initial des logs

Les metadonnees ont ete relevees avant la session A-3, sans supprimer ni
renommer les logs existants.

| Log | LastWriteTime | Taille | SHA-256 |
|---|---|---:|---|
| `error.log` | `2026-07-16T08:48:53.1700028+00:00` | 34 989 | `56F1E7C4E2A826D3DB383FF9D02959F25B4F65A769EB41FE352C617579A9393D` |
| `game.log` | `2026-07-16T08:48:53.1624892+00:00` | 183 566 | `09B5CD8C168D16001B4AD79BCDC1A62A237B3649A35AE0EFD15D57714EA586FC` |
| `debug.log` | `2026-07-16T09:08:08.1931306+00:00` | 140 948 | `1EB0B3FE531ADD3058EF54B15A68D15DF400B14F7D6B550ED59DF6A928914793` |

## 7. Creation de la partie A-3

Une nouvelle partie BIC a ete creee au 1er janvier 1776. Elle n'etait issue ni
d'A-1 ni d'A-2. Le jeu a ete mis en pause immediatement et aucun jour n'a ete
avance avant la preparation ou les choix 2.a.

## 8. Preparation A-3

La decision `Preparer le test Sepoy A-3 a deux receveurs` a ete appliquee. Le
pays joue restait BIC, sujet de GBR ; COO et JEY etaient presents ; MARATH et
NAG etaient presents ; la decision d'ouverture A-3 est devenue disponible et
aucun event Sepoy reel ne s'est ouvert automatiquement.

## 9. Preuve d'absence de mutation territoriale

La carte est restee visuellement inchangee apres la preparation. La portion
BIC de Bundelkhand etait toujours detenue par BIC. Le harnais A-3 ne pose qu'un
marqueur de session et son evenement de preparation annonce explicitement
qu'il n'effectue aucune mutation territoriale.

## 10. Observation de MARATH

`MARATH` et sa portion voisine de Bundelkhand ont ete observes. Les controles
statiques C1H attestent une culture primaire marathi, l'heritage deccani, le
groupe sud-asiatique et une capitale dans `STATE_BOMBAY`, elle-meme dans
`region_south_india`. MARATH etait donc un receveur admissible.

## 11. Observation de NAG

`NAG` et sa portion voisine ont ete observes dans le setup. Les controles
statiques C1H attestent une culture primaire marathi, l'heritage deccani, le
groupe sud-asiatique et une capitale dans `STATE_CENTRAL_PROVINCES`, dans
`region_north_india`. NAG etait donc le second receveur admissible.

## 12. Absence de troisieme receveur

Le controle combine de la topologie, des capitales et des filtres culturels n'a
identifie aucun troisieme owner voisin satisfaisant simultanement les criteres.
Bundelkhand n'appartient pas aux transferts prioritaires de l'option 2.a.

## 13. Sauvegarde pre-option

- Nom : `HOTFIX_5C2E4C1I_A3_PRE_OPTION_1776_01_01`.
- Chemin : `C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/save games/HOTFIX_5C2E4C1I_A3_PRE_OPTION_1776_01_01.v3`.
- Date en jeu : 1er janvier 1776, en pause.
- Contenu : BIC intacte, marqueur A-3 present, event reel non ouvert, aucune
  option choisie et aucun temps avance.

Aucune sauvegarde post-run n'a ete utilisee comme point de depart.

## 14. Hash et integrite de la baseline

| Taille | LastWriteTime | SHA-256 |
|---:|---|---|
| 7 909 129 | `2026-07-16T20:25:35.0363030+00:00` | `9E9A7D7884672FA16C9FA665C8E1D5BC5FC2C5DF7C4EA0DA791607C4F9F54136` |

Ces valeurs ont ete verifiees avant les rechargements et de nouveau apres la
fermeture du jeu.

## 15. Protocole commun des cinq runs

Chaque run a recharge exactement la baseline ci-dessus, est reste en pause,
a ouvert manuellement `sepoy_mutiny_events.2` sur BIC et a selectionne
exclusivement 2.a. Apres la fin des effets, Bundelkhand a ete ouvert
individuellement pour lire son owner ; l'owner n'a pas ete deduit de la seule
couleur de carte.

## 16. Resultat RUN_1

Owner final : `MARATH` (Confederation marathe). Owner unique et autorise ;
pays joue GBR ; BIC annexee ; event ferme ; boucle terminee ; aucun crash,
blocage, owner nul ou troisieme receveur.

## 17. Resultat RUN_2

Owner final : `MARATH` (Confederation marathe). Les memes controles runtime
que RUN_1 sont passes.

## 18. Resultat RUN_3

Owner final : `MARATH` (Confederation marathe). Les memes controles runtime
que RUN_1 sont passes.

## 19. Resultat RUN_4

Owner final : `MARATH` (Confederation marathe). Les memes controles runtime
que RUN_1 sont passes.

## 20. Resultat RUN_5

Owner final : `MARATH` (Confederation marathe). Les memes controles runtime
que RUN_1 sont passes. Victoria 3 a ensuite ete quitte proprement.

## 21. Tableau recapitulatif des owners

| Run | Baseline SHA-256 | Owner final | Autorise | Pays joue final | BIC annexee | Resultat |
|---|---|---|---|---|---|---|
| RUN_1 | `9E9A...F54136` | MARATH | Oui | GBR | Oui | PASS |
| RUN_2 | `9E9A...F54136` | MARATH | Oui | GBR | Oui | PASS |
| RUN_3 | `9E9A...F54136` | MARATH | Oui | GBR | Oui | PASS |
| RUN_4 | `9E9A...F54136` | MARATH | Oui | GBR | Oui | PASS |
| RUN_5 | `9E9A...F54136` | MARATH | Oui | GBR | Oui | PASS |

## 22. Nombre de resultats MARATH

`MARATH = 5`.

## 23. Nombre de resultats NAG

`NAG = 0`.

## 24. Resultats invalides

`Owner hors { MARATH, NAG } = 0`, `owner nul = 0`, `troisieme receveur = 0`
et `double ownership incoherent = 0`.

## 25. Confirmation qu'aucune distribution 50/50 n'est revendiquee

La serie MARATH x5 est valide, mais cinq observations ne demontrent ni une
distribution uniforme ni une probabilite 50/50. Le test valide le domaine des
resultats et la terminaison, pas la qualite statistique du tirage.

## 26. Terminaison des boucles

Les cinq executions ont termine leurs effets. Aucun event bloque, boucle
persistante ou attente indefinie n'a ete observe.

## 27. Statut final de BIC par run

Dans RUN_1 a RUN_5, le pays joue est passe a GBR et BIC a ete annexee apres la
redistribution, conformement a la fin de l'option 2.a.

## 28. Fraicheur des logs

| Log | LastWriteTime final | Taille finale | SHA-256 final | Frais |
|---|---|---:|---|---|
| `error.log` | `2026-07-16T21:58:55.3773740+00:00` | 323 501 | `A6D39C4B9B8CAD9E0AC8BF352388136D0285E1E674A4C32FDFB7CFF47D7EEFFE` | Oui |
| `game.log` | `2026-07-16T21:58:55.3773740+00:00` | 490 013 | `8FF5153BAF68C6467AD94C660E177D6EF93ACAD40A0ADEB86D3F3639E2922FE4` | Oui |
| `debug.log` | `2026-07-16T21:59:15.5732699+00:00` | 203 068 | `E1C26B482E4EDFA8C3181F2F62FE4C999BED9D5F2DE6CF667A91D6ACD0A83A7A` | Oui |

Les trois fichiers ont un horodatage et un hash posterieurs a l'etat initial.
Le processus `victoria3` etait arrete lors de la collecte finale.

## 29. Analyse des logs A-3

Aucune erreur d'execution ne vise `sepoy_mutiny_events.2`,
`STATE_BUNDELKHAND`, `set_state_owner`, `random_scope_state`,
`any_neighbouring_state`, un scope invalide, une boucle non terminee ou un
owner invalide. Aucun avertissement BOM, `PostValidate` ou token inattendu ne
vise A-3.

`error.log` contient cependant 810 occurrences non bloquantes de
`jomini_trigger_description.cpp` sur
`common/decisions/zz_sepoy_functional_test_a3.txt`. Elles disent que des
valeurs de scope dans un `any` devraient etre masquees par un
`custom_tooltip`. Repartition : lignes 23 (52), 35 (104), 48 (312), 94 (38),
106 (76) et 119 (228). `debug.log` en reprend 907 occurrences. Ce sont des
avis de rendu de description des decisions, pas des erreurs de script,
transfert ou boucle ; l'interface et les cinq executions sont restees
fonctionnelles. Cette dette de presentation du harnais est documentee sans
etre corrigee dans cette phase runtime.

## 30. Diagnostics globaux hors perimetre

Les diagnostics frais non attribuables a A-3 sont :

| Diagnostic | Nombre dans `error.log` | Source principale |
|---|---:|---|
| `Unknown strategic region key geographic_region_bombay_old` | 506 | Dette regionale globale |
| `Unknown strategic region key geographic_region_bengal_old` | 506 | Dette regionale globale |
| `Script system error!` | 216 | 212 erreurs `sr` et 4 flags pays invalides |
| `Invalid right side during comparison 'sr'` | 212 | `common/ai_strategies/00_default_strategy.txt`, surtout ligne 5078 (196) |
| `has_diplomatic_pact ... Invalid Country!` | 4 | `common/flag_definitions/00_flag_definitions.txt:1464` |
| GUI `FindChild('interest_group_top')` | 39 | GUI globale |
| `Unknown tooltip type` | 1 | Warning global non bloquant |

La session fraiche ne contient aucune erreur de loi a
`00_landowners.txt:459`, aucun `has_role` et aucune reference a
`01_natural_borders_of_france.txt`. Ces dettes restent hors perimetre.

## 31. Integrite finale de la sauvegarde

La taille, le LastWriteTime et le SHA-256 finaux de la baseline sont
strictement identiques aux valeurs de la section 14. Elle n'a donc pas ete
ecrasee pendant les cinq runs.

## 32. Integrite finale du fork et de la copie

- 25/25 hashes enregistres dans le manifeste C1H sont conformes.
- Les 16 fichiers de harnais sont inchanges.
- `common/journal_entries/04_sepoy_mutiny.txt` :
  `DAEFCB59CCF6B303D2E39C948D8038006C1346AFE40A2B812D45EE4D947E361C`.
- `events/india_events/sepoy_mutiny_events.txt` :
  `557936500AC585F7F69B9F5B063BDDA377AFF4A5AFAA06C70650C55D4AD612F7`.
- Les deux hashes Sepoy sont identiques dans le fork et la copie.
- `descriptor.mod` de la copie et son marqueur de securite sont conformes au
  manifeste C1H.
- La copie contient toujours 960 fichiers, sans `.git` ni `remote_file_id`.

## 33. Resume du CSV

Le CSV joint contient la baseline, les cinq executions, les comptes MARATH,
NAG et invalides, la fraicheur des logs, l'integrite des fichiers et
l'integrite finale de la sauvegarde. Il est encode en UTF-8 avec BOM.

## 34. Verdict

**`PASS_A3_RUNTIME`**

Les cinq runs sont termines ; chaque owner final est autorise ; aucun owner
nul, troisieme receveur, crash, blocage ou erreur runtime A-3/Sepoy n'a ete
observe ; la baseline et les fichiers de mod sont inchanges.

## 35. Ce que le test valide

Le test valide que, dans la topologie A-3 a deux receveurs, l'option 2.a peut
choisir un receveur admissible, transferer Bundelkhand a un owner unique,
terminer la boucle, annexer BIC et rendre le controle a GBR sans erreur
runtime. Il valide cinq fois le resultat MARATH.

## 36. Ce que le test ne valide pas

Il ne prouve pas une probabilite 50/50, ne garantit pas que NAG sera observe
sur un petit echantillon, ne teste pas les options 2.b/2.c/2.e et ne couvre
aucun scenario B/C/E/F. Il ne corrige pas non plus les dettes globales de
regions strategiques ou les avis de description du harnais.

## 37. Recommandation pour la suite B-1

Conserver A-3 comme preuve de terminaison et de domaine valide, puis preparer
B-1 dans une phase statique separee, sur copie jetable, avec son propre
manifeste et sa propre sauvegarde. Ne pas reutiliser les sauvegardes A-1, A-2
ou A-3 et ne pas modifier le fork gameplay pour cette preparation.

## 38. Liste exacte des fichiers crees

1. `docs/reports/hotfix/HOTFIX_5C2E4C1I_SEPOY_A3_RUNTIME_TEST.md`
2. `docs/reports/hotfix/HOTFIX_5C2E4C1I_A3_RUNTIME_RESULTS.csv`

## 39. Confirmation qu'aucun gameplay ou harnais n'a change

Aucun fichier `common/`, `events/`, `localization/`, `map_data/`, Sepoy ou
harnais n'a ete modifie. Les seules ecritures dans le fork sont les deux
livrables documentaires C1I.

## 40. Confirmation que docs/research/technology/ est intact

Les sept fichiers conservent les memes tailles, horodatages et SHA-256 que les
controles anterieurs. Le dossier reste non suivi et n'a subi aucune action.

## 41. Confirmation que le stash MARATH est intact

`stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` est
toujours present. Il n'a ete ni applique, ni modifie, ni supprime.
