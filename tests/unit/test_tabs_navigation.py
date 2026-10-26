"""
Pruebas Unitarias: Navegacion Modular por Pestanas del Dashboard Web (FEAT-008)
Criterios EARS: AC-8.1 a AC-8.5
"""
import pytest
from src.application.challenge_service import ChallengeService
from src.application.dto import RegisterParticipantDTO, RecordPaymentDTO
from src.presentation.web_views import render_dashboard_html


def test_ac_8_1_tabs_header_display():
    """AC-8.1: Despliegue de la barra superior con 4 pestañas accesibles y Panel General activo por defecto."""
    service = ChallengeService()
    html = render_dashboard_html(service)

    # Contenedor de lista de pestañas
    assert 'role="tablist"' in html
    assert 'aria-label="Navegación del Reto Fit"' in html

    # 4 Pestañas presentes
    assert 'id="tab-general"' in html
    assert 'Panel General' in html
    assert 'id="tab-concentrado"' in html
    assert 'Concentrado Físico y Financiero' in html
    assert 'id="tab-informe"' in html
    assert 'Informe Semanal de Cuotas y Cumplimiento' in html
    assert 'id="tab-stats"' in html
    assert 'Estadísticas del Reto' in html

    # Estado inicial: Panel General activo
    assert 'aria-selected="true"' in html
    assert 'aria-controls="panel-general"' in html
    assert 'aria-controls="panel-concentrado"' in html
    assert 'aria-controls="panel-informe"' in html
    assert 'aria-controls="panel-stats"' in html


def test_ac_8_2_concentrado_tab_panel():
    """AC-8.2: Panel dedicado e independiente para el Concentrado Físico y Financiero."""
    service = ChallengeService()
    service.register_participant(RegisterParticipantDTO(id="P1", name="Sofia"))
    service.record_payment(RecordPaymentDTO(participant_id="P1", amount=200.0))

    html = render_dashboard_html(service)

    assert 'id="panel-concentrado"' in html
    assert 'role="tabpanel"' in html
    assert 'aria-labelledby="tab-concentrado"' in html
    assert 'Concentrado Físico y Financiero' in html
    assert 'Sofia' in html
    assert '$200.00' in html


def test_ac_8_3_informe_semanal_tab_panel():
    """AC-8.3: Panel dedicado e independiente para el Informe Semanal de Cuotas y Cumplimiento."""
    service = ChallengeService()
    service.register_participant(RegisterParticipantDTO(id="P1", name="Sofia"))

    html = render_dashboard_html(service)

    assert 'id="panel-informe"' in html
    assert 'role="tabpanel"' in html
    assert 'aria-labelledby="tab-informe"' in html
    assert 'id="weekly-report-select"' in html
    assert 'Informe Semanal de Cuotas y Cumplimiento' in html


def test_ac_8_4_keyboard_navigation_between_tabs():
    """AC-8.4: Script interactivo con soporte de navegación circular por teclado."""
    service = ChallengeService()
    html = render_dashboard_html(service)

    assert 'ArrowRight' in html
    assert 'ArrowLeft' in html
    assert 'Home' in html
    assert 'End' in html
    assert 'tab-general' in html
    assert 'tab-concentrado' in html
    assert 'tab-informe' in html
    assert 'tab-stats' in html


def test_ac_8_5_instant_tab_switching_without_reload():
    """AC-8.5: Función switchTab para alternar de forma reactiva entre los 4 paneles."""
    service = ChallengeService()
    html = render_dashboard_html(service)

    assert 'function switchTab(tabId)' in html
    assert "'concentrado'" in html
    assert "'informe'" in html
    assert "'stats'" in html
    assert "'general'" in html
