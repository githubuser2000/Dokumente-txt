import bpy
import math

# Szene säubern
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Metallisches Material erstellen
def create_metal_material(name, color=(0.8, 0.8, 0.9, 1)):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Metallic"].default_value = 1.0
    bsdf.inputs["Roughness"].default_value = 0.1
    return mat

metal_mat = create_metal_material("PolishedMetal")

# Sternpunkte generieren
def star_points(n, R1, R2):
    points = []
    for i in range(2 * n):
        angle = math.pi * i / n
        r = R1 if i % 2 == 0 else R2
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        points.append((x, y))
    return points

# Mesh erstellen aus 2D-Kurve
def create_star_mesh(name, points, z_offset=0, depth=0.1, bevel=0.01, scale=1.0):
    curve = bpy.data.curves.new(name, type='CURVE')
    curve.dimensions = '2D'
    polyline = curve.splines.new('POLY')
    polyline.points.add(len(points))
    for i, (x, y) in enumerate(points + [points[0]]):  # geschlossen
        polyline.points[i].co = (scale * x, scale * y, z_offset, 1)
    curve.extrude = depth
    curve.bevel_depth = bevel
    obj = bpy.data.objects.new(name, curve)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(metal_mat)
    return obj

# Dekagramm
create_star_mesh("Dekagramm", star_points(10, 1.0, 0.8), z_offset=0.0, depth=0.05, bevel=0.002)

# Heptagramm (stark skaliert)
create_star_mesh("Heptagramm", star_points(7, 0.7, 0.3), z_offset=0.05, depth=0.1, bevel=0.01, scale=0.6)

# Bowen-Knoten (vereinfachtes Schleifenquadrat)
def create_bowen_knot():
    coords = [(0.2,0.2), (-0.2,0.2), (-0.2,-0.2), (0.2,-0.2)]
    curve = bpy.data.curves.new('BowenKnot', type='CURVE')
    curve.dimensions = '2D'
    spline = curve.splines.new('POLY')
    spline.points.add(len(coords))
    for i, (x, y) in enumerate(coords + [coords[0]]):  # Schleife schließen
        spline.points[i].co = (x, y, 0.1, 1)
    curve.extrude = 0.05
    curve.bevel_depth = 0.005
    obj = bpy.data.objects.new("BowenKnot", curve)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(metal_mat)
    return obj

create_bowen_knot()

# Kamera hinzufügen
def add_camera():
    bpy.ops.object.camera_add(location=(0, -3.5, 1.8), rotation=(math.radians(75), 0, 0))
    cam = bpy.context.object
    bpy.context.scene.camera = cam

add_camera()

# Licht hinzufügen
def add_light():
    bpy.ops.object.light_add(type='AREA', location=(0, -2, 2))
    light = bpy.context.object
    light.data.energy = 1000
    light.data.size = 3

add_light()

