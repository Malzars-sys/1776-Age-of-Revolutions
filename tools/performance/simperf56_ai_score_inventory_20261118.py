"""Static candidate inventory, never runtime frequency/cost evidence."""
from pathlib import Path
import hashlib, json, re, sys
from simperf56_ai_cohorts import LAB
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from validate_diplomacy_ottoman_1776 import parse
plan=json.loads((LAB/'SOURCE_PLAN.json').read_text(encoding='utf-8'))
root=Path(plan['main_frozen'])
steam=Path('C:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game')
rows=[]
for path in sorted((root/'common/buildings').glob('*.txt')):
    raw=path.read_text(encoding='utf-8-sig')
    for building in parse(raw):
        for value in building.children('ai_value'):
            block=raw[value.start:value.end]
            calls=sorted(set(re.findall(r'\baor1776_ai_\w+',block)))
            if not calls:continue
            native=steam/path.relative_to(root)
            nv=None
            if native.exists():
                candidates=[x for x in parse(native.read_text(encoding='utf-8-sig')) if x.key==building.key]
                if candidates:nv=candidates[0].one('ai_value')
            rows.append(dict(file=str(path.relative_to(root)),building=building.key,
                line=raw.count('\n',0,value.start)+1,initial_value=value.one('value'),
                mod_callbacks=calls,any_scope_building_occurrences=block.count('any_scope_building'),
                block_sha256=hashlib.sha256(block.encode('utf-8')).hexdigest(),
                steam_value_kind='block' if isinstance(nv,list) else 'scalar_or_absent',
                steam_scalar_value=nv if not isinstance(nv,list) else None))
out=dict(scope='Static frozen-runtime inventory only; no call frequency or CPU attribution',
    blocks=len(rows),files=len(set(r['file'] for r in rows)),rows=rows,
    monthly_controller_removal_does_not_remove_these_callbacks=True,
    proposed_category='Only modded building ai_value callback evaluation; native AI/controllers/objectives preserved',
    experimental_runtime_created=False,gameplay_preserving_optimization_validated=False)
with (LAB/'MODDED_AI_SCORE_CALLBACK_INVENTORY_20261118.json').open('x',encoding='utf-8') as f:json.dump(out,f,indent=2)
print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
