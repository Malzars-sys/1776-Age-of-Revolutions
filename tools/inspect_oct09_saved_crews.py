"""Read-only, streaming inspection of a locally melted Victoria 3 save."""
from pathlib import Path
import collections
import json
import re

SAVE = Path('.asset-cache/oct09_balance_revision/autosave_exit_readonly.txt')

def objects():
    section = None
    ident = None
    lines = []
    for line in SAVE.open(encoding='utf-8'):
        if line and not line[0].isspace():
            section = line.split('=',1)[0] if line.endswith('={\n') else None
        m = re.fullmatch(r'\t\t(\d+)=\{\n',line)
        if m:
            ident = int(m[1]); lines = [line]
        elif ident is not None:
            lines.append(line)
            if line == '\t\t}\n':
                yield section,ident,''.join(lines)
                ident = None

def field(raw,name):
    m = re.search(r'^\t\t\t'+name+r'=(.*)$',raw,re.M)
    return m[1].strip('"') if m else None

def main():
    fleets = {}; ships = []; buildings = []; models = {}; country = None
    for section,ident,raw in objects():
        if section == 'military_formation_manager' and field(raw,'country') == '1':
            fleets[ident] = {k:field(raw,k) for k in ('type','localizable_name','home_hq','supply_hub')}
        elif section == 'ship_manager':
            ships.append((ident,raw))
        elif section == 'ship_design_manager':
            models[ident] = raw
        elif section == 'building_manager' and 'building_naval_administration' in raw:
            buildings.append((ident,raw))
        elif section == 'country_manager' and ident == 1:
            country = raw
    groups = collections.defaultdict(list)
    samples = []
    assigned = collections.Counter()
    slots = collections.Counter()
    for ident,raw in ships:
        fleet = int(field(raw,'fleet') or -1)
        if fleet not in fleets: continue
        crew = sum(map(int,re.findall(r'^\t{5}crew=(\d+)',raw,re.M)))
        version = field(raw,'version')
        groups[(fleet,version)].append(crew)
        for state,n in re.findall(r'\t{5}state=(\d+)\n\t{5}crew=(\d+)',raw):
            assigned[state] += int(n)
            slots[state] += 1
        if len(samples)<3:
            samples.append({'id':ident,'fields':raw[-1800:]})
    out = {'assigned_per_state':dict(assigned),'slots_per_state':dict(slots),'fleets':fleets,'crews':[{'fleet':k[0],'version':k[1],'count':len(v),'crew_histogram':dict(collections.Counter(v)),'total':sum(v)} for k,v in groups.items()],
           'ship_samples':samples,'naval_building_samples':[{'id':i,'raw':r[:3500]} for i,r in buildings[:6]],
           'country_sailor_lines':[l.strip() for l in (country or '').splitlines() if 'sailor' in l or 'crew' in l]}
    Path('.asset-cache/oct09_balance_revision/saved_crews_diagnosis.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out))

if __name__ == '__main__': main()
