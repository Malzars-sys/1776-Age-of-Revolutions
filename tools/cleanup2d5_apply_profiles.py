#!/usr/bin/env python3
"""Apply the reconciled CLEANUP-2D-5 character profiles.

This is a deterministic bulk rewrite limited to general creation/attachment
blocks, the exact existing ruler records selected for reuse, and dedicated
EN/FR localization.
"""

from __future__ import annotations

import csv
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs/research/military/CLEANUP2D5_GLOBAL_RECONCILIATION_MATRIX.csv"
BASE = ROOT / "docs/research/military/GENERALS_1776_IMPLEMENTATION_MATRIX.csv"
FORMATIONS = ROOT / "common/history/military_formations"

with MATRIX.open(encoding="utf-8-sig", newline="") as handle:
    matrix = {r["record_id"]: r for r in csv.DictReader(handle)}
with BASE.open(encoding="utf-8-sig", newline="") as handle:
    baseline = {r["record_id"]: r for r in csv.DictReader(handle)}

names = {int(rid[-3:]): row["final_historical_character"] for rid, row in matrix.items() if row["final_historical_character"]}


def profile(culture="", religion="", home="", birth="", age=""):
    return {"culture":culture,"religion":religion,"home":home,"birth":birth,"age":age}


P = {
2:profile("polish","catholic","STATE_WEST_GALICIA",age="45"),3:profile("north_german","protestant","STATE_BRANDENBURG","1709.4.10"),4:profile("north_german","protestant","STATE_POMERANIA","1719.6.2"),5:profile("north_german","protestant","STATE_BRANDENBURG","1724.1.7"),6:profile("north_german","","STATE_POMERANIA","1710.4.18"),
9:profile("hungarian","catholic","STATE_SLOVAKIA","1734.10.2"),10:profile("croat","catholic","STATE_CENTRAL_HUNGARY","1719.7.2"),11:profile("hungarian","catholic","STATE_SLOVAKIA","1710.10.16"),12:profile("north_italian","catholic","STATE_LOMBARDY",age="79"),
15:profile("french","catholic","STATE_FRANCHE_COMTE","1707.4.15"),16:profile("french","catholic",birth="1704.10.11"),17:profile("french","catholic","STATE_ILE_DE_FRANCE","1696.3.13"),18:profile("french","catholic"),19:profile("british","protestant",birth="1729.8.10"),20:profile("british","protestant","STATE_HOME_COUNTIES","1717.1.29"),21:profile("scottish","protestant","STATE_LOWLANDS","1717.12.25"),
24:profile("russian","orthodox","STATE_SMOLENSK","1739.10.11"),27:profile("russian","orthodox","STATE_MOSCOW","1725.1.15"),28:profile(),33:profile("north_german","protestant","STATE_SCHLESWIG_HOLSTEIN","1709.7.9"),38:profile("north_german","protestant",birth="1698.8.28"),47:profile("swedish","protestant","STATE_UUSIMAA","1740.8.16"),
62:profile("north_german","protestant","STATE_BRUNSWICK","1718.9.25"),63:profile("french","catholic","STATE_ALSACE_LORRAINE","1726.4.20"),64:profile("portuguese","catholic","STATE_AZORES",age="82"),65:profile("spanish","catholic","STATE_ARAGON","1727.9.12"),66:profile("irish","catholic","STATE_ULSTER","1720.11.1"),67:profile("spanish","catholic","STATE_EXTREMADURA","1726.3.6"),
70:profile("uzbek","sunni"),74:profile("uzbek","sunni"),81:profile("kirgiz","sunni"),87:profile("dixie","protestant","STATE_VIRGINIA","1732.2.22"),88:profile("french","catholic","STATE_ILE_DE_FRANCE","1732.3.24"),89:profile("spanish","catholic","STATE_ARAGON",age="50"),90:profile("spanish","catholic","STATE_EXTREMADURA"),92:profile("miskito"),
93:profile("north_german","protestant","STATE_ELBE",age="67"),95:profile("spanish","catholic","STATE_LEON"),96:profile("spanish","catholic",birth="1708.5.23"),100:profile("maghrebi","sunni"),102:profile("turkish","sunni","STATE_AYDIN",age="50"),104:profile("maghrebi","sunni"),
106:profile("north_caucasian","sunni"),112:profile("","shiite"),113:profile("pashtun","sunni","STATE_KHORASAN",age="29"),116:profile("bedouin","sunni",age="21"),
118:profile("panjabi","sikh","STATE_PUNJAB","1718.5.3"),120:profile("british","protestant",age="37"),121:profile("scottish","protestant"),122:profile("british","protestant",age="53"),125:profile("marathi","hindu",age="46"),126:profile("marathi","hindu"),127:profile("marathi","hindu",age="48"),128:profile("marathi","hindu"),129:profile("deccani","sunni","STATE_MYSORE",age="53"),130:profile("deccani","sunni","STATE_MYSORE","1750.11.20"),140:profile("flemish","catholic",age="60"),142:profile("persian","shiite",age="52"),
143:profile("manchu"),144:profile("manchu",birth="1717.9.7"),145:profile("manchu"),146:profile("manchu",age="39"),147:profile("mongol"),148:profile("manchu",age="47"),149:profile("manchu"),150:profile("manchu",age="29"),152:profile("burmese","theravada",age="55"),153:profile("basque","catholic",birth="1709.10.28"),155:profile("japanese",age="43"),166:profile("malay","sunni","STATE_MALAYA",age="49"),175:profile("thai","theravada","STATE_BANGKOK","1737.3.20"),
194:profile("amhara","orthodox"),195:profile("fulbe","sunni"),202:profile("bambara","animist"),209:profile("bambara","animist",age="57"),210:profile("nguni","animist"),
}
P.update({
    68:profile("irish","catholic","STATE_MUNSTER","1698.6.15"),
    76:profile("korean",age="57"),
    80:profile("nepali",home="STATE_HIMALAYAS",age="31"),
})

reuse = {
68:("common/history/characters/cleanup2b3 - residual europe rulers 1776.txt","George"),
70:("common/history/characters/cleanup2c1 - non europe rulers 1776.txt","CLEANUP2C1_NAME_BUK"),74:("common/history/characters/cleanup2c1 - non europe rulers 1776.txt","CLEANUP2C1_NAME_KHI"),81:("common/history/characters/cleanup2c1 - non europe rulers 1776.txt","CLEANUP2C1_NAME_OZH"),
88:("common/history/characters/cleanup2c1 - non europe rulers 1776.txt","CLEANUP2C1_NAME_HAI"),89:("common/history/characters/cleanup2c1 - non europe rulers 1776.txt","CLEANUP2C1_NAME_CUB"),90:("common/history/characters/cleanup2c1 - non europe rulers 1776.txt","CLEANUP2C1_NAME_PCO"),96:("common/history/characters/cleanup2c1 - non europe rulers 1776.txt","CLEANUP2C1_NAME_SC2"),102:("common/history/characters/cleanup2c1 - non europe rulers 1776.txt","CLEANUP2C1_NAME_CON"),
113:("common/history/characters/dur.txt","CLEANUP2C1_NAME_DUR"),116:("common/history/characters/cleanup2c1 - non europe rulers 1776.txt","CLEANUP2C1_NAME_HDJ"),118:("common/history/characters/cleanup2c1 - non europe rulers 1776.txt","CLEANUP2C1_NAME_PAN"),127:("common/history/characters/cleanup2c1 - non europe rulers 1776.txt","CLEANUP2C1_NAME_GWA"),128:("common/history/characters/cleanup2c1 - non europe rulers 1776.txt","CLEANUP2C1_NAME_NAG"),129:("common/history/characters/cleanup2b1 - major rulers 1776.txt","Hyder"),153:("common/history/characters/cleanup2c1 - non europe rulers 1776.txt","CLEANUP2C1_NAME_PHI"),195:("common/history/characters/cleanup2c1 - non europe rulers 1776.txt","CLEANUP2C1_NAME_FTJ"),202:("common/history/characters/cleanup2c1 - non europe rulers 1776.txt","CLEANUP2C1_NAME_KRT"),209:("common/history/characters/cleanup2c1 - non europe rulers 1776.txt","CLEANUP2C1_NAME_SGU"),210:("common/history/characters/cleanup2c1 - non europe rulers 1776.txt","CLEANUP2C1_NAME_SWZ"),
}


def direct_block(number: int) -> str:
    p=P[number]
    lines=["\t\tcreate_character = {",f"\t\t\tfirst_name = cleanup2d5_name_{number:03d}","\t\t\tlast_name = cleanup2d5_empty_name","\t\t\thistorical = yes"]
    if p["culture"]: lines.append(f"\t\t\tculture = cu:{p['culture']}")
    if p["religion"]: lines.append(f"\t\t\treligion = rel:{p['religion']}")
    if p["home"]: lines.append(f"\t\t\thome_region = {p['home']}")
    if p["birth"]: lines.append(f"\t\t\tbirth_date = {p['birth']}")
    elif p["age"]: lines.append(f"\t\t\tage = {p['age']} # BIRTH_YEAR_ONLY / supported approximation; no fabricated month/day")
    lines += ["\t\t\tinterest_group = ig_armed_forces"]
    if number==87: lines.append("\t\t\tdna = dna_washington_traitor")
    if number in (76,80): lines.append("\t\t\t# 2D5M recommends experienced_commander, but that is not a Victoria 3 1.13 trait token; intentionally unset.")
    lines += ["\t\t\tis_general = yes",f"\t\t\tsave_scope_as = cleanup2d4_general_{number:03d}","\t\t}",f"\t\tscope:cleanup2d4_general_{number:03d} = {{",f"\t\t\ttransfer_to_formation = scope:{baseline[f'GEN1776-{number:03d}']['formation_scope_after']}","\t\t}"]
    return "\n".join(lines)


formation_files=sorted(FORMATIONS.glob("0[0-7]_military_formations_*.txt"))
found=set()
for path in formation_files:
    rel=path.relative_to(ROOT).as_posix()
    # The eight gameplay files were verified clean against HEAD before this
    # phase. Starting from the immutable blob makes this transform idempotent
    # and safely recovers from an interrupted earlier run.
    text=subprocess.check_output(["git","show",f"HEAD:{rel}"],cwd=ROOT).decode("utf-8-sig")
    for number in names:
        rid=f"GEN1776-{number:03d}"
        marker=re.compile(rf"(?ms)(?P<indent>\t\t)# GEN1776-{number:03d}[^\n]*\n.*?(?=\t\t# (?:GEN1776-|END CLEANUP-2D-4 STARTING GENERALS 1776))")
        if not marker.search(text): continue
        found.add(number)
        header=f"\t\t# GEN1776-{number:03d} — {names[number]} — CLEANUP-2D-5"
        if number in reuse:
            scope=f"cleanup2d5_reuse_{number:03d}"
            body="\n".join([header,f"\t\tscope:{scope} = {{",f"\t\t\ttransfer_to_formation = scope:{baseline[rid]['formation_scope_after']}","\t\t}",""])
        else:
            body=header+"\n"+direct_block(number)+"\n"
        text=marker.sub(lambda _m: body,text,count=1)
    path.write_text(text,encoding="utf-8",newline="\n")

if found != set(names):
    raise SystemExit(f"Failed to locate formation marker(s): {sorted(set(names)-found)}")


def find_block(text: str, first_key: str) -> tuple[int,int]:
    match=re.search(rf"(?m)^\s*first_name\s*=\s*{re.escape(first_key)}\s*$",text)
    if not match: raise ValueError(f"first_name key not found: {first_key}")
    start=text.rfind("\t\tcreate_character = {",0,match.start())
    if start<0: raise ValueError(f"create_character block not found for {first_key}")
    brace=text.find("{",start); depth=0
    for pos in range(brace,len(text)):
        if text[pos]=="{": depth+=1
        elif text[pos]=="}":
            depth-=1
            if depth==0: return start,pos+1
    raise ValueError(f"unclosed block for {first_key}")


by_file={}
for number,(relpath,key) in reuse.items():
    path=ROOT/relpath
    if path in by_file:
        text=by_file[path]
    else:
        text=subprocess.check_output(["git","show",f"HEAD:{path.relative_to(ROOT).as_posix()}"],cwd=ROOT).decode("utf-8-sig")
    start,end=find_block(text,key); block=text[start:end]
    lines=block.splitlines()
    dropped_fields="culture|religion|home_region|birth_date|age|is_general|save_scope_as" if number == 68 else "first_name|last_name|culture|religion|home_region|birth_date|age|is_general|save_scope_as"
    drop=re.compile(rf"^\s*({dropped_fields})\s*=")
    lines=[line for line in lines if not drop.match(line)]
    insert=next(i for i,line in enumerate(lines) if "historical = yes" in line)+1
    p=P[number]
    fields=[] if number == 68 else [f"\t\t\tfirst_name = cleanup2d5_name_{number:03d}","\t\t\tlast_name = cleanup2d5_empty_name"]
    # Names must precede historical for conventional readability.
    hist=insert-1
    lines[hist:hist]=fields
    insert=hist+len(fields)+1
    extra=[]
    if p["culture"]: extra.append(f"\t\t\tculture = cu:{p['culture']}")
    if p["religion"]: extra.append(f"\t\t\treligion = rel:{p['religion']}")
    if p["home"]: extra.append(f"\t\t\thome_region = {p['home']}")
    if p["birth"]: extra.append(f"\t\t\tbirth_date = {p['birth']}")
    elif p["age"]: extra.append(f"\t\t\tage = {p['age']} # BIRTH_YEAR_ONLY / supported approximation; no fabricated month/day")
    extra += ["\t\t\tis_general = yes",f"\t\t\tsave_scope_as = cleanup2d5_reuse_{number:03d}"]
    lines[insert:insert]=extra
    text=text[:start]+"\n".join(lines)+text[end:]
    by_file[path]=text
for path,text in by_file.items():
    # Preserve the tracked BOM convention of the newly touched 2B3 ruler file;
    # the three already-generated 2D5 character files retain their established output.
    encoding="utf-8-sig" if path.name == "cleanup2b3 - residual europe rulers 1776.txt" else "utf-8"
    path.write_text(text,encoding=encoding,newline="\n")


def yml(language: str) -> str:
    lines=[f"l_{language}:"," cleanup2d5_empty_name:0 \"\""]
    for number in sorted(names):
        if number == 68: continue  # Existing George/Browne localization is reused.
        escaped=names[number].replace('"','\\"')
        lines.append(f" cleanup2d5_name_{number:03d}:0 \"{escaped}\"")
    return "\n".join(lines)+"\n"

(ROOT/"localization/english/cleanup2d5_generals_l_english.yml").write_text(yml("english"),encoding="utf-8-sig",newline="\n")
(ROOT/"localization/french/cleanup2d5_generals_l_french.yml").write_text(yml("french"),encoding="utf-8-sig",newline="\n")

print(f"HISTORICAL_FORMATION_ATTACHMENTS={len(found)}")
print(f"REUSED_EXISTING_CHARACTERS={len(reuse)}")
print(f"NEW_OR_DIRECT_REBUILT_CHARACTERS={len(names)-len(reuse)}")
