from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

from core.llm import llm
from prompt.req_gather_prompt import PROJECT_REQUIREMENT_GATHERING
from responce_model.requrementModel import RequirmentAgentResponceModel

requirement_agent = create_agent(
    model=llm,
    system_prompt=PROJECT_REQUIREMENT_GATHERING,
    response_format=ToolStrategy(RequirmentAgentResponceModel),
)
