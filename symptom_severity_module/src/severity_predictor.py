"""
Severity Predictor Module

This module provides a rule-based implementation for predicting
symptom severity based on predefined symptom scores.
"""

class SymptomSeverityPredictor:
    """
    Predicts symptom severity using a rule-based scoring system.

    Each symptom is assigned a severity score between 1 and 5.
    The total score determines the risk category:

    - Total score ≤ 3  → Low Risk
    - Total score 4–7  → Moderate Risk
    - Total score ≥ 8  → High Risk
    """

    def __init__(self):
        """
        Initialize the predictor with a predefined symptom scoring table.
        """
        self.symptom_scores = {

            # Mild Symptoms (1 point)
            "headache": 1,
            "fatigue": 1,
            "sore throat": 1,
            "runny nose": 1,
            "loss of appetite": 1,
            "skin rash": 1,
            "mild cough": 1,
            "mild fever": 1,
            "muscle weakness": 1,
            "chills": 1,

            # Moderate Symptoms (2–3 points)
            "fever": 2,
            "cough": 2,
            "body ache": 2,
            "nausea": 2,
            "vomiting": 2,
            "diarrhea": 2,
            "loss of taste": 2,
            "loss of smell": 2,
            "dizziness": 2,
            "moderate shortness of breath": 2,
            "moderate headache": 2,
            "moderate fatigue": 2,
            "high fever": 3,
            "persistent cough": 3,
            "chest tightness": 3,
            "abdominal pain": 3,
            "persistent vomiting": 3,
            "severe diarrhea": 3,

            # Severe Symptoms (4–5 points)
            "shortness of breath": 5,
            "chest pain": 5,
            "wheezing": 4,
            "rapid heartbeat": 4,
            "confusion": 5,
            "bluish lips or face": 5,
            "severe dehydration": 5,
            "loss of consciousness": 5,
            "severe chest tightness": 5,
            "persistent high fever": 5,
            "extreme fatigue": 5,
            "severe dizziness": 4,
            "difficulty speaking": 5,
            "severe headache": 5,
            "severe nausea": 4,
            "severe abdominal pain": 5,
            "persistent vomiting and diarrhea": 5,
            "severe body ache": 4,
            "confusion and disorientation": 5,
            "difficulty breathing": 5
        }

    def predict_severity(self, symptoms):
        """
        Predict the severity level based on input symptoms.

        Args:
            symptoms (list[str]): List of symptom names provided by the user.

        Returns:
            str: Severity classification ('Low Risk', 'Moderate Risk', 'High Risk').
        """
        total_score = sum(self.symptom_scores.get(s.lower(), 0) for s in symptoms)

        if total_score <= 3:
            return "Low Risk"
        elif total_score <= 7:
            return "Moderate Risk"
        else:
            return "High Risk"