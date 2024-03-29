
from model import Model

jobs_list = ["dev"]
techs_list = ["c"]
prompts = ["sou dev trabalho com c"]


def test_model_creation():
    model = Model(jobs_list=jobs_list, techs_list=techs_list, prompts=prompts)

    assert model.jobs_list == jobs_list
    assert model.techs_list == techs_list
    assert model.prompts == prompts
    for job, tech in zip(jobs_list, techs_list):
        assert job in model.base_prompt
        assert tech in model.base_prompt
