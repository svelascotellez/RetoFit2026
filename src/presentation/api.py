"""
Capa de Presentacion: Router FastAPI con Endpoints REST para Reto Fit
Criterios EARS: AC-2.1 a AC-2.6, AC-2.8
"""
from typing import Callable
from fastapi import APIRouter, Depends, HTTPException, status
from src.application.challenge_service import ChallengeService
from src.application.dto import (
    RegisterParticipantDTO,
    RecordPaymentDTO,
    RecordActivityDTO,
)
from src.presentation.schemas import (
    ParticipantCreateSchema,
    ParticipantResponseSchema,
    PaymentCreateSchema,
    PaymentResponseSchema,
    ActivityCreateSchema,
    ActivityResponseSchema,
    WeeklyCloseResponseSchema,
    SummaryResponseSchema,
    ParticipantSummaryItem,
    HealthCheckResponse,
)

router = APIRouter()


_service_instance = ChallengeService()


def get_challenge_service() -> ChallengeService:
    return _service_instance


@router.get("/health", response_model=HealthCheckResponse, summary="Verificacion de salud para Railway")
def healthcheck() -> HealthCheckResponse:
    """Endpoint de comprobacion de estado operativo para Railway.com."""
    return HealthCheckResponse(status="healthy")


@router.get("/api/summary", response_model=SummaryResponseSchema, summary="Concentrado general y por participante")
def get_summary(service: ChallengeService = Depends(get_challenge_service)) -> SummaryResponseSchema:
    """Retorna las metricas consolidadas, fondos y resumen individual de los participantes."""
    general = service.get_general_summary()
    return SummaryResponseSchema(
        total_participants=general.total_participants,
        total_funds_collected=general.total_funds_collected,
        total_penalties_distributed=general.total_penalties_distributed,
        total_rollover_balance=general.total_rollover_balance,
        participants=[
            ParticipantSummaryItem(
                participant_id=p.participant_id,
                name=p.name,
                total_contributed=p.total_contributed,
                weeks_met=p.weeks_met,
                weeks_missed=p.weeks_missed,
                total_penalties=p.total_penalties,
                total_earnings=p.total_earnings,
                net_balance=p.net_balance,
            )
            for p in general.participants
        ],
    )


@router.post(
    "/api/participants",
    response_model=ParticipantResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo participante",
)
def register_participant(
    payload: ParticipantCreateSchema,
    service: ChallengeService = Depends(get_challenge_service),
) -> ParticipantResponseSchema:
    """Registra a un miembro DIDT en el Reto Fit."""
    try:
        participant = service.register_participant(
            RegisterParticipantDTO(id=payload.id, name=payload.name)
        )
        return ParticipantResponseSchema(
            id=participant.id,
            name=participant.name,
            total_contributed=participant.total_contributed,
            target_contribution=participant.TARGET_CONTRIBUTION,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/api/payments",
    response_model=PaymentResponseSchema,
    summary="Registrar aportacion economica quincenal",
)
def record_payment(
    payload: PaymentCreateSchema,
    service: ChallengeService = Depends(get_challenge_service),
) -> PaymentResponseSchema:
    """Registra un abono quincenal (meta total de $1,000 en 5 pagos de $200)."""
    if payload.amount <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Monto debe ser mayor a cero")
    try:
        total = service.record_payment(
            RecordPaymentDTO(participant_id=payload.participant_id, amount=payload.amount)
        )
        return PaymentResponseSchema(
            participant_id=payload.participant_id,
            total_contributed=total,
        )
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/api/activity",
    response_model=ActivityResponseSchema,
    summary="Registrar actividad fisica diaria",
)
def record_activity(
    payload: ActivityCreateSchema,
    service: ChallengeService = Depends(get_challenge_service),
) -> ActivityResponseSchema:
    """Registra calorias o pasos diarios y determina si el dia es exitoso (>= 300 kcal o >= 10,000 pasos)."""
    try:
        is_successful = service.record_daily_activity(
            RecordActivityDTO(
                participant_id=payload.participant_id,
                week_number=payload.week_number,
                day_of_week=payload.day_of_week,
                calories=payload.calories,
                steps=payload.steps,
            )
        )
        return ActivityResponseSchema(
            participant_id=payload.participant_id,
            week_number=payload.week_number,
            day_of_week=payload.day_of_week,
            calories=payload.calories,
            steps=payload.steps,
            is_successful=is_successful,
        )
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/api/weeks/{week_number}/close",
    response_model=WeeklyCloseResponseSchema,
    summary="Liquidar y cerrar semana del reto",
)
def close_week(
    week_number: int,
    service: ChallengeService = Depends(get_challenge_service),
) -> WeeklyCloseResponseSchema:
    """Liquida la semana evaluando cumplidores, aplicando penalizaciones y repartiendo la bolsa o rollover."""
    try:
        result = service.close_and_liquidate_week(week_number)
        return WeeklyCloseResponseSchema(
            week_number=result.week_number,
            met_count=result.met_count,
            missed_count=result.missed_count,
            pool_collected=result.pool_collected,
            gain_per_participant=result.gain_per_participant,
            rollover_to_next=result.rollover_to_next,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
