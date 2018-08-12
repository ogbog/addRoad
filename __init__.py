bl_info = {
    "name":"Add a road ",
    "author":"Oscar",
    "version":(1,0),
    "blender":(2,79),
    "location":"View3D > Add > Mesh > Add road",
    "description":"Adds a new road",
    "warning":"",
    "wiki_url":"",
    "category":"Add Mesh"
    }

'''
Import logic: 

1. UI elements
2. curve setup
2. material setup
3. road mesh setup
4. accessories mesh setup
5. a two-way function that adds a road
6. init: brings all these together
'''


if "bpy" in locals():
    import importlib
    importlib.reload(roadInterface)
    importlib.reload(makeCurve)
    importlib.reload(curveSetup)
    importlib.reload(meshSetup)
    importlib.reload(materialSetup)
#    importlib.reload(parentRig)
    

else:
    from . import roadInterface
    from . import makeCurve
    from . import curveSetup
    from . import meshSetup
    from . import materialSetup
#    from . import parentRig
    
    
    

import os
import bpy
import random
from mathutils import Vector
C=bpy.context
D=bpy.data
O=bpy.ops


# classes
class OBJECT_OT_add_road(bpy.types.Operator):

    
    """Adds a road to the 3D view"""
    bl_label = "Add road"
    bl_idname = "mesh.add_road"
    bl_options = {'REGISTER', 'UNDO'}
    
    '''
    We're assuming 1 blender unit = 1 meter
    based on that, here's some real world measurements. 
    ***UNIVERSITY DISTRICT STREET***
    5 feet:            1.5
    Human:             1.8
    Lanes:             1
    Lane width:        2
    divider width:     ?
    shoulder width:    1.8
    bike width:        0
    gutter width:      0.1
    greenway width:    1.5
    sidewalk width:    1.5
    
    
    
    '''
    
    
    roadPresets = bpy.props.EnumProperty(
        name = "Road presets",
        description = "Various default roads",
        
        items = [('university', "University Ave", "University Ave"), #identifier, name, description
                 ('mainstreet', "Main Street USA", "A generic beginner street"),
                 ('highway520', "Highway 520", "A highway with IUD lights in the middle, LOL")]
        #update = updateRoadPreset()
        )
    
    accDividerOn=bpy.props.BoolProperty(name="Divider accessories on/off", default=True, description="Turn on Accessories on the road divider")
    accShoulderOn=bpy.props.BoolProperty(name="Shoulder accessories on/off", default=True, description="Turn on Accessories on the shoulder")
    accGutterOn=bpy.props.BoolProperty(name="Gutter accessories on/off", default=True, description="Turn on Accessories on the gutter")
    accGreenwayOn=bpy.props.BoolProperty(name="Greenway accessories on/off", default=True, description="Turn on Accessories on the greenway")
    accSidewalkOn=bpy.props.BoolProperty(name="Sidewalk accessories on/off", default=True, description="Turn on Accessories on the sidewalk")
    
    accDivider=bpy.props.EnumProperty(
        name = "Divider accessory",
        description = "Selects which kind of divider accessory to insert",
        items = [("rail", "rail", "rail"), ("concrete", "concrete", "concrete"), ("poles", "poles", "poles")
            ]
        )
    
    
    lanes = bpy.props.IntProperty( 
        name = "Lanes",
        default = 2,
        min = 1,
        description = "Number of lanes"
        )
    laneWidth = bpy.props.FloatProperty(
        name = "Lane Width",
        default = 3,
        min = .01,
        description = "How wide across each lane is"
        )
    dividerWidth = bpy.props.FloatProperty(
        name = "Divider width",
        default = .5,
        min = 0,
        description = "division size between east/west traffic lanes"
        )
    shoulderWidth = bpy.props.FloatProperty(
        name = "Shoulder width",
        default = 2,
        min = 0,
        description = "width of shoulder or parking lane to left/right"
        )

    bikeWidth = bpy.props.FloatProperty(
        name = "Bike width",
        default = 1,
        min = 0,
        description = "width of shoulder or parking lane to left/right"
        )
    gutterWidth = bpy.props.FloatProperty(
        name = "Gutter width",
        default = .2,
        min = 0,
        description = "width of gutter as transition to pedestrian area" #needs a height modifier...?
        )
    greenwayWidth = bpy.props.FloatProperty(
        name="Greenway width",
        default = 1,
        min = 0,
        description = "width of greenish area ala seattle" )    
    sidewalkWidth = bpy.props.FloatProperty(
        name="Sidewalk width",
        default = 1.5,
        min = 0,
        description = "width of sidewalk" )
    name = bpy.props.StringProperty(
        name = "Name",
        default = "Road",
        description = "Name of added road"
        )


    
    def draw(self, context):
            layout = self.layout
            scene = bpy.data.window_managers["WinMan"].operators['MESH_OT_add_road']
            #that big long name is where used panels are
            #hence still uses our props
            #it should instead be on the rig. So rig should be before...?
            layout.label(text="Add a road, dude!")   
            

            row = layout.row()
            row.prop(scene, "roadPresets")
           
            
            layout.label(text="pathway widths")
            row = layout.row()
            row.prop(scene, "lanes")
            row.prop(scene, "laneWidth")

            row = layout.row()
            row.prop(scene, "dividerWidth")
            row.prop(scene, "shoulderWidth")

            row = layout.row()
            row.prop(scene, "bikeWidth")
            row.prop(scene, "gutterWidth")

            row = layout.row()
            row.prop(scene, "greenwayWidth")
            row.prop(scene, "sidewalkWidth")
            
            layout.label(text="accessories")
            row = layout.row()
            row.prop(scene, "accDividerOn")
            row.prop(scene, "accShoulderOn")
            row.prop(scene, "accGutterOn")
            row.prop(scene, "accGreenwayOn")
            row.prop(scene, "accSidewalkOn")
            
            row = layout.row()
            row.prop(scene, "accDivider")
        
#mesh.splines[0].bezier_points[0].co[1]
    
#list of roads

#lanes, laneWidth, dividerWidth, shoulderWidth, bikeWidth, gutterWidth, greenwayWidth, sidewalkWidth, name

 
    roads = [[1, 2, .1, 1.8, 0, 0.1, 1.5, 1.5, "university"],
             [1, 2, .1, 1.8, 0, 0.1, 1.5, 1.5, "mainstreet"],
             [4, 2.5, 1, 3, 0, 0, 5, 0, "highway520"]]        
            


    def execute(self, context):
        
        
        def setPreset():
            bpy.data.window_managers["WinMan"].operators['MESH_OT_add_road'].roadPresets

    

        
        #combining them in a modifier stack
            
            


        

        #distance bookmarks


#assembling the default road
        roadExtras = []
        roadMeshes = []


        makeCurve.makeCurve()
        roadCurve = bpy.context.selected_objects[-1]        
        
        
        
        if (self.dividerWidth !=0):
            divider = meshSetup.groundMesh("divider", 0, self.dividerWidth)
            curveSetup.curveSetup (roadCurve, divider, 1)     
            roadMeshes.append(divider)
        if (self.laneWidth !=0):
            lanes = meshSetup.groundMesh("lanes", self.dividerWidth, self.dividerWidth+self.laneWidth)
            curveSetup.curveSetup (roadCurve, lanes, 1, self.lanes)     
            roadMeshes.append(lanes)
        
        #since road is multiplicative, a custom variable
        newLaneStart = self.laneWidth*self.lanes
        newLaneStart +=self.dividerWidth

#        roadExtras = [shoulder, bike, gutter, greenway, sidewalk]
#        roadMeshes=[divider, lanes, shoulder, bike, gutter, greenway, sidewalk]        


        
        if (self.shoulderWidth != 0):
            shoulder = meshSetup.groundMesh("shoulder", newLaneStart, newLaneStart + self.shoulderWidth)            
            newLaneStart+=self.shoulderWidth        
            roadExtras.append(shoulder)
        
        if (self.bikeWidth !=0):
            bike = meshSetup.groundMesh("bike", newLaneStart, newLaneStart + self.bikeWidth)
            newLaneStart+=self.bikeWidth        
            roadExtras.append(bike)
        
        if (self.gutterWidth !=0):
            gutter = meshSetup.groundMesh("gutter", newLaneStart, newLaneStart + self.gutterWidth)
            newLaneStart+=self.gutterWidth        
            roadExtras.append(gutter)
        if (self.greenwayWidth !=0):
            greenway = meshSetup.groundMesh("greenway", newLaneStart, newLaneStart + self.greenwayWidth)
            newLaneStart+=self.greenwayWidth        
            roadExtras.append(greenway)
        if (self.sidewalkWidth !=0):
            sidewalk = meshSetup.groundMesh("sidewalk", newLaneStart, newLaneStart + self.sidewalkWidth)
            newLaneStart+=self.sidewalkWidth
            roadExtras.append(sidewalk)
        
        roadMeshes += roadExtras

        for i in roadExtras:
            curveSetup.curveSetup (roadCurve, i, 1)      



        
        
        #for i in range(len(x)):
        #    if (len(bpy.data.objects[x[i]].material_slots) == 0):
        #        materialSetup.randomMaterial(bpy.data.objects[x[i]])
            
            
            
        
        for i in roadMeshes: 
            materialSetup.randomMaterial(i)

        return {'FINISHED'}



def add_object_button(self, context):
    self.layout.operator(
            OBJECT_OT_add_road.bl_idname)

# registration
def register():
    bpy.utils.register_class(OBJECT_OT_add_road)
    #bpy.utils.register_class(smooth_monkey_panel)
    bpy.types.INFO_MT_mesh_add.append(add_object_button)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_road)
    #bpy.utils.unregister_class(smooth_monkey_panel)
    bpy.types.INFO_MT_mesh_add.remove(ct_button)

if __name__ == "__main__":
    register()