"""Read-only source audit; writes only ASSET2 CSV reports beside this file.

Run from the repository root with Python 3. No game definitions are changed.
"""
from __future__ import annotations

import csv
import hashlib
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
VANILLA = Path(r"C:\Games\Victoria 3\game")
WORKSHOP = Path(r"C:\Program Files (x86)\Steam\steamapps\workshop\content\529340")


def read(path):
    return path.read_text(encoding="utf-8-sig", errors="replace")


def tokenize(src):
    # Clausewitz tokens, comments and quoted strings. Every brace remains explicit.
    return re.findall(r'"(?:\\.|[^"\\])*"|\#[^\n]*|\{|\}|=|[^\s{}=#]+', src)


def definitions(folder):
    result = {}
    for file in sorted(folder.glob("*.txt")):
        tokens = [t for t in tokenize(read(file)) if not t.startswith("#")]
        i = 0
        while i + 2 < len(tokens):
            if tokens[i + 1] != "=" or tokens[i + 2] != "{":
                i += 1
                continue
            key = tokens[i]
            depth = 1
            j = i + 3
            while j < len(tokens) and depth:
                depth += (tokens[j] == "{") - (tokens[j] == "}")
                j += 1
            if depth == 0:
                result[key] = (tokens[i + 3:j - 1], file)
            i = j
    return result


def effective(subdir):
    return definitions(VANILLA / subdir) | definitions(ROOT / subdir)


def value(tokens, key):
    for i in range(len(tokens) - 2):
        if tokens[i] == key and tokens[i + 1] == "=":
            return tokens[i + 2].strip('"') if tokens[i + 2] != "{" else ""
    return ""


def block(tokens, key):
    for i in range(len(tokens) - 2):
        if tokens[i] == key and tokens[i + 1:i + 3] == ["=", "{"]:
            depth = 1
            for j in range(i + 3, len(tokens)):
                depth += (tokens[j] == "{") - (tokens[j] == "}")
                if depth == 0:
                    return tokens[i + 3:j]
    return []


def refs(tokens, key, prefix):
    return sorted(set(t for t in block(tokens, key) if t.startswith(prefix) and re.fullmatch(r'[A-Za-z][\w.\-]*', t) and t not in ('yes', 'no')))


def locs(lang):
    result = {}
    for base in (VANILLA / "localization" / lang, ROOT / "localization" / lang):
        if not base.exists():
            continue
        for file in sorted(base.rglob("*.yml")):
            for line in read(file).splitlines():
                m = re.match(r'^\s*([\w.\-]+):\d*\s+"((?:\\.|[^"\\])*)"', line)
                if m:
                    result[m[1]] = m[2]
    return result


EN, FR = locs("english"), locs("french")


def name(key, lang):
    return lang.get(key, key.replace("_", " ").capitalize())


def csvout(filename, rows, fields):
    with (OUT / filename).open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


BASE_EVIDENCE = list(csv.DictReader((OUT / "ASSET1_EXTERNAL_ASSET_FILE_EVIDENCE.csv").open(encoding="utf-8-sig", newline="")))
BY_HASH = defaultdict(list)
for entry in BASE_EVIDENCE:
    BY_HASH[entry["SHA256"]].append(entry)


def texture_info(texture):
    if not texture:
        return "NO", "NONE", "MISSING"
    normalized = texture.replace("\\", "/")
    local = ROOT / normalized
    vanilla = VANILLA / normalized
    if local.is_file():
        source = "FORK_CUSTOM"
        hash_ = sha(local)
        matches = BY_HASH.get(hash_, [])
        if any(r["Workshop_ID"] == "3472248460" for r in matches):
            source = "TECH_RES_PERMISSION_PENDING"
        elif any(r["Workshop_ID"] == "3715913236" for r in matches):
            source = "LA_GABELLE_AUTHORIZED"
        elif any(r["Workshop_ID"] == "2880120246" for r in matches):
            source = "BASILEIA_PERMISSION_PENDING"
        exists = "YES"
    elif vanilla.is_file():
        source, exists = "VANILLA", "YES"
    else:
        source, exists = "NONE", "NO"
    low = normalized.lower()
    if exists == "NO":
        status = "MISSING"
    elif source == "TECH_RES_PERMISSION_PENDING":
        status = "UNAUTHORIZED_EXTERNAL"
    elif source == "LA_GABELLE_AUTHORIZED":
        status = "AUTHORIZED_EXTERNAL"
    elif any(s in low for s in ("error_manul", "error_deer", "error_", "disabled.dds")):
        status = "PLACEHOLDER"
    elif "mixed_icon" in low or "generic_icon" in low:
        status = "GENERIC"
    elif source == "VANILLA":
        status = "FINAL_VANILLA"
    else:
        status = "FINAL_CUSTOM_REVIEW"
    return exists, source, status


def category(kind, id_, token):
    if kind == "TECHNOLOGY":
        branch = value(token, "category").upper()
        s = id_.lower()
        keys = {
            "PRODUCTION": [
                ("AGRICULTURE", "crop seed soil farm husbandry agrarian plant agricultur sericultur fertiliz") ,
                ("FORESTRY", "forestr lumber timber wood sawmill"),
                ("MINING", "mine mining quarry drill shaft extraction"),
                ("METALLURGY", "iron steel coke smelt metal forge puddling blast"),
                ("TEXTILES", "textile cotton weaving spinning loom dye"),
                ("CHEMISTRY", "chemical acid alkali pharmaceutical medicine gasification") ,
                ("ENERGY", "steam engine coal power electric fuel"),
                ("TRANSPORT", "road rail canal locomotive transport") ,
                ("CONSTRUCTION", "construction cement building masonry") ,
            ],
            "MILITARY": [
                ("NAVAL", "naval ship frigate boat fleet sail dock maritime") ,
                ("ARTILLERY", "artillery cannon powder gunpowder") ,
                ("CAVALRY", "cavalry horse dragoon") ,
                ("FORTIFICATION", "fort wall defense siege") ,
                ("LOGISTICS", "supply logistics quartermaster") ,
            ],
            "SOCIETY": [
                ("EDUCATION", "education school academ univers polytechnic") ,
                ("SCIENCE", "science scientific research empiric astronomy") ,
                ("MEDICINE", "medicine medical hospital vaccin health") ,
                ("FINANCE", "bank credit currency monetary financial saving") ,
                ("COMMERCE", "trade commerce insurance charter market") ,
                ("ADMINISTRATION", "administr state archiv census statist") ,
                ("COMMUNICATION", "press newspaper postal telegraph") ,
                ("LAW", "law police legal justice") ,
                ("POLITICS", "constitution democracy parliament politics") ,
            ],
        }
        for domain, words in keys.get(branch, []):
            if any(w in s for w in words.split()):
                return branch + "_" + domain
        return {"PRODUCTION": "PRODUCTION_MANUFACTURING", "MILITARY": "MILITARY_INFANTRY", "SOCIETY": "SOCIETY_POLITICS"}.get(branch, branch or "REVIEW")
    s = id_.lower()
    if any(x in s for x in ("chemical", "fertiliz", "pharma", "sulfur")):
        return "CHEMICAL"
    if any(x in s for x in ("port", "shipyard", "naval", "dock")):
        return "PORT_NAVAL"
    if any(x in s for x in ("farm", "ranch", "husband", "livestock")):
        return "AGRICULTURE"
    if "plantation" in s:
        return "PLANTATION"
    if any(x in s for x in ("mine", "quarry")):
        return "MINING"
    if any(x in s for x in ("logging", "fishing", "resource")):
        return "RESOURCE"
    if any(x in s for x in ("power", "oil", "electric", "gas")):
        return "ENERGY"
    if any(x in s for x in ("barracks", "military", "munition", "arms", "artillery", "fort")):
        return "MILITARY"
    if any(x in s for x in ("university", "academy", "school")):
        return "EDUCATION"
    if any(x in s for x in ("admin", "government", "hospital")):
        return "ADMINISTRATION"
    if any(x in s for x in ("trade", "merchant", "commercial")):
        return "TRADE"
    if "construction" in s:
        return "CONSTRUCTION"
    if any(x in s for x in ("canal", "rail", "road", "urban", "infrastructure")):
        return "INFRASTRUCTURE"
    if any(x in s for x in ("steel", "metal", "alloy", "iron", "machinery")):
        return "HEAVY_INDUSTRY"
    return "LIGHT_INDUSTRY"


def brief(kind, id_, category_, en):
    subject = en if en != id_.replace("_", " ").capitalize() else id_.replace("_", " ")
    if kind == "TECHNOLOGY":
        return subject, "Un objet ou une scène conceptuelle dominante; lisible à 64 px", "XVIIIe–début XIXe siècle selon la technologie", "Outils et matériaux d'époque", "Atelier, champ ou intérieur discret", "NO", "NO", "Texte, logos modernes et anachronismes", "gfx/interface/icons/invention_icons/"
    if kind == "GOOD":
        return subject, "Matière ou objet isolé, centré, silhouette nette", "Époque 1776–1836 sauf bien ultérieur", "Produit physique identifiable", "Fond transparent", "NO", "NO", "Texte, marques et emballages modernes", "gfx/interface/icons/goods_icons/"
    if kind == "BUILDING":
        return subject, "Bâtiment ou site de production, produit en premier plan inférieur droit", "Époque 1776–1836 sauf bâtiment ultérieur", "Architecture et outil typiques", "Site historique, lumière sobre", "SMALL_ONLY", "NO", "Architecture industrielle anachronique", "gfx/interface/icons/building_icons/"
    return subject, "Procédé ou machine spécifique, composition simple", "Époque de la PM", "Transformation visible", "Atelier discret ou transparent", "SMALL_ONLY", "NO", "Texte, logos et technologie postérieure", "gfx/interface/icons/production_method_icons/"


def priority(status, id_, kind):
    if status in ("PLACEHOLDER", "MISSING"):
        return "P0"
    if kind in ("GOOD", "BUILDING") and any(x in id_ for x in ("chemical", "pharma", "phosph", "salt", "copper", "aluminium", "cement")):
        return "P1"
    if status in ("UNAUTHORIZED_EXTERNAL", "SEMANTIC_MISMATCH"):
        return "P2"
    return "P3"


def stage(kind, tokens, id_):
    if kind == "TECHNOLOGY":
        return value(tokens, "era") or "UNKNOWN"
    return "1776+" if not any(x in id_ for x in ("electric", "automobile", "aircraft")) else "LATER"


techs = definitions(ROOT / "common/technology/technologies")
goods = effective("common/goods")
buildings = effective("common/buildings")
pmgs = effective("common/production_method_groups")
pms = effective("common/production_methods")
techs = {k: v for k, v in techs.items() if k != "technology" and value(v[0], "can_research") != "no" and value(v[0], "texture")}
building_to_pmg = {k: refs(t, "production_method_groups", "pmg_") for k, (t, _) in buildings.items()}
active_pmgs = set(x for v in building_to_pmg.values() for x in v)
pmg_to_pm = {k: refs(t, "production_methods", "pm_") for k, (t, _) in pmgs.items() if k in active_pmgs}
active_pms = set(x for v in pmg_to_pm.values() for x in v)
pmg_buildings = defaultdict(list)
pm_pmg = defaultdict(list)
for building, group_ids in building_to_pmg.items():
    for group_id in group_ids:
        pmg_buildings[group_id].append(building)
for group_id, method_ids in pmg_to_pm.items():
    for method_id in method_ids:
        pm_pmg[method_id].append(group_id)

records = []
for kind, defs in (("TECHNOLOGY", techs), ("GOOD", goods), ("BUILDING", buildings), ("PRODUCTION_METHOD_GROUP", {k: v for k, v in pmgs.items() if k in active_pmgs}), ("PRODUCTION_METHOD", {k: v for k, v in pms.items() if k in active_pms})):
    for id_, (tokens, sourcefile) in sorted(defs.items()):
        icon = value(tokens, "icon" if kind == "BUILDING" else "texture")
        exists, source, status = texture_info(icon)
        if kind == "BUILDING":
            panel = value(tokens, "background")
            panel_exists, panel_source, panel_status = texture_info(panel)
        else:
            panel = panel_exists = panel_source = panel_status = ""
        cat = category(kind, id_, tokens)
        gate = "|".join(refs(tokens, "unlocking_technologies", ""))
        # Vanilla generic/disabled PMs are genuine UI states, not automatically illustration gaps.
        need = "YES" if status in ("PLACEHOLDER", "MISSING") else ("REVIEW" if status in ("GENERIC", "UNAUTHORIZED_EXTERNAL", "FINAL_CUSTOM_REVIEW") else "NO")
        if status == "GENERIC" and kind == "PRODUCTION_METHOD_GROUP":
            need = "NO"
        # Hidden vanilla world monuments use map entities, not a building-card icon.
        if kind == "BUILDING" and not icon and value(tokens, "building_group") == "bg_monuments_hidden":
            status, need = "NOT_APPLICABLE_MAP_ENTITY", "NO"
        # A PMG without explicit texture may inherit its member PM's UI art.
        # Keep it visible in the full inventory but do not invent an icon requirement.
        if kind == "PRODUCTION_METHOD_GROUP" and not icon:
            status, need = "NO_EXPLICIT_TEXTURE_REVIEW", "REVIEW"
        if kind == "PRODUCTION_METHOD" and id_ == "pm_dummy":
            status, need = "NOT_APPLICABLE_DUMMY", "NO"
        subject, composition, historical, objects, background, human, text, avoid, style = brief(kind, id_, cat, name(id_, EN))
        records.append(dict(Object_Type=kind, Object_ID=id_, Name_EN=name(id_, EN), Name_FR=name(id_, FR), Category=cat,
                            Era_or_Stage=stage(kind, tokens, id_), Current_Texture=icon, Texture_Exists=exists,
                            Texture_Source=source, Visual_Status=status, Needs_New_Asset=need, Definition_File=str(sourcefile.relative_to(ROOT if ROOT in sourcefile.parents else VANILLA)),
                            Building_Group=value(tokens, "building_group"), Current_Illustration=panel, Illustration_Exists=panel_exists,
                            Illustration_Source=panel_source, Illustration_Status=panel_status,
                            PMG_ID="|".join(pm_pmg[id_]) if kind == "PRODUCTION_METHOD" else "",
                            Building="|".join(sorted({b for g in pm_pmg[id_] for b in pmg_buildings[g]})) if kind == "PRODUCTION_METHOD" else "|".join(pmg_buildings[id_]) if kind == "PRODUCTION_METHOD_GROUP" else "",
                            Technology_Gate=gate, Visual_Subject=subject, Composition=composition,
                            Historical_Period=historical, Important_Objects=objects, Background=background,
                            Human_Figure_Allowed=human, Text_Allowed=text, Elements_To_Avoid=avoid,
                            Closest_Vanilla_Style_Reference=style,
                            Priority=priority(status, id_, kind),
                            Creation_Type="NEW_ORIGINAL" if need == "YES" else ("REVIEW" if need == "REVIEW" else "NONE")))

for r in records:
    r.update(Good_ID=r["Object_ID"] if r["Object_Type"] == "GOOD" else "",
             Building_ID=r["Object_ID"] if r["Object_Type"] == "BUILDING" else "",
             PM_ID=r["Object_ID"] if r["Object_Type"] == "PRODUCTION_METHOD" else "",
             PMG_Object_ID=r["Object_ID"] if r["Object_Type"] == "PRODUCTION_METHOD_GROUP" else "",
             Current_Icon=r["Current_Texture"], Icon_Source=r["Texture_Source"], Source=r["Texture_Source"],
             Status=r["Visual_Status"], Final_or_Placeholder=r["Visual_Status"],
             Economic_Category=r["Category"],
             Needs_Icon="YES" if r["Object_Type"] == "BUILDING" and r["Needs_New_Asset"] == "YES" else "NO",
             Needs_Illustration="NO" if r["Object_Type"] == "BUILDING" else "",
             Suggested_Visual_Subject=r["Visual_Subject"])

fields = ["Object_Type", "Object_ID", "Name_EN", "Name_FR", "Category", "Era_or_Stage", "Current_Texture", "Texture_Exists", "Texture_Source", "Visual_Status", "Needs_New_Asset", "Definition_File", "Building_Group", "Current_Illustration", "Illustration_Exists", "Illustration_Source", "Illustration_Status", "PMG_ID", "Building", "Technology_Gate", "Visual_Subject", "Composition", "Historical_Period", "Important_Objects", "Background", "Human_Figure_Allowed", "Text_Allowed", "Elements_To_Avoid", "Closest_Vanilla_Style_Reference", "Priority", "Creation_Type"]
csvout("ASSET2_FULL_OBJECT_VISUAL_INVENTORY.csv", records, fields)

tech_baseline = {r["Technology_ID"]: r for r in csv.DictReader((OUT / "ASSET1_TECH_ICONS_REMAINING_TO_CREATE.csv").open(encoding="utf-8-sig", newline=""))}
for r in records:
    if r["Object_Type"] == "TECHNOLOGY" and r["Object_ID"] in tech_baseline:
        baseline = tech_baseline[r["Object_ID"]]
        r["ASSET1_Status"] = baseline["Current_Status"]
        if r["Needs_New_Asset"] == "YES":
            r["Visual_Subject"] = baseline["Suggested_Visual_Subject"] or r["Visual_Subject"]
            r["Composition"] = baseline["Suggested_Composition"] or r["Composition"]
            r["Important_Objects"] = baseline["Important_Historical_Elements"] or r["Important_Objects"]
            r["Elements_To_Avoid"] = baseline["Elements_To_Avoid"] or r["Elements_To_Avoid"]

basileia_pending = {
    "organized_workshops": "br_tech_artisan_manufacturing.dds",
    "institutionalized_scientific_exchange": "br_tech_early_modern_universities.dds",
    "traditional_papermaking": "br_tech_paper_manufacturies.dds",
    "improved_agricultural_implements": "br_tech_seed_drill.dds",
}
for r in records:
    if r["Object_Type"] == "TECHNOLOGY" and r["Object_ID"] in basileia_pending and r["Needs_New_Asset"] == "YES":
        r["Creation_Type"] = "AUTHORIZED_EXTERNAL_REUSE_PENDING"

for kind, filename in (("TECHNOLOGY", "ASSET2_TECH_ASSET_CREATION_LIST.csv"), ("GOOD", "ASSET2_GOOD_ASSET_CREATION_LIST.csv"), ("BUILDING", "ASSET2_BUILDING_ASSET_CREATION_LIST.csv"), ("PRODUCTION_METHOD", "ASSET2_PM_ASSET_CREATION_LIST.csv"), ("PRODUCTION_METHOD_GROUP", "ASSET2_PMG_ASSET_CREATION_LIST.csv")):
    subset = [r for r in records if r["Object_Type"] == kind]
    extra = {"TECHNOLOGY": ["ASSET1_Status"], "GOOD": ["Good_ID", "Current_Icon", "Icon_Source", "Final_or_Placeholder"],
             "BUILDING": ["Building_ID", "Economic_Category", "Current_Icon", "Source", "Status", "Needs_Icon", "Needs_Illustration"],
             "PRODUCTION_METHOD": ["PM_ID", "Current_Icon", "Source", "Status", "Suggested_Visual_Subject"],
             "PRODUCTION_METHOD_GROUP": ["PMG_Object_ID", "Current_Icon", "Source", "Status", "Suggested_Visual_Subject"]}[kind]
    csvout(filename, subset, fields + extra)

master = []
for r in records:
    if r["Needs_New_Asset"] == "NO":
        continue
    pending_candidate = basileia_pending.get(r["Object_ID"], "") if r["Object_Type"] == "TECHNOLOGY" else ""
    master.append(dict(Priority=r["Priority"], Object_Type=r["Object_Type"], Category=r["Category"], Object_ID=r["Object_ID"], Name_EN=r["Name_EN"], Name_FR=r["Name_FR"], Era_or_Stage=r["Era_or_Stage"], Current_Asset=r["Current_Texture"], Current_Source=r["Texture_Source"], Current_Status=r["Visual_Status"], External_Candidate=pending_candidate, Permission_Status="PENDING" if pending_candidate or r["Texture_Source"] == "TECH_RES_PERMISSION_PENDING" else "NOT_APPLICABLE", Needs_New_Asset=r["Needs_New_Asset"], Visual_Subject=r["Visual_Subject"], Composition=r["Composition"], Historical_Period=r["Historical_Period"], Style_Reference=r["Closest_Vanilla_Style_Reference"], Creation_Type=r["Creation_Type"], Notes="Pending source/provenance review" if r["Needs_New_Asset"] == "REVIEW" else ("Use only after express permission; otherwise create original" if pending_candidate else "Original illustration brief; no image generated")))
master.sort(key=lambda r: (r["Priority"], r["Object_Type"], r["Category"], r["Era_or_Stage"], r["Object_ID"]))
csvout("ASSET2_MASTER_ASSET_CREATION_LIST.csv", master, ["Priority", "Object_Type", "Category", "Object_ID", "Name_EN", "Name_FR", "Era_or_Stage", "Current_Asset", "Current_Source", "Current_Status", "External_Candidate", "Permission_Status", "Needs_New_Asset", "Visual_Subject", "Composition", "Historical_Period", "Style_Reference", "Creation_Type", "Notes"])

print("DEFINITIONS", len(techs), len(goods), len(buildings), len(active_pms), len(active_pmgs))
print("RESOLVED", Counter(r["Object_Type"] for r in records))
print("NEED", Counter(r["Object_Type"] for r in records if r["Needs_New_Asset"] == "YES"))
print("REVIEW", Counter(r["Object_Type"] for r in records if r["Needs_New_Asset"] == "REVIEW"))
print("STATUS", Counter(r["Visual_Status"] for r in records))
print("UNRESOLVED REFS", sorted(active_pmgs - pmgs.keys()), sorted(active_pms - pms.keys()))

# Provenance: compare every candidate from ASSET1 plus the subsequently added
# coal-gasification technology icon. Hash equality demonstrates copying, not authorship.
techres = [e for e in BASE_EVIDENCE if e["Workshop_ID"] == "3472248460"]
coal = WORKSHOP / "3472248460/gfx/interface/icons/invention_icons/coal_gasification.dds"
if coal.is_file():
    techres.append(dict(Exact_Source_Path=str(coal), Asset_Category="TECH", SHA256=sha(coal),
                        Matching_Fork_File=str(ROOT / "gfx/interface/icons/invention_icons/coal_gasification.dds")))
other_hashes = defaultdict(list)
for moddir in WORKSHOP.iterdir():
    if moddir.name in ("3472248460", "3617930953", "3780935876") or not moddir.is_dir():
        continue
    for file in moddir.rglob("*.dds"):
        try:
            other_hashes[sha(file)].append(str(file))
        except OSError:
            pass
provenance = []
for entry in techres:
    src = Path(entry["Exact_Source_Path"])
    hash_ = sha(src) if src.is_file() else ""
    matches = [Path(s) for s in entry.get("Matching_Fork_File", "").split("|") if s]
    existing = [p for p in matches if p.is_file()]
    identical = [p for p in existing if sha(p) == hash_]
    object_ids = []
    for p in existing:
        try:
            rel = p.relative_to(ROOT).as_posix()
        except ValueError:
            continue
        object_ids.extend(r["Object_Type"] + ":" + r["Object_ID"] for r in records if r["Current_Texture"].replace("\\", "/") == rel)
    peer = other_hashes.get(hash_, [])
    third = "|".join(peer)
    third_confirmed = bool(peer)
    # Workshop credits mention third-party components but not these exact files.
    action = "THIRD_PARTY_PERMISSION_REQUIRED" if third_confirmed else ("KEEP_IF_PERMISSION_GRANTED" if identical else "REVIEW")
    provenance.append(dict(Asset_Path=src.relative_to(WORKSHOP / "3472248460").as_posix(), Asset_Type=entry["Asset_Category"],
                           Used_By_Fork_Object="|".join(sorted(set(object_ids))) or "NOT_ACTIVE_OR_NOT_DIRECTLY_REFERENCED",
                           Already_In_Fork="YES" if existing else "NO", Binary_Identical="YES" if identical else "NO",
                           TechRes_Original_Path=str(src), SHA256=hash_, Fork_Files="|".join(str(p) for p in existing),
                           Possible_Third_Party_Source=third or "UNCONFIRMED; Workshop credits other mods without file-level attribution",
                           Author_Ownership_Confidence="LOW" if third_confirmed else "UNKNOWN",
                           Permission_Needed="YES", Recommended_Action=action,
                           Notes="PNG signature despite .dds extension" if src.is_file() and src.read_bytes()[:8] == b'\x89PNG\r\n\x1a\n' else ""))
csvout("ASSET2_TECHRES_PROVENANCE.csv", provenance, ["Asset_Path", "Asset_Type", "Used_By_Fork_Object", "Already_In_Fork", "Binary_Identical", "TechRes_Original_Path", "SHA256", "Fork_Files", "Possible_Third_Party_Source", "Author_Ownership_Confidence", "Permission_Needed", "Recommended_Action", "Notes"])

basileia_visuals = {
    "br_tech_artisan_manufacturing.dds": ("Atelier rural en pierre et brique, toit de tuiles, établi et chariot", "organized_workshops", "HIGH", "HIGH", "HIGH"),
    "br_tech_early_modern_universities.dds": ("Bâtiment universitaire de pierre à plusieurs étages, tour, livre et plume", "institutionalized_scientific_exchange", "MEDIUM", "MEDIUM", "HIGH"),
    "br_tech_four_field_crop_rotation.dds": ("Diagramme de quatre parcelles avec céréales et cultures sarclées", "advanced_crop_rotations", "HIGH", "HIGH", "HIGH"),
    "br_tech_frigate.dds": ("Frégate de bois à trois mâts sous voiles", "scientific_naval_architecture", "HIGH", "MEDIUM", "HIGH"),
    "br_tech_hand_tools.dds": ("Scie, rabot, marteau et ciseau sur établi en bois", "organized_workshops", "HIGH", "MEDIUM", "HIGH"),
    "br_tech_paper_manufacturies.dds": ("Presse à vis pour papier, bassin de pâte et feuilles", "traditional_papermaking", "HIGH", "HIGH", "HIGH"),
    "br_tech_seed_drill.dds": ("Semoir en bois à roues et rangs de semis", "improved_agricultural_implements", "HIGH", "HIGH", "HIGH"),
    "br_tech_silver_standard.dds": ("Lingot d'argent et piles de pièces d'argent", "institutionalized_public_credit", "MEDIUM", "LOW", "HIGH"),
}
basileia = []
for filename, (visual, target, hist, semantic, visualfit) in basileia_visuals.items():
    targetrec = next((r for r in records if r["Object_Type"] == "TECHNOLOGY" and r["Object_ID"] == target), None)
    source = next(e for e in BASE_EVIDENCE if e["Workshop_ID"] == "2880120246" and Path(e["Exact_Source_Path"]).name == filename)
    basileia.append(dict(Basileia_Asset=source["Exact_Source_Path"], Visual_Subject=visual, Target_Tech_ID=target,
                         Target_Tech_Name=targetrec["Name_FR"] if targetrec else "NOT_FOUND", Historical_Fit=hist,
                         Semantic_Fit=semantic, Visual_Fit=visualfit,
                         Would_Remove_Need_For_New_Asset="YES" if targetrec and targetrec["Needs_New_Asset"] == "YES" and semantic != "LOW" else "NO",
                         Permission_Status="PERMISSION_REQUIRED",
                         Notes="Competes with artisan manufacturing for same target" if filename == "br_tech_hand_tools.dds" else ("Already has Vanilla icon" if targetrec and targetrec["Needs_New_Asset"] == "NO" else "Candidate only; no file copied")))
csvout("ASSET2_BASILEIA_TECH_ICON_MAPPING.csv", basileia, ["Basileia_Asset", "Visual_Subject", "Target_Tech_ID", "Target_Tech_Name", "Historical_Fit", "Semantic_Fit", "Visual_Fit", "Would_Remove_Need_For_New_Asset", "Permission_Status", "Notes"])

shortlist = []
moddetails = {
    "3715913236": ("La Gabelle", "Tokugawa_Mori", "ALREADY_AUTHORIZED", "Permission documented 2026-08-28"),
    "3472248460": ("[1.13] Tech & Res", "Mattia10", "PERMISSION_REQUIRED", "Author and redistribution rights unconfirmed"),
    "2880120246": ("Basileia Romaion 1736", "Alexedishi;Drogan;Smekens", "PERMISSION_REQUIRED", "Authorship split must be clarified"),
}
for e in BASE_EVIDENCE:
    id_ = e["Workshop_ID"]
    if id_ not in moddetails:
        continue
    modname, author, status, note = moddetails[id_]
    sourcefile = Path(e["Exact_Source_Path"])
    matched = [r for r in records if any(str(ROOT / r["Current_Texture"]) == p for p in e.get("Matching_Fork_File", "").split("|") if r["Current_Texture"])]
    shortlist.append(dict(Mod_Name=modname, Workshop_ID=id_, Author=author,
                          URL="https://steamcommunity.com/sharedfiles/filedetails/?id=" + id_, Asset_Type=e["Asset_Category"],
                          Asset_Path=str(sourcefile), Visual_Subject=sourcefile.stem.replace("_", " "),
                          Potential_Target_Object="|".join(sorted({r["Object_Type"] for r in matched})) or "REVIEW",
                          Potential_Target_ID="|".join(sorted({r["Object_ID"] for r in matched})) or "REVIEW",
                          Already_In_Fork="YES" if e.get("Matching_Fork_File", "") and any(Path(p).is_file() for p in e["Matching_Fork_File"].split("|")) else "NO",
                          License="No public license identified" if id_ != "3715913236" else "Individual permission documented",
                          Permission_Status=status, Third_Party_Risk="POSSIBLE" if id_ == "3472248460" else "UNKNOWN",
                          Priority="P1" if matched else "P2", Notes=note))
if coal.is_file():
    shortlist.append(dict(Mod_Name="[1.13] Tech & Res", Workshop_ID="3472248460", Author="Mattia10",
                          URL="https://steamcommunity.com/sharedfiles/filedetails/?id=3472248460", Asset_Type="TECH",
                          Asset_Path=str(coal), Visual_Subject="coal gasification", Potential_Target_Object="TECHNOLOGY",
                          Potential_Target_ID="coal_gasification", Already_In_Fork="YES", License="No public license identified",
                          Permission_Status="PERMISSION_REQUIRED", Third_Party_Risk="POSSIBLE", Priority="P1",
                          Notes="Added after ASSET1; byte identity verified in provenance"))
csvout("ASSET2_EXTERNAL_MOD_SHORTLIST.csv", shortlist, ["Mod_Name", "Workshop_ID", "Author", "URL", "Asset_Type", "Asset_Path", "Visual_Subject", "Potential_Target_Object", "Potential_Target_ID", "Already_In_Fork", "License", "Permission_Status", "Third_Party_Risk", "Priority", "Notes"])

print("PROVENANCE", len(provenance), Counter(r["Binary_Identical"] for r in provenance))
print("SHORTLIST", len(shortlist), Counter(r["Mod_Name"] for r in shortlist))

def tally(label, subset):
    counts = Counter(r["Visual_Status"] for r in subset)
    definite = sum(r["Creation_Type"] == "NEW_ORIGINAL" for r in subset)
    lines = [f"### {label}", "", f"TOTAL OBJECTS = {len(subset)}",
             f"FINAL = {counts['FINAL_VANILLA'] + counts['AUTHORIZED_EXTERNAL']}",
             f"VANILLA FINAL = {counts['FINAL_VANILLA']}",
             f"AUTHORIZED EXTERNAL = {counts['AUTHORIZED_EXTERNAL']}",
             f"PERMISSION PENDING = {counts['UNAUTHORIZED_EXTERNAL'] + sum(r['Creation_Type'] == 'AUTHORIZED_EXTERNAL_REUSE_PENDING' for r in subset)}",
             f"NEEDS ORIGINAL ASSET = {definite}",
             f"REVIEW = {sum(r['Needs_New_Asset'] == 'REVIEW' for r in subset)}", ""]
    return lines

sections = ["# ASSET PASS 2 — bilan de création", "", "Audit du fork local au 24 septembre 2026, sans modification du jeu ni des textures.", "",
            "## Méthode et périmètre", "",
            "Les définitions `common/` du fork prévalent par identifiant sur Vanilla; seuls les PMG présents dans les bâtiments et les PM présents dans ces PMG sont comptés. Les technologies non recherchables sont exclues. Les textures sont résolues d'abord dans le fork, puis dans Vanilla. Les identités externes sont vérifiées par SHA-256. La liste ASSET1 sert de baseline technologique; aucun nouvel audit de réutilisation Vanilla n'a été effectué. Les nombres reflètent l'arbre de travail actuel, qui contenait déjà des modifications non commitées avant cette passe.", "",
            f"La baseline ASSET1 comptait {len(tech_baseline)} technologies à illustrer; l'arbre actuel en compte {sum(r['Object_Type'] == 'TECHNOLOGY' and r['Needs_New_Asset'] == 'YES' for r in records)}. Ce total inclut {sum(r['Object_Type'] == 'TECHNOLOGY' and r['Needs_New_Asset'] == 'YES' and r['Object_ID'] not in tech_baseline for r in records)} entrées absentes de la baseline; les autres écarts correspondent à des visuels déjà réaffectés entre les deux passes.", "",
            "`FINAL` signifie uniquement texture Vanilla finale ou copie externe autorisée. Les icônes génériques du jeu, les objets non visuels et les créations locales dont la sémantique reste à vérifier ne sont pas gonflés dans ce total. `PERMISSION PENDING` compte les objets actifs dépendant d'une copie Tech & Res, plus les candidats Basileia distincts. `NEEDS ORIGINAL ASSET` compte les originaux certains; les quatre candidats Basileia demanderaient eux aussi un original si l'autorisation est refusée.", "",
            "## TECHNOLOGIES", ""]
for prefix in ("PRODUCTION", "MILITARY", "SOCIETY"):
    sections += tally(prefix, [r for r in records if r["Object_Type"] == "TECHNOLOGY" and r["Category"].startswith(prefix)])
sections += ["## GOODS", ""] + tally("Tous les biens", [r for r in records if r["Object_Type"] == "GOOD"])
sections += ["## BUILDINGS", ""]
for label, cats in (("agriculture", ("AGRICULTURE", "PLANTATION")), ("extraction", ("MINING", "RESOURCE")),
                    ("industry", ("HEAVY_INDUSTRY", "LIGHT_INDUSTRY", "CHEMICAL", "ENERGY")),
                    ("infrastructure", ("INFRASTRUCTURE", "PORT_NAVAL", "TRADE", "CONSTRUCTION")),
                    ("military", ("MILITARY",)), ("public/service", ("ADMINISTRATION", "EDUCATION"))):
    sections += tally(label, [r for r in records if r["Object_Type"] == "BUILDING" and r["Category"] in cats])
sections += ["## PRODUCTION METHODS", ""] + tally("Toutes les PM actives", [r for r in records if r["Object_Type"] == "PRODUCTION_METHOD"])
sections += ["## PMG", ""] + tally("Tous les PMG actifs", [r for r in records if r["Object_Type"] == "PRODUCTION_METHOD_GROUP"])
sections += ["## Points de décision", "",
             "- Les 14 monuments cachés sans `icon` sont des entités de carte, pas 14 icônes à inventer.",
             "- `pm_dummy` est un état technique non illustré; il ne constitue pas une création.",
             "- Les 13 PMG actifs sans `texture` explicite restent en revue, car l'interface peut hériter de l'illustration des PM; ne pas commander d'images avant vérification en jeu.",
             "- Le `background` d'un bâtiment est un fond de panneau générique distinct de son `icon`; aucune nouvelle illustration de panneau spécifique n'est déduite de ce champ.",
             "- Les 25 fichiers Tech & Res (24 baseline + `coal_gasification.dds`) ont une propriété non confirmée; 23 sont déjà présents byte-identical dans le fork. La page Workshop crédite des tiers sans attribuer ces fichiers individuellement; aucune provenance tierce au niveau fichier n'est prouvée par les hachages des autres mods installés.",
             "- Les quatre candidats Basileia prioritaires restent conditionnels; aucune image n'a été copiée.",
             "- La Gabelle: permission déjà documentée; aucune nouvelle demande générale.", "",
             "## Totaux", "",
             f"Objets actifs inventoriés: {len(records)}.",
             f"Besoins visuels certains ou conditionnels: {sum(r['Needs_New_Asset'] == 'YES' for r in records)}.",
             f"Originaux certains: {sum(r['Creation_Type'] == 'NEW_ORIGINAL' for r in records)}.",
             f"Candidats externes Basileia conditionnels: {sum(r['Creation_Type'] == 'AUTHORIZED_EXTERNAL_REUSE_PENDING' for r in records)}.",
             f"Objets en revue: {sum(r['Needs_New_Asset'] == 'REVIEW' for r in records)}.",
             "Les copies Tech & Res existantes sont en revue de permission; si elle est refusée, leur remplacement devra être planifié séparément pour chaque fichier distinct.", ""]
(OUT / "ASSET2_CREATION_SUMMARY.md").write_text("\n".join(sections), encoding="utf-8")

print("TOTAL_NEW_ORIGINAL", sum(r["Creation_Type"] == "NEW_ORIGINAL" for r in records))
print("PRIORITIES", Counter(r["Priority"] for r in master))

techres_paths = "\n".join("- `" + p["Asset_Path"] + "`" for p in provenance)
basileia_paths = "\n".join("- `" + Path(b["Basileia_Asset"]).relative_to(WORKSHOP / "2880120246").as_posix() + "`" for b in basileia)
request_doc = f"""# Demandes d'autorisation — brouillons non envoyés

## Meilleur canal pour Tech & Res

La [page Workshop officielle](https://steamcommunity.com/sharedfiles/filedetails/?id=3472248460) identifie Mattia10 et renvoie vers son [dépôt GitHub](https://github.com/mattia2110/tech-and-res). Le dépôt a des [Issues ouvertes](https://github.com/mattia2110/tech-and-res/issues): c'est le meilleur canal pour une demande de droits précise, publique et retrouvable. Un commentaire court sur la page Workshop peut ensuite signaler l'issue si nécessaire. Ne pas supposer qu'un message privé Steam est ouvert aux non-amis. Aucun message n'a été envoyé.

La page Workshop cite Morgenröte pour une industrie d'édition et un atelier d'instruments, Tech56 pour des idées, Lunakibby pour des drapeaux, Glompspark/Caracus pour une règle. Cette attribution générale ne démontre pas que Mattia10 détient les droits des 25 fichiers ci-dessous, ni qu'ils proviennent des tiers nommés. Demander l'auteur effectif de chaque fichier et une autorisation écrite d'utiliser **et de redistribuer** ceux dont il détient les droits; demander le contact de l'ayant droit pour tout fichier tiers. Les hachages ne prouvent que l'identité binaire.

## Mattia10 — texte proposé (GitHub Issue, en anglais)

**Title:** Permission to use and redistribute specific Tech & Res visual assets in 1776 – Age of Revolutions

> Hi Mattia10, I maintain *1776 – Age of Revolutions*, a Victoria 3 total-conversion fork. We would like your explicit permission to use **and redistribute** the 25 Tech & Res visual files listed in Appendix A in our Steam Workshop release, with clear credit to you and Tech & Res. For transparency, 23 of these files are already byte-identical in our fork; we want to regularize that use before continuing. Can you confirm which files you personally own, whether any are third-party, and whether you authorize their use and Workshop redistribution? If any are third-party, please identify the rights holder so we can ask them directly. A reply here stating the permitted files and attribution wording would be ideal. Thank you.

Annexe A = liste exacte ci-dessous; joindre ou coller cette annexe à l'issue. Ne pas publier le fork comme « autorisé » sur cette base tant que Mattia10 n'a pas répondu explicitement.

### Annexe A — fichiers Tech & Res ({len(provenance)})

{techres_paths}

## Basileia Romaion 1736 — auteurs affichés

La [page Workshop Basileia](https://steamcommunity.com/sharedfiles/filedetails/?id=2880120246) affiche Alexedishi, Drogan et Smekens. Envoyer un message séparé à chacun, ou demander au premier interlocuteur de confirmer qui détient les huit icônes. Ne pas considérer la réponse d'un seul comme autorisation des trois sans confirmation de propriété.

### Alexedishi — texte proposé

> Hi Alexedishi, I maintain *1776 – Age of Revolutions*, a Victoria 3 total-conversion fork. May we use **and redistribute** the eight Basileia Romaion 1736 technology icons in Appendix B in our Steam Workshop release, with credit to you and the mod? Could you confirm which of these files you own and whether any require permission from Drogan, Smekens or another artist? Thank you.

### Drogan — texte proposé

> Hi Drogan, I maintain *1776 – Age of Revolutions*, a Victoria 3 total-conversion fork. May we use **and redistribute** the eight Basileia Romaion 1736 technology icons in Appendix B in our Steam Workshop release, with credit to you and the mod? Could you confirm which of these files you own and whether any require permission from Alexedishi, Smekens or another artist? Thank you.

### Smekens — texte proposé

> Hi Smekens, I maintain *1776 – Age of Revolutions*, a Victoria 3 total-conversion fork. May we use **and redistribute** the eight Basileia Romaion 1736 technology icons in Appendix B in our Steam Workshop release, with credit to you and the mod? Could you confirm which of these files you own and whether any require permission from Alexedishi, Drogan or another artist? Thank you.

### Annexe B — fichiers Basileia ({len(basileia)})

{basileia_paths}

## La Gabelle

Permission existante de Tokugawa_Mori documentée dans `docs/workshop/STEAM_WORKSHOP_CREDITS.md` et ASSET1. Aucune nouvelle demande générale recommandée.
"""
(OUT / "ASSET2_PERMISSION_REQUESTS_FINAL.md").write_text(request_doc, encoding="utf-8")

search_doc = """# Recherche complémentaire de mods visuels

## Mods installés vérifiés

- La Gabelle, Tech & Res, Basileia Romaion 1736: 45 fichiers concrets en shortlist, voir `ASSET2_EXTERNAL_MOD_SHORTLIST.csv`.
- Community Mod Framework (`3385002128`): bibliothèque d'interface et d'illustrations d'événements; aucun candidat exact supplémentaire validé pour les cinq catégories demandées.
- Shaped by the Land (`3734242682`) et Kuromi's AI (`3227982912`): aucun fichier DDS trouvé dans l'installation locale.
- News Events (`3786344818`): assets de journaux/événements, hors périmètre des icônes d'objet demandées.
- Mod original `3617930953` et Steam build `3780935876`: autres versions du même projet, non traitées comme sources tierces nouvelles.

## Pistes Web non téléchargées et non comptées comme assets shortlistés

- [More Technological Variety](https://steamcommunity.com/workshop/filedetails/?id=3286449081), Edouard_Saladier: le descriptif permet une intégration avec crédit, mais les fichiers précis, leur provenance et la compatibilité des visuels n'ont pas été inspectés. Contacter l'auteur avant toute réutilisation d'images non vérifiées.
- [Napoleonic Wars - Smithy](https://steamcommunity.com/workshop/filedetails/?id=3523731800), Smithy / Izabella / JJman: période 1789 proche du projet et arbre technologique remanié; aucun fichier précis inspecté ni permission identifiée.

Aucun fichier d'un mod nouvellement repéré n'a été copié. La shortlist de 45 entrées est strictement au niveau de chemins de fichiers vérifiés localement.
"""
(OUT / "ASSET2_OTHER_MOD_SEARCH.md").write_text(search_doc, encoding="utf-8")
