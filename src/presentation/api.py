"""
Capa de Presentacion: Router FastAPI con Endpoints REST para Reto Fit
Criterios EARS: AC-2.1 a AC-2.6, AC-2.8
"""
from typing import Callable, Any, Dict
from pydantic import BaseModel, Field, field_validator
from fastapi import APIRouter, Depends, HTTPException, status, FastAPI
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
    WeeklyReportResponseSchema,
    WeeklyParticipantReportItem,
    GlobalStatsResponseSchema,
    ParticipantRankingSchema,
    WeeklyStatsTrendSchema,
)

router = APIRouter()


import os
from src.infrastructure.sqlite_repository import SQLiteChallengeRepository

_db_path = os.environ.get("RETOFIT_DB_PATH", "data/retofit.db")
_sqlite_repo = SQLiteChallengeRepository(db_path=_db_path)
_service_instance = ChallengeService(repository=_sqlite_repo)


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


@router.get(
    "/api/reports/weekly/{week_number}",
    response_model=WeeklyReportResponseSchema,
    summary="Informe semanal de cuotas y cumplimiento del reto",
)
def get_weekly_report(
    week_number: int,
    service: ChallengeService = Depends(get_challenge_service),
) -> WeeklyReportResponseSchema:
    """Retorna el informe detallado de cuotas acumuladas y cumplimiento fisico para una semana (1 a 9)."""
    if week_number < 1 or week_number > 9:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El numero de semana debe estar entre 1 y 9",
        )
    try:
        report = service.get_weekly_report(week_number)
        return WeeklyReportResponseSchema(
            week_number=report.week_number,
            total_participants=report.total_participants,
            met_count=report.met_count,
            missed_count=report.missed_count,
            compliance_rate=report.compliance_rate,
            expected_contribution_per_participant=report.expected_contribution_per_participant,
            total_expected_funds=report.total_expected_funds,
            total_collected_funds=report.total_collected_funds,
            participants_up_to_date=report.participants_up_to_date,
            participants_behind=report.participants_behind,
            is_closed=report.is_closed,
            pool_amount=report.pool_amount,
            gain_per_compliant=report.gain_per_compliant,
            participants=[
                WeeklyParticipantReportItem(
                    participant_id=p.participant_id,
                    name=p.name,
                    successful_days=p.successful_days,
                    is_met=p.is_met,
                    total_contributed=p.total_contributed,
                    expected_contribution=p.expected_contribution,
                    financial_status=p.financial_status,
                    pending_amount=p.pending_amount,
                    penalty=p.penalty,
                    earnings=p.earnings,
                    net_balance_impact=p.net_balance_impact,
                )
                for p in report.participants
            ],
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/api/statistics",
    response_model=GlobalStatsResponseSchema,
    summary="Estadisticas integrales, ranking y tendencias del reto",
)
def get_statistics(service: ChallengeService = Depends(get_challenge_service)) -> GlobalStatsResponseSchema:
    """Retorna las metricas acumuladas globales, ranking de participantes y tendencias semanales."""
    stats = service.get_global_statistics()
    return GlobalStatsResponseSchema(
        total_calories=stats.total_calories,
        total_steps=stats.total_steps,
        total_successful_days=stats.total_successful_days,
        total_activity_days=stats.total_activity_days,
        average_daily_calories=stats.average_daily_calories,
        average_daily_steps=stats.average_daily_steps,
        total_participants=stats.total_participants,
        total_penalties=stats.total_penalties,
        total_distributed_pool=stats.total_distributed_pool,
        ranking=[
            ParticipantRankingSchema(
                rank_position=r.rank_position,
                participant_id=r.participant_id,
                name=r.name,
                successful_days=r.successful_days,
                total_calories=r.total_calories,
                total_steps=r.total_steps,
                is_podium=r.is_podium,
            )
            for r in stats.ranking
        ],
        weekly_trends=[
            WeeklyStatsTrendSchema(
                week_number=t.week_number,
                successful_days=t.successful_days,
                compliant_participants=t.compliant_participants,
                total_participants=t.total_participants,
                compliance_rate=t.compliance_rate,
                pool_amount=t.pool_amount,
            )
            for t in stats.weekly_trends
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


class ParticipantUpdateSchema(BaseModel):
    name: str = Field(..., min_length=1, description="Nuevo nombre del participante")

    @field_validator("name")
    @classmethod
    def validate_name_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("El nombre no puede estar vacio")
        return v.strip()


@router.put(
    "/api/participants/{participant_id}",
    response_model=ParticipantResponseSchema,
    summary="Actualizar nombre de un participante",
)
def update_participant(
    participant_id: str,
    payload: ParticipantUpdateSchema,
    service: ChallengeService = Depends(get_challenge_service),
) -> ParticipantResponseSchema:
    """Actualiza el nombre de un participante registrado."""
    try:
        updated = service.update_participant_name(participant_id, payload.name)
        return ParticipantResponseSchema(
            id=updated.id,
            name=updated.name,
            total_contributed=updated.total_contributed,
            target_contribution=updated.TARGET_CONTRIBUTION,
        )
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@router.delete(
    "/api/participants/{participant_id}",
    summary="Eliminar participante y sus registros asociados",
)
def delete_participant(
    participant_id: str,
    service: ChallengeService = Depends(get_challenge_service),
) -> Dict[str, Any]:
    """Elimina en cascada a un participante, sus abonos y sus actividades."""
    try:
        service.delete_participant(participant_id)
        return {"success": True, "message": f"Participante {participant_id} eliminado exitosamente"}
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete(
    "/api/participants/{participant_id}/payments/last",
    summary="Anular el ultimo abono quincenal de un participante",
)
def delete_last_payment(
    participant_id: str,
    service: ChallengeService = Depends(get_challenge_service),
) -> Dict[str, Any]:
    """Elimina la aportacion mas reciente y reduce el saldo acumulado."""
    try:
        removed_amount = service.delete_last_payment(participant_id)
        current_total = service.participants[participant_id].total_contributed
        return {
            "success": True,
            "removed_amount": removed_amount,
            "total_contributed": current_total,
            "message": f"Abono de ${removed_amount:.2f} anulado exitosamente",
        }
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete(
    "/api/activities/{participant_id}/weeks/{week_number}/days/{day_of_week}",
    summary="Eliminar o restablecer la actividad de un dia especifico",
)
def delete_activity(
    participant_id: str,
    week_number: int,
    day_of_week: int,
    service: ChallengeService = Depends(get_challenge_service),
) -> Dict[str, Any]:
    """Elimina el registro de actividad fisica de un dia y semana especificos."""
    try:
        removed = service.delete_daily_activity(participant_id, week_number, day_of_week)
        return {
            "success": True,
            "removed": removed,
            "message": f"Actividad del dia {day_of_week} semana {week_number} eliminada",
        }
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


def create_app(service: ChallengeService) -> FastAPI:
    """Crea una aplicacion FastAPI configurada con una instancia de servicio dada."""
    test_app = FastAPI(title="Reto Fit API")
    test_app.include_router(router)
    test_app.dependency_overrides[get_challenge_service] = lambda: service

    from src.presentation.web_views import render_dashboard_html
    from fastapi.responses import HTMLResponse

    @test_app.get("/", response_class=HTMLResponse)
    def root_view() -> HTMLResponse:
        return HTMLResponse(content=render_dashboard_html(service))

    return test_app


