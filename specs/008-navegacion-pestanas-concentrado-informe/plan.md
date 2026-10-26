# Plan Tecnico de Implementacion: FEAT-008

## 1. Diseno Arquitectonico (Clean Architecture)
- **Dominio (`src/domain/`)**: Sin modificaciones en reglas de negocio ni entidades puras.
- **Aplicacion (`src/application/`)**: Cero modificaciones de servicios existentes. Reutilización completa de `ChallengeService`.
- **Infraestructura (`src/infrastructure/`)**: Reutilización de SQLite sin alteraciones.
- **Presentacion (`src/presentation/`)**:
  - `src/presentation/web_views.py`: Reorganización del renderizado HTML del Dashboard en 4 paneles tabulares (`tabpanel`):
    1. `#panel-general`: Métricas clave superiores, Fechas de aportación y los 4 formularios operativos (Inscribir miembro, Abonar pago, Registrar actividad, Liquidar semana).
    2. `#panel-concentrado`: Tabla completa del Concentrado Físico y Financiero con gestión rápida de participantes, abonos y estado de balance (o estado vacío accesible).
    3. `#panel-informe`: Sección interactiva del Informe Semanal de Cuotas y Cumplimiento con selector de semanas (1 a 9), badge de liquidación y tabla detallada.
    4. `#panel-stats`: Analítica global deportiva (calorías, pasos), podio de 3 primeros lugares y tendencias semanales.
  - Implementación de la barra de navegación superior con 4 botones de pestaña (`tab`) y función `switchTab(tabId)` ampliada para conmutar dinámicamente entre las 4 pestañas y soporte de teclado accesible.

## 2. UI/UX Design System Specification (Design-System First)
- **Arquetipo Visual**: Fitness Dark Mode Energy Neon (`#0F172A`, `#1E293B`, `#10B981`, `#06B6D4`, `#F97316`).
- **Tokens de Color y Tipografia**:
  - Tipografía: 'Outfit', Inter, sans-serif para títulos e interactivos; 'Fira Code' para números y métricas.
  - Paleta: `--bg-main: #0F172A`, `--surface: #1E293B`, `--border: #334155`, `--primary: #10B981`, `--neon-accent: #06B6D4`, `--secondary: #F97316`.
- **Estados Obligatorios**:
  - Default: Pestaña "Panel General" activa con subrayado en gradiente neón (`#10B981` a `#06B6D4`), demás paneles ocultos.
  - Hover/Focus: Micro-interacciones suaves, `:focus-visible` con borde resaltado de 2px en `--neon-accent`.
  - Loading/Skeleton: Indicadores de carga preservados para solicitudes dinámicas.
  - Empty State: Estados vacíos semánticos con `role="status"` y `aria-live="polite"` cuando correspondan.
  - Error State: Notificaciones flotantes toast con borde `--error`.
- **Accesibilidad**: WCAG 2.1 AA (contraste >= 4.5:1 en texto, >= 3:1 en bordes/gráficos), soporte completo de teclado en tabs (`ArrowRight`, `ArrowLeft`, `Home`, `End`), roles semánticos `role="tablist"`, `role="tab"`, `role="tabpanel"`, `aria-selected`, `aria-controls`, `aria-labelledby`.

## 3. Contratos y Esquemas
- `switchTab(tabId: 'general' | 'concentrado' | 'informe' | 'stats'): void`
  - Conmuta la clase `active` en la pestaña seleccionada.
  - Ajusta `aria-selected="true"` en la pestaña activa y `aria-selected="false"` en las inactivas.
  - Ajusta `tabindex="0"` en la activa y `"-1"` en las inactivas.
  - Muestra el panel asociado (`display: block`, remover `.hidden`) y oculta los otros 3 paneles (`display: none`, agregar `.hidden`).

## 4. Allowed Dependencies
Librerias externas de terceros autorizadas:
- `pydantic`
- `fastapi`
- `pytest`
- `pytest-bdd`

## 5. Matriz de Trazabilidad BDD / TDD
| Criterio EARS | Escenario Gherkin | Test Automatizado |
| :--- | :--- | :--- |
| `AC-8.1` | `@AC-8.1` | `test_ac_8_1_tabs_header_display` |
| `AC-8.2` | `@AC-8.2` | `test_ac_8_2_concentrado_tab_panel` |
| `AC-8.3` | `@AC-8.3` | `test_ac_8_3_informe_semanal_tab_panel` |
| `AC-8.4` | `@AC-8.4` | `test_ac_8_4_keyboard_navigation_between_tabs` |
| `AC-8.5` | `@AC-8.5` | `test_ac_8_5_instant_tab_switching_without_reload` |
