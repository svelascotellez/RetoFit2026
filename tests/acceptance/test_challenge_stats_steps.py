"""
Step definitions BDD para FEAT-007: Pestaña de Estadísticas Integrales del Reto Fit
Mapeo a Criterios EARS: @AC-7.1 a @AC-7.6
"""
import pytest
from pathlib import Path
from typing import Dict, Any
from fastapi.testclient import TestClient
from pytest_bdd import scenarios, given, when, then, parsers

from src.infrastructure.sqlite_repository import SQLiteChallengeRepository
from src.application.challenge_service import ChallengeService
from src.application.dto import RegisterParticipantDTO, RecordActivityDTO
from src.presentation.api import create_app
from src.presentation.web_views import render_dashboard_html

scenarios("../../specs/007-pestana-estadisticas-retofit/scenarios.feature")


@pytest.fixture
def bdd_db_path(tmp_path: Path) -> str:
    return str(tmp_path / "bdd_challenge_stats.db")


@pytest.fixture
def ctx(bdd_db_path: str) -> Dict[str, Any]:
    repo = SQLiteChallengeRepository(db_path=bdd_db_path)
    service = ChallengeService(repository=repo)
    app = create_app(service)
    client = TestClient(app)
    return {
        "db_path": bdd_db_path,
        "repo": repo,
        "service": service,
        "client": client,
        "stats": None,
        "last_response": None,
        "html_content": None,
    }


# ============================================================================
# AC-7.1: Cálculo de métricas globales de calorías y pasos acumulados
# ============================================================================

@given("que existen participantes con actividades registradas en el reto")
@given("existen participantes con actividades registradas en el reto")
def given_participants_with_activities(ctx: Dict[str, Any]) -> None:
    service = ctx["service"]
    service.register_participant(RegisterParticipantDTO(id="P1", name="Ana"))
    service.register_participant(RegisterParticipantDTO(id="P2", name="Beto"))

    # Actividades de P1 (2 días)
    service.record_daily_activity(
        RecordActivityDTO(participant_id="P1", week_number=1, day_of_week=1, calories=350, steps=8000)
    )
    service.record_daily_activity(
        RecordActivityDTO(participant_id="P1", week_number=1, day_of_week=2, calories=250, steps=12000)
    )

    # Actividades de P2 (2 días)
    service.record_daily_activity(
        RecordActivityDTO(participant_id="P2", week_number=1, day_of_week=1, calories=400, steps=9000)
    )
    service.record_daily_activity(
        RecordActivityDTO(participant_id="P2", week_number=1, day_of_week=2, calories=100, steps=4000)
    )


@when("se calculan las estadisticas globales del reto")
def when_calculate_global_stats(ctx: Dict[str, Any]) -> None:
    ctx["stats"] = ctx["service"].get_global_statistics()


@then("el total de calorias y el total de pasos reflejan la suma de todas las actividades")
def then_total_calories_and_steps_reflect_sum(ctx: Dict[str, Any]) -> None:
    stats = ctx["stats"]
    assert stats.total_calories == 1100.0  # 350 + 250 + 400 + 100
    assert stats.total_steps == 33000  # 8000 + 12000 + 9000 + 4000
    assert stats.total_activity_days == 4
    assert stats.total_successful_days == 3


@then("se calculan los promedios diarios correspondientes")
def then_calculate_daily_averages(ctx: Dict[str, Any]) -> None:
    stats = ctx["stats"]
    assert stats.average_daily_calories == 275.0  # 1100 / 4
    assert stats.average_daily_steps == 8250.0  # 33000 / 4


# ============================================================================
# AC-7.2: Generación de ranking con desempate por calorías
# ============================================================================

@given(parsers.parse('que el participante "{participant_id}" tiene {successful_days:d} dias exitosos y {calories:d} calorias acumuladas'))
@given(parsers.parse('el participante "{participant_id}" tiene {successful_days:d} dias exitosos y {calories:d} calorias acumuladas'))
def given_participant_with_metrics(ctx: Dict[str, Any], participant_id: str, successful_days: int, calories: int) -> None:
    service = ctx["service"]
    if participant_id not in service.participants:
        service.register_participant(RegisterParticipantDTO(id=participant_id, name=f"Miembro {participant_id}"))

    # Repartir los días exitosos y calorías a lo largo de las semanas
    cal_per_day = int(calories / max(1, successful_days))
    remainder_cal = calories - (cal_per_day * successful_days)

    day_counter = 0
    for d in range(1, successful_days + 1):
        week = ((d - 1) // 7) + 1
        day = ((d - 1) % 7) + 1
        c = cal_per_day + (remainder_cal if d == successful_days else 0)
        service.record_daily_activity(
            RecordActivityDTO(
                participant_id=participant_id,
                week_number=week,
                day_of_week=day,
                calories=c,
                steps=5000,
            )
        )


@when("se genera la tabla de ranking de participantes")
def when_generate_ranking_table(ctx: Dict[str, Any]) -> None:
    ctx["stats"] = ctx["service"].get_global_statistics()


@then(parsers.parse('el participante "{participant_id}" ocupa la posicion {position:d}'))
def then_participant_occupies_position(ctx: Dict[str, Any], participant_id: str, position: int) -> None:
    ranking = ctx["stats"].ranking
    item = next((r for r in ranking if r.participant_id == participant_id), None)
    assert item is not None, f"Participante {participant_id} no encontrado en el ranking"
    assert item.rank_position == position


@then(parsers.parse('el participante "{participant_id}" ocupa la posicion {position:d} por desempate de calorias'))
def then_participant_occupies_position_tie_breaker(ctx: Dict[str, Any], participant_id: str, position: int) -> None:
    ranking = ctx["stats"].ranking
    item = next((r for r in ranking if r.participant_id == participant_id), None)
    assert item is not None
    assert item.rank_position == position


# ============================================================================
# AC-7.3: Cálculo de tendencias de cumplimiento semanal
# ============================================================================

@given("que se han registrado actividades y cierres de semana en el sistema")
@given("se han registrado actividades y cierres de semana en el sistema")
def given_activities_and_closes_recorded(ctx: Dict[str, Any]) -> None:
    service = ctx["service"]
    if "P1" not in service.participants:
        service.register_participant(RegisterParticipantDTO(id="P1", name="P1"))
    if "P2" not in service.participants:
        service.register_participant(RegisterParticipantDTO(id="P2", name="P2"))

    # P1 cumple semana 1 (4 días)
    for d in range(1, 5):
        service.record_daily_activity(
            RecordActivityDTO(participant_id="P1", week_number=1, day_of_week=d, calories=350, steps=2000)
        )

    # P2 incumple semana 1 (0 días)
    service.close_and_liquidate_week(week_number=1)


@when("se evalua la tendencia de las 9 semanas del reto")
def when_evaluate_9_weeks_trend(ctx: Dict[str, Any]) -> None:
    ctx["stats"] = ctx["service"].get_global_statistics()


@then("se obtienen las metricas semanales con dias exitosos y participantes cumplidores")
def then_verify_weekly_metrics(ctx: Dict[str, Any]) -> None:
    trends = ctx["stats"].weekly_trends
    assert len(trends) == 9
    w1 = trends[0]
    assert w1.week_number == 1
    assert w1.successful_days == 4
    assert w1.compliant_participants == 1
    assert w1.total_participants >= 2
    assert w1.compliance_rate > 0.0


# ============================================================================
# AC-7.4: Endpoint REST /api/statistics
# ============================================================================

@given("que el servicio de estadisticas esta disponible")
@given("el servicio de estadisticas esta disponible")
def given_statistics_service_available(ctx: Dict[str, Any]) -> None:
    assert ctx["client"] is not None


@when(parsers.parse('se envia una peticion GET al endpoint "{endpoint}"'))
def when_get_endpoint(ctx: Dict[str, Any], endpoint: str) -> None:
    ctx["last_response"] = ctx["client"].get(endpoint)


@then("la API responde con codigo 200 y el esquema de estadisticas globales y ranking")
def then_api_responds_with_200_and_schema(ctx: Dict[str, Any]) -> None:
    res = ctx["last_response"]
    assert res.status_code == 200
    data = res.json()
    assert "total_calories" in data
    assert "total_steps" in data
    assert "total_successful_days" in data
    assert "ranking" in data
    assert "weekly_trends" in data
    assert len(data["weekly_trends"]) == 9


# ============================================================================
# AC-7.5: Navegación por pestañas interactiva en el Dashboard Web
# ============================================================================

@given("que el usuario carga el Dashboard Web")
@given("el usuario carga el Dashboard Web")
def given_user_loads_dashboard(ctx: Dict[str, Any]) -> None:
    ctx["html_content"] = render_dashboard_html(ctx["service"])


@when("observa la barra de navegacion con pestanas")
def when_observes_tab_bar(ctx: Dict[str, Any]) -> None:
    assert ctx["html_content"] is not None


@then('existen las pestanas accesibles "Panel General" y "Estadísticas del Reto" con roles "tab" y contenedor "tabpanel"')
def then_verify_accessible_tabs(ctx: Dict[str, Any]) -> None:
    html = ctx["html_content"]
    assert 'role="tablist"' in html
    assert 'role="tab"' in html
    assert 'role="tabpanel"' in html
    assert 'id="tab-general"' in html
    assert 'id="tab-stats"' in html
    assert 'Panel General' in html
    assert 'Estadísticas del Reto' in html
    assert 'id="panel-general"' in html
    assert 'id="panel-stats"' in html


# ============================================================================
# AC-7.6: Estado vacío accesible en la pestaña de estadísticas
# ============================================================================

@given("que no existen actividades fisicas registradas en el reto")
@given("no existen actividades fisicas registradas en el reto")
def given_no_physical_activities(ctx: Dict[str, Any]) -> None:
    # Service inicial sin actividades
    pass


@when('el usuario activa la pestana de "Estadísticas del Reto"')
def when_user_activates_stats_tab(ctx: Dict[str, Any]) -> None:
    ctx["html_content"] = render_dashboard_html(ctx["service"])


@then('se visualiza el estado vacio accesible con rol "status" informando la falta de actividad')
def then_verify_accessible_empty_state_in_stats(ctx: Dict[str, Any]) -> None:
    html = ctx["html_content"]
    assert 'id="stats-empty-state"' in html
    assert 'role="status"' in html
    assert 'No hay actividades registradas en el reto' in html
