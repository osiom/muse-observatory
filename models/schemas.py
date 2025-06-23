from typing import List

from pydantic import BaseModel


class ProjectModel(BaseModel):
    project_name: str
    organization: str
    geographic_level: str
    link_to_organization: str


class InspirationModel(BaseModel):
    user_input: str
    projects: List[ProjectModel]


class FunFactModel(BaseModel):
    kingdoms_life_subject: str
    fun_fact: str
    question_asked: str
    fact_check_link: str


class AppInfoResponse(BaseModel):
    name: str
    description: str
    environment: str
