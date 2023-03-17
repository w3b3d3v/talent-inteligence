from typing import List, Tuple, Dict

class Matcher:
    def __init__(self, techs: List, jobs: List, names: List, uf: List) -> None:
        self.techs = techs
        self.jobs = jobs
        self.names = names
        self.uf = uf
        self.ai_prompts = []
        self.last_id_index = None
    
    def match_prompt(self, prompt: str) -> Tuple:
        matched_techs = []
        matched_jobs = []
        matched_name = ""
        matched_uf = ""

        for tech in self.techs:
            if tech in prompt.lower():
                matched_techs.append(tech)
        # enqueue prompts that did not matched so that the AI can continue
        for job in self.jobs:
            if job in prompt.lower():
                matched_jobs.append(job)
        
        for name in self.names:
            if name in prompt.lower():
                matched_name = name
        
        for uf in self.uf:
            if uf in prompt.lower():
                matched_uf = uf
                
        
        if len(matched_techs) == 0 or len(matched_jobs) == 0:
            self.ai_prompts.append(prompt)
            return ()
        return (matched_jobs, matched_techs, matched_name or "", matched_uf or "")
    
    def to_json(self, matches: Tuple) -> Dict:
        try:
            return {
                "jobs": matches[0],
                "techs": matches[1],
                "name": matches[2],
                "uf": matches[3]
            } 
        except:
            return {}

    def get_ai_prompts(self) -> List[str]:
        return self.ai_prompts

    