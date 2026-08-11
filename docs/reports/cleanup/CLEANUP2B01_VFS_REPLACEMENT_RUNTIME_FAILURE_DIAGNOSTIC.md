# CLEANUP-2B-0.1 — VFS Replacement Runtime Failure Diagnostic

Date de l'audit : 2026-08-11

Branche observée : `cleanup-post-release`

HEAD observé : `25e346efd7c9ea247ad5946e8a756c2467c21ea2`

Version cible : Victoria 3 1.13 / The Great Wave

Ce rapport est strictement diagnostique. Codex n'a lancé ni Victoria 3 ni le launcher, n'a modifié aucun fichier de gameplay ou d'historique, n'a créé aucun shadow file et n'a effectué aucune mutation Git.

## 1. Failed runtime evidence

Le test utilisateur de CLEANUP-2B-0 est un échec : les fichiers vanilla de `common/history/characters` continuent d'être chargés malgré la présence de `replace_path = "common/history/characters"` dans les deux descripteurs.

Les captures montrent encore des titulaires 1836 anachroniques au 1er janvier 1776, notamment Daoguang pour CHI, Mahmud II pour TUR, Maria II pour POR et Tokugawa Ienari pour JAP.

Le journal du lancement utilisateur le plus pertinent, `logs/debug.1.log`, établit la séquence suivante :

```text
1:  [14:50:42][pdx_steam.cpp:192]: Failed to initialize Steam so skipping getting of Steam-specific command line parameters
2:  [14:50:42][virtualfilesystem_physfs.cpp:460]: Mounted Data: C:/Games/Victoria 3 The Great Wave/clausewitz
3:  [14:50:42][virtualfilesystem_physfs.cpp:460]: Mounted Data: C:/Games/Victoria 3 The Great Wave/jomini
4:  [14:50:42][virtualfilesystem_physfs.cpp:460]: Mounted Data: C:/Games/Victoria 3 The Great Wave/platform_specific_game_data
5:  [14:50:42][virtualfilesystem_physfs.cpp:460]: Mounted Data: C:/Games/Victoria 3 The Great Wave/game
48: [14:50:44][pdx_mod_metadata.cpp:168]: Mod metadata read error. Error: Expected member (game_custom_data), near: {"name":"Age of revolution /Fork","id":"","version":"2.2.0","supported_game_version":"1.13.0","short_description":"","tags":[],"relationships":[]}
86: [14:50:44][virtualfilesystem_physfs.cpp:460]: Mounted Data: C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork
```

Le journal `logs/debug.log` montre ensuite simultanément des fichiers vanilla à basename long et des fichiers du fork à basename court :

```text
309-311: PostValidate ... common/history/characters/aus - austria.txt
312:     PostValidate ... common/history/characters/aus.txt
315-318: PostValidate ... common/history/characters/gbr - great britain.txt
319:     PostValidate ... common/history/characters/pru - prussia.txt
320-321: PostValidate ... common/history/characters/rus - russia.txt
```

La recherche large dans les logs n'a trouvé aucune lecture de `replace_path`, aucun diagnostic de parsing d'un `descriptor.mod` et aucune seconde couche de mod réintroduisant les fichiers. Elle trouve en revanche l'erreur explicite du lecteur `pdx_mod_metadata` à chaque lancement récent (`debug.1.log`, `debug.2.log`, `debug.4.log`, `debug.5.log`).

Classification de la cause parmi les hypothèses demandées : **F — la politique de remplacement est absente de l'objet metadata réellement chargé**. Le répertoire du mod est tout de même monté comme source de fichiers, mais sans la politique `replace_paths` attendue par le chargeur 1.13.

## 2. Active mod mount

Le fichier généré `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\content_load.json` contient exactement :

```json
{"enabledMods":[{"path":"C:\\Users\\simeo\\Documents\\Paradox Interactive\\Victoria 3\\mod\\1776_Age_of_Revolutions_fork"}],"disabledDLC":[],"enabledUGC":[]}
```

Les lignes 69 à 85 de `debug.1.log` montent les 17 DLC officiels installés. La ligne 86 monte ensuite une seule source utilisateur : le dépôt attendu. Aucun montage du Workshop `3617930953`, de `1776_Age_of_Revolutions_hotfix_source`, de `Age of revolution Fork [Steam Build]`, de Basileia ou d'un autre mod n'apparaît dans ce runtime.

```text
ACTIVE_1776_MOD_PATH = C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork
ACTIVE_1776_MOD_ID = "" (vide/non résolu dans le metadata courant)
DUPLICATE_1776_MOD_MOUNTS = 0
OTHER_ACTIVE_MODS = NONE
```

La condition « une seule copie attendue du fork » est donc démontrée. L'échec ne vient ni d'un doublon Workshop ni d'un hotfix chargé après le fork.

## 3. Descriptor parsing

Les deux descripteurs contiennent réellement la directive :

```text
descriptor.mod:3
replace_path = "common/history/characters"

C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_age_of_revolutions_fork.mod:4
replace_path="common/history/characters"
```

```text
INTERNAL_DESCRIPTOR_REPLACE_PATH_PRESENT = YES
EXTERNAL_DESCRIPTOR_REPLACE_PATH_PRESENT = YES
```

Réponse directe à la question utilisateur : **oui, le descripteur externe possède bien lui aussi le `replace_path`**.

Cette présence n'a néanmoins aucun effet dans le runtime observé. Le journal nomme le lecteur effectif `pdx_mod_metadata.cpp`, reproduit le JSON de `.metadata/metadata.json`, puis signale que `game_custom_data` manque. Il ne signale aucune ingestion des deux clés legacy `replace_path`.

Le descripteur externe reste un moyen pour le launcher/local setup d'associer un nom à un chemin physique. Il n'est pas une solution portable Workshop : les paquets Workshop 1.13 examinés n'ont pas de `descriptor.mod` à leur racine et transportent leur politique VFS dans `.metadata/metadata.json`.

Conclusion : le singulier legacy `replace_path` placé dans les descripteurs n'est **pas supporté comme mécanisme de remplacement dans ce contexte de chargement 1.13**. Son retrait devra être proposé après validation du mécanisme moderne, mais il n'est pas effectué pendant ce diagnostic.

## 4. Metadata architecture

Le metadata actuellement monté est :

```json
{"name":"Age of revolution /Fork","id":"","version":"2.2.0","supported_game_version":"1.13.0","short_description":"","tags":[],"relationships":[]}
```

Il ne contient pas `game_custom_data`. Le runtime ne se contente pas de l'ignorer silencieusement : il écrit précisément `Expected member (game_custom_data)`.

Les metadata 1.13 valides accessibles localement ont cette structure :

```json
"game_custom_data": {
  "multiplayer_synchronized": true,
  "replace_paths": [
    "common/history/characters"
  ]
}
```

La clé démontrée est donc :

- fichier : `.metadata/metadata.json` ;
- objet parent : `game_custom_data` ;
- clé : `replace_paths` au pluriel ;
- format : tableau JSON de chemins VFS relatifs, sans chemin utilisateur absolu.

Occurrence particulièrement probante : la source locale `1776_Age_of_Revolutions_hotfix_source` et sa copie Workshop installée `3617930953` ont toutes deux un metadata version `2.3.0` contenant `game_custom_data.replace_paths`, dont `common/history/characters`. Le dépôt actif utilise encore un metadata `2.2.0` incomplet.

La source hotfix contient également `common/history/character_templates`; ce chemin semble distinct du répertoire réel `common/character_templates` et ne doit pas être copié aveuglément. Cette anomalie n'affecte pas la preuve concernant le chemin exact `common/history/characters`.

## 5. Local 1.13 replace/override evidence

La recherche récursive, avec inclusion des répertoires cachés `.metadata`, donne les occurrences pertinentes suivantes :

| Fichier | Mod | Format | Clé | Valeur pertinente |
|---|---|---|---|---|
| `1776_Age_of_Revolutions_fork/descriptor.mod` | fork actif | script legacy | `replace_path` | `common/history/characters` — runtime inefficace |
| `1776_age_of_revolutions_fork.mod` | descripteur local externe | script legacy | `replace_path` | `common/history/characters` — runtime inefficace |
| `1776_Age_of_Revolutions_hotfix_source/.metadata/metadata.json` | source 1776 2.3.0 | JSON 1.13 | `game_custom_data.replace_paths` | inclut `common/history/characters` |
| `Basileia_Romaion_1736/.metadata/metadata.json` | Basileia local 1.13 | JSON 1.13 | `game_custom_data.replace_paths` | inclut `common/history/characters`, `states`, `pops`, `buildings`, `map_data/state_regions`, etc. |
| `Workshop/529340/2880120246/.metadata/metadata.json` | Basileia Workshop | JSON 1.13 | `game_custom_data.replace_paths` | identique à la copie locale |
| `Workshop/529340/3617930953/.metadata/metadata.json` | 1776 Workshop 2.3.0 | JSON 1.13 | `game_custom_data.replace_paths` | inclut `common/history/characters` |

Les formes `replacePath` et `replacePaths` n'ont donné aucune occurrence. L'installation de base `C:\Games\Victoria 3 The Great Wave` ne contient aucune occurrence texte de `replace_path`, `replace_paths`, `game_custom_data`, `substitute_path`, `override_path` ou `path_mapping` dans les fichiers inspectables.

L'absence de ces chaînes dans l'installation ne contredit pas le mécanisme : le parseur est dans le binaire Jomini/Paradox, tandis que la preuve d'interface est fournie par l'erreur runtime et par les packages 1.13.

## 6. Working total-conversion comparisons

### Basileia Romaion 1736

La copie locale et le paquet Workshop `2880120246` sont identiques sur les éléments décisifs :

- `supported_game_version = 1.13.*` ;
- `game_id = victoria3` ;
- `game_custom_data.multiplayer_synchronized = true` ;
- `game_custom_data.replace_paths` contient `common/history/characters` et de nombreux autres répertoires de total conversion ;
- aucun `descriptor.mod` à la racine du paquet local ou Workshop ;
- les répertoires remplacés sont réellement fournis, par exemple 88 fichiers de personnages, 21 fichiers de states, 22 de pops, 23 de buildings et 17 de state regions.

C'est le meilleur exemple local de total conversion Victoria 3 1.13 utilisant le mécanisme moderne.

### 1776 Workshop / hotfix source

Le paquet Workshop installé `3617930953` et `1776_Age_of_Revolutions_hotfix_source` contiennent chacun :

- 13 fichiers dans `common/history/characters` ;
- un metadata `2.3.0` valide avec `game_custom_data` ;
- `replace_paths` contenant explicitement `common/history/characters` ;
- aucun `descriptor.mod` à la racine du paquet Workshop.

Ce paquet est une preuve encore plus directement transposable : la solution portable avait déjà été encodée dans une version 2.3.0 de 1776, mais n'est pas présente dans le metadata 2.2.0 du dépôt actif.

### DLC officiels

Les 17 DLC sont montés séparément par `virtualfilesystem_physfs.cpp` avant le mod. Aucun `metadata.json`, `descriptor.mod`, manifeste de remplacement ou occurrence texte des clés recherchées n'a été trouvé sous `game/dlc`. Leur activation est gérée par le produit/installateur et ne fournit donc pas un format directement transposable aux mods utilisateur. Aucune extrapolation DLC vers mod n'est nécessaire pour le verdict.

## 7. Filename precedence behavior

L'installation 1.13 contient actuellement 262 fichiers vanilla dans `common/history/characters`; le fork en contient 13. Il n'existe que trois collisions de basename exactes :

```text
dei - dutch east indies.txt
fra - france.txt
per - persia.txt
```

Les variantes suivantes ne sont pas des collisions et coexistent donc dans l'inventaire VFS :

| Fork | Vanilla | Conséquence observée |
|---|---|---|
| `aus.txt` | `aus - austria.txt` | les deux sont parsés dans `debug.log` |
| `gbr.txt` | `gbr - great britain.txt` | le vanilla long reste actif |
| `rus.txt` | `rus - russia.txt` | le vanilla long reste actif |
| `spa.txt` | `spa - spain.txt` | aucune collision de nom, donc coexistence |

L'audit CLEANUP-2A avait ainsi reconstruit 272 fichiers effectifs : `13 + 262 - 3`. Le runtime échoué confirme directement la coexistence pour AUS et les fichiers vanilla GBR/RUS/PRU.

```text
FILENAME_OVERRIDE_CONFIRMED = YES
```

Cette précédence exacte par fichier est le comportement VFS de repli, mais ce n'est pas la seule primitive disponible : `game_custom_data.replace_paths` fournit bien un remplacement de répertoire en 1.13.

Un fichier comment-only portant exactement `chi - china.txt` devrait suffire au niveau VFS pour masquer le fichier homonyme vanilla. L'acceptation d'un fichier vide/comment-only par le chargeur de ce datatype n'a toutefois pas encore été validée en runtime. Cette hypothèse ne justifie pas la génération de masse.

## 8. Workshop portability

Une solution portable doit être contenue dans le package, sans modification d'un `.mod` externe chez l'abonné. `game_custom_data.replace_paths` satisfait cette condition :

- le chemin est relatif au VFS ;
- il se trouve dans `.metadata/metadata.json`, inclus dans le package ;
- il est présent à l'identique dans Basileia local et Workshop ;
- il est déjà présent dans le Workshop 1776 `3617930953` ;
- aucun chemin `C:\Users\simeo` n'est requis ;
- aucun `descriptor.mod` Workshop n'est requis.

La modification manuelle du descripteur externe doit donc être rejetée comme solution de distribution.

## 9. Candidate solutions

| Option | SUPPORTED_BY_LOCAL_1_13_EVIDENCE | WORKSHOP_PORTABLE | MAINTAINABILITY | DLC_UPDATE_RISK | NUMBER_OF_FILES_REQUIRED | VERDICT |
|---|---|---|---|---|---:|---|
| A — `game_custom_data.replace_paths` dans `.metadata/metadata.json` | YES | YES | haute | faible à modéré : les nouveaux personnages vanilla sont volontairement exclus | 1 metadata modifié | **RECOMMANDÉE** |
| B — `replace_path` legacy dans un autre descripteur | NO : les deux placements testés échouent et aucune référence 1.13 n'en dépend | NO pour un `.mod` externe manuel | faible | inconnu | indéterminé | REJETÉE |
| C — shadow exact filename-by-filename | PARTIAL : précédence exacte prouvée, fichier vide non testé | YES | faible | élevé : chaque nouveau fichier vanilla doit être ajouté | 259 nouveaux noms au minimum aujourd'hui, car 3 des 262 existent déjà | FALLBACK seulement |
| D — reconstruire une autre architecture d'historique | NO | UNKNOWN | faible | élevé | indéterminé | NON JUSTIFIÉE |
| E — synchroniser la structure metadata déjà publiée par 1776 2.3.0 | YES | YES | haute | faible à modéré | 1 metadata modifié | équivalent concret de A, **RECOMMANDÉE** |

Le risque DLC de l'option A est un choix de total conversion : les ajouts officiels futurs dans le dossier remplacé ne seront pas hérités automatiquement. C'est précisément la propriété recherchée ici et elle évite la réapparition silencieuse de titulaires 1836.

## 10. Recommended controlled experiment

Le prochain test doit modifier un seul fichier de configuration, pas un personnage :

1. lors d'une phase explicitement autorisée, conserver les champs existants de `.metadata/metadata.json` et ajouter uniquement :

   ```json
   "game_custom_data": {
     "multiplayer_synchronized": true,
     "replace_paths": [
       "common/history/characters"
     ]
   }
   ```

2. ne modifier ni le descripteur interne ni le descripteur externe pendant ce test, afin que le seul changement causal soit le metadata moderne ;
3. l'utilisateur effectue un redémarrage complet de Victoria 3 ;
4. contrôler uniquement CHI au 1er janvier 1776, sans QA mondiale ;
5. contrôler aussi que la nouvelle session ne produit plus `Expected member (game_custom_data)`.

Résultat binaire :

```text
MECHANISM_WORKS = YES
```

si l'erreur metadata disparaît et si Daoguang issu de `chi - china.txt` vanilla n'est plus chargé. Sinon : `MECHANISM_WORKS = NO`, puis seulement alors préparer le test fallback d'un unique shadow `chi - china.txt` comment-only.

Le test recommandé ne crée pas Qianlong et ne corrige pas encore CHI. L'absence temporaire du titulaire historique attendu est acceptable pour prouver uniquement l'isolation VFS.

## 11. Protected-state verification

- branche et HEAD conformes à l'attendu ;
- `git diff --check` ne signale aucune erreur ;
- aucun fichier sous `common/history/characters` n'est modifié ou non suivi ;
- aucun batch historique CLEANUP-2B n'est commencé ;
- les sept fichiers de recherche technologique sont toujours présents, untracked et unstaged ; aucun n'a été écrit pendant cet audit ;
- BIC conserve `activate_law = law_type:law_frontier_colonization` à la ligne 13 de `common/history/countries/bic - british east india company.txt` et ce fichier ne contient pas `law_colonial_exploitation` ;
- aucune entrée fichier/répertoire nommée exactement `bject` n'est présente hors internals Git ;
- Codex n'a lancé aucun processus Victoria 3 ;
- aucune commande Git mutante n'a été exécutée.

Anomalie de baseline à ne pas masquer : `git status --short` affiche actuellement `M  descriptor.mod`, et `git diff --cached --name-only` affiche `descriptor.mod`. Le descripteur interne est donc **déjà staged** au moment de ce diagnostic. Codex n'a ni créé ni modifié ce staging et ne l'a pas annulé, car toute mutation Git est interdite par la demande. La validation « aucun staging » n'est donc pas satisfaite par l'état reçu, même si aucun staging supplémentaire n'a été effectué ici.

Seul le présent rapport est créé par cette phase.

## 12. Final verdict

```text
REPLACE_PATH_SUPPORTED_IN_THIS_CONTEXT = NO
REPLACE_PATH_FAILURE_REASON = Le singulier legacy placé dans descriptor.mod et le .mod externe n'est pas importé comme politique VFS par le flux metadata 1.13 observé; le runtime lit .metadata/metadata.json, le rejette faute de game_custom_data, puis monte le contenu sans replace_paths.
ACTUAL_VFS_OVERRIDE_MECHANISM = game_custom_data.replace_paths dans .metadata/metadata.json pour un répertoire complet; sinon précédence par basename exact fichier par fichier.
METADATA_MECHANISM_FOUND = YES
WORKING_1_13_REFERENCE_MOD = [1.13] Basileia Romaion 1736 (local + Workshop 2880120246), corroboré par 1776 Workshop 3617930953
WORKSHOP_PORTABLE_SOLUTION_IDENTIFIED = YES
RECOMMENDED_NEXT_EXPERIMENT = Ajouter seulement game_custom_data.replace_paths=["common/history/characters"] au metadata du fork actif, puis un seul lancement utilisateur et contrôle CHI/Daoguang + absence de l'erreur metadata.
```

La primitive de remplacement de dossier existe donc bien dans Victoria 3 1.13, mais son emplacement démontré est le metadata JSON moderne et sa clé est `replace_paths` au pluriel. CLEANUP-2B-0 n'est pas runtime validé. Toute reconstruction historique reste bloquée jusqu'au résultat de ce test contrôlé.

```text
CLEANUP2B0_RUNTIME = FAIL
REPLACE_PATH_RUNTIME_VALIDATED = NO

ACTIVE_1776_MOD_PATH = C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork
DUPLICATE_1776_MOD_MOUNTS = 0

REPLACE_PATH_SUPPORTED_IN_THIS_CONTEXT = NO
REPLACE_PATH_FAILURE_REASON = Le chargeur 1.13 lit le metadata JSON moderne, exige game_custom_data et n'applique pas les clés legacy des descripteurs; le metadata actif incomplet est monté sans game_custom_data.replace_paths.

METADATA_REPLACEMENT_MECHANISM_FOUND = YES
WORKING_VICTORIA3_1_13_REFERENCE_FOUND = YES

FILENAME_OVERRIDE_CONFIRMED = YES
WORKSHOP_PORTABLE_SOLUTION_IDENTIFIED = YES

HISTORICAL_RULER_RECONSTRUCTION_BLOCKED = YES
CODEX_LAUNCHED_VICTORIA3 = NO

SAFE_FOR_NEXT_CONTROLLED_EXPERIMENT = YES
```

STOP.
