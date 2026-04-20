from unittest.mock import MagicMock

from backend.app.models.chat import ReportSection
from backend.app.services.health_report_service import HealthReportService


def _make_report(**kwargs) -> ReportSection:
    defaults = dict(
        symptoms_detected=["headache", "fever"],
        possible_conditions=["viral infection"],
        suggested_precautions=["rest", "stay hydrated"],
        when_to_consult_doctor="See a doctor if symptoms persist beyond 3 days.",
        summary="Patient reports headache and fever.",
    )
    defaults.update(kwargs)
    return ReportSection(**defaults)


def _make_service(report: ReportSection, messages=None) -> HealthReportService:
    session_repo = MagicMock()
    session_repo.get_messages.return_value = messages or []

    llm = MagicMock()
    llm.generate_report_data.return_value = report

    return HealthReportService(session_repo, llm)


def test_report_section_defaults():
    report = ReportSection(
        symptoms_detected=[],
        possible_conditions=[],
        suggested_precautions=[],
        when_to_consult_doctor="Consult a doctor.",
        summary="No data.",
    )
    assert report.severity_score is None
    assert report.risk_level is None


def test_report_section_with_severity():
    report = _make_report(severity_score=7, risk_level="high")
    assert report.severity_score == 7
    assert report.risk_level == "high"


def test_generate_pdf_returns_bytes():
    report = _make_report()
    service = _make_service(report)
    pdf = service.generate_pdf("conv-123")
    assert isinstance(pdf, bytes)
    assert pdf[:4] == b"%PDF"


def test_generate_pdf_with_patient_name():
    report = _make_report()
    service = _make_service(report)
    pdf = service.generate_pdf("conv-abc", patient_name="Jane Doe")
    assert isinstance(pdf, bytes)
    assert pdf[:4] == b"%PDF"


def test_generate_pdf_includes_risk_level():
    report = _make_report(severity_score=8, risk_level="high")
    service = _make_service(report)
    pdf = service.generate_pdf("conv-xyz")
    assert isinstance(pdf, bytes)
    assert len(pdf) > 0


def test_generate_pdf_without_severity_score():
    report = _make_report(severity_score=None)
    service = _make_service(report)
    pdf = service.generate_pdf("conv-no-risk")
    assert isinstance(pdf, bytes)
    assert pdf[:4] == b"%PDF"


def test_generate_report_data_fallback_no_llm():
    from backend.app.services.llm_service import LLMService

    llm = LLMService(api_key="")
    history = [
        {"role": "user", "content": "I have a headache and fever"},
        {"role": "assistant", "content": "I recommend rest and hydration."},
    ]
    result = llm.generate_report_data(history)
    assert isinstance(result, ReportSection)
    assert "headache" in result.symptoms_detected or "fever" in result.symptoms_detected
    assert len(result.suggested_precautions) > 0
    assert result.when_to_consult_doctor


def test_generate_report_data_fallback_empty_history():
    from backend.app.services.llm_service import LLMService

    llm = LLMService(api_key="")
    result = llm.generate_report_data([])
    assert isinstance(result, ReportSection)
    assert result.summary
