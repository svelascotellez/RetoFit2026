"""
Step definitions BDD para FEAT-002: Interfaz Web y API FastAPI para Reto Fit
Trazabilidad de Criterios EARS:
- AC-2.1: Consulta del concentrado general mediante API REST
- AC-2.2: Registro exitoso de un nuevo participante via API
- AC-2.3: Registro de aportacion economica via API
- AC-2.4: Registro de actividad fisica diaria via API
- AC-2.5: Cierre y liquidacion semanal via API
- AC-2.6: Endpoint de verificacion de salud para Railway
- AC-2.7: Servir la aplicacion web interactiva en la ruta raiz
- AC-2.8: Manejo de errores y validaciones en la API
- AC-2.9: Estado vacio accesible cuando no hay participantes registrados
"""
import json
import os
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from fastapi.testclient import TestClient

from src.main import app, get_service
from src.presentation.api import get_challenge_service
from src.application.challenge_service import ChallengeService
from src.application.dto import RegisterParticipantDTO, RecordPaymentDTO

FEATURE_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "specs", "002-interfaz-web-api", "scenarios.feature"
)
scenarios(FEATURE_FILE)


@pytest.fixture
def client():
    # Creamos un servicio limpio para cada escenario
    service = ChallengeService()
    app.dependency_overrides[get_challenge_service] = lambda: service
    app.dependency_overrides[get_service] = lambda: service
    test_client = TestClient(app)
    yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def context():
    return {}


# AC-2.1 Steps
@given('que el sistema tiene participantes registrados con aportaciones')
def system_has_participants_with_payments(client):
    client.post("/api/participants", json={"id": "p1", "name": "Maria"})
    client.post("/api/payments", json={"participant_id": "p1", "amount": 200.0})


@when('el cliente envia una solicitud GET a "/api/summary"')
def get_summary(client, context):
    context["response"] = client.get("/api/summary")


@then('la respuesta tiene codigo de estado 200')
def assert_status_200(context):
    assert context["response"].status_code == 200


@then(parsers.parse('el cuerpo contiene "{field1}" y "{field2}"'))
def assert_body_contains_fields(context, field1, field2):
    data = context["response"].json()
    assert field1 in data
    assert field2 in data


# AC-2.2 Steps
@given(parsers.parse('que no existe un participante con id "{pid}"'))
def participant_does_not_exist(pid):
    pass


@when(parsers.parse('el cliente envia una solicitud POST a "/api/participants" con id "{pid}" y nombre "{name}"'))
def create_participant_request(client, context, pid, name):
    context["response"] = client.post("/api/participants", json={"id": pid, "name": name})


@then('la respuesta tiene codigo de estado 201')
def assert_status_201(context):
    assert context["response"].status_code == 201


@then(parsers.parse('el cuerpo confirma el registro de "{name}"'))
def assert_body_confirms_name(context, name):
    data = context["response"].json()
    assert data["name"] == name


# AC-2.3 Steps
@given(parsers.parse('un participante existente con id "{pid}"'))
def existing_participant(client, pid):
    client.post("/api/participants", json={"id": pid, "name": "Participante Existente"})


@when(parsers.parse('el cliente envia una solicitud POST a "/api/payments" con monto {monto:d} para "{pid}"'))
def make_payment_request(client, context, monto, pid):
    context["response"] = client.post("/api/payments", json={"participant_id": pid, "amount": float(monto)})


@then(parsers.parse('el saldo aportado retornado es {saldo:d}'))
def assert_returned_balance(context, saldo):
    data = context["response"].json()
    assert data["total_contributed"] == float(saldo)


# AC-2.4 Steps
@when(parsers.parse('el cliente registra actividad en semana {week:d} dia {day:d} con "{calorias}" calorias y "{pasos}" pasos'))
def record_activity_request(client, context, week, day, calorias, pasos):
    context["response"] = client.post(
        "/api/activity",
        json={
            "participant_id": "p10",
            "week_number": week,
            "day_of_week": day,
            "calories": int(calorias),
            "steps": int(pasos),
        },
    )


@then(parsers.parse('la respuesta indica que el dia fue "{exitoso}"'))
def assert_activity_success(context, exitoso):
    data = context["response"].json()
    expected = True if exitoso == "true" else False
    assert data["is_successful"] == expected


# AC-2.5 Steps
@given('participantes registrados en la semana 1 con actividades evaluadas')
def setup_participants_week_1(client):
    client.post("/api/participants", json={"id": "p1", "name": "Ana"})
    client.post("/api/participants", json={"id": "p2", "name": "Beto"})
    # Ana cumple 4 dias
    for d in range(1, 5):
        client.post(
            "/api/activity",
            json={"participant_id": "p1", "week_number": 1, "day_of_week": d, "calories": 350, "steps": 2000},
        )


@when('el administrador envia una solicitud POST a "/api/weeks/1/close"')
def close_week_1(client, context):
    context["response"] = client.post("/api/weeks/1/close")


@then(parsers.parse('el cuerpo de la liquidacion contiene "{field1}" y "{field2}"'))
def assert_close_week_body(context, field1, field2):
    data = context["response"].json()
    assert field1 in data
    assert field2 in data


# AC-2.6 Steps
@given('que el servicio FastAPI esta en ejecucion')
def service_is_running():
    pass


@when('se solicita el estado de salud en "/health"')
def check_health(client, context):
    context["response"] = client.get("/health")


@then(parsers.parse('el estado reportado es "{status}"'))
def assert_health_status(context, status):
    data = context["response"].json()
    assert data["status"] == status


# AC-2.7 Steps
@given('que el servidor web esta activo')
def web_server_active():
    pass


@when('un usuario navega a la ruta "/"')
def navigate_root(client, context):
    context["response"] = client.get("/")


@then('contiene encabezados HTML con el diseno del Reto Fit')
def assert_html_headers(context):
    html = context["response"].text
    assert "<!DOCTYPE html>" in html
    assert "Reto Fit" in html


# AC-2.8 Steps
@given('que el servicio API esta disponible')
def api_available():
    pass


@when(parsers.parse('se envia una peticion invalida a "{endpoint}" con cuerpo "{payload}"'))
def send_invalid_request(client, context, endpoint, payload):
    data = json.loads(payload)
    context["response"] = client.post(endpoint, json=data)


@then(parsers.parse('la respuesta de error tiene codigo "{codigo_error}"'))
def assert_error_code(context, codigo_error):
    assert context["response"].status_code == int(codigo_error)


# AC-2.9 Steps
@given('que no hay participantes registrados en el sistema')
def no_registered_participants():
    pass


@when('se consulta la vista web principal')
def query_main_web_view(client, context):
    context["response"] = client.get("/")


@then(parsers.parse('se presenta un mensaje accesible con rol "{role}" indicando que no hay participantes'))
def assert_empty_state_accessible(context, role):
    html = context["response"].text
    assert f'role="{role}"' in html
    assert "No hay participantes registrados" in html
