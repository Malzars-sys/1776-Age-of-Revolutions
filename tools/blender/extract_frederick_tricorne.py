"""Inspect/extract the supplied CC BY-SA Frederick bust using installed Blender.

Native assets are local technical references only, never copied into deliverables.
All diagnostic renders and unpacked archives stay in the ignored asset cache.
"""
import argparse
import copy
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from build_frederick_wig import checked_child, pdx_modules, write_dds

CACHE = ROOT / '.asset-cache/portraits/frederick_tricorne'
SOURCE_SHA = '9b1b574abbd9620eacb55c66a9eb1664b3d307008faa0a10911c2814f6f47f44'
BOW_SOURCE = ROOT/'docs/portraits/sources/ribbon_bow_original.zip'
BOW_SOURCE_SHA = 'aecdf0cdfdf19e822e40bed034d94392e01e9ee920de7045cc681ee6df88b239'
REFERENCES = [
    'gfx/models/portraits/attachments/male_headgear/european_military/05/male_headgear_european_military_05.mesh',
    'gfx/models/portraits/attachments/male_headgear/european_common/01/male_headgear_european_common_01.mesh',
    'gfx/models/portraits/attachments/male_headgear/european_common/03/male_headgear_european_common_03.mesh',
]
WIG = ROOT / 'gfx/models/portraits/attachments/male_hair/aor_frederick_wig/aor_frederick_wig.mesh'
STEM = 'male_headgear_frederick_tricorne'
RUNTIME = ROOT / 'gfx/models/portraits/attachments/male_headgear/prussian/aor1776_frederick_tricorne'
WORK = ROOT / 'docs/portraits/frederick_tricorne_work.blend'
# Revised from the user's in-game fit feedback, not just a neutral-head BVH.
# The painting places the front opening just above the brows (~49cm native).
# Lower the opening while deepening the crown so the upper wig stays covered.
SOURCE_BASE_Z = 2.088842
FIT_SCALE = (27.5, 36.0, 24.0)
FIT_BASE_Z = 44.5
FIT_DEPTH_OFFSET = 3.5
CROWN_WIG_CLEARANCE_CM = 0.7
CENTRAL_PEAK_LIFT_CM = 4.0


def source_opening_seam(x, y):
    return 2.30-0.21*min(abs(x)/0.76, 1.0)**1.5+0.01*y


def fitted_point(x, y, z):
    """Source +Y faces rearward after conversion to native portrait -Y."""
    # A triangular central rise sharpens the silhouette. Its influence is zero
    # at the opening, so making the crown taller cannot perch the hat again.
    above_seam = max(z-source_opening_seam(x, y), 0.0)
    peak = (CENTRAL_PEAK_LIFT_CM*min(above_seam/0.55, 1.0)
            *max(1.0-abs(x)/0.80, 0.0)**2)
    return (-x*FIT_SCALE[0], -y*FIT_SCALE[1]+FIT_DEPTH_OFFSET,
            (z-SOURCE_BASE_Z)*FIT_SCALE[2]+FIT_BASE_Z+peak)


def unpack(archive):
    archive = Path(archive)
    assert hashlib.sha256(archive.read_bytes()).hexdigest() == SOURCE_SHA
    target = CACHE / 'source'
    target.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as outer:
        with zipfile.ZipFile(io.BytesIO(outer.read('source/upload_scan.zip'))) as inner:
            for item in inner.infolist():
                if item.is_dir():
                    continue
                path = checked_child(target, item.filename)
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(inner.read(item))
    sources = list(target.glob('*.obj'))
    assert len(sources) == 1
    return sources[0]


def object_summary(obj):
    points = [obj.matrix_world @ v.co for v in obj.data.vertices]
    return {'name':obj.name, 'vertices':len(points),
            'triangles':sum(len(f.vertices)-2 for f in obj.data.polygons),
            'bounds':[[min(v[i] for v in points),max(v[i] for v in points)] for i in range(3)],
            'uv_layers':list(obj.data.uv_layers.keys()),
            'vertex_groups':list(obj.vertex_groups.keys()),
            'modifiers':[(m.type,m.name) for m in obj.modifiers]}


def import_bow_source():
    """Import the user's actual FBX, keeping the original ZIP unmodified."""
    import bpy
    assert hashlib.sha256(BOW_SOURCE.read_bytes()).hexdigest()==BOW_SOURCE_SHA
    target=CACHE/'ribbon_bow_source'
    with zipfile.ZipFile(BOW_SOURCE) as z:
        for item in z.infolist():
            if item.is_dir():continue
            path=checked_child(target,item.filename);path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes(z.read(item))
    prior=set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=str(target/'source/ribbon bow.fbx'))
    objects=set(bpy.data.objects)-prior
    meshes=sorted((o for o in objects if o.type=='MESH'),key=lambda o:o.name)
    if not meshes:raise RuntimeError('Ribbon FBX contains no mesh')
    report=[object_summary(o) for o in meshes]
    select_only(meshes,active=meshes[0])
    bpy.ops.object.join()
    bow=bpy.context.object
    bow['source_parts']=json.dumps(report)
    return bow, set(bpy.data.objects)-prior


def inspect_bow():
    import bpy
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
    bow,_=import_bow_source()
    plain_material(bow,(.15,.15,.15))
    report=object_summary(bow)
    render_views(bow,'ribbon_source')
    (CACHE/'ribbon_source.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report))


def render_views(obj, prefix):
    import bpy
    from mathutils import Vector
    scene = bpy.context.scene
    points = [obj.matrix_world @ v.co for v in obj.data.vertices]
    lo = Vector(tuple(min(p[i] for p in points) for i in range(3)))
    hi = Vector(tuple(max(p[i] for p in points) for i in range(3)))
    centre = (lo+hi)/2
    size = max(hi-lo)
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 12
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 640
    scene.render.resolution_y = 640
    scene.render.resolution_percentage = 100
    scene.world.color = (0.15,0.15,0.15)
    bpy.ops.object.camera_add()
    camera = bpy.context.object
    camera.data.type = 'ORTHO'
    camera.data.ortho_scale = size*1.2
    scene.camera = camera
    bpy.ops.object.light_add(type='AREA',location=centre+Vector((size,-size,size)))
    key = bpy.context.object
    key.data.energy = size*size*100
    key.data.shape = 'DISK'
    key.data.size = size
    key.rotation_euler = (centre-key.location).to_track_quat('-Z','Y').to_euler()
    for name,direction in [('front',(0,-1,0.15)),('back',(0,1,0.15)),('right',(1,0,0.15)),('top',(0,-0.15,1))]:
        camera.location = centre+Vector(direction)*size*3
        camera.rotation_euler = (centre-camera.location).to_track_quat('-Z','Y').to_euler()
        scene.render.filepath = str(CACHE / (prefix+'_'+name+'.png'))
        bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(camera,do_unlink=True)
    bpy.data.objects.remove(key,do_unlink=True)


def plain_material(obj, colour, roughness=0.8):
    import bpy
    obj.data.materials.clear()
    mat = bpy.data.materials.new(obj.name + '_diagnostic')
    mat.use_nodes = True
    shader = mat.node_tree.nodes.get('Principled BSDF')
    shader.inputs['Base Color'].default_value = (*colour, 1)
    shader.inputs['Roughness'].default_value = roughness
    obj.data.materials.append(mat)
    for face in obj.data.polygons:
        face.material_index = 0
        face.use_smooth = True


def blender_fit(args):
    """Fit candidate to actual head/wig geometry; references remain cache-only."""
    import bpy
    from mathutils import Vector
    from mathutils.bvhtree import BVHTree
    data, pdx = pdx_modules(Path(args.pdx))
    bpy.ops.wm.open_mainfile(filepath=str(CACHE / 'extraction_candidate.blend'))
    hat = next(o for o in bpy.context.scene.objects if o.type == 'MESH')
    # Source bust faces +Y; installed portrait assets face -Y. Fit in centimetres.
    for vertex in hat.data.vertices:
        x, y, z = vertex.co
        vertex.co = fitted_point(x, y, z)
    clearance = fit_upper_wig_clearance(hat, pdx)
    plain_material(hat, (0.035, 0.031, 0.025))
    meshes = []
    for path, colour in [(WIG, (0.62, 0.61, 0.59)),
                          (Path(args.game)/'gfx/models/portraits/male_head/male_head.mesh', (0.38, 0.24, 0.16))]:
        prior=set(bpy.data.objects)
        pdx.import_meshfile(str(path), imp_locs=False)
        added=set(bpy.data.objects)-prior
        for obj in added:
            if obj.type == 'MESH':
                plain_material(obj, colour)
                meshes.append(obj)
    hat.data.update()
    def bvh(obj):
        obj.data.calc_loop_triangles()
        return BVHTree.FromPolygons([obj.matrix_world @ v.co for v in obj.data.vertices],
                                   [tuple(t.vertices) for t in obj.data.loop_triangles], all_triangles=True)
    report = {'hat':object_summary(hat), 'references':[object_summary(o) for o in meshes],
              'crown_wig_clearance':clearance}
    report['surface_triangle_overlaps'] = {o.name:len(bvh(hat).overlap(bvh(o))) for o in meshes}
    # Frame the complete head/wig instead of the hat alone.
    camera_bounds = bpy.data.objects.new('fit_frame', hat.data.copy())
    bpy.context.collection.objects.link(camera_bounds)
    camera_bounds.hide_render = True
    all_points = [v.co.copy() for obj in [hat]+meshes for v in obj.data.vertices]
    camera_bounds.data.clear_geometry()
    camera_bounds.data.from_pydata(all_points, [], [])
    render_views(camera_bounds, 'fit')
    bpy.data.objects.remove(camera_bounds, do_unlink=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(CACHE/'fit_candidate.blend'))
    (CACHE/'fit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report))


def blender_inspect(args):
    import bpy
    import bmesh
    data,pdx = pdx_modules(Path(args.pdx))
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    bpy.ops.wm.obj_import(filepath=args.obj,forward_axis='NEGATIVE_Z',up_axis='Y')
    candidates = [o for o in bpy.context.scene.objects if o.type=='MESH']
    assert len(candidates)==1
    source = candidates[0]
    report = {'source':object_summary(source),'references':[]}
    bm = bmesh.new()
    bm.from_mesh(source.data)
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
    bm.verts.ensure_lookup_table()
    unseen = set(bm.verts)
    components = []
    while unseen:
        seed=unseen.pop(); group={seed}; queue=[seed]
        while queue:
            v=queue.pop()
            for edge in v.link_edges:
                other=edge.other_vert(v)
                if other in unseen:
                    unseen.remove(other);group.add(other);queue.append(other)
        components.append({'vertices':len(group),'bounds':[[min(v.co[i] for v in group),max(v.co[i] for v in group)] for i in range(3)]})
    report['welded_components']=sorted(components,key=lambda c:-c['vertices'])[:12]
    bm.free()
    render_views(source,'source')
    source.hide_render=True
    for relative in REFERENCES:
        prior=set(bpy.data.objects)
        pdx.import_meshfile(str(Path(args.game)/relative),imp_locs=False)
        added=set(bpy.data.objects)-prior
        report['references'].extend(object_summary(o) for o in added if o.type=='MESH')
        for obj in added:
            bpy.data.objects.remove(obj,do_unlink=True)
    (CACHE/'inspection.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report))


def blender_extract(args, diagnostics=True):
    """Candidate seam cut: curved boundary, not a destructive cut of the source."""
    import bpy
    import bmesh
    from mathutils import Matrix
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    bpy.ops.wm.obj_import(filepath=args.obj,forward_axis='NEGATIVE_Z',up_axis='Y')
    source=next(o for o in bpy.context.scene.objects if o.type=='MESH')
    matrix=source.matrix_world.copy()
    for v in source.data.vertices:
        v.co=matrix @ v.co
    source.matrix_world=Matrix.Identity(4)
    bm=bmesh.new();bm.from_mesh(source.data)
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
    # Temporarily flatten the selected anatomical seam, perform an exact cut,
    # then restore positions. New intersection vertices retain interpolated UVs.
    for v in bm.verts:
        v.co.z-=source_opening_seam(v.co.x,v.co.y)
    bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),
                          plane_co=(0,0,0),plane_no=(0,0,1),clear_inner=True)
    for v in bm.verts:
        v.co.z+=source_opening_seam(v.co.x,v.co.y)
    bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS')
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    bm.to_mesh(source.data);bm.free();source.data.update()
    source.name=STEM
    if diagnostics:
        render_views(source,'extracted')
        bpy.ops.wm.save_as_mainfile(filepath=str(CACHE/'extraction_candidate.blend'))
    print(json.dumps(object_summary(source)))
    return source


def select_only(objects, active=None):
    import bpy
    bpy.ops.object.select_all(action='DESELECT')
    for obj in objects:
        obj.hide_set(False)
        obj.select_set(True)
    bpy.context.view_layer.objects.active = active or objects[-1]


def surface_bvh(obj):
    from mathutils.bvhtree import BVHTree
    obj.data.calc_loop_triangles()
    return BVHTree.FromPolygons([obj.matrix_world @ v.co for v in obj.data.vertices],
                               [tuple(t.vertices) for t in obj.data.loop_triangles], all_triangles=True)


def fit_upper_wig_clearance(hat, pdx):
    """Widen only the crown where the unchanged wig would pierce the felt.

    Horizontal rays measure the outer wig envelope. The open forehead seam is
    preserved; adjustment blends in above 50cm, leaving the side curls exposed.
    Source UVs and the untouched extract remain on the separate backup mesh.
    """
    import bpy
    from math import sqrt
    from mathutils import Vector
    prior = set(bpy.data.objects)
    pdx.import_meshfile(str(WIG), imp_locs=False)
    imported = set(bpy.data.objects)-prior
    wig = next(o for o in imported if o.type == 'MESH')
    tree = surface_bvh(wig)
    changed = 0
    maximum = 0.0
    for vertex in hat.data.vertices:
        point = vertex.co
        blend = min(max((point.z-50.0)/2.0, 0.0), 1.0)
        if not blend:
            continue
        origin = Vector((0.0, 2.5, point.z))
        direction = point-origin
        radius = direction.length
        if radius < 1e-5:
            continue
        direction.normalize()
        cursor = origin.copy()
        outer = None
        # Both wig shells/strands may be hit; use the outermost, not first hit.
        for _ in range(24):
            hit, _, _, _ = tree.ray_cast(cursor, direction, 60.0)
            if hit is None:
                break
            outer = (hit-origin).length
            cursor = hit+direction*0.02
        if outer is None:
            continue
        difference = outer+CROWN_WIG_CLEARANCE_CM-radius
        if difference <= -1.5:
            continue
        # Smooth maximum avoids a sharp crease at the edge of the correction.
        displacement = blend*0.5*(difference+sqrt(difference*difference+0.09))
        vertex.co += direction*displacement
        changed += 1
        maximum = max(maximum, displacement)
    hat.data.update()
    for obj in imported:
        bpy.data.objects.remove(obj, do_unlink=True)
    return {'adjusted_vertices':changed, 'max_displacement_cm':maximum,
            'target_clearance_cm':CROWN_WIG_CLEARANCE_CM,
            'forehead_seam_preserved_below_cm':50.0}


def bake_normal(high, low):
    import bpy
    size = 1024
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 16
    image = bpy.data.images.new('aor1776_tricorne_detail_bake', width=size, height=size,
                                float_buffer=False, is_data=True)
    image.generated_color = (0.5, 0.5, 1, 1)
    mat = bpy.data.materials.new('aor1776_tricorne_bake_target')
    mat.use_nodes = True
    node = mat.node_tree.nodes.new('ShaderNodeTexImage')
    node.image = image
    mat.node_tree.nodes.active = node
    low.data.materials.clear()
    low.data.materials.append(mat)
    select_only([high, low], low)
    scene.render.bake.use_selected_to_active = True
    scene.render.bake.cage_extrusion = 0.7
    scene.render.bake.max_ray_distance = 1.4
    scene.render.bake.margin = 12
    # IO PDX flips texture V and spatial handedness; its stored tangent W is
    # unchanged. The native UnpackRRxGNormal negates A, yielding Blender's +Y
    # tangent normal after the handedness conversion. Bake OpenGL (+Y) here.
    scene.render.bake.normal_space = 'TANGENT'
    scene.render.bake.normal_r = 'POS_X'
    scene.render.bake.normal_g = 'POS_Y'
    scene.render.bake.normal_b = 'POS_Z'
    bpy.ops.object.bake(type='NORMAL')
    image.filepath_raw = str(CACHE/'baked_normal.png')
    image.file_format = 'PNG'
    image.save()
    return image


def add_hat_finishes(hat, high):
    """Add a pale fibrous fringe and a black ribbon bow, without moving felt.

    Finishing geometry uses previously unused atlas tiles. Keeping the same
    material/rig avoids extra entities, texture copies or hairstyle changes.
    """
    import bpy
    import bmesh
    from math import cos, sin, pi, radians
    import random
    from mathutils import Vector, Matrix
    tree = surface_bvh(hat)
    vertices, faces, uvs = [], [], []

    def vertex(point):
        vertices.append(tuple(point))
        return len(vertices)-1

    def face(indices, coords):
        faces.append(tuple(indices))
        uvs.append(coords)

    # Follow the real upper crest of the approved scan, not the low head opening.
    source_points = [v.co.copy() for v in hat.data.vertices]
    lo, hi = min(p.x for p in source_points)+0.35, max(p.x for p in source_points)-0.35
    ridge, front_ridge = [], []
    path_segments = 60
    ring_sides = 4
    for i in range(path_segments+1):
        x = lo+(hi-lo)*i/path_segments
        # Exact plane/triangle intersections on the final approved surface.
        # Sampling the highpoly, then nearest-projecting to the lowpoly, can
        # jump to an inward-facing fold and put the trim across a hat panel.
        section = []
        for triangle in hat.data.loop_triangles:
            points = [source_points[j] for j in triangle.vertices]
            for a,b in zip(points, points[1:]+points[:1]):
                if (a.x-x)*(b.x-x)<=0 and abs(a.x-b.x)>1e-6:
                    section.append(a.lerp(b, (x-a.x)/(b.x-a.x)))
        # The back crest is visible above the front fold in the portrait's
        # slightly elevated view. Follow its upper envelope, not that inner
        # fold's absolute-Z maximum (which reads as a stripe across the felt).
        ridge.append(max(section, key=lambda p:p.z+0.15*p.y).copy())
        front_candidates=[p for p in section if p.y<5.0]
        if not front_candidates:
            raise RuntimeError('Front rim is missing in the approved hat section')
        front_ridge.append(max(front_candidates,key=lambda p:p.z).copy())
    radius = 0.17  # Small undercoat beneath the irregular, raised fibres.

    def fringe(path,seed,skip=()):
        # Reject isolated inner-fold jumps. Split real folded-rim switches
        # rather than drawing a chord across a hat panel.
        for i in range(1,len(path)-1):
            a,p,b=path[i-1:i+2]
            if abs(a.y-b.y)<1.5 and abs(p.y-(a.y+b.y)/2)>2.0:
                path[i]=a.lerp(b,.5)
        breaks={i for i in range(path_segments) if abs(path[i+1].y-path[i].y)>3.0}
        breaks.update(skip)
        centres,normals=[],[]
        for point in path:
            _,normal,_,_=tree.find_nearest(point)
            centres.append(point+Vector((0,0,.09)));normals.append(normal)
        base=len(vertices)
        for i,(point,normal) in enumerate(zip(centres,normals)):
            tangent=(centres[min(i+1,path_segments)]-centres[max(i-1,0)]).normalized()
            across=tangent.cross(normal).normalized()
            outward=across.cross(tangent).normalized()
            for side in range(ring_sides):
                angle=2*pi*side/ring_sides
                vertex(point+radius*(cos(angle)*across+sin(angle)*outward))
        for i in range(path_segments):
            if i in breaks:continue
            for side in range(ring_sides):
                other=(side+1)%ring_sides
                face((base+i*ring_sides+side,base+i*ring_sides+other,
                      base+(i+1)*ring_sides+other,base+(i+1)*ring_sides+side),
                     [(0.925+side/ring_sides*0.055,0.33+i/path_segments*0.48),
                      (0.925+(side+1)/ring_sides*0.055,0.33+i/path_segments*0.48),
                      (0.925+(side+1)/ring_sides*0.055,0.33+(i+1)/path_segments*0.48),
                      (0.925+side/ring_sides*0.055,0.33+(i+1)/path_segments*0.48)])
        # Tapered solid fibres give the fringe its irregular silhouette. No
        # alpha-blended shell; a fixed seed preserves the approved rear trim.
        rng=random.Random(seed)
        count=0
        for i in range(path_segments):
            if i in breaks:continue
            tangent=(centres[i+1]-centres[i]).normalized()
            lift=Vector((-tangent.z,0,tangent.x)).normalized()
            normal=(normals[i]+normals[i+1]).normalized()
            for strand in range(4):
                t=(strand+.25+rng.random()*.5)/4
                root=centres[i].lerp(centres[i+1],t)+normal*rng.uniform(-.07,.12)
                direction=(lift+normal*rng.uniform(-.30,.30)+tangent*rng.uniform(-.25,.25)).normalized()
                length=rng.uniform(.45,.85)
                across=direction.cross(tangent).normalized()
                other=direction.cross(across).normalized()
                start=len(vertices)
                width=rng.uniform(.055,.085)
                for side in range(3):
                    angle=2*pi*side/3
                    vertex(root+width*(cos(angle)*across+sin(angle)*other))
                vertex(root+direction*length)
                for side in range(3):
                    face((start+side,start+(side+1)%3,start+3),
                         [(0.933,.42),(0.951,.42),(0.944,.74)])
                face((start+2,start+1,start),[(.933,.42),(.951,.42),(.944,.74)])
                count+=1
        return {'fibres':count,'path_breaks':sorted(breaks)}

    rear_fringe=fringe(ridge,177607)
    # The two raised brim faces have different crests: the rear-only envelope
    # hides the front fringe. Follow its own highest front-facing edge too,
    # skipping already-covered sections where both crests physically coincide.
    covered={i for i in range(path_segments)
             if max((front_ridge[j]-ridge[j]).length for j in (i,i+1))<.5}
    front_fringe=fringe(front_ridge,177608,covered)
    fibre_count=rear_fringe['fibres']+front_fringe['fibres']
    trim_end = len(vertices)

    # The scan's raised cockade/bow base lies on the right front face.
    anchor, normal, _, _ = tree.ray_cast((6.2,-100,60.0), (0,1,0), 150.0)
    if anchor is None:
        raise RuntimeError('Bow mount is no longer on the approved hat')

    def bow_uv(u, v):
        return (0.925+u*0.055, 0.14+v*0.09)

    # Use the supplied Ribbon Bow, not the earlier procedural stand-in. The
    # pristine FBX archive is the regeneration master; only a small collapsed
    # derivative is merged into the runtime hat. Never export the 48k source.
    bow, imported = import_bow_source()
    source_summary = object_summary(bow)
    bow.data.transform(bow.matrix_world)
    bow.matrix_world = Matrix.Identity(4)
    select_only([bow])
    decimate = bow.modifiers.new('portrait_bow_budget', 'DECIMATE')
    decimate.ratio = 900/source_summary['triangles']
    decimate.use_collapse_triangulate = True
    bpy.ops.object.modifier_apply(modifier=decimate.name)
    bow.data.calc_loop_triangles()
    bow_triangles = len(bow.data.loop_triangles)
    if not 400 <= bow_triangles <= 1000:
        raise RuntimeError(f'Ribbon bow exceeded the portrait budget: {bow_triangles}')
    # Turn its two real ribbon loops upright, as in the painting. The central
    # binding covers the scanned bump; short tails run down and to one side.
    angle, scale = radians(65), 1.7
    bow_points=[]
    clearance=.35
    for v in bow.data.vertices:
        x,y,z=v.co
        u=scale*(cos(angle)*x-sin(angle)*y)
        v_up=scale*(sin(angle)*x+cos(angle)*y)
        hit,_,_,_=tree.ray_cast((anchor.x+u,-100,anchor.z+v_up),(0,1,0),150)
        if hit is not None:
            clearance=max(clearance,anchor.y-hit.y-scale*z+.25)
        bow_points.append((u,v_up,scale*z))
    start = len(vertices)
    for u,v_up,depth in bow_points:
        # Keep the actual folded loops intact. Projecting the backing to each
        # front/rear scan fold would stretch the bow badly in profile.
        vertex(anchor+Vector((u,-clearance-depth,v_up)))
    for triangle in bow.data.loop_triangles:
        ids = tuple(triangle.vertices)
        coords = [bow_uv((bow.data.vertices[j].co.x+2)/4,
                         (bow.data.vertices[j].co.y+1.6)/2.2) for j in ids]
        face(tuple(start+j for j in ids),coords)
    for obj in imported:
        bpy.data.objects.remove(obj,do_unlink=True)

    bm = bmesh.new(); bm.from_mesh(hat.data)
    uv = bm.loops.layers.uv.active
    layer = bm.faces.layers.int.new('aor1776_finish')
    added = [bm.verts.new(point) for point in vertices]
    new_faces = []
    for indices, coords in zip(faces, uvs):
        f = bm.faces.new([added[i] for i in indices]); f[layer]=1
        for loop, coord in zip(f.loops, coords):
            loop[uv].uv = coord
        f.smooth = True
        new_faces.append(f)
    bmesh.ops.recalc_face_normals(bm,faces=new_faces)
    bmesh.ops.triangulate(bm,faces=new_faces)
    bm.to_mesh(hat.data); bm.free(); hat.data.update()
    return {'trim_radius_cm':radius,'trim_path_points':len(ridge),
            'fringe_fibres':fibre_count,'fringe_length_cm':[.45,.85],
            'rear_fringe':rear_fringe,'front_fringe':front_fringe,
            'trim_vertices':trim_end,'bow_anchor_cm':list(anchor),
            'bow_vertices':len(vertices)-trim_end,
            'bow_triangles':bow_triangles,'bow_source_triangles':source_summary['triangles'],
            'bow_source':'Ribbon Bow by Maggatron (MaggaModels), CC BY 4.0',
            'bow_scale_cm_per_source_unit':scale,'bow_rotation_degrees':65,
            'bow_mount_clearance_cm':clearance,
            'body_vertices_moved':0, 'shared_material_atlas':True}


def native_export(args, hat, data, pdx, original):
    import xml.etree.ElementTree as ET
    output = Path(args.output)
    pdx.set_mesh_index(hat.data, 0)
    meshpath = output / f'{STEM}.mesh'
    # Export topology/tangents/UVs with the installed plugin. Preserve native
    # bind matrices separately: unused zero-scale bones are changed on import.
    select_only([hat])
    pdx.export_meshfile(str(meshpath), exp_skel=False, exp_locs=False, sort_verts='+')
    result = data.read_meshfile(str(meshpath))
    shape = result.find('object')[0]
    skeleton = original.find('skeleton')
    index = next(b.attrib['ix'][0] for b in skeleton if b.tag.split(':')[-1] == 'bn_h_skull')
    for mesh in shape.findall('mesh'):
        old = mesh.find('skin')
        if old is not None:
            mesh.remove(old)
        count = len(mesh.attrib['p'])//3
        skin = ET.SubElement(mesh, 'skin')
        skin.attrib.update(bones=[4], ix=[index,-1,-1,-1]*count, w=[1.0,0.0,0.0,0.0]*count)
    old = shape.find('skeleton')
    if old is not None:
        shape.remove(old)
    shape.append(copy.deepcopy(skeleton))
    data.write_meshfile(str(meshpath), result)
    check = data.read_meshfile(str(meshpath)).find('object')[0]
    assert [(b.tag,b.attrib) for b in check.find('skeleton')] == [(b.tag,b.attrib) for b in skeleton]
    return {'triangles':sum(len(m.attrib['tri'])//3 for m in check.findall('mesh')),
            'vertices':sum(len(m.attrib['p'])//3 for m in check.findall('mesh')),
            'materials':len(check.findall('mesh')), 'bone':'bn_h_skull', 'bone_index':index,
            'native_bind_matrices_preserved':True}


def blender_build(args):
    import bpy
    import bmesh
    from mathutils import Vector
    from math import radians
    data,pdx = pdx_modules(Path(args.pdx))
    high = blender_extract(args, diagnostics=False)
    high.name = STEM + '_extracted_highpoly'
    high.data.name = high.name + 'Shape'
    original_summary = object_summary(high)
    # Keep the unoptimized extract and its usable source UVs in the work file.
    backup = high.copy(); backup.data = high.data.copy()
    backup.name = STEM + '_source_backup'
    backup.data.name = backup.name + 'Shape'
    bpy.context.collection.objects.link(backup)
    backup.hide_render = True
    backup.hide_set(True)
    backup.use_fake_user = True
    for vertex in high.data.vertices:
        vertex.co = fitted_point(*vertex.co)
    high.data.update()
    crown_clearance = fit_upper_wig_clearance(high, pdx)
    high.data.normals_split_custom_set([(0,0,0)]*len(high.data.loops))
    for f in high.data.polygons:
        f.use_smooth = True
    # Use the actual native bicorne's outer-surface budget, not an arbitrary cap.
    reference_path = Path(args.game)/REFERENCES[0]
    original = data.read_meshfile(str(reference_path)).find('object')[0]
    benchmark = sum(len(m.attrib['tri'])//3 for m in original.findall('mesh'))
    low = high.copy(); low.data = high.data.copy()
    low.name = STEM; low.data.name = STEM+'Shape'
    bpy.context.collection.objects.link(low)
    select_only([low])
    decimate = low.modifiers.new('Native_bicorne_triangle_budget','DECIMATE')
    # Reserve part of the native reference budget for an inner felt shell.
    # Normal baking keeps scanned braid/cockade relief on the lighter exterior.
    decimate.ratio = (benchmark*0.65)/original_summary['triangles']
    bpy.ops.object.modifier_apply(modifier=decimate.name)
    # New UV atlas for the bake; retain the original UVs only on the backup.
    for layer in list(low.data.uv_layers):
        low.data.uv_layers.remove(layer)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=radians(66), island_margin=0.025)
    bpy.ops.object.mode_set(mode='OBJECT')
    for uv in low.data.uv_layers.active.data:
        uv.uv *= 0.88  # Reserve a flat-normal patch for the new inner lining.
    high_tree = surface_bvh(high)
    deviation = max(high_tree.find_nearest(v.co)[3] for v in low.data.vertices)
    normal_image = bake_normal(high,low)
    high.hide_render = True; high.hide_set(True)
    # A thin, open-bottom shell gives a real lining, not an opaque plate across
    # the head opening. Solidify follows the extracted seam and closes only rim.
    select_only([low])
    outside_faces = len(low.data.polygons)
    solid = low.modifiers.new('Thin_felt_lining','SOLIDIFY')
    solid.thickness = 0.12; solid.offset = -1
    bpy.ops.object.modifier_apply(modifier=solid.name)
    uv = low.data.uv_layers.active
    lining_uv = [(0.93,0.02),(0.98,0.02),(0.98,0.07),(0.93,0.07)]
    for face in list(low.data.polygons)[outside_faces:]:
        for corner, loop in enumerate(face.loop_indices):
            uv.data[loop].uv = lining_uv[corner]
    bm=bmesh.new(); bm.from_mesh(low.data)
    bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS')
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    bmesh.ops.triangulate(bm,faces=list(bm.faces))
    bm.to_mesh(low.data); bm.free(); low.data.update()
    body_summary = object_summary(low)
    finishes = add_hat_finishes(low, high)
    finishes['triangles'] = object_summary(low)['triangles']-body_summary['triangles']
    # Import references for measured clearance only; never save native geometry
    # in the work blend or export it to the mod.
    refs=[]; rigs=[]
    for path in [WIG, Path(args.game)/'gfx/models/portraits/male_head/male_head.mesh', reference_path]:
        prior=set(bpy.data.objects)
        pdx.import_meshfile(str(path),imp_locs=False)
        added=set(bpy.data.objects)-prior
        refs.extend(o for o in added if o.type=='MESH')
        rigs.extend(o for o in added if o.type=='ARMATURE')
    wig = next(o for o in refs if o.name.startswith('aor_frederick_wig'))
    head = next(o for o in refs if o.name.startswith('male_head'))
    wig_tree = surface_bvh(wig)
    # A hat must surround the upper hair, not float above every strand.
    # Do not raise it automatically to avoid all wig-surface contacts: that
    # caused the perched fit rejected in the actual game screenshot. Record
    # these contacts for visual review while still rejecting skull penetration.
    wig_contacts = surface_bvh(low).overlap(wig_tree)
    head_contacts = surface_bvh(low).overlap(surface_bvh(head))
    overlaps = {'wig':len(wig_contacts), 'head':len(head_contacts)}
    contact_heights = [wig.data.vertices[i].co.z for _,triangle in wig_contacts
                       for i in wig.data.loop_triangles[triangle].vertices]
    if overlaps['head']:
        # Keep failed candidates only in the ignored cache for local fitting.
        # Never silently lift the opening or integrate a skull-intersecting hat.
        collision_points = [(sum((head.data.vertices[i].co for i in
                             head.data.loop_triangles[t].vertices),
                             Vector()) / 3)[:]
                            for _,t in head_contacts]
        (CACHE/'failed_fit.json').write_text(json.dumps({
            'overlaps':overlaps,'head_contact_centres_cm':collision_points,
            'fit_scale':FIT_SCALE,'fit_base_z_cm':FIT_BASE_Z},indent=2),encoding='utf-8')
        bpy.ops.wm.save_as_mainfile(filepath=str(CACHE/'failed_fit.blend'))
        raise RuntimeError(f'Fit needs revision before integration: {overlaps}')
    # Native rig, exact rigid vertex group and armature setup.
    rig = rigs[-1]
    low.vertex_groups.clear()
    group = low.vertex_groups.new(name='bn_h_skull')
    group.add(list(range(len(low.data.vertices))),1.0,'REPLACE')
    armature=low.modifiers.new('io_pdx_rig_skin','ARMATURE'); armature.object=rig
    # Native texture packing is done by the outer Python driver, after the bake.
    plain_material(low,(0.02,0.019,0.016))
    plain_material(high,(0.02,0.019,0.016))
    plain_material(backup,(0.02,0.019,0.016))
    # Defer texture installation/export until DDSs have been packed by driver.
    report={'source_extract':original_summary,'native_reference':REFERENCES[0],
            'native_reference_triangles':benchmark,'outside_decimation_distance_cm':deviation,
            'fit_scale':list(FIT_SCALE),'fit_base_z_cm':FIT_BASE_Z,
            'fit_depth_offset_cm':FIT_DEPTH_OFFSET,'crown_wig_clearance':crown_clearance,
            'central_peak_lift_cm':CENTRAL_PEAK_LIFT_CM,
            'approved_felt_body':body_summary,'finishes':finishes,
            'fit_lift_cm':0.0,'surface_triangle_overlaps':overlaps,
            'wig_contact_height_range_cm':([min(contact_heights),max(contact_heights)] if contact_heights else None),
            'final':object_summary(low)}
    for obj in refs:
        bpy.data.objects.remove(obj,do_unlink=True)
    for other in rigs[:-1]:
        if other.name in bpy.data.objects:
            bpy.data.objects.remove(other,do_unlink=True)
    rig.name='aor1776_tricorne_native_head_rig'
    select_only([low])
    bpy.ops.wm.save_as_mainfile(filepath=str(CACHE/'export_ready.blend'))
    (CACHE/'build.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report))


def pack_textures(output):
    """Opaque charcoal felt; native G/A normal and G/B/A material channels."""
    from PIL import Image
    normal = Image.open(CACHE/'baked_normal.png').convert('RGB')
    nx,ny,_=normal.split()
    packed=Image.merge('RGBA',(Image.new('L',normal.size,128),nx,Image.new('L',normal.size,0),ny))
    # The reserved lining patch is a flat tangent normal, opaque like the body.
    for x in range(920,1024):
        for y in range(920,1024):
            packed.putpixel((x,y),(128,128,0,128))
    diffuse=Image.new('RGBA',normal.size)
    diffuse.putdata([(38+(x*73+y*151+x*y*3)%7,37+(x*73+y*151+x*y*3)%7,
                      34+(x*73+y*151+x*y*3)%7,255) for y in range(1024) for x in range(1024)])
    properties=Image.new('RGBA',normal.size,(0,35,0,230))
    # New UVs use only the previously reserved right-hand atlas column.
    # Leave the approved felt and flat-normal lining tiles untouched.
    for x in range(920,1012):
        for y in range(155,725):
            fibre = ((x*11+y*7)%13)-6
            diffuse.putpixel((x,y),(207+fibre,204+fibre,190+fibre,255))
            packed.putpixel((x,y),(128,128+fibre//2,0,128-fibre//2))
            properties.putpixel((x,y),(0,35,0,225))
        for y in range(760,905):
            thread = (x*3+y*5)%5
            diffuse.putpixel((x,y),(23+thread,24+thread,22+thread,255))
            packed.putpixel((x,y),(128,128,0,128))
            properties.putpixel((x,y),(0,50,0,190))
    for suffix,image in [('diffuse',diffuse),('normal',packed),('properties',properties)]:
        write_dds(image,output/f'{STEM}_{suffix}.dds')


def blender_export(args):
    import bpy
    data,pdx=pdx_modules(Path(args.pdx))
    bpy.ops.wm.open_mainfile(filepath=str(CACHE/'export_ready.blend'))
    hat=bpy.data.objects[STEM]
    # Older cached builds named these mesh datablocks after the imported OBJ.
    # Renaming only objects was insufficient: the native-reference purge then
    # deleted the highpoly/source backups from the saved work file.
    for name in (STEM, STEM+'_extracted_highpoly', STEM+'_source_backup'):
        obj = bpy.data.objects.get(name)
        if obj is None or obj.type != 'MESH':
            raise RuntimeError(f'Missing required work-file backup: {name}')
        obj.data.name = name + 'Shape'
    material = __import__('types').SimpleNamespace(shader=['portrait_attachment'],
        diff=[f'{STEM}_diffuse.dds'],n=[f'{STEM}_normal.dds'],spec=[f'{STEM}_properties.dds'])
    hat.data.materials.clear()
    pdx.create_material(material,hat.data,str(Path(args.output)),use_diffuse_alpha=False)
    # Relink the installed native packed DDSs for a self-contained work file.
    for image in bpy.data.images:
        if image.filepath.lower().endswith('.dds'):
            image.reload()
            image.pack()
    original=data.read_meshfile(str(Path(args.game)/REFERENCES[0])).find('object')[0]
    report=json.loads((CACHE/'build.json').read_text(encoding='utf-8'))
    if args.mode != 'work':
        report['export']=native_export(args,hat,data,pdx,original)
    # Purge unused native meshes/materials before saving the deliverable.
    for mesh in list(bpy.data.meshes):
        if mesh.users == 0 or not mesh.name.startswith(STEM):
            bpy.data.meshes.remove(mesh)
    used_materials={mat for obj in bpy.data.objects if obj.type=='MESH' for mat in obj.data.materials}
    for mat in list(bpy.data.materials):
        if mat not in used_materials:
            bpy.data.materials.remove(mat)
    used_images={node.image for mat in used_materials if mat.use_nodes for node in mat.node_tree.nodes
                 if node.type=='TEX_IMAGE' and node.image}
    for image in list(bpy.data.images):
        if image not in used_images:
            bpy.data.images.remove(image)
    select_only([hat])
    bpy.ops.wm.save_as_mainfile(filepath=str(WORK))
    report['work_file_backups_preserved'] = True
    (CACHE/'build.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report))


def blender_preview(args):
    import bpy
    from mathutils import Vector
    _,pdx=pdx_modules(Path(args.pdx))
    bpy.ops.wm.open_mainfile(filepath=str(WORK))
    hat=bpy.data.objects[STEM]
    for path,colour in [(WIG,None),(Path(args.game)/'gfx/models/portraits/male_head/male_head.mesh',(0.38,0.24,0.16))]:
        prior=set(bpy.data.objects)
        pdx.import_meshfile(str(path),imp_locs=False)
        for obj in set(bpy.data.objects)-prior:
            if obj.type=='MESH' and colour:
                plain_material(obj,colour)
    # Use genuine wig textures/materials, not the white diagnostic proxy.
    meshes=[o for o in bpy.context.scene.objects if o.type=='MESH' and not o.hide_render]
    frame=bpy.data.objects.new('preview_frame',hat.data.copy())
    bpy.context.collection.objects.link(frame);frame.hide_render=True
    frame.data.clear_geometry()
    frame.data.from_pydata([o.matrix_world @ v.co for o in meshes for v in o.data.vertices],[],[])
    render_views(frame,'final_fit')
    print(json.dumps({'preview':'cached only; native reference geometry is not saved'}))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',default=str(ROOT/'docs/portraits/sources/bust_of_frederick_the_great_original.zip'))
    parser.add_argument('--game',default='C:/Games/Victoria 3/game')
    parser.add_argument('--blender',default='C:/Program Files/Blender Foundation/Blender 5.2/blender.exe')
    parser.add_argument('--pdx',default='C:/Users/simeo/AppData/Roaming/Blender Foundation/Blender/5.2/extensions/user_default/io_pdx_mesh')
    parser.add_argument('--blender-stage',action='store_true')
    parser.add_argument('--obj')
    parser.add_argument('--output',default=str(CACHE/'runtime'))
    parser.add_argument('--integrate',action='store_true')
    parser.add_argument('--mode',choices=['inspect','inspect-bow','extract','fit','build','export','work','preview'],default='inspect')
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else None)
    if args.blender_stage:
        if args.mode=='inspect-bow':
            inspect_bow()
        elif args.mode=='inspect':
            blender_inspect(args)
        elif args.mode=='fit':
            blender_fit(args)
        elif args.mode=='build':
            blender_build(args)
        elif args.mode in ('export','work'):
            blender_export(args)
        elif args.mode=='preview':
            blender_preview(args)
        else:
            blender_extract(args)
        return
    obj=unpack(args.source)
    # 'work' repairs only the .blend from the ignored build cache, linking the
    # approved runtime textures. It never rewrites the game-facing mesh/DDSs.
    output=RUNTIME if args.integrate or args.mode=='work' else Path(args.output).resolve()
    if not output.is_relative_to(ROOT) or output == ROOT:
        raise ValueError('Output must stay in the repository')
    output.mkdir(parents=True,exist_ok=True)
    command=[args.blender,'--background','--factory-startup','--python-exit-code','1',
                    '--python',str(Path(__file__).resolve()),'--','--blender-stage',
                    '--game',args.game,'--pdx',args.pdx,'--obj',str(obj),'--output',str(output),'--mode',args.mode]
    subprocess.run(command,check=True)
    if args.mode=='build':
        pack_textures(output)
        command[-1]='export'
        subprocess.run(command,check=True)


if __name__=='__main__':
    main()
