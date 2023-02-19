
bl_info = {
    'name': 'Unity Exporter',
    'category': '3D View',
    'author': 'Hotox',
    'location': 'View 3D > Tool Shelf > FBX',
    'description': 'Correctly exports FBX files for Unity',
    'version': (1, 0, 0),
    'blender': (3, 4, 0),
}

first_startup = "bpy" not in locals()
import bpy
import sys

from . import operators
from . import panels
from . import utils

if not first_startup:
    import importlib
    importlib.reload(operators)
    importlib.reload(panels)
    importlib.reload(utils)


classes = [
    panels.MainPanel,
    operators.ExportButton,
]


def check_unsupported_blender_versions():
    version = (3, 4)
    version_str = ".".join([str(v) for v in version])

    # Don't allow older Blender versions
    if bpy.app.version < version:
        unregister()
        sys.tracebacklimit = 0
        raise ImportError(f'\n\nBlender versions older than {version_str} are not supported by this plugin. '
                          f'\nPlease use Blender {version_str}.'
                          '\n')


def register():
    print("\n#### Loading FBX Unity Exporter.. ####")

    # Check if Blender version is supported
    check_unsupported_blender_versions()

    # Load all classes
    for cls in classes:
        try:
            bpy.utils.register_class(cls)
        except:
            print("Failed to load", cls)

    print("#### Loaded FBX Unity Exporter ####\n")


def unregister():
    print("#### Unloading FBX Unity Exporter.. ####")

    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except:
            print("Failed to unload", cls)

    print("#### Unloaded FBX Unity Exporter ####")


if __name__ == '__main__':
    register()
