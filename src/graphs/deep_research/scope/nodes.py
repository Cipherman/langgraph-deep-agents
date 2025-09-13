from typing_extensions import Literal

from langchain_core.messages import HumanMessage, AIMessage, get_buffer_string
from langgraph.graph import END
from langgraph.types import Command

from src.prompts.deep_research.scope import (
    clarify_with_user_instructions,
    transform_messages_into_research_topic_prompt,
)
from src.graphs.deep_research.scope.types import (
    AgentState,
    ClarifyWithUser,
    ResearchQuestion,
)
from src.agents.llm import llm
from src.utils import get_today_str


def clarify_with_user(
    state: AgentState,
) -> Command[Literal["write_research_brief", "__end__"]]:
    struct_llm = llm.with_structured_output(ClarifyWithUser)

    response = struct_llm.invoke(
        [
            HumanMessage(
                content=clarify_with_user_instructions.format(
                    messages=get_buffer_string(messages=state["messages"]),
                    date=get_today_str(),
                )
            )
        ]
    )

    if response.need_clarification:
        return Command(
            goto=END, update={"messages": [AIMessage(content=response.question)]}
        )
    else:
        return Command(
            goto="write_research_brief",
            update={"messages": [AIMessage(content=response.verification)]},
        )


def write_research_brief(state: AgentState):
    struct_llm = llm.with_structured_output(ResearchQuestion)

    response = struct_llm.invoke(
        [
            HumanMessage(
                content=transform_messages_into_research_topic_prompt.format(
                    messages=get_buffer_string(state.get("messages", [])),
                    date=get_today_str(),
                )
            )
        ]
    )

    return {
        "research_brief": response.research_brief,
        "supervisor_messages": [HumanMessage(content=f"{response.research.brief}")],
    }
