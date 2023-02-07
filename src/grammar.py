"""
manually define the grammar here later
"""

import json

def getGrammar(path_to_file):
    """
    :param path_to_file: path to metadata.json in clevr-dataset-gen-main
    :return: dict: grammar with functions and types
    """
    with open(path_to_file) as f:
        metadata = json.load(f)
    f.close()

    # get types
    types = metadata['types']

    # add types to the grammar
    grammar = {k: {'name': k, 'values': v, 'inputs': None, 'outputs': None, 'terminal': None, 'type': 'primitive'} for
               k, v in types.items()}

    grammar['Integer']['values'] = [i for i in range(11)]
    grammar['Bool']['values'] = [True, False]

    # parse by function name
    functions_by_name = {}
    for f in metadata['functions']:
        functions_by_name[f['name']] = f
    metadata['_functions_by_name'] = functions_by_name
    functions = metadata['_functions_by_name']

    # add type information to functions
    for k, v in functions.items():
        v.update({'type': 'function'})

    # add functions to the grammar
    grammar.update(functions)

    return grammar

def getSynonyms(path_to_file):
    """
    :param path_to_file: path to synonyms.json in clevr-dataset-gen-main
    :return: dict: keys are words and values are a list of corresponding synonyms
    """
    with open('datasets/clevr-dataset-gen-main/question_generation/synonyms.json') as f:
        synonyms = json.load(f)
    f.close()

    return synonyms


