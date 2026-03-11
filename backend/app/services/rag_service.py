from ..repositories.vector_db import VectorDatabase
from .llm_service import LLMService
from typing import List, Dict, Any, Optional
from ..models.chat import SymptomAnalysis
import re

class RAGService:
    def __init__(self, vector_db: VectorDatabase, llm_service: LLMService):
        self.vector_db = vector_db
        self.llm_service = llm_service

    def extract_symptoms_from_text(self, text: str) -> List[str]:
        """Extract potential symptoms from user text using simple NLP."""
        # Common symptom keywords and patterns
        symptom_keywords = [
            'pain', 'fever', 'headache', 'cough', 'nausea', 'vomiting', 'dizziness',
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
            if re.search(pattern, text_lower):
                # Extract the main symptom from the pattern
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

        # Search for relevant medical knowledge
        search_results = self.vector_db.search(question, n_results=5)

        # Extract document contents and sources
        contexts = []
        sources = []

        if search_results['documents']:
            for doc, metadata in zip(
                search_results['documents'][0],
                search_results['metadatas'][0]
            ):
                contexts.append(doc)
                sources.append(metadata.get('source', 'unknown'))

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
            'symptom_analysis': symptom_analysis
        }

    def query(self, question: str, n_results: int = 3) -> Dict[str, Any]:
        """Legacy method for backward compatibility."""
        return self.query_with_symptoms(question)

    def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        """Add new documents to the vector database."""
        self.vector_db.add_documents(documents)

    def clear_documents(self) -> None:
        """Clear all documents from the vector database."""
        self.vector_db.clear_collection()