
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

from core.llm import llm
from prompt.arhcitecture_prompt import ARCHITECTURE_PROMPT
from responce_model.architecture_agent import SystemArchitectureModel

architecture_agent = create_agent(
    name="architecture_agent",
    model=llm,
    system_prompt=ARCHITECTURE_PROMPT,
    response_format=ToolStrategy(SystemArchitectureModel),
)
