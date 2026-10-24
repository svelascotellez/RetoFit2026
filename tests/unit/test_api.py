"""
Pruebas unitarias para la API y Presentacion Web (AC-2.1 a AC-2.9)
"""
import pytest
from fastapi.testclient import TestClient
from src.main import app, get_service
from src.presentation.api import get_challenge_service
from src.application.challenge_service import ChallengeService


@pytest.fixture
def client():
    service = ChallengeService()
    app.dependency_overrides[get_challenge_service] = lambda: service
    app.dependency_overrides[get_service] = lambda: service
    test_client = TestClient(app)
    yield test_client
    app.dependency_overrides.clear()


def test_ac_2_1_get_summary_endpoint(client):
    # AC-2.1: Consulta del concentrado general mediante GET /api/summary
    res = client.get("/api/summary")
    assert res.status_code == 200
    data = res.json()
    assert data["total_participants"] == 0
    assert data["total_funds_collected"] == 0.0


def test_ac_2_2_register_participant_endpoint(client):
    # AC-2.2: Registro de participante via POST /api/participants
    res = client.post("/api/participants", json={"id": "p1", "name": "Sofia"})
    assert res.status_code == 201
    data = res.json()
    assert data["id"] == "p1"
    assert data["name"] == "Sofia"
    assert data["total_contributed"] == 0.0


def test_ac_2_3_record_payment_endpoint(client):
    # AC-2.3: Registro de aportacion economica de $200 (meta total $1,000)
    client.post("/api/participants", json={"id": "p1", "name": "Sofia"})
    res = client.post("/api/payments", json={"participant_id": "p1", "amount": 200.0})
    assert res.status_code == 200
    assert res.json()["total_contributed"] == 200.0


def test_ac_2_4_record_activity_endpoint(client):
    # AC-2.4: Registro de actividad fisica diaria (>= 300 kcal o >= 10,000 pasos es exitoso)
    client.post("/api/participants", json={"id": "p1", "name": "Sofia"})

    # Caso exitoso por calorias
    res_cal = client.post(
        "/api/activity",
        json={"participant_id": "p1", "week_number": 1, "day_of_week": 1, "calories": 350, "steps": 2000},
    )
    assert res_cal.status_code == 200
    assert res_cal.json()["is_successful"] is True

    # Caso no exitoso
    res_fail = client.post(
        "/api/activity",
        json={"participant_id": "p1", "week_number": 1, "day_of_week": 2, "calories": 150, "steps": 5000},
    )
    assert res_fail.status_code == 200
    assert res_fail.json()["is_successful"] is False


def test_ac_2_5_close_week_endpoint(client):
    # AC-2.5: Cierre y liquidacion semanal via POST /api/weeks/{week_number}/close
    client.post("/api/participants", json={"id": "p1", "name": "Sofia"})
    client.post("/api/participants", json={"id": "p2", "name": "Pedro"})

    # Sofia cumple 4 dias
    for d in range(1, 5):
        client.post(
            "/api/activity",
            json={"participant_id": "p1", "week_number": 1, "day_of_week": d, "calories": 300, "steps": 1000},
        )

    res = client.post("/api/weeks/1/close")
    assert res.status_code == 200
    data = res.json()
    assert data["met_count"] == 1
    assert data["missed_count"] == 1
    assert data["pool_collected"] == 100.0
    assert data["gain_per_participant"] == 100.0


def test_ac_2_6_healthcheck_endpoint(client):
    # AC-2.6: Endpoint GET /health para Railway
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"


def test_ac_2_7_serve_web_dashboard(client):
    # AC-2.7: Servir vista web interactiva en Dark Mode Energy Neon
    res = client.get("/")
    assert res.status_code == 200
    assert "<!DOCTYPE html>" in res.text
    assert "Reto Fit 2026" in res.text
    assert "19 Oct al 20 Dic" in res.text


def test_ac_2_8_error_handling_endpoints(client):
    # AC-2.8: Manejo de errores 404, 400 y 422
    # 404 participante no encontrado
    res_404 = client.post("/api/payments", json={"participant_id": "no_existe", "amount": 200.0})
    assert res_404.status_code == 404

    # 400 monto negativo
    client.post("/api/participants", json={"id": "p1", "name": "Sofia"})
    res_400 = client.post("/api/payments", json={"participant_id": "p1", "amount": -100.0})
    assert res_400.status_code == 422 or res_400.status_code == 400


def test_ac_2_9_empty_state_accessibility(client):
    # AC-2.9: Estado vacio accesible con rol status
    res = client.get("/")
    assert res.status_code == 200
    assert 'role="status"' in res.text
    assert "No hay participantes registrados" in res.text
