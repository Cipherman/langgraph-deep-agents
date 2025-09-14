from langgraph.graph import StateGraph, START, END

from .types import ResearcherState, ResearchOutputState
from .nodes import llm_call, tool_node, compress_research, should_continue


def build_research_graph():
    builder = StateGraph(ResearcherState, output_schema=ResearchOutputState)

    builder.add_node("llm_call", llm_call)
    builder.add_node("tool_node", tool_node)
    builder.add_node("compress_research", compress_research)

    builder.add_edge(START, "llm_call")
    builder.add_conditional_edges(
        "llm_call",
        should_continue,
        {
            "tool_node": "tool_node",
            "compress_research": "compress_research",
        },
    )
    builder.add_edge("tool_node", "llm_call")
    builder.add_edge("compress_research", END)

    return builder.compile()
