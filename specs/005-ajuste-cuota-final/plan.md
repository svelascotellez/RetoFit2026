# Plan Tecnico de Implementacion: FEAT-005

## 1. Diseno Arquitectonico (Clean Architecture)
- **Dominio (`src/domain/`)**:
  - `Participant`: Modificar `TARGET_CONTRIBUTION = 900.0`. Mantener `MAX_CONTRIBUTIONS = 5`.
- **Presentacion (`src/presentation/`)**:
  - `schemas.py`: Actualizar el valor por defecto `target_contribution: float = 900.0` en `ParticipantResponseSchema`, `PaymentResponseSchema` y `ParticipantSummaryItem`.
  - `web_views.py`:
    - Actualizar encabezados y columnas de tabla a `/ $900.00`.
    - Actualizar la tarjeta de métricas consolidadas ("Meta total: 4 quincenas de $200 + 1 semana de $100 = $900 por miembro").
    - Actualizar el calendario de fechas: 14 de diciembre con monto de $100.00.
    - Agregar botón de acción rápida `[+ $100]` en cada fila de participante junto al de `[+ $200]`.

## 2. UI/UX Design System Specification (Design-System First)
- **Arquetipo Visual**: Dark Mode Energy Neon / Bento Grid.
- **Tokens de Color y Tipografia**:
  - `--bg-main: #0F172A;`
  - `--surface: #1E293B;`
  - `--primary: #10B981;`
  - `--secondary: #F97316;`
- **Accesibilidad**: WCAG 2.1 AA, contraste de texto >= 4.5:1.

## 3. Contratos y Esquemas
- Esquemas de respuesta Pydantic con `target_contribution: float = 900.0`.

## 4. Allowed Dependencies
- `pydantic`
- `fastapi`
- `pytest`
- `pytest-bdd`

## 5. Matriz de Trazabilidad BDD / TDD
| Criterio EARS | Escenario Gherkin | Test Automatizado |
| :--- | :--- | :--- |
| `AC-5.1` | `@AC-5.1` | `tests/unit/test_participant_financial_target.py::test_target_contribution_default_900` |
| `AC-5.2` | `@AC-5.2` | `tests/unit/test_participant_financial_target.py::test_contributions_accumulate_to_900` |
| `AC-5.3` | `@AC-5.3` | `tests/acceptance/test_financial_quota_steps.py::test_dashboard_calendar_shows_900_and_december_100` |
| `AC-5.4` | `@AC-5.4` | `tests/acceptance/test_financial_quota_steps.py::test_quick_pay_buttons_available` |
| `AC-5.5` | `@AC-5.5` | `tests/acceptance/test_financial_quota_steps.py::test_api_schemas_reflect_900_target` |
