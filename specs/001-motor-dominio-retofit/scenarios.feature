# language: es
Característica: Motor de Dominio del Reto Fit (FEAT-001)
  Como Administrador y Participante del Reto Fit DIDT
  Quiero registrar cumplimiento de actividad física, aportaciones y penalizaciones
  Para calcular equitativamente la bolsa semanal y el concentrado financiero

  @AC-1.1
  Esquema del escenario: Determinacion de dia exitoso por calorias o pasos
    Dado un participante registrado "Carlos"
    Cuando registra en un dia "<calorias>" calorias y "<pasos>" pasos
    Entonces el estado del dia se determina como "<resultado>"

    Ejemplos:
      | calorias | pasos | resultado |
      | 350      | 5000  | exitoso   |
      | 150      | 10500 | exitoso   |
      | 300      | 10000 | exitoso   |
      | 250      | 8000  | no_exitoso|

  @AC-1.2
  Esquema del escenario: Evaluacion de cumplimiento semanal con base en dias exitosos
    Dado un participante registrado con "<dias_exitosos>" dias exitosos en la semana
    Cuando se evalua el cumplimiento de la semana
    Entonces el resultado semanal es "<cumplio>"

    Ejemplos:
      | dias_exitosos | cumplio    |
      | 4             | cumplido   |
      | 6             | cumplido   |
      | 3             | incumplido |
      | 0             | incumplido |

  @AC-1.3
  Escenario: Aplicacion de penalizacion de $100 al participante que incumple
    Dado un participante "Ana" que incumplio la meta de la semana 1
    Cuando se procesa el cierre de la semana 1
    Entonces se aplica una penalizacion de 100 pesos a "Ana"
    Y la bolsa semanal de penalizaciones recibe 100 pesos

  @AC-1.4
  Escenario: Reparto equitativo de la bolsa semanal entre participantes cumplidores
    Dado que en la semana 1 tres participantes incumplieron generando 300 pesos en la bolsa
    Y dos participantes "Luis" y "Sofia" si cumplieron el reto
    Cuando se liquida la bolsa de la semana 1
    Entonces cada participante cumplidor recibe 150 pesos de ganancia adicional

  @AC-1.5
  Escenario: Traslado de bolsa desierta a la siguiente semana cuando nadie cumple
    Dado que en la semana 2 los cuatro participantes registrados incumplieron el reto
    Y la bolsa semanal acumula 400 pesos de penalizaciones
    Cuando se liquida la semana 2 sin cumplidores
    Entonces la bolsa acumulada de 400 pesos se traslada como fondo inicial para la semana 3

  @AC-1.6
  Escenario: Registro de aportaciones economicas hasta 1000 pesos
    Dado un participante "Jorge" recien inscrito
    Cuando abona un pago de aportacion de 200 pesos
    Entonces el saldo aportado de "Jorge" es de 200 pesos de un total de 1000 pesos

  @AC-1.7
  Escenario: Calculo del concentrado financiero individual y general
    Dado un participante "Maria" que aporto 1000 pesos en total
    Y "Maria" cumplio 7 semanas e incumplio 2 semanas
    Y recibio 350 pesos por reparto de bolsas semanales
    Cuando se genera el concentrado financiero de "Maria"
    Entonces el total penalizado es de 200 pesos
    Y el monto neto final a recibir es de 1150 pesos

  @AC-1.8
  Esquema del escenario: Rechazo de valores negativos en actividad y aportaciones
    Dado un participante registrado en el sistema
    Cuando intenta registrar "<campo>" con valor invalido "<valor>"
    Entonces el sistema rechaza la transaccion con error de dominio "<mensaje>"

    Ejemplos:
      | campo       | valor | mensaje                          |
      | calorias    | -50   | Calorias no pueden ser negativas |
      | pasos       | -100  | Pasos no pueden ser negativos    |
      | aportacion  | -200  | Monto debe ser mayor a cero      |
