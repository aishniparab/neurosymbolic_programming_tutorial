#https://www.youtube.com/watch?v=0ZDPvdp2uFk&list=PLGNbPb3dQJ_5FTPfFIg28UxuMpu7k0eT4&index=2
# stopped working on rdp and this file at 11:14pm 2/22
# implemented single tokens for attributes
# need to figure out how to parse a sentence like "blue ball"
# then need to add more semantics to the sentence like "what is the size of the blue ball"
# for neural one see nsvqa https://github.com/kexinyi/ns-vqa; https://github.com/nerdimite/neuro-symbolic-ai-soc/blob/master/semantic_parser.py

# purpose of tokenizer is to extract a stream of token with some type and value

class Tokenizer:
    def __init__(self, input_string):
        self._string = input_string
        self._position = 0 # track position of each character; characters are grouped into tokens

    def has_more_tokens(self):
        """
        True if position has not reached at the end of the string, False otherwise
        :return: bool
        """
        return self._position < len(self._string)

    def get_next_token(self):
        """
        Obtains next token. Called from the parser
        :return: token type.. ?
        """
        if not self.has_more_tokens():
            return None

        # recognize tokens
        current_string = self._string[self._position:] # return rest of the string starting at position

        # recognize colors
        if current_string[0:3] in ['blu', 'red', 'gre', 'yel', 'cya', 'pur', 'gra', 'bro']:
            color = ''
            # consume token
            while current_string[self._position] != ' ':
                color += current_string[self._position]
                self._position += 1
            return {
                'type': 'Color',
                'value': color
            }

        # recognize sizes
        if current_string[0:3] in ['lar', 'big', 'sma', 'tin']:
            size = ''
            while current_string[self._position] != ' ':
                size += current_string[self._position]
                self._position += 1
            return {
                'type': 'Size',
                'value': size
            }

        # recognize materials
        if current_string[0:3] in ['mat', 'rub', 'met', 'shi']:
            material = ''
            while current_string[self._position] != ' ':
                material += current_string[self._position]
                self._position += 1
            return {
                'type': 'Material',
                'value': material
            }

        # recognize shapes
        if current_string[0:3] in ['cub', 'sph', 'blo', 'cyl', 'bal']:
            shape = ''
            while current_string[self._position] != ' ':
                shape += current_string[self._position]
                self._position += 1
            return {
                'type': 'Shape',
                'value': shape
            }

        # recognize relations
        if current_string[0:4] in ['fron', 'behi', 'righ', 'left', 'abov', 'belo', 'to t', 'on t', 'in f']:
            relation = ''
            # skip position to relation for special cases
            if current_string[0:6] in ['to the', 'on the']: # to the <rel> of, on the <rel> of, in front of cases
                self._position += len('to the ')
            elif current_string[0:6] in ['in fro']: # in front of case
                self._position += len('in ')

            while current_string[self._position] != ' ': # parse atomic relation: left, right, front, behind, above, below
                relation += current_string[self._position]
                self._position += 1

            # move position forward for special cases
            if current_string[0:6] in ['to the', 'on the', 'in fro']: # to the <rel> of, on the <rel> of, in front of cases
                self._position += len('of ')
            if current_string[self._position+1:self._position+2] == ['of']: # right of, left of case
                self._postion += len('of ')
            return {
                'type': 'Relation',
                'value': relation
            }

# playing around below to check vocabulary statistics of the questions
#tokenizer = Tokenizer("What is the size of the blue ball?")
#tokenizer.get_next_token()

### doing some checks here to see what kinds of tokens we need to eat

#from spacy.tokenizer import Tokenizer
#from spacy.lang.en import English

#nlp = English()

# Create a blank Tokenizer with just the English vocab
#tokenizer = Tokenizer(nlp.vocab)
#tokens = tokenizer("What is the size of the blue ball?")
#print(tokens)
#for token in tokens:
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

