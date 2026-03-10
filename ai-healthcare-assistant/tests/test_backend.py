import pytest
from backend.services.vector_db import VectorDatabase
from backend.services.llm_service import LLMService
from backend.services.rag_service import RAGService
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

# Note: LLM tests require API keys and are integration tests
# They should be run separately with proper environment setup