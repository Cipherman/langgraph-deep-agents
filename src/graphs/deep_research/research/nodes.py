from typing_extensions import Literal

from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage, filter_messages


from src.utils import get_today_str
from src.agents.llm import llm, compress_llm
from src.graphs.deep_research.research.types import ResearcherState
from src.prompts.deep_research.research import (research_agent_prompt, 
                                                compress_research_system_prompt, 
                                                compress_research_human_message)
from src.tools.think import think_tool
from src.tools.tavily_search import tavily_search

tools = [tavily_search, think_tool]
tools_by_name = {tool.name: tool for tool in tools}
tool_llm = llm.bind_tools(tools)


def llm_call(state: ResearcherState):

    return {
        "researcher_messages": [
            tool_llm.invoke(
                [SystemMessage(content=research_agent_prompt)] + state["researcher_messages"]
            )
        ]
    }


def tool_node(state: ResearcherState):
    tool_calls = state["researcher_messages"][-1].tool_calls

    observations = []
    for tool_call in tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observations.append(tool.invoke(tool_call["args"]))

    tool_outputs = [
        ToolMessage(
            content=observation,
            name=tool_call["name"],
            tool_call_id = tool_call["id"]
        ) for observation, tool_call in zip(observations, tool_calls)
    ]

    return {"researcher_messages": tool_outputs}


def compress_research(state: ResearcherState) -> dict:
    system_message = compress_research_system_prompt.format(date=get_today_str())
    messages = [SystemMessage(content=system_message)] + state.get("researcher_messages",[]) + [HumanMessage(content=compress_research_human_message)]
    response = compress_llm.invoke(messages)

    raw_notes = [
        str(m.content) for m in filter_messages(
            state["researcher_messages"],
            include_types=["tool", "ai"]
        )
    ]

    return {
        "compressed_research": str(response.content),
        "raw_notes": ["\n".join(raw_notes)]
    }

def should_continue(state: ResearcherState) -> Literal["tool_node", "compress_research"]:
    messages = state["researcher_messages"]
    last_message = messages[-1]
   
    if last_message.tool_calls:
        return "tool_node"
    return "compress_research"
