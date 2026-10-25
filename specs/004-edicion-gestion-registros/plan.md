# Plan Tecnico de Implementacion: FEAT-004

## 1. Diseno Arquitectonico (Clean Architecture)
- **Dominio (`src/domain/`)**:
  - `Participant`: Métodos de dominio para mutación controlada: `update_name(new_name: str)`, `remove_last_contribution() -> float`, `remove_activity(week_number: int, day_of_week: int) -> bool`.
- **Aplicacion (`src/application/`)**:
  - `ChallengeRepository` (Protocolo en `repository.py`):
    - `update_participant_name(participant_id: str, new_name: str) -> None`
    - `delete_participant(participant_id: str) -> None`
    - `delete_last_payment(participant_id: str) -> Optional[float]`
    - `delete_activity(participant_id: str, week_number: int, day_of_week: int) -> bool`
  - `ChallengeService` (`challenge_service.py`):
    - `update_participant_name(participant_id: str, new_name: str) -> Participant`
    - `delete_participant(participant_id: str) -> bool`
    - `delete_last_payment(participant_id: str) -> float`
    - `delete_daily_activity(participant_id: str, week_number: int, day_of_week: int) -> bool`
- **Infraestructura (`src/infrastructure/`)**:
  - `SQLiteChallengeRepository` (`sqlite_repository.py`):
    - Implementa operaciones SQL de actualización y borrado garantizando atomicidad y consistencia en `data/retofit.db`.
- **Presentacion (`src/presentation/`)**:
  - `api.py`:
    - `PUT /api/participants/{id}` (Actualizar nombre)
    - `DELETE /api/participants/{id}` (Eliminar participante en cascada)
    - `DELETE /api/participants/{id}/payments/last` (Anular último abono quincenal)
    - `DELETE /api/activities/{participant_id}/weeks/{week_number}/days/{day_of_week}` (Limpiar actividad)
  - `web_views.py`:
    - Botones de acción en la tabla general: `[✏️ Editar Nombre]`, `[🗑️ Eliminar]`, `[↩️ Anular Abono]`.
    - Modal accesible de confirmación con `role="dialog"`, `aria-modal="true"` y botones Cancelar/Confirmar.
    - Botón de restablecer actividad diaria en el panel de captura física.

## 2. UI/UX Design System Specification (Design-System First)
- **Arquetipo Visual**: Dark Mode Energy Neon / Bento Grid.
- **Tokens de Color y Tipografia**:
  - `--bg-primary: #0B0F17;`
  - `--accent-primary: #00FF87;`
  - `--color-danger: #FF3B30;` (Contraste 4.6:1 sobre fondo oscuro para acciones destructivas)
  - `--color-warning: #FF9500;`
- **Estados Obligatorios**: Default, Hover/Focus visible (outline 2px solid cyan/green), Loading/Processing, Empty State y Toast/Feedback con `role="status"`.
- **Accesibilidad**: WCAG 2.1 AA, navegación por teclado (`tabindex="0"`, soporte de tecla `Escape` en modales).

## 3. Contratos y Esquemas
- `UpdateParticipantDTO`:
  - `name: str` (no vacía, longitud 1 a 100 caracteres).
- Retornos estructurados JSON en API con mensajes de éxito y datos actualizados.

## 4. Allowed Dependencies
- `pydantic`
- `fastapi`
- `sqlite3`
- `pytest`
- `pytest-bdd`

## 5. Matriz de Trazabilidad BDD / TDD
| Criterio EARS | Escenario Gherkin | Test Automatizado |
| :--- | :--- | :--- |
| `AC-4.1` | `@AC-4.1` | `tests/unit/test_participant_management.py::test_update_participant_name_success` |
| `AC-4.2` | `@AC-4.2` | `tests/unit/test_participant_management.py::test_update_participant_name_invalid_raises_error` |
| `AC-4.3` | `@AC-4.3` | `tests/unit/test_participant_management.py::test_delete_participant_cascades` |
| `AC-4.4` | `@AC-4.4` | `tests/unit/test_participant_management.py::test_delete_last_payment` |
| `AC-4.5` | `@AC-4.5` | `tests/unit/test_participant_management.py::test_delete_activity` |
| `AC-4.6` | `@AC-4.6` | `tests/acceptance/test_record_management_steps.py::test_accessible_modal_interaction` |
