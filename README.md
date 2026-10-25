# 🏋️‍♂️ RetoFit 2026 — DIDT

Sistema de Gestión Físico y Financiero para el evento **RetoFit 2026** de la **Dirección de Informática y Desarrollo Tecnológico (DIDT)**. Desarrollado bajo **Clean Architecture**, **Spec-Driven Development (SDD v4.3)** y **Behavior-Driven Development (BDD)**.

---

## 📋 Índice
- [Descripción General](#-descripción-general)
- [Reglas del Reto Fit](#-reglas-del-reto-fit)
  - [Objetivos Físicos Semanales](#objetivos-físicos-semanales)
  - [Esquema Financiero y Calendario](#esquema-financiero-y-calendario)
  - [Dinámica de la Bolsa y Penalizaciones](#dinámica-de-la-bolsa-y-penalizaciones)
- [Funcionalidades Implementadas](#-funcionalidades-implementadas)
- [Arquitectura de Software](#-arquitectura-de-software)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Instalación y Puesta en Marcha](#-instalación-y-puesta-en-marcha)
- [Uso de la Aplicación](#-uso-de-la-aplicación)
  - [Dashboard Web Interactivo](#dashboard-web-interactivo)
  - [Documentación Interactiva de la API](#documentación-interactiva-de-la-api)
- [Pruebas y Aseguramiento de Calidad](#-pruebas-y-aseguramiento-de-calidad)
- [Documentación y Guías de Usuario](#-documentación-y-guías-de-usuario)

---

## 🎯 Descripción General

**RetoFit 2026** es una iniciativa de bienestar y acondicionamiento físico de 9 semanas (del **19 de octubre al 20 de diciembre de 2026**) para el equipo de la DIDT. La plataforma permite:
- Registrar y monitorear la actividad física diaria (calorías y pasos).
- Controlar aportaciones económicas y cuotas quincenales.
- Liquidar semanalmente la bolsa de penalizaciones y ganancias de manera contable y transparente.
- Gestionar participantes, editar datos erróneos y restablecer registros con persistencia transaccional en SQLite.

---

## ⚖️ Reglas del Reto Fit

### Objetivos Físicos Semanales
- **Criterio de Día Exitoso:** Cada participante debe registrar en el día al menos:
  - **$\ge$ 300 kcal** quemadas, **O**
  - **$\ge$ 10,000 pasos** caminados.
- **Criterio de Semana Cumplida:** Acumular un mínimo de **4 días exitosos** durante la semana (lunes a domingo).

### Esquema Financiero y Calendario
La cuota total por participante es de **$900.00 MXN** distribuida en 5 aportaciones oficiales:

| # | Fecha Oficial | Periodo Cubierto | Monto Cuota | Acumulado |
|---|---|---|---|---|
| 1 | **19 de octubre** | Semanas 1 y 2 | $200.00 MXN | $200.00 MXN |
| 2 | **2 de noviembre** | Semanas 3 y 4 | $200.00 MXN | $400.00 MXN |
| 3 | **16 de noviembre** | Semanas 5 y 6 | $200.00 MXN | $600.00 MXN |
| 4 | **30 de noviembre** | Semanas 7 y 8 | $200.00 MXN | $800.00 MXN |
| 5 | **14 de diciembre** | Semana 9 (Final) | **$100.00 MXN** | **$900.00 MXN** |

> **Nota:** La aportación del 14 de diciembre es de $100.00 MXN debido a que la última etapa del reto cubre únicamente una semana (del 14 al 20 de diciembre).

### Dinámica de la Bolsa y Penalizaciones
- **Penalización por Incumplimiento:** Si un participante no alcanza 4 días exitosos en la semana, se le aplica una penalización contable de **$100.00 MXN**.
- **Distribución de la Bolsa:**
  $$\text{Fondo Semanal} = \text{Penalizaciones de la Semana} + \text{Rollover Anterior}$$
  - El fondo acumulado se reparte de forma equitativa en partes enteras entre quienes cumplieron la meta física esa semana.
  - Los remanentes o centavos indivisibles se acumulan como **Rollover** para la bolsa de la siguiente semana.
- **Balance Neto Individual:**
  $$\text{Balance Neto} = \text{Total Aportado} - \text{Total Penalizaciones} + \text{Total Ganancias de Bolsa}$$

---

## 🚀 Funcionalidades Implementadas

El sistema se desarrolló mediante el ciclo **SDD v4.3** con candados criptográficos SHA-256 por funcionalidad:

- **`FEAT-001` — Motor de Dominio del Reto Fit:** Modelos de dominio puros (`Participant`, `DailyActivity`, `WeeklyPool`, `ChallengeLedger`), reglas de cálculo contable y acumulación de días exitosos sin dependencias externas.
- **`FEAT-002` — Interfaz Web y API FastAPI:** Endpoints REST con validación Pydantic V2 y Dashboard Web interactivo con diseño *Dark Mode Energy Neon* (Bento Grid, WCAG 2.1 AA) en Vanilla HTML/CSS/JS.
- **`FEAT-003` — Persistencia de Datos en SQLite:** Base de datos relacional transaccional (`retofit.db`), repositorios desacoplados y recuperación automática del estado ante reinicios.
- **`FEAT-004` — Edición y Gestión de Registros:** Soporte para corregir nombres de participantes, borrado seguro en cascada con modal accesible, anulación del último abono registrado y restablecimiento/limpieza de actividad física por día.
- **`FEAT-005` — Ajuste de Cuota Financiera y Calendario:** Actualización de la meta financiera a $900.00 MXN, calendario detallado con cuota final de $100.00 y botones rápidos `+ $200` y `+ $100` en el concentrado.

---

## 🏛 Arquitectura de Software

El proyecto sigue una estricta separación por capas (**Clean Architecture**):

```
                   ┌────────────────────────────────────────┐
                   │        Presentation Layer              │
                   │   FastAPI Endpoints + Web Views HTML   │
                   └──────────────────┬─────────────────────┘
                                      │
                                      ▼
                   ┌────────────────────────────────────────┐
                   │         Application Layer              │
                   │    ChallengeService + DTOs + Ports     │
                   └──────────────────┬─────────────────────┘
                                      │
                                      ▼
                   ┌────────────────────────────────────────┐
                   │           Domain Layer                 │
                   │  Entities (Participant, Pool, Ledger) │
                   └──────────────────┬─────────────────────┘
                                      │
                                      ▲
                   ┌──────────────────┴─────────────────────┐
                   │        Infrastructure Layer            │
                   │      SQLiteChallengeRepository         │
                   └────────────────────────────────────────┘
```

- **Domain:** Lógica empresarial pura, inmutable y aislada de frameworks.
- **Application:** Orquestación de casos de uso mediante DTOs e interfaces de repositorio (`ChallengeRepository`).
- **Infrastructure:** Implementación concreta de almacenamiento en SQLite con mapeo a entidades de dominio.
- **Presentation:** Rutas HTTP FastAPI, esquemas Pydantic V2 y renderizado del Dashboard Web.

---

## 📂 Estructura del Proyecto

```text
RetoFit2026/
├── .specify/                  # Configuración y memoria del arnés SDD v4.3
│   ├── memory/constitution.md # Principios arquitectónicos innegociables
│   └── harness-config.json    # Parámetros de auditoría y pruebas
├── docs/                      # Guías de usuario por funcionalidad
│   ├── user_guide_002-interfaz-web-api.md
│   ├── user_guide_003-persistencia-sqlite.md
│   ├── user_guide_004-edicion-gestion-registros.md
│   └── user_guide_005-ajuste-cuota-final.md
├── harness/                   # Herramientas de automatización PowerShell
│   ├── init.ps1               # Verificación de salud y suite de tests
│   ├── sdd.ps1                # Orquestador del ciclo SDD y candados SHA-256
│   └── spec-gate.ps1          # Auditor séptuple (Scope, Arch, BDD, etc.)
├── specs/                     # Especificaciones formales (EARS + Gherkin)
│   ├── 001-motor-dominio-retofit/
│   ├── 002-interfaz-web-api/
│   ├── 003-persistencia-sqlite/
│   ├── 004-edicion-gestion-registros/
│   └── 005-ajuste-cuota-final/
├── src/
│   ├── domain/                # Entidades y reglas de negocio puras
│   │   ├── activity.py
│   │   ├── ledger.py
│   │   ├── participant.py
│   │   └── pool.py
│   ├── application/           # Casos de uso y contratos de repositorio
│   │   ├── challenge_service.py
│   │   ├── dto.py
│   │   └── repository.py
│   ├── infrastructure/        # Adaptadores externos y base de datos
│   │   ├── database.py
│   │   └── sqlite_repository.py
│   ├── presentation/          # Endpoints REST y vistas web
│   │   ├── api.py
│   │   ├── schemas.py
│   │   └── web_views.py
│   └── main.py                # Punto de entrada de la aplicación
├── tests/                     # Suite de pruebas automatizadas
│   ├── acceptance/            # Pruebas BDD con pytest-bdd
│   │   ├── test_challenge_steps.py
│   │   ├── test_financial_quota_steps.py
│   │   ├── test_record_management_steps.py
│   │   ├── test_sqlite_persistence_steps.py
│   │   └── test_web_api_steps.py
│   └── unit/                  # Pruebas unitarias de dominio y servicios
├── feature_list.json          # Backlog formal con firmas criptográficas
├── requirements.txt           # Dependencias de producción y testing
└── README.md                  # Este documento
```

---

## ⚙️ Instalación y Puesta en Marcha

### Prerrequisitos
- Python 3.10 o superior instalado.
- Git.
- PowerShell (en entornos Windows) o Bash.

### 1. Clonar el Repositorio
```bash
git clone https://github.com/svelascotellez/RetoFit2026.git
cd RetoFit2026
```

### 2. Crear y Activar Entorno Virtual
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar Dependencias
```powershell
pip install -r requirements.txt
```

### 4. Ejecutar el Servidor
```powershell
python -m uvicorn src.main:app --host 0.0.0.0 --port 8010 --reload
```

---

## 🖥️ Uso de la Aplicación

### Dashboard Web Interactivo
Una vez levantado el servidor, abre tu navegador en:
👉 **[http://localhost:8010](http://localhost:8010)**

Desde el dashboard podrás:
1. **Inscribir Miembros:** Registrar nuevos participantes con ID y nombre completo.
2. **Abonar Pagos:** Registrar aportaciones quincenales ($200.00) o final ($100.00) con los botones rápidos `+ $200` y `+ $100` en la tabla o mediante el formulario manual.
3. **Registrar Actividad Diaria:** Capturar calorías y pasos indicando el participante, semana (1 a 9) y día (1 a 7).
4. **Liquidar Semanas:** Ejecutar el cierre de semana para calcular penalizaciones, repartir la bolsa y actualizar los balances.
5. **Gestionar y Editar:** Corregir nombres (`✏️ Editar`), anular abonos erróneos (`↩️ Anular`), limpiar días de actividad o dar de baja participantes (`🗑️`).

### Documentación Interactiva de la API
FastAPI genera automáticamente la documentación interactiva OpenAPI / Swagger UI:
- **Swagger UI:** [http://localhost:8010/docs](http://localhost:8010/docs)
- **ReDoc:** [http://localhost:8010/redoc](http://localhost:8010/redoc)

---

## 🧪 Pruebas y Aseguramiento de Calidad

El proyecto cuenta con una cobertura completa de pruebas unitarias y de aceptación BDD (Gherkin):

### Ejecutar Suite Completa de Tests
```powershell
python -m pytest -v
```
> **Resultado:** 94 pruebas ejecutadas con 100% de éxito.

### Verificación del Arnés SDD
```powershell
powershell -ExecutionPolicy Bypass -File .\harness\init.ps1
```

### Auditoría Séptuple con Spec-Gate
```powershell
powershell -ExecutionPolicy Bypass -File .\harness\spec-gate.ps1 -FeatureId 005-ajuste-cuota-final
```
Auditoría que valida:
1. Sin Spec Drift (respeto a `Allowed Files`).
2. Clean Architecture (aislamiento de Dominio y Aplicación).
3. Dependencias autorizadas.
4. Cobertura BDD completa.
5. Trazabilidad de pruebas.
6. Guía de usuario obligatoria.
7. Cumplimiento de estándares UI/UX y accesibilidad WCAG 2.1 AA.

### Análisis Estático de Tipos
```powershell
python -m mypy src --ignore-missing-imports --explicit-package-bases
```

---

## 📖 Documentación y Guías de Usuario

Cada funcionalidad incluye su respectiva guía operativa para usuarios y administradores:
- [Guía de Usuario FEAT-002: Interfaz Web y API](docs/user_guide_002-interfaz-web-api.md)
- [Guía de Usuario FEAT-003: Persistencia de Datos en SQLite](docs/user_guide_003-persistencia-sqlite.md)
- [Guía de Usuario FEAT-004: Edición y Gestión de Registros](docs/user_guide_004-edicion-gestion-registros.md)
- [Guía de Usuario FEAT-005: Ajuste de Cuota Financiera y Calendario](docs/user_guide_005-ajuste-cuota-final.md)
- [Principios Constitucionales de Arquitectura](.specify/memory/constitution.md)

---

## 👥 Equipo y Créditos
- **Organización:** Dirección de Informática y Desarrollo Tecnológico (DIDT).
- **Evento:** RetoFit 2026.
- **Desarrollador / Mantenedor:** Salvador Velasco Téllez ([@svelascotellez](https://github.com/svelascotellez)).
- **Licencia:** MIT.
