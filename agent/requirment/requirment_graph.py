"""
Requirements Gathering Graph
Handles the interactive requirements gathering process with user interrupts.
"""

from typing import Optional

from langchain.messages import AIMessage, HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.types import interrupt

from agent.requirment.requirment_agent import requirement_agent

checkpointer = InMemorySaver()


class RequirementsGraphState(MessagesState):
    """State for the requirements gathering graph."""
    requirements_complete: bool
    interruption_message: str
    requirements: Optional[dict]


def requirements_agent_node(state: RequirementsGraphState) -> RequirementsGraphState:
    """
    Invoke the requirements agent to gather information.
    Returns either a question for missing info or complete requirements.
    """
    response = requirement_agent.invoke({"messages": state["messages"]})
    response = response["structured_response"]
    requirements_response = response.requirements

    # Check if agent needs more information
    if requirements_response.missing_info.question != "":
        return {
            "messages": [
                AIMessage(content=requirements_response.missing_info.question)
            ],
            "interruption_message": requirements_response.missing_info.question,
            "requirements_complete": False,
            "requirements": None,
        }

    # Requirements are complete
    return {
        "messages": [],
        "requirements_complete": True,
        "interruption_message": "",
        "requirements": requirements_response.model_dump(),
    }


def should_ask_user_for_info(state: RequirementsGraphState) -> bool:
    """Determine if we need to ask the user for more information."""
    return not state["requirements_complete"]


def ask_user_for_info(state: RequirementsGraphState) -> RequirementsGraphState:
    """
    Interrupt execution to ask user for missing information.
    Returns the user's response as a new message.
    """
    user_response = interrupt(state["interruption_message"])

    return {
        "messages": [HumanMessage(content=user_response)],
        "interruption_message": "",
        "requirements_complete": False,
        "requirements": None,
    }


# Build the requirements graph
graph = StateGraph(RequirementsGraphState)
graph.add_node("requirements_agent", requirements_agent_node)
graph.add_node("ask_user_for_info", ask_user_for_info)
graph.add_edge(START, "requirements_agent")
graph.add_conditional_edges(
    "requirements_agent",
    should_ask_user_for_info,
    {True: "ask_user_for_info", False: END},
)
graph.add_edge("ask_user_for_info", "requirements_agent")

requirements_graph = graph.compile(checkpointer=checkpointer)

