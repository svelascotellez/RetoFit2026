# Guia de Usuario: FEAT-006 - Informe Semanal de Cuotas y Cumplimiento del Reto

## 1. Descripcion General
El **Informe Semanal de Cuotas y Cumplimiento del Reto** permite a los organizadores y miembros de la DIDT auditar el avance físico y financiero semana por semana (de la semana 1 a la semana 9) dentro de **RetoFit2026**.

Esta herramienta integra en una sola vista:
- **Cumplimiento Físico Semanal**: Registro de días exitosos por participante (días con $\ge 300$ kcal quemadas o $\ge 10,000$ pasos caminados), dictaminando si se alcanzó la meta obligatoria de al menos 4 días exitosos a la semana.
- **Penalizaciones y Bolsa Semanal**: Cálculo automático de la penalización de $100.00 MXN para quienes no cumplan la meta física, acumulando la bolsa semanal e indicando las ganancias adicionales ganadas por los cumplidores.
- **Auditoría de Cuotas según el Calendario Oficial**: Comparación del monto acumulado aportado por cada miembro contra la cuota exigible al momento según el calendario oficial ($900.00 MXN en total):
  1. 19 de octubre (Semanas 1 y 2): $200.00 MXN
  2. 2 de noviembre (Semanas 3 y 4): $400.00 MXN
  3. 16 de noviembre (Semanas 5 y 6): $600.00 MXN
  4. 30 de noviembre (Semanas 7 y 8): $800.00 MXN
  5. 14 de diciembre (Semana 9 Final): $900.00 MXN
- **Estatus Financiero Inmediato**: Clasificación instantánea entre participantes **"Al corriente"** o con **"Saldo pendiente"** (mostrando el monto exacto por regularizar).

---

## 2. Requisitos Previos y Configuracion
- Tener la aplicación ejecutándose en local (`uvicorn src.main:app --reload`) o en el entorno desplegado en Railway.
- Contar con al menos un participante registrado en el sistema.
- Para consultar actividades y penalizaciones precisas, haber ingresado registros diarios mediante el formulario de actividades físicas o haber liquidado semanas anteriores.

---

## 3. Instrucciones de Uso Paso a Paso

### A. Consulta Interactiva desde el Dashboard Web
1. Abre el Dashboard Web en tu navegador (por ejemplo `http://localhost:8000/`).
2. Localiza la tarjeta Bento Grid **"📊 Informe Semanal de Cuotas y Cumplimiento"**.
3. En el selector desplegable de **Semana**, elige la semana que deseas auditar (Semana 1 a Semana 9).
4. El sistema actualizará de inmediato:
   - **Badge de Estado**: Muestra si la semana ya fue liquidada (`Semana Liquidada`) o si está en progreso (`Semana en Curso / Preliminar`).
   - **Tarjetas KPI Ejecutivas**: Tasa de cumplimiento físico global (%), cuota exigible acumulada por persona y bolsa de penalizaciones recolectada/estimada.
   - **Tabla Detallada**: Desglose por miembro con días logrados (ej. `4/7 días (Cumplió)`), total aportado vs cuota exigible, badge de estatus de cuota (`Al corriente` o `Pendiente: -$X.XX`), penalización y ganancia estimada.

### B. Consulta Automatizada mediante la API REST
Puedes consumir los datos del informe en formato JSON a través del endpoint dedicado:
- **Método**: `GET`
- **Ruta**: `/api/reports/weekly/{week_number}`
- **Parámetro**: `{week_number}`: Número entero entre 1 y 9.

---

## 4. Ejemplos de Uso

### Ejemplo 1: Consulta de Semana 1 vía API
**Petición:**
```http
GET /api/reports/weekly/1 HTTP/1.1
Host: localhost:8000
Accept: application/json
```

**Respuesta Exitosa (200 OK):**
```json
{
  "week_number": 1,
  "total_participants": 2,
  "met_count": 1,
  "missed_count": 1,
  "compliance_rate": 50.0,
  "expected_contribution_per_participant": 200.0,
  "total_expected_funds": 400.0,
  "total_collected_funds": 250.0,
  "participants_up_to_date": 1,
  "participants_behind": 1,
  "is_closed": false,
  "pool_amount": 100.0,
  "gain_per_compliant": 100.0,
  "participants": [
    {
      "participant_id": "DIDT-01",
      "name": "Mariana",
      "successful_days": 4,
      "is_met": true,
      "total_contributed": 200.0,
      "expected_contribution": 200.0,
      "financial_status": "AL_CORRIENTE",
      "pending_amount": 0.0,
      "penalty": 0.0,
      "earnings": 0.0,
      "net_balance_impact": 0.0
    },
    {
      "participant_id": "DIDT-02",
      "name": "Carlos",
      "successful_days": 2,
      "is_met": false,
      "total_contributed": 50.0,
      "expected_contribution": 200.0,
      "financial_status": "PENDIENTE",
      "pending_amount": 150.0,
      "penalty": 100.0,
      "earnings": 0.0,
      "net_balance_impact": -100.0
    }
  ]
}
```

---

## 5. Respuestas a Errores y Preguntas Frecuentes

| Mensaje de Error / Comportamiento | Causa | Como Resolverlo |
| :--- | :--- | :--- |
| `El numero de semana debe estar entre 1 y 9` (HTTP 400) | Se especificó un número de semana menor a 1 o mayor a 9. | El Reto Fit dura 9 semanas (19 oct - 20 dic 2026). Selecciona un valor válido de 1 a 9. |
| Estado vacío: `Sin datos de informe semanal` | Aún no hay ningún participante registrado en la plataforma. | Utiliza el formulario **"👤 Inscribir Miembro"** para agregar al primer integrante. |
| El estatus marca `Pendiente: -$100.00` a pesar de haber abonado | La cuota exigible acumulada aumenta con cada quincena del calendario. | Realiza el abono correspondiente mediante los botones rápidos `+ $200` o `+ $100` en la tabla general. |
