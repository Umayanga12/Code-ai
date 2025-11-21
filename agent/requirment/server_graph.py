import os
import sys

from agent.requirment.requirment_graph import RequirementsGraphState, requirements_graph

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

sys.path.insert(1, os.path.join("..", "core"))
sys.path.insert(1, os.path.join("..", "prompt"))
sys.path.insert(1, os.path.join("..", "responce_model"))

import json
from typing import Optional

from langchain.messages import AIMessage, HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.types import Command, interrupt

checkpointer = InMemorySaver()


class RequirementSystemState(MessagesState):
    requirements: Optional[dict]
    itinerary: Optional[dict]


def requirements_subgraph_node(
    state: RequirementSystemState, config: RunnableConfig
) -> RequirementSystemState:
    """
    Invoke the requirements graph as a subgraph.
    The subgraph shares 'messages' and 'requirements' state with parent.

    Handles interrupt loop using LangGraph interrupt() instead of input().
    """
    print(f"DEBUG: requirements_subgraph_node called")
    # Create subgraph state from parent state
    subgraph_state = RequirementsGraphState(
        messages=state["messages"],
        requirements_complete=False,
        interruption_message="",
        requirements=state.get("requirements"),
    )

    # Extract parent's thread_id from config and derive subgraph thread_id
    configurable = config.get("configurable", {}) if config else {}
    parent_thread_id = configurable.get("thread_id", "main-thread")
    subgraph_thread_id = f"{parent_thread_id}-requirements"
    subgraph_config = {"configurable": {"thread_id": subgraph_thread_id}}
    print(f"DEBUG: Subgraph thread_id: {subgraph_thread_id}")

    # Invoke the compiled requirements graph
    try:
        print(f"DEBUG: Invoking requirements_graph")
        subgraph_result = requirements_graph.invoke(
            subgraph_state,
            subgraph_config,
        )
    except Exception as e:
        print(f"DEBUG: Exception during requirements_graph invoke: {e}")
        # Check if it's a GraphInterrupt (it might be wrapped or direct)
        if type(e).__name__ == "GraphInterrupt":
             # It interrupted. We need to expose this to our parent.
             # The exception contains the interrupt value.
             interrupt_value = e.args[0]
             print(f"DEBUG: Caught GraphInterrupt: {interrupt_value}")
             
             # We interrupt ourself, passing the value up.
             # When we resume, we get user input.
             user_input = interrupt(interrupt_value)
             print(f"DEBUG: Resumed from interrupt with input: {user_input}")
             
             # Resume subgraph
             # We need to loop this handling.
             pass
        raise e

    while True:
        if isinstance(subgraph_result, dict) and "__interrupt__" in subgraph_result:
            # Extract interrupt message
            interrupt_value = subgraph_result["__interrupt__"]
            if isinstance(interrupt_value, list) and len(interrupt_value) > 0:
                interrupt_message = str(interrupt_value[0].value)
            else:
                interrupt_message = str(interrupt_value)
            
            print(f"DEBUG: Subgraph returned interrupt: {interrupt_message}")

            # Use interrupt() to pause and get user input from server
            user_input = interrupt(interrupt_message)
            print(f"DEBUG: Resumed from interrupt with input: {user_input}")

            # Resume execution with user input
            print(f"DEBUG: Resuming requirements_graph with user input")
            subgraph_result = requirements_graph.invoke(
                Command(resume=user_input),
                subgraph_config,
            )
        else:
            # No interrupt, execution completed
            print(f"DEBUG: Subgraph execution completed without interrupt")
            break

    # Extract requirements from completed subgraph execution
    requirements = subgraph_result.get("requirements")
    print(f"DEBUG: Extracted requirements: {requirements}")

    return {
        "messages": [AIMessage(content=json.dumps(requirements), name="requirements")],
        "requirements": requirements,
        "itinerary": None,
    }


graph = StateGraph(RequirementSystemState)

graph.add_node("requirements_subgraph", requirements_subgraph_node)
graph.add_edge(START, "requirements_subgraph")
graph.add_edge("requirements_subgraph", END)


server_graph = graph.compile(checkpointer=checkpointer)
