# Plan Tecnico de Implementacion: FEAT-001 - Motor de Dominio del Reto Fit

## 1. Diseno Arquitectonico (Clean Architecture)
- **Dominio (`src/domain/`)**:
  - `activity.py`: Value Object `DailyActivity` que valida calorías (>= 0), pasos (>= 0) y determina si el día es exitoso (`calories >= 300 or steps >= 10_000`).
  - `participant.py`: Entidad `Participant` que encapsula ID, nombre, aportaciones registradas (máximo 5 abonos sumando $900) y registro de actividades diarias por semana.
  - `challenge_week.py`: Entidad `ChallengeWeek` que evalúa si un participante cumplió la semana (>= 4 días exitosos) y gestiona los participantes cumplidores e incumplidores.
  - `challenge_pool.py`: Entidad `WeeklyPool` que gestiona las penalizaciones de $100 por participante incumplido, calcula el fondo total y el reparto equitativo entre participantes cumplidores (o rollover acumulativo si no hay cumplidores).
  - `financial_summary.py`: Value Object / DTO de dominio `FinancialSummary` que calcula: total aportado, semanas cumplidas, semanas incumplidas, penalizaciones totales, ganancias por bolsa y balance neto final (`aportado - penalizaciones + ganancias`).
- **Aplicacion (`src/application/`)**:
  - `dto.py`: Modelos de transferencia de datos inmutables para registro de participantes, registro de actividad diaria, aportaciones económicas y reportes concentrados.
  - `challenge_service.py`: Servicio de aplicación `ChallengeService` que orquesta el ciclo de vida del reto: registro de participantes, registro de actividades, cierre y liquidación de semanas y generación de concentrados.
- **Infraestructura (`src/infrastructure/`)**:
  - Repositorio en memoria (`InMemoryParticipantRepository`, `InMemoryChallengeRepository`) para persistencia desacoplada de la lógica de negocio.
- **Presentacion (`src/presentation/`)**:
  - N/A para FEAT-001 (capa de dominio y casos de uso puro; la UI web se desarrollará e integrará en la siguiente feature sobre FastAPI).

## 2. UI/UX Design System Specification (Design-System First)
- **Arquetipo Visual**: Fitness Dashboard Moderno / Dark Mode & Energy Neon (`fitness_dark_energy_neon`).
- **Tokens de Color y Tipografia**: Alineados con `.specify/design-system/design-tokens.json` (`primary: #10B981`, `secondary: #F97316`, `background: #0F172A`, `surface: #1E293B`, fuente Outfit / Inter).
- **Estados Obligatorios**: Default, Hover, Loading Skeleton, Empty State y Error State.
- **Accesibilidad**: WCAG 2.1 AA (contraste de texto >= 4.5:1, etiquetas y roles semánticos accesibles).

## 3. Contratos y Esquemas
```python
# Entradas
RegisterParticipantRequest(id: str, name: str)
RecordPaymentRequest(participant_id: str, amount: float)
RecordDailyActivityRequest(participant_id: str, week_number: int, day_of_week: int, calories: int, steps: int)

# Salidas
DailyActivityResult(day_of_week: int, calories: int, steps: int, is_successful: bool)
WeeklyEvaluationResult(week_number: int, successful_days: int, is_met: bool, penalty: float, pool_bonus: float)
ParticipantSummaryDTO(participant_id: str, name: str, total_paid: float, weeks_met: int, weeks_missed: int, total_penalties: float, total_earnings: float, net_balance: float)
```

## 4. Allowed Dependencies
Librerias externas de terceros autorizadas:
- `pydantic`
- `pytest`
- `pytest-bdd`
- `mypy`

## 5. Matriz de Trazabilidad BDD / TDD
| Criterio EARS | Escenario Gherkin | Test Automatizado |
| :--- | :--- | :--- |
| `AC-1.1` | `@AC-1.1` Determinacion de dia exitoso por calorias o pasos | `test_ac_1_1_daily_activity_success` |
| `AC-1.2` | `@AC-1.2` Evaluacion de cumplimiento semanal con base en dias exitosos | `test_ac_1_2_weekly_compliance_evaluation` |
| `AC-1.3` | `@AC-1.3` Aplicacion de penalizacion de $100 al participante que incumple | `test_ac_1_3_weekly_penalty_application` |
| `AC-1.4` | `@AC-1.4` Reparto equitativo de la bolsa semanal entre participantes cumplidores | `test_ac_1_4_weekly_pool_distribution` |
| `AC-1.5` | `@AC-1.5` Traslado de bolsa desierta a la siguiente semana cuando nadie cumple | `test_ac_1_5_rollover_empty_pool` |
| `AC-1.6` | `@AC-1.6` Registro de aportaciones economicas hasta 900 pesos | `test_ac_1_6_participant_contributions` |
| `AC-1.7` | `@AC-1.7` Calculo del concentrado financiero individual y general | `test_ac_1_7_financial_summary_calculation` |
| `AC-1.8` | `@AC-1.8` Rechazo de valores negativos en actividad y aportaciones | `test_ac_1_8_negative_values_rejected` |
