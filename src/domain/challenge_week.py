"""
Modulo de Dominio: Semana del Reto Fit
Criterio EARS: AC-1.2
"""
from dataclasses import dataclass, field
from typing import Set


@dataclass
class ChallengeWeek:
    week_number: int
    MIN_SUCCESSFUL_DAYS: int = 4
    met_participants: Set[str] = field(default_factory=set)
    missed_participants: Set[str] = field(default_factory=set)

    def __post_init__(self) -> None:
        if self.week_number < 1:
            raise ValueError("El numero de semana debe ser al menos 1")

    def evaluate_participant(self, successful_days: int) -> bool:
        """Determina si un participante cumple la semana con base en sus dias exitosos.
        Regla: Minimo 4 dias exitosos en la semana.
        """
        if successful_days < 0 or successful_days > 7:
            raise ValueError("Dias exitosos deben estar entre 0 y 7")
        return successful_days >= self.MIN_SUCCESSFUL_DAYS

    def register_result(self, participant_id: str, successful_days: int) -> bool:
        """Registra el resultado de cumplimiento de un participante en la semana."""
        is_met = self.evaluate_participant(successful_days)
        if is_met:
            self.met_participants.add(participant_id)
            self.missed_participants.discard(participant_id)
        else:
            self.missed_participants.add(participant_id)
            self.met_participants.discard(participant_id)
        return is_met
