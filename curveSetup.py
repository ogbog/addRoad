import bpy
import random
from mathutils import Vector


def curveSetup (curve, repeater, spacing, lanes=0):

    mySpline = curve.data.splines.active
    mySpline.bezier_points[0].co.xyz = Vector((0,0,0))
    mySpline.bezier_points[1].co.xyz = Vector((0,100,0))

    for i, bezierPoint in enumerate(mySpline.bezier_points):
        if i == 0:
            bezierPoint.handle_left_type = 'VECTOR'
            bezierPoint.handle_right_type = 'VECTOR'
        else:
            bezierPoint.handle_left_type = 'ALIGNED'
            bezierPoint.handle_right_type = 'ALIGNED'
            bezierPoint.handle_left = (50, 75, 0)
            bezierPoint.handle_left = (-50, 125, 0)

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
