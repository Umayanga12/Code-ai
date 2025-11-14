import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

sys.path.insert(1, os.path.join(".", "agent"))

from agent.requirment_system_graph import requirment_system_graph

# initial_state = RequirementSystemState(
#     messages=[
#         HumanMessage(
#             content="I need to create the system that can manage my product stocks"
#         )
#     ],
#     requirements=None,
#     itinerary=None,
# )

# config = {"configurable": {"thread_id": "thread-1"}}

# # Invoke the graph - interrupt loop is now handled inside requirements_subgraph_node
# result = requirment_system_graph.invoke(initial_state, config)

# print("\n=== FINAL RESULTS ===")
# print(f"Requirements: {json.dumps(result.get('requirements'), indent=2)}")
# print(f"\nItinerary: {json.dumps(result.get('itinerary'), indent=2)}")
# print(f"\nRequirmnets: {json.dumps(result.get('requirements'), indent=2)}")
# print(result)


def create_graph():
    return requirment_system_graph
