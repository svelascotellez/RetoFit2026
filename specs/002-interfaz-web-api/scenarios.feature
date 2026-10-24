# language: es
Característica: Interfaz Web y API FastAPI para Reto Fit (FEAT-002)
  Como Administrador y Participante del Reto Fit DIDT
  Quiero acceder a endpoints REST y a la aplicacion web interactiva
  Para gestionar el evento y visualizar el concentrado general en Railway

  @AC-2.1
  Escenario: Consulta del concentrado general mediante API REST
    Dado que el sistema tiene participantes registrados con aportaciones
    Cuando el cliente envia una solicitud GET a "/api/summary"
    Entonces la respuesta tiene codigo de estado 200
    Y el cuerpo contiene "total_participants" y "total_funds_collected"

  @AC-2.2
  Escenario: Registro exitoso de un nuevo participante via API
    Dado que no existe un participante con id "p10"
    Cuando el cliente envia una solicitud POST a "/api/participants" con id "p10" y nombre "Laura Mendez"
    Entonces la respuesta tiene codigo de estado 201
    Y el cuerpo confirma el registro de "Laura Mendez"

  @AC-2.3
  Escenario: Registro de aportacion economica via API
    Dado un participante existente con id "p10"
    Cuando el cliente envia una solicitud POST a "/api/payments" con monto 200 para "p10"
    Entonces la respuesta tiene codigo de estado 200
    Y el saldo aportado retornado es 200

  @AC-2.4
  Esquema del escenario: Registro de actividad fisica diaria via API
    Dado un participante existente con id "p10"
    Cuando el cliente registra actividad en semana 1 dia 1 con "<calorias>" calorias y "<pasos>" pasos
    Entonces la respuesta tiene codigo de estado 200
    Y la respuesta indica que el dia fue "<exitoso>"

    Ejemplos:
      | calorias | pasos | exitoso |
      | 350      | 2000  | true    |
      | 100      | 11000 | true    |
      | 200      | 5000  | false   |

  @AC-2.5
  Escenario: Cierre y liquidacion semanal via API
    Dado participantes registrados en la semana 1 con actividades evaluadas
    Cuando el administrador envia una solicitud POST a "/api/weeks/1/close"
    Entonces la respuesta tiene codigo de estado 200
    Y el cuerpo de la liquidacion contiene "gain_per_participant" y "rollover_to_next"

  @AC-2.6
  Escenario: Endpoint de verificacion de salud para Railway
    Dado que el servicio FastAPI esta en ejecucion
    Cuando se solicita el estado de salud en "/health"
    Entonces la respuesta tiene codigo de estado 200
    Y el estado reportado es "healthy"

  @AC-2.7 @UI-UX
  Escenario: Servir la aplicacion web interactiva en la ruta raiz
    Dado que el servidor web esta activo
    Cuando un usuario navega a la ruta "/"
    Entonces la respuesta tiene codigo de estado 200
    Y contiene encabezados HTML con el diseno del Reto Fit

  @AC-2.8
  Esquema del escenario: Manejo de errores y validaciones en la API
    Dado que el servicio API esta disponible
    Cuando se envia una peticion invalida a "<endpoint>" con cuerpo "<payload>"
    Entonces la respuesta de error tiene codigo "<codigo_error>"

    Ejemplos:
      | endpoint          | payload                                    | codigo_error |
      | /api/payments     | {"participant_id": "inexistente", "amount": 100} | 404          |
      | /api/payments     | {"participant_id": "p10", "amount": -50}   | 400          |
      | /api/participants | {"id": "p10", "name": ""}                  | 422          |

  @AC-2.9 @UI-UX
  Escenario: Estado vacio accesible cuando no hay participantes registrados
    Dado que no hay participantes registrados en el sistema
    Cuando se consulta la vista web principal
    Entonces se presenta un mensaje accesible con rol "status" indicando que no hay participantes
