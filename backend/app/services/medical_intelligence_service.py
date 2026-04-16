from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from ..models.chat import DoctorRecommendation, RiskLevel, SymptomAnalysis

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


# Mapping of specialist to (symptom keywords, weight).
# Weight reflects how strongly the keyword indicates that specialist.
SPECIALIST_SYMPTOM_MAP: Dict[str, List[Tuple[str, float]]] = {
    "Cardiologist": [
        ("chest pain", 1.0),
        ("heart palpitations", 1.0),
        ("palpitations", 0.9),
        ("irregular heartbeat", 1.0),
        ("high blood pressure", 0.8),
        ("shortness of breath", 0.6),
        ("swollen ankles", 0.7),
        ("chest tightness", 0.9),
        ("heart", 0.7),
    ],
    "Dermatologist": [
        ("skin rash", 1.0),
        ("rash", 0.9),
        ("acne", 1.0),
        ("eczema", 1.0),
        ("psoriasis", 1.0),
        ("itchy skin", 0.9),
        ("hives", 0.9),
        ("skin lesion", 0.9),
        ("mole", 0.8),
        ("skin", 0.5),
    ],
    "Neurologist": [
        ("severe headache", 1.0),
        ("migraine", 1.0),
        ("seizure", 1.0),
        ("numbness", 0.8),
        ("tingling", 0.8),
        ("dizziness", 0.7),
        ("tremor", 0.9),
        ("memory loss", 0.8),
        ("confusion", 0.7),
        ("headache", 0.6),
    ],
    "Pulmonologist": [
        ("chronic cough", 1.0),
        ("wheezing", 1.0),
        ("asthma", 1.0),
        ("shortness of breath", 0.7),
        ("coughing blood", 1.0),
        ("breathing difficulty", 0.9),
        ("persistent cough", 0.9),
        ("cough", 0.5),
    ],
    "Gastroenterologist": [
        ("abdominal pain", 1.0),
        ("stomach pain", 0.9),
        ("bloating", 0.8),
        ("diarrhea", 0.8),
        ("constipation", 0.8),
        ("acid reflux", 1.0),
        ("heartburn", 0.9),
        ("nausea", 0.6),
        ("vomiting", 0.7),
        ("blood in stool", 1.0),
    ],
    "Orthopedist": [
        ("joint pain", 1.0),
        ("back pain", 1.0),
        ("knee pain", 1.0),
        ("fracture", 1.0),
        ("bone pain", 0.9),
        ("sprain", 0.9),
        ("swollen joint", 0.9),
        ("stiffness", 0.7),
        ("muscle pain", 0.6),
    ],
    "ENT Specialist": [
        ("ear pain", 1.0),
        ("sore throat", 0.8),
        ("hearing loss", 1.0),
        ("tinnitus", 1.0),
        ("nasal congestion", 0.8),
        ("sinus pain", 0.9),
        ("nosebleed", 0.8),
        ("hoarseness", 0.8),
        ("snoring", 0.7),
    ],
    "Ophthalmologist": [
        ("blurred vision", 1.0),
        ("eye pain", 1.0),
        ("vision loss", 1.0),
        ("red eye", 0.9),
        ("eye infection", 1.0),
        ("double vision", 1.0),
        ("floaters", 0.8),
    ],
    "Endocrinologist": [
        ("excessive thirst", 0.9),
        ("frequent urination", 0.8),
        ("weight gain", 0.7),
        ("weight loss", 0.6),
        ("thyroid", 1.0),
        ("diabetes", 1.0),
        ("hormonal imbalance", 1.0),
        ("fatigue", 0.4),
    ],
    "Psychiatrist": [
        ("anxiety", 1.0),
        ("depression", 1.0),
        ("insomnia", 0.8),
        ("panic attack", 1.0),
        ("mood swings", 0.9),
        ("hallucinations", 1.0),
        ("suicidal thoughts", 1.0),
    ],
    "Urologist": [
        ("painful urination", 1.0),
        ("blood in urine", 1.0),
        ("frequent urination", 0.7),
        ("kidney pain", 0.9),
        ("urinary incontinence", 1.0),
    ],
    "Allergist": [
        ("allergic reaction", 1.0),
        ("allergy", 1.0),
        ("sneezing", 0.7),
        ("watery eyes", 0.7),
        ("hives", 0.7),
        ("swelling", 0.6),
    ],
    "Rheumatologist": [
        ("joint swelling", 1.0),
        ("arthritis", 1.0),
        ("lupus", 1.0),
        ("chronic fatigue", 0.7),
        ("morning stiffness", 0.9),
        ("joint pain", 0.6),
    ],
    "Pediatrician": [
        ("child", 0.9),
        ("children", 0.9),
        ("infant", 1.0),
        ("baby", 1.0),
        ("toddler", 1.0),
    ],
}


@dataclass
class DoctorRecommendationService:
    """Recommends a medical specialist based on symptom-to-specialist weighted mapping."""

    _specialist_map: Dict[str, List[Tuple[str, float]]] = field(
        default_factory=lambda: SPECIALIST_SYMPTOM_MAP
    )

    def recommend(self, symptoms: List[str]) -> str:
        """Return the top specialist name (backwards-compatible)."""
        rec = self.recommend_detailed(symptoms)
        return rec.specialist

    def recommend_detailed(self, symptoms: List[str]) -> DoctorRecommendation:
        """Return a structured recommendation with confidence and reasoning."""
        if not symptoms:
            return DoctorRecommendation(
                specialist="General Physician",
                confidence=0.5,
                reasoning="No specific symptoms detected. A General Physician can perform an initial assessment.",
            )

        joined = " ".join(symptoms).lower()
        scores: Dict[str, float] = {}
        matched_keywords: Dict[str, List[str]] = {}

        for specialist, keyword_weights in self._specialist_map.items():
            specialist_score = 0.0
            matches: List[str] = []
            for keyword, weight in keyword_weights:
                if keyword in joined:
                    specialist_score += weight
                    matches.append(keyword)
            if specialist_score > 0:
                scores[specialist] = specialist_score
                matched_keywords[specialist] = matches

        if not scores:
            return DoctorRecommendation(
                specialist="General Physician",
                confidence=0.5,
                reasoning=f"Symptoms ({', '.join(symptoms)}) did not match a specific specialty. A General Physician is recommended for initial evaluation.",
            )

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_specialist, top_score = ranked[0]

        # Confidence: normalize score relative to the max possible for that specialist
        max_possible = sum(w for _, w in self._specialist_map[top_specialist])
        confidence = min(round(top_score / max_possible, 2), 1.0)

        # Build reasoning from matched keywords
        matches_str = ", ".join(matched_keywords[top_specialist])
        reasoning = (
            f"Based on symptoms matching: {matches_str}. "
            f"A {top_specialist} is recommended for further evaluation."
        )

        # Alternatives: next specialists with score > 0, excluding the top one
        alternatives = [s for s, _ in ranked[1:4] if scores[s] > 0]

        return DoctorRecommendation(
            specialist=top_specialist,
            confidence=confidence,
            reasoning=reasoning,
            alternative_specialists=alternatives,
        )
