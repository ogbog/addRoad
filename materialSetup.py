import bpy
import random
import os
from mathutils import Vector


def cyclesCheck():
    if bpy.context.scene.render.engine != 'CYCLES':
        bpy.context.scene.render.engine = 'CYCLES'



#assign random RGB to make more visible
def randomMaterial(ob):
    newMat = bpy.data.materials.new(ob.name+"Material")
    newMat.use_nodes = True
    ob.active_material = newMat
    
    myTuple = (random.random(), random.random(), random.random(), 1.0)
    newMat.node_tree.nodes['Diffuse BSDF'].inputs[0].default_value = myTuple # black






def mainMaterial(ob):
    path = bpy.utils.script_path_user()    
    path += "\\addons\\addRoad\\materials.blend"
    mat = ob.name+"Material"
    with bpy.data.libraries.load(path) as (data_from, data_to):
        data_to.materials = [mat]
    

    newMat = bpy.data.materials[mat]
    ob.active_material = newMat
