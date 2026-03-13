# Symptom_Severity_Prototype/tests/test_severity.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from colorama import Fore, Style, init
from src.severity_predictor import SymptomSeverityPredictor

init(autoreset=True)  # Color output

predictor = SymptomSeverityPredictor()

color_map = {
    "Low Risk": Fore.GREEN,
    "Moderate Risk": Fore.YELLOW,
    "High Risk": Fore.RED
}

def run_test_case(symptoms, expected_risk):
    """Run a single test case with symptoms and expected risk."""
    risk = predictor.predict_severity(symptoms)

    # Print details for readability
    print("\n=== Test Case ===")
    print("Symptoms:", symptoms)
    for s in symptoms:
        print(f"- {s.title()}: Score {predictor.symptom_scores.get(s.lower(), 0)}")
    print("Expected Risk:", expected_risk)
    print("Predicted Risk:", color_map[risk] + risk + Style.RESET_ALL)

    # Assertion ensures this is a unit test
    assert risk == expected_risk, f"FAIL: Expected {expected_risk}, got {risk}"

# Unit test functions
def test_low_risk():
    run_test_case(["headache"], "Low Risk")
    run_test_case(["fatigue", "runny nose"], "Low Risk")

def test_moderate_risk():
    run_test_case(["fever", "cough"], "Moderate Risk")
    run_test_case(["high fever", "body ache"], "Moderate Risk")

def test_high_risk():
    run_test_case(["chest pain", "shortness of breath"], "High Risk")
    run_test_case(["confusion", "persistent high fever", "difficulty breathing"], "High Risk")

# Optional: to run this script directly without pytest
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
