
from helpers import generateTrainingData, getJson, cleanData
import random
import spacy 
from spacy.training import Example
from pathlib import Path
from tqdm import tqdm

model = None
n_iter=100
output_dir = Path("./saved_model")

# Checks to see if there is a current model or no model. In this case I will be starting with a blank model 
if model is not None:
    ner_model = spacy.load(model)  # load existing spaCy model
    print("Loaded model '%s'" % model)
else:
# this will create a blank english model
  ner_model = spacy.blank('pt')  # create blank Language class
  print("Created blank 'pt' model")

TRAIN_DATA = generateTrainingData(cleanData(getJson('labeled')))

ner_model.add_pipe('ner')
ner = ner_model.get_pipe('ner')
for _, annotations in TRAIN_DATA:
    for ent in annotations:
      ner.add_label(ent[2])
      
other_pipes = [pipe for pipe in ner_model.pipe_names if pipe != 'ner']
with ner_model.disable_pipes(*other_pipes):  # only train NER
    optimizer = ner_model.begin_training()
    for itn in range(n_iter):
        random.shuffle(TRAIN_DATA)
        losses = {}
        for text, annotations in tqdm(TRAIN_DATA):
            doc = ner_model.make_doc(text)
            example = Example.from_dict(doc, {"entities": annotations})
            ner_model.update(
                [example],
                sgd=optimizer,  # callable to update weights
                losses=losses)
        print(losses)

if output_dir is not None:
    output_dir = Path(output_dir)
    if not output_dir.exists():
        output_dir.mkdir()
    ner_model.meta['name'] = "Entity Extractor" # rename model
    ner_model.to_disk(output_dir)
    print("Saved model to", output_dir)
