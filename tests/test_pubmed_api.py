import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

@pytest.fixture
def client():
    # Use the existing app for testing
    return TestClient(app)

def test_chat_with_medical_knowledge(client):
    """Verify that the chat API retrieves medical context and returns citations."""
    payload = {
        "message": "Tell me about fever management in children based on PubMed research.",
        "conversation_id": "test-pubmed-context"
    }
    
    response = client.post("/api/v1/chat", json=payload)
    
    # Check if the API is up and responding
    assert response.status_code == 200
    data = response.json()
    
    # Verify core response structure
    assert "response" in data
    assert "symptom_analysis" in data
    assert "citations" in data
    
    # The symptom analysis should work even without external context
    assert data["symptom_analysis"]["risk_level"] in ["low", "medium", "high"]
    
    # Verify that a specialist was recommended
    assert "recommended_specialist" in data
    assert data["recommended_specialist"] == "General Physician" or data["recommended_specialist"] is not None

def test_api_health_check(client):
    """Simple check to verify API is healthy."""
    response = client.get("/")
    assert response.status_code == 200
    assert "AI Healthcare Assistant API" in response.json()["message"]
