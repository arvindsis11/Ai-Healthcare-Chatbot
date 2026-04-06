import io
from datetime import datetime
from typing import Optional

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from ..models.chat import ReportSection
from ..repositories.session_repository import SessionRepository
from ..services.llm_service import LLMService

_BRAND_BLUE = colors.HexColor("#0369a1")
_BRAND_LIGHT = colors.HexColor("#e0f2fe")
_RISK_HIGH = colors.HexColor("#dc2626")
_RISK_MEDIUM = colors.HexColor("#d97706")
_RISK_LOW = colors.HexColor("#16a34a")
_SECTION_BG = colors.HexColor("#f8fafc")
_BORDER = colors.HexColor("#cbd5e1")
_TEXT_MUTED = colors.HexColor("#64748b")


def _build_styles() -> dict:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "ReportTitle",
            parent=base["Heading1"],
            fontSize=22,
            textColor=_BRAND_BLUE,
            spaceAfter=4,
            alignment=TA_CENTER,
            fontName="Helvetica-Bold",
        ),
        "subtitle": ParagraphStyle(
            "ReportSubtitle",
            parent=base["Normal"],
            fontSize=10,
            textColor=_TEXT_MUTED,
            spaceAfter=2,
            alignment=TA_CENTER,
        ),
        "section_heading": ParagraphStyle(
            "SectionHeading",
            parent=base["Heading2"],
            fontSize=12,
            textColor=_BRAND_BLUE,
            spaceBefore=14,
            spaceAfter=6,
            fontName="Helvetica-Bold",
        ),
        "body": ParagraphStyle(
            "ReportBody",
            parent=base["Normal"],
            fontSize=10,
            leading=15,
            textColor=colors.HexColor("#1e293b"),
        ),
        "bullet": ParagraphStyle(
            "ReportBullet",
            parent=base["Normal"],
            fontSize=10,
            leading=15,
            leftIndent=14,
            bulletIndent=4,
            textColor=colors.HexColor("#1e293b"),
        ),
        "disclaimer": ParagraphStyle(
            "Disclaimer",
            parent=base["Normal"],
            fontSize=8,
            textColor=_TEXT_MUTED,
            alignment=TA_CENTER,
            leading=12,
        ),
        "meta": ParagraphStyle(
            "MetaInfo",
            parent=base["Normal"],
            fontSize=9,
            textColor=_TEXT_MUTED,
            alignment=TA_LEFT,
        ),
    }


def _risk_color(severity_score: Optional[int]) -> colors.Color:
    if severity_score is None:
        return _RISK_LOW
    if severity_score >= 7:
        return _RISK_HIGH
    if severity_score >= 4:
        return _RISK_MEDIUM
    return _RISK_LOW


def _risk_label(severity_score: Optional[int]) -> str:
    if severity_score is None:
        return "N/A"
    if severity_score >= 7:
        return f"HIGH ({severity_score}/10)"
    if severity_score >= 4:
        return f"MEDIUM ({severity_score}/10)"
    return f"LOW ({severity_score}/10)"


class HealthReportService:
    def __init__(self, session_repository: SessionRepository, llm_service: LLMService) -> None:
        self._sessions = session_repository
        self._llm = llm_service

    def generate_pdf(
        self,
        conversation_id: str,
        patient_name: Optional[str] = None,
    ) -> bytes:
        messages = self._sessions.get_messages(conversation_id)
        history = [{"role": m.role, "content": m.content} for m in messages]

        report: ReportSection = self._llm.generate_report_data(history)

        severity_score: Optional[int] = report.severity_score

        buf = io.BytesIO()
        doc = SimpleDocTemplate(
            buf,
            pagesize=letter,
            leftMargin=0.85 * inch,
            rightMargin=0.85 * inch,
            topMargin=0.75 * inch,
            bottomMargin=0.75 * inch,
        )

        styles = _build_styles()
        story: list = []

        story.append(Paragraph("AI Healthcare Platform", styles["title"]))
        story.append(Paragraph("Patient Health Report", styles["subtitle"]))
        story.append(Spacer(1, 6))
        story.append(HRFlowable(width="100%", thickness=1.5, color=_BRAND_BLUE))
        story.append(Spacer(1, 8))

        meta_rows = [
            ["Report Date:", datetime.utcnow().strftime("%B %d, %Y")],
            ["Conversation ID:", conversation_id],
        ]
        if patient_name:
            meta_rows.insert(0, ["Patient Name:", patient_name])

        meta_table = Table(meta_rows, colWidths=[1.4 * inch, 4.5 * inch])
        meta_table.setStyle(
            TableStyle(
                [
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("TEXTCOLOR", (0, 0), (0, -1), _TEXT_MUTED),
                    ("TEXTCOLOR", (1, 0), (1, -1), colors.HexColor("#1e293b")),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                    ("TOPPADDING", (0, 0), (-1, -1), 3),
                ]
            )
        )
        story.append(meta_table)

        if severity_score is not None:
            risk_rows = [["Overall Risk:", _risk_label(severity_score)]]
            risk_table = Table(risk_rows, colWidths=[1.4 * inch, 4.5 * inch])
            risk_table.setStyle(
                TableStyle(
                    [
                        ("FONTNAME", (0, 0), (0, 0), "Helvetica-Bold"),
                        ("FONTNAME", (1, 0), (1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, -1), 9),
                        ("TEXTCOLOR", (0, 0), (0, 0), _TEXT_MUTED),
                        ("TEXTCOLOR", (1, 0), (1, 0), _risk_color(severity_score)),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                        ("TOPPADDING", (0, 0), (-1, -1), 3),
                    ]
                )
            )
            story.append(risk_table)

        story.append(Spacer(1, 10))

        story.append(Paragraph("Summary", styles["section_heading"]))
        story.append(HRFlowable(width="100%", thickness=0.5, color=_BORDER))
        story.append(Spacer(1, 4))
        story.append(Paragraph(report.summary or "No summary available.", styles["body"]))

        story.append(Paragraph("Symptoms Detected", styles["section_heading"]))
        story.append(HRFlowable(width="100%", thickness=0.5, color=_BORDER))
        story.append(Spacer(1, 4))
        if report.symptoms_detected:
            for symptom in report.symptoms_detected:
                story.append(Paragraph(f"\u2022  {symptom.capitalize()}", styles["bullet"]))
        else:
            story.append(Paragraph("No specific symptoms identified.", styles["body"]))

        story.append(Paragraph("Possible Conditions", styles["section_heading"]))
        story.append(HRFlowable(width="100%", thickness=0.5, color=_BORDER))
        story.append(Spacer(1, 4))
        if report.possible_conditions:
            for condition in report.possible_conditions:
                story.append(Paragraph(f"\u2022  {condition}", styles["bullet"]))
        else:
            story.append(Paragraph("Unable to determine possible conditions.", styles["body"]))

        story.append(Paragraph("Suggested Precautions", styles["section_heading"]))
        story.append(HRFlowable(width="100%", thickness=0.5, color=_BORDER))
        story.append(Spacer(1, 4))
        if report.suggested_precautions:
            for precaution in report.suggested_precautions:
                story.append(Paragraph(f"\u2022  {precaution}", styles["bullet"]))
        else:
            story.append(Paragraph("No specific precautions identified.", styles["body"]))

        story.append(Paragraph("When to Consult a Doctor", styles["section_heading"]))
        story.append(HRFlowable(width="100%", thickness=0.5, color=_BORDER))
        story.append(Spacer(1, 4))
        story.append(
            Paragraph(
                report.when_to_consult_doctor or "Please consult a healthcare professional for guidance.",
                styles["body"],
            )
        )

        story.append(Spacer(1, 20))
        story.append(HRFlowable(width="100%", thickness=0.5, color=_BORDER))
        story.append(Spacer(1, 6))
        story.append(
            Paragraph(
                "MEDICAL DISCLAIMER: This report is generated for informational purposes only and does not constitute "
                "medical advice, diagnosis, or treatment. Always seek the advice of a qualified healthcare provider "
                "with any questions you may have regarding a medical condition.",
                styles["disclaimer"],
            )
        )

        doc.build(story)
        return buf.getvalue()
