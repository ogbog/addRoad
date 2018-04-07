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
        bpy.data.objects[repeater.name].modifiers.new("ArrayLanes", type='ARRAY')
        bpy.data.objects[repeater.name].modifiers["ArrayLanes"].count = lanes
        bpy.data.objects[repeater.name].modifiers["ArrayLanes"].relative_offset_displace = (0,1,0)



    #mirror, since these are 2 way symmetrical roads
    repeater.modifiers.new("Mirror_Twoway", type='MIRROR')
    repeater.modifiers["Mirror_Twoway"].use_x = False
    repeater.modifiers["Mirror_Twoway"].use_y = True #identical, left in to show goal
    

    #repeat along the curve
    repeater.modifiers.new("ArrayCurveLength", type='ARRAY')
    repeater.modifiers["ArrayCurveLength"].fit_type = 'FIT_CURVE'
    repeater.modifiers["ArrayCurveLength"].curve = curve
    repeater.modifiers["ArrayCurveLength"].use_merge_vertices = True




    #curve deformer
    repeater.modifiers.new("Curve", type='CURVE')
    repeater.modifiers["Curve"].object=curve
    
    bpy.context.scene.objects.active = repeater
    bpy.ops.object.location_clear(clear_delta=False)


    #Visibility
    curve.show_x_ray = True #
