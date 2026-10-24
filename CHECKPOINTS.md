# CHECKPOINTS.md — Criterios de Aceptacion y Calidad de Cierre (v4.3)

Para autorizar el estado `done` en `feature_list.json`, cada funcionalidad debe cumplir:

- [x] Cero errores en `.\harness\init.ps1` (linter/typecheck + pytest unitario y pytest-bdd en verde).
- [x] Cero violaciones en `.\harness\spec-gate.ps1`:
      1. Cero archivos modificados fuera de `Allowed Files` (Spec Drift).
      2. Cero importaciones prohibidas de infraestructura en `src\domain` y `src\application`.
      3. Cero dependencias no autorizadas en `plan.md`.
      4. 100% de los criterios EARS (`AC-x.x`) mapeados a etiquetas `@AC-x.x` en `scenarios.feature`.
      5. 100% de los criterios EARS (`AC-x.x`) probados en `tests\`.
      6. Guia de Usuario obligatoria generada y completa en `docs\user_guide_<feature>.md`.
      7. UI/UX Design Compliance: Si toca `src\presentation`, plan.md debe incluir especificacion UI/UX valida.
- [x] Documentacion registrada en `progress\review_<feature>.md`.