"""
Modulo de Dominio: Concentrado y Balance Financiero
Criterio EARS: AC-1.7
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class FinancialSummary:
    participant_id: str
    name: str
    total_contributed: float
    weeks_met: int
    weeks_missed: int
    total_penalties: float
    total_earnings: float
    net_balance: float

    @classmethod
    def calculate(
        cls,
        participant_id: str,
        name: str,
        total_contributed: float,
        weeks_met: int,
        weeks_missed: int,
        total_earnings: float = 0.0,
        penalty_per_missed_week: float = 100.0,
    ) -> "FinancialSummary":
        """Calcula el balance y resumen financiero para un participante.
        Formula:
        Total Penalizado = Semanas Incumplidas * $100
        Monto Neto Final = Total Aportado - Total Penalizado + Total Ganancias de Bolsa
        """
        penalties = round(weeks_missed * penalty_per_missed_week, 2)
        net = round(total_contributed - penalties + total_earnings, 2)
        return cls(
            participant_id=participant_id,
            name=name,
            total_contributed=round(total_contributed, 2),
            weeks_met=weeks_met,
            weeks_missed=weeks_missed,
            total_penalties=penalties,
            total_earnings=round(total_earnings, 2),
            net_balance=net,
        )
