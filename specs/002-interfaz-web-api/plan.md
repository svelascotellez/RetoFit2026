# Plan Tecnico de Implementacion: FEAT-002 - Interfaz Web y API FastAPI para Reto Fit

## 1. Diseno Arquitectonico (Clean Architecture)
- **Dominio (`src/domain/`)**: Reutiliza las entidades inmutables y reglas puras implementadas en FEAT-001 (`Participant`, `DailyActivity`, `ChallengeWeek`, `WeeklyPool`, `FinancialSummary`).
- **Aplicacion (`src/application/`)**: Consume `ChallengeService` y los DTOs para orquestar la lógica de negocio sin acoplamiento con la web.
- **Infraestructura (`src/infrastructure/`)**: Instancia de servicio en memoria lista para su consumo.
- **Presentacion (`src/presentation/`)**:
  - `schemas.py`: Esquemas Pydantic V2 para validación estricta de payloads HTTP (`RegisterParticipantRequest`, `RecordPaymentRequest`, `RecordActivityRequest`, `WeeklySummaryResponse`, `ErrorResponse`).
  - `api.py`: Router FastAPI con los endpoints REST `/api/summary`, `/api/participants`, `/api/payments`, `/api/activity`, `/api/weeks/{week_number}/close` y `/health`.
  - `web_views.py`: Componente de presentación que genera la vista web interactiva (Single Page Dashboard) con CSS moderno, tarjetas Bento Grid y micro-interacciones.
- **Punto de Entrada (`src/main.py`)**:
  - Instancia `app = FastAPI(title="Reto Fit 2026 API & Web")`, monta los routers y sirve la vista web en `/`, listo para ejecutarse en Railway con `uvicorn src.main:app --host 0.0.0.0 --port $PORT`.

## 2. UI/UX Design System Specification (Design-System First)
- **Arquetipo Visual**: Fitness Dashboard Moderno / Dark Mode & Energy Neon (`fitness_dark_energy_neon`).
- **Paleta de Colores (design-tokens.json)**:
  - Fondo principal: `#0F172A` (Slate 900)
  - Superficie / Tarjetas Bento: `#1E293B` (Slate 800)
  - Bordes y divisores: `#334155` (Slate 700)
  - Primario (Cumplimiento/Éxito): `#10B981` (Emerald Green)
  - Secundario (Energía/Reto): `#F97316` (Vibrant Orange)
  - Acento Neón: `#06B6D4` (Cyan Neon)
  - Texto principal: `#F8FAFC` (Contraste 13.5:1 > WCAG 4.5:1)
  - Texto secundario: `#94A3B8` (Contraste 5.8:1 > WCAG 4.5:1)
  - Error: `#EF4444` (Red 500)
- **Tipografia**:
  - Títulos y Métricas: `Outfit, Inter, system-ui, sans-serif`
  - Números y Balances: `Fira Code, monospace`
- **Layout Bento Grid**:
  - Hero Widget: Bolsa acumulada actual y conteo de participantes.
  - Widget Calendario de Pagos: Las 5 quincenas programadas de $200 (19 oct, 2 nov, 16 nov, 30 nov, 14 dic).
  - Widget Registro Rápido: Formularios modales/tabs para registrar participante, abonar pago o cargar día de ejercicio.
  - Widget Concentrado de Participantes: Tabla responsiva con estado de cada miembro, días exitosos, aportación acumulada y balance final neto.
- **5 Estados Obligatorios**:
  - `default`: Visualización con datos en tarjetas con sombreado sutil.
  - `hover / focus`: Realce de borde con acento `#10B981` y escala suave (`transform: translateY(-2px)`).
  - `loading_skeleton`: Animación shimmer de carga para tarjetas mientras se sincronizan los datos.
  - `empty_state`: Vista cuando `total_participants == 0`, con rol ARIA semántico `status` y botón de llamada a la acción para registrar el primer participante.
  - `error_state`: Mensaje de alerta visual con icono de aviso y borde rojo `#EF4444`.
- **Accesibilidad**: WCAG 2.1 AA (navegación por teclado, atributos ARIA `role="status"`, `aria-live="polite"`).

## 3. Contratos y Esquemas
```python
class ParticipantCreateSchema(BaseModel):
    id: str = Field(min_length=1)
    name: str = Field(min_length=1)

class PaymentCreateSchema(BaseModel):
    participant_id: str
    amount: float = Field(gt=0)

class ActivityCreateSchema(BaseModel):
    participant_id: str
    week_number: int = Field(ge=1)
    day_of_week: int = Field(ge=1, le=7)
    calories: int = Field(ge=0)
    steps: int = Field(ge=0)

class HealthCheckResponse(BaseModel):
    status: str = "healthy"
```

## 4. Allowed Dependencies
- `fastapi`
- `uvicorn`
- `pydantic`
- `httpx`
- `pytest`
- `pytest-bdd`
- `mypy`

## 5. Matriz de Trazabilidad BDD / TDD
| Criterio EARS | Escenario Gherkin | Test Automatizado |
| :--- | :--- | :--- |
| `AC-2.1` | `@AC-2.1` Consulta del concentrado general mediante API REST | `test_ac_2_1_get_summary_endpoint` |
| `AC-2.2` | `@AC-2.2` Registro exitoso de un nuevo participante via API | `test_ac_2_2_register_participant_endpoint` |
| `AC-2.3` | `@AC-2.3` Registro de aportacion economica via API | `test_ac_2_3_record_payment_endpoint` |
| `AC-2.4` | `@AC-2.4` Registro de actividad fisica diaria via API | `test_ac_2_4_record_activity_endpoint` |
| `AC-2.5` | `@AC-2.5` Cierre y liquidacion semanal via API | `test_ac_2_5_close_week_endpoint` |
| `AC-2.6` | `@AC-2.6` Endpoint de verificacion de salud para Railway | `test_ac_2_6_healthcheck_endpoint` |
| `AC-2.7` | `@AC-2.7` Servir la aplicacion web interactiva en la ruta raiz | `test_ac_2_7_serve_web_dashboard` |
| `AC-2.8` | `@AC-2.8` Manejo de errores y validaciones en la API | `test_ac_2_8_error_handling_endpoints` |
| `AC-2.9` | `@AC-2.9` Estado vacio accesible cuando no hay participantes | `test_ac_2_9_empty_state_accessibility` |
