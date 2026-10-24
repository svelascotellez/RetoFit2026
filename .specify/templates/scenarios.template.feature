# language: es
Caracteristica: {FEATURE_NAME} ({FEATURE_ID})
  Como {ROL}
  Quiero {ACCION}
  Para {BENEFICIO}

  @AC-1.1
  Escenario: Ejecucion exitosa del flujo principal
    Dado {precondicion inicial}
    Cuando {accion ejecutada}
    Entonces {resultado esperado}

  @AC-1.2
  Esquema del escenario: Manejo de errores y casos invalidos
    Dado {precondicion inicial}
    Cuando ingresa datos con error en "<campo>" y valor "<valor>"
    Entonces el sistema responde con error "<mensaje_esperado>"

    Ejemplos:
      | campo | valor | mensaje_esperado |
      | email | inval | Email invalido   |

  # REGLA UI/UX EN BDD: Validar interaccion accesible y estados (roles ARIA, teclado, vacio, carga); NUNCA clases CSS cosmeticas.
  @AC-1.3 @UI-UX
  Escenario: Feedback visual accesible y manejo de estado vacio
    Dado que el usuario navega a la vista de "{FEATURE_NAME}"
    Cuando no existen datos registrados en el sistema
    Entonces se muestra el estado vacio accesible con rol "status" y sugerencia de accion