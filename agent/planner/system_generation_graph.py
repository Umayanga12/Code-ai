"""
System Generation Graph
Orchestrates the system planning and architecture generation workflow.
"""

from typing import Optional, Dict, Any

from langchain.messages import AIMessage, HumanMessage
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.checkpoint.memory import InMemorySaver

from agent.planner.planner_agent import planner_agent
from agent.planner.architecturer.architecture_agent import architecture_agent
from responce_model.planner_agent_Model import PlannerAgentModel
from responce_model.architecture_agent import SystemArchitectureModel

checkpointer = InMemorySaver()


class SystemGenerationState(MessagesState):
    """State for the system generation workflow."""
    requirements: Dict[str, Any]  # Input from requirements gathering
    planner_output: Optional[PlannerAgentModel]
    architecture_output: Optional[SystemArchitectureModel]
    final_output: Optional[Dict[str, Any]]


def planner_node(state: SystemGenerationState) -> SystemGenerationState:
    """
    Generate a high-level plan based on requirements.
    """
    requirements = state.get("requirements", {})
    
    # Convert requirements to a string representation for the prompt
    req_str = f"User Requirements (Graph Entities): {requirements}"
    
    messages = [HumanMessage(content=req_str)]
    
    response = planner_agent.invoke({"messages": messages})
    planner_output = response["structured_response"]
    
    return {
        "messages": [AIMessage(content="Plan generated.")],
        "planner_output": planner_output
    }


def architecture_node(state: SystemGenerationState) -> SystemGenerationState:
    """
    Generate detailed system architecture based on the plan.
    """
    planner_output = state["planner_output"]
    
    # Construct input for architecture agent
    arch_input = f"""
    Based on the following High-Level Plan, generate a detailed System Architecture.
    
    High-Level Plan:
    {planner_output.model_dump_json(indent=2)}
    
    Original Requirements:
    {state.get("requirements", {})}
    """
    
    messages = [HumanMessage(content=arch_input)]
    
    response = architecture_agent.invoke({"messages": messages})
    architecture_output = response["structured_response"]
    
    return {
        "messages": [AIMessage(content="Architecture generated.")],
        "architecture_output": architecture_output
    }


def finalize_node(state: SystemGenerationState) -> SystemGenerationState:
    """
    Combine plan and architecture into final output.
    """
    planner = state["planner_output"]
    architecture = state["architecture_output"]
    
    final_data = {
        "plan": planner.model_dump(),
        "architecture": architecture.model_dump()
    }
    
    return {
        "final_output": final_data
    }


# Build the system generation graph
graph = StateGraph(SystemGenerationState)

graph.add_node("planner_node", planner_node)
graph.add_node("architecture_node", architecture_node)
graph.add_node("finalize_node", finalize_node)

graph.add_edge(START, "planner_node")
graph.add_edge("planner_node", "architecture_node")
graph.add_edge("architecture_node", "finalize_node")
graph.add_edge("finalize_node", END)

system_generation_graph = graph.compile(checkpointer=checkpointer)

