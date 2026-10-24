"""
Pruebas Unitarias para SQLiteChallengeRepository
Criterios EARS: AC-3.1 a AC-3.6
"""
import pytest
from pathlib import Path
from src.infrastructure.sqlite_repository import SQLiteChallengeRepository
from src.domain.participant import Participant
from src.domain.activity import DailyActivity


@pytest.fixture
def temp_repo(tmp_path: Path) -> SQLiteChallengeRepository:
    db_file = tmp_path / "test_retofit.db"
    return SQLiteChallengeRepository(db_path=str(db_file))


def test_schema_creation_and_auto_init(temp_repo: SQLiteChallengeRepository) -> None:
    """AC-3.6: Verifica que el archivo de base de datos y sus tablas se inicialicen automaticamente."""
    assert Path(temp_repo.db_path).exists()
    assert temp_repo.get_rollover() == 0.0


def test_save_and_get_participant(temp_repo: SQLiteChallengeRepository) -> None:
    """AC-3.1: Persiste un participante y lo recupera por su ID."""
    p = Participant(id="p10", name="Sofia Morales")
    temp_repo.save_participant(p)

    retrieved = temp_repo.get_participant("p10")
    assert retrieved is not None
    assert retrieved.id == "p10"
    assert retrieved.name == "Sofia Morales"
    assert retrieved.total_contributed == 0.0


def test_record_payment_persistence(temp_repo: SQLiteChallengeRepository) -> None:
    """AC-3.2: Persiste pagos quincenales y acumula el saldo en SQLite."""
    p = Participant(id="p20", name="Roberto Gomez")
    temp_repo.save_participant(p)

    temp_repo.record_payment("p20", 200.0)
    temp_repo.record_payment("p20", 200.0)

    retrieved = temp_repo.get_participant("p20")
    assert retrieved is not None
    assert retrieved.total_contributed == 400.0


def test_record_activity_persistence(temp_repo: SQLiteChallengeRepository) -> None:
    """AC-3.3: Persiste actividades diarias de ejercicio en SQLite."""
    p = Participant(id="p30", name="Carmen Diaz")
    temp_repo.save_participant(p)

    act = DailyActivity(calories=320, steps=4000)
    temp_repo.record_activity("p30", week_number=1, day_of_week=1, activity=act)

    state = temp_repo.load_all_state()
    assert "p30" in state["activities"]
    assert len(state["activities"]["p30"]) == 1
    assert state["activities"]["p30"][0]["calories"] == 320


def test_record_week_close_persistence(temp_repo: SQLiteChallengeRepository) -> None:
    """AC-3.4: Persiste el cierre de semana y actualiza el rollover."""
    temp_repo.record_week_close(
        week_number=1,
        compliant_ids=["p1"],
        non_compliant_ids=["p2"],
        pool_collected=100.0,
        rollover_amount=0.0,
        payout_per_compliant=100.0,
    )

    state = temp_repo.load_all_state()
    assert len(state["weekly_closes"]) == 1
    assert state["weekly_closes"][0]["week_number"] == 1
    assert state["weekly_closes"][0]["pool_collected"] == 100.0


def test_rehydration_state_structure(temp_repo: SQLiteChallengeRepository) -> None:
    """AC-3.5: Carga todo el estado para rehidratacion completa."""
    p = Participant(id="p40", name="Daniela")
    temp_repo.save_participant(p)
    temp_repo.record_payment("p40", 200.0)
    temp_repo.set_rollover(50.0)

    state = temp_repo.load_all_state()
    assert len(state["participants"]) == 1
    assert state["participants"][0].id == "p40"
    assert state["participants"][0].total_contributed == 200.0
    assert state["rollover"] == 50.0
