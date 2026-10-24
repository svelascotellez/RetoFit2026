"""
Step definitions BDD para FEAT-003: Persistencia en SQLite para Reto Fit
Mapeo a Criterios EARS: @AC-3.1 a @AC-3.6
"""
import pytest
from pathlib import Path
from typing import Dict, Any
from pytest_bdd import scenarios, given, when, then, parsers
from src.infrastructure.sqlite_repository import SQLiteChallengeRepository
from src.application.challenge_service import ChallengeService
from src.application.dto import RegisterParticipantDTO, RecordPaymentDTO, RecordActivityDTO

scenarios("../../specs/003-persistencia-sqlite/scenarios.feature")


@pytest.fixture
def test_db_path(tmp_path: Path) -> str:
    return str(tmp_path / "bdd_retofit.db")


@pytest.fixture
def ctx(test_db_path: str) -> Dict[str, Any]:
    repo = SQLiteChallengeRepository(db_path=test_db_path)
    svc = ChallengeService(repository=repo)
    return {
        "db_path": test_db_path,
        "repo": repo,
        "service": svc,
    }


# @AC-3.1
@given("una base de datos SQLite inicializada y limpia")
def given_clean_sqlite(ctx: Dict[str, Any]) -> None:
    assert Path(ctx["db_path"]).exists()


@when(parsers.parse('se registra un participante con ID "{participant_id}" y nombre "{name}"'))
def when_register_participant(ctx: Dict[str, Any], participant_id: str, name: str) -> None:
    ctx["service"].register_participant(RegisterParticipantDTO(id=participant_id, name=name))


@then(parsers.parse('el participante "{participant_id}" debe existir en la base de datos con nombre "{name}"'))
def then_participant_exists_in_sqlite(ctx: Dict[str, Any], participant_id: str, name: str) -> None:
    p = ctx["repo"].get_participant(participant_id)
    assert p is not None
    assert p.id == participant_id
    assert p.name == name


# @AC-3.2
@given(parsers.parse('un participante "{participant_id}" registrado en SQLite'))
def given_participant_registered(ctx: Dict[str, Any], participant_id: str) -> None:
    ctx["service"].register_participant(RegisterParticipantDTO(id=participant_id, name="Test User"))


@when(parsers.parse('se registra un abono de {amount:f} pesos para "{participant_id}"'))
def when_record_payment(ctx: Dict[str, Any], amount: float, participant_id: str) -> None:
    ctx["service"].record_payment(RecordPaymentDTO(participant_id=participant_id, amount=amount))


@then(parsers.parse('el total aportado en SQLite para "{participant_id}" debe ser {amount:f} pesos'))
def then_total_contributed_in_sqlite(ctx: Dict[str, Any], participant_id: str, amount: float) -> None:
    p = ctx["repo"].get_participant(participant_id)
    assert p is not None
    assert p.total_contributed == amount


# @AC-3.3
@when(parsers.parse('se registra una actividad fisica en la semana {week:d} dia {day:d} con {cals:d} calorias y {steps:d} pasos para "{participant_id}"'))
def when_record_activity(ctx: Dict[str, Any], week: int, day: int, cals: int, steps: int, participant_id: str) -> None:
    ctx["service"].record_daily_activity(
        RecordActivityDTO(
            participant_id=participant_id,
            week_number=week,
            day_of_week=day,
            calories=cals,
            steps=steps,
        )
    )


@then("la actividad fisica debe quedar registrada en SQLite indicando dia exitoso")
def then_activity_successful_in_sqlite(ctx: Dict[str, Any]) -> None:
    state = ctx["repo"].load_all_state()
    activities = state["activities"]
    assert len(activities) > 0


# @AC-3.4
@given("un participante cumplidor y un participante incumplidor en SQLite para la semana 1")
def given_compliant_and_non_compliant(ctx: Dict[str, Any]) -> None:
    ctx["service"].register_participant(RegisterParticipantDTO(id="p1", name="Cumplidor"))
    ctx["service"].register_participant(RegisterParticipantDTO(id="p2", name="Incumplidor"))
    # 4 dias exitosos para p1
    for day in range(1, 5):
        ctx["service"].record_daily_activity(
            RecordActivityDTO(participant_id="p1", week_number=1, day_of_week=day, calories=350, steps=5000)
        )


@when("se ejecuta el cierre de la semana 1 en SQLite")
def when_close_week(ctx: Dict[str, Any]) -> None:
    ctx["service"].close_and_liquidate_week(1)


@then("el registro del cierre semanal 1 debe persistir con bolsa de 100.0 pesos")
def then_close_persists_in_sqlite(ctx: Dict[str, Any]) -> None:
    state = ctx["repo"].load_all_state()
    assert len(state["weekly_closes"]) == 1
    assert state["weekly_closes"][0]["pool_collected"] == 100.0


# @AC-3.5
@given("una base de datos SQLite con participantes, pagos y actividades previas")
def given_db_with_data(ctx: Dict[str, Any]) -> None:
    ctx["service"].register_participant(RegisterParticipantDTO(id="hero", name="Heroico"))
    ctx["service"].record_payment(RecordPaymentDTO(participant_id="hero", amount=200.0))
    ctx["service"].record_daily_activity(
        RecordActivityDTO(participant_id="hero", week_number=1, day_of_week=1, calories=400, steps=10000)
    )


@when("se inicializa una nueva instancia de ChallengeService conectada a la misma base de datos")
def when_reinit_service(ctx: Dict[str, Any]) -> None:
    new_repo = SQLiteChallengeRepository(db_path=ctx["db_path"])
    ctx["new_service"] = ChallengeService(repository=new_repo)


@then("el nuevo servicio debe restaurar todos los participantes con sus saldos y estados intactos")
def then_rehydrated_state_intact(ctx: Dict[str, Any]) -> None:
    summary = ctx["new_service"].get_participant_summary("hero")
    assert summary.participant_id == "hero"
    assert summary.name == "Heroico"
    assert summary.total_contributed == 200.0


# @AC-3.6
@given("que el archivo de base de datos no existe previamente en disco")
def given_file_does_not_exist(tmp_path: Path, ctx: Dict[str, Any]) -> None:
    ctx["fresh_db_path"] = str(tmp_path / "subfolder" / "fresh.db")
    assert not Path(ctx["fresh_db_path"]).exists()


@when("se inicializa el repositorio SQLite")
def when_init_fresh_repo(ctx: Dict[str, Any]) -> None:
    ctx["fresh_repo"] = SQLiteChallengeRepository(db_path=ctx["fresh_db_path"])


@then("el archivo de base de datos y todas sus tablas deben ser creados exitosamente")
def then_database_file_and_tables_created(ctx: Dict[str, Any]) -> None:
    assert Path(ctx["fresh_db_path"]).exists()
    assert ctx["fresh_repo"].get_rollover() == 0.0
