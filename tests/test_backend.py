import pytest
from backend.app.repositories.vector_db import VectorDatabase
from backend.app.services.llm_service import LLMService
from backend.app.services.rag_service import RAGService
from backend.app.models.chat import SymptomAnalysis, RiskLevel
import tempfile
import os

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir

@pytest.fixture
def vector_db(temp_dir):
    return VectorDatabase(
        persist_directory=temp_dir,
        collection_name="test_collection"
    )

def test_vector_db_initialization(vector_db):
    """Test vector database initialization."""
    assert vector_db.collection_name == "test_collection"
    assert os.path.exists(vector_db.persist_directory)

def test_add_and_search_documents(vector_db):
    """Test adding documents and searching."""
    documents = [
        {
            "content": "Fever is a common symptom of infection.",
            "metadata": {"topic": "fever"}
        }
    ]

    vector_db.add_documents(documents)

    results = vector_db.search("What are symptoms of fever?")
    assert len(results['documents']) > 0
    assert "fever" in results['documents'][0][0].lower()

def test_symptom_analysis_structure():
    """Test symptom analysis model structure."""
    analysis = SymptomAnalysis(
        symptoms=["headache", "nausea"],
        severity_score=6,
        risk_level=RiskLevel.MEDIUM,
        possible_conditions=["migraine", "viral infection"],
        urgency_recommendation="See a doctor within a few days"
    )

    assert analysis.symptoms == ["headache", "nausea"]
    assert analysis.severity_score == 6
    assert analysis.risk_level == RiskLevel.MEDIUM
    assert "migraine" in analysis.possible_conditions
    assert "doctor" in analysis.urgency_recommendation

def test_rag_symptom_extraction():
    """Test symptom extraction from text."""
    from backend.app.services.rag_service import RAGService

    # Mock RAG service for testing
    class MockVectorDB:
        pass

    class MockLLMService:
        pass

    rag_service = RAGService(MockVectorDB(), MockLLMService())

    # Test symptom extraction
    symptoms = rag_service.extract_symptoms_from_text("I have a headache and feel nauseous")
    assert "headache" in symptoms
    assert "nausea" in symptoms or "nauseous" in symptoms

# Note: LLM tests require API keys and are integration tests
# They should be run separately with proper environment setup