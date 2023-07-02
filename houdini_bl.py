bl_info = {
    "name": "Send to Houdini",
    "version": (1, 0),
    "blender": (3, 6, 0),
    "location": "View3D > Toolbar > Houdini",
    "description": "send objects to houidini",
    "category": "Houdini"
}

import bpy
import os.path
import subprocess


class SimplePanel(bpy.types.Panel):
    """This class defines a panel that appears in the Blender UI. It is responsible for displaying the Houdini menu in
    the 3D Viewport toolbar. The panel is defined with the following properties: """
    bl_idname = "OBJECT_PT_Houdini_Panel"
    bl_category = "Houdini"
    bl_label = "Houdini Menu"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        """
    The draw function is called every time Blender redraws the 3D view.
    It's where you put all your UI code. The layout variable is a reference to
    a special UI object that has methods for drawing all kinds of elements.

    :param self: Access the properties of the class
    :param context: Access the window manager,
    :return: A list of tuples, the first element in each tuple is a string
    :doc-author: Trelent
    """
        layout = self.layout
        layout.operator('object.send_houdini_fbx')
        layout.operator('object.update_fbx')


def show_popup_message(message, title="Error", icon='ERROR'):
    """This function displays a pop-up message in Blender. It takes three parameters:
    @param title: str
    @param icon: str
    @param message: Any

    """
    bpy.context.window_manager.popup_menu(
        lambda self, context: self.layout.label(text=message),
        title=title, icon=icon
    )


def check_file_saved():
    """This function checks if the current Blender file is saved. If the file is not saved, it displays a pop-up message
    and returns False; otherwise, it returns True."""
    if bpy.data.is_saved:
        return True
    else:
        show_popup_message("Blender file is not saved!")
        return False


class SendToHoudiniFBX(bpy.types.Operator):
    """This class defines an operator for exporting objects to Houdini in FBX format. It is responsible for exporting the
    selected objects as an FBX file and launching Houdini with a Python script for importing the FBX file. """
    bl_idname = 'object.send_houdini_fbx'
    bl_label = 'Send2Hou fbx'

    def execute(self, context):
        """
    The execute function is the main function of the operator. It is called when
    the operator runs, and must contain all the logic needed to perform its task.
    The execute function can access and modify scene data, as long as it restores
    the scene to its original state before finishing (see restrictions below). The
    execute function may also invoke other operators if needed.

    :param self: Refer to the class itself
    :param context: Access the scene data, and is used to determine what objects are selected
    :return: A set of status flags that indicate the success or failure of the operator
    :doc-author: Trelent
    """
        '''Retrieves the path of the current Blender file'''
        blend_filepath = bpy.data.filepath

        '''Determines the directory of the Blender file'''
        blend_dir = os.path.dirname(blend_filepath)

        '''Sets the export filepath for the FBX file by appending the filename with the extension ".fbx".'''
        export_filepath = os.path.join(blend_dir, bpy.path.display_name_from_filepath(blend_filepath) + ".fbx")

        print("FBX exported to:", export_filepath)
        '''Exports the selected objects to the FBX file using Blender's built-in export_scene.fbx operator.'''
        bpy.ops.export_scene.fbx(filepath=export_filepath)

        '''Specifies the path to the Houdini executable and the Python script for importing the FBX file.'''
        houdinipath = 'C:/Program Files/Side Effects Software/Houdini 19.5.631/bin/houdinifx.exe'
        '''Specifies the path to the Houdini executable and the Python script for importing the FBX file.'''
        houdiniscript = 'C:/temp/python_staging/import_houdini.py'
        cmd = [houdinipath, houdiniscript]
        '''Executes the Houdini subprocess with the specified command.'''
        subprocess.Popen(cmd)

        return {'FINISHED'}

    def invoke(self, context: object, event):
        """
    The invoke function is called when the operator is executed.
    It can be used to open a pop-up menu if the file is not saved, or to do some other checks before executing the operator.
    The invoke function must return either {'FINISHED'} or {'CANCELLED'}. If it returns {‘RUNNING_MODAL’}, then it will be called again with an event parameter.

    :param self: Refer to the class itself, and is used for
    :param context: object: Pass the context of the event to
    :param event: Check if the user has pressed a key
    :return: A dictionary
    :doc-author: Trelent
    """
        if not check_file_saved():
            return {'CANCELLED'}

        return self.execute(context)


class SendToHoudiniUSD(bpy.types.Operator):
    """This class defines an operator for exporting objects to Houdini in USD format. It is similar to the
    SendToHoudiniFBX class, but it exports objects to USD instead of FBX. The class has """
    bl_idname = 'object.send_houdini_usd'
    bl_label = 'Send2Hou usd'

    def execute(self, context):
        """
    The execute function is called when the operator is invoked.
    It takes a single argument, context, which contains information about the active object and scene.
    The execute function returns a set of status flags that indicate whether or not it was successful.

    :param self: Access the class attributes and methods
    :param context: Access the scene information
    :return: A set
    :doc-author: Trelent
    """
        blend_filepath = bpy.data.filepath
        blend_dir = os.path.dirname(blend_filepath)

        # Set the export filepath
        export_filepath = os.path.join(blend_dir, bpy.path.display_name_from_filepath(blend_filepath) + ".fbx")
        # Print the export filepath
        print("USD exported to:", export_filepath)
        # Export USD
        bpy.ops.wm.usd_export(filepath=export_filepath)

        houdinipath = 'C:/Program Files/Side Effects Software/Houdini 19.5.631/bin/houdinifx.exe'
        houdiniscript = 'C:/temp/python_staging/import_houdini.py'
        cmd = [houdinipath, houdiniscript]
        subprocess.Popen(cmd)
        return {'FINISHED'}

    def invoke(self, context, event):
        """The invoke method is also implemented to handle the operator invocation. It calls the check_file_saved
            function to ensure the Blender file is saved before executing the operator. """
        ''' Open a pop-up menu if the file is not saved'''
        if not check_file_saved():
            return {'CANCELLED'}
        return self.execute(context)


class UpdateFbx(bpy.types.Operator):
    """This class defines an operator for updating the exported FBX file. It exports the selected objects to the FBX
    file, similar to the SendToHoudiniFBX class. The class has the following properties: """
    bl_idname = 'object.update_fbx'
    bl_label = 'Update fbx'

    def execute(self, context):
        """
        The execute function is called when the operator is invoked. It takes a single argument, context, which is a
        dictionary containing information about the state of Blender at the time this operator was executed. The
        execute function should return a set of enum items in {‘CANCELLED’, ‘FINISHED’, ‘PASS_THROUGH’} to indicate
        how Blender should handle this operator.

        :param self: Access the class itself
        :param context: Access the scene data, active object and so on
        :return: A dictionary with a finished status
        :doc-author: Trelent
        """
        blend_filepath = bpy.data.filepath
        blend_dir = os.path.dirname(blend_filepath)
        export_filepath = os.path.join(blend_dir, bpy.path.display_name_from_filepath(blend_filepath) + ".fbx")
        print("FBX exported to:", export_filepath)
        # Export FBX
        bpy.ops.export_scene.fbx(filepath=export_filepath)

        return {'FINISHED'}


def register():
    """
    The register function is called when the script is loaded.
    It registers all classes defined in this script, so that Blender knows about them and can use them.


    :return: Nothing
    :doc-author: Trelent
    """

    bpy.utils.register_class(SimplePanel)
    bpy.utils.register_class(SendToHoudiniFBX)
    bpy.utils.register_class(UpdateFbx)


def unregister():
    """
    The unregister function is called when the add-on is disabled.
    It removes all classes and functions that were registered in register().

    :return: A list of classes that were registered
    :doc-author: Trelent
    """

    bpy.utils.unregister_class(SimplePanel)
    bpy.utils.unregister_class(SendToHoudiniFBX)
    bpy.utils.unregister_class(UpdateFbx)


if __name__ == "__main__":
    '''The add-on is registered by calling the register function if the Python script is directly executed.'''
    register()

'''Note: This documentation provides an overview of the code structure and functionality. For more detailed 
explanations, refer to the code comments and the Blender API documentation. '''
