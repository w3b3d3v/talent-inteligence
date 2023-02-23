import os
import json
import openai
from typing import List, Dict
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

class Model:
  def __init__(self, prompts: List) -> None:
    self.prompts = prompts
    self.base_prompt = """A mensagem a seguir é um texto de apresentação. Extraia desse texto os campos: emprego, nome e tecnologias. Retorne esses dados no formato JSON, com os rótulos: job, name, techs. Cada rótulo corresponde a uma lista de strings, onde irão os dados extraídos. Caso identifique que o usuário é um estudante também, adicione estudante ao campo job. Caso não encontre os campos especificados, deixe o atributo em branco. Retorne apenas o JSON, sem nenhum outro texto na resposta.\n"""
  
  def extract_from_all_prompts(self) -> List:
    responses = []
    for prompt in self.prompts:
      final_prompt = self.base_prompt + prompt
      response = openai.Completion.create(
        model="text-davinci-003",
        prompt=final_prompt,
        temperature=0.5,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0.8,
        presence_penalty=0
      )
      responses.append(response)
    print("extracted from prompts correctly")
    return responses
  
  def remove_characters(self, responses: List) -> List:
    formated = []
    for response in responses:
      response = response.replace(".", "")
      response = response.replace("/", "")
      response = response.replace("-", "")
      response = response.replace("_", "")
      formated.append(response)
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
      