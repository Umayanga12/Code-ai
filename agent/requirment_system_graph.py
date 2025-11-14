import json
from typing import Optional

from langchain.messages import AIMessage, HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.types import Command
from requirment_graph import RequirementsGraphState, requirements_graph

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

    Handles interrupt loop internally to gather all user input before proceeding.
    Similar to requirements_graph.py main block pattern.
    """
    # Create subgraph state from parent state
    subgraph_state = RequirementsGraphState(
        messages=state["messages"],
        requirements_complete=False,
        interruption_message="",
        requirements=state.get("requirements"),
    )

    # Extract parent's thread_id from config and derive subgraph thread_id
    # RunnableConfig is dict-like with "configurable" key containing thread_id
    configurable = config.get("configurable", {}) if config else {}
    parent_thread_id = configurable.get("thread_id", "main-thread")
    subgraph_thread_id = f"{parent_thread_id}-requirements"
    subgraph_config = {"configurable": {"thread_id": subgraph_thread_id}}

    # Invoke the compiled requirements graph
    subgraph_result = requirements_graph.invoke(
        subgraph_state,
        subgraph_config,
    )

    # Handle interrupt loop - similar to requirements_graph.py
    while True:
        if "__interrupt__" in subgraph_result:
            # Extract interrupt message
            interrupt_value = subgraph_result["__interrupt__"]
            if isinstance(interrupt_value, list) and len(interrupt_value) > 0:
                interrupt_message = str(interrupt_value[0].value)
            else:
                interrupt_message = str(interrupt_value)

            # Display interrupt message to user
            print(f"\n{interrupt_message}")

            # Get user input
            user_input = input("Your response: ").strip()

            # Resume execution with user input
            subgraph_result = requirements_graph.invoke(
                Command(resume=user_input),
                subgraph_config,
            )
        else:
            # No interrupt, execution completed
            break

    # Extract requirements from completed subgraph execution
    requirements = subgraph_result.get("requirements")

    # The result contains 'requirements' field populated when complete
    return {
        "messages": [AIMessage(content=json.dumps(requirements), name="requirements")],
        "requirements": requirements,
        "itinerary": None,
    }


graph = StateGraph(RequirementSystemState)

graph.add_node("requirements_subgraph", requirements_subgraph_node)
graph.add_edge(START, "requirements_subgraph")
graph.add_edge("requirements_subgraph", END)


requirment_system_graph = graph.compile(checkpointer=checkpointer)

if __name__ == "__main__":
    initial_state = RequirementSystemState(
        messages=[
            HumanMessage(
                content="I need to create the system that can manage my product stocks"
            )
        ],
        requirements=None,
        itinerary=None,
    )

    config = {"configurable": {"thread_id": "thread-1"}}

    # Invoke the graph - interrupt loop is now handled inside requirements_subgraph_node
    result = requirment_system_graph.invoke(initial_state, config)

    print("\n=== FINAL RESULTS ===")
    print(f"Requirements: {json.dumps(result.get('requirements'), indent=2)}")
    print(f"\nItinerary: {json.dumps(result.get('itinerary'), indent=2)}")
    print(f"\nRequirmnets: {json.dumps(result.get('requirements'), indent=2)}")
