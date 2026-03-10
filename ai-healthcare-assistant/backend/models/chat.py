from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class SymptomAnalysis(BaseModel):
    symptoms: List[str]
    severity_score: int  # 1-10 scale
    risk_level: RiskLevel
    possible_conditions: List[str]
    urgency_recommendation: str

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[datetime] = None
    symptom_analysis: Optional[SymptomAnalysis] = None

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    user_id: Optional[str] = None
    symptoms: Optional[List[str]] = None  # Explicit symptom list

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    sources: Optional[List[str]] = None
    symptom_analysis: Optional[SymptomAnalysis] = None
    disclaimer: str = "This is not medical advice. Please consult a healthcare professional for proper diagnosis and treatment."

class Document(BaseModel):
    content: str
    metadata: Optional[dict] = None
    source: Optional[str] = None

class HealthCheck(BaseModel):
    status: str
    timestamp: datetime
    version: str