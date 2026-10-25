"""
Unit tests para gestion y mutaciones del participante (FEAT-004)
Criterios EARS: AC-4.1 a AC-4.5
"""
import pytest
from src.domain.participant import Participant
from src.domain.activity import DailyActivity


def test_update_name_success() -> None:
    p = Participant(id="P-01", name="Carlos")
    p.update_name("Carlos Gomez")
    assert p.name == "Carlos Gomez"


def test_update_name_empty_or_whitespace_raises_value_error() -> None:
    p = Participant(id="P-01", name="Carlos")
    with pytest.raises(ValueError, match="El nombre no puede estar vacio"):
        p.update_name("")
    with pytest.raises(ValueError, match="El nombre no puede estar vacio"):
        p.update_name("   ")
    assert p.name == "Carlos"


def test_remove_last_contribution_success() -> None:
    p = Participant(id="P-01", name="Carlos")
    p.add_contribution(200.0)
    p.add_contribution(200.0)
    assert p.total_contributed == 400.0
    assert len(p.contributions) == 2

    removed = p.remove_last_contribution()
    assert removed == 200.0
    assert p.total_contributed == 200.0
    assert len(p.contributions) == 1


def test_remove_last_contribution_empty_raises_value_error() -> None:
    p = Participant(id="P-01", name="Carlos")
    with pytest.raises(ValueError, match="El participante no tiene aportaciones registradas"):
        p.remove_last_contribution()


def test_remove_activity_success() -> None:
    p = Participant(id="P-01", name="Carlos")
    act = DailyActivity(calories=350, steps=11000)
    p.record_activity(week_number=1, day_of_week=3, activity=act)
    assert p.get_successful_days(1) == 1

    removed = p.remove_activity(week_number=1, day_of_week=3)
    assert removed is True
    assert p.get_successful_days(1) == 0
    assert 3 not in p.activities.get(1, {})


def test_remove_activity_non_existent_returns_false() -> None:
    p = Participant(id="P-01", name="Carlos")
    removed = p.remove_activity(week_number=1, day_of_week=5)
    assert removed is False


def test_remove_activity_invalid_day_raises_value_error() -> None:
    p = Participant(id="P-01", name="Carlos")
    with pytest.raises(ValueError, match="El dia de la semana debe ser entre 1 y 7"):
        p.remove_activity(week_number=1, day_of_week=8)


def test_service_participant_management_methods() -> None:
    from src.application.challenge_service import ChallengeService
    from src.application.dto import RegisterParticipantDTO, RecordPaymentDTO, RecordActivityDTO

    svc = ChallengeService()
    svc.register_participant(RegisterParticipantDTO(id="S-01", name="Juan"))
    svc.record_payment(RecordPaymentDTO(participant_id="S-01", amount=200.0))
    svc.record_daily_activity(RecordActivityDTO(participant_id="S-01", week_number=1, day_of_week=1, calories=350, steps=10000))

    # Update name
    updated = svc.update_participant_name("S-01", "Juan Perez")
    assert updated.name == "Juan Perez"

    # Delete payment
    removed_pay = svc.delete_last_payment("S-01")
    assert removed_pay == 200.0
    assert svc.participants["S-01"].total_contributed == 0.0

    # Delete activity
    removed_act = svc.delete_daily_activity("S-01", 1, 1)
    assert removed_act is True
    assert svc.participants["S-01"].get_successful_days(1) == 0

    # Delete participant
    assert svc.delete_participant("S-01") is True
    assert "S-01" not in svc.participants

