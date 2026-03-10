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
                            'type': 'conversation'
                        }
                    })
        except Exception as e:
            print(f"Error loading {yaml_file}: {e}")

    return documents

def preprocess_text(text: str) -> str:
    """Basic text preprocessing for medical content."""
    # Remove extra whitespace
    text = ' '.join(text.split())
    # Basic cleaning
    return text.strip()

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """Split text into overlapping chunks."""
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)

    return chunks