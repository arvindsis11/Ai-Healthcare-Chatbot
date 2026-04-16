import logging

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from ..core.dependencies import get_health_report_service
from ..models.chat import HealthReportRequest
from ..services.health_report_service import HealthReportService

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/reports/generate")
async def generate_health_report(
    request: HealthReportRequest,
    report_service: HealthReportService = Depends(get_health_report_service),
) -> StreamingResponse:
    """Generate a downloadable PDF health report from a conversation."""
    try:
        pdf_bytes = report_service.generate_pdf(
            conversation_id=request.conversation_id,
            patient_name=request.patient_name,
        )

        filename = f"health_report_{request.conversation_id[:8]}.pdf"

        return StreamingResponse(
            iter([pdf_bytes]),
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )

    except Exception as e:
        logger.error("Error generating health report: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Error generating health report")
