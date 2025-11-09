import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

sys.path.insert(1, os.path.join(".", "core"))
sys.path.insert(1, os.path.join(".", "prompt"))
sys.path.insert(1, os.path.join(".", "responce_model"))

from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

from core.llm import llm
from prompt.req_gather_prompt import PROJECT_REQUIREMENT_GATHERING
from responce_model.requrementModel import CompleteRequirement

requirment_agent = create_agent(
    model=llm,
    system_prompt=PROJECT_REQUIREMENT_GATHERING,
    response_format=ToolStrategy(CompleteRequirement),
)
