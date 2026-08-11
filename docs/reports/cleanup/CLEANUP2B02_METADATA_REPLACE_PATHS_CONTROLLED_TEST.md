# CLEANUP-2B-0.2 — Metadata replace_paths Controlled Test

Date : 2026-08-11

Version cible : Victoria 3 1.13 / The Great Wave

Cette phase prépare un test runtime utilisateur à variable unique. Elle ne valide pas encore le mécanisme et ne commence aucune reconstruction historique.

## 1. Baseline

La baseline a été contrôlée avant toute écriture :

```text
BRANCH = cleanup-post-release
HEAD = 25e346efd7c9ea247ad5946e8a756c2467c21ea2
GIT_DIFF_CHECK = PASS
STAGED_FILES = NONE
```

`descriptor.mod` apparaît comme modification non staged (` M descriptor.mod`). Il ne figure plus dans `git diff --cached --name-only`; le garde-fou imposant l'arrêt en présence d'un descripteur staged est donc levé.

Empreintes de référence avant modification :

```text
descriptor.mod SHA256 = 99B3A0AAA3337D296661D75BD0DD7496C4709DE4AA14F3BC2A50772E650B4246
1776_age_of_revolutions_fork.mod SHA256 = F0A761AFB6787FAC6CC52E55BA1BD13776C351746D4F190C8F80D35F6934C0A2
```

Le rapport `CLEANUP2B01_VFS_REPLACEMENT_RUNTIME_FAILURE_DIAGNOSTIC.md` a été lu intégralement avant l'expérience.

## 2. Previous runtime failure

CLEANUP-2B-0 reste en échec runtime. Les directives legacy `replace_path="common/history/characters"` des descripteurs interne et externe n'ont pas empêché le chargement des fichiers vanilla.

Le runtime utilisateur précédent signalait :

```text
Mod metadata read error. Error: Expected member (game_custom_data)
```

Les logs continuaient en outre de référencer notamment :

```text
common/history/characters/aus - austria.txt
common/history/characters/gbr - great britain.txt
common/history/characters/pru - prussia.txt
common/history/characters/rus - russia.txt
```

Le mécanisme n'est pas marqué PASS avant le nouveau runtime utilisateur.

## 3. Metadata before

Contenu exact avant cette phase :

```json
{"name":"Age of revolution /Fork","id":"","version":"2.2.0","supported_game_version":"1.13.0","short_description":"","tags":[],"relationships":[]}
```

Tous ces champs ont été conservés, avec leurs valeurs d'origine.

## 4. Victoria 3 1.13 reference structure

Trois références locales compatibles 1.13 ont été comparées :

1. `1776_Age_of_Revolutions_hotfix_source/.metadata/metadata.json`, version 2.3.0 ;
2. Workshop Victoria 3 `3617930953/.metadata/metadata.json`, version 2.3.0 ;
3. `Basileia_Romaion_1736/.metadata/metadata.json`, compatible `1.13.*`.

Les trois placent la politique VFS sous la même structure :

```json
"game_custom_data": {
  "multiplayer_synchronized": true,
  "replace_paths": [
    "common/history/characters"
  ]
}
```

La clé correcte est `replace_paths`, au pluriel. Aucun autre chemin des références n'a été copié. En particulier, cette expérience n'ajoute ni templates, ni states, ni pops, ni buildings, ni state regions.

## 5. Metadata modification

Un seul changement fonctionnel a été effectué, dans `.metadata/metadata.json`. Contenu final :

```json
{
  "name": "Age of revolution /Fork",
  "id": "",
  "version": "2.2.0",
  "supported_game_version": "1.13.0",
  "short_description": "",
  "tags": [],
  "relationships": [],
  "game_custom_data": {
    "multiplayer_synchronized": true,
    "replace_paths": [
      "common/history/characters"
    ]
  }
}
```

Le fichier `.metadata/metadata.json` est actuellement ignoré par `.gitignore:5` (`.metadata/`) et n'est pas suivi par Git. Cela n'empêche pas le test local, car le fichier existe dans le répertoire monté, mais confirme que la future phase CLEANUP-2B-0.3 devra traiter explicitement le suivi/packaging du metadata et auditer `tools/workshop/build_steam_package.ps1`.

Les descripteurs legacy sont volontairement laissés dans leur état reçu pour isoler la variable metadata.

## 6. Static validation

Validation stricte par parsing JSON :

```text
METADATA_JSON_VALID = YES
GAME_CUSTOM_DATA_PRESENT = YES
MULTIPLAYER_SYNCHRONIZED = true
REPLACE_PATHS_PRESENT = YES
REPLACE_PATH_COUNT = 1
REPLACE_PATH_1 = common/history/characters
```

Champs présents sous `game_custom_data` :

```text
multiplayer_synchronized
replace_paths
```

Aucune clé fautive `replace_path`, `replacePath` ou `replacePaths` n'est présente.

Contrôles d'isolation :

- empreinte du descripteur interne après modification : `99B3A0AAA3337D296661D75BD0DD7496C4709DE4AA14F3BC2A50772E650B4246`, identique à la baseline ;
- empreinte du descripteur externe après modification : `F0A761AFB6787FAC6CC52E55BA1BD13776C351746D4F190C8F80D35F6934C0A2`, identique à la baseline ;
- 13 fichiers de character history, comme avant ;
- 27 fichiers de character templates, comme avant ;
- aucun diff ou fichier non suivi sous `common/history/characters` ou `common/character_templates` ;
- `common/history/characters/chi - china.txt` n'existe pas dans le fork ;
- aucun shadow file créé ;
- `git diff --check` passe ;
- `git diff --cached --name-only` est vide.

## 7. USER runtime test

Codex ne lance pas Victoria 3. L'utilisateur doit effectuer exactement ce test minimal :

1. fermer complètement Victoria 3 ;
2. relancer avec uniquement `1776_Age_of_Revolutions_fork` actif ;
3. commencer une nouvelle partie au 1er janvier 1776 ;
4. ouvrir uniquement CHI / Chine des Qing ;
5. vérifier si Daoguang est encore le souverain ;
6. fermer le jeu ;
7. transmettre les nouveaux logs ou le résultat du contrôle.

L'absence de Qianlong est normale. CHI peut temporairement ne pas avoir de titulaire historique ou recevoir un personnage générique : ce test mesure uniquement l'isolation VFS.

## 8. Expected outcomes

Après le runtime utilisateur, rechercher :

```text
Expected member (game_custom_data)
common/history/characters/chi - china.txt
common/history/characters/gbr - great britain.txt
common/history/characters/pru - prussia.txt
common/history/characters/aus - austria.txt
pdx_mod_metadata
replace_paths
```

Le test sera PASS seulement si les trois conditions suivantes sont simultanément satisfaites :

```text
METADATA_PARSE_ERROR_GONE = YES
DAOGUANG_ABSENT_AT_CHI = YES
VANILLA_CHI_CHARACTER_HISTORY_NOT_ACTIVE = YES
```

Alors seulement :

```text
MECHANISM_WORKS = YES
```

Si l'une manque, `MECHANISM_WORKS = NO`. Aucun verdict n'est anticipé dans le présent rapport.

## 9. Protected-state verification

- les sept recherches technologiques sont toujours untracked et unstaged ; leurs tailles et empreintes SHA-256 correspondent au diagnostic précédent ;
- BIC conserve `activate_law = law_type:law_frontier_colonization` à la ligne 13 et son fichier de pays ne contient pas `law_colonial_exploitation` ;
- aucune entrée fichier/répertoire nommée exactement `bject` n'est présente hors internals Git ;
- aucun personnage ni template n'a été modifié ;
- aucun shadow file n'a été créé ;
- aucun descripteur n'a été modifié pendant cette phase ;
- aucun builder Workshop n'a été modifié ;
- aucune mutation Git ni aucun staging n'a été effectué ;
- Codex n'a pas lancé Victoria 3.

Fichiers touchés par cette phase :

- modifié : `.metadata/metadata.json` — fichier ignoré par Git ;
- créé : `docs/reports/cleanup/CLEANUP2B02_METADATA_REPLACE_PATHS_CONTROLLED_TEST.md` ;
- aucun autre fichier.

## 10. Pending verdict

```text
METADATA_JSON_VALID = YES
GAME_CUSTOM_DATA_PRESENT = YES
REPLACE_PATHS_PRESENT = YES
REPLACE_PATH_COUNT = 1
REPLACE_PATH_1 = common/history/characters

LEGACY_DESCRIPTOR_CHANGED_THIS_PHASE = NO
CHARACTER_HISTORY_MODIFIED = NO
SHADOW_FILES_CREATED = NO

CODEX_LAUNCHED_VICTORIA3 = NO
USER_RUNTIME_REQUIRED = YES

MECHANISM_WORKS = PENDING_USER_RUNTIME
CLEANUP2B0_RUNTIME_VALIDATED = NO

SAFE_FOR_USER_RUNTIME = YES
```

STOP.

## 11. Final user runtime result (supersedes the pending verdict)

Le runtime utilisateur du 11 août 2026 démarré à 15:21:36, arrivé au chargement de partie à 15:24 et fermé à 15:31:41 valide l'expérience. Le fichier actif `logs/debug.log` ne contient plus `Expected member (game_custom_data)` ni aucune erreur de lecture du metadata.

Le même log monte exactement une source de mod utilisateur :

```text
C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork
```

Il ne contient aucune référence à `common/history/characters/chi - china.txt` ni aux autres fichiers vanilla de character history vus dans les anciens logs. Les deux seules références à ce répertoire sont :

```text
common/history/characters/ir1 - mamluk iraq.txt
common/history/characters/aus.txt
```

Ces deux fichiers appartiennent au fork. Les treize références à des fichiers vanilla observées dans `debug.1.log` avant le test ne sont plus présentes. Aucune nouvelle erreur VFS massive n'apparaît. Le constat visuel utilisateur — Daoguang absent de CHI, Maria II absente de POR et remplacement temporaire par des rulers génériques — concorde avec les logs.

Les rulers génériques ne sont que des placeholders moteur ; ce PASS ne vaut pas reconstruction historique.

```text
METADATA_PARSE_ERROR_GONE = YES
VANILLA_CHARACTER_HISTORY_EXCLUDED = YES
DAOGUANG_ABSENT_AT_CHI = YES
MECHANISM_WORKS = YES
CLEANUP2B0_RUNTIME_VALIDATED = YES
FINAL_VERDICT = PASS
```
