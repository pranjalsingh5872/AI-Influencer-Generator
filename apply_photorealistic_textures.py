"""
Apply High-Resolution Photographic Human Skin & Facial Textures
==============================================================
Uses:
- ananya_face_diffuse.jpg (8K frontal photographic texture of 17yo Indian girl)
- UV Project / Frontal projection mapped directly to facial landmarks
- Micro-pore bump map generation
- Organic Subsurface Scattering for human skin realism
"""

import bpy
import math
import os

DIFFUSE_PATH = os.path.abspath("ananya_face_diffuse.jpg")
OUTPUT_BLEND = os.path.abspath("ananya_photorealistic.blend")
OUTPUT_STILL = os.path.abspath("ananya_3d_photorealistic_portrait.png")

def apply_photorealistic_skin():
    print("[*] Loading ananya_production.blend...")
    bpy.ops.wm.open_mainfile(filepath=os.path.abspath("ananya_production.blend"))
    
    body = bpy.data.objects.get("Ananya_Body")
    if not body:
        print("[!] Ananya_Body not found!")
        return

    # 1. Create a Frontal Texture Projection Camera / Empty
    proj_cam_data = bpy.data.cameras.new(name="Face_Projector_Cam_Data")
    proj_cam_data.lens = 85.0  # Flatter focal length for minimal distortion
    proj_cam = bpy.data.objects.new(name="Face_Projector_Cam", object_data=proj_cam_data)
    bpy.context.collection.objects.link(proj_cam)
    # Position projector directly in front of head at eye level (Z=1.49m)
    proj_cam.location = (0.0, -1.05, 1.49)
    proj_cam.rotation_euler = (math.radians(90), 0, 0)

    # 2. Add UV Project Modifier
    # Create a dedicated UV map for projection
    proj_uv = body.data.uv_layers.new(name="UV_Face_Projection")
    body.data.uv_layers.active = proj_uv
    
    mod = body.modifiers.new(name="UVProject_Face", type='UV_PROJECT')
    mod.uv_layer = "UV_Face_Projection"
    mod.projector_count = 1
    mod.projectors[0].object = proj_cam
    mod.aspect_x = 1.0
    mod.aspect_y = 1.0
    mod.scale_x = 1.05
    mod.scale_y = 1.05

    # 3. Setup Photorealistic PBR Material Nodes
    mat = body.data.materials[0] if body.data.materials else bpy.data.materials.new(name="Ananya_Photorealistic_Skin")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Create Material Nodes
    output_node = nodes.new("ShaderNodeOutputMaterial")
    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (400, 0)

    # Base Color: Mix Photographic Texture with Organic Base Tone
    tex_img = nodes.new("ShaderNodeTexImage")
    tex_img.image = bpy.data.images.load(DIFFUSE_PATH)
    tex_img.location = (-300, 200)

    tex_coord = nodes.new("ShaderNodeTexCoord")
    tex_coord.location = (-700, 200)

    # UV Map node targeting UV_Face_Projection
    uv_node = nodes.new("ShaderNodeUVMap")
    uv_node.uv_map = "UV_Face_Projection"
    uv_node.location = (-500, 200)
    links.new(uv_node.outputs['UV'], tex_img.inputs['Vector'])

    # Mix Color: Blend photo face with warm base body skin
    mix_node = nodes.new("ShaderNodeMix")
    mix_node.data_type = 'RGBA'
    mix_node.location = (100, 200)
    mix_node.inputs['Factor'].default_value = 0.88  # 88% photo fidelity
    mix_node.inputs[6].default_value = (0.75, 0.52, 0.38, 1.0) # Base body color
    links.new(tex_img.outputs['Color'], mix_node.inputs[7])
    links.new(mix_node.outputs['Result'], bsdf.inputs['Base Color'])

    # Micro-pore Bump Map
    bump_node = nodes.new("ShaderNodeBump")
    bump_node.location = (100, -200)
    bump_node.inputs['Strength'].default_value = 0.18
    bump_node.inputs['Distance'].default_value = 0.05
    links.new(tex_img.outputs['Color'], bump_node.inputs['Height'])
    links.new(bump_node.outputs['Normal'], bsdf.inputs['Normal'])

    # Subsurface Scattering for warm glowing skin
    if 'Subsurface Weight' in bsdf.inputs:
        bsdf.inputs['Subsurface Weight'].default_value = 0.12
        bsdf.inputs['Subsurface Radius'].default_value = (1.0, 0.35, 0.15)
    elif 'Subsurface' in bsdf.inputs:
        bsdf.inputs['Subsurface'].default_value = 0.12
    if 'Roughness' in bsdf.inputs:
        bsdf.inputs['Roughness'].default_value = 0.38

    links.new(bsdf.outputs['BSDF'], output_node.inputs['Surface'])

    # 4. Refine Hair Material to Match Photographic Realism
    hair_crown = bpy.data.objects.get("Ananya_Hair_Crown")
    if hair_crown and hair_crown.data.materials:
        h_mat = hair_crown.data.materials[0]
        h_bsdf = h_mat.node_tree.nodes.get("Principled BSDF")
        if h_bsdf:
            h_bsdf.inputs['Base Color'].default_value = (0.02, 0.015, 0.01, 1.0)
            h_bsdf.inputs['Roughness'].default_value = 0.25

    # 5. Save and Render
    bpy.ops.wm.save_as_mainfile(filepath=OUTPUT_BLEND)
    print(f"[+] Saved updated project to {OUTPUT_BLEND}")

    scene = bpy.context.scene
    scene.frame_set(30)
    scene.render.filepath = OUTPUT_STILL
    bpy.ops.render.render(write_still=True)
    print(f"[SUCCESS] Photorealistic 3D Portrait Rendered: {OUTPUT_STILL}")

if __name__ == "__main__":
    apply_photorealistic_skin()
