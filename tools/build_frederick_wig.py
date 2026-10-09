"""Rebuild the attributed Frederick II wig from the author's original FBX ZIP.

Run with the normal Python + Pillow runtime. Blender and an installed IO PDX Mesh
extension are required. Only the wig is exported; no vanilla mesh is redistributed.
Outputs default to ignored cache. Pass --integrate to write the runtime wig folder.
"""
import argparse
import copy
import hashlib
import importlib
import json
import logging
import struct
import subprocess
import sys
import types
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / '.asset-cache' / 'portraits' / 'frederick_wig_build'
RUNTIME = ROOT / 'gfx/models/portraits/attachments/male_hair/aor_frederick_wig'
STEM = 'aor_frederick_wig'
SOURCE_SHA256 = 'fa5c2d3a49663acca307f775b40a67cb797b00994ee3e3e79388a76cc5b6f37c'
HAIR_SHADERS = ('portrait_hair_opaque', 'portrait_hair')
# Local portrait calibration, not a global lighting/shader override. Keep the
# powdered wig light grey, but leave headroom for the portrait's key light.
POWDERED_ALBEDO_SCALE = 0.88
MIN_WIG_ROUGHNESS = 198  # ~0.78, comparable to native European hair, vs source 146.
WIG_SPECULAR = 56       # Retain the native non-metal hair specular strength.


def alpha_coverage(alpha, reference):
    """Fraction passing the native cutoff; alpha is an 8-bit mask, not colour."""
    histogram = alpha.histogram()
    threshold = int(reference * 255) + 1
    return sum(histogram[threshold:]) / sum(histogram)


def scale_alpha_for_coverage(alpha, reference, target):
    """Preserve cutout area after minification, without filling zero-mask gaps.

    Similar in purpose to DirectXTex ScaleMipMapsAlphaForCoverage. The effective
    cutoff accounts for the native portrait_hair 1 + 0.25 * mip alpha boost;
    otherwise that boost and an ordinary coverage correction would compound.
    """
    histogram = alpha.histogram()
    pixels = sum(histogram)

    def measure(scale):
        lut = [min(255, round(value * scale)) for value in range(256)]
        coverage = sum(count for value, count in enumerate(histogram)
                       if lut[value] / 255 > reference) / pixels
        return coverage, lut

    best_coverage, best_lut = measure(1.0)
    best_error = abs(best_coverage - target)
    low, high = 0.0, 256.0
    for _ in range(28):
        scale = (low + high) / 2
        coverage, lut = measure(scale)
        error = abs(coverage - target)
        if error < best_error:
            best_error, best_lut = error, lut
        if coverage < target:
            low = scale
        else:
            high = scale
    return alpha.point(best_lut)


def checked_child(base, relative):
    base = Path(base).resolve()
    child = (base / relative).resolve()
    if child == base or not child.is_relative_to(base):
        raise ValueError(f'Unsafe archive/output path: {relative}')
    return child


def extract_source(archive, target):
    target.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as z:
        for entry in z.infolist():
            path = checked_child(target, entry.filename)
            if entry.is_dir():
                path.mkdir(parents=True, exist_ok=True)
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                with z.open(entry) as src, path.open('wb') as dst:
                    import shutil
                    shutil.copyfileobj(src, dst)


def resize_texture_channels(image, size):
    """Filter packed channels independently: A can be normal Y or roughness.

    Pillow's RGBA resize premultiplies RGB by A. That changes encoded normals
    and specular data, and can erase them wherever the fourth channel is zero.
    """
    from PIL import Image
    if image.size == size:
        return image
    return Image.merge(image.mode, tuple(channel.resize(size, Image.Resampling.LANCZOS)
                                        for channel in image.split()))


def pack_native_normal(normal):
    """Match native UnpackRRxGNormal: X in G, source DirectX Y in A, B=0.

    The shader negates Y on unpack. Zero B deliberately bypasses DNA hair tint
    for this powdered wig. R is not used by that normal decoder.
    """
    from PIL import Image
    nx, ny, _ = normal.convert('RGB').split()
    return Image.merge('RGBA', (Image.new('L', normal.size, 128), nx,
                                Image.new('L', normal.size, 0), ny))


def pack_native_properties(rma):
    """R=SSS mask (off), G=specular, B=metalness, A=perceptual roughness."""
    from PIL import Image
    roughness, metallic, _ao = rma.convert('RGB').split()
    roughness = roughness.point(lambda value: max(MIN_WIG_ROUGHNESS, value))
    return Image.merge('RGBA', (Image.new('L', rma.size, 0),
                                Image.new('L', rma.size, WIG_SPECULAR),
                                metallic, roughness))


def write_dds(image, target, cutout_coverage=None):
    """Legacy A8R8G8B8, complete independent-channel mips; BGRA storage/masks."""
    from PIL import Image
    image = image.convert('RGBA')
    if image.width != image.height or image.width & (image.width - 1):
        raise ValueError('Power-of-two square texture required')
    levels = []
    coverage_report = []
    size = image.width
    while size >= 1:
        if cutout_coverage is None:
            level = resize_texture_channels(image, (size, size))
        else:
            # RGB is valid independently of opacity in the author's padded
            # atlas. Do not premultiply it by the very thin strand mask.
            rgb = image.convert('RGB').resize((size, size), Image.Resampling.LANCZOS)
            alpha = image.getchannel('A').resize((size, size), Image.Resampling.LANCZOS)
            reference = 0.5 / (1.0 + 0.25 * len(levels))
            alpha = scale_alpha_for_coverage(alpha, reference, cutout_coverage)
            level = rgb.convert('RGBA')
            level.putalpha(alpha)
            coverage_report.append({'size':size, 'coverage':alpha_coverage(alpha, reference)})
        levels.append(level.tobytes('raw', 'BGRA'))
        size //= 2
    header = bytearray(128)
    header[:4] = b'DDS '
    values = {4: 124, 8: 0x2100F, 12: image.height, 16: image.width,
              20: image.width * 4, 28: len(levels), 76: 32, 80: 0x41,
              88: 32, 92: 0xFF0000, 96: 0xFF00, 100: 0xFF,
              104: 0xFF000000, 108: 0x401008}
    for offset, value in values.items():
        struct.pack_into('<I', header, offset, value)
    target.write_bytes(bytes(header) + b''.join(levels))
    if coverage_report:
        print(json.dumps({'cutout_texture':target.name, 'source_coverage':cutout_coverage,
                          'mip_coverage':coverage_report}))


def textures(source, output):
    from PIL import Image
    prefix = 'uploads_files_2348854_TX_Wig_01a_'
    size = (1024, 1024)
    albedo = Image.open(source / (prefix + 'ALB.tga')).convert('RGBA')
    source_alpha = albedo.getchannel('A')
    rgb = albedo.convert('RGB').resize(size, Image.Resampling.LANCZOS)
    rgb = rgb.point(lambda value: round(value * POWDERED_ALBEDO_SCALE))
    diffuse = rgb.convert('RGBA')
    diffuse.putalpha(source_alpha.resize(size, Image.Resampling.LANCZOS))
    base_diffuse = rgb.convert('RGBA')
    # The structural curl volumes must write alpha 1 to the portrait target.
    # A separate opaque base texture also prevents accidental cutout fallback.
    base_diffuse.putalpha(255)
    normal = Image.open(source / (prefix + 'NRM.tga')).convert('RGB').resize(size, Image.Resampling.LANCZOS)
    rma = Image.open(source / (prefix + 'RMA.tga')).convert('RGB').resize(size, Image.Resampling.LANCZOS)
    normal_native = pack_native_normal(normal)
    properties = pack_native_properties(rma)
    write_dds(base_diffuse, output / f'{STEM}_base_diffuse.dds')
    write_dds(diffuse, output / f'{STEM}_diffuse.dds',
              cutout_coverage=alpha_coverage(source_alpha, 0.5))
    for suffix, image in [('normal', normal_native), ('properties', properties)]:
        write_dds(image, output / f'{STEM}_{suffix}.dds')


def pdx_modules(extension):
    """Load only installed library modules, without add-on UI/updater/settings writes."""
    package = types.ModuleType('io_pdx_mesh')
    package.__path__ = [str(extension)]
    package.IO_PDX_LOG = logging.getLogger('io_pdx')
    sys.modules['io_pdx_mesh'] = package
    blender_package = types.ModuleType('io_pdx_mesh.pdx_blender')
    blender_package.__path__ = [str(extension / 'pdx_blender')]
    sys.modules['io_pdx_mesh.pdx_blender'] = blender_package
    data = importlib.import_module('io_pdx_mesh.pdx_data')
    exporter = importlib.import_module('io_pdx_mesh.pdx_blender.blender_import_export')
    return data, exporter


def blender_stage(args):
    import bpy
    from mathutils import Matrix, Vector
    from mathutils.kdtree import KDTree
    import xml.etree.ElementTree as ET
    data, pdx = pdx_modules(Path(args.pdx))
    output = Path(args.output)
    source = Path(args.extracted)
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    bpy.ops.import_scene.fbx(filepath=str(source / 'uploads_files_2348854_SM_Wig_01a.fbx'))
    candidates = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    if len(candidates) != 1:
        raise RuntimeError(f'Expected one original wig mesh, found {len(candidates)}')
    wig = candidates[0]
    # Author model is in centimetres. PDX head units are also centimetres;
    # FBX importer adds a 0.01 object scale, which is replaced here.
    wig.scale = (1, 1, 1)
    wig.location = (0, 0, 56)
    bpy.context.view_layer.update()
    transform = wig.matrix_world.copy()
    for vertex in wig.data.vertices:
        vertex.co = transform @ vertex.co
    wig.matrix_world = Matrix.Identity(4)
    wig.name = STEM
    wig.data.name = STEM + 'Shape'
    indices = [p.material_index for p in wig.data.polygons]
    if set(indices) != {0, 1}:
        raise RuntimeError('Original two wig-shell material slots changed')
    wig.data.materials.clear()
    # Use the inner MI_Wig_01a curl volumes as a genuinely opaque wig body;
    # only the slightly expanded MI_Wig_01b shell uses the fine strand mask.
    # Applying the source strand opacity to both shells made the whole wig
    # disappear at the native cutoff. PS_attachment alone was not sufficient:
    # its grey output alpha leaked the background through the portrait GUI.
    for i, shader in enumerate(HAIR_SHADERS):
        diffuse_name = f'{STEM}_base_diffuse.dds' if i == 0 else f'{STEM}_diffuse.dds'
        material = types.SimpleNamespace(shader=[shader],
            diff=[diffuse_name], n=[f'{STEM}_normal.dds'],
            spec=[f'{STEM}_properties.dds'])
        pdx.create_material(material, wig.data, str(output), use_diffuse_alpha=i == 1)
    for polygon, index in zip(wig.data.polygons, indices):
        polygon.material_index = index
        polygon.use_smooth = True
    pdx.set_mesh_index(wig.data, 0)
    meshpath = output / f'{STEM}.mesh'
    pdx.export_meshfile(str(meshpath), exp_skel=False, exp_locs=False, sort_verts='+')

    # Transfer native hair skin weights in engine coordinates. Preserve the exact
    # original inverse-bind matrices: re-exporting zero-scale unused bones would
    # alter them. Only rig metadata/weights are reused, not vanilla geometry.
    hairpath = Path(args.game) / 'gfx/models/portraits/attachments/male_hair/european/male_hair_european_06/male_hair_european_06.mesh'
    original = data.read_meshfile(str(hairpath)).find('object')[0]
    original_mesh = original.find('mesh')
    original_skin = original_mesh.find('skin')
    original_skeleton = original.find('skeleton')
    points = original_mesh.attrib['p']
    bone_count = original_skin.attrib['bones'][0]
    source_ix, source_w = original_skin.attrib['ix'], original_skin.attrib['w']
    tree = KDTree(len(points) // 3)
    for i in range(len(points) // 3):
        tree.insert(Vector(points[i*3:i*3+3]), i)
    tree.balance()
    result = data.read_meshfile(str(meshpath))
    shape = result.find('object')[0]
    head_index = next(b.attrib['ix'][0] for b in original_skeleton if b.tag.split(':')[-1] == 'bn_h_head')
    vertices = 0
    for mesh in shape.findall('mesh'):
        positions = mesh.attrib['p']
        ix, weights = [], []
        for i in range(len(positions) // 3):
            position = Vector(positions[i*3:i*3+3])
            # The long rear queue hangs below the native hair; bind it to the
            # head itself, not the neck, to avoid bending/stretching its ribbon.
            if position.y < 37:
                merged = {head_index: 1.0}
            else:
                merged = {}
                for _, nearest, distance in tree.find_n(position, 3):
                    influence = 1.0 / max(distance, 0.05)**2
                    for j in range(bone_count):
                        bone = source_ix[nearest*bone_count+j]
                        weight = source_w[nearest*bone_count+j]
                        if bone >= 0 and weight > 0:
                            merged[bone] = merged.get(bone, 0) + weight * influence
            strongest = sorted(merged.items(), key=lambda p: (-p[1], p[0]))[:4]
            total = sum(w for _, w in strongest)
            if total <= 0:
                raise RuntimeError('Unweighted wig vertex')
            ix.extend([b for b, _ in strongest] + [-1]*(4-len(strongest)))
            weights.extend([w/total for _, w in strongest] + [0.0]*(4-len(strongest)))
        skin = ET.SubElement(mesh, 'skin')
        skin.attrib.update(bones=[4], ix=ix, w=weights)
        vertices += len(positions) // 3
    shape.append(copy.deepcopy(original_skeleton))
    data.write_meshfile(str(meshpath), result)
    check = data.read_meshfile(str(meshpath)).find('object')[0]
    assert check.find('skeleton').attrib == original_skeleton.attrib
    for a, b in zip(check.find('skeleton'), original_skeleton):
        assert a.tag == b.tag and a.attrib == b.attrib
    for i, mesh in enumerate(check.findall('mesh')):
        assert mesh.find('material').attrib['shader'] == [HAIR_SHADERS[i]], 'Incorrect solid/strand shader assignment'
        p, skin = mesh.attrib['p'], mesh.find('skin').attrib
        assert len(skin['ix']) == len(skin['w']) == len(p)//3*4
        for i in range(len(p)//3):
            assert abs(sum(skin['w'][i*4:i*4+4])-1) < 1e-5
    print(json.dumps({'status':'PASS_WIG_EXPORT', 'vertices':vertices,
                      'triangles':sum(len(m.attrib['tri'])//3 for m in check.findall('mesh')),
                      'materials':len(check.findall('mesh')), 'bind_matrices_preserved':True}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', default=str(ROOT / 'docs/portraits/sources/wig_hype404_original.zip'))
    parser.add_argument('--game', required=True, help='Victoria 3 game directory')
    parser.add_argument('--blender', required=True, help='Installed blender.exe')
    parser.add_argument('--pdx', required=True, help='Installed io_pdx_mesh directory')
    parser.add_argument('--output', default=str(CACHE / 'runtime'))
    parser.add_argument('--integrate', action='store_true')
    parser.add_argument('--blender-stage', action='store_true')
    parser.add_argument('--extracted')
    args = parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else None)
    if args.blender_stage:
        blender_stage(args)
        return
    source = Path(args.source).resolve()
    if SOURCE_SHA256 and hashlib.sha256(source.read_bytes()).hexdigest() != SOURCE_SHA256:
        raise RuntimeError('Original source archive hash changed')
    output = RUNTIME if args.integrate else Path(args.output).resolve()
    if not output.is_relative_to(ROOT) or output == ROOT:
        raise ValueError('Output must remain inside this repository')
    output.mkdir(parents=True, exist_ok=True)
    extracted = CACHE / 'original'
    extract_source(source, extracted)
    textures(extracted, output)
    command = [args.blender, '--background', '--factory-startup', '--python-exit-code', '1',
               '--python', str(Path(__file__).resolve()), '--', '--blender-stage',
               '--source', str(source), '--game', args.game, '--pdx', args.pdx,
               '--blender', args.blender, '--output', str(output), '--extracted', str(extracted)]
    subprocess.run(command, check=True)
    print(json.dumps({'output':str(output), 'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in sorted(output.glob('*')) if p.suffix in {'.mesh','.dds'}}}))


if __name__ == '__main__':
    main()
