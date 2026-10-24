# Plan Tecnico de Implementacion: FEAT-003 - Persistencia de Datos en SQLite para Reto Fit

## 1. Diseno Arquitectonico (Clean Architecture)
- **Dominio (`src/domain/`)**: Inalterado e independiente de bases de datos. Entidades puras `Participant`, `DailyActivity`, `ChallengeWeek`, `WeeklyPool`.
- **Aplicacion (`src/application/`)**:
  - `repository.py`: Interfaz abstracta `ChallengeRepository` (Protocol) con métodos para persistir participantes, pagos, actividades y cierres semanales.
  - `challenge_service.py`: Adaptado para recibir opcionalmente una instancia de `ChallengeRepository`. Si se proporciona, persiste cada evento y rehidrata el estado en memoria durante `__init__`.
- **Infraestructura (`src/infrastructure/`)**:
  - `sqlite_repository.py`: Implementación concreta `SQLiteChallengeRepository` utilizando `sqlite3` estándar con transacciones atómicas, creación automática del esquema DDL y métodos de consulta/escritura.
- **Presentacion (`src/presentation/` & `src/main.py`)**:
  - Composición de dependencias: Inicializa `SQLiteChallengeRepository(db_path="data/retofit.db")` y lo inyecta a `ChallengeService`.
  - Los endpoints HTTP y vistas web consumen el servicio persistente de forma transparente.

## 2. UI/UX Design System Specification (Design-System First)
- **Consistencia Visual**: Mantiene el arquetipo Fitness Dark Mode & Energy Neon (`fitness_dark_energy_neon`) y tarjetas Bento Grid de acuerdo con `.specify/design-system/design-tokens.json`.
- **Indicador de Persistencia**: Las tarjetas web continúan operando con los estilos definidos, y el badge de estado en el header (`role="status"`) refleja el estado activo con persistencia local en SQLite.
- **Accesibilidad**: WCAG 2.1 AA preservada en todas las respuestas visuales.

## 3. Esquema de Base de Datos SQLite (`data/retofit.db`)
Tablas DDL:
1. `participants`: `(id TEXT PRIMARY KEY, name TEXT NOT NULL, created_at TEXT NOT NULL)`
2. `payments`: `(id INTEGER PRIMARY KEY AUTOINCREMENT, participant_id TEXT NOT NULL, amount REAL NOT NULL, created_at TEXT NOT NULL, FOREIGN KEY (participant_id) REFERENCES participants(id))`
3. `activities`: `(id INTEGER PRIMARY KEY AUTOINCREMENT, participant_id TEXT NOT NULL, week_number INTEGER NOT NULL, day_of_week INTEGER NOT NULL, calories INTEGER NOT NULL, steps INTEGER NOT NULL, is_successful INTEGER NOT NULL, created_at TEXT NOT NULL, UNIQUE(participant_id, week_number, day_of_week), FOREIGN KEY (participant_id) REFERENCES participants(id))`
4. `weekly_closes`: `(week_number INTEGER PRIMARY KEY, compliant_participants TEXT NOT NULL, non_compliant_participants TEXT NOT NULL, pool_collected REAL NOT NULL, rollover_amount REAL NOT NULL, payout_per_compliant REAL NOT NULL, closed_at TEXT NOT NULL)`
5. `rollover_state`: `(id INTEGER PRIMARY KEY CHECK (id = 1), current_rollover REAL NOT NULL)`

## 4. Estrategia de Rehidratacion
Al instanciar `ChallengeService(repository=sqlite_repo)`:
1. Recupera todos los participantes y sus pagos para restaurar `total_contributed`.
2. Recupera todas las actividades registradas agrupadas por participante y semana.
3. Recupera el historial de semanas cerradas y el balance actual de rollover.
4. El servicio queda en el mismo estado operativo en memoria que antes de reiniciar, garantizando lecturas a velocidad de memoria (< 5 ms) y escrituras persistidas en disco.
