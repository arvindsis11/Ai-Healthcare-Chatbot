from .vector_db import VectorDatabase
from .llm_service import LLMService
from typing import List, Dict, Any, Optional

class RAGService:
    def __init__(self, vector_db: VectorDatabase, llm_service: LLMService):
        self.vector_db = vector_db
        self.llm_service = llm_service

    def query(self, question: str, n_results: int = 3) -> Dict[str, Any]:
        """Perform RAG query: retrieve relevant docs and generate response."""
        # Search for relevant documents
        search_results = self.vector_db.search(question, n_results=n_results)

        # Extract document contents
        contexts = []
        sources = []

        if search_results['documents']:
            for doc, metadata in zip(
                search_results['documents'][0],
                search_results['metadatas'][0]
            ):
                contexts.append(doc)
                sources.append(metadata.get('source', 'unknown'))

        # Generate response using LLM with context
        response = self.llm_service.generate_response(question, contexts)

        return {
            'response': response,
            'sources': sources,
            'contexts': contexts
        }

    def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        """Add new documents to the vector database."""
        self.vector_db.add_documents(documents)

    def clear_documents(self) -> None:
        """Clear all documents from the vector database."""
        self.vector_db.clear_collection()