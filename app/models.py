"""Entidades del dominio."""

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Employee:
    """Empleado validado antes de persistirlo."""

    full_name: str
    email: str
    position: str
    salary: float
    id: int | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.full_name, str):
            raise ValueError("El nombre debe ser texto.")
        if not isinstance(self.email, str):
            raise ValueError("El correo debe ser texto.")
        if not isinstance(self.position, str):
            raise ValueError("El cargo debe ser texto.")

        name = self.full_name.strip()
        email = self.email.strip().lower()
        position = self.position.strip()

        if not name:
            raise ValueError("El nombre no puede estar vacío.")
        if not email or "@" not in email or "." not in email.rsplit("@", 1)[-1]:
            raise ValueError("Ingresa un correo electrónico válido.")
        if any(character.isspace() for character in email):
            raise ValueError("El correo no puede contener espacios.")
        if not position:
            raise ValueError("El cargo no puede estar vacío.")
        if isinstance(self.salary, bool) or not isinstance(self.salary, (int, float)):
            raise ValueError("El sueldo debe ser un número.")
        if not math.isfinite(self.salary) or self.salary < 0:
            raise ValueError("El sueldo debe ser un número finito igual o mayor que cero.")
        if self.id is not None and (
            isinstance(self.id, bool) or not isinstance(self.id, int) or self.id <= 0
        ):
            raise ValueError("El identificador debe ser un entero positivo.")

        object.__setattr__(self, "full_name", name)
        object.__setattr__(self, "email", email)
        object.__setattr__(self, "position", position)
        object.__setattr__(self, "salary", float(self.salary))
