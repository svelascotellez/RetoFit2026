# Lista de Tareas Atomicas: FEAT-001 - Motor de Dominio del Reto Fit

- [x] `T-01`: [tests/acceptance/test_challenge_steps.py] Implementar step definitions BDD para `@AC-1.1` a `@AC-1.8` basados en `scenarios.feature`. (Rojo)
- [x] `T-02`: [tests/unit/test_activity.py, src/domain/activity.py] Implementar Value Object `DailyActivity` con validaciones y determinación de día exitoso (`@AC-1.1`, `@AC-1.8`).
- [x] `T-03`: [tests/unit/test_challenge_week.py, src/domain/challenge_week.py] Implementar entidad `ChallengeWeek` para evaluación de cumplimiento semanal (`@AC-1.2`).
- [x] `T-04`: [tests/unit/test_challenge_pool.py, src/domain/challenge_pool.py] Implementar entidad `WeeklyPool` para penalizaciones ($100), reparto equitativo y rollover (`@AC-1.3`, `@AC-1.4`, `@AC-1.5`).
- [x] `T-05`: [tests/unit/test_participant.py, src/domain/participant.py] Implementar entidad `Participant` para aportaciones económicas (hasta $900) y registro de actividades (`@AC-1.6`, `@AC-1.8`).
- [x] `T-06`: [tests/unit/test_challenge_service.py, src/application/challenge_service.py, src/application/dto.py, src/domain/financial_summary.py] Implementar orquestador `ChallengeService` y cálculo de concentrado financiero (`@AC-1.7`).
- [x] `T-07`: [docs/user_guide_001-motor-dominio-retofit.md] Redactar la Guia de Usuario obligatoria usando `.specify/templates/user_guide.template.md`.
- [x] `T-08`: [harness] Ejecutar `.\harness\init.ps1` y auditar con `.\harness\spec-gate.ps1 -FeatureId 001-motor-dominio-retofit`.
