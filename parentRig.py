import bpy

def parentRig(name, baby):

    amt = bpy.data.armatures.new(name)
    ob = bpy.data.objects.new(name, amt)
    scn = bpy.context.scene
    scn.objects.link(ob)
    
    scn.objects.active = ob
    ob.select = True
    bpy.ops.object.mode_set(mode='EDIT')

    bone = amt.edit_bones.new('Bone')
    bone.head = (0,0,0)
    bone.tail = (0,0,1)
    
    baby.parent= ob
    
    return (ob)