# Especificacion Funcional: FEAT-005 - Ajuste de Cuota Financiera y Calendario de Aportaciones

## 1. Contexto e Historia de Usuario
Como Administrador y Miembro del Reto Fit 2026 (DIDT)
Quiero ajustar la cuota total de aportación a $900.00 MXN distribuida en 5 fechas oficiales (4 abonos de $200 y el abono final del 14 de diciembre de $100)
Para reflejar con exactitud que el reto consta de 9 semanas en total, donde las primeras 4 quincenas cubren 2 semanas cada una ($200 c/u) y el periodo final del 14 al 20 de diciembre cubre únicamente la semana 9 ($100).

## 2. Criterios de Aceptacion (Sintaxis EARS)
- **AC-5.1**: CUANDO un participante es registrado en el sistema, EL SISTEMA DEBE fijar su meta total de aportación en $900.00 MXN (`TARGET_CONTRIBUTION = 900.0`) y mantener el límite de hasta 5 aportaciones oficiales.
- **AC-5.2**: CUANDO se registran abonos económicos para un participante, EL SISTEMA DEBE acumularlos hacia la meta de $900.00 MXN y reflejar el progreso individual correspondiente.
- **AC-5.3**: MIENTRAS el usuario consulta el Dashboard Web, EL SISTEMA DEBE mostrar en el concentrado general y en la tarjeta de fechas el calendario oficial ajustado a $900.00 MXN:
  1. 19 de octubre: $200.00 (Semanas 1 y 2)
  2. 2 de noviembre: $200.00 (Semanas 3 y 4)
  3. 16 de noviembre: $200.00 (Semanas 5 y 6)
  4. 30 de noviembre: $200.00 (Semanas 7 y 8)
  5. 14 de diciembre: $100.00 (Semana 9 final)
- **AC-5.4**: CUANDO el usuario interactúa con la tabla de participantes en el Dashboard Web, EL SISTEMA DEBE ofrecer botones de acción rápida para abonar `+ $200` y `+ $100`.
- **AC-5.5**: MIENTRAS se consumen los endpoints REST de la API (`/api/participants`, `/api/payments`, `/api/summary`), EL SISTEMA DEBE retornar `target_contribution: 900.0` en los esquemas de respuesta.

## 3. Comportamientos Fuera de Alcance (Out of Scope)
- No se altera la regla de penalización semanal ($100 por semana incumplida con < 4 días exitosos).
- No se altera la meta física diaria (mínimo 300 kcal o 10,000 pasos en al menos 4 días por semana).
- No se modifican semanas pasadas ya liquidadas en SQLite.

## 4. Requisitos No Funcionales, UI/UX y Accesibilidad
- Contraste visual accesible WCAG 2.1 AA en todas las etiquetas y badges de aportación.
- Actualización sincronizada en memoria y en la base de datos persistente SQLite.
- Botones de acción rápida con etiquetas legibles y atributos `title` accesibles.

## 5. Allowed Files
Rutas exactas autorizadas para creacion o modificacion durante esta funcionalidad:
- `src/domain/participant.py`
- `src/presentation/schemas.py`
- `src/presentation/web_views.py`
- `tests/unit/test_participant_financial_target.py`
- `tests/acceptance/test_financial_quota_steps.py`
- `tests/unit/test_participant.py`
- `tests/acceptance/test_challenge_steps.py`
