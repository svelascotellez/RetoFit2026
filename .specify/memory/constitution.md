# Constitucion del Proyecto: RetoFit2026 (SDD + BDD + Clean Architecture v4.3)

## Contexto y Dominio del Proyecto: Reto Fit DIDT 2026
- **Propósito:** Sistema de gestión integral (físico y financiero) para el evento "Reto Fit" de los miembros de la DIDT (Dirección de Informática y Desarrollo Tecnológico).
- **Vigencia:** 19 de octubre al 20 de diciembre de 2026 (~9 semanas).
- **Regla Física del Reto:** Cada participante debe "quemar" 300 calorías o caminar 10,000 pasos en un día, al menos 4 días a la semana.
- **Regla Financiera y Penalizaciones:**
  - Total de aportaciones: $1,000 por participante en 5 pagos quincenales de $200 cada uno (Fechas: 19 de octubre, 2 de noviembre, 16 de noviembre, 30 de noviembre y 14 de diciembre).
  - Si cumple la meta semanal: conserva $100.
  - Si incumple la meta semanal: se penaliza con $100, los cuales pasan a la "bolsa semanal".
  - Distribución de incentivos: La bolsa semanal de penalizaciones se reparte equitativamente entre los participantes que cumplieron esa semana.
- **Cálculos y Reportes Automatizados:** Registro y cálculo automático de semanas cumplidas/incumplidas, dinero aportado, penalizaciones, ganancias adicionales de la bolsa, balance neto final y concentrado individual y general.
- **Despliegue Objetivo:** Aplicación Web en Python (FastAPI + Uvicorn) desplegable en Railway.com.
- **Arquetipo Visual:** Fitness Dark Mode con acentos Energy Neon, tarjetas Bento Grid y cumplimiento WCAG 2.1 AA.

---

## Principios Innegociables de Desarrollo
Toda especificacion, escenario Gherkin, plan tecnico, tarea e implementacion debe cumplir estas reglas innegociables:

1. **La Spec Manda:** Ningun codigo de produccion se escribe ni se modifica sin estar respaldado por un requisito EARS en `specs\<feature>\spec.md` y un escenario Gherkin en `specs\<feature>\scenarios.feature`.
2. **Stack Tecnologico:** Gobernado dinamicamente por `.specify\harness-config.json` (Python 3.11+, FastAPI, Uvicorn, pytest, pytest-bdd, mypy).
3. **Cero Dependencias Sorpresa:** Prohibido anadir paquetes externos no aprobados en `## 3. Allowed Dependencies` de `plan.md`.
4. **Logica Separada de la Interfaz (Clean Architecture):** El dominio (`src\domain\`) y los casos de uso (`src\application\`) no deben importar detalles HTTP, UI, bases de datos o librerias de infraestructura.
5. **Double-Loop BDD + TDD Obligatorio:** Primero se define el escenario en `scenarios.feature`, se implementan los step definitions en `tests\acceptance\` y tests unitarios en `tests\unit\` (Rojo), se implementa el codigo minimo en `src\` (Verde) y se refactoriza.
6. **Trazabilidad Triple de Criterios:** Cada Criterio de Aceptacion (`AC-x.x`) debe estar mapeado a `@AC-x.x` en `scenarios.feature` y probado en `tests\`.
7. **Inmutabilidad y Candado SHA-256:** Ninguna funcionalidad puede pasar a desarrollo sin la firma criptografica humana generada por `.\harness\sdd.ps1 -Action approve`.
8. **Guia de Usuario Obligatoria:** Ninguna funcionalidad puede considerarse finalizada ni pasar a estado `done` sin contar con su Guia de Usuario en `docs\user_guide_<feature>.md`, redactada a partir de los escenarios BDD para usuarios finales.
9. **UI/UX Design-System First & Aislamiento de Presentacion:** Toda interfaz de usuario reside exclusivamente en `src\presentation\`, gobernada por `.specify\design-system\design-tokens.json` y definida en la seccion 2 de `plan.md` antes de implementar. Las pruebas BDD validan interaccion, roles semanticos y accesibilidad (WCAG 2.1 AA), prohibiendose aserciones acopladas a clases CSS cosmeticas.