"""
Build Ananya Complete Production Character in Blender
======================================================
Integrates pre-styled 3D assets via MPFB:
- 17yo Indian female phenotype
- High-poly flowing dark hair (Elvs island princess hair)
- High-res sculpted eyebrows (Mindfront eyebrows)
- Elegant fitted dress/kurti in pastel pink
- Anatomical realistic eyes (deep brown iris, wet cornea)
- Subsurface scattering skin with warm Indian complexion
- 9:16 vertical interview camera, golden hour lights, reporter mic
"""

import bpy
import os
import math

bpy.ops.preferences.addon_enable(module='bl_ext.blender_org.mpfb')
from bl_ext.blender_org.mpfb.services import TargetService, HumanService, AssetService

OUTPUT_BLEND = os.path.abspath("ananya_production_final.blend")
OUTPUT_RENDER = os.path.abspath("ananya_option_b_portrait.png")

# 1. Load studio scene (camera, lights, mic)
bpy.ops.wm.open_mainfile(filepath=os.path.abspath("ananya_production.blend"))

# Clean old temporary meshes
for name in list(bpy.data.objects.keys()):
    if any(k in name for k in ['Ananya', 'Curves', 'Human', 'GEO', 'clothes', 'Hair', 'Kurti']):
        bpy.data.objects.remove(bpy.data.objects[name], do_unlink=True)

print("[1/5] Creating 17yo Indian Female Human via MPFB...")
bpy.ops.mpfb.create_human()
human = bpy.data.objects.get("Human")
human.name = "Ananya_Body"

# Phenotype
phenotype = {
    'gender': 1.0,           # Female
    'age': 0.22,             # 17 years old
    'muscle': 0.30,          # Light natural tone
    'weight': 0.42,          # Lean
    'proportions': 0.5,
    'height': 0.48,          # ~164 cm
    'cupsize': 0.42,
    'firmness': 0.5,
    'race': {
        'asian': 0.65,       # South Asian / Indian facial structure
        'caucasian': 0.35,
        'african': 0.0
    }
}
TargetService.reapply_macro_details(human, phenotype)

# Smooth shading & subdivision
for poly in human.data.polygons:
    poly.use_smooth = True

subsurf = human.modifiers.new(name="Subsurf", type='SUBSURF')
subsurf.levels = 1
subsurf.render_levels = 2

# Skin Material with warm Indian complexion
bpy.context.view_layer.objects.active = human
bpy.ops.mpfb.create_v2_skin()
skin_mat = bpy.data.materials.get("v2 skin material")
if skin_mat and skin_mat.node_tree:
    colorgroup = skin_mat.node_tree.nodes.get("colorgroup")
    # Set warm glowing Indian skin tone
    skin_bsdf = skin_mat.node_tree.nodes.get("Principled BSDF")
    if skin_bsdf:
        skin_bsdf.inputs['Base Color'].default_value = (0.72, 0.52, 0.40, 1.0)
        if 'Subsurface Weight' in skin_bsdf.inputs:
            skin_bsdf.inputs['Subsurface Weight'].default_value = 0.12
            skin_bsdf.inputs['Subsurface Radius'].default_value = (1.0, 0.4, 0.2)
        elif 'Subsurface' in skin_bsdf.inputs:
            skin_bsdf.inputs['Subsurface'].default_value = 0.12

print("[2/5] Equipping High-Poly Hair and Sculpted Eyebrows...")
# Hair
hair_assets = AssetService.get_asset_list('hair')
hair_key = 'Elvs island princess hair' if 'Elvs island princess hair' in hair_assets else list(hair_assets.keys())[0]
hair_path = hair_assets[hair_key]['full_path']
hair_obj = HumanService.add_mhclo_asset(hair_path, human, asset_type='Hair', set_up_rigging=False)
hair_obj.name = "Ananya_Hair"

# Hair Shader (lustrous natural dark brown/black Indian hair)
hair_mat = bpy.data.materials.new(name="Ananya_Hair_Shader")
hair_mat.use_nodes = True
h_bsdf = hair_mat.node_tree.nodes.get("Principled BSDF")
if h_bsdf:
    h_bsdf.inputs['Base Color'].default_value = (0.025, 0.018, 0.014, 1.0)
    h_bsdf.inputs['Roughness'].default_value = 0.28
    if 'Specular IOR Level' in h_bsdf.inputs:
        h_bsdf.inputs['Specular IOR Level'].default_value = 0.7
hair_obj.data.materials.clear()
hair_obj.data.materials.append(hair_mat)

# Eyebrows
eb_assets = AssetService.get_asset_list('eyebrows')
eb_key = 'Mindfront eyebrows 01' if 'Mindfront eyebrows 01' in eb_assets else list(eb_assets.keys())[0]
eb_path = eb_assets[eb_key]['full_path']
eb_obj = HumanService.add_mhclo_asset(eb_path, human, asset_type='Eyebrows', set_up_rigging=False)
eb_obj.name = "Ananya_Eyebrows"
eb_mat = bpy.data.materials.new(name="Ananya_Eyebrow_Shader")
eb_mat.use_nodes = True
eb_bsdf = eb_mat.node_tree.nodes.get("Principled BSDF")
if eb_bsdf:
    eb_bsdf.inputs['Base Color'].default_value = (0.02, 0.015, 0.012, 1.0)
    eb_bsdf.inputs['Roughness'].default_value = 0.4
eb_obj.data.materials.clear()
eb_obj.data.materials.append(eb_mat)

print("[3/5] Equipping Fitted Pastel Kurti Dress...")
clothes_assets = AssetService.get_asset_list('clothes')
# Prefer a dress or tunic
dress_key = 'Toigo keyhole neck dress' if 'Toigo keyhole neck dress' in clothes_assets else list(clothes_assets.keys())[0]
dress_path = clothes_assets[dress_key]['full_path']
dress_obj = HumanService.add_mhclo_asset(dress_path, human, asset_type='Clothes', set_up_rigging=False)
dress_obj.name = "Ananya_Kurti"

# Pastel Pink Silk Kurti Material
kurti_mat = bpy.data.materials.new(name="Ananya_Kurti_PastelPink")
kurti_mat.use_nodes = True
k_bsdf = kurti_mat.node_tree.nodes.get("Principled BSDF")
if k_bsdf:
    k_bsdf.inputs['Base Color'].default_value = (0.91, 0.64, 0.72, 1.0) # Pastel pink
    k_bsdf.inputs['Roughness'].default_value = 0.65
dress_obj.data.materials.clear()
dress_obj.data.materials.append(kurti_mat)

print("[4/5] Aligning Realistic Anatomical Eyes...")
bundle_blend = os.path.abspath('blender_assets/human_base_meshes/human-base-meshes-bundle-v1.4.1/human_base_meshes_bundle.blend')
with bpy.data.libraries.load(bundle_blend, link=False) as (data_from, data_to):
    data_to.objects = ['GEO-body_female_realistic.eye.L', 'GEO-body_female_realistic.eye.R']

eye_l = data_to.objects[0]
eye_r = data_to.objects[1]
bpy.context.collection.objects.link(eye_l)
bpy.context.collection.objects.link(eye_r)

# Precise eye socket alignment based on MPFB joint-eye coordinates
# Position: Z=1.546, Y=-0.118, X=±0.0315
eye_l.location = (0.0315, -0.118, 1.545)
eye_r.location = (-0.0315, -0.118, 1.545)
eye_l.scale = (0.92, 0.92, 0.92)
eye_r.scale = (0.92, 0.92, 0.92)
eye_l.parent = human
eye_r.parent = human

# Realistic Indian Eye Material (rich amber brown iris, wet cornea)
eye_mat = bpy.data.materials.new(name="Ananya_Indian_Eyes")
eye_mat.use_nodes = True
e_bsdf = eye_mat.node_tree.nodes.get("Principled BSDF")
if e_bsdf:
    e_bsdf.inputs['Base Color'].default_value = (0.10, 0.05, 0.015, 1.0)
    e_bsdf.inputs['Roughness'].default_value = 0.04
    if 'IOR' in e_bsdf.inputs:
        e_bsdf.inputs['IOR'].default_value = 1.38
eye_l.data.materials.clear()
eye_l.data.materials.append(eye_mat)
eye_r.data.materials.clear()
eye_r.data.materials.append(eye_mat)

print("[5/5] Configuring Interview Camera, Lighting & Rendering...")
cam = bpy.data.objects.get("Interview_Camera")
cam.location = (0.0, -1.15, 1.48)
cam.rotation_euler = (math.radians(88), 0, 0)
cam.data.lens = 65.0
cam.data.dof.use_dof = True
cam.data.dof.focus_object = eye_l
cam.data.dof.aperture_fstop = 2.8

# Save blend file
bpy.ops.wm.save_as_mainfile(filepath=OUTPUT_BLEND)
print(f"[+] Project saved to {OUTPUT_BLEND}")

# Render portrait
scene = bpy.context.scene
scene.render.resolution_x = 720
scene.render.resolution_y = 1280
scene.render.filepath = OUTPUT_RENDER
bpy.ops.render.render(write_still=True)
print(f"[SUCCESS] Rendered Ananya Option B Portrait to {OUTPUT_RENDER}")
