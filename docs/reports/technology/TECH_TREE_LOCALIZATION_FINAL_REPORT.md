# Technology tree localization — final pass

## Scope and authority

The current local working tree is authoritative. The target game data is Victoria 3 1.13.11 under `C:/Games/Victoria 3/game`. This pass changed localization only: no technology definitions, eras, prerequisites, unlocks, buildings, production methods, history, or gameplay values were edited. The working tree already contained unrelated gameplay changes before this pass; they were left untouched.

The baseline is preserved in `TECH_TREE_LOCALIZATION_AUDIT.csv`, whose notes include source definitions, prerequisites, and directly unlocked buildings or production methods where present. Text decisions, including the old and proposed titles and the new English and French descriptions, are in `TECH_TREE_LOCALIZATION_PROPOSALS.csv`. The proposal inventory also lists all 21 mod-added technologies whose existing text was already suitable and therefore retained. The `TECH_TREE_LOCALIZATION_REVIEW.csv` contains its requested header and no unresolved rows.

## Inventory and findings

| Measure | Before | After |
| --- | ---: | ---: |
| Technologies defined in the fork | 292 | 292 |
| Mod-added technologies | 114 | 114 |
| Vanilla IDs with fork definitions | 178 | 178 |
| Generic or ID-derived names identified | 0 | 0 |
| Missing English names | 1 | 0 |
| Missing French names | 0 | 0 |
| English titles over three words | 5 | 0 |
| French titles over three words | 27 | 0 |
| Generic English descriptions | 86 | 0 |
| Generic French descriptions | 86 | 0 |
| Missing English descriptions | 1 | 0 |
| Missing French descriptions | 0 | 0 |
| Duplicate technology-description texts, English / French | 0 / 0 | 0 / 0 |
| Duplicate technology localization keys, English / French | 0 / 0 | 0 / 0 |

The 86 generic descriptions in each language used repeated production, military, naval, or institutional templates. They have been replaced with technology-specific historical context, normally one sentence per language. The previously absent English title and description for `mechanized_spinning` are now present. Descriptions that were already specific were preserved. Several otherwise healthy late-game titles were shortened solely to respect the three-word interface limit; their gameplay definitions and descriptions were not changed.

## Editorial choices

- Production descriptions distinguish early craft or agricultural practice from later machinery, chemistry, and systematic engineering.
- Military and naval descriptions identify the relevant weapon, organization, construction method, or navigational practice rather than repeating a generic statement about army or fleet progress.
- Society descriptions distinguish institutions, scientific methods, education, printing, and medical practices. Variolation, vaccination, and organized immunization are kept conceptually separate.
- Existing vanilla localizations that were specific and already fitted the interface were not rewritten.
- Names were checked in both languages against the maximum of three lexical words. Historical nuance that did not fit in a title was placed in the description.

The existing `localization/*/replace/1776_overrides_l_*.yml` files remain authoritative for the keys already present there. The new `localization/*/replace/tech_tree_final_localization_replace_l_*.yml` files contain only keys previously absent from the fork's localization files, including concise overrides for longer vanilla titles. No technology key is defined twice within either fork language directory.

A directory-wide check also found one pre-existing, identical duplicate outside technology localization in each language: `pm_arc_welded_buildings_desc` appears in both `tech3a_technology_l_*.yml` and `replace/tech3a_arc_welding_replace_l_*.yml`. The latter is the intentional authoritative override. It is a production-method description, was not modified in this pass, and is not an ambiguous technology-key duplicate.

## Files changed in this pass

- `localization/english/tech3a_technology_l_english.yml`
- `localization/french/tech3a_technology_l_french.yml`
- `localization/english/replace/1776_overrides_l_english.yml`
- `localization/french/replace/1776_overrides_l_french.yml`
- `localization/english/replace/tech_tree_final_localization_replace_l_english.yml` (new)
- `localization/french/replace/tech_tree_final_localization_replace_l_french.yml` (new)
- `docs/reports/technology/TECH_TREE_LOCALIZATION_AUDIT.csv` (baseline)
- `docs/reports/technology/TECH_TREE_LOCALIZATION_PROPOSALS.csv`
- `docs/reports/technology/TECH_TREE_LOCALIZATION_REVIEW.csv`
- `docs/reports/technology/tech_tree_localization_pass.mjs` (reproducible inventory and validation)
- This report

## Validation

The technology/localization inventory checks all 292 defined IDs against English and French names and `_desc` keys, including vanilla fallbacks. The final validation found no missing title or description, no remaining generic description, no title over three words, no duplicate technology key, and no exact duplicated technology description. All modified localization files retain their UTF-8 BOM; changed entries passed Paradox-style quoted-line validation. The three CSV files were imported and checked as rectangular tables: 292 audit rows, 133 proposal-inventory rows (112 changed; 21 retained), and zero REVIEW rows. `git diff --check` passes. No game launch was performed.

This pass made **0 gameplay-file changes**. No commit or push was made.

## Required final summary

```text
TECHNOLOGIES DEFINED = 292
MOD-ADDED OR MODIFIED TECHNOLOGIES = 292 (114 added; 178 vanilla IDs redefined by the fork)
GENERIC NAMES BEFORE = 0
GENERIC NAMES AFTER = 0
MISSING EN NAMES BEFORE = 1
MISSING EN NAMES AFTER = 0
MISSING FR NAMES BEFORE = 0
MISSING FR NAMES AFTER = 0
GENERIC DESCRIPTIONS BEFORE = 172 strings (86 EN; 86 FR)
GENERIC DESCRIPTIONS AFTER = 0
MISSING EN DESCRIPTIONS AFTER = 0
MISSING FR DESCRIPTIONS AFTER = 0
EN LOCALIZATIONS CHANGED = 96 keys
FR LOCALIZATIONS CHANGED = 117 keys
DUPLICATE EN KEYS = 0
DUPLICATE FR KEYS = 0
REVIEW CASES = 0
GAMEPLAY FILE CHANGES = 0 in this pass
git diff --check = PASS
NO COMMIT
NO PUSH
```
