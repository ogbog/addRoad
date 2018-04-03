import bpy
import random
from mathutils import Vector


#assign random RGB to make more visible
def randomMaterial(ob):
    if bpy.context.scene.render.engine != 'CYCLES':
        bpy.context.scene.render.engine = 'CYCLES'
        

    newMat = bpy.data.materials.new(ob.name+"Material")
    newMat.use_nodes = True
    ob.active_material = newMat
    newMat.node_tree.nodes['Diffuse BSDF'].inputs[0].default_value = (random.random(), random.random(), random.random(), 1) # black
