from deepagents import create_deep_agent
from core.coding import model_coding
from prompt.builder.configHandler import CONFIGURATION_MANAGER_PROMPT
from prompt.builder.controller_prompt import API_CONTROLLER_PROMPT
from prompt.builder.model_prompt import DATABASE_MODEL_BUILDER_PROMPT
from prompt.builder.router_prompt import ROUTER_PROMPT
from prompt.builder.middleware import MIDDLEWARE_BUILDER_PROMPT
from prompt.builder.tester_prompt import TEST_WRITER_PROMPT
from tool.fileOperator import file_operator_tools


db_model_coding_agent = create_deep_agent(
    model=model_coding,
    system_prompt=DATABASE_MODEL_BUILDER_PROMPT,
    tools=file_operator_tools
)

controller_coding_agent = create_deep_agent(
    model=model_coding,
    system_prompt=API_CONTROLLER_PROMPT,
    tools=file_operator_tools
)

router_coding_agent = create_deep_agent(
    model=model_coding,
    system_prompt=ROUTER_PROMPT,
    tools=file_operator_tools
)

cofiguration_agent = create_deep_agent(
    model=model_coding,
    system_prompt= CONFIGURATION_MANAGER_PROMPT,
    tools=file_operator_tools
)

middlware_agent = create_deep_agent(
    model=model_coding,
    system_prompt = MIDDLEWARE_BUILDER_PROMPT,
    tools=file_operator_tools
)


tester_agent = create_deep_agent(
    model=model_coding,
    system_prompt= TEST_WRITER_PROMPT,
    tools=file_operator_tools
)