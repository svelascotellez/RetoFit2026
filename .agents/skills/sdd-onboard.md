---
name: sdd-onboard
description: Guia la entrevista interactiva inicial (1 pregunta por turno) para configurar el proyecto, constitution.md, feature_list.json y la primera spec + scenarios.feature.
---
# Skill: SDD Onboard (v4.3)
## REGLA FUNDAMENTAL DE INTERACCION
Realiza EXACTAMENTE UNA PREGUNTA POR TURNO. Espera la respuesta antes de formular la siguiente.
## Workflow
1. Pregunta 1: Tipo de aplicacion y proposito principal.
2. Pregunta 2: Tipo de interfaz (CLI/TUI, Web Frontend, Movil, Desktop o API/Backend sin interfaz visual).
3. Pregunta 3: Lenguaje, version y librerias clave (actualiza `.specify/harness-config.json`).
4. Pregunta 4 (UI/UX Intelligence): Si tiene interfaz: ¿Cual es el arquetipo visual preferido (p. ej. Modern Clean SaaS, Minimalista, Bento Grid, Dark Mode), la paleta de colores y el nivel de accesibilidad deseado? (Configura `.specify/design-system/design-tokens.json`). Si es backend puro, registrar como "headless/sin UI".
5. Pregunta 5: Linters, typecheck y test runner (actualiza `.specify/harness-config.json`).
6. Actualiza `.specify/memory/constitution.md` y `AGENTS.md`.
7. Pregunta 6: Nombre y descripcion de FEAT-001. Registra en `feature_list.json` con `"status": "pending"`.
8. Preguntas 7 a 9 (una por turno): Roles/historia principal, casos borde/errores/estados UI (loading, empty, error) y elementos Fuera de Alcance.
9. Genera `specs/001-<slug>/spec.md` y `specs/001-<slug>/scenarios.feature` usando `.specify/templates/`.
10. Cambia el estado a `"spec_ready"` e indica al usuario ejecutar: `.\harness\sdd.ps1 -Action next` (lo cual invocará interactivamente el candado criptográfico).