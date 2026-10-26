# Especificacion Funcional: FEAT-006 - Informe Semanal de Cuotas y Cumplimiento del Reto

## 1. Contexto e Historia de Usuario
Como Administrador y Miembro del Reto Fit 2026 (DIDT)
Quiero generar y consultar un informe semanal integral de cuotas y cumplimiento físico por cada semana del reto (1 a 9)
Para auditar la recaudación de aportaciones contra el calendario oficial ($200 quincenales, $100 final en semana 9), detectar rezagos de pago, monitorear la tasa de cumplimiento físico (mínimo 4 días exitosos), calcular penalizaciones y visualizar la bolsa semanal acumulada de forma clara y accesible.

## 2. Criterios de Aceptacion (Sintaxis EARS)
- **AC-6.1**: CUANDO se solicita el informe de una semana válida (1 a 9), EL SISTEMA DEBE calcular por cada participante los días exitosos registrados (días con $\ge 300$ kcal o $\ge 10,000$ pasos), determinar si cumplió la meta física semanal ($\ge 4$ días exitosos), computar la penalización semanal ($100.00 MXN si incumplió, $0.00 MXN si cumplió) y calcular la ganancia asignada o estimada de la bolsa semanal.
- **AC-6.2**: CUANDO se calcula el informe semanal, EL SISTEMA DEBE determinar la cuota exigible acumulada según el calendario oficial ($200.00 para semanas 1-2, $400.00 para semanas 3-4, $600.00 para semanas 5-6, $800.00 para semanas 7-8 y $900.00 para semana 9), clasificando el estatus financiero de cada participante como "AL_CORRIENTE" (si total aportado $\ge$ cuota exigible) o "PENDIENTE" (si total aportado $<$ cuota exigible) e indicando el saldo pendiente.
- **AC-6.3**: CUANDO se solicita el informe semanal con un número de semana inválido (menor a 1 o mayor a 9), EL SISTEMA DEBE rechazar la solicitud retornando un error de validación (HTTP 400 Bad Request).
- **AC-6.4**: MIENTRAS se consulta el endpoint REST de la API `/api/reports/weekly/{week_number}`, EL SISTEMA DEBE responder con el consolidado semanal que incluye KPIs ejecutivos (tasa de cumplimiento, participantes cumplidores vs incumplidores, fondos recaudados vs exigibles, bolsa recolectada, estatus de liquidación) y la lista detallada de participantes.
- **AC-6.5**: MIENTRAS el usuario interactúa con el Dashboard Web, EL SISTEMA DEBE renderizar una sección interactiva de informe semanal con selector de semana (1 a 9), tarjetas Bento de métricas clave (tasa de cumplimiento %, fondos, bolsa), tabla detallada por participante con badges accesibles y cumplimiento estricto de contraste WCAG 2.1 AA.
- **AC-6.6**: SI no existen participantes registrados o no hay actividad en la semana seleccionada, EL SISTEMA DEBE desplegar un estado vacío accesible con rol semántico "status", indicando que no hay datos disponibles sin generar errores de ejecución.

## 3. Comportamientos Fuera de Alcance (Out of Scope)
- No se modifican las reglas base de cumplimiento (300 kcal o 10,000 pasos en al menos 4 días).
- No se modifican las penalizaciones fijas ($100 por semana incumplida).
- No se realiza cobro automático ni pasarela de pagos electrónicos externa.
- No se permite seleccionar semanas fuera del rango oficial del reto (semanas 1 a 9).

## 4. Requisitos No Funcionales, UI/UX y Accesibilidad
- Tiempo de respuesta del endpoint de reporte < 150 ms en memoria / SQLite.
- Contraste visual mínimo WCAG 2.1 AA (4.5:1 para texto normal, 3:1 para badges y controles).
- Navegación por teclado completa en el selector de semanas y tablas.
- Estados de interfaz obligatorios: default (datos cargados), loading (skeleton/indicador), empty_state (sin participantes o datos) y error_state (semana inválida).

## 5. Allowed Files
Rutas exactas autorizadas para creacion o modificacion durante esta funcionalidad:
- `src/domain/weekly_report.py`
- `src/application/dto.py`
- `src/application/challenge_service.py`
- `src/presentation/schemas.py`
- `src/presentation/api.py`
- `src/presentation/web_views.py`
- `tests/unit/test_weekly_report.py`
- `tests/acceptance/test_weekly_report_steps.py`
