# HOTFIX-5C2E4C1C1 - Correction BOM et retest du harnais Sepoy

## 1. Resume

Les deux scripts jetables du harnais ont recu uniquement le prefixe UTF-8 BOM
`EF BB BF`. Une comparaison octet par octet prouve que tous les anciens octets
restent identiques apres ce prefixe. Les textes, lignes, indentations et fins
de ligne n'ont pas change.

Les sessions BIC et GBR ont ensuite ete rejouees avec la copie comme seul mod
actif. La decision et l'event fonctionnent pour BIC, la decision est absente
pour GBR, aucun effet persistant n'est observe et les logs ne signalent plus
les deux fichiers du harnais.

**Verdict : `PASS_HARNESS_RUNTIME_CLEAN`.**

## 2. Etat Git initial

- Racine : `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork`.
- Branche : `hotfix-dlc-audit`.
- HEAD initial : `246441e Test disposable Sepoy root harness`.
- Le rapport C1C etait donc commit avant C1C1.
- Aucun fichier suivi n'etait modifie.
- Stash present et non applique :
  `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla`.

## 3. Exception docs/research/technology

Le dossier non suivi `docs/research/technology/` contenait les sept fichiers
preexistants autorises. Il n'a ete ni modifie ni copie pendant cette phase.

## 4. Etat de la copie avant correction

Les six fichiers jetables requis, le descripteur et le marqueur existaient.
La copie contenait exactement 948 fichiers et correspondait a la fin de C1C.

| Script | Taille attendue | Taille relevee | SHA-256 attendu et releve |
|---|---:|---:|---|
| `common/decisions/zz_sepoy_functional_test.txt` | 298 | 298 | `02721DE11FE7B45CAF95DE11CF5199FA77D2A9C3799AD264DD69284F47EB3C8B` |
| `events/zz_sepoy_functional_test_events.txt` | 463 | 463 | `32D3CF4164CADC3ECF1DBCE0C5A7C2809DD3A1A5407C89378FE7939D729EA4E0` |

Le jeu et le launcher ont ete fermes avant toute ecriture. Quatre processus
`Paradox Launcher` detectes initialement ont ete fermes manuellement par
l'utilisateur, puis leur absence a ete reverifiee.

## 5. Preuve de l'absence initiale de BOM

Les trois premiers octets des deux scripts etaient `23 20 44`, soit le debut
ASCII du commentaire `# D`. `HasUtf8Bom` valait `False` pour les deux fichiers.

- Decision : 22 lignes, 21 fins de ligne LF, zero CRLF.
- Event : 27 lignes, 26 fins de ligne LF, zero CRLF.

## 6. Hashes avant correction

| Controle | Taille | SHA-256 |
|---|---:|---|
| Localisation EN copie | 556 | `93BF3B0FEF1FD871ABE77ED8CA4EBDCD7258ED7F085F9928B6E103D4F0BFA6EF` |
| Localisation FR copie | 627 | `59EAC034463C9976944AF8E170912ED4C3C20329E08D749EC0FD901096B67C87` |
| JE Sepoy copie | 16 040 | `DAEFCB59CCF6B303D2E39C948D8038006C1346AFE40A2B812D45EE4D947E361C` |
| Events Sepoy copie | 63 210 | `557936500AC585F7F69B9F5B063BDDA377AFF4A5AFAA06C70650C55D4AD612F7` |
| `descriptor.mod` copie | 104 | `1921791546626A938E18EEADC765538120325AFA87E0EA309C2C3C6502175B40` |
| Marqueur jetable | 406 | `280066169F9D9D7020FEF4342264D18C5B1613CA40B74D519ADD4E7F3492838A` |
| Descripteur launcher | 206 | `FBFDFB891E3E355C05ED996B4A6866475E259081E8196187A2424C9DECCC3733` |
| JE Sepoy fork | 16 040 | `DAEFCB59CCF6B303D2E39C948D8038006C1346AFE40A2B812D45EE4D947E361C` |
| Events Sepoy fork | 63 210 | `557936500AC585F7F69B9F5B063BDDA377AFF4A5AFAA06C70650C55D4AD612F7` |
| `descriptor.mod` fork | 98 | `93C2AD4C459B1E897A37AA6964EEEFB1C7522D5175F12B43B0BB35020BA82021` |

## 7. Methode exacte d'ajout du BOM

Pour chaque script :

1. lecture du tableau d'octets existant avec `ReadAllBytes` ;
2. verification de la taille, du SHA-256 et de l'absence de BOM ;
3. allocation d'un tableau de taille ancienne + 3 ;
4. ecriture de `EF BB BF` aux offsets 0, 1 et 2 ;
5. copie du tableau initial sans transformation a partir de l'offset 3 ;
6. ecriture avec `WriteAllBytes` ;
7. relecture et comparaison de chaque octet.

Aucun editeur, decodeur-reencodeur ou normalisateur de fins de ligne n'a ete
utilise pour la modification.

## 8. Preuve que les payloads sont identiques

Pour chacun des 298 octets de la decision, l'octet initial `i` est identique a
l'octet final `i+3`. Le meme controle reussit pour les 463 octets de l'event.

Le texte decode apres retrait du BOM est strictement identique. Les nombres de
lignes, LF et CRLF sont aussi inchanges. `payload_identical_after_bom` et
`TextIdentical` valent `True` pour les deux scripts.

## 9. Tailles et hashes apres correction

| Script | Taille avant | Taille apres | SHA-256 apres |
|---|---:|---:|---|
| Decision | 298 | 301 | `E8CC4B78AB7447A5CED31C525B99814542C82AEEE5C47C530446870772C120FF` |
| Event | 463 | 466 | `E69B386716B7E33BC311CF3450C89B0605A0E92AA6C74B689591171810D156EE` |

Les deux fichiers commencent desormais par `EF BB BF`.

## 10. Validation statique du harnais

- BOM present sur les deux scripts et les deux YAML.
- Zero terme interdit.
- Un seul `trigger_event`, vers `zz_sepoy_test.1`.
- Trois gardes `c:BIC ?= this` toujours presentes.
- Zero appel a `sepoy_mutiny_events.2`.
- Fichiers Sepoy inchanges.
- Aucun nouveau fichier dans la copie.
- Copie : 948 fichiers et 17 327 126 octets.

## 11. Resume du manifest

`HOTFIX_5C2E4C1C1_HARNESS_BOM_MANIFEST.csv` est encode en UTF-8 avec BOM et
contient 13 lignes :

- 2 `BOM_ADDED_PAYLOAD_IDENTICAL` ;
- 9 `UNCHANGED_CONTROL` ;
- 2 `CREATED_REPORT`.

Il couvre les scripts, YAML, sources Sepoy copie/fork, descripteurs, marqueur
et les deux livrables C1C1. Le hash propre du manifest reste vide car il serait
auto-referentiel.

## 12. Verification du playset

L'utilisateur a fourni une capture du launcher montrant `playset1`, `Mods : 1`
et uniquement `1776_Age_of_Revolutions_sepoy_test` active. Le fork principal
et les autres copies 1776 n'etaient pas actifs.

Les descripteurs n'ont aucun `remote_file_id` et aucun lien Workshop n'a ete
ajoute.

## 13. Horodatage initial des logs

Avant le retest BIC :

| Log | Derniere ecriture | Taille | SHA-256 |
|---|---|---:|---|
| `error.log` | 2026-07-15 01:09:30.730 +00:00 | 362 258 | `9BE863B7F4909FEC776F60DA40184211AA23F60DE2532B639977F5E6935A7A94` |
| `game.log` | 2026-07-15 01:09:30.730 +00:00 | 272 163 | `86DC75568C67EBFC33C0D5F0F4B6D4EC61AE5EE2C8C17894B652770C6D891054` |
| `debug.log` | 2026-07-15 01:09:39.709 +00:00 | 251 637 | `3F2636AF4F4C2B7EAC25F6B849F13DDC28B5D3EF8AE044335BA7EFC50D75B9CC` |

Les logs n'ont pas ete supprimes automatiquement.

## 14. Retest BIC

Une nouvelle partie BIC a ete lancee avec le playset jetable seul et mise en
pause au 1er janvier 1776. La decision a ete prise, l'event ferme, les deux
sujets controles, puis le jeu quitte proprement sans temps avance.

## 15. Visibilite de la decision

`Verifier le scope de test BIC` restait visible et utilisable pour BIC. Les
textes francais etaient identiques au premier test. Aucune cle brute du
namespace du harnais n'etait visible.

## 16. Ouverture de l'event

Le clic a ouvert `Scope BIC verifie`. La description confirmait la Compagnie
des Indes orientales comme scope pays racine et l'event possedait une seule
option de fermeture.

## 17. Absence d'effet persistant

- Date : 1 janvier 1776 avant et apres.
- Sujets BIC : Cooch Behar et Jeypore avant et apres.
- Aucun nouvel event ou JE Sepoy.
- Aucun owner, controller, state, sujet, capitale ou pop modifie.
- Aucun appel console et aucun temps de jeu avance.

## 18. Analyse des logs BIC

| Log | Derniere ecriture apres BIC | Taille | SHA-256 |
|---|---|---:|---|
| `error.log` | 2026-07-15 02:18:22.199 +00:00 | 453 065 | `9CB6C65CE772A9BDA259316651EC5D4D849D37C04AA05094866A39E1BFAB9490` |
| `game.log` | 2026-07-15 02:18:22.199 +00:00 | 71 410 | `0C169E088C1528C5709583A94FA0BB5CF065D37754AEE3EB31BACEBA990746E6` |
| `debug.log` | 2026-07-15 02:18:28.173 +00:00 | 321 834 | `B76E166EC27514DF9FA502F1FEA3F1F80CA3147B3639157C1F39629804AC39ED` |

Resultats :

- zero avertissement BOM visant le harnais ;
- zero diagnostic parsing/scope/validation attribuable au harnais ;
- zero appel Sepoy interdit ;
- zero cle brute du harnais.

## 19. Retest GBR

Une nouvelle partie GBR a ete lancee avec le meme playset, mise en pause au
1er janvier 1776, puis la liste des decisions inspectee. Le jeu a ete quitte
proprement sans console et sans temps avance.

## 20. Absence de la decision GBR

La capture montre les decisions normales de GBR mais aucune occurrence de
`Verifier le scope de test BIC`. La garde de root reste donc fonctionnelle.

## 21. Analyse des logs GBR

| Log | Derniere ecriture apres GBR | Taille | SHA-256 |
|---|---|---:|---|
| `error.log` | 2026-07-15 02:35:09.342 +00:00 | 515 068 | `46A0D9A75EBC00BAF6F35EF91BD728CAF61F69397825A8B4AEF319BEC4EA0626` |
| `game.log` | 2026-07-15 02:35:09.342 +00:00 | 365 958 | `95C724CBA74A4FC29501666FB677E90157E344628B585D1D38F54FB87FF3D934` |
| `debug.log` | 2026-07-15 02:35:30.034 +00:00 | 391 639 | `305D19A6A96618B06B83D80B8049D87D807961692E47E90538F33583A6F83055` |

Resultats :

- zero avertissement BOM visant les deux scripts ;
- zero erreur ou execution du namespace du harnais ;
- zero invocation d'un event Sepoy ;
- zero pattern runtime territorial interdit.

## 22. Diagnostics globaux hors perimetre

Les deux sessions contiennent encore 16 avertissements BOM visant d'autres
fichiers, notamment Sakoku/Tenpo, plusieurs historiques Japon/IR1, Australasie,
`00_states.txt`, les government types et country ranks. Ils ne visent plus les
deux scripts du harnais.

Dans la session GBR, `error.log` contient 2 687 `Script system error` : 2 684
proviennent de `common/ai_strategies/00_default_strategy.txt:5078`, deux de
`02_acre_dispute.txt:8` et une de `03_afghanistan.txt:1834`. `debug.log`
contient 427 `Unexpected token`, 677 `PostValidate` et un doublon dans
`common/character_templates/default_template.txt:4`.

Ces dettes globales sont documentees sans correction dans C1C1.

## 23. Hashes apres runtime

La verification des valeurs `sha256_after` et `size_after` du manifest donne
zero erreur apres les deux sessions. La copie contient toujours 948 fichiers
et 17 327 126 octets.

| Controle | SHA-256 final | Statut |
|---|---|---|
| Decision BOM | `E8CC4B78AB7447A5CED31C525B99814542C82AEEE5C47C530446870772C120FF` | identique post-correction |
| Event BOM | `E69B386716B7E33BC311CF3450C89B0605A0E92AA6C74B689591171810D156EE` | identique post-correction |
| Localisation EN | `93BF3B0FEF1FD871ABE77ED8CA4EBDCD7258ED7F085F9928B6E103D4F0BFA6EF` | inchangee |
| Localisation FR | `59EAC034463C9976944AF8E170912ED4C3C20329E08D749EC0FD901096B67C87` | inchangee |
| JE Sepoy copie/fork | `DAEFCB59CCF6B303D2E39C948D8038006C1346AFE40A2B812D45EE4D947E361C` | inchangee |
| Events Sepoy copie/fork | `557936500AC585F7F69B9F5B063BDDA377AFF4A5AFAA06C70650C55D4AD612F7` | inchanges |
| Descripteur copie | `1921791546626A938E18EEADC765538120325AFA87E0EA309C2C3C6502175B40` | inchange |
| Marqueur | `280066169F9D9D7020FEF4342264D18C5B1613CA40B74D519ADD4E7F3492838A` | inchange |
| Descripteur launcher | `FBFDFB891E3E355C05ED996B4A6866475E259081E8196187A2424C9DECCC3733` | inchange |
| Descripteur fork | `93C2AD4C459B1E897A37AA6964EEEFB1C7522D5175F12B43B0BB35020BA82021` | inchange |

Les sept fichiers de recherche conservent aussi leurs tailles et hashes
initiaux.

## 24. Verdict

**`PASS_HARNESS_RUNTIME_CLEAN`**

Les BOM sont les seules modifications des scripts, les payloads restent
identiques, les deux tests fonctionnels reussissent et aucun diagnostic ne
vise desormais le harnais.

## 25. Ce que la phase valide

- Encodage UTF-8 BOM propre des deux scripts jetables.
- Identite octet par octet des payloads.
- Chargement sans diagnostic du harnais.
- Decision visible et fonctionnelle pour BIC.
- Event execute sur le root BIC.
- Aucune consequence persistante.
- Decision absente pour GBR.
- Aucun event Sepoy appele.
- Integrite du fork et de la copie apres runtime.

## 26. Ce que la phase ne valide pas

- `sepoy_mutiny_events.2` et ses options.
- Une preparation territoriale.
- Les transferts, independances, capitales ou radicaux.
- Les dettes globales d'encodage, scripts, JE ou localisation.
- Un test avec le temps de jeu en mouvement.

## 27. Etape territoriale suivante

Le harnais de root est maintenant propre et peut servir de base a une phase
territoriale jetable distincte. La prochaine phase doit preparer un seul
scenario a la fois, commencer par le cas le moins destructif retenu dans C0,
et continuer a interdire toute modification du fork principal.

Aucun scenario territorial n'a ete cree dans C1C1.

## 28. Fichiers modifies dans la copie

Uniquement :

- `common/decisions/zz_sepoy_functional_test.txt` ;
- `events/zz_sepoy_functional_test_events.txt`.

La seule difference est le prefixe `EF BB BF`.

## 29. Fichiers crees dans le fork

Uniquement :

- `docs/reports/hotfix/HOTFIX_5C2E4C1C1_SEPOY_HARNESS_BOM_RETEST.md` ;
- `docs/reports/hotfix/HOTFIX_5C2E4C1C1_HARNESS_BOM_MANIFEST.csv`.

## 30. Confirmation du fork principal

Aucun fichier gameplay du fork n'a ete modifie. Les sources Sepoy et le
`descriptor.mod` conservent leurs hashes initiaux. Le fork et la copie n'ont
jamais ete actifs simultanement selon le playset confirme.

## 31. Confirmation docs/research/technology

Les sept fichiers conservent leurs hashes initiaux :

| Fichier | SHA-256 |
|---|---|
| `TECH_TREE_BUILDING_AND_PRODUCTION_CANDIDATES.csv` | `315CB857B94D547492E1F7C36E10A67EF53DBCBDA0FF63CBA4246DBA7B6FC6D5` |
| `TECH_TREE_INDUSTRIAL_CHAINS.md` | `981A0C119D02C5A5F795C41800B678DDBEC9AD91890CDE4588DF36A98D011799` |
| `TECH_TREE_INDUSTRIAL_HISTORY_DEEP_RESEARCH.md` | `0FE06A1843F5B67413E222ECFDABBF4E6957EAA2E97D466A018C59FA27DA4596` |
| `TECH_TREE_INDUSTRIAL_INNOVATIONS_DATABASE.csv` | `01A37C0BD8BE839EC59E11AA4742CB4D96824EEAFCEA94979839391D8798094D` |
| `TECH_TREE_RESEARCH_BIBLIOGRAPHY.md` | `C4EF474D8C1502DBC1D36A9D52473EE4B5E41C3D14A2081F1A526B9383FF1AF5` |
| `TECH_TREE_RESOURCE_CANDIDATES.csv` | `6E7A48765FB9C20A4F8992D1CCD32BB75340A7BD6FC00B365E503F930BFD8F9A` |
| `TECH_TREE_VICTORIA3_GAP_ANALYSIS.md` | `150256D3C56333CAF8C37A7631074110060678FC115DB24FC48F702DFD6840FA` |

## 32. Confirmation du stash MARATH

Le stash `WIP NAVY-3C-3 Maratha Konkan Flotilla` reste present, intact et non
applique. Aucun `git stash pop` ni commit automatique n'a ete execute.
