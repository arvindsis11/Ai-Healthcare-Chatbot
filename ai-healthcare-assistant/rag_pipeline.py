#!/usr/bin/env python3
"""
RAG Pipeline for Healthcare Chatbot
Integrates retrieval and generation for medical question answering.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import json
from datetime import datetime

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from services.llm_service import LLMService
from vector_store import MedicalVectorStore
from embedding_pipeline import MedicalEmbeddingPipeline

class MedicalRAGPipeline:
    """Retrieval-Augmented Generation pipeline for healthcare."""

    def __init__(self,
                 vector_store: MedicalVectorStore,
                 llm_service: LLMService,
                 embedding_pipeline: Optional[MedicalEmbeddingPipeline] = None):
        """
        Initialize the RAG pipeline.

        Args:
            vector_store: Vector store for retrieval
            llm_service: LLM service for generation
            embedding_pipeline: Embedding pipeline (optional)
        """
        self.vector_store = vector_store
        self.llm_service = llm_service
        self.embedding_pipeline = embedding_pipeline

        print("Initialized Medical RAG Pipeline")

    def retrieve_context(self,
                        query: str,
                        n_results: int = 3,
                        filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Retrieve relevant context for a query.

        Args:
            query: User query
            n_results: Number of documents to retrieve
            filters: Metadata filters for retrieval

        Returns:
            Retrieved documents with relevance scores
        """
        # Search vector store
        search_results = self.vector_store.search(
            query=query,
            n_results=n_results,
            where=filters
        )

        if not search_results['documents']:
            return []

        # Format results
        context_docs = []
        for doc, metadata, distance in zip(
            search_results['documents'][0],
            search_results['metadatas'][0],
            search_results['distances'][0]
        ):
            context_docs.append({
                'content': doc,
                'metadata': metadata,
                'relevance_score': 1 - distance,  # Convert distance to similarity score
                'source': metadata.get('source', 'unknown'),
                'type': metadata.get('type', 'unknown')
            })

        return context_docs

    def generate_answer(self,
                       query: str,
                       context: List[Dict[str, Any]],
                       conversation_history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        """
        Generate an answer using retrieved context.

        Args:
            query: User query
            context: Retrieved context documents
            conversation_history: Previous conversation turns

        Returns:
            Generated answer with metadata
        """
        # Format context for LLM
        context_texts = []
        sources = []

        for doc in context:
            context_texts.append(doc['content'])
            sources.append({
                'source': doc['source'],
                'type': doc['type'],
                'relevance': doc['relevance_score']
            })

        # Generate response using LLM service
        response = self.llm_service.generate_medical_response(
            query=query,
            context=context_texts
        )

        return {
            'answer': response,
            'sources': sources,
            'context_used': len(context),
            'timestamp': datetime.utcnow().isoformat()
        }

    def answer_question(self,
                       query: str,
                       n_context_docs: int = 3,
                       filters: Optional[Dict[str, Any]] = None,
                       conversation_history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        """
        Complete RAG pipeline: retrieve context and generate answer.

        Args:
            query: User question
            n_context_docs: Number of context documents to retrieve
            filters: Metadata filters for retrieval
            conversation_history: Previous conversation turns

        Returns:
            Complete answer with context and metadata
        """
        # Step 1: Retrieve relevant context
        context = self.retrieve_context(query, n_context_docs, filters)

        # Step 2: Generate answer
        result = self.generate_answer(query, context, conversation_history)

        # Step 3: Add retrieval metadata
        result.update({
            'query': query,
            'retrieval': {
                'num_docs_retrieved': len(context),
                'filters_used': filters,
                'context_docs': context
            }
        })

        return result

    def add_medical_knowledge(self, documents: List[Dict[str, Any]]) -> None:
        """
        Add new medical knowledge to the system.

        Args:
            documents: New documents to add
        """
        if self.embedding_pipeline:
            # Create embeddings for new documents
            embedded_docs = self.embedding_pipeline.create_embeddings(documents)
        else:
            # Assume documents already have embeddings
            embedded_docs = documents

        # Add to vector store
        self.vector_store.add_documents(embedded_docs)

        print(f"Added {len(documents)} new documents to knowledge base")

    def update_medical_knowledge(self, doc_id: str, new_content: str, new_metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Update existing medical knowledge.

        Args:
            doc_id: Document ID to update
            new_content: New content
            new_metadata: New metadata
        """
        self.vector_store.update_document(doc_id, new_content, new_metadata)
        print(f"Updated document {doc_id}")

    def get_knowledge_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the medical knowledge base.

        Returns:
            Knowledge base statistics
        """
        vector_stats = self.vector_store.get_collection_stats()

        return {
            'vector_store': vector_stats,
            'total_knowledge_items': vector_stats['total_documents'],
            'knowledge_sources': vector_stats['sources'],
            'content_types': vector_stats['types']
        }

    def find_related_information(self, topic: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Find related medical information for a topic.

        Args:
            topic: Medical topic to search for
            n_results: Number of results to return

        Returns:
            Related information
        """
        return self.retrieve_context(topic, n_results)

    def explain_medical_concept(self, concept: str) -> Dict[str, Any]:
        """
        Explain a medical concept using RAG.

        Args:
            concept: Medical concept to explain

        Returns:
            Explanation with sources
        """
        query = f"Explain the medical concept: {concept}"
        return self.answer_question(query, n_context_docs=2)

    def get_treatment_info(self, condition: str) -> Dict[str, Any]:
        """
        Get treatment information for a medical condition.

        Args:
            condition: Medical condition

        Returns:
            Treatment information
        """
        query = f"What are the treatments for {condition}?"
        filters = {'type': 'treatment'}  # Filter for treatment documents
        return self.answer_question(query, n_context_docs=3, filters=filters)

    def get_precaution_info(self, condition: str) -> Dict[str, Any]:
        """
        Get precaution information for a medical condition.

        Args:
            condition: Medical condition

        Returns:
            Precaution information
        """
        query = f"What precautions should be taken for {condition}?"
        filters = {'type': 'precaution'}  # Filter for precaution documents
        return self.answer_question(query, n_context_docs=2, filters=filters)

    def analyze_symptoms_with_knowledge(self, symptoms: List[str]) -> Dict[str, Any]:
        """
        Analyze symptoms using medical knowledge base.

        Args:
            symptoms: List of symptoms

        Returns:
            Symptom analysis with medical context
        """
        symptom_text = ", ".join(symptoms)
        query = f"I have these symptoms: {symptom_text}. What could this indicate?"

        # Get symptom analysis from LLM
        symptom_analysis = self.llm_service.analyze_symptoms(symptoms, symptom_text)

        # Get relevant medical knowledge
        answer = self.answer_question(query, n_context_docs=3)

        return {
            'symptom_analysis': symptom_analysis,
            'medical_context': answer,
            'combined_insights': {
                'symptoms': symptoms,
                'possible_conditions': symptom_analysis.possible_conditions,
                'recommended_action': symptom_analysis.urgency_recommendation
            }
        }

    def save_conversation(self, conversation: List[Dict[str, Any]], filename: str) -> None:
        """
        Save a conversation for analysis or training.

        Args:
            conversation: Conversation history
            filename: Output filename
        """
        conversation_data = {
            'conversation': conversation,
            'timestamp': datetime.utcnow().isoformat(),
            'metadata': {
                'total_turns': len(conversation),
                'rag_enabled': True
            }
        }

        with open(filename, 'w') as f:
            json.dump(conversation_data, f, indent=2)

        print(f"Saved conversation to {filename}")

    def evaluate_answer_quality(self, question: str, answer: str, context: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Evaluate the quality of a generated answer.

        Args:
            question: Original question
            answer: Generated answer
            context: Context used

        Returns:
            Quality metrics
        """
        # Simple evaluation metrics
        metrics = {
            'answer_length': len(answer.split()),
            'context_used': len(context),
            'has_medical_terms': any(term in answer.lower() for term in
                                   ['symptom', 'treatment', 'condition', 'medical', 'health']),
            'has_disclaimer': 'consult a healthcare professional' in answer.lower(),
            'relevance_score': sum(doc['relevance_score'] for doc in context) / len(context) if context else 0
        }

        return metrics

def create_medical_rag_pipeline(openai_api_key: str,
                               persist_dir: str = "./embeddings",
                               collection_name: str = "medical_knowledge") -> MedicalRAGPipeline:
    """
    Factory function to create a complete medical RAG pipeline.

    Args:
        openai_api_key: OpenAI API key
        persist_dir: Vector store persistence directory
        collection_name: Vector store collection name

    Returns:
        Configured RAG pipeline
    """
    # Initialize components
    vector_store = MedicalVectorStore(
        persist_directory=persist_dir,
        collection_name=collection_name
    )

    llm_service = LLMService(api_key=openai_api_key)

    embedding_pipeline = MedicalEmbeddingPipeline()

    # Create RAG pipeline
    rag_pipeline = MedicalRAGPipeline(
        vector_store=vector_store,
        llm_service=llm_service,
        embedding_pipeline=embedding_pipeline
    )

    return rag_pipeline

def main():
    """Main function for command-line usage."""
    import argparse

    parser = argparse.ArgumentParser(description='Medical RAG Pipeline')
    parser.add_argument('--openai-key', required=True, help='OpenAI API key')
    parser.add_argument('--persist-dir', default='./embeddings', help='Vector store directory')
    parser.add_argument('--collection', default='medical_knowledge', help='Collection name')
    parser.add_argument('--query', help='Query to test')
    parser.add_argument('--data-dir', help='Data directory to ingest')

    args = parser.parse_args()

    # Create RAG pipeline
    rag = create_medical_rag_pipeline(
        openai_api_key=args.openai_key,
        persist_dir=args.persist_dir,
        collection_name=args.collection
    )

    if args.data_dir:
        # Ingest data
        print(f"Ingesting data from {args.data_dir}")
        documents = rag.embedding_pipeline.load_medical_datasets(args.data_dir)
        processed_docs = rag.embedding_pipeline.preprocess_documents(documents)
        embedded_docs = rag.embedding_pipeline.create_embeddings(processed_docs)
        rag.add_medical_knowledge(embedded_docs)
        print("Data ingestion completed")

    elif args.query:
        # Answer query
        print(f"Query: {args.query}")
        result = rag.answer_question(args.query)
        print(f"Answer: {result['answer']}")
        print(f"Sources: {len(result['sources'])}")

    else:
        # Show stats
        stats = rag.get_knowledge_stats()
        print("Knowledge Base Statistics:")
        print(json.dumps(stats, indent=2))

if __name__ == "__main__":
    main()