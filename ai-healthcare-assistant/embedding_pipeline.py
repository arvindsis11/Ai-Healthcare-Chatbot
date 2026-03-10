#!/usr/bin/env python3
"""
Embedding Pipeline for Healthcare RAG System
Processes medical data and creates embeddings for vector storage.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
import json
import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
from tqdm import tqdm

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from utils.text_processing import preprocess_medical_text, chunk_text, extract_medical_entities

class MedicalEmbeddingPipeline:
    """Pipeline for processing medical data and creating embeddings."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the embedding pipeline.

        Args:
            model_name: Sentence transformer model name
        """
        self.model_name = model_name
        self.embedding_model = SentenceTransformer(model_name)
        self.embedding_dim = self.embedding_model.get_sentence_embedding_dimension()

        print(f"Initialized embedding pipeline with model: {model_name}")
        print(f"Embedding dimension: {self.embedding_dim}")

    def load_medical_datasets(self, data_dir: str) -> List[Dict[str, Any]]:
        """
        Load various medical datasets.

        Args:
            data_dir: Directory containing medical data files

        Returns:
            List of processed medical documents
        """
        documents = []
        data_path = Path(data_dir)

        print(f"Loading medical datasets from: {data_path}")

        # Load YAML conversation data (existing)
        yaml_docs = self._load_yaml_data(data_path)
        documents.extend(yaml_docs)

        # Load structured medical data (if available)
        structured_docs = self._load_structured_data(data_path)
        documents.extend(structured_docs)

        # Load text documents (if available)
        text_docs = self._load_text_documents(data_path)
        documents.extend(text_docs)

        print(f"Loaded {len(documents)} total documents")
        return documents

    def _load_yaml_data(self, data_path: Path) -> List[Dict[str, Any]]:
        """Load existing YAML conversation data."""
        from utils.text_processing import load_yaml_files

        yaml_files = list(data_path.glob("*.yml"))
        if not yaml_files:
            return []

        print(f"Loading {len(yaml_files)} YAML files...")
        return load_yaml_files(str(data_path))

    def _load_structured_data(self, data_path: Path) -> List[Dict[str, Any]]:
        """Load structured medical data (CSV, JSON)."""
        documents = []

        # Look for CSV files
        csv_files = list(data_path.glob("*.csv"))
        for csv_file in csv_files:
            try:
                df = pd.read_csv(csv_file)
                print(f"Processing CSV: {csv_file.name}")

                for _, row in df.iterrows():
                    content = self._row_to_text(row, csv_file.stem)
                    if content:
                        doc = {
                            'content': content,
                            'metadata': {
                                'source': csv_file.name,
                                'type': 'structured',
                                'dataset': csv_file.stem,
                                'row_data': row.to_dict()
                            }
                        }
                        documents.append(doc)
            except Exception as e:
                print(f"Error loading {csv_file}: {e}")

        # Look for JSON files
        json_files = list(data_path.glob("*.json"))
        for json_file in json_files:
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)

                print(f"Processing JSON: {json_file.name}")

                if isinstance(data, list):
                    for item in data:
                        content = self._json_to_text(item)
                        if content:
                            doc = {
                                'content': content,
                                'metadata': {
                                    'source': json_file.name,
                                    'type': 'structured',
                                    'dataset': json_file.stem,
                                    'item_data': item
                                }
                            }
                            documents.append(doc)
            except Exception as e:
                print(f"Error loading {json_file}: {e}")

        return documents

    def _load_text_documents(self, data_path: Path) -> List[Dict[str, Any]]:
        """Load plain text medical documents."""
        documents = []

        text_files = list(data_path.glob("*.txt")) + list(data_path.glob("*.md"))
        for text_file in text_files:
            try:
                with open(text_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                print(f"Processing text file: {text_file.name}")

                # Chunk long documents
                if len(content.split()) > 500:
                    chunks = chunk_text(content, chunk_size=400, overlap=50)
                    for i, chunk in enumerate(chunks):
                        doc = {
                            'content': chunk,
                            'metadata': {
                                'source': text_file.name,
                                'type': 'text',
                                'chunk_id': i,
                                'total_chunks': len(chunks)
                            }
                        }
                        documents.append(doc)
                else:
                    doc = {
                        'content': content,
                        'metadata': {
                            'source': text_file.name,
                            'type': 'text'
                        }
                    }
                    documents.append(doc)
            except Exception as e:
                print(f"Error loading {text_file}: {e}")

        return documents

    def _row_to_text(self, row: pd.Series, dataset_name: str) -> str:
        """Convert DataFrame row to readable text."""
        if dataset_name.lower() == 'symptoms':
            return f"Symptom: {row.get('symptom', '')}. Description: {row.get('description', '')}. Common causes: {row.get('causes', '')}"
        elif dataset_name.lower() == 'diseases':
            return f"Disease: {row.get('name', '')}. Description: {row.get('description', '')}. Symptoms: {row.get('symptoms', '')}. Treatment: {row.get('treatment', '')}"
        elif dataset_name.lower() == 'treatments':
            return f"Treatment: {row.get('name', '')}. For condition: {row.get('condition', '')}. Description: {row.get('description', '')}. Side effects: {row.get('side_effects', '')}"
        elif dataset_name.lower() == 'precautions':
            return f"Precaution: {row.get('title', '')}. For: {row.get('condition', '')}. Advice: {row.get('advice', '')}"
        else:
            # Generic conversion
            return '. '.join([f"{col}: {val}" for col, val in row.items() if pd.notna(val)])

    def _json_to_text(self, item: Dict[str, Any]) -> str:
        """Convert JSON item to readable text."""
        if 'symptom' in item:
            return f"Symptom: {item.get('symptom', '')}. Description: {item.get('description', '')}"
        elif 'disease' in item or 'condition' in item:
            name = item.get('disease') or item.get('condition')
            return f"Medical Condition: {name}. Description: {item.get('description', '')}. Symptoms: {item.get('symptoms', '')}"
        elif 'treatment' in item:
            return f"Treatment: {item.get('treatment', '')}. Purpose: {item.get('purpose', '')}"
        else:
            return json.dumps(item, indent=2)

    def preprocess_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Preprocess documents for embedding.

        Args:
            documents: Raw documents

        Returns:
            Processed documents ready for embedding
        """
        processed_docs = []

        print("Preprocessing documents...")

        for doc in tqdm(documents):
            content = doc['content']

            # Preprocess text
            processed_content = preprocess_medical_text(content)

            # Extract medical entities
            entities = extract_medical_entities(processed_content)

            # Create processed document
            processed_doc = {
                'content': processed_content,
                'metadata': {
                    **doc['metadata'],
                    'original_length': len(content),
                    'processed_length': len(processed_content),
                    'entities': entities,
                    'word_count': len(processed_content.split())
                }
            }

            processed_docs.append(processed_doc)

        print(f"Processed {len(processed_docs)} documents")
        return processed_docs

    def create_embeddings(self, documents: List[Dict[str, Any]], batch_size: int = 32) -> List[Dict[str, Any]]:
        """
        Create embeddings for documents.

        Args:
            documents: Documents to embed
            batch_size: Batch size for embedding

        Returns:
            Documents with embeddings
        """
        print("Creating embeddings...")

        # Extract texts for batch processing
        texts = [doc['content'] for doc in documents]

        # Create embeddings in batches
        embeddings = []
        for i in tqdm(range(0, len(texts), batch_size)):
            batch_texts = texts[i:i + batch_size]
            batch_embeddings = self.embedding_model.encode(batch_texts, show_progress_bar=False)
            embeddings.extend(batch_embeddings.tolist())

        # Add embeddings to documents
        for doc, embedding in zip(documents, embeddings):
            doc['embedding'] = embedding

        print(f"Created embeddings for {len(documents)} documents")
        return documents

    def save_embeddings(self, documents: List[Dict[str, Any]], output_file: str) -> None:
        """
        Save documents with embeddings to file.

        Args:
            output_file: Output file path
        """
        print(f"Saving embeddings to {output_file}")

        # Convert to serializable format
        serializable_docs = []
        for doc in documents:
            serializable_doc = {
                'content': doc['content'],
                'metadata': doc['metadata'],
                'embedding': doc['embedding']
            }
            serializable_docs.append(serializable_doc)

        with open(output_file, 'w') as f:
            json.dump(serializable_docs, f, indent=2)

        print(f"Saved {len(serializable_docs)} documents with embeddings")

    def load_embeddings(self, input_file: str) -> List[Dict[str, Any]]:
        """
        Load documents with embeddings from file.

        Args:
            input_file: Input file path

        Returns:
            Documents with embeddings
        """
        print(f"Loading embeddings from {input_file}")

        with open(input_file, 'r') as f:
            documents = json.load(f)

        print(f"Loaded {len(documents)} documents with embeddings")
        return documents

    def run_pipeline(self, data_dir: str, output_file: str, save_intermediate: bool = True) -> List[Dict[str, Any]]:
        """
        Run the complete embedding pipeline.

        Args:
            data_dir: Input data directory
            output_file: Output file for embeddings
            save_intermediate: Whether to save intermediate results

        Returns:
            Documents with embeddings
        """
        print("Starting embedding pipeline...")

        # Step 1: Load data
        raw_documents = self.load_medical_datasets(data_dir)

        if save_intermediate:
            with open('raw_documents.json', 'w') as f:
                json.dump(raw_documents, f, indent=2)

        # Step 2: Preprocess
        processed_documents = self.preprocess_documents(raw_documents)

        if save_intermediate:
            with open('processed_documents.json', 'w') as f:
                json.dump(processed_documents, f, indent=2)

        # Step 3: Create embeddings
        embedded_documents = self.create_embeddings(processed_documents)

        # Step 4: Save results
        self.save_embeddings(embedded_documents, output_file)

        print("Embedding pipeline completed!")
        return embedded_documents

def main():
    """Main function for command-line usage."""
    import argparse

    parser = argparse.ArgumentParser(description='Medical Embedding Pipeline')
    parser.add_argument('--data-dir', default='../data', help='Input data directory')
    parser.add_argument('--output', default='../embeddings/medical_embeddings.json', help='Output embeddings file')
    parser.add_argument('--model', default='all-MiniLM-L6-v2', help='Embedding model name')
    parser.add_argument('--batch-size', type=int, default=32, help='Embedding batch size')

    args = parser.parse_args()

    # Create output directory
    Path(args.output).parent.mkdir(exist_ok=True)

    # Run pipeline
    pipeline = MedicalEmbeddingPipeline(model_name=args.model)
    documents = pipeline.run_pipeline(args.data_dir, args.output)

    print(f"Pipeline completed! Created embeddings for {len(documents)} documents.")

if __name__ == "__main__":
    main()