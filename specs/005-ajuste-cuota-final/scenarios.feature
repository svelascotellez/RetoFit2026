# language: es
Característica: Ajuste de Cuota Financiera y Calendario de Aportaciones (FEAT-005)
  Como Administrador y Miembro del Reto Fit 2026 (DIDT)
  Quiero que la cuota total de aportación sea de $900.00 MXN en 5 abonos (4 de $200 y el final de $100)
  Para ajustar el balance al total real de 9 semanas del evento

  @AC-5.1
  Escenario: Meta de aportacion fijada en 900 pesos por participante
    Dado que se crea un nuevo participante con id "MEM-01" y nombre "Mariana"
    Cuando se consulta la meta de aportacion del participante
    Entonces la meta de aportacion es de 900.0 pesos

  @AC-5.2
  Escenario: Acumulacion de abonos hacia la meta de 900 pesos
    Dado que el participante "MEM-02" tiene 4 abonos de 200.0 pesos registrados
    Cuando registra su quinto y ultimo abono por 100.0 pesos
    Entonces el total aportado del participante alcanza exactamente 900.0 pesos

  @AC-5.3
  Escenario: Calendario oficial de fechas de pago en el Dashboard Web
    Dado que el usuario accede al Dashboard Web
    Cuando revisa la seccion del calendario de aportaciones
    Entonces se visualizan las fechas oficiales sumando un total de 900.0 pesos con el 14 de diciembre en 100.0 pesos

  @AC-5.4 @UI-UX
  Escenario: Disponibilidad de botones de abono rapido en la interfaz
    Dado que el usuario visualiza la tabla de participantes en el Dashboard Web
    Cuando observa las acciones de cada participante
    Entonces estan disponibles botones de acceso rapido tanto para "+ $200" como para "+ $100"

  @AC-5.5
  Escenario: Endpoint de API retorna cuota objetivo de 900 pesos
    Dado que se consulta el concentrado general a traves de la API en "/api/summary"
    Cuando la API responde exitosamente
    Entonces los esquemas de participante reflejan la meta de 900.0 pesos
