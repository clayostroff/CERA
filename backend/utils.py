import asyncio
from datetime import datetime, timezone
from textwrap import dedent
from typing import Literal

from langsmith import traceable

from tavily import AsyncTavilyClient

from state import Section



def get_current_utc_datetime() -> str:
    """
    Returns the current UTC date and time as a string formatted as YYYY-MM-DD HH:MM:SS.
    """
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")



def format_sections(sections: list[Section]) -> str:
    """
    Formats a list of sections into a string.
    """
    sections_as_string = ""
    for section in sections:
        section_as_string = dedent(f"""\
            SECTION TITLE:
            {section.name}
            DESCRIPTION:
            {section.description}
            REQUIRES RESEARCH:
            {section.research}
            CONTENT:
            {section.content if section.content else '[no content]'}
            \n{'-'*80}\n
        """)
        sections_as_string += section_as_string
    return sections_as_string



@traceable
async def tavily_search(search_queries: list[str], depth: Literal['basic', 'advanced']) -> list[dict]:
    """
    Does parallel web searches using Tavily Search

    Parameters:
        search_queries (list[str]): List of search queries as strings

    Returns:
        list[dict]: List of dict responses from Tavily Search, each with the format:
            {
                "query":  str,
                "results": [
                    {
                        "title": str,
                        "url": str,
                        "content": str,
                        "score": float,
                        "raw_content": str
                    },
                    ...
                ],
                "response_time": float
            }
    """
    
    async_tavily_client = AsyncTavilyClient()
    search_tasks = []
    for query in search_queries:
            search_tasks.append(
                async_tavily_client.search(
                    query = query,
                    search_depth = depth,
                    # topic = "news",
                    max_results = 2, # results per query
                    include_raw_content = True
                )
            )

    search_results = await asyncio.gather(*search_tasks)

    return search_results



def format_search_results(search_responses: list[dict]) -> str:
    """
    Formats a list of search responses into a string.
 
    Parameters:
        search_responses: List of search response dicts with the format:
            {
                "query":  str,
                "results": [
                    {
                        "title": str,
                        "url": str,
                        "content": str,
                        "score": float,
                        "raw_content": str
                    },
                    ...
                ],
                "response_time": float
            }
            
    Returns:
        str: Formatted string with deduplicated sources
    """

    results = []
    for response in search_responses:
        results.extend(response['results'])
    
    # Deduplicate by URL
    unique_sources = {source['url']: source for source in results}

    formatted_results = "CONTENT FROM SOURCES:\n\n"

    for source in unique_sources.values():
        formatted_results += f"{'-' * 80}\n"
        formatted_results += f"SOURCE TITLE: {source['title']}\n"
        formatted_results += f"URL: {source['url']}\n"
        formatted_results += f"CLEANED CONTENT: {source['content']}"

        raw_content = source.get('raw_content', '') or ""

        # Potentially clean raw content with a lightweight model

        if len(raw_content) > 10000:
            raw_content = raw_content[:10000] + "... [truncated at 10000 chars]"

        formatted_results += f"RAW CONTENT: {raw_content}\n\n"
        formatted_results += f"{'-'*80}\n\n"

    return formatted_results.strip()



async def execute_searches(query_list: list[str], depth: Literal['basic', 'advanced'] = 'basic') -> str:
    """
    Executes web searches for a list of queries
    
    Parameters:
        query_list: List of search queries
        
    Returns:
        str: Formatted string of search results
    """
    search_results = await tavily_search(query_list, depth)
    return format_search_results(search_results)