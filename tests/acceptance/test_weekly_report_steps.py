"""
Step definitions BDD para FEAT-006: Informe Semanal de Cuotas y Cumplimiento del Reto
Mapeo a Criterios EARS: @AC-6.1 a @AC-6.6
"""
import pytest
from pathlib import Path
from typing import Dict, Any
from fastapi.testclient import TestClient
from pytest_bdd import scenarios, given, when, then, parsers

from src.infrastructure.sqlite_repository import SQLiteChallengeRepository
from src.application.challenge_service import ChallengeService
from src.application.dto import RegisterParticipantDTO, RecordPaymentDTO, RecordActivityDTO
from src.presentation.api import create_app
from src.presentation.web_views import render_dashboard_html

scenarios("../../specs/006-informe-semanal-cuotas-cumplimiento/scenarios.feature")


@pytest.fixture
def bdd_db_path(tmp_path: Path) -> str:
    return str(tmp_path / "bdd_weekly_report.db")


@pytest.fixture
def ctx(bdd_db_path: str) -> Dict[str, Any]:
    repo = SQLiteChallengeRepository(db_path=bdd_db_path)
    service = ChallengeService(repository=repo)
    app = create_app(service)
    client = TestClient(app)
    return {
        "db_path": bdd_db_path,
        "repo": repo,
        "service": service,
        "client": client,
        "report": None,
        "last_response": None,
        "html_content": None,
        "error_caught": None,
    }


# @AC-6.1
@given("que existen participantes registrados en el reto")
def given_registered_participants(ctx: Dict[str, Any]) -> None:
    service = ctx["service"]
    if "P1" not in service.participants:
        service.register_participant(RegisterParticipantDTO(id="P1", name="Participante Uno"))
    if "P2" not in service.participants:
        service.register_participant(RegisterParticipantDTO(id="P2", name="Participante Dos"))


@given(parsers.parse('el participante "{participant_id}" registra {days:d} dias exitosos en la semana {week:d}'))
def given_participant_records_days(ctx: Dict[str, Any], participant_id: str, days: int, week: int) -> None:
    service = ctx["service"]
    for d in range(1, days + 1):
        service.record_daily_activity(
            RecordActivityDTO(
                participant_id=participant_id,
                week_number=week,
                day_of_week=d,
                calories=350,
                steps=5000,
            )
        )


@when(parsers.parse("se genera el informe de la semana {week:d}"))
def when_generate_report_for_week(ctx: Dict[str, Any], week: int) -> None:
    ctx["report"] = ctx["service"].get_weekly_report(week)


@then(parsers.parse('el participante "{participant_id}" se reporta con cumplimiento exitoso y penalizacion de {penalty:f} pesos'))
def then_participant_met_and_penalty(ctx: Dict[str, Any], participant_id: str, penalty: float) -> None:
    report = ctx["report"]
    part = next(p for p in report.participants if p.participant_id == participant_id)
    assert part.is_met is True
    assert part.penalty == penalty


@then(parsers.parse('el participante "{participant_id}" se reporta como no cumplido con penalizacion de {penalty:f} pesos'))
def then_participant_missed_and_penalty(ctx: Dict[str, Any], participant_id: str, penalty: float) -> None:
    report = ctx["report"]
    part = next(p for p in report.participants if p.participant_id == participant_id)
    assert part.is_met is False
    assert part.penalty == penalty


# @AC-6.2
@given(parsers.parse('que el participante "{participant_id}" tiene abonos acumulados por {amount:f} pesos'))
@given(parsers.parse('el participante "{participant_id}" tiene abonos acumulados por {amount:f} pesos'))
def given_participant_contributions(ctx: Dict[str, Any], participant_id: str, amount: float) -> None:
    service = ctx["service"]
    if participant_id not in service.participants:
        service.register_participant(RegisterParticipantDTO(id=participant_id, name=f"Nombre {participant_id}"))
    service.record_payment(RecordPaymentDTO(participant_id=participant_id, amount=amount))


@when(parsers.parse("se genera el informe de cuotas para la semana {week:d}"))
def when_generate_quota_report_for_week(ctx: Dict[str, Any], week: int) -> None:
    ctx["report"] = ctx["service"].get_weekly_report(week)


@then(parsers.parse("la cuota exigible acumulada para la semana {week:d} es de {expected_quota:f} pesos"))
def then_expected_quota_is(ctx: Dict[str, Any], week: int, expected_quota: float) -> None:
    report = ctx["report"]
    assert report.expected_contribution_per_participant == expected_quota


@then(parsers.parse('el participante "{participant_id}" tiene estatus de cuota "{status}" con saldo pendiente de {pending:f} pesos'))
def then_participant_financial_status(ctx: Dict[str, Any], participant_id: str, status: str, pending: float) -> None:
    report = ctx["report"]
    part = next(p for p in report.participants if p.participant_id == participant_id)
    assert part.financial_status == status
    assert part.pending_amount == pending


# @AC-6.3
@given("que el sistema tiene el rango de semanas entre 1 y 9")
def given_system_weeks_range(ctx: Dict[str, Any]) -> None:
    pass


@when("se solicita el informe de la semana 0 o de la semana 10")
def when_request_invalid_weeks(ctx: Dict[str, Any]) -> None:
    errors = []
    try:
        ctx["service"].get_weekly_report(0)
    except ValueError as e:
        errors.append(str(e))
    try:
        ctx["service"].get_weekly_report(10)
    except ValueError as e:
        errors.append(str(e))
    ctx["error_caught"] = errors


@then("el sistema responde con error de semana invalida")
def then_system_raises_invalid_week_error(ctx: Dict[str, Any]) -> None:
    assert len(ctx["error_caught"]) == 2
    for err in ctx["error_caught"]:
        assert "El numero de semana debe estar entre 1 y 9" in err


# @AC-6.4
@given("que la aplicacion API esta disponible con datos de participantes")
def given_api_with_data(ctx: Dict[str, Any]) -> None:
    service = ctx["service"]
    if not service.participants:
        service.register_participant(RegisterParticipantDTO(id="P1", name="Participante API"))
        service.record_payment(RecordPaymentDTO(participant_id="P1", amount=200.0))


@when('se realiza una peticion GET al endpoint "/api/reports/weekly/1"')
def when_get_api_weekly_report(ctx: Dict[str, Any]) -> None:
    client = ctx["client"]
    res = client.get("/api/reports/weekly/1")
    ctx["last_response"] = res


@then("la API responde con codigo 200 y el esquema contiene la tasa de cumplimiento y el detalle de cuotas")
def then_api_response_is_valid(ctx: Dict[str, Any]) -> None:
    res = ctx["last_response"]
    assert res.status_code == 200
    data = res.json()
    assert "compliance_rate" in data
    assert "expected_contribution_per_participant" in data
    assert data["expected_contribution_per_participant"] == 200.0
    assert len(data["participants"]) >= 1


# @AC-6.5 @UI-UX
@given("que el usuario accede al Dashboard Web")
def given_user_accesses_dashboard(ctx: Dict[str, Any]) -> None:
    if not ctx["service"].participants:
        ctx["service"].register_participant(RegisterParticipantDTO(id="P1", name="Mariana UI"))
        ctx["service"].record_payment(RecordPaymentDTO(participant_id="P1", amount=200.0))
    ctx["html_content"] = render_dashboard_html(ctx["service"])


@when("visualiza la tarjeta de informe semanal")
def when_user_views_weekly_report_card(ctx: Dict[str, Any]) -> None:
    assert "weekly-report-card" in ctx["html_content"]


@then("se presenta un selector de semana del 1 al 9 y una tabla accesible con indicadores de cumplimiento y aportacion")
def then_weekly_selector_and_table_accessible(ctx: Dict[str, Any]) -> None:
    html = ctx["html_content"]
    assert 'id="weekly-report-select"' in html
    assert 'aria-label="Informe Semanal de Cuotas y Cumplimiento"' in html
    assert "Tasa de Cumplimiento Físico" in html
    assert "Cuota Exigible Acumulada" in html
    assert "Bolsa Semanal (Penalizaciones)" in html


# @AC-6.6 @UI-UX
@given("que no existen participantes registrados en el sistema")
def given_no_participants_in_system(bdd_db_path: str, ctx: Dict[str, Any]) -> None:
    # Service nuevo sin participantes
    empty_repo = SQLiteChallengeRepository(db_path=bdd_db_path + "_empty")
    ctx["service"] = ChallengeService(repository=empty_repo)


@when("se consulta la vista del informe semanal en el Dashboard Web")
def when_view_weekly_report_empty(ctx: Dict[str, Any]) -> None:
    ctx["html_content"] = render_dashboard_html(ctx["service"])


@then('se visualiza el estado vacio accesible con rol "status" indicando ausencia de datos')
def then_accessible_empty_state_shown(ctx: Dict[str, Any]) -> None:
    html = ctx["html_content"]
    assert 'role="status"' in html
    assert 'id="weekly-report-empty"' in html
    assert "Sin datos de informe semanal" in html
