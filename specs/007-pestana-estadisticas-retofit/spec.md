# Especificacion Funcional: FEAT-007 - Pestaña de Estadísticas Integrales del Reto Fit

## 1. Contexto e Historia de Usuario
Como Administrador y Miembro del Reto Fit 2026 (DIDT)
Quiero navegar a una pestaña dedicada de estadísticas y analítica interactiva en el Dashboard Web
Para visualizar el ranking general de participantes, métricas globales deportivas (pasos y calorías acumuladas y promedios diarios), tendencias de cumplimiento por semana y el balance de la bolsa, promoviendo la motivación y la transparencia durante las 9 semanas del reto.

## 2. Criterios de Aceptacion (Sintaxis EARS)
- **AC-7.1**: CUANDO se consultan las estadísticas del reto, EL SISTEMA DEBE calcular las métricas globales acumuladas: total de calorías quemadas, total de pasos caminados, total de días exitosos registrados, días totales con actividad registrada, y promedios de calorías y pasos por día registrado.
- **AC-7.2**: CUANDO se procesan las estadísticas individuales, EL SISTEMA DEBE generar el ranking de participantes ordenado descendentemente por mayor número de días exitosos (y como criterio de desempate secundario por total de calorías quemadas), asignando la posición de ranking (1, 2, 3...) a cada miembro.
- **AC-7.3**: CUANDO se evalúa la tendencia semanal del evento, EL SISTEMA DEBE computar para cada semana del reto (semanas 1 a 9) el total de días exitosos, número de participantes cumplidores, bolsa semanal acumulada y tasa de cumplimiento porcentual.
- **AC-7.4**: MIENTRAS se consulta el endpoint REST de la API en `/api/statistics`, EL SISTEMA DEBE responder con código HTTP 200 y el esquema consolidado que incluye totales globales, el ranking de participantes, la evolución semanal y el resumen contable.
- **AC-7.5**: MIENTRAS el usuario interactúa con la interfaz web, EL SISTEMA DEBE proveer una barra de navegación con pestañas accesibles (`tablist`, `tab`, `tabpanel`) con soporte completo de teclado y roles ARIA que permita alternar instantáneamente entre el "Panel General" y las "Estadísticas del Reto" sin recargar la página.
- **AC-7.6**: SI no existen actividades registradas o participantes en el sistema, EL SISTEMA DEBE desplegar en la pestaña de estadísticas el estado vacío accesible con rol semántico "status" indicando que no hay estadísticas acumuladas aún.

## 3. Comportamientos Fuera de Alcance (Out of Scope)
- No se modifican las reglas del motor de dominio ni de cálculo de penalizaciones.
- No se requiere integración con wearables externos (smartwatches, Apple Health, Google Fit) por API directa; se calculan a partir de los registros ingresados en el sistema.
- No se alteran los datos existentes en SQLite ni esquemas de participantes.

## 4. Requisitos No Funcionales, UI/UX y Accesibilidad
- Tiempo de respuesta del endpoint `/api/statistics` < 150 ms.
- Navegación por pestañas con roles ARIA (`role="tablist"`, `role="tab"`, `role="tabpanel"`, `aria-selected="true/false"`).
- Atributos de foco accesibles y navegación por teclado en la barra de pestañas.
- Contraste visual mínimo WCAG 2.1 AA (4.5:1 para texto normal, 3:1 para barras y medidores).
- Estados de interfaz obligatorios: default (datos cargados), loading (skeleton/indicador), empty_state (sin actividades) y error_state.

## 5. Allowed Files
Rutas exactas autorizadas para creacion o modificacion durante esta funcionalidad:
- `src/domain/challenge_stats.py`
- `src/application/dto.py`
- `src/application/challenge_service.py`
- `src/presentation/schemas.py`
- `src/presentation/api.py`
- `src/presentation/web_views.py`
- `tests/unit/test_challenge_stats.py`
- `tests/acceptance/test_challenge_stats_steps.py`
