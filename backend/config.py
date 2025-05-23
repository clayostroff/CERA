# import os
# from dataclasses import dataclass, fields
# from textwrap import dedent
# from typing import Any, Optional, Dict

# from langchain_core.language_models.chat_models import BaseChatModel
# from langchain_core.runnables import RunnableConfig

# from dataclasses import dataclass

# REPORT_STRUCTURE = dedent("""
#     (1) Introduction to the topic:
#         * Brief overview of matter at hand
#         * No research needed
#     (2) Main body sections:
#         * Research needed
#         * Each section should focus on a sub-topic that helps answer the user's question
#     (3) Conclusion or summary:
#         * Should include key take-aways
#         * No research needed
# """)

# @dataclass(kw_only=True)
# class Config:
#     report_structure: str = REPORT_STRUCTURE
#     planning_queries: int = 2 # Report planning queries
#     queries_per_section: int = 2 # Number of search queries per section
#     num_follow_up_queries: int = 0 # Number of follow-up search queries per iteration
#     max_follow_up_iterations: int = 0 # Maximum number of follow-up search iterations per section

#     @classmethod
#     def from_runnable_config(cls, config: Optional[RunnableConfig] = None) -> "Config":
#         """
#         Creates a Config instance from a RunnableConfig.
#         """
#         configurable = (
#             config["configurable"] if config and "configurable" in config
#             else {}
#         )
#         values: dict[str, Any] = {
#             f.name: os.environ.get(f.name.upper(), configurable.get(f.name))
#             for f in fields(cls)
#             if f.init
#         }
#         return cls(**{k: v for k, v in values.items() if v})