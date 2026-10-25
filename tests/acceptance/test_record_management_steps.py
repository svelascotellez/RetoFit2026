"""
Step definitions BDD para FEAT-004: Edicion y Gestion de Registros de Reto Fit
Mapeo a Criterios EARS: @AC-4.1 a @AC-4.6
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

scenarios("../../specs/004-edicion-gestion-registros/scenarios.feature")


@pytest.fixture
def bdd_db_path(tmp_path: Path) -> str:
    return str(tmp_path / "bdd_records_mgmt.db")


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
        "last_response": None,
        "last_status_code": None,
        "error_caught": None,
    }


# @AC-4.1
@given(parsers.parse('que existe un participante con id "{participant_id}" y nombre "{name}"'))
def given_participant_exists(ctx: Dict[str, Any], participant_id: str, name: str) -> None:
    ctx["service"].register_participant(RegisterParticipantDTO(id=participant_id, name=name))


@when(parsers.parse('se solicita actualizar el nombre a "{new_name}"'))
def when_update_participant_name(ctx: Dict[str, Any], new_name: str) -> None:
    resp = ctx["client"].put("/api/participants/DEV-01", json={"name": new_name})
    ctx["last_response"] = resp
    ctx["last_status_code"] = resp.status_code


@then(parsers.parse('el participante refleja el nuevo nombre "{expected_name}" en el sistema y en SQLite'))
def then_participant_name_updated(ctx: Dict[str, Any], expected_name: str) -> None:
    assert ctx["last_status_code"] == 200
    p = ctx["service"].participants["DEV-01"]
    assert p.name == expected_name
    p_db = ctx["repo"].get_participant("DEV-01")
    assert p_db is not None
    assert p_db.name == expected_name


# @AC-4.2
@given(parsers.parse('que existe un participante con id "{participant_id}" y nombre "{name}"'))
def given_participant_for_invalid(ctx: Dict[str, Any], participant_id: str, name: str) -> None:
    ctx["service"].register_participant(RegisterParticipantDTO(id=participant_id, name=name))


@when(parsers.re(r'se solicita actualizar el nombre con el valor "(?P<nombre_invalido>.*)"'))
def when_update_name_with_invalid(ctx: Dict[str, Any], nombre_invalido: str) -> None:
    # Interpretar secuencias de escape si vienen del feature file
    cleaned = nombre_invalido.replace("\\t", "\t")
    resp = ctx["client"].put("/api/participants/DEV-02", json={"name": cleaned})
    ctx["last_response"] = resp
    ctx["last_status_code"] = resp.status_code


@then(parsers.parse('el sistema rechaza la solicitud con codigo {code:d} y mantiene el nombre "{original_name}"'))
def then_rejects_and_maintains_name(ctx: Dict[str, Any], code: int, original_name: str) -> None:
    assert ctx["last_status_code"] == code
    p = ctx["service"].participants["DEV-02"]
    assert p.name == original_name
    p_db = ctx["repo"].get_participant("DEV-02")
    assert p_db is not None
    assert p_db.name == original_name


# @AC-4.3
@given(parsers.parse('que existe un participante con id "{participant_id}" con abonos y actividades registradas'))
def given_participant_with_payments_and_activities(ctx: Dict[str, Any], participant_id: str) -> None:
    ctx["service"].register_participant(RegisterParticipantDTO(id=participant_id, name="Laura"))
    ctx["service"].record_payment(RecordPaymentDTO(participant_id=participant_id, amount=200.0))
    ctx["service"].record_daily_activity(
        RecordActivityDTO(participant_id=participant_id, week_number=1, day_of_week=1, calories=350, steps=10500)
    )


@when(parsers.parse('se solicita eliminar al participante con id "{participant_id}"'))
def when_delete_participant(ctx: Dict[str, Any], participant_id: str) -> None:
    resp = ctx["client"].delete(f"/api/participants/{participant_id}")
    ctx["last_status_code"] = resp.status_code


@then(parsers.parse('el participante y todos sus pagos y actividades son eliminados de SQLite y del resumen general'))
def then_participant_cascaded(ctx: Dict[str, Any]) -> None:
    assert ctx["last_status_code"] == 200
    assert "DEV-03" not in ctx["service"].participants
    assert ctx["repo"].get_participant("DEV-03") is None
    summary = ctx["service"].get_general_summary()
    ids = [p.participant_id for p in summary.participants]
    assert "DEV-03" not in ids



# @AC-4.4
@given(parsers.parse('que el participante "{participant_id}" tiene un abono registrado de {amount:f} pesos'))
def given_participant_with_single_payment(ctx: Dict[str, Any], participant_id: str, amount: float) -> None:
    ctx["service"].register_participant(RegisterParticipantDTO(id=participant_id, name="Pedro"))
    ctx["service"].record_payment(RecordPaymentDTO(participant_id=participant_id, amount=amount))


@when(parsers.parse('se solicita eliminar el abono de {amount:f} pesos del participante "{participant_id}"'))
def when_delete_payment(ctx: Dict[str, Any], amount: float, participant_id: str) -> None:
    resp = ctx["client"].delete(f"/api/participants/{participant_id}/payments/last")
    ctx["last_status_code"] = resp.status_code


@then(parsers.parse('el total aportado del participante disminuye a {expected_total:f} pesos y el pago no existe en SQLite'))
def then_payment_deleted_and_decremented(ctx: Dict[str, Any], expected_total: float) -> None:
    assert ctx["last_status_code"] == 200
    p = ctx["service"].participants["DEV-04"]
    assert p.total_contributed == expected_total
    p_db = ctx["repo"].get_participant("DEV-04")
    assert p_db is not None
    assert p_db.total_contributed == expected_total


# @AC-4.5
@given(parsers.parse('que el participante "{participant_id}" tiene una actividad de {cal:d} kcal y {steps:d} pasos en la semana {week:d} dia {day:d}'))
def given_participant_with_activity(ctx: Dict[str, Any], participant_id: str, cal: int, steps: int, week: int, day: int) -> None:
    ctx["service"].register_participant(RegisterParticipantDTO(id=participant_id, name="Sofia"))
    ctx["service"].record_daily_activity(
        RecordActivityDTO(participant_id=participant_id, week_number=week, day_of_week=day, calories=cal, steps=steps)
    )
    assert ctx["service"].participants[participant_id].get_successful_days(week) == 1


@when(parsers.parse('se solicita eliminar la actividad del participante "{participant_id}" para la semana {week:d} dia {day:d}'))
def when_delete_activity(ctx: Dict[str, Any], participant_id: str, week: int, day: int) -> None:
    resp = ctx["client"].delete(f"/api/activities/{participant_id}/weeks/{week}/days/{day}")
    ctx["last_status_code"] = resp.status_code


@then(parsers.parse('el dia {day:d} de la semana {week:d} queda sin registro de actividad y no suma como dia exitoso'))
def then_activity_cleared(ctx: Dict[str, Any], day: int, week: int) -> None:
    assert ctx["last_status_code"] == 200
    p = ctx["service"].participants["DEV-05"]
    assert p.get_successful_days(week) == 0
    assert day not in p.activities.get(week, {})


# @AC-4.6 @UI-UX
@given("que el usuario accede al Dashboard Web del Reto Fit")
def given_user_on_dashboard(ctx: Dict[str, Any]) -> None:
    resp = ctx["client"].get("/")
    assert resp.status_code == 200
    ctx["dashboard_html"] = resp.text


@when("abre el dialogo de confirmacion para eliminar un registro")
def when_opens_confirmation_dialog(ctx: Dict[str, Any]) -> None:
    # Verificamos que el HTML incluya la estructura accesible del modal de confirmación
    assert 'role="dialog"' in ctx["dashboard_html"] or 'id="confirmModal"' in ctx["dashboard_html"]


@then(parsers.parse('el dialogo expone el rol accesible "{expected_role}" con opciones de cancelar y confirmar la accion destructiva'))
def then_accessible_dialog_verified(ctx: Dict[str, Any], expected_role: str) -> None:
    html = ctx["dashboard_html"]
    assert f'role="{expected_role}"' in html
    assert 'aria-modal="true"' in html
    assert "Cancelar" in html or "cancel" in html.lower()
    assert "Confirmar" in html or "confirm" in html.lower()
