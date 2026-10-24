# Especificacion Funcional: FEAT-003 - Persistencia de Datos en SQLite para Reto Fit

## 1. Contexto e Historia de Usuario
Como Administrador y Participante del Reto Fit DIDT,
Quiero que todos los registros de miembros, aportaciones quincenales, actividades físicas diarias y liquidaciones semanales se almacenen de forma persistente en una base de datos local SQLite,
Para que la información nunca se pierda ante reinicios del servidor, recargas en caliente (`--reload`), cortes de energía o nuevos despliegues.

## 2. Criterios de Aceptacion (Sintaxis EARS)
- **AC-3.1**: CUANDO se registra un participante en el sistema, EL SISTEMA DEBE persistir de forma inmediata su identificador y nombre en la tabla correspondiente de SQLite.
- **AC-3.2**: CUANDO se registra una aportación económica hacia la cuota de $1,000 MXN, EL SISTEMA DEBE guardar el registro de la transacción con su monto y fecha en SQLite y actualizar el total aportado.
- **AC-3.3**: CUANDO se registra una sesión de actividad física diaria, EL SISTEMA DEBE almacenar el día, semana, calorías, pasos y resultado de éxito en SQLite.
- **AC-3.4**: CUANDO se liquida y cierra una semana del reto, EL SISTEMA DEBE guardar el resumen del cierre semanal (bolsa acumulada, cumplidores, incumplidores, rollover y ganancia por persona) en SQLite.
- **AC-3.5**: CUANDO el servidor o servicio se reinicia, EL SISTEMA DEBE rehidratar y restaurar automáticamente todo el estado histórico desde SQLite garantizando cero pérdida de datos.
- **AC-3.6**: MIENTRAS se inicia el sistema y no existe la base de datos en disco, EL SISTEMA DEBE inicializar automáticamente el esquema de tablas en SQLite en el directorio `data/retofit.db`.

## 3. Comportamientos Fuera de Alcance (Out of Scope)
- No se incluye migración hacia motores cliente-servidor externos (ej. PostgreSQL, MySQL, Oracle).
- No se incluye encriptación a nivel de columna ni replicación multi-región en esta versión.

## 4. Requisitos No Funcionales y Arquitectura
- Arquitectura Limpia: La capa de infraestructura implementa el patrón Repository (`SQLiteChallengeRepository`), manteniendo desacoplado el Dominio y la Aplicación.
- Motor de Almacenamiento: SQLite 3 nativo de Python (`sqlite3`) sin dependencias de ORMs pesados.
- Ruta por defecto de la base de datos: `data/retofit.db` (creada automáticamente si el directorio no existe).
- Transaccionalidad: Las operaciones de escritura deben ser atómicas (`commit` / `rollback`).

## 5. Allowed Files
Rutas exactas autorizadas para creacion o modificacion durante esta funcionalidad:
- `src/application/repository.py`
- `src/application/challenge_service.py`
- `src/infrastructure/sqlite_repository.py`
- `src/presentation/api.py`
- `src/main.py`
- `tests/unit/test_sqlite_repository.py`
- `tests/acceptance/test_sqlite_persistence_steps.py`
