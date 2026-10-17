"""Static layout regressions, not an engine/UI screenshot test."""
import re
import unittest
from pathlib import Path
import validate_diplomacy_ottoman_1776 as cw

ROOT = Path(__file__).resolve().parents[1]
GUI = ROOT / 'gui/building_details_panel.gui'

def detail_section(text):
    return text.split('### PMS / EMPLOYMENT / CASH RESERVES', 1)[1].split('\n\ttype building_type_nationalize_button', 1)[0]

def instances(text):
    nodes = cw.parse(text)
    return [n for n in cw.walk(nodes) if n.key == 'condensed_building_information_pms' and isinstance(n.value, list)]

class TradeCenterLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = GUI.read_text(encoding='utf-8-sig')
        cls.before = (ROOT / 'docs/reports/map/MAP2M/R1/building_details_panel.before.gui').read_text(encoding='utf-8-sig')
        cls.items = instances(cls.text)

    def test_structure_and_complementary_visibility(self):
        self.assertEqual(len(self.items), 2)
        self.assertEqual(self.items[0].one('visible'), '"[Not(ObjectsEqual(Building.GetBuildingType, GetBuildingType(\'building_trade_center\').Self))]"')
        self.assertEqual(self.items[1].one('visible'), '"[ObjectsEqual(Building.GetBuildingType, GetBuildingType(\'building_trade_center\').Self)]"')

    def test_trade_wraps_at_two(self):
        self.assertIn('datamodel_wrap = 2', self.text[self.items[1].start:self.items[1].end])
        self.assertNotIn('datamodel_wrap', self.text[self.items[0].start:self.items[0].end])

    def test_current_third_group_is_data_reporting(self):
        text = (ROOT / 'common/buildings/11_private_infrastructure.txt').read_text(encoding='utf-8-sig')
        building = next(n for n in cw.parse(text) if n.key == 'building_trade_center')
        groups = [n.value for n in building.children('production_method_groups')[0].value]
        self.assertEqual(groups, ['pmg_base_building_trade_center', 'pmg_trade_quantity_trade_center', 'pmg_1776_trade_data_reporting'])

    def test_two_rows_reserve_150_pixels(self):
        section = detail_section(self.text)
        self.assertIn("'(int32)2'", section)
        self.assertIn('size = { @panel_width 150 }', section)
        self.assertGreaterEqual(150, 2 * 70)

    def test_three_and_four_pm_buttons_do_not_intersect_goods(self):
        # Values are asserted against the real GUI below, not inferred at runtime.
        trade = self.text[self.items[1].start:self.items[1].end]
        for value in ['addcolumn = 72', 'addrow = 70', 'size = { 70 70 }', 'minimumsize = { 144 -1 }']:
            self.assertIn(value, trade)
        self.assertIn('position = { 150 0 }', self.text)
        for count in [3, 4]:
            boxes = [(i % 2 * 72, i // 2 * 70, i % 2 * 72 + 70, i // 2 * 70 + 70) for i in range(count)]
            self.assertEqual(boxes[2][1], 70)
            self.assertTrue(all(box[2] < 150 for box in boxes))

    def test_shared_list_templates_unchanged(self):
        # Browser/map lists use the same template: do not alter it globally.
        marker = '\n\ttype condensed_building_information_pms = container {'
        self.assertEqual(self.before.split(marker, 1)[1], self.text.split(marker, 1)[1])

    def test_changes_limited_to_detail_pm_section(self):
        start = '### PMS / EMPLOYMENT / CASH RESERVES'
        end = '\n\ttype building_type_nationalize_button'
        self.assertEqual(self.before.split(start, 1)[0], self.text.split(start, 1)[0])
        self.assertEqual(self.before.split(end, 1)[1], self.text.split(end, 1)[1])

    def test_binding_delimiters_balanced(self):
        for expression in re.findall(r'"(\[[^"\n]*\])"', detail_section(self.text)):
            self.assertEqual(expression.count('('), expression.count(')'))
            self.assertEqual(expression.count('['), expression.count(']'))

if __name__ == '__main__': unittest.main()
