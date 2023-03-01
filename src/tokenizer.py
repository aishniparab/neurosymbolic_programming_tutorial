# https://www.youtube.com/watch?v=0ZDPvdp2uFk&list=PLGNbPb3dQJ_5FTPfFIg28UxuMpu7k0eT4&index=2
# stopped working on rdp and this file at 1:30 pm 2/24
# going through questions in the dataset to identify patterns manually in visualize_question_trees.py and adding comments here in rules
# spacy has a library to parse sentence into a tree; can use that to map to AST
# for neural one see nsvqa https://github.com/kexinyi/ns-vqa; https://github.com/nerdimite/neuro-symbolic-ai-soc/blob/master/semantic_parser.py

# purpose of tokenizer is to extract a stream of token with some type and value

# set of rules, values are regex expressions
import re

color_rule = re.compile('(blue|green|red|yellow|cyan|brown|purple|gray)')
size_rule = re.compile('(large|big|small|tiny)')
shape_rule = re.compile('(cube|sphere|box|cylinder|ball|block)')
material_rule = re.compile('(matte|rubber|metallic|shiny)')
relation_rule = re.compile('(front|\b[in front of]\b|behind|right|\b[right of]\b|\b[to the right of]\b|\b[on the '
                           'right side of]\b|left|\b[left of]\b|\b[to the left side]\b|\b[on the right side '
                           'of]\b|above|below)')
whitespace_rule = re.compile('\s')

# operator rules
exists_rule = re.compile('(\b[Is there a]\b)') # |\b[Are any]|)')
#unique_rule = re.compile('\b[the (adjective) object]')

"""
what_questions = {
    'what number': count(objset??),
    'what is': query(??),
    'what material': query_material(obj??),
    'what color': query_color(obj??),
    'what shape': query_shape(obj??),
    'what size': query_size(obj??)
} #roots: is, are, have, made, left

how_questions = {
    'how many' : count(objset??),
    'how big' : query_size(obj??) # check for "how small" and other possibilities
} roots: are, have, is, made, left, spheres, objects

are_questions = {
    'are there the same number': ,
    'are any': exist(filter_attr(),
    'are the <attr>':,
    'are the object <rel>': # where <rel> is 'in front of', 'left of', 'that is in front of', 'that is left of', 'behind the' 
} # roots: are

the_questions = {
    'the object/thing that is <rel> <obj with attr> is made of/of what <attr>': ,
    'the object/thing that is the same <attr> as the <obj with attr> is what <attr>':  
    'the object/thing that is both <rel/attr> and/or <rel/attr>' has what/is what <attr>': 
    'the object/thing <rel> obj has what/is what <attr>': , 
    'the <obj/attr> that is (the same) <rel> has what/is what <attr>': ,
    'the other <attr> is what <attr> that is (made of) the same <attr> as <obj with attr> is what <attr>': 
} # roots: is, has, made, object, thing, cylinder, sphere, block, ball, cube, left

is_questions = {
    'is the number of (<attr>) things/balls/objs that are <attr>/<rel> of <obj> <less/greater/same> as the number of <objs attr>
    'is the <attr>/<attr name>':,
    'is there a <obj>?':
    'is there a <obj> that has/that is <rel>/made of/the same <attr> as <obj>':
    'is there a object (made of <attr>, made of the same <attr>, of the same <attr> as, <rel>) <obj>':
    'is there any other thing (of, that has/is) (made of/the same) <attr> as the <obj attr>'
    'is there anything else (of, that has/is) (the same/made of) <attr> as the <obj attr>':
    'is there another object/<attr> that has the same <attr> as the <attr> thing':
} # roots: Is

there_questions = {
    'there is a (object <rel> object)/(<attr> that/thing is <rel>/same as <obj>); recurse question: 
    'there is another <attr obj> that is/made of the same <attr> as the <obj>; recurse question: 
} # roots: is, are, have, made, left

do_questions = {
    'do the <obj/attr> (thing) (and <obj/attr> thing) that/<rel> is/the <rel>/<obj> have the same <attr>': 
} # roots: have, Do, right, left

does_questions = {
    'does the <obj/attr> (thing) <rel> <obj/attr> *have* the same attr as <obj/attr>:?
} # roots: have 
"""

spec = {
    'Space': whitespace_rule,
    'Color': color_rule,
    'Size': size_rule,
    'Shape': shape_rule,
    'Material': material_rule,
    'Relation': relation_rule,
    # operator rules
    'Exists': exists_rule
}
class Tokenizer:
    def __init__(self, input_string):
        self._string = input_string
        self._position = 0  # track position of each character; characters are grouped into tokens

    def has_more_tokens(self):
        """
        True if position has not reached at the end of the string, False otherwise
        :return: bool
        """
        return self._position < len(self._string)

    def _match(self, regexp, input_string):
        matched = re.search(regexp, input_string)
        if matched is None:
            return None
        else:
            self._position += len(matched.group())
            return matched.group()

    def get_next_token(self):
        """
        Obtains next token. Called from the parser
        :return: token type.. ?
        """
        if not self.has_more_tokens():
            return None

        # recognize tokens
        current_string = self._string[self._position:] # return rest of the string starting at position

        for token_type, regexp in spec.items():
            token_value = self._match(regexp, current_string)
            if token_value is None:
                continue
            # skip whitespace tokens
            if token_type == 'Space':
                return self.get_next_token()
            else:
                return {
                    'type': token_type,
                    'value': token_value
                }

        raise SyntaxError("Unexpected Token: {}".format(current_string[0]))