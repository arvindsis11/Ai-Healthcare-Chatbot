import pytest
from app.services.medical_intelligence_service import (
    SymptomExtractionService,
    TriageService,
    DoctorRecommendationService
)
from app.models.chat import RiskLevel

@pytest.fixture
def symptom_service():
    return SymptomExtractionService()

@pytest.fixture
def triage_service():
    return TriageService()

@pytest.fixture
def doctor_service():
    return DoctorRecommendationService()

def test_symptom_extraction(symptom_service):
    text = "I have been experiencing a high fever and some chest pain lately."
    extracted = symptom_service.extract(text)
    assert "fever" in extracted
    assert "chest pain" in extracted

def test_triage_high_risk(triage_service):
    symptoms = ["chest pain", "shortness of breath"]
    analysis = triage_service.assess(symptoms)
    assert analysis.risk_level == RiskLevel.HIGH
    assert analysis.severity_score == 8

def test_triage_medium_risk(triage_service):
    symptoms = ["fever"]
    analysis = triage_service.assess(symptoms)
    assert analysis.risk_level == RiskLevel.MEDIUM
    assert "Book an appointment" in analysis.urgency_recommendation

def test_doctor_recommendation_cardio(doctor_service):
    symptoms = ["chest pain"]
    recommendation = doctor_service.recommend_detailed(symptoms)
    assert recommendation.specialist == "Cardiologist"
    assert "chest pain" in recommendation.reasoning

def test_doctor_recommendation_dermo(doctor_service):
    symptoms = ["skin rash", "itchy skin"]
    recommendation = doctor_service.recommend_detailed(symptoms)
    assert recommendation.specialist == "Dermatologist"
