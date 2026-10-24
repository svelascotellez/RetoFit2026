"""
Modulo de Dominio: Bolsa Semanal de Penalizaciones
Criterios EARS: AC-1.3, AC-1.4, AC-1.5
"""
from dataclasses import dataclass
from typing import Tuple


@dataclass
class WeeklyPool:
    week_number: int
    initial_rollover: float = 0.0
    total_penalties: float = 0.0
    is_closed: bool = False
    gain_per_participant: float = 0.0
    rollover_to_next: float = 0.0

    def __post_init__(self) -> None:
        if self.week_number < 1:
            raise ValueError("El numero de semana debe ser al menos 1")
        if self.initial_rollover < 0:
            raise ValueError("El fondo inicial no puede ser negativo")

    @property
    def current_total(self) -> float:
        """Total acumulado en la bolsa (fondo transferido + penalizaciones acumuladas)."""
        return round(self.initial_rollover + self.total_penalties, 2)

    def add_penalty(self, amount: float = 100.0) -> None:
        """Agrega el monto de una penalizacion por participante que incumplio."""
        if self.is_closed:
            raise ValueError("No se pueden agregar penalizaciones a una bolsa cerrada")
        if amount <= 0:
            raise ValueError("El monto de penalizacion debe ser positivo")
        self.total_penalties = round(self.total_penalties + amount, 2)

    def distribute(self, met_participants_count: int) -> Tuple[float, float]:
        """Liquida la bolsa semanal:
        - Si hay al menos un cumplidor: reparte equitativamente a 2 decimales y rollover es 0.
        - Si no hay cumplidores: la bolsa completa se traslada (rollover) a la siguiente semana.
        Retorna (ganancia_por_cumplidor, monto_trasladado).
        """
        if self.is_closed:
            return self.gain_per_participant, self.rollover_to_next

        if met_participants_count < 0:
            raise ValueError("El conteo de participantes no puede ser negativo")

        total = self.current_total

        if met_participants_count > 0:
            self.gain_per_participant = round(total / met_participants_count, 2)
            self.rollover_to_next = 0.0
        else:
            self.gain_per_participant = 0.0
            self.rollover_to_next = total

        self.is_closed = True
        return self.gain_per_participant, self.rollover_to_next
