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


def test_update_participant_name_persistence(temp_repo: SQLiteChallengeRepository) -> None:
    """AC-4.1: Actualiza el nombre en SQLite."""
    p = Participant(id="p50", name="Original")
    temp_repo.save_participant(p)

    temp_repo.update_participant_name("p50", "Actualizado")
    retrieved = temp_repo.get_participant("p50")
    assert retrieved is not None
    assert retrieved.name == "Actualizado"


def test_delete_participant_cascade_persistence(temp_repo: SQLiteChallengeRepository) -> None:
    """AC-4.3: Elimina participante y sus pagos/actividades en cascada."""
    p = Participant(id="p60", name="Para Borrar")
    temp_repo.save_participant(p)
    temp_repo.record_payment("p60", 200.0)
    temp_repo.record_activity("p60", 1, 1, DailyActivity(calories=350, steps=10000))

    deleted = temp_repo.delete_participant("p60")
    assert deleted is True
    assert temp_repo.get_participant("p60") is None

    # Verificar que en SQLite no queden pagos ni actividades de p60
    with temp_repo._get_connection() as conn:
        pay_count = conn.execute("SELECT count(*) as c FROM payments WHERE participant_id = 'p60';").fetchone()["c"]
        act_count = conn.execute("SELECT count(*) as c FROM activities WHERE participant_id = 'p60';").fetchone()["c"]
        assert pay_count == 0
        assert act_count == 0


def test_delete_last_payment_persistence(temp_repo: SQLiteChallengeRepository) -> None:
    """AC-4.4: Elimina el ultimo abono quincenal."""
    p = Participant(id="p70", name="Pagos Test")
    temp_repo.save_participant(p)
    temp_repo.record_payment("p70", 200.0)
    temp_repo.record_payment("p70", 200.0)

    removed = temp_repo.delete_last_payment("p70")
    assert removed == 200.0

    retrieved = temp_repo.get_participant("p70")
    assert retrieved is not None
    assert retrieved.total_contributed == 200.0


def test_delete_activity_persistence(temp_repo: SQLiteChallengeRepository) -> None:
    """AC-4.5: Elimina el registro de actividad de un dia especifico."""
    p = Participant(id="p80", name="Actividad Test")
    temp_repo.save_participant(p)
    temp_repo.record_activity("p80", 1, 2, DailyActivity(calories=400, steps=12000))

    deleted = temp_repo.delete_activity("p80", 1, 2)
    assert deleted is True

    state = temp_repo.load_all_state()
    assert "p80" not in state["activities"] or len(state["activities"]["p80"]) == 0

