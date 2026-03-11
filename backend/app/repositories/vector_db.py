import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import uuid
from pathlib import Path

class VectorDatabase:
    def __init__(self, persist_directory: str, collection_name: str):
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(exist_ok=True)
        self.collection_name = collection_name

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=str(self.persist_directory),
            settings=Settings(anonymized_telemetry=False)
        )

        # Initialize embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

        # Get or create collection
        try:
            self.collection = self.client.get_collection(name=collection_name)
        except Exception:
            self.collection = self.client.create_collection(name=collection_name)

    def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        """Add documents to the vector database."""
        ids = []
        embeddings = []
        metadatas = []
        contents = []

        for i, doc in enumerate(documents):
            content = doc['content']
            metadata = doc.get('metadata', {})

            # Generate embedding
            embedding = self.embedding_model.encode(content).tolist()

            ids.append(str(uuid.uuid4()))
            embeddings.append(embedding)
            metadatas.append(metadata)
            contents.append(content)

        self.collection.add(
            embeddings=embeddings,
            documents=contents,
            metadatas=metadatas,
            ids=ids
        )

    def search(self, query: str, n_results: int = 5) -> Dict[str, Any]:
        """Search for similar documents."""
        query_embedding = self.embedding_model.encode(query).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        return results

    def get_all_documents(self) -> List[Dict[str, Any]]:
        """Retrieve all documents from the collection."""
        results = self.collection.get(include=['documents', 'metadatas'])
        documents = []

        for doc, metadata in zip(results['documents'], results['metadatas']):
            documents.append({
                'content': doc,
                'metadata': metadata
            })

        return documents

    def clear_collection(self) -> None:
        """Clear all documents from the collection."""
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.create_collection(name=self.collection_name)