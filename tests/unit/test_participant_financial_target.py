"""
Pruebas unitarias de dominio para la cuota financiera ajustada de $900 MXN (AC-5.1, AC-5.2)
"""
import pytest
from src.domain.participant import Participant


def test_ac_5_1_target_contribution_default_900():
    # AC-5.1: Cuota objetivo fijada en 900.0 MXN por participante
    p = Participant(id="p_test", name="Mariana")
    assert p.TARGET_CONTRIBUTION == 900.0
    assert p.MAX_CONTRIBUTIONS == 5
    assert p.total_contributed == 0.0


def test_ac_5_2_accumulate_four_200_and_one_100_reaches_900():
    # AC-5.2: 4 abonos de 200 y 1 abono de 100 completan exactamente los 900
    p = Participant(id="p_test2", name="Carlos")
    # Quincenas 1 a 4
    for _ in range(4):
        p.add_contribution(200.0)
    assert p.total_contributed == 800.0
    assert len(p.contributions) == 4

    # Semana final 9
    p.add_contribution(100.0)
    assert p.total_contributed == 900.0
    assert len(p.contributions) == 5

    # Intentar un 6to pago debe fallar por MAX_CONTRIBUTIONS
    with pytest.raises(ValueError, match="maximo de 5 aportaciones"):
        p.add_contribution(100.0)
