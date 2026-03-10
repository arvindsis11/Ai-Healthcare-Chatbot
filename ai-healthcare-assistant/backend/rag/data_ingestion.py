from ..utils.text_processing import load_yaml_files, chunk_text
from ..services.vector_db import VectorDatabase
from typing import List, Dict, Any

class DataIngestionPipeline:
    def __init__(self, vector_db: VectorDatabase):
        self.vector_db = vector_db

    def ingest_data(self, data_dir: str) -> None:
        """Ingest all data from the data directory."""
        print("Loading YAML files...")
        documents = load_yaml_files(data_dir)

        print(f"Found {len(documents)} documents")

        # Process documents (chunk if needed)
        processed_docs = []
        for doc in documents:
            content = doc['content']

            # For conversation data, we can keep as is or chunk
            if len(content.split()) > 500:  # If longer than 500 words
                chunks = chunk_text(content, chunk_size=400, overlap=50)
                for chunk in chunks:
                    processed_docs.append({
                        'content': chunk,
                        'metadata': doc['metadata']
                    })
            else:
                processed_docs.append(doc)

        print(f"Processed into {len(processed_docs)} chunks")

        # Add to vector database
        print("Adding to vector database...")
        self.vector_db.add_documents(processed_docs)
        print("Ingestion complete!")

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the ingested data."""
        documents = self.vector_db.get_all_documents()
        topics = {}

        for doc in documents:
            topic = doc['metadata'].get('topic', 'unknown')
            topics[topic] = topics.get(topic, 0) + 1

        return {
            'total_documents': len(documents),
            'topics': topics
        }