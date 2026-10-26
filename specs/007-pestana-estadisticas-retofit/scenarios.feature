# language: es
Característica: Pestaña de Estadísticas Integrales del Reto Fit (FEAT-007)
  Como Administrador y Miembro del Reto Fit 2026 (DIDT)
  Quiero consultar estadísticas consolidadas y ranking del reto
  Para monitorear el progreso físico colectivo, el avance deportivo y la analítica de la bolsa

  @AC-7.1
  Escenario: Calculo de metricas globales de calorias y pasos acumulados
    Dado que existen participantes con actividades registradas en el reto
    Cuando se calculan las estadisticas globales del reto
    Entonces el total de calorias y el total de pasos reflejan la suma de todas las actividades
    Y se calculan los promedios diarios correspondientes

  @AC-7.2
  Escenario: Generacion de ranking de participantes por dias exitosos y calorias
    Dado que el participante "P1" tiene 8 dias exitosos y 2800 calorias acumuladas
    Y el participante "P2" tiene 10 dias exitosos y 3200 calorias acumuladas
    Y el participante "P3" tiene 8 dias exitosos y 3100 calorias acumuladas
    Cuando se genera la tabla de ranking de participantes
    Entonces el participante "P2" ocupa la posicion 1
    Y el participante "P3" ocupa la posicion 2 por desempate de calorias
    Y el participante "P1" ocupa la posicion 3

  @AC-7.3
  Escenario: Calculo de tendencias de cumplimiento semanal
    Dado que se han registrado actividades y cierres de semana en el sistema
    Cuando se evalua la tendencia de las 9 semanas del reto
    Entonces se obtienen las metricas semanales con dias exitosos y participantes cumplidores

  @AC-7.4
  Escenario: Consulta de estadisticas completas a traves del endpoint REST
    Dado que el servicio de estadisticas esta disponible
    Cuando se envia una peticion GET al endpoint "/api/statistics"
    Entonces la API responde con codigo 200 y el esquema de estadisticas globales y ranking

  @AC-7.5 @UI-UX
  Escenario: Navegacion por pestanas interactiva en el Dashboard Web
    Dado que el usuario carga el Dashboard Web
    Cuando observa la barra de navegacion con pestanas
    Entonces existen las pestanas accesibles "Panel General" y "Estadísticas del Reto" con roles "tab" y contenedor "tabpanel"

  @AC-7.6 @UI-UX
  Escenario: Estado vacio accesible en la pestana de estadisticas sin actividades
    Dado que no existen actividades fisicas registradas en el reto
    Cuando el usuario activa la pestana de "Estadísticas del Reto"
    Entonces se visualiza el estado vacio accesible con rol "status" informando la falta de actividad
