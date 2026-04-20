# Automated Testing Pipeline

This project uses **GitHub Actions** to automate testing, linting, and building for both the frontend and backend.

## CI/CD Workflows

The following workflows are automatically triggered on **push** or **pull requests** that modify the respective project directories:

1.  **Backend CI (`.github/workflows/backend-ci.yml`)**:
    - Runs Python tests using `pytest` (scanning both `tests/` and `backend/tests/`).
    - Lints the backend code with `ruff`.
    - Builds the Docker image for the backend.

2.  **Frontend CI (`.github/workflows/frontend-ci.yml`)**:
    - Installs Node dependencies.
    - Runs linting (`npm run lint`).
    - Runs tests using `jest` (`npm run test`).
    - Verifies the build (`npm run build`).

## Running Tests Locally

You can run the tests on your local machine to verify changes before pushing.

### Backend Tests
Ensure you have the virtual environment activated and dependencies installed.

```bash
# Run all backend tests
pytest tests/ backend/tests/

# Run a specific test file
pytest tests/test_ci_setup.py
```

### Frontend Tests
Run these from the `frontend/` directory.

```bash
cd frontend
npm run test
```

## How to Trigger the CI Pipeline

To trigger the automated pipeline:
1.  **Commit** your changes to a feature branch.
2.  **Push** the branch to GitHub.
3.  **Open a Pull Request** to the `main` or `develop` branch.
4.  The **Checks** tab on GitHub will show the status of the tests.

## Adding New Tests

- **Backend:** Create new Python files in `backend/tests/` prefixed with `test_`.
- **Frontend:** Create new `.test.ts` or `.test.tsx` files in `frontend/src/__tests__/` or next to their respective components.

---

### Key Test Categories

#### 1. Medical Intelligence Tests (`backend/tests/test_medical_logic.py`)
- **Symptom Extraction:** Verifies that the AI correctly identifies symptoms in natural language.
- **Triage Risk Assessment:** Ensures the system correctly identifies high-risk (emergency) vs. low-risk symptoms.
- **Specialist Recommendations:** Validates that symptoms map correctly to the right medical specialists.

#### 2. API & Security Tests (`backend/tests/test_api_endpoints.py`)
- **API Health:** Verifies the FastAPI endpoints are active.
- **Prompt Injection Protection:** Tests the `PromptGuard` to ensure malicious prompts are blocked with a `400 Bad Request`.

#### 3. Verification Tests
- **Backend:** `tests/test_ci_setup.py` (Simple arithmetic and dependency check).
- **Frontend:** `frontend/src/__tests__/ci_setup.test.ts` (Simple equality check).
