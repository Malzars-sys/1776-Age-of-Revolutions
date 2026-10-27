"""Geometry failures that must not become colonial enclaves."""
import unittest
import numpy as np
from hbc02_map_candidates import graph, pixel_components, shortest


class CorridorGeometry(unittest.TestCase):
    def test_corner_contact_does_not_connect_provinces(self):
        adjacency=graph(np.array([[1,0],[0,2]],dtype=np.uint32),np.array([1,2]))
        self.assertNotIn(2,adjacency[1])

    def test_shared_edge_is_counted_in_both_directions(self):
        adjacency=graph(np.array([[1,2],[1,2]],dtype=np.uint32),np.array([1,2]))
        self.assertEqual(adjacency[1][2],2)
        self.assertEqual(adjacency[2][1],2)

    def test_same_rgb_can_hide_an_isolated_fragment(self):
        mask=np.array([[True,True,False,True]])
        roots,sizes,_=pixel_components(mask,[[0,0],[3,0]])
        self.assertNotEqual(*roots)
        self.assertEqual(sorted(sizes),[1,2])

    def test_unreachable_post_has_no_route(self):
        self.assertEqual(shortest({1:{},2:{}},{1:1,2:1},1,{2}),[])

    def test_route_avoids_large_territory_when_small_corridor_exists(self):
        adjacency={1:{2:1,3:1},2:{1:1,4:1},3:{1:1,4:1},4:{2:1,3:1}}
        self.assertEqual(shortest(adjacency,{1:1,2:10000,3:1,4:1},1,{4}),[1,3,4])


if __name__=='__main__':unittest.main()
