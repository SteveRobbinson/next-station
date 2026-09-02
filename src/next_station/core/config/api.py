from collections.abs import Mapping

from pydantic import BaseModel, HttpUrl


class ApiRequestsConfig(BaseModel):
    allowed_methods: set[str] = {"GET", "HEAD", "POST"}

    base_railway_stations_url: HttpUrl
    payload_for_railway_stations: str

    base_population_grid_url: HttpUrl
    user_agent: str
    referer: str

    @property
    def headers(self) -> Mapping[str, str]:
        return {"User-Agent": self.user_agent, "Referer": self.referer}
