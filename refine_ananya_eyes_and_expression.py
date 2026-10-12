"""
Refine Eye Proportions, Expression Targets & Final Polish
=========================================================
- Properly load MPFB eyelid closure and smile targets via TargetService.load_target()
- Normalize procedural eye shader coordinate (vec_len * 72.0) for realistic 60% iris coverage
- Position eyebrows cleanly on brow ridge
- Render final photorealistic 9:16 portrait
"""

import bpy
import os
import math

bpy.ops.preferences.addon_enable(module='bl_ext.blender_org.mpfb')
from bl_ext.blender_org.mpfb.services import TargetService

BLEND_FILE = os.path.abspath("ananya_production_final.blend")
OUTPUT_RENDER = os.path.abspath("ananya_option_b_portrait.png")

bpy.ops.wm.open_mainfile(filepath=BLEND_FILE)
human = bpy.data.objects.get("Ananya_Body")

# 1. Load Real Facial Expression Targets
print("[1/3] Loading Anatomical Expression Targets...")
units_dir = r"C:\Users\priya\AppData\Roaming\Blender Foundation\Blender\5.2\extensions\blender_org\mpfb\data\targets\expression\units\asian"

eye_l_target = os.path.join(units_dir, "eye-left-closure.target.gz")
eye_r_target = os.path.join(units_dir, "eye-right-closure.target.gz")
smile_target = os.path.join(units_dir, "mouth-corner-puller.target.gz")
smile_up_target = os.path.join(units_dir, "mouth-upward-retraction.target.gz")

if os.path.exists(eye_l_target):
    TargetService.load_target(human, eye_l_target, weight=0.32)
if os.path.exists(eye_r_target):
    TargetService.load_target(human, eye_r_target, weight=0.32)
if os.path.exists(smile_target):
    TargetService.load_target(human, smile_target, weight=0.35)
if os.path.exists(smile_up_target):
    TargetService.load_target(human, smile_up_target, weight=0.18)

# 2. Perfect Iris Proportions via Normalized Radial Coordinates
print("[2/3] Rebuilding Normalized Procedural Eye Shader...")
eye_mat = bpy.data.materials.get("Procedural_Realistic_Eye")
if eye_mat and eye_mat.node_tree:
    nodes = eye_mat.node_tree.nodes
    links = eye_mat.node_tree.links
    nodes.clear()

    out = nodes.new('ShaderNodeOutputMaterial')
    out.location = (800, 0)

    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (500, 0)
    bsdf.inputs['Roughness'].default_value = 0.03
    if 'IOR' in bsdf.inputs: bsdf.inputs['IOR'].default_value = 1.38
    links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])

    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-700, 0)

    sep = nodes.new('ShaderNodeSeparateXYZ')
    sep.location = (-500, 0)
    links.new(tex_coord.outputs['Object'], sep.inputs['Vector'])

    comb = nodes.new('ShaderNodeCombineXYZ')
    comb.location = (-300, 0)
    links.new(sep.outputs['X'], comb.inputs['X'])
    links.new(sep.outputs['Z'], comb.inputs['Y'])

    vec_len = nodes.new('ShaderNodeVectorMath')
    vec_len.operation = 'LENGTH'
    vec_len.location = (-100, 0)
    links.new(comb.outputs['Vector'], vec_len.inputs[0])

    # Multiply by 72.0 to normalize radius to 0.0 - 1.0 range
    mult = nodes.new('ShaderNodeMath')
    mult.operation = 'MULTIPLY'
    mult.location = (100, 0)
    mult.inputs[1].default_value = 72.0
    links.new(vec_len.outputs['Value'], mult.inputs[0])

    # Color Ramp for Realistic Eye
    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.location = (300, 0)
    ramp.color_ramp.interpolation = 'LINEAR'
    
    # 0: Pupil (Black)
    ramp.color_ramp.elements[0].position = 0.18
    ramp.color_ramp.elements[0].color = (0.01, 0.01, 0.01, 1.0)

    # 1: Iris (Warm Honey Amber Brown)
    ramp.color_ramp.elements[1].position = 0.52
    ramp.color_ramp.elements[1].color = (0.28, 0.13, 0.035, 1.0)

    # 2: Limbal Ring (Dark espresso border)
    el2 = ramp.color_ramp.elements.new(0.62)
    el2.color = (0.03, 0.015, 0.01, 1.0)

    # 3: Sclera (Natural off-white)
    el3 = ramp.color_ramp.elements.new(0.68)
    el3.color = (0.92, 0.90, 0.88, 1.0)

    links.new(mult.outputs['Value'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])

# 3. Eyebrows Adjustment
print("[3/3] Fine-tuning Eyebrow Alignment...")
eb_obj = bpy.data.objects.get("Ananya_Eyebrows")
if eb_obj:
    eb_obj.location.y = -0.005 # Bring forward over brow ridge
    eb_obj.location.z = 0.002

# Save & Render
bpy.ops.wm.save_as_mainfile(filepath=BLEND_FILE)
print(f"[+] Saved project to {BLEND_FILE}")

scene = bpy.context.scene
scene.render.filepath = OUTPUT_RENDER
bpy.ops.render.render(write_still=True)
print(f"[SUCCESS] Final Master Portrait Rendered to {OUTPUT_RENDER}")
