import requests
from typing import List
import json
from dotenv import load_dotenv
import os

load_dotenv()

API_TOKEN = os.getenv("STRAPI_API_TOKEN")
HEADERS = {
    "Authorization": f"bearer {API_TOKEN}"
}
POST_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"bearer {API_TOKEN}"
}


class Api:
    def __init__(self, predictions: List = []) -> None:
        self.predictions = predictions
        self.base_api_url = os.getenv("BASE_API_URL")
    def insert_predictions(self):
        for prediction in self.predictions:
            job = "_".join(prediction["job"])

            if prediction["name"]:
                name = prediction["name"][0]
            else:
                name = ""

            techs = "_".join(prediction["techs"])

            req = requests.post(url=f"{self.base_api_url}users-data", headers=POST_HEADERS, data=json.dumps(
                {
                   "data": {
                    "jobs": job,
                    "name": name,
                    "techs": techs
                   } 
                }
            ))
            if req.status_code == 200:
                print("inserted")
    
    def get_predictions(self):
        req = requests.get(url=f"{self.base_api_url}users-data?populate=*", headers=HEADERS)
        return req.text