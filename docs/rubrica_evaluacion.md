# Matriz de trazabilidad de la rúbrica

Cada indicador vale hasta 3 puntos (Excelente), 2 (Bueno) o 0
(Insatisfactorio). Esta matriz conecta los 20 indicadores con archivos,
demostraciones y argumentos para la defensa individual de un estudiante.

> **Condición para aspirar a Excelente:** cotejar y ajustar la propuesta con el
> UML validado de Unidad 1. Ese diagrama no estaba entre los archivos recibidos;
> por ello no se debe afirmar correspondencia exacta hasta completar esa
> comparación.

| Indicador | Tipo | Evidencia / demostración | Qué explicar en la defensa |
|---|---|---|---|
| 2.1.1.G.1 | Código | `Employee` en `app/models.py`, atributos tipados, constructor generado por `dataclass` y validación en `__post_init__`. | Cómo cada atributo y método coincide con la entidad del UML. Ajustar el modelo si el UML real difiere. |
| 2.1.1.G.2 | Código | `EmployeeRepository` usa `Database` y crea/retorna objetos `Employee`; diagrama de clases en `docs/diagrama_flujo.md`. | Traducir asociaciones a atributos/parámetros de objetos. Explicar herencia solo si el UML la tiene; el modelo recibido no justifica inventarla. |
| 2.1.1.I.3 | Oral | Código y diagrama UML validado, puestos lado a lado. | Relacionar, uno a uno, entidades, atributos, constructores y métodos. No dar por hecho el UML faltante. |
| 2.1.1.I.4 | Oral | Flechas del diagrama de clases y referencias en `app/repository.py`. | `EmployeeRepository` mantiene una instancia de `Database` y consume/produce `Employee`; explicar la sintaxis Python concreta y las relaciones reales del UML. |
| 2.1.2.G.5 | Código | `Employee` es `frozen=True`, normaliza y valida datos; `Database` y repositorio separan responsabilidades. | La inmutabilidad evita cambios posteriores no validados. Python no impone privacidad absoluta; `frozen=True` y la interfaz pública restringida de cada clase promueven encapsulamiento. No crear herencia artificial. |
| 2.1.2.G.6 | Código | El modelo se reutiliza en CRUD; validaciones centralizadas y conexión compartida por el repositorio. | La validación y representación común evitan duplicar reglas entre operaciones. Contrastar la estructura con el UML real. |
| 2.1.2.I.7 | Oral | Constructor validante e instancia inmutable en `app/models.py`. | Los valores pasan las reglas al crear la instancia; normalización y objeto congelado impiden dejarla en estado inconsistente después. |
| 2.1.2.I.8 | Oral | Separación `Employee` / `EmployeeRepository` / `Database` / menú. | Se reutiliza composición y separación de responsabilidades. No se agregó herencia ni abstracción porque solo hay un tipo de empleado en los requisitos recibidos; si el UML muestra subtipos, implementar esa relación y justificarla. |
| 2.1.3.G.9 | Código | `Database.connection()` llama a `oracledb.connect` con usuario, contraseña y DSN configurados por variables de entorno. | `oracledb` es el driver oficial Python para Oracle; explicar los parámetros y no exponer credenciales. |
| 2.1.3.G.10 | Código | Métodos `create`, `get_by_id`, `list_all`, `update`, `delete`; ciclo CRUD probado en `tests/test_repository.py`. | Ejecutar registro, consulta, actualización y eliminación y confirmar los cambios. |
| 2.1.3.I.11 | Oral | `Database.__init__`, `connection`, `.env.example` y esquema de `app/database.py`. | Explicar `ORACLE_USER`, `ORACLE_PASSWORD`, `ORACLE_DSN`, `oracledb.connect`, commit/rollback y cierre de conexión. |
| 2.1.3.I.12 | Oral | SQL Oracle parametrizado del repositorio y ciclo CRUD probado con un doble de conexión. | `INSERT` registra; `SELECT` consulta; `UPDATE` cambia; `DELETE` elimina. Los binds `:nombre` separan los valores del SQL. |
| 2.1.4.G.13 | Código | `try-except` en menú y `connection()` revierte excepciones; inicialización informa errores Oracle y termina con código 1. | Mostrar los puntos de captura concretos y cómo una transacción fallida se revierte. |
| 2.1.4.G.14 | Código | Reglas de `Employee`; conversión de ID/sueldo y menú resistente a errores esperables. | Probar sueldo no numérico, identificador no numérico, correo inválido, sueldo negativo y correo duplicado; mostrar que se informa y el menú continúa. |
| 2.1.4.I.15 | Oral | `except ValueError`, `LookupError`, `oracledb.IntegrityError` y `oracledb.Error` en `app/__main__.py`. | `ValueError`: configuración/entrada; `LookupError`: ID inexistente; `IntegrityError`: restricción como correo duplicado; `oracledb.Error`: fallo Oracle. |
| 2.1.4.I.16 | Oral | Restricciones Oracle, validación de dominio y mensajes del menú. | Validar antes de persistir y reforzar restricciones en BD evita datos incoherentes; binds Oracle evitan interpolar entradas SQL. |
| 2.1.5.G.17 | Código | Pruebas ejecutables con `python -m pytest`; registro personal en `docs/validacion_ia.md`. | Mostrar un caso válido y casos límite, resultados reales y cualquier error encontrado. Añadir a la bitácora fallos reales antes de entregar. |
| 2.1.5.G.18 | Código | Decisiones y sus verificaciones están en `docs/validacion_ia.md`; revisar consultas, validaciones y pruebas. | Identificar al menos una sugerencia adoptada y una modificación o descarte, con motivo técnico y prueba asociada; completar con el trabajo real. |
| 2.1.5.I.19 | Oral | Declaración y tabla de registro en `docs/validacion_ia.md`. | Identificar transparentemente qué módulos o fragmentos recibieron apoyo de IA. Sustituir el ejemplo por consultas y cambios que efectivamente ocurrieron. |
| 2.1.5.I.20 | Oral | Criterios de coherencia UML, seguridad SQL, errores y pruebas en la bitácora. | Justificar decisiones por seguridad, funcionamiento, eficiencia suficiente y coherencia con el modelo; distinguir recomendaciones de IA de evidencia medida. |

## Confirmaciones previas

- La guía de la evaluación define modalidad grupal de 2 a 3 estudiantes. Esta
  entrega está adaptada para una persona por solicitud; confirma la autorización
  con el docente.
- La guía referencia un UML validado en Unidad 1 que no estaba entre los
  archivos recibidos. Sin cotejarlo, no se puede demostrar equivalencia exacta.
- Verifica que Oracle sea el gestor disponible y que tu usuario tenga permisos
  para consultar `USER_TABLES` y crear la tabla en su propio esquema.

## Ensayo de evaluación

1. Ejecuta las pruebas con `python -m pytest`.
2. Ejecuta `python -m app` y demuestra las cuatro operaciones CRUD.
3. Prueba entradas inválidas y un correo duplicado.
4. Abre el UML validado y comprueba cada entidad, campo, relación y método
   contra el código. Corrige cualquier discrepancia antes de presentar.
5. Completa la bitácora con las interacciones reales de IA y los resultados de
   pruebas que realmente observaste.
6. Ensaya la explicación de cada fila sin leerla literalmente.

La matriz sirve para organizar evidencia, no garantiza puntaje: la evaluación
final depende de la implementación, la comparación con el UML original y la
defensa individual efectiva.
