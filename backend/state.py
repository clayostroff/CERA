from typing import Annotated, Literal, TypedDict, Optional
from pydantic import BaseModel, Field
import operator

class Section(BaseModel):
    name: str = Field(
        description="Name for this section of the report."
    )
    description: str = Field(
        description="Overview of the main topics and key points to be covered in this section."
    )
    research: bool = Field(
        description="Whether independent research is needed for this section of the report."
    )
    content: str = Field(
        description="The content of the section."
    )

class Sections(BaseModel):
    sections: list[Section] = Field(
        description="Sections of the report."
    )

class SearchQuery(BaseModel):
    search_query: str = Field(
        description="Query for web search."
    )

class SearchQueries(BaseModel):
    queries: list[SearchQuery] = Field(
        description="List of search queries."
    )

class Feedback(BaseModel):
    grade: Literal['pass', 'fail'] = Field(
        description="Evaluation indicating whether the response is satisfactory (pass) or needs revision (fail)."
    )
    follow_up_queries: list[SearchQuery] = Field(
        description="List of follow-up search queries."
    )

class ReportInputState(TypedDict):
    topic: str # Report topic
    
class ReportOutputState(TypedDict):
    finished_report: str # Finished report

class ReportState(TypedDict):
    topic: str # Report topic
    # For giving feedback on the report plan. Can be used to implement human-in-the-loop.
    # feedback: str
    sections: list[Section] # List of report sections
    finished_sections_list: Annotated[list[Section], operator.add] # Send() key
    finished_sections_str: str # String of finished sections used to write final sections
    finished_report: str # Finished report

class SectionState(TypedDict):
    topic: str # Report topic
    section: Section # Report section
    search_queries: list[SearchQuery] # List of search queries
    search_iterations: int # Number of search iterations that have been done
    source_content_str: str # String of formatted source content from web search
    finished_sections_list: list[Section] # Final key duplicated in outer state for Send()
    finished_sections_str: str # String of finished sections used to write final sections

class SectionOutputState(TypedDict):
    finished_sections_list: list[Section] # Final key duplicated in outer state for Send()