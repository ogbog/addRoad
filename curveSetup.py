import bpy
import random
from mathutils import Vector


def curveSetup (curve, mesh, spacing):
    
    bpy.context.scene.objects.active = mesh

    #mirror, since these are 2 way symmetrical roads
    MirrorTwoway = mesh.modifiers.new("Mirror_Twoway", type='MIRROR')
    MirrorTwoway.use_x = False
    MirrorTwoway.use_y = True #identical, left in to show goal 

    #repeat along the curve
    ArrayCurveLength = mesh.modifiers.new("ArrayCurveLength", type='ARRAY')
    ArrayCurveLength.fit_type = 'FIT_CURVE'
    ArrayCurveLength.curve = curve
    ArrayCurveLength.use_merge_vertices = True

    #curve deformer
    CurveModifier = mesh.modifiers.new("Curve", type='CURVE')
    CurveModifier.object=curve
    
    bpy.context.scene.objects.active = mesh


    #Visibility
    curve.show_x_ray = True
    mesh.parent=curve


def lanesSetup (object, amt):
        ArrayLanes = object.modifiers.new("ArrayLanes", type='ARRAY')
        ArrayLanes.count = amt
        ArrayLanes.relative_offset_displace = (0,1,0)
