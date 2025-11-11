import bpy
import bmesh
import math

# Alles löschen
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# ----------------------------
# Parameter
# ----------------------------
outer_radius = 1.0
inner_radius = 0.4
num_points = 10
depth = 0.2

# ----------------------------
# 2D Stern (Dekagramm) erstellen
# ----------------------------
verts2d = []
angle_step = math.pi / num_points

for i in range(num_points * 2):
    angle = i * angle_step
    r = outer_radius if i % 2 == 0 else inner_radius
    x = r * math.cos(angle)
    y = r * math.sin(angle)
    verts2d.append((x, y))

# Curve-Objekt erzeugen
curve_data = bpy.data.curves.new(name='StarCurve', type='CURVE')
curve_data.dimensions = '2D'
polyline = curve_data.splines.new('POLY')
polyline.points.add(len(verts2d) - 1)

for i, (x, y) in enumerate(verts2d):
    polyline.points[i].co = (x, y, 0, 1)

polyline.use_cyclic_u = True

curve_obj = bpy.data.objects.new('DekagramCurve', curve_data)
bpy.context.collection.objects.link(curve_obj)

# In Mesh umwandeln und extrudieren
bpy.context.view_layer.objects.active = curve_obj
bpy.ops.object.convert(target='MESH')
bpy.ops.object.editmode_toggle()
bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, depth)})
bpy.ops.object.editmode_toggle()

# Objekt umbenennen
curve_obj.name = "Dekagram"

# ----------------------------
# Material erstellen und zuweisen
# ----------------------------
mat = bpy.data.materials.new(name="MetallicMaterial")
mat.use_nodes = True

nodes = mat.node_tree.nodes
links = mat.node_tree.links

# Clear nodes
for node in nodes:
    nodes.remove(node)

# Nodes hinzufügen
output = nodes.new(type='ShaderNodeOutputMaterial')
bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
output.location = (300, 0)
bsdf.location = (0, 0)

# Material-Eigenschaften
bsdf.i

