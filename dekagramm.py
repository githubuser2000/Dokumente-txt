import bpy
import bmesh

# Parameter
n = 10            # Anzahl Ecken (Zacken)
skip = 3          # Schrittweite für Sternpolygon (z.B. 10/3 für Dekagramm)
radius = 1.0      # Radius
height = 0.2      # Höhe des 3D-Körpers

# Punktberechnung
import math
angle_step = 2 * math.pi / n
points = []
current = 0

for _ in range(n):
    angle = current * angle_step
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    points.append((x, y))
    current = (current + skip) % n

# Neues Mesh und Objekt
mesh = bpy.data.meshes.new(name='Dekagram')
obj = bpy.data.objects.new(name='Dekagram', object_data=mesh)
bpy.context.collection.objects.link(obj)
bpy.context.view_layer.objects.active = obj
bm = bmesh.new()

# Vertices: oben
for x, y in points:
    bm.verts.new((x, y, height / 2))

# Vertices: unten
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

# Deckfläche (oben)
bm.faces.new([bm.verts[i] for i in range(n)])

# Bodenfläche (unten)
bm.faces.new([bm.verts[i + n] for i in reversed(range(n))])

# Mesh finalisieren
bm.to_mesh(mesh)
bm.free()

