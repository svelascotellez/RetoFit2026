# Guia de Usuario: FEAT-003 - Persistencia de Datos en SQLite para Reto Fit

## 1. Descripcion General
La funcionalidad **Persistencia de Datos en SQLite para Reto Fit** dota al sistema de almacenamiento duradero y transaccional mediante una base de datos local SQLite (`data/retofit.db`).

Con esta implementación:
- **Sobrevivencia a Reinicios:** Todos los miembros inscritos, aportaciones económicas quincenales hacia la cuota de $1,000 MXN, registros diarios de ejercicio (calorías/pasos) y liquidaciones semanales de bolsa se guardan de forma instantánea en disco.
- **Tolerancia a Recargas en Caliente (`--reload`):** Cuando el desarrollador o administrador actualiza archivos o Uvicorn reinicia el proceso, el sistema rehidrata y restaura automáticamente el estado completo en memoria en menos de 5 milisegundos.
- **Cero Configuración:** La base de datos, el directorio `data/` y todas las tablas requeridas se generan automáticamente al iniciar el servicio por primera vez.

---

## 2. Requisitos Previos y Configuracion

### Dependencias
- **Python:** Versión 3.11 o superior (incluye el módulo estándar `sqlite3` de fábrica, sin requerir drivers externos).
- **Ruta del Archivo:** Por defecto se almacena en `data/retofit.db`.

### Variable de Entorno Opcional
- `RETOFIT_DB_PATH`: Permite sobreescribir la ubicación del archivo SQLite (por ejemplo, para pruebas automatizadas o entornos de almacenamiento persistente en la nube como volúmenes Railway):
  ```powershell
  $env:RETOFIT_DB_PATH = "data/retofit.db"
  ```

---

## 3. Instrucciones de Uso Paso a Paso

### Paso 1: Iniciar el Servidor con Persistencia
Inicia el servicio en PowerShell de manera habitual:
```powershell
python -m uvicorn src.main:app --host 0.0.0.0 --port 8010 --reload
```
Al arrancar, el sistema verificará si existe `data/retofit.db`. Si no existe, creará la estructura de tablas automáticamente.

### Paso 2: Registrar Datos en el Dashboard Web
1. Ingresa a [http://localhost:8010/](http://localhost:8010/).
2. Inscribe a los participantes de la DIDT (ej. `didt-01`, `Ana Gomez`).
3. Registra sus aportaciones quincenales (ej. `$200.00`).
4. Carga las actividades diarias (ej. Semana 1, Día 1, 350 kcal).
5. Cada operación se confirma tanto en pantalla como de forma síncrona en el archivo SQLite.

### Paso 3: Comprobar la Supervivencia de Datos ante Reinicios
1. Detén el servidor en la terminal presionando `Ctrl + C`.
2. Vuelve a iniciarlo con:
   ```powershell
   python -m uvicorn src.main:app --host 0.0.0.0 --port 8010 --reload
   ```
3. Refresca tu navegador en [http://localhost:8010/](http://localhost:8010/).
4. Comprobarás que **todos los participantes, aportaciones y balances permanecen exactamente iguales**, sin pérdida de información.

### Paso 4: Respaldar o Trasladar la Informacion
Para generar un respaldo de seguridad del Reto Fit, basta con copiar el archivo:
```powershell
Copy-Item data\retofit.db data\retofit_backup.db
```

---

## 4. Ejemplos de Uso

### 4.1 Uso Programático desde Python (Capa de Aplicación e Infraestructura)
```python
from src.infrastructure.sqlite_repository import SQLiteChallengeRepository
from src.application.challenge_service import ChallengeService
from src.application.dto import RegisterParticipantDTO, RecordPaymentDTO

# Inicializar repositorio SQLite en disco
repo = SQLiteChallengeRepository(db_path="data/retofit.db")

# Inyectar al servicio orquestador (rehidrata el estado automáticamente)
service = ChallengeService(repository=repo)

# Registrar participante (se guarda en memoria y en SQLite)
service.register_participant(RegisterParticipantDTO(id="p1", name="Carlos Ruiz"))

# Registrar abono quincenal de $200
service.record_payment(RecordPaymentDTO(participant_id="p1", amount=200.0))

print(f"Total acumulado: ${service.get_participant_summary('p1').total_contributed}")
```

### 4.2 Inspección Directa de Tablas SQLite
Puedes consultar las tablas con cualquier visor SQLite o mediante PowerShell:
```powershell
python -c "import sqlite3; conn = sqlite3.connect('data/retofit.db'); print(conn.execute('SELECT * FROM participants;').fetchall())"
```

---

## 5. Respuestas a Errores y Preguntas Frecuentes

| Mensaje de Error / Comportamiento | Causa | Como Resolverlo |
| :--- | :--- | :--- |
| `sqlite3.OperationalError: unable to open database file` | Permisos insuficientes en el directorio o ruta de disco bloqueada. | Verifique que el usuario tenga permisos de escritura en la carpeta `data/` del proyecto. |
| `sqlite3.IntegrityError: UNIQUE constraint failed: participants.id` | Intento de registrar dos veces el mismo ID de participante. | Utilice un ID único para cada miembro o consulte el listado en el dashboard. |
| Los datos no se visualizan tras reiniciar el servidor. | Se eliminó manualmente el archivo `data/retofit.db` o la variable `RETOFIT_DB_PATH` apunta a otra ruta. | Compruebe la existencia de `data/retofit.db` en el directorio raíz. |
| ¿Qué ocurre si se apaga el servidor a mitad de una transacción? | SQLite utiliza transacciones ACID con `commit` atómico. | No habrá estados corruptos; la operación incompleta se revierte automáticamente (*rollback*). |
