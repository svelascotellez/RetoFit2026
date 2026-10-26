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


@dataclass(frozen=True)
class WeeklyParticipantReportDTO:
    participant_id: str
    name: str
    successful_days: int
    is_met: bool
    total_contributed: float
    expected_contribution: float
    financial_status: str
    pending_amount: float
    penalty: float
    earnings: float
    net_balance_impact: float


@dataclass(frozen=True)
class WeeklyReportDTO:
    week_number: int
    total_participants: int
    met_count: int
    missed_count: int
    compliance_rate: float
    expected_contribution_per_participant: float
    total_expected_funds: float
    total_collected_funds: float
    participants_up_to_date: int
    participants_behind: int
    is_closed: bool
    pool_amount: float
    gain_per_compliant: float
    participants: List[WeeklyParticipantReportDTO]


@dataclass(frozen=True)
class ParticipantRankingDTO:
    rank_position: int
    participant_id: str
    name: str
    successful_days: int
    total_calories: float
    total_steps: int
    is_podium: bool


@dataclass(frozen=True)
class WeeklyStatsTrendDTO:
    week_number: int
    successful_days: int
    compliant_participants: int
    total_participants: int
    compliance_rate: float
    pool_amount: float


@dataclass(frozen=True)
class GlobalStatsDTO:
    total_calories: float
    total_steps: int
    total_successful_days: int
    total_activity_days: int
    average_daily_calories: float
    average_daily_steps: float
    total_participants: int
    total_penalties: float
    total_distributed_pool: float
    ranking: List[ParticipantRankingDTO]
    weekly_trends: List[WeeklyStatsTrendDTO]
