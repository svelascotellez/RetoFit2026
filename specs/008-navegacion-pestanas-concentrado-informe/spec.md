# Especificacion Funcional: FEAT-008 - Navegacion Modular por Pestañas del Dashboard Web

## 1. Contexto e Historia de Usuario
Como Administrador y Miembro del Reto Fit 2026 (DIDT)
Quiero visualizar el Concentrado Físico y Financiero y el Informe Semanal de Cuotas y Cumplimiento como pestañas independientes en la barra superior del Dashboard Web
Para organizar de manera limpia, intuitiva y modular las operaciones de registro, el estado financiero de los participantes, la auditoría semanal y la analítica deportiva sin saturación visual en una sola página larga.

## 2. Criterios de Aceptacion (Sintaxis EARS)
- **AC-8.1**: MIENTRAS el usuario interactúa con la interfaz web, EL SISTEMA DEBE proveer en la parte superior una barra de navegación con 4 pestañas accesibles (`role="tablist"`): "Panel General", "Concentrado Físico y Financiero", "Informe Semanal de Cuotas y Cumplimiento" y "Estadísticas del Reto".
- **AC-8.2**: CUANDO el usuario selecciona la pestaña "Concentrado Físico y Financiero", EL SISTEMA DEBE visualizar de forma exclusiva el contenedor accesible (`role="tabpanel"`, `id="panel-concentrado"`) con la tabla consolidada de participantes, sus aportaciones acumuladas, penalizaciones, ganancias y botones de gestión rápida (o el estado vacío accesible con rol "status" si no hay participantes).
- **AC-8.3**: CUANDO el usuario selecciona la pestaña "Informe Semanal de Cuotas y Cumplimiento", EL SISTEMA DEBE visualizar de forma exclusiva el contenedor accesible (`role="tabpanel"`, `id="panel-informe"`) con el selector dinámico de semanas (1 a 9), badge de liquidación, tarjetas KPI semanales y tabla detallada de cumplimiento por participante.
- **AC-8.4**: MIENTRAS el usuario utiliza el teclado en la barra de navegación de pestañas, EL SISTEMA DEBE soportar la navegación secuencial y circular mediante las teclas `ArrowRight`, `ArrowLeft`, `Home` y `End`, transfiriendo el foco y activando la pestaña correspondiente.
- **AC-8.5**: SI el usuario alterna entre cualquiera de las 4 pestañas, EL SISTEMA DEBE actualizar los atributos ARIA (`aria-selected="true/false"`, `tabindex="0/-1"`) y ocultar de forma accesible los paneles inactivos sin provocar recarga de página.

## 3. Comportamientos Fuera de Alcance (Out of Scope)
- No se alteran las rutas de la API REST existentes (`/api/summary`, `/api/reports/weekly/{week_number}`, `/api/statistics`, etc.).
- No se modifica la persistencia en base de datos SQLite ni modelos de dominio.
- No se eliminan funcionalidades de los formularios de registro de miembros, pagos o actividades diarias.

## 4. Requisitos No Funcionales, UI/UX y Accesibilidad
- Diseño acorde al arquetipo Fitness Dark Mode Energy Neon (`#0F172A`, `#1E293B`, `#10B981`, `#06B6D4`, `#F97316`).
- Estándar de accesibilidad WCAG 2.1 AA (contraste >= 4.5:1 en texto de pestañas, bordes de foco de 2px en `:focus-visible`).
- Atributos semánticos ARIA completos (`role="tablist"`, `role="tab"`, `role="tabpanel"`, `aria-selected`, `aria-controls`, `aria-labelledby`).
- Transición instantánea (< 16 ms) entre pestañas mediante manipulación del DOM sin peticiones de red adicionales para conmutar paneles.

## 5. Allowed Files
Rutas exactas autorizadas para creacion o modificacion durante esta funcionalidad:
- `src/presentation/web_views.py`
- `tests/unit/test_tabs_navigation.py`
- `tests/acceptance/test_tabs_navigation_steps.py`
