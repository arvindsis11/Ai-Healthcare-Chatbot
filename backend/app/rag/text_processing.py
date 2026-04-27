import yaml
from typing import List, Dict, Any
from pathlib import Path

def load_yaml_files(data_dir: str) -> List[Dict[str, Any]]:
    """Load all YAML files from the data directory, supporting both flat and structured data."""
    documents = []
    data_path = Path(data_dir)

    for yaml_file in data_path.rglob("*.yml"):
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                try:
                    # Parse YAML content
                    data = yaml.load(f, Loader=yaml.SafeLoader)
                except yaml.YAMLError as e:
                    print(f"YAML Syntax Error in {yaml_file}: {e}")
                    continue
                
                if not data:
                    continue
                
                # If it's a list of documents (like PubMed data or conversation pairs)
                if isinstance(data, list):
                    for item in data:
                        # If the item is a dictionary (like PubMed abstract)
                        if isinstance(item, dict):
                            content = item.get('content', str(item))
                            item_metadata = item.get('metadata', {})
                        # If the item is a list (like a Q&A pair [Q, A])
                        elif isinstance(item, list):
                            content = "\n".join([str(x) for x in item])
                            item_metadata = {'type': 'conversation'}
                        # If the item is something else (like a simple string)
                        else:
                            content = str(item)
                            item_metadata = {}

                        documents.append({
                            'content': content,
                            'metadata': {
                                'source': yaml_file.name,
                                'topic': yaml_file.stem,
                                'file_path': str(yaml_file),
                                **item_metadata
                            }
                        })
                # If it's a single document or simple KV pair
                else:
                    documents.append({
                        'content': str(data),
                        'metadata': {
                            'source': yaml_file.name,
                            'topic': yaml_file.stem,
                            'type': 'document',
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