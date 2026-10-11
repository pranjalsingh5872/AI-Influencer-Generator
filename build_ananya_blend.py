"""
Assemble Ananya 3D Base Character in Blender 5.2
================================================
Extracts the female head and body meshes from the official
Blender Studio Human Base Meshes bundle and places them
into our 9:16 vertical interview studio.
"""

import bpy
import math
import os

BUNDLE_BLEND = os.path.abspath("blender_assets/human_base_meshes/human-base-meshes-bundle-v1.4.1/human_base_meshes_bundle.blend")
OUTPUT_BLEND = os.path.abspath("ananya_base_character.blend")

def assemble():
    print(f"[*] Loading bundle from: {BUNDLE_BLEND}")
    
    # 1. Reset scene
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    # 2. Append Female Base Mesh from Bundle
    # Look for female objects in bundle
    with bpy.data.libraries.load(BUNDLE_BLEND) as (data_from, data_to):
        female_objs = [name for name in data_from.objects if "female" in name.lower() or "head" in name.lower() or "body" in name.lower()]
        print(f"[*] Found candidate objects in bundle: {female_objs}")
        
        # Pick realistic female body/head or primitive female
        targets = []
        for cand in female_objs:
            if "female_realistic" in cand.lower() or "realistic_head" in cand.lower() or "body_female" in cand.lower():
                targets.append(cand)
        
        if not targets:
            targets = [female_objs[0]] if female_objs else []
            
        print(f"[*] Appending target objects: {targets}")
        data_to.objects = targets

    # Link objects to collection
    for obj in data_to.objects:
        if obj:
            bpy.context.collection.objects.link(obj)
            print(f"[+] Linked object: {obj.name}")

    # 3. Create Procedural Warm Indian Skin Shader
    skin_mat = bpy.data.materials.new(name="Ananya_Warm_Skin")
    skin_mat.use_nodes = True
    nodes = skin_mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        # Warm golden-wheatish skin tone
        bsdf.inputs['Base Color'].default_value = (0.76, 0.54, 0.38, 1.0)
        # Subsurface scattering for realistic skin translucency
        if 'Subsurface Weight' in bsdf.inputs:
            bsdf.inputs['Subsurface Weight'].default_value = 0.08
        elif 'Subsurface' in bsdf.inputs:
            bsdf.inputs['Subsurface'].default_value = 0.08
        if 'Roughness' in bsdf.inputs:
            bsdf.inputs['Roughness'].default_value = 0.45

    # Apply skin material to appended meshes
    for obj in bpy.context.collection.objects:
        if obj.type == 'MESH':
            if not obj.data.materials:
                obj.data.materials.append(skin_mat)
            else:
                obj.data.materials[0] = skin_mat

    # 4. Import the studio setup (Camera, Lights, Microphone)
    sys.path.append(os.path.abspath("blender_pipeline"))
    import blender_setup_studio
    blender_setup_studio.setup_render_settings()
    blender_setup_studio.setup_camera()
    blender_setup_studio.setup_golden_hour_lighting()
    blender_setup_studio.create_microphone_prop()

    # 5. Save as ananya_base_character.blend
    bpy.ops.wm.save_as_mainfile(filepath=OUTPUT_BLEND)
    print(f"[SUCCESS] Saved assembled project: {OUTPUT_BLEND}")

if __name__ == "__main__":
    import sys
    assemble()
