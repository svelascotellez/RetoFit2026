# Lista de Tareas Atomicas: {FEATURE_ID}

- [ ] `T-01`: [tests/acceptance/test_{FEATURE}_steps.py] Implementar step definitions BDD para `@AC-1.1`. (Rojo)
- [ ] `T-02`: [src/domain/{MODULE}.py] Crear entidad de dominio para cumplir `@AC-1.1`. (Verde)
- [ ] `T-03`: [tests/unit/test_{MODULE}.py] Crear suite de pruebas unitarias para `@AC-1.2`. (Rojo)
- [ ] `T-04`: [src/application/{SERVICE}.py] Implementar validacion de error para `@AC-1.2`. (Verde)
- [ ] `T-05`: [docs/user_guide_{FEATURE_DIR}.md] Redactar la Guia de Usuario obligatoria usando `.specify\templates\user_guide.template.md`.
- [ ] `T-06`: [harness] Ejecutar `.\harness\init.ps1` y auditar con `.\harness\spec-gate.ps1 -FeatureId {FEATURE_DIR}`.