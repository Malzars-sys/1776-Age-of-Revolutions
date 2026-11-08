import copy,json,sys,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[5]/'tools'))
import map2l_registry as registry

class BavariaMigrationScope(unittest.TestCase):
    def setUp(self):
        self.directory=Path(__file__).resolve().parent
        self.migration=self.directory/'REGISTRY_MIGRATION.json'
        self.geometry=self.directory/'GEOMETRY.json'
        self.original=Path.read_text
        self.m=json.loads(self.original(self.migration,encoding='utf-8'))
        self.g=json.loads(self.original(self.geometry,encoding='utf-8'))
    def rejected(self,path,data):
        original=self.original
        def read(p,*a,**k):
            return json.dumps(data) if p==path else original(p,*a,**k)
        with patch.object(Path,'read_text',read):
            with self.assertRaises(AssertionError):
                registry.approved_lot_dirs()
    def test_valid_lot_is_last_explicit_migration(self):
        self.assertEqual(registry.approved_lot_dirs()[-1],self.directory)
    def test_existing_Passau_title_cannot_be_taken(self):
        next(r for r in self.m['updated'] if r['rgb']=='xEDC000')['beneficiary']='BAV'
        self.rejected(self.migration,self.m)
    def test_wrong_target_holder_rejected(self):
        next(r for r in self.m['updated'] if r['rgb']=='xFDA6CB')['beneficiary']='AUS'
        self.rejected(self.migration,self.m)
    def test_no_new_member_can_be_smuggled(self):
        self.m['new_members']=['BAV']
        self.rejected(self.migration,self.m)
    def test_no_extra_imperial_extent_can_be_added(self):
        self.m['extent_added_cells']=[[4393,911]]
        self.rejected(self.migration,self.m)
    def test_wrong_geometry_cell_count_rejected(self):
        self.g['assignments'][0]['pixels']=174
        self.rejected(self.geometry,self.g)

if __name__=='__main__':unittest.main()
