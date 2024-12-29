# react_agent/agent.py
import os

from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI

from react_agent.tools import calculator_tool, search_tool

load_dotenv()

# Set up OpenAI API Key
openai_api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(openai_api_key=openai_api_key)

prompt = hub.pull("hwchase17/react")
tools = [search_tool, calculator_tool]
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=10,
    return_intermediate_steps=True,
)


def get_agent_executor():
    return agent_executor
