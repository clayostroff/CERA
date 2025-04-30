import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager
import json

from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
import uvicorn

from graph import graph
from state import ReportInputState

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    missing_keys = [k for k in ("OPENAI_API_KEY", "TAVILY_API_KEY") if not os.getenv(k)]
    if missing_keys:
        raise RuntimeError(f"Missing API keys: {', '.join(missing_keys)}")
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://cera.clayostroff.com",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", status_code=200)
def root():
    return {"status": "OK"}

@app.get("/report")
async def stream_report(topic: str, request: Request):
    """
    SSE endpoint that streams updates as the graph runs.
    """

    input_state = ReportInputState(topic=topic)

    async def event_generator():
        try:
            # https://langchain-ai.github.io/langgraph/how-tos/streaming-subgraphs/
            async for update in graph.astream(input_state, stream_mode="updates", subgraphs=True):
                if await request.is_disconnected():
                    break
                node, diff = next(iter(update[1].items()))
                payload = {
                    "node": node,
                    "diff": jsonable_encoder(diff)
                }
                yield {
                    "event": "step",
                    "data": json.dumps(payload)
                }
        except Exception as e:
            yield {
                "event": "error",
                "data": {"error": str(e)}
            }

    return EventSourceResponse(event_generator())

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)