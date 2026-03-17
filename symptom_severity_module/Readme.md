# Symptom Severity Predictor Prototype

## Overview

This project is a **standalone prototype** for predicting the severity of symptoms. It classifies user-entered symptoms into **Low Risk, Moderate Risk, or High Risk** using a **rule-based scoring system**.  

## Features

- Rule-based symptom severity prediction  

- Color-coded console output  

- Detailed symptom scores  

- Unit tested with pytest  

## Folder Structure
```
Symptom_Severity_Prototype
├── src/
│   └── severity_predictor.py      # Core logic
├── app/
│   └── demo_app.py                # Interactive demo
├── tests/
│   └── test_severity.py           # Unit tests
├── docs/
│   └── DOCUMENTATION.md           # Detailed documentation
├── requirements.txt               # Dependencies
└── README.md                      # Project overview
```

## Setup

1. Clone the repository:

```bash
git clone <your-repo-url>
cd Symptom_Severity_Prototype
```
2. Create and activate a virtual environment:
```
python -m venv venv
.\venv\Scripts\activate   # Windows
venv/bin/activate   # Linux/macOS
```
3. Install dependencies:
```
pip install -r requirements.txt
```
4. Usage

Run the demo app:
```
python -m app.demo\_app
Enter your symptoms separated by commas, *(e.g.: fever, cough, fatigue)*
```
5. Output shows:
```
Symptoms Summary
Predicted severity (Low / Moderate / High)
Advice based on risk level
```
6. Running Unit Tests
```
pytest -v -s
```
Tests check low, moderate, and high-risk scenarios with readable output.

7. Example Input/Output

    Input:
    headache, fatigue
    
    Output:
    Predicted Risk: Low Risk
    Advice: Symptoms are mild. Monitor and rest.

8. Future Enhancements
    -Machine learning-based classification.
    -Web interface or chatbot integration.
    -Expanded symptom database for more accurate predictions.



For detailed project documentation, see \[DOCUMENTATION](docs/DOCUMENTATION.md)

