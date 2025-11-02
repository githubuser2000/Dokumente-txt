import bpy
import bmesh
import math

# ----------------------------
# Parameter
# ----------------------------
n = 10        # Anzahl Ecken
skip = 3      # Schrittweite für Sternform
radius = 1.0
depth = 0.2   # Dicke des Objekts

# ----------------------------
# Punkte für 2D-Stern erzeugen
# ----------------------------
angle_step = 2 * math.pi / n
points2d = []
idx = 0

for _ in range(n):
    angle = idx * angle_step
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    points2d.append((x, y))
    idx = (idx + skip) % n

# ----------------------------
# Mesh-Objekt mit BMesh erzeugen
# ----------------------------
mesh = bpy.data.meshes.new("Dekagram")
obj = bpy.data.objects.new("Dekagram", mesh)
bpy.context.collection.objects.link(obj)
bpy.context.view_layer.objects.active = obj
bpy.ops.object.select_all(action='DESELECT')
obj.select_set(True)

bm = bmesh.new()

# 2D-Punkte auf Z=0 Ebene als Vertices
verts = [bm.verts.new((x, y, 0)) for x, y in points2d]
bmesh.ops.contextual_create(bm, geom=verts)

# Fläche extrudieren
bm.faces.ensure_lookup_table()
face = bm.faces[0]

extrude_result = bmesh.ops.extrude_face_region(bm, geom=[face])
bmesh.ops.translate(
    bm,
    vec=(0, 0, depth),
    verts=[v for v in extrude_result["geom"] if isinstance(v, bmesh.types.BMVert)]
)

bm.normal_update()
bm.to_mesh(mesh)
bm.free()

# ----------------------------
# Material: Metallisch glänzend
# ----------------------------
mat = bpy.data.materials.new(name="Metallisch")
mat.use_nodes = True
nodes = mat.node_tree.nodes
links = mat.node_tree.links

# Bestehende Nodes entfernen
for node in nodes:
    nodes.remove(node)

# Neue Nodes
output = nodes.new(type='ShaderNodeOutputMaterial')
principled = nodes.new(type='ShaderNodeBsdfPrincipled')

output.location = (300, 0)
principled.location = (0, 0)

# Eigenschaften setzen
principled.inputs["Metallic"].default_value = 1.0
principled.inputs["Roughness"].default_value = 0.05
principled.inputs["Base Color"].default_value = (0.9, 0.95, 1.0, 1.0)

# Verbinden
links.new(principled.outputs["BSDF"], output.inputs["Surface"])

# Zuweisen
obj.data.materials.append(mat)

