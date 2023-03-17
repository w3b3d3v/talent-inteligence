import pytest
from matcher import Matcher

matcher = Matcher(
    techs=["c++", "c#", "javascript", "ruby"],
    jobs=["desenvolvedor", "engenheiro de software"],
    names=["lorenzo", "rafael", "gabriel"],
    uf=["rio grande do sul", "são paulo"]
)

def test_ai_prompts_getter():
    ai_prompts = matcher.get_ai_prompts()
    assert type(ai_prompts) == list, "Ai_prompts should be list"

def test_match_prompt():
    prompt = "Meu nome é rafael, sou desenvolvedor e utilizo javascript. Moro no rio grande do sul."
    match = matcher.match_prompt(prompt=prompt)
    assert len(match) == 4, "All properties should be set, even if no match"
    assert type(match[0]) == list, "matched jobs should be a list"
    assert type(match[1]) == list, "matched techs should be a list"

def test_to_json():
    matches = (["desenvolvedor"], ["javascript"], "lorenzo", "rio grande do sul")
    json_matches = matcher.to_json(matches)
    assert json_matches == {
        "jobs": ["desenvolvedor"], 
        "techs": ["javascript"], 
        "name": "lorenzo",
        "uf": "rio grande do sul"
    }, "matched object should be formated correctly"