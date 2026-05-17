import logging
import base64
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from ..services.face_analysis import FaceAnalysisService

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/face-analysis")
async def analyze_face(file: UploadFile = File(...)):
    """Analyze facial indicators for potential health issues."""
    try:
        # Read uploaded file and convert to base64
        image_bytes = await file.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        # Run analysis
        service = FaceAnalysisService()
        result = service.analyze(image_base64)

        return result

    except Exception as e:
        logger.error(f"Face analysis error: {e}")
        raise HTTPException(status_code=500, detail="Error analyzing face image")