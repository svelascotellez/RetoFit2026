"""
Pruebas unitarias para DailyActivity (AC-1.1, AC-1.8)
"""
import pytest
from src.domain.activity import DailyActivity


def test_ac_1_1_daily_activity_success_with_calories():
    # AC-1.1: 300 o mas calorias es exitoso independientemente de los pasos
    activity = DailyActivity(calories=300, steps=2000)
    assert activity.is_successful() is True


def test_ac_1_1_daily_activity_success_with_steps():
    # AC-1.1: 10,000 o mas pasos es exitoso independientemente de las calorias
    activity = DailyActivity(calories=100, steps=10000)
    assert activity.is_successful() is True


def test_ac_1_1_daily_activity_failure_below_thresholds():
    # AC-1.1: Menos de 300 calorias y menos de 10,000 pasos no es exitoso
    activity = DailyActivity(calories=299, steps=9999)
    assert activity.is_successful() is False


def test_ac_1_8_negative_calories_raises_error():
    # AC-1.8: Calorias no pueden ser negativas
    with pytest.raises(ValueError, match="Calorias no pueden ser negativas"):
        DailyActivity(calories=-10, steps=5000)


def test_ac_1_8_negative_steps_raises_error():
    # AC-1.8: Pasos no pueden ser negativos
    with pytest.raises(ValueError, match="Pasos no pueden ser negativos"):
        DailyActivity(calories=200, steps=-500)
