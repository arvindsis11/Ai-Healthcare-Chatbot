from .text_processing import load_yaml_files, chunk_text
from ..repositories.vector_db import VectorDatabase
from typing import List, Dict, Any

class DataIngestionPipeline:
    def __init__(self, vector_db: VectorDatabase):
        self.vector_db = vector_db

    def process_medical_content(self, content: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process medical content with enhanced chunking for healthcare data."""
        processed_docs = []

        # Metadata-based routing for processing
        content_type = metadata.get('type', 'unknown')

        # 1. For conversation pairs, we keep the Q&A unit intact
        if content_type == 'conversation':
            processed_docs.append({
                'content': content.strip(),
                'metadata': {
                    **metadata,
                    'chunk_type': 'qa_pair',
                    'content_length': len(content)
                }
            })
        
        # 2. For longer medical literature or abstracts (e.g., PubMed)
        elif content_type == 'medical_abstract' or len(content.split()) > 300:
            chunks = chunk_text(content, chunk_size=250, overlap=50)
            for chunk in chunks:
                processed_docs.append({
                    'content': chunk.strip(),
                    'metadata': {
                        **metadata,
                        'chunk_type': 'text_chunk',
                        'content_length': len(chunk)
                    }
                })
        
        # 3. Default for other short documents
        else:
            processed_docs.append({
                'content': content.strip(),
                'metadata': {
                    **metadata,
                    'chunk_type': 'full_text',
                    'content_length': len(content)
                }
            })

        return processed_docs

    def ingest_data(self, data_dir: str) -> None:
        """Ingest all data from the data directory with medical-specific processing."""
        print("Loading YAML files...")
        documents = load_yaml_files(data_dir)

        print(f"Found {len(documents)} raw documents")

        # Process documents with medical-specific logic
        processed_docs = []
        for doc in documents:
            medical_docs = self.process_medical_content(doc['content'], doc['metadata'])
            processed_docs.extend(medical_docs)

        print(f"Processed into {len(processed_docs)} medical content chunks")

        # Add to vector database
        print("Adding to vector database...")
        self.vector_db.add_documents(processed_docs)
        print("Ingestion complete!")

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the ingested medical data."""
        documents = self.vector_db.get_all_documents()
        topics = {}
        chunk_types = {}

        for doc in documents:
            # Topic statistics
            topic = doc['metadata'].get('topic', 'unknown')
            topics[topic] = topics.get(topic, 0) + 1

            # Chunk type statistics
            chunk_type = doc['metadata'].get('chunk_type', 'unknown')
            chunk_types[chunk_type] = chunk_types.get(chunk_type, 0) + 1

        return {
            'total_documents': len(documents),
            'topics': topics,
            'chunk_types': chunk_types,
            'avg_content_length': sum(doc['metadata'].get('content_length', 0) for doc in documents) / len(documents) if documents else 0
        }