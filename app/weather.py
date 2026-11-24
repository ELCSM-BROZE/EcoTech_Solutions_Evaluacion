"""Consulta del clima actual usando WeatherAPI.com."""

from dataclasses import dataclass
import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from dotenv import load_dotenv


class WeatherAPIError(Exception):
    """Error de configuración, conexión o respuesta de WeatherAPI."""


@dataclass(frozen=True)
class CurrentWeather:
    location: str
    region: str
    country: str
    local_time: str
    condition: str
    temperature_c: float
    feels_like_c: float
    humidity: int


class WeatherAPI:
    """Cliente pequeño para el endpoint de clima actual de WeatherAPI."""

    endpoint = "https://api.weatherapi.com/v1/current.json"

    def __init__(self) -> None:
        load_dotenv()
        self.api_key = os.getenv("WEATHERAPI_API_KEY")
        if not self.api_key:
            raise WeatherAPIError(
                "Configura WEATHERAPI_API_KEY en el archivo .env."
            )
        self.default_city = os.getenv("WEATHERAPI_DEFAULT_CITY") or "Santiago, Colina"

    def current(self, city: str) -> CurrentWeather:
        if not city.strip():
            raise ValueError("La ciudad no puede estar vacía.")

        query = urlencode({"key": self.api_key, "q": city, "lang": "es"})
        request = Request(
            f"{self.endpoint}?{query}",
            headers={"Accept": "application/json"},
        )
        try:
            with urlopen(request, timeout=10) as response:
                data = json.load(response)
        except HTTPError as error:
            message = self._api_error_message(error)
            raise WeatherAPIError(message) from None
        except (URLError, TimeoutError):
            raise WeatherAPIError("No se pudo conectar con WeatherAPI.") from None
        except (json.JSONDecodeError, UnicodeDecodeError):
            raise WeatherAPIError("WeatherAPI devolvió una respuesta inválida.") from None

        if not isinstance(data, dict):
            raise WeatherAPIError("WeatherAPI devolvió una respuesta inválida.")

        try:
            location = data["location"]
            current = data["current"]
            condition = current["condition"]
            if not all(
                isinstance(value, dict)
                for value in (location, current, condition)
            ):
                raise TypeError
            return CurrentWeather(
                location=self._text(location, "name"),
                region=self._text(location, "region"),
                country=self._text(location, "country"),
                local_time=self._text(location, "localtime"),
                condition=self._text(condition, "text"),
                temperature_c=self._number(current, "temp_c"),
                feels_like_c=self._number(current, "feelslike_c"),
                humidity=self._integer(current, "humidity"),
            )
        except (KeyError, TypeError, ValueError):
            raise WeatherAPIError("WeatherAPI devolvió datos incompletos.") from None

    @staticmethod
    def _text(data: dict[str, object], key: str) -> str:
        value = data[key]
        if not isinstance(value, str):
            raise TypeError
        return value

    @staticmethod
    def _number(data: dict[str, object], key: str) -> float:
        value = data[key]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError
        return float(value)

    @staticmethod
    def _integer(data: dict[str, object], key: str) -> int:
        value = data[key]
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError
        return value

    @staticmethod
    def _api_error_message(error: HTTPError) -> str:
        try:
            data = json.load(error)
            message = data["error"]["message"]
            if isinstance(message, str):
                return f"WeatherAPI: {message}"
        except (json.JSONDecodeError, KeyError, TypeError, UnicodeDecodeError):
            pass
        return f"WeatherAPI devolvió el error HTTP {error.code}."
