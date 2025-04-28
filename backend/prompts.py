report_researcher_prompt = """You're doing research for a news-style report that will answer a user's current events-related question.

CURRENT DATE AND TIME: {current_date_and_time}

<REPORT TOPIC>
{topic}
</REPORT TOPIC>

<REPORT STRUCTURE>
{report_structure}
</REPORT STRUCTURE>

<CONTEXT>
Web search results from just the user's question:
{context}
</CONTEXT>

<TASK>
Your goal is to generate {num_queries} web search queries that will help find information for planning the report's sections. 

Your queries should (1) be related to REPORT TOPIC and (2) help satisfy the requirements specified in REPORT STRUCTURE.

The queries should help find high-quality, relevant sources that cover the breadth needed to satisfy the report structure.
</TASK>

<FORMAT>
Call the SearchQueries tool.
</FORMAT>"""



report_planner_prompt = """Write a plan for a news-style, all-you-need-to-know report (e.g. something that would be found on cnn.com or nytimes.com) that answers the user's current events-related question. The report should cover all important information while being concise and focused.

CURRENT DATE AND TIME: {current_date_and_time}

<REPORT TOPIC>
{topic}
</REPORT TOPIC>

<REPORT STRUCTURE>
Refer to this general structure. Feel free to alter it as you see fit to better address the user's question.
{report_structure}
</REPORT STRUCTURE>

<CONTEXT>
Context to help plan the sections of the report: 
{context}
</CONTEXT>

<TASK>
Generate a list of sections for the report. Your plan should be concise and focused, with no overlapping sections or unnecessary filler. LONGER DOES NOT EQUAL BETTER. MORE SECTIONS DOES NOT EQUAL BETTER.

For example, a good report could, though not necessarily, look like this:
(1) Introduction
(2) Overview of sub-topic 1
(3) Overview of sub-topic 2
(4) Summary.

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

<FORMAT>
Call the Sections tool 
</FORMAT>"""



section_researcher_prompt = """You are an assistant tasked with crafting targeted web search queries that will help gather comprehensive information for writing a section of a news-style report that answers a user's current events-related question.

CURRENT DATE AND TIME: {current_date_and_time}

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

Design the queries to find high-quality, relevant sources.
</TASK>

<FORMAT>
Call the SearchQueries tool 
</FORMAT>"""



section_writer_prompt = """Write one section of a news-style report that answers a user's current events-related question.

CURRENT DATE AND TIME: {current_date_and_time}

<Task>
1. Review the report topic, section name, and section topic carefully.
2. Review any already-written section content, then look at the provided source material.
3. Decide which sources you will use to write the section. You do not have to use every source.
4. Write the section and list your sources. 
</Task>

<Writing Guidelines>
* If there's not existing content for the section, write from scratch.
* If there is existing content, consider it when writing.
* Use clear language.
* Use short paragraphs (2-4 sentences).
* Use ## for section title (Markdown format).
* Write no fewer than 100 words but no more than 200 words.
</Writing Guidelines>

<Citations>
* Assign each unique URL a single citation number in your response.
* End with "### Sources" listing each source with corresponding numbers.
* Number sources sequentially without gaps (e.g. 1, 2, 3) regardless of which you choose.
* Source should be formatted as a Markdown list item with "-".
* Example:
  "- [1] Source Title (URL)"
  "- [2] Source Title (URL)"
  "- [3] Source Title (URL)"
</Citations>

<Final Check>
(1) Confirm each URL appears only once in the source list.
(2) Verify that your claims are grounded in the provided source material.
(3) Ensure that sources are numbered sequentially (e.g. 1, 2, 3) without gaps.
(4) Ensure that each source is listed on its own new line.
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



section_grader_prompt = """Review a section of a news-style report relative to the user's current events-related question.

CURRENT DATE AND TIME: {current_date_and_time}

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



introduction_and_conclusion_writer_prompt = """You are a reporter writing a section of a NEWS-STYLE REPORT about a current event that synthesizes information from the rest of the report. You could be tasked with writing an introduction, a conclusion, or a summary, though only one of these (i.e. just an introduction, just a conclusion, or just a summary). 

CURRENT DATE AND TIME: {current_date_and_time}

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
* Completely avoid being meta (i.e. NEVER reference the report or section you're writing).
* DON'T USE PHRASES SUCH AS: "this report", "this assessment", etc.
* Focus on the most important points and key takeaways.
* Use specific examples over general statements.
* Obey word counts.

If you're tasked with writing an introduction:
* Use # for the report title (Markdown format).
* The report title can and likely should be different from the report topic.
* Write in clear and simple language.
* Focus on important information.
* Use between 50 and 125 words.
* No sources section.

If you're tasked with writing a conclusion or summary:
* Use ## for the section title (Markdown format).
* Provide specific implications.
* Use between 50 and 125 words.
* No sources section.
</TASK>

<FINAL CHECK>
* Introduction: (1) between 50 and 125 words, (2) # for the report title, (3) no sources section.
* Conclusion: (1) between 50 and 125 words, (2) ## for the section title, (3) no sources section.
* Do not include any preamble in your response.
* Do not include or reference word counts.
* Use Markdown format.
* NEVER reference the report itself or the section you're writing (i.e. don't be meta).
</FINAL CHECK>"""