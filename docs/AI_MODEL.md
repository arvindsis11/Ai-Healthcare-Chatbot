# 🤖 AI Models Documentation

This document describes the AI and machine learning models used in the AI Healthcare Chatbot, their training approaches, and how they are integrated into the system.

---

## Table of Contents

- [Overview](#overview)
- [ChatterBot: Retrieval-Based Model](#chatterbot-retrieval-based-model)
  - [Dataset](#dataset)
  - [Training Approach](#training-approach)
  - [Inference Logic](#inference-logic)
- [OpenAI GPT-3.5-Turbo: Language Model](#openai-gpt-35-turbo-language-model)
  - [Integration](#integration)
  - [Medical Prompt Engineering](#medical-prompt-engineering)
  - [Symptom Classification Logic](#symptom-classification-logic)
- [OpenAI Whisper: Speech Recognition](#openai-whisper-speech-recognition)
- [ElevenLabs TTS: Speech Synthesis](#elevenlabs-tts-speech-synthesis)
- [Sentence Transformers: RAG Embeddings](#sentence-transformers-rag-embeddings)
- [ChromaDB: Vector Database](#chromadb-vector-database)
- [Model Comparison Table](#model-comparison-table)
- [Future ML Improvements](#future-ml-improvements)

---

## Overview

The chatbot uses a **multi-model architecture** where different AI/ML components handle specific tasks:

```
User Input
    │
    ├── Text Path
    │       │
    │       ├── ChatterBot (classic mode)
    │       │     └── BestMatch similarity → training data
    │       │
    │       └── GPT-3.5-Turbo (FastAPI mode)
    │               ├── Medical response generation
    │               └── Symptom analysis JSON
    │
    └── Voice Path
            │
            ├── Whisper (speech → text)
            ├── GPT-3.5-Turbo (text → response)
            └── ElevenLabs (response → speech)
```

---

## ChatterBot: Retrieval-Based Model

### What is ChatterBot?

[ChatterBot](https://github.com/gunthercox/ChatterBot) is an open-source Python library that uses machine learning to produce automated responses to an input statement.

**Version used**: 0.8.4

### Dataset

The chatbot is trained on custom YAML healthcare datasets located in the `data/` directory:

| File | Topic | Conversations |
|------|-------|---------------|
| `greetings.yml` | Greetings and farewells | ~20 pairs |
| `fever.yml` | Fever symptoms, crocin, doctor referral | ~15 pairs |
| `headache.yml` | Headache guidance | ~12 pairs |
| `cough.cold.yml` | Cough and cold management | ~12 pairs |
| `fracture.yml` | Bone fracture guidance | ~10 pairs |
| `doctor.yml` | Doctor appointment booking | ~8 pairs |
| `generalhealth.yml` | General health advice | ~15 pairs |
| `botprofile.yml` | Bot identity responses | ~10 pairs |
| `personalinfo.yml` | Personal information handling | ~8 pairs |
| `new.yml` | Miscellaneous health topics | ~10 pairs |

**YAML Format:**
```yaml
- - User trigger message
  - Bot response message
- - Another trigger
  - Another response
```

**Example from `fever.yml`:**
```yaml
- - I am not feeling well.
  - Okay. can you tell me what's wrong? what are your symptoms?
- - My body temperature has raised.
  - This is a symptom of fever, you should take a tablet of crocin after you have your meal.
- - I took crocin.
  - Good, now take some rest and then let me know if you are feeling better after having crocin.
```

### Training Approach

The `train.py` script uses **ListTrainer**:

```python
from chatterbot.trainers import ListTrainer

english_bot = ChatBot('Bot')
english_bot.set_trainer(ListTrainer)

for file in os.listdir('data'):
    convData = open('data/' + file, 'r').readlines()
    english_bot.train(convData)
```

**How ListTrainer works:**
1. Reads each line as a statement
2. Creates sequential pairs (line N is followed by line N+1)
3. Stores each pair with confidence scores in SQLite
4. The BestMatch adapter retrieves the most similar stored response at inference time

### Inference Logic

**BestMatch Adapter:**
- At query time, ChatterBot computes similarity between the user's input and all stored statements
- The algorithm uses **Levenshtein distance** and **Jaccard similarity** to find the best match
- Returns the response associated with the closest matching input

```python
english_bot = ChatBot('Bot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        {'import_path': 'chatterbot.logic.BestMatch'}
    ]
)
response = str(english_bot.get_response(userText))
```

**Limitation**: The model only responds from what it was trained on. Queries outside the training data receive the closest approximate match, which may be inaccurate.

---

## OpenAI GPT-3.5-Turbo: Language Model

### What is GPT-3.5-Turbo?

GPT-3.5-Turbo is OpenAI's large language model capable of understanding context and generating human-like text responses.

**Configuration used:**
```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.3,    # Lower = more consistent, less creative
    max_tokens=1500
)
```

**Why temperature=0.3?** Medical contexts require consistent, accurate responses. Higher temperatures produce more varied (and potentially inaccurate) output.

### Integration

The LLM is integrated via **LangChain**:

```
ChatPromptTemplate
    │  System prompt (medical safety constraints)
    │  Human message (user's input)
    ▼
ChatOpenAI (gpt-3.5-turbo)
    ▼
StrOutputParser
    ▼
Response text
```

### Medical Prompt Engineering

A carefully designed system prompt enforces medical safety:

```python
medical_system_prompt = """
You are a medical assistant AI. You provide helpful, accurate information 
about health and symptoms, but you ALWAYS emphasize that you are not a 
substitute for professional medical advice.

Key principles:
1. Never diagnose conditions
2. Always recommend consulting healthcare professionals
3. Provide general information only
4. Be empathetic and supportive
5. Include appropriate medical disclaimers

When discussing symptoms, focus on:
- General information about possible causes
- When to seek medical attention
- Basic self-care measures
- Preventive measures
"""
```

**Prompt Template:**
```
{medical_system_prompt}

User Message: {message}

Provide a helpful, empathetic response that:
1. Acknowledges the user's concern
2. Provides general health information
3. Gives appropriate self-care advice
4. Strongly recommends professional medical consultation
5. Ends with a medical disclaimer

Response:
```

### Symptom Classification Logic

When symptom-related keywords are detected in the user message, a **second LLM call** performs structured symptom analysis:

**Keyword Detection:**
```python
symptom_keywords = [
    'pain', 'ache', 'hurt', 'sore', 'fever', 'cough', 'nausea',
    'headache', 'dizzy', 'fatigue', 'tired', 'sick', 'ill',
    'symptom', 'feeling', 'stomach', 'chest', 'throat'
]

has_symptoms = any(keyword in message.lower() for keyword in symptom_keywords)
```

**Analysis Prompt:**
```
Analyze the symptoms mentioned in this message and provide a structured assessment.
Return your response as a JSON object with this exact structure:

{
    "severity_score": <number 1-10>,
    "risk_level": "<low|medium|high>",
    "possible_conditions": ["condition1", "condition2"],
    "urgency_recommendation": "<recommendation text>"
}

Guidelines:
- Severity 1-3: Mild, routine care
- Severity 4-6: Moderate, see doctor within days
- Severity 7-10: Severe, immediate attention
- Be conservative with high scores
```

**Severity Scale:**

| Score | Level | Clinical Meaning | Action |
|-------|-------|-----------------|--------|
| 1–3 | 🟢 Mild | Minor discomfort | Self-care, monitor |
| 4–6 | 🟡 Moderate | Noticeable symptoms | See doctor within days |
| 7–10 | 🔴 Severe | Potentially dangerous | Immediate attention |

**Risk Classification:**

| Risk Level | Examples | Recommendation |
|------------|---------|----------------|
| `low` | Mild headache, sniffles | Rest, hydrate, OTC meds |
| `medium` | Persistent fever, chest discomfort | See GP within 48 hrs |
| `high` | Severe chest pain, difficulty breathing | Emergency services (911) |

---

## OpenAI Whisper: Speech Recognition

### What is Whisper?

[Whisper](https://openai.com/research/whisper) is OpenAI's automatic speech recognition (ASR) model trained on 680,000 hours of multilingual and multitask supervised data.

**Model used**: `whisper-1` (via API)

**Supported audio formats**:
- WAV, MP3, M4A, WebM, FLAC, OGG, MP4, MPEG, MPGA

### Integration

```python
# In VoiceService.speech_to_text()
# Uses OpenAI Python SDK v1.0+ syntax
client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

with open(audio_path, "rb") as audio_file:
    transcript = await client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        language="en"   # Specified for healthcare context accuracy
    )

text = transcript.text.strip()
```

**Audio preprocessing** (pydub):
- If the uploaded file is in an unsupported format, it is converted to WAV
- Audio is saved temporarily, processed, then cleaned up

### Why Whisper for Healthcare?

- High accuracy on medical terminology
- Language specified as English for consistent results
- Handles different microphone qualities and accents
- Supports WebM format (default browser recording format)

---

## ElevenLabs TTS: Speech Synthesis

### What is ElevenLabs?

[ElevenLabs](https://elevenlabs.io/) provides state-of-the-art neural text-to-speech synthesis with natural-sounding voices.

**Model used**: `eleven_monolingual_v1`
**Default voice**: Rachel (`21m00Tcm4TlvDq8ikWAM`)

### Integration

```python
from elevenlabs import generate, set_api_key

audio = generate(
    text=response_text,
    voice=self.voice_id,       # Configurable via ENV
    model=self.model_id        # Configurable via ENV
)

# Save to temp file
audio_path = f"temp/tts_{uuid4()}.mp3"
with open(audio_path, "wb") as f:
    f.write(audio)
```

### Voice Configuration

You can configure the voice via environment variables:
```env
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM   # Rachel (default)
ELEVENLABS_MODEL_ID=eleven_monolingual_v1
```

Other available voices can be retrieved via the API:
```python
voices_list = voices()
# Returns: [{ voice_id, name, category, labels }, ...]
```

---

## Sentence Transformers: RAG Embeddings

### What are Sentence Transformers?

[Sentence Transformers](https://www.sbert.net/) are transformer models fine-tuned to produce semantically meaningful sentence embeddings, where similar sentences have similar vector representations.

### Use in RAG Pipeline

```python
# During data ingestion
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
text_chunks = load_yaml_data()  # Parse YAML files

embeddings = model.encode(text_chunks)  # Dense vectors
# Store in ChromaDB
```

**At query time:**
```python
query_embedding = model.encode(user_query)
# ChromaDB similarity search
results = collection.query(
    query_embeddings=[query_embedding.tolist()],
    n_results=5
)
```

**Why Sentence Transformers?**
- Much faster than GPT embeddings for bulk data
- Can run locally without API costs
- `all-MiniLM-L6-v2` is well-suited for semantic similarity tasks

---

## ChromaDB: Vector Database

### What is ChromaDB?

[ChromaDB](https://www.trychroma.com/) is an open-source embedding database designed for AI applications. It stores vector embeddings and enables fast similarity search.

### Use in This Project

```python
import chromadb

client = chromadb.Client()
collection = client.create_collection("healthcare_knowledge")

# Store embeddings
collection.add(
    documents=text_chunks,
    embeddings=embeddings,
    metadatas=[{"source": filename, "topic": topic}],
    ids=[f"doc_{i}" for i in range(len(text_chunks))]
)

# Query
results = collection.query(
    query_embeddings=[query_vector],
    n_results=5,
    include=["documents", "metadatas", "distances"]
)
```

**Similarity Metric**: Cosine similarity (default in ChromaDB)

**Storage**: Persistent on disk — embeddings survive server restarts

---

## Model Comparison Table

| Model | Type | Task | Local/API | Cost |
|-------|------|------|-----------|------|
| ChatterBot BestMatch | Retrieval | Pattern matching | Local | Free |
| GPT-3.5-Turbo | LLM | Response generation | API | Pay-per-token |
| Whisper-1 | ASR | Speech-to-text | API | Pay-per-minute |
| ElevenLabs TTS | Neural TTS | Text-to-speech | API | Pay-per-character |
| Sentence Transformers | Embedding | Vector encoding | Local | Free |
| ChromaDB | Vector DB | Similarity search | Local | Free |

---

## Future ML Improvements

### Short-term
- [ ] **Add more YAML training data** — Expand coverage to more conditions (diabetes, hypertension, allergies)
- [ ] **Improve symptom keywords list** — Use NLP entity recognition instead of keyword matching
- [ ] **Use GPT-4** — Better reasoning and medical accuracy than GPT-3.5

### Medium-term
- [ ] **Fine-tune on medical datasets** — Use PubMedQA, MedQA, or MedMCQA datasets
- [ ] **Named Entity Recognition (NER)** — Use spaCy or Hugging Face models to extract symptoms, medications, and conditions automatically
- [ ] **Multi-turn conversation memory** — Use LangChain's ConversationBufferMemory to maintain context

### Long-term
- [ ] **Local LLM deployment** — Run Llama 3, Mistral, or Phi-3 locally for privacy
- [ ] **Multimodal input** — Allow image input (e.g., photos of rashes, wounds)
- [ ] **Clinical NLP models** — Integrate Bio_ClinicalBERT or Med-PaLM for higher accuracy
- [ ] **Federated learning** — Train models on distributed health data while preserving privacy
- [ ] **RLHF feedback loop** — Collect user feedback ratings to improve response quality over time
