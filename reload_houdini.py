import hou

# path = 'C:/temp/Cube.fbx'
bl_file_node = hou.node('/obj/geo1/file1')
# bl_file_node.parm('file').set(path)
bl_file_node.parm('reload').pressButton()