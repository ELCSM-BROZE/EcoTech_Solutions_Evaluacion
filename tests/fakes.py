"""Doubles de prueba para probar el repositorio sin un servidor Oracle."""

from contextlib import contextmanager


class FakeDatabase:
    def __init__(self) -> None:
        self.rows: dict[int, dict[str, object]] = {}
        self.next_id = 1

    def initialize(self) -> None:
        pass

    @contextmanager
    def connection(self):
        yield FakeConnection(self)


class FakeConnection:
    def __init__(self, database: FakeDatabase) -> None:
        self.database = database

    def cursor(self):
        return FakeCursor(self.database)


class FakeCursor:
    def __init__(self, database: FakeDatabase) -> None:
        self.database = database
        self.result = None
        self.results = []
        self.rowcount = -1

    def execute(self, statement: str, parameters: dict[str, object] | None = None) -> None:
        sql = " ".join(statement.upper().split())
        values = parameters or {}
        self.result = None
        self.results = []
        self.rowcount = -1

        if sql.startswith("INSERT INTO EMPLOYEES"):
            employee_id = self.database.next_id
            self.database.next_id += 1
            self.database.rows[employee_id] = {
                "employee_id": employee_id,
                "full_name": values["full_name"],
                "email": values["email"],
                "position": values["position"],
                "salary": values["salary"],
            }
        elif sql.startswith("SELECT EMPLOYEE_ID FROM EMPLOYEES WHERE EMAIL"):
            self.result = next(
                (
                    (row["employee_id"],)
                    for row in self.database.rows.values()
                    if row["email"] == values["email"]
                ),
                None,
            )
        elif sql.startswith("SELECT EMPLOYEE_ID, FULL_NAME, EMAIL, POSITION, SALARY"):
            if "WHERE EMPLOYEE_ID = :EMPLOYEE_ID" in sql:
                row = self.database.rows.get(values["employee_id"])
                self.result = self._as_tuple(row) if row is not None else None
            else:
                self.results = [
                    self._as_tuple(row)
                    for _, row in sorted(self.database.rows.items())
                ]
        elif sql.startswith("UPDATE EMPLOYEES"):
            row = self.database.rows.get(values["employee_id"])
            if row is not None:
                row.update(
                    full_name=values["full_name"],
                    email=values["email"],
                    position=values["position"],
                    salary=values["salary"],
                )
                self.rowcount = 1
            else:
                self.rowcount = 0
        elif sql.startswith("DELETE FROM EMPLOYEES"):
            removed = self.database.rows.pop(values["employee_id"], None)
            self.rowcount = int(removed is not None)
        else:
            raise AssertionError(f"Consulta no contemplada por FakeCursor: {sql}")

    def fetchone(self):
        return self.result

    def fetchall(self):
        return self.results

    def close(self) -> None:
        pass

    @staticmethod
    def _as_tuple(row: dict[str, object]) -> tuple[object, ...]:
        return (
            row["employee_id"],
            row["full_name"],
            row["email"],
            row["position"],
            row["salary"],
        )
