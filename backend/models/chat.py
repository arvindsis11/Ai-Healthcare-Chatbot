"""
Pydantic models for the AI Healthcare Assistant API
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class SymptomAnalysis(BaseModel):
    """Symptom analysis model"""
    severity_score: int
    risk_level: str  # 'low', 'medium', 'high'
    possible_conditions: list[str]
    urgency_recommendation: str

class ChatRequest(BaseModel):
    """Text-based chat request"""
    message: str
    conversation_id: Optional[str] = None

class VoiceChatRequest(BaseModel):
    """Voice-based chat request"""
    generate_audio: bool = True

class ChatResponse(BaseModel):
    """Chat response model"""
    message: str
    symptom_analysis: Optional[SymptomAnalysis] = None
    audio_url: Optional[str] = None
    transcribed_text: Optional[str] = None
    timestamp: Optional[datetime] = None

class VoiceConfig(BaseModel):
    """Voice configuration"""
    stt_model: str = "whisper-1"
    tts_voice: str = "Rachel"  # ElevenLabs voice
    tts_model: str = "eleven_monolingual_v1"

class AudioUploadResponse(BaseModel):
    """Response for audio upload endpoints"""
    success: bool
    text: Optional[str] = None
    audio_url: Optional[str] = None
    error: Optional[str] = None

class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str
    services: Dict[str, bool]
    timestamp: datetime = datetime.now()