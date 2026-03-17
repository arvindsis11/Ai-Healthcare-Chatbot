"""
Demo Application for Symptom Severity Prediction

This script provides a simple CLI interface for users to input symptoms
and receive a severity classification with advice.
"""

import sys
import os
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Add root folder to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.severity_predictor import SymptomSeverityPredictor


# Module-level constant (BEST PRACTICE)
RISK_DESCRIPTIONS = {
    "Low Risk": "Symptoms are mild. Monitor and rest.",
    "Moderate Risk": "Symptoms are moderate. Consider consulting a doctor.",
    "High Risk": "Symptoms are severe. Seek medical attention immediately."
}


def main():
    """
    Run the CLI demo for symptom severity prediction.
    """
    predictor = SymptomSeverityPredictor()

    print("=== Symptom Severity Prediction Prototype ===\n")

    user_input = input("Enter your symptoms separated by commas: ")
    symptoms = [s.strip() for s in user_input.split(",") if s.strip()]

    if not symptoms:
        print("No symptoms entered. Exiting...")
        return

    risk = predictor.predict_severity(symptoms)

    # Color mapping
    color_map = {
        "Low Risk": Fore.GREEN,
        "Moderate Risk": Fore.YELLOW,
        "High Risk": Fore.RED
    }

    color = color_map.get(risk, Fore.WHITE)

    print("\n=== Symptoms Summary ===")
    for s in symptoms:
        print(f"- {s.title()}")

    print("\nPredicted Severity:", color + risk + Style.RESET_ALL)
    print("Advice:", RISK_DESCRIPTIONS[risk])


if __name__ == "__main__":
    main()