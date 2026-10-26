"""
Modulo de Dominio: Informe Semanal de Cuotas y Cumplimiento
Criterios EARS: AC-6.1, AC-6.2, AC-6.3
"""
from dataclasses import dataclass, field
from typing import List


def get_expected_contribution_for_week(week_number: int) -> float:
    """Calcula la cuota acumulada exigible segun el calendario oficial de 5 aportaciones:
    - 19 oct (Semanas 1 y 2): $200.00
    - 2 nov (Semanas 3 y 4): $400.00 acumulados
    - 16 nov (Semanas 5 y 6): $600.00 acumulados
    - 30 nov (Semanas 7 y 8): $800.00 acumulados
    - 14 dic (Semana 9 final): $900.00 acumulados
    """
    if week_number < 1 or week_number > 9:
        raise ValueError("El numero de semana debe estar entre 1 y 9")
    if week_number in (1, 2):
        return 200.0
    elif week_number in (3, 4):
        return 400.0
    elif week_number in (5, 6):
        return 600.0
    elif week_number in (7, 8):
        return 800.0
    else:
        return 900.0


@dataclass(frozen=True)
class WeeklyParticipantReportItem:
    participant_id: str
    name: str
    successful_days: int
    is_met: bool
    total_contributed: float
    expected_contribution: float
    financial_status: str  # "AL_CORRIENTE" | "PENDIENTE"
    pending_amount: float
    penalty: float
    earnings: float
    net_balance_impact: float

    @classmethod
    def calculate(
        cls,
        participant_id: str,
        name: str,
        successful_days: int,
        total_contributed: float,
        week_number: int,
        is_week_closed: bool = False,
        assigned_earnings: float = 0.0,
        min_successful_days: int = 4,
        penalty_amount: float = 100.0,
    ) -> "WeeklyParticipantReportItem":
        expected = get_expected_contribution_for_week(week_number)
        is_met = successful_days >= min_successful_days
        penalty = 0.0 if is_met else penalty_amount
        earnings = round(assigned_earnings, 2) if is_week_closed and is_met else 0.0
        pending = round(max(0.0, expected - total_contributed), 2)
        financial_status = "AL_CORRIENTE" if total_contributed >= expected else "PENDIENTE"
        net_impact = round(earnings - penalty, 2)

        return cls(
            participant_id=participant_id,
            name=name,
            successful_days=successful_days,
            is_met=is_met,
            total_contributed=round(total_contributed, 2),
            expected_contribution=round(expected, 2),
            financial_status=financial_status,
            pending_amount=pending,
            penalty=round(penalty, 2),
            earnings=earnings,
            net_balance_impact=net_impact,
        )


@dataclass(frozen=True)
class WeeklyReport:
    week_number: int
    total_participants: int
    met_count: int = 0
    missed_count: int = 0
    compliance_rate: float = 0.0
    expected_contribution_per_participant: float = 0.0
    total_expected_funds: float = 0.0
    total_collected_funds: float = 0.0
    participants_up_to_date: int = 0
    participants_behind: int = 0
    is_closed: bool = False
    pool_amount: float = 0.0
    gain_per_compliant: float = 0.0
    participants: List[WeeklyParticipantReportItem] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.week_number < 1 or self.week_number > 9:
            raise ValueError("El numero de semana debe estar entre 1 y 9")
