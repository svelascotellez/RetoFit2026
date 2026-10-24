# Especificacion Funcional: FEAT-001 - Motor de Dominio del Reto Fit

## 1. Contexto e Historia de Usuario
Como Administrador y Participante del Reto Fit DIDT 2026,
Quiero registrar participantes, aportaciones económicas ($1,000 en 5 pagos quincenales de $200: 19 oct, 2 nov, 16 nov, 30 nov, 14 dic), registrar la actividad física diaria (calorías/pasos) y evaluar el cumplimiento semanal (mínimo 4 días de 300 kcal o 10k pasos),
Para calcular de manera automatizada las penalizaciones ($100 por incumplimiento), la distribución equitativa de la bolsa semanal entre los cumplidores y el concentrado de balance financiero final.

## 2. Criterios de Aceptacion (Sintaxis EARS)
- **AC-1.1**: CUANDO se registra la actividad diaria de un participante con calorías quemadas o pasos caminados, EL SISTEMA DEBE marcar el día como exitoso si las calorías son mayores o iguales a 300 o los pasos son mayores o iguales a 10,000.
- **AC-1.2**: CUANDO se evalúa el cumplimiento de una semana para un participante, EL SISTEMA DEBE registrar la semana como cumplida si el participante cuenta con al menos 4 días exitosos en esa semana, o incumplida si cuenta con menos de 4 días exitosos.
- **AC-1.3**: CUANDO un participante no cumple la meta semanal, EL SISTEMA DEBE deducir una penalización de $100 MXN de su asignación semanal y asignar ese importe a la bolsa semanal de penalizaciones.
- **AC-1.4**: CUANDO se liquida o cierra una semana con uno o más participantes cumplidores, EL SISTEMA DEBE repartir equitativamente el monto acumulado en la bolsa semanal entre todos los participantes que cumplieron en esa semana, redondeando a dos decimales.
- **AC-1.5**: SI ningún participante cumple la meta en una semana (cero cumplidores), EL SISTEMA DEBE trasladar (rollover) el total acumulado en la bolsa semanal hacia la bolsa de la semana siguiente.
- **AC-1.6**: CUANDO se registra un pago de aportación de un participante, EL SISTEMA DEBE registrar el abono hacia su cuota total de $1,000 MXN distribuida en 5 aportaciones quincenales de $200 (19 oct, 2 nov, 16 nov, 30 nov, 14 dic) y rechazar montos menores o iguales a cero.
- **AC-1.7**: MIENTRAS se consulta el concentrado individual o general, EL SISTEMA DEBE calcular en tiempo real: total aportado, semanas cumplidas, semanas incumplidas, total de penalizaciones descontadas, total de ganancias obtenidas de la bolsa y monto neto final a recibir (Total Aportado - Penalizaciones + Ganancias).
- **AC-1.8**: CUANDO se ingresan valores negativos en pasos, calorías o montos de aportación, EL SISTEMA DEBE rechazar la transacción retornando un error de validación de dominio.

## 3. Comportamientos Fuera de Alcance (Out of Scope)
- No se incluye sincronización automática directa con APIs de dispositivos vestibles (smartwatches, Apple Health, Garmin, Fitbit, Strava).
- No se incluye integración con pasarelas de pago bancarias o dispersión bancaria automatizada (Stripe, SPEI, Mercado Pago).
- No se incluyen notificaciones automáticas en tiempo real vía WhatsApp o SMS en esta funcionalidad.

## 4. Requisitos No Funcionales, UI/UX y Accesibilidad
- Tiempo de cálculo de liquidación semanal y concentrado general < 50 ms en memoria.
- Modelos de dominio inmutables o fuertemente tipados con dataclasses puras o Pydantic V2 sin dependencias externas en dominio.
- Arquitectura Limpia estricta: `src/domain` y `src/application` no deben tener acoplamiento con librerías web, bases de datos o frameworks.
- Cobertura de pruebas unitarias y de aceptación (BDD) del 100% de los criterios EARS AC-1.1 a AC-1.8.

## 5. Allowed Files
Rutas exactas autorizadas para creacion o modificacion durante esta funcionalidad:
- `src/domain/participant.py`
- `src/domain/activity.py`
- `src/domain/challenge_week.py`
- `src/domain/challenge_pool.py`
- `src/domain/financial_summary.py`
- `src/application/challenge_service.py`
- `src/application/dto.py`
- `tests/unit/test_participant.py`
- `tests/unit/test_activity.py`
- `tests/unit/test_challenge_week.py`
- `tests/unit/test_challenge_pool.py`
- `tests/unit/test_challenge_service.py`
- `tests/acceptance/test_challenge_steps.py`
