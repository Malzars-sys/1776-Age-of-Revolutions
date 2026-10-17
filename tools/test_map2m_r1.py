"""A GUI authorization must never waive a territorial or unrelated edit."""
import unittest
from validate_map2m_r1 import unauthorized_changes
from map2m_r1_research import GUI

class PreservationTests(unittest.TestCase):
    def test_exact_gui_exception_only(self):
        self.assertEqual(unauthorized_changes({GUI:'a','map':'same'},{GUI:'b','map':'same'},{'before_sha256':'a','after_sha256':'b'}),[])

    def test_other_edit_still_fails(self):
        self.assertEqual(unauthorized_changes({GUI:'a','map':'same'},{GUI:'b','map':'changed'},{'before_sha256':'a','after_sha256':'b'}),['map'])

    def test_modified_gui_does_not_match_authorized_hash(self):
        self.assertEqual(unauthorized_changes({GUI:'a'},{GUI:'unexpected'},{'before_sha256':'a','after_sha256':'b'}),[GUI])

    def test_added_or_removed_file_never_waived(self):
        self.assertEqual(unauthorized_changes({GUI:'a','deleted':'x'},{GUI:'b','added':'x'},{'before_sha256':'a','after_sha256':'b'}),['added','deleted'])

if __name__=='__main__':unittest.main()
