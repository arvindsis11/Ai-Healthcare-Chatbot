"""
AI Healthcare Assistant - Backend API
FastAPI application with voice interaction capabilities
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import tempfile
import uuid
from pathlib import Path
from typing import Optional
import logging

from services.voice_service import VoiceService
from services.llm_service import LLMService
from models.chat import ChatRequest, ChatResponse, VoiceChatRequest

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Healthcare Assistant API",
    description="Healthcare chatbot with voice interaction capabilities",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000", "*"],  # Allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
voice_service = VoiceService()
llm_service = LLMService()

# Create temp directory for audio files
TEMP_DIR = Path("temp")
TEMP_DIR.mkdir(exist_ok=True)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "AI Healthcare Assistant API", "status": "healthy"}

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "services": {
            "voice": voice_service.is_available(),
            "llm": llm_service.is_available()
        }
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Text-based chat endpoint"""
    try:
        logger.info(f"Received chat request: {request.message[:50]}...")

        # Get LLM response
        response = await llm_service.generate_response(request.message)

        return ChatResponse(
            message=response["message"],
            symptom_analysis=response.get("symptom_analysis"),
            audio_url=None  # No audio for text-only responses
        )

    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")

@app.post("/api/chat/voice", response_model=ChatResponse)
async def voice_chat(
    background_tasks: BackgroundTasks,
    audio: UploadFile = File(...),
    generate_audio: bool = True
):
    """Voice-based chat endpoint"""
    try:
        logger.info(f"Received voice chat request, file: {audio.filename}")

        # Validate audio file
        if not audio.filename.lower().endswith(('.wav', '.mp3', '.m4a', '.webm')):
            raise HTTPException(status_code=400, detail="Unsupported audio format")

        # Save uploaded audio temporarily
        temp_audio_path = TEMP_DIR / f"{uuid.uuid4()}_{audio.filename}"
        with open(temp_audio_path, "wb") as buffer:
            content = await audio.read()
            buffer.write(content)

        try:
            # Convert speech to text
            text = await voice_service.speech_to_text(str(temp_audio_path))
            logger.info(f"STT result: {text[:50]}...")

            if not text.strip():
                raise HTTPException(status_code=400, detail="Could not transcribe audio")

            # Get LLM response
            llm_response = await llm_service.generate_response(text)

            response_data = {
                "message": llm_response["message"],
                "symptom_analysis": llm_response.get("symptom_analysis"),
                "transcribed_text": text
            }

            # Generate audio response if requested
            if generate_audio:
                audio_path = await voice_service.text_to_speech(llm_response["message"])
                if audio_path:
                    # Schedule cleanup of temp files
                    background_tasks.add_task(cleanup_files, temp_audio_path, audio_path)

                    # Return audio URL (in a real deployment, this would be a proper URL)
                    response_data["audio_url"] = f"/api/audio/{Path(audio_path).name}"
                else:
                    background_tasks.add_task(cleanup_files, temp_audio_path)
            else:
                background_tasks.add_task(cleanup_files, temp_audio_path)

            return ChatResponse(**response_data)

        except Exception as e:
            # Clean up on error
            if temp_audio_path.exists():
                temp_audio_path.unlink()
            raise e

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Voice chat error: {e}")
        raise HTTPException(status_code=500, detail=f"Voice processing failed: {str(e)}")

@app.get("/api/audio/{filename}")
async def get_audio(filename: str):
    """Serve generated audio files"""
    audio_path = TEMP_DIR / filename
    if not audio_path.exists():
        raise HTTPException(status_code=404, detail="Audio file not found")

    return FileResponse(
        path=audio_path,
        media_type="audio/mpeg",
        filename=filename
    )

@app.post("/api/voice/stt")
async def speech_to_text_only(audio: UploadFile = File(...)):
    """Convert speech to text only"""
    try:
        # Save uploaded audio temporarily
        temp_audio_path = TEMP_DIR / f"{uuid.uuid4()}_{audio.filename}"
        with open(temp_audio_path, "wb") as buffer:
            content = await audio.read()
            buffer.write(content)

        try:
            text = await voice_service.speech_to_text(str(temp_audio_path))
            return {"text": text, "success": True}
        finally:
            # Clean up temp file
            if temp_audio_path.exists():
                temp_audio_path.unlink()

    except Exception as e:
        logger.error(f"STT error: {e}")
        raise HTTPException(status_code=500, detail=f"Speech to text failed: {str(e)}")

@app.post("/api/voice/tts")
async def text_to_speech_only(text: str):
    """Convert text to speech only"""
    try:
        audio_path = await voice_service.text_to_speech(text)
        if audio_path:
            filename = Path(audio_path).name
            return {
                "audio_url": f"/api/audio/{filename}",
                "success": True
            }
        else:
            raise HTTPException(status_code=500, detail="TTS generation failed")

    except Exception as e:
        logger.error(f"TTS error: {e}")
        raise HTTPException(status_code=500, detail=f"Text to speech failed: {str(e)}")

def cleanup_files(*file_paths: Path):
    """Clean up temporary files"""
    for file_path in file_paths:
        try:
            if file_path.exists():
                file_path.unlink()
                logger.info(f"Cleaned up file: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to cleanup {file_path}: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)