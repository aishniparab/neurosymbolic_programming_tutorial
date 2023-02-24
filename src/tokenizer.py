# https://www.youtube.com/watch?v=0ZDPvdp2uFk&list=PLGNbPb3dQJ_5FTPfFIg28UxuMpu7k0eT4&index=2
# stopped working on rdp and this file at 10:52pm 2/23
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

"""
what_questions = {
    'what number': count(objset??),
    'what is': query(??),
    'what material': query_material(obj??),
    'what color': query_color(obj??),
    'what shape': query_shape(obj??),
    'what size': query_size(obj??)
}

how_questions = {
    'how many' : count(objset??),
    'how big' : query_size(obj??)
}

are_questions = {
    'are there the same number': ,
    'are any': exist(filter_attr(),
    'are the <attr>':,
    'are the object <rel>': # where <rel> is 'in front of', 'left of', 'that is in front of', 'that is left of', 'behind the' 
}

the_questions = {
    'the object/thing': ,
    'the <attr>': ,
    'the other': 
}
"""
# There questions
# Is questions
# How questions
# Are questions
# The questions
# Do questions
# Does questions

spec = {
    'Space': whitespace_rule,
    'Color': color_rule,
    'Size': size_rule,
    'Shape': shape_rule,
    'Material': material_rule,
    'Relation': relation_rule
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


# playing around below to check vocabulary statistics of the questions
# tokenizer = Tokenizer("What is the size of the blue ball?")
# tokenizer.get_next_token()

### doing some checks here to see what kinds of tokens we need to eat

# from spacy.tokenizer import Tokenizer
# from spacy.lang.en import English

# nlp = English()

# Create a blank Tokenizer with just the English vocab
# tokenizer = Tokenizer(nlp.vocab)
# tokens = tokenizer("What is the size of the blue ball?")
# print(tokens)
# for token in tokens:
#    if token == "size":
"""
import data
import pandas as pd

questions_data = data.getQuestions('../datasets/CLEVR_sample_nscl/train/questions.json')
questions_df = pd.DataFrame(questions_data)
unique_tokens = set()
questions_df['question'].str.split().apply(unique_tokens.update)

print(questions_df.head())
print(unique_tokens)
"""
