# Lista de Tareas Atomicas: FEAT-005

- [x] `T-01`: [tests/acceptance/test_financial_quota_steps.py] Implementar step definitions BDD para `@AC-5.1` a `@AC-5.5`. (Rojo)
- [x] `T-02`: [src/domain/participant.py, tests/unit/test_participant_financial_target.py] Actualizar `TARGET_CONTRIBUTION = 900.0` y tests unitarios de dominio. (Verde)
- [x] `T-03`: [src/presentation/schemas.py] Actualizar esquemas Pydantic con cuota objetivo de $900.00 MXN. (Verde)
- [x] `T-04`: [src/presentation/web_views.py] Actualizar calendario oficial a $900 ($100 en 14 dic) y agregar botón rápido `[+ $100]`. (Verde)
- [x] `T-05`: [docs/user_guide_005-ajuste-cuota-final.md, harness] Redactar Guía de Usuario, ejecutar `.\harness\init.ps1` y auditar con `.\harness\spec-gate.ps1 -FeatureId 005-ajuste-cuota-final`.
