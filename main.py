from langchain_ollama import ChatOllama
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.memory import ConversationBufferMemory
from Graph import generate_graph
from entityExtraction import extract_entities

# Set up local LLM
llm = ChatOllama(model="hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF", temperature=0.7)

# Define tools for the agent
tools = [
    Tool(name="ExtractEntities", func=extract_entities, description="Extract structured entities from requirements text."),
    Tool(name="GenerateGraph", func=generate_graph, description="Generate a graph image from extracted entity data.")
]

system_prompt = """
You are an AI backend developer agent. Your goal is to help design software based on user requirements.
- If the input is unclear or incomplete, ask specific questions to clarify (e.g., about data types, relationships).
- Once requirements are clear, use 'ExtractEntities' tool to parse into entities/properties/behaviors.
- Then use 'GenerateGraph' to create a visual graph.
- Respond conversationally, and end with the graph if ready.
"""

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
agent = initialize_agent(
    tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True, memory=memory, handle_parsing_errors=True
)
agent.agent.llm_chain.prompt.template = system_prompt + agent.agent.llm_chain.prompt.template


def run_agent():
    print("AI Backend Developer Agent: Hello! Describe your backend requirements.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        response = agent.run(input=user_input)
        print("Agent:", response)
        # If graph generated, it will be in response (e.g., print the base64 or save image)

if __name__ == "__main__":
    run_agent()
