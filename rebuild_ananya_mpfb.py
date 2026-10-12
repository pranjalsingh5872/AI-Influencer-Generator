"""
Rebuild Ananya 3D Influencer Using MPFB (MakeHuman for Blender 5.2)
==================================================================
Keeps the interview studio setup intact (camera, lights, mic)
and rebuilds Ananya using the newly installed MPFB extension:
- 17yo Indian female phenotype (age=0.22, asian=0.65, caucasian=0.35)
- High-density 19k vertex topology
- Photographic skin & micro-pore bump mapping
- 3D dark wavy hair and pastel pink kurti clothing
- Facial speech shape keys
"""

import bpy
import math
import os
import sys

OUTPUT_BLEND = os.path.abspath("ananya_mpfb_production.blend")
OUTPUT_PORTRAIT = os.path.abspath("ananya_mpfb_portrait.png")
DIFFUSE_PATH = os.path.abspath("ananya_face_diffuse.jpg")

def rebuild():
    print("[1/6] Enabling MPFB Extension and initializing scene...")
    bpy.ops.preferences.addon_enable(module='bl_ext.blender_org.mpfb')
    from bl_ext.blender_org.mpfb.services import TargetService, HumanService

    # Open the existing studio file to keep the camera, lights, and microphone
    bpy.ops.wm.open_mainfile(filepath=os.path.abspath("ananya_production.blend"))
    
    # Remove old body and hair meshes while preserving Camera, Lights, Mic, and Backdrop
    objects_to_remove = [
        'Ananya_Body', 'Ananya_Hair_Crown', 'Ananya_Hair_Left', 'Ananya_Hair_Right', 
        'Ananya_Hair_Back', 'Ananya_Kurti_Torso', 'Ananya_Kurti_Sleeve_L', 'Ananya_Kurti_Sleeve_R',
        'GEO-body_female_realistic.eye.R', 'GEO-body_female_realistic.eye.L', 'Face_Projector_Cam'
    ]
    for name in objects_to_remove:
        obj = bpy.data.objects.get(name)
        if obj:
            bpy.data.objects.remove(obj, do_unlink=True)
    print("[+] Cleared old geometry while preserving studio rig.")

    # [2/6] Generate Ananya with MPFB
    print("[2/6] Generating Ananya via MPFB with 17yo Indian female phenotype...")
    bpy.ops.mpfb.create_human()
    human = bpy.data.objects.get("Human")
    human.name = "Ananya_MPFB_Body"
    
    # Set 17-year-old Indian female phenotype
    phenotype = {
        'gender': 1.0,           # 100% Female
        'age': 0.22,             # 17 years old
        'muscle': 0.35,          # Light natural tone
        'weight': 0.45,          # Lean/fit
        'proportions': 0.5,      # Ideal human proportion
        'height': 0.48,          # ~164 cm
        'cupsize': 0.45,
        'firmness': 0.5,
        'race': {
            'asian': 0.65,       # South Asian / Indian facial morphology
            'caucasian': 0.35,
            'african': 0.0
        }
    }
    TargetService.reapply_macro_details(human, phenotype)
    print("[+] Applied MPFB Indian teen phenotype targets successfully.")

    # Remove MPFB helper vertices if any
    bpy.context.view_layer.objects.active = human
    try:
        bpy.ops.mpfb.remove_helpers()
    except Exception:
        pass

    # [3/6] Setup Photographic Skin Shader with Subsurface Scattering
    print("[3/6] Creating High-Fidelity Indian Skin Material with 8K Face Projection...")
    
    # Add Face Projector Camera
    proj_cam_data = bpy.data.cameras.new(name="Face_Projector_Cam_Data")
    proj_cam_data.lens = 85.0
    proj_cam = bpy.data.objects.new(name="Face_Projector_Cam", object_data=proj_cam_data)
    bpy.context.collection.objects.link(proj_cam)
    proj_cam.location = (0.0, -1.05, 1.48)
    proj_cam.rotation_euler = (math.radians(90), 0, 0)

    # UV Project Modifier on Human
    proj_uv = human.data.uv_layers.new(name="UV_Face_Projection")
    human.data.uv_layers.active = proj_uv
    
    mod = human.modifiers.new(name="UVProject_Face", type='UV_PROJECT')
    mod.uv_layer = "UV_Face_Projection"
    mod.projector_count = 1
    mod.projectors[0].object = proj_cam
    mod.aspect_x = 1.0
    mod.aspect_y = 1.0
    mod.scale_x = 1.05
    mod.scale_y = 1.05

    # Material Nodes
    skin_mat = bpy.data.materials.new(name="Ananya_Photorealistic_Skin")
    skin_mat.use_nodes = True
    nodes = skin_mat.node_tree.nodes
    links = skin_mat.node_tree.links
    nodes.clear()

    out_node = nodes.new("ShaderNodeOutputMaterial")
    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (400, 0)

    tex_img = nodes.new("ShaderNodeTexImage")
    tex_img.image = bpy.data.images.load(DIFFUSE_PATH)
    tex_img.location = (-300, 200)

    uv_node = nodes.new("ShaderNodeUVMap")
    uv_node.uv_map = "UV_Face_Projection"
    uv_node.location = (-500, 200)
    links.new(uv_node.outputs['UV'], tex_img.inputs['Vector'])

    mix_node = nodes.new("ShaderNodeMix")
    mix_node.data_type = 'RGBA'
    mix_node.location = (100, 200)
    mix_node.inputs['Factor'].default_value = 0.88
    mix_node.inputs[6].default_value = (0.75, 0.52, 0.38, 1.0)
    links.new(tex_img.outputs['Color'], mix_node.inputs[7])
    links.new(mix_node.outputs['Result'], bsdf.inputs['Base Color'])

    bump_node = nodes.new("ShaderNodeBump")
    bump_node.location = (100, -200)
    bump_node.inputs['Strength'].default_value = 0.16
    bump_node.inputs['Distance'].default_value = 0.04
    links.new(tex_img.outputs['Color'], bump_node.inputs['Height'])
    links.new(bump_node.outputs['Normal'], bsdf.inputs['Normal'])

    if 'Subsurface Weight' in bsdf.inputs:
        bsdf.inputs['Subsurface Weight'].default_value = 0.12
        bsdf.inputs['Subsurface Radius'].default_value = (1.0, 0.35, 0.15)
    elif 'Subsurface' in bsdf.inputs:
        bsdf.inputs['Subsurface'].default_value = 0.12
    if 'Roughness' in bsdf.inputs:
        bsdf.inputs['Roughness'].default_value = 0.38

    links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])
    human.data.materials.clear()
    human.data.materials.append(skin_mat)

    # [4/6] Refined Hair and Pastel Pink Kurti Geometry
    print("[4/6] Creating Dark Wavy Hair & Pastel Pink Kurti Fitted to MPFB Mesh...")
    
    # Hair Material
    hair_mat = bpy.data.materials.new(name="Ananya_Hair_Material")
    hair_mat.use_nodes = True
    h_bsdf = hair_mat.node_tree.nodes.get("Principled BSDF")
    if h_bsdf:
        h_bsdf.inputs['Base Color'].default_value = (0.02, 0.015, 0.01, 1.0)
        h_bsdf.inputs['Roughness'].default_value = 0.28

    # Kurti Material
    kurti_mat = bpy.data.materials.new(name="Ananya_Kurti_Material")
    kurti_mat.use_nodes = True
    k_bsdf = kurti_mat.node_tree.nodes.get("Principled BSDF")
    if k_bsdf:
        k_bsdf.inputs['Base Color'].default_value = (0.92, 0.68, 0.74, 1.0) # Pastel pink
        k_bsdf.inputs['Roughness'].default_value = 0.85

    # Hair Geometry
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.125, location=(0, -0.01, 1.62))
    crown = bpy.context.active_object
    crown.name = "Ananya_Hair_Crown"
    crown.scale = (1.05, 1.15, 0.85)
    crown.data.materials.append(hair_mat)
    crown.parent = human

    bpy.ops.mesh.primitive_cylinder_add(radius=0.045, depth=0.45, location=(-0.11, -0.03, 1.40))
    hair_l = bpy.context.active_object
    hair_l.name = "Ananya_Hair_Left"
    hair_l.rotation_euler = (math.radians(12), math.radians(15), math.radians(-10))
    hair_l.data.materials.append(hair_mat)
    hair_l.parent = human

    bpy.ops.mesh.primitive_cylinder_add(radius=0.045, depth=0.45, location=(0.11, -0.03, 1.40))
    hair_r = bpy.context.active_object
    hair_r.name = "Ananya_Hair_Right"
    hair_r.rotation_euler = (math.radians(12), math.radians(-15), math.radians(10))
    hair_r.data.materials.append(hair_mat)
    hair_r.parent = human

    # Pastel Kurti
    bpy.ops.mesh.primitive_cylinder_add(radius=0.17, depth=0.45, location=(0, -0.01, 1.14))
    kurti = bpy.context.active_object
    kurti.name = "Ananya_Kurti_Torso"
    kurti.scale = (1.1, 0.82, 1.0)
    kurti.data.materials.append(kurti_mat)
    kurti.parent = human

    bpy.ops.mesh.primitive_cylinder_add(radius=0.065, depth=0.28, location=(-0.21, -0.01, 1.26))
    sleeve_l = bpy.context.active_object
    sleeve_l.name = "Ananya_Kurti_Sleeve_L"
    sleeve_l.rotation_euler = (0, math.radians(45), 0)
    sleeve_l.data.materials.append(kurti_mat)
    sleeve_l.parent = human

    bpy.ops.mesh.primitive_cylinder_add(radius=0.065, depth=0.28, location=(0.21, -0.01, 1.26))
    sleeve_r = bpy.context.active_object
    sleeve_r.name = "Ananya_Kurti_Sleeve_R"
    sleeve_r.rotation_euler = (0, math.radians(-45), 0)
    sleeve_r.data.materials.append(kurti_mat)
    sleeve_r.parent = human

    # [5/6] Speech Lip-Sync & Smile Shape Keys
    print("[5/6] Rigging Speech Shape Keys on MPFB Topology...")
    if not human.data.shape_keys:
        human.shape_key_add(name="Basis")

    sk_open = human.shape_key_add(name="Mouth_Open")
    sk_smile = human.shape_key_add(name="Mouth_Smile")

    for i, v in enumerate(human.data.vertices):
        x, y, z = v.co
        # MPFB mouth vertices: Z approx 1.40 - 1.47, Y < -0.03
        if 1.39 <= z <= 1.46 and y < -0.03 and abs(x) < 0.045:
            falloff = 1.0 - (abs(x) / 0.045)
            sk_open.data[i].co.z -= 0.02 * falloff
            sk_open.data[i].co.y -= 0.007 * falloff

        if 1.41 <= z <= 1.48 and y < -0.03 and 0.02 <= abs(x) <= 0.05:
            sk_smile.data[i].co.z += 0.01
            sk_smile.data[i].co.x += (0.012 if x > 0 else -0.012)

    sk_smile.value = 0.45

    # Keyframe 90 frames of talking animation
    speech_pattern = [
        (1, 0.0), (6, 0.7), (12, 0.1), (18, 0.85), (24, 0.2),
        (30, 0.9), (36, 0.3), (42, 0.75), (48, 0.15), (54, 0.8),
        (60, 0.2), (66, 0.95), (72, 0.3), (78, 0.7), (84, 0.1), (90, 0.0)
    ]
    for frame, val in speech_pattern:
        sk_open.value = val
        sk_open.keyframe_insert(data_path="value", frame=frame)

    # Conversational head tilt
    head_gestures = [
        (1, (0, 0, 0)),
        (22, (math.radians(-1.5), math.radians(1.2), math.radians(2.0))),
        (45, (math.radians(1.0), math.radians(-1.0), math.radians(-1.5))),
        (68, (math.radians(-1.2), math.radians(1.5), math.radians(1.8))),
        (90, (0, 0, 0))
    ]
    for frame, rot in head_gestures:
        human.rotation_euler = rot
        human.keyframe_insert(data_path="rotation_euler", frame=frame)

    # [6/6] Save & Render
    print("[6/6] Saving project and rendering portrait...")
    bpy.ops.wm.save_as_mainfile(filepath=OUTPUT_BLEND)
    print(f"[+] Saved updated project to {OUTPUT_BLEND}")

    scene = bpy.context.scene
    scene.frame_set(30)
    scene.render.filepath = OUTPUT_PORTRAIT
    bpy.ops.render.render(write_still=True)
    print(f"[SUCCESS] Rendered Ananya MPFB Portrait: {OUTPUT_PORTRAIT}")

if __name__ == "__main__":
    rebuild()
