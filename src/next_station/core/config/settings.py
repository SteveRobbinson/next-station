from pathlib import Path

from pydantic import BaseModel, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from next_station.core.config.api import ApiRequestsConfig
from next_station.core.config.aws import AWSConfig
from next_station.core.config.databricks import DatabricksConfig

ROOT_DIR = Path(__file__).resolve().parents[4]
ENV_PATH = ROOT_DIR / ".env"


class ExportTask(BaseModel):
    name: str
    databricks_fqn: str
    aws_target_uri: str


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_PATH, env_file_encoding="utf-8", env_nested_delimiter="__"
    )

    databricks: DatabricksConfig
    aws: AWSConfig
    api: ApiRequestsConfig

    @computed_field  # type: ignore[prop-decorator]
    @property
    def export_tasks(self) -> list[ExportTask]:

        return [
            ExportTask(
                name="population_grid",
                databricks_fqn=self.databricks.population_grid_silver_fqn,
                aws_target_uri=self.aws.population_grid_public,
            ),
            ExportTask(
                name="railway_stations",
                databricks_fqn=self.databricks.railway_stations_silver_fqn,
                aws_target_uri=self.aws.railway_stations_public,
            ),
        ]


settings = AppConfig()  # pyright: ignore[reportCallIssue]  #type: ignore
