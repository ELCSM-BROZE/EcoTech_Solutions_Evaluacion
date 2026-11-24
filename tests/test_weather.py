import io
import json
from urllib.error import HTTPError
from urllib.parse import parse_qs, urlparse

import pytest

from app import weather


class FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *_args):
        self.close()


def test_current_weather_parses_api_response_and_uses_requested_city(monkeypatch) -> None:
    monkeypatch.setenv("WEATHERAPI_API_KEY", "test-key")
    response_data = {
        "location": {
            "name": "Colina",
            "region": "Santiago",
            "country": "Chile",
            "localtime": "2026-11-23 20:00",
        },
        "current": {
            "condition": {"text": "Soleado"},
            "temp_c": 22.5,
            "feelslike_c": 23.0,
            "humidity": 40,
        },
    }
    request_data = {}

    def fake_urlopen(request, timeout):
        request_data["url"] = request.full_url
        request_data["timeout"] = timeout
        return FakeResponse(json.dumps(response_data).encode())

    monkeypatch.setattr(weather, "urlopen", fake_urlopen)
    service = weather.WeatherAPI()

    result = service.current("Colina, Chile")

    query = parse_qs(urlparse(request_data["url"]).query)
    assert query == {"key": ["test-key"], "q": ["Colina, Chile"], "lang": ["es"]}
    assert request_data["timeout"] == 10
    assert result.location == "Colina"
    assert result.condition == "Soleado"
    assert result.temperature_c == 22.5
    assert result.humidity == 40


def test_missing_api_key_is_reported(monkeypatch) -> None:
    monkeypatch.delenv("WEATHERAPI_API_KEY", raising=False)
    monkeypatch.setattr(weather, "load_dotenv", lambda: None)

    with pytest.raises(weather.WeatherAPIError, match="WEATHERAPI_API_KEY"):
        weather.WeatherAPI()


def test_api_error_message_does_not_expose_key(monkeypatch) -> None:
    api_key = "private-test-key"
    monkeypatch.setenv("WEATHERAPI_API_KEY", api_key)

    def fail_request(request, timeout):
        raise HTTPError(
            request.full_url,
            401,
            "Unauthorized",
            None,
            io.BytesIO(b'{"error":{"message":"API key is invalid"}}'),
        )

    monkeypatch.setattr(weather, "urlopen", fail_request)
    service = weather.WeatherAPI()

    with pytest.raises(weather.WeatherAPIError, match="API key is invalid") as error:
        service.current("Colina")

    assert api_key not in str(error.value)
