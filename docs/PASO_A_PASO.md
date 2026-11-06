# Paso a paso de desarrollo y uso

## 1. Definir el alcance individual

El proyecto lo desarrolla una sola persona. El estudiante toma las decisiones,
ejecuta el código, revisa las sugerencias de IA y puede explicar cada archivo.
La IA es apoyo para proponer y revisar, no reemplaza el análisis ni la autoría
de las decisiones finales.

La guía de evaluación indica modalidad grupal de 2 a 3 estudiantes. Como esta
adaptación es individual por solicitud, confirma previamente con el docente
que puedes entregar y defender el proyecto de forma individual.

El problema consiste en mantener los datos de empleados de EcoTech Solutions.
El programa permite crear, consultar, actualizar y eliminar empleados desde una
interfaz de consola y persiste los datos en Oracle Database, siguiendo el
patrón de conexión del CRUD Oracle de ejemplo.

## 2. Confirmar el modelo antes de programar

La guía supone que existe un diagrama UML validado de la unidad anterior, pero
no se recibió ese archivo. Como base implementable se propone:

- `Employee`: entidad con identificador, nombre, correo, cargo y sueldo.
- `EmployeeRepository`: concentra las operaciones de persistencia (CRUD).
- `Database`: administra la conexión Oracle y crea la tabla `EMPLOYEES`.
- `main`: presenta el menú y comunica errores al usuario.

La relación es de dependencia en la ejecución: `EmployeeRepository` usa
`Database` para operar y convierte filas Oracle en objetos `Employee`. No se
agregó herencia porque el alcance no define subtipos de empleado. Antes de
entregar, compara esta propuesta con el UML de Unidad 1 y adapta las clases si
el docente validó otra estructura.

## 3. Preparar Python y el entorno virtual

Abre PowerShell en la carpeta del proyecto y ejecuta:

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
```

El entorno `.venv` aísla las dependencias del proyecto. `oracledb` es el driver
oficial de Python para Oracle, `python-dotenv` carga la configuración de `.env`
y `pytest` ejecuta las pruebas.

En `.env`, reemplaza los valores de ejemplo por los datos entregados para tu
instancia:

```text
ORACLE_USER=tu_usuario
ORACLE_PASSWORD=tu_contrasena
ORACLE_DSN=host:puerto/servicio
```

Por ejemplo, una instancia local puede usar un DSN como
`localhost:1521/FREEPDB1`; el host, puerto y servicio reales dependen de la
instalación del estudiante. No subas el archivo `.env` ni incluyas credenciales
en capturas o entregas públicas.

## 4. Entender la estructura y las responsabilidades

1. `app/models.py`: valida los datos y representa un empleado como objeto
   inmutable. El correo se normaliza a minúsculas.
2. `app/database.py`: carga las variables `ORACLE_USER`, `ORACLE_PASSWORD` y
   `ORACLE_DSN`, abre/cierra conexiones con `oracledb`, crea el esquema si falta
   y confirma o revierte la transacción.
3. `app/repository.py`: implementa alta, búsqueda, listado, actualización y
   eliminación. Usa binds Oracle (`:employee_id`, `:email`) y no concatena
   entradas del usuario.
4. `app/__main__.py`: solicita entradas, muestra resultados y maneja errores
   esperables sin cerrar el programa ante una entrada incorrecta.
5. `tests/`: comprueba validaciones, operaciones CRUD y menú usando un doble de
   conexión en memoria; no requiere acceso a Oracle.

Al iniciar, la aplicación comprueba `USER_TABLES` y, si `EMPLOYEES` no existe
en el esquema conectado, crea una tabla con ID identity, correo único y sueldo
no negativo. Se requiere permiso para crear tablas en ese esquema y Oracle 12c
o superior para la columna identity usada en este proyecto.

## 5. Ejecutar y probar el CRUD

Inicia la aplicación con:

```powershell
.\.venv\Scripts\python.exe -m app
```

Prueba el menú en este orden:

1. Registra un empleado con datos válidos.
2. Lista empleados y busca el registro por su ID.
3. Actualiza el cargo, el correo u otro dato del mismo ID.
4. Intenta registrar de nuevo el mismo correo y confirma que se informa el
   conflicto.
5. Elimina el empleado y comprueba que ya no aparece.
6. Ingresa texto donde se espera un número y confirma que el menú sigue activo.

Los registros quedan en la tabla `EMPLOYEES` del esquema Oracle asociado al
usuario configurado. Para las pruebas manuales usa datos ficticios y, de ser
posible, un esquema de prueba.

## 6. Validar técnicamente el apoyo de IA

Solicita a la IA tareas acotadas (por ejemplo, proponer pruebas para el CRUD o
explicar una consulta SQL), no que entregue el proyecto terminado sin revisión.
Para cada sugerencia:

1. Contrástala con el UML, el objetivo y los criterios de evaluación.
2. Revisa tipos, validaciones, consultas SQL, errores y efectos sobre datos.
3. Ejecuta las pruebas y agrega casos límite relevantes.
4. Adopta, modifica o descarta la sugerencia y anota la razón en
   `docs/validacion_ia.md`.
5. Asegúrate de poder explicar en una defensa cada decisión y cada fragmento
   que incluyas.

## 7. Ejecutar la suite y preparar la entrega

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

Verifica el resultado, revisa el contenido de los archivos y actualiza la
documentación con cualquier cambio que hayas realizado. Entrega la carpeta del
código fuente y la documentación según las instrucciones del docente. No es
necesario entregar `.venv`; se reconstruye usando `python -m venv .venv` y
`python -m pip install -r requirements.txt`.
Tampoco entregues `.env`; cada persona configura sus propias credenciales a
partir de `.env.example`.

## 8. Preparar la defensa individual

Explica con tus propias palabras:

- Cómo se mapean entidad, atributos y relaciones UML a clases Python.
- Por qué el modelo valida los datos y por qué el repositorio mantiene separada
  la persistencia.
- Cómo `oracledb.connect(user=..., password=..., dsn=...)` establece la
  conexión, qué significa cada parámetro y por qué las credenciales se cargan
  desde `.env`.
- Cómo funcionan las cuatro operaciones CRUD y las consultas parametrizadas.
- Qué errores de validación y Oracle se manejan y qué pruebas demuestran el
  comportamiento. Las pruebas simuladas no sustituyen una conexión real.
- Qué recomendó la IA, qué validaste y qué modificaste o descartaste.

Usa la [matriz de la rúbrica](rubrica_evaluacion.md) para preparar evidencia
concreta para los 20 indicadores, tanto de implementación como de defensa oral.
