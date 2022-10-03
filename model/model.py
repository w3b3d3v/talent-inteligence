from helpers import generateTrainingData
import random
import spacy 
from spacy.training import Example

nlp = spacy.blank('pt')  # new, empty model. Let’s say it’s for the English language
nlp.vocab.vectors.name = 'example_model_training'   # give a name to our list of vectors
# add NER pipeline
# our pipeline would just do NER
nlp.add_pipe('ner', last=True)  # we add the pipeline to the model

ner = nlp.get_pipe("ner")

DATA = generateTrainingData()

ner.add_label("TECH")

optimizer = nlp.begin_training()

for i in range(20):
    random.shuffle(DATA)
    for text, annotations in DATA:
        doc = nlp.make_doc(text)
        example = Example.from_dict(doc, {"entities": annotations})
        nlp.update([example], sgd=optimizer)

doc = nlp("Olá pessoal! Meu nome é Lucas e sou um desenvolvedor web buscando aprender sobre web3, solidity e blockchain.")

for entity in doc.ents:
  print(entity.label_, ' | ', entity.text)