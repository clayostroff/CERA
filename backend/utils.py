import os
import asyncio
import textwrap

import requests
import random 
import concurrent
import aiohttp
import time
import logging

from tavily import AsyncTavilyClient

from langsmith import traceable

from state import Section



def format_sections(sections: list[Section]) -> str:
    """Formats a list of sections into a string."""
    sections_as_string = ""
    for section in sections:
        section_as_string = textwrap.dedent(f"""\
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
async def tavily_search(search_queries: list[str]) -> list[dict]:
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

    # print("tavily_search : checkpoint 1")

    async_tavily_client = AsyncTavilyClient()
    search_tasks = []
    for query in search_queries:
            search_tasks.append(
                async_tavily_client.search(
                    query,
                    search_depth = "advanced",
                    topic = "general",
                    max_results = 5,
                    raw_content = True
                )
            )

    # print("tavily_search : checkpoint 2")

    search_results = await asyncio.gather(*search_tasks)

    # print("tavily_search : checkpoint 3")

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

    print("format_search_results : checkpoint 1")

    results = []
    for response in search_responses:
        results.extend(response['results'])
    
    # Deduplicate by URL
    unique_sources = {source['url']: source for source in results}

    formatted_results = "CONTENT FROM SOURCES:\n\n"

    print("format_search_results : checkpoint 2")

    for source in unique_sources.values():
        formatted_results += f"{'-' * 80}\n"
        formatted_results += f"SOURCE TITLE: {source['title']}\n"
        formatted_results += f"URL: {source['url']}\n"
        formatted_results += f"CLEANED CONTENT: {source['content']}"

        raw_content = source.get('raw_content', "") or ""

        if len(raw_content) > 10000:
            raw_content = raw_content[:10000] + "... [truncated at 10000 chars]"

        formatted_results += f"RAW CONTENT: {raw_content}\n\n"
        formatted_results += f"{'-'*80}\n\n"

    return formatted_results.strip()



async def execute_searches(query_list: list[str]) -> str:
    """
    Executes web searches for a list of queries
    
    Parameters:
        query_list: List of search queries
        
    Returns:
        str: Formatted string of search results
    """

    print("execute_searches : checkpoint 1")

    search_results = await tavily_search(query_list)

    print("execute_searches : checkpoint 2")

    return format_search_results(search_results)