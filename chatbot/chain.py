from langchain.docstore.document import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.retrievers import BM25Retriever
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter
from langchain_core.runnables import (
    RunnableLambda,
    RunnablePassthrough,
    RunnableSequence,
    RunnableMap,
)

from common import load_prompt


def create_retriever(documents):
    docs = [
        Document(page_content=doc["content"], metadata=doc["metadata"])
        for doc in documents
    ]

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=10)
    split_documents = text_splitter.split_documents(docs)

    kiwi_bm25 = BM25Retriever.from_documents(
        split_documents,
        k=3,
    )

    return kiwi_bm25


def create_chain(retriever, memory):
    extract_chat_history = RunnableLambda(
        lambda inputs: memory.load_memory_variables(inputs)
    ) | itemgetter("chat_history")
    extract_context = RunnableLambda(
        lambda inputs: retriever.invoke(inputs["question"])
    )
    pass_question = RunnablePassthrough()
    prompt = load_prompt("./prompts/prompt.yaml", encoding="utf-8")
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0)

    chain = prompt | llm | StrOutputParser()
    runnable_map = RunnableMap(
        {
            "chat_history": extract_chat_history,
            "context": extract_context,
            "question": pass_question,
        }
    )
    runnable_chain = RunnableSequence(runnable_map, chain)
    return runnable_chain
