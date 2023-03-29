import os
import re
import json
import openai
from typing import List, Dict
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


class Model:
    def __init__(self, jobs_list: List, techs_list: List, prompts: List) -> None:
        self.jobs_list = jobs_list
        self.techs_list = techs_list
        self.prompts = prompts
        self.base_prompt = f"""A mensagem a seguir é um texto de apresentação. Extraia desse texto os campos: emprego, nome, cidade, estado e tecnologias. Tente encaixar as tecnologias extraídas na seguinte lista: {self.techs_list} . Tente encaixar os trabalhos extraídos na seguinte lista: {self.jobs_list} . Caso a tecnologia ou trabalho não se encaixe em nenhuma categoria, crie uma nova com o nome adequado. Retorne esses dados no formato JSON, com os rótulos: job, name, city, state, techs. job e techs devem ser listas de strings. Caso não encontre os campos especificados, deixe o atributo em branco. Retorne apenas o JSON, sem nenhum outro texto na resposta.\n"""

    def extract_from_all_prompts(self) -> List:
        responses = []
        for prompt in self.prompts:
            final_prompt = self.base_prompt + prompt
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=final_prompt,
                temperature=0.1,
                max_tokens=250,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            responses.append(response)
        print("extracted from prompts correctly")
        return responses

    def remove_characters(self, responses: List) -> List:
        formated = []
        for response in responses:
            res = re.sub(r'[\., \,, \/, \-, _]', '', response)
            formated.append(res)
        return formated

    def to_json(self, responses: List) -> List:
        complete = []
        for res in responses:
            try:
                complete.append(json.loads(res))
            except Exception as e:
                print(e)
                pass
        return complete

    def format_responses(self, responses: List) -> List[Dict]:
        formated_responses = []
        try:
            for response in responses:
                response = json.loads(str(response.choices[0]).replace("\n", ""))["text"]
                formated_responses.append(response)
                formated_responses = [formated_response.replace("\n", "") for formated_response in formated_responses]
            formated = self.remove_characters(formated_responses)
            print("Formated responses correctly")
            return formated
        except Exception as e:
            print(e)
            return []
