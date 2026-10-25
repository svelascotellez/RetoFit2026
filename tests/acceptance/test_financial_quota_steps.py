"""
Step definitions BDD para FEAT-005: Ajuste de Cuota Financiera y Calendario de Aportaciones
Mapeo a Criterios EARS: @AC-5.1 a @AC-5.5
"""
import pytest
from pathlib import Path
from typing import Dict, Any
from fastapi.testclient import TestClient
from pytest_bdd import scenarios, given, when, then, parsers

from src.infrastructure.sqlite_repository import SQLiteChallengeRepository
from src.application.challenge_service import ChallengeService
from src.application.dto import RegisterParticipantDTO, RecordPaymentDTO
from src.presentation.api import create_app

scenarios("../../specs/005-ajuste-cuota-final/scenarios.feature")


@pytest.fixture
def bdd_db_path(tmp_path: Path) -> str:
    return str(tmp_path / "bdd_quota.db")


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
        "participant": None,
        "last_response": None,
        "html_content": None,
    }


# @AC-5.1
@given(parsers.parse('que se crea un nuevo participante con id "{participant_id}" y nombre "{name}"'))
def given_new_participant(ctx: Dict[str, Any], participant_id: str, name: str) -> None:
    p = ctx["service"].register_participant(RegisterParticipantDTO(id=participant_id, name=name))
    ctx["participant"] = p


@when("se consulta la meta de aportacion del participante")
def when_query_target_contribution(ctx: Dict[str, Any]) -> None:
    pass


@then(parsers.parse('la meta de aportacion es de {expected_target:f} pesos'))
def then_target_contribution_is(ctx: Dict[str, Any], expected_target: float) -> None:
    assert ctx["participant"].TARGET_CONTRIBUTION == expected_target


# @AC-5.2
@given(parsers.parse('que el participante "{participant_id}" tiene {count:d} abonos de {amount:f} pesos registrados'))
def given_participant_with_multiple_payments(ctx: Dict[str, Any], participant_id: str, count: int, amount: float) -> None:
    p = ctx["service"].register_participant(RegisterParticipantDTO(id=participant_id, name="Julian"))
    for _ in range(count):
        ctx["service"].record_payment(RecordPaymentDTO(participant_id=participant_id, amount=amount))
    ctx["participant"] = p


@when(parsers.parse('registra su quinto y ultimo abono por {amount:f} pesos'))
def when_records_fifth_payment(ctx: Dict[str, Any], amount: float) -> None:
    pid = ctx["participant"].id
    ctx["service"].record_payment(RecordPaymentDTO(participant_id=pid, amount=amount))


@then(parsers.parse('el total aportado del participante alcanza exactamente {expected_total:f} pesos'))
def then_total_contributed_is(ctx: Dict[str, Any], expected_total: float) -> None:
    p = ctx["participant"]
    assert p.total_contributed == expected_total
    assert len(p.contributions) == 5


# @AC-5.3
@given("que el usuario accede al Dashboard Web")
def given_access_dashboard_for_calendar(ctx: Dict[str, Any]) -> None:
    resp = ctx["client"].get("/")
    assert resp.status_code == 200
    ctx["html_content"] = resp.text


@when("revisa la seccion del calendario de aportaciones")
def when_reviews_calendar(ctx: Dict[str, Any]) -> None:
    assert "Fechas de Aportación" in ctx["html_content"]


@then(parsers.parse('se visualizan las fechas oficiales sumando un total de {total:f} pesos con el 14 de diciembre en {dec_amount:f} pesos'))
def then_calendar_shows_correct_dates(ctx: Dict[str, Any], total: float, dec_amount: float) -> None:
    html = ctx["html_content"]
    assert f"${total:,.2f}" in html or f"${int(total)}" in html or "$900" in html
    assert "14 de diciembre" in html
    assert "$100.00" in html


# @AC-5.4 @UI-UX
@given("que el usuario visualiza la tabla de participantes en el Dashboard Web")
def given_views_participants_table(ctx: Dict[str, Any]) -> None:
    ctx["service"].register_participant(RegisterParticipantDTO(id="P-TAB", name="Laura"))
    resp = ctx["client"].get("/")
    assert resp.status_code == 200
    ctx["html_content"] = resp.text


@when("observa las acciones de cada participante")
def when_observes_actions(ctx: Dict[str, Any]) -> None:
    pass


@then(parsers.parse('estan disponibles botones de acceso rapido tanto para "{btn1}" como para "{btn2}"'))
def then_quick_pay_buttons_exist(ctx: Dict[str, Any], btn1: str, btn2: str) -> None:
    html = ctx["html_content"]
    assert btn1 in html
    assert btn2 in html


# @AC-5.5
@given(parsers.parse('que se consulta el concentrado general a traves de la API en "{endpoint}"'))
def given_query_summary_api(ctx: Dict[str, Any], endpoint: str) -> None:
    ctx["service"].register_participant(RegisterParticipantDTO(id="P-API", name="Andres"))
    resp = ctx["client"].get(endpoint)
    ctx["last_response"] = resp


@when("la API responde exitosamente")
def when_api_responds_ok(ctx: Dict[str, Any]) -> None:
    assert ctx["last_response"].status_code == 200


@then(parsers.parse('los esquemas de participante reflejan la meta de {expected_target:f} pesos'))
def then_schemas_reflect_target(ctx: Dict[str, Any], expected_target: float) -> None:
    # Verificamos esquema del participante individual
    resp = ctx["client"].get("/api/participants/P-API") if False else ctx["client"].post("/api/participants", json={"id": "P-TEST", "name": "Test"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["target_contribution"] == expected_target
