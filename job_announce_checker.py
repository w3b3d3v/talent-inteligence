import os
import requests
from dotenv import load_dotenv
import openai
import json
load_dotenv()

class JobAnnounceChecker:
    def __init__(self) -> None:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.base_prompt = "Identifique se a mensagem abaixo é um anúncio de vaga, golpe ou venda de algum produto. Geralmente envolvem oferecer muito dinheiro em pouco tempo, anúncio de cursos, vagas ou produtos. Retorne apenas 'true' ou 'false' sem linhas novas ou outros caracteres. Considere mensagens em inglês.\nMensagem: "
        pass

    def check_message(self, message: str) -> bool:
        final_prompt = self.base_prompt + message
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
        }
        print(type(headers))
        res = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            data=json.dumps({
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": final_prompt}],
            "temperature": 0.2
            })
        )
        res = res.json()["choices"][0]["message"]["content"]
        return True if res == 'true' else False
