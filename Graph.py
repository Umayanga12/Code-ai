import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def generate_graph(extracted_data: dict) -> str:
    """
    Create a directed graph: Entities as nodes, properties/behaviors as node attributes.
    Relationships inferred (e.g., if behaviors reference other entities).
    Returns base64-encoded PNG image.
    """
    G = nx.DiGraph()
    for entity, details in extracted_data.items():
        # Add entity node with attributes
        G.add_node(entity, properties=details.get('properties', {}), behaviors=details.get('behaviors', []))
        # Infer edges (simple: if a behavior mentions another entity, add edge)
        for behavior in details.get('behaviors', []):
            for other_entity in extracted_data.keys():
                if other_entity.lower() in behavior.lower() and other_entity != entity:
                    G.add_edge(entity, other_entity, label=behavior)

    # Visualize
    pos = nx.spring_layout(G)  
    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10)
    nx.draw_networkx_edge_labels(G, pos)
    # Add node labels for props/behaviors
    for node, (x, y) in pos.items():
        props = G.nodes[node].get('properties', {})
        behvs = G.nodes[node].get('behaviors', [])
        plt.text(x, y - 0.1, f"Props: {props}\nBehvs: {behvs}", fontsize=8, ha='center')

    # Save to buffer and encode
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    return f"data:image/png;base64,{img_base64}"

