import operator
from typing_extensions import TypedDict, Annotated, List, Sequence
from pydantic import BaseModel
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

# State Definitions
class ResearcherState(TypedDict):
    researcher_messages: Annotated[Sequence[BaseMessage], add_messages]
    tool_call_iterations: int
    research_topic: str
    compressed_research: str
    raw_notes: Annotated[List[str], operator.add]

class ResearchOutputState(TypedDict):
    compressed_research: str
    raw_notes: Annotated[List[str], operator.add]
    researcher_messages: Annotated[Sequence[BaseMessage], add_messages]

# Structured Output Schemas
class ClarifyWithUser(BaseModel):
    need_clarification: bool
    question: str
    verification: str

class ResearchQuestion(BaseModel):
    research_brief: str

class Summary(BaseModel):
    summary: str
    key_excerpts: str