# Plan Tecnico de Implementacion: FEAT-006

## 1. Diseno Arquitectonico (Clean Architecture)
- **Dominio (`src/domain/`)**:
  - `src/domain/weekly_report.py`: Entidades inmutables `WeeklyParticipantReportItem` y `WeeklyReport`. Lógica pura de cálculo para cuotas acumuladas según el calendario oficial ($200 por quincena, $100 final en semana 9), días exitosos, meta física semanal ($\ge 4$ días), penalización semanal ($100 si incumple, $0 si cumple) y estatus financiero ("AL_CORRIENTE" vs "PENDIENTE"). Cero dependencias externas.
- **Aplicacion (`src/application/`)**:
  - `src/application/dto.py`: Declaración de `WeeklyParticipantReportDTO` y `WeeklyReportDTO`.
  - `src/application/challenge_service.py`: Método `get_weekly_report(week_number: int) -> WeeklyReportDTO` que valida el rango de semanas (1 a 9), consulta participantes, actividades y pools semanales, y orquesta la entidad de dominio.
- **Infraestructura (`src/infrastructure/`)**:
  - `src/infrastructure/sqlite_repository.py`: Reutilización transparente de los métodos de carga de estado y persistencia de actividades, abonos y cierres semanales.
- **Presentacion (`src/presentation/`)**:
  - `src/presentation/schemas.py`: Modelos Pydantic `WeeklyParticipantReportItem` y `WeeklyReportResponseSchema`.
  - `src/presentation/api.py`: Endpoint REST `GET /api/reports/weekly/{week_number}` con validación de semana 1-9 (400 Bad Request si inválida).
  - `src/presentation/web_views.py`: Componente visual Bento Grid con selector interactivo de semana (1 a 9), tarjetas KPI de resumen ejecutivo, tabla detallada con badges accesibles, indicador de carga y estado vacío accesible con rol "status".

## 2. UI/UX Design System Specification (Design-System First)
- **Arquetipo Visual**: Fitness Dark Mode con acentos Energy Neon (`#10B981`, `#06B6D4`, `#F97316`) y tarjetas Bento Grid sobre superficie `#1E293B`.
- **Tokens de Color y Tipografia**:
  - Tipografía: 'Outfit', Inter, sans-serif para títulos y texto; 'Fira Code' para métricas financieras y montos.
  - Paleta: `--bg-main: #0F172A`, `--surface: #1E293B`, `--border: #334155`, `--primary: #10B981`, `--neon-accent: #06B6D4`, `--secondary: #F97316`, `--error: #EF4444`.
- **Estados Obligatorios**:
  - Default: Selector activo, KPIs calculados y tabla detallada renderizada.
  - Hover/Focus: Micro-interacciones con borde resaltado (`--primary`) y contorno accesible.
  - Loading/Skeleton: Indicador visual mientras se realiza el fetch dinámico de la semana seleccionada.
  - Empty State: Contenedor semántico con `role="status"` y `aria-live="polite"` cuando no hay participantes o registros para la semana.
  - Error State: Toast/alerta accesible con borde rojo ante semanas fuera de rango.
- **Accesibilidad**: WCAG 2.1 AA (contraste $\ge 4.5:1$ en texto y $\ge 3:1$ en badges), etiquetas semánticas `aria-label`, foco visible y navegación por teclado en el selector.

## 3. Contratos y Esquemas
- `GET /api/reports/weekly/{week_number}`
  - Request: `week_number: int` (Path parameter, 1 <= week_number <= 9)
  - Response (200 OK): `WeeklyReportResponseSchema`
    - `week_number: int`
    - `total_participants: int`
    - `met_count: int`
    - `missed_count: int`
    - `compliance_rate: float`
    - `expected_contribution_per_participant: float`
    - `total_expected_funds: float`
    - `total_collected_funds: float`
    - `participants_up_to_date: int`
    - `participants_behind: int`
    - `is_closed: bool`
    - `pool_amount: float`
    - `gain_per_compliant: float`
    - `participants: List[WeeklyParticipantReportItem]`
      - `participant_id: str`
      - `name: str`
      - `successful_days: int`
      - `is_met: bool`
      - `total_contributed: float`
      - `expected_contribution: float`
      - `financial_status: str` ("AL_CORRIENTE" | "PENDIENTE")
      - `pending_amount: float`
      - `penalty: float`
      - `earnings: float`
      - `net_balance_impact: float`

## 4. Allowed Dependencies
Librerias externas de terceros autorizadas:
- `pydantic`
- `fastapi`
- `pytest`
- `pytest-bdd`

## 5. Matriz de Trazabilidad BDD / TDD
| Criterio EARS | Escenario Gherkin | Test Automatizado |
| :--- | :--- | :--- |
| `AC-6.1` | `@AC-6.1` | `test_ac_6_1_weekly_compliance_and_penalties` |
| `AC-6.2` | `@AC-6.2` | `test_ac_6_2_calendar_quotas_and_financial_status` |
| `AC-6.3` | `@AC-6.3` | `test_ac_6_3_invalid_week_rejection` |
| `AC-6.4` | `@AC-6.4` | `test_ac_6_4_rest_api_weekly_report` |
| `AC-6.5` | `@AC-6.5` | `test_ac_6_5_dashboard_interactive_section` |
| `AC-6.6` | `@AC-6.6` | `test_ac_6_6_accessible_empty_state` |
