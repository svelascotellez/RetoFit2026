# Especificacion Funcional: FEAT-002 - Interfaz Web y API FastAPI para Reto Fit

## 1. Contexto e Historia de Usuario
Como Administrador y Participante del Reto Fit DIDT,
Quiero acceder a una interfaz web moderna en Dark Mode Energy Neon y consumir endpoints REST de FastAPI,
Para consultar el concentrado general y por participante, registrar abonos y entrenamientos diarios, liquidar semanas del reto y disponer de una plataforma lista para su despliegue en Railway.com.

## 2. Criterios de Aceptacion (Sintaxis EARS)
- **AC-2.1**: CUANDO se realiza una peticion HTTP GET a `/api/summary`, EL SISTEMA DEBE responder con codigo 200 y la estructura completa del concentrado financiero y fisico (participantes, aportaciones, fondo en bolsa, rollover y detalle individual).
- **AC-2.2**: CUANDO se envia una peticion HTTP POST a `/api/participants` con `id` y `name` validos, EL SISTEMA DEBE registrar al participante y responder con codigo 201 y los datos del participante registrado.
- **AC-2.3**: CUANDO se envia una peticion HTTP POST a `/api/payments` con un monto positivo hacia la cuota de $1,000 MXN en 5 abonos de $200 (19 de octubre, 2 de noviembre, 16 de noviembre, 30 de noviembre y 14 de diciembre), EL SISTEMA DEBE abonar el pago al participante y retornar el balance aportado con codigo 200.
- **AC-2.4**: CUANDO se envia una peticion HTTP POST a `/api/activity` con calorias o pasos validos, EL SISTEMA DEBE registrar la sesion diaria y retornar con codigo 200 indicando si el dia fue exitoso (`is_successful: true/false`).
- **AC-2.5**: CUANDO se envia una peticion HTTP POST a `/api/weeks/{week_number}/close`, EL SISTEMA DEBE liquidar la semana especificada y retornar el resultado de la bolsa (cumplidores, incumplidores, ganancia por persona y rollover) con codigo 200.
- **AC-2.6**: CUANDO se realiza una peticion HTTP GET a `/health`, EL SISTEMA DEBE responder con codigo 200 y el estado saludable (`{"status": "healthy"}`) para verificaciones de despliegue en Railway.com.
- **AC-2.7**: MIENTRAS un usuario navega a la ruta principal `/`, EL SISTEMA DEBE servir una aplicacion web interactiva en Dark Mode Energy Neon con tarjetas Bento Grid reflejando metricas del evento Reto Fit.
- **AC-2.8**: CUANDO se reciben entradas invalidas en la API (participante inexistente, montos negativos o campos faltantes), EL SISTEMA DEBE responder con codigo HTTP 400 o 404 o 422 y un mensaje de error descriptivo en formato JSON.
- **AC-2.9**: MIENTRAS no existan participantes registrados en el sistema, EL SISTEMA DEBE presentar en la interfaz un estado vacio accesible (`empty_state`) con rol semantico `status` y sugerencia de accion para registrar el primer participante.

## 3. Comportamientos Fuera de Alcance (Out of Scope)
- No se incluye autenticacion OAuth2 / Single Sign-On (SSO) empresarial en esta version.
- No se incluye persistencia en base de datos PostgreSQL/MySQL (el almacenamiento activo opera en memoria para despliegue rapido).
- No se incluyen pasarelas de pago externas ni sincronizacion automatica con APIs de smartwatches.

## 4. Requisitos No Funcionales, UI/UX y Accesibilidad
- Arquetipo visual: Fitness Dark Mode con acentos Energy Neon (`#10B981`, `#F97316`, `#0F172A`, `#1E293B`) y tarjetas Bento Grid segun `.specify/design-system/design-tokens.json`.
- Cumplimiento de accesibilidad WCAG 2.1 AA (contraste tipografico >= 4.5:1, estructura semantica HTML5 y roles ARIA).
- Compatibilidad para ejecucion y despliegue directo en Railway.com via Uvicorn (`uvicorn src.main:app --host 0.0.0.0 --port $PORT`).
- Tiempo de respuesta de endpoints API < 50 ms.

## 5. Allowed Files
Rutas exactas autorizadas para creacion o modificacion durante esta funcionalidad:
- `src/presentation/schemas.py`
- `src/presentation/api.py`
- `src/presentation/web_views.py`
- `src/main.py`
- `tests/unit/test_api.py`
- `tests/acceptance/test_web_api_steps.py`
