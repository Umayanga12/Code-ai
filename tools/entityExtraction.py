from langchain.prompts import PromptTemplate
import json
from main import llm


def extract_entities(requirements: str) -> dict:
    """
    Use LLM to parse requirements into structured data.
    Example output: {'User': {'properties': {'id': 'int', 'name': 'str'}, 'behaviors': ['login', 'logout']}}
    """
    prompt = PromptTemplate.from_template(
        "Extract entities, their properties (with types), and behaviors (methods) from this requirement: {req}. "
        "Output as JSON: {{'entity1': {{'properties': {{'prop1': 'type'}}, 'behaviors': ['method1']}}, ...}}"
    )
    chain = prompt | llm
    response = chain.invoke({"req": requirements})
    # Parse response to dict (assume JSON-like; add error handling in production)

    return json.loads(response.content)



