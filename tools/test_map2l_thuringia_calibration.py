"""Tests of the diagnostic algorithm, not proof of historical boundaries."""
import unittest
import numpy as np
from map2l_thuringia_calibration import nearest,robust_translation,robust_similarity,summary
from georeference.model import forward,inverse

class LocalTests(unittest.TestCase):
    def test_nearest_pixel_centres(self):
        distance,index=nearest(np.array([[0,0],[3,4]]),np.array([[0,0],[5,4]]))
        np.testing.assert_allclose(distance,[0,2]);self.assertEqual(index.tolist(),[0,1])
    def test_known_translation(self):
        fixed=np.array([[0,0],[20,0],[0,30],[40,50],[60,-30],[100,80]],float)
        route=fixed+np.array([-5.7,-4.3]);cost,offset,_=robust_translation(fixed,route)
        np.testing.assert_allclose(offset,[-5.7,-4.3],atol=1e-7);self.assertLess(cost,1e-10)
    def test_known_similarity(self):
        fixed=np.array([[0,0],[20,0],[0,30],[40,50],[60,-30],[100,80]],float)
        angle=.01;transform=.99*np.array([[np.cos(angle),np.sin(angle)],[-np.sin(angle),np.cos(angle)]])
        route=fixed@transform+[2,-3];matrix,offset,parameters=robust_similarity(fixed,route,[2,-3])
        np.testing.assert_allclose(matrix,transform,atol=1e-7);np.testing.assert_allclose(offset,[2,-3],atol=1e-7)
        self.assertAlmostEqual(parameters['scale'],.99)
    def test_modified_profile_roundtrip(self):
        model={'kind':'miller_affine','matrix':[[1200,-1],[2,-1250],[4100,2070]]}
        p=[[11.0328,50.9787],[10.2597,51.5125],[10.1344,51.3775]]
        np.testing.assert_allclose(inverse(model,forward(model,p)),p,atol=1e-10)
    def test_metrics(self):
        s=summary(np.array([3.,4.]));self.assertEqual(s['count'],2);self.assertEqual(s['mean_px'],3.5)
        self.assertEqual(s['max_px'],4);self.assertAlmostEqual(s['rms_px'],np.sqrt(12.5))

if __name__=='__main__':unittest.main()
