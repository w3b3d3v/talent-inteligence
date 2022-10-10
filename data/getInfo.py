from typing import List, Tuple
import json

from yaml import parse

def getJson(labeled: str = True) -> List[Tuple]:
    if labeled == False:
        data_path = "./data/unlabeled.json"
    else:
        data_path = "./data/unlabeled.json"
    with open(data_path) as f:
        file_contents = f.read()
    parsed_json = json.loads(file_contents)
    print(len(parsed_json))
    return len(parsed_json)

getJson(False)