# Guia de Usuario: FEAT-002 - Interfaz Web y API FastAPI para Reto Fit

## 1. Descripcion General
La **Interfaz Web y API FastAPI para Reto Fit** proporciona una plataforma completa, moderna y accesible para gestionar tanto el seguimiento físico como el control financiero del evento "Reto Fit 2026" de la DIDT (19 de octubre al 20 de diciembre de 2026). 

Esta funcionalidad integra:
- **Dashboard Web Interactivo**: Diseñado bajo el arquetipo *Fitness Dark Mode & Energy Neon* con tarjetas Bento Grid responsivas, micro-interacciones fluidas, soporte de accesibilidad WCAG 2.1 AA y estado vacío accesible con rol semántico `status`.
- **API RESTful de Alto Rendimiento**: Endpoints en FastAPI con esquemas Pydantic V2 para registro de participantes, aportaciones quincenales hacia la cuota total de $1,000 MXN en 5 pagos de $200 (19 oct, 2 nov, 16 nov, 30 nov, 14 dic), registro de sesiones de actividad física diaria (>= 300 kcal o >= 10,000 pasos), cierre y liquidación semanal de bolsa con rollover automático, y consulta de concentrado en tiempo real.
- **Preparación para Despliegue en la Nube**: Configuración nativa para ejecución inmediata en **Railway.com** mediante Uvicorn con endpoint de monitoreo de salud `/health`.

---

## 2. Requisitos Previos y Configuracion

### Dependencias del Entorno
- **Python:** Versión 3.11 o superior.
- **Paquetes Requeridos:** `fastapi`, `uvicorn`, `pydantic`.

### Variables de Entorno (Opcionales)
- `PORT`: Puerto de escucha del servidor HTTP (por defecto `8010`, asignado automáticamente por Railway en producción).
- `HOST`: Dirección de enlace de red (por defecto `0.0.0.0`).

### Ejecucion Local
Para iniciar el servidor web y la API en su máquina local:
```powershell
python -m uvicorn src.main:app --host 0.0.0.0 --port 8010 --reload
```
O directamente ejecutando el script principal:
```powershell
python src/main.py
```
Una vez iniciado, acceda a:
- **Dashboard Web:** [http://localhost:8010/](http://localhost:8010/)
- **Documentación Interactiva Swagger / OpenAPI:** [http://localhost:8010/docs](http://localhost:8010/docs)
- **Especificación OpenAPI JSON:** [http://localhost:8010/openapi.json](http://localhost:8010/openapi.json)

### Despliegue en Railway.com
En Railway, configure el comando de inicio en la pestaña *Settings -> Deploy*:
```bash
uvicorn src.main:app --host 0.0.0.0 --port $PORT
```
Railway utilizará el endpoint `GET /health` como healthcheck de monitoreo continuo.

---

## 3. Instrucciones de Uso Paso a Paso

### Paso 1: Explorar el Dashboard Web y Estado Vacio
1. Abra su navegador web en `http://localhost:8000/`.
2. Si aún no hay participantes registrados, el sistema desplegará de forma automática la tarjeta de **Estado Vacío** con el atributo semántico `role="status"`, informando que no hay miembros inscritos y orientando al usuario a realizar el primer registro.
3. Se mostrará el calendario oficial con las **5 fechas de pago quincenal** de $200 MXN:
   - 19 de octubre
   - 2 de noviembre
   - 16 de noviembre
   - 30 de noviembre
   - 14 de diciembre

### Paso 2: Registrar Participantes
- **Vía Web:** Complete el formulario "Registrar Participante" ingresando el ID único (ej. `didt-01`) y el nombre completo (ej. `Ana Lopez`), y presione **Registrar**.
- **Vía API:** Envíe una petición `POST /api/participants` con el payload JSON:
  ```json
  {
    "id": "didt-01",
    "name": "Ana Lopez"
  }
  ```
  El servidor responderá con código `201 Created` y los datos del participante registrado.

### Paso 3: Registrar Aportaciones Economicas
- **Vía Web:** En la pestaña "Abonar Pago", seleccione el ID del participante e introduzca el monto del abono (ej. `$200.00`).
- **Vía API:** Envíe una petición `POST /api/payments` con:
  ```json
  {
    "participant_id": "didt-01",
    "amount": 200.0
  }
  ```
  El sistema valida que el monto sea positivo, que el participante exista y que no exceda el tope de $1,000 MXN en sus 5 quincenas, respondiendo con código `200 OK`.

### Paso 4: Registrar Actividad Fisica Diaria
- **Vía Web:** Ingrese el ID del participante, el número de semana (1 a 9), el día (1 a 7), y las calorías o pasos registrados.
- **Vía API:** Envíe una petición `POST /api/activity`:
  ```json
  {
    "participant_id": "didt-01",
    "week_number": 1,
    "day_number": 1,
    "calories": 320,
    "steps": 4500
  }
  ```
  El sistema responderá con código `200 OK` y el atributo `is_successful: true` (al superar las 300 kcal o 10,000 pasos).

### Paso 5: Cerrar y Liquidar la Semana del Reto
- **Vía Web:** Seleccione el número de semana a liquidar y presione **Liquidar Semana**.
- **Vía API:** Envíe una petición `POST /api/weeks/1/close`.
  El sistema evaluará quiénes lograron al menos 4 días exitosos:
  - Los incumplidores son penalizados con $100 MXN.
  - La bolsa acumulada se reparte equitativamente entre los cumplidores.
  - Si nadie cumple, el 100% de la bolsa se traslada (rollover) a la siguiente semana.

### Paso 6: Consultar el Concentrado General
- Acceda a `GET /api/summary` para obtener el desglose completo del estado del reto, total aportado global, fondo en bolsa, rollover y el balance individual neto de cada participante.

---

## 4. Ejemplos de Uso (cURL y Python)

### 4.1 Verificacion de Salud del Servicio (`GET /health`)
```bash
curl -X GET http://localhost:8010/health
```
**Respuesta esperada (200 OK):**
```json
{
  "status": "healthy"
}
```

### 4.2 Registro de Participante (`POST /api/participants`)
```bash
curl -X POST http://localhost:8010/api/participants \
  -H "Content-Type: application/json" \
  -d '{"id": "didt-01", "name": "Carlos Gomez"}'
```
**Respuesta esperada (201 Created):**
```json
{
  "id": "didt-01",
  "name": "Carlos Gomez",
  "total_contributed": 0.0,
  "successful_weeks": 0,
  "failed_weeks": 0,
  "total_penalties": 0.0,
  "total_pool_earnings": 0.0,
  "net_balance": 0.0
}
```

### 4.3 Abono de Pago Quincenal (`POST /api/payments`)
```bash
curl -X POST http://localhost:8010/api/payments \
  -H "Content-Type: application/json" \
  -d '{"participant_id": "didt-01", "amount": 200.0}'
```
**Respuesta esperada (200 OK):**
```json
{
  "participant_id": "didt-01",
  "amount_paid": 200.0,
  "total_contributed": 200.0,
  "status": "success"
}
```

### 4.4 Registro de Actividad (`POST /api/activity`)
```bash
curl -X POST http://localhost:8010/api/activity \
  -H "Content-Type: application/json" \
  -d '{"participant_id": "didt-01", "week_number": 1, "day_number": 1, "calories": 350, "steps": 5000}'
```
**Respuesta esperada (200 OK):**
```json
{
  "participant_id": "didt-01",
  "week_number": 1,
  "day_number": 1,
  "is_successful": true
}
```

### 4.5 Cierre y Liquidacion Semanal (`POST /api/weeks/1/close`)
```bash
curl -X POST http://localhost:8010/api/weeks/1/close
```
**Respuesta esperada (200 OK):**
```json
{
  "week_number": 1,
  "compliant_participants": ["didt-01"],
  "non_compliant_participants": ["didt-02"],
  "pool_collected": 100.0,
  "rollover_amount": 0.0,
  "payout_per_compliant": 100.0
}
```

### 4.6 Concentrado General (`GET /api/summary`)
```bash
curl -X GET http://localhost:8010/api/summary
```
**Respuesta esperada (200 OK):**
```json
{
  "total_participants": 2,
  "total_contributed_global": 400.0,
  "current_pool": 0.0,
  "rollover_pool": 0.0,
  "participants": [
    {
      "id": "didt-01",
      "name": "Carlos Gomez",
      "total_contributed": 200.0,
      "successful_weeks": 1,
      "failed_weeks": 0,
      "total_penalties": 0.0,
      "total_pool_earnings": 100.0,
      "net_balance": 300.0
    },
    {
      "id": "didt-02",
      "name": "Ana Perez",
      "total_contributed": 200.0,
      "successful_weeks": 0,
      "failed_weeks": 1,
      "total_penalties": 100.0,
      "total_pool_earnings": 0.0,
      "net_balance": 100.0
    }
  ]
}
```

---

## 5. Respuestas a Errores y Preguntas Frecuentes

| Codigo HTTP | Causa | Como Resolverlo |
| :--- | :--- | :--- |
| `400 Bad Request` | Monto de pago menor o igual a cero (`amount <= 0`). | Ingrese un monto positivo (ej. $200.00). |
| `400 Bad Request` | Calorías o pasos con valores negativos en registro de actividad. | Verifique los sensores de su dispositivo e ingrese valores >= 0. |
| `400 Bad Request` | Participante con ID duplicado al registrarse. | Verifique que el ID no haya sido registrado previamente por otro usuario. |
| `404 Not Found` | El `participant_id` especificado no existe en el sistema. | Registre primero al participante con `POST /api/participants`. |
| `404 Not Found` | Intento de liquidar una semana que no existe o participante sin semana iniciada. | Asegúrese de registrar actividad o inicializar la semana antes de su liquidación. |
| `422 Unprocessable Entity` | Formato JSON malformado o campos obligatorios faltantes. | Valide que el cuerpo de la petición cumpla con el esquema JSON indicado en Swagger (`/docs`). |
