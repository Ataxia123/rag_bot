# from langchain.embeddings import HuggingFaceBgeEmbeddings
# from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

# import ollama


# Embedder
class EmbeddingFunction:
    def __init__(self):
        self.embedder = FastEmbedEmbeddings()

    # else:
    #     self.embedder = self.default_method
