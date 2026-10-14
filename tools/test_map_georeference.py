"""Synthetic numerical and safety tests. They do not certify real geography."""
import copy
import unittest
import numpy as np
from PIL import Image
from georeference.model import fit,forward,inverse,evaluate,grid_lines,KINDS
from map_georeference import render_grid,warp_raster,output_path,ROOT

def controls():
    return [{'name':str(i),'role':'FIT','geo':p,'pixel':[p[0]*10+50,200-p[1]*10],'quality':'manual_unverified'}
        for i,p in enumerate([[0,0],[2,0],[0,2],[2,2],[1,1]])]

class ModelTests(unittest.TestCase):
    def test_roundtrip_all_models(self):
        for kind in KINDS:
            m=fit(controls(),kind,(256,256))
            np.testing.assert_allclose(inverse(m,forward(m,[[1.25,.75],[.1,1.7]])),[[1.25,.75],[.1,1.7]],atol=1e-10)
    def test_known_affine(self):
        m=fit(controls(),'geographic_affine',(256,256))
        np.testing.assert_allclose(forward(m,[[1,1]]),[[60,190]],atol=1e-10)
    def test_no_targets_in_fit_or_errors(self):
        r=controls()+[{'name':'target','role':'TARGET','geo':[1,1],'pixel':None}]
        e=evaluate(fit(r,'geographic_affine'))
        self.assertEqual(e['fit']['count'],5);self.assertIsNone(e['points'][-1]['residual_px'])
        self.assertEqual(e['accuracy_status'],'NOT_ESTABLISHED');self.assertIsNone(e['confidence_interval_px'])
    def test_check_not_used_to_fit(self):
        r=controls()+[{'name':'held','role':'CHECK','geo':[1,1],'pixel':[67,190],'quality':'manual_unverified'}]
        m=fit(r,'geographic_affine');e=evaluate(m)
        self.assertAlmostEqual(e['check']['rms_px'],7);self.assertEqual(m['fit_count'],5)
        self.assertEqual(len(e['leave_one_out']),5)
    def test_trusted_checks_and_extrapolation(self):
        r=controls()+[{'name':str(i),'role':'CHECK','geo':p,'pixel':[10*p[0]+50,200-10*p[1]],'quality':'surveyed_landmark'}
            for i,p in enumerate([[.5,.5],[1,.5],[.5,1]])]
        e=evaluate(fit(r,'geographic_affine'));self.assertEqual(e['accuracy_status'],'EMPIRICALLY_CHECKED_NOT_EXACT')
        r[-1]['geo']=[4,4];e=evaluate(fit(r,'geographic_affine'))
        self.assertEqual(e['accuracy_status'],'NOT_ESTABLISHED');self.assertTrue(e['points'][-1]['extrapolated'])
    def test_invalid_controls(self):
        for bad in [[],[{}],None,controls()[:2]]:
            with self.assertRaises(ValueError):fit(bad)
        r=controls();r[0]['geo']=[0,None]
        with self.assertRaises(ValueError):fit(r)
        r=controls();r[0]['pixel']=[float('nan'),2]
        with self.assertRaises(ValueError):fit(r)
    def test_collinear(self):
        r=controls()[:3]
        for i,v in enumerate(r):v['geo']=[i,i]
        with self.assertRaises(ValueError):fit(r,'geographic_affine')
    def test_native_equator_is_hypothesis(self):
        m=fit([],'native_miller_hypothesis')
        np.testing.assert_allclose(forward(m,[[0,0]]),[[4096,2097.28]])
        self.assertEqual(m['status'],'HYPOTHESIS_NOT_EXACT')
        with self.assertRaises(ValueError):grid_lines(m)
    def test_spacing_limits(self):
        m=fit(controls(),'geographic_affine')
        for value in [0,float('nan'),40]:
            with self.assertRaises(ValueError):grid_lines(m,value)
        with self.assertRaises(ValueError):grid_lines(m,.1,False)
    def test_png_transparency_and_alignment(self):
        m=fit(controls(),'geographic_affine',(256,256));im=render_grid(m,1)
        self.assertEqual(im.size,(256,256));self.assertEqual(im.mode,'RGBA')
        self.assertEqual(im.getpixel((0,0))[3],0);self.assertGreater(im.getpixel((60,190))[3],0)
    def test_historical_warp_identity(self):
        m=fit(controls(),'geographic_affine',(256,256));y,x=np.indices((256,256),dtype=np.uint8)
        im=Image.fromarray(np.dstack((x,y,np.full_like(x,200),np.full_like(x,255))))
        warped=warp_raster(im,m,m,[50,50,82,82]);self.assertEqual(warped.size,(32,32))
        np.testing.assert_allclose(warped.getpixel((16,16)),(66,66,200,255),atol=1)
        np.testing.assert_allclose(warped.getpixel((2,25)),(52,75,200,255),atol=1)
        with self.assertRaises(ValueError):warp_raster(im,m,m,[0,0,5000,10])
    def test_output_cannot_overwrite_runtime_source_existing_or_outside(self):
        for path in [ROOT/'map_data/provinces.png',ROOT/'common/test.txt',ROOT.parent/'unsafe.png',ROOT/'tools/georeference/controls.example.json']:
            with self.assertRaises(ValueError):output_path(path)
        with self.assertRaises(ValueError):output_path(ROOT/'docs/reports/map/test.png',[ROOT/'docs/reports/map/test.png'])

if __name__=='__main__':unittest.main()
