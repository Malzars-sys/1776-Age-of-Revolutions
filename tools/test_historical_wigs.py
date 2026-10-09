"""Static checks for the curated 1776 wig assignments; no game or renders needed.

Run: python tools/test_historical_wigs.py
These checks establish bindings and scope, not in-game visual fit.
"""
import re
import unittest
from pathlib import Path

import build_start_1776_research_input_pack as history


ROOT = Path(__file__).resolve().parents[1]
FLAG = "aor1776_historical_powdered_wig"
CURATED = {
    "SWE": "Gustav_III",
    "DENNOR": "Christian_VII",
    "BAV": "Maximilian_III_Joseph",
    "SAX": "Frederick_Augustus_III",
    "WUR": "Karl_Eugen",
    "BAD": "Karl_Friedrich_Baden",
    "BRA": "Karl_I_Brunswick",
    "HEK": "Friedrich_II_Hesse_Kassel",
    "HES": "Ludwig_IX",
    "MEC": "Friedrich_II_the_Pious",
    "MST": "Adolf_Friedrich_IV",
    "COB": "Ernst_Friedrich",
}
DNA = {
    "fra": ("00_king_louis_xvi_fra.txt", "king_louis_xvi_fra"),
    "gbr": ("00_king_of_britain.txt", "gbr_george_iii_hanover_template"),
    "spa": ("00_charles_iii_spa.txt", "spa_charles_bourbon_iii"),
}
MODIFIER = ROOT / "gfx/portraits/portrait_modifiers/zz_aor1776_historical_powdered_wigs.txt"
MODEL = ROOT / "gfx/models/portraits/attachments/male_hair/aor_frederick_wig"


def starting_characters():
    """Country history uses ?=; reuse the existing string-aware brace parser."""
    for path in sorted((ROOT / "common/history/characters").glob("*.txt")):
        raw = history.read(path)
        cleaned = history.clean_comments(raw)
        depths, pairs = history.brace_maps(cleaned)
        for match in re.finditer(r"(?m)^[ \t]*c:(\w+)\s*\?=\s*\{", cleaned):
            if depths[match.start()] != 1:
                continue
            opening = cleaned.index("{", match.start(), match.end())
            country = history.Block(match.group(1), raw[match.start():pairs[opening]+1], path, 1)
            for character in history.subblocks(country, "create_character"):
                yield country.object_id, character


class HistoricalWigTests(unittest.TestCase):
    def test_exact_named_character_opt_ins(self):
        marked = []
        for tag, character in starting_characters():
            text = history.clean_comments(character.text)
            if FLAG not in text:
                continue
            marked.append((tag, history.scalar(text, "first_name")))
            for key, expected in (("historical", "yes"), ("ruler", "yes")):
                self.assertEqual(history.scalar(text, key), expected, tag)
            self.assertNotEqual(history.scalar(text, "female"), "yes", tag)
            self.assertFalse(history.scalar(text, "dna"), tag)
            self.assertLessEqual(int(history.scalar(text, "birth_date").split(".")[0]), 1758, tag)
            created = history.subblocks(character, "on_created")
            self.assertEqual(len(created), 1, tag)
            self.assertEqual(history.scalar(created[0].text, "set_variable"), FLAG, tag)
        self.assertCountEqual(marked, list(CURATED.items()))

    def test_existing_dna_and_character_template_bindings(self):
        characters = list(starting_characters())
        for tag, (filename, template_name) in DNA.items():
            with self.subTest(tag=tag):
                dna_path = ROOT / "common/dna_data" / filename
                dna = history.named_blocks(dna_path, r"\w+", 0)
                self.assertEqual(len(dna), 1)
                values = history.tokens_flat(history.braced_tokens(dna[0].text, "hairstyles"))
                self.assertEqual(values, ["aor_frederick_wig", "127", "aor_frederick_wig", "127"])
                templates = history.named_blocks(ROOT / "common/character_templates" / f"country_{tag}.txt", r"\w+", 0)
                template = next(t for t in templates if t.object_id == template_name)
                self.assertEqual(history.scalar(template.text, "dna"), dna[0].object_id)
                self.assertTrue(any(country == tag.upper() and history.scalar(char.text, "template") == template_name
                                    for country, char in characters))

    def test_modifier_has_no_unconditional_or_fallback_application(self):
        groups = history.named_blocks(MODIFIER, r"\w+", 0)
        self.assertEqual([g.object_id for g in groups], ["aor1776_historical_powdered_wigs"])
        group = groups[0]
        self.assertEqual(history.scalar(group.text, "usage"), "game")
        self.assertEqual(history.scalar(group.text, "selection_behavior"), "weighted_random")
        entries = history.subblocks(group, r"\w+")
        self.assertEqual([e.object_id for e in entries], ["aor1776_named_ruler_wig"])
        entry = entries[0]
        dna = history.subblocks(entry, "dna_modifiers")[0]
        changes = history.subblocks(dna, r"\w+")
        self.assertEqual([c.object_id for c in changes], ["accessory"])
        for key, expected in (("mode", "replace"), ("gene", "hairstyles"), ("template", "aor_frederick_wig")):
            self.assertEqual(history.scalar(changes[0].text, key), expected)
        weight = history.subblocks(entry, "weight")[0]
        self.assertEqual(history.scalar(weight.text, "base"), "0")
        conditions = history.subblocks(weight, "modifier")
        self.assertEqual(len(conditions), 1)
        condition = conditions[0].text
        self.assertRegex(condition, r"scope:character\s*\?=\s*\{")
        for key, expected in (("has_variable", FLAG), ("is_historical", "yes"), ("is_female", "no"), ("is_adult", "yes")):
            self.assertEqual(history.scalar(condition, key), expected)

    def test_gene_accessory_entity_mesh_and_texture_bindings(self):
        path = ROOT / "common/genes/02_genes_accessories_hairstyles.txt"
        genes = history.named_blocks(path, "accessory_genes", 0)[0]
        hairstyles = history.subblocks(genes, "hairstyles")[0]
        templates = history.subblocks(hairstyles, r"\w+")
        indexes = [history.scalar(t.text, "index") for t in templates]
        self.assertEqual(len(indexes), len(set(indexes)))
        wig = next(t for t in templates if t.object_id == "aor_frederick_wig")
        self.assertEqual(history.scalar(wig.text, "index"), "33")
        self.assertRegex(wig.text, r"male\s*=\s*\{\s*1\s*=\s*aor_frederick_wig\s*\}")
        accessory = history.read(ROOT / "gfx/portraits/accessories/aor_frederick_wig.txt")
        self.assertIn('entity = "aor_frederick_wig_entity"', accessory)
        asset = history.read(MODEL / "aor_frederick_wig.asset")
        history.brace_maps(history.clean_comments(asset))
        self.assertIn('name = "aor_frederick_wig_entity"', asset)
        self.assertIn('pdxmesh = "aor_frederick_wig_mesh"', asset)
        self.assertIn('name = "aor_frederick_wig_mesh"', asset)
        for filename in re.findall(r'(?m)^[ \t]*(?:file|texture_\w+)\s*=\s*"([^"]+)"', asset):
            self.assertTrue((MODEL / filename).is_file(), filename)
        attribution = history.read(MODEL / "LICENSE.txt")
        self.assertIn("hype404", attribution)
        self.assertIn("https://creativecommons.org/licenses/by/4.0/", attribution)


if __name__ == "__main__":
    unittest.main(verbosity=2)
