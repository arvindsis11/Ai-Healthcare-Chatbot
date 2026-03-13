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
symptom_severity_module
├── src/
│   └── severity_predictor.py      # Core logic
├── app/
│   └── demo_app.py                # Interactive demo
├── tests/
│   └── test_severity.py           # Unit tests
├── docs/
│   └── DOCUMENTATION.md           # Detailed documentation
├── requirements.txt               # Dependencies
└── Readme.md                      # Project overview
```

## Setup

1. Navigate to the module directory:

```bash
cd symptom_severity_module
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux/macOS
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the demo app:
```bash
python -m app.demo_app
```

Enter your symptoms separated by commas *(e.g.: fever, cough, fatigue)*

## Output

```
=== Symptoms Summary ===
Predicted severity (Low / Moderate / High)
Advice based on risk level
```

## Running Unit Tests
```bash
pytest -v -s
```

Tests check low, moderate, and high-risk scenarios with readable output.

## Example Input/Output

**Input:**
```
headache, fatigue
```

**Output:**
```
Predicted Risk: Low Risk
Advice: Symptoms are mild. Monitor and rest.
```

## Future Enhancements

- Machine learning-based classification.
- Web interface or chatbot integration.
- Expanded symptom database for more accurate predictions.

---

For detailed project documentation, see [DOCUMENTATION](docs/DOCUMENTATION.md).
