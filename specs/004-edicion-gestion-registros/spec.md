# Especificacion Funcional: FEAT-004 - Edicion y Gestion de Registros de Reto Fit

## 1. Contexto e Historia de Usuario
Como Administrador y Miembro del Reto Fit 2026 (DIDT)
Quiero poder corregir nombres de participantes, eliminar participantes dados de baja o creados por error, cancelar abonos monetarios erróneos y restablecer registros de actividad diaria incorrectos
Para mantener la veracidad contable de los fondos recolectados, evitar penalizaciones o ganancias injustificadas y contar con un panel de control flexible y seguro frente a errores de captura.

## 2. Criterios de Aceptacion (Sintaxis EARS)
- **AC-4.1**: CUANDO el usuario solicita actualizar el nombre de un participante registrado con un nombre válido (no vacío), EL SISTEMA DEBE actualizar el nombre del participante en memoria y en la base de datos SQLite y retornar el participante actualizado con código HTTP 200.
- **AC-4.2**: CUANDO el usuario solicita actualizar el nombre de un participante con una cadena vacía o espacios en blanco, EL SISTEMA DEBE rechazar la actualización con código HTTP 422 y mantener el nombre inalterado.
- **AC-4.3**: CUANDO el usuario solicita eliminar un participante existente, EL SISTEMA DEBE eliminar al participante y en cascada sus pagos y actividades registradas de SQLite y memoria, recalculando el concentrado global y retornando código HTTP 200.
- **AC-4.4**: CUANDO el usuario solicita eliminar/anular un abono quincenal de un participante existente, EL SISTEMA DEBE remover el registro de pago de SQLite y de memoria, decrementar el total acumulado y liberar el contador de quincenas abonadas para permitir capturas futuras.
- **AC-4.5**: CUANDO el usuario solicita restablecer o eliminar el registro de actividad física de un participante para una semana y día específicos, EL SISTEMA DEBE remover dicho registro de SQLite y de memoria, dejando el día en estado sin registrar y recalculando los días exitosos semanales.
- **AC-4.6**: MIENTRAS el usuario opera en el Dashboard Web, EL SISTEMA DEBE exigir confirmación explícita antes de ejecutar borrados irreversibles (participantes o abonos) y presentar alertas accesibles con rol "status" y botones con foco visible.

## 3. Comportamientos Fuera de Alcance (Out of Scope)
- No se incluye la modificación retroactiva de semanas ya cerradas y liquidadas financieramente (`weekly_closes`), para garantizar la inmutabilidad de bolsas previamente pagadas a los ganadores.
- No se incluye un sistema complejo de autenticación multi-rol o permisos RBAC (se mantiene como herramienta colaborativa interna de confianza para el equipo DIDT).
- No se incluye la modificación del identificador inmutable (`id`) de un participante (si se erró el ID, se debe eliminar y volver a registrar).

## 4. Requisitos No Funcionales, UI/UX y Accesibilidad
- Tiempo de respuesta de endpoints de edición y borrado < 150 ms.
- Persistencia atómica e íntegra en SQLite (`PRAGMA foreign_keys = ON;`, transacciones consistentes con `ON DELETE CASCADE`).
- Contraste visual accesible WCAG 2.1 AA (mínimo 4.5:1 para textos y 3:1 para botones de acción destructiva con tokens `--color-danger`).
- Diálogos modales o confirmaciones integradas accesibles con atributos ARIA (`role="dialog"`, `aria-modal="true"`, `aria-labelledby`).
- Estados de interfaz obligatorios: default, loading/processing, empty y feedback/toast accesible (`role="status"`).

## 5. Allowed Files
Rutas exactas autorizadas para creacion o modificacion durante esta funcionalidad:
- `src/domain/participant.py`
- `src/application/repository.py`
- `src/application/challenge_service.py`
- `src/infrastructure/sqlite_repository.py`
- `src/presentation/api.py`
- `src/presentation/web_views.py`
- `tests/unit/test_participant_management.py`
- `tests/unit/test_sqlite_repository.py`
- `tests/acceptance/test_record_management_steps.py`

