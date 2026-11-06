# Diagrama de flujo y relación de componentes

```mermaid
flowchart TD
    A[Estudiante: define alcance y revisa UML] --> B[IA: propone ideas o fragmentos acotados]
    B --> C{Revisión técnica del estudiante}
    C -->|No cumple UML, seguridad o pruebas| D[Modificar o descartar sugerencia]
    D --> C
    C -->|Comprendido y validado| E[Modelo Employee: datos y reglas]
    E --> F[Menú de consola: recibe y valida entradas]
    F --> G[EmployeeRepository: coordina CRUD]
    G --> H[Database: oracledb.connect y transacción]
    H --> I[(Oracle: esquema y tabla EMPLOYEES)]
    I --> H
    H --> G
    G --> F
    F --> J{¿Entrada, registro o consulta falla?}
    J -->|Sí| K[Manejo de ValueError, LookupError u oracledb.Error]
    K --> F
    J -->|No| L[Mostrar resultado al estudiante]
    E --> M[pytest: pruebas del modelo y CRUD]
    G --> M
    M --> N{¿Pruebas pasan?}
    N -->|No| O[Analizar fallo y corregir código]
    O --> M
    N -->|Sí| P[Registrar validación y preparar defensa]
```

## Por qué se relacionan así

- **El estudiante y la IA** se conectan mediante revisión: la IA puede acelerar
  propuestas, pero el estudiante compara con el UML, verifica pruebas y decide.
  Así se satisface el uso crítico de IA sin delegar la comprensión.
- **El modelo `Employee`** contiene los datos del dominio y sus reglas de
  validación; tanto el menú como el repositorio usan esa misma representación.
- **El menú** recoge datos y comunica resultados; el **repositorio** separa el
  CRUD de la interfaz y expresa las consultas de almacenamiento.
- **El repositorio** usa `Database`, que administra conexiones y transacciones;
  esta capa utiliza `oracledb` para guardar los datos en **Oracle Database**.
- **Las excepciones** vuelven desde validación o almacenamiento al menú, que
  informa el problema y permite continuar en vez de finalizar abruptamente.
- **pytest** prueba modelo y repositorio de manera aislada con una base
  temporal. Los resultados orientan correcciones antes de la defensa.
- **`requirements.txt`** instala `oracledb`, `python-dotenv` y `pytest`.
  `oracledb` es el driver oficial; `python-dotenv` carga las credenciales
  locales y pytest ejecuta pruebas sin conectarse a Oracle.

## Diagrama de clases propuesto

```mermaid
classDiagram
    class Employee {
        +int id
        +str full_name
        +str email
        +str position
        +float salary
        +validate()
    }
    class EmployeeRepository {
        -Database database
        +create(employee) Employee
        +get_by_id(id) Employee
        +list_all() list~Employee~
        +update(employee) Employee
        +delete(id) bool
    }
    class Database {
        +str user
        +str dsn
        +connection()
        +initialize()
    }
    EmployeeRepository --> Database : usa para SQL
    EmployeeRepository ..> Employee : crea y consulta
    Database --> oracledb : conexión y transacción
    oracledb --> Oracle : conexión al esquema
```

Las credenciales y el DSN se leen desde `.env`, excluido del repositorio. El
archivo `.env.example` documenta los nombres de las variables sin contener
secretos.
