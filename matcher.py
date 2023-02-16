import re
from typing import List, Dict

class User:
    def __init__(self, user_data: Dict) -> None:
        assert len(user_data) == 7, "Wrong user structure. Make sure you have all needed attributes."
        assert list(user_data.keys()) == ["discord_name", "discord_id", "builder_type", "techs", "linkedin", "twitter", "website"], "User data have missing or more keys than needed."
        self.user_data = user_data
    
    def __str__(self) -> str:
        return str(self.get_discord_name())
    
    def get_user_data(self) -> Dict:
        return self.user_data
    
    def get_linkedin(self) -> str:
        return self.user_data.get("linkedin")
    
    def get_twitter(self) -> str:
        return self.user_data.get("twitter")
    
    def get_website(self) -> str:
        return self.user_data.get("website")
    
    def get_builder_type(self) -> List:
        return self.user_data.get("builder_type")
    
    def get_techs(self) -> List:
        return self.user_data.get("techs")
    
    def get_discord_name(self) -> str:
        return self.user_data.get("discord_name")
    
    def get_discord_id(self) -> str:
        return self.user_data.get("discord_id")

class Matcher:
    def build_user(self, message: str, discord_name: str, discord_id: str) -> User:
        builder_types = self.find_builder_type(message)
        techs = self.find_techs(message)
        linkedin = self.find_linkedin_link(message)
        twitter = self.find_twitter_link(message)
        website = self.find_website_link(message)
        user_data = {
            "discord_name": discord_name, 
            "discord_id": discord_id,
            "builder_type": builder_types,
            "techs": techs,
            "linkedin": linkedin,
            "twitter": twitter,
            "website": website
        }
        return User(user_data=user_data)

    def find_builder_type(self, message: str) -> List:
        builder_types = ["founder", "front end", "frontend", "back end", "backend", "full stack", "fullstack", "solidity", "solana", "full stack web3", "fullstack web3", "engenheiro de dados", "cientista de dados", "analista de dados", "engenheiro de jogos", "desenvolvedor de jogos", "devops", "product manager", "pm", "product designer", "ui/ux", "community manager", "marketing", "growth", "devrel", "escritor técnico", "copywriter", "contribuinte", "dao", "programador"]
        return [builder_type for builder_type in builder_types if builder_type in message.lower()]

    def find_techs(self,message: str) -> List:
        techs_list = ["angular", "c", "c#", "c++", "clojure", "dart", "elixir", "elm", "erlang", "f#", "ganache", "go", "graphql", "hardhat", "haskell", "java", "javascript", "kind", "kotlin", "meteor.js", "mongodb", "mysql", "nextjs", "node", "postgresql", "python", "react", "ruby", "rust", "scala", "solidity", "swift", "teal", "truffle", "typescript", "vue", "vyper", "php"]
        return [tech for tech in techs_list if tech in message.lower()]

    def find_linkedin_link(self, message: str) -> str:
        result = re.search(r"(?:https?:)?\/\/(?:[\w]+\.)?linkedin\.com\/in\/(?P<permalink>[\w\-\_À-ÿ%]+)\/?", message.lower())
        return result.group() if result else ""

    def find_twitter_link(self, message: str) -> str:
        result = re.search(r"(?:https?:)?\/\/(?:[A-z]+\.)?twitter\.com\/@?(?!home|share|privacy|tos)(?P<username>[A-z0-9_]+)\/?", message.lower())
        return result.group() if result else ""

    def find_website_link(self, message: str) -> str:
        result = re.search(r"/https:\/\/.{1,}/g", message.lower())
        return result.group() if result else ""


    
