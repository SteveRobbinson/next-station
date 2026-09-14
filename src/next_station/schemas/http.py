from collections.abc import Mapping
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, HttpUrl, PositiveInt


class APIEndpointConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    method: Literal["GET", "POST", "HEAD"]
    url: HttpUrl | str
    data: str | None = None
    headers: Mapping[str, str] | None = None
    stream: bool = True
    allow_redirects: bool = False
    timeout: PositiveInt = 60

    def get_request_config(self) -> Mapping[str, Any]:
        return self.model_dump(mode="json", exclude_none=True)
