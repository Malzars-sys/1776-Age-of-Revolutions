"""Create matched all-country AI trials from the verified 1.15.2 witness."""
from collections import Counter
from pathlib import Path
import copy
import re
import shutil

from simperf56_economic_goals_20261118 import goal_state
from simperf56_native_categories_20261123 import LAB as previous_lab, read, sha, write
from simperf56_save_state import sections


LAB = previous_lab.with_name('aor56_global_ai_20261124')
EXPECTED = 646
ENABLED = re.compile(r'(?m)^([ \t]*enabled=)yes(?=\r?$)')
DISABLED = re.compile(r'(?m)^([ \t]*enabled=)no(?=\r?$)')


def prepare():
    assert not LAB.exists(), 'Preserve any previous preparation and run.'
    source_plan = previous_lab/'PREPARATION.json'
    plan = read(source_plan)
    assert sha(plan['executable']) == plan['executable_sha256'], 'Requalify the engine binary.'
    parent = plan['profiles']['NAC2']
    assert parent['expected_enabled'] == 'yes' and parent['native_disabled_define'] is None
    assert parent['matching_steam_gui'] and parent['native_ui_autostart']
    source = Path(parent['seed_path'])
    assert sha(source) == parent['common_save_sha256']
    (prior_run,) = (previous_lab/'runs').glob('NAC2_*')
    settings = prior_run/'SETTINGS.json'
    content = prior_run/'CONTENT_LOAD.json'
    assert sha(settings) == parent['settings_sha256']
    assert [item['path'] for item in read(content)['enabledMods']] == parent['mods']
    assert sha(parent['native_define_file']) == parent['native_define_sha256']

    raw = source.read_bytes()
    text = raw.decode('utf-8-sig')
    start, end = sections(text)['ai']
    active = text[start:end]
    inactive, changes = ENABLED.subn(r'\g<1>no', active)
    assert changes == EXPECTED and not DISABLED.search(active)
    assert DISABLED.sub(r'\g<1>yes', inactive) == active
    modified = text[:start]+inactive+text[end:]
    bom = b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b''
    assert bom+text.encode('utf-8') == raw
    variants = {'GON1': (raw, 'yes'), 'GOF1': (bom+modified.encode('utf-8'), 'no')}

    plan.update(lab=str(LAB), profiles={})
    (LAB/'requests').mkdir(parents=True)
    (LAB/'evidence').mkdir()
    expected = goal_state(text)
    assert Counter(c['enabled'] for c in expected.values()) == {'yes': EXPECTED}
    assert expected == {country: dict(c, enabled='yes') for country, c in goal_state(modified).items()}
    for name, (save, flag) in variants.items():
        profile = LAB/'profiles'/name
        seed = profile/'save games'/source.name
        seed.parent.mkdir(parents=True)
        seed.write_bytes(save)
        shutil.copyfile(settings, profile/'pdx_settings.json')
        shutil.copyfile(content, profile/'content_load.json')
        shutil.copytree(Path(parent['path'])/'user_bindings', profile/'user_bindings')
        spec = copy.deepcopy(parent)
        spec.update(path=str(profile), seed_path=str(seed), common_save_sha256=sha(seed),
                    expected_enabled=flag, controllers_disabled=EXPECTED if flag == 'no' else 0,
                    gameplay_preserving=flag == 'yes', comparison_group='global_country_ai_1.15.2_20261124',
                    setup_proof=str(LAB/'SETUP.json'), repetition_of='NAC2' if flag == 'yes' else None)
        plan['profiles'][name] = spec

    shutil.copyfile(previous_lab/'run_profile_trial.ps1', LAB/'run_profile_trial.ps1')
    write(LAB/'SETUP.json', dict(source=str(source), source_sha256=sha(source),
          controller_ids=sorted(expected), treatment_only_changes_enabled_flags=changes,
          matched_settings_sha256=sha(settings), matched_content_sha256=sha(content),
          profiles=plan['profiles']))
    write(LAB/'PREPARATION.json', plan)
    print(f'Prepared GON1 and GOF1 with {changes} country AI flags as the sole save difference.')


if __name__ == '__main__':
    prepare()
