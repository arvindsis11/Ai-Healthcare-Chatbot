"""Tests for the DoctorRecommendationService."""

import pytest

from app.services.medical_intelligence_service import DoctorRecommendationService


@pytest.fixture
def service():
    return DoctorRecommendationService()


class TestRecommend:
    """Tests for the backwards-compatible recommend() method."""

    def test_chest_pain_returns_cardiologist(self, service):
        assert service.recommend(["chest pain"]) == "Cardiologist"

    def test_skin_rash_returns_dermatologist(self, service):
        assert service.recommend(["skin rash"]) == "Dermatologist"

    def test_headache_returns_neurologist(self, service):
        assert service.recommend(["severe headache"]) == "Neurologist"

    def test_empty_symptoms_returns_general_physician(self, service):
        assert service.recommend([]) == "General Physician"

    def test_unknown_symptoms_returns_general_physician(self, service):
        assert service.recommend(["xyz unknown"]) == "General Physician"


class TestRecommendDetailed:
    """Tests for the enhanced recommend_detailed() method."""

    def test_returns_doctor_recommendation_model(self, service):
        rec = service.recommend_detailed(["chest pain"])
        assert rec.specialist == "Cardiologist"
        assert 0.0 < rec.confidence <= 1.0
        assert "chest pain" in rec.reasoning

    def test_empty_symptoms_low_confidence(self, service):
        rec = service.recommend_detailed([])
        assert rec.specialist == "General Physician"
        assert rec.confidence == 0.5

    def test_multiple_symptoms_picks_highest_score(self, service):
        rec = service.recommend_detailed(["chest pain", "heart palpitations"])
        assert rec.specialist == "Cardiologist"
        assert rec.confidence > 0.3

    def test_alternative_specialists_populated(self, service):
        # Shortness of breath maps to both Cardiologist and Pulmonologist
        rec = service.recommend_detailed(["shortness of breath"])
        all_specialists = [rec.specialist] + rec.alternative_specialists
        assert len(all_specialists) >= 2

    def test_dermatologist_confidence(self, service):
        rec = service.recommend_detailed(["skin rash", "itchy skin", "hives"])
        assert rec.specialist == "Dermatologist"
        assert rec.confidence >= 0.3

    def test_gastroenterologist_mapping(self, service):
        rec = service.recommend_detailed(["abdominal pain", "bloating", "acid reflux"])
        assert rec.specialist == "Gastroenterologist"

    def test_ent_specialist_mapping(self, service):
        rec = service.recommend_detailed(["ear pain", "hearing loss"])
        assert rec.specialist == "ENT Specialist"

    def test_ophthalmologist_mapping(self, service):
        rec = service.recommend_detailed(["blurred vision", "eye pain"])
        assert rec.specialist == "Ophthalmologist"

    def test_psychiatrist_mapping(self, service):
        rec = service.recommend_detailed(["anxiety", "depression", "insomnia"])
        assert rec.specialist == "Psychiatrist"

    def test_orthopedist_mapping(self, service):
        rec = service.recommend_detailed(["joint pain", "back pain"])
        assert rec.specialist == "Orthopedist"

    def test_endocrinologist_mapping(self, service):
        rec = service.recommend_detailed(["thyroid", "excessive thirst"])
        assert rec.specialist == "Endocrinologist"

    def test_urologist_mapping(self, service):
        rec = service.recommend_detailed(["painful urination", "blood in urine"])
        assert rec.specialist == "Urologist"

    def test_pulmonologist_mapping(self, service):
        rec = service.recommend_detailed(["chronic cough", "wheezing", "asthma"])
        assert rec.specialist == "Pulmonologist"

    def test_allergist_mapping(self, service):
        rec = service.recommend_detailed(["allergic reaction", "sneezing", "watery eyes"])
        assert rec.specialist == "Allergist"

    def test_rheumatologist_mapping(self, service):
        rec = service.recommend_detailed(["arthritis", "joint swelling", "morning stiffness"])
        assert rec.specialist == "Rheumatologist"

    def test_reasoning_contains_matched_keywords(self, service):
        rec = service.recommend_detailed(["migraine"])
        assert "migraine" in rec.reasoning.lower()

    def test_confidence_never_exceeds_one(self, service):
        # Even with many matching symptoms
        rec = service.recommend_detailed([
            "skin rash", "acne", "eczema", "psoriasis",
            "itchy skin", "hives", "skin lesion", "mole"
        ])
        assert rec.confidence <= 1.0
