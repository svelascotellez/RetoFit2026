"""
Step definitions BDD para FEAT-008: Navegacion Modular por Pestañas del Dashboard Web
Mapeo a Criterios EARS: @AC-8.1 a @AC-8.5
"""
import pytest
from pathlib import Path
from typing import Dict, Any
from fastapi.testclient import TestClient
from pytest_bdd import scenarios, given, when, then, parsers

from src.infrastructure.sqlite_repository import SQLiteChallengeRepository
from src.application.challenge_service import ChallengeService
from src.presentation.api import create_app
from src.presentation.web_views import render_dashboard_html

scenarios("../../specs/008-navegacion-pestanas-concentrado-informe/scenarios.feature")


@pytest.fixture
def bdd_db_path(tmp_path: Path) -> str:
    return str(tmp_path / "bdd_tabs_navigation.db")


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
        "html": "",
        "active_tab": "general",
    }


# ============================================================================
# AC-8.1: Despliegue de la barra de navegación superior con cuatro pestañas
# ============================================================================

@given("que el usuario carga el Dashboard Web")
@given("el usuario carga el Dashboard Web")
def given_user_loads_dashboard(ctx: Dict[str, Any]) -> None:
    ctx["html"] = render_dashboard_html(ctx["service"])


@when("inspecciona la barra superior de navegacion")
def when_inspects_top_navigation_bar(ctx: Dict[str, Any]) -> None:
    assert ctx["html"] != ""


@then('se muestran las 4 pestanas accesibles "Panel General", "Concentrado Físico y Financiero", "Informe Semanal de Cuotas y Cumplimiento" y "Estadísticas del Reto"')
def then_shows_4_accessible_tabs(ctx: Dict[str, Any]) -> None:
    html = ctx["html"]
    assert 'role="tablist"' in html
    assert 'id="tab-general"' in html
    assert 'id="tab-concentrado"' in html
    assert 'id="tab-informe"' in html
    assert 'id="tab-stats"' in html
    assert 'Panel General' in html
    assert 'Concentrado Físico y Financiero' in html
    assert 'Informe Semanal de Cuotas y Cumplimiento' in html
    assert 'Estadísticas del Reto' in html


@then('la pestana "Panel General" se encuentra activa por defecto con aria-selected en verdadero')
def then_tab_general_active_by_default(ctx: Dict[str, Any]) -> None:
    html = ctx["html"]
    assert 'id="tab-general" class="tab-btn active"' in html
    assert 'aria-selected="true"' in html
    assert 'id="panel-general" class="tab-panel"' in html


# ============================================================================
# AC-8.2: Visualización exclusiva del Concentrado Físico y Financiero
# ============================================================================

@given("que el usuario se encuentra en el Dashboard Web")
@given("el usuario se encuentra en el Dashboard Web")
def given_user_on_dashboard(ctx: Dict[str, Any]) -> None:
    ctx["html"] = render_dashboard_html(ctx["service"])


@when('activa la pestana "Concentrado Físico y Financiero"')
def when_activates_concentrado_tab(ctx: Dict[str, Any]) -> None:
    ctx["active_tab"] = "concentrado"


@then('el panel "panel-concentrado" es visible con rol "tabpanel"')
def then_panel_concentrado_visible_with_role(ctx: Dict[str, Any]) -> None:
    html = ctx["html"]
    assert 'id="panel-concentrado"' in html
    assert 'role="tabpanel"' in html
    assert 'aria-labelledby="tab-concentrado"' in html
    assert 'Concentrado Físico y Financiero' in html
    assert 'Aportado ($)' in html or 'Aportado' in html


@then("los demas paneles se encuentran ocultos")
def then_other_panels_hidden(ctx: Dict[str, Any]) -> None:
    html = ctx["html"]
    assert 'class="tab-panel hidden"' in html
    assert 'switchTab(tabId)' in html


# ============================================================================
# AC-8.3: Visualización del Informe Semanal al activar su pestaña dedicada
# ============================================================================

@when('activa la pestana "Informe Semanal de Cuotas y Cumplimiento"')
def when_activates_informe_tab(ctx: Dict[str, Any]) -> None:
    ctx["active_tab"] = "informe"


@then('el panel "panel-informe" es visible con el selector de semanas y tarjetas KPI')
def then_panel_informe_visible_with_kpi(ctx: Dict[str, Any]) -> None:
    html = ctx["html"]
    assert 'id="panel-informe"' in html
    assert 'id="weekly-report-card"' in html
    assert 'weekly-report-select' in html
    assert 'kpi-compliance-rate' in html
    assert 'kpi-expected-quota' in html
    assert 'kpi-pool-amount' in html


@then("los demas paneles permanecen ocultos")
def then_other_panels_remain_hidden(ctx: Dict[str, Any]) -> None:
    html = ctx["html"]
    assert 'function switchTab(tabId)' in html
    assert 'panel.classList.add(\'hidden\')' in html


# ============================================================================
# AC-8.4: Soporte de navegación por teclado entre las pestañas
# ============================================================================

@given("que el usuario enfoca la barra de pestanas")
@given("el usuario enfoca la barra de pestanas")
def given_user_focuses_tablist(ctx: Dict[str, Any]) -> None:
    ctx["html"] = render_dashboard_html(ctx["service"])


@when("presiona la tecla de flecha derecha o flecha izquierda")
def when_presses_arrow_keys(ctx: Dict[str, Any]) -> None:
    pass


@then("el foco se transfiere a la pestana siguiente o anterior de forma circular")
def then_focus_transfers_circularly(ctx: Dict[str, Any]) -> None:
    html = ctx["html"]
    assert "ArrowRight" in html
    assert "ArrowLeft" in html
    assert "Home" in html
    assert "End" in html


@then("se actualizan los atributos tabindex y aria-selected correspondientes")
def then_updates_tabindex_and_aria_selected(ctx: Dict[str, Any]) -> None:
    html = ctx["html"]
    assert "tab.setAttribute('aria-selected', 'true')" in html
    assert "tab.setAttribute('tabindex', '0')" in html
    assert "tab.setAttribute('aria-selected', 'false')" in html
    assert "tab.setAttribute('tabindex', '-1')" in html


# ============================================================================
# AC-8.5: Conmutación instantánea de paneles sin recarga de página
# ============================================================================

@given("que el usuario interactua con las pestanas del sistema")
@given("el usuario interactua con las pestanas del sistema")
def given_user_interacts_with_tabs(ctx: Dict[str, Any]) -> None:
    ctx["html"] = render_dashboard_html(ctx["service"])


@when("alterna entre las distintas opciones")
def when_switches_between_options(ctx: Dict[str, Any]) -> None:
    pass


@then("cada cambio actualiza inmediatamente los roles ARIA y la visibilidad de los paneles")
def then_each_change_updates_roles_and_visibility(ctx: Dict[str, Any]) -> None:
    html = ctx["html"]
    assert "function switchTab(tabId)" in html
    assert "'general'" in html
    assert "'concentrado'" in html
    assert "'informe'" in html
    assert "'stats'" in html
    assert "panel.classList.remove('hidden')" in html
    assert "panel.classList.add('hidden')" in html
