# Guia de Usuario: FEAT-005 - Ajuste de Cuota Financiera y Calendario de Aportaciones

## 1. Descripcion General
Esta funcionalidad actualiza el calendario y la meta total de aportación financiera del **Reto Fit 2026 (DIDT)** a **$900.00 MXN** distribuidos en 5 fechas oficiales:
- El reto consta de **9 semanas en total** (del 19 de octubre al 20 de diciembre de 2026).
- Las primeras 4 quincenas cubren 2 semanas cada una con cuotas de **$200.00 MXN** ($800.00 acumulados).
- La quinta aportación del **14 de diciembre** cubre únicamente la **semana 9 final** (del 14 al 20 de diciembre), por lo que su monto es de solo **$100.00 MXN**.
- Total acumulado por participante: $200 x 4 + $100 x 1 = **$900.00 MXN**.
- Se incorporan botones de acceso rápido `[+ $200]` y `[+ $100]` en la tabla del concentrado para facilitar el registro de ambos tipos de cuotas con un solo clic.

## 2. Calendario Oficial de Fechas y Cuotas
| # | Fecha Oficial | Periodo Cubierto | Monto Cuota | Monto Acumulado |
|---|---|---|---|---|
| 1 | 19 de octubre | Semanas 1 y 2 | $200.00 MXN | $200.00 MXN |
| 2 | 2 de noviembre | Semanas 3 y 4 | $200.00 MXN | $400.00 MXN |
| 3 | 16 de noviembre | Semanas 5 y 6 | $200.00 MXN | $600.00 MXN |
| 4 | 30 de noviembre | Semanas 7 y 8 | $200.00 MXN | $800.00 MXN |
| 5 | 14 de diciembre | Semana 9 (Final) | **$100.00 MXN** | **$900.00 MXN** |

## 3. Instrucciones de Uso en el Dashboard Web

### 3.1. Consulta del Calendario y Métricas Financieras
1. Abre tu navegador web en [http://localhost:8010](http://localhost:8010).
2. En la sección superior del Bento Grid, verifica la tarjeta **Fondo Total Aportado**, la cual ahora indica:
   *"Meta total: 4 quincenas de $200 + 1 semana de $100 = $900 por miembro."*
3. En la tarjeta **Fechas de Aportación ($900.00)**, revisa el listado de las 5 fechas oficiales donde el abono del **14 de diciembre (1 sem)** muestra claramente **$100.00**.

### 3.2. Abono Rápido de Cuotas Quincenales ($200) y Cuota Final ($100)
1. En la tabla del **Concentrado de Participantes**, localiza la fila del miembro que desea abonar.
2. La columna de aportación ahora muestra el avance respecto a la meta actualizada: `${total} / $900.00`.
3. Para registrar una de las primeras 4 quincenas normales, haz clic en el botón naranja **`+ $200`**.
4. Para registrar la aportación final correspondiente a la semana 9, haz clic en el botón naranja **`+ $100`**.
5. El sistema registrará el abono inmediatamente en SQLite y memoria, mostrará una notificación confirmando el saldo y recargará la tabla automáticamente.

### 3.3. Formulario Manual de Abonos
1. Si prefieres abonar a través del formulario **Abonar Pago Quincenal**:
2. Ingresa el ID del miembro (ej. `didt-01`).
3. En el campo **Monto a Abonar (MXN)** ingresa `200.00` o `100.00` según corresponda.
4. Presiona el botón **💳 Abonar Pago Quincenal**.

## 4. Ejemplos de Uso via API REST

### Consulta de Participante con Meta de $900.00 MXN
```bash
curl -X GET http://localhost:8010/api/participants/didt-01
```
Respuesta esperada (HTTP 200):
```json
{
  "id": "didt-01",
  "name": "Mariana Lopez",
  "total_contributed": 800.0,
  "target_contribution": 900.0
}
```

### Registro de la Aportación Final de $100.00 MXN
```bash
curl -X POST http://localhost:8010/api/payments \
  -H "Content-Type: application/json" \
  -d '{"participant_id": "didt-01", "amount": 100.0}'
```
Respuesta esperada (HTTP 201):
```json
{
  "participant_id": "didt-01",
  "total_contributed": 900.0,
  "target_contribution": 900.0
}
```

## 5. Solucion de Problemas y Preguntas Frecuentes
- **¿Qué pasa si un participante ya aportó $1,000 por error?**  
  Puedes usar el botón **`↩️ Anular`** en la tabla para remover el último abono registrado, o registrar un ajuste según el acuerdo de los organizadores.
- **¿Cuántas aportaciones permite el sistema en total?**  
  El límite se mantiene en un máximo de **5 aportaciones** oficiales. Al completarse los 4 abonos de $200 y el abono final de $100, el saldo aportado del participante alcanzará exactamente los **$900.00 MXN**.
