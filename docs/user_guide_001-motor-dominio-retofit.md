# Guia de Usuario: FEAT-001 - Motor de Dominio del Reto Fit

## 1. Descripcion General
El **Motor de Dominio del Reto Fit** es el núcleo de cálculo físico y financiero para el evento "Reto Fit" de la DIDT (19 de octubre al 20 de diciembre de 2026). Permite gestionar la lista de participantes, registrar sus aportaciones quincenales (hasta sumar $1,000 MXN en 5 pagos de $200 en las fechas: 19 oct, 2 nov, 16 nov, 30 nov, 14 dic), registrar sus sesiones diarias de ejercicio, evaluar automáticamente si cumplen el reto semanal (mínimo 4 días quemando 300 kcal o caminando 10,000 pasos), aplicar la penalización de $100 MXN a quienes incumplan, y liquidar equitativamente la bolsa semanal acumulada entre los participantes cumplidores (o trasladarla como fondo para la siguiente semana si nadie cumple).

---

## 2. Requisitos Previos y Reglas de Negocio
- **Entorno:** Python 3.11+ con dependencias de ejecución instaladas.
- **Aportaciones Económicas:** Cada participante aporta un total de **$1,000 MXN**, dividido en 5 pagos quincenales de **$200 MXN**:
  1. 19 de octubre
  2. 2 de noviembre
  3. 16 de noviembre
  4. 30 de noviembre
  5. 14 de diciembre
- **Regla Diaria de Ejercicio:** Un día se considera exitoso si el participante quema al menos **300 calorías** o camina al menos **10,000 pasos**.
- **Regla Semanal:** El participante debe acumular al menos **4 días exitosos** en la semana calendario para conservar su aportación semanal ($100 MXN).
- **Penalizaciones:** Si no alcanza los 4 días exitosos, se descuentan **$100 MXN** que se transfieren a la **bolsa semanal**.
- **Distribución de la Bolsa:** Los participantes que sí cumplieron esa semana reciben una parte equitativa del total de la bolsa.
- **Bolsa Desierta (Rollover):** Si en una semana ningún participante cumple la meta (0 cumplidores), la bolsa no se pierde: se acumula íntegramente a la bolsa de la siguiente semana.

---

## 3. Instrucciones de Uso Paso a Paso

### Paso 1: Registrar Participantes y sus Aportaciones
1. El Administrador registra a los miembros DIDT con su identificador único y nombre.
2. Se registran los abonos de las 5 aportaciones quincenales hasta cubrir el total de **$900 MXN**.

### Paso 2: Registrar Actividad Diaria
1. Por cada día de la semana (días 1 a 7), se ingresan las calorías quemadas y/o los pasos caminados.
2. El sistema determina de forma inmediata si el día fue exitoso.

### Paso 3: Cierre y Liquidación Semanal
1. Al finalizar la semana, el Administrador ejecuta el cierre semanal.
2. El sistema evalúa a todos los participantes registrados:
   - Identifica quiénes lograron 4 o más días exitosos (cumplidores) y quiénes tuvieron 3 o menos (incumplidores).
   - Cobra $100 MXN de penalización a cada participante que incumplió.
   - Si hay cumplidores, divide la bolsa acumulada equitativamente entre ellos y abona sus ganancias.
   - Si no hay cumplidores, transfiere el fondo acumulado a la semana siguiente.

### Paso 4: Consultar Concentrado y Balance Financiero
1. Se consulta el concentrado individual o general.
2. El sistema calcula en tiempo real:
   - **Total Aportado**
   - **Semanas Cumplidas** vs **Semanas Incumplidas**
   - **Total de Penalizaciones Descontadas**
   - **Total de Ganancias Obtenidas de la Bolsa**
   - **Monto Neto Final a Recibir** = `Total Aportado - Total Penalizaciones + Total Ganancias`

---

## 4. Ejemplos de Uso

### Ejemplo 1: Registro y Validación de Actividad Diaria
```python
from src.domain.activity import DailyActivity

# Ejemplo A: Cumple por calorías
act_cal = DailyActivity(calories=320, steps=3000)
assert act_cal.is_successful() is True

# Ejemplo B: Cumple por pasos
act_pasos = DailyActivity(calories=120, steps=10200)
assert act_pasos.is_successful() is True

# Ejemplo C: No alcanza el umbral
act_fail = DailyActivity(calories=250, steps=8000)
assert act_fail.is_successful() is False
```

### Ejemplo 2: Orquestación Completa con ChallengeService
```python
from src.application.challenge_service import ChallengeService
from src.application.dto import RegisterParticipantDTO, RecordPaymentDTO, RecordActivityDTO

service = ChallengeService()

# 1. Registrar participantes
service.register_participant(RegisterParticipantDTO(id="p1", name="María González"))
service.register_participant(RegisterParticipantDTO(id="p2", name="Carlos Soto"))

# 2. Aportaciones económicas ($1,000 en abonos quincenales de $200)
service.record_payment(RecordPaymentDTO(participant_id="p1", amount=1000.0))
service.record_payment(RecordPaymentDTO(participant_id="p2", amount=1000.0))

# 3. Registrar actividades de la Semana 1
# María entrena 4 días
for day in [1, 2, 3, 4]:
    service.record_daily_activity(
        RecordActivityDTO(participant_id="p1", week_number=1, day_of_week=day, calories=350, steps=2000)
    )

# Carlos entrena solo 2 días
for day in [1, 2]:
    service.record_daily_activity(
        RecordActivityDTO(participant_id="p2", week_number=1, day_of_week=day, calories=350, steps=2000)
    )

# 4. Liquidar Semana 1
cierre = service.close_and_liquidate_week(week_number=1)
print(f"Cumplidores: {cierre.met_count}, Incumplidores: {cierre.missed_count}")
print(f"Bolsa: ${cierre.pool_collected}, Ganancia por cumplidor: ${cierre.gain_per_participant}")
# Salida: Cumplidores: 1, Incumplidores: 1, Bolsa: $100.0, Ganancia por cumplidor: $100.0

# 5. Consultar balance financiero final de María
resumen_maria = service.get_participant_summary("p1")
print(f"Neto a recibir para María: ${resumen_maria.net_balance}")
# Salida: $1100.0 (Aportó $1000 - $0 penalización + $100 ganancia)
```

---

## 5. Respuestas a Errores y Preguntas Frecuentes

| Mensaje de Error / Comportamiento | Causa | Cómo Resolverlo |
| :--- | :--- | :--- |
| `Calorias no pueden ser negativas` | Se ingresó un valor menor a 0 en el campo de calorías quemadas. | Ingrese un entero mayor o igual a 0. |
| `Pasos no pueden ser negativos` | Se ingresó un valor menor a 0 en el conteo de pasos. | Ingrese un entero mayor o igual a 0. |
| `Monto debe ser mayor a cero` | Se intentó registrar una aportación con valor negativo o igual a $0. | Registre un monto positivo correspondiente al abono quincenal. |
| `Ya se ha registrado el maximo de 5 aportaciones` | El participante ya cuenta con sus 5 abonos registrados. | Verifique el historial de aportaciones del participante en el concentrado. |
| `Dias exitosos deben estar entre 0 y 7` | Se ingresó un número de días fuera del rango de una semana. | Ingrese un valor válido entre 0 y 7 días. |
| La bolsa muestra $0 de ganancia pero nadie cumplió | Cuando 0 participantes cumplen la meta semanal, nadie recibe incentivo esa semana. | El dinero se traslada automáticamente a la semana siguiente (`rollover_to_next`). |
