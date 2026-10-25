# Google Antigravity Environment Guidelines (Windows - v4.3)

@AGENTS.md

## 1. Reglas de Ejecucion en el IDE
- La terminal predeterminada es PowerShell. Usa siempre sintaxis nativa de Windows (`.\harness\init.ps1`, `.\harness\sdd.ps1`).
- Antes de proponer cambios o invocar subagentes, ejecuta `.\harness\init.ps1`.
- Respeta estrictamente la seccion `## 5. Allowed Files` de la especificacion activa.
- Utiliza las plantillas de `.specify\templates\` para redactar `spec.md`, `scenarios.feature`, `plan.md` y `tasks.md`.
- Genera obligatoriamente la Guia de Usuario en `docs\user_guide_<id>.md` utilizando `.specify\templates\user_guide.template.md` antes de invocar la auditoria de cierre.

## 2. Regla Anti-Telefono-Descompuesto
- No pases bloques de codigo por el chat entre subagentes.
- Escribe los resultados tecnicos en `progress\impl_<id>.md` o `progress\review_<id>.md` y responde unicamente con la referencia al archivo en disco.

## 3. Puertas de Control Humano y Candado Criptografico (Antigravity IDE First)
- Queda ESTRICTAMENTE PROHIBIDO que el agente modifique arbitrariamente el estado en `feature_list.json`.
- En Antigravity IDE, el Agente solicita aprobacion humana directamente en el chat. Al recibir la confirmacion del usuario, el Agente ejecuta internamente:
  `powershell -ExecutionPolicy Bypass -Command ".\harness\sdd.ps1 -Action approve -FeatureId <id> -Force"`
- El usuario nunca debe ser obligado a abrir o manipular una consola externa para autorizar checkpoints.