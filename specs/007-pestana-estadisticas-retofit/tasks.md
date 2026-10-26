# Lista de Tareas Atomicas: FEAT-007

- [x] `T-01`: [tests/unit/test_challenge_stats.py & src/domain/challenge_stats.py] Implementar entidades de dominio `ParticipantRankingItem`, `WeeklyStatsTrendItem`, `GlobalStats` y suite de pruebas unitarias para métricas globales, ranking con desempate por calorías y tendencias semanales. (Rojo/Verde para AC-7.1, AC-7.2 y AC-7.3).
- [x] `T-02`: [src/application/dto.py & src/application/challenge_service.py] Implementar DTOs y método `get_global_statistics()` en el servicio de aplicación. (Verde para AC-7.1, AC-7.2 y AC-7.3).
- [x] `T-03`: [src/presentation/schemas.py & src/presentation/api.py] Implementar esquemas Pydantic y endpoint REST `GET /api/statistics`. (Rojo/Verde para AC-7.4).
- [x] `T-04`: [src/presentation/web_views.py] Implementar sistema de pestañas accesibles (`tablist`, `tab`, `tabpanel`) con soporte de teclado, Bento Grid de estadísticas integrales (tarjetas KPI, podio/ranking, tendencias) y estado vacío accesible (`role="status"`). (Rojo/Verde para AC-7.5 y AC-7.6).
- [x] `T-05`: [tests/acceptance/test_challenge_stats_steps.py] Implementar step definitions BDD para `@AC-7.1`, `@AC-7.2`, `@AC-7.3`, `@AC-7.4`, `@AC-7.5` y `@AC-7.6`.
- [x] `T-06`: [docs/user_guide_007-pestana-estadisticas-retofit.md] Redactar la Guía de Usuario obligatoria usando `.specify/templates/user_guide.template.md`.
- [x] `T-07`: [harness] Ejecutar `.\harness\init.ps1` y auditar con `.\harness\spec-gate.ps1 -FeatureId 007-pestana-estadisticas-retofit`.
