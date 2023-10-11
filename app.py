import chainlit as cl

from constants import llm_chain


@cl.on_chat_start
def main():
    # Store the chain in the user session
    cl.user_session.set("llm_chain", llm_chain)


@cl.on_message
async def main(message: str):
    # Retrieve the chain from the user session
    llm_chain = cl.user_session.get("llm_chain")  # type: RetrievalQA

    try:
        # Call the chain asynchronously
        res = await llm_chain.acall(message, callbacks=[cl.AsyncLangchainCallbackHandler()])
    except NotImplementedError:
        # If the chain does not support asynchronous calls, fallback to synchronous
        res = llm_chain(message, callbacks=[cl.LangchainCallbackHandler()])

    # Do any post processing here

    # "res" is a Dict. For this chain, we get the response by reading the "text" key.
    # This varies from chain to chain, you should check which key to read.
    await cl.Message(content=res["result"]).send()
