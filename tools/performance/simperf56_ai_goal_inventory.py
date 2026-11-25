"""Describe registered native AI goals and diplomatic target records, not cost."""
from collections import Counter
import json
from simperf56_ai_cohorts import LAB, SOURCE, db_chunks
from simperf56_save_state import sections

inventory=json.loads((LAB/'CONTROLLER_INVENTORY.json').read_text(encoding='utf-8'))
countries={r['country_id']:r for r in inventory['controllers']}
text=SOURCE.read_text(encoding='utf-8-sig'); spans=sections(text)
groups={k:dict(controllers=0,registered_goal_types=Counter(),diplomatic_target_entries=0,
    initialized_targets=0,secret_goal_initialized_targets=0,targets_without_populated_country=0,
    scalar_field_names=Counter()) for k in ('DEC','OTHER')}
for rid,a,b,n in db_chunks(text,spans['ai']):
    country=str(n.one('country')); meta=countries[country]
    group=groups['DEC' if meta['country_type']=='decentralized' else 'OTHER']
    group['controllers']+=1
    group['registered_goal_types'].update(str(x.one('type')) for x in n.children('ai_goal'))
    group['scalar_field_names'].update(x.key for x in n.children() if not isinstance(x.value,list))
    for mapping in n.children('country_goal'):
        for target in mapping.children():
            group['diplomatic_target_entries']+=1
            group['initialized_targets']+=target.one('initialized')=='yes'
            group['secret_goal_initialized_targets']+=target.one('secret_goal_initialized')=='yes'
            ident=str(target.one('target'))
            group['targets_without_populated_country']+=ident not in countries or not countries[ident]['populated']
out=dict(source=str(SOURCE),cohorts=groups,
    qualification='Registered AI goal types and per-target diplomatic threat/attitude data. Not an execution queue, call frequency, timing, or causal proof.')
with (LAB/'NATIVE_GOAL_INVENTORY.json').open('x',encoding='utf-8') as f:json.dump(out,f,indent=2)
print(json.dumps({k:{a:b for a,b in v.items() if a!='scalar_field_names'} for k,v in groups.items()},indent=2))
