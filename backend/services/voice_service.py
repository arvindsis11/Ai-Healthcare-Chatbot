"""
Voice Service for AI Healthcare Assistant
Handles Speech-to-Text and Text-to-Speech functionality
"""

import os
import logging
from pathlib import Path
from typing import Optional
import tempfile
import uuid

try:
    import openai
    from elevenlabs import generate, set_api_key, voices
    from pydub import AudioSegment
    import aiofiles
except ImportError as e:
    logging.error(f"Missing voice dependencies: {e}")
    raise

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class VoiceService:
    """Service for handling voice interactions"""

    def __init__(self):
        # Initialize OpenAI for Whisper
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
        else:
            logger.warning("OPENAI_API_KEY not found - STT will not work")

        # Initialize ElevenLabs for TTS
        self.elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        if self.elevenlabs_api_key:
            set_api_key(self.elevenlabs_api_key)
        else:
            logger.warning("ELEVENLABS_API_KEY not found - TTS will not work")

        # Voice configuration
        self.voice_id = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")  # Default: Rachel
        self.model_id = os.getenv("ELEVENLABS_MODEL_ID", "eleven_monolingual_v1")

        # Create temp directory
        self.temp_dir = Path("temp")
        self.temp_dir.mkdir(exist_ok=True)

    def is_available(self) -> dict:
        """Check if voice services are available"""
        return {
            "stt": bool(self.openai_api_key),
            "tts": bool(self.elevenlabs_api_key),
            "openai_key": bool(self.openai_api_key),
            "elevenlabs_key": bool(self.elevenlabs_api_key)
        }

    async def speech_to_text(self, audio_file_path: str) -> str:
        """
        Convert speech to text using OpenAI Whisper

        Args:
            audio_file_path: Path to audio file

        Returns:
            Transcribed text
        """
        if not self.openai_api_key:
            raise ValueError("OpenAI API key not configured for STT")

        try:
            logger.info(f"Converting speech to text: {audio_file_path}")

            # Convert audio to supported format if needed
            audio_path = await self._prepare_audio_for_whisper(audio_file_path)

            # Use OpenAI Whisper API
            with open(audio_path, "rb") as audio_file:
                transcript = await openai.Audio.atranscribe(
                    model="whisper-1",
                    file=audio_file,
                    language="en"  # Specify English for healthcare context
                )

            text = transcript["text"].strip()
            logger.info(f"STT successful: {len(text)} characters")

            # Clean up temp file if different from input
            if audio_path != audio_file_path:
                Path(audio_path).unlink(missing_ok=True)

            return text

        except Exception as e:
            logger.error(f"STT failed: {e}")
            raise

    async def text_to_speech(self, text: str) -> Optional[str]:
        """
        Convert text to speech using ElevenLabs

        Args:
            text: Text to convert to speech

        Returns:
            Path to generated audio file, or None if failed
        """
        if not self.elevenlabs_api_key:
            logger.warning("ElevenLabs API key not configured - skipping TTS")
            return None

        try:
            logger.info(f"Converting text to speech: {len(text)} characters")

            # Generate speech using ElevenLabs
            audio = generate(
                text=text,
                voice=self.voice_id,
                model=self.model_id
            )

            # Save audio to temp file
            audio_filename = f"tts_{uuid.uuid4()}.mp3"
            audio_path = self.temp_dir / audio_filename

            async with aiofiles.open(audio_path, "wb") as f:
                await f.write(audio)

            logger.info(f"TTS successful: {audio_path}")
            return str(audio_path)

        except Exception as e:
            logger.error(f"TTS failed: {e}")
            return None

    async def _prepare_audio_for_whisper(self, audio_path: str) -> str:
        """
        Prepare audio file for Whisper API
        Whisper supports: flac, m4a, mp3, mp4, mpeg, mpga, oga, ogg, wav, webm

        Args:
            audio_path: Input audio file path

        Returns:
            Path to prepared audio file
        """
        path = Path(audio_path)
        if not path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        # Check if file is already in supported format
        supported_formats = {'.flac', '.m4a', '.mp3', '.mp4', '.mpeg', '.mpga', '.oga', '.ogg', '.wav', '.webm'}
        if path.suffix.lower() in supported_formats:
            return audio_path

        try:
            # Convert to WAV using pydub
            logger.info(f"Converting audio format: {path.suffix} -> .wav")

            audio = AudioSegment.from_file(audio_path)
            wav_path = self.temp_dir / f"converted_{uuid.uuid4()}.wav"
            audio.export(str(wav_path), format="wav")

            return str(wav_path)

        except Exception as e:
            logger.error(f"Audio conversion failed: {e}")
            # Return original file if conversion fails
            return audio_path

    async def get_available_voices(self) -> list:
        """Get list of available ElevenLabs voices"""
        if not self.elevenlabs_api_key:
            return []

        try:
            voices_list = voices()
            return [
                {
                    "voice_id": voice.voice_id,
                    "name": voice.name,
                    "category": voice.category,
                    "labels": voice.labels
                }
                for voice in voices_list
            ]
        except Exception as e:
            logger.error(f"Failed to get voices: {e}")
            return []

    def cleanup_temp_files(self, *file_paths: str):
        """Clean up temporary files"""
        for file_path in file_paths:
            try:
                Path(file_path).unlink(missing_ok=True)
                logger.info(f"Cleaned up temp file: {file_path}")
            except Exception as e:
                logger.warning(f"Failed to cleanup {file_path}: {e}")