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
    assert isinstance(ai_prompts, list), "ai_prompts should be a list"

def test_match_prompt():
    prompt = "Meu nome é rafael, sou desenvolvedor e utilizo javascript. Moro no rio grande do sul."
    match = matcher.match_prompt(prompt=prompt)
    assert len(match) == 4, "All properties should be set, even if no match"
    assert isinstance(match[0], list), "matched jobs should be a list"
    assert isinstance(match[1], list), "matched techs should be a list"
    assert isinstance(match[2], str), "matched name should be a string"
    assert isinstance(match[3], str), "matched uf should be a string"

def test_match_prompt_no_matches():
    prompt = "I am an artist living in New York."
    match = matcher.match_prompt(prompt=prompt)
    assert len(match) == 0, "No matches should be found"

def test_to_json():
    match = (["desenvolvedor"], ["javascript"], "rafael", "rio grande do sul")
    result = matcher.to_json(match)
    assert "jobs" in result
    assert "techs" in result
    assert "name" in result
    assert "state" in result
    assert "city" in result

def test_to_json_empty_match():
    match = ()
    result = matcher.to_json(match)
    assert result == {}

if __name__ == "__main__":
    pytest.main()
