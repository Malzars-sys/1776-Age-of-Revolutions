# HOTFIX-5C2E4C1C - Test runtime du harnais Sepoy

## 1. Resume

Deux sessions ont ete executees manuellement avec la copie jetable comme seul
mod actif : une session BIC, puis une session GBR. La decision est visible et
fonctionnelle pour BIC, ouvre l'event de confirmation sur le root BIC et reste
absente pour GBR. Aucun temps n'a avance et aucun effet persistant n'a ete
observe.

Le controle strict des logs detecte toutefois deux avertissements du lexer qui
visent directement les deux fichiers script du harnais : ils ne sont pas en
UTF-8 avec BOM. Le moteur les charge quand meme, mais le protocole C1C impose
un echec lorsqu'un diagnostic pointe vers l'un des quatre fichiers.

**Verdict strict : `FAIL_HARNESS_PARSE`.**

## 2. Etat Git initial

- Racine : `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork`.
- Branche : `hotfix-dlc-audit`.
- HEAD initial : `c91ad14 Add disposable Sepoy root harness`.
- Le commit C1B contient uniquement son rapport et son manifest.
- Aucun fichier suivi n'etait modifie.
- Stash present et non applique :
  `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla`.

## 3. Exception docs/research/technology

Le seul contenu non suivi initial etait `docs/research/technology/`, avec sept
fichiers preexistants. Il n'a ete ni modifie, ni copie, ni utilise comme
destination pendant C1C.

## 4. Hashes du harnais avant lancement

Les 11 lignes du manifest C1B ont ete controlees avant lancement : zero erreur
de taille ou de SHA-256.

| Fichier dans la copie | Taille | SHA-256 avant runtime |
|---|---:|---|
| `common/decisions/zz_sepoy_functional_test.txt` | 298 | `02721DE11FE7B45CAF95DE11CF5199FA77D2A9C3799AD264DD69284F47EB3C8B` |
| `events/zz_sepoy_functional_test_events.txt` | 463 | `32D3CF4164CADC3ECF1DBCE0C5A7C2809DD3A1A5407C89378FE7939D729EA4E0` |
| `localization/english/zz_sepoy_functional_test_l_english.yml` | 556 | `93BF3B0FEF1FD871ABE77ED8CA4EBDCD7258ED7F085F9928B6E103D4F0BFA6EF` |
| `localization/french/zz_sepoy_functional_test_l_french.yml` | 627 | `59EAC034463C9976944AF8E170912ED4C3C20329E08D749EC0FD901096B67C87` |

Les deux fichiers Sepoy, le descripteur interne, le descripteur launcher et le
marqueur correspondaient aussi au manifest. La copie contenait exactement 948
fichiers, sans `.git`, `remote_file_id` ou cinquieme fichier de harnais.

## 5. Verification du playset

L'utilisateur a cree et selectionne un playset dedie contenant uniquement
`1776_Age_of_Revolutions_sepoy_test` (16,52 MB). Il a confirme que les deux
entrees normales de 1776 et tous les autres mods etaient exclus.

Le descripteur externe et le descripteur interne ne contiennent aucun
`remote_file_id`. Aucune publication Workshop n'a ete effectuee pendant le
test. La confirmation du contenu actif du launcher reste une observation
manuelle de l'utilisateur, conformement au protocole.

## 6. Horodatage initial des logs

Victoria 3 ne tournait pas lors du releve initial.

| Log | Derniere ecriture | Taille | SHA-256 initial |
|---|---|---:|---|
| `error.log` | 2026-07-14 22:05:17.020 +00:00 | 238 648 | `0E702415F997EAB2A7EFA3626C044E57EA591BD63F8AFE4C190C4B5566247046` |
| `game.log` | 2026-07-14 22:05:17.020 +00:00 | 208 228 | `9BC2C48611A995D246D94AC7BC1B2DC9735DD53ED527C6283275739B1C9DDE5E` |
| `debug.log` | 2026-07-14 22:05:23.501 +00:00 | 110 737 | `8F9DA529016A27C6D920B27988E5ADCB7F95390FAA2BE0DAA3F2607DD12863D6` |

Les anciens logs n'ont pas ete supprimes automatiquement.

## 7. Deroulement de la session BIC

1. Le jeu a ete lance avec le playset jetable seul.
2. Une nouvelle partie BIC a ete ouverte au 1er janvier 1776.
3. Le jeu a ete mis en pause sans faire avancer le temps.
4. La liste des decisions a ete ouverte.
5. La decision de test a ete prise.
6. L'event de confirmation a ete ferme avec son unique option.
7. L'utilisateur a controle les sujets et l'absence de nouvel event ou JE
   Sepoy, puis a quitte proprement.
8. Le processus `victoria3` etait arrete avant lecture des logs.

## 8. Visibilite de la decision BIC

La decision `Verifier le scope de test BIC` etait visible et cliquable. Les
deux conditions affichees etaient cochees : pays controle par un joueur et
pays courant egal a la Compagnie des Indes orientales.

Le tooltip repete plusieurs fois le nom de la Compagnie dans le rendu des
triggers. C'est un defaut d'affichage secondaire du trigger automatique, pas
une cle brute et pas une erreur de scope fonctionnelle.

## 9. Localisations observees

Les textes propres au harnais etaient correctement affiches en francais :

- titre de decision : `Verifier le scope de test BIC` ;
- description complete du harnais jetable ;
- event : `Scope BIC verifie` ;
- description confirmant le scope pays racine BIC ;
- option unique : `Fermer l'evenement de test`.

Aucune cle `zz_sepoy_test*` n'etait visible. En revanche,
`objective_battle_for_india_idle_header` et
`objective_battle_for_india_idle_hint` apparaissaient dans l'objectif
`Bataille pour l'Inde`. Ces deux cles sont une dette de localisation existante
hors harnais.

## 10. Ouverture de l'evenement

Le clic a ouvert immediatement le country event de confirmation. L'event
utilisait l'image indienne attendue, possedait un seul bouton et n'affichait ni
option supplementaire ni branche Sepoy.

## 11. Confirmation du root BIC

Le titre et la description affichaient explicitement que la Compagnie des
Indes orientales etait le scope pays racine. Le popup etait situe en Bengale
de l'Ouest et les deux gardes BIC de la decision etaient satisfaites.

Cette observation valide le chemin decision -> `zz_sepoy_test.1` sur BIC. Elle
ne valide pas encore l'appel destructif de `sepoy_mutiny_events.2`, qui est
reste interdit et absent.

## 12. Verification d'absence d'effet persistant

| Controle | Avant | Apres | Resultat |
|---|---|---|---|
| Pays joue | BIC | BIC | inchange |
| Date | 1 janvier 1776 | 1 janvier 1776 | aucun temps avance |
| JE visible | `Renforcer la domination coloniale` | aucune nouvelle JE Sepoy | inchange pour le harnais |
| Region state de West Bengal | BIC, avec une province COO dans la state region | aucun changement observe | inchange |
| Parties de Bombay | POR, MARATH, SAT et KHP dans le setup | aucun changement observe | inchange |
| Sujets directs BIC | Cooch Behar et Jeypore | Cooch Behar et Jeypore | 2 -> 2 |
| Decision | visible avant le clic | event ferme normalement | conforme |

Aucun owner, controller, sujet, state, capitale, population, journal entry ou
event Sepoy n'a change. Le controle territorial est volontairement limite aux
elements demandes et n'est pas un audit mondial.

## 13. Analyse des logs BIC

| Log | Derniere ecriture apres BIC | Taille | SHA-256 |
|---|---|---:|---|
| `error.log` | 2026-07-15 00:36:56.284 +00:00 | 300 109 | `547A257A4A266339579D28D7975D999272375C79AF3B5D108FFB0CCCCDFF6E27` |
| `game.log` | 2026-07-15 00:36:56.283 +00:00 | 501 944 | `1745BAEA92FF099E23BF46D2A7995E9937D28946697A0C50172D517199E23004` |
| `debug.log` | 2026-07-15 00:37:02.441 +00:00 | 181 171 | `A8C7E9AC4456E354A252E3C0C5BDE6A3BEE2E0C44FC58B3749074220ED199DE5` |

La recherche C1C a retourne zero occurrence pour le namespace, les deux
chemins du harnais et les textes EN/FR du popup. Elle a aussi retourne zero
occurrence des patterns runtime Sepoy interdits.

Les compteurs generaux etaient eleves mais hors harnais : 1 525 `Script
system error` dans `error.log`, 2 616 dans `game.log`, 294 `Unexpected token`,
677 `PostValidate` et 10 mentions `Localization` dans `debug.log`.

## 14. Deroulement de la session non-BIC

Le meme playset jetable a ete relance sans modification. Une nouvelle partie
GBR a ete ouverte, mise en pause au 1er janvier 1776, puis la liste des
decisions a ete inspectee. Aucune console n'a ete utilisee et aucun temps n'a
avance. Le jeu a ensuite ete quitte proprement.

## 15. Absence de la decision non-BIC

La capture GBR montre les decisions ordinaires, notamment `Proclamer le Raj
britannique`, mais aucune occurrence de `Verifier le scope de test BIC`.

La garde racine fonctionne donc pour la visibilite : **PASS**. Aucun event de
confirmation n'a ete ouvert ou force pour GBR.

## 16. Analyse des logs non-BIC

| Log | Derniere ecriture apres GBR | Taille | SHA-256 |
|---|---|---:|---|
| `error.log` | 2026-07-15 01:09:30.730 +00:00 | 362 258 | `9BE863B7F4909FEC776F60DA40184211AA23F60DE2532B639977F5E6935A7A94` |
| `game.log` | 2026-07-15 01:09:30.730 +00:00 | 272 163 | `86DC75568C67EBFC33C0D5F0F4B6D4EC61AE5EE2C8C17894B652770C6D891054` |
| `debug.log` | 2026-07-15 01:09:39.709 +00:00 | 251 637 | `3F2636AF4F4C2B7EAC25F6B849F13DDC28B5D3EF8AE044335BA7EFC50D75B9CC` |

Zero pattern runtime Sepoy interdit a ete trouve et aucune execution de
`zz_sepoy_test.1` n'est indiquee. Deux diagnostics de chargement visent
cependant directement les scripts du harnais :

```text
debug.log:72  File 'events/zz_sepoy_functional_test_events.txt' should be in utf8-bom encoding (will try to use it anyways)
debug.log:302 File 'common/decisions/zz_sepoy_functional_test.txt' should be in utf8-bom encoding (will try to use it anyways)
```

Le moteur a reussi a charger et utiliser ces fichiers, mais ces avertissements
violent la condition stricte C1C. Les YAML EN/FR, deja en UTF-8 BOM, ne sont
pas cites.

## 17. Diagnostics hors perimetre

La seconde session contient 1 861 `Script system error` dans `error.log`, dont
1 858 proviennent de `common/ai_strategies/00_default_strategy.txt:5078`
(`Invalid right side during comparison 'sr'`). Deux viennent de
`02_acre_dispute.txt:8` et une de `03_afghanistan.txt:1834`.

`debug.log` contient aussi 425 `Unexpected token`, 677 `PostValidate`, 10
mentions `Localization` et un doublon dans
`common/character_templates/default_template.txt:4`. De nombreux anciens
`should_be_pinned_by_default` et des lois non permises restent des dettes
globales du mod. Aucun de ces diagnostics n'est attribue au comportement du
harnais, hormis les deux avertissements BOM isoles ci-dessus.

## 18. Hashes apres runtime

Une nouvelle validation du manifest C1B donne **zero erreur de taille ou de
SHA-256**. La copie contient toujours 948 fichiers et 17 327 120 octets.

| Controle | SHA-256 apres les deux sessions | Statut |
|---|---|---|
| Decision jetable | `02721DE11FE7B45CAF95DE11CF5199FA77D2A9C3799AD264DD69284F47EB3C8B` | identique |
| Event jetable | `32D3CF4164CADC3ECF1DBCE0C5A7C2809DD3A1A5407C89378FE7939D729EA4E0` | identique |
| Localisation EN | `93BF3B0FEF1FD871ABE77ED8CA4EBDCD7258ED7F085F9928B6E103D4F0BFA6EF` | identique |
| Localisation FR | `59EAC034463C9976944AF8E170912ED4C3C20329E08D749EC0FD901096B67C87` | identique |
| JE Sepoy copie/fork | `DAEFCB59CCF6B303D2E39C948D8038006C1346AFE40A2B812D45EE4D947E361C` | identique |
| Events Sepoy copie/fork | `557936500AC585F7F69B9F5B063BDDA377AFF4A5AFAA06C70650C55D4AD612F7` | identique |
| `descriptor.mod` copie | `1921791546626A938E18EEADC765538120325AFA87E0EA309C2C3C6502175B40` | identique |
| Marqueur jetable | `280066169F9D9D7020FEF4342264D18C5B1613CA40B74D519ADD4E7F3492838A` | identique |
| `descriptor.mod` fork | `93C2AD4C459B1E897A37AA6964EEEFB1C7522D5175F12B43B0BB35020BA82021` | identique |

Les sept fichiers technologiques conservent egalement leurs tailles et hashes
initiaux. Le jeu et le launcher n'ont ecrit dans aucun fichier controle du
fork ou de la copie.

## 19. Verdict

**`FAIL_HARNESS_PARSE`**

La logique runtime reussit, la garde root reussit et aucun effet persistant
n'est observe. Le verdict reste un echec strict parce que `debug.log` signale
deux fichiers du harnais avec un encodage script non conforme. Le libelle
`FAIL_HARNESS_PARSE` est le verdict autorise le plus proche pour ce diagnostic
du lexer ; il ne signifie pas que le moteur a refuse de charger les scripts.

## 20. Ce que le test valide

- La copie seule peut lancer une partie BIC et une partie GBR.
- La decision est visible et utilisable sur le root BIC.
- `zz_sepoy_test.1` s'ouvre sur BIC avec les textes francais attendus.
- L'event possede une option unique sans effet observable.
- La decision est absente pour GBR.
- Aucun appel a la chaine Sepoy et aucun effet persistant n'ont lieu.
- Les fichiers controles restent bit a bit identiques apres runtime.

## 21. Ce que le test ne valide pas

- L'appel de `sepoy_mutiny_events.2`.
- Les options territoriales 2.a, 2.b, 2.c ou 2.e.
- Les transferts, independances, choix de capitales ou radicaux.
- Un scenario avec temps de jeu avance.
- La correction des dettes generales de logs ou des cles de l'objectif Inde.
- La conformite finale du harnais tant que les deux scripts n'ont pas de BOM.

## 22. Etape territoriale suivante

La preparation territoriale reste bloquee. Une phase intermediaire distincte
doit uniquement convertir les deux scripts jetables en UTF-8 avec BOM, mettre
a jour leur manifest puis rejouer les sessions BIC et GBR. Aucune logique ou
localisation ne doit changer pendant cette correction.

Le premier scenario territorial C1D/C2 ne doit commencer qu'apres un nouveau
verdict sans diagnostic visant le harnais.

## 23. Liste exacte des fichiers crees

Dans le fork, C1C cree uniquement :

- `docs/reports/hotfix/HOTFIX_5C2E4C1C_SEPOY_HARNESS_RUNTIME_TEST.md`

Aucun fichier n'a ete cree dans la copie jetable.

## 24. Confirmation gameplay

Aucun fichier gameplay n'a ete modifie dans le fork ou dans la copie. Aucun
event Sepoy n'a ete declenche et aucun scenario territorial n'a ete prepare.
`STATE_WEST_BENGAL` n'a pas ete modifie.

## 25. Confirmation d'activation exclusive

Selon la confirmation manuelle et les captures de l'utilisateur, le fork
principal n'a jamais ete active avec la copie. Les deux sessions ont utilise
le playset dont `1776_Age_of_Revolutions_sepoy_test` etait le seul mod.

## 26. Confirmation docs/research/technology

Les sept fichiers conservent exactement leurs hashes initiaux :

| Fichier | SHA-256 |
|---|---|
| `TECH_TREE_BUILDING_AND_PRODUCTION_CANDIDATES.csv` | `315CB857B94D547492E1F7C36E10A67EF53DBCBDA0FF63CBA4246DBA7B6FC6D5` |
| `TECH_TREE_INDUSTRIAL_CHAINS.md` | `981A0C119D02C5A5F795C41800B678DDBEC9AD91890CDE4588DF36A98D011799` |
| `TECH_TREE_INDUSTRIAL_HISTORY_DEEP_RESEARCH.md` | `0FE06A1843F5B67413E222ECFDABBF4E6957EAA2E97D466A018C59FA27DA4596` |
| `TECH_TREE_INDUSTRIAL_INNOVATIONS_DATABASE.csv` | `01A37C0BD8BE839EC59E11AA4742CB4D96824EEAFCEA94979839391D8798094D` |
| `TECH_TREE_RESEARCH_BIBLIOGRAPHY.md` | `C4EF474D8C1502DBC1D36A9D52473EE4B5E41C3D14A2081F1A526B9383FF1AF5` |
| `TECH_TREE_RESOURCE_CANDIDATES.csv` | `6E7A48765FB9C20A4F8992D1CCD32BB75340A7BD6FC00B365E503F930BFD8F9A` |
| `TECH_TREE_VICTORIA3_GAP_ANALYSIS.md` | `150256D3C56333CAF8C37A7631074110060678FC115DB24FC48F702DFD6840FA` |

## 27. Confirmation du stash MARATH

Le stash `WIP NAVY-3C-3 Maratha Konkan Flotilla` reste present, intact et non
applique. Aucun `git stash pop` n'a ete execute et aucun commit automatique n'a
ete cree.
