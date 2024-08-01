from tools.retrieval_eventi import get_relevant_document_tool
from tools.aws import ec2_shutdown_tools, ec2_turnon_tools
from tools.tavily import web_search_tool
from tools.utils import get_today_date_tool

# from prompts.react import prompt_react
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv(override=True)

tools = [get_relevant_document_tool, get_today_date_tool, web_search_tool]
retrieved_text = ""

# Load ReAct prompt
prompt_react = hub.pull("hwchase17/react")

# Initialize ChatGroq model for language understanding
model = ChatOpenAI(
    model_name="meta-llama/Meta-Llama-3.1-8B-Instruct",
    base_url="http://vllm:8000/v1",
    temperature=0,
)

# Create ReAct agent
react_agent = create_react_agent(model, tools=tools, prompt=prompt_react)
react_agent_executor = AgentExecutor(
    agent=react_agent, tools=tools, verbose=True, handle_parsing_errors=True
)
