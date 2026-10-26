"""
Pruebas Unitarias: Estadisticas Integrales del Reto Fit
Criterios EARS: AC-7.1, AC-7.2, AC-7.3
"""
import pytest
from src.domain.challenge_stats import (
    ParticipantRankingItem,
    WeeklyStatsTrendItem,
    GlobalStats,
    calculate_participant_ranking,
    calculate_global_stats,
)


def test_ac_7_1_global_calories_and_steps_metrics():
    """AC-7.1: Calcula metricas globales acumuladas de calorias y pasos con promedios diarios."""
    participants_data = [
        {
            "participant_id": "P1",
            "name": "Ana",
            "activities": [
                {"calories": 350.0, "steps": 8000, "is_successful": True},
                {"calories": 250.0, "steps": 12000, "is_successful": True},
            ],
        },
        {
            "participant_id": "P2",
            "name": "Carlos",
            "activities": [
                {"calories": 400.0, "steps": 9000, "is_successful": True},
                {"calories": 100.0, "steps": 4000, "is_successful": False},
            ],
        },
    ]

    stats = calculate_global_stats(
        participants_data=participants_data,
        total_penalties=200.0,
        total_distributed_pool=150.0,
    )

    assert stats.total_calories == 1100.0
    assert stats.total_steps == 33000
    assert stats.total_activity_days == 4
    assert stats.total_successful_days == 3
    assert stats.average_daily_calories == 275.0  # 1100 / 4
    assert stats.average_daily_steps == 8250.0  # 33000 / 4
    assert stats.total_penalties == 200.0
    assert stats.total_distributed_pool == 150.0


def test_ac_7_1_empty_activities_zero_division_guard():
    """AC-7.1: Manejo seguro de cero actividades sin ZeroDivisionError."""
    stats = calculate_global_stats(participants_data=[])

    assert stats.total_calories == 0.0
    assert stats.total_steps == 0
    assert stats.total_activity_days == 0
    assert stats.total_successful_days == 0
    assert stats.average_daily_calories == 0.0
    assert stats.average_daily_steps == 0.0
    assert stats.ranking == []
    assert len(stats.weekly_trends) == 9


def test_ac_7_2_ranking_generation_with_tie_breaker():
    """AC-7.2: Ranking ordenado por dias exitosos desc, desempate por calorias desc."""
    items = [
        {"participant_id": "P1", "name": "Ana", "successful_days": 8, "total_calories": 2800.0, "total_steps": 70000},
        {"participant_id": "P2", "name": "Beto", "successful_days": 10, "total_calories": 3200.0, "total_steps": 85000},
        {"participant_id": "P3", "name": "Clara", "successful_days": 8, "total_calories": 3100.0, "total_steps": 72000},
        {"participant_id": "P4", "name": "David", "successful_days": 5, "total_calories": 2000.0, "total_steps": 45000},
    ]

    ranking = calculate_participant_ranking(items)

    assert len(ranking) == 4
    # P2 tiene 10 días
    assert ranking[0].participant_id == "P2"
    assert ranking[0].rank_position == 1
    assert ranking[0].is_podium is True

    # P3 y P1 tienen 8 días, pero P3 tiene 3100 cal vs 2800 cal
    assert ranking[1].participant_id == "P3"
    assert ranking[1].rank_position == 2
    assert ranking[1].is_podium is True

    assert ranking[2].participant_id == "P1"
    assert ranking[2].rank_position == 3
    assert ranking[2].is_podium is True

    # P4 queda fuera del podio
    assert ranking[3].participant_id == "P4"
    assert ranking[3].rank_position == 4
    assert ranking[3].is_podium is False


def test_ac_7_3_weekly_compliance_trends():
    """AC-7.3: Tendencias semanales para las 9 semanas con dias exitosos y tasa de cumplimiento."""
    weekly_raw_data = {
        1: {"successful_days": 24, "compliant": 6, "total": 8, "pool": 200.0},
        2: {"successful_days": 20, "compliant": 5, "total": 8, "pool": 300.0},
    }

    stats = calculate_global_stats(
        participants_data=[],
        weekly_raw_data=weekly_raw_data,
        total_participants_count=8,
    )

    trends = stats.weekly_trends
    assert len(trends) == 9

    # Semana 1
    assert trends[0].week_number == 1
    assert trends[0].successful_days == 24
    assert trends[0].compliant_participants == 6
    assert trends[0].total_participants == 8
    assert trends[0].compliance_rate == 75.0
    assert trends[0].pool_amount == 200.0

    # Semana 2
    assert trends[1].week_number == 2
    assert trends[1].compliance_rate == 62.5

    # Semana 3 (sin datos registrados)
    assert trends[2].week_number == 3
    assert trends[2].successful_days == 0
    assert trends[2].compliant_participants == 0
    assert trends[2].compliance_rate == 0.0


def test_ac_7_4_rest_api_statistics_endpoint():
    """AC-7.4: Endpoint REST /api/statistics responde con 200 y esquema consolidado."""
    from fastapi.testclient import TestClient
    from src.presentation.api import create_app
    from src.application.challenge_service import ChallengeService
    from src.application.dto import RegisterParticipantDTO, RecordActivityDTO

    service = ChallengeService()
    service.register_participant(RegisterParticipantDTO(id="P1", name="Ana"))
    service.record_daily_activity(
        RecordActivityDTO(participant_id="P1", week_number=1, day_of_week=1, calories=400, steps=11000)
    )

    app = create_app(service)
    client = TestClient(app)

    res = client.get("/api/statistics")
    assert res.status_code == 200
    data = res.json()

    assert data["total_calories"] == 400.0
    assert data["total_steps"] == 11000
    assert data["total_successful_days"] == 1
    assert data["total_activity_days"] == 1
    assert data["average_daily_calories"] == 400.0
    assert data["average_daily_steps"] == 11000.0
    assert len(data["ranking"]) == 1
    assert data["ranking"][0]["participant_id"] == "P1"
    assert data["ranking"][0]["rank_position"] == 1
    assert data["ranking"][0]["is_podium"] is True
    assert len(data["weekly_trends"]) == 9


def test_ac_7_5_accessible_tabs_navigation():
    """AC-7.5: Navegacion por pestanas accesibles con roles semanticos ARIA."""
    from src.application.challenge_service import ChallengeService
    from src.presentation.web_views import render_dashboard_html

    service = ChallengeService()
    html = render_dashboard_html(service)

    # Roles semánticos y accesibilidad
    assert 'role="tablist"' in html
    assert 'role="tab"' in html
    assert 'role="tabpanel"' in html
    assert 'id="tab-general"' in html
    assert 'id="tab-stats"' in html
    assert 'id="panel-general"' in html
    assert 'id="panel-stats"' in html
    assert 'aria-controls="panel-general"' in html
    assert 'aria-controls="panel-stats"' in html
    assert 'switchTab(' in html


def test_ac_7_6_accessible_empty_state_without_activities():
    """AC-7.6: Despliegue de estado vacio accesible con role status sin actividades registradas."""
    from src.application.challenge_service import ChallengeService
    from src.application.dto import RegisterParticipantDTO, RecordActivityDTO
    from src.presentation.web_views import render_dashboard_html

    # Caso 1: Sin actividades
    service_empty = ChallengeService()
    html_empty = render_dashboard_html(service_empty)

    assert 'id="stats-empty-state"' in html_empty
    assert 'role="status"' in html_empty
    assert 'No hay actividades registradas en el reto' in html_empty

    # Caso 2: Con actividades registradas -> visualiza podio y analitica
    service_active = ChallengeService()
    service_active.register_participant(RegisterParticipantDTO(id="P1", name="Ana"))
    service_active.record_daily_activity(
        RecordActivityDTO(participant_id="P1", week_number=1, day_of_week=1, calories=500, steps=12000)
    )
    html_active = render_dashboard_html(service_active)

    assert 'Podio y Ranking de Rendimiento' in html_active
    assert 'Calorías Totales Quemadas' in html_active
    assert 'Pasos Totales Caminados' in html_active
    assert 'id="stats-empty-state"' not in html_active
