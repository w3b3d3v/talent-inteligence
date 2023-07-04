import requests
from typing import Dict

def trigger_cloud_function(url: str, headers: Dict):
    try:
        res = requests.get(url=url, headers=headers)
        if res.status_code == 200:
            print("Triggered cloud function for url: ", url)
        else:
            print("Error on cloud function request: ", res.status_code)
    except Exception as e:
        print("Error on cloud function request: ", e)