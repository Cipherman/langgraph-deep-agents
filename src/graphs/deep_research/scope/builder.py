from langgraph.graph import StateGraph, START, END

from .types import AgentState, AgentInputState
from .nodes import clarify_with_user, write_research_brief


def build_scope_graph():
    builder = StateGraph(AgentState, input_schema=AgentInputState)

    builder.add_node("clarify_with_user", clarify_with_user)
    builder.add_node("write_research_brief", write_research_brief)

    builder.add_edge(START, "clarify_with_user")
    builder.add_edge("write_research_brief", END)

    return builder.compile()
