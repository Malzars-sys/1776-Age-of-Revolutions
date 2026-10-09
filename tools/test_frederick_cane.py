"""Static/native readback checks for the original cane; not in-game QA."""
import importlib.util
import math
from pathlib import Path
import re
import subprocess
import sys
import unittest

import build_start_1776_research_input_pack as history
from test_frederick_wig import dds_levels
from test_historical_wigs import starting_characters

ROOT=Path(__file__).resolve().parents[1]
GAME=Path('C:/Games/Victoria 3/game')
PDX=Path('C:/Users/simeo/AppData/Roaming/Blender Foundation/Blender/5.2/extensions/user_default/io_pdx_mesh')
BLENDER=Path('C:/Program Files/Blender Foundation/Blender 5.2/blender.exe')
STEM='aor1776_frederick_cane'
MODEL=ROOT/'gfx/models/portraits/attachments/props'/STEM
ANIM=ROOT/'gfx/portraits/portrait_animations/animations.txt'
GENE=ROOT/'common/genes/aor1776_cane_accessory_gene.txt'
ACCESSORY=ROOT/'gfx/portraits/accessories/aor1776_frederick_cane.txt'
MODIFIER=ROOT/'gfx/portraits/portrait_modifiers/aor1776_frederick_cane.txt'


class FrederickCane(unittest.TestCase):
    def test_pose_is_scoped_to_frederick_and_adds_only_compatible_prop(self):
        idle=history.named_blocks(ANIM,'idle',0)[0]
        male=history.subblocks(idle,'male')[0]
        entry=history.subblocks(male,STEM+'_idle')[0]
        self.assertIn('head = "idle_head_pop_walkingcane" torso = "idle_body_walkingcane"',entry.text)
        weight=history.subblocks(entry,'weight')[0]
        self.assertEqual(history.scalar(weight.text,'base'),'0')
        condition=history.subblocks(weight,'modifier')[0].text
        for key,value in [('add','90000'),('has_variable','aor1776_frederick_tricorne'),
                          ('is_historical','yes'),('is_female','no'),('is_adult','yes')]:
            self.assertEqual(history.scalar(condition,key),value)
        self.assertIn('aor1776_frederick_cane_props = aor1776_cane_attachment',entry.text)
        self.assertNotIn('animations_props = walkingcane_attachment',entry.text)
        marked=[(tag,history.scalar(c.text,'first_name')) for tag,c in starting_characters()
                if 'aor1776_frederick_tricorne' in history.clean_comments(c.text)]
        self.assertEqual(marked,[('PRU','Frederick_II')])

    def test_other_native_animation_rules_are_preserved_exactly(self):
        path=GAME/'gfx/portraits/portrait_animations/animations.txt'
        if not path.is_file(): self.skipTest('Native animation reference unavailable')
        text=history.read(ANIM)
        start=text.index('\t\t# AOR1776:')
        end=text.index('\t\tsmoker_character_idle',start)
        self.assertEqual((text[:start]+text[end:]).strip(),history.read(path).strip())
        head=history.read(GAME/'gfx/models/portraits/male_head/male_head.asset')
        body=history.read(GAME/'gfx/models/portraits/male_body/male_body.asset')
        self.assertIn('name = "idle_head_pop_walkingcane"',head)
        self.assertIn('name = "idle_body_walkingcane"',body)

    def test_hand_attachment_and_special_gene(self):
        container=history.named_blocks(GENE,'special_genes',0)[0]
        accessory_genes=history.subblocks(container,'accessory_genes')[0]
        gene=history.subblocks(accessory_genes,'aor1776_hand_prop')[0]
        self.assertEqual(history.scalar(gene.text,'inheritable'),'no')
        templates=history.subblocks(gene,r'\w+')
        self.assertEqual([history.scalar(t.text,'index') for t in templates],['0','1'])
        self.assertIn('male = { 1 = aor1776_frederick_cane_accessory }',templates[1].text)
        self.assertIn('female = { 1 = empty }',templates[1].text)
        accessory=history.read(ACCESSORY)
        self.assertIn('node = "bn_r_prop"',accessory)
        self.assertNotIn('shared_pose_entity',history.clean_comments(accessory))
        modifier=history.read(MODIFIER)
        self.assertIn('usage = none',modifier)
        self.assertIn('mode = add',modifier)
        self.assertIn('gene = aor1776_hand_prop',modifier)
        self.assertNotRegex(modifier,r'gene\s*=\s*(?:props|headgear|hairstyles)\b')
        for path in [ANIM,GENE,ACCESSORY,MODIFIER]:
            self.assertTrue(path.read_bytes().startswith(b'\xef\xbb\xbf'),str(path))

    def test_asset_binding_and_original_provenance(self):
        asset=history.read(MODEL/f'{STEM}.asset')
        for name in re.findall(r'(?m)^\s*(?:file|texture_\w+)\s*=\s*"([^"]+)"',asset):
            self.assertTrue((MODEL/name).is_file(),name)
        self.assertIn('name = "aor1776_frederick_caneShape"',asset)
        self.assertIn('shader = "portrait_attachment"',asset)
        self.assertIn('No BlenderKit asset',history.read(MODEL/'PROVENANCE.txt'))

    def test_dds_mips_opaque_and_correct_channel_packing(self):
        for kind in ['diffuse','normal','properties']:
            levels=dds_levels(MODEL/f'{STEM}_{kind}.dds')
            self.assertEqual(len(levels),10)
            self.assertEqual(levels[0].size,(512,512))
            self.assertEqual(levels[-1].size,(1,1))
            for level in levels:
                if kind=='diffuse': self.assertEqual(level.getchannel('A').getextrema(),(255,255))
                elif kind=='normal': self.assertEqual(level.getextrema(),((128,128),(128,128),(0,0),(128,128)))
                else: self.assertEqual(level.getchannel('R').getextrema(),(0,0))
            if kind=='properties':
                self.assertEqual(levels[0].getpixel((80,80)),(0,45,0,195))
                self.assertEqual(levels[0].getpixel((300,80)),(0,55,0,175))
                self.assertEqual(levels[0].getpixel((440,80)),(0,65,180,165))

    def test_rigid_unskinned_native_prop_convention_and_topology(self):
        module=PDX/'pdx_data.py'
        if not module.is_file(): self.skipTest('IO PDX readback unavailable')
        spec=importlib.util.spec_from_file_location('cane_pdx',module)
        data=importlib.util.module_from_spec(spec);spec.loader.exec_module(data)
        result=data.read_meshfile(str(MODEL/f'{STEM}.mesh'))
        self.assertEqual(len(result.find('object')),1)
        shape=result.find('object')[0]
        self.assertEqual(shape.tag,STEM+'Shape')
        self.assertIsNone(shape.find('skeleton'))
        self.assertEqual(len(shape.findall('mesh')),1)
        mesh=shape.find('mesh');self.assertIsNone(mesh.find('skin'))
        self.assertEqual(len(mesh.attrib['tri'])//3,1808)
        count=len(mesh.attrib['p'])//3
        for key,width in [('p',3),('n',3),('ta',4),('u0',2)]:
            self.assertEqual(len(mesh.attrib[key]),count*width)
            self.assertTrue(all(math.isfinite(x) for x in mesh.attrib[key]))
        self.assertTrue(all(0<=x<count for x in mesh.attrib['tri']))
        bounds=mesh.find('aabb').attrib
        self.assertTrue(-47<bounds['min'][2]<-45)
        self.assertTrue(44<bounds['max'][2]<47)
        self.assertLess(bounds['max'][1]-bounds['min'][1],3)
        self.assertEqual(mesh.find('material').attrib['shader'],['portrait_attachment'])

    def test_work_file_contains_only_original_prop_and_packed_runtime_textures(self):
        if not BLENDER.is_file():self.skipTest('Blender unavailable')
        blend=ROOT/'docs/portraits/frederick_cane_work.blend'
        expression=("import bpy;from pathlib import Path;"
            f"bpy.ops.wm.open_mainfile(filepath={str(blend)!r});"
            f"assert [(o.name,o.type) for o in bpy.data.objects]==[({STEM!r},'MESH')];"
            "assert len(bpy.data.meshes)==1 and len(bpy.data.images)==3;"
            "assert all(i.packed_file and bytes(i.packed_file.data)==Path(bpy.path.abspath(i.filepath)).read_bytes() for i in bpy.data.images)")
        result=subprocess.run([str(BLENDER),'--background','--factory-startup','--python-exit-code','1',
                               '--python-expr',expression],capture_output=True,text=True,timeout=60)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)


if __name__=='__main__':unittest.main(verbosity=2)
