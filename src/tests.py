"""
stopped working 02/21/2023 1:15pm
need clevrobj dsl to init obj without having all the details about the obj
"""

import recursive_descent_parser as rdp

# parser
Parser = rdp.Parser()
program = 'blue'
ast = Parser.parse(program)
print(ast)

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