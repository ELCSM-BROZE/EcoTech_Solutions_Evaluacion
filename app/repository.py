"""Operaciones CRUD de empleados para Oracle Database."""

from app.database import Database
from app.models import Employee


class EmployeeRepository:
    """Guarda y recupera empleados sin acoplarse a la interfaz de consola."""

    def __init__(self, database: Database) -> None:
        self.database = database

    def create(self, employee: Employee) -> Employee:
        with self.database.connection() as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    """
                    INSERT INTO employees (full_name, email, position, salary)
                    VALUES (:full_name, :email, :position, :salary)
                    """,
                    {
                        "full_name": employee.full_name,
                        "email": employee.email,
                        "position": employee.position,
                        "salary": employee.salary,
                    },
                )
                cursor.execute(
                    "SELECT employee_id FROM employees WHERE email = :email",
                    {"email": employee.email},
                )
                row = cursor.fetchone()
                if row is None:
                    raise RuntimeError("Oracle no devolvió el ID del empleado registrado.")
                employee_id = int(row[0])
            finally:
                cursor.close()

        return Employee(
            id=employee_id,
            full_name=employee.full_name,
            email=employee.email,
            position=employee.position,
            salary=employee.salary,
        )

    def get_by_id(self, employee_id: int) -> Employee | None:
        with self.database.connection() as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    """
                    SELECT employee_id, full_name, email, position, salary
                    FROM employees
                    WHERE employee_id = :employee_id
                    """,
                    {"employee_id": employee_id},
                )
                row = cursor.fetchone()
            finally:
                cursor.close()
        return self._from_row(row) if row is not None else None

    def list_all(self) -> list[Employee]:
        with self.database.connection() as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    """
                    SELECT employee_id, full_name, email, position, salary
                    FROM employees
                    ORDER BY employee_id
                    """
                )
                rows = cursor.fetchall()
            finally:
                cursor.close()
        return [self._from_row(row) for row in rows]

    def update(self, employee: Employee) -> Employee:
        if employee.id is None:
            raise ValueError("El empleado debe tener identificador para actualizarse.")

        with self.database.connection() as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    """
                    UPDATE employees
                    SET full_name = :full_name,
                        email = :email,
                        position = :position,
                        salary = :salary
                    WHERE employee_id = :employee_id
                    """,
                    {
                        "full_name": employee.full_name,
                        "email": employee.email,
                        "position": employee.position,
                        "salary": employee.salary,
                        "employee_id": employee.id,
                    },
                )
                if cursor.rowcount == 0:
                    raise LookupError(f"No existe un empleado con ID {employee.id}.")
            finally:
                cursor.close()
        return employee

    def delete(self, employee_id: int) -> bool:
        with self.database.connection() as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    "DELETE FROM employees WHERE employee_id = :employee_id",
                    {"employee_id": employee_id},
                )
                deleted = cursor.rowcount > 0
            finally:
                cursor.close()
        return deleted

    @staticmethod
    def _from_row(row: tuple[object, ...]) -> Employee:
        employee_id, full_name, email, position, salary = row
        return Employee(
            id=int(employee_id),
            full_name=str(full_name),
            email=str(email),
            position=str(position),
            salary=float(salary),
        )
