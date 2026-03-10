#!/usr/bin/env python3
"""
Vector Store for Healthcare RAG System
Manages ChromaDB operations for medical embeddings.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import json
import numpy as np
from tqdm import tqdm
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

class MedicalVectorStore:
    """Vector store for medical embeddings using ChromaDB."""

    def __init__(self,
                 persist_directory: str = "./embeddings",
                 collection_name: str = "medical_knowledge",
                 embedding_model: str = "all-MiniLM-L6-v2"):
        """
        Initialize the vector store.

        Args:
            persist_directory: Directory to persist ChromaDB data
            collection_name: Name of the ChromaDB collection
            embedding_model: Embedding model name
        """
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(exist_ok=True)
        self.collection_name = collection_name

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=str(self.persist_directory),
            settings=Settings(anonymized_telemetry=False)
        )

        # Use sentence transformer embedding function
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=embedding_model
        )

        # Get or create collection
        try:
            self.collection = self.client.get_collection(
                name=collection_name,
                embedding_function=self.embedding_function
            )
            print(f"Loaded existing collection: {collection_name}")
        except:
            self.collection = self.client.create_collection(
                name=collection_name,
                embedding_function=self.embedding_function
            )
            print(f"Created new collection: {collection_name}")

    def add_documents(self, documents: List[Dict[str, Any]], batch_size: int = 100) -> None:
        """
        Add documents to the vector store.

        Args:
            documents: Documents with embeddings
            batch_size: Batch size for adding documents
        """
        print(f"Adding {len(documents)} documents to vector store...")

        for i in tqdm(range(0, len(documents), batch_size)):
            batch = documents[i:i + batch_size]

            ids = []
            documents_text = []
            metadatas = []

            for j, doc in enumerate(batch):
                doc_id = doc.get('metadata', {}).get('id') or f"doc_{i + j}"
                content = doc['content']
                metadata = doc.get('metadata', {})

                # Ensure metadata is serializable
                clean_metadata = {}
                for key, value in metadata.items():
                    if isinstance(value, (str, int, float, bool)):
                        clean_metadata[key] = value
                    else:
                        clean_metadata[key] = str(value)

                ids.append(doc_id)
                documents_text.append(content)
                metadatas.append(clean_metadata)

            # Add batch to collection
            self.collection.add(
                documents=documents_text,
                metadatas=metadatas,
                ids=ids
            )

        print(f"Successfully added {len(documents)} documents")

    def search(self,
               query: str,
               n_results: int = 5,
               where: Optional[Dict[str, Any]] = None,
               where_document: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Search for similar documents.

        Args:
            query: Search query
            n_results: Number of results to return
            where: Metadata filters
            where_document: Document content filters

        Returns:
            Search results
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where,
            where_document=where_document,
            include=['documents', 'metadatas', 'distances']
        )

        return results

    def search_by_embedding(self,
                           embedding: List[float],
                           n_results: int = 5,
                           where: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Search by embedding vector.

        Args:
            embedding: Query embedding
            n_results: Number of results to return
            where: Metadata filters

        Returns:
            Search results
        """
        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=n_results,
            where=where,
            include=['documents', 'metadatas', 'distances']
        )

        return results

    def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific document by ID.

        Args:
            doc_id: Document ID

        Returns:
            Document data or None if not found
        """
        try:
            result = self.collection.get(
                ids=[doc_id],
                include=['documents', 'metadatas']
            )

            if result['documents']:
                return {
                    'id': doc_id,
                    'content': result['documents'][0],
                    'metadata': result['metadatas'][0]
                }
        except:
            pass

        return None

    def update_document(self, doc_id: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Update a document.

        Args:
            doc_id: Document ID
            content: New content
            metadata: New metadata
        """
        update_data = {'documents': [content]}

        if metadata:
            # Clean metadata
            clean_metadata = {}
            for key, value in metadata.items():
                if isinstance(value, (str, int, float, bool)):
                    clean_metadata[key] = value
                else:
                    clean_metadata[key] = str(value)
            update_data['metadatas'] = [clean_metadata]

        self.collection.update(
            ids=[doc_id],
            **update_data
        )

    def delete_document(self, doc_id: str) -> None:
        """
        Delete a document.

        Args:
            doc_id: Document ID to delete
        """
        self.collection.delete(ids=[doc_id])

    def get_all_documents(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get all documents in the collection.

        Args:
            limit: Maximum number of documents to return

        Returns:
            List of documents
        """
        result = self.collection.get(
            include=['documents', 'metadatas'],
            limit=limit
        )

        documents = []
        for doc, metadata in zip(result['documents'], result['metadatas']):
            documents.append({
                'content': doc,
                'metadata': metadata
            })

        return documents

    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the collection.

        Returns:
            Collection statistics
        """
        documents = self.get_all_documents()

        # Analyze metadata
        sources = {}
        types = {}
        total_words = 0

        for doc in documents:
            metadata = doc['metadata']

            # Count sources
            source = metadata.get('source', 'unknown')
            sources[source] = sources.get(source, 0) + 1

            # Count types
            doc_type = metadata.get('type', 'unknown')
            types[doc_type] = types.get(doc_type, 0) + 1

            # Count words
            total_words += len(doc['content'].split())

        return {
            'total_documents': len(documents),
            'sources': sources,
            'types': types,
            'total_words': total_words,
            'avg_words_per_doc': total_words / len(documents) if documents else 0
        }

    def clear_collection(self) -> None:
        """Clear all documents from the collection."""
        print(f"Clearing collection: {self.collection_name}")

        # Delete and recreate collection
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.create_collection(
            name=self.collection_name,
            embedding_function=self.embedding_function
        )

        print("Collection cleared")

    def backup_collection(self, backup_file: str) -> None:
        """
        Backup collection data to JSON file.

        Args:
            backup_file: Backup file path
        """
        print(f"Backing up collection to {backup_file}")

        documents = self.get_all_documents()

        with open(backup_file, 'w') as f:
            json.dump(documents, f, indent=2)

        print(f"Backed up {len(documents)} documents")

    def restore_collection(self, backup_file: str) -> None:
        """
        Restore collection from backup file.

        Args:
            backup_file: Backup file path
        """
        print(f"Restoring collection from {backup_file}")

        with open(backup_file, 'r') as f:
            documents = json.load(f)

        # Clear current collection
        self.clear_collection()

        # Add documents back
        self.add_documents(documents)

        print(f"Restored {len(documents)} documents")

    def find_similar_documents(self, doc_id: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Find documents similar to a given document.

        Args:
            doc_id: Reference document ID
            n_results: Number of similar documents to find

        Returns:
            Similar documents
        """
        # Get the reference document
        ref_doc = self.get_document(doc_id)
        if not ref_doc:
            return []

        # Search using the document content
        results = self.search(ref_doc['content'], n_results + 1)  # +1 to exclude self

        # Remove the reference document from results
        similar_docs = []
        for doc, metadata, distance in zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        ):
            if metadata.get('id') != doc_id:  # Avoid returning the same document
                similar_docs.append({
                    'content': doc,
                    'metadata': metadata,
                    'similarity_score': 1 - distance  # Convert distance to similarity
                })

        return similar_docs[:n_results]

def main():
    """Main function for command-line usage."""
    import argparse

    parser = argparse.ArgumentParser(description='Medical Vector Store')
    parser.add_argument('--persist-dir', default='./embeddings', help='Persistence directory')
    parser.add_argument('--collection', default='medical_knowledge', help='Collection name')
    parser.add_argument('--model', default='all-MiniLM-L6-v2', help='Embedding model')
    parser.add_argument('--command', choices=['stats', 'clear', 'backup', 'restore'], help='Command to run')
    parser.add_argument('--backup-file', help='Backup file for backup/restore commands')

    args = parser.parse_args()

    # Initialize vector store
    vector_store = MedicalVectorStore(
        persist_directory=args.persist_dir,
        collection_name=args.collection,
        embedding_model=args.model
    )

    if args.command == 'stats':
        stats = vector_store.get_collection_stats()
        print("Collection Statistics:")
        print(json.dumps(stats, indent=2))

    elif args.command == 'clear':
        confirm = input("Are you sure you want to clear the collection? (yes/no): ")
        if confirm.lower() == 'yes':
            vector_store.clear_collection()
            print("Collection cleared")

    elif args.command == 'backup':
        if not args.backup_file:
            print("Error: --backup-file required for backup command")
            return
        vector_store.backup_collection(args.backup_file)

    elif args.command == 'restore':
        if not args.backup_file:
            print("Error: --backup-file required for restore command")
            return
        vector_store.restore_collection(args.backup_file)

if __name__ == "__main__":
    main()