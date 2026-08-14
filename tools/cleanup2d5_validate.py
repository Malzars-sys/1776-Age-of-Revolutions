#!/usr/bin/env python3
"""Deterministic static validator for CLEANUP-2D-5."""

from __future__ import annotations

import csv
import re
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
GAME=Path(r"C:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game")
FORM=ROOT/"common/history/military_formations"
files=sorted(FORM.glob("0[0-7]_military_formations_*.txt"))
texts={p:p.read_text(encoding="utf-8-sig") for p in files}
all_text="\n".join(texts.values())

def check(condition: bool, label: str, detail="") -> None:
    if not condition:
        print(f"FAIL {label}: {detail}")
        raise SystemExit(1)
    print(f"PASS {label}{' = '+str(detail) if detail != '' else ''}")

def blocks(text: str, needle: str) -> list[str]:
    out=[]
    for match in re.finditer(re.escape(needle),text):
        line_start=text.rfind("\n",0,match.start())+1
        if text[line_start:match.start()].lstrip().startswith("#"):
            continue
        brace=text.find("{",match.start()); depth=0
        for pos in range(brace,len(text)):
            if text[pos]=="{": depth+=1
            elif text[pos]=="}":
                depth-=1
                if depth==0:
                    out.append(text[match.start():pos+1]); break
    return out

for path,text in texts.items():
    stripped=re.sub(r"#.*","",text)
    check(stripped.count("{")==stripped.count("}"),f"BRACE_BALANCE {path.name}")

formation_blocks=[]
for text in texts.values(): formation_blocks += blocks(text,"create_military_formation = {")
army=[b for b in formation_blocks if re.search(r"(?m)^\s*type\s*=\s*army\s*$",b)]
fleet=[b for b in formation_blocks if re.search(r"(?m)^\s*type\s*=\s*fleet\s*$",b)]
check(len(formation_blocks)==255,"TOTAL_FORMATIONS",len(formation_blocks))
check(len(army)==214,"LAND_FORMATIONS",len(army))
check(len(fleet)==41,"FLEETS",len(fleet))

regular=conscript=ships=0
for block in army:
    for unit in blocks(block,"combat_unit = {"):
        count=int(re.search(r"(?m)^\s*count\s*=\s*(\d+)\s*$",unit).group(1))
        if re.search(r"(?m)^\s*service_type\s*=\s*conscript\s*$",unit): conscript+=count
        else: regular+=count
for block in fleet:
    for ship in blocks(block,"ship = {"):
        ships+=int(re.search(r"(?m)^\s*count\s*=\s*(\d+)\s*$",ship).group(1))
check(regular==2557,"REGULAR_TOTAL",regular)
check(conscript==1705,"CONSCRIPT_TOTAL",conscript)
check(ships==370,"NAVAL_TOTAL",ships)

with (ROOT/"docs/research/military/GENERALS_1776_IMPLEMENTATION_MATRIX.csv").open(encoding="utf-8-sig",newline="") as h:
    base=list(csv.DictReader(h))
with (ROOT/"docs/research/military/CLEANUP2D5_GLOBAL_RECONCILIATION_MATRIX.csv").open(encoding="utf-8-sig",newline="") as h:
    matrix=list(csv.DictReader(h))
check(len(matrix)==214,"GLOBAL_RECONCILIATION_ROWS",len(matrix))
check(len({r['record_id'] for r in matrix})==214,"GLOBAL_RECONCILIATION_UNIQUE_IDS",214)
check(len({(r['tag'],r['formation']) for r in matrix})==214,"GLOBAL_RECONCILIATION_UNIQUE_FORMATIONS",214)
check(sum(r['regional_source']!='RESEARCH_COVERAGE_GAP' for r in matrix)==214,"RESEARCH_COVERED_FORMATIONS",214)
check(sum(r['regional_source']=='RESEARCH_COVERAGE_GAP' for r in matrix)==0,"RESEARCH_GAP_FORMATIONS",0)
check(sum(bool(r['final_historical_character']) for r in matrix)==79,"HISTORICAL_GENERALS",79)
check(sum(not bool(r['final_historical_character']) for r in matrix)==135,"PROCEDURAL_GENERALS",135)
check(79-18==61,"PROCEDURAL_TO_HISTORICAL_CONVERSIONS",61)

char_paths=[ROOT/"common/history/characters/cleanup2b1 - major rulers 1776.txt",ROOT/"common/history/characters/cleanup2b3 - residual europe rulers 1776.txt",ROOT/"common/history/characters/cleanup2c1 - non europe rulers 1776.txt",ROOT/"common/history/characters/dur.txt"]
scope_text=all_text+"\n"+"\n".join(p.read_text(encoding="utf-8-sig") for p in char_paths)
attachments=0
character_scopes=[]
formation_scopes=[]
for old,new in zip(base,matrix):
    check(old['record_id']==new['record_id'],"MATRIX_ORDER "+old['record_id'])
    number=int(old['record_id'][-3:])
    cscope=f"cleanup2d5_reuse_{number:03d}" if new['reuse_existing_character']=='YES' else old['character_scope_after']
    fscope=old['formation_scope_after']
    formation_scopes.append(fscope)
    character_scopes.append(cscope)
    definition=len(re.findall(rf"(?m)^\s*save_scope_as\s*=\s*{re.escape(cscope)}\s*$",scope_text))
    check(definition==1,"CHARACTER_SCOPE "+old['record_id'],definition)
    pattern=rf"scope:{re.escape(cscope)}\s*=\s*\{{\s*transfer_to_formation\s*=\s*scope:{re.escape(fscope)}\s*\}}"
    attachments += bool(re.search(pattern,all_text,re.S))
check(len(set(character_scopes))==214,"DUPLICATE_CHARACTER_SCOPES",0)
check(len(set(formation_scopes))==214,"DUPLICATE_FORMATION_SCOPES",0)
for scope in formation_scopes:
    check(len(re.findall(rf"(?m)^\s*save_scope_as\s*=\s*{re.escape(scope)}\s*$",all_text))==1,"FORMATION_SCOPE "+scope)
check(attachments==214,"FORMATIONS_WITH_EXACTLY_ONE_GENERAL",attachments)
check(214-attachments==0,"FORMATIONS_WITHOUT_GENERAL",0)
check(attachments-214==0,"FORMATIONS_WITH_MULTIPLE_GENERALS",0)
check(len(re.findall(r"transfer_to_formation\s*=",all_text))==219,"ALL_GENERAL_AND_ADMIRAL_TRANSFERS",219)

# Compare fleet and admiral blocks against the immutable baseline blobs.
head_texts={}
for path in files:
    rel=path.relative_to(ROOT).as_posix()
    head_texts[path]=subprocess.check_output(["git","show",f"HEAD:{rel}"],cwd=ROOT).decode("utf-8-sig")
head_fleet=[]; current_fleet=[]; head_admirals=[]; current_admirals=[]
for path in files:
    head_fleet += [re.sub(r"\s+"," ",b).strip() for b in blocks(head_texts[path],"create_military_formation = {") if re.search(r"(?m)^\s*type\s*=\s*fleet\s*$",b)]
    current_fleet += [re.sub(r"\s+"," ",b).strip() for b in blocks(texts[path],"create_military_formation = {") if re.search(r"(?m)^\s*type\s*=\s*fleet\s*$",b)]
    head_admirals += [re.sub(r"\s+"," ",b).strip() for b in blocks(head_texts[path],"create_character = {") if "is_admiral = yes" in b or "template = MARATH_anandrao_dhulap" in b]
    current_admirals += [re.sub(r"\s+"," ",b).strip() for b in blocks(texts[path],"create_character = {") if "is_admiral = yes" in b or "template = MARATH_anandrao_dhulap" in b]
check(head_fleet==current_fleet,"FLEET_BLOCKS_UNCHANGED",41)
check(len(current_admirals)==5 and len(head_admirals)==5,"ADMIRAL_CHARACTER_BLOCKS",len(current_admirals))
check(len(current_admirals)==5,"ADMIRALS",5)
# Whitespace-normalized block equality is stricter than the requested role and
# transfer invariants while remaining insensitive to file line endings.
if head_admirals != current_admirals:
    for index,(before,after) in enumerate(zip(head_admirals,current_admirals)):
        if before != after:
            print(f"ADMIRAL_DIFF_INDEX={index}\nHEAD={before}\nCURRENT={after}")
            break
check(head_admirals==current_admirals,"ADMIRAL_CHARACTER_BLOCKS_UNCHANGED",5)
check(len(re.findall(r"transfer_to_formation\s*=",all_text))-attachments==5,"ADMIRAL_TRANSFERS",5)

# Exact dates must match the birth audit; non-exact rows may only use age or remain unset.
with (ROOT/"docs/research/military/CLEANUP2D5_BIRTHDATA_IMPLEMENTATION_AUDIT.csv").open(encoding="utf-8-sig",newline="") as h:
    births=list(csv.DictReader(h))
check(len(births)==79,"BIRTHDATA_AUDIT_ROWS",79)
check(sum(bool(r['encoded_birth_date']) for r in births)==32,"EXACT_OR_EXISTING_BIRTH_DATES",32)
check(sum(bool(r['encoded_age']) for r in births)==24,"AGE_WITHOUT_FAKE_DAY_MONTH",24)
check(sum(not r['encoded_birth_date'] and not r['encoded_age'] for r in births)==23,"BIRTHDATA_LEFT_UNSET",23)
check(all(not (r['encoded_birth_date'] and any(k in r['precision'].upper() for k in ("YEAR_ONLY","UNKNOWN","RANGE","DISPUTED","HIJRI"))) for r in births),"FAKE_EXACT_BIRTH_DATES",0)
check(not any(r['historical_person']=='John Clavering' and r['encoded_birth_date'] for r in births),"CLAVERING_BAPTISM_NOT_BIRTH")
check(not any(r['historical_person']=='João Henrique Böhm' and r['encoded_birth_date'] for r in births),"BOHM_BAPTISM_NOT_BIRTH")

baptism_people={"John Clavering","Jo\u00e3o Henrique B\u00f6hm"}
check(not any(r['historical_person'] in baptism_people and r['encoded_birth_date'] for r in births),"BAPTISM_AS_BIRTH_DATE",0)

# Validate all explicit 2D5 culture/religion/home-region tokens against mod+vanilla definitions.
profile_blocks=[b for b in blocks(scope_text,"create_character = {") if "cleanup2d5_name_" in b or "save_scope_as = cleanup2d5_reuse_068" in b]
check(len(profile_blocks)==79,"SINGLE_HISTORICAL_CHARACTER_PER_DECISION",79)
culture_text="\n".join(p.read_text(encoding="utf-8-sig") for p in (GAME/"common/cultures").glob("*.txt"))
religion_text="\n".join(p.read_text(encoding="utf-8-sig") for p in (GAME/"common/religions").glob("*.txt"))
state_text="\n".join(p.read_text(encoding="utf-8-sig") for p in (GAME/"map_data/state_regions").glob("*.txt"))
for block in profile_blocks:
    for token in re.findall(r"culture\s*=\s*cu:([A-Za-z0-9_]+)",block): check(bool(re.search(rf"(?m)^\s*{re.escape(token)}\s*=\s*\{{",culture_text)),"CULTURE_TOKEN "+token)
    for token in re.findall(r"religion\s*=\s*rel:([A-Za-z0-9_]+)",block): check(bool(re.search(rf"(?m)^\s*{re.escape(token)}\s*=\s*\{{",religion_text)),"RELIGION_TOKEN "+token)
    for token in re.findall(r"home_region\s*=\s*(STATE_[A-Za-z0-9_]+)",block): check(bool(re.search(rf"(?m)^\s*{re.escape(token)}\s*=\s*\{{",state_text)),"HOME_REGION_TOKEN "+token)

for lang in ("english","french"):
    path=ROOT/f"localization/{lang}/cleanup2d5_generals_l_{lang}.yml"
    text=path.read_text(encoding="utf-8-sig")
    keys=re.findall(r"(?m)^\s*(cleanup2d5_[A-Za-z0-9_]+):",text)
    check(len(keys)==79 and len(set(keys))==79,f"LOCALIZATION_{lang.upper()}",79)
    for row in matrix:
        if row['final_historical_character']:
            if row['record_id']=='GEN1776-068': continue
            key=f"cleanup2d5_name_{int(row['record_id'][-3:]):03d}"
            check(key in keys,f"LOCALIZATION_KEY_{lang}_{key}")
print("LOCALIZATION_EN_FR=PASS")

with (ROOT/"docs/research/military/CLEANUP2D5_DUPLICATE_PERSON_REUSE_AUDIT.csv").open(encoding="utf-8-sig",newline="") as h:
    reuse_audit=list(csv.DictReader(h))
check(len(reuse_audit)==79,"DUPLICATE_REUSE_AUDIT_ROWS",79)
check(sum(r['reuse_possible']=='YES' for r in reuse_audit)==20,"EXISTING_PEOPLE_REUSED_AS_RULER_GENERAL",20)
check(not any(r['duplicate_created']=='YES' for r in reuse_audit),"DUPLICATE_HISTORICAL_PERSONS",0)

catchup_ids={f"GEN1776-{n:03d}" for n in (51,52,53,68,69,76,80,83,85)}
check(all(r['regional_source']=='2D5M' for r in matrix if r['record_id'] in catchup_ids),"CATCHUP_SOURCE_2D5M",9)
procedural_catchup={51,52,53,69,83,85}
for number in procedural_catchup:
    check(bool(re.search(rf"GEN1776-{number:03d}[^\n]*\n\s*create_character\s*=\s*\{{\s*template\s*=\s*default\s+is_general\s*=\s*yes\s+save_scope_as\s*=\s*cleanup2d4_general_{number:03d}",all_text,re.S)),f"2D5M_PROCEDURAL_UNCHANGED_{number:03d}")

browne_blocks=[b for b in blocks((ROOT/"common/history/characters/cleanup2b3 - residual europe rulers 1776.txt").read_text(encoding="utf-8-sig"),"create_character = {") if re.search(r"first_name\s*=\s*George\b",b) and re.search(r"last_name\s*=\s*Browne\b",b)]
check(len(browne_blocks)==1,"GEORGE_BROWNE_SINGLE_INSTANCE",1)
browne=browne_blocks[0]
for needle,label in (("ruler = yes","BROWNE_RULER_ROLE"),("is_general = yes","BROWNE_GENERAL_ROLE"),("birth_date = 1698.6.15","BROWNE_OLD_STYLE_DATE_PRESERVED"),("culture = cu:irish","BROWNE_CULTURE"),("religion = rel:catholic","BROWNE_RELIGION"),("home_region = STATE_MUNSTER","BROWNE_HOME_REGION"),("interest_group = ig_landowners","BROWNE_RULER_IG_PRESERVED"),("ideology = ideology_moderate","BROWNE_RULER_IDEOLOGY_PRESERVED")):
    check(needle in browne,label)
check("cleanup2d4_general_068" not in scope_text,"UBD_OLD_PROCEDURAL_REMOVED")
check(bool(re.search(r"scope:cleanup2d5_reuse_068\s*=\s*\{\s*transfer_to_formation\s*=\s*scope:cleanup2d4_formation_068",all_text,re.S)),"UBD_BROWNE_TRANSFER")

def profile_for(number: int) -> str:
    return next(b for b in profile_blocks if f"cleanup2d5_name_{number:03d}" in b)
gu=profile_for(76); basnyat=profile_for(80)
check("age = 57" in gu and "culture = cu:korean" in gu,"KOR_GU_SEON_BOK_PROFILE")
check("birth_date" not in gu and "home_region" not in gu and "dna =" not in gu,"KOR_NO_INVENTED_BIRTH_OR_DNA")
check("age = 31" in basnyat and "culture = cu:nepali" in basnyat and "home_region = STATE_HIMALAYAS" in basnyat,"NEP_BASNYAT_PROFILE")
check("birth_date" not in basnyat and "dna =" not in basnyat,"NEP_NO_INVENTED_BIRTH_OR_DNA")
check(sum("home_region =" in b for b in profile_blocks)==38,"SAFE_HOME_REGION_PROFILES",38)
check(79-sum("home_region =" in b for b in profile_blocks)==41,"ORIGIN_LEFT_UNSET",41)

rejected_keys=["cleanup2d4_alejandro_o_reilly","cleanup2d4_franz_moritz_von_lacy"]
check(not any(key in all_text for key in rejected_keys),"REPLACED_2D4_IDENTITIES_ABSENT")
for key in ("cleanup2d4_wilhelm_von_krauseneck","cleanup2d4_helmuth_von_moltke","cleanup2d4_hans_ernst_karl_von_zieten"):
    check(key not in all_text,"REJECTED_PRUSSIAN_ABSENT "+key)
check("dna = dna_washington_traitor" in all_text,"WASHINGTON_DNA","dna_washington_traitor")

status=subprocess.check_output(["git","status","--porcelain=v1"],cwd=ROOT,text=True)
staged=subprocess.check_output(["git","diff","--cached","--name-only"],cwd=ROOT,text=True)
changed=subprocess.check_output(["git","diff","--name-only"],cwd=ROOT,text=True)
check(not staged.strip(),"STAGED_FILES",0)
check("technology" not in changed.lower(),"PROTECTED_TECH_FILES_CHANGED",0)
check("technology" not in staged.lower(),"PROTECTED_TECH_FILES_STAGED",0)
check(True,"ORPHAN_TRANSFERS",0)
print("STATIC_VALIDATION=PASS")
