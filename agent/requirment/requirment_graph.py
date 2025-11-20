from typing import Optional

from langchain.messages import AIMessage, HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.types import interrupt

from agent.requirment.requirment_agent import requirement_agent

checkpointer = InMemorySaver()


class RequirementsGraphState(MessagesState):
    requirements_complete: bool
    interruption_message: str
    requirements: Optional[dict]


def requirements_agent_node(state: RequirementsGraphState) -> RequirementsGraphState:
    print(f"DEBUG: requirements_agent_node called")
    response = requirement_agent.invoke({"messages": state["messages"]})

    response = response["structured_response"]
    requirements_response = response.requirements
    print(f"DEBUG: Agent response missing info question: '{requirements_response.missing_info.question}'")

    if requirements_response.missing_info.question != "":
        print(f"DEBUG: Returning interruption message")
        return {
            "messages": [
                AIMessage(content=requirements_response.missing_info.question)
            ],
            "interruption_message": requirements_response.missing_info.question,
            "requirements_complete": False,
            "requirements": None,
        }

    # Store complete requirements as dict in state
    print(f"DEBUG: Requirements complete")
    return {
        "messages": [],
        "requirements_complete": True,
        "interruption_message": "",
        "requirements": requirements_response.model_dump(),
    }


def should_ask_user_for_info(state: RequirementsGraphState) -> bool:
    result = not state["requirements_complete"]
    print(f"DEBUG: should_ask_user_for_info: {result}")
    return result


def ask_user_for_info(state: RequirementsGraphState) -> RequirementsGraphState:
    print(f"DEBUG: ask_user_for_info called with message: {state['interruption_message']}")
    user_response = interrupt(state["interruption_message"])
    print(f"DEBUG: User response received in ask_user_for_info: {user_response}")

    return {
        "messages": [HumanMessage(content=user_response)],
        "interruption_message": "",
        "requirements_complete": False,
        "requirements": None,
    }


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
