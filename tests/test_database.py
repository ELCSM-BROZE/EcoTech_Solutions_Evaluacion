import pytest

from app.database import Database


class FakeOracleCursor:
    def __init__(self, table_exists: bool = False) -> None:
        self.table_exists = table_exists
        self.statements: list[str] = []
        self.closed = False

    def execute(self, statement: str, parameters=None) -> None:
        self.statements.append(" ".join(statement.split()))

    def fetchone(self):
        return ("EMPLOYEES",) if self.table_exists else None

    def close(self) -> None:
        self.closed = True


class FakeOracleConnection:
    def __init__(self, cursor: FakeOracleCursor | None = None) -> None:
        self.fake_cursor = cursor or FakeOracleCursor()
        self.commits = 0
        self.rollbacks = 0
        self.closed = False

    def cursor(self) -> FakeOracleCursor:
        return self.fake_cursor

    def commit(self) -> None:
        self.commits += 1

    def rollback(self) -> None:
        self.rollbacks += 1

    def close(self) -> None:
        self.closed = True


def test_connection_uses_oracle_credentials_and_commits(monkeypatch) -> None:
    connection = FakeOracleConnection()
    received = {}

    def fake_connect(**kwargs):
        received.update(kwargs)
        return connection

    monkeypatch.setattr("app.database.oracledb.connect", fake_connect)
    database = Database(user="student", password="secret", dsn="localhost:1521/FREEPDB1")

    with database.connection() as opened:
        assert opened is connection

    assert received == {
        "user": "student",
        "password": "secret",
        "dsn": "localhost:1521/FREEPDB1",
    }
    assert connection.commits == 1
    assert connection.rollbacks == 0
    assert connection.closed


def test_connection_rolls_back_and_closes_after_error(monkeypatch) -> None:
    connection = FakeOracleConnection()
    monkeypatch.setattr("app.database.oracledb.connect", lambda **_kwargs: connection)
    database = Database(user="student", password="secret", dsn="localhost:1521/FREEPDB1")

    with pytest.raises(RuntimeError, match="failure"):
        with database.connection():
            raise RuntimeError("failure")

    assert connection.commits == 0
    assert connection.rollbacks == 1
    assert connection.closed


def test_missing_credentials_fail_before_connect(monkeypatch) -> None:
    def unexpected_connect(**_kwargs):
        raise AssertionError("No debe intentar conectar sin configuración.")

    monkeypatch.setattr("app.database.oracledb.connect", unexpected_connect)
    database = Database(user="", password="secret", dsn="localhost:1521/FREEPDB1")

    with pytest.raises(ValueError, match="ORACLE_USER"):
        with database.connection():
            pass


def test_initialize_creates_table_only_when_missing(monkeypatch) -> None:
    connection = FakeOracleConnection()
    monkeypatch.setattr("app.database.oracledb.connect", lambda **_kwargs: connection)
    database = Database(user="student", password="secret", dsn="localhost:1521/FREEPDB1")

    database.initialize()

    assert any("CREATE TABLE employees" in sql for sql in connection.fake_cursor.statements)
    assert connection.fake_cursor.closed
    assert connection.commits == 1


def test_initialize_does_not_recreate_existing_table(monkeypatch) -> None:
    cursor = FakeOracleCursor(table_exists=True)
    connection = FakeOracleConnection(cursor)
    monkeypatch.setattr("app.database.oracledb.connect", lambda **_kwargs: connection)
    database = Database(user="student", password="secret", dsn="localhost:1521/FREEPDB1")

    database.initialize()

    assert len(cursor.statements) == 1
    assert "CREATE TABLE" not in cursor.statements[0]
    assert cursor.closed
    assert connection.commits == 1
