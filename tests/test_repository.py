import pytest

from app.models import Employee
from app.repository import EmployeeRepository
from tests.fakes import FakeDatabase


@pytest.fixture
def repository() -> EmployeeRepository:
    return EmployeeRepository(FakeDatabase())


def make_employee(
    *,
    employee_id: int | None = None,
    name: str = "Ana Pérez",
    email: str = "ana@example.com",
) -> Employee:
    return Employee(
        id=employee_id,
        full_name=name,
        email=email,
        position="Analista",
        salary=1200,
    )


def test_crud_lifecycle(repository: EmployeeRepository) -> None:
    created = repository.create(make_employee())
    assert created.id == 1
    assert repository.get_by_id(created.id) == created
    assert repository.list_all() == [created]

    updated = make_employee(employee_id=created.id, name="Ana Rojas")
    assert repository.update(updated) == updated
    assert repository.get_by_id(created.id) == updated

    assert repository.delete(created.id) is True
    assert repository.get_by_id(created.id) is None
    assert repository.delete(created.id) is False


def test_update_requires_existing_employee(repository: EmployeeRepository) -> None:
    with pytest.raises(LookupError):
        repository.update(make_employee(employee_id=99))


def test_update_requires_identifier(repository: EmployeeRepository) -> None:
    with pytest.raises(ValueError):
        repository.update(make_employee())
