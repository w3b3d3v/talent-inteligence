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
    def __init__(self, predictions: List = [], jobs: List = [], techs: List = []) -> None:
        self.predictions = predictions
        self.base_api_url = os.getenv("BASE_API_URL")
        self.jobs = jobs
        self.techs = techs

    def insert_jobs(self):
        try:
            for job in self.jobs:
                req = requests.post(url=f"{self.base_api_url}jobs", headers=POST_HEADERS, data=json.dumps(
                    {
                        "data": {
                            "name": job
                        }
                    }
                ))
                if req.status_code == 200:
                    print("inserted")
        except Exception as e:
            print(e)

    def insert_techs(self):
        try:
            for tech in self.techs:
                req = requests.post(url=f"{self.base_api_url}techs", headers=POST_HEADERS, data=json.dumps(
                    {
                        "data": {
                            "name": tech
                        }
                    }
                ))
                if req.status_code == 200:
                    print("inserted")
        except Exception as e:
            print(e)

    def insert_predictions(self):
        for prediction in self.predictions:
            job_ids = [self.get_job_id_by_name(job_name=job) for job in prediction["jobs"] if self.get_job_id_by_name(job_name=job) is not None]
            tech_ids = [self.get_tech_id_by_name(tech_name=tech) for tech in prediction["techs"] if self.get_tech_id_by_name(tech_name=tech) is not None]

            name = self._get_prediction_in_dict(prediction_key="name", prediction=prediction)

            city = self._get_prediction_in_dict(prediction_key="city", prediction=prediction)

            state = self._get_prediction_in_dict(prediction_key="state", prediction=prediction)
            req = requests.post(url=f"{self.base_api_url}talents", headers=POST_HEADERS, data=json.dumps(
                {
                   "data": {
                        "jobs": job_ids,
                        "name": name,
                        "state": state,
                        "city": city,
                        "techs": tech_ids,
                        "discord_id": prediction["discord_user_id"]
                   }
                }
            ))
            if req.status_code == 200:
               print("Messages processed and stored.") 
            else:
                print(req.json())

    def get_predictions(self):
        req = requests.get(url=f"{self.base_api_url}talents?populate=*", headers=HEADERS)
        return req.text

    def get_tech_id_by_name(self, tech_name: str):
        req = requests.get(url=f"{self.base_api_url}techs?name={tech_name}", headers=HEADERS)
        data = req.json()
        filtered_ids = [item["id"] for item in data["data"] if item["attributes"]["name"] == tech_name]
        return filtered_ids[0] if len(filtered_ids) > 0 else None

    def get_job_id_by_name(self, job_name: str):
        req = requests.get(url=f"{self.base_api_url}jobs?name={job_name}", headers=HEADERS)
        data = req.json()
        filtered_ids = [item["id"] for item in data["data"] if item["attributes"]["name"] == job_name]
        return filtered_ids[0] if len(filtered_ids) > 0 else None

    def _get_prediction_in_dict(self, prediction_key: str, prediction: Dict):
        return prediction[prediction_key] if prediction[prediction_key] else ""
