import chainlit as cl
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

template = """You are a Retrieval-Augmented Generation chatbot that answers questions on
documents provided to you. Act as an expert in the subject matter of the document
discussed. If a question is not relevant for the document or if it cannot be answered
using the information of the document, please do not answer the question and provide
the reason. You're going to be working with the following document:
{document}

Given the above document, please answer the following question:
{{question}}
"""

document_path = "data/business_1.txt"
with open(document_path) as f:
    document = f.read()


@cl.on_chat_start
def main():
    # Instantiate the chain for that user session
    prompt = PromptTemplate.from_template(template.format(document=document))
    llm_chain = LLMChain(prompt=prompt, llm=OpenAI(temperature=0), verbose=True)

    # Store the chain in the user session
    cl.user_session.set("llm_chain", llm_chain)


@cl.on_message
async def main(message: str):
    # Retrieve the chain from the user session
    llm_chain = cl.user_session.get("llm_chain")  # type: LLMChain

    # Call the chain asynchronously
    res = await llm_chain.acall(message, callbacks=[cl.AsyncLangchainCallbackHandler()])

    # Do any post processing here

    # "res" is a Dict. For this chain, we get the response by reading the "text" key.
    # This varies from chain to chain, you should check which key to read.
    await cl.Message(content=res["text"]).send()
