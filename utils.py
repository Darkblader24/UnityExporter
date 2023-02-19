
import bpy


def set_active(obj, select=False, deselect_others=False):
    if deselect_others:
        bpy.ops.object.select_all(action='DESELECT')
    if select:
        set_select(obj, True)
    bpy.context.view_layer.objects.active = obj


def get_active():
    return bpy.context.view_layer.objects.active


def set_select(obj, select):
    obj.select_set(select)


def get_selected_collection(context) -> bpy.types.Collection:
    # Get an active outliner area
    outliner_area = None
    for area in bpy.context.screen.areas:
        if area.type == 'OUTLINER':
            outliner_area = area
            break

    # Only return the collection if it is active AND selected in the outliner
    active_collection = None
    with context.temp_override(area=outliner_area):
        selected_collections = [c for c in context.selected_ids if c.bl_rna.identifier == "Collection"]
        if context.collection in selected_collections:
            active_collection = context.collection

    return active_collection


def create_sockets(group, inputs, outputs):
    # Check first sockets, they MUST always be a geometry node
    input_first = None
    for socket in group.inputs:
        input_first = socket
        break
    if not input_first or not input_first.bl_socket_idname == "NodeSocketGeometry":
        group.inputs.clear()

    output_first = None
    for socket in group.outputs:
        output_first = socket
        break
    if not output_first or not output_first.bl_socket_idname == "NodeSocketGeometry":
        group.outputs.clear()

    # Remove invalid sockets and remove found sockets from their list if they were found
    for socket in group.inputs:
        remove = True
        for target_socket in reversed(inputs):
            if socket.name == target_socket[1] and socket.bl_socket_idname == target_socket[0]:
                remove = False
                inputs.remove(target_socket)
                break
        if remove:
            group.inputs.remove(socket)

    for socket in group.outputs:
        remove = True
        for target_socket in reversed(outputs):
            if socket.name == target_socket[1] and socket.bl_socket_idname == target_socket[0]:
                remove = False
                outputs.remove(target_socket)
                break
        if remove:
            group.outputs.remove(socket)

    # Add back missing and not-found sockets
    for socket in inputs:
        group.inputs.new(socket[0], socket[1])
    for socket in outputs:
        group.outputs.new(socket[0], socket[1])




