
import bpy

from . import operators as ops


# Initializes the main panel in the toolbar
class Panel(object):
    bl_label = 'FBX'
    bl_idname = 'VIEW3D_TS_fbx_unity_exporter'
    bl_category = 'FBX'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'


class MainPanel(Panel, bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_fbx_unity_exporter'
    bl_label = 'Unity Exporter'

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = False

        row = layout.row(align=True)
        row.scale_y = 1.5
        row.operator(ops.ExportButton.bl_idname)
