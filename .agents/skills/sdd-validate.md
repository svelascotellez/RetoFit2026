---
name: sdd-validate
description: Audita el cierre de la feature con spec-gate.ps1 (Auditor Sextuple que incluye la Guia de Usuario).
---
# Skill: SDD Validate (v4.3)
Verifica la existencia y calidad de `docs/user_guide_<feature>.md`, ejecuta `.\harness\spec-gate.ps1 -FeatureId <feature_dir>` y comprueba `CHECKPOINTS.md`.