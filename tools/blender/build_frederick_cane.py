"""Build an original cane from the user's Frederick painting (not BlenderKit).

The native cane supplies only local bounds/attachment/pose conventions. No
native geometry, textures or animations are exported. Diagnostics stay ignored.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'tools'))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_frederick_wig import pdx_modules, write_dds

CACHE = ROOT/'.asset-cache/portraits/frederick_cane'
RUNTIME = ROOT/'gfx/models/portraits/attachments/props/aor1776_frederick_cane'
WORK = ROOT/'docs/portraits/frederick_cane_work.blend'
STEM = 'aor1776_frederick_cane'
NATIVE = 'gfx/models/portraits/attachments/props/walkingcane/prop_walkingcane.mesh'


def textures(output):
    from PIL import Image
    diffuse = Image.new('RGBA', (512,512))
    properties = Image.new('RGBA', (512,512))
    for y in range(512):
        for x in range(512):
            grain = ((x*13+(y//13)*3)%17)-8
            if x<256:  # Longitudinal dark wood grain; no baked scene lighting.
                colour=(62+grain,36+grain//2,20+grain//3,255)
                material=(0,45,0,195)
            elif x<384:  # Light, carved horn/wood-like crook in the painting.
                colour=(147+grain,111+grain,63+grain//2,255)
                material=(0,55,0,175)
            else:  # Small aged-brass collar and end ferrule, not the shaft.
                colour=(121+grain,93+grain,43+grain//2,255)
                material=(0,65,180,165)
            diffuse.putpixel((x,y),colour)
            properties.putpixel((x,y),material)
    normal=Image.new('RGBA',(512,512),(128,128,0,128))
    for kind,image in [('diffuse',diffuse),('normal',normal),('properties',properties)]:
        write_dds(image,output/f'{STEM}_{kind}.dds')


def build(args):
    import bpy
    import bmesh
    from math import pi, cos, sin
    from mathutils import Vector
    data,pdx=pdx_modules(Path(args.pdx))
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    vertices,faces,uvs=[],[],[]

    def tube(path,radii,tile,sides=12):
        start=len(vertices)
        length=len(path)-1
        for i,p in enumerate(path):
            tangent=(path[min(i+1,length)]-path[max(0,i-1)]).normalized()
            across=tangent.cross(Vector((0,0,1))).normalized()
            other=tangent.cross(across).normalized()
            for j in range(sides):
                angle=2*pi*j/sides
                vertices.append(tuple(p+radii[i]*(cos(angle)*across+sin(angle)*other)))
        for i in range(length):
            for j in range(sides):
                n=(j+1)%sides
                faces.append((start+i*sides+j,start+i*sides+n,
                              start+(i+1)*sides+n,start+(i+1)*sides+j))
                u0,u1=tile
                uvs.append([(u0+(u1-u0)*j/sides,.06+.88*i/length),
                            (u0+(u1-u0)*(j+1)/sides,.06+.88*i/length),
                            (u0+(u1-u0)*(j+1)/sides,.06+.88*(i+1)/length),
                            (u0+(u1-u0)*j/sides,.06+.88*(i+1)/length)])
        for row,reverse in ((0,True),(length,False)):
            ids=[start+row*sides+j for j in range(sides)]
            faces.append(tuple(reversed(ids) if reverse else ids))
            uvs.append([(sum(tile)/2,.5)]*sides)

    # Native prop local +Z is the shaft axis; in Blender this is local +Y.
    # Its origin is inside the grip, not at the bottom or the top of the cane.
    shaft=[Vector((0,-46+84*i/24,0)) for i in range(25)]
    tube(shaft,[.74+.26*i/24 for i in range(25)],(.04,.46))
    controls=[Vector(p) for p in [(0,37.8,0),(0,40,0),(1.6,42.7,0),
                                 (4.8,44,0),(7.6,43.5,0),(9,41.5,0),
                                 (8.5,39.8,0),(7.8,39.5,0)]]
    extended=[controls[0]]+controls+[controls[-1]]
    curve=[]
    # Catmull-Rom gives a smooth, original curved grip instead of downloading
    # the commercial library's bird-headed cane or copying native vertices.
    for segment in range(len(controls)-1):
        a,b,c,d=extended[segment:segment+4]
        for j in range(6):
            t=j/6
            curve.append(.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+
                             (-a+3*b-3*c+d)*t*t*t))
    curve.append(controls[-1])
    tube(curve,[1.08+.18*sin(pi*i/(len(curve)-1)) for i in range(len(curve))],(.52,.72))
    tube([Vector((0,y,0)) for y in (36.8,37,37.5,37.7)], [1.03,1.14,1.14,1.03],(.79,.96))
    tube([Vector((0,y,0)) for y in (-46.3,-46.1,-44.7,-44.5)], [.78,.85,.85,.78],(.79,.96))
    mesh=bpy.data.meshes.new(STEM+'Shape')
    mesh.from_pydata(vertices,[],faces); mesh.update()
    cane=bpy.data.objects.new(STEM,mesh); bpy.context.collection.objects.link(cane)
    layer=mesh.uv_layers.new(name='UVMap')
    for face,coords in zip(mesh.polygons,uvs):
        face.use_smooth=True
        for index,coord in zip(face.loop_indices,coords):
            layer.data[index].uv=coord
    bm=bmesh.new();bm.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    bmesh.ops.triangulate(bm,faces=list(bm.faces))
    bm.to_mesh(mesh);bm.free();mesh.update()
    material=SimpleNamespace(shader=['portrait_attachment'],diff=[f'{STEM}_diffuse.dds'],
                             n=[f'{STEM}_normal.dds'],spec=[f'{STEM}_properties.dds'])
    pdx.create_material(material,mesh,args.output,use_diffuse_alpha=False)
    for image in bpy.data.images:
        image.pack()
    bpy.ops.object.select_all(action='DESELECT');cane.select_set(True)
    bpy.context.view_layer.objects.active=cane
    pdx.set_mesh_index(mesh,0)
    output=Path(args.output)/f'{STEM}.mesh'
    pdx.export_meshfile(str(output),exp_skel=False,exp_locs=False,sort_verts='+')
    shape=data.read_meshfile(str(output)).find('object')[0]
    reference=data.read_meshfile(str(Path(args.game)/NATIVE)).find('object')[0]
    exported=shape.find('mesh')
    assert shape.find('skeleton') is None and exported.find('skin') is None
    report={'provenance':'original procedural reconstruction from supplied painting; no BlenderKit model used',
            'attachment_node':'bn_r_prop','grip_origin_cm':[0,0,0],
            'triangles':len(exported.attrib['tri'])//3,
            'split_vertices':len(exported.attrib['p'])//3,
            'materials':len(shape.findall('mesh')),
            'bounds_pdx_cm':exported.find('aabb').attrib,
            'native_reference_bounds_pdx_cm':reference.find('mesh').find('aabb').attrib,
            'native_reference_triangles':len(reference.find('mesh').attrib['tri'])//3}
    bpy.context.scene['aor1776_provenance']=report['provenance']
    # The factory cube's unused datablock must not pollute the editable source.
    for unused in list(bpy.data.meshes):
        if unused.users == 0: bpy.data.meshes.remove(unused)
    for unused in list(bpy.data.materials):
        if unused.users == 0: bpy.data.materials.remove(unused)
    for unused in list(bpy.data.images):
        if unused.users == 0 or unused.type in ('RENDER_RESULT','COMPOSITING'):
            bpy.data.images.remove(unused)
    bpy.ops.wm.save_as_mainfile(filepath=str(WORK))
    (CACHE/'build.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report))


def render(scene,centre,scale,path,direction=(0,-1,.18)):
    import bpy
    from mathutils import Vector
    scene.render.engine='CYCLES';scene.cycles.samples=16;scene.cycles.use_denoising=True
    scene.render.resolution_x=768;scene.render.resolution_y=768;scene.render.resolution_percentage=100
    scene.world.color=(.13,.13,.13)
    bpy.ops.object.camera_add()
    camera=bpy.context.object;camera.data.type='ORTHO';camera.data.ortho_scale=scale
    camera.location=centre+Vector(direction)*scale*3
    camera.rotation_euler=(centre-camera.location).to_track_quat('-Z','Y').to_euler();scene.camera=camera
    bpy.ops.object.light_add(type='AREA',location=centre+Vector((scale,-scale,scale)))
    light=bpy.context.object;light.data.energy=scale*scale*65;light.data.size=scale
    light.rotation_euler=(centre-light.location).to_track_quat('-Z','Y').to_euler()
    scene.render.filepath=str(path);bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(camera,do_unlink=True);bpy.data.objects.remove(light,do_unlink=True)


def preview(args):
    import bpy
    from mathutils import Vector
    _,pdx=pdx_modules(Path(args.pdx))
    bpy.ops.wm.open_mainfile(filepath=str(WORK))
    cane=bpy.data.objects[STEM]
    # Stand the prop upright only in the diagnostic, not in exported local space.
    from math import pi
    cane.rotation_euler.x=pi/2
    render(bpy.context.scene,Vector((3,0,0)),105,CACHE/'cane.png')
    cane.rotation_euler.x=0
    pdx.import_meshfile(str(Path(args.game)/'gfx/models/portraits/male_body/male_body.mesh'),imp_locs=False)
    rig=next(o for o in bpy.data.objects if o.type=='ARMATURE')
    pdx.import_animfile(str(Path(args.game)/'gfx/models/portraits/male_body/male_body_walkingcane_idle.anim'))
    for o in bpy.data.objects:
        if o.type=='MESH' and o!=cane:
            from extract_frederick_tricorne import plain_material
            plain_material(o,(.30,.25,.21))
    frames=[]
    for frame in (1,76,151):
        bpy.context.scene.frame_set(frame);bpy.context.view_layer.update()
        matrix=rig.matrix_world@rig.pose.bones['bn_r_prop'].matrix
        cane.matrix_world=matrix
        grip=matrix.translation
        frames.append({'frame':frame,'grip_world_cm':list(grip),
                       'matrix': [list(row) for row in matrix]})
        render(bpy.context.scene,grip,62,CACHE/f'grip_{frame}.png')
    (CACHE/'grip_validation.json').write_text(json.dumps({'native_pose_frames':frames,
        'runtime_attachment':'bn_r_prop, rigid local-origin hand prop',
        'reference_geometry_saved':False,'in_game_verified':False},indent=2),encoding='utf-8')
    # No preview/reference geometry is saved back into WORK.


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--game',default='C:/Games/Victoria 3/game')
    p.add_argument('--blender',default='C:/Program Files/Blender Foundation/Blender 5.2/blender.exe')
    p.add_argument('--pdx',default='C:/Users/simeo/AppData/Roaming/Blender Foundation/Blender/5.2/extensions/user_default/io_pdx_mesh')
    p.add_argument('--mode',choices=['build','preview'],default='build')
    p.add_argument('--integrate',action='store_true')
    p.add_argument('--blender-stage',action='store_true')
    p.add_argument('--output')
    args=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else None)
    CACHE.mkdir(parents=True,exist_ok=True)
    if args.blender_stage:
        (build if args.mode=='build' else preview)(args);return
    output=RUNTIME if args.integrate else CACHE/'runtime'
    output=output.resolve()
    if not output.is_relative_to(ROOT) or output==ROOT:
        raise ValueError('Output must be in the repository')
    output.mkdir(parents=True,exist_ok=True)
    if args.mode=='build': textures(output)
    subprocess.run([args.blender,'--background','--factory-startup','--python-exit-code','1',
                    '--python',str(Path(__file__).resolve()),'--','--blender-stage',
                    '--mode',args.mode,'--game',args.game,'--pdx',args.pdx,'--output',str(output)],check=True)


if __name__=='__main__':main()
