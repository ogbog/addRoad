import bpy
import random
from mathutils import Vector


def makeCurve():
    if (len(bpy.context.selected_objects) > 0 and bpy.context.selected_objects[-1].type == "CURVE"):
        useCurve(bpy.context.selected_objects[-1])
    else:
        createCurve()
    


def useCurve(ob):
    ob.select=True
    ob.show_name = True
    if ob.data.splines[0].use_cyclic_u == False:
        start = ob.data.splines[0].bezier_points[0].co
        bpy.context.scene.cursor_location = start
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    else: 
        ob.data.use_path = False    
def createCurve(): #style = selected curve or new curve. curve is optional variable.
    cu=bpy.data.curves.new("myCurve", 'CURVE')
    ob=bpy.data.objects.new("CurvyRoad", cu)
    ob.location = (0,0,0)
    ob.select=True
    ob.show_name = True
    bpy.context.scene.objects.link(ob)
    cu.splines.data.splines.new("BEZIER")
    cu.splines.data.splines[0].bezier_points.add(2)

    cu.dimensions = '3D'


    cu.splines.data.splines[0].bezier_points[0].co.xyz = Vector((0,0,0))
    cu.splines.data.splines[0].bezier_points[1].co.xyz = Vector((20,50,0))
    cu.splines.data.splines[0].bezier_points[2].co.xyz = Vector((0,100,0))
    
        
        
        
    
    for i, bezierPoint in enumerate(cu.splines[0].bezier_points):
            origin = [bezierPoint.co[0], bezierPoint.co[1], bezierPoint.co[2]] 
            if i == 0:
                bezierPoint.handle_left_type = 'ALIGNED'
                bezierPoint.handle_right_type = 'ALIGNED'
                bezierPoint.handle_left = (0, -10, 0)
                bezierPoint.handle_right = (0, 10, 0)
            else:
                bezierPoint.handle_left_type = 'ALIGNED'
                bezierPoint.handle_right_type = 'ALIGNED'
                bezierPoint.handle_left = (origin[0], origin[1]-20, origin[2])
                bezierPoint.handle_right = (origin[0], origin[1]+20, origin[2])
        