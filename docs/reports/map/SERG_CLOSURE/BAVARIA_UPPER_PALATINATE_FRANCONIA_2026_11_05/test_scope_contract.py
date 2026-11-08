"""The Bavarian registry layer must reject unreviewed scope expansion."""
from pathlib import Path
import json,unittest
from unittest.mock import patch
import map2l_registry as registry
HERE=Path(__file__).resolve().parent
class BavarianScopeContract(unittest.TestCase):
 def altered(self,change,geometry=False):
  path=HERE/('GEOMETRY.json' if geometry else 'REGISTRY_MIGRATION.json')
  current=json.loads(path.read_text(encoding='utf-8'));change(current)
  original=Path.read_text
  def read(p,*a,**kw):
   if p==path:return json.dumps(current)
   return original(p,*a,**kw)
  with patch.object(Path,'read_text',read):
   with self.assertRaises(AssertionError):registry.approved_lot_dirs()
 def test_accepts_exact_reviewed_layer(self):
  self.assertEqual(registry.approved_lot_dirs()[-1],HERE)
 def test_rejects_new_member(self):
  self.altered(lambda m:m['new_members'].append('TEST'))
 def test_rejects_added_imperial_extent(self):
  self.altered(lambda m:m['extent_added_cells'].append([0,0]))
 def test_rejects_removing_imperial_extent(self):
  self.altered(lambda m:m['extent_removed_cells'].append([0,0]))
 def test_rejects_modifying_existing_title(self):
  self.altered(lambda m:m['updated'][0].update(beneficiary='AUS'))
 def test_rejects_wrong_new_beneficiary(self):
  self.altered(lambda m:next(r for r in m['updated'] if r['rgb']=='xEEC807').update(beneficiary='BAV'))
 def test_rejects_new_country_definition(self):
  self.altered(lambda m:m['country_additions'].update(TEST='unreviewed'))
 def test_rejects_unreviewed_state_region(self):
  self.altered(lambda m:m['replaced_regions'].append('STATE_FRANCONIA'))
 def test_rejects_claiming_cadastral_accuracy(self):
  self.altered(lambda g:g.update(historical_cadastral_precision=True),True)
