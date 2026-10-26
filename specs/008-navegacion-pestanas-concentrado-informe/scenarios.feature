# language: es
Característica: Navegacion Modular por Pestañas del Dashboard Web (FEAT-008)
  Como Administrador y Miembro del Reto Fit 2026 (DIDT)
  Quiero navegar entre pestañas dedicadas para el Panel General, el Concentrado, el Informe Semanal y las Estadísticas
  Para tener una experiencia limpia, accesible y sin desplazamiento vertical excesivo

  @AC-8.1 @UI-UX
  Escenario: Despliegue de la barra de navegacion superior con cuatro pestanas
    Dado que el usuario carga el Dashboard Web
    Cuando inspecciona la barra superior de navegacion
    Entonces se muestran las 4 pestanas accesibles "Panel General", "Concentrado Físico y Financiero", "Informe Semanal de Cuotas y Cumplimiento" y "Estadísticas del Reto"
    Y la pestana "Panel General" se encuentra activa por defecto con aria-selected en verdadero

  @AC-8.2 @UI-UX
  Escenario: Visualizacion exclusiva del Concentrado Fisico y Financiero al activar su pestana
    Dado que el usuario se encuentra en el Dashboard Web
    Cuando activa la pestana "Concentrado Físico y Financiero"
    Entonces el panel "panel-concentrado" es visible con rol "tabpanel"
    Y los demas paneles se encuentran ocultos

  @AC-8.3 @UI-UX
  Escenario: Visualizacion del Informe Semanal al activar su pestana dedicada
    Dado que el usuario se encuentra en el Dashboard Web
    Cuando activa la pestana "Informe Semanal de Cuotas y Cumplimiento"
    Entonces el panel "panel-informe" es visible con el selector de semanas y tarjetas KPI
    Y los demas paneles permanecen ocultos

  @AC-8.4 @UI-UX
  Escenario: Soporte de navegacion por teclado entre las pestanas
    Dado que el usuario enfoca la barra de pestanas
    Cuando presiona la tecla de flecha derecha o flecha izquierda
    Entonces el foco se transfiere a la pestana siguiente o anterior de forma circular
    Y se actualizan los atributos tabindex y aria-selected correspondientes

  @AC-8.5 @UI-UX
  Escenario: Conmutacion instantanea de paneles sin recarga de pagina
    Dado que el usuario interactua con las pestanas del sistema
    Cuando alterna entre las distintas opciones
    Entonces cada cambio actualiza inmediatamente los roles ARIA y la visibilidad de los paneles
