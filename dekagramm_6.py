import bpy
import math
from mathutils import Vector

# Szene leeren
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Parameter
num_points = 10
outer_radius = 1.0
inner_radius = 0.4
height = 0.3

# Punkte für Stern erzeugen
verts_top = []
verts_bottom = []
angle_step = math.pi / num_points

for i in range(num_points * 2):
    angle = i * angle_step
    radius = outer_radius if i % 2 == 0 else inner_radius
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    verts_top.append((x, y, height / 2))
    verts_bottom.append((x, y, -height / 2))

verts = verts_top + verts_bottom
faces = []

# Seiten
for i in range(len(verts_top)):
    next_i = (i + 1) % len(verts_top)
    top1 = i
    top2 = next_i
    bottom1 = i + len(verts_top)
    bottom2 = next_i + len(verts_top)
    faces.append([top1, top2, bottom2, bottom1])

# Deckel oben & unten
faces.append([i for i in range(len(verts_top))])
faces.append([i + len(verts_top) for i in reversed(range(len(verts_top)))])

# Mesh und Objekt
mesh = bpy.data.meshes.new("Dekagram")
mesh.from_pydata(verts, [], faces)
mesh.update()

obj = bpy.data.objects.new("Dekagram", mesh)
bpy.context.collection.objects.link(obj)

# Material
mat = bpy.data.materials.new(name="ShinyMetal")
mat.use_nodes = True
nodes = mat.node_tree.nodes
principled = nodes.get("Principled BSDF")
principled.inputs["Metallic"].default_value = 1.0
principled.inputs["Roughness"].default_value = 0.05
principled.inputs["Base Color"].default_value = (0.9, 0.95, 1.0, 1)
obj.data.materials.append(mat)

# Kamera hinzufügen
cam_data = bpy.data.cameras.new(name="Camera")
cam = bpy.data.objects.new("Camera", cam_data)
bpy.context.collection.objects.link(cam)

# Kamera-Position und -Ausrichtung
cam.location = Vector((0, -4, 2))
cam.rotation_euler = (math.radians(60), 0, 0)
bpy.context.scene.camera = cam

# Lichtquelle hinzufügen
light_data = bpy.data.lights.new(name="Light", type='AREA')
light_data.energy = 1000
light_data.size = 3.0
light = bpy.data.objects.new("Light", light_data)
light.location = (2, -2, 5)
bpy.context.collection.objects.link(light)

# Weltfarbe dunkel (für Kontrast)
bpy.context.scene.world.use_nodes = True
bg = bpy.context.scene.world.node_tree.nodes['Background']
bg.inputs[0].default_value = (0.02, 0.02, 0.02, 1)

