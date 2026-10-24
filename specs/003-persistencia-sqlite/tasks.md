# Lista de Tareas Atomicas: FEAT-003 - Persistencia de Datos en SQLite para Reto Fit

- [x] `T-01`: [tests/acceptance/test_sqlite_persistence_steps.py] Implementar step definitions BDD para `@AC-3.1` a `@AC-3.6` basados en `scenarios.feature`. (Rojo)
- [x] `T-02`: [src/application/repository.py, tests/unit/test_sqlite_repository.py] Implementar interfaz de repositorio y tests unitarios de SQLite (`@AC-3.6`).
- [x] `T-03`: [src/infrastructure/sqlite_repository.py] Implementar `SQLiteChallengeRepository` con DDL y operaciones de persistencia (`@AC-3.1` a `@AC-3.4`, `@AC-3.6`).
- [x] `T-04`: [src/application/challenge_service.py] Adaptar `ChallengeService` para rehidratación y sincronización persistente (`@AC-3.5`).
- [x] `T-05`: [src/presentation/api.py, src/main.py] Inyectar `SQLiteChallengeRepository` en el punto de entrada FastAPI (`@AC-3.5`).
- [x] `T-06`: [docs/user_guide_003-persistencia-sqlite.md, harness] Redactar Guía de Usuario, ejecutar `.\harness\init.ps1` y auditar con `.\harness\spec-gate.ps1 -FeatureId 003-persistencia-sqlite`.
