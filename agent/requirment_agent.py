from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

from llm import llm
from prompt import PROJECT_REQUIREMENT_GATHERING
from responce_model import CompleteRequirement

requirment_agent = create_agent(
    model=llm,
    system_prompt=PROJECT_REQUIREMENT_GATHERING,
    response_format=ToolStrategy(CompleteRequirement),
)
