"""
Modulo de Dominio: Actividad Diaria
Criterios EARS: AC-1.1, AC-1.8
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class DailyActivity:
    calories: int
    steps: int

    def __post_init__(self) -> None:
        if self.calories < 0:
            raise ValueError("Calorias no pueden ser negativas")
        if self.steps < 0:
            raise ValueError("Pasos no pueden ser negativos")

    def is_successful(self) -> bool:
        """Determina si el dia es exitoso segun las reglas del Reto Fit:
        Quemar al menos 300 calorias o caminar al menos 10,000 pasos.
        """
        return self.calories >= 300 or self.steps >= 10_000
