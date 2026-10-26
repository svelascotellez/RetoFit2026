# Guia de Usuario: FEAT-008 - Navegacion Modular por Pestañas del Dashboard Web

## 1. Descripcion General
La **Navegación Modular por Pestañas del Dashboard Web** transforma la experiencia visual y operativa del sistema **RetoFit2026** (DIDT), desacoplando verticalmente los grandes componentes del panel en 4 pestañas superiores de acceso instantáneo:

1. **📋 Panel General (`#panel-general`)**: Tarjetas de métricas financieras de alto nivel (Bolsa Semanal/Rollover, Miembros Registrados, Total Recaudado), calendario de aportaciones quincenales obligatorias ($900.00 en 5 fechas) y los 4 formularios operativos para registrar miembros, abonar cuotas quincenales, cargar actividad física diaria y liquidar semanas del reto.
2. **👥 Concentrado Físico y Financiero (`#panel-concentrado`)**: Tabla unificada de participantes con su detalle de aportaciones acumuladas, semanas completadas, penalizaciones de $100 por semana incumplida, ganancias redistribuidas de la bolsa, balance financiero neto y botones de edición rápida, anulación y eliminación.
3. **📊 Informe Semanal de Cuotas y Cumplimiento (`#panel-informe`)**: Módulo interactivo de auditoría con selector dinámico de semanas 1 a 9, badge de estado (Liquidada vs En Curso), 4 tarjetas KPI de cumplimiento y solvencia, y desglose individual por participante sin recargar la página.
4. **📈 Estadísticas del Reto (`#panel-stats`)**: Analítica deportiva global (calorías totales, pasos acumulados, promedios por día activo), podio y ranking competitivo Top 3 con insignias (Oro, Plata, Bronce) y resolución técnica de empates por calorías, además del histograma de tendencias de cumplimiento semanal.

Esta distribución resuelve la sobrecarga cognitiva del usuario, reduce el desplazamiento vertical en pantallas móviles y de escritorio, y garantiza accesibilidad universal conforme al estándar WAI-ARIA (`role="tablist"`, `role="tab"`, `role="tabpanel"`).

---

## 2. Requisitos Previos y Configuracion
- El servicio web debe estar en ejecución local mediante:
  ```powershell
  python -m uvicorn src.main:app --host 127.0.0.1 --port 8010
  ```
- Navegador moderno compatible con estándares HTML5 y JavaScript ECMAScript 6+ (Chrome, Firefox, Safari, Edge).
- No requiere autenticación previa ni configuraciones adicionales de cookies o sesión; el estado de las pestañas se conmuta en el cliente de manera reactiva e inmediata.

---

## 3. Instrucciones de Uso Paso a Paso

### A. Acceso y Navegación entre Pestañas con Ratón o Táctil
1. Abre tu navegador e ingresa a `http://127.0.0.1:8010/`.
2. En la parte superior, debajo del encabezado principal, verás la barra horizontal con 4 pestañas identificadas con iconos claros:
   - `[📋 Panel General]` (activa por defecto al cargar).
   - `[👥 Concentrado Físico y Financiero]`.
   - `[📊 Informe Semanal de Cuotas y Cumplimiento]`.
   - `[📈 Estadísticas del Reto]`.
3. Haz clic sobre cualquiera de las pestañas:
   - El panel seleccionado se desplegará al instante.
   - La pestaña activa resaltará con borde inferior degradado y tipografía destacada.
   - Los otros tres paneles se ocultarán automáticamente (`display: none;` y `aria-selected="false"`), manteniendo intacta la información y sin recargar la página.

### B. Navegación Accesible por Teclado (Accesibilidad Universal)
El sistema cumple estrictamente con el patrón WAI-ARIA Tabs Design Pattern:
1. Presiona `Tab` desde la barra de direcciones hasta enfocar la barra de navegación por pestañas.
2. Utiliza las teclas de navegación:
   - `Flecha Derecha` (`ArrowRight`) o `Flecha Abajo` (`ArrowDown`): Mueve el foco a la pestaña siguiente de forma circular (al llegar a la cuarta, regresa a la primera).
   - `Flecha Izquierda` (`ArrowLeft`) o `Flecha Arriba` (`ArrowUp`): Mueve el foco a la pestaña anterior de forma circular.
   - `Inicio` (`Home`): Salta directamente a la primera pestaña (**Panel General**).
   - `Fin` (`End`): Salta directamente a la última pestaña (**Estadísticas del Reto**).
3. Al transferir el foco mediante teclado, el panel correspondiente se activa y se muestra automáticamente, actualizando `aria-selected="true"` y transfiriendo el foco al contenedor del panel para continuar la lectura accesible con lectores de pantalla.

### C. Uso Especializado de Cada Pestaña
- **Para registrar participantes o pagos**: Ve a la pestaña **Panel General**.
- **Para consultar estados de cuenta y saldos acumulados de los miembros**: Ve a la pestaña **Concentrado Físico y Financiero**.
- **Para auditar quién cumplió o no en una semana específica y quién va al corriente con las cuotas**: Ve a la pestaña **Informe Semanal de Cuotas y Cumplimiento** y selecciona la semana en el menú desplegable.
- **Para revisar quién lidera el podio deportivo DIDT**: Ve a la pestaña **Estadísticas del Reto**.

---

## 4. Ejemplos de Uso

### Flujo Principal: Navegación Completa entre Pestañas
```text
1. Usuario abre http://127.0.0.1:8010/
   -> Panel General visible: Formulario para registrar miembro o abono rápido.
   -> aria-selected="true" en #tab-general.

2. Usuario hace clic en "Concentrado Físico y Financiero"
   -> Se ejecuta switchTab('concentrado') sin recargar la página.
   -> #panel-general se oculta; #panel-concentrado se visualiza.
   -> Visualización completa de tabla de participantes con aportaciones, penalizaciones y ganancias.

3. Usuario presiona tecla 'ArrowRight'
   -> Foco avanza a #tab-informe.
   -> Se visualiza #panel-informe con selector de semanas 1 a 9 y tarjetas KPI.
   -> El usuario puede seleccionar la Semana 2 y visualizar el estado financiero y físico en tiempo real.

4. Usuario presiona tecla 'ArrowRight'
   -> Foco avanza a #tab-stats.
   -> Se visualiza #panel-stats con el podio Top 3, calorías totales y gráficos de barras.
```

---

## 5. Respuestas a Errores y Preguntas Frecuentes

| Mensaje de Error / Comportamiento | Causa | Como Resolverlo |
| :--- | :--- | :--- |
| Al hacer clic en una pestaña la página no cambia de vista | JavaScript se encuentra deshabilitado en el navegador o hubo una interrupción en la carga del script. | Verifica que JavaScript esté activado y refresca la ventana del navegador (`Ctrl + F5`). |
| No puedo navegar con las teclas de flecha | El foco del teclado no está situado sobre uno de los botones de la barra de pestañas. | Presiona la tecla `Tab` hasta que la pestaña activa reciba el foco del teclado; luego usa `ArrowRight` o `ArrowLeft`. |
| La pestaña de Informe Semanal muestra datos de una semana que aún no concluye | Se seleccionó una semana posterior a la fecha actual del reto. | El selector permite auditar tanto semanas ya liquidadas como semanas preliminares en curso con su respectivo badge informativo. |
| ¿Al cambiar de pestaña se pierden los datos escritos en un formulario no enviado? | No; el cambio de pestañas simplemente conmuta la visibilidad en el DOM sin recargar la página ni reiniciar los campos de texto. | Puedes regresar a la pestaña "Panel General" y continuar llenando el formulario sin pérdida de información. |
