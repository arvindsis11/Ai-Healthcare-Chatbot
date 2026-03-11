from dataclasses import dataclass
from typing import List

from ..models.chat import RiskLevel, SymptomAnalysis

try:
    import spacy
except Exception:  # pragma: no cover - optional dependency fallback
    spacy = None


@dataclass
class SymptomExtractionService:
    def __post_init__(self):
        self._nlp = None
        if spacy is not None:
            try:
                self._nlp = spacy.load("en_core_web_sm")
            except Exception:
                self._nlp = None

    def extract(self, text: str, explicit_symptoms: List[str] | None = None) -> List[str]:
        if explicit_symptoms:
            return explicit_symptoms

        keywords = [
            "fever",
            "headache",
            "nausea",
            "dizziness",
            "cough",
            "fatigue",
            "chest pain",
            "shortness of breath",
            "sore throat",
        ]
        lowered = text.lower()
        found = {item for item in keywords if item in lowered}

        if self._nlp is not None:
            doc = self._nlp(text)
            for chunk in doc.noun_chunks:
                phrase = chunk.text.lower().strip()
                if phrase in keywords:
                    found.add(phrase)

        return list(found)


@dataclass
class TriageService:
    def assess(self, symptoms: List[str]) -> SymptomAnalysis:
        high_risk_signals = {"chest pain", "shortness of breath"}
        medium_risk_signals = {"fever", "dizziness", "persistent cough"}

        symptom_set = set(symptoms)
        if symptom_set & high_risk_signals:
            severity = 8
            risk = RiskLevel.HIGH
            urgency = "Seek immediate medical attention or emergency care."
        elif symptom_set & medium_risk_signals:
            severity = 5
            risk = RiskLevel.MEDIUM
            urgency = "Book an appointment with a healthcare professional within 24-72 hours."
        else:
            severity = 3 if symptoms else 2
            risk = RiskLevel.LOW
            urgency = "Monitor symptoms and consult a clinician if symptoms worsen or persist."

        return SymptomAnalysis(
            symptoms=symptoms,
            severity_score=severity,
            risk_level=risk,
            possible_conditions=["General symptom cluster requiring clinical correlation"],
            urgency_recommendation=urgency,
        )


@dataclass
class DoctorRecommendationService:
    def recommend(self, symptoms: List[str]) -> str:
        joined = " ".join(symptoms).lower()
        if "skin" in joined or "rash" in joined:
            return "Dermatologist"
        if "chest" in joined or "heart" in joined:
            return "Cardiologist"
        if "head" in joined or "dizziness" in joined:
            return "Neurologist"
        if "children" in joined:
            return "Pediatrician"
        return "General Physician"
