from collections.abc import Mapping
from dataclasses import asdict, dataclass
from typing import Any, Literal

from next_station.core.config.settings import settings
from next_station.core.exceptions.api import APIRelatedError


@dataclass(frozen=True)
class APIEndpointConfig:
    method: Literal["GET", "POST", "HEAD"]
    url: str
    payload: str | None = None
    headers: Mapping[str, str] | None = None
    stream: bool = True
    allow_redirects: bool = False
    timeout: int = 60

    def __post_init__(self) -> None:

        method = self.method.upper()
        if method not in settings.api.allowed_methods:
            raise (
                APIRelatedError(
                    f"Method {method} is not supported. Check allowed methods in config."
                )
            )

        if self.timeout < 0:
            raise (
                APIRelatedError(
                    f"Timeout must be a positive integer, got {self.timeout}"
                )
            )

    def get_request_config(self) -> Mapping[str, Any]:
        config = asdict(self)

        if self.payload:
            config["data"] = self.payload
            del config["payload"]

        return config
