import requests
from typing import List, Dict
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

            name = self._get_prediction_in_list(prediction_key="name", prediction=prediction)

            city = self._get_prediction_in_list(prediction_key="city", prediction=prediction)

            state = self._get_prediction_in_list(prediction_key="state", prediction=prediction)
            
            techs = "_".join(prediction["techs"])

            req = requests.post(url=f"{self.base_api_url}talents", headers=POST_HEADERS, data=json.dumps(
                {
                   "data": {
                    "jobs": job,
                    "name": name,
                    "state": state,
                    "city": city,
                    "techs": techs
                   } 
                }
            ))
            if req.status_code == 200:
                print("inserted")
    
    def get_predictions(self):
        req = requests.get(url=f"{self.base_api_url}talents?populate=*", headers=HEADERS)
        return req.text

    def _get_prediction_in_list(self, prediction_key: str, prediction: Dict):
        return prediction[prediction_key][0] if prediction[prediction_key] else ""
        