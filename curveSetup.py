import bpy
import random
from mathutils import Vector


def curveSetup (curve, repeater, spacing, lanes=0):
    
    mySpline=bpy.data.curves[curve.data.name].splines.active
    mySpline.bezier_points[0].co.xyz=Vector((0,0,0))                        
    mySpline.bezier_points[1].co.xyz=Vector((0,100,0))

    for i in range(len(mySpline.bezier_points)): 
        if i == 0:
            mySpline.bezier_points[i].handle_left_type = 'VECTOR'
            mySpline.bezier_points[i].handle_right_type = 'VECTOR'
        else: z
            mySpline.bezier_points[i].handle_left_type = 'ALIGNED'
            mySpline.bezier_points[i].handle_right_type = 'ALIGNED'
            mySpline.bezier_points[i].handle_left = (50, 75, 0)
            mySpline.bezier_points[i].handle_right = (-50, 125, 0)
    


    
    bpy.data.objects[repeater.name].parent=curve
    bpy.context.scene.objects.active = repeater




    ## of lanes across the highway
    if repeater.name =="lanes":
        bpy.data.objects[repeater.name].modifiers.new("ArrayLanes", type='ARRAY')
        bpy.data.objects[repeater.name].modifiers["ArrayLanes"].count=lanes
        bpy.data.objects[repeater.name].modifiers["ArrayLanes"].relative_offset_displace=(0,1,0)



    #mirror, since these are 2 way symmetrical roads
    repeater.modifiers.new("Mirror_Twoway", type='MIRROR')
    bpy.data.objects[repeater.name].modifiers["Mirror_Twoway"].use_x=False
    repeater.modifiers["Mirror_Twoway"].use_y=True #identical, left in to show goal
    

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

    


