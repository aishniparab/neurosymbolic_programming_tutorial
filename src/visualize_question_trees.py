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


def what_condition(x):
    if x.split()[0] == "What":
        return x

def there_condition(x):
    if x.split()[0] == "There":
        return x

def is_condition(x):
    if x.split()[0] == "Is":
        return x

def how_condition(x):
    if x.split()[0] == "How":
        return x

def are_condition(x):
    if x.split()[0] == "Are":
        return x

def the_condition(x):
    if x.split()[0] == "The":
        return x

def do_condition(x):
    if x.split()[0] == "Do":
        return x

def does_condition(x):
    if x.split()[0] == "Does":
        return x

if __name__ == "__main__":
    questions_data = data.getQuestions('../datasets/CLEVR_sample_nscl/val/questions.json')
    questions_df = pd.DataFrame(questions_data)
    first_words = questions_df['question'].apply(lambda x: x.split()[0])

    what_questions = questions_df['question'].apply(what_condition).dropna()
    there_questions = questions_df['question'].apply(there_condition).dropna()
    is_questions = questions_df['question'].apply(is_condition).dropna()
    how_questions = questions_df['question'].apply(how_condition).dropna()
    are_questions = questions_df['question'].apply(are_condition).dropna()
    the_questions = questions_df['question'].apply(the_condition).dropna()
    do_questions = questions_df['question'].apply(do_condition).dropna()
    does_questions = questions_df['question'].apply(does_condition).dropna()

    en_nlp = spacy.load('en_core_web_sm')

    what_questions_second_words = what_questions.apply(lambda x: x.split()[1])
    how_questions_second_words = how_questions.apply(lambda x: x.split()[1])
    are_questions_second_words = are_questions.apply(lambda x: x.split()[:3])
    the_questions_second_words = the_questions.apply(lambda x: x.split()[1])
    #print(what_questions_second_words.value_counts())
    #print(how_questions_second_words.value_counts())
    #print(are_questions_second_words.value_counts())
    print(the_questions_second_words.value_counts())

    are_there_the_questions = [q for q in are_questions if q.split()[:3] == ['Are', 'there', 'the']]

    are_the_questions = [q.split()[3] for q in are_questions if q.split()[:3] == ['Are', 'the']]

    the_attr_questions = [q.split()[2] for q in the_questions if q.split()[3] not in ['object', 'thing']]

    print(the_attr_questions)
    print(pd.DataFrame(the_attr_questions).value_counts())

    """
    for q in what_questions.sample(20):
        print(q)
        tree = [to_nltk_tree(sent.root).pretty_print() for sent in en_nlp(q).sents]
    """