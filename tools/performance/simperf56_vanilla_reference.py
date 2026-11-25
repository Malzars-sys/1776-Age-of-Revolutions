"""Optional Steam 1836 reference, isolated profile, same observer and GUI only."""
from pathlib import Path
from collections import Counter
import argparse, json, re, shutil
from simperf56_ai_cohorts import LAB, PREVIOUS, PARENT, sha, write, db_chunks
from simperf56_save_state import sections

def profile(label,source=None):
    pp=LAB/'PREPARATION.json';raw=pp.read_bytes();plan=json.loads(raw)
    assert label not in plan['profiles']
    path=LAB/'profiles'/label;assert not path.exists();path.mkdir()
    settings=(PARENT/'runtime/MAIN2_20261117T022325277Z/SETTINGS.json').read_bytes()
    (path/'pdx_settings.json').write_bytes(settings)
    seed=Path('C:/Users/simeo/AppData/Local/Temp/aor1776_simperf56_20261117/profiles/MATURE1')
    for folder in ('shadercache','user_bindings'):
        if (seed/folder).exists():shutil.copytree(seed/folder,path/folder)
    (path/'save games').mkdir()
    if source:
        assert 'Temp' in source.parts and source.is_file()
        shutil.copyfile(source,path/'save games'/source.name)
        assert sha(source)==sha(path/'save games'/source.name)
        assert re.search(rb'\bgame_date=1836\.1\.1\b',source.open('rb').read(4096))
    mods=[(PREVIOUS/'telemetry_profile').as_posix()]
    write(path/'content_load.json',dict(enabledMods=[dict(path=x) for x in mods],disabledDLC=[],enabledUGC=[]))
    spec=dict(path=str(path),mods=mods,settings_sha256=sha(path/'pdx_settings.json'),expected_year=1836,
        common_save_sha256=sha(source) if source else None,saved_date='1836.1.1' if source else None,
        reference_scope='Vanilla Steam1836, same executable/DLC/settings, common telemetry+GUI only; production mod absent')
    plan['profiles'][label]=spec;(LAB/('PLAN_BEFORE_'+label+'.json')).write_bytes(raw)
    assert pp.read_bytes()==raw
    pp.write_text(json.dumps(plan,indent=2,ensure_ascii=False),encoding='utf-8')
    write(LAB/('PROFILE_'+label+'.json'),spec)
    print(json.dumps(spec,indent=2))

def verify(label,path,phase,expected):
    text=path.read_text(encoding='utf-8-sig');ss=sections(text)
    ai={str(n.one('country')):dict(id=rid,enabled=n.one('enabled'))
        for rid,a,b,n in db_chunks(text,ss['ai']) if n.one('country') is not None}
    wanted='yes' if expected=='ON' else 'no'
    differences={i:r for i,r in ai.items() if r['enabled']!=wanted}
    assert not differences,differences
    out=dict(trial=label,phase=phase,date=re.search(r'\bgame_date=([\d.]+)',text[:4096])[1],
        save=str(path),sha256=sha(path),controllers=len(ai),enabled_counts=dict(Counter(r['enabled'] for r in ai.values())),
        unexpected_flags=differences,expected_flag=wanted,actual=ai,scope='Vanilla1836 reference, not the 1776 controller inventory')
    write(LAB/(label+'_'+phase+'_AI_PROOF.json'),out)
    print(json.dumps({k:v for k,v in out.items() if k!='actual'},indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('action',choices=('profile','verify'));ap.add_argument('--label',required=True)
    ap.add_argument('--save',type=Path);ap.add_argument('--phase',choices=('PRE','POST'));ap.add_argument('--expected',choices=('ON','OFF'));a=ap.parse_args()
    if a.action=='profile':profile(a.label,a.save)
    else:verify(a.label,a.save,a.phase,a.expected)
