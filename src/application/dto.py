"""
Capa de Aplicacion: Objetos de Transferencia de Datos (DTOs)
"""
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class RegisterParticipantDTO:
    id: str
    name: str


@dataclass(frozen=True)
class RecordPaymentDTO:
    participant_id: str
    amount: float


@dataclass(frozen=True)
class RecordActivityDTO:
    participant_id: str
    week_number: int
    day_of_week: int
    calories: int
    steps: int


@dataclass(frozen=True)
class WeeklyCloseResultDTO:
    week_number: int
    met_count: int
    missed_count: int
    pool_collected: float
    gain_per_participant: float
    rollover_to_next: float


@dataclass(frozen=True)
class GeneralSummaryDTO:
    total_participants: int
    total_funds_collected: float
    total_penalties_distributed: float
    total_rollover_balance: float
    participants: List["ParticipantSummaryDTO"]


@dataclass(frozen=True)
class ParticipantSummaryDTO:
    participant_id: str
    name: str
    total_contributed: float
    weeks_met: int
    weeks_missed: int
    total_penalties: float
    total_earnings: float
    net_balance: float
