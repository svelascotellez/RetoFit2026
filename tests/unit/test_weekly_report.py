"""
Pruebas Unitarias para el Modulo de Dominio y Servicio de Reporte Semanal
Criterios EARS: AC-6.1, AC-6.2, AC-6.3
"""
import pytest
from src.domain.weekly_report import (
    WeeklyReport,
    WeeklyParticipantReportItem,
    get_expected_contribution_for_week,
)


def test_ac_6_1_weekly_compliance_and_penalties() -> None:
    """Verifica calculo de dias exitosos, cumplimiento fisico (>= 4 dias) y penalizacion."""
    item_met = WeeklyParticipantReportItem.calculate(
        participant_id="P1",
        name="Participante Cumplidor",
        successful_days=4,
        total_contributed=200.0,
        week_number=1,
        is_week_closed=False,
    )
    assert item_met.is_met is True
    assert item_met.penalty == 0.0
    assert item_met.successful_days == 4

    item_missed = WeeklyParticipantReportItem.calculate(
        participant_id="P2",
        name="Participante No Cumplidor",
        successful_days=2,
        total_contributed=200.0,
        week_number=1,
        is_week_closed=False,
    )
    assert item_missed.is_met is False
    assert item_missed.penalty == 100.0
    assert item_missed.successful_days == 2


def test_ac_6_2_calendar_quotas_and_financial_status() -> None:
    """Verifica el calendario oficial de cuotas exigibles y el estatus financiero."""
    # Calendario oficial:
    # Semanas 1 y 2: $200.00
    # Semanas 3 y 4: $400.00
    # Semanas 5 y 6: $600.00
    # Semanas 7 y 8: $800.00
    # Semana 9: $900.00
    assert get_expected_contribution_for_week(1) == 200.0
    assert get_expected_contribution_for_week(2) == 200.0
    assert get_expected_contribution_for_week(3) == 400.0
    assert get_expected_contribution_for_week(4) == 400.0
    assert get_expected_contribution_for_week(5) == 600.0
    assert get_expected_contribution_for_week(6) == 600.0
    assert get_expected_contribution_for_week(7) == 800.0
    assert get_expected_contribution_for_week(8) == 800.0
    assert get_expected_contribution_for_week(9) == 900.0

    # Evaluacion de estatus de cuota:
    item_up_to_date = WeeklyParticipantReportItem.calculate(
        participant_id="P1",
        name="Mariana",
        successful_days=5,
        total_contributed=200.0,
        week_number=1,
    )
    assert item_up_to_date.expected_contribution == 200.0
    assert item_up_to_date.financial_status == "AL_CORRIENTE"
    assert item_up_to_date.pending_amount == 0.0

    item_pending = WeeklyParticipantReportItem.calculate(
        participant_id="P2",
        name="Carlos",
        successful_days=3,
        total_contributed=100.0,
        week_number=1,
    )
    assert item_pending.expected_contribution == 200.0
    assert item_pending.financial_status == "PENDIENTE"
    assert item_pending.pending_amount == 100.0


def test_ac_6_3_invalid_week_rejection() -> None:
    """Verifica que semanas fuera del rango 1 a 9 lanzan ValueError."""
    with pytest.raises(ValueError, match="El numero de semana debe estar entre 1 y 9"):
        get_expected_contribution_for_week(0)

    with pytest.raises(ValueError, match="El numero de semana debe estar entre 1 y 9"):
        get_expected_contribution_for_week(10)

    with pytest.raises(ValueError, match="El numero de semana debe estar entre 1 y 9"):
        WeeklyReport(week_number=0, total_participants=0)

    with pytest.raises(ValueError, match="El numero de semana debe estar entre 1 y 9"):
        WeeklyReport(week_number=10, total_participants=0)


def test_service_get_weekly_report_calculation() -> None:
    """Verifica que ChallengeService calcula metricas de reporte semanal agregadas."""
    from src.application.challenge_service import ChallengeService
    from src.application.dto import RegisterParticipantDTO, RecordPaymentDTO, RecordActivityDTO

    service = ChallengeService()
    service.register_participant(RegisterParticipantDTO(id="P1", name="Mariana"))
    service.register_participant(RegisterParticipantDTO(id="P2", name="Carlos"))

    # P1 abona $200 (al corriente semana 1) y registra 4 dias exitosos
    service.record_payment(RecordPaymentDTO(participant_id="P1", amount=200.0))
    for day in range(1, 5):
        service.record_daily_activity(RecordActivityDTO(participant_id="P1", week_number=1, day_of_week=day, calories=350, steps=5000))

    # P2 abona $50 (pendiente $150 para semana 1) y registra 2 dias exitosos
    service.record_payment(RecordPaymentDTO(participant_id="P2", amount=50.0))
    for day in range(1, 3):
        service.record_daily_activity(RecordActivityDTO(participant_id="P2", week_number=1, day_of_week=day, calories=350, steps=5000))

    report = service.get_weekly_report(1)
    assert report.week_number == 1
    assert report.total_participants == 2
    assert report.met_count == 1
    assert report.missed_count == 1
    assert report.compliance_rate == 50.0
    assert report.expected_contribution_per_participant == 200.0
    assert report.total_expected_funds == 400.0
    assert report.total_collected_funds == 250.0
    assert report.participants_up_to_date == 1
    assert report.participants_behind == 1
    assert report.is_closed is False
    assert report.pool_amount == 100.0
    assert report.gain_per_compliant == 100.0

    p1_report = next(p for p in report.participants if p.participant_id == "P1")
    assert p1_report.is_met is True
    assert p1_report.financial_status == "AL_CORRIENTE"
    assert p1_report.pending_amount == 0.0

    p2_report = next(p for p in report.participants if p.participant_id == "P2")
    assert p2_report.is_met is False
    assert p2_report.financial_status == "PENDIENTE"
    assert p2_report.pending_amount == 150.0


def test_ac_6_4_rest_api_weekly_report() -> None:
    """Verifica el endpoint REST /api/reports/weekly/{week_number} y codigos 200 y 400."""
    from fastapi.testclient import TestClient
    from src.application.challenge_service import ChallengeService
    from src.application.dto import RegisterParticipantDTO, RecordPaymentDTO
    from src.presentation.api import create_app

    service = ChallengeService()
    service.register_participant(RegisterParticipantDTO(id="DIDT-01", name="Elena"))
    service.record_payment(RecordPaymentDTO(participant_id="DIDT-01", amount=200.0))

    client = TestClient(create_app(service))

    # Peticion valida semana 1
    res = client.get("/api/reports/weekly/1")
    assert res.status_code == 200
    data = res.json()
    assert data["week_number"] == 1
    assert data["total_participants"] == 1
    assert data["expected_contribution_per_participant"] == 200.0
    assert len(data["participants"]) == 1
    assert data["participants"][0]["participant_id"] == "DIDT-01"
    assert data["participants"][0]["financial_status"] == "AL_CORRIENTE"

    # Peticion invalida semana 0
    res_zero = client.get("/api/reports/weekly/0")
    assert res_zero.status_code == 400
    assert "El numero de semana debe estar entre 1 y 9" in res_zero.json()["detail"]

    # Peticion invalida semana 10
    res_ten = client.get("/api/reports/weekly/10")
    assert res_ten.status_code == 400


def test_ac_6_5_dashboard_interactive_section() -> None:
    """Verifica que el Dashboard Web incluye la seccion de informe semanal con selector y tabla."""
    from src.application.challenge_service import ChallengeService
    from src.application.dto import RegisterParticipantDTO, RecordPaymentDTO
    from src.presentation.web_views import render_dashboard_html

    service = ChallengeService()
    service.register_participant(RegisterParticipantDTO(id="P1", name="Mariana"))
    service.record_payment(RecordPaymentDTO(participant_id="P1", amount=200.0))

    html = render_dashboard_html(service)
    assert 'id="weekly-report-select"' in html
    assert 'aria-label="Informe Semanal de Cuotas y Cumplimiento"' in html
    assert 'Informe Semanal de Cuotas y Cumplimiento' in html
    assert 'Mariana' in html


def test_ac_6_6_accessible_empty_state() -> None:
    """Verifica que el estado vacio accesible con role status se muestra cuando no hay participantes."""
    from src.application.challenge_service import ChallengeService
    from src.presentation.web_views import render_dashboard_html

    service = ChallengeService()
    html = render_dashboard_html(service)
    assert 'role="status"' in html
    assert 'id="weekly-report-empty"' in html or 'Sin datos de informe semanal' in html or 'No hay participantes registrados' in html
