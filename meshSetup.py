#groundMesh = most simple. 
import bpy
import random
from mathutils import Vector



def groundMesh (name, dist1, dist2): #dist1&2 are distance from center and how far from that start
    me=bpy.data.meshes.new(name+"Mesh")
    ob=bpy.data.objects.new(name, me)
    ob.location = (0,0,0)
    ob.select=True
    ob.show_name = True
    bpy.context.scene.objects.link(ob)

    myVerts = [
        (0,dist1,0),
        (0,dist2,0),
        (5,dist2,0),
        (5,dist1,0)
    ]
    me.from_pydata(myVerts, [], [(0,1,2,3)])
    me.uv_textures.new(name="base")
    me.uv_textures.new(name="accent")
#    uv_textures["UVMap"].name
    
#    bpy.data.meshes['lanesMesh'].uv_textures[1].name='accent'

    return ob