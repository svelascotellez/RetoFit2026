"""
Modulo de Dominio: Participante del Reto Fit
Criterios EARS: AC-1.6, AC-1.8
"""
from dataclasses import dataclass, field
from typing import Dict, List
from src.domain.activity import DailyActivity


@dataclass
class Participant:
    id: str
    name: str
    TARGET_CONTRIBUTION: float = 900.0
    MAX_CONTRIBUTIONS: int = 5
    contributions: List[float] = field(default_factory=list)
    # activities: week_number -> {day_of_week -> DailyActivity}
    activities: Dict[int, Dict[int, DailyActivity]] = field(default_factory=dict)

    @property
    def total_contributed(self) -> float:
        """Suma de todas las aportaciones realizadas."""
        return round(sum(self.contributions), 2)

    def add_contribution(self, amount: float) -> None:
        """Registra un pago quincenal de aportacion hacia la meta de $900."""
        if amount <= 0:
            raise ValueError("Monto debe ser mayor a cero")
        if len(self.contributions) >= self.MAX_CONTRIBUTIONS:
            raise ValueError(f"Ya se ha registrado el maximo de {self.MAX_CONTRIBUTIONS} aportaciones")
        self.contributions.append(round(amount, 2))

    def record_activity(self, week_number: int, day_of_week: int, activity: DailyActivity) -> None:
        """Registra la actividad de un dia en una semana especifica (day_of_week: 1 a 7)."""
        if day_of_week < 1 or day_of_week > 7:
            raise ValueError("El dia de la semana debe ser entre 1 y 7")
        if week_number not in self.activities:
            self.activities[week_number] = {}
        self.activities[week_number][day_of_week] = activity

    def update_name(self, new_name: str) -> None:
        """Actualiza el nombre del participante validando que no sea vacio."""
        if not new_name or not new_name.strip():
            raise ValueError("El nombre no puede estar vacio")
        self.name = new_name.strip()

    def remove_last_contribution(self) -> float:
        """Elimina la ultima aportacion registrada del participante y devuelve el monto eliminado."""
        if not self.contributions:
            raise ValueError("El participante no tiene aportaciones registradas")
        return self.contributions.pop()

    def remove_activity(self, week_number: int, day_of_week: int) -> bool:
        """Elimina la actividad registrada para un dia y semana especificos. Retorna True si existia."""
        if day_of_week < 1 or day_of_week > 7:
            raise ValueError("El dia de la semana debe ser entre 1 y 7")
        if week_number in self.activities and day_of_week in self.activities[week_number]:
            del self.activities[week_number][day_of_week]
            return True
        return False

    def get_successful_days(self, week_number: int) -> int:
        """Calcula el total de dias exitosos acumulados en una semana especifica."""
        week_data = self.activities.get(week_number, {})
        return sum(1 for act in week_data.values() if act.is_successful())

