"""Scoping Types"""

import operator
from typing_extensions import Optional, Annotated, Sequence

from langchain_core.messages import BaseMessage
from langgraph.graph import MessagesState
from langgraph.graph.message import add_messages
from pydantic import BaseModel


# State Definition
class AgentInputState(MessagesState):
    pass


class AgentState(MessagesState):
    research_brief: Optional[str]
    supervisor_messages: Annotated[Sequence[BaseMessage], add_messages]
    raw_notes: Annotated[list[str], operator.add] = []
    notes: Annotated[list[str], operator.add] = []
    final_report: str


# Structured Output Schema
class ClarifyWithUser(BaseModel):
    need_clarification: bool
    question: str
    verification: str


class ResearchQuestion(BaseModel):
    research_brief: str
