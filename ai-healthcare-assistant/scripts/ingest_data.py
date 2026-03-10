#!/usr/bin/env python3
"""
Data ingestion script for AI Healthcare Assistant.
Loads YAML data and creates vector embeddings with medical-specific processing.
"""

import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from config.settings import settings
from services.vector_db import VectorDatabase
from rag.data_ingestion import DataIngestionPipeline

def main():
    print("Starting medical data ingestion...")

    # Initialize vector database
    vector_db = VectorDatabase(
        persist_directory=settings.chroma_persist_directory,
        collection_name=settings.chroma_collection_name
    )

    # Initialize ingestion pipeline
    pipeline = DataIngestionPipeline(vector_db)

    # Data directory
    data_dir = Path(__file__).parent / "data"

    if not data_dir.exists():
        print(f"Data directory not found: {data_dir}")
        return

    # Clear existing data
    print("Clearing existing data...")
    vector_db.clear_collection()

    # Ingest new data with medical processing
    pipeline.ingest_data(str(data_dir))

    # Print enhanced stats
    stats = pipeline.get_stats()
    print("\nIngestion complete!")
    print(f"Total documents: {stats['total_documents']}")
    print(f"Average content length: {stats['avg_content_length']:.0f} characters")
    print("\nTopics:")
    for topic, count in stats['topics'].items():
        print(f"  {topic}: {count}")
    print("\nChunk types:")
    for chunk_type, count in stats['chunk_types'].items():
        print(f"  {chunk_type}: {count}")

if __name__ == "__main__":
    main()