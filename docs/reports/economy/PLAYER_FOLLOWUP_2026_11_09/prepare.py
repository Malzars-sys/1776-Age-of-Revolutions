"""Prepare bounded player-requested economy changes; does not install candidates."""
import sys, json, re, hashlib, collections
from pathlib import Path
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'tools'))
from validate_diplomacy_ottoman_1776 import parse, walk

def digest(b): return hashlib.sha256(b).hexdigest()
def dump(name, obj):
    with (OUT / name).open('x', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write('\n')

assert not (OUT / 'PLAN.json').exists(), 'Evidence already prepared'
paths = [
 'common/production_methods/09_misc_resource.txt',
 'common/production_method_groups/99_tech_tree_wood_rework_pmgs.txt',
 'common/history/buildings/99_1776_econ_paper_forestry_livestock.txt',
 'common/history/buildings/99_1776_prussian_forestry_addon.txt',
 'localization/french/tech3a_technology_l_french.yml',
 'localization/english/tech3a_technology_l_english.yml',
 'common/production_methods/99_tech_start_1776_subsistence_tools.txt',
 'common/history/buildings/00_west_europe.txt',
 'common/history/buildings/98_build_start_1776_world_redistribution.txt',
 'tools/tech_start_1776_implementation.py',
]
before = {p: (ROOT / p).read_bytes() for p in paths}
raws = {p: b.decode('utf-8-sig') for p, b in before.items()}
edits = collections.defaultdict(list)
def edit(p, start, end, new, reason):
    edits[p].append(dict(start=start, end=end, before=raws[p][start:end], after=new, reason=reason))
def lines_matching(p, pattern, expected, reason):
    matches = list(re.finditer(pattern, raws[p], re.M))
    assert len(matches) == expected, (p, len(matches), expected)
    for m in matches: edit(p, m.start(), m.end(), '', reason)

p = paths[0]
n = next(n for n in parse(raws[p]) if n.key == 'pm_organized_forestry')
edit(p, n.start, n.end, '', 'Remove redundant forestry PM; simple forestry has identical output/jobs')
lines_matching(paths[1], r'^\t\tpm_organized_forestry\r?\n', 1, 'Remove PM from selectable group')
for p, count in [(paths[2], 3), (paths[3], 2)]:
    ms = list(re.finditer(r'\bpm_organized_forestry\b', raws[p]))
    assert len(ms) == count
    for m in ms: edit(p, m.start(), m.end(), 'pm_simple_forestry', 'Preserve forestry starts using surviving identical recipe')
for p in paths[4:6]:
    lines_matching(p, r'^\s*pm_organized_forestry(?:_desc)?:[^\r\n]*\r?\n', 2, 'Remove obsolete PM labels; preserve technology labels')
p = paths[6]
lines_matching(p, r'^\t\t\tgoods_output_tools_add = 0\.(?:10|20)\r?\n', 5, 'Remove tools from all five domestic subsistence workshop variants')
old = '# 1776 start compatibility: before tooling workshops become available through\r\n# coke_smelting, domestic workshops provide a deliberately small tools supply.'
assert raws[p].startswith(old)
edit(p, 0, len(old), '# Domestic subsistence workshops: clothes, furniture and liquor only.\r\n# Player decision of 2026-11-09: tools require dedicated industrial production.', 'Update obsolete header')

def placements(p):
    rows = []
    def rec(nodes, state=None, owner=None):
        for n in nodes:
            s = n.key[2:] if n.key.startswith('s:STATE_') else state
            o = n.key.split(':', 1)[1] if n.key.startswith('region_state:') else owner
            if n.key == 'create_building':
                rows.append((s, o, n.one('building', '').strip('"'), n))
            rec(n.children(), s, o)
    rec(parse(raws[p]))
    return rows
def level_edit(p, state, building, old, new):
    nodes = [n for s,o,b,n in placements(p) if (s,o,b)==(state,'GBR',building)]
    assert len(nodes)==1, (p,state,building,len(nodes))
    fields = [x for x in walk(nodes[0].children()) if x.key=='levels']
    assert len(fields)==1 and fields[0].value==str(old), (state,old)
    x=fields[0]; text=raws[p][x.start:x.end]
    m=re.search(r'(?<=\=)\s*'+str(old)+r'$',text)
    assert m
    token_start=x.start+m.start()+len(m.group())-len(str(old))
    edit(p,token_start,x.end,str(new),'Player relocation/addition of starting building levels')

regional, overlay = paths[7:9]
# Human observation: five Lancashire levels in the running game. The regional
# six-level declaration is an older variant, not ten additional active levels.
# The current overlay owns the five-level declaration; move only four levels.
level_edit(overlay, 'STATE_LANCASHIRE', 'building_tooling_workshop', 5, 1)
level_edit(overlay, 'STATE_MIDLANDS', 'building_tooling_workshop', 6, 8)
level_edit(regional, 'STATE_YORKSHIRE', 'building_tooling_workshop', 2, 4)

# Activate every existing British glass declaration, including the earlier variant.
glass_template = None
for p in (regional, overlay):
    for s,o,b,n in placements(p):
        if o=='GBR' and b=='building_glassworks':
            text=raws[p][n.start:n.end]
            assert text.count('pm_forest_glass')==1 and text.count('pm_disabled_ceramics')==1
            replacement=text.replace('pm_forest_glass','pm_leaded_glass').replace('pm_disabled_ceramics','pm_ceramics')
            edit(p,n.start,n.end,replacement,'Activate leaded glass and industrial ceramics')
            if p==overlay: glass_template=replacement
assert glass_template
# Add three levels: one extra in Midlands and one each in Lancashire/Yorkshire.
# The Midlands increment is inside its glass replacement span.
for e in edits[overlay]:
    if e['reason']=='Activate leaded glass and industrial ceramics':
        assert e['after'].count('levels=1')==1
        e['after']=e['after'].replace('levels=1','levels=2',1)
        e['reason'] += '; add one Midlands level'
for state in ['STATE_LANCASHIRE','STATE_YORKSHIRE']:
    state_nodes=[n for root in parse(raws[overlay]) for n in root.children() if n.key=='s:'+state]
    assert len(state_nodes)==1
    owners=state_nodes[0].children('region_state:GBR')
    assert len(owners)==1
    at=owners[0].end-1
    new=glass_template.replace('STATE_MIDLANDS',state)
    edit(overlay,at,at,'\r\n\t\t\t'+new+'\r\n\t\t','Add one glassworks level with local British ownership and requested PMs')

# Maintain the existing technology validator against the new player policy.
p=paths[9]
node_start=raws[p].index('def validate_subsistence_pm()')
node_end=raws[p].index('\r\ndef validate_structural_trunks(',node_start)
new='''def validate_subsistence_pm() -> list[str]:
    # Player decision, 2026-11-09: domestic workshops must not produce tools.
    expected = {
        "pm_home_workshops_building_subsistence_farm": "0.25",
        "pm_home_workshops_building_subsistence_orchard": "0.25",
        "pm_home_workshops_building_subsistence_pasture": "0.25",
        "pm_home_workshops_building_subsistence_fishing_village": "0.25",
        "pm_home_workshops_building_subsistence_rice_farm": "0.50",
    }
    errors: list[str] = []
    if not SUBSISTENCE_PM_FILE.exists():
        return ["fichier PM de subsistance absent"]
    for pm, value in expected.items():
        try:
            block = named_block(SUBSISTENCE_PM_FILE, pm)
        except ValueError:
            errors.append(f"{pm} absent")
            continue
        if re.search(r"(?m)^\\s*goods_output_tools_(?:add|mult)\\s*=", block):
            errors.append(f"{pm}: sortie outils interdite")
        for good in ("clothes", "furniture", "liquor"):
            if not re.search(rf"(?m)^\\s*goods_output_{good}_add\\s*=\\s*{re.escape(value)}\\s*$", block):
                errors.append(f"{pm}: sortie {good} {value} absente")
    return errors

'''.replace('\n','\r\n')
edit(p,node_start,node_end,new,'Replace old tools-preservation policy with explicit no-tools and retained-goods checks')

protected={}
for folder in ('common','events','localization','map_data','gui'):
    for p in (ROOT/folder).rglob('*'):
        if p.is_file() and p.suffix.lower() in {'.txt','.yml','.gui','.csv','.mod'}:
            protected[p.relative_to(ROOT).as_posix()]=digest(p.read_bytes())
protected[paths[9]]=digest(before[paths[9]])
dump('SOURCE_BASELINE.json',protected)
manifest=[]
for p, data in before.items():
    previous=-1
    for e in sorted(edits[p],key=lambda x:(x['start'],x['end'])):
        assert e['start']>=previous,(p,'overlap')
        previous=e['end']
    raw=raws[p]
    for e in sorted(edits[p],key=lambda x:x['start'],reverse=True):
        raw=raw[:e['start']]+e['after']+raw[e['end']:]
    if p.endswith('.txt'): parse(raw)
    if p.endswith('.py'): compile(raw,p,'exec')
    candidate=(b'\xef\xbb\xbf' if data.startswith(b'\xef\xbb\xbf') else b'')+raw.encode('utf-8')
    for kind, payload in [('before',data),('candidate',candidate)]:
        dest=OUT/kind/p;dest.parent.mkdir(parents=True,exist_ok=True)
        with dest.open('xb') as f:f.write(payload)
    manifest.append(dict(path=p,before_sha256=digest(data),after_sha256=digest(candidate),spans=edits[p]))
dump('PLAN.json',manifest)
print(json.dumps({'candidate_files':len(manifest),'protected_sources':len(protected),'gameplay_files':len(manifest)-1,'status':'PREPARED_NOT_INSTALLED'}))
