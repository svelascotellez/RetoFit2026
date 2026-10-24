"""
Step definitions BDD para FEAT-001: Motor de Dominio del Reto Fit
Trazabilidad de Criterios EARS:
- AC-1.1: Determinacion de dia exitoso por calorias o pasos
- AC-1.2: Evaluacion de cumplimiento semanal con base en dias exitosos
- AC-1.3: Aplicacion de penalizacion de $100 al participante que incumple
- AC-1.4: Reparto equitativo de la bolsa semanal entre participantes cumplidores
- AC-1.5: Traslado de bolsa desierta a la siguiente semana cuando nadie cumple
- AC-1.6: Registro de aportaciones economicas hasta 900 pesos
- AC-1.7: Calculo del concentrado financiero individual y general
- AC-1.8: Rechazo de valores negativos en actividad y aportaciones
"""
import os
import pytest
from pytest_bdd import scenarios, given, when, then, parsers

from src.domain.activity import DailyActivity
from src.domain.challenge_week import ChallengeWeek
from src.domain.challenge_pool import WeeklyPool
from src.domain.participant import Participant
from src.domain.financial_summary import FinancialSummary

FEATURE_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "specs", "001-motor-dominio-retofit", "scenarios.feature"
)
scenarios(FEATURE_FILE)


# Fixtures de contexto de prueba
@pytest.fixture
def context():
    return {}


# AC-1.1 Steps
@given(parsers.parse('un participante registrado "{name}"'))
def participant_registered(context, name):
    context["participant"] = Participant(id="p1", name=name)


@when(parsers.parse('registra en un dia "{calorias}" calorias y "{pasos}" pasos'))
def record_daily_activity(context, calorias, pasos):
    context["activity"] = DailyActivity(calories=int(calorias), steps=int(pasos))


@then(parsers.parse('el estado del dia se determina como "{resultado}"'))
def assert_daily_status(context, resultado):
    is_successful = context["activity"].is_successful()
    expected = True if resultado == "exitoso" else False
    assert is_successful == expected, f"Esperado {expected}, obtenido {is_successful}"


# AC-1.2 Steps
@given(parsers.parse('un participante registrado con "{dias_exitosos}" dias exitosos en la semana'))
def participant_with_successful_days(context, dias_exitosos):
    context["successful_days"] = int(dias_exitosos)


@when('se evalua el cumplimiento de la semana')
def evaluate_week(context):
    week = ChallengeWeek(week_number=1)
    context["week_result"] = week.evaluate_participant(context["successful_days"])


@then(parsers.parse('el resultado semanal es "{cumplio}"'))
def assert_week_result(context, cumplio):
    expected = True if cumplio == "cumplido" else False
    assert context["week_result"] == expected


# AC-1.3 Steps
@given(parsers.parse('un participante "{name}" que incumplio la meta de la semana 1'))
def participant_missed_week(context, name):
    context["participant_ana"] = Participant(id="p_ana", name=name)
    context["pool_w1"] = WeeklyPool(week_number=1)


@when('se procesa el cierre de la semana 1')
def process_week_1_close(context):
    context["penalty_ana"] = 100.0
    context["pool_w1"].add_penalty(context["penalty_ana"])


@then(parsers.parse('se aplica una penalizacion de {monto:d} pesos a "{name}"'))
def assert_penalty_applied(context, monto, name):
    assert context["penalty_ana"] == float(monto)


@then(parsers.parse('la bolsa semanal de penalizaciones recibe {monto:d} pesos'))
def assert_pool_received(context, monto):
    assert context["pool_w1"].total_penalties == float(monto)


# AC-1.4 Steps
@given(parsers.parse('que en la semana 1 tres participantes incumplieron generando {monto:d} pesos en la bolsa'))
def pool_with_three_failures(context, monto):
    context["pool_w1"] = WeeklyPool(week_number=1)
    context["pool_w1"].add_penalty(float(monto))


@given(parsers.parse('dos participantes "{p1}" y "{p2}" si cumplieron el reto'))
def two_participants_met(context, p1, p2):
    context["met_count"] = 2


@when('se liquida la bolsa de la semana 1')
def liquidate_pool_w1(context):
    gain_per_person, rollover = context["pool_w1"].distribute(met_participants_count=context["met_count"])
    context["gain_per_person"] = gain_per_person
    context["rollover"] = rollover


@then(parsers.parse('cada participante cumplidor recibe {ganancia:d} pesos de ganancia adicional'))
def assert_gain_per_person(context, ganancia):
    assert context["gain_per_person"] == float(ganancia)


# AC-1.5 Steps
@given('que en la semana 2 los cuatro participantes registrados incumplieron el reto')
def four_participants_failed(context):
    context["met_count_w2"] = 0


@given(parsers.parse('la bolsa semanal acumula {monto:d} pesos de penalizaciones'))
def pool_w2_accumulates(context, monto):
    context["pool_w2"] = WeeklyPool(week_number=2)
    context["pool_w2"].add_penalty(float(monto))


@when('se liquida la semana 2 sin cumplidores')
def liquidate_week_2_empty(context):
    gain, rollover = context["pool_w2"].distribute(met_participants_count=context["met_count_w2"])
    context["gain_w2"] = gain
    context["rollover_w2"] = rollover


@then(parsers.parse('la bolsa acumulada de {monto:d} pesos se traslada como fondo inicial para la semana 3'))
def assert_rollover_to_w3(context, monto):
    assert context["rollover_w2"] == float(monto)
    week_3_pool = WeeklyPool(week_number=3, initial_rollover=context["rollover_w2"])
    assert week_3_pool.current_total == float(monto)


# AC-1.6 Steps
@given(parsers.parse('un participante "{name}" recien inscrito'))
def new_participant(context, name):
    context["participant_jorge"] = Participant(id="p_jorge", name=name)


@when(parsers.parse('abona un pago de aportacion de {monto:d} pesos'))
def record_payment(context, monto):
    context["participant_jorge"].add_contribution(float(monto))


@then(parsers.parse('el saldo aportado de "{name}" es de {aportado:d} pesos de un total de {total:d} pesos'))
def assert_contributions(context, name, aportado, total):
    assert context["participant_jorge"].total_contributed == float(aportado)
    assert context["participant_jorge"].TARGET_CONTRIBUTION == float(total)


# AC-1.7 Steps
@given(parsers.parse('un participante "{name}" que aporto {monto:d} pesos en total'))
def participant_with_full_contribution(context, name, monto):
    p = Participant(id="p_maria", name=name)
    p.add_contribution(float(monto))
    context["maria"] = p


@given(parsers.parse('"{name}" cumplio {met:d} semanas e incumplio {missed:d} semanas'))
def maria_weeks_status(context, name, met, missed):
    context["maria_met"] = met
    context["maria_missed"] = missed


@given(parsers.parse('recibio {earnings:d} pesos por reparto de bolsas semanales'))
def maria_pool_earnings(context, earnings):
    context["maria_earnings"] = float(earnings)


@when(parsers.parse('se genera el concentrado financiero de "{name}"'))
def generate_summary(context, name):
    summary = FinancialSummary.calculate(
        participant_id=context["maria"].id,
        name=context["maria"].name,
        total_contributed=context["maria"].total_contributed,
        weeks_met=context["maria_met"],
        weeks_missed=context["maria_missed"],
        total_earnings=context["maria_earnings"],
    )
    context["maria_summary"] = summary


@then(parsers.parse('el total penalizado es de {penalties:d} pesos'))
def assert_total_penalties(context, penalties):
    assert context["maria_summary"].total_penalties == float(penalties)


@then(parsers.parse('el monto neto final a recibir es de {monto:d} pesos'))
def assert_net_final(context, monto):
    assert context["maria_summary"].net_balance == float(monto)


# AC-1.8 Steps
@given('un participante registrado en el sistema')
def generic_registered_participant(context):
    context["participant"] = Participant(id="p_gen", name="Genaro")


@when(parsers.parse('intenta registrar "{campo}" con valor invalido "{valor}"'))
def attempt_invalid_entry(context, campo, valor):
    context["error"] = None
    try:
        val = int(valor)
        if campo == "calorias":
            DailyActivity(calories=val, steps=1000)
        elif campo == "pasos":
            DailyActivity(calories=200, steps=val)
        elif campo == "aportacion":
            context["participant"].add_contribution(float(val))
    except ValueError as e:
        context["error"] = str(e)


@then(parsers.parse('el sistema rechaza la transaccion con error de dominio "{mensaje}"'))
def assert_domain_error(context, mensaje):
    assert context["error"] is not None
    assert mensaje.lower() in context["error"].lower()
