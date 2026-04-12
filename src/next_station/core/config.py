from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import PurePosixPath

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    train_stations_url: str
    population_grid_url: str
    query_for_train_stations: str
    absolute_population_grid_path: PurePosixPath
    absolute_railway_stations_path: PurePosixPath
    aws_railway_file_explode_by: str
    absolute_databricks_path: PurePosixPath
    databricks_railway_stations_table: str
    databricks_population_grid_table: str
    databricks_sql_user_name: str
    databricks_python_user_name: str
    aws_s3_protocol: str

settings = Settings()
