# Guia de Usuario: FEAT-004 - Edicion y Gestion de Registros de Reto Fit

## 1. Descripcion General
Esta funcionalidad permite a los administradores y miembros del Reto Fit corregir datos capturados erróneamente sin necesidad de reiniciar la aplicación ni manipular manualmente la base de datos:
- **Editar el nombre** de un participante manteniendo su ID, aportaciones y actividades.
- **Eliminar a un participante** dado de baja o registrado por duplicado, removiendo en cascada todos sus abonos y actividades asociadas de SQLite y memoria.
- **Anular la última aportación quincenal** registrada por error, reduciendo el total acumulado y liberando el contador de aportaciones.
- **Restablecer / limpiar la actividad diaria** de un participante para un día y semana específicos si se ingresaron pasos o calorías equivocadas.

## 2. Requisitos Previos y Configuracion
- El servidor de Reto Fit debe estar en ejecución:
  ```powershell
  python -m uvicorn src.main:app --host 0.0.0.0 --port 8010 --reload
  ```
- Acceder al Dashboard Web mediante el navegador: [http://localhost:8010](http://localhost:8010).

## 3. Instrucciones de Uso Paso a Paso

### 3.1. Editar el Nombre de un Participante
1. En la tabla del concentrado, localiza la fila del miembro que deseas corregir.
2. Haz clic en el botón **`✏️ Editar`**.
3. Se abrirá una ventana de diálogo solicitando el nuevo nombre. Escribe el nombre corregido (por ejemplo: `Carlos Méndez`) y presiona **Aceptar**.
4. El sistema actualizará el nombre en memoria y en la base de datos SQLite inmediatamente, mostrando una notificación de confirmación y recargando la tabla.

### 3.2. Eliminar un Participante (Borrado en Cascada)
1. En la fila del participante a remover, haz clic en el botón rojo con ícono de papelera **`🗑️`**.
2. Aparecerá el **Modal Accesible de Confirmación**: *"¿Estás seguro de que deseas eliminar permanentemente a [Nombre]? Se eliminarán también en cascada todos sus abonos y actividades."*
3. Presiona **Confirmar**. El participante y todos sus registros desaparecerán de SQLite y el concentrado financiero general se recalculará automáticamente.

### 3.3. Anular el Último Abono Quincenal
1. Si registraste un abono de más o por error, localiza la fila del participante y haz clic en **`↩️ Anular`**.
2. Confirma la acción en el cuadro de diálogo.
3. El sistema descontará la última aportación de $200 de SQLite y de memoria, permitiendo registrar la quincena correcta posteriormente.

### 3.4. Restablecer / Limpiar Actividad Diaria
1. En la tarjeta de **Actividad Física Diaria**, ingresa el **ID Miembro**, la **Semana (1-9)** y el **Día (1-7)** que deseas restablecer.
2. Haz clic en el botón **`Limpiar`**.
3. Confirma la acción. El registro de calorías y pasos de ese día quedará eliminado tanto en SQLite como en memoria, actualizando los días exitosos semanales.

## 4. Ejemplos de Uso
### Modificación de Nombre via API REST
```bash
curl -X PUT http://localhost:8010/api/participants/didt-01 \
  -H "Content-Type: application/json" \
  -d '{"name": "Carlos Mendez"}'
```
Respuesta esperada (HTTP 200):
```json
{
  "id": "didt-01",
  "name": "Carlos Mendez",
  "total_contributed": 200.0,
  "target_contribution": 1000.0
}
```

### Anulación de Abono via API REST
```bash
curl -X DELETE http://localhost:8010/api/participants/didt-01/payments/last
```
Respuesta esperada (HTTP 200):
```json
{
  "success": true,
  "removed_amount": 200.0,
  "total_contributed": 0.0,
  "message": "Abono de $200.00 anulado exitosamente"
}
```

## 5. Respuestas a Errores y Preguntas Frecuentes
| Mensaje de Error / Comportamiento | Causa | Como Resolverlo |
| :--- | :--- | :--- |
| `El nombre no puede estar vacio` (HTTP 422) | Se envió una cadena vacía o solo espacios al actualizar el nombre. | Ingresa un nombre con al menos un carácter visible. |
| `Participante ... no encontrado` (HTTP 404) | El ID del participante no existe en el sistema. | Verifica el ID en la tabla general de concentrado antes de ejecutar la acción. |
| `El participante no tiene aportaciones registradas` (HTTP 400) | Se intentó anular un abono a un miembro que tiene $0.00 aportados. | No es necesario anular; el participante no tiene pagos pendientes. |
| ¿Se pueden modificar semanas ya cerradas? | No. Los cierres y liquidaciones de bolsa son definitivos para proteger la distribución contable de las ganancias. | Realiza las correcciones de actividad antes de presionar el botón "Liquidar Semana". |
