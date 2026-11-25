"""Read serialized flags and native task cursors, without attributing CPU cost."""
from pathlib import Path
from collections import Counter
import json, re
from simperf56_save_state import sections, parse

LAB = Path('C:/Users/simeo/AppData/Local/Temp/aor56_state_20261117')
out = {'qualification': ('Serialized state only. Flags are not all temporary modifiers; '
    'expiry fields have different semantics. update_index values do not prove '
    'queue length, cache cost, repeated work, or causality. '
    'The old STATE_*.dated_data.aor_variable_names used name= rather than flag= '
    'and is not a valid count; this extraction uses the actual flag= field.')}
for label in ('INITIAL', 'JULY', 'MATURE'):
    meta = json.loads((LAB/('STATE_'+label+'.json')).read_text(encoding='utf-8'))
    text = Path(meta['path']).read_text(encoding='utf-8-sig')
    spans = sections(text)
    a, b = spans['tasks']
    node = parse(text[a:b])[0]
    tasks = node.children()
    cursors = {n.key: {x.key:x.value for x in n.children()} for n in tasks if n.children()}
    flags = Counter(re.findall(r'\bflag=(aor1776_[\w]+)', text))
    out[label] = dict(date=meta['date'], sha256=meta['sha256'],
        native_task_entries=len(tasks), nonempty_tasks=cursors,
        aor_flag_occurrences=sum(flags.values()), unique_aor_flags=len(flags),
        selected_flags={k:flags[k] for k in ('aor1776_ai_regional_cooldown',
            'aor1776_hre_membership_guard_scheduled','aor1776_r3_startup_scheduled',
            'aor1776_french_approach_scheduled')},
        expiry_date_fields=len(re.findall(r'\bexpiry_date=', text)),
        expiration_date_fields=len(re.findall(r'\bexpiration_date=', text)))
with (LAB/'PERSISTENT_STATE_COMPARISON.json').open('x',encoding='utf-8') as f:
    json.dump(out,f,indent=2,ensure_ascii=False)
print(json.dumps(out,indent=2))
