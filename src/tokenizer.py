#https://www.youtube.com/watch?v=0ZDPvdp2uFk&list=PLGNbPb3dQJ_5FTPfFIg28UxuMpu7k0eT4&index=2
# stopped working on rdp and this file at 10:49pm 2/18
# need to figure out how a symbolic parser would work
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
        current_string = self._string[self._position:] # return rest of the string startng at position
        print(current_string)

        # boolean
        # "true

        # make a call in parser to capture token values into the AST
        # types of tokens we might have
        # colors: 8
        # shapes: sphere (ball), cube (block), cylinder
        # size: small (tiny), large (big)
        # material: metal (metallic, shiny), rubber (matte)
        # relations: left (left of, to the left of, on the left side), right (right of, to the right of, on the right side of), behind, front (in front of), above



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

import data
import pandas as pd

questions_data = data.getQuestions('../datasets/CLEVR_sample_nscl/train/questions.json')
questions_df = pd.DataFrame(questions_data)
unique_tokens = set()
questions_df['question'].str.split().apply(unique_tokens.update)

print(questions_df.head())
print(unique_tokens)


