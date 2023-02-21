import json

def getScene(path_to_file):
    with open(path_to_file) as f:
        scenes = json.load(f)
    f.close()
    return scenes['scenes'] # list of scene dictionaries

def getQuestions(path_to_file):
    with open(path_to_file) as f:
        questions = json.load(f)
    f.close()
    return questions['questions'] # list of scene dictionaries

#getScene('../datasets/CLEVR_sample/scenes/CLEVR_train_scenes.json')

# def getImage():
    #pass

# dataloader