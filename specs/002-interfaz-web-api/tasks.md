# Lista de Tareas Atomicas: FEAT-002 - Interfaz Web y API FastAPI para Reto Fit

- [x] `T-01`: [tests/acceptance/test_web_api_steps.py] Implementar step definitions BDD para `@AC-2.1` a `@AC-2.9` basados en `scenarios.feature`. (Rojo)
- [x] `T-02`: [tests/unit/test_api.py, src/presentation/schemas.py] Implementar esquemas Pydantic V2 de validacion de solicitudes y respuestas (`@AC-2.2`, `@AC-2.3`, `@AC-2.8`).
- [x] `T-03`: [src/presentation/api.py] Implementar endpoints REST de FastAPI para participantes, pagos, actividad y liquidacion semanal (`@AC-2.1` a `@AC-2.6`, `@AC-2.8`).
- [x] `T-04`: [src/presentation/web_views.py, src/main.py] Implementar vista web en Dark Mode Energy Neon con Bento Grid, estado vacio con rol status y app principal (`@AC-2.6`, `@AC-2.7`, `@AC-2.9`).
- [x] `T-05`: [docs/user_guide_002-interfaz-web-api.md] Redactar la Guia de Usuario obligatoria usando `.specify/templates/user_guide.template.md`.
- [x] `T-06`: [harness] Ejecutar `.\harness\init.ps1` y auditar con `.\harness\spec-gate.ps1 -FeatureId 002-interfaz-web-api`.
