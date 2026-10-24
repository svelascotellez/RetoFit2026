# Contexto Operativo y Contrato del Agente (Windows Environment - SDD v4.3)

## 1. Resumen del Proyecto
Sistema para la gestión integral (físico y financiero) de **RetoFit2026** (evento DIDT) bajo arquitectura limpia, Spec-Driven Development (SDD) y Behavior-Driven Development (BDD) en Google Antigravity sobre Windows. La especificacion en `specs\` (`spec.md` + `scenarios.feature`) es la unica fuente de la verdad.

## 2. Protocolo Obligatorio de Inicio
1. Ejecuta `.\harness\init.ps1` antes de cualquier accion. Si falla, repara el entorno.
2. Si no se te asigno rol, actua segun `.agents\skills\`.
3. Prohibido tocar codigo en `src\` sin una especificacion aprobada con hash criptografico valido en `feature_list.json` y una tarea activa en `tasks.md`.
4. Toda funcionalidad debe contar obligatoriamente con su Guia de Usuario en `docs\user_guide_<feature>.md` antes de solicitar revision o cierre.

## 3. Mapa de Documentacion
- Principios innegociables: `.specify\memory\constitution.md`
- Configuracion de ejecucion: `.specify\harness-config.json`
- Plantillas de artefactos: `.specify\templates\`
- Guias de usuario obligatorias: `docs\user_guide_<feature>.md`
- Criterios de cierre: `CHECKPOINTS.md`
- Estado del backlog: `feature_list.json`

## 4. Comandos del Entorno (PowerShell)
- Validar salud y tests: `.\harness\init.ps1`
- Consultar backlog: `.\harness\sdd.ps1 -Action status`
- Avanzar ciclo: `.\harness\sdd.ps1 -Action next` (despliega Checkpoint Humano automático si hay specs listas)
- Aprobar con candado criptografico (Humano): `.\harness\sdd.ps1 -Action approve -FeatureId <id>`
- Auditar alcance, arquitectura, guia y UI/UX: `.\harness\spec-gate.ps1 -FeatureId <carpeta_feature>`