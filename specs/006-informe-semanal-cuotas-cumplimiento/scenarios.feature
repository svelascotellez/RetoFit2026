# language: es
Característica: Informe Semanal de Cuotas y Cumplimiento del Reto (FEAT-006)
  Como Administrador y Miembro del Reto Fit 2026 (DIDT)
  Quiero consultar un informe semanal de cuotas y cumplimiento físico
  Para evaluar el avance del reto, auditar las aportaciones del calendario y revisar la bolsa de penalizaciones

  @AC-6.1
  Escenario: Calculo de cumplimiento fisico y penalizaciones para una semana valida
    Dado que existen participantes registrados en el reto
    Y el participante "P1" registra 4 dias exitosos en la semana 1
    Y el participante "P2" registra 2 dias exitosos en la semana 1
    Cuando se genera el informe de la semana 1
    Entonces el participante "P1" se reporta con cumplimiento exitoso y penalizacion de 0.0 pesos
    Y el participante "P2" se reporta como no cumplido con penalizacion de 100.0 pesos

  @AC-6.2
  Escenario: Determinacion de cuotas exigibles y estatus financiero segun calendario
    Dado que el participante "P1" tiene abonos acumulados por 200.0 pesos
    Y el participante "P2" tiene abonos acumulados por 100.0 pesos
    Cuando se genera el informe de cuotas para la semana 1
    Entonces la cuota exigible acumulada para la semana 1 es de 200.0 pesos
    Y el participante "P1" tiene estatus de cuota "AL_CORRIENTE" con saldo pendiente de 0.0 pesos
    Y el participante "P2" tiene estatus de cuota "PENDIENTE" con saldo pendiente de 100.0 pesos

  @AC-6.3
  Escenario: Rechazo de solicitud para semanas invalidas fuera de rango
    Dado que el sistema tiene el rango de semanas entre 1 y 9
    Cuando se solicita el informe de la semana 0 o de la semana 10
    Entonces el sistema responde con error de semana invalida

  @AC-6.4
  Escenario: Consulta del informe semanal consolidado a traves del endpoint REST
    Dado que la aplicacion API esta disponible con datos de participantes
    Cuando se realiza una peticion GET al endpoint "/api/reports/weekly/1"
    Entonces la API responde con codigo 200 y el esquema contiene la tasa de cumplimiento y el detalle de cuotas

  @AC-6.5 @UI-UX
  Escenario: Seccion interactiva de informe semanal en el Dashboard Web
    Dado que el usuario accede al Dashboard Web
    Cuando visualiza la tarjeta de informe semanal
    Entonces se presenta un selector de semana del 1 al 9 y una tabla accesible con indicadores de cumplimiento y aportacion

  @AC-6.6 @UI-UX
  Escenario: Manejo de estado vacio accesible sin participantes
    Dado que no existen participantes registrados en el sistema
    Cuando se consulta la vista del informe semanal en el Dashboard Web
    Entonces se visualiza el estado vacio accesible con rol "status" indicando ausencia de datos
