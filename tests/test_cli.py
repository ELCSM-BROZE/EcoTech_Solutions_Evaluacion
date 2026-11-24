from app import __main__ as cli
from app.weather import CurrentWeather
from tests.fakes import FakeDatabase


def test_invalid_salary_returns_to_menu(monkeypatch, capsys) -> None:
    database = FakeDatabase()
    monkeypatch.setattr(cli, "Database", lambda: database)
    answers = iter(["1", "Ana Pérez", "ana@example.com", "Analista", "no-numérico", "0"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))

    assert cli.main() == 0

    output = capsys.readouterr().out
    assert "Entrada no válida" in output
    assert "Hasta luego." in output
    assert database.rows == {}


def test_end_of_input_exits_cleanly(monkeypatch, capsys) -> None:
    database = FakeDatabase()
    monkeypatch.setattr(cli, "Database", lambda: database)
    monkeypatch.setattr("builtins.input", lambda _prompt: (_ for _ in ()).throw(EOFError))

    assert cli.main() == 0
    assert "Entrada finalizada" in capsys.readouterr().out


def test_non_positive_id_is_rejected(monkeypatch) -> None:
    monkeypatch.setattr("builtins.input", lambda _prompt: "0")

    try:
        cli._read_positive_id("ID: ")
    except ValueError as error:
        assert "entero positivo" in str(error)
    else:
        raise AssertionError("El ID cero debió ser rechazado.")


def test_complete_crud_flow_from_console(monkeypatch, capsys) -> None:
    database = FakeDatabase()
    monkeypatch.setattr(cli, "Database", lambda: database)
    answers = iter(
        [
            "1", "Ana Pérez", "ana@example.com", "Analista", "1200",
            "2",
            "3", "1",
            "4", "1", "Ana Rojas", "ana@example.com", "Senior", "1500",
            "2",
            "5", "1",
            "2",
            "0",
        ]
    )
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))

    assert cli.main() == 0

    output = capsys.readouterr().out
    assert "Empleado registrado con ID 1." in output
    assert "ID: 1 | Ana Pérez | ana@example.com | Analista | Sueldo: 1200.00" in output
    assert "Empleado actualizado." in output
    assert "ID: 1 | Ana Rojas | ana@example.com | Senior | Sueldo: 1500.00" in output
    assert "Empleado eliminado." in output
    assert "No hay empleados registrados." in output
    assert database.rows == {}


def test_weather_can_be_queried_when_oracle_is_unavailable(
    monkeypatch, capsys
) -> None:
    class UnavailableDatabase:
        def initialize(self) -> None:
            raise ValueError("Configura Oracle para usar el CRUD.")

    class FakeWeatherAPI:
        default_city = "Santiago, Colina"

        def current(self, city: str) -> CurrentWeather:
            assert city == "Santiago, Colina"
            return CurrentWeather(
                location="Colina",
                region="Santiago",
                country="Chile",
                local_time="2026-11-23 20:00",
                condition="Soleado",
                temperature_c=22.5,
                feels_like_c=23.0,
                humidity=40,
            )

    monkeypatch.setattr(cli, "Database", UnavailableDatabase)
    monkeypatch.setattr(cli, "WeatherAPI", FakeWeatherAPI)
    answers = iter(["2", "6", "", "0"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))

    assert cli.main() == 0

    output = capsys.readouterr()
    assert "Oracle no está disponible" in output.err
    assert "requieren una conexión Oracle" in output.out
    assert "Entrada no válida" not in output.out
    assert "Clima actual en Colina, Santiago, Chile" in output.out
    assert "Soleado, 22.5 °C" in output.out
