from ..repositories.vector_db import VectorDatabase
from .llm_service import LLMService
from typing import List, Dict, Any, Optional
from ..models.chat import SymptomAnalysis
import re


def _keyword_overlap_score(query: str, content: str) -> float:
    query_terms = {token for token in re.findall(r"\w+", query.lower()) if len(token) > 2}
    doc_terms = {token for token in re.findall(r"\w+", content.lower()) if len(token) > 2}
    if not query_terms or not doc_terms:
        return 0.0
    return len(query_terms & doc_terms) / max(len(query_terms), 1)

class RAGService:
    def __init__(self, vector_db: VectorDatabase, llm_service: LLMService):
        self.vector_db = vector_db
        self.llm_service = llm_service

    def extract_symptoms_from_text(self, text: str) -> List[str]:
        """Extract potential symptoms from user text using simple NLP."""
        # Common symptom keywords and patterns
        symptom_keywords = [
            'pain', 'fever', 'headache', 'cough', 'nausea', 'nauseous', 'vomiting', 'dizziness',
            'fatigue', 'weakness', 'rash', 'sore throat', 'runny nose', 'congestion',
            'chest pain', 'shortness of breath', 'abdominal pain', 'diarrhea',
            'constipation', 'joint pain', 'muscle pain', 'back pain', 'neck pain',
            'itching', 'swelling', 'bruising', 'bleeding', 'coughing', 'sneezing',
            'chills', 'sweating', 'loss of appetite', 'weight loss', 'insomnia'
        ]

        text_lower = text.lower()
        found_symptoms = []

        for symptom in symptom_keywords:
            if symptom in text_lower:
                found_symptoms.append(symptom)

        # Also look for symptom descriptions
        symptom_patterns = [
            r'feeling (?:very |really |so )?(?:sick|unwell|ill|nauseous|dizzy|tired|weak)',
            r'have (?:a |an )?(?:severe |bad |terrible )?(?:headache|stomach ache|cough|fever)',
            r'(?:my |the )?(?:head|stomach|throat|chest|back|neck|arm|leg|knee|shoulder) (?:hurts|aches|pains)',
            r'temperature (?:is |was )?(?:high|elevated|above \d+)',
            r'been (?:vomiting|throwing up|coughing|sneezing|bleeding)'
        ]

        for pattern in symptom_patterns:
            match = re.search(pattern, text_lower)
            if match:
                found_symptoms.append(match.group().strip())

        # Remove duplicates and return
        return list(set(found_symptoms))

    def query_with_symptoms(self, question: str, explicit_symptoms: Optional[List[str]] = None) -> Dict[str, Any]:
        """Enhanced RAG query with symptom analysis."""
        # Extract symptoms from the question if not provided explicitly
        symptoms = explicit_symptoms or self.extract_symptoms_from_text(question)

        # Analyze symptoms
        symptom_analysis = self.llm_service.analyze_symptoms(symptoms, question)

        # Hybrid retrieval: vector retrieval + lexical reranking.
        search_results = self.vector_db.search(question, n_results=8)

        candidates: List[Dict[str, Any]] = []
        if search_results.get("documents"):
            for idx, (doc, metadata) in enumerate(
                zip(search_results["documents"][0], search_results["metadatas"][0])
            ):
                candidates.append(
                    {
                        "rank": idx,
                        "content": doc,
                        "metadata": metadata or {},
                        "vector_distance": search_results.get("distances", [[None]])[0][idx]
                        if search_results.get("distances")
                        else None,
                        "keyword_score": _keyword_overlap_score(question, doc),
                    }
                )

        reranked = sorted(
            candidates,
            key=lambda item: (
                item["keyword_score"],
                -(item["rank"]),
            ),
            reverse=True,
        )[:5]

        # Chunk context snippets for more focused prompts.
        contexts: List[str] = []
        sources: List[str] = []
        citations: List[Dict[str, str]] = []

        for item in reranked:
            source = item["metadata"].get("source", "unknown")
            chunk = self._chunk_text(item["content"], max_words=80)[:2]
            for i, text_chunk in enumerate(chunk):
                contexts.append(text_chunk)
                citation_id = f"{source}#chunk-{i + 1}"
                citations.append(
                    {
                        "id": citation_id,
                        "source": source,
                        "excerpt": text_chunk[:220],
                    }
                )
            sources.append(source)

        # Generate medical response with analysis
        response = self.llm_service.generate_medical_response(
            question,
            contexts,
            symptom_analysis
        )

        return {
            'response': response,
            'sources': sources,
            'contexts': contexts,
            'symptom_analysis': symptom_analysis,
            'citations': citations,
        }

    def query(self, question: str, n_results: int = 3) -> Dict[str, Any]:
        """Legacy method for backward compatibility."""
        return self.query_with_symptoms(question)

    def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        """Add new documents to the vector database."""
        expanded_docs: List[Dict[str, Any]] = []
        for doc in documents:
            content = doc.get("content", "")
            metadata = doc.get("metadata", {})
            chunks = self._chunk_text(content)
            for idx, chunk in enumerate(chunks):
                expanded_docs.append(
                    {
                        "content": chunk,
                        "metadata": {
                            **metadata,
                            "chunk_index": idx,
                            "chunk_total": len(chunks),
                        },
                    }
                )

        self.vector_db.add_documents(expanded_docs)

    def clear_documents(self) -> None:
        """Clear all documents from the vector database."""
        self.vector_db.clear_collection()

    def _chunk_text(self, text: str, max_words: int = 120) -> List[str]:
        words = text.split()
        if len(words) <= max_words:
            return [text]

        chunks = []
        start = 0
        while start < len(words):
            end = start + max_words
            chunks.append(" ".join(words[start:end]))
            start += max_words // 2
        return chunks