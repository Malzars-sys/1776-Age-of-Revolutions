"""Portable regression tests for wig opacity, native material data and DDS mips.

Run: python tools/test_frederick_wig.py
Requires Pillow; no Blender/game installation or preview files are needed.
"""
import contextlib
import io
import struct
import tempfile
import unittest
from pathlib import Path

from PIL import Image
import build_frederick_wig as wig


def dds_levels(path):
    data = path.read_bytes()
    if data[:4] != b'DDS ':
        raise AssertionError('Not a DDS file')
    height, width = struct.unpack_from('<II', data, 12)
    count = struct.unpack_from('<I', data, 28)[0]
    masks = struct.unpack_from('<IIII', data, 92)
    if masks != (0xFF0000, 0xFF00, 0xFF, 0xFF000000):
        raise AssertionError('Unexpected BGRA channel masks')
    offset = 128
    result = []
    for _ in range(count):
        length = width * height * 4
        result.append(Image.frombytes('RGBA', (width, height),
                                     data[offset:offset+length], 'raw', 'BGRA'))
        offset += length
        width, height = max(1, width//2), max(1, height//2)
    if offset != len(data):
        raise AssertionError('Incomplete or extra mip payload')
    return result


class WigAlphaTests(unittest.TestCase):
    def test_solid_core_never_inherits_strand_mask(self):
        self.assertEqual(wig.HAIR_SHADERS, ('portrait_hair_opaque', 'portrait_hair'))
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'core.dds'
            wig.write_dds(Image.new('RGBA', (64,64), (212,218,225,255)), output)
            for level in dds_levels(output):
                self.assertEqual(level.getchannel('A').getextrema(), (255,255))
                self.assertEqual(level.getpixel((0,0)), (212,218,225,255))

    def test_coverage_scaling_keeps_true_gaps(self):
        mask = Image.new('L', (32,32))
        mask.putdata([0 if i % 3 == 0 else (i*37) % 256 for i in range(1024)])
        adjusted = wig.scale_alpha_for_coverage(mask, .5, .4)
        for before, after in zip(mask.tobytes(), adjusted.tobytes()):
            if before == 0:
                self.assertEqual(after, 0)

    def test_strand_mips_preserve_native_shader_coverage(self):
        image = Image.new('RGBA', (64,64), (212,218,225,255))
        alpha = Image.new('L', image.size)
        alpha.putdata([0 if x < 5 or x > 58 else min(255,(x*5+y*3)%256)
                       for y in range(64) for x in range(64)])
        image.putalpha(alpha)
        target = wig.alpha_coverage(alpha, .5)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'strands.dds'
            with contextlib.redirect_stdout(io.StringIO()):
                wig.write_dds(image, output, cutout_coverage=target)
            for index, level in enumerate(dds_levels(output)):
                coverage = wig.alpha_coverage(level.getchannel('A'), .5/(1+.25*index))
                tolerance = max(.035, 3/(level.width*level.height))
                self.assertLessEqual(abs(coverage-target), tolerance)
                self.assertEqual(level.convert('RGB').getpixel((0,0)), (212,218,225))

    def test_runtime_core_and_strands_have_distinct_materials(self):
        asset = (wig.RUNTIME / f'{wig.STEM}.asset').read_text(encoding='utf-8-sig')
        sections = asset.split('meshsettings = {')[1:]
        self.assertEqual(len(sections), 2)
        self.assertIn('shader = "portrait_hair_opaque"', sections[0])
        self.assertIn('texture_diffuse = "aor_frederick_wig_base_diffuse.dds"', sections[0])
        self.assertIn('shader = "portrait_hair"', sections[1])
        self.assertIn('texture_diffuse = "aor_frederick_wig_diffuse.dds"', sections[1])
        for level in dds_levels(wig.RUNTIME / f'{wig.STEM}_base_diffuse.dds'):
            self.assertEqual(level.getchannel('A').getextrema(), (255,255))


class WigMaterialTests(unittest.TestCase):
    def test_native_normal_channel_order_and_flat_normal(self):
        normal = Image.new('RGB', (4,4), (128,128,255))
        normal.putpixel((0,0), (201,79,220))
        packed = wig.pack_native_normal(normal)
        self.assertEqual(packed.getpixel((0,0)), (128,201,0,79))
        self.assertEqual(packed.getpixel((1,0)), (128,128,0,128))
        # Mirror the game's UnpackRRxGNormal, including its Y sign flip.
        _, g, _, a = packed.getpixel((1,0))
        x, y = 2*g/255-1, -(2*a/255-1)
        self.assertLess(abs(x), .004)
        self.assertLess(abs(y), .004)
        self.assertGreater((1-x*x-y*y)**.5, .999)

    def test_packed_mips_do_not_treat_data_alpha_as_opacity(self):
        image = Image.new('RGBA', (16,16))
        image.putdata([(128, (x*23+y*17)%256, 0, 0 if x < 8 else 220)
                       for y in range(16) for x in range(16)])
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'normal.dds'
            wig.write_dds(image, output)
            for level in dds_levels(output):
                self.assertEqual(level.getchannel('R').getextrema(), (128,128))
                self.assertEqual(level.getchannel('B').getextrema(), (0,0))
                for source, filtered in zip(image.split(), level.split()):
                    expected = source.resize(level.size, Image.Resampling.LANCZOS)
                    self.assertEqual(filtered.tobytes(), expected.tobytes())

    def test_material_is_matte_nonmetal_and_has_no_sss_mask(self):
        rma = Image.new('RGB', (4,4), (146,0,239))
        rma.putpixel((0,0), (225,0,150))
        packed = wig.pack_native_properties(rma)
        self.assertEqual(packed.getpixel((0,0)), (0,56,0,225))
        self.assertEqual(packed.getpixel((1,0)), (0,56,0,198))

    def test_integrated_material_data_and_powder_colour(self):
        core = dds_levels(wig.RUNTIME / f'{wig.STEM}_base_diffuse.dds')
        strands = dds_levels(wig.RUNTIME / f'{wig.STEM}_diffuse.dds')
        # Both shells share the same toned-down colour, with opacity unchanged.
        self.assertLessEqual(core[0].convert('RGB').getextrema()[2][1], 224)
        for base, strand in zip(core, strands):
            self.assertEqual(base.convert('RGB').tobytes(), strand.convert('RGB').tobytes())
        for level in dds_levels(wig.RUNTIME / f'{wig.STEM}_properties.dds'):
            self.assertEqual(level.getchannel('R').getextrema(), (0,0))
            self.assertEqual(level.getchannel('G').getextrema(), (56,56))
            self.assertEqual(level.getchannel('B').getextrema(), (0,0))
            self.assertGreaterEqual(level.getchannel('A').getextrema()[0], 198)
        for level in dds_levels(wig.RUNTIME / f'{wig.STEM}_normal.dds'):
            self.assertEqual(level.getchannel('R').getextrema(), (128,128))
            self.assertEqual(level.getchannel('B').getextrema(), (0,0))


if __name__ == '__main__':
    unittest.main(verbosity=2)
