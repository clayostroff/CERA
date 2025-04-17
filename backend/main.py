import asyncio
import os
from dotenv import load_dotenv

from graph import graph
from state import ReportStateInput

async def run_agent(topic: str):

    # API keys
    load_dotenv()
    if not os.getenv("GOOGLE_API_KEY") or not os.getenv("OPENAI_API_KEY") or not os.getenv("TAVILY_API_KEY"):
        print("ERROR: GOOGLE_API_KEY, OPENAI_API_KEY, and TAVILY_API_KEY must be set")
        return

    # Prepare the input
    inputs: ReportStateInput = {"topic": topic}

    # Invoke the graph with ainvoke() because the graph contains async steps
    try:
        state = await graph.ainvoke(inputs)
        # Print the report
        print("\n")
        print(state["finished_report"])
        print("\n")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    report_topic = "Trump tariffs"
    asyncio.run(run_agent(report_topic))