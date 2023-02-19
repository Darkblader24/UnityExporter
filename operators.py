import math
import pathlib

import bpy
from bpy_extras.io_utils import ImportHelper
from . import utils


class ExportButton(bpy.types.Operator, ImportHelper):
    bl_idname = "fbx_unity.export"
    bl_label = "Export as FBX"
    bl_description = "Exports the currently active collection as an FBX file for Unity"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def execute(self, context):
        rotations = {}

        # Correctly setup rotations for export to Unity
        for obj in context.collection.all_objects:
            if obj.parent:
                continue

            utils.set_active(obj, select=True, deselect_others=True)
            rotations[obj] = obj.rotation_euler[0]
            obj.rotation_euler[0] += math.radians(-90)
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
            obj.rotation_euler[0] += math.radians(90)

        # Export the file
        path = pathlib.Path(self.filepath)
        path = path.parent / (path.stem + '.fbx')
        bpy.ops.export_scene.fbx('EXEC_DEFAULT',
                                 filepath=str(path),
                                 use_active_collection=True,
                                 path_mode="COPY",
                                 embed_textures=True,
                                 bake_anim=False,
                                 apply_scale_options='FBX_SCALE_UNITS',
                                 )

        # Rotate the objects back
        for obj, rotation in rotations.items():
            # obj.rotation_euler[0] += math.radians(90)
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
            obj.rotation_euler[0] = -rotation
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
            obj.rotation_euler[0] = rotation

        self.report({'INFO'}, f'Exported to {path}')
        return {'FINISHED'}

