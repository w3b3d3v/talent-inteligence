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
            job_ids = [self.get_job_id_by_name(job_name=job, job_index=index) for index, job in enumerate(prediction["jobs"])]

            tech_ids = [self.get_tech_id_by_name(tech_name=tech, tech_index=index) for index, tech in enumerate(prediction["techs"])]

            name = self._get_prediction_in_dict(prediction_key="name", prediction=prediction)

            city = self._get_prediction_in_dict(prediction_key="city", prediction=prediction)

            state = self._get_prediction_in_dict(prediction_key="uf", prediction=prediction)

            req = requests.post(url=f"{self.base_api_url}talents", headers=POST_HEADERS, data=json.dumps(
                {
                   "data": {
                        "jobs": job_ids,
                        "name": name,
                        "state": state,
                        "city": city,
                        "teches": tech_ids,
                        "discord_id": prediction["discord_id"]
                   }
                }
            ))
            if req.status_code == 200:
                print("inserted")

    def get_predictions(self):
        req = requests.get(url=f"{self.base_api_url}talents?populate=*", headers=HEADERS)
        return req.text
    
    def get_tech_id_by_name(self, tech_name: str, tech_index: int = 0):
        req = requests.get(url=f"{self.base_api_url}techs?name={tech_name}", headers=HEADERS)
        return req.json()["data"][tech_index]["id"]

    def get_job_id_by_name(self, job_name: str, job_index: int = 0):
        req = requests.get(url=f"{self.base_api_url}jobs?name={job_name}", headers=HEADERS)
        return req.json()["data"][job_index]["id"]

    def _get_prediction_in_dict(self, prediction_key: str, prediction: Dict):
        return prediction[prediction_key] if prediction[prediction_key] else ""
