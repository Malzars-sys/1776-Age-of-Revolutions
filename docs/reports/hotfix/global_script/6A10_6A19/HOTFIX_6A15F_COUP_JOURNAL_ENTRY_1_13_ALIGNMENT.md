# HOTFIX 6A.15F — Alignement de la journal entry Coup sur Victoria 3 1.13

Date : 2026-07-30

Phase : `HOTFIX_6A15F_COUP_JOURNAL_ENTRY_1_13_ALIGNMENT`

## État d'entrée

- branche : `hotfix-dlc-audit`;
- HEAD initial : `3d1d65c83f7e396f36b19026de73d346d6e4f23f`;
- message du HEAD : `Audit Coup journal entry 1.13 compatibility`;
- rapport 6A.15R présent dans le HEAD avec les cinq verdicts requis;
- fichiers suivis propres, index staged vide;
- seuls `bject` et les sept fichiers technologiques protégés étaient non suivis;
- aucun processus Victoria 3, dowser ou Paradox actif;
- stash : `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla`;
- objet du stash : `518df704fa14599c0f254fae13859210663dd976`;
- `git diff --check` : PASS.

Les éléments non suivis protégés et le contenu du stash n'ont été ni ouverts,
ni modifiés, ni stagés.

## Preuves trois voies

| Version | Taille | SHA-256 |
| --- | ---: | --- |
| fork avant correction | 2932 | `3AB98023990198A9871FAEE3CF459558B36FECC11B927F1FCF34982A39E5FB2F` |
| source hotfix, lecture seule | 3074 | `F39D26651A3200B1044A2E79D070A8BFEEBB205183079A9BB993EF6D520C5665` |
| vanilla 1.13, lecture seule | 2741 | `3E4705DFC02785CED86F9C5967CDDC0D5AC0E411E30974F82052ACD4004C7ACB` |

Avant écriture, l'objet `je_ip4_coup` contenait exactement une occurrence
active de l'ancienne propriété et zéro occurrence de la propriété moderne.
La source hotfix et vanilla contenaient toutes deux la propriété moderne.

## Substitution chirurgicale

Fichier : `common/journal_entries/01_coup.txt`

Objet unique : `je_ip4_coup`

```diff
-	should_be_pinned_by_default = yes
+	should_be_pinned_by_default_uninvolved_or_context = yes
```

La modification a été effectuée comme une substitution de ligne isolée. La
validation binaire avant/après confirme la conservation du BOM UTF-8, des fins
de ligne LF, du saut final, de l'indentation et de tout le contenu adjacent.
Aucun remplacement global n'a été exécuté.

## Validation statique

- ancienne propriété dans l'objet : `0`;
- nouvelle propriété dans l'objet : `1`;
- SHA-256 final : `37C2669619CD26C30450F41082716BF30CA12949AA5FEE59BA0D25D498339602`;
- taille finale : `2954` octets;
- BOM UTF-8 : conservé;
- fins de ligne : `145` LF et `0` CRLF, conservées;
- saut final : conservé;
- accolades : `49/49`;
- diff gameplay : un fichier, un objet, un hunk, `1+/1-`;
- `git diff --check` : PASS;
- index staged : vide;
- aucun processus Victoria 3, dowser ou Paradox actif.

Le hash de la source hotfix reste
`F39D26651A3200B1044A2E79D070A8BFEEBB205183079A9BB993EF6D520C5665`
et celui de vanilla reste
`3E4705DFC02785CED86F9C5967CDDC0D5AC0E411E30974F82052ACD4004C7ACB`.

Les fichiers événementiels interdits sont inchangés :

- `events/iberia_events/ip4_coup_events.txt` :
  `8DD5A07F60A3E1C623CF48495B062AFE0388602E256CBA8384CD8540067B5AD2`;
- `events/agitators_events/coup_events.txt` :
  `88D1B0AE45F296A84FBB997C3F089423A2240790742291DDE359A9509DA5F3CE`.

Aucune loi, aucun scope, personnage, groupe d'intérêt, lobby, cooldown,
cleanup, invalidation, formule, variable, localisation ou équilibrage n'a été
modifié. Les événements Coup et toutes les zones protégées restent hors
périmètre.

## Baseline des logs avant correction

Le snapshot contient `60` fichiers, avec le manifeste :
`C3CB860A3A213219125B274B64205EA9DE743528AABB51DFAC261023EF98EDBA`.

Les trois rotations historiques contiennent `1122` occurrences du diagnostic
legacy, soit `374` par chargement. Elles contiennent `3` erreurs ciblées sur
`common/journal_entries/01_coup.txt:139`, soit une par chargement. La baseline
fonctionnelle documentée est de `374` diagnostics dans `140` fichiers par
chargement. Les diagnostics distincts des deux fichiers d'événements Coup
restent explicitement hors périmètre.

## État après correction statique

- branche : `hotfix-dlc-audit`;
- HEAD inchangé :
  `3d1d65c83f7e396f36b19026de73d346d6e4f23f`;
- aucun commit automatique;
- index staged vide;
- stash inchangé :
  `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla`;
- objet du stash inchangé :
  `518df704fa14599c0f254fae13859210663dd976`;
- un seul fichier gameplay modifié;
- le présent rapport est le seul document créé avant runtime;
- aucun document de navigation n'a encore été modifié.

## Rollback exact

En cas d'échec postérieur, le rollback autorisé consiste uniquement à remplacer :

```txt
should_be_pinned_by_default_uninvolved_or_context = yes
```

par :

```txt
should_be_pinned_by_default = yes
```

Le résultat doit retrouver exactement le SHA-256 initial
`3AB98023990198A9871FAEE3CF459558B36FECC11B927F1FCF34982A39E5FB2F`.
Aucune commande Git destructive ni copie complète ne doit être utilisée.

## Runtime humain

L'opérateur a lancé une nouvelle partie avec le Vietnam, a joué du 1er au
10 janvier 1776 et n'a observé aucune clé brute ni anomalie politique visible.
La journal entry Coup n'a pas été forcée. L'opérateur a ensuite confirmé
explicitement la fermeture de Victoria 3 et du launcher Paradox; le contrôle
processus final trouve `0` processus Victoria 3, dowser ou Paradox.

Le nouveau `debug.1.log` prouve les montages :

```text
National Awakening|dlc/dlc014_ip3/dlc014_ip3.dlc
Mounted Data: C:/Games/Victoria 3 The Great Wave/game/dlc/dlc014_ip3
1776 - Age of Revolutions, Total Conversion Mod|C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork
Mounted Data: C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork
```

Codex n'a lancé ni le jeu ni le launcher.

## Analyse des nouveaux logs

Le manifeste des `60` fichiers après runtime est :
`E578A7EA4391E256D4D921DBCB3B002CCAF5174D991E467384AD8DA9ACAB5DD0`.
Il diffère du manifeste pré-runtime et confirme une nouvelle production.

Le lancement est réparti par rotation entre `debug.1.log` et `debug.log` :

| Périmètre | Diagnostics legacy | Fichiers distincts | Cible `01_coup.txt:139` |
| --- | ---: | ---: | ---: |
| `debug.1.log` | 373 | 139 | 0 |
| `debug.log` | 0 | 0 | 0 |
| runtime combiné | 373 | 139 | 0 |

La baseline passe donc exactement de `374` diagnostics dans `140` fichiers à
`373` diagnostics dans `139` fichiers. Le diagnostic ciblé
`Unexpected token: should_be_pinned_by_default` dans
`common/journal_entries/01_coup.txt:139` passe de `1` à `0`.

Les anciennes rotations `debug.3.log` et `debug.5.log` conservent chacune leur
preuve historique `374/140` et leur ancienne erreur ciblée; elles sont
antérieures au runtime de validation et ne sont pas comptées comme résultat
post-correction.

Les diagnostics d'API Coup restant dans le runtime sont distincts et hors
périmètre :

- `events/iberia_events/ip4_coup_events.txt` : `8`;
- `events/agitators_events/coup_events.txt` : `8`.

Ils ne remettent pas en cause la suppression de l'erreur de propriété ciblée.
Aucun diagnostic HBC, NAVY, BIC ou Merchant Banking n'est revendiqué comme
corrigé par 6A.15F.

## Finalisation documentaire et état final

Après runtime, exactement cinq documents sont créés ou modifiés :

1. le présent rapport;
2. `docs/reports/hotfix/INDEX.md`;
3. `HOTFIX_REPORT_INDEX.csv`;
4. `HOTFIX_MERGE_BLOCK_STATUS.csv`;
5. `HOTFIX_MERGE_COMPLETION_ROADMAP.md`.

`HOTFIX_NEXT_MERGE_PHASE_PROMPT.md` reste inchangé.

Les CSV sont validés avec `Import-Csv` :

- `HOTFIX_REPORT_INDEX.csv` : `127 × 22` avant, `128 × 22` après;
- `HOTFIX_MERGE_BLOCK_STATUS.csv` : `40 × 17` avant, `41 × 17` après;
- cellules structurelles nulles : `0`;
- chaque nouvelle ligne 6A.15F est unique;
- aucune ligne mal formée.

État final :

- branche `hotfix-dlc-audit`;
- HEAD initial et final :
  `3d1d65c83f7e396f36b19026de73d346d6e4f23f`;
- hash gameplay final :
  `37C2669619CD26C30450F41082716BF30CA12949AA5FEE59BA0D25D498339602`;
- un seul fichier gameplay modifié;
- aucun fichier événementiel modifié;
- index staged vide;
- aucun commit automatique;
- stash et objet du stash inchangés;
- `git diff --check` : PASS;
- Victoria 3 et le launcher Paradox fermés.

HOTFIX_6A15F_COUP_JOURNAL_ENTRY_1_13_STATIC_PASS
COUP_JOURNAL_ENTRY_PINNING_ONE_FILE_ONE_OBJECT_ONE_HUNK_ALIGNED
COUP_EVENT_SCOPE_LOBBY_LAW_COOLDOWN_UNCHANGED
HOTFIX_6A15F_COUP_JOURNAL_ENTRY_1_13_RUNTIME_PASS
COUP_JOURNAL_ENTRY_PINNING_PARSER_ERROR_1_TO_0
HOTFIX_6A15F_COUP_JOURNAL_ENTRY_1_13_ALIGNMENT_COMPLETE
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
NO_AUTOMATIC_COMMIT
