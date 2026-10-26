# Plan Tecnico de Implementacion: FEAT-007

## 1. Diseno Arquitectonico (Clean Architecture)
- **Dominio (`src/domain/`)**:
  - `src/domain/challenge_stats.py`: Entidades inmutables `ParticipantRankingItem`, `WeeklyStatsTrendItem` y `GlobalStats`. Lógica pura de cálculo para totales globales (calorías, pasos, días exitosos, días de actividad), promedios diarios, ranking de participantes ordenado descendentemente por días exitosos con desempate secundario por calorías quemadas acumuladas, y tendencias semanales (semanas 1 a 9). Cero dependencias externas.
- **Aplicacion (`src/application/`)**:
  - `src/application/dto.py`: Declaración de DTOs inmutables `ParticipantRankingDTO`, `WeeklyStatsTrendDTO` y `GlobalStatsDTO`.
  - `src/application/challenge_service.py`: Método `get_global_statistics() -> GlobalStatsDTO` que agrega participantes, actividades físicas, abonos y pools cerrados, invocando la lógica de dominio para generar las estadísticas completas.
- **Infraestructura (`src/infrastructure/`)**:
  - `src/infrastructure/sqlite_repository.py`: Reutilización transparente de los repositorios existentes sin modificar esquemas ni realizar queries acopladas a la presentación.
- **Presentacion (`src/presentation/`)**:
  - `src/presentation/schemas.py`: Modelos Pydantic `ParticipantRankingSchema`, `WeeklyStatsTrendSchema` y `GlobalStatsResponseSchema`.
  - `src/presentation/api.py`: Endpoint REST `GET /api/statistics` que retorna el esquema consolidado con código HTTP 200.
  - `src/presentation/web_views.py`: Componente de navegación por pestañas (`role="tablist"`, `role="tab"`, `role="tabpanel"`) permitiendo conmutar entre "Panel General" y "Estadísticas del Reto", tarjetas KPI en Bento Grid con diseño fitness dark neon, tabla interactiva de podio y ranking, barras de tendencia semanal y contenedor de estado vacío accesible con `role="status"`.

## 2. UI/UX Design System Specification (Design-System First)
- **Arquetipo Visual**: Fitness Dark Mode Neon Dashboard (Bento Grid con acentos `#10B981`, `#06B6D4`, `#F97316` y `#EAB308` para el podio).
- **Tokens de Color y Tipografia**:
  - Tipografía: 'Outfit', Inter, sans-serif para títulos y etiquetas; 'Fira Code' para métricas numéricas y posiciones del ranking.
  - Paleta: `--bg-main: #0F172A`, `--surface: #1E293B`, `--border: #334155`, `--primary: #10B981`, `--neon-accent: #06B6D4`, `--podium-gold: #F59E0B`, `--podium-silver: #94A3B8`, `--podium-bronze: #D97706`.
- **Estados Obligatorios**:
  - Default: Pestaña activa con tarjetas KPI (calorías totales/promedio, pasos totales/promedio), podio visual y tabla de ranking, gráfico/barras de tendencias semanales.
  - Hover/Focus: Micro-interacciones con elevación sutil, borde iluminado y focus-visible accesible en tabs e items.
  - Loading/Skeleton: Indicador visual mientras se procesan los datos.
  - Empty State: Contenedor accesible con `role="status"` y `aria-live="polite"` cuando no hay actividades físicas registradas en el reto.
  - Error State: Mensaje claro en caso de falla de conexión o datos corruptos.
- **Accesibilidad**: WCAG 2.1 AA (contraste >= 4.5:1 en texto, >= 3:1 en gráficos y barras), soporte de teclado en pestañas (`ArrowLeft`, `ArrowRight`, `Home`, `End`), roles ARIA semánticos (`tablist`, `tab`, `tabpanel`, `aria-selected`, `aria-controls`).

## 3. Contratos y Esquemas
- `GET /api/statistics`
  - Response (200 OK): `GlobalStatsResponseSchema`
    - `total_calories: float`
    - `total_steps: int`
    - `total_successful_days: int`
    - `total_activity_days: int`
    - `average_daily_calories: float`
    - `average_daily_steps: float`
    - `total_participants: int`
    - `total_penalties: float`
    - `total_distributed_pool: float`
    - `ranking: List[ParticipantRankingSchema]`
      - `rank_position: int`
      - `participant_id: str`
      - `name: str`
      - `successful_days: int`
      - `total_calories: float`
      - `total_steps: int`
      - `is_podium: bool`
    - `weekly_trends: List[WeeklyStatsTrendSchema]`
      - `week_number: int`
      - `successful_days: int`
      - `compliant_participants: int`
      - `total_participants: int`
      - `compliance_rate: float`
      - `pool_amount: float`

## 4. Allowed Dependencies
Librerias externas de terceros autorizadas:
- `pydantic`
- `fastapi`
- `pytest`
- `pytest-bdd`

## 5. Matriz de Trazabilidad BDD / TDD
| Criterio EARS | Escenario Gherkin | Test Automatizado |
| :--- | :--- | :--- |
| `AC-7.1` | `@AC-7.1` | `test_ac_7_1_global_calories_and_steps_metrics` |
| `AC-7.2` | `@AC-7.2` | `test_ac_7_2_ranking_generation_with_tie_breaker` |
| `AC-7.3` | `@AC-7.3` | `test_ac_7_3_weekly_compliance_trends` |
| `AC-7.4` | `@AC-7.4` | `test_ac_7_4_rest_api_statistics_endpoint` |
| `AC-7.5` | `@AC-7.5` | `test_ac_7_5_accessible_tabs_navigation` |
| `AC-7.6` | `@AC-7.6` | `test_ac_7_6_accessible_empty_state_without_activities` |
