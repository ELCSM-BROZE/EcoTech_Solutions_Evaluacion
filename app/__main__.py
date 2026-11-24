"""Interfaz de consola del sistema."""

import oracledb
import sys

from app.database import Database
from app.models import Employee
from app.repository import EmployeeRepository
from app.weather import WeatherAPI, WeatherAPIError


def _read_employee() -> Employee:
    name = input("Nombre completo: ")
    email = input("Correo: ")
    position = input("Cargo: ")
    salary = float(input("Sueldo: "))
    return Employee(full_name=name, email=email, position=position, salary=salary)


def _read_positive_id(prompt: str) -> int:
    employee_id = int(input(prompt))
    if employee_id <= 0:
        raise ValueError("El ID debe ser un entero positivo.")
    return employee_id


def _show_employee(employee: Employee) -> None:
    print(
        f"ID: {employee.id} | {employee.full_name} | {employee.email} | "
        f"{employee.position} | Sueldo: {employee.salary:.2f}"
    )


def _show_weather() -> None:
    try:
        weather_api = WeatherAPI()
        city = input(f"Ciudad [{weather_api.default_city}]: ").strip()
        weather = weather_api.current(city or weather_api.default_city)
    except WeatherAPIError as error:
        print(f"No se pudo consultar el clima: {error}")
        return

    location = ", ".join(
        part for part in (weather.location, weather.region, weather.country) if part
    )
    print(
        f"Clima actual en {location} ({weather.local_time}): "
        f"{weather.condition}, {weather.temperature_c:.1f} °C "
        f"(sensación {weather.feels_like_c:.1f} °C), "
        f"humedad {weather.humidity}%."
    )


def main() -> int:
    database = Database()
    repository = EmployeeRepository(database)
    database_available = True
    try:
        database.initialize()
    except ValueError as error:
        database_available = False
        print(f"Oracle no está disponible: {error}", file=sys.stderr)
    except oracledb.Error as error:
        database_available = False
        print(f"Oracle no está disponible: {error}", file=sys.stderr)

    while True:
        print(
            "\n=== EcoTech Solutions | Gestión de Empleados ===\n"
            "1. Registrar empleado\n"
            "2. Listar empleados\n"
            "3. Buscar por ID\n"
            "4. Actualizar empleado\n"
            "5. Eliminar empleado\n"
            "6. Consultar clima actual\n"
            "0. Salir"
        )
        try:
            choice = input("Opción: ").strip()
        except EOFError:
            print("\nEntrada finalizada. Hasta luego.")
            return 0

        if choice == "0":
            print("Hasta luego.")
            return 0

        if choice in {"1", "2", "3", "4", "5"} and not database_available:
            print("Las operaciones de empleados requieren una conexión Oracle.")
            continue

        try:
            if choice == "1":
                employee = repository.create(_read_employee())
                print(f"Empleado registrado con ID {employee.id}.")
            elif choice == "2":
                employees = repository.list_all()
                if not employees:
                    print("No hay empleados registrados.")
                for employee in employees:
                    _show_employee(employee)
            elif choice == "3":
                employee_id = _read_positive_id("ID del empleado: ")
                employee = repository.get_by_id(employee_id)
                if employee is None:
                    print("No se encontró ese empleado.")
                else:
                    _show_employee(employee)
            elif choice == "4":
                employee_id = _read_positive_id("ID del empleado a actualizar: ")
                if repository.get_by_id(employee_id) is None:
                    raise LookupError(f"No existe un empleado con ID {employee_id}.")
                updated = _read_employee()
                employee = Employee(
                    id=employee_id,
                    full_name=updated.full_name,
                    email=updated.email,
                    position=updated.position,
                    salary=updated.salary,
                )
                repository.update(employee)
                print("Empleado actualizado.")
            elif choice == "5":
                employee_id = _read_positive_id("ID del empleado a eliminar: ")
                if repository.delete(employee_id):
                    print("Empleado eliminado.")
                else:
                    print("No se encontró ese empleado.")
            elif choice == "6":
                _show_weather()
            else:
                print("Opción no válida. Elige un número del menú.")
        except ValueError as error:
            print(f"Entrada no válida: {error}")
        except LookupError as error:
            print(error)
        except oracledb.IntegrityError:
            print("No se pudo guardar: ese correo ya está registrado.")
        except oracledb.Error as error:
            print(f"Error de Oracle Database: {error}")


if __name__ == "__main__":
    raise SystemExit(main())
