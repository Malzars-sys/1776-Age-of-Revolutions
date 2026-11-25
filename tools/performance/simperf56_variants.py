"""Prepare one diagnostic variable and identical initial-save trial profiles."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil,sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
from validate_diplomacy_ottoman_1776 import parse
REPORT=ROOT/'docs/reports/performance/INITIAL_SIMULATION_ISSUE56_2026_11_17'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
planpath=REPORT/'PREPARATION.json';oldplan=planpath.read_bytes();plan=json.loads(oldplan)
lab=Path(plan['lab']);base=Path(plan['main_frozen']);diag=lab/'diagnostic_no_hre_daily_guard'
assert not diag.exists(),'Keep existing variants.'
manifest=json.loads((lab/'FROZEN_MANIFEST.json').read_text())['files']
assert all(sha(base/rel)==spec['sha256'] for rel,spec in manifest.items())
shutil.copytree(base,diag)
relative='common/scripted_effects/1776_imperial_constitution.txt'
path=diag/relative;original=path.read_bytes();text=original.decode('utf-8-sig')
nodes=[n for n in parse(text) if n.key=='aor1776_hre_schedule_membership_guard']
assert len(nodes)==1
node=nodes[0]
replacement='aor1776_hre_schedule_membership_guard = {\n # ISSUE56 DIAGNOSTIC ONLY: do not reschedule daily guard.\n # Monthly HRE hooks, initial history and every other helper remain intact.\n}'
updated=text[:node.start]+replacement+text[node.end:]
assert len(parse(updated))==len(parse(text))
path.write_bytes((b'\xef\xbb\xbf' if original.startswith(b'\xef\xbb\xbf') else b'')+updated.encode('utf-8'))
differences=[rel for rel,spec in manifest.items() if sha(diag/rel)!=spec['sha256']]
assert differences==[relative]
initial=lab/'profiles/MAIN1/save games/royaume de france_1776_01_01.v3'
assert initial.is_file()
settings=(REPORT/'runtime/MAIN1_20261117T015301024Z/SETTINGS.json').read_bytes()
seed=lab/'profiles/MAIN1'
for label,mount in [('MAIN2',base),('MAIN3',base),('HRE1',diag),('HRE2',diag)]:
    profile=lab/'profiles'/label;profile.mkdir()
    (profile/'pdx_settings.json').write_bytes(settings)
    for folder in ('shadercache','user_bindings'):
        if (seed/folder).exists():shutil.copytree(seed/folder,profile/folder)
    (profile/'save games').mkdir();shutil.copyfile(initial,profile/'save games'/initial.name)
    mods=[{'path':p.as_posix()} for p in (mount,Path(plan['telemetry']))]
    (profile/'content_load.json').write_text(json.dumps(dict(enabledMods=mods,disabledDLC=[],enabledUGC=[]),indent=2),encoding='utf-8')
    plan['profiles'][label]=dict(path=str(profile),mods=[p['path'] for p in mods],settings_sha256=sha(profile/'pdx_settings.json'),expected_year=1776,common_save_sha256=sha(initial))
# Correct only the common instrumentation metadata before the measured series.
# The pilot's original bytes and log warning are retained for transparency.
meta=Path(plan['telemetry'])/'.metadata/metadata.json';oldmeta=meta.read_bytes()
archive=REPORT/'pilot_instrumentation_metadata.json';assert not archive.exists();archive.write_bytes(oldmeta)
metadata=json.loads(oldmeta);metadata['id']=''
assert meta.read_bytes()==oldmeta
meta.write_text(json.dumps(metadata,indent=2),encoding='utf-8')
evidence=dict(utc=datetime.now(timezone.utc).isoformat(),diagnostic=str(diag),changed_files=differences,
 source_sha256=hashlib.sha256(original).hexdigest(),diagnostic_sha256=sha(path),common_save=str(initial),common_save_sha256=sha(initial),
 diagnostic_semantics='Daily HRE guard rescheduling disabled only; existing first-day pending event may fire once. Monthly HRE remains. Intentionally NOT gameplay equivalent, NOT a proposed fix.',
 pilot_metadata_sha256=hashlib.sha256(oldmeta).hexdigest(),corrected_common_metadata_sha256=sha(meta),
 instrumentation_hashes={str(p.relative_to(Path(plan['telemetry']))):sha(p) for p in Path(plan['telemetry']).rglob('*') if p.is_file()})
plan['diagnostics'].append(evidence)
(REPORT/'PREPARATION_BEFORE_VARIANTS.json').write_bytes(oldplan)
assert planpath.read_bytes()==oldplan
planpath.write_text(json.dumps(plan,indent=2,ensure_ascii=False),encoding='utf-8')
with (REPORT/'DIAGNOSTIC_PREPARATION.json').open('x',encoding='utf-8') as out:json.dump(evidence,out,indent=2,ensure_ascii=False)
print(json.dumps(evidence,indent=2,ensure_ascii=False))
