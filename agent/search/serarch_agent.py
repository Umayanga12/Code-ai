"""
Can use to fetch the documentations
"""
from langchain.agents import create_agent
from core.llm import llm
from prompt.search_agent_prompt import SEARCH_AGENT_PROMPT
from tool.search_doc import internet_search


search_agent = create_agent(
    llm=llm,
    system_prompt=SEARCH_AGENT_PROMPT,
    tools=[internet_search],
)
