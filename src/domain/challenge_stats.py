"""
Modulo de Dominio: Estadisticas Integrales del Reto Fit
Criterios EARS: AC-7.1, AC-7.2, AC-7.3
Arquitectura Limpia: Cero dependencias externas.
"""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class ParticipantRankingItem:
    rank_position: int
    participant_id: str
    name: str
    successful_days: int
    total_calories: float
    total_steps: int
    is_podium: bool


@dataclass(frozen=True)
class WeeklyStatsTrendItem:
    week_number: int
    successful_days: int
    compliant_participants: int
    total_participants: int
    compliance_rate: float
    pool_amount: float


@dataclass(frozen=True)
class GlobalStats:
    total_calories: float = 0.0
    total_steps: int = 0
    total_successful_days: int = 0
    total_activity_days: int = 0
    average_daily_calories: float = 0.0
    average_daily_steps: float = 0.0
    total_participants: int = 0
    total_penalties: float = 0.0
    total_distributed_pool: float = 0.0
    ranking: List[ParticipantRankingItem] = field(default_factory=list)
    weekly_trends: List[WeeklyStatsTrendItem] = field(default_factory=list)


def calculate_participant_ranking(participants_summary: List[Dict[str, Any]]) -> List[ParticipantRankingItem]:
    """Genera el ranking de participantes ordenado descendentemente por dias exitosos,
    y desempate secundario por total de calorias quemadas.
    Asigna posicion consecutiva y marca podio a los primeros 3.
    """
    sorted_items = sorted(
        participants_summary,
        key=lambda item: (
            item.get("successful_days", 0),
            item.get("total_calories", 0.0),
            item.get("total_steps", 0),
        ),
        reverse=True,
    )

    ranking: List[ParticipantRankingItem] = []
    for idx, p in enumerate(sorted_items, start=1):
        ranking.append(
            ParticipantRankingItem(
                rank_position=idx,
                participant_id=str(p.get("participant_id", "")),
                name=str(p.get("name", "")),
                successful_days=int(p.get("successful_days", 0)),
                total_calories=round(float(p.get("total_calories", 0.0)), 2),
                total_steps=int(p.get("total_steps", 0)),
                is_podium=(idx <= 3),
            )
        )
    return ranking


def calculate_global_stats(
    participants_data: Optional[List[Dict[str, Any]]] = None,
    total_penalties: float = 0.0,
    total_distributed_pool: float = 0.0,
    weekly_raw_data: Optional[Dict[int, Dict[str, Any]]] = None,
    total_participants_count: Optional[int] = None,
) -> GlobalStats:
    """Calcula las metricas globales, ranking y tendencias para el reto fit."""
    p_data = participants_data or []
    w_data = weekly_raw_data or {}

    total_calories = 0.0
    total_steps = 0
    total_successful_days = 0
    total_activity_days = 0

    ranking_input: List[Dict[str, Any]] = []

    for p in p_data:
        p_id = p.get("participant_id", "")
        p_name = p.get("name", "")
        p_calories = 0.0
        p_steps = 0
        p_success = 0

        # Si se paso lista de actividades
        activities = p.get("activities", [])
        for act in activities:
            c = float(act.get("calories", 0.0))
            s = int(act.get("steps", 0))
            succ = bool(act.get("is_successful", False))

            p_calories += c
            p_steps += s
            total_calories += c
            total_steps += s
            total_activity_days += 1
            if succ:
                p_success += 1
                total_successful_days += 1

        # O si ya vienen agregadas
        if not activities and ("total_calories" in p or "successful_days" in p):
            p_calories = float(p.get("total_calories", 0.0))
            p_steps = int(p.get("total_steps", 0))
            p_success = int(p.get("successful_days", 0))
            p_activity_days = int(p.get("total_activity_days", p_success))
            total_calories += p_calories
            total_steps += p_steps
            total_successful_days += p_success
            total_activity_days += p_activity_days

        ranking_input.append(
            {
                "participant_id": p_id,
                "name": p_name,
                "successful_days": p_success,
                "total_calories": p_calories,
                "total_steps": p_steps,
            }
        )

    ranking = calculate_participant_ranking(ranking_input)

    avg_calories = (
        round(total_calories / total_activity_days, 2)
        if total_activity_days > 0
        else 0.0
    )
    avg_steps = (
        round(total_steps / total_activity_days, 2)
        if total_activity_days > 0
        else 0.0
    )

    participant_count = (
        total_participants_count
        if total_participants_count is not None
        else len(ranking_input)
    )

    # Generar tendencias de las 9 semanas
    weekly_trends: List[WeeklyStatsTrendItem] = []
    for w in range(1, 10):
        w_info = w_data.get(w, {})
        w_succ = int(w_info.get("successful_days", 0))
        w_compliant = int(w_info.get("compliant", 0))
        w_total = int(w_info.get("total", participant_count))
        w_pool = round(float(w_info.get("pool", 0.0)), 2)
        w_rate = (
            round((w_compliant / w_total) * 100.0, 1)
            if w_total > 0
            else 0.0
        )
        weekly_trends.append(
            WeeklyStatsTrendItem(
                week_number=w,
                successful_days=w_succ,
                compliant_participants=w_compliant,
                total_participants=w_total,
                compliance_rate=w_rate,
                pool_amount=w_pool,
            )
        )

    return GlobalStats(
        total_calories=round(total_calories, 2),
        total_steps=total_steps,
        total_successful_days=total_successful_days,
        total_activity_days=total_activity_days,
        average_daily_calories=avg_calories,
        average_daily_steps=avg_steps,
        total_participants=participant_count,
        total_penalties=round(total_penalties, 2),
        total_distributed_pool=round(total_distributed_pool, 2),
        ranking=ranking,
        weekly_trends=weekly_trends,
    )
