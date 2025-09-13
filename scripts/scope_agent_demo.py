from langchain_core.messages import HumanMessage
from src.graphs.deep_research.scope.builder import build_scope_graph

scope = build_scope_graph()

result = scope.invoke({"messages":[HumanMessage(content="I want to research the best hotel in Tokyo.")]})
print(result)