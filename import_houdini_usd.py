import hou

obj_level1 = hou.node('/obj')
geo_node = obj_level1.createNode('geo')
file_node = geo_node.createNode('usdimport')

path = 'C:/temp/test2.usd'

file_node.parm('file').set(path)