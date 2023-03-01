import spacy
from nltk import Tree
import json
import data
import pandas as pd

def to_nltk_tree(node):
    if node.n_lefts + node.n_rights > 0:
        return Tree(node.orth_, [to_nltk_tree(child) for child in node.children])
    else:
        return node.orth_
def get_root_stats(questions):
    roots = pd.DataFrame([str([sent.root for sent in en_nlp(q).sents][0]) for q in questions])
    return roots.value_counts()

def get_root(question):
    root = str([sent.root for sent in en_nlp(question).sents][0])
    return root
def get_parse_tree(question):
    tree = [to_nltk_tree(sent.root).pretty_print() for sent in en_nlp(question).sents]

def sample_by_start_phrase(df, start_phrase):
    start_phrase_df = df.where(df['question'].apply(lambda x: x.startswith(start_phrase))).dropna()
    start_phrase_sample = start_phrase_df.sample(1)
    start_phrase_sample_question = start_phrase_sample['question'].tolist()[0]
    start_phrase_sample_program = start_phrase_sample['program'].tolist()[0]
    print(start_phrase_sample_question)
    get_parse_tree(start_phrase_sample_question)
    for term in start_phrase_sample_program:
        print(term)

if __name__ == "__main__":
    en_nlp = spacy.load('en_core_web_sm')
    # read questions from json to df
    questions_data = data.getQuestions('../datasets/CLEVR_sample_nscl/train/questions.json')
    questions_df = pd.DataFrame(questions_data)

    # what are the unique first words in questions
    first_words = questions_df['question'].apply(lambda x: x.split()[0])
    print("first words\n")
    print(first_words.value_counts())

    # make separate list for first word
    what_df = questions_df.where(questions_df['question'].apply(lambda x: x.split()[0] == "What")).dropna()
    what_questions = what_df['question']
    there_df = questions_df.where(questions_df['question'].apply(lambda x: x.split()[0] == "There")).dropna()
    there_questions = there_df['question']
    is_df = questions_df.where(questions_df['question'].apply(lambda x: x.split()[0] == "Is")).dropna()
    is_questions = is_df['question']
    how_df = questions_df.where(questions_df['question'].apply(lambda x: x.split()[0] == "How")).dropna()
    how_questions = how_df['question']
    are_df = questions_df.where(questions_df['question'].apply(lambda x: x.split()[0] == "Are")).dropna()
    are_questions = are_df['question']
    the_df = questions_df.where(questions_df['question'].apply(lambda x: x.split()[0] == "The")).dropna()
    the_questions = the_df['question']
    do_df = questions_df.where(questions_df['question'].apply(lambda x: x.split()[0] == "Do")).dropna()
    do_questions = do_df['question']
    does_df = questions_df.where(questions_df['question'].apply(lambda x: x.split()[0] == "Does")).dropna()
    does_questions = does_df['question']

    # what is the second word in each of the above categories? (see tokenizer.py comments for rules)
    what_questions_second_words = what_questions.apply(lambda x: x.split()[1])
    how_questions_second_words = how_questions.apply(lambda x: x.split()[1])
    are_questions_second_words = are_questions.apply(lambda x: x.split()[:3])
    the_questions_second_words = the_questions.apply(lambda x: x.split()[1])
    is_questions_second_words = is_questions.apply(lambda x: x.split()[1])
    there_questions_third_words = there_questions.apply(lambda x: x.split()[2])
    do_questions_third_words = do_questions.apply(lambda x: x.split()[2])
    does_questions_third_words = does_questions.apply(lambda x: x.split()[2])

    #print(does_questions_third_words.value_counts())
    #does_questions_test = [q.split()[:7] for q in does_questions if q.split()[3] not in ['that']]
    #print(does_questions_test)
    #print(len([q for q in there_questions if len([w for w in q if w.endswith(';')])]))
    #print(pd.DataFrame(does_questions_test).value_counts())
    #print([q for q in the_questions if q.split()[1] not in ['other', 'object', 'thing'] and q.split()[3] == ['that']])


    # what are the root words for each question type
    print("what questions root words")
    #print(len(what_questions))
    print(get_root_stats(what_questions))

    print("there questions root words")
    #print(len(there_questions))
    print(get_root_stats(there_questions))

    print("is questions root words")
    #print(len(is_questions))
    print(get_root_stats(is_questions))

    print("how questions root words")
    #print(len(how_questions))
    print(get_root_stats(how_questions))

    print("are questions root words")
    #print(len(are_questions))
    print(get_root_stats(are_questions))

    print("the questions root words")
    #print(len(the_questions))
    print(get_root_stats(the_questions))

    print("do questions root words")
    #print(len(do_questions))
    print(get_root_stats(do_questions))

    print("does questions root words")
    #print(len(does_questions))
    print(get_root_stats(does_questions))

    # analyze trees with root: "have"
    print("parse trees with root -- \"have\"")
    does_sample = does_questions.sample(1).tolist()[0]
    print(does_sample)
    get_parse_tree(does_sample)
    print("--------------------------------------------------------------------------")
    what_questions_root_have = what_questions.where(what_questions.apply(lambda x: get_root(x) == 'have')).dropna()
    what_questions_root_have_sample = what_questions_root_have.sample(1).tolist()[0]
    print(what_questions_root_have_sample)
    get_parse_tree(what_questions_root_have_sample)
    print("--------------------------------------------------------------------------")
    how_questions_root_have = how_questions.where(how_questions.apply(lambda x: get_root(x) == 'have')).dropna()
    print(get_root_stats(how_questions_root_have), len(how_questions_root_have))
    how_questions_root_have_sample = how_questions_root_have.sample(1).tolist()[0]
    print(how_questions_root_have_sample)
    get_parse_tree(how_questions_root_have_sample)
    print("--------------------------------------------------------------------------")
    there_questions_root_have = there_questions.where(there_questions.apply(lambda x: get_root(x) == 'have')).dropna()
    print(get_root_stats(there_questions_root_have), len(there_questions_root_have))
    there_questions_root_have_sample = there_questions_root_have.sample(1).tolist()[0]
    print(there_questions_root_have_sample)
    get_parse_tree(there_questions_root_have_sample)
    print("--------------------------------------------------------------------------")
    do_questions_root_have = do_questions.where(do_questions.apply(lambda x: get_root(x) == 'have')).dropna()
    print(get_root_stats(do_questions_root_have), len(do_questions_root_have))
    do_questions_root_have_sample = do_questions_root_have.sample(1).tolist()[0]
    print(do_questions_root_have_sample)
    get_parse_tree(do_questions_root_have_sample)
    print("--------------------------------------------------------------------------")

    """
    # analyze question parse trees and ground truth programs of questions starting with "Is there a"
    #[sample_by_start_phrase(is_df, "Is there a ") for i in range(5)]

    # analyze all Is roots
    roots = questions_df['question'].apply(get_root)
    questions_df['root'] = roots
    print(questions_df.where(questions_df['root'] in ['is', 'Is']))

    #print(len(is_roots))
    # what does an AST for a program expression look like?
    """
    """
    2 + 2
    {
        type: 'Program',
        body: [
        {
            type: 'ExpressionStatement',
            expression: {
                type: 'BinaryExpression', 'blue box'
                operator: '+', # plus() query()
                left: {
                    type: 'NumericLiteral', Color
                    value: 2,
                },
                right: {
                    type: 'NumericLiteral', 
                    value: 2,
                }, # plus(2, 2)
            }
        }
        ]
    }
    
    3 + 2 + 2 is still a binary expression because 3 + 2 = 5, then we have 5 + 2
    
    2 + 2 in our style is: plus(2, 2)
    operator "+" --> plus()
    numeric literals are inputs
    
    """

    """
    #for q in does_questions.sample(20):
    #    print(q)
    #    tree = [to_nltk_tree(sent.root).pretty_print() for sent in en_nlp(q).sents]

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
