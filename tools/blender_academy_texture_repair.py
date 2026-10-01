"""Inspect and repair the already-open academy scene from Blender's Python console.

Nothing is imported, deleted or exported. Running this file only writes an audit;
repair_blender_scene() must be called separately to change the current scene.
"""

import json
import re
from datetime import datetime
from pathlib import Path

import bpy


REPORT_DIR = Path(
    r"C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/"
    r"1776_Age_of_Revolutions_fork/docs/reports/assets/blender"
)
GAME_GFX = Path(r"C:/Games/Victoria 3/game/gfx")
ACADEMY_DIR = GAME_GFX / "models/buildings/european/european_city/european_city_academy_01"
ASSET_FILE = ACADEMY_DIR / "european_city_academy_01.asset"


def inspect_blender_scene():
    report = {
        "blend_file": bpy.data.filepath,
        "objects": [],
    }
    for obj in bpy.context.scene.objects:
        if obj.type != "MESH":
            continue
        entry = {
            "name": obj.name,
            "hidden": obj.hide_get(),
            "hide_render": obj.hide_render,
            "vertices": len(obj.data.vertices),
            "materials": [],
        }
        for slot in obj.material_slots:
            mat = slot.material
            if mat is None:
                continue
            entry["materials"].append({
                "slot": slot.slot_index,
                "name": mat.name,
                "properties": {
                    key: str(mat[key]) for key in mat.keys()
                },
                "images": [
                    {"node": node.name, "name": node.image.name,
                     "file": node.image.filepath, "has_data": node.image.has_data}
                    for node in mat.node_tree.nodes
                    if node.type == "TEX_IMAGE" and node.image is not None
                ] if mat.use_nodes else [],
            })
        report["objects"].append(entry)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output = REPORT_DIR / ("BLENDER_LIVE_TEXTURE_AUDIT_" + stamp + ".json")
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Audit Blender :", output)
    return report


def _read_asset_materials():
    """Read balanced meshsettings blocks, including their nested texture entries."""
    text = ASSET_FILE.read_text(encoding="utf-8-sig")
    settings = {}
    for match in re.finditer(r"\bmeshsettings\s*=\s*\{", text):
        start = match.end()
        depth, end, quoted = 1, start, False
        while depth:
            char = text[end]
            if char == '"':
                quoted = not quoted
            if not quoted:
                depth += (char == "{") - (char == "}")
            end += 1
        block = text[start:end - 1]
        name = re.search(r'\bname\s*=\s*"([^"]+)"', block).group(1)
        source_index = int(re.search(r"\bindex\s*=\s*(\d+)", block).group(1))
        object_name = name.removesuffix("Shape").replace("|", "_")
        entry = {"shader": re.search(r'\bshader\s*=\s*"([^"]+)"', block).group(1)}
        for field, role in [("texture_diffuse", "diffuse"),
                            ("texture_normal", "normal"),
                            ("texture_specular", "properties")]:
            entry[role] = re.search(r'\b' + field + r'\s*=\s*"([^"]+)"', block).group(1)
        extra = re.search(r'\btexture\s*=\s*\{\s*file\s*=\s*"([^"]+)"', block)
        if extra:
            entry["extra"] = extra.group(1)
        settings[(object_name, source_index)] = entry
    return settings


def repair_blender_scene():
    """Keep all geometry and PDX metadata; repair texture bindings and preview only."""
    settings = _read_asset_materials()
    expected_objects = {key[0] for key in settings}
    targets = [obj for obj in bpy.context.scene.objects if obj.name in expected_objects]
    if {obj.name for obj in targets} != expected_objects:
        raise RuntimeError("The open scene does not contain the expected academy objects.")

    texture_dirs = [ACADEMY_DIR,
                    GAME_GFX / "models/environment/trees/tree_oak",
                    GAME_GFX / "models/environment/trees",
                    GAME_GFX / "models/buildings/european/european_urban_city_decal",
                    GAME_GFX / "models/buildings/generic/decals"]
    files = {}
    for entry in settings.values():
        for role in ("diffuse", "normal", "properties", "extra"):
            if role not in entry:
                continue
            basename = entry[role]
            matches = [directory / basename for directory in texture_dirs
                       if (directory / basename).is_file()]
            if len(matches) != 1:
                raise RuntimeError("Texture missing or ambiguous: " + basename)
            files[basename] = matches[0]

    plans = []
    for obj in targets:
        for slot in obj.material_slots:
            mat = slot.material
            if mat is None or mat.node_tree is None:
                raise RuntimeError("Material missing on " + obj.name)
            entry = settings[(obj.name, int(mat.get("pdxMaterialIndex", slot.slot_index)))]
            image_nodes = {}
            for role in ("diffuse", "normal", "properties"):
                nodes = [node for node in mat.node_tree.nodes
                         if node.type == "TEX_IMAGE" and node.name.endswith("_" + role + ".dds")]
                if len(nodes) != 1:
                    raise RuntimeError("Unexpected texture nodes: " + mat.name + " / " + role)
                image_nodes[role] = nodes[0]
            shaders = [node for node in mat.node_tree.nodes if node.type == "BSDF_PRINCIPLED"]
            if len(shaders) != 1:
                raise RuntimeError("Unexpected material shader on " + mat.name)
            plans.append((obj, mat, entry, image_nodes, shaders[0]))

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    backup = REPORT_DIR / ("Academie_AVANT_reparation_" + stamp + ".blend")
    if backup.exists():
        raise RuntimeError("Backup already exists; refusing to overwrite it.")
    result = bpy.ops.wm.save_as_mainfile(filepath=str(backup), copy=True)
    if "FINISHED" not in result or not backup.is_file():
        raise RuntimeError("Backup failed; the scene was not changed.")

    # Images are loaded before changing the existing material links.
    images = {}
    for basename, file in files.items():
        image = bpy.data.images.load(str(file), check_existing=True)
        # Blender 5.2 loads file-backed image buffers lazily. Requesting pixels
        # is necessary before has_data can reliably indicate successful loading.
        buffer_length = len(image.pixels)
        if not buffer_length:
            image.reload()
            buffer_length = len(image.pixels)
        if not buffer_length or not image.has_data:
            raise RuntimeError("Blender could not load " + str(file))
        image.colorspace_settings.name = "Non-Color" if basename.endswith(("_normal.dds", "_properties.dds", "_mask_01.dds")) else "sRGB"
        images[basename] = image

    changes = []
    for obj, mat, entry, nodes, shader in plans:
        for role, node in nodes.items():
            node.image = images[entry[role]]
            changes.append({"object": obj.name, "material": mat.name,
                            "role": role, "file": str(files[entry[role]])})
        links = mat.node_tree.links
        if entry["shader"] == "tree_colormap":
            alpha = mat.node_tree.nodes.new("ShaderNodeMath")
            alpha.name = "PDX_preview_leaf_alpha"
            alpha.label = "Découpe du feuillage"
            alpha.operation = "GREATER_THAN"
            alpha.inputs[1].default_value = 0.5
            links.new(nodes["diffuse"].outputs["Alpha"], alpha.inputs[0])
            links.new(alpha.outputs[0], shader.inputs["Alpha"])
            # Native trees use a tint lookup. Preview a fixed midpoint of this lookup.
            tint = mat.node_tree.nodes.new("ShaderNodeTexImage")
            tint.name = "PDX_preview_tree_tint"
            tint.image = images[entry["extra"]]
            tint.inputs["Vector"].default_value = (0.5, 0.5, 0.0)
            mix = mat.node_tree.nodes.new("ShaderNodeMixRGB")
            mix.name = "PDX_preview_tree_softlight"
            mix.blend_type = "SOFT_LIGHT"
            mix.inputs[0].default_value = 1.0
            links.new(nodes["diffuse"].outputs["Color"], mix.inputs[1])
            links.new(tint.outputs["Color"], mix.inputs[2])
            links.new(mix.outputs[0], shader.inputs["Base Color"])
        elif entry["shader"] == "decal_local":
            links.new(nodes["diffuse"].outputs["Alpha"], shader.inputs["Alpha"])
        elif entry["shader"] == "decal_world":
            mask = mat.node_tree.nodes.new("ShaderNodeTexImage")
            mask.name = "PDX_preview_ground_mask"
            mask.image = images[entry["extra"]]
            channels = mat.node_tree.nodes.new("ShaderNodeSeparateColor")
            channels.name = "PDX_preview_ground_mask_red"
            links.new(mask.outputs["Color"], channels.inputs[0])
            links.new(channels.outputs["Red"], shader.inputs["Alpha"])
        if entry["shader"] in {"tree_colormap", "decal_local", "decal_world"}:
            if hasattr(mat, "surface_render_method"):
                mat.surface_render_method = "DITHERED"
            if hasattr(mat, "use_transparency_overlap"):
                mat.use_transparency_overlap = False
        mat.update_tag()

    for obj in targets:
        higher_lod = not obj.name.startswith("LOD_0_")
        obj.hide_set(higher_lod)
        obj.hide_render = higher_lod
        obj.select_set(False)
    main = bpy.data.objects["LOD_0_mesh_mesh"]
    main.select_set(True)
    bpy.context.view_layer.objects.active = main
    bpy.context.view_layer.update()

    report = {"backup": str(backup), "objects_preserved": len(targets),
              "materials_repaired": len(plans), "texture_bindings_repaired": len(changes),
              "changes": changes,
              "preview_note": "Blender preview only: game terrain overlays and seasonal tinting are not recreated."}
    output = REPORT_DIR / ("BLENDER_TEXTURE_REPAIR_" + stamp + ".json")
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Réparation terminée :", len(plans), "matériaux,", len(changes), "textures reconnectées.")
    print("Copie de sécurité :", backup)
    return report


def save_repaired_scene_copy():
    """Check the live result and save a new copy without naming/overwriting the open scene."""
    target_names = {key[0] for key in _read_asset_materials()}
    targets = [obj for obj in bpy.context.scene.objects if obj.name in target_names]
    if len(targets) != len(target_names):
        raise RuntimeError("An academy object is missing.")
    failures = []
    used_images = {}
    for obj in targets:
        if obj.hide_get() != (not obj.name.startswith("LOD_0_")):
            failures.append("Unexpected visibility: " + obj.name)
        for slot in obj.material_slots:
            for node in slot.material.node_tree.nodes:
                if node.type != "TEX_IMAGE":
                    continue
                image = node.image
                if image is None or not len(image.pixels) or not image.has_data:
                    failures.append("Unloaded image: " + obj.name + " / " + node.name)
                else:
                    used_images[image.name] = image.filepath
    if failures:
        raise RuntimeError("\n".join(failures))
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    output = REPORT_DIR / ("Academie_TEXTURES_CORRIGEES_" + stamp + ".blend")
    if output.exists():
        raise RuntimeError("Refusing to overwrite an existing scene.")
    # Restore the previous 3D editor before saving, so the copy opens on the model.
    if bpy.context.area is not None and bpy.context.area.type == "CONSOLE":
        bpy.context.area.type = "VIEW_3D"
    result = bpy.ops.wm.save_as_mainfile(filepath=str(output), copy=True)
    if "FINISHED" not in result or not output.is_file():
        raise RuntimeError("The corrected scene copy could not be saved.")
    verification = {"corrected_copy": str(output), "objects_preserved": len(targets),
                    "visible_objects": [obj.name for obj in targets if not obj.hide_get()],
                    "loaded_images": used_images, "failures": failures,
                    "open_scene_filepath": bpy.data.filepath}
    (REPORT_DIR / ("BLENDER_REPAIR_VERIFIED_" + stamp + ".json")).write_text(
        json.dumps(verification, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Scène corrigée vérifiée et copiée :", output)
    return verification


BLENDER_TEXTURE_AUDIT = inspect_blender_scene()
