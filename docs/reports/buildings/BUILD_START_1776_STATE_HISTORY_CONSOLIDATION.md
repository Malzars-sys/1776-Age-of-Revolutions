# 1776 state building-history consolidation

The 21 September 2026 runtime exposed a structural flaw: generated `97*`,
`98*`, and `99*` building-history files added a second `s:STATE_*` definition
for states already present in the regional files. The static building tally had
treated all definitions as additive, but that did not establish how the game
would load the repeated state configurations.

The generated building placements have been folded into the existing
`00_west_europe.txt` through `15_russia.txt` regional files. Five states that
appeared only in the generated overlay were placed in their corresponding
regional file. The seven generated overlay files were removed. The older
duplicate definitions of `STATE_BREST` and `STATE_JETISY` were also joined.

Mechanical before/after verification preserved all **2,597** `create_building`
placements, including building ID, level, owner, active production methods and
body content. The result has **674** distinct `s:STATE_*` blocks, with no
repeated state block or `region_state:*` owner block. The final target validator
still reports zero building target mismatches, missing rows and extra rows;
protected military/naval and Serenissima changes remain zero. The validator
now fails if state or owner blocks are duplicated again.

## Game log checked

The latest `error.log` available for this review was written on 21 September
2026 at 20:17, before consolidation. It contains 16 `state.cpp` reports of
unsupported or over-capacity buildings: Mysore millet farm; Maharashtra salt
works; Taiwan sugar plantation; Shandong salt works; Ruuchuu logging camp;
Shikoku whaling station; Yeongnam salt works; Sambas and Pontianak gold mines;
Qurum salt works; Kursk, Kokand Syr-Daria, Tambov and Riazan wheat farms; Perm
salt mine; and Aleksandrovsk salt works. These log entries identify a separate
resource/building compatibility issue; moving the same placements into unique
state blocks does not by itself establish that the game will accept them.

A fresh game start is required to confirm the runtime effect of consolidation
and to produce a new error log. The older log is not evidence that the corrected
file topology has already been loaded by the game.
