# Lista de Tareas Atomicas: FEAT-006

- [x] `T-01`: [tests/unit/test_weekly_report.py & src/domain/weekly_report.py] Implementar entidad de dominio inmutable `WeeklyReport` y cálculo de cuotas según calendario oficial ($200 quincenales, $100 final) y cumplimiento físico. (Rojo/Verde para AC-6.1 y AC-6.2).
- [x] `T-02`: [src/application/dto.py & src/application/challenge_service.py] Implementar DTOs y método `get_weekly_report(week_number)` con validación de semana 1 a 9. (Rojo/Verde para AC-6.3).
- [x] `T-03`: [src/presentation/schemas.py & src/presentation/api.py] Implementar endpoint REST `GET /api/reports/weekly/{week_number}` con validación de entrada y manejo de errores. (Rojo/Verde para AC-6.4).
- [x] `T-04`: [src/presentation/web_views.py] Crear sección interactiva Bento Grid en Dashboard Web con selector dinámico de semana (1 a 9), KPIs ejecutivos, tabla detallada y estado vacío accesible. (Rojo/Verde para AC-6.5 y AC-6.6).
- [x] `T-05`: [tests/acceptance/test_weekly_report_steps.py] Implementar step definitions BDD para `@AC-6.1`, `@AC-6.2`, `@AC-6.3`, `@AC-6.4`, `@AC-6.5` y `@AC-6.6`.
- [x] `T-06`: [docs/user_guide_006-informe-semanal-cuotas-cumplimiento.md] Redactar la Guía de Usuario obligatoria usando `.specify/templates/user_guide.template.md`.
- [x] `T-07`: [harness] Ejecutar `.\harness\init.ps1` y auditar con `.\harness\spec-gate.ps1 -FeatureId 006-informe-semanal-cuotas-cumplimiento`.
