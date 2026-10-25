"""
Capa de Presentacion: Esquemas Pydantic V2 para la API de Reto Fit
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class ParticipantCreateSchema(BaseModel):
    id: str = Field(..., min_length=1, description="Identificador único del participante")
    name: str = Field(..., min_length=1, description="Nombre del participante")


class ParticipantResponseSchema(BaseModel):
    id: str
    name: str
    total_contributed: float
    target_contribution: float = 900.0


class PaymentCreateSchema(BaseModel):
    participant_id: str = Field(..., min_length=1)
    amount: float = Field(..., description="Monto de aportación quincenal")


class PaymentResponseSchema(BaseModel):
    participant_id: str
    total_contributed: float
    target_contribution: float = 900.0


class ActivityCreateSchema(BaseModel):
    participant_id: str = Field(..., min_length=1)
    week_number: int = Field(..., ge=1, le=10, description="Número de semana (1 a 9)")
    day_of_week: int = Field(..., ge=1, le=7, description="Día de la semana (1 a 7)")
    calories: int = Field(..., ge=0, description="Calorías quemadas (mínimo 0)")
    steps: int = Field(..., ge=0, description="Pasos caminados (mínimo 0)")


class ActivityResponseSchema(BaseModel):
    participant_id: str
    week_number: int
    day_of_week: int
    calories: int
    steps: int
    is_successful: bool


class WeeklyCloseResponseSchema(BaseModel):
    week_number: int
    met_count: int
    missed_count: int
    pool_collected: float
    gain_per_participant: float
    rollover_to_next: float


class ParticipantSummaryItem(BaseModel):
    participant_id: str
    name: str
    total_contributed: float
    weeks_met: int
    weeks_missed: int
    total_penalties: float
    total_earnings: float
    net_balance: float


class SummaryResponseSchema(BaseModel):
    total_participants: int
    total_funds_collected: float
    total_penalties_distributed: float
    total_rollover_balance: float
    participants: List[ParticipantSummaryItem]


class HealthCheckResponse(BaseModel):
    status: str = "healthy"
