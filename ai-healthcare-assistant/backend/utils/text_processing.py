import yaml
import os
from typing import List, Dict, Any
from pathlib import Path

def load_yaml_files(data_dir: str) -> List[Dict[str, Any]]:
    """Load all YAML files from the data directory."""
    documents = []
    data_path = Path(data_dir)

    for yaml_file in data_path.glob("*.yml"):
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Parse YAML content
                data = yaml.safe_load(content)
                if data:
                    documents.append({
                        'content': content,
                        'metadata': {
                            'source': yaml_file.name,
                            'topic': yaml_file.stem,
                            'type': 'conversation',
                            'file_path': str(yaml_file)
                        }
                    })
        except Exception as e:
            print(f"Error loading {yaml_file}: {e}")

    return documents

def preprocess_medical_text(text: str) -> str:
    """Advanced text preprocessing for medical content."""
    # Remove extra whitespace
    text = ' '.join(text.split())

    # Normalize medical terms (basic)
    medical_normalizations = {
        'temp': 'temperature',
        'bp': 'blood pressure',
        'hr': 'heart rate',
        'rr': 'respiratory rate',
        'sob': 'shortness of breath',
        'cp': 'chest pain',
        'abdo': 'abdominal',
        'neuro': 'neurological'
    }

    for abbr, full in medical_normalizations.items():
        text = text.replace(f' {abbr} ', f' {full} ')
        text = text.replace(f' {abbr}.', f' {full}')

    return text.strip()

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """Split text into overlapping chunks, preserving medical context."""
    words = text.split()
    chunks = []

    # For medical content, try to preserve sentence boundaries
    sentences = text.replace('?', '.').replace('!', '.').split('.')
    current_chunk = ""
    current_length = 0

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        sentence_length = len(sentence.split())

        if current_length + sentence_length > chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            # Start new chunk with overlap
            overlap_words = current_chunk.split()[-overlap:]
            current_chunk = ' '.join(overlap_words) + ' ' + sentence
            current_length = len(overlap_words) + sentence_length
        else:
            current_chunk += ' ' + sentence
            current_length += sentence_length

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks if chunks else [text]

def extract_medical_entities(text: str) -> Dict[str, List[str]]:
    """Extract medical entities from text (basic implementation)."""
    # This is a simplified version - in production, use medical NLP libraries
    symptoms = []
    conditions = []
    medications = []

    text_lower = text.lower()

    # Common symptoms
    symptom_list = ['fever', 'headache', 'cough', 'nausea', 'pain', 'fatigue', 'dizziness']
    for symptom in symptom_list:
        if symptom in text_lower:
            symptoms.append(symptom)

    # Common conditions
    condition_list = ['infection', 'flu', 'cold', 'pneumonia', 'migraine']
    for condition in condition_list:
        if condition in text_lower:
            conditions.append(condition)

    # Common medications (basic)
    med_list = ['paracetamol', 'ibuprofen', 'aspirin', 'crocin']
    for med in med_list:
        if med.lower() in text_lower:
            medications.append(med)

    return {
        'symptoms': symptoms,
        'conditions': conditions,
        'medications': medications
    }