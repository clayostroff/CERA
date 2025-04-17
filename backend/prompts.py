report_researcher_prompt = """You're doing research for a report that will answer a user's current events-related question.

<REPORT TOPIC>
{topic}
</REPORT TOPIC>

<REPORT STRUCTURE>
{report_structure}
</REPORT STRUCTURE>

<TASK>
Your goal is to generate {num_queries} web search queries that will help find information for planning the report's sections. 

The queries you generate should:
(1) Be related to REPORT TOPIC.
(2) Help satisfy the requirements specified in REPORT STRUCTURE.

Make the queries specific enough to find high-quality, relevant sources while still covering the breadth needed for the report structure.
</TASK>

<FORMAT>
Call the SearchQueries tool.
</FORMAT>"""



report_planner_prompt = """Write a plan for a report that is concise and focused.

<REPORT TOPIC>
The topic of the report is: {topic}
</REPORT TOPIC>

<REPORT STRUCTURE>
The report should follow this structure:
{report_structure}
</REPORT STRUCTURE>

<CONTEXT>
The following is context to help you plan the sections of the report: 
{context}
</CONTEXT>

<TASK>
Generate a list of sections for the report. Your plan should be focused, with no overlapping sections or unnecessary filler.

For example, a good report structure COULD (though not necessarily) look like:
(1) introduction
(2) overview of sub-topic a
(3) overview of sub-topic b
(4) comparison of a and b
(5) conclusion


Fields (each section should have the following):
* name: Name for this section of the report.
* description: Brief overview of the main topics covered in this section.
* research: Whether (or not) to perform research for this section of the report.
* content: Content of the section (which you will leave blank for now).

Guidelines:
* Include examples and implementation details within main topic sections, not as separate sections.
* Ensure each section has a distinct purpose with no content overlap between sections.
* Combine related topics rather than separating them.

Before returning your response, review your structure to ensure it has a logical flow and no redundant sections.
</TASK>

<FEEDBACK>
Here is feedback on the report structure (if any):
{feedback}
</FEEDBACK>

<FORMAT>
Call the Sections tool 
</FORMAT>"""



section_researcher_prompt = """You are an expert researcher crafting targeted web search queries that will gather comprehensive information for writing a section of a report that answers a user's question.

<REPORT TOPIC>
{topic}
</REPORT TOPIC>

<SECTION TOPIC>
{section_topic}
</SECTION TOPIC>

<TASK>
Your goal is to generate {num_queries} search queries that will help gather comprehensive information about the section's topic.

The queries should:
(1) Be related to the section's topic.
(2) Examine different aspects of the section's topic.

Make the queries specific enough to find high-quality, relevant sources.
</TASK>

<FORMAT>
Call the SearchQueries tool 
</FORMAT>"""



section_writer_prompt = """Write one section of a research report that answers a user's question.

<Task>
1. Review the report topic, section name, and section topic carefully.
2. If present, review any already-written section content. 
3. Then, look at the provided source material.
4. Decide which sources you will use to write the section.
5. Write the section and list your sources. 
</Task>

<Writing Guidelines>
* If there's not existing content for the section, write from scratch.
* If there is existing content, consider it when writing the section.
* Don't write fewer than 100 words or more than 300 words.
* Use clear language.
* Use short paragraphs (2-4 sentences).
* Use ## for section title (Markdown format).
</Writing Guidelines>

<Citations>
* Assign each unique URL a single citation number in your response.
* End with "### Sources" listing each source with corresponding numbers.
* Number sources sequentially without gaps (1, 2, 3, ...) in the list regardless of which sources you choose.
* Example:
  [1] Source Title (URL)
  [2] Source Title (URL)
</Citations>

<Final Check>
(1) Verify that every claim is grounded in the provided source material.
(2) Confirm each URL appears only once in the source list.
(3) Verify that sources are numbered sequentially (1, 2, 3, ...) without any gaps.
</Final Check>"""



section_writer_inputs = """<REPORT TOPIC>
{topic}
</REPORT TOPIC>

<SECTION NAME>
{section_name}
</SECTION NAME>

<SECTION TOPIC>
{section_topic}
</SECTION TOPIC>

<EXISTING SECTION CONTENT>
{section_content}
</EXISTING SECTION CONTENT>

<SOURCE MATERIAL>
{context}
</SOURCE MATERIAL>"""



section_grader_prompt = """Review a section of a reseach report relative to the specified topic:

<REPORT TOPIC>
{topic}
</REPORT TOPIC>

<SECTION TOPIC>
{section_topic}
</SECTION TOPIC>

<SECTION CONTENT>
{section_content}
</SECTION CONTENT>

<TASK>
Evaluate whether the section content adequately addresses the section topic.

If the section content does not adequately address the section topic, generate {num_queries} follow-up search queries to gather missing information.
</TASK>

<FORMAT>
Call the Feedback tool and output according to the following schema:

grade: Literal["pass", "fail"] = Field(
    description="Evaluation indicating whether the response is satisfactory (pass) or needs revision (fail)."
)
follow_up_queries: List[SearchQuery] = Field(
    description="List of follow-up search queries.",
)
</FORMAT>"""



introduction_and_conclusion_writer_prompt = """You are a writer making a section of a report that synthesizes information from the rest of the report. Completely avoid being meta (i.e. do not reference the report or the section you're writing). Thus, DON'T USE PHRASES SUCH AS BUT NOT LIMITED TO: "this report", "this assessment", etc.

<REPORT TOPIC>
{topic}
</REPORT TOPIC>

<SECTION NAME>
{section_name}
</SECTION NAME>

<SECTION TOPIC> 
{section_topic}
</SECTION TOPIC>

<REPORT CONTENT>
{context}
</REPORT CONTENT>

<TASK>
Guidelines:

For Introduction:
* Use # for the report title (Markdown format).
* Should be between 50 and 200 words.
* Write in clear and simple language.
* Focus on important information.
* NO SOURCES SECTION NEEDED.

For Conclusion/Summary:
* Use ## for section title (Markdown format)
* Should be between 50 and 200 words.
* End with specific implications.
* NO SOURCES SECTION NEEDED.

Writing Approach:
* Obey word counts.
* Use specific examples not general statements.
* Focus on the most the important points and key takeaways.
</TASK>

<FINAL CHECK>
* For Introduction: between 50 and 200 words; # for the report title; no sources section.
* For Conclusion/Summary: between 50 and 200 words; ## for the section title; no sources section.
* Use Markdown format.
* Do not include any preamble in your response.
* Do not include or reference word counts.
</FINAL CHECK>"""