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
        (1,dist2,0),
        (1,dist1,0)
    ]
    me.from_pydata(myVerts, [], [(0,1,2,3)])
    bpy.ops.object.shade_smooth()
    return ob