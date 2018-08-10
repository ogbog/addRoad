import bpy
import random
from mathutils import Vector


def curveSetup (curve, repeater, spacing, lanes=0):

    

    repeater.parent=curve
    bpy.context.scene.objects.active = repeater




    ## of lanes across the highway
    # TODO(Joey): change this from checking if the name is "lanes"
    #             to lanes value being non-zero
    if repeater.name =="lanes":
        ArrayLanes = repeater.modifiers.new("ArrayLanes", type='ARRAY')
        ArrayLanes.count = lanes
        ArrayLanes.relative_offset_displace = (0,1,0)



    #mirror, since these are 2 way symmetrical roads
    MirrorTwoway = repeater.modifiers.new("Mirror_Twoway", type='MIRROR')
    MirrorTwoway.use_x = False
    MirrorTwoway.use_y = True #identical, left in to show goal
    

    #repeat along the curve
    ArrayCurveLength = repeater.modifiers.new("ArrayCurveLength", type='ARRAY')
    ArrayCurveLength.fit_type = 'FIT_CURVE'
    ArrayCurveLength.curve = curve
    ArrayCurveLength.use_merge_vertices = True




    #curve deformer
    CurveModifier = repeater.modifiers.new("Curve", type='CURVE')
    CurveModifier.object=curve
    
    bpy.context.scene.objects.active = repeater
    bpy.ops.object.location_clear(clear_delta=False)


    #Visibility
    curve.show_x_ray = True


