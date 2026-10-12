"""
Refine Direct Eye Contact & Microphone Framing
================================================
- Tilt eyeballs slightly upward to establish direct camera eye contact
- Increase eyelid relaxation (weight=0.42) for natural eye shape
- Bring reporter microphone into clear foreground view
- Save blend and render 9:16 portrait
"""

import bpy
import os
import math

BLEND_FILE = os.path.abspath("ananya_production_final.blend")
OUTPUT_RENDER = os.path.abspath("ananya_option_b_portrait.png")

bpy.ops.wm.open_mainfile(filepath=BLEND_FILE)
human = bpy.data.objects.get("Ananya_Body")

# 1. Adjust Eyelids via Shape Keys
if human.data.shape_keys:
    kb_l = human.data.shape_keys.key_blocks.get("asian_eye-left-closure")
    kb_r = human.data.shape_keys.key_blocks.get("asian_eye-right-closure")
    if kb_l: kb_l.value = 0.44
    if kb_r: kb_r.value = 0.44

# 2. Eye Rotation for Direct Camera Eye Contact
eye_l = bpy.data.objects.get("GEO-body_female_realistic.eye.L")
eye_r = bpy.data.objects.get("GEO-body_female_realistic.eye.R")

if eye_l and eye_r:
    # Rotate slightly upward to look directly into camera lens
    eye_l.rotation_euler = (math.radians(-6), math.radians(2), 0)
    eye_r.rotation_euler = (math.radians(-6), math.radians(-2), 0)

# 3. Position Handheld Microphone in Foreground
mic_handle = bpy.data.objects.get("Mic_Handle")
if mic_handle:
    mic_handle.location = (0.13, -0.75, 1.26)
    mic_handle.rotation_euler = (math.radians(-25), math.radians(10), math.radians(-8))

# Save & Render
bpy.ops.wm.save_as_mainfile(filepath=BLEND_FILE)
print(f"[+] Saved project to {BLEND_FILE}")

scene = bpy.context.scene
scene.render.filepath = OUTPUT_RENDER
bpy.ops.render.render(write_still=True)
print(f"[SUCCESS] Direct Eye Contact Portrait Rendered to {OUTPUT_RENDER}")
