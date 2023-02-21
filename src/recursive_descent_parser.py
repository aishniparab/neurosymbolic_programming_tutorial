# recursive descent parser
# https://www.youtube.com/watch?v=0ZDPvdp2uFk&list=PLGNbPb3dQJ_5FTPfFIg28UxuMpu7k0eT4&index=2

import dsl


class Parser:
    """
    Parses a program into an AST in json format
    Ideally I want to parse question string into AST
    """

    def __init__(self):
        self._string = None

    def boolean(self):
        return {
            'type': 'Boolean',
            'value': dsl.Boolean(self._string)  # convert string to Boolean type
        }

    def clevrobject(self):
        obj = dsl.ClevrObject()
        attribute_name = dsl.ClevrObject.get_attr(self._string)
        obj.set_attr(attribute_name, self._string)

        return {
            'type': 'ClevrObject',
            'value': obj
        }

    def parse(self, input_string):
        """
        parse recursively from the main entry point, the scene
        :param input_string:
        :return: scene
        """

        self._string = input_string
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
            'body': self.clevrobject() #self.boolean()
        }
