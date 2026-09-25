# Blender-Python: stilisierte 3-D-Mülltüte für AR / Artivive
# Verwendung: Blender öffnen -> Scripting -> New -> diesen Code einfügen -> Run Script.
# Danach entsteht eine transparente, leicht zerknitterte Mülltüte mit 360°-Animation.
#
# Hinweis: Die Form ist bewusst künstlerisch/stilisiert rekonstruiert.
# Für eine exakte Silhouette kann das Foto anschließend als Hintergrund/Referenz
# in Blender geladen und einzelne Vertices angepasst werden.

import bpy
import math
from mathutils import Vector

# ------------------------------------------------------------
# Szene leeren
# ------------------------------------------------------------
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# ------------------------------------------------------------
# Grundparameter
# ------------------------------------------------------------
W = 2.0
H = 3.15
cols = 13
rows = 21

verts = []
faces = []

# Silhouette: oben etwas schmaler, mittig breit, unten leicht zusammengezogen
def half_width(y):
    t = y / H
    if t < 0.10:
        return 0.72 + 0.20*t/0.10
    if t < 0.72:
        return 0.92 + 0.05*math.sin(t*math.pi*2)
    return 0.92 - 0.18*((t-0.72)/0.28)

# Erzeuge gewölbtes Raster
for r in range(rows + 1):
    y = H * r / rows
    t = r / rows
    hw = half_width(y)

    for c in range(cols + 1):
        u = c / cols
        x = (u - 0.5) * 2 * hw

        # leichte unregelmäßige Falten / Volumen
        center = 1.0 - abs(u - 0.5) * 2
        bulge = 0.18 * center * math.sin(t*math.pi*3.2)
        bulge += 0.07 * math.sin(u*math.pi*4 + t*5.0)

        # stärkere Falten in verschiedenen Höhen
        fold = (
            0.055 * math.sin(u*math.pi*7 + t*2.2)
            + 0.035 * math.sin(t*math.pi*9 + u*3.0)
        )

        z = bulge + fold

        # leichte Asymmetrie
        x += 0.045 * math.sin(t*math.pi*2.3) * (u-0.5)

        verts.append((x, 0.0, y + 0.04*math.sin(u*math.pi*2)*math.sin(t*math.pi)))

for r in range(rows):
    for c in range(cols):
        a = r*(cols+1)+c
        b = a+1
        d = (r+1)*(cols+1)+c
        cc = d+1
        faces.append((a,b,cc,d))

mesh = bpy.data.meshes.new("Muelltüte_Mesh")
mesh.from_pydata(verts, [], faces)
mesh.update()

obj = bpy.data.objects.new("Muelltüte_AR", mesh)
bpy.context.collection.objects.link(obj)

# ------------------------------------------------------------
# Solidify: hauchdünne Folie
# ------------------------------------------------------------
solid = obj.modifiers.new("Dünne_Kunststofffolie", 'SOLIDIFY')
solid.thickness = 0.012
solid.offset = 0.0

# leichte Glättung
bpy.context.view_layer.objects.active = obj
obj.select_set(True)
bpy.ops.object.shade_smooth()

# ------------------------------------------------------------
# Material: transparente Kunststofffolie
# ------------------------------------------------------------
mat = bpy.data.materials.new("Transparentes_Plastic")
mat.use_nodes = True

bsdf = mat.node_tree.nodes.get("Principled BSDF")
bsdf.inputs["Base Color"].default_value = (0.92, 0.95, 0.96, 1.0)
bsdf.inputs["Roughness"].default_value = 0.22
bsdf.inputs["Metallic"].default_value = 0.0

# Blender 4.x
if "Transmission Weight" in bsdf.inputs:
    bsdf.inputs["Transmission Weight"].default_value = 0.82
if "IOR" in bsdf.inputs:
    bsdf.inputs["IOR"].default_value = 1.45

# Transparenz etwas zurücknehmen, damit die Falten sichtbar bleiben
if "Alpha" in bsdf.inputs:
    bsdf.inputs["Alpha"].default_value = 0.48

mat.surface_render_method = 'DITHERED' if hasattr(mat, "surface_render_method") else mat.surface_render_method

obj.data.materials.append(mat)

# ------------------------------------------------------------
# 360°-Animation
# ------------------------------------------------------------
scene = bpy.context.scene
scene.render.fps = 30
scene.frame_start = 1
scene.frame_end = 270  # 9 Sekunden

obj.rotation_mode = 'XYZ'
obj.rotation_euler = (0, 0, 0)
obj.keyframe_insert(data_path="rotation_euler", frame=1, index=2)

obj.rotation_euler[2] = math.radians(360)
obj.keyframe_insert(data_path="rotation_euler", frame=270, index=2)

# Linearer, gleichmäßiger Loop
if obj.animation_data and obj.animation_data.action:
    for fc in obj.animation_data.action.fcurves:
        for kp in fc.keyframe_points:
            kp.interpolation = 'LINEAR'

    # zyklische Wiederholung
    for fc in obj.animation_data.action.fcurves:
        fc.modifiers.new('CYCLES')

# ------------------------------------------------------------
# Ursprung / Skalierung
# ------------------------------------------------------------
bpy.context.view_layer.objects.active = obj
obj.select_set(True)
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

# ------------------------------------------------------------
# Kamera (nur zur Kontrolle)
# ------------------------------------------------------------
bpy.ops.object.camera_add(location=(0, -5.5, H/2))
cam = bpy.context.object
cam.name = "Kontrollkamera"
cam.rotation_euler = (math.radians(90), 0, 0)
scene.camera = cam

# ------------------------------------------------------------
# Export-Hinweis als Custom Property
# ------------------------------------------------------------
obj["AR_EXPORT"] = "GLB"
obj["AR_NOTE"] = "Animierte transparente Mülltüte – für Artivive"

print("Fertig: Muelltüte_AR wurde erstellt.")
print("Export: File > Export > glTF 2.0 (.glb), Animation aktivieren.")
