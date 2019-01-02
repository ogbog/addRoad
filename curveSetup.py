import bpy
import random
from mathutils import Vector


def curveSetup (curve, ob, spacing):
    #ob.select_set(1)
    #bpy.context.scene.objects.active = mesh

    #mirror, since these are 2 way symmetrical roads
    MirrorTwoway = ob.modifiers.new("Mirror_Twoway", type='MIRROR')
    MirrorTwoway.use_axis[0] = 0
    MirrorTwoway.use_axis[1] = 1 #identical, left in to show goal 

    #repeat along the curve
    ArrayCurveLength = ob.modifiers.new("ArrayCurveLength", type='ARRAY')
    ArrayCurveLength.fit_type = 'FIT_CURVE'
    ArrayCurveLength.curve = curve
    ArrayCurveLength.use_merge_vertices = True

    #curve deformer
    CurveModifier = ob.modifiers.new("Curve", type='CURVE')
    CurveModifier.object=curve
    
    #bpy.context.scene.objects.active = mesh


    #Visibility
    curve.show_in_front = True
    ob.parent=curve


def lanesSetup (object, amt):
        ArrayLanes = object.modifiers.new("ArrayLanes", type='ARRAY')
        ArrayLanes.count = amt
        ArrayLanes.relative_offset_displace = (0,1,0)
