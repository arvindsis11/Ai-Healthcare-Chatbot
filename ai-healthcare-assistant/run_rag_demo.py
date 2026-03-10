#!/usr/bin/env python3
"""
Complete RAG System Setup and Usage Example
Demonstrates the full medical RAG pipeline.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from embedding_pipeline import MedicalEmbeddingPipeline
from vector_store import MedicalVectorStore
from rag_pipeline import MedicalRAGPipeline, create_medical_rag_pipeline
from backend.services.llm_service import LLMService

def setup_medical_rag_system():
    """Set up the complete medical RAG system."""

    print("🔧 Setting up Medical RAG System...")

    # Check for OpenAI API key
    openai_key = os.getenv('OPENAI_API_KEY')
    if not openai_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    # Create RAG pipeline
    rag_pipeline = create_medical_rag_pipeline(
        openai_api_key=openai_key,
        persist_dir="./embeddings",
        collection_name="medical_knowledge"
    )

    return rag_pipeline

def ingest_medical_data(rag_pipeline, data_dir: str = "./data"):
    """Ingest medical data into the RAG system."""

    print(f"📚 Ingesting medical data from {data_dir}...")

    # Load and process data
    documents = rag_pipeline.embedding_pipeline.load_medical_datasets(data_dir)
    print(f"Loaded {len(documents)} raw documents")

    processed_docs = rag_pipeline.embedding_pipeline.preprocess_documents(documents)
    print(f"Processed {len(processed_docs)} documents")

    embedded_docs = rag_pipeline.embedding_pipeline.create_embeddings(processed_docs)
    print(f"Created embeddings for {len(embedded_docs)} documents")

    # Add to vector store
    rag_pipeline.add_medical_knowledge(embedded_docs)
    print("✅ Data ingestion completed")

def demonstrate_rag_capabilities(rag_pipeline):
    """Demonstrate various RAG capabilities."""

    print("\n🩺 Demonstrating RAG Capabilities...")

    # Example queries
    test_queries = [
        "What are the symptoms of diabetes?",
        "How to treat a fever?",
        "What precautions should I take for high blood pressure?",
        "I have chest pain and shortness of breath - what could this be?",
        "Explain what pneumonia is"
    ]

    for query in test_queries:
        print(f"\n❓ Query: {query}")

        try:
            result = rag_pipeline.answer_question(query)

            print(f"🤖 Answer: {result['answer'][:200]}..." if len(result['answer']) > 200 else f"🤖 Answer: {result['answer']}")
            print(f"📄 Sources used: {len(result['sources'])}")
            print(f"🎯 Context docs retrieved: {result['retrieval']['num_docs_retrieved']}")

        except Exception as e:
            print(f"❌ Error: {e}")

def demonstrate_symptom_analysis(rag_pipeline):
    """Demonstrate symptom analysis capabilities."""

    print("\n🔍 Demonstrating Symptom Analysis...")

    test_symptoms = [
        ["headache", "nausea", "sensitivity to light"],
        ["chest pain", "shortness of breath", "dizziness"],
        ["fever", "cough", "fatigue"],
        ["abdominal pain", "vomiting", "diarrhea"]
    ]

    for symptoms in test_symptoms:
        print(f"\n🩹 Symptoms: {', '.join(symptoms)}")

        try:
            analysis = rag_pipeline.analyze_symptoms_with_knowledge(symptoms)

            symptom_analysis = analysis['symptom_analysis']
            print(f"📊 Severity Score: {symptom_analysis.severity_score}/10")
            print(f"⚠️ Risk Level: {symptom_analysis.risk_level.value}")
            print(f"🔍 Possible Conditions: {', '.join(symptom_analysis.possible_conditions[:2])}")
            print(f"🏥 Recommendation: {symptom_analysis.urgency_recommendation}")

        except Exception as e:
            print(f"❌ Error: {e}")

def show_knowledge_stats(rag_pipeline):
    """Show statistics about the medical knowledge base."""

    print("\n📊 Knowledge Base Statistics...")

    try:
        stats = rag_pipeline.get_knowledge_stats()

        print(f"📚 Total Knowledge Items: {stats['total_knowledge_items']}")
        print(f"📝 Total Words: {stats['vector_store']['total_words']:,}")
        print(f"📄 Average Words per Document: {stats['vector_store']['avg_words_per_doc']:.0f}")

        print("\n📂 Content Sources:")
        for source, count in stats['knowledge_sources'].items():
            print(f"  • {source}: {count}")

        print("\n🏷️ Content Types:")
        for content_type, count in stats['content_types'].items():
            print(f"  • {content_type}: {count}")

    except Exception as e:
        print(f"❌ Error getting stats: {e}")

def main():
    """Main demonstration function."""

    print("🏥 Medical RAG System Demonstration")
    print("=" * 50)

    try:
        # Setup system
        rag_pipeline = setup_medical_rag_system()

        # Check if data needs to be ingested
        stats = rag_pipeline.get_knowledge_stats()
        if stats['total_knowledge_items'] == 0:
            print("📥 No knowledge base found. Ingesting data...")
            ingest_medical_data(rag_pipeline)
        else:
            print(f"📚 Found existing knowledge base with {stats['total_knowledge_items']} items")

        # Show knowledge statistics
        show_knowledge_stats(rag_pipeline)

        # Demonstrate capabilities
        demonstrate_rag_capabilities(rag_pipeline)
        demonstrate_symptom_analysis(rag_pipeline)

        print("\n✅ Medical RAG System demonstration completed!")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()