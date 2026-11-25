"""Prepare new isolated comparisons on the explicitly requested second display."""
from pathlib import Path
import copy, hashlib, json, shutil
from datetime import datetime, timezone
from simperf56_ai_cohorts import LAB

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))

planpath = LAB/'PREPARATION.json'
before = planpath.read_bytes()
plan = read(planpath)
basepath = Path(plan['profiles']['ECNQ3']['path'])/'pdx_settings.json'
base = basepath.read_bytes()
assert sha(basepath) == plan['profiles']['ECNQ3']['settings_sha256']
settings = json.loads(base)
settings['Graphics']['resolution'] = '1600x900'
settings['Graphics']['display_index'] = '1'
assert settings['Graphics']['display_mode'] == 'windowed'
actual = read(LAB/'profiles/ECNQ2/pdx_settings.json')
assert actual['Graphics']['resolution'] == '1600x900'
assert actual['Graphics']['display_index'] == '1'
payload = json.dumps(settings, indent=2, ensure_ascii=False).encode('utf-8')
settings_sha = hashlib.sha256(payload).hexdigest()
pairs = [('ECNG1','ECNQ3'), ('SCORG1','SCORQ3'),
         ('SCORG2','SCORQ3'), ('ECNG2','ECNQ3'),
         ('VAN_OFFG1','VAN_OFFQ2'), ('VAN_ONG1','VAN_ONQ2')]
specs = {}
for label, parent in pairs:
    assert label not in plan['profiles']
    old = plan['profiles'][parent]
    profile = LAB/'profiles'/label
    assert not profile.exists()
    source = Path(old['seed_path'])
    assert sha(source) == old['common_save_sha256']
    (profile/'save games').mkdir(parents=True)
    seed = profile/'save games'/source.name
    shutil.copyfile(source, seed)
    for name in ('content_load.json',):
        shutil.copyfile(Path(old['path'])/name, profile/name)
    shutil.copytree(Path(old['path'])/'user_bindings', profile/'user_bindings')
    (profile/'pdx_settings.json').write_bytes(payload)
    assert sha(seed) == old['common_save_sha256']
    spec = copy.deepcopy(old)
    spec.update(path=str(profile), seed_path=str(seed), settings_sha256=settings_sha,
                display_scope='SECONDARY_GAOMON_ONLY_1600x900_WINDOWED',
                comparison_group='secondary_mod_ABBA_20261119' if old['expected_year']==1776 else 'secondary_vanilla_OFF_ON_20261119',
                derived_from_unrun_profile=parent)
    specs[label] = spec
    plan['profiles'][label] = spec
with (LAB/'SECONDARY_DISPLAY_PLAN_BEFORE_20261119.json').open('xb') as f: f.write(before)
assert planpath.read_bytes() == before
planpath.write_text(json.dumps(plan, indent=2), encoding='utf-8')
receipt = dict(utc=datetime.now(timezone.utc).isoformat(),
    user_request='Use exclusively the smaller second display; leave the 4K OLED free.',
    settings_sha256=settings_sha, previous_settings_sha256=hashlib.sha256(base).hexdigest(),
    changed_settings={'Graphics.resolution':['1920x1080','1600x900'],
                      'Graphics.display_index':['not explicitly set','1 (GAOMON156 PRO)']},
    native_UI_display_selection_verified=True,
    observed_window_bounds={'x':-1762,'y':278,'width':1604,'height':960},
    desktop_display_resolution_changed=False,
    ECNQ2='Display setup only; zero simulated DAY markers; no performance result accepted.',
    order=[x[0] for x in pairs], profiles=specs)
with (LAB/'SECONDARY_DISPLAY_SETUP_20261119.json').open('x', encoding='utf-8') as f:
    json.dump(receipt, f, indent=2)
with (LAB/'RUN_STATE.md').open('a', encoding='utf-8') as f:
    f.write('\n\n2026-11-19 — Reprise: SCORQ1 complet 52/101/174 s, 646 yes et objectifs intacts dans autosave avril. ECNQ1 interrompu sans DAY; pas de témoin contemporain pour SCORQ1. Vanilla Q1: ON13/23/45, OFF10/18/34, POST natifs confirmés; NIC né dans ON seulement, tous contrôleurs présents avec flag attendu.\n')
    f.write('Utilisateur demande exclusivement écran secondaire GAOMON, grand 4K OLED libre. ECNQ2 réservé au réglage écran, zéro DAY, ne pas traiter comme benchmark. Nouvelle série dédiée 1600x900 fenêtre/display_index1: ECNG1→SCORG1→SCORG2→ECNG2, puis VAN_OFFG1→VAN_ONG1. Réglages identiques entre nouveaux cas; ne pas agréger avec anciens 1920x1080. Aucun fichier normal remplacé.\n')
print(json.dumps({'settings_sha256':settings_sha,'order':receipt['order']}))
