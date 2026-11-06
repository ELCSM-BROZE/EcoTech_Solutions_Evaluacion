# Sistema de Gestión de Empleados — EcoTech Solutions

Aplicación de consola CRUD desarrollada en Python con programación orientada a
objetos y Oracle Database. Está planteada para que **un estudiante** realice y
explique el trabajo con apoyo crítico de una herramienta de IA.

> **Modalidad:** la guía original indica equipos de 2 a 3 estudiantes. Esta
> versión está adaptada a la solicitud de trabajo individual; confirma con el
> docente que puedes entregar en esa modalidad.

> **Alcance del modelo:** la guía hace referencia a un diagrama UML validado en
> la unidad anterior, pero ese diagrama no venía en los archivos recibidos. Este
> proyecto propone un modelo mínimo de `Empleado` y `EmpleadoRepository`.
> Antes de entregar, coteja nombres, atributos y relaciones con tu UML validado
> y ajusta el código si es distinto.

## Requisitos

- Python 3.11 o superior (el entorno se creó con Python 3.13).
- `pip`, incluido con Python.
- Instancia Oracle accesible y un usuario con permisos para crear tablas en su
  propio esquema.
- `oracledb` (driver oficial de Python para Oracle) y `python-dotenv`.
- `pytest`, para ejecutar las pruebas automatizadas.
- Editor de código y una IA generativa como apoyo opcional, no como sustituto
  de la revisión del estudiante.

## Configuración y ejecución en Windows PowerShell

Desde la carpeta del proyecto:

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
python -m app
```

Edita `.env` con el usuario, contraseña y DSN de **tu propia instancia Oracle**.
El DSN suele tener el formato `host:puerto/servicio` (por ejemplo,
`localhost:1521/FREEPDB1`). No compartas ni subas `.env`; está ignorado por Git.
La aplicación crea la tabla `EMPLOYEES` en el esquema de ese usuario si aún no
existe. Para salir, selecciona `0`.

El driver usa el modo Thin por defecto, que no requiere instalar Oracle Instant
Client para conexiones TCP habituales. Si PowerShell impide activar el entorno,
usa `.\.venv\Scripts\python.exe` en lugar de `python`.

## Pruebas

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

Las pruebas usan un doble en memoria del contrato de conexión y no necesitan
credenciales ni modifican Oracle. Para validar una conexión real, configura
`.env` y ejecuta la aplicación contra una instancia de prueba.

## Funcionalidades

- Registrar, listar, consultar, actualizar y eliminar empleados.
- Validar nombre, correo, cargo y sueldo antes de guardar.
- Evitar correos duplicados mediante una restricción `UNIQUE` de Oracle.
- Usar parámetros con nombre (`:email`, `:employee_id`) en las consultas.
- Manejar errores de validación, registros inexistentes y problemas de Oracle.

## Estructura

```text
app/
  __init__.py
  __main__.py       # punto de entrada y menú
  database.py       # conexión y esquema Oracle
  models.py         # entidad Empleado y validaciones
  repository.py     # operaciones CRUD
tests/
  fakes.py
  test_cli.py
  test_models.py
  test_repository.py
docs/
  PASO_A_PASO.md
  diagrama_flujo.md
  rubrica_evaluacion.md
  validacion_ia.md
PRUEBA.txt
requirements.txt
.env.example
```

Consulta [el paso a paso](docs/PASO_A_PASO.md), [el diagrama de flujo y sus
relaciones](docs/diagrama_flujo.md), [la matriz de evidencia para los 20
criterios de la rúbrica](docs/rubrica_evaluacion.md) y [la pauta para validar
el apoyo de IA](docs/validacion_ia.md).
