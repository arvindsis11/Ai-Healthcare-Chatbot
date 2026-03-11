# 🤝 Contributing Guide

Thank you for your interest in contributing to the AI Healthcare Chatbot! This guide will walk you through everything you need to know to make a meaningful contribution.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Before You Start](#before-you-start)
- [Fork and Clone the Repository](#fork-and-clone-the-repository)
- [Setting Up Your Development Environment](#setting-up-your-development-environment)
- [Creating a Branch](#creating-a-branch)
- [Making Changes](#making-changes)
- [Running the Project Locally](#running-the-project-locally)
- [Running Tests](#running-tests)
- [Coding Standards](#coding-standards)
- [Submitting a Pull Request](#submitting-a-pull-request)
- [Types of Contributions](#types-of-contributions)
- [Getting Help](#getting-help)

---

## Code of Conduct

By participating in this project, you agree to be respectful, inclusive, and constructive. We follow the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/).

**Key principles:**
- Be welcoming to newcomers
- Use inclusive language
- Accept constructive criticism graciously
- Focus on what is best for the community

---

## Before You Start

1. **Check existing issues** — Browse [open issues](https://github.com/arvindsis11/Ai-Healthcare-Chatbot/issues) to see what's being worked on
2. **Check existing pull requests** — Make sure nobody is already working on your idea
3. **Open an issue first** — For large changes, open an issue to discuss your approach before coding
4. **Read the docs** — Familiarize yourself with [ARCHITECTURE.md](ARCHITECTURE.md), [SETUP.md](SETUP.md), and [AI_MODEL.md](AI_MODEL.md)

---

## Fork and Clone the Repository

### Step 1: Fork

1. Go to https://github.com/arvindsis11/Ai-Healthcare-Chatbot
2. Click the **Fork** button (top right)
3. This creates a copy under your GitHub account

### Step 2: Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/Ai-Healthcare-Chatbot.git
cd Ai-Healthcare-Chatbot
```

### Step 3: Add Upstream Remote

This keeps your fork in sync with the original repository:

```bash
git remote add upstream https://github.com/arvindsis11/Ai-Healthcare-Chatbot.git
git remote -v
# Should show: origin (your fork) and upstream (original)
```

---

## Setting Up Your Development Environment

Follow the [SETUP.md](SETUP.md) guide to get the project running locally.

**Quick start for the Flask chatbot:**
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python train.py
python app.py
```

**Quick start for the FastAPI backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add your API keys to .env
uvicorn main:app --reload
```

**Quick start for the frontend:**
```bash
cd frontend
npm install
npm run dev
```

---

## Creating a Branch

Always work on a branch, never directly on `main`.

### Branch Naming Convention

Use the format: `type/short-description`

| Type | Use Case | Example |
|------|----------|---------|
| `feature/` | New functionality | `feature/add-diabetes-responses` |
| `fix/` | Bug fixes | `fix/voice-transcription-error` |
| `docs/` | Documentation changes | `docs/update-setup-guide` |
| `refactor/` | Code restructuring | `refactor/llm-service-cleanup` |
| `test/` | Adding or fixing tests | `test/add-chat-api-tests` |
| `chore/` | Maintenance tasks | `chore/update-dependencies` |

**Create your branch:**
```bash
# Make sure you're on main and up-to-date
git checkout main
git pull upstream main

# Create your branch
git checkout -b feature/your-feature-name
```

---

## Making Changes

### What Can You Contribute?

See the [Types of Contributions](#types-of-contributions) section below.

### Tips for Good Changes

1. **Make small, focused commits** — One logical change per commit
2. **Write descriptive commit messages** — See the commit message format below
3. **Add comments to complex code** — Especially for ML logic
4. **Update documentation** — If you change behavior, update the relevant docs
5. **Test your changes** — Make sure nothing breaks

### Commit Message Format

Use [Conventional Commits](https://www.conventionalcommits.org/) format:

```
type(scope): short description

Optional longer description explaining WHY the change was made.
```

**Examples:**
```
feat(data): add diabetes conversation training data
fix(voice): handle webm audio format conversion error
docs(setup): clarify virtual environment activation steps
refactor(llm): extract symptom analysis to separate method
test(api): add tests for /api/chat endpoint
```

**Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

---

## Running the Project Locally

After making changes, verify everything still works:

**Test Flask chatbot:**
```bash
python train.py
python app.py
# Visit http://localhost:5000 and test a conversation
```

**Test FastAPI backend:**
```bash
cd backend
uvicorn main:app --reload
# Visit http://localhost:8000/docs and try the endpoints
```

**Test Frontend:**
```bash
cd frontend
npm run dev
# Visit http://localhost:3000 and test the UI
```

**Test API manually:**
```bash
# Health check
curl http://localhost:8000/health

# Text chat
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I have a headache"}'
```

---

## Running Tests

### Backend Tests (RAG module)

```bash
cd ai-healthcare-assistant
python -m pytest tests/ -v
```

### Frontend Linting

```bash
cd frontend
npm run lint
```

### Manual Testing Checklist

Before submitting a PR, verify:

- [ ] Flask chatbot starts and responds to messages
- [ ] Training completes without errors
- [ ] FastAPI `/health` endpoint returns `{"status": "healthy"}`
- [ ] Chat API returns a response with a message
- [ ] Frontend renders without console errors
- [ ] Dark mode toggle works
- [ ] Voice recording button appears (requires HTTPS or localhost)

---

## Coding Standards

### Python

- Follow **PEP 8** style guidelines
- Use **type hints** for function signatures
- Add **docstrings** to all public functions and classes
- Maximum line length: **79 characters** (PEP 8 standard); tool configuration in this project permits up to **120 characters** for readability in complex expressions
- Use f-strings for string formatting

**Example:**
```python
def analyze_symptoms(message: str) -> Optional[Dict[str, Any]]:
    """
    Analyze symptoms from a user message.
    
    Args:
        message: The user's input message
        
    Returns:
        A dict with severity_score, risk_level, possible_conditions,
        and urgency_recommendation, or None if no symptoms detected.
    """
    # Implementation
```

### TypeScript/React

- Use **TypeScript** types and interfaces — avoid `any`
- Follow **React hooks** best practices
- Use **functional components** (no class components)
- Name components using **PascalCase**
- Name hooks as `useXxx`

**Example:**
```typescript
interface Message {
  id: string
  content: string
  role: 'user' | 'assistant'
  timestamp: Date
}

export function MessageBubble({ message }: { message: Message }) {
  return (
    <div className={`bubble ${message.role}`}>
      {message.content}
    </div>
  )
}
```

### YAML Training Data

When adding new training data:

1. Follow the existing format exactly:
```yaml
- - User trigger phrase
  - Bot response
- - Another trigger
  - Another response
```

2. Ensure responses are:
   - Medically accurate (general advice only)
   - Include disclaimers for serious symptoms
   - Recommend doctor consultation when appropriate

3. Add the file to `data/` and it will be picked up automatically by `train.py`

---

## Submitting a Pull Request

### Step 1: Sync with Upstream

Before submitting, sync your branch with the latest upstream changes:

```bash
git fetch upstream
git rebase upstream/main
```

If there are conflicts, resolve them:
```bash
# Fix conflicts in the editor, then:
git add .
git rebase --continue
```

### Step 2: Push Your Branch

```bash
git push origin feature/your-feature-name
```

### Step 3: Open a Pull Request

1. Go to https://github.com/arvindsis11/Ai-Healthcare-Chatbot
2. You'll see a banner: **"Compare & pull request"** — click it
3. Fill in the PR template:

**PR Title Format:**
```
feat: add diabetes symptom conversation flows
```

**PR Description Template:**
```markdown
## Summary
Brief description of what this PR does.

## Changes Made
- Added `data/diabetes.yml` with 15 conversation pairs
- Updated `README.md` to mention diabetes support
- Added tests for diabetes-related queries

## Testing
Describe how you tested your changes.

## Screenshots (if UI changes)
Add screenshots here.

## Checklist
- [ ] Tested locally
- [ ] Linting passes
- [ ] Documentation updated
- [ ] No sensitive data committed
```

### Step 4: Address Review Feedback

- Respond to all comments
- Make requested changes on your branch
- Push new commits — the PR updates automatically
- Request re-review when ready

---

## Types of Contributions

### 🩺 Healthcare Data
**Adding new YAML training data files**
- New symptom categories (e.g., diabetes, allergies, mental health)
- Improved response quality
- More natural conversation flows

### 🐛 Bug Fixes
- Fix broken API endpoints
- Handle edge cases in voice processing
- Fix UI rendering issues

### ✨ New Features
- New symptom analysis categories
- Improved risk assessment logic
- UI enhancements (accessibility, responsiveness)
- Docker improvements

### 📖 Documentation
- Fix typos or unclear explanations
- Add more examples
- Improve setup instructions
- Add diagrams or screenshots

### 🧪 Tests
- Add unit tests for LLM service
- Add integration tests for API endpoints
- Add component tests for React components

### 🌐 Internationalization
- Translate YAML training data
- Add language detection
- Support multilingual responses

---

## Getting Help

If you're stuck or have questions:

1. **Read the docs** in the `/docs` folder
2. **Check existing issues** on GitHub
3. **Open a new issue** with the `question` label
4. **Ask in the PR** if you have questions about your specific changes

We're happy to help! No question is too small. 🙂
