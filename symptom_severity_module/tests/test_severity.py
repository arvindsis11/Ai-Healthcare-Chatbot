"""
Unit Tests for Symptom Severity Predictor

This module contains pytest-based unit tests to validate
the correctness of symptom severity classification.

Includes readable console output for better debugging.
"""

import sys
import os
import pytest
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Add root path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.severity_predictor import SymptomSeverityPredictor


# Initialize predictor
predictor = SymptomSeverityPredictor()


# Color mapping for readability
COLOR_MAP = {
    "Low Risk": Fore.GREEN,
    "Moderate Risk": Fore.YELLOW,
    "High Risk": Fore.RED
}


def print_test_case(symptoms, expected_risk, predicted_risk):
    """
    Print formatted test case details for better readability.

    Args:
        symptoms (list): Input symptoms
        expected_risk (str): Expected classification
        predicted_risk (str): Model prediction
    """
    print("\n=== Test Case ===")
    print("Symptoms:", symptoms)

    total_score = 0
    for s in symptoms:
        score = predictor.symptom_scores.get(s.lower(), 0)
        total_score += score
        print(f"- {s.title()}: Score {score}")

    print("Total Score:", total_score)
    print("Expected Risk:", expected_risk)
    print("Predicted Risk:", COLOR_MAP[predicted_risk] + predicted_risk + Style.RESET_ALL)


# ✅ Parametrized tests (BEST PRACTICE)
@pytest.mark.parametrize(
    "symptoms, expected_risk",
    [
        # Low Risk Cases
        (["headache"], "Low Risk"),
        (["fatigue", "runny nose"], "Low Risk"),

        # Moderate Risk Cases
        (["fever", "cough"], "Moderate Risk"),
        (["high fever", "body ache"], "Moderate Risk"),

        # High Risk Cases
        (["chest pain", "shortness of breath"], "High Risk"),
        (["confusion", "persistent high fever", "difficulty breathing"], "High Risk"),
    ]
)
def test_predict_severity(symptoms, expected_risk):
    """
    Test severity prediction for multiple symptom combinations.

    Uses parametrization for scalability and cleaner test design.
    """
    predicted_risk = predictor.predict_severity(symptoms)

    # Print readable output
    print_test_case(symptoms, expected_risk, predicted_risk)

    # Assertion (core unit test validation)
    assert predicted_risk == expected_risk, (
        f"FAIL: Expected {expected_risk}, got {predicted_risk}"
    )


# Optional: run directly without pytest CLI
if __name__ == "__main__":
    pytest.main(["-v", "-s"])