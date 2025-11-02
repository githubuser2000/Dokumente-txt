import bpy
import bmesh
import math

# ----------------------------
# Parameter
# ----------------------------
n = 10            # Anzahl Ecken (Zacken)
skip = 3          # Schrittweite für Sternpolygon (z.B. 10/3 für Dekagramm)
radius = 1.0      # Radius des Dekagramms
height = 0.2      # Höhe des 3D-Objekts

# ----------------------------
# Punkte des Dekagramms berechnen
# ----------------------------
angle_step = 2 * math.pi / n
points = []
current = 0

for _ in range(n):
    angle = current * angle_step
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    points.append((x, y))
    current = (current + skip) % n

# ----------------------------
# Neues Mesh & Objekt
# ----------------------------
mesh = bpy.data.meshes.new(name='Dekagram')
obj = bpy.data.objects.new(name='Dekagram', object_data=mesh)
bpy.context.collection.objects.link(obj)
bpy.context.view_layer.objects.active = obj
bm = bmesh.new()

# Vertices oben
for x, y in points:
    bm.verts.new((x, y, height / 2))

# Vertices unten
for x, y in points:
    bm.verts.new((x, y, -height / 2))

bm.verts.ensure_lookup_table()

# Seitenflächen
for i in range(n):
    top1 = i
    top2 = (i + 1) % n
    bottom1 = i + n
    bottom2 = ((i + 1) % n) + n
    bm.faces.new([
        bm.verts[top1],
        bm.verts[top2],
        bm.verts[bottom2],
        bm.verts[bottom1]
    ])

# Deckel und Boden
bm.faces.new([bm.verts[i] for i in range(n)])             # oben
bm.faces.new([bm.verts[i + n] for i in reversed(range(n))])  # unten

# Mesh finalisieren
bm.to_mesh(mesh)
bm.free()

# ----------------------------
# Material erstellen und zuweisen
# ----------------------------
mat = bpy.data.materials.new(name="MetallischGlänzend")
mat.use_nodes = True

# Nodes manipulieren
nodes = mat.node_tree.nodes
links = mat.node_tree.links

# Vorhandene löschen
for node in nodes:
    nodes.remove(node)

# Neue Nodes
output_node = nodes.new(type='ShaderNodeOutputMaterial')
principled = nodes.new(type='ShaderNodeBsdfPrincipled')

# Positionieren (für Übersichtlichkeit im Shader-Editor)
output_node.location = (300, 0)
principled.location = (0, 0)

# Einstellungen für glänzendes Metall
principled.inputs["Metallic"].default_value = 1.0
principled.inputs["Roughness"].default_value = 0.1
principled.inputs["Base Color"].default_value = (0.9, 0.9, 1.0, 1)  # leicht bläulich

# Verbinden
links.new(principled.outputs["BSDF"], output_node.inputs["Surface"])

# Material zuweisen
if obj.data.materials:
    obj.data.materials[0] = mat
else:
    obj.data.materials.append(mat)

