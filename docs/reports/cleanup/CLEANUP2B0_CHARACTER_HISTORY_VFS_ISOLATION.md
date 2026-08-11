# CLEANUP-2B-0 — Character History VFS Isolation

Audit and implementation date: 2026-08-11  
Target: Victoria 3 1.13 / The Great Wave  
Scope: isolate start character history only; no individual historical-character correction; no runtime by Codex.

## 1. Baseline

| Check | Result |
|---|---|
| Branch | `cleanup-post-release` |
| HEAD | `25e346efd7c9ea247ad5946e8a756c2467c21ea2` |
| Commit subject | `Complete Maratha Konkan flotilla cleanup` |
| Tracked diff at entry | none |
| Staged files at entry | none |
| `git diff --check` at entry | PASS |
| CLEANUP-2A report read completely | YES |
| CLEANUP-2A CSV parsed completely | YES, 816 rows |

The pre-existing untracked CLEANUP-1D/CLEANUP-2A documents and seven protected technology research files were retained. No file was staged and no Git mutation command was used.

## 2. Structural root cause

The repository descriptor did not isolate `common/history/characters`. Victoria 3 therefore merged fork and vanilla files by exact filename. Only three of the thirteen fork filenames matched a vanilla filename; the other 259 vanilla history files remained active.

This is the demonstrated cause of the 536 deterministic vanilla-1836 instances in CLEANUP-2A. Correcting those instances individually would preserve the wrong loading architecture and require permanent maintenance against vanilla and DLC changes.

`STRUCTURAL_ROOT_CAUSE_CONFIRMED = YES`.

## 3. Current VFS

### Before isolation

| Measure | Count |
|---|---:|
| Fork character-history files | 13 |
| Vanilla character-history files on disk | 262 |
| Exact filename overrides | 3 |
| Active vanilla character-history files | 259 |
| Effective character-history files | 272 |
| Potential `create_character` commands in the 259 active vanilla files | 838 |
| Commands that instantiate for countries present in the effective 1776 setup | 536 |

The exact overrides were:

- `dei - dutch east indies.txt`
- `fra - france.txt`
- `per - persia.txt`

The distinction between 838 commands and 536 start instances matters: many vanilla files target countries that do not exist in this 1776 map, so their guarded `c:TAG ?=` blocks do not instantiate.

### After isolation

`replace_path = "common/history/characters"` removes all vanilla files in that directory from the effective VFS and exposes only the thirteen fork files. The 259 currently active vanilla files disappear; the three already-shadowed vanilla files remain excluded as before.

| Required metric | Result |
|---|---:|
| `CURRENT_EFFECTIVE_CHARACTER_HISTORY_FILES` | 272 |
| `FORK_CHARACTER_HISTORY_FILES` | 13 |
| `VANILLA_CHARACTER_HISTORY_FILES` | 262 |
| `EXACT_FILENAME_OVERRIDES` | 3 |
| `VANILLA_FILES_REMOVED_BY_REPLACE_PATH` | 259 active VFS files; all 262 base-directory files excluded |
| `START_CHARACTERS_REMOVED_BY_REPLACE_PATH` | 536 |
| `EFFECTIVE_CHARACTER_HISTORY_FILES_AFTER` | 13 |

### Exact active vanilla file inventory before isolation

The following table lists every vanilla filename that was active before the descriptor change. “Potential” counts parsed `create_character` commands in the file; “1776 instances” counts rows that actually instantiated according to the CLEANUP-2A country/start inventory.

| Active vanilla file | Potential commands | 1776 instances |
|---|---:|---:|
| `abu - abu dhabi.txt` | 3 | 0 |
| `ace - aceh.txt` | 2 | 2 |
| `agc - angoche.txt` | 2 | 2 |
| `ait - ait abbas.txt` | 2 | 2 |
| `alk - alyaska.txt` | 0 | 0 |
| `alw - alwar.txt` | 2 | 0 |
| `anh - anhalt.txt` | 2 | 2 |
| `ank - ankole.txt` | 1 | 1 |
| `arb - arabistan.txt` | 2 | 2 |
| `arg - argentina.txt` | 10 | 0 |
| `ash - ashanti.txt` | 1 | 1 |
| `asm - assam .txt` | 3 | 0 |
| `aus - austria.txt` | 13 | 13 |
| `awa - awadh.txt` | 3 | 3 |
| `aws - aussa.txt` | 1 | 0 |
| `bad - baden.txt` | 6 | 6 |
| `bag - bagelkhand.txt` | 2 | 0 |
| `bal - bali.txt` | 2 | 2 |
| `bas - bastar.txt` | 2 | 0 |
| `bav - bavaria.txt` | 6 | 6 |
| `bce - ceylon.txt` | 2 | 0 |
| `bel - belgium.txt` | 11 | 0 |
| `ber - baroda.txt` | 3 | 0 |
| `bgi - bagirmi.txt` | 1 | 1 |
| `bgm - begemder.txt` | 3 | 0 |
| `bhn - bahrain.txt` | 1 | 1 |
| `bho - bhopal.txt` | 3 | 0 |
| `bhu - bhutan.txt` | 1 | 1 |
| `bhv - bhavnagar.txt` | 3 | 3 |
| `bhw - bahawalpur.txt` | 2 | 0 |
| `bic - britishindia.txt` | 11 | 11 |
| `bik - bikaner.txt` | 2 | 0 |
| `blg - bulungan.txt` | 2 | 2 |
| `bnj - banjar.txt` | 2 | 2 |
| `bol - bolivia.txt` | 6 | 0 |
| `bor - bornu.txt` | 2 | 2 |
| `bra - brunswick.txt` | 1 | 1 |
| `bre - bremen.txt` | 1 | 1 |
| `bru - brunei.txt` | 2 | 2 |
| `brz - brazil.txt` | 13 | 13 |
| `bst - basuto.txt` | 1 | 1 |
| `btn - buton.txt` | 2 | 2 |
| `buk - bukhara.txt` | 2 | 2 |
| `bun - bundelkhand.txt` | 2 | 0 |
| `bur - burma.txt` | 2 | 2 |
| `cam - cambodia.txt` | 2 | 2 |
| `chc - chechnya.txt` | 2 | 2 |
| `chi - china.txt` | 10 | 10 |
| `chl - chile.txt` | 8 | 0 |
| `chp - champasak.txt` | 2 | 2 |
| `cht - chitral.txt` | 2 | 0 |
| `cir - circassia.txt` | 2 | 2 |
| `clm - colombia.txt` | 6 | 0 |
| `cob - saxe-coburg-gotha.txt` | 2 | 2 |
| `coc - cochin.txt` | 3 | 3 |
| `con - constantine.txt` | 2 | 2 |
| `coo - cooch behar.txt` | 3 | 3 |
| `cro - croatia.txt` | 3 | 0 |
| `cub - cuba.txt` | 8 | 8 |
| `dai - dai nam.txt` | 2 | 2 |
| `den - denmark.txt` | 12 | 0 |
| `dha - dharmpur.txt` | 2 | 0 |
| `ecu - ecuador.txt` | 3 | 0 |
| `egy - egypt.txt` | 6 | 0 |
| `ezo - ezochi.txt` | 1 | 1 |
| `frm - frankfurt.txt` | 1 | 1 |
| `fzn - fezzan.txt` | 2 | 0 |
| `gar - garwhal.txt` | 2 | 2 |
| `gbr - great britain.txt` | 18 | 18 |
| `gjm - gojjam.txt` | 1 | 0 |
| `gld - geledi.txt` | 1 | 1 |
| `gre - greece.txt` | 10 | 0 |
| `gwa - gwalior.txt` | 3 | 3 |
| `gza - gaza.txt` | 2 | 0 |
| `hai - haiti.txt` | 7 | 7 |
| `ham - hamburg.txt` | 1 | 1 |
| `han - hannover.txt` | 3 | 3 |
| `har - harar.txt` | 3 | 0 |
| `haw - hawaii.txt` | 3 | 3 |
| `hbc - hudson bay company.txt` | 0 | 0 |
| `hdj - hedjaz.txt` | 2 | 2 |
| `hek - hesse-kassel.txt` | 2 | 2 |
| `her - herat.txt` | 3 | 0 |
| `hes - hesse.txt` | 2 | 2 |
| `hoh - hohenzollern.txt` | 2 | 2 |
| `hun - hungary.txt` | 8 | 8 |
| `hyd - hyderabad.txt` | 4 | 4 |
| `ida - idar.txt` | 2 | 0 |
| `ind - indore.txt` | 2 | 0 |
| `ion - ionian islands.txt` | 1 | 0 |
| `isq - isaaq.txt` | 1 | 1 |
| `jab - jabal shammar.txt` | 2 | 0 |
| `jai - jaipur.txt` | 3 | 0 |
| `jap - japan.txt` | 21 | 21 |
| `jas - jaisalmer.txt` | 2 | 0 |
| `jey - jeypore.txt` | 2 | 2 |
| `jhn - jhansi.txt` | 2 | 0 |
| `jmb - jambi.txt` | 2 | 2 |
| `jod - jodhpur.txt` | 3 | 0 |
| `joh - johore.txt` | 2 | 2 |
| `jun - junagadh.txt` | 3 | 0 |
| `kab - kabul.txt` | 3 | 0 |
| `kaf - kafiristan.txt` | 2 | 0 |
| `kal - kalat.txt` | 3 | 0 |
| `kan - kandahar.txt` | 1 | 0 |
| `kas - kashmir.txt` | 1 | 0 |
| `kat - kathiri.txt` | 1 | 0 |
| `kau - kaurna.txt` | 0 | 0 |
| `khi - khiva.txt` | 2 | 2 |
| `khp - kolhapur.txt` | 2 | 2 |
| `kno - kurnool.txt` | 1 | 1 |
| `kok - kokand.txt` | 2 | 2 |
| `kon - kongo.txt` | 1 | 1 |
| `kor - korea.txt` | 7 | 7 |
| `kot - kotah.txt` | 1 | 0 |
| `kra - krakow.txt` | 1 | 0 |
| `kti - kutai.txt` | 1 | 1 |
| `kun - kunduz.txt` | 1 | 0 |
| `kut - kutch.txt` | 2 | 0 |
| `kzh - kishi zhuz.txt` | 1 | 1 |
| `lad - ladakh.txt` | 2 | 0 |
| `lah - lahej.txt` | 1 | 1 |
| `lan - lanfang.txt` | 1 | 1 |
| `lib - liberia.txt` | 6 | 0 |
| `lip - lippe.txt` | 2 | 2 |
| `lua - luang prabang.txt` | 2 | 2 |
| `lub - lubeck.txt` | 1 | 1 |
| `luc - lucca.txt` | 2 | 2 |
| `mad - madagascar.txt` | 1 | 1 |
| `mah - mahra.txt` | 1 | 0 |
| `mai - maimana.txt` | 1 | 0 |
| `mas - mascara.txt` | 3 | 3 |
| `mbs - mombasa.txt` | 4 | 4 |
| `mec - mecklenburg.txt` | 2 | 2 |
| `mei - saxe-meiningen.txt` | 2 | 2 |
| `mew - mewar.txt` | 3 | 0 |
| `mex - mexico.txt` | 8 | 0 |
| `mgd - maguindanao.txt` | 2 | 2 |
| `mjt - majerteen.txt` | 1 | 1 |
| `mkt - miskito.txt` | 2 | 2 |
| `mld - maldives.txt` | 2 | 2 |
| `mnp - manipur.txt` | 2 | 0 |
| `mod - modena.txt` | 2 | 2 |
| `mol - moldavia.txt` | 1 | 1 |
| `mon - montenegro.txt` | 5 | 5 |
| `mor - morocco.txt` | 3 | 3 |
| `msn - massina.txt` | 4 | 4 |
| `mst - mecklenburg-strelitz.txt` | 2 | 2 |
| `mtb - matabele.txt` | 1 | 1 |
| `mug - hindustan.txt` | 4 | 4 |
| `myb - mayurbhanj.txt` | 2 | 0 |
| `mys - mysore.txt` | 1 | 1 |
| `nag - nagpur.txt` | 2 | 2 |
| `nar - narsinghpur.txt` | 2 | 0 |
| `nas - nassau.txt` | 2 | 2 |
| `naw - nawanagar.txt` | 2 | 0 |
| `nbs - new brunswick.txt` | 4 | 4 |
| `nej - nejd.txt` | 2 | 0 |
| `nep - nepal.txt` | 2 | 2 |
| `net - netherlands.txt` | 4 | 4 |
| `nor - norway.txt` | 9 | 0 |
| `nsw - new south wales.txt` | 7 | 0 |
| `nto - ngati toa.txt` | 1 | 1 |
| `nvs - nova scotia.txt` | 1 | 1 |
| `nzp - nimiipuu.txt` | 1 | 1 |
| `old - oldenburg.txt` | 2 | 2 |
| `oma - oman.txt` | 3 | 3 |
| `ont - ontario.txt` | 8 | 8 |
| `ora - oranje.txt` | 2 | 2 |
| `org - oregon.txt` | 7 | 0 |
| `ori - orissa.txt` | 2 | 0 |
| `ozh - orta zhuz.txt` | 1 | 1 |
| `pan - punjab.txt` | 10 | 10 |
| `pap - papacy.txt` | 5 | 5 |
| `par - parma.txt` | 2 | 2 |
| `pco - puerto rico.txt` | 1 | 1 |
| `peu - peru.txt` | 7 | 1 |
| `phi - philippines.txt` | 11 | 11 |
| `phl - philippolis.txt` | 4 | 4 |
| `plp - palanpur.txt` | 2 | 0 |
| `ply - tahiti.txt` | 1 | 1 |
| `pni - piratini.txt` | 2 | 0 |
| `pon - pontianak.txt` | 2 | 2 |
| `por - portugal.txt` | 12 | 12 |
| `pra - gao-para.txt` | 1 | 0 |
| `prg - paraguay.txt` | 8 | 0 |
| `prk - perak.txt` | 2 | 2 |
| `pru - prussia.txt` | 9 | 9 |
| `pta - patiala.txt` | 2 | 0 |
| `ptn - patna.txt` | 2 | 0 |
| `pud - pudukottai.txt` | 2 | 2 |
| `que - quebec.txt` | 6 | 6 |
| `qwr - qwara.txt` | 1 | 0 |
| `rus - russia.txt` | 12 | 12 |
| `ryu - ryukyu.txt` | 1 | 1 |
| `saf - south africa.txt` | 3 | 0 |
| `sak - siak.txt` | 2 | 2 |
| `sar - sardinia-piedmont.txt` | 9 | 9 |
| `sas - south australia.txt` | 6 | 0 |
| `sat - satara.txt` | 2 | 2 |
| `sax - saxony.txt` | 3 | 3 |
| `scm - schaumburg-lippe.txt` | 2 | 2 |
| `scw - schwarzburg.txt` | 1 | 1 |
| `sel - selangor.txt` | 2 | 2 |
| `seq - indian territory.txt` | 1 | 0 |
| `ser - serbia.txt` | 9 | 0 |
| `sgu - segou.txt` | 1 | 1 |
| `shw - shewa.txt` | 2 | 0 |
| `sia - siam.txt` | 2 | 2 |
| `sic - two sicilies.txt` | 5 | 5 |
| `sik - sikkim.txt` | 2 | 2 |
| `sil - sierra leone.txt` | 1 | 1 |
| `sin - sindh.txt` | 1 | 1 |
| `slw - sulawesi.txt` | 2 | 2 |
| `smb - sambas.txt` | 2 | 2 |
| `sml - seminole.txt` | 1 | 1 |
| `sok - sokoto.txt` | 3 | 3 |
| `spa - spain.txt` | 12 | 12 |
| `spc - carlist spain.txt` | 6 | 0 |
| `srk - surakarta.txt` | 2 | 2 |
| `stg - sintang.txt` | 2 | 2 |
| `sul - sulu.txt` | 2 | 2 |
| `sur - surguja.txt` | 2 | 0 |
| `swe - sweden.txt` | 11 | 11 |
| `swi - switzerland.txt` | 4 | 4 |
| `swz - swaziland.txt` | 2 | 2 |
| `tas - tasmania.txt` | 6 | 0 |
| `tex - texas.txt` | 6 | 0 |
| `tgi - tungi.txt` | 1 | 1 |
| `tgr - tigray.txt` | 1 | 0 |
| `tib - tibet.txt` | 1 | 1 |
| `tid - tidore.txt` | 2 | 2 |
| `tra - travancore.txt` | 2 | 2 |
| `tri - tripoli.txt` | 1 | 1 |
| `trn - transvaal.txt` | 2 | 2 |
| `trs - transylvania.txt` | 4 | 4 |
| `tug - touggourt.txt` | 2 | 2 |
| `tun - tunis.txt` | 2 | 2 |
| `tur - ottomans.txt` | 10 | 10 |
| `tus - tuscany.txt` | 2 | 2 |
| `ubd - baltic.txt` | 1 | 1 |
| `uca - central america.txt` | 1 | 0 |
| `uru - uruguay.txt` | 5 | 0 |
| `usa - america.txt` | 12 | 12 |
| `uzh - uly zhuz.txt` | 1 | 1 |
| `vnz - venezuela.txt` | 7 | 0 |
| `wad - wadai.txt` | 2 | 2 |
| `wal - wallachia.txt` | 1 | 1 |
| `was - western australia.txt` | 4 | 0 |
| `wbl - griqualand.txt` | 1 | 1 |
| `wei - saxe-weimar.txt` | 2 | 2 |
| `wld - waldeck.txt` | 2 | 2 |
| `wlg - welega.txt` | 1 | 0 |
| `wlt - wolaita.txt` | 1 | 0 |
| `wtu - witu.txt` | 3 | 3 |
| `wur - wurttemberg.txt` | 5 | 5 |
| `yog - yogyakarta.txt` | 2 | 2 |
| `zai - zaidi.txt` | 2 | 2 |
| `zul - zulu.txt` | 5 | 0 |

## 4. Fork character-history coverage

The thirteen retained fork files create 21 characters. Counts below are per character and role flags may overlap.

| File | Countries | Characters | Rulers | IG leaders | Generals | Admirals | Other | Uses vanilla-only template |
|---|---|---:|---:|---:|---:|---:|---:|---|
| `aus.txt` | AUS | 2 | 2 | 0 | 0 | 0 | 0 | NO |
| `bic - british india.txt` | BIC | 6 | 0 | 5 | 0 | 0 | 1 | NO |
| `dei - dutch east indies.txt` | DEI | 1 | 0 | 0 | 0 | 0 | 1 | NO |
| `dur.txt` | DUR | 1 | 1 | 0 | 0 | 0 | 0 | NO |
| `fra - france.txt` | FRA | 1 | 1 | 0 | 0 | 0 | 0 | NO |
| `gbr.txt` | GBR | 1 | 1 | 0 | 0 | 0 | 0 | NO |
| `ir1 - mamluk iraq.txt` | IR1 | 1 | 1 | 0 | 0 | 0 | 0 | NO |
| `per - persia.txt` | PER | 2 | 1 | 0 | 1 | 0 | 1 | NO |
| `plc - poland lithuania.txt` | PLC | 1 | 1 | 0 | 0 | 0 | 0 | NO |
| `rus.txt` | RUS | 2 | 1 | 0 | 0 | 0 | 1 | NO |
| `sic - naples sicily.txt` | SIC | 1 | 1 | 0 | 0 | 0 | 0 | NO |
| `spa.txt` | SPA | 1 | 1 | 0 | 0 | 0 | 0 | NO |
| `usa.txt` | USA | 1 | 1 | 1 | 0 | 0 | 0 | NO |
| **Total** | 13 tags | **21** | **12** | **6** | **1** | **0** | **4** | — |

The other 54 retained deterministic characters are instantiated from fork military-formation history, which is outside the replaced directory. The post-isolation deterministic total is therefore 21 + 54 = 75.

## 5. Template dependency analysis

Character templates are a separate VFS path and must remain merged:

| Template measure | Count |
|---|---:|
| Fork template files | 27 |
| Vanilla template files | 210 |
| Exact-name template overrides | 24 |
| Effective template files | 213 |

No retained start-history instance currently resolves to a vanilla-only template: 66 of the 75 retained instances are inline/no-template definitions and nine resolve to fork templates. This does not make vanilla templates disposable. Across fork scripts and events, 136 template identifiers are referenced; 60 resolve only from the retained vanilla template set. Examples include the Japanese imperial succession templates, later Brazilian and Balkan characters, Bismarck, late Ottoman rulers, Korean characters, and Iberian dynastic characters.

Additionally, 49 template IDs formerly instantiated by vanilla start history are referenced by effective scripts outside character-history definitions. Those references remain syntactically valid after isolation because their template definitions still exist. Checks such as `has_template` may no longer find a start instance, which is an expected functional consequence until appropriate 1776 characters or event paths are authored.

`DO_WE_NEED_REPLACE_PATH_CHARACTER_TEMPLATES = NO`.

## 6. Start-instance dependency analysis

The 259 removed vanilla files were scanned for saved scopes and variables, and their tokens were searched through the effective fork-plus-vanilla script VFS.

| Dependency | Source/start character family | Effective consumers | Would break after replace path | Severity / disposition |
|---|---|---|---|---|
| `scope:lavallette_gen` | vanilla USA history | none outside the removed history file | NO | NONE |
| `emperor_var` | vanilla JAP Emperor instance | guarded EP2 scripted effects/events; later setters exist | NO structural; initial Japan flavor reference becomes absent | MEDIUM, author with future 1776 Japan setup |
| `john_frost_var` | vanilla GBR history | fork historic-agitator events use guarded `has_variable` searches | NO | LOW; 1836 event correctly stays dormant |
| `mazzini_var` | vanilla SAR history | guarded character interaction/event searches | NO | LOW; 1836 event correctly stays dormant |
| `ranavalona` | vanilla Madagascar history | vanilla decision condition | NO | LOW; unavailable until a suitable ruler exists |
| `ismail_var`, `hawduqo_var` | vanilla Circassian rulers | guarded Russian scripted-button conditions | NO | LOW; no invalid scope |
| `sikh_maharaja_enthroned` | vanilla Punjab ruler | fork on-action has absence check and self-initialization | NO | LOW; Punjab history must be rebuilt later |
| `colonial_governor_term` | vanilla colonial governors | guarded cycle plus fallback initialization | NO | LOW |
| `regency_years` | vanilla regents | guarded checks plus fallback initialization | NO | LOW |
| `is_married` | several vanilla rulers/heirs | generic marriage eligibility checks; also supplied by templates | NO | LOW |
| `cardinal_var` | vanilla Spain history | later fork event setter only | NO | NONE |
| 49 externally referenced removed-instance template IDs | multiple 1836 characters | `has_template`, effects, JEs and events | NO parser break; some content remains dormant | MEDIUM functional backlog |

No removed stable scope is consumed elsewhere. No unguarded direct character-instance identifier was found. The known effects are missing/dormant historical content, not parse failures, invalid scopes, or country-setup crashes. Such gaps are expected when a 1836 setup is removed and will be addressed only in later historical reconstruction batches.

`KNOWN_BREAKING_DEPENDENCIES = 0` at structural/parser level. Guarded functional dependencies are explicitly recorded above and require the user runtime check.

## 7. Replace-path options

| Option | Correctness | Maintainability | Risk / DLC compatibility | Future rework impact | Verdict |
|---|---|---|---|---|---|
| A — `replace_path = "common/history/characters"` | Removes the wrong start-history layer at its source | One declarative line | Requires authoring 1776 rulers; templates/events/DLC definitions remain available | Clean baseline for future history work | **SELECTED** |
| B — create fork files for all 262 vanilla basenames | Can shadow today's files | Very poor; hundreds of empty/neutralizing files | New vanilla/DLC filenames can leak back in; easy to miss updates | Large permanent maintenance burden | REJECT |
| C — more targeted VFS mechanism | No valid directory-exclusion mechanism more targeted than filename overrides was found in the local 1.13 setup | N/A | Would reduce risk only if supported | No demonstrated implementation | NOT AVAILABLE |
| D — retain vanilla and repair/delete 536 instances individually | Does not fix the loading architecture | Worst; every upstream character remains a liability | High duplication and update risk | Pollutes all later historical work | REJECT |

## 8. Selected strategy

Option A is the only strategy that removes the proven root cause without touching templates or maintaining 262 shadow files. It intentionally converts inherited rulers into explicit reconstruction gaps.

The active `content_load.json` points directly to the repository directory. The repository-root `descriptor.mod` is therefore the payload/runtime descriptor for this local mod. The sibling launcher descriptor contains only the path/metadata pointer and was not edited.

## 9. Descriptor change

Exactly one VFS/game-loading line was added to `descriptor.mod`, after `supported_version`:

```text
replace_path = "common/history/characters"
```

No character-history file, template, date, ruler, event, formation, technology, external launcher descriptor, or other gameplay file was modified.

## 10. Before / after static inventory

| Measure | Before | After static isolation | Delta |
|---|---:|---:|---:|
| Effective character-history files | 272 | 13 | -259 |
| Deterministic start characters | 611 | 75 | -536 |
| Vanilla-sourced start characters | 536 | 0 | -536 |
| Fork character-history characters | 21 | 21 | 0 |
| Fork military-formation characters | 54 | 54 | 0 |
| Negative ages | 285 | 0 | -285 |
| Born after start | 285 | 0 | -285 |
| Scripted ruler instances | 172 | 12 | -160 |
| Countries with duplicate scripted rulers | 2 | 1 (`AUS`) | -1 |
| Unresolved ruler slots | 205 | 364 | +159 |
| Audit CSV rows including unresolved slots | 816 | 439 | -377 |

The post-isolation CSV contains 75 retained deterministic instances plus 364 unresolved country-ruler slots. It does not classify a retained formation character as vanilla inheritance merely because a reusable vanilla template might still exist; provenance is based on the start-instantiation file.

Static zero negative ages does not prove that all 75 retained characters are historically correct. It only proves that all 285 automatically impossible dates found in CLEANUP-2A came from the isolated vanilla character-history layer.

## 11. Major-country effect

| Country | Before | After simulated | Expected result |
|---|---|---|---|
| `CHI` | 20 deterministic characters; Daoguang ruler | 10 formation-history commanders; no scripted ruler | Daoguang removed; Qianlong remains to be authored later |
| `TUR` | 12 characters; Mahmud II ruler | 2 formation-history generals; no scripted ruler | Mahmud II removed; Abdülhamid I remains to be authored later |
| `POR` | 12 characters; Maria II ruler | no deterministic character; no scripted ruler | Maria II removed; José I remains to be authored later |
| `PRU` | 12 characters; later Friedrich Wilhelm ruler | 3 formation-history generals; no scripted ruler | wrong ruler removed; Frederick II remains to be authored later |
| `SWE` | 11 characters; Bernadotte ruler | no deterministic character; no scripted ruler | Bernadotte removed; Gustav III remains to be authored later |
| `JAP` | 21 characters; Ienari ruler | no deterministic character; no scripted ruler | 1836 shogunate court removed; Ieharu and the 1776 imperial representation remain to be authored |
| `MUG` | 4 characters; Akbar II ruler | no deterministic character; no scripted ruler | Akbar II removed; Shah Alam II/effective-power model remains to be authored |
| `SIC` | 6 characters; fork Ferdinand IV/III plus vanilla Ferdinand II | one fork character: Ferdinand IV/III ruler | inherited duplicate removed; correct fork identity retained |
| `AUS` | 15 characters; fork Maria Theresa and Joseph II plus vanilla secondaries | two fork rulers: Maria Theresa and Joseph II | vanilla secondaries removed; fork co-regency remains, including its known date issues |

No ruler was created or corrected in CLEANUP-2B-0.

## 12. Remaining 1776 ruler gaps

After isolation, twelve scripted ruler instances remain across eleven country tags:

`AUS, DUR, FRA, GBR, IR1, PER, PLC, RUS, SIC, SPA, USA`.

With 375 state-owning country tags in the CLEANUP-2A map inventory, 364 ruler slots have no surviving deterministic `ruler = yes` character. That is the correct reconstruction backlog, not a structural failure. `AUS` remains the sole multi-ruler country because the fork deliberately scripts both Maria Theresa and Joseph II; its historical/game-model decision and dates belong to a later phase.

## 13. Runtime plan for USER

Codex did not launch Victoria 3. The user should perform one condensed session:

1. Confirm the game reaches the menu with only the fork enabled.
2. Start a new 1776 campaign and confirm country selection does not crash.
3. Inspect `GBR`, `FRA`, `RUS`, `CHI`, `TUR`, `POR`, `PRU`, `SWE`, `JAP`, `MUG`, `AUS`, and `SIC`.
4. Record displayed ruler, age, and whether the ruler is absent or engine-generated.
5. Confirm the removed cases—Daoguang, Mahmud II, Maria II, Bernadotte, Ienari, Akbar II, later Friedrich Wilhelm, and Ferdinand II—do not reappear from vanilla history.
6. Confirm no obvious negative age remains among the inspected rulers/characters.
7. Advance several days and observe immediate events/on-actions.
8. Save and reload once in the same session if practical.
9. Inspect `error.log`, `game.log`, `setup.log`, and `script_system.log` for descriptor parsing, invalid character scopes, or mass errors.

A missing or generic ruler is an expected reconstruction gap. Structural failure means crash, descriptor parse failure, country setup failure, mass invalid-scope errors, or unrelated systems disappearing.

## 14. Protected-state verification

Final static validation confirms:

- CLEANUP-2A report and CSV remain present and unchanged;
- the only VFS/game-loading modification is one line in `descriptor.mod`;
- no character gameplay file was modified;
- no external launcher descriptor was modified;
- no file is staged;
- `git diff --check` passes;
- all seven protected technology research files remain untracked, unstaged, and byte-identical to their CLEANUP-2A hashes;
- the accidental path `bject` is absent;
- BIC retains `activate_law = law_type:law_frontier_colonization` and does not contain `law_colonial_exploitation`;
- Victoria 3 was not launched by Codex.

## 15. Final verdict

Static validation passes. The descriptor isolation is structurally justified and safe for the user's runtime test. Historical ruler reconstruction must wait for runtime confirmation; CLEANUP-2B-0 did not begin any individual correction.

```text
STRUCTURAL_ROOT_CAUSE_CONFIRMED = YES
REPLACE_PATH_HISTORY_SAFE = YES
REPLACE_PATH_TEMPLATES_REQUIRED = NO
DESCRIPTOR_REPLACE_PATH_ADDED = YES

VANILLA_1836_START_CHARACTERS_BEFORE = 536
VANILLA_1836_START_CHARACTERS_AFTER = 0

NEGATIVE_AGE_BEFORE = 285
NEGATIVE_AGE_AFTER_STATIC = 0

BORN_AFTER_START_BEFORE = 285
BORN_AFTER_START_AFTER_STATIC = 0

SCRIPTED_RULERS_AFTER_ISOLATION = 12
UNRESOLVED_RULER_SLOTS_AFTER_ISOLATION = 364

GAMEPLAY_CHARACTER_FILES_MODIFIED = NO
CODEX_LAUNCHED_VICTORIA3 = NO
USER_RUNTIME_REQUIRED = YES

V13_STATIC_VALIDATION = PASS
SAFE_FOR_USER_RUNTIME = YES
SAFE_TO_BEGIN_HISTORICAL_RULER_RECONSTRUCTION = NO
```
