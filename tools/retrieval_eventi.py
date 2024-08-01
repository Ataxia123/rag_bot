from langchain.agents import Tool
import os
from utils import database_managers
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

# embedding = embedding.EmbeddingFunction().embedder


def combine_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def get_relevant_document(question: str) -> str:

    vectore_store = database_managers.QDrantDBManager(
        url=os.getenv("QDRANT_URL"),
        port=6333,
        collection_name="web-places",
        vector_size=386,  # ??
        embedding=FastEmbedEmbeddings(),
        record_manager_url=r"sqlite:///record_manager_cache.sql",
    )
    vectore_store_client = vectore_store.vector_store
    retriever = vectore_store_client.as_retriever()
    retrieved_docs = retriever.invoke(question)
    total_content = combine_docs(retrieved_docs)

    return total_content


get_relevant_document_tool = Tool(
    name="Web eventi",
    func=get_relevant_document,
    description="A database for a Dungeons and Dragons adventure",
)
