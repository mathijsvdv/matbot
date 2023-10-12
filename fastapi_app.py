from http import HTTPStatus
from typing import Dict

from fastapi import FastAPI
from pydantic import BaseModel

from constants import llm_chain, llm_name


class Message(BaseModel):
    content: str


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
async def _chat(message: Message) -> Dict:
    content = message.content
    try:
        # Call the chain asynchronously
        res = await llm_chain.acall(content)
    except NotImplementedError:
        # If the chain does not support asynchronous calls, fallback to synchronous
        res = llm_chain(content)

    return res
