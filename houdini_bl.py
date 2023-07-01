bl_info = {
    "name": "Send to Houdini",
    "version": (1, 0),
    "blender": (3, 6, 0),
    "location": "View3D > Toolbar > Houdini",
    "description": "sending objects to houidini",
    "catagory": "Houdini"
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
        """The draw method of this class is called to draw the panel and add operators to it."""
        layout = self.layout
        layout.operator('object.send_houdini_fbx')
        layout.operator('object.update_fbx')


def show_popup_message(message, title="Error", icon='ERROR'):
    """This function displays a pop-up message in Blender. It takes three parameters:"""
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
        '''The class provides the execute method, which is called when the operator is invoked. It performs the following
         steps:'''

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

    def invoke(self, context, event):
        '''The invoke method is also implemented to handle the operator invocation. It calls the check_file_saved
            function to ensure the Blender file is saved before executing the operator. '''
        '''Open a pop-up menu if the file is not saved'''
        if not check_file_saved():
            return {'CANCELLED'}

        return self.execute(context)


class SendToHoudiniUSD(bpy.types.Operator):
    '''This class defines an operator for exporting objects to Houdini in USD format. It is similar to the
    SendToHoudiniFBX class, but it exports objects to USD instead of FBX. The class has '''
    bl_idname = 'object.send_houdini_usd'
    bl_label = 'Send2Hou usd'

    def execute(self, context):
        # usdpath = 'C:/temp/test.usd'

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
        '''The invoke method is also implemented to handle the operator invocation. It calls the check_file_saved
            function to ensure the Blender file is saved before executing the operator. '''
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
        """The execute method of this class performs the following steps:
            Retrieves the path of the current Blender file.
            Determines the directory of the Blender file.
            Sets the export filepath for the FBX file by appending the filename with the extension ".fbx".
            Prints the export filepath to the console.
            Exports the selected objects to the FBX file using Blender's built-in export_scene.fbx operator."""
        blend_filepath = bpy.data.filepath
        blend_dir = os.path.dirname(blend_filepath)
        export_filepath = os.path.join(blend_dir, bpy.path.display_name_from_filepath(blend_filepath) + ".fbx")
        print("FBX exported to:", export_filepath)
        # Export FBX
        bpy.ops.export_scene.fbx(filepath=export_filepath)

        return {'FINISHED'}


def register():
    """These functions are used to register and unregister the add-on's classes. The register function calls
    bpy.utils.register_class for each class defined in the add-on, while the unregister function calls
    bpy.utils.unregister_class for each class. """
    bpy.utils.register_class(SimplePanel)
    bpy.utils.register_class(SendToHoudiniFBX)
    bpy.utils.register_class(UpdateFbx)


def unregister():
    bpy.utils.unregister_class(SimplePanel)
    bpy.utils.unregister_class(SendToHoudiniFBX)
    bpy.utils.unregister_class(UpdateFbx)


if __name__ == "__main__":
    '''The add-on is registered by calling the register function if the Python script is directly executed.'''
    register()

'''Note: This documentation provides an overview of the code structure and functionality. For more detailed 
explanations, refer to the code comments and the Blender API documentation. '''
