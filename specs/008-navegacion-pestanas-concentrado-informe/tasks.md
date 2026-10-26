# Lista de Tareas Atomicas: FEAT-008

- [x] `T-01`: [tests/unit/test_tabs_navigation.py] Crear suite de pruebas unitarias para la conmutación y estructura de los 4 paneles de pestañas. (Rojo para AC-8.1, AC-8.2 y AC-8.3).
- [x] `T-02`: [src/presentation/web_views.py] Reorganizar los paneles HTML separando el Concentrado Físico y Financiero y el Informe Semanal en paneles tabulares independientes y ampliar la barra de navegación superior con las 4 pestañas y soporte de teclado accesible. (Verde para AC-8.1, AC-8.2, AC-8.3, AC-8.4 y AC-8.5).
- [x] `T-03`: [tests/acceptance/test_tabs_navigation_steps.py] Implementar step definitions BDD para `@AC-8.1`, `@AC-8.2`, `@AC-8.3`, `@AC-8.4` y `@AC-8.5`.
- [x] `T-04`: [docs/user_guide_008-navegacion-pestanas-concentrado-informe.md] Redactar la Guía de Usuario obligatoria usando `.specify/templates/user_guide.template.md`.
- [x] `T-05`: [harness] Ejecutar `.\harness\init.ps1` y auditar con `.\harness\spec-gate.ps1 -FeatureId 008-navegacion-pestanas-concentrado-informe`.
