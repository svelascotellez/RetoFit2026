---
name: sdd-ui-ux
description: Inteligencia de Diseno UI/UX Pro Max adaptada a SDD. Aplica tokens de diseno, arquetipos visuales y accesibilidad WCAG en plan.md y src/presentation/.
---
# Skill: SDD UI/UX Pro Max - Design Intelligence (v4.3)
Guia el diseno visual de interfaces bajo Spec-Driven Development:
1. Consulta `.specify/design-system/design-tokens.json` para obtener paleta, tipografia y escalas.
2. Exige la definicion de 5 estados obligatorios en cada vista: Default, Hover/Focus, Loading/Skeleton, Empty State y Error State.
3. Garantiza accesibilidad WCAG 2.1 AA (contraste >= 4.5:1, navegacion por teclado, atributos semanticos/ARIA).
4. Prohibe el uso de estilos cosmeticos arbitrarios: todo componente debe implementarse en `src/presentation/` alineado con `plan.md` y `design-tokens.json`.
5. Toda dependencia de UI (librerias de iconos, componentes o CSS) debe registrarse en `## 4. Allowed Dependencies` de `plan.md`.