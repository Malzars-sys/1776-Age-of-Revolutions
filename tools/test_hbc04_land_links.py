"""Prevent false land access through diagonals, barriers or separate enclaves."""
import unittest
import numpy as np
from hbc04_land_links import flood,contacts,pair


class LandLinks(unittest.TestCase):
    def test_diagonal_is_not_a_land_connection(self):
        a=np.array([[1,0],[0,2]],dtype=np.uint32)
        _,goal=flood(a,np.isin(a,[1,2]),[0],set(),{3})
        self.assertIsNone(goal)

    def test_forbidden_native_border_is_respected(self):
        a=np.array([[1,2]],dtype=np.uint32)
        _,goal=flood(a,np.ones_like(a,dtype=bool),[0],{pair(1,2)},{1})
        self.assertIsNone(goal)

    def test_intervening_decentralized_or_sea_cell_is_not_traversed(self):
        a=np.array([[1,9,2]],dtype=np.uint32)
        _,goal=flood(a,np.isin(a,[1,2]),[0],set(),{2})
        self.assertIsNone(goal)

    def test_flat_index_does_not_wrap_to_next_row(self):
        a=np.array([[0,1],[2,0]],dtype=np.uint32)
        _,goal=flood(a,np.isin(a,[1,2]),[1],set(),{2})
        self.assertIsNone(goal)

    def test_separate_ont_enclave_cannot_borrow_mainlands_usa_border(self):
        a=np.array([[2,3,9],[9,9,9],[1,2,2]],dtype=np.uint32)
        border=contacts(a,a==2,a==3,set())
        reachable,_=flood(a,a==2,[u for u,v in border],set())
        hbc_border=contacts(a,a==1,a==2,set())
        self.assertTrue(border and hbc_border)
        self.assertFalse(any(v in reachable for u,v in hbc_border))

    def test_shared_edge_contact_has_correct_orientation(self):
        a=np.array([[1,2],[1,2]],dtype=np.uint32)
        self.assertEqual(contacts(a,a==1,a==2,set()),[(0,1),(2,3)])


if __name__=='__main__':unittest.main()
