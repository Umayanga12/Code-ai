
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

from core.llm import llm
from prompt.planner_agent_prompt import PLANNER_AGENT_PROMPT
from responce_model.planner_agent_Model import PlannerAgentModel

planner_agent = create_agent(
    name="planner_agent",
    model=llm,
    system_prompt=PLANNER_AGENT_PROMPT,
    response_format=ToolStrategy(PlannerAgentModel),
)
