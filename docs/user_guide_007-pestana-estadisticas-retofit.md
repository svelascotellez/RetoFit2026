# Guia de Usuario: FEAT-007 - Pestaña de Estadísticas Integrales del Reto Fit

## 1. Descripcion General
La **Pestaña de Estadísticas Integrales del Reto Fit** introduce una vista analítica y deportiva en el Dashboard Web de **RetoFit2026** (evento DIDT), complementando el panel operativo tradicional con visualización del desempeño colectivo e individual.

Esta funcionalidad proporciona:
- **Navegación por Pestañas Accesibles (Tabs)**: Alternancia instantánea entre el **"Panel General"** y las **"Estadísticas del Reto"** mediante una barra accesible (`role="tablist"`, `role="tab"`, `role="tabpanel"`) compatible con teclado y lectores de pantalla.
- **Métricas Deportivas Globales**: Indicadores acumulados de calorías totales quemadas, pasos caminados, días con actividades físicas registradas y promedios diarios por día activo.
- **Podio y Ranking Competitivo**: Clasificación general de participantes jerarquizada descendentemente por días exitosos cumplidos, utilizando las calorías quemadas acumuladas como criterio de desempate técnico, destacando los 3 primeros puestos con insignias de podio (🥇 Oro, 🥈 Plata, 🥉 Bronce).
- **Tendencias de Cumplimiento Semanal**: Gráfico de barras porcentuales y tabla comparativa del avance de las 9 semanas oficiales del reto, mostrando la tasa de efectividad, miembros cumplidores y fondos de bolsa.
- **Endpoint REST Consolidado**: Acceso vía API en `/api/statistics` para integración y consumo automatizado.

---

## 2. Requisitos Previos y Configuracion
- Sistema en ejecución local (`python -m uvicorn src.main:app --host 127.0.0.1 --port 8010`) o desplegado en Railway.
- Se recomienda contar con participantes y actividades físicas registradas en el sistema para visualizar las métricas completas y el podio. Si no existen registros aún, la pestaña desplegará automáticamente un estado vacío accesible informando la situación.

---

## 3. Instrucciones de Uso Paso a Paso

### A. Navegación entre Pestañas en el Dashboard Web
1. Ingresa a la URL principal del sistema (ej. `http://127.0.0.1:8010/`).
2. En la parte superior de la página, localiza la barra de navegación con las opciones:
   - **📋 Panel General**: Contiene las métricas financieras, formularios de registro, informe semanal y tabla general de concentrado.
   - **📊 Estadísticas del Reto**: Despliega la analítica deportiva, podio de participantes y tendencias.
3. Haz clic en la pestaña **"Estadísticas del Reto"** o utiliza el teclado:
   - Presiona `ArrowRight` o `ArrowLeft` para alternar entre pestañas.
   - Presiona `Home` o `End` para ir a la primera o última pestaña.
4. El cambio entre vistas se realiza de inmediato y sin recarga de página.

### B. Exploración del Podio y Ranking
1. En la pestaña de estadísticas, revisa las tarjetas KPI de totales y promedios diarios.
2. Consulta la sección **"🏆 Podio y Ranking de Rendimiento"**:
   - Observa la posición asignada (1, 2, 3...) calculada según el mayor número de días exitosos ($\ge 300$ kcal o $\ge 10,000$ pasos).
   - En caso de empate en días, el sistema desempata automáticamente por mayor volumen de calorías quemadas.
   - Los primeros tres lugares ostentan los distintivos **🥇 1° Lugar (Oro)**, **🥈 2° Lugar (Plata)** y **🥉 3° Lugar (Bronce)**.

### C. Consulta Automatizada vía API REST
Para obtener todas las estadísticas consolidadas en formato JSON:
- **Método**: `GET`
- **Ruta**: `/api/statistics`
- **Autenticación**: No requerida.
- **Códigos HTTP**: `200 OK`.

---

## 4. Ejemplos de Uso

### Flujo Principal: Petición al Endpoint REST
**Petición:**
```http
GET /api/statistics HTTP/1.1
Host: 127.0.0.1:8010
Accept: application/json
```

**Respuesta Exitosa (200 OK):**
```json
{
  "total_calories": 5400.0,
  "total_steps": 125000,
  "total_successful_days": 15,
  "total_activity_days": 18,
  "average_daily_calories": 300.0,
  "average_daily_steps": 6944.0,
  "total_participants": 3,
  "total_penalties": 200.0,
  "total_distributed_pool": 200.0,
  "ranking": [
    {
      "rank_position": 1,
      "participant_id": "didt-02",
      "name": "Carlos Mendoza",
      "successful_days": 8,
      "total_calories": 3200.0,
      "total_steps": 75000,
      "is_podium": true
    },
    {
      "rank_position": 2,
      "participant_id": "didt-03",
      "name": "Clara Solís",
      "successful_days": 5,
      "total_calories": 1400.0,
      "total_steps": 32000,
      "is_podium": true
    },
    {
      "rank_position": 3,
      "participant_id": "didt-01",
      "name": "Ana Gómez",
      "successful_days": 2,
      "total_calories": 800.0,
      "total_steps": 18000,
      "is_podium": true
    }
  ],
  "weekly_trends": [
    {
      "week_number": 1,
      "successful_days": 10,
      "compliant_participants": 2,
      "total_participants": 3,
      "compliance_rate": 66.7,
      "pool_amount": 100.0
    }
  ]
}
```

---

## 5. Respuestas a Errores y Preguntas Frecuentes

| Mensaje de Error / Comportamiento | Causa | Como Resolverlo |
| :--- | :--- | :--- |
| Se muestra el recuadro "No hay actividades registradas en el reto" | No se han registrado aún calorías ni pasos en el sistema para ningún participante. | Dirígete a la pestaña "Panel General" y registra actividades diarias mediante el formulario correspondiente. |
| Dos participantes tienen los mismos días exitosos pero distinta posición | El criterio secundario de ordenamiento es el total de calorías quemadas. | Si el participante con menor posición desea subir, debe incrementar sus calorías acumuladas o registrar días exitosos adicionales. |
| La pestaña de estadísticas no responde al hacer clic | El script del navegador pudo ser bloqueado o hay un problema de carga. | Recarga la página con `Ctrl + F5` o verifica que JavaScript esté habilitado en el navegador. |
| El promedio de calorías/pasos muestra 0.0 | Se registraron 0 días de actividad física en total. | El sistema protege contra división entre cero; los promedios se calcularán tan pronto se registre el primer día. |
