# Lista de Tareas Atomicas: FEAT-004

- [x] `T-01`: [tests/acceptance/test_record_management_steps.py] Implementar step definitions BDD para `@AC-4.1` a `@AC-4.6`. (Rojo)
- [x] `T-02`: [src/domain/participant.py, tests/unit/test_participant_management.py] Implementar mutaciones de dominio `update_name`, `remove_last_contribution`, `remove_activity` y tests unitarios. (Verde)
- [x] `T-03`: [src/application/repository.py, src/infrastructure/sqlite_repository.py] Implementar métodos de persistencia para actualizar nombre, eliminar participante, anular pago y borrar actividad en SQLite. (Verde)
- [x] `T-04`: [src/application/challenge_service.py] Implementar casos de uso de gestión de registros en `ChallengeService`. (Verde)
- [x] `T-05`: [src/presentation/api.py, src/presentation/web_views.py] Implementar endpoints REST (`PUT`, `DELETE`) e interfaz interactiva con modales y feedback accesible. (Verde)
- [x] `T-06`: [docs/user_guide_004-edicion-gestion-registros.md, harness] Redactar la Guía de Usuario, ejecutar `.\harness\init.ps1` y auditar con `.\harness\spec-gate.ps1 -FeatureId 004-edicion-gestion-registros`.
