from typing import Literal

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig

from langgraph.constants import Send
from langgraph.graph import START, END, StateGraph
from langgraph.types import interrupt, Command

from state import (
    ReportStateInput,
    ReportStateOutput,
    Sections,
    ReportState,
    SectionState,
    SectionOutputState,
    SearchQueries,
    Feedback
)

from prompts import (
    report_researcher_prompt,
    report_planner_prompt,
    section_researcher_prompt,
    section_writer_prompt,
    section_writer_inputs,
    section_grader_prompt,
    introduction_and_conclusion_writer_prompt
)

from config import Config

from utils import (
    format_sections,
    get_current_utc_datetime,
    execute_searches
)



async def plan_report(state: ReportState, config: RunnableConfig) -> dict:
    """
    Plans a report that answers a user's current events-related question
    
    1. Gets report structure from config
    2. Generates search queries with GPT-4.1
    3. Searches with Tavily for the queries
    4. Generates a plan for the report with o4-mini
    
    Parameters:
        state: Graph state with the user's question
        
    Returns:
        dict: Generated sections
    """
    topic = state['topic']
    feedback = state.get('feedback', '')

    configurable = Config.from_runnable_config(config)
    report_structure = configurable.report_structure
    num_queries = configurable.num_queries

    # Search queries LLM
    llm = init_chat_model(model="gpt-4.1", model_provider="openai")
    structured_llm = llm.with_structured_output(SearchQueries)

    system_message = report_researcher_prompt.format(
        current_date_and_time=get_current_utc_datetime(),
        topic=topic,
        report_structure=report_structure,
        num_queries=num_queries
    )

    # Generate queries as a SearchQueries object
    results = structured_llm.invoke(
        [
            SystemMessage(content=system_message),
            HumanMessage(content="Generate search queries that will help in planning the sections of the report.")
        ]
    )

    queries = [query.search_query for query in results.queries]

    search_results = await execute_searches(queries)

    system_message = report_planner_prompt.format(
        current_date_and_time=get_current_utc_datetime(),
        topic=topic,
        report_structure=report_structure,
        context=search_results,
        feedback=feedback
    )

    human_message = """Generate the sections of the report. Your response must include a sections field containing a list of sections. Each section must include name, description, research, and content fields."""
    
    # Report planner LLM
    llm = init_chat_model(model="o4-mini", model_provider="openai")
    structured_llm = llm.with_structured_output(Sections)

    report_sections = structured_llm.invoke([
        SystemMessage(content=system_message),
        HumanMessage(content=human_message)
    ])

    # Get sections
    sections = report_sections.sections

    # Updates sections in the report state
    return {"sections": sections}



def initiate_section_writing(state: ReportState) -> Command[Literal["build_section"]]:
    return Command(goto = [
        Send(
            "build_section",
            {
                "topic": state['topic'],
                "section": section,
                "search_iterations": 0
            }
        )
        for section in state['sections']
        if section.research
    ])



def generate_queries(state: SectionState, config: RunnableConfig):
    """
    Generates search queries  using an LLM based on the section topic and description.
    
    Parameters:
        state: Current section state
        config: Configuration including number of queries to generate
        
    Returns:
        Dict containing the generated search queries
    """

    # Get state 
    topic = state["topic"]
    section = state["section"]

    # Get configuration
    configurable = Config.from_runnable_config(config)
    num_queries = configurable.num_queries

    # Generate queries
    llm = init_chat_model(model="gpt-4.1", model_provider="openai")
    structured_llm = llm.with_structured_output(SearchQueries)

    # Format system instructions
    system_message = section_researcher_prompt.format(
        current_date_and_time=get_current_utc_datetime(),
        topic=topic,
        section_topic=section.description,
        num_queries=num_queries
    )

    # Generate queries  
    queries = structured_llm.invoke([
        SystemMessage(content=system_message),
        HumanMessage(content="Generate search queries on the provided topic.")
    ])

    return {"search_queries": queries.queries}



async def search_web(state: SectionState):
    """
    Executes web searches for the generated queries.

    Parameters:
        state: Current section state with search queries
        
    Returns:
        Dict with search results and updated iteration count
    """

    # Get state
    search_queries = state["search_queries"]

    # Web search
    queries = [query.search_query for query in search_queries]

    # Search the web with parameters
    source_content_str = await execute_searches(queries)

    return {
        "source_content_str": source_content_str,
        "search_iterations": state["search_iterations"] + 1
    }



def write_section(state: SectionState) -> Command[Literal[END, "search_web"]]: # type: ignore
    """
    Writes a section of the report and evaluates if more research is needed.

    (1) Writes the section using the search results.
    (2) Evaluates the quality of the section.
    (3) Completes the section if quality passes and does more research if quality fails.
    
    Args:
        state: Current section state with search results
        
    Returns:
        Command to complete section or do more research
    """

    # Get state 
    topic = state["topic"]
    section = state["section"]
    source_content_str = state["source_content_str"]

    # Format system message
    formatted_section_writer_prompt = section_writer_prompt.format(
        current_date_and_time=get_current_utc_datetime()
    )

    # Format human message
    formatted_section_writer_inputs = section_writer_inputs.format(
        topic=topic,
        section_name=section.name,
        section_topic=section.description,
        context=source_content_str,
        section_content=section.content
    )

    llm = init_chat_model(
        model="gpt-4.1", # gemini-2.5-pro-preview
        model_provider="openai" # google
    )
    section_content = llm.invoke([
        SystemMessage(content=formatted_section_writer_prompt),
        HumanMessage(content=formatted_section_writer_inputs)
    ])
    
    # Write content to the section object  
    section.content = section_content.content

    # Grader prompt
    section_grader_message = "Grade the following section of a news-style report. Consider follow-up questions for missing information. If the grade is 'pass', return empty strings for the follow-up queries. If the grade is 'fail', provide specific search queries to gather the missing information."
    
    formatted_section_grader_prompt = section_grader_prompt.format(
        current_date_and_time=get_current_utc_datetime(),
        topic=topic,
        section_topic=section.description,
        section_content=section.content,
        num_queries=2
    )

    # Reasoning model for feedback
    structured_llm = init_chat_model(model="o4-mini", model_provider="openai").with_structured_output(Feedback)
    feedback = structured_llm.invoke([
        SystemMessage(content=formatted_section_grader_prompt),
        HumanMessage(content=section_grader_message)
    ])

    if feedback.grade == "pass" or state["search_iterations"] >= 0: # 2
        return Command(update={"finished_sections_list": [section]}, goto=END)
    else:
        return  Command(update={"search_queries": feedback.follow_up_queries, "section": section}, goto="search_web")



def write_intro_and_conclusion(state: SectionState):
    """
    Write the intro and conclusion.
    
    Handles introduction and conclusion sections and summaries that use researched sections as context.
    
    Parameters:
        state: Current section state with finished  sections as context

    Returns:
        Dict containing the newly written section
    """

    topic = state["topic"]
    section = state["section"]
    finished_sections = state["finished_sections_str"]
    
    # Format system instructions
    system_message = introduction_and_conclusion_writer_prompt.format(
        current_date_and_time=get_current_utc_datetime(),
        topic=topic,
        section_name=section.name,
        section_topic=section.description,
        context=finished_sections
    )

    # gemini-2.5-pro-exp-03-25
    # google
    llm = init_chat_model(model="gpt-4.1", model_provider="openai")
    
    section_content = llm.invoke([
        SystemMessage(content=system_message),
        HumanMessage(content="Write a section of a report that answers a user's current events question using the information you were provided.")
    ])
    
    # Write content to the section object
    section.content = section_content.content

    return {"finished_sections_list": [section]}



def format_sections_as_string(state: ReportState) -> dict:
    """
    Formats finished sections as a string to be used as context for writing the introduction and conclusion.
    
    Parameters:
        state: Current report state
        
    Returns:
        Dict with formatted sections as context
    """
    return {"finished_sections_str": format_sections(state["finished_sections_list"])}



def initiate_intro_and_conclusion_writing(state: ReportState):
    """
    Creates parallel tasks to write non-researched sections (i.e. the introduction and conclusion).
    
    EDGE

    Identifies sections that don't need independent research and creates parallel tasks to write them.
    
    Parameters:
        state: Current report state with finished sections
        
    Returns:
        List of Send commands for parallelized section writing
    """

    # Writes sections that do not require research in parallel via Send()
    return [
        Send(
            "write_intro_and_conclusion",
            {
                "topic": state["topic"],
                "section": section,
                "finished_sections_str": state["finished_sections_str"]
            }
        ) 
        for section in state["sections"] 
        if not section.research
    ]



def compile_report(state: ReportState):
    """
    Compiles all sections of the report.
    
    1. Gets all sections of the report.
    2. Orders them according to the plan
    3. Combines them into a report.
    
    Parameters:
        state: Current report state with all the sections finished
        
    Returns:
        Dict containing the complete report
    """

    # Get sections
    sections = state["sections"]
    finished_sections = {section.name: section.content for section in state["finished_sections_list"]}

    # Update sections with finished content in the original order
    for section in sections:
        if section.name in finished_sections:
            section.content = finished_sections[section.name]

    # Compile report
    report = "\n\n".join([section.content for section in sections])

    return {"finished_report": report}



# SUB-GRAPH 
section_builder = StateGraph(SectionState, output=SectionOutputState)
# Add nodes
section_builder.add_node("generate_queries", generate_queries)
section_builder.add_node("search_web", search_web)
section_builder.add_node("write_section", write_section)
# Add edges
section_builder.add_edge(START, "generate_queries")
section_builder.add_edge("generate_queries", "search_web")
section_builder.add_edge("search_web", "write_section")

# GRAPH
builder = StateGraph(ReportState, input=ReportStateInput, output=ReportStateOutput)
# Add nodes
builder.add_node("plan_report", plan_report)
builder.add_node("initiate_section_writing", initiate_section_writing)
builder.add_node("build_section", section_builder.compile())
builder.add_node("format_sections_as_string", format_sections_as_string)
builder.add_node("write_intro_and_conclusion", write_intro_and_conclusion)
builder.add_node("compile_report", compile_report)
# Add edges
builder.add_edge(START, "plan_report")
builder.add_edge("plan_report", "initiate_section_writing")
builder.add_edge("build_section", "format_sections_as_string")
builder.add_conditional_edges("format_sections_as_string", initiate_intro_and_conclusion_writing, ["write_intro_and_conclusion"])
builder.add_edge("write_intro_and_conclusion", "compile_report")
builder.add_edge("compile_report", END)
# Build graph
graph = builder.compile()