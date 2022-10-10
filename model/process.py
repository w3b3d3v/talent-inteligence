
from pathlib import Path
from typing import List
import spacy 
from spacy.language import Language;
from helpers import getMessages;

model_dir = Path("./saved_model")

def load_model(model_dir: Path=model_dir) -> Language:
    nlp = spacy.load(model_dir)
    return nlp

def predict(model: Language, messages: List[str]):
    ents = []
    for message in messages:
        doc = model(message)
        this_ent = []
        for ent in doc.ents:
            this_ent.append((ent.label_, ent.text))
        ents.append(this_ent)
    return ents

messages = getMessages()
texts = [message[0] for message in messages]
model = load_model()
prediction = predict(model, texts)

i = 0
for pred in prediction:
    i+= 1
    print(f"prediction #{i}")
    for p in pred:
        print(p)
    
        