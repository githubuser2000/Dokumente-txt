import bpy
import math

# Szene leeren
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Parameter
num_points = 10
outer_radius = 1.0
inner_radius = 0.4
height = 0.3

# Punkte für den Stern generieren
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

# Oben und unten verbinden
verts = verts_top + verts_bottom
faces = []

# Seitenflächen
for i in range(len(verts_top)):
    next_i = (i + 1) % len(verts_top)
    top1 = i
    top2 = next_i
    bottom1 = i + len(verts_top)
    bottom2 = next_i + len(verts_top)
    faces.append([top1, top2, bottom2, bottom1])

# Deckel oben
faces.append([i for i in range(len(verts_top))])

# Deckel unten
faces.append([i + len(verts_top) for i in reversed(range(len(verts_top)))])

# Mesh erstellen
mesh = bpy.data.meshes.new("Dekagram")
mesh.from_pydata(verts, [], faces)
mesh.update()

obj = bpy.data.objects.new("Dekagram", mesh)
bpy.context.collection.objects.link(obj)

# Metallisches Material hinzufügen
mat = bpy.data.materials.new(name="ShinyMetal")
mat.use_nodes = True
nodes = mat.node_tree.nodes
principled = nodes.get("Principled BSDF")
principled.inputs["Metallic"].default_value = 1.0
principled.inputs["Roughness"].default_value = 0.05
principled.inputs["Base Color"].default_value = (0.9, 0.95, 1.0, 1)

obj.data.materials.append(mat)

