"""
stopped working 02/21/2023 1:15pm
#need clevrobj dsl to init obj without having all the details about the obj
"""

import recursive_descent_parser as rdp

# parser
Parser = rdp.Parser()
program = 'What is the shape of the blue object?'
scene_graph
# {'type': query_shape, value: {type: filter, value: {'type': Color, value: Blue}}} ===> query_shape((filter(blue)) ==> "shape"
# [query_shape(), filter(), blue]

#program = 'block is blue'
#program = 'object is shiny'
#program = 'behind'
ast = Parser.parse(program)
print(ast)
print(ast['body']['value'].value)

""" 
# boolean type
program1 = 'true'
ast = Parser.parse(program1)
print(ast)
print(ast['body']['value'].value == 'yes')
program2 = 'false'
ast = Parser.parse(program2)
print(ast)
print(ast['body']['value'].value == 'no')
"""