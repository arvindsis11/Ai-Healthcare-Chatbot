You are a senior software architect and AI systems engineer.

Your task is to analyze the entire repository and generate a COMPLETE technical report describing the current state of the project.

This report will be used for architecture redesign and enterprise upgrades.

IMPORTANT RULES

1. Analyze ALL directories and files in the repository.
2. Do NOT skip files even if they seem small.
3. Identify the real architecture of the project.
4. Explain how each component interacts with others.
5. Detect duplicate systems or legacy components.
6. Provide a detailed and structured report.

OUTPUT FORMAT

Generate a markdown document called:

PROJECT_ANALYSIS.md

The report must contain the following sections.

--------------------------------------------------

# 1. Project Overview

Explain the purpose of the project.

Include:

- project type
- problem it solves
- main features
- target users

--------------------------------------------------

# 2. Technology Stack

Identify all technologies used.

Example categories:

Backend
Frontend
AI / ML
Vector Database
Voice AI
DevOps
Testing

For each technology explain:

- where it is used
- why it is used

--------------------------------------------------

# 3. Repository Structure

Analyze the folder structure.

Provide a tree like:

repo/
 ├ backend/
 ├ frontend/
 ├ data/
 ├ scripts/
 ├ docs/

Explain the responsibility of each folder.

--------------------------------------------------

# 4. Backend Architecture

Explain:

- FastAPI structure
- API routes
- services layer
- models
- RAG pipeline
- vector database usage

Describe how requests flow through the system.

Example:

User request
 → API route
 → service
 → vector retrieval
 → LLM generation
 → response

--------------------------------------------------

# 5. Frontend Architecture

Explain:

- Next.js structure
- components
- state management
- API integration
- UI features

Include component hierarchy.

--------------------------------------------------

# 6. AI / ML System

Explain all AI components:

LLM
RAG
Embeddings
Voice AI
Symptom analysis

Explain how they interact.

Example flow:

User question
 → embedding
 → vector search
 → retrieved context
 → LLM prompt
 → response

--------------------------------------------------

# 7. Data Pipeline

Explain:

- YAML datasets
- ingestion pipeline
- embedding generation
- vector storage

--------------------------------------------------

# 8. API Endpoints

List all API endpoints with purpose.

Example:

POST /api/chat
GET /health

Explain request/response structure.

--------------------------------------------------

# 9. Configuration & Environment Variables

Identify:

.env variables
config files

Explain their purpose.

--------------------------------------------------

# 10. Dependencies

List major dependencies.

Explain their role.

Example:

FastAPI
LangChain
ChromaDB
OpenAI
SentenceTransformers

--------------------------------------------------

# 11. Deployment Architecture

Explain how the system runs locally and in production.

Include:

Docker
docker-compose
NGINX
CI/CD

--------------------------------------------------

# 12. Current Strengths

Explain what is already well designed.

Examples:

good modularity
clear AI pipeline
good documentation

--------------------------------------------------

# 13. Architectural Problems

Identify issues such as:

duplicate systems
legacy code
tight coupling
missing security
scalability issues

--------------------------------------------------

# 14. Enterprise Readiness Score

Rate the project from 1–10 for:

architecture
scalability
security
AI pipeline
DevOps
documentation

--------------------------------------------------

# 15. Recommended Improvements

List improvements categorized by priority.

High Priority
Medium Priority
Low Priority

--------------------------------------------------

# 16. Suggested Enterprise Architecture

Propose an improved architecture for the project.

--------------------------------------------------

IMPORTANT

Write the report in a way that a new developer could understand the entire project without reading the code.

The output must be a structured markdown file.