
## Que paja documentar ##


PRUEBA DEL SISTEMA DE GESTION DE EMPLEADOS CON ORACLE
======================================================

Abre PowerShell en la carpeta del proyecto.

1. Preparar el entorno (solo la primera vez)
---------------------------------------------

python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env

En .env, reemplaza los valores de ejemplo por los datos de tu instancia:

ORACLE_USER=tu_usuario
ORACLE_PASSWORD=tu_contrasena
ORACLE_DSN=host:puerto/servicio

# Clave de tu cuenta WeatherAPI.com (no la compartas ni la subas a Git).
WEATHERAPI_API_KEY=tu_clave_weatherapi
WEATHERAPI_DEFAULT_CITY=Santiago, Colina

Ejemplo de formato DSN local: localhost:1521/FREEPDB1.
No compartas ni subas .env; contiene credenciales privadas.

2. Ejecutar las pruebas automatizadas
--------------------------------------

.\.venv\Scripts\python.exe -m pytest -v

Resultado esperado: todas las pruebas terminan con "passed". La cantidad puede
cambiar si se agregan nuevos casos de prueba.
Las pruebas usan una conexión simulada y no requieren una instancia Oracle.

3. Iniciar la aplicación para probarla manualmente
---------------------------------------------------

.\.venv\Scripts\python.exe -m app

En el menu, prueba estas acciones:

1. Registra un empleado:
   Nombre completo: Ana Perez
   Correo: ana@example.com
   Cargo: Analista
   Sueldo: 1200

2. Selecciona la opcion 2 para listar los empleados.
3. Selecciona la opcion 3 y escribe el ID mostrado al registrar.
4. Selecciona la opcion 4, escribe ese ID y proporciona los nuevos datos.
5. Selecciona la opcion 5 y escribe el ID para eliminar el empleado.
6. Selecciona la opcion 6 para consultar el clima de Santiago, Colina o escribe
   otra ciudad. Se requiere una clave WeatherAPI valida y conexion a Internet.
7. Selecciona la opcion 0 para salir.

Prueba tambien escribir letras cuando se solicite un sueldo o ID. El sistema
debe mostrar un mensaje de error y continuar mostrando el menu.
Prueba registrar otra vez el mismo correo para verificar que informa el
conflicto y no detiene la aplicacion.

La primera ejecución crea la tabla EMPLOYEES en el esquema de Oracle configurado
si no existe. El usuario debe poder consultar USER_TABLES y crear tablas en su
esquema. Los registros se guardan en esa base Oracle, no en un archivo local.
Usa datos ficticios o un esquema de prueba.


# Registro de uso y validación de IA

## Declaración de uso
## Yo no declare nada es la IA []~(￣▽￣)~* .

En esta entrega se utilizó un asistente de IA (Copilot SDK en VS Code) como
apoyo para proponer y revisar la estructura de la aplicación, implementar
fragmentos de Python, elaborar pruebas y redactar documentación. Por lo tanto,
el código de los archivos `app/`, `tests/` y la documentación del proyecto
recibió apoyo de IA; no se presenta como código escrito íntegramente sin ayuda.

## Criterios de revisión aplicados

| Criterio | Evidencia verificable en el proyecto |
|---|---|
| Coherencia del modelo | `Employee` representa los datos administrados; falta cotejarlo con el UML original de Unidad 1. |
| POO y responsabilidades | Modelo (`app/models.py`), conexión (`app/database.py`), repositorio (`app/repository.py`) e interfaz (`app/__main__.py`) separados. |
| Persistencia | Driver oficial `oracledb`, configuración por `.env` y tabla Oracle con restricciones. |
| Seguridad de consultas | Binds Oracle (`:employee_id`, `:email`), sin concatenación de entradas. |
| Secretos | `.env` está excluido de Git; `.env.example` contiene solo valores de muestra. |
| Validación y estabilidad | Reglas de `Employee`, comprobación de IDs y captura de errores específicos. |
| Funcionamiento | Pruebas automatizadas con un doble de conexión; no requieren una instancia ni credenciales Oracle. |

## Análisis de propuestas y decisiones

| Propuesta apoyada por IA | Decisión del estudiante | Criterio técnico y evidencia |
|---|---|---|
| Usar el driver `oracledb` y `python-dotenv` del ejemplo | Adoptada | Mantiene el gestor solicitado en el ejemplo. La aplicación carga la configuración del `.env` sin incluir credenciales en el código. |
| Separar entidad, repositorio y conexión | Adoptada y revisada | Mantiene validación de dominio, SQL y menú en responsabilidades distintas; inspeccionar los módulos indicados arriba. |
| Usar parámetros con nombre de Oracle | Adoptada | Evita concatenar entrada en consultas; verificar los binds como `:email` en `app/repository.py`. |
| Usar `float(input(...))` sin capturar el error | Modificada | La conversión puede fallar ante texto; el menú captura `ValueError` y vuelve a solicitar una opción en el siguiente ciclo. Probar con `no-numérico`. |
| Aceptar cualquier ID numérico | Modificada | Un ID cero o negativo no es un identificador válido; `_read_positive_id` lo rechaza. Hay prueba de esta regla. |
| Afirmar equivalencia exacta con el UML sin tenerlo | Descartada | El UML de Unidad 1 no fue entregado con los materiales disponibles. La comparación debe hacerse antes de afirmar correspondencia o cerrar el modelo. |
| Copiar literalmente `conexion.cursor()` del ejemplo | Descartada | El ejemplo define `abrir()` para obtener una conexión, pero luego invoca `cursor()` en el objeto `ConexionOracle`, que no lo implementa. La versión actual crea un cursor desde la conexión que entrega el context manager y siempre lo cierra. |
| Ejecutar `CREATE TABLE` en cada inicio sin comprobar si existe | Modificada | La inicialización consulta `USER_TABLES` y solo crea `EMPLOYEES` si no existe; errores de permisos o conexión se informan explícitamente. |

## Pruebas de esta versión

La suite automatizada cubre validación de atributos, el ciclo completo CRUD
desde el menú, operaciones del repositorio contra un doble de conexión,
configuración de credenciales, commit/rollback/cierre, creación idempotente de
la tabla, actualización de registros inexistentes, entradas no numéricas,
finalización de entrada y rechazo de IDs no positivos. No comprueba una
instancia Oracle real ni la validez del DSN. Ejecuta:

  ## Porque Powershell mejor CMD ╰（‵□′）╯ .
  ```powershell
  .\.venv\Scripts\python.exe -m pytest -v
  ```

Anota el resultado que obtuviste tú al ejecutar el comando. No declares una
prueba manual como realizada si no la ejecutaste.

En la última ejecución automatizada de este proyecto, pytest reportó 20 pruebas
aprobadas y `compileall` compiló correctamente `app/` y `tests/`. Estos
resultados verifican el código local con dobles de prueba; no equivalen a una
conexión ni a una operación sobre un servidor Oracle real.

## Bitácora individual que completa el estudiante

Para evidenciar autoría y criterio propio, añade al menos dos consultas reales
que hayas realizado, el código concreto revisado, la prueba ejecutada y tu
decisión. No inventes interacciones ni resultados.

| Consulta real a la IA y fragmento revisado | Prueba o criterio aplicado por el estudiante | Resultado observado y decisión personal |
|---|---|---|
| Completar con la consulta y el archivo real | Completar después de ejecutar | Completar con resultado real |
| Completar con otra consulta y el fragmento real | Completar después de revisar | Completar con resultado real |

> **Pendiente antes de entregar:** cotejar y actualizar el modelo según el UML
> validado de Unidad 1; configurar y probar una instancia Oracle real con datos
> de prueba; confirmar que el usuario Oracle tiene los permisos requeridos;
> completar la bitácora con evidencia propia y real.

## No tengo cuenta de oracle (;´༎ຶД༎ຶ`) .