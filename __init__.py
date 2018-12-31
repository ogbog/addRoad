bl_info = {
    "name":"Add a road ",
    "author":"Oscar",
    "version":(1,0),
    "blender":(2,80,0),
    "location":"View3D > Add > Mesh > Add road",
    "description":"Adds a new road",
    "warning":"",
    "wiki_url":"",
    "category":"Add Mesh"
    }



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
from bpy.types import Operator
from bpy.props import FloatVectorProperty, BoolProperty, IntProperty, EnumProperty, StringProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector


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
    Pole height:       50 ft or 15 units
    
    '''
    
    
    
    roadPresets = EnumProperty(
        name = "Road presets",
        description = "Various default roads",
        
        items = [('university', "University Ave", "University Ave"), #identifier, name, description
                 ('mainstreet', "Main Street USA", "A generic beginner street"),
                 ('highway520', "Highway 520", "A highway with IUD lights in the middle, LOL")]
        #update = updateRoadPreset()
        )
    
    accDividerOn=BoolProperty(name="Divider accessories on/off", default=True, description="Turn on Accessories on the road divider")
    accShoulderOn=BoolProperty(name="Shoulder accessories on/off", default=True, description="Turn on Accessories on the shoulder")
    accGutterOn=BoolProperty(name="Gutter accessories on/off", default=True, description="Turn on Accessories on the gutter")
    accGreenwayOn=BoolProperty(name="Greenway accessories on/off", default=True, description="Turn on Accessories on the greenway")
    accSidewalkOn=BoolProperty(name="Sidewalk accessories on/off", default=True, description="Turn on Accessories on the sidewalk")
    accDivider=EnumProperty(name = "Divider accessory", description = "Selects which kind of divider accessory to insert", items = [("rail", "rail", "motherfucking rail"), ("concrete", "concrete", "motherfucking concrete"), ("poles", "poles", "motherfucking poles")])
    #enums 
    
    name = StringProperty(name = "Name", default = "Road", description = "Name of added road")
    laneCount = IntProperty(name = "Lane Count", default = 2, min = 1, description = "Number of lanes")

    
    laneWidth = FloatProperty(name = "lanes", default = 3.0, min = .01, description = "How wide across each lane is")
    dividerWidth = FloatProperty(name = "divider", default = .5, min = 0.0, description = "division size between east/west traffic lanes")
    shoulderWidth = FloatProperty(name = "shoulder", default = 2.0, min = 0.0, description = "width of shoulder or parking lane to left/right")
    bikeWidth = FloatProperty(name = "bike", default = 1.9, min = 0.0, description = "width of shoulder or parking lane to left/right")
    gutterWidth = FloatProperty(name = "gutter", default = .2, min = 0.0, description = "width of gutter as transition to pedestrian area" )#needs a height modifier...? 
    greenwayWidth = FloatProperty(name="greenway", default = 1.0, min = 0.0, description = "width of greenish area ala seattle" )    
    sidewalkWidth = FloatProperty(name="sidewalk", default = 1.5, min = 0.0, description = "width of sidewalk" )
    
    


    



    
    
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
            row.prop(scene, "laneCount")
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


        makeCurve.makeCurve()
        roadCurve = bpy.context.selected_objects[-1]        
        

        roadMeshes = []
        roadOrder = ["divider", "lanes", "sidewalk", "greenway", "gutter", "bike", "shoulder"]
        meshiepoos = {
            "divider" : self.dividerWidth,
            "lanes" : self.laneWidth,
            "sidewalk" : self.sidewalkWidth,
            "greenway" : self.greenwayWidth,
            "gutter" : self.gutterWidth,
            "bike" : self.bikeWidth,
            "shoulder" : self.shoulderWidth
            } 



        newLaneStart = 0.0
        
        for x in roadOrder: 
            y = meshiepoos[x]
            if y !=0.0:
                z = meshSetup.groundMesh(x, newLaneStart, newLaneStart + y)
                roadMeshes.append(z)
                if x != "lanes":
                    curveSetup.curveSetup (roadCurve, z, 1)       
                    newLaneStart+=y     
                else:
                    if (y > 1):  
                        curveSetup.lanesSetup(z, self.laneCount)  
                        curveSetup.curveSetup (roadCurve, z, 1)       
                        newLaneStart += y*self.laneCount

                materialSetup.mainMaterial(z)

        



    


        materialSetup.cyclesCheck()
        
                
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