
from langgraph.prebuilt import create_react_agent
from src.config.env import setup_env

from src.tools.think import think_tool
from src.tools.tavily_search import tavily_search

from src.prompts.deep_research.research import research_agent_prompt

setup_env()

agent = create_react_agent(
    model= "anthropic:claude-3-5-haiku-latest",
    tools= [tavily_search, think_tool],
    prompt=research_agent_prompt,
)