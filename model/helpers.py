
from typing import List, Tuple
import sqlite3
import json


def generateTrainingData(all_data: List[object] = []) -> List[Tuple]:
  training_data = []
  
  for data in all_data:
    annots = [(an["start"], an["end"], an["labels"][0]) for an in data["annotations"]]
    
    training_data.append((data["original_text"], annots))
    
  return training_data

def cleanData(all_data: List=[]) -> List[str]:
  cleaned = []
  for data in all_data:
    text = data["data"]["text"]
    data_id = data["id"]
    annotations_dirty = data["annotations"][0]["result"]
    annotations = [an["value"] for an in annotations_dirty]
   
    cleaned_obj = {
      "data_id": data_id,
      "original_text": text,
      "annotations": annotations
    }
    cleaned.append(cleaned_obj)
  return cleaned


def getMessages(limit: int=100) -> List[str]:
    con = sqlite3.connect("db/messages.db")
    cur = con.cursor()
    query = f"SELECT text FROM messages LIMIT {limit};"
    res = cur.execute(query)
    messages = res.fetchall()
    return [msg[0] for msg in messages]
  
def getJson(filename) -> List[Tuple]:
  with open(f"./data/{filename}.json") as f:
    file_contents = f.read()

  parsed_json = json.loads(file_contents)
  return parsed_json

generateTrainingData(cleanData(getJson("labeled")))