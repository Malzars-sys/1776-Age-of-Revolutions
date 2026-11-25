"""Single diagnostic category: 12 modded building priority callbacks, native AI intact."""
from pathlib import Path
import hashlib, json, re, shutil, sys
from simperf56_ai_cohorts import LAB, PREVIOUS, SOURCE
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from validate_diplomacy_ottoman_1776 import parse
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
frozen=Path(json.loads((LAB/'SOURCE_PLAN.json').read_text())['main_frozen'])
inventory=json.loads((LAB/'MODDED_AI_SCORE_CALLBACK_INVENTORY_20261118.json').read_text())
assert inventory['blocks']==12 and inventory['files']==9
overlay=LAB/'building_priority_bases_20261118';assert not overlay.exists();overlay.mkdir()
changes=[]
for relative in sorted({r['file'] for r in inventory['rows']}):
    src=frozen/relative;raw=src.read_bytes();text=raw.decode('utf-8-sig');edits=[]
    for building in parse(text):
        for value in building.children('ai_value'):
            block=text[value.start:value.end]
            if not re.search(r'\baor1776_ai_\w+',block):continue
            base=value.one('value');assert isinstance(base,str) and re.fullmatch(r'\d+(?:\.\d+)?',base)
            edits.append((value.start,value.end,'ai_value = '+base))
            changes.append(dict(file=relative,building=building.key,base=base,line=text.count('\n',0,value.start)+1,
                original_block_sha256=hashlib.sha256(block.encode('utf-8')).hexdigest()))
    assert edits
    changed=text
    for a,b,replacement in sorted(edits,reverse=True):changed=changed[:a]+replacement+changed[b:]
    target=overlay/relative;target.parent.mkdir(parents=True,exist_ok=True)
    with target.open('xb') as f:f.write((b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'')+changed.encode('utf-8'))
    for row in changes:
        if row['file']==relative:row.update(original_file_sha256=sha(src),diagnostic_file_sha256=sha(target))
assert len(changes)==12
assert {(r['file'],r['building'],r['base']) for r in changes}=={(r['file'],r['building'],r['initial_value']) for r in inventory['rows']}
raw=SOURCE.read_bytes();text=raw.decode('utf-8-sig')
assert sha(SOURCE)=='387a363748cecd677229d4d03e98c6699830a1da471416491fb6233184d93ed2'
changed,n=re.subn(r'(?m)^speed=2\r?$', 'speed=4',text);assert n==1
seed=LAB/'MOD_Q_S0_SPEED5.v3'
with seed.open('xb') as f:f.write((b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'')+changed.encode('utf-8'))
settings=(LAB/'profiles/VAN_OFFQ1/pdx_settings.json').read_bytes()
assert hashlib.sha256(settings).hexdigest()=='718eb8e11996500326bb3753c59f66b8513983bb8fc86e19eb2b782b8caafeaa'
pp=LAB/'PREPARATION.json';before=pp.read_bytes();plan=json.loads(before);specs={}
for label,diag in (('SCORQ1',True),('ECNQ1',False),('ECNQ2',False),('SCORQ2',True)):
    assert label not in plan['profiles']
    profile=LAB/'profiles'/label;assert not profile.exists();(profile/'save games').mkdir(parents=True)
    shutil.copyfile(seed,profile/'save games'/seed.name)
    (profile/'pdx_settings.json').write_bytes(settings)
    shutil.copytree(LAB/'profiles/VAN_OFF3/user_bindings',profile/'user_bindings')
    mods=[frozen.as_posix(),(PREVIOUS/'telemetry_profile').as_posix()]+([overlay.as_posix()] if diag else [])
    (profile/'content_load.json').write_text(json.dumps(dict(enabledMods=[{'path':x} for x in mods],disabledDLC=[],enabledUGC=[]),indent=2),encoding='utf-8')
    spec=dict(path=str(profile),mods=mods,settings_sha256=sha(profile/'pdx_settings.json'),expected_year=1776,
        saved_date='1776.1.1',common_save_sha256=sha(seed),seed_path=str(profile/'save games'/seed.name),
        expected_enabled='yes',diagnostic_category='12 modded building priority callbacks replaced by their base constants' if diag else None,
        native_objectives_removed=0,controllers_disabled=0,gameplay_preserving=False if diag else None)
    plan['profiles'][label]=spec;specs[label]=spec
with (LAB/'SCORE_BASES_PLAN_BEFORE_20261118.json').open('xb') as f:f.write(before)
assert pp.read_bytes()==before;pp.write_text(json.dumps(plan,indent=2),encoding='utf-8')
with (LAB/'SCORE_BASES_SETUP_20261118.json').open('x',encoding='utf-8') as f:
    json.dump(dict(overlay=str(overlay),source_sha256=sha(SOURCE),prepared_seed_sha256=sha(seed),
        changes=changes,profiles=specs,only_category='modded regional infrastructure priority callbacks in building ai_value',
        other_bytes_in_override_files_retained=True,all_native_ai_objectives_preserved=True,
        all_646_controllers_active_in_source=True,no_ai_frequency_changes=True,
        diagnostic_changes_decision_preferences=True,production_optimization=False,
        runtime_verification_required='Native virtual-file checksums must differ for exactly these nine building files; native autosave must retain the expected controllers and objectives'),f,indent=2)
print(json.dumps({'profiles':list(specs),'callbacks':len(changes),'files':9,'overlay':str(overlay),'order':'SCORQ1 ECNQ1 ECNQ2 SCORQ2'}))
