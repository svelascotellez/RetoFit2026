"""
Capa de Aplicacion: Contrato de Persistencia (Repository Pattern)
Criterios EARS: AC-3.1 a AC-3.6
"""
from typing import Protocol, List, Optional, Dict, Any
from src.domain.participant import Participant
from src.domain.activity import DailyActivity


class ChallengeRepository(Protocol):
    """Interfaz abstracta para el almacenamiento persistente del Reto Fit."""

    def save_participant(self, participant: Participant) -> None:
        """Persiste un participante en la base de datos."""
        ...

    def get_participant(self, participant_id: str) -> Optional[Participant]:
        """Obtiene un participante por su ID."""
        ...

    def list_participants(self) -> List[Participant]:
        """Lista todos los participantes registrados."""
        ...

    def record_payment(self, participant_id: str, amount: float) -> None:
        """Registra un abono para un participante."""
        ...

    def record_activity(
        self,
        participant_id: str,
        week_number: int,
        day_of_week: int,
        activity: DailyActivity,
    ) -> None:
        """Registra la actividad diaria de un participante."""
        ...

    def record_week_close(
        self,
        week_number: int,
        compliant_ids: List[str],
        non_compliant_ids: List[str],
        pool_collected: float,
        rollover_amount: float,
        payout_per_compliant: float,
    ) -> None:
        """Registra la liquidacion y cierre de una semana."""
        ...

    def get_rollover(self) -> float:
        """Obtiene el fondo acumulado de rollover actual."""
        ...

    def set_rollover(self, amount: float) -> None:
        """Actualiza el fondo acumulado de rollover."""
        ...

    def load_all_state(self) -> Dict[str, Any]:
        """Carga todo el estado estructurado para rehidratar el servicio."""
        ...
