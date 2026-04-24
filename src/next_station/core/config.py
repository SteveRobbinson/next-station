from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import HttpUrl, BaseModel, computed_field
from enum import Enum


class ComputeMode(str, Enum):
    SQL = 'sql'
    PYTHON = 'python'


class ExportTask(BaseModel):
    name: str
    databricks_fqn: str
    aws_target_uri: str


class DatabricksConfig(BaseModel):
    compute_config: str = 'python-dev'
    catalog: str = 'main'
    schema_bronze: str
    schema_silver: str
    railway_stations_bronze_table: str = 'railway_stations'
    railway_stations_silver_table: str = 'int_railway_stations_h3'
    population_grid_bronze_table: str = 'population_grid'
    population_grid_silver_table: str = 'int_population_grid_h3'

    @computed_field # type: ignore[prop-decorator]
    @property
    def railway_stations_bronze_fqn(self) -> str:
        return f"{self.catalog}.{self.schema_bronze}.{self.railway_stations_bronze_table}"

    @computed_field # type: ignore[prop-decorator]
    @property
    def population_grid_bronze_fqn(self) -> str:
        return f"{self.catalog}.{self.schema_bronze}.{self.population_grid_bronze_table}"

    @computed_field # type: ignore[prop-decorator]
    @property
    def population_grid_silver_fqn(self) -> str:
        return f"{self.catalog}.{self.schema_silver}.{self.population_grid_silver_table}"

    @computed_field # type: ignore[prop-decorator]
    @property
    def railway_stations_silver_fqn(self) -> str:
        return f"{self.catalog}.{self.schema_silver}.{self.railway_stations_silver_table}"


class AWSConfig(BaseModel):
    s3_protocol: str = 's3://'
    s3_bucket_name: str
    s3_railway_stations_file_name: str
    s3_population_grid_file_name: str
    railway_file_explode_by: str = 'elements'

    @property
    @computed_field
    def railway_stations_uri(self) -> str:
        return f"{self.s3_protocol}{self.s3_bucket_name}/{self.s3_railway_stations_file_name}"

    @property
    @computed_field
    def population_grid_uri(self) -> str:
        return f"{self.s3_protocol}{self.s3_bucket_name}/{self.s3_population_grid_file_name}"


class ApiRequestsConfig(BaseModel):
    allowed_methods: set[str] = {'GET', 'HEAD', 'POST'}

    base_railway_stations_url: HttpUrl
    payload_for_railway_stations: str

    base_population_grid_url: HttpUrl


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', env_nested_delimiter='__')
    
    databricks: DatabricksConfig
    aws: AWSConfig
    api: ApiRequestsConfig


    @classmethod
    def load_compute_config(cls, mode: ComputeMode):
        configs = {
                ComputeMode.SQL: 'sql-dev',
                ComputeMode.PYTHON: 'python-dev'
                }

        return cls(databricks={'compute_config': configs[mode]}) # type: ignore

    @computed_field # type: ignore[prop-decorator]
    @property
    def export_tasks(self) -> list[ExportTask]:

        return [
                ExportTask(name = 'population_grid',
                           databricks_fqn = self.databricks.population_grid_silver_fqn,
                           aws_target_uri = self.aws.population_grid_public
                           ),
                ExportTask(name = 'railway_stations',
                           databricks_fqn = self.databricks.railway_stations_silver_fqn,
                           aws_target_uri = self.aws.railway_stations_public)
                ]

settings = AppConfig() # type: ignore
