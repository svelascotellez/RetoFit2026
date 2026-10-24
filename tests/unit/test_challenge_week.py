"""
Pruebas unitarias para ChallengeWeek (AC-1.2)
"""
import pytest
from src.domain.challenge_week import ChallengeWeek


def test_ac_1_2_weekly_compliance_evaluation_met():
    # AC-1.2: 4 o mas dias exitosos cumple la meta semanal
    week = ChallengeWeek(week_number=1)
    assert week.evaluate_participant(successful_days=4) is True
    assert week.evaluate_participant(successful_days=5) is True
    assert week.evaluate_participant(successful_days=7) is True


def test_ac_1_2_weekly_compliance_evaluation_missed():
    # AC-1.2: Menos de 4 dias exitosos no cumple la meta semanal
    week = ChallengeWeek(week_number=1)
    assert week.evaluate_participant(successful_days=3) is False
    assert week.evaluate_participant(successful_days=0) is False


def test_ac_1_2_invalid_successful_days():
    # Validacion de rango de dias (0 a 7)
    week = ChallengeWeek(week_number=1)
    with pytest.raises(ValueError, match="Dias exitosos deben estar entre 0 y 7"):
        week.evaluate_participant(successful_days=-1)
    with pytest.raises(ValueError, match="Dias exitosos deben estar entre 0 y 7"):
        week.evaluate_participant(successful_days=8)
