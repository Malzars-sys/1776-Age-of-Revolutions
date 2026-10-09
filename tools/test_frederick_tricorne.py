"""Static tricorne binding/material checks, NOT an in-game appearance test.

Run: python tools/test_frederick_tricorne.py
Requires Pillow. Optional --game, --pdx and --blender paths enable native checks.
No saves, game files or previews are changed.
"""
import argparse
import hashlib
import importlib.util
import json
import math
import re
import subprocess
import sys
import unittest
from pathlib import Path

import build_start_1776_research_input_pack as history
from test_frederick_wig import dds_levels
from test_historical_wigs import starting_characters

ROOT = Path(__file__).resolve().parents[1]
STEM = "male_headgear_frederick_tricorne"
MODEL = ROOT / "gfx/models/portraits/attachments/male_headgear/prussian/aor1776_frederick_tricorne"
GENE = ROOT / "common/genes/aor1776_tricorne_accessory_gene.txt"
ACCESSORY = ROOT / "gfx/portraits/accessories/aor1776_frederick_tricorne.txt"
MODIFIER = ROOT / "gfx/portraits/portrait_modifiers/zzz_aor1776_frederick_tricorne.txt"
FLAG = "aor1776_frederick_tricorne"
GAME = Path("C:/Games/Victoria 3/game")
PDX = Path("C:/Users/simeo/AppData/Roaming/Blender Foundation/Blender/5.2/extensions/user_default/io_pdx_mesh")
BLENDER = Path("C:/Program Files/Blender Foundation/Blender 5.2/blender.exe")
NATIVE = "gfx/models/portraits/attachments/male_headgear/european_military/05/male_headgear_european_military_05.mesh"


class TricorneBindings(unittest.TestCase):
    def test_special_gene_template_bindings_and_unique_indexes(self):
        containers = history.named_blocks(GENE, "special_genes", 0)
        self.assertEqual(len(containers), 1)
        accessories = history.subblocks(containers[0], "accessory_genes")[0]
        genes = history.subblocks(accessories, r"\w+")
        self.assertEqual([g.object_id for g in genes], ["aor1776_headgear"])
        gene = genes[0]
        self.assertEqual(history.scalar(gene.text, "inheritable"), "no")
        templates = history.subblocks(gene, r"\w+")
        self.assertEqual([t.object_id for t in templates], ["aor1776_no_headgear", FLAG])
        self.assertEqual([history.scalar(t.text, "index") for t in templates], ["0", "1"])
        self.assertRegex(templates[0].text, r"male\s*=\s*\{\s*1\s*=\s*empty\s*\}")
        self.assertRegex(templates[1].text, r"male\s*=\s*\{\s*1\s*=\s*aor1776_frederick_tricorne_headgear\s*\}")
        self.assertRegex(templates[1].text, r"female\s*=\s*\{\s*1\s*=\s*empty\s*\}")

    def test_special_accessory_is_added_not_replaced_in_absent_dna(self):
        group = history.named_blocks(MODIFIER, r"\w+", 0)[0]
        self.assertEqual(history.scalar(group.text, "usage"), "game")
        self.assertEqual(history.scalar(group.text, "selection_behavior"), "weighted_random")
        self.assertFalse(history.scalar(group.text, "fallback"))
        entries = history.subblocks(group, r"\w+")
        self.assertEqual(len(entries), 1)
        entry = entries[0]
        modifiers = history.subblocks(entry, "dna_modifiers")[0]
        changes = history.subblocks(modifiers, r"\w+")
        self.assertEqual([c.object_id for c in changes], ["accessory", "accessory"])
        custom, generic = changes
        for key, value in (("mode", "add"), ("gene", "aor1776_headgear"), ("template", FLAG)):
            self.assertEqual(history.scalar(custom.text, key), value)
        # Only the generic headgear is cleared; neither face nor wig is replaced.
        for key, value in (("mode", "replace"), ("gene", "headgear"), ("template", "no_headgear")):
            self.assertEqual(history.scalar(generic.text, key), value)
        weight = history.subblocks(entry, "weight")[0]
        self.assertEqual(history.scalar(weight.text, "base"), "0")
        condition = history.subblocks(weight, "modifier")[0].text
        self.assertEqual(history.scalar(condition, "add"), "90000")
        self.assertRegex(condition, r"scope:character\s*\?=\s*\{")
        for key, value in (("has_variable", FLAG), ("is_historical", "yes"), ("is_female", "no"), ("is_adult", "yes")):
            self.assertEqual(history.scalar(condition, key), value)

    def test_only_frederick_is_marked_and_face_dna_is_not_used_for_hat(self):
        marked = []
        for tag, character in starting_characters():
            if FLAG not in history.clean_comments(character.text):
                continue
            marked.append((tag, history.scalar(character.text, "first_name")))
            self.assertEqual(history.scalar(character.text, "dna"), "dna_frederick_great_pru")
            created = history.subblocks(character, "on_created")
            self.assertEqual(len(created), 1)
            self.assertEqual(history.scalar(created[0].text, "set_variable"), FLAG)
        self.assertEqual(marked, [("PRU", "Frederick_II")])
        dna = history.read(ROOT / "common/dna_data/00_frederick_great_pru.txt")
        self.assertNotIn("aor1776_headgear", dna)
        self.assertIn('hairstyles = { "aor_frederick_wig" 127 "aor_frederick_wig" 127 }', dna)

    def test_accessory_entity_mesh_and_textures_exist(self):
        accessory = history.named_blocks(ACCESSORY, r"\w+", 0)[0]
        self.assertEqual(accessory.object_id, "aor1776_frederick_tricorne_headgear")
        clean = history.clean_comments(accessory.text)
        self.assertNotIn("no_hair", clean)
        self.assertIn("shared_pose_entity = head", clean)
        self.assertIn('entity = "aor1776_frederick_tricorne_entity"', clean)
        path = MODEL / f"{STEM}.asset"
        mesh, entity = history.named_blocks(path, r"\w+", 0)
        self.assertEqual(mesh.object_id, "pdxmesh")
        self.assertEqual(history.scalar(mesh.text, "name"), "aor1776_frederick_tricorne_mesh")
        self.assertEqual(history.scalar(entity.text, "pdxmesh"), "aor1776_frederick_tricorne_mesh")
        self.assertEqual(history.scalar(entity.text, "name"), "aor1776_frederick_tricorne_entity")
        settings = history.subblocks(mesh, "meshsettings")
        self.assertEqual(len(settings), 1)
        self.assertEqual(history.scalar(settings[0].text, "name"), STEM + "Shape")
        self.assertEqual(history.scalar(settings[0].text, "shader"), "portrait_attachment")
        for filename in re.findall(r'(?m)^\s*(?:file|texture_\w+)\s*=\s*"([^"]+)"', mesh.text):
            self.assertTrue((MODEL / filename).is_file(), filename)
        for identifier in ("aor1776_frederick_tricorne_mesh", "aor1776_frederick_tricorne_entity"):
            definitions = sum(len(re.findall(r'\bname\s*=\s*"' + identifier + r'"', history.read(p)))
                              for p in (ROOT / "gfx/models").rglob("*.asset"))
            self.assertEqual(definitions, 1, identifier)

    def test_dds_mips_and_local_finishing_tiles(self):
        for kind in ("diffuse", "normal", "properties"):
            levels = dds_levels(MODEL / f"{STEM}_{kind}.dds")
            self.assertEqual(len(levels), 11)
            self.assertEqual(levels[0].size, (1024, 1024))
            self.assertEqual(levels[-1].size, (1, 1))
            for level in levels:
                if kind == "diffuse":
                    self.assertEqual(level.getchannel("A").getextrema(), (255, 255))
                elif kind == "normal":
                    self.assertEqual(level.getchannel("R").getextrema(), (128, 128))
                    self.assertEqual(level.getchannel("B").getextrema(), (0, 0))
                else:
                    self.assertEqual(level.getchannel("R").getextrema(), (0,0))
                    self.assertEqual(level.getchannel("B").getextrema(), (0,0))
            base=levels[0]
            if kind=="diffuse":
                self.assertLessEqual(max(v[1] for v in base.crop((0,0,900,1024)).convert("RGB").getextrema()),44)
                ivory=base.getpixel((950,400))
                self.assertTrue(201<=ivory[0]<=213 and 198<=ivory[1]<=210 and 184<=ivory[2]<=196)
                self.assertLessEqual(max(base.getpixel((950,820))[:3]),28)
            elif kind=="properties":
                self.assertEqual(base.getpixel((0,0)),(0,35,0,230))
                self.assertEqual(base.getpixel((950,400)),(0,35,0,225))
                self.assertEqual(base.getpixel((950,820)),(0,50,0,190))

    def test_master_source_and_share_alike_attribution(self):
        archive = ROOT / "docs/portraits/sources/bust_of_frederick_the_great_original.zip"
        self.assertEqual(hashlib.sha256(archive.read_bytes()).hexdigest(),
                         "9b1b574abbd9620eacb55c66a9eb1664b3d307008faa0a10911c2814f6f47f44")
        license_text = history.read(MODEL / "LICENSE.txt")
        self.assertIn("christian.schulz.nuernberg", license_text)
        self.assertIn("https://creativecommons.org/licenses/by-sa/4.0/", license_text)
        bow = ROOT / "docs/portraits/sources/ribbon_bow_original.zip"
        self.assertEqual(hashlib.sha256(bow.read_bytes()).hexdigest(),
                         "aecdf0cdfdf19e822e40bed034d94392e01e9ee920de7045cc681ee6df88b239")
        self.assertIn("Maggatron", license_text)
        self.assertIn("https://creativecommons.org/licenses/by/4.0/", license_text)
        self.assertTrue((ROOT / "docs/portraits/frederick_tricorne_work.blend").is_file())

    def test_portrait_definitions_use_required_bom(self):
        for path in (GENE, ACCESSORY, MODIFIER):
            self.assertTrue(path.read_bytes().startswith(b"\xef\xbb\xbf"), str(path))

    def test_optional_work_blend_keeps_extracted_backups_without_native_geometry(self):
        if not BLENDER.is_file():
            self.skipTest("Blender unavailable; set --blender for work-file checks")
        blend = ROOT / "docs/portraits/frederick_tricorne_work.blend"
        expression = (
            "import bpy,bmesh; from pathlib import Path; "
            f"bpy.ops.wm.open_mainfile(filepath={str(blend)!r}); "
            "meshes=[o for o in bpy.data.objects if o.type=='MESH']; "
            f"assert {{o.name for o in meshes}}=={{{STEM!r},{(STEM+'_extracted_highpoly')!r},{(STEM+'_source_backup')!r}}}; "
            f"assert len(bpy.data.objects[{(STEM+'_source_backup')!r}].data.vertices)==19255; "
            "assert all(len(o.data.uv_layers)>0 for o in meshes); "
            f"bm=bmesh.new(); bm.from_mesh(bpy.data.objects[{(STEM+'_extracted_highpoly')!r}].data); "
            "rim=[v.co.z for v in bm.verts if v.is_boundary and abs(v.co.x)<=2 and v.co.y < -7]; "
            "assert rim and 49.0<=min(rim)<=max(rim)<=50.0, rim; bm.free(); "
            "assert len(bpy.data.images)==3; "
            "assert all(i.packed_file and bytes(i.packed_file.data)==Path(bpy.path.abspath(i.filepath)).read_bytes() for i in bpy.data.images)"
        )
        result = subprocess.run([str(BLENDER), "--background", "--factory-startup", "--python-exit-code", "1",
                                 "--python-expr", expression], capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_optional_native_mode_and_shader_reference(self):
        reference = GAME / "gfx/portraits/portrait_modifiers/01_headgear.txt"
        if not reference.is_file():
            self.skipTest("Victoria 3 not installed at --game path")
        self.assertNotRegex(history.clean_comments(history.read(reference)), r"mode\s*=\s*replace")
        self.assertRegex(history.read(reference), r"mode\s*=\s*add")
        shader = history.read(GAME.parent / "jomini/gfx/FX/jomini/portrait.shader")
        self.assertRegex(shader, r"Effect\s+portrait_attachment\s*\{")

    def test_optional_pdx_mesh_readback_and_exact_native_rigid_skin(self):
        module_path = PDX / "pdx_data.py"
        native_path = GAME / NATIVE
        if not module_path.is_file() or not native_path.is_file():
            self.skipTest("IO PDX or native mesh unavailable; set --pdx and --game")
        spec = importlib.util.spec_from_file_location("tricorne_pdx_data", module_path)
        data = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(data)
        shape = data.read_meshfile(str(MODEL / f"{STEM}.mesh")).find("object")[0]
        native = data.read_meshfile(str(native_path)).find("object")[0]
        self.assertEqual(shape.tag, STEM + "Shape")
        skeleton = shape.find("skeleton")
        self.assertEqual([(b.tag, b.attrib) for b in skeleton], [(b.tag, b.attrib) for b in native.find("skeleton")])
        self.assertEqual(len(skeleton), 61)
        skull = next(b.attrib["ix"][0] for b in skeleton if b.tag == "bn_h_skull")
        meshes = shape.findall("mesh")
        self.assertEqual(len(meshes), 1)
        self.assertEqual(sum(len(m.attrib["tri"]) // 3 for m in meshes), 6378)
        # Additive trim/bow must not change the user-approved felt's positions
        # or UVs, including the low front opening, despite export reordering.
        body=[]
        fringe_triangles=0
        bow_triangles=0
        for mesh in meshes:
            p,u,tri=(mesh.attrib[k] for k in ("p","u0","tri"))
            for i in range(0,len(tri),3):
                ids=tri[i:i+3]
                if all(u[2*j]<.89 for j in ids) or all(u[2*j+1]>.90 for j in ids):
                    body.append(sorted(tuple(round(x,5) for x in p[j*3:j*3+3]+u[j*2:j*2+2]) for j in ids))
                if all(u[2*j]>.92 and .75<u[2*j+1]<.89 for j in ids):
                    bow_triangles+=1
                if all(u[2*j]>.92 and .18<u[2*j+1]<.68 for j in ids):
                    fringe_triangles+=1
        self.assertEqual(bow_triangles,898)
        self.assertLessEqual(bow_triangles,1000)
        self.assertEqual(fringe_triangles,2592)
        self.assertEqual(len(body),2888)
        self.assertEqual(hashlib.sha256(json.dumps(sorted(body),separators=(',',':')).encode()).hexdigest(),
                         '0637e8ad078b936b8e90167c370d12e68132486a454f09e9b4b9186479184089')
        felt_apex=max(point[1] for triangle in body for point in triangle)
        self.assertAlmostEqual(felt_apex,67.15824,places=4)
        bounds = meshes[0].find("aabb").attrib
        lo, hi = bounds["min"], bounds["max"]
        # In PDX, Y is height and Z is depth. Preserve the user's lower,
        # broader/taller fit rather than the rejected 55cm perched opening.
        self.assertGreaterEqual(hi[0] - lo[0], 45.0)
        self.assertLessEqual(hi[0] - lo[0], 48.0)
        self.assertGreaterEqual(hi[1] - lo[1], 22.0)
        self.assertLessEqual(hi[1] - lo[1], 24.0)
        self.assertGreaterEqual(hi[2] - lo[2], 33.0)
        self.assertLessEqual(hi[2] - lo[2], 36.0)
        self.assertGreaterEqual(lo[1], 44.0)
        self.assertLessEqual(lo[1], 45.0)
        self.assertGreaterEqual(hi[1], 66.5)
        # Additive fibre tips rise above the unchanged felt apex, not the cap.
        self.assertLessEqual(hi[1], felt_apex+.95)
        for mesh in meshes:
            vertices = len(mesh.attrib["p"]) // 3
            for key, width in (("p", 3), ("n", 3), ("ta", 4), ("u0", 2)):
                self.assertEqual(len(mesh.attrib[key]), vertices * width)
                self.assertTrue(all(math.isfinite(v) for v in mesh.attrib[key]), key)
            self.assertTrue(all(0 <= i < vertices for i in mesh.attrib["tri"]))
            skin = mesh.find("skin").attrib
            self.assertEqual(skin["bones"], [4])
            self.assertEqual(skin["ix"], [skull, -1, -1, -1] * vertices)
            self.assertEqual(skin["w"], [1.0, 0.0, 0.0, 0.0] * vertices)
            self.assertEqual(mesh.find("material").attrib["shader"], ["portrait_attachment"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--game", type=Path, default=GAME)
    parser.add_argument("--pdx", type=Path, default=PDX)
    parser.add_argument("--blender", type=Path, default=BLENDER)
    args, remainder = parser.parse_known_args()
    GAME, PDX, BLENDER = args.game, args.pdx, args.blender
    unittest.main(argv=[sys.argv[0], *remainder], verbosity=2)
