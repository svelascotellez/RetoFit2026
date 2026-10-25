"""
Pruebas unitarias para Participant (AC-1.6, AC-1.8)
"""
import pytest
from src.domain.participant import Participant
from src.domain.activity import DailyActivity


def test_ac_1_6_participant_contributions():
    # AC-1.6 / AC-5.1: Registro de aportaciones acumulativas hasta 900 pesos (ajustado en FEAT-005)
    p = Participant(id="p1", name="Jorge")
    assert p.total_contributed == 0.0
    assert p.TARGET_CONTRIBUTION == 900.0

    p.add_contribution(200.0)
    assert p.total_contributed == 200.0
    assert len(p.contributions) == 1

    p.add_contribution(200.0)
    assert p.total_contributed == 400.0
    assert len(p.contributions) == 2


def test_ac_1_8_participant_negative_or_zero_contribution():
    # AC-1.8: Monto debe ser mayor a cero
    p = Participant(id="p1", name="Jorge")
    with pytest.raises(ValueError, match="Monto debe ser mayor a cero"):
        p.add_contribution(-50.0)

    with pytest.raises(ValueError, match="Monto debe ser mayor a cero"):
        p.add_contribution(0.0)


def test_participant_activity_registration():
    p = Participant(id="p1", name="Jorge")
    activity = DailyActivity(calories=320, steps=8000)
    p.record_activity(week_number=1, day_of_week=1, activity=activity)

    assert p.get_successful_days(week_number=1) == 1
