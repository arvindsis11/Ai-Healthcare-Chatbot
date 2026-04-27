# Medical Knowledge Base Integration (PubMed)

To ensure the AI Healthcare Assistant provides evidence-based information, we have integrated the ability to pull medical abstracts from **PubMed (NCBI Entrez)**.

## Overview
The integration consists of a one-time fetching mechanism that populates the RAG (Retrieval-Augmented Generation) system with peer-reviewed medical literature. This data is then indexed into the vector database (ChromaDB) and used to ground the AI's responses with citations.

## How to Fetch Medical Knowledge
You can trigger a manual fetch of medical literature using the provided script. This script searches PubMed for predefined health topics (fever, headache, etc.) and saves the abstracts as structured YAML data.

### 1. Run the Fetcher Script
From the project root, run:
```bash
python scripts/fetch_pubmed_data.py
```
This will:
- Query the NCBI Entrez API for recent high-impact medical papers.
- Extract titles, abstracts, authors, and publication years.
- Save the results to `data/pubmed/pubmed_knowledge.yml`.

### 2. Ingest the Data into the RAG System
Once the knowledge is fetched, you need to re-index the vector database:
```bash
python scripts/ingest_data.py
```
The ingestion pipeline will automatically pick up the new PubMed data, chunk it, and store it in ChromaDB.

## Data Structure
The fetched PubMed data is stored in the following format:
- **`title`**: The article title.
- **`content`**: The full abstract.
- **`metadata`**:
    - `source`: `pubmed`
    - `pmid`: PubMed ID for citation.
    - `authors`: List of researchers.
    - `year`: Publication year.
    - `topic`: Categorization for the RAG system.

## Citation in AI Responses
When the chatbot uses information retrieved from a PubMed paper, it will include a citation. This is handled by the `RAGService` in the backend and displayed via the `CitationList` component in the frontend.
