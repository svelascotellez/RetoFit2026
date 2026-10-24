"""
Pruebas unitarias para WeeklyPool (AC-1.3, AC-1.4, AC-1.5)
"""
import pytest
from src.domain.challenge_pool import WeeklyPool


def test_ac_1_3_weekly_penalty_application():
    # AC-1.3: Penalizacion de $100 se suma a la bolsa
    pool = WeeklyPool(week_number=1)
    pool.add_penalty(100.0)
    assert pool.total_penalties == 100.0
    assert pool.current_total == 100.0


def test_ac_1_4_weekly_pool_distribution_equitable():
    # AC-1.4: Reparto equitativo entre cumplidores
    pool = WeeklyPool(week_number=1)
    pool.add_penalty(100.0)
    pool.add_penalty(100.0)
    pool.add_penalty(100.0)  # Total 300
    gain, rollover = pool.distribute(met_participants_count=2)
    assert gain == 150.0
    assert rollover == 0.0
    assert pool.is_closed is True


def test_ac_1_4_weekly_pool_distribution_rounding():
    # AC-1.4: Redondeo a 2 decimales en division no exacta
    pool = WeeklyPool(week_number=1)
    pool.add_penalty(100.0)  # $100 entre 3 personas = 33.33
    gain, rollover = pool.distribute(met_participants_count=3)
    assert gain == 33.33
    assert rollover == 0.0


def test_ac_1_5_rollover_empty_pool_when_nobody_meets_goal():
    # AC-1.5: Si nadie cumple (0 cumplidores), la bolsa se traslada a la siguiente semana
    pool = WeeklyPool(week_number=2)
    pool.add_penalty(100.0)
    pool.add_penalty(100.0)
    pool.add_penalty(100.0)
    pool.add_penalty(100.0)  # Total 400
    gain, rollover = pool.distribute(met_participants_count=0)
    assert gain == 0.0
    assert rollover == 400.0
    assert pool.is_closed is True

    # La semana siguiente inicia con el rollover
    next_pool = WeeklyPool(week_number=3, initial_rollover=rollover)
    assert next_pool.current_total == 400.0


def test_weekly_pool_invalid_negative_penalty():
    pool = WeeklyPool(week_number=1)
    with pytest.raises(ValueError, match="El monto de penalizacion debe ser positivo"):
        pool.add_penalty(-50.0)
