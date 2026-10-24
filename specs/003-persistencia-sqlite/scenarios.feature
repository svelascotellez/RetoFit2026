# language: es
Característica: FEAT-003 - Persistencia de Datos en SQLite para Reto Fit

  @AC-3.1
  Escenario: Persistencia inmediata de registro de participante
    Dado una base de datos SQLite inicializada y limpia
    Cuando se registra un participante con ID "didt-10" y nombre "Elena Rivas"
    Entonces el participante "didt-10" debe existir en la base de datos con nombre "Elena Rivas"

  @AC-3.2
  Escenario: Persistencia de aportaciones economicas
    Dado un participante "didt-10" registrado en SQLite
    Cuando se registra un abono de 200.0 pesos para "didt-10"
    Entonces el total aportado en SQLite para "didt-10" debe ser 200.0 pesos

  @AC-3.3
  Escenario: Persistencia de actividad fisica diaria
    Dado un participante "didt-10" registrado en SQLite
    Cuando se registra una actividad fisica en la semana 1 dia 1 con 350 calorias y 4000 pasos para "didt-10"
    Entonces la actividad fisica debe quedar registrada en SQLite indicando dia exitoso

  @AC-3.4
  Escenario: Persistencia de cierre y liquidacion semanal
    Dado un participante cumplidor y un participante incumplidor en SQLite para la semana 1
    Cuando se ejecuta el cierre de la semana 1 en SQLite
    Entonces el registro del cierre semanal 1 debe persistir con bolsa de 100.0 pesos

  @AC-3.5
  Escenario: Rehidratacion completa del estado tras reinicio del servicio
    Dado una base de datos SQLite con participantes, pagos y actividades previas
    Cuando se inicializa una nueva instancia de ChallengeService conectada a la misma base de datos
    Entonces el nuevo servicio debe restaurar todos los participantes con sus saldos y estados intactos

  @AC-3.6
  Escenario: Creacion automatica del esquema SQLite si no existe
    Dado que el archivo de base de datos no existe previamente en disco
    Cuando se inicializa el repositorio SQLite
    Entonces el archivo de base de datos y todas sus tablas deben ser creados exitosamente
