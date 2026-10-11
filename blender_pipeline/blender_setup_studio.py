"""
Blender 5.2 Automation Script: Street Interview Studio Setup
============================================================
Run inside Blender or via CLI:
blender.exe your_character.blend -P blender_setup_studio.py

Sets up:
1. 9:16 Vertical Instagram Reel Resolution (1080 x 1920)
2. Portrait Camera (50mm lens) with Depth of Field focused on character
3. Golden-Hour 3-Point Lighting (Warm Key, Cool Fill, Golden Rim Sun)
4. 3D Reporter Wireless Microphone Prop placed on the right side
"""

import bpy
import math

def setup_render_settings():
    print("[*] Configuring 9:16 Vertical Video Render Settings...")
    scene = bpy.context.scene
    scene.render.resolution_x = 1080
    scene.render.resolution_y = 1920
    scene.render.resolution_percentage = 100
    scene.render.fps = 30
    
    # Color Management (AgX / Filmic)
    try:
        scene.view_settings.view_transform = 'AgX'
    except Exception:
        try:
            scene.view_settings.view_transform = 'Filmic'
        except Exception:
            pass
    try:
        scene.view_settings.look = 'Medium High Contrast'
    except Exception:
        pass

def setup_camera():
    print("[*] Setting up 50mm Portrait Interview Camera...")
    # Remove existing cameras or create new
    cam_data = bpy.data.cameras.new(name="Interview_Camera_Data")
    cam_data.lens = 50.0  # 50mm portrait lens
    cam_data.dof.use_dof = True
    cam_data.dof.aperture_fstop = 2.8  # Soft cinematic bokeh

    cam_obj = bpy.data.objects.new(name="Interview_Camera", object_data=cam_data)
    bpy.context.collection.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj

    # Position camera at eye level, framed medium close-up
    cam_obj.location = (0.2, -2.2, 1.45)
    cam_obj.rotation_euler = (math.radians(88), 0, math.radians(5))

    return cam_obj

def setup_golden_hour_lighting():
    print("[*] Creating Golden-Hour Interview Lighting Rig...")
    
    # 1. Warm Golden Rim Sun (Sunset Backlight)
    sun_data = bpy.data.lights.new(name="Sun_Backlight_Data", type='SUN')
    sun_data.energy = 4.5
    sun_data.color = (1.0, 0.72, 0.42)  # Golden orange
    sun_obj = bpy.data.objects.new(name="Sun_Backlight", object_data=sun_data)
    bpy.context.collection.objects.link(sun_obj)
    sun_obj.location = (-2.0, 3.0, 3.0)
    sun_obj.rotation_euler = (math.radians(45), math.radians(20), math.radians(-130))

    # 2. Key Light (Soft Warm Fill on Face)
    key_data = bpy.data.lights.new(name="Key_Light_Data", type='AREA')
    key_data.energy = 120.0
    key_data.size = 1.2
    key_data.color = (1.0, 0.92, 0.82)
    key_obj = bpy.data.objects.new(name="Key_Light", object_data=key_data)
    bpy.context.collection.objects.link(key_obj)
    key_obj.location = (1.2, -1.8, 1.8)
    key_obj.rotation_euler = (math.radians(65), 0, math.radians(35))

    # 3. Soft Ambient Fill
    fill_data = bpy.data.lights.new(name="Fill_Light_Data", type='AREA')
    fill_data.energy = 40.0
    fill_data.size = 2.0
    fill_data.color = (0.75, 0.85, 1.0)  # Gentle sky reflection
    fill_obj = bpy.data.objects.new(name="Fill_Light", object_data=fill_data)
    bpy.context.collection.objects.link(fill_obj)
    fill_obj.location = (-1.5, -1.5, 1.4)
    fill_obj.rotation_euler = (math.radians(60), 0, math.radians(-40))

def create_microphone_prop():
    print("[*] Spawning 3D Reporter Microphone Prop...")
    
    # Mic Handle
    bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=0.18, location=(0.28, -1.2, 1.18))
    handle = bpy.context.active_object
    handle.name = "Microphone_Handle"
    handle.rotation_euler = (math.radians(-25), math.radians(-15), math.radians(-30))

    # Mic Windscreen Mesh (Sphere top)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.032, location=(0.24, -1.13, 1.27))
    head = bpy.context.active_object
    head.name = "Microphone_Head"

    # Material: Matte Black
    mat = bpy.data.materials.new(name="Mic_Dark_Metal")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.05, 0.05, 0.05, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.4
    
    handle.data.materials.append(mat)
    head.data.materials.append(mat)

def main():
    print("====================================================")
    print("  BLENDER AI INFLUENCER INTERVIEW STUDIO SETUP")
    print("====================================================")
    setup_render_settings()
    setup_camera()
    setup_golden_hour_lighting()
    create_microphone_prop()
    print("[SUCCESS] Studio Setup Complete! Ready for character import & rendering.")

if __name__ == "__main__":
    main()
