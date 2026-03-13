class SymptomSeverityPredictor:
    """Rule-based symptom severity predictor.

    Classifies a list of symptoms into one of three risk levels:
    - Low Risk: total score <= 3
    - Moderate Risk: total score 4-7
    - High Risk: total score >= 8

    Each symptom is assigned a score from 1 (mild) to 5 (severe).
    Unknown symptoms contribute a score of 0.
    """

    def __init__(self):
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

            # Moderate Symptoms (2-3 points)
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

            # Severe Symptoms (4-5 points)
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
            "difficulty breathing": 5,
        }

    def predict_severity(self, symptoms):
        """Predict the severity risk level for a list of symptoms.

        Args:
            symptoms (list[str]): A list of symptom strings (case-insensitive).

        Returns:
            str: The predicted risk level — 'Low Risk', 'Moderate Risk', or 'High Risk'.
        """
        total_score = sum(self.symptom_scores.get(s.lower(), 0) for s in symptoms)
        if total_score <= 3:
            return "Low Risk"
        elif total_score <= 7:
            return "Moderate Risk"
        else:
            return "High Risk"
