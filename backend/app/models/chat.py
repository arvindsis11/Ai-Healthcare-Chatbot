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
    citations: Optional[List[Dict[str, str]]] = None
    symptom_analysis: Optional[SymptomAnalysis] = None
    detected_language: Optional[str] = None
    recommended_specialist: Optional[str] = None
    disclaimer: str = "This is not medical advice. Please consult a healthcare professional for proper diagnosis and treatment."

class Document(BaseModel):
    content: str
    metadata: Optional[dict] = None
    source: Optional[str] = None

class HealthCheck(BaseModel):
    status: str
    timestamp: datetime
    version: str

class HealthReportRequest(BaseModel):
    conversation_id: str
    patient_name: Optional[str] = None

class ReportSection(BaseModel):
    symptoms_detected: List[str]
    possible_conditions: List[str]
    suggested_precautions: List[str]
    when_to_consult_doctor: str
    summary: str
    severity_score: Optional[int] = None
    risk_level: Optional[str] = None