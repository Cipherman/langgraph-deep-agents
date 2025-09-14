from typing_extensions import Annotated, List, Literal
from pydantic import BaseModel

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool, InjectedToolArg

from tavily import TavilyClient

from src.utils import get_today_str
from src.agents.llm import summarize_llm
from src.prompts.deep_research.research import summarize_webpage_prompt


class Summary(BaseModel):
    summary: str
    key_excerpts: str


tavily_client = TavilyClient()


def tavily_search_multiple(
    search_queries: List[str],
    max_results: int = 3,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = True,
) -> List[dict]:
    # Note: can use AsyncTavilyClient for parallization
    search_docs = []
    for query in search_queries:
        result = tavily_client.search(
            query,
            max_results=max_results,
            include_raw_content=include_raw_content,
            topic=topic,
        )
        search_docs.append(result)

    return search_docs


def summarize_webpage_content(webpage_content: str) -> str:
    try:
        struct_llm = summarize_llm.with_structured_output(Summary)

        summary = struct_llm.invoke(
            [
                HumanMessage(
                    content=summarize_webpage_prompt.format(
                        webpage_content=webpage_content,
                        date=get_today_str(),
                    )
                )
            ]
        )

        formatted_summary = (
            f"<summary>\n{summary.summary}\n</summary>\n\n"
            f"<key_excerpts>\n{summary.key_excerpts}\n</key_excerpts>"
        )

        return formatted_summary

    except Exception as e:
        print(f"Failed to summarize webpage: {str(e)}")
        return (
            webpage_content[:1000] + "..."
            if len(webpage_content) > 1000
            else webpage_content
        )


def deduplicate_search_results(search_results: List[dict]) -> dict:
    unqiue_results = {}

    for response in search_results:
        for result in response["results"]:
            url = result["url"]
            if url not in unqiue_results:
                unqiue_results[url] = result

    return unqiue_results


def process_search_results(unique_results: dict) -> dict:
    summarized_results = {}

    for url, result in unique_results.items():
        if not result.get("raw_content"):
            content = result["content"]
        else:
            content = summarize_webpage_content(result["raw_content"])

        summarized_results[url] = {"title": result["title"], "content": content}

    return summarized_results


def format_search_output(summarized_results: dict) -> str:
    if not summarized_results:
        return "No valide search results found."

    formatted_output = "Search results: \n\n"

    for i, (url, result) in enumerate(summarized_results.items(), 1):
        formatted_output += f"\n\n--- SOURCE {i}: {result['title']} ---\n"
        formatted_output += f"URL: {url}\n\n"
        formatted_output += f"SUMMARY:\n{result['content']}\n\n"
        formatted_output += "-" * 80 + "\n"

    return formatted_output


@tool(parse_docstring=True)
def tavily_search(
    query: str,
    max_results: Annotated[int, InjectedToolArg] = 3,
    topic: Annotated[
        Literal["general", "news", "finance"], InjectedToolArg
    ] = "general",
) -> str:
    """Fetch results from Tavily search API with content summarization.

    Args:
        query: A single search query to execute
        max_results: Maximum number of results to return
        topic: Topic to filter results by ('general', 'news', 'finance')

    Returns:
        Formatted string of search results with summaries
    """
    # Execute search for single query
    search_results = tavily_search_multiple(
        [query],  # Convert single query to list for the internal function
        max_results=max_results,
        topic=topic,
        include_raw_content=True,
    )

    # Deduplicate results by URL to avoid processing duplicate content
    unique_results = deduplicate_search_results(search_results)

    # Process results with summarization
    summarized_results = process_search_results(unique_results)

    # Format output for consumption
    return format_search_output(summarized_results)
