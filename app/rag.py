import chromadb
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from app.config import Config

class RAGPipeline:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=Config.VECTOR_DB_PATH)
        self.collection = self.client.get_or_create_collection("terraform_knowledge")
        self.embeddings = OpenAIEmbeddings()

    def retrieve_context(self, query: str) -> str:
        results = self.collection.query(
            query_texts=[query],
            n_results=3
        )
        contexts = [doc["text"] for doc in results["documents"][0]]
        return "\n".join(contexts) if contexts else "No relevant information found."

rag_pipeline = RAGPipeline()
