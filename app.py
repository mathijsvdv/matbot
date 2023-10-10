import chainlit as cl
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import RetrievalQA
from langchain.embeddings.ollama import OllamaEmbeddings
from langchain.llms import Ollama, OpenAI
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Chroma

llms = {
    "openai": OpenAI(temperature=0),
    "mistral": Ollama(
        model="mistral", verbose=True, callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
    ),
}

persist_directory = "./docs/chroma"
embedding = OllamaEmbeddings(model="mistral")
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)

template = """You are a Retrieval-Augmented Generation chatbot that answers questions on
documents provided to you. Act as an expert in the subject matter of the document
discussed. If a question is not relevant for the document or if it cannot be answered
using the information of the document, please do not answer the question and politely provide
the reason.
Document: {context}

Question: {question}
Helpful Answer:"""


@cl.on_chat_start
def main():
    # Instantiate the chain for that user session
    prompt = PromptTemplate.from_template(template)
    llm_chain = RetrievalQA.from_chain_type(
        llm=llms["mistral"],
        retriever=vectordb.as_retriever(),
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt, "verbose": True},
    )

    # Store the chain in the user session
    cl.user_session.set("llm_chain", llm_chain)


@cl.on_message
async def main(message: str):
    # Retrieve the chain from the user session
    llm_chain = cl.user_session.get("llm_chain")  # type: LLMChain

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
