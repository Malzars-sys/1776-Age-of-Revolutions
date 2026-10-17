"""Regression tests for the observed game-side exporter defect, not engine tests."""
from pathlib import Path
import importlib.util
import json
import unittest
import infrastructure_landscape_prototype as prototype
import validate_diplomacy_ottoman_1776 as cw

SPEC = importlib.util.spec_from_file_location('vic3_bridge_reader', prototype.ROOT / 'tools/vic3-diagnostic-bridge/server/bridge.py')
bridge = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(bridge)


class ExportScopeFixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.effects = {n.key: n for n in prototype.nodes('common/scripted_effects') if n.key.startswith('aor1776_bridge_')}

    def lookup(self, effect_id, level):
        messages = []
        for condition in self.effects[effect_id].children('if'):
            predicate = condition.children('limit')[0].children()[0]
            take = level == int(predicate.value) if predicate.op == '=' else level > int(predicate.value)
            if take:
                messages.append(cw.scalar(condition.children('debug_log')[0].value))
        return messages

    def test_exact_regional_levels_and_explicit_overflow(self):
        for n in range(257):
            self.assertEqual(self.lookup('aor1776_bridge_export_regional_level', n), [f'AOR1776_BRIDGE_V1|regional_levels={n}'])
        self.assertEqual(self.lookup('aor1776_bridge_export_regional_level', 300), ['AOR1776_BRIDGE_V1|regional_levels=UNSUPPORTED_LEVEL'])

    def test_exact_probe_levels_and_explicit_overflow(self):
        for n in range(5):
            self.assertEqual(self.lookup('aor1776_bridge_export_probe_level', n), [f'AOR1776_BRIDGE_V1|probe_levels={n}'])
        self.assertEqual(self.lookup('aor1776_bridge_export_probe_level', 5), ['AOR1776_BRIDGE_V1|probe_levels=UNSUPPORTED_LEVEL'])

    def test_no_null_scope_scriptvalue_interpolation(self):
        for effect in self.effects.values():
            for n in cw.walk(effect.children()):
                if n.key == 'debug_log':
                    for bad in ('SCOPE.', 'THIS.', 'ScriptValue', 'MakeScope', 'GetPlayer'):
                        self.assertNotIn(bad, cw.scalar(n.value))
                    if '[' in cw.scalar(n.value):
                        self.assertEqual(cw.scalar(n.value), 'AOR1776_BRIDGE_V1|game_date=[TimeKeeper.GetCurrentDate.GetString]')

    def test_static_identity_matches_effective_definitions(self):
        import vic3_bridge_identity as identity
        expected, counts = identity.render()
        path = prototype.SOURCE / identity.TARGET
        self.assertEqual(path.read_text(encoding='utf-8'), expected)
        effect = self.effects['aor1776_bridge_export_identity']
        countries = effect.children('owner')[0].children('if')
        regions = effect.children('if')
        self.assertEqual(len(countries), counts['country_tags'])
        self.assertEqual(len(regions), counts['region_keys'])
        for case in countries:
            predicates = case.children('limit')[0].children()
            tag = predicates[0].value.removeprefix('c:')
            self.assertEqual([n.key for n in predicates], ['exists', 'this'])
            self.assertEqual(predicates[1].value, 'c:' + tag)
            self.assertEqual(cw.scalar(case.children('debug_log')[0].value), 'AOR1776_BRIDGE_V1|country_name=TAG:' + tag)
        for case in regions:
            predicate = case.children('limit')[0].children()[0]
            self.assertEqual(predicate.key, 'state_region')
            region = predicate.value.removeprefix('s:')
            self.assertEqual(cw.scalar(case.children('debug_log')[0].value), 'AOR1776_BRIDGE_V1|state_name=REGION:' + region)

    def test_synthetic_static_identity_frame_compatible_with_reader(self):
        path = prototype.ROOT / 'docs/reports/bridge/VIC3_LOCAL_BRIDGE/IDENTITY_FIX_2026_10_16/RUNTIME_BEFORE.json'
        observed = json.loads(path.read_text(encoding='utf-8'))['rejected_record']
        # Synthetic correction for parser compatibility only, not engine evidence.
        fields = dict(observed['fields'], country_name='TAG:FRA', state_name='REGION:STATE_ILE_DE_FRANCE')
        for key in ('regional_levels', 'probe_levels'):
            fields[key] = str(fields[key])
        frame = {'fields': fields, 'pms': observed['pms'], 'errors': []}
        bridge.validate_frame(frame)
        self.assertEqual(frame['errors'], [])
        self.assertTrue(frame['probe_matches_expected'])

    def test_local_player_guard(self):
        entry = self.effects['aor1776_bridge_export_state']
        self.assertEqual(len(entry.children('if')), 1)
        condition = entry.children('if')[0]
        local = condition.children('limit')[0].children('owner')[0].children('is_local_player')[0]
        self.assertEqual(local.value, 'yes')
        self.assertEqual(condition.children('aor1776_bridge_export_local_capital')[0].value, 'yes')

    def test_no_game_mutations_in_export(self):
        forbidden = {'create_building', 'remove_building', 'set_variable', 'remove_variable',
            'activate_production_method', 'add_treasury', 'add_technology_researched'}
        self.assertFalse(forbidden & {n.key for effect in self.effects.values() for n in cw.walk(effect.children())})

    def test_actual_invalid_frame_stays_rejected(self):
        path = prototype.ROOT / 'docs/reports/bridge/VIC3_LOCAL_BRIDGE/EXPORT_SCOPE_FIX_2026_10_16/RUNTIME_BEFORE.json'
        data = json.loads(path.read_text(encoding='utf-8'))
        actual = data['last_complete']
        self.assertTrue(actual['errors'])
        self.assertEqual(actual['fields']['country_name'], '')
        self.assertIn('NULL_STATE', actual['fields']['state_name'])
        # A future complete frame with the same bad labels must never be accepted.
        frame = {'fields': dict(actual['fields']), 'pms': list(actual['pms']), 'errors': []}
        for key in ('regional_levels', 'probe_levels'):
            frame['fields'][key] = str(frame['fields'][key])
        bridge.validate_frame(frame)
        self.assertTrue(frame['errors'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
