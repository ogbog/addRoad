#groundMesh = most simple. 
import bpy
import random
from mathutils import Vector



def groundMesh (name, dist1, dist2): #dist1&2 are distance from center and how far from that start
    me=bpy.data.meshes.new(name+"Mesh")
    ob=bpy.data.objects.new(name, me)
    ob.location = (0,0,0)
    #stick in the newest collection, aka the one makeCurve made
    col = bpy.context.scene.collection.children[-1]
    col.objects.link(ob)
    ob.show_name = True
    ob.select_set(1)
    #bpy.context.scene.objects.link(ob)

    myVerts = [
        (0,dist1,0),
        (0,dist2,0),
        (5,dist2,0),
        (5,dist1,0)
    ]
    me.from_pydata(myVerts, [], [(0,1,2,3)])
    me.uv_layers.new(name="base")
    me.uv_layers.new(name="accent")
#    uv_textures["UVMap"].name
    
#    bpy.data.meshes['lanesMesh'].uv_textures[1].name='accent'

    return ob