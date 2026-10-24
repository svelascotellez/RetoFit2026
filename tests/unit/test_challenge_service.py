"""
Pruebas unitarias para ChallengeService (AC-1.7, orquestacion completa)
"""
import pytest
from src.application.challenge_service import ChallengeService
from src.application.dto import RegisterParticipantDTO, RecordPaymentDTO, RecordActivityDTO


def test_ac_1_7_financial_summary_calculation():
    # AC-1.7: Calculo de concentrado individual y general
    service = ChallengeService()
    service.register_participant(RegisterParticipantDTO(id="p1", name="Maria"))

    # Aporta $1,000
    service.record_payment(RecordPaymentDTO(participant_id="p1", amount=1000.0))

    # Semana 1: Cumple (4 dias exitosos de 300 cal)
    for day in range(1, 5):
        service.record_daily_activity(
            RecordActivityDTO(participant_id="p1", week_number=1, day_of_week=day, calories=350, steps=2000)
        )
    # Registramos un segundo participante que no cumple en semana 1
    service.register_participant(RegisterParticipantDTO(id="p2", name="Carlos"))
    service.record_payment(RecordPaymentDTO(participant_id="p2", amount=1000.0))

    # Liquidamos semana 1: Carlos incumple ($100 penalizacion), Maria cumple y se lleva los $100
    close_w1 = service.close_and_liquidate_week(week_number=1)
    assert close_w1.met_count == 1
    assert close_w1.missed_count == 1
    assert close_w1.gain_per_participant == 100.0

    # Resumen de Maria:
    # Aportado: $1000, Semanas cumplidas: 1, Semanas incumplidas: 0, Penalizaciones: $0, Ganancias: $100, Balance: $1100
    summary_maria = service.get_participant_summary("p1")
    assert summary_maria.total_contributed == 1000.0
    assert summary_maria.weeks_met == 1
    assert summary_maria.weeks_missed == 0
    assert summary_maria.total_penalties == 0.0
    assert summary_maria.total_earnings == 100.0
    assert summary_maria.net_balance == 1100.0

    # Resumen de Carlos:
    # Aportado: $1000, Semanas cumplidas: 0, Semanas incumplidas: 1, Penalizaciones: $100, Ganancias: $0, Balance: $900
    summary_carlos = service.get_participant_summary("p2")
    assert summary_carlos.total_contributed == 1000.0
    assert summary_carlos.weeks_met == 0
    assert summary_carlos.weeks_missed == 1
    assert summary_carlos.total_penalties == 100.0
    assert summary_carlos.total_earnings == 0.0
    assert summary_carlos.net_balance == 900.0


def test_general_summary():
    service = ChallengeService()
    service.register_participant(RegisterParticipantDTO(id="p1", name="Participante 1"))
    service.register_participant(RegisterParticipantDTO(id="p2", name="Participante 2"))
    service.record_payment(RecordPaymentDTO(participant_id="p1", amount=200.0))
    service.record_payment(RecordPaymentDTO(participant_id="p2", amount=200.0))

    summary = service.get_general_summary()
    assert summary.total_participants == 2
    assert summary.total_funds_collected == 400.0
