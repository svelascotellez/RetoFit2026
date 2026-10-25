# language: es
Característica: Edicion y Gestion de Registros de Reto Fit (FEAT-004)
  Como Administrador y Miembro del Reto Fit 2026 (DIDT)
  Quiero corregir nombres, anular abonos erróneos y eliminar registros de actividad o participantes
  Para mantener la integridad contable y la precisión de los datos del reto

  @AC-4.1
  Escenario: Modificacion exitosa del nombre de un participante registrado
    Dado que existe un participante con id "DEV-01" y nombre "Carlos"
    Cuando se solicita actualizar el nombre a "Carlos Mendez"
    Entonces el participante refleja el nuevo nombre "Carlos Mendez" en el sistema y en SQLite

  @AC-4.2
  Esquema del escenario: Rechazo de actualizacion de nombre invalido o vacio
    Dado que existe un participante con id "DEV-02" y nombre "Ana"
    Cuando se solicita actualizar el nombre con el valor "<nombre_invalido>"
    Entonces el sistema rechaza la solicitud con codigo 422 y mantiene el nombre "Ana"

    Ejemplos:
      | nombre_invalido |
      |                 |
      |       \t        |

  @AC-4.3
  Escenario: Eliminacion en cascada de un participante y sus registros asociados
    Dado que existe un participante con id "DEV-03" con abonos y actividades registradas
    Cuando se solicita eliminar al participante con id "DEV-03"
    Entonces el participante y todos sus pagos y actividades son eliminados de SQLite y del resumen general

  @AC-4.4
  Escenario: Anulacion de un abono quincenal registrado por error
    Dado que el participante "DEV-04" tiene un abono registrado de 200.0 pesos
    Cuando se solicita eliminar el abono de 200.0 pesos del participante "DEV-04"
    Entonces el total aportado del participante disminuye a 0.0 pesos y el pago no existe en SQLite

  @AC-4.5
  Escenario: Restablecimiento o eliminacion de actividad diaria capturada por error
    Dado que el participante "DEV-05" tiene una actividad de 450 kcal y 11000 pasos en la semana 1 dia 2
    Cuando se solicita eliminar la actividad del participante "DEV-05" para la semana 1 dia 2
    Entonces el dia 2 de la semana 1 queda sin registro de actividad y no suma como dia exitoso

  @AC-4.6 @UI-UX
  Escenario: Interaccion accesible para confirmacion de borrado y estados de control
    Dado que el usuario accede al Dashboard Web del Reto Fit
    Cuando abre el dialogo de confirmacion para eliminar un registro
    Entonces el dialogo expone el rol accesible "dialog" con opciones de cancelar y confirmar la accion destructiva
