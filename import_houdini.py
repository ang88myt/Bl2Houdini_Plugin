import hou

obj_level1 = hou.node('/obj')
geo_node = obj_level1.createNode('geo')
file_node = geo_node.createNode('file')
scale_factor = 0.01

path = 'C:/temp/Cube.fbx'
geo_node.parm('scale').set(scale_factor)
file_node.parm('file').set(path)



