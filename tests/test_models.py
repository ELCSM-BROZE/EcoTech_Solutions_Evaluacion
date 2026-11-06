import pytest

from app.models import Employee


def test_employee_normalizes_and_trims_fields() -> None:
    employee = Employee(
        full_name="  Ana Pérez  ",
        email="  ANA@EXAMPLE.COM ",
        position="  Analista  ",
        salary=1200,
    )

    assert employee.full_name == "Ana Pérez"
    assert employee.email == "ana@example.com"
    assert employee.position == "Analista"
    assert employee.salary == 1200.0


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("full_name", "  "),
        ("email", "no-es-correo"),
        ("position", ""),
        ("salary", -1),
        ("salary", float("inf")),
        ("id", 1.5),
        ("full_name", None),
    ],
)
def test_employee_rejects_invalid_values(field: str, value: object) -> None:
    values: dict[str, object] = {
        "full_name": "Ana Pérez",
        "email": "ana@example.com",
        "position": "Analista",
        "salary": 1000.0,
        "id": None,
    }
    values[field] = value

    with pytest.raises(ValueError):
        Employee(**values)  # type: ignore[arg-type]
