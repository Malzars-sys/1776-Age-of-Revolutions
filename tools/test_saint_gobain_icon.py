"""Format and reproducibility checks, not engine-render tests."""
import io
import struct
import unittest

from PIL import Image

import build_saint_gobain_icon as icon


class SaintGobainIcon(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = icon.ICON.read_bytes()

    def test_approved_original_retained(self):
        self.assertEqual(icon.sha(icon.MASTER.read_bytes()), icon.SOURCE_SHA256)

    def test_export_reproducible(self):
        self.assertEqual(self.payload, icon.dds_bytes(icon.prepared_icon()))

    def test_dimensions_256(self):
        self.assertEqual(Image.open(io.BytesIO(self.payload)).size, (256, 256))

    def test_native_uncompressed_layout(self):
        self.assertEqual(self.payload[84:88], b'\0' * 4)
        icon.assert_export_layout(self.payload, 'france_saint_gobain.dds')

    def test_complete_nine_level_chain(self):
        self.assertEqual(struct.unpack_from('<I', self.payload, 28)[0], 9)
        self.assertEqual(len(self.payload), 128 + sum((256 >> n) ** 2 * 4 for n in range(9)))

    def test_top_mip_exact_and_alpha_preserved(self):
        decoded = Image.open(io.BytesIO(self.payload)).convert('RGBA')
        expected = icon.prepared_icon()
        self.assertEqual(decoded.tobytes(), expected.tobytes())
        self.assertEqual(decoded.getchannel('A').getextrema(), (0, 255))

    def test_company_binding_unchanged(self):
        definition = (icon.ROOT / 'common/company_types/00_companies_france.txt').read_text(encoding='utf-8-sig')
        self.assertIn('icon = "' + icon.ICON.relative_to(icon.ROOT).as_posix() + '"', definition)


if __name__ == '__main__':
    unittest.main()
