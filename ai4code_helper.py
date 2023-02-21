# questions as programs and searching over them in clevr
# https://github.com/facebookresearch/clevr-dataset-gen

# reading clevr data from json

train_length = 30000
training_data = {}
with open('datasets/CLEVR_v1.0/questions/CLEVR_train_questions.json') as f:
    data = json.load(f)
    for K in range(train_length):
        i = data['questions'][K]
        temp={}
        #for path in glob.glob('/datasets/clevr-dataset/CLEVR_v1.0/images/train/'+i['image_filename']): 
        #    temp['path'] = path
        temp['image_index'] = i['image_index']
        temp['program'] = i['program']
        temp['question'] = i['question']
        temp['answer'] = i['answer']
        training_data[K] = temp
f.close()
train_df = pd.DataFrame.from_dict(training_data, orient='index')
train_df.to_csv('datasets/clevr_train.csv')
del(data)
del(training_data)

val_length = 5000
val_data = {}
with open('datasets/CLEVR_v1.0/questions/CLEVR_val_questions.json') as f:
    data = json.load(f)
    for K in range(val_length):
        i = data['questions'][K]
        #for path in glob.glob('/datasets/clevr-dataset/CLEVR_v1.0/images/train/'+i['image_filename']): 
        #    temp['path'] = path
        temp['image_index'] = i['image_index']
        temp['program'] = i['program']
        temp['question'] = i['question']
        temp['answer'] = i['answer']
        val_data[K] = temp
f.close()
val_df = pd.DataFrame.from_dict(val_data, orient='index')
val_df.to_csv('datasets/clevr_val.csv')
del(data)
del(val_data)

train_df = pd.read_csv('datasets/clevr_train.csv', index_col=0)
train_df['image_index'] = train_df.index
val_df = pd.read_csv('datasets/clevr_val.csv', index_col=0)
val_df['image_index'] = val_df.index



# CLEVR DSL
class CLEVR_OBJECT():
    def __init__(self):
      self.attribute = self.attribute = {  
        'size' : ["small", "large"],
        'color' : ["gray", "red", "blue", "green", "brown", "purple", "cyan", "yellow"],
        'shape' : ["cube", "sphere", "cylinder"],
        'material' : ["rubber", "metal"]
      }
      self.position
    def get_attr(self, x):
      return [k for k, v in self.attribute.items() if x in v][0]

class CLEVR_DSL():
  def __init__(self):
    self.obj = CLEVR_OBJECT()
    self.integer = [{str(i)} for i in range(11)]
    self.relation = ["left", "right", "behind", "front"]
    self.str2func = {'count': self.count}
  
  def query(self, obj, attr):
    i = obj.index[0]
    return obj[attr][i]

  def count(self, objects):
    return len(objects)
  
  #def relate(self, object, relation):

class ProgramExecutor(CLEVR_DSL):
  def __init__(self):
    super().__init__()
    pass
  
  def execute(self, function, params, output):
    output = self.str2func[function](output)
    return output

  def __call__(self, scene, program):
    self.scene = scene
    output = None
    for seq in program:
      args = seq.split()
      prev_out = self.execute(args[0], args[1], output)
    return output

# count number of parameters
num_params = 1
for k, v in metadata['_functions_by_name'].items():
  #print(v['inputs'], len(v['inputs']))
  if (len(v['inputs']) > 0):
    num_params = num_params * len(v['inputs'])
print(len(grammar.keys()), "functions and ", num_params, "possible input permutations!")


# sampling questions
# num of val = num of test
# num of train/num of val = 4.6667
# chose 3000/4.667 = 642 for val and test
# did the following in terminal shell python3

train_files = os.listdir('train/')
train_files_dict = {f.split('_')[-1].split('.')[0]: f for f in train_files}
idx = [f.split('_')[-1].split('.')[0] for f in train_files]
random_idx = random.sample(idx, 3000)
train_sample = [train_files_dict[i] for i in random_idx]
srcpath = os.getcwd()+'/train/'
dstpath = '/Users/aishni/universe/nsym/tutorials/neurosymbolic_programming_tutorial/datasets/CLEVR_sample/images/train/'
[shutil.copyfile(srcpath+f, dstpath+f) for f in train_sample]

test_files = os.listdir('test/')
test_files_dict = {f.split('_')[-1].split('.')[0]: f for f in test_files}
idx_test = [f.split('_')[-1].split('.')[0] for f in test_files]
random_idx_test = random.sample(idx_test, 642)
test_sample = [test_files_dict[i] for i in random_idx_test]
srcpath = os.getcwd()+'/test/'
dstpath = '/Users/aishni/universe/nsym/tutorials/neurosymbolic_programming_tutorial/datasets/CLEVR_sample/images/test/'
[shutil.copyfile(srcpath+f, dstpath+f) for f in test_sample]

val_files_dict = {f.split('_')[-1].split('.')[0]: f for f in val_files}
idx_val = [f.split('_')[-1].split('.')[0] for f in val_files]
random_idx_val = random.sample(idx_val, 642)
val_sample = [val_files_dict[i] for i in random_idx_val]
srcpath = os.getcwd()+'/val/'
dstpath = '/Users/aishni/universe/nsym/tutorials/neurosymbolic_programming_tutorial/datasets/CLEVR_sample/images/val/'
[shutil.copyfile(srcpath+f, dstpath+f) for f in val_sample]

dstpath = '/Users/aishni/universe/nsym/tutorials/neurosymbolic_programming_tutorial/datasets/CLEVR_sample/questions/'

with open('../questions/CLEVR_val_questions.json') as f:
...     val_questions = json.load(f)
"""
val_question_all = {q['image_filename']: q  for q in val_questions['questions']}
val_question_sample = {f: val_question_all[f] for f in val_sample}
val_question_sample_reformat = [val for fname, val in val_question_sample.items()]
val_question_sample_out = {'info': "02/02/2022 uniformly sampled 642 questions", 'questions': val_question_sample_reformat}
"""
# prev method wrong because each image has 10 questions or less except for 
# 'CLEVR_train_008231.png', 'CLEVR_train_023595.png', 'CLEVR_train_026360.png', 'CLEVR_train_030574.png' have 2, 9, 9, 9
# 'CLEVR_test_000913.png', 'CLEVR_test_006571.png', 'CLEVR_test_008583.png'have 2, 9, 9, 9 [(913, 2), (6571, 8), (8583, 8)]
# 'CLEVR_val_005595.png', 'CLEVR_val_003233.png' have 9 and 2 
# but these were not in the sample anyway

val_sample_files = os.listdir(outpath+'/val')
val_questions_sample = [q for q in val_questions['questions'] if q['image_filename'] in val_sample_files]
questions_out = {'info': "02/02/2022 uniformly sampled 3000 images and its corresponding 10 questions", 'questions': val_questions_sample}
with open(dstpath+'CLEVR_val_questions.json', "w") as outfile:
    json.dump(questions_out, outfile)

dstpath = '/Users/aishni/universe/nsym/tutorials/neurosymbolic_programming_tutorial/datasets/CLEVR_sample/scenes/'

>>> with open('../scenes/CLEVR_val_scenes.json') as f:
...   val_scenes = json.load(f)
... 
val_scenes_all = {s['image_filename']: s for s in val_scenes['scenes']}
val_scenes_sample = {f: val_scenes_all[f] for f in val_sample}
val_scenes_sample_reformat = [val for fname, val in val_scenes_sample.items()]
val_scenes_sample_out = {'info': "02/02/2022 uniformly sampled 642 scenes", 'scenes': val_scenes_sample_reformat}

with open(dstpath+'CLEVR_val_scenes.json', "w") as outfile:
...   json.dump(val_scenes_sample_out, outfile)

