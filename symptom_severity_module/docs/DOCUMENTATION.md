**Path:** `Symptom_Severity_Prototype/DOCUMENTATION.md`

# Symptom Severity Prediction Prototype – Detailed Documentation

## 1. Introduction
This prototype predicts **severity of symptoms** (Low, Moderate, High) using a **rule-based scoring system**. It is standalone, modular, and can later be integrated into larger healthcare systems.

## 2. Features
- Rule-based severity classification
- Color-coded terminal output
- Detailed scoring for each symptom
- Unit tested for reliability
- Easy to extend to machine learning

## 3. Architecture & Workflow
1. **User Input:** Enter symptoms via console (comma-separated).
2. **Preprocessing:** Symptoms are cleaned and matched to scoring table.
3. **Scoring:** Each symptom has a score (1–5).
4. **Severity Classification:**
   - Total score ≤ 3 → Low Risk
   - Total score 4–7 → Moderate Risk
   - Total score ≥ 8 → High Risk
5. **Output:** Display scores, predicted risk, and advice.

**Flowchart:**
User Input → Preprocess Symptoms → Calculate Scores → Classify Risk → Display Result

## 4. Folder Structure
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

## 5. Symptom Scoring Table

| Symptom                            | Score | Risk Level      |
|------------------------------------|-------|-----------------|
| Headache, Fatigue, Mild Cough      | 1     | Low Risk        |
| Fever, Body Ache, Nausea           | 2–3   | Moderate Risk   |
| Chest Pain, Shortness of Breath    | 4–5   | High Risk       |
| Confusion, Loss of Consciousness   | 5     | High Risk       |
| Persistent Vomiting/Diarrhea       | 3–5   | Moderate–High   |
| Severe Fatigue, Severe Headache    | 4–5   | High Risk       |

## 6. Example Inputs & Outputs

| Input Symptoms                              | Predicted Risk | Advice                                    |
|---------------------------------------------|----------------|-------------------------------------------|
| headache, fatigue                           | Low Risk       | Monitor and rest                          |
| fever, cough, fatigue                       | Moderate Risk  | Consider consulting a doctor              |
| chest pain, shortness of breath, confusion  | High Risk      | Seek medical attention immediately        |

## 7. Unit Testing

Run tests:
```bash
cd symptom_severity_module
pytest -v -s
```

Tests include:
- Low-risk scenarios
- Moderate-risk scenarios
- High-risk scenarios

Outputs symptom scores, expected vs predicted risk, and PASS/FAIL.

## 8. Setup Instructions

- Clone repository.
- Create virtual environment.
- Install dependencies via `pip install -r requirements.txt`.
- Run demo or unit tests.

## 9. Future Enhancements

- Add ML-based classifier for dynamic predictions.
- Extend symptoms database.
- Web or chatbot interface.
- Integrate confidence scoring.

## 10. Contribution Guidelines

- Keep prototype standalone.
- Update documentation and tests for any new symptoms.
- Use `src/severity_predictor.py` for integration in larger projects.
