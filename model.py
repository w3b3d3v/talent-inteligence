import os
import openai
from typing import List
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

class Model:
  def __init__(self, prompts: List) -> None:
    self.prompts = prompts

  def predict_job(self, prompt: str) -> str:
    base_prompt = "Extraia o trabalho do usuário:\n"
    final_prompt = base_prompt + prompt
    final_prompt.encode("utf-8")
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=final_prompt,
      temperature=0.5,
      max_tokens=60,
      top_p=1,
      frequency_penalty=0.8,
      presence_penalty=0
    )
    return response["choices"][0]["text"]
  
  def predict_techs(self, prompt: str) -> str:
    base_prompt = "Extraia as tecnologias:\n"
    final_prompt = base_prompt + prompt
    final_prompt.encode("utf-8")
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=final_prompt,
      temperature=0.5,
      max_tokens=60,
      top_p=1,
      frequency_penalty=0.8,
      presence_penalty=0
    )
    return response["choices"][0]["text"]

  def print_responses(self, responses: List) -> None:
    i = 1
    for response in responses:
      print(f"Prompt #{i}")
      i += 1
      print(f"Prompt: {response[0]}")
      print(f"{response[1][0]}")
      print(f"{response[1][1]}")
  
  def predict_all(self) -> List:
    results = []
    for prompt in self.prompts:
      techs = self.predict_techs(prompt=prompt)
      job = self.predict_job(prompt=prompt)
      results.append([prompt, (techs, job)])
    self.print_responses(results)
    return results

