# Symptom_Severity_Prototype/app/demo_app.py

import sys
import os
from colorama import Fore, Style, init

# Initialize colorama for Windows
init(autoreset=True)

# Add root folder to sys.path for importing src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.severity_predictor import SymptomSeverityPredictor

def main():
    predictor = SymptomSeverityPredictor()

    print("=== Symptom Severity Prediction Prototype ===\n")
    user_input = input("Enter your symptoms separated by commas: ")
    symptoms = [s.strip() for s in user_input.split(",") if s.strip()]

    if not symptoms:
        print("No symptoms entered. Exiting...")
        return

    risk = predictor.predict_severity(symptoms)

    # Color-coded output
    color_map = {
        "Low Risk": Fore.GREEN,
        "Moderate Risk": Fore.YELLOW,
        "High Risk": Fore.RED
    }
    color = color_map.get(risk, Fore.WHITE)

    # Print summary
    print("\n=== Symptoms Summary ===")
    for s in symptoms:
        #score = predictor.symptom_scores.get(s.lower(), 0)
        print(f"- {s.title()}")

    # Risk output and advice
    risk_description = {
        "Low Risk": "Symptoms are mild. Monitor and rest.",
        "Moderate Risk": "Symptoms are moderate. Consider consulting a doctor.",
        "High Risk": "Symptoms are severe. Seek medical attention immediately."
    }

    print("\nPredicted Severity:", color + risk + Style.RESET_ALL)
    print("Advice:", risk_description[risk])

if __name__ == "__main__":
    main()
