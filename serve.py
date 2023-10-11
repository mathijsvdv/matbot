from http import HTTPStatus
from typing import Dict

from fastapi import FastAPI

from constants import llm_chain, llm_name

# Define application
app = FastAPI(
    title="MatBot",
    description="Answer questions about your documents.",
    version="0.1",
)


@app.get("/")
def _index() -> Dict:
    """Health check."""
    response = {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": {},
    }
    return response


@app.get("/llm/")
def _llm() -> Dict:
    """Get the LLM used."""
    return {"llm": llm_name}


@app.post("/chat/")
async def _chat(message: str) -> Dict:
    try:
        # Call the chain asynchronously
        res = await llm_chain.acall(message)
    except NotImplementedError:
        # If the chain does not support asynchronous calls, fallback to synchronous
        res = llm_chain(message)

    return res
