# recursive descent parser
# https://www.youtube.com/watch?v=0ZDPvdp2uFk&list=PLGNbPb3dQJ_5FTPfFIg28UxuMpu7k0eT4&index=2

import dsl
import tokenizer


class Parser:
    """
    Parses a program into an AST in json format
    Ideally I want to parse question string into AST
    """

    def __init__(self):
        self._string = ''
        self._lookahead = ''
        self._tokenizer = None

    def boolean(self):
        return {
            'type': 'Boolean',
            'value': dsl.Boolean(self._string)  # convert string to Boolean type
        }

    def clevrobject(self):
        # obj = dsl.ClevrObject()
        # attr = self._string
        # attribute_name = dsl.ClevrObject.get_attr(attr)
        # obj.set_attr(attribute_name, self._string)
        # return {
        #   'type': 'ClevrObject',
        #   'value': obj
        # }
        pass

    def color(self):
        token = self._eat('Color')
        return {
            'type': 'Color',
            'value': dsl.Color(token['value'])
        }

    def size(self):
        token = self._eat('Size')
        return {
            'type': 'Size',
            'value': dsl.Size(token['value'])
        }

    def material(self):
        token = self._eat('Material')
        return {
            'type': 'Material',
            'value': dsl.Material(token['value'])
        }

    def shape(self):
        token = self._eat('Shape')
        return {
            'type': 'Shape',
            'value': dsl.Shape(token['value'])
        }

    def relation(self):
        token = self._eat('Relation')
        return {
            'type': 'Relation',
            'value': dsl.Relation(token['value'])
        }

    def literal(self):
        if self._lookahead['type'] == 'Color':
            return self.color()
        elif self._lookahead['type'] == 'Size':
            return self.size()
        elif self._lookahead['type'] == 'Material':
            return self.material()
        elif self._lookahead['type'] == 'Shape':
            return self.shape()
        elif self._lookahead['type'] == 'Relation':
            return self.relation()
        else:
            return "Unexpected Literal"

    def _eat(self, token_type): # should handle None case
        token = self._lookahead
        if not token: # end of the string
            raise "Unexpected end of input, expected: "+str(token_type)
        elif token['type'] != token_type:
            raise "Unexpected token: "+str(token['value'])+", expected: "+str(token_type)
        else:
            self._lookahead = self._tokenizer.get_next_token()
            return token

    def parse(self, input_string):
        """
        parse recursively from the main entry point, the scene
        :param input_string:
        :return: scene
        """
        self._string = input_string
        self._tokenizer = tokenizer.Tokenizer(input_string) # init pointer at start
        self._lookahead = self._tokenizer.get_next_token() # used for predictive parsing
        return self.program()

    # main entry point of rdp
    # starts from the starting symbol and goes recursively down (top-down)
    # entry point:
    # Scene:
    #   : Boolean | Integer | Object | ObjectSet | Relation
    #   ;
    #
    def program(self): # aka scene?
        """
        :return: AST dictionary
        """
        return {
            'type': 'Scene',
            'body': self.literal()
        }

