import bpy
import random
from mathutils import Vector
C=bpy.context
D=bpy.data
O=bpy.ops

#assign random RGB to make more visible
def randomMaterial(ob):
    if C.scene.render.engine != 'CYCLES':
        C.scene.render.engine = 'CYCLES'
        

    
    bpy.ops.material.new()
    new_mat = bpy.data.materials[-1]  # the new material is the last one in the list
    new_mat.name = ob.name+"Material"
    ob.active_material=bpy.data.materials[ob.name+'Material']
    D.materials[ob.name+'Material'].node_tree.nodes['Diffuse BSDF'].inputs[0].default_value = (random.random(), random.random(), random.random(), 1) # black
