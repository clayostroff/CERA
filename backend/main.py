import asyncio
import os
from dotenv import load_dotenv

# Adjust the import path based on your project structure if needed
from graph import graph 
from state import ReportStateInput

async def run_agent(topic: str):
    """Runs the LangGraph agent for a given topic."""
    print(f"Running agent for topic: {topic}\n{'-'*30}")

    # Ensure API keys are loaded
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY") or not os.getenv("TAVILY_API_KEY"):
        print("ERROR: OPENAI_API_KEY and TAVILY_API_KEY must be set in the .env file.")
        return

    # Prepare the input
    inputs: ReportStateInput = {"topic": topic}

    # Invoke the graph
    # Use .ainvoke() because the graph contains async steps
    try:
        final_state = await graph.ainvoke(inputs)

        # Print the final report
        print(f"\n{'-'*30}\nFinal Report:\n{'-'*30}")
        print(final_state["finished_report"])

    except Exception as e:
        print(f"An error occurred during agent execution: {e}")
        # Add more specific error handling if needed

if __name__ == "__main__":
    # --- Replace with your desired topic --- 
    report_topic = "Trump tariffs"
    # ----------------------------------------

    asyncio.run(run_agent(report_topic)) 