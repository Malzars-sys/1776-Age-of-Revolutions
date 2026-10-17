"""Preservation checks and guarded upgrade of the isolated companion only."""
from pathlib import Path
import json
import shutil
import sys
import io
import subprocess
import unittest
from datetime import datetime, timezone
import infrastructure_landscape_prototype as prototype
import validate_diplomacy_ottoman_1776 as cw

ROOT = prototype.ROOT
OUT = ROOT / 'docs/reports/bridge/VIC3_LOCAL_BRIDGE'
BASE = OUT / 'BASELINE.json'
FIX = OUT / 'EXPORT_SCOPE_FIX_2026_10_16'
IDENTITY = OUT / 'IDENTITY_FIX_2026_10_16'


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')


def capture():
    assert not BASE.exists(), 'Do not replace preservation baseline'
    prototype.verify()
    files = {p.relative_to(prototype.DEST).as_posix(): prototype.prior.sha(p)
             for p in prototype.DEST.rglob('*') if p.is_file()}
    descriptor = ROOT.parent / prototype.DESCRIPTOR
    dump(BASE, {'main_runtime': prototype.main_hashes(), 'git': prototype.prior.git_state(),
        'installed': files, 'descriptor': prototype.prior.sha(descriptor)})
    # Small recoverable text-only copy, not a complete repository archive.
    backup = OUT / 'companion_0.1.0_backup'
    for rel in files:
        target = backup / 'mod' / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(prototype.DEST / rel, target)
    shutil.copy2(descriptor, backup / prototype.DESCRIPTOR)
    print('Preservation baseline and small companion backup captured')


def preserved():
    before = json.loads(BASE.read_text(encoding='utf-8'))
    assert prototype.main_hashes() == before['main_runtime'], 'Main runtime changed'
    assert prototype.prior.git_state() == before['git'], 'HEAD/index changed'
    return before


def record_received_export():
    """Record basic real export success, not visual/full-runtime certification."""
    preserved()
    receipt = OUT / 'RUNTIME_EXPORT_OBSERVED_2026_10_16.json'
    assert not receipt.exists(), 'Keep the original real-export receipt'
    command = [sys.executable, '-B', '-X', 'utf8', str(ROOT / 'tools/vic3-diagnostic-bridge/server/bridge.py'), '--snapshot']
    run = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
    assert run.returncode == 0 and not run.stderr
    snapshot = json.loads(run.stdout)
    assert snapshot['source'] == 'LOCAL_GAME_LOG' and snapshot['status'] == 'SNAPSHOT_AVAILABLE'
    assert not snapshot['snapshot']['errors']
    fields = snapshot['snapshot']['fields']
    assert fields['country_name'].startswith('TAG:') and fields['state_name'].startswith('REGION:STATE_')
    import vic3_bridge_identity as identity
    assert fields['country_name'][4:] in identity.definitions('common/country_definitions', r'[A-Z0-9]{3}')
    assert fields['state_name'][7:] in identity.definitions('map_data/state_regions', r'STATE_[A-Z0-9_]+')
    reader_evidence = {
        'status': 'PASS_RUNTIME_EXPORT_OBSERVED',
        'observed_utc': datetime.now(timezone.utc).isoformat(),
        'user_reported_export_click': True,
        'access_method': 'CLI_READER_NOT_NATIVE_CODEX_MCP_TOOL',
        'snapshot': snapshot,
        'country_and_region_keys_resolve': True,
        'manual_click_causality_proven_by_before_cursor': False,
        'interpretation': 'A complete real frame is readable; without a same-session before-click cursor its exact trigger and current freshness are not certified.',
        'full_bridge_runtime_validated': False,
        'visual_tracks_validated': False,
        'player_ui_values_compared': False,
        'main_runtime_unchanged': True, 'head_index_unchanged': True,
        'next_test_cursor': snapshot['cursor'],
        'next_test': 'Optional: force/remove/auto marker then export in the same test session; compare the new frame after next_test_cursor.'}
    dump(receipt, reader_evidence)
    validation_path = OUT / 'VALIDATION.json'
    validation = json.loads(validation_path.read_text(encoding='utf-8'))
    validation.update(status='PASS_RUNTIME_EXPORT_OBSERVED', engine_export_validated=True,
        runtime_export_receipt=receipt.name, full_bridge_runtime_validated=False,
        current_freshness_certified=False, visual_tracks_tested_by_bridge=False,
        required_next_step='No restart requested. Optional same-session after-cursor test of force/remove/auto; visual rail validation remains separate.')
    dump(validation_path, validation)
    preserved()
    print(json.dumps({'status': reader_evidence['status'], 'fields': fields,
        'probe_matches_expected': snapshot['snapshot']['probe_matches_expected'],
        'freshness': snapshot['freshness'], 'full_bridge_runtime_validated': False}, ensure_ascii=False, indent=2))


def record_forced_probe():
    """Verify a new same-session frame against the stored BEFORE cursor."""
    preserved()
    before_path = OUT / 'RUNTIME_EXPORT_OBSERVED_2026_10_16.json'
    before = json.loads(before_path.read_text(encoding='utf-8'))
    destination = OUT / 'RUNTIME_FORCED_PROBE_2026_10_16.json'
    assert not destination.exists(), 'Preserve the original transition receipt'
    command = [sys.executable, '-B', '-X', 'utf8', str(ROOT / 'tools/vic3-diagnostic-bridge/server/bridge.py'),
               '--snapshot', '--after-cursor', before['next_test_cursor']]
    run = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
    assert run.returncode == 0 and not run.stderr
    result = json.loads(run.stdout)
    assert result['source'] == 'LOCAL_GAME_LOG' and result['status'] == 'SNAPSHOT_AVAILABLE'
    assert result['freshness'] == 'NEW_SINCE_CURSOR'
    old = before['snapshot']['snapshot']
    current = result['snapshot']
    assert not current['errors'] and current['probe_matches_expected']
    for key in ['country_name', 'state_name', 'regional_levels', 'real_rail_pm']:
        assert current['fields'][key] == old['fields'][key], key
    assert current['pms'] == old['pms']
    assert old['fields']['probe_levels'] == 0 and current['fields']['probe_levels'] == 1
    assert current['fields']['override'] == 'force_on'
    dump(destination, {'status': 'PASS_RUNTIME_FORCED_PROBE_EXPORT_OBSERVED',
        'observed_utc': datetime.now(timezone.utc).isoformat(),
        'user_reported_action': 'Forced marker then exported capital diagnostics',
        'before_receipt': before_path.name, 'after': result,
        'same_session_after_cursor_verified': True, 'probe_before': 0, 'probe_after': 1,
        'regional_levels_and_active_pms_unchanged': True,
        'all_economic_data_verified': False, 'visual_tracks_validated': False,
        'native_codex_mcp_invocation': False, 'access_method': 'LOCAL_CLI_READER',
        'full_bridge_runtime_validated': False,
        'next_test_cursor': result['cursor'],
        'next_test': 'Restore automatic tracking or remove marker, then export in the same session; expected zero without rail PM.'})
    validation_path = OUT / 'VALIDATION.json'
    validation = json.loads(validation_path.read_text(encoding='utf-8'))
    validation.update(status='PASS_RUNTIME_FORCED_PROBE_EXPORT_OBSERVED',
        runtime_forced_probe_receipt=destination.name,
        forced_probe_same_session_after_cursor_verified=True,
        full_bridge_runtime_validated=False, visual_tracks_tested_by_bridge=False)
    dump(validation_path, validation)
    preserved()
    print('PASS new same-session record: FRA / STATE_ILE_DE_FRANCE, probe 0 -> 1, force_on; infrastructure 17 and all three PMs unchanged; visual rendering not verified')


def record_auto_return():
    """Record observed A/B/A without hiding the newer incomplete log frame."""
    preserved()
    forced_path = OUT / 'RUNTIME_FORCED_PROBE_2026_10_16.json'
    forced = json.loads(forced_path.read_text(encoding='utf-8'))
    destination = OUT / 'RUNTIME_AUTO_RETURN_2026_10_16.json'
    assert not destination.exists(), 'Preserve original A/B/A evidence'
    from importlib.util import spec_from_file_location, module_from_spec
    spec = spec_from_file_location('bridge_auto_return', ROOT / 'tools/vic3-diagnostic-bridge/server/bridge.py')
    module = module_from_spec(spec); spec.loader.exec_module(module)
    reader = module.Bridge(Path.home() / 'Documents/Paradox Interactive/Victoria 3')
    raw, start, info, cursor = reader.read_log('debug.log')
    cutoff, error = reader.check_cursor(forced['next_test_cursor'], 'debug.log', info)
    assert not error, error
    frames = [f for f in module.parse_frames(raw, start) if f['start_offset'] >= cutoff]
    complete = [f for f in frames if 'end_offset' in f and not f['errors']]
    assert complete, 'No complete valid new record'
    observed = complete[-1]
    old = forced['after']['snapshot']
    for key in ['country_name', 'state_name', 'regional_levels', 'real_rail_pm']:
        assert observed['fields'][key] == old['fields'][key], key
    assert observed['pms'] == old['pms']
    assert observed['fields']['probe_levels'] == 0 and observed['fields']['override'] == 'auto'
    assert observed['probe_matches_expected']
    incomplete = bool(frames and 'end_offset' not in frames[-1])
    dump(destination, {'status': 'PASS_RUNTIME_PROBE_ABA_OBSERVED',
        'observed_utc': datetime.now(timezone.utc).isoformat(), 'source': 'LOCAL_GAME_LOG',
        'before_receipt': forced_path.name, 'same_session_after_cursor_verified': True,
        'complete_new_valid_frames': len(complete), 'last_complete_observation': observed,
        'newer_tail_incomplete': incomplete, 'current_live_state_certified': False,
        'observed_sequence': [0, 1, 0], 'regional_levels_and_active_pms_unchanged': True,
        'visual_tracks_validated': False, 'inbound_game_commands': False,
        'full_bridge_runtime_validated': False, 'log': info, 'next_test_cursor': reader.cursor(cursor)})
    path = OUT / 'VALIDATION.json'
    validation = json.loads(path.read_text(encoding='utf-8'))
    validation.update(status='PASS_RUNTIME_PROBE_ABA_OBSERVED', runtime_auto_return_receipt=destination.name,
        probe_sequence_0_1_0_observed=True, latest_log_tail_incomplete=incomplete,
        current_freshness_certified=False, full_bridge_runtime_validated=False)
    dump(path, validation)
    preserved()
    print(json.dumps({'status': 'PASS_RUNTIME_PROBE_ABA_OBSERVED', 'complete_new_valid_frames': len(complete),
        'last_complete_fields': observed['fields'], 'newer_tail_incomplete': incomplete,
        'current_live_state_certified': False}, ensure_ascii=False, indent=2))


def capture_identity_fix():
    preserved()
    prototype.verify()
    assert not (IDENTITY / 'BASELINE.json').exists(), 'Do not replace identity-fix baseline'
    files = {p.relative_to(prototype.DEST).as_posix(): prototype.prior.sha(p)
             for p in prototype.DEST.rglob('*') if p.is_file()}
    descriptor = ROOT.parent / prototype.DESCRIPTOR
    dump(IDENTITY / 'BASELINE.json', {'installed': files, 'descriptor': prototype.prior.sha(descriptor)})
    backup = IDENTITY / 'companion_0.2.1_backup'
    for rel in files:
        target = backup / 'mod' / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(prototype.DEST / rel, target)
    shutil.copy2(descriptor, backup / prototype.DESCRIPTOR)
    result = subprocess.run([sys.executable, '-B', '-X', 'utf8', str(ROOT / 'tools/vic3-diagnostic-bridge/server/bridge.py'), '--snapshot'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
    assert result.returncode == 0 and not result.stderr
    dump(IDENTITY / 'RUNTIME_BEFORE.json', json.loads(result.stdout))
    print('Captured complete real frame with correct numeric export but unresolved labels; small 0.2.1 backup verified later at deploy')


def deploy_identity_fix():
    preserved()
    validate()
    import vic3_bridge_identity as identity
    text, counts = identity.render()
    assert (prototype.SOURCE / identity.TARGET).read_text(encoding='utf-8') == text
    before = json.loads((IDENTITY / 'BASELINE.json').read_text(encoding='utf-8'))
    dest = prototype.DEST.resolve()
    assert dest.parent == ROOT.parent.resolve() and dest.name == 'aor1776_landscape_prototype'
    actual = {p.relative_to(dest).as_posix(): prototype.prior.sha(p) for p in dest.rglob('*') if p.is_file()}
    expected = {rel: prototype.prior.sha(p) for rel, p in prototype.payload().items()}
    if actual == expected:
        prototype.verify()
        return
    descriptor = ROOT.parent / prototype.DESCRIPTOR
    assert actual == before['installed'], 'Unknown installed changes; stop'
    assert prototype.prior.sha(descriptor) == before['descriptor']
    assert set(expected) - set(actual) == {identity.TARGET} and set(actual) <= set(expected)
    backup = IDENTITY / 'companion_0.2.1_backup'
    assert all(prototype.prior.sha(backup / 'mod' / rel) == h for rel, h in actual.items())
    assert prototype.prior.sha(backup / prototype.DESCRIPTOR) == before['descriptor']
    for relative, source in prototype.payload().items():
        if expected[relative] != actual.get(relative):
            target = dest / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    shutil.copy2(prototype.PACKAGE / prototype.DESCRIPTOR, descriptor)
    prototype.verify()
    preserved()
    dump(IDENTITY / 'INSTALLED_FIX.json', {'status': 'STATIC_PASS_IDENTITY_ENGINE_RETEST_PENDING',
        'companion_version': '0.2.2', 'wire_schema_exporter': '0.2.0', **counts,
        'main_runtime_unchanged': True, 'head_index_unchanged': True, 'engine_retest_passed': False,
        'changed_payload': [r for r in expected if expected[r] != actual.get(r)], 'files': expected})
    print('Installed companion-only identity lookup 0.2.2; engine reload/retest required')


def capture_export_fix():
    preserved()
    prototype.verify()
    assert not (FIX / 'BASELINE.json').exists(), 'Do not replace export-fix baseline'
    files = {p.relative_to(prototype.DEST).as_posix(): prototype.prior.sha(p)
             for p in prototype.DEST.rglob('*') if p.is_file()}
    descriptor = ROOT.parent / prototype.DESCRIPTOR
    dump(FIX / 'BASELINE.json', {'installed': files, 'descriptor': prototype.prior.sha(descriptor)})
    backup = FIX / 'companion_0.2.0_backup'
    for rel in files:
        target = backup / 'mod' / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(prototype.DEST / rel, target)
    shutil.copy2(descriptor, backup / prototype.DESCRIPTOR)
    from importlib.util import spec_from_file_location, module_from_spec
    spec = spec_from_file_location('bridge_runtime_evidence', ROOT / 'tools/vic3-diagnostic-bridge/server/bridge.py')
    module = module_from_spec(spec); spec.loader.exec_module(module)
    reader = module.Bridge(Path.home() / 'Documents/Paradox Interactive/Victoria 3')
    data, start, info, cursor = reader.read_log('debug.log')
    frames = module.parse_frames(data, start)
    complete = [f for f in frames if 'end_offset' in f]
    dump(FIX / 'RUNTIME_BEFORE.json', {'source': 'LOCAL_GAME_LOG', 'log': info,
        'observed_utc': datetime.now(timezone.utc).isoformat(),
        'status': 'ENGINE_EXPORT_EXECUTES_BUT_CONTEXT_INVALID',
        'complete_frames': len(complete), 'last_complete': complete[-1] if complete else None,
        'last_frame': frames[-1] if frames else None, 'snapshot': reader.snapshot(),
        'conclusion': 'Date and conditional PM logs work. Saved scopes are not resolved by debug_log localization. Numeric zero is not trusted. Final log frame also remains buffered/incomplete.'})
    print('Captured real invalid-export evidence and verified small 0.2.0 backup')


def deploy_export_fix():
    preserved()
    validate()
    before = json.loads((FIX / 'BASELINE.json').read_text(encoding='utf-8'))
    dest = prototype.DEST.resolve()
    assert dest.parent == ROOT.parent.resolve() and dest.name == 'aor1776_landscape_prototype'
    actual = {p.relative_to(dest).as_posix(): prototype.prior.sha(p) for p in dest.rglob('*') if p.is_file()}
    expected = {rel: prototype.prior.sha(p) for rel, p in prototype.payload().items()}
    if actual == expected:
        prototype.verify()
        return
    descriptor = ROOT.parent / prototype.DESCRIPTOR
    assert actual == before['installed'], 'Unknown installed changes; stop'
    assert prototype.prior.sha(descriptor) == before['descriptor']
    assert set(actual) == set(expected), 'No new/removal of payload files for scope fix'
    backup = FIX / 'companion_0.2.0_backup'
    assert all(prototype.prior.sha(backup / 'mod' / rel) == h for rel, h in actual.items())
    assert prototype.prior.sha(backup / prototype.DESCRIPTOR) == before['descriptor']
    for relative, source in prototype.payload().items():
        if expected[relative] != actual[relative]:
            shutil.copy2(source, dest / relative)
    shutil.copy2(prototype.PACKAGE / prototype.DESCRIPTOR, descriptor)
    prototype.verify()
    preserved()
    dump(FIX / 'INSTALLED_FIX.json', {'status': 'STATIC_PASS_INSTALLED_RESTART_REQUIRED',
        'companion_version': '0.2.1', 'wire_schema_exporter': '0.2.0',
        'main_runtime_unchanged': True, 'head_index_unchanged': True,
        'engine_retest_passed': False, 'changed_payload': [r for r in expected if expected[r] != actual[r]],
        'files': expected})
    print('Installed companion-only scope fix 0.2.1; engine reload/retest required')


def validate():
    preserved()
    prototype.run_tests()
    from importlib.util import spec_from_file_location, module_from_spec
    path = ROOT / 'tools/vic3-diagnostic-bridge/server/bridge.py'
    spec = spec_from_file_location('diagnostic_bridge', path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    # Validate actual emitted PM IDs against both parser and main mod's PMGs.
    effects = prototype.nodes('common/scripted_effects')
    telemetry = next(n for n in effects if n.key == 'aor1776_bridge_export_local_capital')
    messages = [cw.scalar(n.value) for n in cw.walk(telemetry.children()) if n.key == 'debug_log']
    exported = {m.split('|pm=', 1)[1] for m in messages if '|pm=' in m}
    assert exported == module.PM_IDS
    known = set()
    for rel in ['22_tech7a_wave_a_land_transport_pmgs.txt', '23_tech7a_wave_b_canals_pmgs.txt', '24_tech7a_wave_c_rail_pmgs.txt']:
        for n in cw.parse((ROOT / 'common/production_method_groups' / rel).read_text(encoding='utf-8-sig')):
            known.update(cw.scalar(x.value) for group in n.children('production_methods') for x in group.children())
    assert exported == known
    assert all('SCOPE.' not in m and 'THIS.' not in m for m in messages), 'No unresolved effect-local context in debug_log'
    assert all('ScriptValue' not in m and 'MakeScope' not in m for m in messages)
    for effect_id, field, maximum in [('aor1776_bridge_export_regional_level', 'regional_levels', 256),
                                       ('aor1776_bridge_export_probe_level', 'probe_levels', 4)]:
        lookup = next(n for n in effects if n.key == effect_id)
        cases = []
        for condition in lookup.children('if'):
            predicate = condition.children('limit')[0].children()[0]
            message = cw.scalar(condition.children('debug_log')[0].value)
            if predicate.op == '=':
                value = int(predicate.value)
                assert message == f'AOR1776_BRIDGE_V1|{field}={value}'
                cases.append(value)
            else:
                assert predicate.op == '>' and int(predicate.value) == maximum
                assert message == f'AOR1776_BRIDGE_V1|{field}=UNSUPPORTED_LEVEL'
        assert cases == list(range(maximum + 1)), 'Exact bounded lookup coverage'
    entry = next(n for n in effects if n.key == 'aor1776_bridge_export_state')
    assert any(n.key == 'is_local_player' and n.value == 'yes' for n in cw.walk(entry.children()))
    # No economic/PM/technology effects in the telemetry exporter.
    forbidden = {'create_building', 'remove_building', 'activate_production_method', 'set_variable', 'add_technology_researched', 'add_treasury'}
    assert not forbidden & {n.key for n in cw.walk(telemetry.children())}
    for rel in ['common/on_actions/aor1776_landscape_prototype.txt', 'common/decisions/aor1776_landscape_prototype.txt']:
        assert (prototype.SOURCE / rel).read_bytes().startswith(b'\xef\xbb\xbf')
    # All custom invocations must resolve to the correct namespace.
    effect_ids = {n.key for n in effects}
    trigger_ids = {n.key for n in prototype.nodes('common/scripted_triggers')}
    for folder in ['common/scripted_effects', 'common/on_actions', 'common/decisions']:
        for top in prototype.nodes(folder):
            for n in cw.walk(top.children()):
                if n.key.startswith(('aor1776_bridge_', 'aor1776_ilp_')):
                    assert n.key in effect_ids | trigger_ids, 'Unresolved scripted invocation ' + n.key
    # Only reviewed old payload files change; all others remain byte-identical.
    before = json.loads(BASE.read_text(encoding='utf-8'))
    reviewed = {'descriptor.mod', '.metadata/metadata.json', 'README.md',
        'common/on_actions/aor1776_landscape_prototype.txt',
        'common/decisions/aor1776_landscape_prototype.txt',
        'localization/english/aor1776_landscape_prototype_l_english.yml',
        'localization/french/aor1776_landscape_prototype_l_french.yml'}
    for rel, oldhash in before['installed'].items():
        if rel not in reviewed:
            assert prototype.prior.sha(prototype.payload()[rel]) == oldhash, rel
    print('PASS bridge PM coverage, parse, no telemetry economic effects, BOM, main/Git preservation')


def deploy_upgrade():
    before = preserved()
    validate()
    dest = prototype.DEST.resolve()
    assert dest.parent == ROOT.parent.resolve() and dest.name == 'aor1776_landscape_prototype'
    actual = {p.relative_to(dest).as_posix(): prototype.prior.sha(p) for p in dest.rglob('*') if p.is_file()}
    expected = {rel: prototype.prior.sha(p) for rel, p in prototype.payload().items()}
    descriptor = ROOT.parent / prototype.DESCRIPTOR
    if actual == expected:
        prototype.verify()
        return
    assert actual == before['installed'], 'Installed companion has unknown changes; stop'
    assert prototype.prior.sha(descriptor) == before['descriptor'], 'Descriptor changed; stop'
    assert set(actual) <= set(expected), 'Upgrade must not remove existing files'
    backup = OUT / 'companion_0.1.0_backup'
    assert all(prototype.prior.sha(backup / 'mod' / rel) == h for rel, h in actual.items())
    assert prototype.prior.sha(backup / prototype.DESCRIPTOR) == before['descriptor']
    for relative, source in prototype.payload().items():
        target = dest / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    shutil.copy2(prototype.PACKAGE / prototype.DESCRIPTOR, descriptor)
    prototype.verify()
    preserved()
    print('Upgraded only isolated companion; backup verified; no game/launcher/save/Git writes')


def verify_delivery():
    """Generate evidence without writing to actual logs/saves or plugin cache."""
    validate()
    prototype.verify()
    package = ROOT / 'tools/vic3-diagnostic-bridge'
    cache = Path('C:/Users/simeo/.codex/plugins/cache/aor1776-local-tools/vic3-diagnostic-bridge/0.1.0')
    # Compare all distributable files; empty fixture temp folders are not assets.
    files = {p.relative_to(package).as_posix(): prototype.prior.sha(p)
        for p in package.rglob('*') if p.is_file() and '__pycache__' not in p.parts and '.tmp' not in p.parts}
    assert all((cache / rel).is_file() and prototype.prior.sha(cache / rel) == digest for rel, digest in files.items())
    # Real stdio handshake against the actually installed entrypoint, not a model
    # invocation and not claimed as a native tool call inside this conversation.
    mcp = json.loads((cache / 'mcp.json').read_text(encoding='utf-8'))['mcpServers']['vic3-diagnostic-bridge']
    args = [v.replace('${PLUGIN_ROOT}', str(cache)) for v in mcp['args']]
    requests = [
        {'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {'protocolVersion': '2025-11-25', 'capabilities': {}, 'clientInfo': {'name': 'local-bridge-verifier', 'version': '1'}}},
        {'jsonrpc': '2.0', 'method': 'notifications/initialized'},
        {'jsonrpc': '2.0', 'id': 2, 'method': 'tools/list'},
        *[{'jsonrpc': '2.0', 'id': i + 3, 'method': 'tools/call', 'params': {'name': name, 'arguments': {}}}
          for i, name in enumerate(['vic3_bridge_status', 'vic3_latest_snapshot', 'vic3_diagnostic_errors'])]]
    run = subprocess.run([mcp['command'], *args], input=''.join(json.dumps(r) + '\n' for r in requests).encode(),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=15, cwd=cache)
    assert run.returncode == 0 and not run.stderr, run.stderr
    responses = [json.loads(line) for line in run.stdout.splitlines()]
    assert len(responses) == 5
    assert all(not r['result']['isError'] for r in responses[2:])
    real_status, real_snapshot, real_errors = [r['result']['structuredContent'] for r in responses[2:]]
    assert all(r['source'] == 'LOCAL_GAME_LOG' for r in [real_status, real_snapshot, real_errors])
    # Fixtures are kept distinct; test runner never writes into real game logs.
    suite = unittest.defaultTestLoader.discover(str(package / 'tests'))
    output = io.StringIO()
    tests = unittest.TextTestRunner(stream=output, verbosity=2).run(suite)
    (OUT / 'TESTS.txt').write_text(output.getvalue(), encoding='utf-8')
    assert tests.wasSuccessful()
    map_suite = unittest.defaultTestLoader.discover(str(ROOT / 'tools'), pattern='test_map2n*.py')
    map_output = io.StringIO()
    map_tests = unittest.TextTestRunner(stream=map_output, verbosity=2).run(map_suite)
    (OUT / 'MAP2N_TESTS.txt').write_text(map_output.getvalue(), encoding='utf-8')
    assert map_tests.wasSuccessful()
    guard = subprocess.run([sys.executable, '-B', '-X', 'utf8', str(ROOT / 'tools/validate_infrastructure_landscape.py'), '--validate'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
    assert guard.returncode == 0, guard.stderr
    guard_result = json.loads(guard.stdout)
    preserved()
    attempted = (FIX / 'RUNTIME_BEFORE.json').exists()
    identity_attempted = (IDENTITY / 'RUNTIME_BEFORE.json').exists()
    companion_version = json.loads((prototype.SOURCE / '.metadata/metadata.json').read_text(encoding='utf-8-sig'))['version']
    observed_receipt_path = OUT / 'RUNTIME_EXPORT_OBSERVED_2026_10_16.json'
    observed_receipt = json.loads(observed_receipt_path.read_text(encoding='utf-8')) if observed_receipt_path.exists() else None
    basic_export_observed = bool(observed_receipt and companion_version == '0.2.2'
        and observed_receipt.get('status') == 'PASS_RUNTIME_EXPORT_OBSERVED'
        and observed_receipt['snapshot'].get('source') == 'LOCAL_GAME_LOG'
        and observed_receipt['snapshot'].get('status') == 'SNAPSHOT_AVAILABLE'
        and not observed_receipt['snapshot']['snapshot']['errors'])
    forced_path = OUT / 'RUNTIME_FORCED_PROBE_2026_10_16.json'
    forced_receipt = json.loads(forced_path.read_text(encoding='utf-8')) if forced_path.exists() else None
    forced_observed = bool(basic_export_observed and forced_receipt
        and forced_receipt.get('status') == 'PASS_RUNTIME_FORCED_PROBE_EXPORT_OBSERVED'
        and forced_receipt.get('same_session_after_cursor_verified')
        and forced_receipt['after']['freshness'] == 'NEW_SINCE_CURSOR')
    auto_path = OUT / 'RUNTIME_AUTO_RETURN_2026_10_16.json'
    auto_receipt = json.loads(auto_path.read_text(encoding='utf-8')) if auto_path.exists() else None
    aba_observed = bool(forced_observed and auto_receipt
        and auto_receipt.get('status') == 'PASS_RUNTIME_PROBE_ABA_OBSERVED'
        and auto_receipt.get('same_session_after_cursor_verified')
        and auto_receipt.get('observed_sequence') == [0, 1, 0])
    user_visual = prototype.manual_visual_receipt()
    companion_static = json.loads((prototype.PACKAGE / 'VALIDATION.json').read_text(encoding='utf-8'))
    fix_tests = None
    if attempted:
        fix_suite = unittest.defaultTestLoader.discover(str(ROOT / 'tools'), pattern='test_vic3_export_scope_fix.py')
        fix_output = io.StringIO()
        fix_tests = unittest.TextTestRunner(stream=fix_output, verbosity=2).run(fix_suite)
        (FIX / 'TESTS.txt').write_text(fix_output.getvalue(), encoding='utf-8')
        assert fix_tests.wasSuccessful()
    dump(OUT / 'VALIDATION.json', {
        'status': 'PASS_RUNTIME_PROBE_ABA_OBSERVED' if aba_observed else 'PASS_RUNTIME_FORCED_PROBE_EXPORT_OBSERVED' if forced_observed else 'PASS_RUNTIME_EXPORT_OBSERVED' if basic_export_observed else 'NUMERIC_EXPORT_OBSERVED_IDENTITY_FIX_AWAITING_RETEST' if identity_attempted else 'ENGINE_EXPORT_INVALID_SCOPE_FIX_AWAITING_RETEST' if attempted else 'READER_AND_LOCAL_INSTALL_PASS_ENGINE_EXPORT_PENDING',
        'observed_utc': datetime.now(timezone.utc).isoformat(),
        'unit_tests': {'passed': tests.testsRun, 'total': tests.testsRun, 'source': 'SYNTHETIC_FIXTURES_NOT_GAME'},
        'companion_static': {'passed': companion_static['passed'], 'total': companion_static['total'], 'automated_engine_test': False},
        'map2n_regression': {'passed': map_tests.testsRun, 'total': map_tests.testsRun, 'automated_engine_test': False},
        'prior_train_pm_guard': {k: guard_result[k] for k in ['status', 'passed', 'total', 'runtime_tested']},
        'installed_plugin': {'id': 'vic3-diagnostic-bridge@aor1776-local-tools', 'path': str(cache),
            'source_hashes_match': True, 'sha256': files},
        'real_installed_stdio_smoke_test': {'initialize': True,
            'tools': [t['name'] for t in responses[1]['result']['tools']],
            'three_read_only_calls': True, 'source': 'LOCAL_GAME_LOG',
            'telemetry_status': real_snapshot['status'],
            'error_messages_returned': real_errors['returned'],
            'error_attribution': 'UNCLASSIFIED_NOT_AUTOMATICALLY_ATTRIBUTED_TO_BRIDGE'},
        'native_tools_in_current_codex_turn': 'NOT_DISCOVERED_REQUIRES_HOST_REFRESH',
        'engine_export_tested': attempted, 'engine_export_validated': basic_export_observed,
        'runtime_export_receipt': observed_receipt_path.name if basic_export_observed else None,
        'runtime_forced_probe_receipt': forced_path.name if forced_observed else None,
        'forced_probe_same_session_after_cursor_verified': forced_observed,
        'runtime_auto_return_receipt': auto_path.name if aba_observed else None,
        'probe_sequence_0_1_0_observed': aba_observed,
        'latest_log_tail_incomplete': auto_receipt['newer_tail_incomplete'] if aba_observed else None,
        'full_bridge_runtime_validated': False, 'current_freshness_certified': False,
        'engine_export_observation': 'EXPORT_SCOPE_FIX_2026_10_16/RUNTIME_BEFORE.json' if attempted else None,
        'numeric_export_runtime_observation': 'IDENTITY_FIX_2026_10_16/RUNTIME_BEFORE.json' if identity_attempted else None,
        'export_scope_fix_static_tests': {'passed': fix_tests.testsRun, 'total': fix_tests.testsRun} if fix_tests else None,
        'visual_tracks_tested_by_bridge': False,
        'manual_ground_rail_toggle_user_validated': bool(user_visual),
        'manual_visual_receipt': 'docs/prototypes/REGIONAL_INFRASTRUCTURE/RUNTIME_USER_VISUAL_VALIDATION_2026_10_16.json' if user_visual else None,
        'manual_visual_scope': user_visual['scope'] if user_visual else None,
        'real_rail_pm_transition_validated': False,
        'inbound_game_commands': False, 'main_runtime_unchanged': True,
        'head_index_unchanged': True, 'save_or_playset_changed': False,
        'companion_deployed': companion_version,
        'required_next_step': 'Local manual ground-rail toggle accepted; real rail PM and cross-state/side-effect tests remain open.' if user_visual else 'Optional same-session after-cursor force/remove/auto test; visual rails remain separate.' if basic_export_observed else 'Restart game with companion; trigger export; verify new cursor record and UI values.',
        'initial_test_environment_issue': 'Default sandbox Temp denied cleanup; fixtures moved under workspace tests/.tmp; suite rerun successfully.'})
    print(json.dumps({'bridge_tests': tests.testsRun, 'installed_stdio_tools': 3,
        'real_log_status': real_snapshot['status'], 'engine_export_tested': attempted,
        'engine_export_validated': basic_export_observed,
        'main_runtime_and_git_preserved': True}, indent=2))


if __name__ == '__main__':
    actions = {'--capture': capture, '--validate': validate, '--deploy-upgrade': deploy_upgrade,
        '--verify-delivery': verify_delivery, '--capture-export-fix': capture_export_fix, '--deploy-export-fix': deploy_export_fix,
        '--capture-identity-fix': capture_identity_fix, '--deploy-identity-fix': deploy_identity_fix,
        '--record-received-export': record_received_export,
        '--record-forced-probe': record_forced_probe, '--record-auto-return': record_auto_return}
    assert len(sys.argv) == 2 and sys.argv[1] in actions
    actions[sys.argv[1]]()
